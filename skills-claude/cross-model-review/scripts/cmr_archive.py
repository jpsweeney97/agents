"""Local records for one review; no model calls or semantic judgments."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, NoReturn


class ReviewError(Exception):
    """A review operation could not be completed faithfully."""


class RecordError(ReviewError):
    """A local record could not be written; saved work stays resumable."""


def fail(
    operation: str,
    reason: str,
    got: object,
    error: type[ReviewError] = ReviewError,
) -> NoReturn:
    """Raise the repository's explicit operation diagnostic."""
    raise error(f"{operation} failed: {reason}. Got: {got!r:.100}")


def read_text(path: Path) -> str:
    """Read a UTF-8 input without changing it."""
    try:
        return path.read_bytes().decode("utf-8")
    except (OSError, UnicodeError) as exc:
        fail("read input", str(exc), str(path))


class Archive:
    """Files for a review; mutable progress is separate from original records."""

    def __init__(self, root: Path) -> None:
        self.root = root.expanduser().resolve()

    @classmethod
    def create(cls, root: Path, repo: Path, source: Path, limit: int) -> Archive:
        """Snapshot a source into a new external review directory."""
        root, repo, source = (
            root.expanduser().resolve(),
            repo.expanduser().resolve(),
            source.expanduser().resolve(),
        )
        if not repo.is_dir() or root.is_relative_to(repo):
            fail("create review", "review must be outside the target directory", root)
        if type(limit) is not int or limit < 1:
            fail("create review", "round allowance must be positive", limit)
        text = read_text(source)
        try:
            root.mkdir(mode=0o700, parents=True, exist_ok=False)
            (root / "drafts").mkdir()
        except OSError as exc:
            fail("create review", str(exc), root)
        archive = cls(root)
        original = archive.snapshot_text(text)
        archive.save(
            {
                "format": 1,
                "repo": str(repo),
                "source": str(source),
                "original": original,
                "limit": limit,
                "used": 0,
                "phase": "between",
                "session": None,
                "call": None,
                "last_response": None,
                "checked": None,
                "checked_response": None,
                "error": None,
                "extensions": [],
                "continuations": [],
            }
        )
        return archive

    def path(self, name: str) -> Path:
        """Resolve an archive-local reference, refusing external paths."""
        path = (self.root / name).resolve()
        if not path.is_relative_to(self.root):
            fail("resolve record", "record is outside review directory", name)
        return path

    def text(self, name: str) -> str:
        """Read an archive-local text record."""
        text = read_text(self.path(name))
        if name.startswith("drafts/"):
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            if self.path(name).stem != digest:
                fail("read candidate", "saved candidate content changed", name)
        return text

    def read(self, name: str) -> dict[str, Any]:
        """Read one JSON object; malformed records remain errors."""
        try:
            value = json.loads(self.text(name))
        except json.JSONDecodeError as exc:
            fail("read record", str(exc), name)
        if not isinstance(value, dict):
            fail("read record", "expected a JSON object", name)
        return value

    def write(self, name: str, value: dict[str, Any]) -> None:
        """Create an original record without replacing an earlier one."""
        try:
            with self.path(name).open("x", encoding="utf-8") as stream:
                json.dump(value, stream, indent=2, ensure_ascii=False)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
        except OSError as exc:
            fail("write record", str(exc), name, RecordError)

    def snapshot_text(self, text: str) -> str:
        """Save exact candidate bytes under their content digest."""
        data = text.encode("utf-8")
        name = f"drafts/{hashlib.sha256(data).hexdigest()}.md"
        path = self.path(name)
        try:
            if path.exists():
                if path.read_bytes() != data:
                    fail("save candidate", "existing snapshot differs", name)
            else:
                with path.open("xb") as stream:
                    stream.write(data)
                    stream.flush()
                    os.fsync(stream.fileno())
        except OSError as exc:
            fail("save candidate", str(exc), name, RecordError)
        return name

    def load(self) -> dict[str, Any]:
        """Load minimum progress shape, rejecting missing or invalid bookkeeping."""
        state = self.read("state.json")
        required = {
            "format",
            "repo",
            "source",
            "original",
            "limit",
            "used",
            "phase",
            "session",
            "call",
            "last_response",
            "checked",
            "checked_response",
            "error",
            "extensions",
            "continuations",
        }
        if not required <= state.keys() or state["format"] != 1:
            fail("load progress", "missing fields or unknown format", state)
        if (
            type(state["used"]) is not int
            or type(state["limit"]) is not int
            or not 0 <= state["used"] <= state["limit"]
            or state["limit"] < 1
            or state["phase"]
            not in {"between", "opening", "working", "pending", "failed"}
            or not isinstance(state["extensions"], list)
            or not isinstance(state["continuations"], list)
        ):
            fail("load progress", "invalid round bookkeeping", state)
        return state

    def save(self, state: dict[str, Any]) -> None:
        """Replace only the progress index atomically; retain original records."""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.root,
                delete=False,
                prefix="progress-",
                suffix=".tmp",
            ) as stream:
                json.dump(state, stream, indent=2, ensure_ascii=False)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
                temporary = stream.name
            os.replace(temporary, self.root / "state.json")
        except OSError as exc:
            fail("save progress", str(exc), self.root, RecordError)

    @contextmanager
    def locked(self) -> Iterator[None]:
        """Allow one operation at a time, including its model call."""
        try:
            stream = (self.root / ".lock").open("a+")
        except OSError as exc:
            fail("lock review", str(exc), self.root)
        with stream:
            try:
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                fail("lock review", str(exc), self.root)
            try:
                yield
            finally:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
