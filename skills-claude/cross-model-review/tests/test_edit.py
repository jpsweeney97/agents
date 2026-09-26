"""Tests for the ``edit`` command: the next candidate from exact-text edits."""

from __future__ import annotations

import errno
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import cmr_archive
import cmr_edit
import cmr_engine as engine
import pytest
import review as review_cli
from cmr_archive import Archive, RecordError, ReviewError
from cross_model_runtime.codex_transport import CodexResult, CodexTransportError

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent / "scripts"
FIXTURES = TESTS / "fixtures" / "candidate-edit"
CASES = ("m6-r4", "stalemate-r2", "stalemate-r3", "stalemate-r4", "stalemate-r5")
SCRIPT = SCRIPTS / "review.py"

assert Path(cmr_edit.__file__).resolve().parent == SCRIPTS, cmr_edit.__file__

BASE = b"# Title\n\nAlpha beta gamma.\n\nDelta epsilon.\n"
ONE_EDIT = [{"old": "beta", "new": "BETA"}]
AUTO = "auto"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_review(tmp_path: Path, base: bytes = BASE) -> tuple[Archive, Path, Path]:
    """Create a review whose ``host/`` holds ``candidate-1.md`` with ``base``."""
    repo = tmp_path / "target"
    repo.mkdir(parents=True)
    source = repo / "plan.md"
    source.write_bytes(base)
    archive = Archive.create(tmp_path / "review", repo, source, 3)
    host = archive.root / "host"
    host.mkdir()
    candidate = host / "candidate-1.md"
    candidate.write_bytes(base)
    return archive, host, candidate


def write_edits(path: Path, edits: Any) -> Path:
    path.write_text(json.dumps(edits, ensure_ascii=False), encoding="utf-8")
    return path


def edit(
    archive: Archive,
    host: Path,
    candidate: Path,
    *,
    edits: Any = ONE_EDIT,
    out: str | None = None,
    expect_sha: str | None = AUTO,
    base: str | None = None,
) -> dict[str, Any]:
    """Run ``apply_edits``; ``expect_sha=AUTO`` means the candidate's digest.

    The edits file is written outside the review so ``host/`` holds only what
    the command itself creates.
    """
    edits_path = write_edits(archive.root.parent / "edits.json", edits)
    sha = digest(candidate.read_bytes()) if expect_sha == AUTO else expect_sha
    out = str(host / "candidate-2.md") if out is None else out
    return cmr_edit.apply_edits(
        archive, str(candidate) if base is None else base, str(edits_path), out, sha
    )


def published(host: Path, name: str = "candidate-2.md") -> tuple[bool, bool, list[str]]:
    out = host / name
    receipt = host / (name + ".receipt.json")
    temporaries = sorted(path.name for path in host.glob("edit-*.tmp"))
    return os.path.lexists(out), os.path.lexists(receipt), temporaries


def assert_nothing_published(host: Path, name: str = "candidate-2.md") -> None:
    assert published(host, name) == (False, False, [])


# 1. Equivalence against the recorded fold scripts.


@pytest.mark.parametrize("case", CASES)
def test_equivalence_with_recorded_fold_scripts(tmp_path: Path, case: str) -> None:
    base = (FIXTURES / case / "base.md").read_bytes()
    expected = (FIXTURES / case / "expected.md").read_bytes()
    archive, host, candidate = make_review(tmp_path, base)
    edits_file = host / "edits.json"
    edits_file.write_bytes((FIXTURES / case / "edits.json").read_bytes())
    result = cmr_edit.apply_edits(
        archive,
        str(candidate),
        str(edits_file),
        str(host / "candidate-2.md"),
        digest(base),
    )
    assert (host / "candidate-2.md").read_bytes() == expected
    assert result["sha256"] == digest(expected)
    assert result["base_sha256"] == digest(base)
    assert result["edits_applied"] == len(
        json.loads(edits_file.read_text(encoding="utf-8"))
    )
    assert result["lines"] == len(expected.decode("utf-8").splitlines())
    receipt = json.loads(
        (host / "candidate-2.md.receipt.json").read_text(encoding="utf-8")
    )
    assert receipt["semantics"] == 1
    assert receipt["out"]["sha256"] == digest(expected)
    assert receipt["base"]["sha256"] == digest(base)
    assert receipt["edits_file"]["sha256"] == digest(edits_file.read_bytes())
    assert receipt["edits"] == json.loads(edits_file.read_text(encoding="utf-8"))


# 2. Edits-file validation.


@pytest.mark.parametrize(
    ("content", "reason"),
    [
        ("[{", "invalid edits file: Expecting"),
        (
            '{"old": "beta", "new": "b"}',
            "invalid edits file: top level must be an array",
        ),
        ("[1]", "invalid edits file: item 1 is not an object"),
        ('[{"new": "x"}]', "invalid edits file: item 1 needs string old and new"),
        (
            '[{"old": 1, "new": "x"}]',
            "invalid edits file: item 1 needs string old and new",
        ),
        (
            '[{"old": "beta", "new": "x", "extra": 1}]',
            "invalid edits file: item 1 has unknown key extra",
        ),
        ("[]", "invalid edits file: no edits"),
        ('[{"old": "", "new": "x"}]', "invalid edits file: item 1 has empty old"),
        (
            '[{"old": "beta", "new": "x", "label": 3}]',
            "invalid edits file: item 1 label must be a string",
        ),
        (
            '[{"old": "beta", "new": "\\ud800"}]',
            "invalid edits file: item 1 new is not encodable as UTF-8",
        ),
        (
            '[{"old": "\\ud800", "new": "x"}]',
            "invalid edits file: item 1 old is not encodable as UTF-8",
        ),
        (
            '[{"label": "\\ud800", "old": "beta", "new": "x"}]',
            "invalid edits file: item 1 label is not encodable as UTF-8",
        ),
        (
            '[{"old": "beta", "new": "x"}, {"label": "\\ud800", "old": "gamma", "new": "y"}]',
            "invalid edits file: item 2 label is not encodable as UTF-8",
        ),
    ],
)
def test_invalid_edits_file_publishes_nothing(
    tmp_path: Path, content: str, reason: str
) -> None:
    archive, host, candidate = make_review(tmp_path)
    edits_file = host / "edits.json"
    edits_file.write_text(content, encoding="utf-8")
    with pytest.raises(
        ReviewError, match="^edit candidate failed: " + re.escape(reason)
    ):
        cmr_edit.apply_edits(
            archive,
            str(candidate),
            str(edits_file),
            str(host / "candidate-2.md"),
            digest(BASE),
        )
    assert_nothing_published(host)


