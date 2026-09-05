#!/usr/bin/env python3
"""Skill-usage miner: backfill and refresh the global skill-usage ledger from both runtimes' transcripts.

Scans ~/.claude/projects/*/*.jsonl (Claude Code) for skill fires:
- model-invoked: assistant tool_use blocks calling the Skill (or legacy SlashCommand) tool
- user-typed: <command-name> tags in user records (slash-command invocations)

Scans ~/.codex/sessions/**/*.jsonl and ~/.codex/archived_sessions/**/*.jsonl (Codex
rollouts; archiving a thread in Codex moves its rollout to the second store, and until
2026-09-05 the miner never looked there, so every fire in an archived thread was missing)
for skill fires:
- user-typed: <skill><name>...</name> injection blocks in user-role response_item messages
  (how Codex expands a typed `$skill` token).
- model-invoked: a shell tool call that reads a skill's SKILL.md (`cat`, `sed -n`, ...).
  When Codex chooses a skill itself it loads it by reading the file; no <skill> block is
  written, so until 2026-09-05 these fires were invisible (the regex-craft case that
  exposed it: four Codex sessions, zero ledger rows). One row per (session, skill),
  keyed `codex:{session}:read:{skill}`, with `kind: "read"`, `source: "model"`, and
  `read_burst` = how many distinct skills that session first read within
  READ_BURST_WINDOW_S of this one (`session_reads` = the session's total), so a
  consumer can discount a roster scan that read a dozen SKILL.md files in two minutes
  while choosing a route. A read of a skill the same session also loaded by tag is not
  recorded twice.
  Rows mined from the archive carry `archived: true` (informational; the key is the
  same in either store, so a thread archived after mining never double-counts).
Codex records carry `runtime: "codex"`; records without a runtime field are Claude's.
Codex has no live-hook equivalent, so Codex fires land only via re-running this miner;
a launchd job (com.jp.skill-usage-miner, source: scripts/com.jp.skill-usage-miner.plist)
runs it every ~5 days.

Appends new fire records to the cumulative ledger (JSONL), deduped by a stable key,
so transcripts pruned by retention stay in the ledger once mined. Re-runnable anytime;
the live PostToolUse hook (scripts/skill-usage-hook.py) writes the same ledger between runs.

Raw ledger records are never rewritten: the file is append-ordered (Claude projects, then
Codex back-mining), NOT time-sorted — consumers must never assume chronology; compute date
ranges from the `ts` field. All normalization happens at summary time only: typed command
tokens that alias a canonical skill (e.g. `handoff:load` -> `handoff:load-handoff`) are
merged via ALIASES, and rows are classified into current-roster / archived / non-roster
sections by scanning this repo's live skill roots.

Summary-time collapse (T1 over-count repair, 2026-07-19): the summary reads a collapsed
view of the raw rows — session-fork replays (a forked session file replays earlier records
under a new sessionId; the replayed record keeps its globally unique uuid/tool_use_id, so
rows sharing a key tail are one historical fire) and rapid re-invokes (rows for the same
session and skill within BURST_WINDOW_S, including the typed-command + Skill-call double
record one fire can leave) each count once. Codex rows are exempt from fork collapse:
their key tails (`ts:skill`) are not globally unique across sessions, and Codex resumes
are verified not to replay fires. Raw rows are untouched; the collapse is disclosed in
the summary output.

The summary also prints a standing T1 blindness footnote (see FOOTNOTE): the ledger is
blind in both directions — rows are invocation/load markers, not proven fires — and any
re-read (the 2026-08-01 read in particular) must carry those caveats.

Usage: skill-usage-miner.py [--ledger PATH] [--summary-only]
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

LEDGER_DEFAULT = Path.home() / ".claude" / "logs" / "skill-usage-ledger.jsonl"
PROJECTS_DIR = Path.home() / ".claude" / "projects"
CODEX_SESSIONS_DIR = Path.home() / ".codex" / "sessions"
CODEX_ARCHIVED_DIR = Path.home() / ".codex" / "archived_sessions"
CODEX_ROOTS = (CODEX_SESSIONS_DIR, CODEX_ARCHIVED_DIR)
REPO = Path(__file__).resolve().parent.parent

# A shell tool call reading a skill file. The captured group is the skill directory;
# its basename is the skill, qualified `<plugin>:<name>` when the directory sits under
# a plugin tree (repo source `plugins/<p>/skills/<name>` or the Codex plugin cache
# `.../turbo-mode/<p>/<version>/skills/<name>`), matching the typed-token form.
SKILL_READ_RE = re.compile(r"([\w.~+@-]*(?:/[\w.~+@-]+)*)/SKILL\.md\b")
PLUGIN_SKILL_DIR_RE = re.compile(
    r"(?:/plugins/(?P<p1>[\w.~+@-]+)/skills|/turbo-mode/(?P<p2>[\w.~+@-]+)/[\w.~+@-]+/skills)"
    r"/(?P<name>[\w.~+@-]+)$"
)
CODEX_TOOL_CALL_TYPES = ("custom_tool_call", "function_call")
# Tool calls that write a SKILL.md are edits, not loads.
CODEX_EDIT_TOOL_NAMES = ("apply_patch",)
# A roster scan reads many SKILL.md files in quick succession; a chosen skill is read
# on its own when the task needs it. Each read row carries `read_burst`: how many
# distinct skills the session first read within READ_BURST_WINDOW_S of this one
# (itself included). At or above SCAN_READ_BURST the read is a scan, not a choice.
# Consumers may pick their own cut; the row carries the count so they can. A
# per-session total (`session_reads`) is also carried, but long real-work sessions
# read a dozen skills over hours, so the burst is the discriminating signal.
READ_BURST_WINDOW_S = 180.0
SCAN_READ_BURST = 4

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

# Rows for the same session+skill closer than this are one fire (retries, double
# invokes, and the typed-command + Skill-call double record). Known specimen: the
# 13s double-invoke pair in session 5c843a6a (2026-07-06).
BURST_WINDOW_S = 60.0

FOOTNOTE = """\
== T1 blindness footnote — read before treating rows as fires ==
The ledger is blind in both directions; rows are invocation/load markers, never proven fires.
- over-count: a Codex <skill> row records the capsule LOAD, not execution — known specimens
  where the agent declined the skill (routing questions) or the card was re-injected by a
  prose echo (simplify-code census, 2026-07-18). The summary collapses fork replays and
  <=60s re-invokes; semantic echo rows beyond that remain counted.
