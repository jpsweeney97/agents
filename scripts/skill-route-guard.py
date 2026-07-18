#!/usr/bin/env python3
"""PreToolUse hook: block skill-surface mutations outside the satellite lifecycle.

Denies file mutations targeting live skill surfaces in the primary checkout or
any parked satellite, and routes the agent to the worktree-task-cycle lifecycle.
Covers Edit/Write/MultiEdit/NotebookEdit (Claude Code) and apply_patch (Codex);
Bash-mediated mutations, hosted tools, and hook-bypassing tool paths are
disclosed non-coverage — this is a guardrail on the dominant edit path, not a
complete enforcement boundary.

Exit contract: 0 allow (silent) or bypass (warning JSON on stdout); 1
non-blocking error outside guarded territory; 2 deny, reason on stderr.
Unclassifiable input fails closed when the session cwd or any extractable
target resolves into guarded territory, and fails open (exit 1) elsewhere.

Emergency bypass: SKILL_ROUTE_GUARD_BYPASS=1.

Promotion rule: once wired into ~/.claude/settings.json and ~/.codex/hooks.json
this file executes live from the primary working tree, so edit it only through
an activated satellite task landed ff onto main — never on a primary branch.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FLEET_ROOT = REPO.parent / f"{REPO.name}-worktrees"
BYPASS_ENV = "SKILL_ROUTE_GUARD_BYPASS"
GIT_TIMEOUT_SECONDS = 4

SKILL_SURFACE_RE = re.compile(r"^(?:skills|skills-claude)/[^/]+/.+|^plugins/[^/]+/.+")
SKILL_IDENTITY_RE = re.compile(
    r"^(?:skills|skills-claude)/([^/]+)/.+|^plugins/[^/]+/skills/([^/]+)/.+"
)
PATCH_TARGET_RE = re.compile(
    r"^\*\*\* (?:Add|Update|Delete) File: (.+)$|^\*\*\* Move to: (.+)$", re.MULTILINE
)

LIFECYCLE_LINE = (
    "Route: invoke worktree-task-cycle — inspect → lease-acquire → activate → "
    "make this edit in the satellite → validate → record-validation → land → park."
)

GENERIC_LOCATION = (
    "No satellite maps to this path. Work it in any satellite activated for a task; "
    "for a new skill the fleet gains its satellite after landing (attended create-missing)."
)

PARKED_MESSAGE = (
    "skill-route-guard: blocked — this satellite is PARKED (detached HEAD); "
    "its tree is a stale snapshot of an older main.\n"
    "Run the worktree-task-cycle lifecycle first (inspect → lease-acquire → activate), "
    "then redo this edit on the task branch."
)


class Deny(Exception):
    """Raised with the full stderr message for an exit-2 refusal."""


def extract_targets(tool_name: str, tool_input: dict) -> "list[str]":
    """Return every mutation target path, or raise ValueError when unextractable."""
    if tool_name in ("Edit", "Write"):
        return [_require(tool_input, "file_path")]
    if tool_name == "NotebookEdit":
        return [_require(tool_input, "notebook_path")]
    if tool_name == "MultiEdit":
        edits = tool_input.get("edits") or []
        targets = [e.get("file_path") for e in edits if isinstance(e, dict)]
        if not targets or not all(isinstance(t, str) and t for t in targets):
            raise ValueError(
                f"MultiEdit extraction failed: no usable edits. Got: {tool_input!r:.100}"
            )
        return [str(t) for t in targets]
    if tool_name == "apply_patch":
        command = tool_input.get("command")
        if not isinstance(command, str) or not command:
            raise ValueError(
                f"apply_patch extraction failed: no command. Got: {tool_input!r:.100}"
            )
        targets = [m.group(1) or m.group(2) for m in PATCH_TARGET_RE.finditer(command)]
        targets = [t.strip() for t in targets if t and t.strip()]
        if not targets:
            raise ValueError(
                f"apply_patch extraction failed: no file markers. Got: {command!r:.100}"
            )
        return targets
    raise ValueError(
        f"target extraction failed: unhandled tool. Got: {tool_name!r:.100}"
    )


def _require(tool_input: dict, field: str) -> str:
    value = tool_input.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(
            f"target extraction failed: missing {field}. Got: {tool_input!r:.100}"
        )
    return value


def resolve_forms(target: str, cwd: str) -> "tuple[Path, Path]":
    """Return (lexical, physical) absolute forms of a target path.

    Physical form is the realpath of the nearest existing ancestor with any
    nonexistent suffix re-appended, so symlinked and not-yet-created paths both
    classify by where the mutation actually lands.
    """
    p = Path(target)
    if not p.is_absolute():
        p = Path(cwd) / p
    lexical = Path(os.path.normpath(str(p)))
    existing = p
    suffix: "list[str]" = []
    while not existing.exists() and existing != existing.parent:
        suffix.append(existing.name)
        existing = existing.parent
    physical = Path(os.path.realpath(str(existing)))
    for name in reversed(suffix):
        physical = physical / name
    return lexical, Path(os.path.normpath(str(physical)))


def classify(path: Path) -> "tuple[str, str] | None":
    """Classify one absolute form: ('primary-skill'|'satellite', rel) or None."""
    s = str(path)
    repo = str(REPO)
    fleet = str(FLEET_ROOT)
    if s == repo or s.startswith(repo + os.sep):
        rel = os.path.relpath(s, repo).replace(os.sep, "/")
        if SKILL_SURFACE_RE.match(rel):
            return ("primary-skill", rel)
        return None
    if s == fleet or s.startswith(fleet + os.sep):
        return ("satellite", os.path.relpath(s, fleet).replace(os.sep, "/"))
    return None


def route_message(rel: str) -> str:
    match = SKILL_IDENTITY_RE.match(rel)
    identity = (match.group(1) or match.group(2)) if match else None
    subject = f" (skill: {identity})" if identity else ""
    if identity and (FLEET_ROOT / identity).is_dir():
        location = f"Likely satellite (confirm with inspect): {FLEET_ROOT / identity}"
    else:
        location = GENERIC_LOCATION
    return (
        f"skill-route-guard: blocked — skill-surface mutation in the primary checkout.\n"
        f"Target: {rel}{subject}\n"
        "Skill mutations happen in a satellite worktree via the worktree-task-cycle "
        "lifecycle (git-cycle plugin), never in the primary.\n"
        f"{location}\n"
        f"{LIFECYCLE_LINE}"
    )


def check_satellite(rel: str) -> None:
    """Raise Deny for parked or unverifiable satellites; return for active ones."""
    component = rel.split("/", 1)[0]
    if component in ("", ".", ".."):
        raise Deny(
            "skill-route-guard: blocked — unexpected mutation target directly under the "
            f"fleet root ({FLEET_ROOT}). Only satellite worktrees live there."
        )
    sat_dir = FLEET_ROOT / component
    try:
        proc = subprocess.run(
            ["git", "-C", str(sat_dir), "symbolic-ref", "-q", "HEAD"],
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        raise Deny(
            f"skill-route-guard: blocked — satellite state check failed for {sat_dir}. "
            f"Got: {type(exc).__name__}: {exc}"
        ) from exc
    if proc.returncode == 0:
        return
    if proc.returncode == 1 and not proc.stderr.strip():
        raise Deny(PARKED_MESSAGE)
    raise Deny(
        f"skill-route-guard: blocked — cannot verify satellite state for {sat_dir}. "
        f"Got: {proc.stderr.strip()!r:.200}"
    )


def under_guarded_roots(path: Path) -> bool:
    s = str(path)
    for root in (str(REPO), str(FLEET_ROOT)):
        if s == root or s.startswith(root + os.sep):
            return True
    return False


def any_guarded(paths: "list[str]", cwd: str) -> bool:
    for candidate in [cwd, *paths]:
        try:
            if any(under_guarded_roots(form) for form in resolve_forms(candidate, cwd)):
                return True
        except OSError:
            return True
    return False


def evaluate(targets: "list[str]", cwd: str) -> None:
    """Raise Deny for any violating target; return for a full allow."""
    satellite_rels: "list[str]" = []
    for target in targets:
        for form in resolve_forms(target, cwd):
            hit = classify(form)
            if hit is None:
                continue
            kind, rel = hit
            if kind == "primary-skill":
                raise Deny(route_message(rel))
            satellite_rels.append(rel)
    for rel in satellite_rels:
        check_satellite(rel)


def bypass_active() -> bool:
    if os.environ.get(BYPASS_ENV, "").strip() != "1":
        return False
    message = (
        f"Warning: skill-route-guard enforcement bypassed via {BYPASS_ENV}=1. "
        "Skill-surface mutations are NOT being routed to the satellite lifecycle."
    )
    print(
        json.dumps(
            {
                "systemMessage": message,
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": message,
                },
            }
        )
    )
    return True


def main() -> int:
    if bypass_active():
        return 0
    cwd = os.getcwd()
    targets: "list[str]" = []
    try:
        data = json.load(sys.stdin)
        cwd = str(data.get("cwd") or cwd)
        targets = extract_targets(
            str(data.get("tool_name") or ""), data.get("tool_input") or {}
        )
        evaluate(targets, cwd)
        return 0
    except Deny as deny:
        print(str(deny), file=sys.stderr)
        return 2
    except Exception as exc:
        reason = f"{type(exc).__name__}: {exc}"
        if any_guarded(targets, cwd):
            print(
                "skill-route-guard: blocked — could not classify this mutation inside "
                f"guarded territory; failing closed. Got: {reason!r:.200}\n"
                "If the edit does not touch a skill surface, retry with an explicit "
                "absolute file path; otherwise route through worktree-task-cycle.",
                file=sys.stderr,
            )
            return 2
        print(
            f"skill-route-guard: non-blocking error: {reason!r:.200}", file=sys.stderr
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