# 3. Matching.


def test_zero_and_several_matches_are_refused(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path, b"one two three\ntwo four\n")
    with pytest.raises(
        ReviewError,
        match=r"^edit candidate failed: edit 1 matched 0 times, not once\. Got: 'five'",
    ):
        edit(archive, host, candidate, edits=[{"old": "five", "new": "x"}])
    with pytest.raises(
        ReviewError,
        match=r"^edit candidate failed: edit 1 \(dup\) matched 2 times, not once\. Got: 'two'",
    ):
        edit(
            archive, host, candidate, edits=[{"label": "dup", "old": "two", "new": "x"}]
        )
    assert_nothing_published(host)


def test_overlapping_occurrences_count_separately(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path, b"aaa\n")
    with pytest.raises(ReviewError, match=r"edit 1 matched 2 times, not once"):
        edit(archive, host, candidate, edits=[{"old": "aa", "new": "b"}])
    assert_nothing_published(host)


def test_earlier_edit_may_create_a_later_match(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path, b"one two\n")
    result = edit(
        archive,
        host,
        candidate,
        edits=[{"old": "one", "new": "three"}, {"old": "three two", "new": "x"}],
    )
    assert (host / "candidate-2.md").read_bytes() == b"x\n"
    assert result["edits_applied"] == 2
    assert result["lines"] == 1


def test_earlier_edit_making_a_later_match_ambiguous_is_refused(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path, b"one two\n")
    with pytest.raises(ReviewError, match=r"edit 2 matched 2 times, not once"):
        edit(
            archive,
            host,
            candidate,
            edits=[{"old": "one", "new": "two"}, {"old": "two", "new": "x"}],
        )
    assert_nothing_published(host)


# 4. Base identity.


def test_base_identity(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path)
    sha = digest(BASE)
    wrong = "0" * 64
    ref = archive.load()["original"]
    assert ref == f"drafts/{sha}.md"

    result = edit(archive, host, candidate, out=str(host / "ok.md"), expect_sha=sha)
    assert result["base_sha256"] == sha
    with pytest.raises(
        ReviewError,
        match=f"^edit candidate failed: base sha256 is {sha}, expected {wrong}",
    ):
        edit(archive, host, candidate, out=str(host / "bad.md"), expect_sha=wrong)
    with pytest.raises(
        ReviewError, match="expected sha256 is required for a filesystem path base"
    ):
        edit(archive, host, candidate, out=str(host / "nosha.md"), expect_sha=None)
    with pytest.raises(
        ReviewError, match="expected sha256 must be 64 lowercase hex digits"
    ):
        edit(archive, host, candidate, out=str(host / "short.md"), expect_sha="abc")
    with pytest.raises(
        ReviewError, match="expected sha256 must be 64 lowercase hex digits"
    ):
        edit(
            archive, host, candidate, out=str(host / "upper.md"), expect_sha=sha.upper()
        )

    edit(
        archive,
        host,
        candidate,
        base=ref,
        out=str(host / "ref-none.md"),
        expect_sha=None,
    )
    edit(
        archive,
        host,
        candidate,
        base=ref,
        out=str(host / "ref-agree.md"),
        expect_sha=sha,
    )
    with pytest.raises(
        ReviewError, match="expected sha256 disagrees with the drafts reference"
    ):
        edit(
            archive,
            host,
            candidate,
            base=ref,
            out=str(host / "ref-disagree.md"),
            expect_sha=wrong,
        )
    with pytest.raises(
        ReviewError, match="expected sha256 is required for a filesystem path base"
    ):
        edit(
            archive,
            host,
            candidate,
            base="./" + ref,
            out=str(host / "dot.md"),
            expect_sha=None,
        )
    with pytest.raises(
        ReviewError, match="expected sha256 is required for a filesystem path base"
    ):
        edit(
            archive,
            host,
            candidate,
            base=str(archive.path(ref)),
            out=str(host / "abs.md"),
            expect_sha=None,
        )
    with pytest.raises(
        ReviewError, match="^resolve record failed: record is outside review directory"
    ):
        edit(
            archive,
            host,
            candidate,
            base="drafts/../../outside.md",
            out=str(host / "escape.md"),
            expect_sha=None,
        )

    archive.path(ref).write_bytes(BASE + b"tampered\n")
    with pytest.raises(
        ReviewError, match="^read candidate failed: saved candidate content changed"
    ):
        edit(
            archive,
            host,
            candidate,
            base=ref,
            out=str(host / "tampered.md"),
            expect_sha=None,
        )
    for name in (
        "bad",
        "nosha",
        "short",
        "upper",
        "ref-disagree",
        "dot",
        "abs",
        "escape",
        "tampered",
    ):
        assert_nothing_published(host, f"{name}.md")


# 5. Byte fidelity.


@pytest.mark.parametrize(
    ("base", "old", "new", "expected"),
    [
        (b"a\nb\n", "a", "A", b"A\nb\n"),
        (b"a\r\nb\r\n", "a", "A", b"A\r\nb\r\n"),
        (b"a\r\nb\nc", "b", "B", b"a\r\nB\nc"),
        ("héllo → wörld\n".encode(), "→", "⇒", "héllo ⇒ wörld\n".encode()),
        (b"no final newline", "final", "last", b"no last newline"),
    ],
)
def test_byte_fidelity(
    tmp_path: Path, base: bytes, old: str, new: str, expected: bytes
) -> None:
    archive, host, candidate = make_review(tmp_path, base)
    result = edit(archive, host, candidate, edits=[{"old": old, "new": new}])
    on_disk = (host / "candidate-2.md").read_bytes()
    assert on_disk == expected
    assert result["sha256"] == digest(on_disk)
    assert result["lines"] == len(expected.decode("utf-8").splitlines())


