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

Exit codes mirror the anydoc CLI: 0 done; 1 the document could not be read or
parsed (PDF included, since PDFs have no document model); 2 usage error;
3 pages need OCR.
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
EXIT_NEEDS_OCR = 3


def detect_format(data: bytes, path: Path, explicit: str | None) -> str:
    """Return the format to parse with.

    Args:
        data: The document bytes.
        path: The document path, used as the extension fallback.
        explicit: A format name given on the command line, or ``None``.

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

    Image subtypes become the extension as written (``png``, ``jpeg``, ``svgxml``);
    every non-image type becomes ``bin``.

    Args:
        media_type: The asset's MIME type, for example ``image/png``.

    Returns:
        A short extension without a leading dot.
    """
    kind, _, subtype = media_type.partition("/")
    if kind != "image":
        return "bin"
    cleaned = re.sub(r"[^a-z0-9]", "", subtype.lower())
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


def main(argv: list[str] | None = None) -> int:
    """Parse the document, write its assets and model, and print a summary."""
    parser = argparse.ArgumentParser(
        prog="anydoc_extract",
        description="Write a document's embedded assets and document model to a directory.",
    )
    parser.add_argument("file", type=Path, help="the document to parse")
    parser.add_argument(
        "outdir", type=Path, help="directory for assets/ and document.json"
    )
    parser.add_argument(
        "--format",
        dest="format_name",
        default=None,
        help="name the input format instead of detecting it; needed only when the "
        "extension is missing or wrong (csv has no content signature)",
    )
    args = parser.parse_args(argv)

    try:
        data = args.file.read_bytes()
        format_name = detect_format(data, args.file, args.format_name)
        if format_name == "pdf":
            raise anydoc.UnsupportedError(
                "PDF has no document model; use the Markdown path (the anydoc CLI)"
            )
        document = anydoc.to_document(data, format_name)
    except anydoc.NeedsOcrError as error:
        return fail(EXIT_NEEDS_OCR, str(error))
    except (anydoc.ConvertError, OSError, ValueError) as error:
        return fail(EXIT_CONVERSION_ERROR, str(error))

    args.outdir.mkdir(parents=True, exist_ok=True)
    assets_dir = args.outdir / "assets"
    asset_paths: dict[int, str] = {}
    if document.assets:
        assets_dir.mkdir(exist_ok=True)
    for asset in document.assets:
        extension = asset_extension(asset.media_type)
        target = assets_dir / f"{args.file.stem}-{asset.id}.{extension}"
        target.write_bytes(asset.data)
        asset_paths[asset.id] = str(target.relative_to(args.outdir))

    model_path = args.outdir / "document.json"
    model = to_plain(document, asset_paths)
    model_path.write_text(
        json.dumps(model, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )

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
