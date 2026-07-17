#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Mechanical inventory and execution gate for the claude-home-audit skill.

Two modes, both non-semantic (no judgment calls, no ledger join):

    snapshot            Read-only. Prints a schema-versioned JSON inventory of
                        the Claude home directory: per-entry sizes/counts/ages,
                        registry classification of documented platform paths,
                        settings-scope reference extraction, skills/ symlink
                        health, sweep-health computation, and the protected
                        floor (static + derived).
    check <plan.json>   Execution gate. Re-stats each plan item, re-applies the
                        full protected floor (static, derived, registry,
                        7-day rule) at execution time, and verifies size and
                        entry count against the plan within tolerance.
                        Per-item verdicts: block / skip / pass.

The registry below is a stamped snapshot of the official Claude Code docs
(claude-directory page). On a delta from the stamped pair, the audit preflight
re-verifies classifications against live docs before trusting them.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

SNAPSHOT_SCHEMA_VERSION = 1
PLAN_SCHEMA_VERSION = 1

# Registry stamp: the docs snapshot and binary this classification was authored against.
REGISTRY_DOCS_INDEX_DATE = "2026-07-16"
REGISTRY_CLAUDE_VERSION = "2.1.211"

DEFAULT_CLEANUP_DAYS = 30
SWEEP_GRACE_DAYS = 3
LAST_CLEANUP_STALE_DAYS = 7
UNPROPOSABLE_RECENT_DAYS = 7
SIZE_TOLERANCE_FRACTION = 0.10
SIZE_TOLERANCE_FLOOR_BYTES = 4096
ENTRY_TOLERANCE_FRACTION = 0.10
ENTRY_TOLERANCE_FLOOR = 2

MANAGED_SETTINGS_PATH = Path(
    "/Library/Application Support/ClaudeCode/managed-settings.json"
)

# Classification of documented top-level paths under the home directory.
# Classes: authored | swept | kept-forever | platform-managed | mixed | audit-home.
# Everything absent from this table is "unclassified" (protected-pending-evidence).
REGISTRY: dict[str, str] = {
    "CLAUDE.md": "authored",
    "rules": "authored",
    "settings.json": "authored",
    "skills": "authored",
    "commands": "authored",
    "output-styles": "authored",
    "agents": "authored",
    "workflows": "authored",
    "agent-memory": "authored",
    "keybindings.json": "authored",
    "themes": "authored",
    "hooks": "authored",
    "references": "authored",
    ".claude": "authored",
    ".mcp.json": "authored",
    "plugins": "platform-managed",
    ".claude.json": "platform-managed",
    ".last-cleanup": "platform-managed",
    "projects": "mixed",  # transcripts swept; projects/<p>/memory/ kept-forever
    "file-history": "swept",
    "plans": "swept",
    "debug": "swept",
    "paste-cache": "swept",
    "image-cache": "swept",
    "session-env": "swept",
    "tasks": "swept",
    "shell-snapshots": "swept",
    "backups": "swept",
    "feedback-bundles": "swept",
    "todos": "swept",
    "statsig": "swept",
    "logs": "swept",
    "history.jsonl": "kept-forever",
    "stats-cache.json": "kept-forever",
    "remote-settings.json": "kept-forever",
    "audits": "audit-home",
}

# Spec-defined static protected floor (top-level names under the home directory).
STATIC_FLOOR: frozenset[str] = frozenset(
    {
        "settings.json",
        ".claude",
        ".claude.json",
        ".mcp.json",
        "plugins",
        "skills",
        "CLAUDE.md",
        "keybindings.json",
        "references",
        "agents",
        "commands",
        "hooks",
        "rules",
        "output-styles",
        "audits",
    }
)

# Registry classes whose contents the platform owns; the gate never passes them.
PLATFORM_OWNED_CLASSES: frozenset[str] = frozenset(
    {"swept", "mixed", "kept-forever", "platform-managed"}
)