def test_empty_base_matches_nothing(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path, b"")
    with pytest.raises(ReviewError, match=r"edit 1 matched 0 times, not once"):
        edit(archive, host, candidate, edits=[{"old": "x", "new": "y"}])
    assert_nothing_published(host)


# 6. Output protection.


def _existing_file(host: Path, archive: Archive, candidate: Path) -> str:
    (host / "taken.md").write_bytes(b"x")
    return str(host / "taken.md")


def _directory(host: Path, archive: Archive, candidate: Path) -> str:
    (host / "taken.md").mkdir()
    return str(host / "taken.md")


def _live_symlink(host: Path, archive: Archive, candidate: Path) -> str:
    (host / "alias.md").symlink_to(candidate)
    return str(host / "alias.md")


def _dangling_symlink(host: Path, archive: Archive, candidate: Path) -> str:
    (host / "alias.md").symlink_to(host / "missing.md")
    return str(host / "alias.md")


def _existing_receipt(host: Path, archive: Archive, candidate: Path) -> str:
    (host / "new.md.receipt.json").write_bytes(b"{}\n")
    return str(host / "new.md")


def _symlinked_parent(host: Path, archive: Archive, candidate: Path) -> str:
    elsewhere = archive.root.parent / "elsewhere"
    elsewhere.mkdir()
    (host / "link").symlink_to(elsewhere)
    return str(host / "link" / "new.md")


def _dotdot(host: Path, archive: Archive, candidate: Path) -> str:
    return f"{host}/../new.md"


def _trailing_dot(host: Path, archive: Archive, candidate: Path) -> str:
    return f"{host}/new.md/."


def _trailing_dotdot(host: Path, archive: Archive, candidate: Path) -> str:
    return f"{host}/new.md/.."


def _trailing_separator(host: Path, archive: Archive, candidate: Path) -> str:
    return f"{host}/new.md/"


def _review_root(host: Path, archive: Archive, candidate: Path) -> str:
    return str(archive.root / "new.md")


def _subdirectory(host: Path, archive: Archive, candidate: Path) -> str:
    (host / "sub").mkdir()
    return str(host / "sub" / "new.md")


@pytest.mark.parametrize(
    ("setup", "reason"),
    [
        (_existing_file, "output already exists"),
        (_directory, "output already exists"),
        (_live_symlink, "output already exists"),
        (_dangling_symlink, "output already exists"),
        (_existing_receipt, "receipt path already exists"),
        (
            _symlinked_parent,
            "output must be directly inside the review's host directory",
        ),
        (_dotdot, "output must be directly inside the review's host directory"),
        (_trailing_dot, "output must name a file"),
        (_trailing_dotdot, "output must name a file"),
        (_trailing_separator, "output must name a file"),
        (_review_root, "output must be directly inside the review's host directory"),
        (_subdirectory, "output must be directly inside the review's host directory"),
    ],
)
def test_output_protection(tmp_path: Path, setup: Any, reason: str) -> None:
    archive, host, candidate = make_review(tmp_path)
    out = setup(host, archive, candidate)
    before = sorted(str(path) for path in archive.root.rglob("*"))
    with pytest.raises(
        ReviewError, match="^edit candidate failed: " + re.escape(reason)
    ):
        edit(archive, host, candidate, out=out)
    assert sorted(str(path) for path in archive.root.rglob("*")) == before
    assert not (host / "new.md").exists()
    assert not (archive.root / "new.md").exists()


def test_output_equal_to_base_is_refused(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path)
    with pytest.raises(
        ReviewError, match="^edit candidate failed: output already exists"
    ):
        edit(archive, host, candidate, out=str(candidate))
    ghost = host / "ghost.md"
    with pytest.raises(
        ReviewError, match="^edit candidate failed: output must differ from the base"
    ):
        edit(
            archive,
            host,
            candidate,
            base=str(ghost),
            out=str(ghost),
            expect_sha=digest(BASE),
        )
    assert not ghost.exists()


def test_host_must_be_a_real_directory(tmp_path: Path) -> None:
    archive, host, _candidate = make_review(tmp_path)
    real = archive.root / "real-host"
    host.rename(real)
    host.symlink_to(real)
    moved = real / "candidate-1.md"
    with pytest.raises(
        ReviewError,
        match="^edit candidate failed: host directory must exist and not be a symlink",
    ):
        edit(archive, host, moved)
    host.unlink()
    host.symlink_to(archive.root)
    with pytest.raises(
        ReviewError, match="host directory must exist and not be a symlink"
    ):
        edit(archive, host, moved, out=str(host / "02-closing.request.json"))
    assert not (archive.root / "02-closing.request.json").exists()
    host.unlink()
    with pytest.raises(
        ReviewError, match="host directory must exist and not be a symlink"
    ):
        edit(archive, host, moved)
    host.write_bytes(b"not a directory")
    with pytest.raises(
        ReviewError, match="host directory must exist and not be a symlink"
    ):
        edit(archive, host, moved)


# 7. Concurrent creation.


def test_same_out_race_loser_publishes_nothing(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path)
    edits_a = write_edits(host / "a.json", [{"old": "beta", "new": "A"}])
    edits_b = write_edits(host / "b.json", [{"old": "beta", "new": "B"}])
    out = str(host / "candidate-2.md")
    plan_a = cmr_edit._prepare(archive, str(candidate), str(edits_a), out, digest(BASE))
    plan_b = cmr_edit._prepare(archive, str(candidate), str(edits_b), out, digest(BASE))
    cmr_edit._publish(plan_a)
    winner = (
        (host / "candidate-2.md").read_bytes(),
        (host / "candidate-2.md.receipt.json").read_bytes(),
    )
    assert winner[0] == b"# Title\n\nAlpha A gamma.\n\nDelta epsilon.\n"
    with pytest.raises(
        RecordError,
        match="^publish candidate failed: nothing published by this invocation; "
        "output now exists, created concurrently; ",
    ):
        cmr_edit._publish(plan_b)
    assert (
        (host / "candidate-2.md").read_bytes(),
        (host / "candidate-2.md.receipt.json").read_bytes(),
    ) == winner
    assert published(host) == (True, True, [])


