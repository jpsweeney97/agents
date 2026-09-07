import json
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
