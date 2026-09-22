#!/usr/bin/env python3
"""Never-used skill census (run 2026-09-21): the live roster read against the ledger.

Sibling of docs/reviews/2026-09-21-never-used-skill-census.md; its raw output is the .txt beside it.
Reuses the miner's own load/collapse/alias code so the view matches the summary tool.

Three filters separate a real fire from a row that only looks like one:
  - synthetic: the row's cwd is a session scratchpad (a `claude -p` proxy probe, not JP's work).
  - scan-read: a Codex SKILL.md read with read_burst >= SCAN_READ_BURST, i.e. the model was
    reading many skills at once to pick a route and did not choose this one.
  - external tokens: a plugin-qualified token whose prefix is not a local plugin
    (`handoff:triage`, `github:gh-address-comments`, ...) is never credited to the local
    bare-named skill.

With --scan-transcripts it also closes the miner's Claude-side blind spot by scanning every
~/.claude/projects transcript for `skills/<name>/SKILL.md`, catching a skill read without a
Skill call. That pass is minutes long over ~1.8GB; the .txt beside this file holds its result.

Run from anywhere: python3 docs/reviews/2026-09-21-never-used-skill-census.py [--scan-transcripts]
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/Users/jp/.agents")
LEDGER = Path("/Users/jp/.claude/logs/skill-usage-ledger.jsonl")
PROJECTS = Path("/Users/jp/.claude/projects")

# The census moment, so "days since last fire" is reproducible from the record.
TODAY = datetime(2026, 9, 21, tzinfo=timezone.utc)
# A used skill silent this long is reported as cold rather than live.
COLD_DAYS = 56

spec = importlib.util.spec_from_file_location(
    "miner", REPO / "scripts/skill-usage-miner.py"
)
assert spec is not None and spec.loader is not None, "miner import failed"
miner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(miner)

SCRATCHPAD_RE = re.compile(r"^(/private)?/tmp/claude-\d+/|^/tmp/")
CWD_RE = re.compile(r'"cwd"\s*:\s*"([^"]*)"')


def roster() -> tuple[dict[str, str], dict[str, set[str]], dict[str, Path]]:
    """Map the live roster.

    Returns:
        (name -> source label, plugin name -> its skill names, name -> skill directory).
    """
    names: dict[str, str] = {}
    paths: dict[str, Path] = {}
    plugins: dict[str, set[str]] = {}
    for root, label in (
        (REPO / "skills", "skills"),
        (REPO / "skills-claude", "skills-claude"),
    ):
        if not root.is_dir():
            raise SystemExit(
                f"roster scan failed: missing skill root. Got: {str(root)!r:.100}"
            )
        for p in sorted(root.iterdir()):
            if p.is_dir() and not p.name.startswith("."):
                names[p.name], paths[p.name] = label, p
    for skills_dir in sorted((REPO / "plugins").glob("*/skills")):
        plugin = skills_dir.parent.name
        plugins[plugin] = set()
        for p in sorted(skills_dir.iterdir()):
            if p.is_dir() and not p.name.startswith("."):
                names[p.name], paths[p.name] = f"plugins/{plugin}", p
                plugins[plugin].add(p.name)
    return names, plugins, paths


def born(skill_dir: Path) -> str:
    """First appearance of the skill's SKILL.md, following renames into plugin dirs."""
    out = (
        subprocess.run(
            [
                "git",
                "log",
                "--diff-filter=A",
                "--follow",
                "--format=%ad",
                "--date=short",
                "--",
                str(skill_dir / "SKILL.md"),
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        .stdout.strip()
        .splitlines()
    )
    return out[-1] if out else "?"


def inbound_routes(name: str) -> int:
    """How many OTHER live SKILL.md files name this skill."""
    out = subprocess.run(
        [
            "grep",
            "-rl",
            "--include=SKILL.md",
            "-w",
            name,
            "skills",
            "skills-claude",
            "plugins",
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.splitlines()
    return len([f for f in out if not f.endswith(f"/{name}/SKILL.md")])


def days_since(ts: str) -> int | None:
    """Whole days from an ISO timestamp to the census moment, or None if unparseable."""
    if not ts:
        return None
    try:
        return (TODAY - datetime.fromisoformat(ts.replace("Z", "+00:00"))).days
    except ValueError:
        return None


def tally(
    names: dict[str, str], plugins: dict[str, set[str]]
) -> tuple[dict, dict, dict]:
    """Fold ledger rows into per-skill counts, split real / synthetic / scan-read.

    Returns:
        (name -> counters, external token -> count, collapse stats from the miner).
    """
    records, collapse_stats = miner.collapse(miner.load_ledger(LEDGER))
    stats: dict[str, dict] = defaultdict(
        lambda: {
            "real": 0,
            "synth": 0,
            "scan": 0,
            "user": 0,
            "codex": 0,
            "cwds": set(),
            "first": "",
            "last": "",
        }
    )
    external: dict[str, int] = defaultdict(int)
    for row in records:
        token = miner.ALIASES.get(str(row["skill"]), str(row["skill"]))
        bare = token.rsplit(":", 1)[-1]
        if ":" in token:
            prefix = token.rsplit(":", 1)[0]
            if prefix not in plugins or bare not in plugins[prefix]:
                if bare in names:
                    external[token] += 1
                continue
        if bare not in names:
            continue
        s = stats[bare]
        cwd, ts = row.get("cwd") or "", row.get("ts") or ""
        if SCRATCHPAD_RE.match(cwd):
            s["synth"] += 1
        elif (
            row.get("kind") == "read"
            and (row.get("read_burst") or 0) >= miner.SCAN_READ_BURST
        ):
            s["scan"] += 1
        else:
            s["real"] += 1
            s["cwds"].add(cwd)
            if row.get("source") == "user":
                s["user"] += 1
            if row.get("runtime") == "codex":
                s["codex"] += 1
            if ts:
                s["last"] = max(s["last"], ts)
                s["first"] = min(s["first"] or ts, ts)
    return stats, dict(external), collapse_stats


def scan_transcripts(targets: list[str]) -> dict[str, dict[str, int]]:
    """Scan every Claude transcript for `skills/<name>/SKILL.md`, the miner's blind spot.

    A Claude session that reads a SKILL.md without calling the Skill tool leaves no ledger
    row. Returns name -> session cwd -> how many transcripts mention it.
    """
    hits: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    files = sorted(PROJECTS.rglob("*.jsonl"))
    for f in files:
        try:
            text = f.read_text(errors="replace")
        except OSError:
            continue
        found = [n for n in targets if f"skills/{n}/SKILL.md" in text]
        if not found:
            continue
        m = CWD_RE.search(text)
        cwd = m.group(1) if m else "<no-cwd-field>"
        for n in found:
            hits[n][cwd] += 1
    print(f"scanned {len(files)} Claude transcripts")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--scan-transcripts",
        action="store_true",
        help="also scan ~/.claude/projects for unmined SKILL.md reads (slow)",
    )
    args = ap.parse_args()

    names, plugins, paths = roster()
    stats, external, collapse_stats = tally(names, plugins)

    empty = {
        "real": 0,
        "synth": 0,
        "scan": 0,
        "user": 0,
        "codex": 0,
        "cwds": set(),
        "first": "",
        "last": "",
    }
    tiers: dict[str, list] = {
        "t0": [],
        "t1": [],
        "t2": [],
        "t3": [],
        "cold": [],
        "live": [],
    }
    for name, label in sorted(names.items()):
        s = stats.get(name, empty)
        row = (name, label, s, born(paths[name]), inbound_routes(name))
        outside = {c for c in s["cwds"] if c and not c.startswith(str(REPO))}
        if s["real"] == 0 and s["synth"] == 0 and s["scan"] == 0:
            tiers["t0"].append(row)
        elif s["real"] == 0 and s["scan"] == 0:
            tiers["t1"].append(row)
        elif s["real"] == 0:
            tiers["t2"].append(row)
        elif not outside:
            tiers["t3"].append(row)
        elif (days_since(s["last"]) or 0) >= COLD_DAYS:
            tiers["cold"].append(row)
        else:
            tiers["live"].append(row)

    counts = {k: len(v) for k, v in tiers.items()}
    print(
        f"roster: {len(names)} live skills "
        f"(skills {sum(1 for v in names.values() if v == 'skills')}, "
        f"skills-claude {sum(1 for v in names.values() if v == 'skills-claude')}, "
        f"plugins {sum(1 for v in names.values() if v.startswith('plugins'))})"
    )
    print(
        f"ledger view: {collapse_stats['fork'] + collapse_stats['burst']} rows collapsed "
        f"({collapse_stats['fork']} fork replays, {collapse_stats['burst']} rapid re-invokes)"
    )
    print(f"tiers: {counts}\n")

    titles = {
        "t0": "TIER 0 - no row of any kind",
        "t1": "TIER 1 - only synthetic probe rows",
        "t2": "TIER 2 - only roster-scan reads (seen, never chosen)",
        "t3": "TIER 3 - real fires, but only inside /Users/jp/.agents",
        "cold": f"TIER 4 - used in real work, silent >= {COLD_DAYS} days",
        "live": "LIVE - real fires outside this repo within the window",
    }
    header = (
        f"{'skill':<34}{'source':<22}{'born':<12}{'real':>5}{'synth':>6}{'scan':>5}"
        f"{'routes':>7}{'cwds':>5}  last real fire"
    )
    for key in ("t0", "t1", "t2", "t3", "cold", "live"):
        print(f"== {titles[key]} ({counts[key]}) ==")
        print(header)
        for name, label, s, birth, routes in sorted(
            tiers[key], key=lambda r: (r[2]["real"], r[2]["scan"])
        ):
            d = days_since(s["last"])
            last = f"{s['last'][:10]} ({d}d)" if s["last"] else "-"
            print(
                f"{name:<34}{label:<22}{birth:<12}{s['real']:>5}{s['synth']:>6}{s['scan']:>5}"
                f"{routes:>7}{len(s['cwds']):>5}  {last}"
            )
        print()

    if external:
        print("== external plugin tokens sharing a local bare name (NOT credited) ==")
        for token, n in sorted(external.items(), key=lambda kv: -kv[1]):
            print(f"  {token:<46}{n}")
        print()

    if args.scan_transcripts:
        targets = [r[0] for key in ("t0", "t1", "t2") for r in tiers[key]]
        print("== Claude-side blind spot: transcripts naming skills/<name>/SKILL.md ==")
        hits = scan_transcripts(targets)
        print(
            f"{'skill':<34}{'sessions':>9}{'outside .agents':>17}  cwds outside .agents"
        )
        for n in targets:
            h = hits.get(n, {})
            outside = {c: k for c, k in h.items() if not c.startswith(str(REPO))}
            listing = ", ".join(
                f"{c}({k})" for c, k in sorted(outside.items(), key=lambda kv: -kv[1])
            )
            print(f"{n:<34}{sum(h.values()):>9}{sum(outside.values()):>17}  {listing}")
        print()

    print(miner.FOOTNOTE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