def test_receipt_destination_collision_keeps_candidate(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path)
    edits_file = write_edits(host / "edits.json", ONE_EDIT)
    out = host / "candidate-2.md"
    receipt = host / "candidate-2.md.receipt.json"
    plan = cmr_edit._prepare(
        archive, str(candidate), str(edits_file), str(out), digest(BASE)
    )
    receipt.write_bytes(b"foreign\n")
    with pytest.raises(RecordError) as caught:
        cmr_edit._publish(plan)
    message = str(caught.value)
    assert message.startswith(
        f"write receipt failed: candidate published at {out}; receipt not written "
        "by this invocation; receipt path now exists, created concurrently; "
    )
    assert message.endswith(f". Got: {str(receipt)!r:.100}")
    assert out.read_bytes() == plan.candidate_bytes
    assert receipt.read_bytes() == b"foreign\n"
    assert published(host) == (True, True, [])


# 8. Injected publication failures, one at a time.


def _inject(
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    nth: int,
    error: type[OSError],
    message: str = "boom",
) -> None:
    module: Any = tempfile if name == "NamedTemporaryFile" else os
    original = getattr(module, name)
    calls = 0

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        nonlocal calls
        calls += 1
        if calls == nth:
            raise error(message)
        return original(*args, **kwargs)

    monkeypatch.setattr(module, name, wrapper)


INJECTIONS = [
    # (name, nth, error, second injection, out published, receipt published, temporaries left, expected reason)
    (
        "NamedTemporaryFile",
        1,
        OSError,
        None,
        False,
        False,
        0,
        "publish candidate failed: nothing published; boom",
    ),
    (
        "fsync",
        1,
        OSError,
        None,
        False,
        False,
        0,
        "publish candidate failed: nothing published; boom",
    ),
    (
        "link",
        1,
        OSError,
        None,
        False,
        False,
        0,
        "publish candidate failed: nothing published; boom",
    ),
    (
        "link",
        1,
        FileExistsError,
        None,
        False,
        False,
        0,
        "publish candidate failed: nothing published by this invocation; output now exists, created concurrently; boom",
    ),
    (
        "unlink",
        1,
        OSError,
        None,
        True,
        False,
        1,
        "publish candidate failed: candidate published at {out}; receipt not attempted; temporary left at {tmp}: boom",
    ),
    (
        "NamedTemporaryFile",
        2,
        OSError,
        None,
        True,
        False,
        0,
        "write receipt failed: candidate published at {out}; receipt not written; boom",
    ),
    (
        "fsync",
        2,
        OSError,
        None,
        True,
        False,
        0,
        "write receipt failed: candidate published at {out}; receipt not written; boom",
    ),
    (
        "link",
        2,
        OSError,
        None,
        True,
        False,
        0,
        "write receipt failed: candidate published at {out}; receipt not written; boom",
    ),
    (
        "link",
        2,
        FileExistsError,
        None,
        True,
        False,
        0,
        "write receipt failed: candidate published at {out}; receipt not written by this invocation; receipt path now exists, created concurrently; boom",
    ),
    (
        "unlink",
        2,
        OSError,
        None,
        True,
        True,
        1,
        "write receipt failed: candidate and receipt published; temporary left at {tmp}: boom",
    ),
    (
        "link",
        1,
        OSError,
        ("unlink", 1),
        False,
        False,
        1,
        "publish candidate failed: nothing published; boom; temporary left at {tmp}: cleanup boom",
    ),
    (
        "link",
        2,
        FileExistsError,
        ("unlink", 2),
        True,
        False,
        1,
        "write receipt failed: candidate published at {out}; receipt not written by this invocation; receipt path now exists, created concurrently; boom; temporary left at {tmp}: cleanup boom",
    ),
    (
        "link",
        1,
        FileExistsError,
        ("unlink", 1),
        False,
        False,
        1,
        "publish candidate failed: nothing published by this invocation; output now exists, created concurrently; boom; temporary left at {tmp}: cleanup boom",
    ),
    (
        "link",
        2,
        OSError,
        ("unlink", 2),
        True,
        False,
        1,
        "write receipt failed: candidate published at {out}; receipt not written; boom; temporary left at {tmp}: cleanup boom",
    ),
    (
        "fchmod",
        1,
        OSError,
        None,
        False,
        False,
        0,
        "publish candidate failed: nothing published; boom",
    ),
    (
        "fchmod",
        2,
        OSError,
        None,
        True,
        False,
        0,
        "write receipt failed: candidate published at {out}; receipt not written; boom",
    ),
]


@pytest.mark.parametrize(
    (
        "name",
        "nth",
        "error",
        "second",
        "out_published",
        "receipt_published",
        "temporaries",
        "reason",
    ),
    INJECTIONS,
)
def test_injected_publication_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    nth: int,
    error: type[OSError],
    second: tuple[str, int] | None,
    out_published: bool,
    receipt_published: bool,
    temporaries: int,
    reason: str,
) -> None:
    archive, host, candidate = make_review(tmp_path)
    edits_file = write_edits(host / "edits.json", ONE_EDIT)
    out = host / "candidate-2.md"
    receipt = host / "candidate-2.md.receipt.json"
    plan = cmr_edit._prepare(
        archive, str(candidate), str(edits_file), str(out), digest(BASE)
    )
    _inject(monkeypatch, name, nth, error)
    if second is not None:
        _inject(monkeypatch, second[0], second[1], OSError, "cleanup boom")
    with pytest.raises(RecordError) as caught:
        cmr_edit._publish(plan)
    monkeypatch.undo()
    left = sorted(host.glob("edit-*.tmp"))
    assert len(left) == temporaries
    tmp = str(left[0]) if left else ""
    expected = reason.format(out=out, tmp=tmp)
    got = str(out) if expected.startswith("publish candidate") else str(receipt)
    assert str(caught.value) == f"{expected}. Got: {got!r:.100}"
    assert out.exists() == out_published
    assert receipt.exists() == receipt_published
    if out_published:
        assert out.read_bytes() == plan.candidate_bytes
    if receipt_published:
        assert receipt.read_bytes() == plan.receipt_bytes
    if left:
        payload = plan.candidate_bytes if nth == 1 else plan.receipt_bytes
        assert left[0].read_bytes() == payload


