#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Report Claude Code context occupancy for the current session, from its own transcript.

Occupancy is the last assistant turn's ``input_tokens + cache_read_input_tokens +
cache_creation_input_tokens`` — the tokens the model actually read on that turn.

The script reports tokens only. It never converts to a percentage, because the
context-window size is not recorded in the transcript: the ``model`` field omits
the window variant, so a 1M-token session is indistinguishable there from a 200k
one. The window is the caller's assumption to state, not this script's to guess.

Usage:
    occupancy.py [--transcript PATH] [--cwd DIR] [--turns N]

Resolution order for the transcript, when --transcript is not given:
    1. ~/.claude/projects/<cwd-slug>/$CLAUDE_CODE_SESSION_ID.jsonl
    2. ~/.claude/projects/*/$CLAUDE_CODE_SESSION_ID.jsonl  (session ids are unique)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"


def fail(operation: str, reason: str, got: object) -> None:
    """Print a fail-fast diagnostic and exit non-zero."""
    print(f"{operation} failed: {reason}. Got: {got!r:.100}", file=sys.stderr)
    raise SystemExit(1)


def resolve_transcript(explicit: str | None, cwd: str | None) -> tuple[Path, str]:
    """Return (transcript path, how it was resolved)."""
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file():
            fail("transcript resolution", "--transcript path is not a file", explicit)
        return path, "explicit --transcript"

    session = os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    if not session:
        fail(
            "transcript resolution",
            "CLAUDE_CODE_SESSION_ID is unset, so the live session cannot be identified; "
            "pass --transcript",
            session,
        )

    slug = re.sub(r"[/.]", "-", cwd or os.getcwd())
    by_slug = PROJECTS / slug / f"{session}.jsonl"
    if by_slug.is_file():
        return by_slug, "cwd slug"

    matches = sorted(PROJECTS.glob(f"*/{session}.jsonl"))
    if len(matches) == 1:
        return matches[0], "session-id search (cwd slug did not match)"
    if not matches:
        fail(
            "transcript resolution",
            f"no transcript for this session under {PROJECTS}",
            str(by_slug),
        )
    fail(
        "transcript resolution",
        "session id matched several transcripts",
        [str(m) for m in matches],
    )
    raise AssertionError("unreachable")


def is_typed_user_turn(record: dict) -> bool:
    """True for a message the user actually typed, not tool results or runtime noise."""
    if (
        record.get("type") != "user"
        or record.get("isMeta")
        or record.get("isSidechain")
    ):
        return False
    content = (record.get("message") or {}).get("content")
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        blocks = [
            b.get("text", "")
            for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        ]
        if not blocks:
            return False
        text = "\n".join(blocks)
    else:
        return False
    stripped = text.lstrip()
    if stripped.startswith(("<command-", "<local-command")):
        return False
    return bool(stripped.strip())


def scan(path: Path) -> tuple[int, int, str, list[int]]:
    """Return (occupancy now, peak occupancy, model as recorded, occupancy at each typed user turn)."""
    occupancy = 0
    peak = 0
    model = "unknown"
    at_turns: list[int] = []
    with path.open(errors="replace") as handle:
        for line in handle:
            if '"usage"' in line:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if record.get("type") != "assistant":
                    continue
                message = record.get("message") or {}
                usage = message.get("usage") or {}
                if not usage:
                    continue
                occupancy = (
                    usage.get("input_tokens", 0)
                    + usage.get("cache_read_input_tokens", 0)
                    + usage.get("cache_creation_input_tokens", 0)
                )
                peak = max(peak, occupancy)
                model = message.get("model") or model
            elif '"type":"user"' in line:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if occupancy and is_typed_user_turn(record):
                    at_turns.append(occupancy)
    return occupancy, peak, model, at_turns


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transcript", help="explicit transcript path")
    parser.add_argument(
        "--cwd", help="directory to slug for transcript lookup (default: cwd)"
    )
    parser.add_argument(
        "--turns", type=int, default=8, help="how many recent turn deltas to print"
    )
    args = parser.parse_args()

    path, route = resolve_transcript(args.transcript, args.cwd)
    occupancy, peak, model, at_turns = scan(path)
    if not occupancy:
        fail(
            "occupancy read", "transcript holds no assistant turn with usage", str(path)
        )

    print(f"transcript: {path}  ({route})")
    print(
        f"model as recorded: {model}  [window variant not recorded — do not infer the context window from this]"
    )
    print(f"occupancy now: {occupancy:,} tokens")
    print(
        f"peak occupancy: {peak:,} tokens"
        + (
            "  [well above current — the session compacted]"
            if peak > occupancy * 1.5
            else ""
        )
    )
    print(f"typed user turns: {len(at_turns)}")

    deltas = [
        (i, at_turns[i] - at_turns[i - 1], at_turns[i]) for i in range(1, len(at_turns))
    ]
    if not deltas:
        print("turn deltas: none yet — this is the first measurable turn boundary")
        return
    shown = deltas[-args.turns :]
    print(
        f"turn deltas (tokens added between typed user turns; last {len(shown)} of {len(deltas)}):"
    )
    for index, delta, ended in shown:
        print(f"  turn {index:>3}: {delta:+,} (ended at {ended:,})")


if __name__ == "__main__":
    main()