- Codex read rows (`kind: "read"`, the `reads` column): a model-invoked Codex skill is a
  shell read of its SKILL.md, recorded once per session and skill. A read is a LOAD
  with weaker intent than a tag: a session that read many skills while choosing a route
  (`read_burst` >= SCAN_READ_BURST) was scanning, not firing them all. Before
  2026-09-05 no read was recorded and ~/.codex/archived_sessions was never scanned, so
  every ledger read made before that date under-counted Codex (regex-craft: four
  sessions, zero rows).
- under-count (no row can exist): Claude-side skills exercised with no Skill call and no
  typed command (handoff-resumed arcs — e.g. the 07-18/19 methodology-critique treatment
  sessions before mining; a Read of a SKILL.md without a Skill call is not mined);
  Codex-side loads that read only a skill's references/, multi-cycle chains (one tag or
  read -> many cycles), and harness-driven runs (simplify-code census); skills whose
  realistic configurations bypass both instruments (e.g. deliberate's pipeline).
- lag: the live hook records Skill-tool calls only; typed commands and everything else
  land only when this miner runs (launchd ~5 days).
- endogeneity: a fire census is an intervention — treatments can summon the fires they
  count (Era 109/113); treat post-treatment fire surges as partially endogenous before
  crediting or debiting any skill for them.
Sources: docs/reviews/2026-07-18-deliberate-methodology-critique.md (T1),
docs/reviews/2026-07-18-simplify-code-methodology-critique.md (census, observer effect),
docs/reviews/2026-07-19-methodology-critique-methodology-critique.md (unledgered fires)."""


def norm_skill(name: str) -> str:
    return name.strip().lstrip("/$").strip()


def skill_from_read_path(skill_dir: str) -> str:
    """Skill token for a SKILL.md read: bare dir name, plugin-qualified under a plugin tree."""
    m = PLUGIN_SKILL_DIR_RE.search(skill_dir)
    if m:
        return f"{m.group('p1') or m.group('p2')}:{m.group('name')}"
    return skill_dir.rsplit("/", 1)[-1]


def codex_tool_call_text(payload: dict) -> str:
    """The command text of a Codex shell call, whichever field the rollout format used.

    Older rollouts: `function_call` with a JSON string in `arguments`; newer ones:
    `custom_tool_call` (name `exec`) with a JS snippet string in `input`.
    """
    for field in ("input", "arguments"):
        val = payload.get(field)
        if isinstance(val, str):
            return val
        if val is not None:
            return json.dumps(val)
    return ""


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


def iter_codex_fires(path: Path, archived: bool = False):
    """Yield fire dicts from one Codex rollout file. Never raises on malformed lines.

    A typed `$skill` reaches the transcript as a user-role response_item whose input_text
    carries a `<skill><name>...</name>` injection block. Verified against the full session
    corpus: (timestamp, skill) pairs are unique across files (resumes do not replay fires),
    so `codex:{session}:{ts}:{skill}` is a stable dedupe key.

    A model-invoked skill reaches the transcript as a shell tool call whose command reads
    the skill's SKILL.md. Those are buffered per file and yielded at the end as one
    `kind: "read"` row per skill, keyed `codex:{session}:read:{skill}`, annotated with
    `read_burst` (distinct skills first read within READ_BURST_WINDOW_S of it) and
    `session_reads` (distinct skills the session read); a skill the same session also
    loaded by tag is not yielded as a read.
    """
    try:
        fh = path.open(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"skip {path.name}: {e}", file=sys.stderr)
        return
    session = cwd = None
    tagged: set[str] = set()
    reads: dict[str, dict] = {}
    with fh:
        for line in fh:
            if session is None and '"session_meta"' in line:
                try:
                    meta = json.loads(line).get("payload") or {}
                    session, cwd = meta.get("id"), meta.get("cwd")
                except json.JSONDecodeError:
                    pass
            is_tag = "<skill>" in line
            is_read = "SKILL.md" in line
            if not (is_tag or is_read):
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = rec.get("payload") or {}
            base = {
                "ts": rec.get("timestamp"),
                "cwd": cwd,
                "session": session,
                "sidechain": False,
                "runtime": "codex",
            }
            if archived:
                base["archived"] = True
            if is_read and payload.get("type") in CODEX_TOOL_CALL_TYPES:
                if payload.get("name") in CODEX_EDIT_TOOL_NAMES:
                    continue
                for m in SKILL_READ_RE.finditer(codex_tool_call_text(payload)):
                    skill = skill_from_read_path(m.group(1))
                    # A glob or a bare `SKILL.md` leaves no directory: not a load.
                    if not skill or skill.endswith(":"):
                        continue
                    if skill not in reads:
                        reads[skill] = {
                            "key": f"codex:{session}:read:{skill}",
                            "skill": skill,
                            "source": "model",
                            "kind": "read",
                            **base,
                        }
                continue
            if not is_tag:
                continue
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
                    tagged.add(skill.rsplit(":", 1)[-1])
                    yield {
                        "key": f"codex:{session}:{rec.get('timestamp')}:{skill}",
                        "skill": skill,
                        "source": "user",
                        **base,
                    }
    first_read = {s: parse_ts(r.get("ts")) for s, r in reads.items()}
    for skill, row in reads.items():
        if skill.rsplit(":", 1)[-1] in tagged:
            continue
        mine = first_read[skill]
        row["read_burst"] = (
            sum(
                1
                for other in first_read.values()
                if mine is not None
                and other is not None
                and abs((other - mine).total_seconds()) <= READ_BURST_WINDOW_S
            )
            or 1
        )
        row["session_reads"] = len(reads)
        yield row


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


def parse_ts(ts: object) -> "datetime | None":
    if not ts:
        return None
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except ValueError:
        return None


def collapse(records: list[dict]) -> "tuple[list[dict], dict[str, int]]":
    """Collapsed summary view of raw rows; the ledger itself is never rewritten.

    Fork-replay collapse: Claude keys are `{session}:{uuid}:{skill}` (mined user),
    `{session}:{tool_use_id}` (mined model / hook) — the tail after the session is
    globally unique, so two rows sharing a tail are one historical fire replayed
    into a forked session file. Codex keys (`codex:{session}:{ts}:{skill}`) are
    exempt: their tails are not globally unique and Codex resumes do not replay
    fires. Hook fallback tails (`hook-{ts}`, written when tool_use_id was absent)
    are exempt for the same reason.

    Burst collapse: within one (session, bare canonical skill name), rows within
    BURST_WINDOW_S of the last kept row collapse into it — retries, double
    invokes, and the typed-command + Skill-call double record of a single fire.
    Rows without a parseable ts never burst-collapse.
    """
    kept: list[dict] = []
    stats = {"fork": 0, "burst": 0}
    seen_tails: set[str] = set()
    for r in records:
        key = str(r.get("key") or "")
        if key and not key.startswith("codex:") and ":" in key:
            tail = key.split(":", 1)[1]
            if not tail.startswith("hook-"):
                if tail in seen_tails:
                    stats["fork"] += 1
                    continue
                seen_tails.add(tail)
        kept.append(r)

    def burst_group(r: dict) -> "tuple[object, str]":
        token = str(r.get("skill"))
        return r.get("session"), ALIASES.get(token, token).rsplit(":", 1)[-1]

    groups: defaultdict[tuple, list[tuple[datetime, int]]] = defaultdict(list)
    for i, r in enumerate(kept):
        t = parse_ts(r.get("ts"))
        if t is not None:
            groups[burst_group(r)].append((t, i))
    drop: set[int] = set()
    for timed in groups.values():
        timed.sort()
        last_kept = None
        for t, i in timed:
            if (
                last_kept is not None
                and (t - last_kept).total_seconds() <= BURST_WINDOW_S
            ):
                drop.add(i)
                stats["burst"] += 1
            else:
                last_kept = t
    return [r for i, r in enumerate(kept) if i not in drop], stats


class SkillStats:
    def __init__(self) -> None:
        self.total = 0
        self.model = 0
        self.user = 0
        self.codex = 0
        self.reads = 0
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
        names.update(
            p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")
        )
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
    raw_n = len(records)
    records, cstats = collapse(records)
    print(
        f"view: {raw_n} raw rows -> {len(records)} fires "
        f"(collapsed {cstats['fork']} fork replays, "
        f"{cstats['burst']} rapid re-invokes <={BURST_WINDOW_S:.0f}s)\n"
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
        if r.get("kind") == "read":
            s.reads += 1
        if r.get("sidechain"):
            s.subagent += 1
        if r.get("cwd"):
            s.cwds.add(r["cwd"])
        ts = r.get("ts") or ""
        s.last = max(s.last, ts)

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
    header = f"{'skill':<42} {'total':>5} {'model':>5} {'user':>5} {'codex':>5} {'reads':>5} {'subag':>5} {'cwds':>4}  last-fired"
    counts: dict[str, int] = {}
    for title, key in (
        ("current-roster skills", "roster"),
        ("archived skills (skills-archive/)", "archived"),
        (
            "non-roster tokens (built-in commands, plugin-qualified externals, retired/unknown)",
            "other",
        ),
    ):
        sec = [(skill, s) for skill, s in rows if section(skill) == key]
        counts[key] = len(sec)
        if not sec:
            continue
        print(f"== {title} ==")
        print(header)
        for skill, s in sec:
            print(
                f"{skill:<42} {s.total:>5} {s.model:>5} {s.user:>5} {s.codex:>5} {s.reads:>5} {s.subagent:>5} {len(s.cwds):>4}  {s.last[:10]}"
            )
        print()
    print(
        f"{len(rows)} distinct skills, {len(records)} fires total "
        f"(roster {counts['roster']}, archived {counts['archived']}, non-roster {counts['other']})"
    )
    print()
    print(FOOTNOTE)


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
    sources = [(PROJECTS_DIR, "claude"), *((root, "codex") for root in CODEX_ROOTS)]
    n_files = 0
    for root, runtime in sources:
        if not root.is_dir():
            print(f"skip {root}: not a directory", file=sys.stderr)
            continue
        files = sorted(root.rglob("*.jsonl"))
        n_files += len(files)
        for path in files:
            if runtime == "claude":
                fires = iter_fires(path)
            else:
                fires = iter_codex_fires(path, archived=root == CODEX_ARCHIVED_DIR)
            for fire in fires:
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