# 11. CLI.


def _run_cli(cwd: Path, review: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--review", str(review), "edit", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_relative_paths_resolve_against_the_working_directory(
    tmp_path: Path,
) -> None:
    archive, host, candidate = make_review(tmp_path)
    write_edits(host / "edits.json", ONE_EDIT)
    done = _run_cli(
        host,
        archive.root,
        "--from",
        "./candidate-1.md",
        "--edits",
        "./edits.json",
        "--out",
        "./candidate-2.md",
        "--expect-sha",
        digest(BASE),
    )
    assert done.returncode == 0, done.stderr
    result = json.loads(done.stdout)
    assert done.stdout == json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    assert result == {
        "out": str(host / "candidate-2.md"),
        "receipt": str(host / "candidate-2.md.receipt.json"),
        "base_sha256": digest(BASE),
        "sha256": digest(b"# Title\n\nAlpha BETA gamma.\n\nDelta epsilon.\n"),
        "edits_applied": 1,
        "lines": 5,
    }
    receipt = json.loads(
        (host / "candidate-2.md.receipt.json").read_text(encoding="utf-8")
    )
    assert receipt["base"] == {
        "argument": "./candidate-1.md",
        "path": str(candidate),
        "sha256": digest(BASE),
    }
    assert receipt["edits_file"]["argument"] == "./edits.json"
    assert receipt["edits_file"]["path"] == str(host / "edits.json")
    assert receipt["edits"] == ONE_EDIT
    assert receipt["out"] == {
        "path": str(host / "candidate-2.md"),
        "sha256": result["sha256"],
    }


def test_cli_drafts_reference_resolves_against_the_review_root(tmp_path: Path) -> None:
    archive, host, _candidate = make_review(tmp_path)
    write_edits(host / "edits.json", ONE_EDIT)
    foreign = tmp_path / "elsewhere"
    foreign.mkdir()
    ref = archive.load()["original"]
    done = _run_cli(
        foreign,
        archive.root,
        "--from",
        ref,
        "--edits",
        str(host / "edits.json"),
        "--out",
        str(host / "candidate-2.md"),
    )
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["base_sha256"] == digest(BASE)
    receipt = json.loads(
        (host / "candidate-2.md.receipt.json").read_text(encoding="utf-8")
    )
    assert receipt["base"]["argument"] == ref
    assert receipt["base"]["path"] == str(archive.path(ref))

    refused = _run_cli(
        foreign,
        archive.root,
        "--from",
        ref,
        "--edits",
        str(host / "edits.json"),
        "--out",
        "candidate-3.md",
    )
    assert refused.returncode == 1
    assert refused.stdout == ""
    assert refused.stderr.startswith(
        "edit candidate failed: output must be directly inside the review's host directory"
    )
    assert_nothing_published(host, "candidate-3.md")


def test_cli_errors_go_to_stderr_with_exit_one(tmp_path: Path) -> None:
    archive, host, _candidate = make_review(tmp_path)
    write_edits(host / "edits.json", ONE_EDIT)
    failed = _run_cli(
        host,
        archive.root,
        "--from",
        "./candidate-1.md",
        "--edits",
        "./edits.json",
        "--out",
        "./candidate-2.md",
    )
    assert failed.returncode == 1
    assert failed.stdout == ""
    assert failed.stderr.startswith(
        "edit candidate failed: expected sha256 is required for a filesystem path base. "
        "Got: './candidate-1.md'"
    )
    assert_nothing_published(host)


@pytest.mark.parametrize("position", ["--from", "--edits", "--out"])
def test_cli_refuses_a_non_utf8_path_argument(tmp_path: Path, position: str) -> None:
    archive, host, _candidate = make_review(tmp_path)
    write_edits(host / "edits.json", ONE_EDIT)
    arguments = {
        "--from": "./candidate-1.md",
        "--edits": "./edits.json",
        "--out": "./candidate-2.md",
    }
    arguments[position] = arguments[position].replace(".", "\udcff.", 1)
    before = sorted(path.name for path in host.iterdir())
    failed = _run_cli(
        host,
        archive.root,
        "--from",
        arguments["--from"],
        "--edits",
        arguments["--edits"],
        "--out",
        arguments["--out"],
        "--expect-sha",
        digest(BASE),
    )
    assert failed.returncode == 1
    assert failed.stdout == ""
    assert failed.stderr.startswith(
        "edit candidate failed: argument is not encodable as UTF-8"
    )
    assert sorted(path.name for path in host.iterdir()) == before


# 9. Isolation from round state.


def test_edit_leaves_state_untouched_at_every_phase_and_under_lock(
    tmp_path: Path,
) -> None:
    archive, host, candidate = make_review(tmp_path)
    state_path = archive.root / "state.json"
    for index, phase in enumerate(
        ("between", "opening", "working", "pending", "failed")
    ):
        state = archive.load()
        state["phase"] = phase
        state["used"] = 0 if phase == "between" else 1
        state["call"] = (
            {"prefix": "01-opening", "kind": "opening", "revision": state["original"]}
            if phase == "pending"
            else None
        )
        state["error"] = "simulated" if phase == "failed" else None
        archive.save(state)
        before = state_path.read_bytes()
        edit(archive, host, candidate, out=str(host / f"phase-{index}.md"))
        assert state_path.read_bytes() == before
        assert (
            host / f"phase-{index}.md"
        ).read_bytes() == b"# Title\n\nAlpha BETA gamma.\n\nDelta epsilon.\n"
    before = state_path.read_bytes()
    with archive.locked():
        edit(archive, host, candidate, out=str(host / "locked.md"))
    assert state_path.read_bytes() == before
    assert archive.load()["checked"] is None


