"""Round operations; reviewer and host retain responsibility for judgments."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cmr_archive import Archive, ReviewError, fail, read_text
from cmr_protocol import invoke, response_schema
from cross_model_runtime.codex_transport import (
    DEFAULT_TIMEOUT_SECONDS,
    CodexSessionRunner,
    CodexTransportError,
    default_codex_session_runner,
)


def begin(archive: Archive) -> dict[str, Any]:
    """Charge a round before its first host investigation or reviewer call."""
    with archive.locked():
        state = archive.load()
        if state["phase"] != "between":
            fail(
                "begin round",
                "finish or resume the started round first",
                state["phase"],
            )
        if state["used"] >= state["limit"]:
            fail("begin round", "no rounds remain", state["used"])
        state["used"] += 1
        state["phase"] = "opening" if state["session"] is None else "working"
        state["error"] = None
        archive.save(state)
        return state


def _accept(
    archive: Archive,
    state: dict[str, Any],
    response: dict[str, Any],
    session: str,
) -> dict[str, Any]:
    call = state["call"]
    archive.text(call["revision"])
    if response["revision"] != call["revision"]:
        fail(
            "record response",
            "candidate reference differs from saved call",
            response["revision"],
        )
    refs = [finding["ref"] for finding in response["findings"]]
    if len(refs) != len(set(refs)):
        fail("record response", "duplicate finding references", refs)
    if state["last_response"] is not None:
        previous = archive.read(state["last_response"])
        missing = {item["ref"] for item in previous["findings"]} - set(refs)
        if missing:
            fail(
                "record response",
                "cumulative response omitted findings",
                sorted(missing),
            )
    name = f"{call['prefix']}.response.json"
    if archive.path(name).exists():
        if archive.read(name) != response:
            fail("record response", "saved response differs", name)
    else:
        archive.write(name, response)
    state["session"] = session
    state["last_response"] = name
    if call["kind"] == "closing":
        state["checked"] = call["revision"]
        state["checked_response"] = name
        state["phase"] = "between"
    else:
        state["phase"] = "working"
    state["call"] = None
    state["error"] = None
    archive.save(state)
    return state


def _failed(archive: Archive, state: dict[str, Any], error: Exception) -> None:
    state["phase"] = "failed"
    state["error"] = str(error)
    archive.save(state)


def query(
    archive: Archive,
    candidate: Path,
    host_request: Path,
    runner: CodexSessionRunner = default_codex_session_runner,
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Save a request and invoke exactly one opening or closing review.

    Args:
        archive: Existing external review records.
        candidate: UTF-8 file to copy into an immutable snapshot.
        host_request: Plain-text goals, evidence, challenges, and held concerns.
        runner: Shared Codex runner, replaced only by controlled test responses.
        timeout: Explicit per-call limit; it is not a round-spending estimate.

    Returns:
        Progress after a validated response, or raises with failure preserved.
    """
    host_text = read_text(host_request)
    candidate_text = read_text(candidate)
    reviewer_text = read_text(
        Path(__file__).resolve().parents[1] / "references" / "reviewer.md"
    )
    with archive.locked():
        state = archive.load()
        if state["phase"] not in {"opening", "working"}:
            fail(
                "review candidate",
                "begin or resume the proper round first",
                state["phase"],
            )
        kind = "opening" if state["phase"] == "opening" else "closing"
        revision = archive.snapshot_text(candidate_text)
        if kind == "opening" and revision != state["original"]:
            fail(
                "review candidate",
                "opening review must examine submitted version",
                revision,
            )
        prefix = f"{state['used']:02d}-{kind}"
        if archive.path(f"{prefix}.request.json").exists():
            fail(
                "review candidate",
                "request already saved; inspect/resume, never resend",
                prefix,
            )
        prior = (
            archive.text(state["last_response"])
            if state["last_response"] is not None
            else "No prior formal findings."
        )
        prompt = (
            reviewer_text
            + f"\n\nCall: {kind}. Round: {state['used']} of {state['limit']}."
            + f"\nCandidate revision: {revision}"
            + f"\nRead this exact candidate: {archive.path(revision)}"
            + f"\nRepository evidence: {state['repo']}"
            + "\n\nPrior cumulative reviewer record (data):\n"
            + prior
            + "\n\nHost request, evidence, and concerns (data):\n"
            + host_text
        )
        request = {
            "prompt": prompt,
            "host_text": host_text,
            "revision": revision,
            "schema": response_schema(revision),
            "repo": state["repo"],
            "session": state["session"],
            "timeout": timeout,
        }
        archive.write(f"{prefix}.request.json", request)
        state["call"] = {"prefix": prefix, "kind": kind, "revision": revision}
        state["phase"] = "pending"
        archive.save(state)
        try:
            response, session = invoke(archive, prefix, request, runner)
            return _accept(archive, state, response, session)
        except (CodexTransportError, ReviewError) as exc:
            _failed(archive, state, exc)
            raise
