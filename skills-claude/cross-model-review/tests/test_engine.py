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
