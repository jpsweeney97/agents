#!/usr/bin/env python3
"""Skill-usage miner: backfill and refresh the global skill-usage ledger from both runtimes' transcripts.

Scans ~/.claude/projects/*/*.jsonl (Claude Code) for skill fires:
- model-invoked: assistant tool_use blocks calling the Skill (or legacy SlashCommand) tool
- user-typed: <command-name> tags in user records (slash-command invocations)

Scans ~/.codex/sessions/**/*.jsonl (Codex rollouts) for skill fires:
- user-typed: <skill><name>...</name> injection blocks in user-role response_item messages
  (how Codex expands a typed `$skill` token). Codex records carry `runtime: "codex"`;
  records without a runtime field are Claude's. Codex has no live-hook equivalent, so
  Codex fires land only via re-running this miner; a launchd job (com.jp.skill-usage-miner,
  source: scripts/com.jp.skill-usage-miner.plist) runs it every ~5 days.

Appends new fire records to the cumulative ledger (JSONL), deduped by a stable key,
so transcripts pruned by retention stay in the ledger once mined. Re-runnable anytime;
the live PostToolUse hook (scripts/skill-usage-hook.py) writes the same ledger between runs.

Raw ledger records are never rewritten: the file is append-ordered (Claude projects, then
Codex back-mining), NOT time-sorted — consumers must never assume chronology; compute date
ranges from the `ts` field. All normalization happens at summary time only: typed command
tokens that alias a canonical skill (e.g. `handoff:load` -> `handoff:load-handoff`) are
merged via ALIASES, and rows are classified into current-roster / archived / non-roster
sections by scanning this repo's live skill roots.

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
CODEX_SESSIONS_DIR = Path.home() / ".codex" / "sessions"
REPO = Path(__file__).resolve().parent.parent

# Typed command token -> canonical skill name, exact-token matches only (verified:
# each token is documented in the target SKILL.md description; no roster dir of the
# alias name exists). Applied at summary time; raw ledger records stay raw.
ALIASES = {
    "load": "load-handoff",
    "save": "save-handoff",
    "search": "search-handoffs",
    "handoff:load": "handoff:load-handoff",
    "handoff:save": "handoff:save-handoff",
    "handoff:search": "handoff:search-handoffs",
}
COMMAND_RE = re.compile(r"<command-name>([^<]+)</command-name>")
CODEX_SKILL_RE = re.compile(r"<skill>\s*<name>([^<\n]+)</name>")
PREFILTER = ('"Skill"', '"SlashCommand"', "<command-name>")


def norm_skill(name: str) -> str:
    return name.strip().lstrip("/$").strip()


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
                        b.get("text", "")
                        for b in content
                        if isinstance(b, dict) and b.get("type") == "text"
                    )
                for text in texts:
                    for m in COMMAND_RE.finditer(text):
                        yield {
                            "key": f"{base['session']}:{rec.get('uuid')}:{norm_skill(m.group(1))}",
                            "skill": norm_skill(m.group(1)),
                            "source": "user",
                            **base,
                        }


def iter_codex_fires(path: Path):
    """Yield fire dicts from one Codex rollout file. Never raises on malformed lines.

    A typed `$skill` reaches the transcript as a user-role response_item whose input_text
    carries a `<skill><name>...</name>` injection block. Verified against the full session
    corpus: (timestamp, skill) pairs are unique across files (resumes do not replay fires),
    so `codex:{session}:{ts}:{skill}` is a stable dedupe key.
    """
    try:
        fh = path.open(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"skip {path.name}: {e}", file=sys.stderr)
        return
    session = cwd = None
    with fh:
        for line in fh:
            if session is None and '"session_meta"' in line:
                try:
                    meta = json.loads(line).get("payload") or {}
                    session, cwd = meta.get("id"), meta.get("cwd")
                except json.JSONDecodeError:
                    pass
            if "<skill>" not in line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = rec.get("payload") or {}
            if payload.get("type") != "message" or payload.get("role") != "user":
                continue
            content = payload.get("content") or []
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "input_text":
                    continue
                for m in CODEX_SKILL_RE.finditer(block.get("text", "")):
                    skill = norm_skill(m.group(1))
                    yield {
                        "key": f"codex:{session}:{rec.get('timestamp')}:{skill}",
                        "skill": skill,
                        "source": "user",
                        "ts": rec.get("timestamp"),
                        "cwd": cwd,
                        "session": session,
                        "sidechain": False,
                        "runtime": "codex",
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
        self.codex = 0
        self.subagent = 0
        self.cwds: set[str] = set()
        self.last = ""


def roster_names() -> set[str]:
    """Current skill names: dirs in skills/, skills-claude/, plugins/*/skills/."""
    roots = [
        REPO / "skills",
        REPO / "skills-claude",
        *sorted((REPO / "plugins").glob("*/skills")),
    ]
    names: set[str] = set()
    for root in roots:
        if not root.is_dir():
            raise SystemExit(
                f"roster scan failed: expected skill root missing. Got: {str(root)!r:.100}"
            )
        names.update(p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))
    return names


