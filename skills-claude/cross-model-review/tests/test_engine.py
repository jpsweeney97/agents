import json
import sys
from pathlib import Path
from typing import Any

import cmr_engine as engine
import pytest
from cmr_archive import Archive, ReviewError
from cross_model_runtime.codex_transport import CodexResult

FINDING = {
    "ref": "F1",
    "disposition": "standing",
    "material": True,
    "explanation": "The remote upload contradicts the explicit local-only goal.",
}


class Replies:
    def __init__(self, bodies: list[Any]) -> None:
        self.bodies = iter(bodies)
        self.sessions: list[str | None] = []

    def __call__(
        self,
        prompt: str,
        *,
        output_schema: dict[str, Any],
        repo_root: str,
        timeout_seconds: float,
        resume_thread_id: str | None,
    ) -> CodexResult:
        self.sessions.append(resume_thread_id)
        body = next(self.bodies)
        if isinstance(body, Exception):
            raise body
        if isinstance(body, CodexResult):
            return body
        message = (
            body
            if isinstance(body, str)
            else json.dumps(
                {
                    "revision": output_schema["properties"]["revision"]["enum"][0],
                    "findings": body,
                    "review_notes": "Read goals and the whole candidate.",
                }
            )
        )
        return CodexResult(
            message,
            0,
            '{"type":"thread.started","thread_id":"review-session"}\n',
            "",
            ("codex", "controlled-test-runner"),
        )


def setup_review(tmp_path: Path, limit: int = 3) -> tuple[Archive, Path, Path]:
    repo = tmp_path / "target"
    repo.mkdir()
    source = repo / "plan.md"
    source.write_text("Keep data local. Upload all data remotely.\n")
    host = tmp_path / "host.md"
    host.write_text("Goal: keep data local. Review this contradiction.\n")
    return Archive.create(tmp_path / "review", repo, source, limit), source, host


def test_three_rounds_use_four_calls_and_preserve_source(tmp_path: Path) -> None:
    archive, source, host = setup_review(tmp_path)
    before = source.read_bytes()
    replies = Replies([[FINDING]] * 4)
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    for expected_used in (1, 2, 3):
        if expected_used > 1:
            engine.begin(archive)
        engine.query(archive, source, host, replies)
        assert archive.load()["used"] == expected_used
        assert archive.load()["phase"] == "between"
    assert replies.sessions == [
        None,
        "review-session",
        "review-session",
        "review-session",
    ]
    assert source.read_bytes() == before
    with pytest.raises(ReviewError, match="no rounds remain"):
        engine.begin(archive)