_PATH_TOKEN_RE = re.compile(r"(?:~|\$HOME|/)[^\s\"':,;|&]+")


@dataclass
class WalkStats:
    """Aggregate lstat measurements for one filesystem entry."""

    bytes_total: int
    entries: int
    newest_mtime: float
    oldest_mtime: float


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).isoformat(timespec="seconds")


def _age_days(ts: float) -> float:
    return round((_now().timestamp() - ts) / 86400, 2)


def _human(n: int) -> str:
    size = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.1f}{unit}" if unit != "B" else f"{int(size)}B"
        size /= 1024
    raise AssertionError("unreachable")


def walk_stats(path: Path, exclude: frozenset[Path] = frozenset()) -> WalkStats:
    """Measure a path with lstat, never following symlinks.

    Args:
        path: File, directory, or symlink to measure.
        exclude: Directories to skip entirely (used to exclude
            ``projects/<p>/memory/`` from sweep-age computation).

    Returns:
        Totals over the entry and everything beneath it. Symlinks are counted
        by their own lstat and never descended.
    """
    st = path.lstat()
    if not path.is_dir() or path.is_symlink():
        return WalkStats(st.st_size, 0, st.st_mtime, st.st_mtime)
    total, count = 0, 0
    newest, oldest = st.st_mtime, st.st_mtime
    stack: list[Path] = [path]
    while stack:
        current = stack.pop()
        try:
            children = list(os.scandir(current))
        except OSError as exc:
            raise SystemExit(
                f"inventory walk failed: {exc}. Got: {str(current)!r:.100}"
            ) from exc
        for child in children:
            child_path = Path(child.path)
            if child_path in exclude:
                continue
            cst = child_path.lstat()
            count += 1
            total += cst.st_size
            newest = max(newest, cst.st_mtime)
            oldest = min(oldest, cst.st_mtime)
            if child.is_dir(follow_symlinks=False):
                stack.append(child_path)
    return WalkStats(total, count, newest, oldest)


def settings_scopes(home: Path) -> list[dict[str, object]]:
    """Enumerate settings scopes relevant to a home-rooted session.

    Precedence order for ``cleanupPeriodDays`` (highest first): managed,
    nested local, nested project, user.
    """
    scopes = [
        ("managed", MANAGED_SETTINGS_PATH),
        ("local", home / ".claude" / "settings.local.json"),
        ("project", home / ".claude" / "settings.json"),
        ("user", home / "settings.json"),
        ("mcp", home / ".mcp.json"),
    ]
    results: list[dict[str, object]] = []
    for scope, path in scopes:
        entry: dict[str, object] = {
            "scope": scope,
            "path": str(path),
            "exists": path.exists(),
        }
        if path.exists():
            try:
                entry["data"] = json.loads(path.read_text())
                entry["parse_ok"] = True
            except (OSError, json.JSONDecodeError) as exc:
                entry["parse_ok"] = False
                entry["error"] = f"{type(exc).__name__}: {exc}"
        results.append(entry)
    return results


def effective_cleanup_days(scopes: list[dict[str, object]]) -> tuple[int, str]:
    """Resolve the effective cleanupPeriodDays and the scope that set it."""
    for scope_name in ("managed", "local", "project", "user"):
        for entry in scopes:
            if entry["scope"] != scope_name or not entry.get("parse_ok"):
                continue
            data = entry["data"]
            if isinstance(data, dict) and "cleanupPeriodDays" in data:
                value = data["cleanupPeriodDays"]
                if not isinstance(value, int) or value < 1:
                    raise SystemExit(
                        f"settings read failed: invalid cleanupPeriodDays. Got: {value!r:.100}"
                    )
                return value, scope_name
    return DEFAULT_CLEANUP_DAYS, "default"


