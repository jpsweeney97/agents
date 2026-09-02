#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["firecrawl-anydoc==0.2.4"]
# ///
"""Write a document's embedded assets and its document model to a directory.

Companion to the ``document-to-markdown`` skill. The Markdown path (the anydoc
CLI) renders embedded images as alt text only and flattens some structure.
This script uses the anydoc Python library, pinned to the same version, to
write every embedded asset as a file and the whole document model as JSON.
Everything runs locally: ``to_document`` has no network path at all.

Usage::

    anydoc_extract.py <file> <outdir> [--format NAME]

``<outdir>`` must not exist yet or must be empty, so one run never mixes its
assets with another document's. ``--format`` takes one of anydoc's twelve
format names or an extension alias (``xls``, ``docm``, ``ppsx``); it is needed
only for delimited text (``csv``), which carries no content signature.

Exit codes: 0 done; 1 the document could not be read or parsed (PDF included,
since PDFs have no document model) or an output file could not be written;
2 usage error (missing arguments, an unknown format name, an output path that
is not a directory, or a non-empty output directory). The script never exits
3: a PDF is refused before parsing, so anydoc's OCR check never runs here.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import anydoc

EXIT_CONVERSION_ERROR = 1
EXIT_USAGE_ERROR = 2
FORMATS = (
    "doc",
    "docx",
    "odt",
    "pdf",
    "ppt",
    "pptx",
    "rtf",
    "epub",
    "xlsx",
    "ods",
    "odp",
    "csv",
)


def format_name(value: str) -> str:
    """Resolve a ``--format`` argument to one of anydoc's format names.

    Args:
        value: A format name or an extension alias, with or without a dot.

    Returns:
        The canonical anydoc format name.

    Raises:
        argparse.ArgumentTypeError: When the value names no known format, so
            argparse reports a usage error and exits 2.
    """
    resolved = anydoc.format_from_extension(value)
    if resolved is None:
        raise argparse.ArgumentTypeError(
            f"unknown format {value!r}; expected one of {', '.join(FORMATS)} "
            "or an extension alias such as xls, docm, ppsx"
        )
    return resolved


def detect_format(data: bytes, path: Path, explicit: str | None) -> str:
    """Return the format to parse with.

    Args:
        data: The document bytes.
        path: The document path, used as the extension fallback.
        explicit: A canonical format name given on the command line, or ``None``.

    Returns:
        The anydoc format name.

    Raises:
        ValueError: When neither the content nor the extension names a format.
    """
    if explicit:
        return explicit
    detected = anydoc.format_from_bytes(data) or anydoc.format_from_path(path)
    if detected is None:
        raise ValueError(
            "format detection failed: unrecognized content and extension. "
            f"Got: {str(path)!r:.100}"
        )
    return detected


def asset_extension(media_type: str) -> str:
    """Map a MIME type to a file extension.

    Image subtypes become the extension with any structured-syntax suffix
    dropped (``image/png`` gives ``png``, ``image/jpeg`` gives ``jpeg``,
    ``image/svg+xml`` gives ``svg``); every non-image type becomes ``bin``.

    Args:
        media_type: The asset's MIME type, for example ``image/png``.

    Returns:
        A short extension without a leading dot.
    """
    kind, _, subtype = media_type.partition("/")
    if kind != "image":
        return "bin"
    cleaned = re.sub(r"[^a-z0-9]", "", subtype.lower().split("+", 1)[0])
    return cleaned or "bin"


def to_plain(value: Any, asset_paths: dict[int, str]) -> Any:
    """Convert anydoc model objects into JSON-ready values.

    Unset (``None``) fields are dropped so each object shows only the fields its
    ``kind`` uses. Asset bytes are never inlined; an asset carries the path it
    was written to instead.

    Args:
        value: A model object, list, scalar, or bytes.
        asset_paths: Written asset paths by asset id, relative to the output directory.

    Returns:
        A value ``json.dumps`` accepts.
    """
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, bytes):
        return {"bytes": len(value)}
    if isinstance(value, list):
        return [to_plain(item, asset_paths) for item in value]
    if isinstance(value, anydoc.Asset):
        return {
            "id": value.id,
            "media_type": value.media_type,
            "origin_part": value.origin_part,
            "bytes": len(value.data),
            "path": asset_paths[value.id],
        }
    names = [
        name
        for name in dir(value)
        if not name.startswith("_") and not callable(getattr(value, name))
    ]
    names.sort(key=lambda name: (name != "kind", name))
    plain = {name: to_plain(getattr(value, name), asset_paths) for name in names}
    return {name: field for name, field in plain.items() if field is not None}


def fail(code: int, message: str) -> int:
    """Print one diagnostic line to stderr and return the exit code."""
    print(f"anydoc-extract: {message}", file=sys.stderr)
    return code


def write_outputs(
    document: anydoc.Document, source: Path, outdir: Path
) -> tuple[Path, dict[int, str]]:
    """Write the assets and ``document.json`` under ``outdir``.

    Args:
        document: The parsed document model.
        source: The source file; its full name prefixes every asset name.
        outdir: The output directory, created if missing.

    Returns:
        The path of ``document.json`` and the written asset paths by asset id,
        relative to ``outdir``.

    Raises:
        OSError: When a directory or file could not be created or written.
    """
    outdir.mkdir(parents=True, exist_ok=True)
    assets_dir = outdir / "assets"
    asset_paths: dict[int, str] = {}
    if document.assets:
        assets_dir.mkdir(exist_ok=True)
    for asset in document.assets:
        extension = asset_extension(asset.media_type)
        target = assets_dir / f"{source.name}-{asset.id}.{extension}"
        target.write_bytes(asset.data)
        asset_paths[asset.id] = str(target.relative_to(outdir))
    model_path = outdir / "document.json"
    model = to_plain(document, asset_paths)
    model_path.write_text(
        json.dumps(model, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return model_path, asset_paths


def main(argv: list[str] | None = None) -> int:
    """Parse the document, write its assets and model, and print a summary."""
    parser = argparse.ArgumentParser(
        prog="anydoc_extract",
        description="Write a document's embedded assets and document model to a directory.",
    )
    parser.add_argument("file", type=Path, help="the document to parse")
    parser.add_argument(
        "outdir",
        type=Path,
        help="directory for assets/ and document.json; must be new or empty",
    )
    parser.add_argument(
        "--format",
        dest="format_name",
        type=format_name,
        default=None,
        help="name the input format instead of detecting it: one of "
        f"{', '.join(FORMATS)} or an extension alias; needed only for delimited "
        "text (csv has no content signature)",
    )
    args = parser.parse_args(argv)

    if args.outdir.exists():
        if not args.outdir.is_dir():
            return fail(
                EXIT_USAGE_ERROR,
                f"output path is not a directory. Got: {str(args.outdir)!r:.100}",
            )
        if any(args.outdir.iterdir()):
            return fail(
                EXIT_USAGE_ERROR,
                "output directory is not empty; give each run its own directory. "
                f"Got: {str(args.outdir)!r:.100}",
            )

    try:
        data = args.file.read_bytes()
        fmt = detect_format(data, args.file, args.format_name)
        if fmt == "pdf":
            raise anydoc.UnsupportedError(
                "PDF has no document model; use the Markdown path (the anydoc CLI)"
            )
        document = anydoc.to_document(data, fmt)
    except (anydoc.ConvertError, OSError, ValueError) as error:
        return fail(EXIT_CONVERSION_ERROR, str(error))

    try:
        model_path, asset_paths = write_outputs(document, args.file, args.outdir)
    except OSError as error:
        return fail(EXIT_CONVERSION_ERROR, f"writing the output failed: {error}")

    kinds = Counter(block.kind for block in document.blocks)
    kind_summary = ", ".join(f"{kind}={count}" for kind, count in sorted(kinds.items()))
    print(f"document.json: {model_path}")
    print(f"top-level blocks: {kind_summary or 'none'}")
    print(f"notes: {len(document.notes)}  assets: {len(document.assets)}")
    for asset in document.assets:
        size = len(asset.data)
        print(
            f"asset {asset.id}: {asset.media_type} {size} bytes -> {asset_paths[asset.id]}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