# 10. Review integration.


def _controlled_runner(bodies: list[Any]) -> Any:
    def run(
        prompt: str,
        *,
        output_schema: dict[str, Any],
        repo_root: str,
        timeout_seconds: float,
        resume_thread_id: str | None,
    ) -> CodexResult:
        body = bodies.pop(0)
        if isinstance(body, Exception):
            raise body
        message = json.dumps(
            {
                "revision": output_schema["properties"]["revision"]["enum"][0],
                "findings": body,
                "review_notes": "Read the whole candidate.",
            }
        )
        return CodexResult(
            message,
            0,
            '{"type":"thread.started","thread_id":"review-session"}\n',
            "",
            ("codex", "controlled-test-runner"),
        )

    return run


def test_query_snapshots_the_edited_candidate_and_edit_never_moves_checked(
    tmp_path: Path,
) -> None:
    archive, host, candidate = make_review(tmp_path)
    source = tmp_path / "target" / "plan.md"
    request = tmp_path / "request.md"
    request.write_text(
        "Goal: uppercase beta. Review the candidate.\n", encoding="utf-8"
    )
    finding = {
        "ref": "F1",
        "disposition": "standing",
        "material": True,
        "explanation": "beta should be uppercase.",
    }
    resolved = dict(finding, disposition="resolved", explanation="Now uppercase.")

    engine.begin(archive)
    engine.query(archive, source, request, _controlled_runner([[finding]]))
    edit(
        archive,
        host,
        candidate,
        edits=[{"old": "beta", "new": "Beta"}],
        out=str(host / "candidate-2.md"),
    )
    edit(
        archive,
        host,
        host / "candidate-2.md",
        edits=[{"old": "Beta", "new": "BETA"}],
        out=str(host / "candidate-3.md"),
    )
    assert archive.load()["checked"] is None

    state = engine.query(
        archive, host / "candidate-3.md", request, _controlled_runner([[resolved]])
    )
    checked = state["checked"]
    assert checked == f"drafts/{digest((host / 'candidate-3.md').read_bytes())}.md"
    assert archive.path(checked).read_bytes() == (host / "candidate-3.md").read_bytes()
    assert state["phase"] == "between"

    edit(
        archive,
        host,
        host / "candidate-3.md",
        edits=[{"old": "gamma", "new": "GAMMA"}],
        out=str(host / "candidate-4.md"),
    )
    assert archive.load()["checked"] == checked

    engine.begin(archive)
    with pytest.raises(CodexTransportError, match="transport down"):
        engine.query(
            archive,
            host / "candidate-4.md",
            request,
            _controlled_runner([CodexTransportError("transport down")]),
        )
    state = archive.load()
    assert state["phase"] == "failed"
    assert state["checked"] == checked
    assert state["used"] == 2


# 12. Receipt serialization and order of operations (design sections 3.0 and 6.3).


