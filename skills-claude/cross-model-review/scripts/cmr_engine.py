"""Round operations; reviewer and host retain responsibility for judgments."""

from __future__ import annotations

import difflib
import json
from pathlib import Path
from typing import Any

from cmr_archive import Archive, RecordError, ReviewError, fail, read_text
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


def _previous_refs(archive: Archive, state: dict[str, Any]) -> set[str]:
    """Collect finding references from the last valid reviewer response."""
    if state["last_response"] is None:
        return set()
    return {item["ref"] for item in archive.read(state["last_response"])["findings"]}


def _validate(
    call: dict[str, Any],
    response: dict[str, Any],
    previous_refs: set[str],
) -> None:
    """Reject a reviewer reply that misnames the candidate or drops findings.

    Every failure here originates in the reviewer's reply, so callers record
    it as a failed call. Local record problems belong to ``_record``.
    """
    if response["revision"] != call["revision"]:
        fail(
            "record response",
            "candidate reference differs from saved call",
            response["revision"],
        )
    refs = [finding["ref"] for finding in response["findings"]]
    if len(refs) != len(set(refs)):
        fail("record response", "duplicate finding references", refs)
    missing = previous_refs - set(refs)
    if missing:
        fail(
            "record response",
            "cumulative response omitted findings",
            sorted(missing),
        )


def _record(
    archive: Archive,
    state: dict[str, Any],
    response: dict[str, Any],
    session: str,
) -> dict[str, Any]:
    """Persist a validated reply; a local failure here leaves the call pending.

    The response record is written before progress, so a failed write or a
    failed progress save leaves the raw reply and the pending call in place
    for ``resume`` to replay without another model call.
    """
    call = state["call"]
    archive.text(call["revision"])
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
    """Record a failed reviewer call; a RecordError never reaches here."""
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
        previous_refs = _previous_refs(archive, state)
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
            _validate(state["call"], response, previous_refs)
        except RecordError:
            raise
        except (CodexTransportError, ReviewError) as exc:
            _failed(archive, state, exc)
            raise
        return _record(archive, state, response, session)


def resume(archive: Archive) -> dict[str, Any]:
    """Continue only from saved records; this operation never calls a model."""
    with archive.locked():
        state = archive.load()
        if state["phase"] == "failed":
            fail(
                "resume review",
                "recorded failure needs a user decision",
                state["error"],
            )
        if state["phase"] != "pending":
            return state
        call = state["call"]
        if not isinstance(call, dict):
            fail("resume review", "pending call identity is missing", call)
        prefix = call["prefix"]
        if not archive.path(f"{prefix}.raw.json").is_file():
            fail(
                "resume review",
                "reviewer response is missing; no automatic retry",
                prefix,
            )
        request = archive.read(f"{prefix}.request.json")
        previous_refs = _previous_refs(archive, state)
        try:
            response, session = invoke(archive, prefix, request, replay=True)
            _validate(call, response, previous_refs)
        except RecordError:
            raise
        except (CodexTransportError, ReviewError) as exc:
            _failed(archive, state, exc)
            raise
        return _record(archive, state, response, session)


def _lines(text: str) -> list[str]:
    """Split on newline only, so only the final line can lack its terminator."""
    parts = text.split("\n")
    lines = [part + "\n" for part in parts[:-1]]
    if parts[-1]:
        lines.append(parts[-1])
    return lines


def _unified_diff(original: str, candidate: str) -> str:
    """Render a unified diff that stays valid when a final newline is absent."""
    rendered: list[str] = []
    for line in difflib.unified_diff(
        _lines(original),
        _lines(candidate),
        fromfile="submitted",
        tofile="checked-candidate",
    ):
        rendered.append(line)
        if not line.endswith("\n"):
            rendered.append("\n\\ No newline at end of file\n")
    return "".join(rendered)


def _verify_checked_record(
    archive: Archive, state: dict[str, Any], raw_name: str
) -> None:
    """Require the checked candidate's raw reviewer reply to replay and match.

    The captured reply is re-validated through the transport's own replay
    path (exit status, JSON, schema) and must equal the accepted response
    naming the checked candidate. Nothing is reconstructed.
    """
    if not archive.path(raw_name).is_file():
        fail(
            "finish review",
            "reviewer record for the checked candidate is missing",
            raw_name,
        )
    prefix = raw_name.removesuffix(".raw.json")
    accepted = archive.read(state["checked_response"])
    try:
        request = archive.read(f"{prefix}.request.json")
        replied, _session = invoke(archive, prefix, request, replay=True)
    except (CodexTransportError, ReviewError) as exc:
        fail("finish review", "reviewer record failed replay validation", str(exc))
    if replied != accepted or accepted.get("revision") != state["checked"]:
        fail(
            "finish review",
            "reviewer record disagrees with the accepted response",
            raw_name,
        )