def test_resume_replays_saved_response_without_call_or_recharge(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import os

    archive, source, host = setup_review(tmp_path)
    replies = Replies([[FINDING]])
    engine.begin(archive)
    original_replace = os.replace

    def interrupt_after_capture(src: str, dst: Path) -> None:
        if archive.path("01-opening.raw.json").exists():
            raise OSError("simulated failure writing progress after response capture")
        original_replace(src, dst)

    with monkeypatch.context() as context:
        context.setattr(os, "replace", interrupt_after_capture)
        with pytest.raises(ReviewError, match="save progress failed"):
            engine.query(archive, source, host, replies)
    assert archive.load()["phase"] == "pending"
    resumed = engine.resume(archive)
    assert resumed["used"] == 1
    assert resumed["phase"] == "working"
    assert resumed["session"] == "review-session"
    assert replies.sessions == [None]


def test_malformed_response_consumes_round_without_retry(tmp_path: Path) -> None:
    from cross_model_runtime.codex_transport import CodexTransportError

    archive, source, host = setup_review(tmp_path)
    replies = Replies(["not JSON"])
    engine.begin(archive)
    with pytest.raises(CodexTransportError):
        engine.query(archive, source, host, replies)
    assert archive.load()["used"] == 1
    assert archive.load()["phase"] == "failed"
    assert archive.load()["checked"] is None
    assert archive.read("01-opening.raw.json")["final_message"] == "not JSON"
    with pytest.raises(ReviewError, match="user decision"):
        engine.resume(archive)
    assert replies.sessions == [None]


def test_omitted_finding_is_not_withdrawal(tmp_path: Path) -> None:
    archive, source, host = setup_review(tmp_path)
    replies = Replies([[FINDING], []])
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    with pytest.raises(ReviewError, match="omitted findings"):
        engine.query(archive, source, host, replies)
    assert archive.load()["checked"] is None
    assert archive.load()["used"] == 1
    assert archive.read("01-closing.raw.json")["final_message"]


def test_result_preserves_disagreement_and_does_not_invent_completion(
    tmp_path: Path,
) -> None:
    archive, source, host = setup_review(tmp_path)
    replies = Replies([[FINDING], [FINDING]])
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    engine.query(archive, source, host, replies)
    note = tmp_path / "ending.md"
    note.write_text(
        "Claude still holds the local-only concern. Codex requests a constraint change that only JP can authorize; both positions remain open."
    )
    with pytest.raises(ReviewError, match="standing material findings"):
        engine.finish(archive, "complete", note)
    result = engine.finish(archive, "decision", note)
    assert result["candidate_checked"] is True
    assert result["rounds_used"] == 1
    assert "still holds" in archive.text("result.md")
    assert "01-closing.raw.json" in archive.text("result.md")


def test_resolved_candidate_returns_diff_without_adopting_it(tmp_path: Path) -> None:
    archive, source, host = setup_review(tmp_path)
    resolved = dict(
        FINDING, disposition="resolved", explanation="Remote upload removed."
    )
    replies = Replies([[FINDING], [resolved]])
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    candidate = tmp_path / "candidate.md"
    candidate.write_text("Keep data local. Search local files.\n")
    engine.query(archive, candidate, host, replies)
    note = tmp_path / "complete.md"
    note.write_text(
        "Remote upload removed; local-only goal preserved. No held material concerns or user decisions remain."
    )
    result = engine.finish(archive, "complete", note)
    assert result["candidate_checked"] is True
    assert "Search local files" in archive.text("changes.diff")
    assert "Upload all data remotely" in source.read_text()
    raw = archive.read(result["reviewer_record"])
    assert json.loads(raw["final_message"])["findings"][0]["disposition"] == "resolved"


def test_failure_does_not_return_unchecked_revision_as_checked(tmp_path: Path) -> None:
    from cross_model_runtime.codex_transport import CodexTransportError

    archive, source, host = setup_review(tmp_path)
    replies = Replies([[FINDING], [FINDING], "not JSON"])
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    engine.query(archive, source, host, replies)
    checked = archive.load()["checked"]
    engine.begin(archive)
    pending = tmp_path / "pending.md"
    pending.write_text("An unverified replacement.\n")
    with pytest.raises(CodexTransportError):
        engine.query(archive, pending, host, replies)
    note = tmp_path / "failure.md"
    note.write_text("Round two closing validation failed. Its candidate is unverified.")
    result = engine.finish(archive, "failed", note)
    assert result["candidate"] == str(archive.path(checked))
    assert result["rounds_used"] == 2
    assert result["reviewer_record"] == "01-closing.raw.json"


def test_extension_preserves_round_usage_and_review_session(tmp_path: Path) -> None:
    archive, source, host = setup_review(tmp_path)
    replies = Replies([[FINDING]] * 4)
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    for number in (1, 2, 3):
        if number > 1:
            engine.begin(archive)
        engine.query(archive, source, host, replies)
    authorization = tmp_path / "authorization.md"
    authorization.write_text("JP: authorize one additional round for F1.")
    state = engine.extend(archive, 1, authorization)
    assert (state["used"], state["limit"]) == (3, 4)
    assert state["session"] == "review-session"
    assert state["extensions"][0]["authorization"] == authorization.read_text()
    assert engine.begin(archive)["used"] == 4
    assert replies.sessions == [
        None,
        "review-session",
        "review-session",
        "review-session",
    ]


@pytest.mark.parametrize("failure_kind", ("malformed", "omitted", "nonzero"))
def test_authorized_continuation_preserves_records_and_charges_next_round(
    tmp_path: Path,
    failure_kind: str,
) -> None:
    from cross_model_runtime.codex_transport import CodexTransportError

    archive, source, host = setup_review(tmp_path)
    resolved = dict(FINDING, disposition="resolved", explanation="Correction checked.")
    failure: Any = "not JSON"
    if failure_kind == "omitted":
        failure = []
    elif failure_kind == "nonzero":
        failure = CodexResult(
            None, 23, "captured stdout", "process failed", ("controlled",)
        )
    replies = Replies([[FINDING], [resolved], failure, [resolved]])
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    engine.query(archive, source, host, replies)
    engine.begin(archive)
    with pytest.raises((ReviewError, CodexTransportError)):
        engine.query(archive, source, host, replies)
    before = archive.load()
    prefix = before["call"]["prefix"]
    raw_before = archive.path(f"{prefix}.raw.json").read_bytes()
    request_before = archive.path(f"{prefix}.request.json").read_bytes()
    authorization = tmp_path / "continue.md"
    authorization.write_text(
        "JP: authorize continuation after the second closing call."
    )

    after = engine.continue_after_failure(archive, authorization)
    assert after["phase"] == "between"
    for key in (
        "used",
        "limit",
        "session",
        "last_response",
        "checked",
        "checked_response",
    ):
        assert after[key] == before[key]
    assert after["continuations"] == [
        {
            "after_round": 2,
            "failed_call": "02-closing",
            "authorization": authorization.read_text(),
            "failure": before["error"],
        }
    ]
    assert archive.path(f"{prefix}.raw.json").read_bytes() == raw_before
    assert archive.path(f"{prefix}.request.json").read_bytes() == request_before
    assert replies.sessions == [None, "review-session", "review-session"]
    note = tmp_path / "result-note.md"
    note.write_text(
        "The second closing call failed; no new successful check exists yet."
    )
    with pytest.raises(
        ReviewError, match="latest round has no successful closing check"
    ):
        engine.finish(archive, "complete", note)

    assert engine.begin(archive)["used"] == 3
    engine.query(archive, source, host, replies)
    assert replies.sessions == [
        None,
        "review-session",
        "review-session",
        "review-session",
    ]
    assert archive.read(archive.load()["last_response"])["findings"] == [resolved]
    note.write_text("The third closing check passed; no held material concerns remain.")
    result = engine.finish(archive, "complete", note)
    assert result["rounds_used"] == 3
    assert result["continuations"] == after["continuations"]


@pytest.mark.parametrize(
    "case",
    (
        "opening",
        "timeout",
        "missing_raw",
        "corrupt_raw",
        "corrupt_request",
        "missing_candidate",
        "missing_session",
        "corrupt_previous",
        "missing_authorization",
        "empty_authorization",
    ),
)
def test_continuation_refuses_terminal_or_corrupt_records(
    tmp_path: Path, case: str
) -> None:
    from cross_model_runtime.codex_transport import CodexTransportError

    archive, source, host = setup_review(tmp_path)
    if case == "opening":
        replies = Replies(["not JSON"])
        engine.begin(archive)
    else:
        failure: Any = "not JSON"
        if case == "timeout":
            failure = CodexTransportError(
                "review failed: simulated timeout. Got: 'closing'"
            )
        replies = Replies([[FINDING], failure])
        engine.begin(archive)
        engine.query(archive, source, host, replies)
    with pytest.raises((ReviewError, CodexTransportError)):
        engine.query(archive, source, host, replies)
    state = archive.load()
    prefix = state["call"]["prefix"]
    if case == "missing_raw":
        raw = archive.path(f"{prefix}.raw.json")
        raw.rename(raw.with_suffix(".retained"))
    elif case == "corrupt_raw":
        archive.path(f"{prefix}.raw.json").write_text("{}")
    elif case == "corrupt_request":
        archive.path(f"{prefix}.request.json").write_text("{")
    elif case == "missing_candidate":
        candidate = archive.path(state["call"]["revision"])
        candidate.rename(candidate.with_suffix(".retained"))
    elif case == "missing_session":
        state["session"] = None
        archive.save(state)
    elif case == "corrupt_previous":
        archive.path(state["last_response"]).write_text("{}")
    authorization = tmp_path / "authorization.md"
    authorization.write_text(
        "JP: authorize continuation if the saved records permit it."
    )
    if case == "missing_authorization":
        authorization.rename(authorization.with_suffix(".retained"))
    elif case == "empty_authorization":
        authorization.write_text(" \n")
    before = archive.path("state.json").read_bytes()
    attempts = list(replies.sessions)
    with pytest.raises(ReviewError):
        engine.continue_after_failure(archive, authorization)
    assert archive.path("state.json").read_bytes() == before
    assert archive.load()["phase"] == "failed"
    assert archive.load()["continuations"] == []
    assert replies.sessions == attempts


def test_continuation_does_not_create_more_allowance(tmp_path: Path) -> None:
    from cross_model_runtime.codex_transport import CodexTransportError

    archive, source, host = setup_review(tmp_path, limit=2)
    replies = Replies([[FINDING], [FINDING], "not JSON"])
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    engine.query(archive, source, host, replies)
    engine.begin(archive)
    with pytest.raises(CodexTransportError):
        engine.query(archive, source, host, replies)
    authorization = tmp_path / "continue.md"
    authorization.write_text("JP: authorize continuation; no extra rounds granted yet.")
    state = engine.continue_after_failure(archive, authorization)
    assert (state["used"], state["limit"]) == (2, 2)
    with pytest.raises(ReviewError, match="no rounds remain"):
        engine.begin(archive)
    note = tmp_path / "ending.md"
    note.write_text(
        "Round two failed. Round one's checked candidate still has F1; no allowance remains."
    )
    result = engine.finish(archive, "exhausted", note)
    assert result["reviewer_record"] == "01-closing.raw.json"
    assert result["continuations"][0]["failed_call"] == "02-closing"
    extra = tmp_path / "extra.md"
    extra.write_text("JP: authorize one additional round.")
    assert engine.extend(archive, 1, extra)["limit"] == 3
    assert engine.begin(archive)["used"] == 3
    assert replies.sessions == [None, "review-session", "review-session"]


def test_cli_initializes_from_foreign_cwd_without_model_calls(tmp_path: Path) -> None:
    import subprocess

    repo = tmp_path / "target"
    repo.mkdir()
    source = repo / "plan.md"
    source.write_text("# Plan\n")
    review_root = tmp_path / "review"
    script = Path(__file__).resolve().parents[1] / "scripts" / "review.py"
    initialized = subprocess.run(
        [
            sys.executable,
            str(script),
            "--review",
            str(review_root),
            "init",
            "--repo",
            str(repo),
            "--source",
            str(source),
        ],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    assert initialized.returncode == 0, initialized.stderr
    assert json.loads(initialized.stdout)["used"] == 0
    begun = subprocess.run(
        [sys.executable, str(script), "--review", str(review_root), "begin"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    assert begun.returncode == 0, begun.stderr
    assert json.loads(begun.stdout)["used"] == 1
    assert source.read_text() == "# Plan\n"


def test_one_time_progress_save_failure_keeps_call_resumable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import os

    archive, source, host = setup_review(tmp_path)
    replies = Replies([[FINDING]])
    engine.begin(archive)
    original_replace = os.replace
    failures: list[str] = []

    def fail_once(src: str, dst: Path) -> None:
        if archive.path("01-opening.raw.json").exists() and not failures:
            failures.append("one transient failure writing progress")
            raise OSError(failures[0])
        original_replace(src, dst)

    with monkeypatch.context() as context:
        context.setattr(os, "replace", fail_once)
        with pytest.raises(ReviewError, match="save progress failed"):
            engine.query(archive, source, host, replies)
    state = archive.load()
    assert state["phase"] == "pending"
    assert state["call"]["prefix"] == "01-opening"
    assert archive.read("01-opening.response.json")["revision"] == state["original"]
    resumed = engine.resume(archive)
    assert (resumed["used"], resumed["phase"]) == (1, "working")
    assert resumed["session"] == "review-session"
    assert replies.sessions == [None]


def test_one_time_response_write_failure_keeps_call_resumable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    archive, source, host = setup_review(tmp_path)
    resolved = dict(FINDING, disposition="resolved", explanation="Upload removed.")
    replies = Replies([[FINDING], [resolved]])
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    original_write = Archive.write
    failures: list[str] = []

    def fail_once(self: Archive, name: str, value: dict[str, Any]) -> None:
        if name.endswith(".response.json") and not failures:
            failures.append(name)
            raise ReviewError(
                f"write record failed: one transient failure. Got: {name!r}"
            )
        original_write(self, name, value)

    with monkeypatch.context() as context:
        context.setattr(Archive, "write", fail_once)
        with pytest.raises(ReviewError, match="write record failed"):
            engine.query(archive, source, host, replies)
    state = archive.load()
    assert state["phase"] == "pending"
    assert state["call"]["prefix"] == "01-closing"
    assert state["checked"] is None
    assert not archive.path("01-closing.response.json").exists()
    assert archive.read("01-closing.raw.json")["final_message"]
    resumed = engine.resume(archive)
    assert resumed["phase"] == "between"
    assert resumed["checked_response"] == "01-closing.response.json"
    note = tmp_path / "complete.md"
    note.write_text("Upload removed; no held concerns or user decisions remain.")
    assert engine.finish(archive, "complete", note)["candidate_checked"] is True
    assert replies.sessions == [None, "review-session"]


def test_resume_survives_its_own_one_time_save_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import os

    archive, source, host = setup_review(tmp_path)
    replies = Replies([[FINDING]])
    engine.begin(archive)
    original_replace = os.replace

    def fail_after_capture(src: str, dst: Path) -> None:
        if archive.path("01-opening.raw.json").exists():
            raise OSError("persistent failure writing progress")
        original_replace(src, dst)

    with monkeypatch.context() as context:
        context.setattr(os, "replace", fail_after_capture)
        with pytest.raises(ReviewError, match="save progress failed"):
            engine.query(archive, source, host, replies)
    assert archive.load()["phase"] == "pending"
    failures: list[str] = []

    def fail_once(src: str, dst: Path) -> None:
        if not failures:
            failures.append("one transient failure during resume")
            raise OSError(failures[0])
        original_replace(src, dst)

    with monkeypatch.context() as context:
        context.setattr(os, "replace", fail_once)
        with pytest.raises(ReviewError, match="save progress failed"):
            engine.resume(archive)
    state = archive.load()
    assert state["phase"] == "pending"
    assert state["call"]["prefix"] == "01-opening"
    assert engine.resume(archive)["phase"] == "working"
    assert replies.sessions == [None]


def _complete_one_round(tmp_path: Path) -> tuple[Archive, Path]:
    archive, source, host = setup_review(tmp_path)
    resolved = dict(FINDING, disposition="resolved", explanation="Upload removed.")
    replies = Replies([[FINDING], [resolved]])
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    engine.query(archive, source, host, replies)
    note = tmp_path / "note.md"
    note.write_text("Upload removed; no held concerns or user decisions remain.")
    return archive, note


def test_finish_refuses_when_checked_reviewer_record_is_missing(
    tmp_path: Path,
) -> None:
    archive, note = _complete_one_round(tmp_path)
    raw = archive.path("01-closing.raw.json")
    raw.rename(raw.with_suffix(".aside"))
    for outcome in ("complete", "decision"):
        with pytest.raises(ReviewError, match="reviewer record .* is missing"):
            engine.finish(archive, outcome, note)
    assert not archive.path("result.json").exists()
    raw.with_suffix(".aside").rename(raw)
    result = engine.finish(archive, "complete", note)
    assert result["reviewer_record"] == "01-closing.raw.json"
    assert archive.path(result["reviewer_record"]).is_file()


def test_finish_refuses_when_reviewer_record_disagrees_with_response(
    tmp_path: Path,
) -> None:
    archive, note = _complete_one_round(tmp_path)
    raw = archive.path("01-closing.raw.json")
    record = json.loads(raw.read_text())
    reply = json.loads(record["final_message"])
    reply["review_notes"] = "Edited after the fact."
    record["final_message"] = json.dumps(reply)
    raw.write_text(json.dumps(record))
    with pytest.raises(ReviewError, match="reviewer record disagrees"):
        engine.finish(archive, "complete", note)
    raw.write_text("not json")
    with pytest.raises(ReviewError, match="read record failed"):
        engine.finish(archive, "complete", note)


@pytest.mark.parametrize(
    ("original", "candidate", "expected_hunk"),
    (
        (
            "old sentence",
            "new sentence",
            (
                "@@ -1 +1 @@\n-old sentence\n\\ No newline at end of file\n"
                "+new sentence\n\\ No newline at end of file\n"
            ),
        ),
        (
            "old sentence\n",
            "new sentence",
            "@@ -1 +1 @@\n-old sentence\n+new sentence\n\\ No newline at end of file\n",
        ),
        (
            "old sentence",
            "new sentence\n",
            "@@ -1 +1 @@\n-old sentence\n\\ No newline at end of file\n+new sentence\n",
        ),
        (
            "old\nsame",
            "new\nsame",
            "@@ -1,2 +1,2 @@\n-old\n+new\n same\n\\ No newline at end of file\n",
        ),
        (
            "old sentence\n",
            "new sentence\n",
            "@@ -1 +1 @@\n-old sentence\n+new sentence\n",
        ),
    ),
)
def test_diff_marks_missing_final_newlines(
    tmp_path: Path, original: str, candidate: str, expected_hunk: str
) -> None:
    repo = tmp_path / "target"
    repo.mkdir()
    source = repo / "draft.md"
    source.write_bytes(original.encode())
    revised = tmp_path / "candidate.md"
    revised.write_bytes(candidate.encode())
    host = tmp_path / "host.md"
    host.write_text("Goal: say the new sentence.\n")
    archive = Archive.create(tmp_path / "review", repo, source, 3)
    replies = Replies([[], []])
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    engine.query(archive, revised, host, replies)
    engine.finish(archive, "complete", host)
    header = "--- submitted\n+++ checked-candidate\n"
    assert archive.text("changes.diff") == header + expected_hunk
    assert archive.path(archive.load()["checked"]).read_bytes() == candidate.encode()


def test_one_time_raw_capture_failure_keeps_call_resumable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import os

    archive, source, host = setup_review(tmp_path)
    replies = Replies([[FINDING]])
    engine.begin(archive)
    original_fsync = os.fsync
    failures: list[str] = []

    def fail_once(descriptor: int) -> None:
        if archive.path("01-opening.raw.json").exists() and not failures:
            failures.append("one transient failure syncing the raw record")
            raise OSError(failures[0])
        original_fsync(descriptor)

    with monkeypatch.context() as context:
        context.setattr(os, "fsync", fail_once)
        with pytest.raises(ReviewError, match="write record failed"):
            engine.query(archive, source, host, replies)
    state = archive.load()
    assert state["phase"] == "pending"
    assert state["call"]["prefix"] == "01-opening"
    assert archive.read("01-opening.raw.json")["exit_code"] == 0
    resumed = engine.resume(archive)
    assert (resumed["used"], resumed["phase"]) == (1, "working")
    assert replies.sessions == [None]


def test_finish_refuses_when_reviewer_record_fails_replay(tmp_path: Path) -> None:
    archive, note = _complete_one_round(tmp_path)
    raw = archive.path("01-closing.raw.json")
    record = json.loads(raw.read_text())
    record["exit_code"] = 23
    raw.write_text(json.dumps(record))
    with pytest.raises(ReviewError, match="failed replay validation"):
        engine.finish(archive, "complete", note)
    assert not archive.path("result.json").exists()


def _fail_request_record_sync(
    archive: Archive, prefix: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Make the next request-record write leave its file on disk and raise."""
    import os

    original_fsync = os.fsync

    def fail_request_sync(descriptor: int) -> None:
        if archive.path(f"{prefix}.request.json").exists():
            raise OSError("simulated failure syncing the request record")
        original_fsync(descriptor)

    monkeypatch.setattr(os, "fsync", fail_request_sync)


def test_request_record_failure_before_call_renders_failed_ending(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive, source, host = setup_review(tmp_path)
    replies = Replies([[FINDING]])
    engine.begin(archive)
    with monkeypatch.context() as context:
        _fail_request_record_sync(archive, "01-opening", context)
        with pytest.raises(ReviewError, match="write record failed"):
            engine.query(archive, source, host, replies)
    state = archive.load()
    assert (state["phase"], state["call"], state["used"]) == ("opening", None, 1)
    assert archive.path("01-opening.request.json").is_file()
    assert not archive.path("01-opening.raw.json").exists()
    assert replies.sessions == []
    note = tmp_path / "failed.md"
    note.write_text("The request record failed to save before any reviewer call.")
    result = engine.finish(archive, "failed", note)
    assert result["outcome"] == "failed"
    assert result["candidate_checked"] is False
    assert result["candidate"] == str(archive.path(state["original"]))
    assert result["rounds_used"] == 1
    assert "01-opening.request.json" in result["failure"]
    assert "no call recorded" in result["failure"]
    assert archive.path("changes.diff").is_file()
    assert f"Recorded failure: {result['failure']}" in archive.text("result.md")


def _fail_pending_save_in_round_two(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Archive, Path, Path, Replies, str]:
    """Check round one, then lose the pending save before round two's call."""
    import os

    archive, source, host = setup_review(tmp_path)
    resolved = dict(FINDING, disposition="resolved", explanation="Upload removed.")
    replies = Replies([[FINDING], [resolved]])
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    engine.query(archive, source, host, replies)
    checked = archive.load()["checked"]
    engine.begin(archive)
    candidate = tmp_path / "candidate.md"
    candidate.write_text("Keep data local. Search local files.\n")
    original_replace = os.replace

    def fail_pending_save(src: str, dst: Path) -> None:
        if archive.path("02-closing.request.json").exists():
            raise OSError("simulated failure saving the pending state")
        original_replace(src, dst)

    with monkeypatch.context() as context:
        context.setattr(os, "replace", fail_pending_save)
        with pytest.raises(ReviewError, match="save progress failed"):
            engine.query(archive, candidate, host, replies)
    state = archive.load()
    assert (state["phase"], state["call"], state["used"]) == ("working", None, 2)
    assert archive.path("02-closing.request.json").is_file()
    assert not archive.path("02-closing.raw.json").exists()
    return archive, candidate, host, replies, checked


def test_pending_save_failure_after_checked_round_renders_failed_ending(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive, _candidate, _host, replies, checked = _fail_pending_save_in_round_two(
        tmp_path, monkeypatch
    )
    assert replies.sessions == [None, "review-session"]
    note = tmp_path / "failed.md"
    note.write_text("Progress failed to save before the round-two closing call.")
    result = engine.finish(archive, "failed", note)
    assert result["outcome"] == "failed"
    assert result["candidate_checked"] is True
    assert result["candidate"] == str(archive.path(checked))
    assert result["rounds_used"] == 2
    assert result["reviewer_record"] == "01-closing.raw.json"
    assert "02-closing.request.json" in result["failure"]
    assert "no call recorded" in result["failure"]


def test_failed_ending_before_call_leaves_other_operations_unchanged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive, candidate, host, replies, _checked = _fail_pending_save_in_round_two(
        tmp_path, monkeypatch
    )
    progress = archive.path("state.json").read_bytes()
    assert engine.resume(archive)["phase"] == "working"
    with pytest.raises(ReviewError, match="request already saved"):
        engine.query(archive, candidate, host, replies)
    with pytest.raises(ReviewError, match="finish or resume the started round"):
        engine.begin(archive)
    note = tmp_path / "note.md"
    note.write_text("No closing check happened in round two.")
    with pytest.raises(ReviewError, match="no successful closing check"):
        engine.finish(archive, "complete", note)
    with pytest.raises(ReviewError, match="between-round boundary"):
        engine.finish(archive, "exhausted", note)
    engine.finish(archive, "failed", note)
    assert archive.path("state.json").read_bytes() == progress
    assert replies.sessions == [None, "review-session"]


def test_unreadable_request_record_before_call_still_renders_failed_ending(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive, source, host = setup_review(tmp_path)
    replies = Replies([[FINDING]])
    engine.begin(archive)
    with monkeypatch.context() as context:
        _fail_request_record_sync(archive, "01-opening", context)
        with pytest.raises(ReviewError, match="write record failed"):
            engine.query(archive, source, host, replies)
    archive.path("01-opening.request.json").write_text("{")
    with pytest.raises(ReviewError, match="read record failed"):
        archive.read("01-opening.request.json")
    note = tmp_path / "failed.md"
    note.write_text("The request record is truncated; no reviewer call was made.")
    result = engine.finish(archive, "failed", note)
    assert result["outcome"] == "failed"
    assert "01-opening.request.json" in result["failure"]
    assert replies.sessions == []


@pytest.mark.parametrize(
    ("case", "phase"),
    (
        ("fresh", "between"),
        ("checked", "between"),
        ("opening", "opening"),
        ("working", "working"),
        ("working_round_two", "working"),
    ),
)
def test_failed_ending_refused_without_a_recorded_failure(
    tmp_path: Path, case: str, phase: str
) -> None:
    archive, source, host = setup_review(tmp_path)
    replies = Replies([[FINDING], [FINDING]])
    if case != "fresh":
        engine.begin(archive)
    if case in {"checked", "working", "working_round_two"}:
        engine.query(archive, source, host, replies)
    if case in {"checked", "working_round_two"}:
        engine.query(archive, source, host, replies)
    if case == "working_round_two":
        engine.begin(archive)
    assert archive.load()["phase"] == phase
    note = tmp_path / "note.md"
    note.write_text("Nothing failed; a started round is not a failure.")
    with pytest.raises(ReviewError, match="no failed or incomplete call is recorded"):
        engine.finish(archive, "failed", note)
    assert not archive.path("result.json").exists()


def _decision_note(tmp_path: Path) -> Path:
    note = tmp_path / "decision.md"
    note.write_text(
        "JP must choose whether the local-only constraint may change; the models cannot settle that. The saved round state is disclosed below."
    )
    return note


@pytest.mark.parametrize(
    "case",
    ("opening_request_failure", "round_two_pending_save_failure", "unreadable_request"),
)
def test_decision_discloses_pre_call_failure_like_failed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, case: str
) -> None:
    if case == "round_two_pending_save_failure":
        archive, _candidate, _host, replies, checked = _fail_pending_save_in_round_two(
            tmp_path, monkeypatch
        )
        expected = (checked, "working", 2, "02-closing.request.json")
    else:
        archive, source, host = setup_review(tmp_path)
        replies = Replies([[FINDING]])
        engine.begin(archive)
        with monkeypatch.context() as context:
            _fail_request_record_sync(archive, "01-opening", context)
            with pytest.raises(ReviewError, match="write record failed"):
                engine.query(archive, source, host, replies)
        if case == "unreadable_request":
            archive.path("01-opening.request.json").write_text("{")
        expected = (archive.load()["original"], "opening", 1, "01-opening.request.json")
    candidate, phase, used, request = expected
    calls = list(replies.sessions)
    progress = archive.path("state.json").read_bytes()
    note = _decision_note(tmp_path)
    failed = engine.finish(archive, "failed", note)
    result = engine.finish(archive, "decision", note)
    assert result["outcome"] == "decision"
    assert result["phase"] == phase
    assert result["failure"] == failed["failure"]
    assert request in result["failure"]
    assert "no call recorded" in result["failure"]
    assert result["pending_or_failed_call"] is None
    assert result["rounds_used"] == used
    assert result["candidate"] == str(archive.path(candidate))
    assert result["candidate_checked"] is (case == "round_two_pending_save_failure")
    saved = json.loads(archive.text("result.json"))
    assert (saved["outcome"], saved["phase"], saved["failure"]) == (
        "decision",
        phase,
        result["failure"],
    )
    rendered = archive.text("result.md")
    assert "# Review result: decision" in rendered
    assert f"Recorded failure: {result['failure']}" in rendered
    assert archive.path("state.json").read_bytes() == progress
    assert replies.sessions == calls


@pytest.mark.parametrize(
    ("case", "used", "phase"),
    (
        ("before_first_call", 1, "opening"),
        ("after_opening_reply", 1, "working"),
        ("follow_up_after_check", 2, "working"),
        ("final_allowed_round", 3, "working"),
    ),
)
def test_decision_renders_while_a_round_is_open_and_discloses_it(
    tmp_path: Path, case: str, used: int, phase: str
) -> None:
    archive, source, host = setup_review(tmp_path)
    replies = Replies([[FINDING]] * 4)
    engine.begin(archive)
    if case != "before_first_call":
        engine.query(archive, source, host, replies)
    for _round in range(2, used + 1):
        engine.query(archive, source, host, replies)
        engine.begin(archive)
    state = archive.load()
    assert (state["phase"], state["used"]) == (phase, used)
    checked = state["checked"]
    calls = list(replies.sessions)
    progress = archive.path("state.json").read_bytes()
    result = engine.finish(archive, "decision", _decision_note(tmp_path))
    assert (result["outcome"], result["phase"], result["rounds_used"]) == (
        "decision",
        phase,
        used,
    )
    assert result["failure"] is None
    assert result["pending_or_failed_call"] is None
    assert result["candidate_checked"] is (checked is not None)
    assert result["candidate"] == str(archive.path(checked or state["original"]))
    assert json.loads(archive.text("result.json"))["phase"] == phase
    rendered = archive.text("result.md")
    assert f"Saved phase: {phase}." in rendered
    assert (
        f"Round {used} remains open; its closing check is not recorded in progress."
        in rendered
    )
    assert archive.path("state.json").read_bytes() == progress
    assert replies.sessions == calls


def _leave_call_pending(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, kind: str, raw_present: bool
) -> tuple[Archive, Replies, str, str | None]:
    """Leave a call pending: a one-time progress-save failure after capture, or an interruption before capture."""
    import os

    archive, source, host = setup_review(tmp_path)
    interruption = RuntimeError("simulated interruption during the reviewer call")
    if kind == "opening":
        replies = Replies([[FINDING] if raw_present else interruption])
        prefix = "01-opening"
    else:
        resolved = dict(FINDING, disposition="resolved", explanation="Upload removed.")
        replies = Replies(
            [[FINDING], [resolved], [resolved] if raw_present else interruption]
        )
        prefix = "02-closing"
    engine.begin(archive)
    if kind == "closing":
        engine.query(archive, source, host, replies)
        engine.query(archive, source, host, replies)
        engine.begin(archive)
    checked = archive.load()["checked"]
    if raw_present:
        original_replace = os.replace
        failures: list[str] = []

        def fail_once(src: str, dst: Path) -> None:
            if archive.path(f"{prefix}.raw.json").exists() and not failures:
                failures.append("one transient failure writing progress")
                raise OSError(failures[0])
            original_replace(src, dst)

        with monkeypatch.context() as context:
            context.setattr(os, "replace", fail_once)
            with pytest.raises(ReviewError, match="save progress failed"):
                engine.query(archive, source, host, replies)
    else:
        with pytest.raises(RuntimeError, match="simulated interruption"):
            engine.query(archive, source, host, replies)
    state = archive.load()
    assert (state["phase"], state["call"]["prefix"]) == ("pending", prefix)
    assert archive.path(f"{prefix}.raw.json").exists() is raw_present
    return archive, replies, prefix, checked


@pytest.mark.parametrize("raw_present", (True, False))
@pytest.mark.parametrize("kind", ("opening", "closing"))
def test_decision_at_pending_discloses_the_call_and_leaves_resume_intact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, kind: str, raw_present: bool
) -> None:
    archive, replies, prefix, checked = _leave_call_pending(
        tmp_path, monkeypatch, kind, raw_present
    )
    used = 1 if kind == "opening" else 2
    calls = list(replies.sessions)
    progress = archive.path("state.json").read_bytes()
    result = engine.finish(archive, "decision", _decision_note(tmp_path))
    assert (result["outcome"], result["phase"], result["rounds_used"]) == (
        "decision",
        "pending",
        used,
    )
    assert result["pending_or_failed_call"]["prefix"] == prefix
    assert result["failure"] is None
    assert result["candidate_checked"] is (kind == "closing")
    assert result["candidate"] == str(
        archive.path(checked if kind == "closing" else archive.load()["original"])
    )
    rendered = archive.text("result.md")
    assert "Saved phase: pending." in rendered
    assert f"Pending or failed call: {prefix}." in rendered
    assert f"Round {used} remains open" in rendered
    assert archive.path("state.json").read_bytes() == progress
    assert replies.sessions == calls
    if raw_present:
        resumed = engine.resume(archive)
        assert resumed["phase"] == ("working" if kind == "opening" else "between")
        if kind == "closing":
            assert resumed["checked_response"] == "02-closing.response.json"
    else:
        with pytest.raises(
            ReviewError, match="reviewer response is missing; no automatic retry"
        ):
            engine.resume(archive)
        assert archive.path("state.json").read_bytes() == progress
    assert replies.sessions == calls


@pytest.mark.parametrize(
    "case", ("malformed_opening", "closing_timeout_no_raw", "malformed_closing")
)
def test_decision_at_failed_discloses_the_failure_and_leaves_recovery_intact(
    tmp_path: Path, case: str
) -> None:
    from cross_model_runtime.codex_transport import CodexTransportError

    archive, source, host = setup_review(tmp_path)
    if case == "malformed_opening":
        replies = Replies(["not JSON"])
        prefix, used = "01-opening", 1
    else:
        failure: Any = "not JSON"
        if case == "closing_timeout_no_raw":
            failure = CodexTransportError(
                "review failed: simulated timeout. Got: 'closing'"
            )
        replies = Replies([[FINDING], [FINDING], failure])
        prefix, used = "02-closing", 2
    engine.begin(archive)
    if case != "malformed_opening":
        engine.query(archive, source, host, replies)
        engine.query(archive, source, host, replies)
        engine.begin(archive)
    with pytest.raises(CodexTransportError):
        engine.query(archive, source, host, replies)
    state = archive.load()
    assert (state["phase"], state["call"]["prefix"]) == ("failed", prefix)
    assert archive.path(f"{prefix}.raw.json").exists() is (
        case != "closing_timeout_no_raw"
    )
    calls = list(replies.sessions)
    progress = archive.path("state.json").read_bytes()
    result = engine.finish(archive, "decision", _decision_note(tmp_path))
    assert (result["outcome"], result["phase"], result["rounds_used"]) == (
        "decision",
        "failed",
        used,
    )
    assert result["pending_or_failed_call"]["prefix"] == prefix
    assert result["failure"] == state["error"]
    assert result["candidate_checked"] is (case != "malformed_opening")
    assert result["candidate"] == str(
        archive.path(state["checked"] or state["original"])
    )
    rendered = archive.text("result.md")
    assert "Saved phase: failed." in rendered
    assert f"Pending or failed call: {prefix}." in rendered
    assert f"Recorded failure: {state['error']}" in rendered
    label = (
        "Last checked candidate"
        if result["candidate_checked"]
        else "Submitted version; no successful closing check recorded in progress"
    )
    assert f"{label}: [" in rendered
    assert archive.path("state.json").read_bytes() == progress
    with pytest.raises(ReviewError, match="recorded failure needs a user decision"):
        engine.resume(archive)
    empty = tmp_path / "empty.md"
    empty.write_text(" \n")
    with pytest.raises(ReviewError, match="authorization text is required"):
        engine.continue_after_failure(archive, empty)
    authorization = tmp_path / "authorization.md"
    authorization.write_text("JP: authorize continuation after this failed call.")
    if case == "malformed_closing":
        assert (
            engine.continue_after_failure(archive, authorization)["phase"] == "between"
        )
    else:
        with pytest.raises(ReviewError):
            engine.continue_after_failure(archive, authorization)
        assert archive.path("state.json").read_bytes() == progress
    assert replies.sessions == calls


def test_between_round_endings_carry_phase_and_unchanged_failure(
    tmp_path: Path,
) -> None:
    from cross_model_runtime.codex_transport import CodexTransportError

    archive, note = _complete_one_round(tmp_path)
    result = engine.finish(archive, "complete", note)
    assert (result["phase"], result["failure"], result["continuations"]) == (
        "between",
        None,
        [],
    )
    rendered = archive.text("result.md")
    assert "Saved phase: between." in rendered
    assert "remains open" not in rendered
    assert "Pending or failed call: none." in rendered

    (tmp_path / "second").mkdir()
    archive, source, host = setup_review(tmp_path / "second", limit=2)
    replies = Replies([[FINDING], [FINDING], "not JSON"])
    engine.begin(archive)
    engine.query(archive, source, host, replies)
    engine.query(archive, source, host, replies)
    engine.begin(archive)
    with pytest.raises(CodexTransportError):
        engine.query(archive, source, host, replies)
    authorization = tmp_path / "continue.md"
    authorization.write_text("JP: authorize continuation; no extra rounds granted.")
    engine.continue_after_failure(archive, authorization)
    result = engine.finish(archive, "exhausted", note)
    assert (result["phase"], result["failure"]) == ("between", None)
    assert result["continuations"][0]["failed_call"] == "02-closing"
    rendered = archive.text("result.md")
    assert "Saved phase: between." in rendered
    assert "remains open" not in rendered
    assert "Failed rounds followed by authorized continuation: 2." in rendered