def test_receipt_bytes_are_the_specified_serialization(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path)
    edits_path = archive.root.parent / "edits.json"
    edits = [{"old": "beta", "new": "bêta", "label": "é first"}]
    result = edit(archive, host, candidate, edits=edits)
    out = host / "candidate-2.md"
    expected = {
        "semantics": 1,
        "base": {
            "argument": str(candidate),
            "path": str(candidate),
            "sha256": digest(BASE),
        },
        "edits_file": {
            "argument": str(edits_path),
            "path": str(edits_path),
            "sha256": digest(edits_path.read_bytes()),
        },
        "edits": [{"label": "é first", "old": "beta", "new": "bêta"}],
        "out": {"path": str(out), "sha256": digest(out.read_bytes())},
    }
    receipt_bytes = (host / "candidate-2.md.receipt.json").read_bytes()
    assert receipt_bytes == (
        json.dumps(expected, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    assert result["sha256"] == expected["out"]["sha256"]


def test_containment_is_checked_before_the_expected_sha(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path)
    with pytest.raises(
        ReviewError,
        match="^edit candidate failed: output must be directly inside the review's host directory",
    ):
        edit(
            archive, host, candidate, out=str(archive.root / "new.md"), expect_sha=None
        )
    assert not (archive.root / "new.md").exists()


def test_base_digest_is_checked_before_the_edits_file_is_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive, host, _candidate = make_review(tmp_path)
    wrong = "0" * 64
    monkeypatch.chdir(host)
    with pytest.raises(ReviewError) as caught:
        cmr_edit.apply_edits(
            archive,
            "./candidate-1.md",
            str(host / "missing.json"),
            str(host / "candidate-2.md"),
            wrong,
        )
    assert str(caught.value) == (
        f"edit candidate failed: base sha256 is {digest(BASE)}, expected {wrong}. "
        "Got: './candidate-1.md'"
    )
    assert_nothing_published(host)


def test_base_digest_is_checked_before_the_edits_are_parsed(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path)
    wrong = "0" * 64
    malformed = archive.root.parent / "malformed.json"
    malformed.write_text("[{", encoding="utf-8")
    with pytest.raises(
        ReviewError, match=f"^edit candidate failed: base sha256 is {digest(BASE)}"
    ):
        cmr_edit.apply_edits(
            archive, str(candidate), str(malformed), str(host / "candidate-2.md"), wrong
        )
    assert_nothing_published(host)


# 13. Unusual inputs still end in the shared diagnostic format.


def test_deeply_nested_edits_file_is_refused_through_fail(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path)
    deep = archive.root.parent / "deep.json"
    deep.write_text("[" * 200_000 + "]" * 200_000, encoding="utf-8")
    with pytest.raises(
        ReviewError, match="^edit candidate failed: invalid edits file: "
    ) as caught:
        cmr_edit.apply_edits(
            archive,
            str(candidate),
            str(deep),
            str(host / "candidate-2.md"),
            digest(BASE),
        )
    assert isinstance(caught.value.__context__, RecursionError)
    assert_nothing_published(host)


def test_integer_past_the_digit_limit_is_an_invalid_edits_file(tmp_path: Path) -> None:
    archive, host, candidate = make_review(tmp_path)
    huge = archive.root.parent / "huge.json"
    huge.write_text("[" + "9" * 5000 + "]", encoding="utf-8")
    with pytest.raises(
        ReviewError, match="^edit candidate failed: invalid edits file: "
    ) as caught:
        cmr_edit.apply_edits(
            archive,
            str(candidate),
            str(huge),
            str(host / "candidate-2.md"),
            digest(BASE),
        )
    assert isinstance(caught.value.__context__, ValueError)
    assert_nothing_published(host)


def _emulate_python312_resolve(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make ``Path.resolve`` raise on a symlink loop, as Python 3.12 does.

    The helper allows Python 3.12, whose non-strict ``Path.resolve`` raises
    ``RuntimeError`` on a loop; 3.13 and later do not. Emulating 3.12 here lets
    the loop tests catch a return to ``Path.resolve`` under any interpreter.
    """
    original = Path.resolve

    def resolve(self: Path, strict: bool = False) -> Path:
        resolved = original(self, strict=strict)
        try:
            resolved.stat()
        except OSError as exc:
            if exc.errno == errno.ELOOP:
                raise RuntimeError(f"Symlink loop from {exc.filename!r}") from None
        return resolved

    monkeypatch.setattr(Path, "resolve", resolve)


def test_symlink_loops_are_refused_through_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive, host, candidate = make_review(tmp_path)
    loop = archive.root.parent / "loop"
    loop.symlink_to(loop)
    (archive.root / "drafts" / "loop.md").symlink_to(
        archive.root / "drafts" / "loop.md"
    )
    (archive.root / "rootloop").symlink_to(archive.root / "rootloop")
    edits_path = write_edits(archive.root.parent / "edits.json", ONE_EDIT)
    _emulate_python312_resolve(monkeypatch)
    with pytest.raises(
        ReviewError,
        match="^edit candidate failed: output must be directly inside the review's host directory",
    ):
        cmr_edit.apply_edits(
            archive, str(candidate), str(edits_path), str(loop / "new.md"), digest(BASE)
        )
    with pytest.raises(ReviewError, match="^read input failed: "):
        cmr_edit.apply_edits(
            archive,
            str(loop),
            str(edits_path),
            str(host / "candidate-2.md"),
            digest(BASE),
        )
    with pytest.raises(ReviewError, match="^read input failed: "):
        cmr_edit.apply_edits(
            archive,
            str(candidate),
            str(loop),
            str(host / "candidate-2.md"),
            digest(BASE),
        )
    for reference in ("drafts/loop.md", "drafts/../rootloop"):
        with pytest.raises(ReviewError, match="^read input failed: "):
            cmr_edit.apply_edits(
                archive, reference, str(edits_path), str(host / "candidate-2.md"), None
            )
    with pytest.raises(
        ReviewError,
        match="^edit candidate failed: host directory must exist and not be a symlink",
    ):
        cmr_edit.apply_edits(
            Archive(loop),
            str(candidate),
            str(edits_path),
            str(host / "candidate-2.md"),
            digest(BASE),
        )
    assert_nothing_published(host)


def test_review_creation_refuses_symlink_loops_through_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "target"
    repo.mkdir()
    source = repo / "plan.md"
    source.write_bytes(BASE)
    loop = tmp_path / "loop"
    loop.symlink_to(loop)
    _emulate_python312_resolve(monkeypatch)
    with pytest.raises(ReviewError, match="^create review failed: "):
        Archive.create(loop, repo, source, 3)
    with pytest.raises(
        ReviewError,
        match="^create review failed: review must be outside the target directory",
    ):
        Archive.create(tmp_path / "review", loop, source, 3)
    with pytest.raises(ReviewError, match="^read input failed: "):
        Archive.create(tmp_path / "review", repo, loop, 3)
    assert not (tmp_path / "review").exists()


def _emulate_python312_realpath(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make ``os.path.realpath`` stop at a symlink loop, as Python 3.12's does.

    3.12's ``realpath`` resolves up to the first symlink that loops, keeps the
    rest of the path as text, and normalizes it, so ``loop/../outdir`` comes
    back with ``outdir`` unresolved; 3.13 and later keep resolving. This models
    that much of 3.12, which is all the tests below use, so a return to a
    single ``realpath`` fails them under any interpreter.
    """
    original = os.path.realpath

    def realpath(path: Any, *, strict: bool = False) -> str:
        parts = Path(os.getcwd(), path).parts  # keeps ``..``, unlike abspath
        for index in range(1, len(parts)):
            prefix = Path(*parts[: index + 1])
            if not prefix.is_symlink():
                continue
            try:
                prefix.stat()
            except OSError as exc:
                if exc.errno == errno.ELOOP:
                    head = original(Path(*parts[:index]), strict=strict)
                    return os.path.normpath(os.path.join(head, *parts[index:]))
        return original(path, strict=strict)

    monkeypatch.setattr(os.path, "realpath", realpath)


def test_a_symlink_after_a_loop_is_still_resolved(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive, host, candidate = make_review(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.md").write_bytes(BASE)
    drafts = archive.root / "drafts"
    (drafts / "loop").symlink_to(drafts / "loop")
    (drafts / "outdir").symlink_to(outside)
    name = "drafts/loop/../outdir/secret.md"
    real_outside = Path(os.path.realpath(outside))
    _emulate_python312_realpath(monkeypatch)
    assert os.path.realpath(archive.root / name) == str(drafts / "outdir/secret.md")
    assert Archive(drafts / "loop/../outdir").root == real_outside
    with pytest.raises(
        ReviewError,
        match="^resolve record failed: record is outside review directory",
    ):
        archive.path(name)
    with pytest.raises(
        ReviewError,
        match="^resolve record failed: record is outside review directory",
    ):
        edit(archive, host, candidate, base=name, expect_sha=None)
    assert_nothing_published(host)


def test_a_path_that_never_settles_is_refused(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    passes = iter(range(1000))

    def realpath(path: object) -> str:
        return f"/unsettled/{next(passes)}"

    monkeypatch.setattr(cmr_archive.os.path, "realpath", realpath)
    with pytest.raises(
        ReviewError, match="^resolve path failed: symlinks did not settle"
    ):
        cmr_archive.resolve_path(Path("/start"))
    monkeypatch.setattr(sys, "argv", ["review.py", "--review", "/start", "status"])
    assert review_cli.main() == 1
    assert capsys.readouterr().err.startswith(
        "resolve path failed: symlinks did not settle"
    )


# 14. Published files take the mode any other new record gets.


def test_candidate_and_receipt_take_the_umask_default_mode(tmp_path: Path) -> None:
    previous = os.umask(0o027)
    try:
        archive, host, candidate = make_review(tmp_path)
        edit(archive, host, candidate)
        after = os.umask(0o027)
    finally:
        os.umask(previous)
    assert after == 0o027, "edit must leave the process umask as it found it"
    snapshot = archive.path(archive.load()["original"])
    expected = 0o640
    for path in (
        snapshot,
        host / "candidate-2.md",
        host / "candidate-2.md.receipt.json",
    ):
        assert stat.S_IMODE(os.stat(path).st_mode) == expected, path


def test_cli_review_relative_paths_resolve_against_the_review_root(
    tmp_path: Path,
) -> None:
    """Issue #26: paths typed relative to the review directory work anywhere."""
    archive, host, _candidate = make_review(tmp_path)
    write_edits(host / "edits.json", ONE_EDIT)
    foreign = tmp_path / "far" / "away"
    foreign.mkdir(parents=True)
    done = _run_cli(
        foreign,
        archive.root,
        "--from",
        "host/candidate-1.md",
        "--edits",
        "host/edits.json",
        "--out",
        "host/candidate-2.md",
        "--expect-sha",
        digest(BASE),
    )
    assert done.returncode == 0, done.stderr
    result = json.loads(done.stdout)
    assert result["out"] == str(host / "candidate-2.md")
    assert result["edits_applied"] == 1
    receipt = json.loads(
        (host / "candidate-2.md.receipt.json").read_text(encoding="utf-8")
    )
    assert receipt["base"]["argument"] == "host/candidate-1.md"
    assert receipt["base"]["path"] == str(host / "candidate-1.md")
    assert receipt["edits_file"]["argument"] == "host/edits.json"
    assert receipt["edits_file"]["path"] == str(host / "edits.json")


def test_cli_a_path_that_exists_as_typed_wins_over_the_review_copy(
    tmp_path: Path,
) -> None:
    archive, host, _candidate = make_review(tmp_path)
    write_edits(host / "edits.json", ONE_EDIT)
    foreign = tmp_path / "far" / "away"
    (foreign / "host").mkdir(parents=True)
    write_edits(foreign / "host" / "edits.json", [{"old": "gamma", "new": "GAMMA"}])
    done = _run_cli(
        foreign,
        archive.root,
        "--from",
        archive.load()["original"],
        "--edits",
        "host/edits.json",
        "--out",
        "host/candidate-2.md",
    )
    assert done.returncode == 0, done.stderr
    assert (host / "candidate-2.md").read_bytes() == BASE.replace(b"gamma", b"GAMMA")
    receipt = json.loads(
        (host / "candidate-2.md.receipt.json").read_text(encoding="utf-8")
    )
    assert receipt["edits_file"]["path"] == str(foreign / "host" / "edits.json")


def test_cli_missing_input_names_both_directories(tmp_path: Path) -> None:
    archive, host, _candidate = make_review(tmp_path)
    foreign = tmp_path / "far" / "away"
    foreign.mkdir(parents=True)
    refused = _run_cli(
        foreign,
        archive.root,
        "--from",
        archive.load()["original"],
        "--edits",
        "host/edits.json",
        "--out",
        "host/candidate-2.md",
    )
    assert refused.returncode == 1
    assert refused.stdout == ""
    assert refused.stderr == (
        f"locate input failed: not found as typed under {foreign} nor under the "
        f"review directory {archive.root}. Got: 'host/edits.json'\n"
    )
    assert_nothing_published(host)

    write_edits(host / "edits.json", ONE_EDIT)
    refused = _run_cli(
        foreign,
        archive.root,
        "--from",
        archive.load()["original"],
        "--edits",
        "host/edits.json",
        "--out",
        "elsewhere/candidate-2.md",
    )
    assert refused.returncode == 1
    assert refused.stdout == ""
    assert refused.stderr == (
        "edit candidate failed: output must be directly inside the review's host "
        f"directory, as typed under {foreign} or under the review directory "
        f"{archive.root}. Got: 'elsewhere/candidate-2.md'\n"
    )
    assert_nothing_published(host)


def test_cli_review_relative_path_escaping_the_review_is_refused(
    tmp_path: Path,
) -> None:
    archive, host, _candidate = make_review(tmp_path)
    write_edits(tmp_path / "outside.json", ONE_EDIT)
    foreign = tmp_path / "far" / "away"
    foreign.mkdir(parents=True)
    refused = _run_cli(
        foreign,
        archive.root,
        "--from",
        archive.load()["original"],
        "--edits",
        "../outside.json",
        "--out",
        "host/candidate-2.md",
    )
    assert refused.returncode == 1
    assert refused.stdout == ""
    assert refused.stderr == (
        "resolve record failed: record is outside review directory. "
        "Got: '../outside.json'\n"
    )
    assert_nothing_published(host)
