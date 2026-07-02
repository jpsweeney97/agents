#!/usr/bin/env python3
"""Skill-usage miner: backfill and refresh the global skill-usage ledger from Claude Code transcripts.

Scans ~/.claude/projects/*/*.jsonl for skill fires:
- model-invoked: assistant tool_use blocks calling the Skill (or legacy SlashCommand) tool
- user-typed: <command-name> tags in user records (slash-command invocations)

Appends new fire records to the cumulative ledger (JSONL), deduped by a stable key,
so transcripts pruned by retention stay in the ledger once mined. Re-runnable anytime;
the live PostToolUse hook (scripts/skill-usage-hook.py) writes the same ledger between runs.

Usage: skill-usage-miner.py [--ledger PATH] [--summary-only]
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

LEDGER_DEFAULT = Path.home() / ".claude" / "logs" / "skill-usage-ledger.jsonl"
PROJECTS_DIR = Path.home() / ".claude" / "projects"
COMMAND_RE = re.compile(r"<command-name>([^<]+)</command-name>")
PREFILTER = ('"Skill"', '"SlashCommand"', "<command-name>")


def norm_skill(name: str) -> str:
    return name.strip().lstrip("/").strip()


def iter_fires(path: Path):
    """Yield fire dicts from one transcript file. Never raises on malformed lines."""
    subagent = "subagents" in path.parts
    try:
        fh = path.open(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"skip {path.name}: {e}", file=sys.stderr)
        return
    with fh:
        for line in fh:
            if not any(tok in line for tok in PREFILTER):
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            rtype = rec.get("type")
            base = {
                "ts": rec.get("timestamp"),
                "cwd": rec.get("cwd"),
                "session": rec.get("sessionId"),
                "sidechain": bool(rec.get("isSidechain")) or subagent,
            }
            if rtype == "assistant":
                content = (rec.get("message") or {}).get("content") or []
                if not isinstance(content, list):
                    continue
                for block in content:
                    if not isinstance(block, dict) or block.get("type") != "tool_use":
                        continue
                    name = block.get("name")
                    inp = block.get("input") or {}
                    if name == "Skill" and inp.get("skill"):
                        skill = norm_skill(str(inp["skill"]))
                    elif name == "SlashCommand" and inp.get("command"):
                        skill = norm_skill(str(inp["command"]).split()[0])
                    else:
                        continue
                    yield {
                        "key": f"{base['session']}:{block.get('id')}",
                        "skill": skill,
                        "source": "model",
                        **base,
                    }
            elif rtype == "user":
                msg = rec.get("message") or {}
                content = msg.get("content")
                texts = []
                if isinstance(content, str):
                    texts.append(content)
                elif isinstance(content, list):
                    texts.extend(
                        b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"
                    )
                for text in texts:
                    for m in COMMAND_RE.finditer(text):
                        yield {
                            "key": f"{base['session']}:{rec.get('uuid')}:{norm_skill(m.group(1))}",
                            "skill": norm_skill(m.group(1)),
                            "source": "user",
                            **base,
                        }


def load_ledger(ledger: Path):
    records = []
    if ledger.exists():
        with ledger.open(encoding="utf-8") as fh:
            for line in fh:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


class SkillStats:
    def __init__(self) -> None:
        self.total = 0
        self.model = 0
        self.user = 0
        self.subagent = 0
        self.cwds: set[str] = set()
        self.last = ""


def summarize(records):
    by_skill: defaultdict[str, SkillStats] = defaultdict(SkillStats)
    for r in records:
        s = by_skill[r["skill"]]
        s.total += 1
        if r.get("source") == "user":
            s.user += 1
        else:
            s.model += 1
        if r.get("sidechain"):
            s.subagent += 1
        if r.get("cwd"):
            s.cwds.add(r["cwd"])
        ts = r.get("ts") or ""
        if ts > s.last:
            s.last = ts
    rows = sorted(by_skill.items(), key=lambda kv: -kv[1].total)
    print(f"{'skill':<42} {'total':>5} {'model':>5} {'user':>5} {'subag':>5} {'cwds':>4}  last-fired")
    for skill, s in rows:
        print(f"{skill:<42} {s.total:>5} {s.model:>5} {s.user:>5} {s.subagent:>5} {len(s.cwds):>4}  {s.last[:10]}")
    print(f"\n{len(rows)} distinct skills, {len(records)} fires total")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", type=Path, default=LEDGER_DEFAULT)
    ap.add_argument("--summary-only", action="store_true", help="summarize existing ledger; no mining")
    args = ap.parse_args()

    existing = load_ledger(args.ledger)
    if args.summary_only:
        summarize(existing)
        return 0

    seen = {r["key"] for r in existing if "key" in r}
    new = []
    files = sorted(PROJECTS_DIR.rglob("*.jsonl"))
    for path in files:
        for fire in iter_fires(path):
            if fire["key"] in seen:
                continue
            seen.add(fire["key"])
            new.append(fire)

    args.ledger.parent.mkdir(parents=True, exist_ok=True)
    with args.ledger.open("a", encoding="utf-8") as fh:
        for r in new:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"mined {len(files)} transcripts, added {len(new)} new fires (ledger: {len(existing) + len(new)})\n")
    summarize(existing + new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