def _failure_before_call(archive: Archive, state: dict[str, Any]) -> str | None:
    """Name a local record failure that left a saved request with no call.

    The detectable state is the current round's request record on disk with
    no raw reviewer record and no call identity, at phase ``opening`` or
    ``working``. Only file existence is tested, so a partially written
    request record still gets an ending.
    """
    if state["phase"] not in {"opening", "working"} or state["call"] is not None:
        return None
    kind = "opening" if state["phase"] == "opening" else "closing"
    prefix = f"{state['used']:02d}-{kind}"
    request = f"{prefix}.request.json"
    if not archive.path(request).is_file():
        return None
    if archive.path(f"{prefix}.raw.json").exists():
        return None
    return (
        "local record failure before the reviewer call: "
        f"{request} saved, no call recorded"
    )


def finish(archive: Archive, outcome: str, host_note: Path) -> dict[str, Any]:
    """Render the host's declared ending; do not adjudicate its reasoning."""
    note = read_text(host_note)
    if outcome not in {"complete", "decision", "exhausted", "failed"}:
        fail("finish review", "unknown ending", outcome)
    if not note.strip():
        fail("finish review", "an evidence and limitations note is required", host_note)
    with archive.locked():
        state = archive.load()
        response = (
            archive.read(state["last_response"])
            if state["last_response"] is not None
            else None
        )
        if outcome == "complete":
            if (
                state["phase"] != "between"
                or state["checked"] is None
                or state["checked_response"]
                != f"{state['used']:02d}-closing.response.json"
            ):
                fail(
                    "finish review",
                    "latest round has no successful closing check",
                    state["phase"],
                )
            if any(
                finding["material"] and finding["disposition"] == "standing"
                for finding in response["findings"]
            ):
                fail(
                    "finish review",
                    "reviewer has standing material findings",
                    state["last_response"],
                )
        if outcome == "exhausted" and (
            state["used"] != state["limit"] or state["phase"] != "between"
        ):
            fail(
                "finish review",
                "allowance ending requires no remaining rounds at a between-round boundary",
                state,
            )
        before_call = _failure_before_call(archive, state)
        failure = state["error"] if state["error"] is not None else before_call
        if (
            outcome == "failed"
            and state["phase"] not in {"failed", "pending"}
            and before_call is None
        ):
            fail(
                "finish review",
                "no failed or incomplete call is recorded",
                state["phase"],
            )
        candidate = state["checked"] or state["original"]
        original_reviewer_record = None
        if state["checked_response"] is not None:
            original_reviewer_record = (
                state["checked_response"].removesuffix(".response.json") + ".raw.json"
            )
            _verify_checked_record(archive, state, original_reviewer_record)
        result = {
            "outcome": outcome,
            "phase": state["phase"],
            "candidate": str(archive.path(candidate)),
            "candidate_checked": state["checked"] is not None,
            "rounds_used": state["used"],
            "round_limit": state["limit"],
            "reviewer_record": original_reviewer_record,
            "latest_response": state["last_response"],
            "failure": failure,
            "host_note": note,
            "pending_or_failed_call": state["call"],
            "continuations": state["continuations"],
        }
        diff = _unified_diff(archive.text(state["original"]), archive.text(candidate))
        try:
            archive.path("changes.diff").write_text(diff, encoding="utf-8")
            archive.path("result.json").write_text(
                json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            label = (
                "Last checked candidate"
                if result["candidate_checked"]
                else "Submitted version; no successful closing check recorded in progress"
            )
            continued = (
                ", ".join(str(item["after_round"]) for item in state["continuations"])
                or "none"
            )
            open_round = (
                ""
                if state["phase"] == "between"
                else f"Round {state['used']} remains open; its closing check is not recorded in progress.\n\n"
            )
            call = state["call"]["prefix"] if state["call"] is not None else "none"
            archive.path("result.md").write_text(
                f"# Review result: {outcome}\n\n"
                f"{label}: [{candidate}]({archive.path(candidate)})\n\n"
                f"Rounds started: {state['used']} of {state['limit']}.\n\n"
                f"Saved phase: {state['phase']}.\n\n"
                + open_round
                + f"Pending or failed call: {call}.\n\n"
                f"Failed rounds followed by authorized continuation: {continued}. These rounds were not refunded.\n\n"
                f"Original reviewer record for this candidate: {original_reviewer_record}\n\n"
                f"Latest valid reviewer response: {state['last_response']}\n\n"
                f"Recorded failure: {failure}\n\n"
                f"[Changes from submitted version]({archive.path('changes.diff')})\n\n"
                "## Host account: changes, evidence, disagreements, and limitations\n\n"
                + note
                + "\n\nThis is a review record, not a certificate or adoption.\n",
                encoding="utf-8",
            )
        except OSError as exc:
            fail("write result", str(exc), archive.root)
        return result


def extend(archive: Archive, extra: int, authorization: Path) -> dict[str, Any]:
    """Record user-authorized extra rounds; never reset usage or repair a failure."""
    permission = read_text(authorization)
    if type(extra) is not int or extra < 1 or not permission.strip():
        fail(
            "extend review",
            "positive extra rounds and authorization text required",
            extra,
        )
    with archive.locked():
        state = archive.load()
        if state["phase"] != "between":
            fail(
                "extend review",
                "extension requires a between-round boundary",
                state["phase"],
            )
        state["limit"] += extra
        state["extensions"].append(
            {
                "after_round": state["used"],
                "extra": extra,
                "authorization": permission,
            }
        )
        archive.save(state)
        return state


def continue_after_failure(archive: Archive, authorization: Path) -> dict[str, Any]:
    """Record authorized continuation; never call a model or refund a round.

    Args:
        archive: Existing records for the review that failed.
        authorization: JP's explicit authorization for this failed call.

    Returns:
        A between-round boundary with unchanged allowance, usage, and session.
    """
    from cross_model_contracts.schema_validation import schema_violations

    permission = read_text(authorization)
    if not permission.strip():
        fail(
            "continue review", "explicit authorization text is required", authorization
        )
    with archive.locked():
        state = archive.load()
        call = state["call"]
        if (
            state["phase"] != "failed"
            or not isinstance(call, dict)
            or call.get("kind") != "closing"
        ):
            fail("continue review", "requires a failed closing call", state["phase"])
        prefix = call.get("prefix")
        revision = call.get("revision")
        if prefix != f"{state['used']:02d}-closing" or not isinstance(revision, str):
            fail("continue review", "failed call record is inconsistent", call)
        session = state["session"]
        if not isinstance(session, str) or not session.strip():
            fail("continue review", "no session id is recorded", session)

        # Read the outer captured result, not the rejected message's JSON or reason.
        raw = archive.read(f"{prefix}.raw.json")
        required = {"final_message", "exit_code", "stdout", "stderr", "argv"}
        if (
            not required <= raw.keys()
            or type(raw["exit_code"]) is not int
            or not isinstance(raw["stdout"], str)
            or not isinstance(raw["stderr"], str)
            or not isinstance(raw["argv"], list)
            or not all(isinstance(arg, str) for arg in raw["argv"])
            or (
                raw["final_message"] is not None
                and not isinstance(raw["final_message"], str)
            )
        ):
            fail("continue review", "captured raw record is corrupt", prefix)
        request = archive.read(f"{prefix}.request.json")
        if (
            request.get("session") != session
            or request.get("revision") != revision
            or request.get("repo") != state["repo"]
            or not isinstance(request.get("prompt"), str)
            or not isinstance(request.get("host_text"), str)
            or request.get("schema") != response_schema(revision)
        ):
            fail("continue review", "saved request is inconsistent", prefix)
        archive.text(revision)
        previous_name = state["last_response"]
        if not isinstance(previous_name, str):
            fail("continue review", "last valid response is missing", previous_name)
        previous = archive.read(previous_name)
        previous_revision = previous.get("revision")
        if not isinstance(previous_revision, str) or schema_violations(
            response_schema(previous_revision), previous
        ):
            fail(
                "continue review",
                "last valid response record is corrupt",
                previous_name,
            )
        archive.text(previous_revision)
        if state["checked"] is not None and (
            state["checked_response"] != previous_name
            or state["checked"] != previous_revision
        ):
            fail(
                "continue review",
                "checked candidate record is inconsistent",
                state["checked"],
            )
        if state["checked"] is None and state["checked_response"] is not None:
            fail(
                "continue review",
                "checked candidate identity is missing",
                state["checked_response"],
            )

        state["continuations"].append(
            {
                "after_round": state["used"],
                "failed_call": prefix,
                "authorization": permission,
                "failure": state["error"],
            }
        )
        state["phase"] = "between"
        state["call"] = None
        state["error"] = None
        archive.save(state)
        return state