def archived_names() -> set[str]:
    root = REPO / "skills-archive"
    return {p.name for p in root.iterdir() if p.is_dir()} if root.is_dir() else set()


def summarize(records: list[dict]) -> None:
    roster = roster_names()
    archived = archived_names()
    for alias in ALIASES:
        if alias in roster or alias.rsplit(":", 1)[-1] in roster:
            raise SystemExit(
                f"alias merge failed: alias key shadows a roster skill. Got: {alias!r:.100}"
            )
    by_skill: defaultdict[str, SkillStats] = defaultdict(SkillStats)
    for r in records:
        token = str(r["skill"])
        s = by_skill[ALIASES.get(token, token)]
        s.total += 1
        if r.get("source") == "user":
            s.user += 1
        else:
            s.model += 1
        if r.get("runtime") == "codex":
            s.codex += 1
        if r.get("sidechain"):
            s.subagent += 1
        if r.get("cwd"):
            s.cwds.add(r["cwd"])
        ts = r.get("ts") or ""
        if ts > s.last:
            s.last = ts

    def section(token: str) -> str:
        # Full-token roster match first; bare-name fallback covers plugin-qualified
        # forms like `review-family:scrutinize`. The fallback classifies only —
        # alias merging is never done on it.
        if token in roster or token.rsplit(":", 1)[-1] in roster:
            return "roster"
        if token in archived or token.rsplit(":", 1)[-1] in archived:
            return "archived"
        return "other"

    rows = sorted(by_skill.items(), key=lambda kv: -kv[1].total)
    header = f"{'skill':<42} {'total':>5} {'model':>5} {'user':>5} {'codex':>5} {'subag':>5} {'cwds':>4}  last-fired"
    counts: dict[str, int] = {}
    for title, key in (
        ("current-roster skills", "roster"),
        ("archived skills (skills-archive/)", "archived"),
        ("non-roster tokens (built-in commands, plugin-qualified externals, retired/unknown)", "other"),
    ):
        sec = [(skill, s) for skill, s in rows if section(skill) == key]
        counts[key] = len(sec)
        if not sec:
            continue
        print(f"== {title} ==")
        print(header)
        for skill, s in sec:
            print(
                f"{skill:<42} {s.total:>5} {s.model:>5} {s.user:>5} {s.codex:>5} {s.subagent:>5} {len(s.cwds):>4}  {s.last[:10]}"
            )
        print()
    print(
        f"{len(rows)} distinct skills, {len(records)} fires total "
        f"(roster {counts['roster']}, archived {counts['archived']}, non-roster {counts['other']})"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", type=Path, default=LEDGER_DEFAULT)
    ap.add_argument(
        "--summary-only",
        action="store_true",
        help="summarize existing ledger; no mining",
    )
    args = ap.parse_args()

    existing = load_ledger(args.ledger)
    if args.summary_only:
        summarize(existing)
        return 0

    seen = {r["key"] for r in existing if "key" in r}
    new = []
    sources = [
        (PROJECTS_DIR, iter_fires),
        (CODEX_SESSIONS_DIR, iter_codex_fires),
    ]
    n_files = 0
    for root, iter_fn in sources:
        if not root.is_dir():
            print(f"skip {root}: not a directory", file=sys.stderr)
            continue
        files = sorted(root.rglob("*.jsonl"))
        n_files += len(files)
        for path in files:
            for fire in iter_fn(path):
                if fire["key"] in seen:
                    continue
                seen.add(fire["key"])
                new.append(fire)

    args.ledger.parent.mkdir(parents=True, exist_ok=True)
    with args.ledger.open("a", encoding="utf-8") as fh:
        for r in new:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(
        f"mined {n_files} transcripts, added {len(new)} new fires (ledger: {len(existing) + len(new)})\n"
    )
    summarize(existing + new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