def extract_referenced_paths(
    scopes: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Extract path-looking tokens from every string in every parsed scope.

    Heuristic token scan (absolute, ``~``, or ``$HOME`` prefixed); expansion
    only — no existence requirement, since the floor protects referenced
    paths whether or not they currently resolve.
    """
    found: dict[str, dict[str, object]] = {}

    def visit(node: object, source: str) -> None:
        if isinstance(node, dict):
            for value in node.values():
                visit(value, source)
        elif isinstance(node, list):
            for value in node:
                visit(value, source)
        elif isinstance(node, str):
            for token in _PATH_TOKEN_RE.findall(node):
                expanded = (
                    os.path.expandvars(token.replace("~", str(Path.home()), 1))
                    if token.startswith("~")
                    else os.path.expandvars(token)
                )
                if not expanded.startswith("/"):
                    continue
                record = found.setdefault(
                    expanded,
                    {
                        "path": expanded,
                        "exists": Path(expanded).exists(),
                        "sources": [],
                    },
                )
                sources = record["sources"]
                assert isinstance(sources, list)
                if source not in sources:
                    sources.append(source)

    for entry in scopes:
        if entry.get("parse_ok"):
            visit(entry["data"], str(entry["scope"]))
    return sorted(found.values(), key=lambda r: str(r["path"]))


def skills_symlink_health(home: Path) -> list[dict[str, object]]:
    """Report each child of ``skills/``: symlink target health or the non-symlink carve-out."""
    skills_dir = home / "skills"
    if not skills_dir.is_dir():
        return []
    results: list[dict[str, object]] = []
    for child in sorted(skills_dir.iterdir()):
        if child.is_symlink():
            target = os.readlink(child)
            resolved = child.resolve(strict=False)
            results.append(
                {
                    "name": child.name,
                    "symlink": True,
                    "target": target,
                    "resolved": str(resolved),
                    "target_exists": resolved.exists(),
                }
            )
        else:
            results.append(
                {
                    "name": child.name,
                    "symlink": False,
                    "note": "non-symlink child; item-level judgeable by carve-out",
                }
            )
    return results


def _sweep_oldest_mtime(path: Path, cls: str) -> tuple[float | None, int, int]:
    """Oldest mtime among documented-swept, non-symlink entries under ``path``.

    Returns ``(oldest_mtime or None, swept_entry_count, symlinks_ignored)``.

    The sweep manages regular files and directories; symlink pointers (e.g. a
    dangling ``debug/latest`` left after its target aged out) are not swept
    data and are excluded from the age assertion. For ``projects`` (mixed),
    only the documented swept sub-paths count: per-project ``<session>.jsonl``
    transcripts and session directories. Per-project metadata files
    (``sessions-index.json``, ``.session-aliases``) and ``memory/`` are not
    swept and are excluded.
    """
    oldest: float | None = None
    count = 0
    links = 0

    def consider(entry: Path) -> None:
        nonlocal oldest, count
        mtime = entry.lstat().st_mtime
        count += 1
        oldest = mtime if oldest is None else min(oldest, mtime)

    def consider_tree(root: Path, include_self: bool) -> None:
        nonlocal links
        if include_self:
            consider(root)
        stack = [root]
        while stack:
            current = stack.pop()
            try:
                children = list(os.scandir(current))
            except OSError as exc:
                raise SystemExit(
                    f"sweep-health walk failed: {exc}. Got: {str(current)!r:.100}"
                ) from exc
            for child in children:
                child_path = Path(child.path)
                if child.is_symlink():
                    links += 1
                    continue
                if child.is_dir(follow_symlinks=False):
                    stack.append(child_path)
                consider(child_path)

    if cls == "swept":
        consider_tree(path, include_self=False)
    else:
        for proj in sorted(path.iterdir()):
            if proj.is_symlink():
                links += 1
                continue
            if not proj.is_dir():
                continue
            for child in sorted(proj.iterdir()):
                if child.is_symlink():
                    links += 1
                elif child.is_dir() and child.name != "memory":
                    consider_tree(child, include_self=True)
                elif child.is_file() and child.suffix == ".jsonl":
                    consider(child)
    return oldest, count, links


def sweep_health(
    home: Path, cleanup_days: int, scopes: list[dict[str, object]]
) -> dict[str, object]:
    """Assert the sweep's outcome: no swept-path entry older than cutoff + grace."""
    threshold_days = cleanup_days + SWEEP_GRACE_DAYS
    violations: list[dict[str, object]] = []
    checked: list[dict[str, object]] = []
    for name, cls in REGISTRY.items():
        if cls not in ("swept", "mixed"):
            continue
        path = home / name
        if not path.exists():
            continue
        oldest_mtime, entries, links = _sweep_oldest_mtime(path, cls)
        oldest_age = _age_days(oldest_mtime) if oldest_mtime is not None else 0.0
        ok = entries == 0 or oldest_age <= threshold_days
        checked.append(
            {
                "path": name,
                "entries": entries,
                "symlinks_ignored": links,
                "oldest_age_days": oldest_age,
                "ok": ok,
            }
        )
        if not ok:
            violations.append({"path": name, "oldest_age_days": oldest_age})
    last_cleanup = home / ".last-cleanup"
    last_cleanup_info: dict[str, object] = {"exists": last_cleanup.exists()}
    if last_cleanup.exists():
        age = _age_days(last_cleanup.lstat().st_mtime)
        last_cleanup_info["age_days"] = age
        last_cleanup_info["fresh"] = age <= LAST_CLEANUP_STALE_DAYS
        last_cleanup_info["raw"] = last_cleanup.read_text().strip()[:64]
    parse_failures = [
        str(e["path"]) for e in scopes if e["exists"] and not e.get("parse_ok")
    ]
    healthy = (
        not violations
        and not parse_failures
        and bool(last_cleanup_info.get("fresh", False))
    )
    return {
        "healthy": healthy,
        "threshold_days": threshold_days,
        "grace_days": SWEEP_GRACE_DAYS,
        "swept_paths_checked": checked,
        "violations": violations,
        "last_cleanup": last_cleanup_info,
        "settings_parse_failures": parse_failures,
        "sweep_paused_risk": bool(parse_failures),
    }


def classify(name: str) -> str:
    return REGISTRY.get(name, "unclassified")


def snapshot(home: Path) -> dict[str, object]:
    """Build the full read-only inventory snapshot for the home directory."""
    if not home.is_dir():
        raise SystemExit(
            f"snapshot failed: home directory missing. Got: {str(home)!r:.100}"
        )
    scopes = settings_scopes(home)
    cleanup_days, cleanup_source = effective_cleanup_days(scopes)
    referenced = extract_referenced_paths(scopes)
    entries: list[dict[str, object]] = []
    total_bytes = 0
    for child in sorted(home.iterdir()):
        stats = walk_stats(child)
        total_bytes += stats.bytes_total
        entries.append(
            {
                "name": child.name,
                "type": "symlink"
                if child.is_symlink()
                else "dir"
                if child.is_dir()
                else "file",
                "class": classify(child.name),
                "bytes": stats.bytes_total,
                "human": _human(stats.bytes_total),
                "entries": stats.entries,
                "newest_mtime": _iso(stats.newest_mtime),
                "oldest_mtime": _iso(stats.oldest_mtime),
                "newest_age_days": _age_days(stats.newest_mtime),
                "oldest_age_days": _age_days(stats.oldest_mtime),
                "modified_within_7d": _age_days(stats.newest_mtime)
                < UNPROPOSABLE_RECENT_DAYS,
                "on_static_floor": child.name in STATIC_FLOOR,
            }
        )
    projects_breakdown: list[dict[str, object]] = []
    projects_dir = home / "projects"
    if projects_dir.is_dir():
        for proj in sorted(projects_dir.iterdir()):
            if not proj.is_dir():
                continue
            memory = proj / "memory"
            mem_stats = walk_stats(memory) if memory.is_dir() else None
            rest = walk_stats(proj, exclude=frozenset({memory}))
            projects_breakdown.append(
                {
                    "project": proj.name,
                    "swept_bytes": rest.bytes_total,
                    "swept_entries": rest.entries,
                    "swept_oldest_age_days": _age_days(rest.oldest_mtime),
                    "memory_bytes": mem_stats.bytes_total if mem_stats else 0,
                }
            )
    # Redact parsed settings bodies from the emitted scopes; the snapshot needs
    # parse status and provenance, not settings contents.
    scope_report = [{k: v for k, v in entry.items() if k != "data"} for entry in scopes]
    return {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "generated_at": _now().isoformat(timespec="seconds"),
        "home": str(home),
        "registry_stamp": {
            "docs_index_date": REGISTRY_DOCS_INDEX_DATE,
            "claude_version": REGISTRY_CLAUDE_VERSION,
        },
        "effective_cleanup_days": cleanup_days,
        "cleanup_days_source": cleanup_source,
        "total_bytes": total_bytes,
        "total_human": _human(total_bytes),
        "sweep_health": sweep_health(home, cleanup_days, scopes),
        "entries": entries,
        "projects_breakdown": projects_breakdown,
        "skills_symlinks": skills_symlink_health(home),
        "settings_scopes": scope_report,
        "derived_floor": referenced,
        "static_floor": sorted(STATIC_FLOOR),
        "thresholds": {
            "unproposable_recent_days": UNPROPOSABLE_RECENT_DAYS,
            "size_tolerance_fraction": SIZE_TOLERANCE_FRACTION,
            "size_tolerance_floor_bytes": SIZE_TOLERANCE_FLOOR_BYTES,
            "entry_tolerance_fraction": ENTRY_TOLERANCE_FRACTION,
            "entry_tolerance_floor": ENTRY_TOLERANCE_FLOOR,
        },
    }


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def check_item(
    raw_path: str,
    expected_bytes: int,
    expected_entries: int | None,
    home: Path,
    derived_floor: list[Path],
) -> dict[str, object]:
    """Gate one approved plan item: block / skip / pass with a reason."""
    result: dict[str, object] = {"path": raw_path}

    def verdict(kind: str, reason: str) -> dict[str, object]:
        result.update({"verdict": kind, "reason": reason})
        return result

    path = Path(os.path.expanduser(raw_path))
    if not path.is_absolute():
        return verdict("block", "path is not absolute")
    home_real = home.resolve()
    if not _within(Path(os.path.realpath(path.parent)) / path.name, home_real):
        return verdict(
            "block", "resolves outside the home directory (symlink or path escape)"
        )
    if (
        not path.is_symlink()
        and path.exists()
        and not _within(Path(os.path.realpath(path)), home_real)
    ):
        return verdict(
            "block",
            "target resolves outside the home directory; never follow symlinks out",
        )
    try:
        rel = (Path(os.path.realpath(path.parent)) / path.name).relative_to(home_real)
    except ValueError:  # unreachable after containment check; defensive
        return verdict("block", "containment resolution failed")
    top = rel.parts[0]
    if top in STATIC_FLOOR and len(rel.parts) == 1:
        return verdict("block", f"static protected floor: {top}")
    if top in STATIC_FLOOR:
        return verdict("block", f"inside static protected floor: {top}/")
    cls = classify(top)
    if cls in PLATFORM_OWNED_CLASSES:
        return verdict("block", f"platform-owned ({cls}): {top}")
    for protected in derived_floor:
        protected_real = Path(os.path.realpath(protected))
        item_real = (
            Path(os.path.realpath(path))
            if path.exists()
            else Path(os.path.realpath(path.parent)) / path.name
        )
        if (
            item_real == protected_real
            or _within(protected_real, item_real)
            or _within(item_real, protected_real)
        ):
            return verdict(
                "block",
                f"derived floor: referenced from a settings scope ({protected})",
            )
    if not path.exists() and not path.is_symlink():
        return verdict("skip", "no longer exists")
    stats = walk_stats(path)
    result["measured_bytes"] = stats.bytes_total
    result["measured_entries"] = stats.entries
    if _age_days(stats.newest_mtime) < UNPROPOSABLE_RECENT_DAYS:
        return verdict("block", f"modified within {UNPROPOSABLE_RECENT_DAYS} days")
    # Tolerance absorbs directory churn only; a regular file or symlink must
    # match the approved size exactly, or the item is not what was approved.
    if path.is_dir() and not path.is_symlink():
        size_tolerance = max(
            SIZE_TOLERANCE_FLOOR_BYTES, int(expected_bytes * SIZE_TOLERANCE_FRACTION)
        )
    else:
        size_tolerance = 0
    if abs(stats.bytes_total - expected_bytes) > size_tolerance:
        return verdict(
            "skip",
            f"size drift: expected {expected_bytes}±{size_tolerance}, measured {stats.bytes_total}",
        )
    if expected_entries is not None:
        entry_tolerance = max(
            ENTRY_TOLERANCE_FLOOR, int(expected_entries * ENTRY_TOLERANCE_FRACTION)
        )
        if abs(stats.entries - expected_entries) > entry_tolerance:
            return verdict(
                "skip",
                f"entry drift: expected {expected_entries}±{entry_tolerance}, measured {stats.entries}",
            )
    return verdict("pass", "floor clear; measurements within tolerance")


def check(home: Path, plan_path: Path) -> dict[str, object]:
    """Run the execution gate over a plan file."""
    try:
        plan = json.loads(plan_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(
            f"check failed: unreadable plan. Got: {str(plan_path)!r:.100} ({exc})"
        ) from exc
    version = plan.get("schema_version")
    if version != PLAN_SCHEMA_VERSION:
        raise SystemExit(
            f"check failed: unsupported plan schema_version (expected {PLAN_SCHEMA_VERSION}). Got: {version!r:.100}"
        )
    items = plan.get("items")
    if not isinstance(items, list) or not items:
        raise SystemExit(f"check failed: plan has no items. Got: {items!r:.100}")
    scopes = settings_scopes(home)
    derived = [Path(str(r["path"])) for r in extract_referenced_paths(scopes)]
    verdicts = []
    for item in items:
        if (
            not isinstance(item, dict)
            or "path" not in item
            or "expected_bytes" not in item
        ):
            raise SystemExit(f"check failed: malformed plan item. Got: {item!r:.100}")
        verdicts.append(
            check_item(
                str(item["path"]),
                int(item["expected_bytes"]),
                int(item["expected_entries"])
                if item.get("expected_entries") is not None
                else None,
                home,
                derived,
            )
        )
    counts = {
        kind: sum(1 for v in verdicts if v["verdict"] == kind)
        for kind in ("pass", "skip", "block")
    }
    return {
        "schema_version": PLAN_SCHEMA_VERSION,
        "checked_at": _now().isoformat(timespec="seconds"),
        "home": str(home),
        "counts": counts,
        "verdicts": verdicts,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home() / ".claude",
        help="Home directory to audit (fixture override for tests)",
    )
    sub = parser.add_subparsers(dest="mode", required=True)
    sub.add_parser("snapshot", help="print the read-only JSON inventory")
    check_parser = sub.add_parser(
        "check", help="gate approved plan items at execution time"
    )
    check_parser.add_argument(
        "plan",
        type=Path,
        help="plan JSON: {schema_version, items:[{path, expected_bytes, expected_entries}]}",
    )
    args = parser.parse_args(argv)
    if args.mode == "snapshot":
        print(json.dumps(snapshot(args.home), indent=2))
    else:
        print(json.dumps(check(args.home, args.plan), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
