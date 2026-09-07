"""Reviewer request shape and raw capture through the shared transport."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from cmr_archive import Archive
from cross_model_runtime.codex_transport import (
    CodexResult,
    CodexSessionRunner,
    ask_codex_in_session,
    default_codex_session_runner,
    start_codex_session,
)


def response_schema(revision: str) -> dict[str, Any]:
    """Require only revision identity, cumulative declarations, and review prose."""
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["revision", "findings", "review_notes"],
        "properties": {
            "revision": {"type": "string", "enum": [revision]},
            "review_notes": {"type": "string", "minLength": 1},
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["ref", "disposition", "material", "explanation"],
                    "properties": {
                        "ref": {"type": "string", "minLength": 1},
                        "disposition": {
                            "type": "string",
                            "enum": ["resolved", "withdrawn", "standing"],
                        },
                        "material": {"type": "boolean"},
                        "explanation": {"type": "string", "minLength": 1},
                    },
                },
            },
        },
    }


def invoke(
    archive: Archive,
    prefix: str,
    request: dict[str, Any],
    runner: CodexSessionRunner = default_codex_session_runner,
    *,
    replay: bool = False,
) -> tuple[dict[str, Any], str]:
    """Capture the actual returned result before shared validation can raise.

    Args:
        archive: Destination for this review's records.
        prefix: Unique round and opening/closing identifier.
        request: Saved prompt, schema, repository, session, and timeout.
        runner: External call interface; controlled only in unit tests.
        replay: Validate already-saved raw bytes without invoking a model.

    Returns:
        The validated reviewer object and its session identifier.
    """

    def captured(
        prompt: str,
        *,
        output_schema: dict[str, Any],
        repo_root: str,
        timeout_seconds: float,
        resume_thread_id: str | None,
    ) -> CodexResult:
        if replay:
            raw = archive.read(f"{prefix}.raw.json")
            return CodexResult(
                raw["final_message"],
                raw["exit_code"],
                raw["stdout"],
                raw["stderr"],
                tuple(raw["argv"]),
            )
        result = runner(
            prompt,
            output_schema=output_schema,
            repo_root=repo_root,
            timeout_seconds=timeout_seconds,
            resume_thread_id=resume_thread_id,
        )
        archive.write(f"{prefix}.raw.json", asdict(result))
        return result

    arguments = {
        "output_schema": request["schema"],
        "repo_root": request["repo"],
        "timeout_seconds": request["timeout"],
        "runner": captured,
    }
    if request["session"] is None:
        started = start_codex_session(request["prompt"], **arguments)
        return started.response, started.thread_id
    response = ask_codex_in_session(
        request["session"],
        request["prompt"],
        **arguments,
    )
    return response, request["session"]
