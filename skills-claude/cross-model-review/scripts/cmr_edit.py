"""Produce the next candidate from a base and an ordered list of exact-text edits.

Pure text work: no round state is read, no lock is taken, no model is
called, and ``checked`` never advances. Exactly two files are written, both
write-once and both directly inside the review's ``host/`` directory: the
new candidate and a receipt recording how it was produced.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cmr_archive import Archive, RecordError, fail, read_text

SEMANTICS = 1
OPERATION = "edit candidate"
HEX_DIGITS = frozenset("0123456789abcdef")
EDIT_KEYS = frozenset({"label", "old", "new"})
Leftover = tuple[str, OSError] | None


@dataclass(frozen=True)
class Plan:
    """Everything publication needs, fixed in memory before any write."""

    host: Path
    out: Path
    receipt: Path
    candidate_bytes: bytes
    receipt_bytes: bytes
    result: dict[str, Any]


def apply_edits(
    archive: Archive, base: str, edits: str, out: str, expect_sha: str | None
) -> dict[str, Any]:
    """Write ``out`` and its receipt from ``base`` and the edits file.

    Args:
        archive: The review whose ``host/`` directory receives the output.
        base: The ``--from`` argument as typed: a ``drafts/`` reference or a
            filesystem path.
        edits: The ``--edits`` argument as typed, a filesystem path.
        out: The ``--out`` argument as typed, a filesystem path.
        expect_sha: The ``--expect-sha`` argument, or ``None``.

    Returns:
        The result object the command prints.
    """
    return _publish(_prepare(archive, base, edits, out, expect_sha))


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _encodable(value: str) -> bool:
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _check_arguments(base: str, edits: str, out: str) -> None:
    for argument in (base, edits, out):
        if not _encodable(argument):
            fail(OPERATION, "argument is not encodable as UTF-8", argument)


def _host_directory(archive: Archive) -> Path:
    host = archive.root / "host"
    if os.path.islink(host) or not host.is_dir():
        fail(OPERATION, "host directory must exist and not be a symlink", str(host))
    return host


def _output_paths(host: Path, raw: str) -> tuple[Path, Path]:
    """Apply the containment rules to the ``--out`` string as typed."""
    name = raw.rsplit(os.sep, 1)[-1]
    if raw.endswith(os.sep) or name in ("", ".", ".."):
        fail(OPERATION, "output must name a file", raw)
    supplied = Path(raw)
    parent = supplied.parent.resolve()
    if parent != host:
        fail(
            OPERATION,
            "output must be directly inside the review's host directory",
            raw,
        )
    out = parent / supplied.name
    if os.path.lexists(out):
        fail(OPERATION, "output already exists", str(out))
    receipt = out.with_name(out.name + ".receipt.json")
    if os.path.lexists(receipt):
        fail(OPERATION, "receipt path already exists", str(receipt))
    return out, receipt


def _expected_digest(base: str, expect_sha: str | None) -> tuple[bool, str]:
    """Classify ``--from`` and settle the digest the base must have."""
    is_reference = base.startswith("drafts/")
    if not is_reference and expect_sha is None:
        fail(OPERATION, "expected sha256 is required for a filesystem path base", base)
    if expect_sha is not None and (
        len(expect_sha) != 64 or not all(char in HEX_DIGITS for char in expect_sha)
    ):
        fail(OPERATION, "expected sha256 must be 64 lowercase hex digits", expect_sha)
    if not is_reference:
        assert expect_sha is not None
        return False, expect_sha
    stem = Path(base).stem
    if expect_sha is not None and expect_sha != stem:
        fail(
            OPERATION, "expected sha256 disagrees with the drafts reference", expect_sha
        )
    return True, stem


def _parse_edits(text: str, raw: str) -> list[dict[str, str]]:
    """Parse the edits file; every string is checked for UTF-8 encodability."""
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        fail(OPERATION, f"invalid edits file: {exc}", raw)
    if not isinstance(value, list):
        fail(OPERATION, "invalid edits file: top level must be an array", raw)
    if not value:
        fail(OPERATION, "invalid edits file: no edits", raw)
    parsed: list[dict[str, str]] = []
    for index, item in enumerate(value, 1):
        if not isinstance(item, dict):
            fail(OPERATION, f"invalid edits file: item {index} is not an object", item)
        if not isinstance(item.get("old"), str) or not isinstance(item.get("new"), str):
            fail(
                OPERATION,
                f"invalid edits file: item {index} needs string old and new",
                item,
            )
        unknown = sorted(set(item) - EDIT_KEYS)
        if unknown:
            fail(
                OPERATION,
                f"invalid edits file: item {index} has unknown key {unknown[0]}",
                item,
            )
        if "label" in item and not isinstance(item["label"], str):
            fail(
                OPERATION,
                f"invalid edits file: item {index} label must be a string",
                item,
            )
        if item["old"] == "":
            fail(OPERATION, f"invalid edits file: item {index} has empty old", item)
        for field in ("label", "old", "new"):
            if field in item and not _encodable(item[field]):
                fail(
                    OPERATION,
                    f"invalid edits file: item {index} {field} is not encodable as UTF-8",
                    item,
                )
        edit: dict[str, str] = {"label": item["label"]} if "label" in item else {}
        edit["old"] = item["old"]
        edit["new"] = item["new"]
        parsed.append(edit)
    return parsed


def _occurrences(text: str, needle: str) -> int:
    """Count start positions of ``needle`` in ``text``, overlapping included."""
    count = 0
    start = text.find(needle)
    while start >= 0:
        count += 1
        start = text.find(needle, start + 1)
    return count


def _apply(text: str, edits: list[dict[str, str]]) -> str:
    """Apply the edits in order; each must match exactly once as the text stands."""
    for index, edit in enumerate(edits, 1):
        count = _occurrences(text, edit["old"])
        if count != 1:
            label = f" ({edit['label']})" if "label" in edit else ""
            fail(
                OPERATION,
                f"edit {index}{label} matched {count} times, not once",
                edit["old"],
            )
        text = text.replace(edit["old"], edit["new"], 1)
    return text


def _prepare(
    archive: Archive, base: str, edits: str, out: str, expect_sha: str | None
) -> Plan:
    """Validate, read, apply, and serialize; nothing is written."""
    _check_arguments(base, edits, out)
    host = _host_directory(archive)
    out_path, receipt_path = _output_paths(host, out)
    is_reference, expected = _expected_digest(base, expect_sha)
    base_path = archive.path(base) if is_reference else Path(base).resolve()
    if out_path == base_path:
        fail(OPERATION, "output must differ from the base", str(out_path))
    base_text = archive.text(base) if is_reference else read_text(base_path)
    base_digest = _digest(base_text.encode("utf-8"))
    if base_digest != expected:
        fail(OPERATION, f"base sha256 is {base_digest}, expected {expected}", base)
    edits_path = Path(edits).resolve()
    edits_text = read_text(edits_path)
    edit_list = _parse_edits(edits_text, edits)
    text = _apply(base_text, edit_list)
    candidate_bytes = text.encode("utf-8")
    digest = _digest(candidate_bytes)
    receipt = {
        "semantics": SEMANTICS,
        "base": {"argument": base, "path": str(base_path), "sha256": base_digest},
        "edits_file": {
            "argument": edits,
            "path": str(edits_path),
            "sha256": _digest(edits_text.encode("utf-8")),
        },
        "edits": edit_list,
        "out": {"path": str(out_path), "sha256": digest},
    }
    receipt_bytes = (json.dumps(receipt, indent=2, ensure_ascii=False) + "\n").encode(
        "utf-8"
    )
    result = {
        "out": str(out_path),
        "receipt": str(receipt_path),
        "base_sha256": base_digest,
        "sha256": digest,
        "edits_applied": len(edit_list),
        "lines": len(text.splitlines()),
    }
    return Plan(host, out_path, receipt_path, candidate_bytes, receipt_bytes, result)


def _remove(temporary: str | None) -> Leftover:
    """Remove a temporary; report it when removal fails."""
    if temporary is None:
        return None
    try:
        os.unlink(temporary)
    except OSError as exc:
        return temporary, exc
    return None


def _link_once(
    host: Path, data: bytes, destination: Path
) -> tuple[str, OSError | None, Leftover]:
    """Write ``data`` to a temporary in ``host`` and hard-link it at ``destination``.

    Returns ``(outcome, error, leftover)``. ``outcome`` is ``"linked"`` when
    ``destination`` now holds ``data``, ``"exists"`` when another process
    created ``destination`` first, and ``"failed"`` when nothing reached
    ``destination``. ``error`` is the ``OSError`` behind ``"exists"`` or
    ``"failed"``. ``leftover`` names a temporary that could not be removed.
    """
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=host, prefix="edit-", suffix=".tmp", delete=False
        ) as stream:
            temporary = stream.name
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    except OSError as exc:
        return "failed", exc, _remove(temporary)
    try:
        os.link(temporary, destination)
    except FileExistsError as exc:
        return "exists", exc, _remove(temporary)
    except OSError as exc:
        return "failed", exc, _remove(temporary)
    try:
        os.unlink(temporary)
    except OSError as exc:
        return "linked", None, (temporary, exc)
    return "linked", None, None


def _suffix(leftover: Leftover) -> str:
    if leftover is None:
        return ""
    return f"; temporary left at {leftover[0]}: {leftover[1]}"


def _publish(plan: Plan) -> dict[str, Any]:
    """Publish the candidate, then the receipt, each write-once."""
    outcome, error, leftover = _link_once(plan.host, plan.candidate_bytes, plan.out)
    if outcome == "failed":
        fail(
            "publish candidate",
            f"nothing published; {error}{_suffix(leftover)}",
            str(plan.out),
            RecordError,
        )
    if outcome == "exists":
        fail(
            "publish candidate",
            "nothing published by this invocation; output now exists, created "
            f"concurrently; {error}{_suffix(leftover)}",
            str(plan.out),
            RecordError,
        )
    if leftover is not None:
        fail(
            "publish candidate",
            f"candidate published at {plan.out}; receipt not attempted; "
            f"temporary left at {leftover[0]}: {leftover[1]}",
            str(plan.out),
            RecordError,
        )
    outcome, error, leftover = _link_once(plan.host, plan.receipt_bytes, plan.receipt)
    if outcome == "failed":
        fail(
            "write receipt",
            f"candidate published at {plan.out}; receipt not written; {error}"
            f"{_suffix(leftover)}",
            str(plan.receipt),
            RecordError,
        )
    if outcome == "exists":
        fail(
            "write receipt",
            f"candidate published at {plan.out}; receipt not written by this "
            "invocation; receipt path now exists, created concurrently; "
            f"{error}{_suffix(leftover)}",
            str(plan.receipt),
            RecordError,
        )
    if leftover is not None:
        fail(
            "write receipt",
            f"candidate and receipt published; temporary left at {leftover[0]}: "
            f"{leftover[1]}",
            str(plan.receipt),
            RecordError,
        )
    return plan.result
