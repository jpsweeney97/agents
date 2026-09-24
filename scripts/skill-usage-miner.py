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

Raw ledger records are never rewritten (one exception: `--annotate-forks` adds fork
provenance fields to existing Codex rows in place, never changing a key or a value; see
below): the file is append-ordered (Claude projects, then Codex back-mining), NOT time-sorted — consumers must never assume chronology; compute date
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

Codex fork collapse (2026-09-24): Codex `spawn_agent` with `fork_turns: "all"` and Codex
Desktop thread forks copy the parent conversation into the new thread's rollout under
fresh timestamps, so one shaping on 2026-08-13 became 106 ledger rows
(docs/reviews/2026-09-24-outcome-shaping-methodology-critique.md). Codex later compacts
the copied prefix out of the fork's file, so the copied records cannot be re-found by
content, but the fork's `session_meta` keeps `forked_from_id`, `thread_source`, and its own
timestamp. Every Codex row therefore carries `forked_from` (when the thread is a fork),
`sidechain: true` when the thread is a subagent, and `copied: true` when the record was
written within FORK_COPY_WINDOW_S of the fork's creation (the copied prefix lands in the
first second). At summary time a copied row collapses into the parent thread's own row
for that skill or, when the parent was never mined, into one kept copy per (parent,
skill). Rows mined before these fields existed get them from `--annotate-forks`.
Per-turn re-reads of a SKILL.md are not a second inflation: a read row is already one
per (session, skill), and a read of a skill the session also tagged is suppressed.

The summary also prints a standing T1 blindness footnote (see FOOTNOTE): the ledger is
blind in both directions — rows are invocation/load markers, not proven fires — and any
re-read (the 2026-08-01 read in particular) must carry those caveats.

Usage: skill-usage-miner.py [--ledger PATH] [--summary-only | --annotate-forks]
"""

import argparse
import json
import os
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

# A forked Codex thread's rollout opens with a copy of the parent's records, all stamped
# within about a second of the fork's session_meta timestamp (0.2-0.6s on the
# 2026-08-13 forks; 0.005-9.6s across the pre-July corpus, one 31s outlier left as a
# fire). A record later than this was written by the fork itself.
FORK_COPY_WINDOW_S = 10.0

FOOTNOTE = """\
== T1 blindness footnote — read before treating rows as fires ==
The ledger is blind in both directions; rows are invocation/load markers, never proven fires.
- over-count: a Codex <skill> row records the capsule LOAD, not execution — known specimens
  where the agent declined the skill (routing questions) or the card was re-injected by a
  prose echo (simplify-code census, 2026-07-18). The summary collapses fork replays
  (Claude: a record uuid shared across session files; Codex: `copied` rows that a forked
  thread re-stamped from its parent, see --annotate-forks) and <=60s re-invokes; semantic
  echo rows beyond that remain counted.
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


def fork_provenance(meta: dict) -> dict:
    """What a Codex session_meta payload says about the thread's origin.

    Survives Codex's later compaction of a fork's copied prefix, which is why the
    collapse keys on this and not on the copied records themselves.
    """
    return {
        "forked_from": meta.get("forked_from_id") or None,
        "subagent": meta.get("thread_source") == "subagent",
        "created": parse_ts(meta.get("timestamp")),
    }


def fork_fields(ts: object, fork: dict) -> dict:
    """Row fields for one Codex record: `forked_from` when the thread is a fork, plus
    `copied: True` when the record sits inside the fork's copied prefix (within
    FORK_COPY_WINDOW_S of the fork's creation)."""
    fields: dict = {}
    if not fork.get("forked_from"):
        return fields
    fields["forked_from"] = fork["forked_from"]
    t, created = parse_ts(ts), fork.get("created")
    if (
        t is not None
        and created is not None
        and abs((t - created).total_seconds()) <= FORK_COPY_WINDOW_S
    ):
        fields["copied"] = True
    return fields


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

    Every row carries the thread's fork provenance from its session_meta (see
    fork_provenance / fork_fields): `sidechain` is true for a subagent thread, and a
    forked thread's rows carry `forked_from` plus `copied` when re-stamped from the parent.
    """
    try:
        fh = path.open(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"skip {path.name}: {e}", file=sys.stderr)
        return
    session = cwd = None
    fork: dict = {}
    tagged: set[str] = set()
    reads: dict[str, dict] = {}
    with fh:
        for line in fh:
            if session is None and '"session_meta"' in line:
                try:
                    meta = json.loads(line).get("payload") or {}
                except json.JSONDecodeError:
                    meta = {}
                session, cwd = meta.get("id"), meta.get("cwd")
                fork = fork_provenance(meta)
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
                "sidechain": fork.get("subagent", False),
                "runtime": "codex",
                **fork_fields(rec.get("timestamp"), fork),
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

    Codex fork-copy collapse: a row with `copied` is the parent thread's record
    re-stamped into a forked thread (`forked_from`). It collapses into the parent's
    own row for that skill when the parent was mined, else into the first copy seen
    for (parent, skill). A forked thread's own later rows are not copies and stay.

    Burst collapse: within one (session, bare canonical skill name), rows within
    BURST_WINDOW_S of the last kept row collapse into it — retries, double
    invokes, and the typed-command + Skill-call double record of a single fire.
    Rows without a parseable ts never burst-collapse.
    """
    kept: list[dict] = []
    stats = {"fork": 0, "copy": 0, "burst": 0}
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

    def bare(r: dict) -> str:
        token = str(r.get("skill"))
        return ALIASES.get(token, token).rsplit(":", 1)[-1]

    def burst_group(r: dict) -> "tuple[object, str]":
        return r.get("session"), bare(r)

    own = {(r.get("session"), bare(r)) for r in kept if not r.get("copied")}
    seen_copies: set[tuple] = set()
    uncopied: list[dict] = []
    for r in kept:
        if r.get("copied") and r.get("forked_from"):
            group = (r["forked_from"], bare(r))
            if group in own or group in seen_copies:
                stats["copy"] += 1
                continue
            seen_copies.add(group)
        uncopied.append(r)
    kept = uncopied

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
        f"(collapsed {cstats['fork']} fork replays, {cstats['copy']} Codex fork copies, "
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


def codex_session_meta(roots: "tuple[Path, ...] | None" = None) -> "dict[str, dict]":
    """Session id -> fork provenance, from the first line of every Codex rollout."""
    out: dict[str, dict] = {}
    for root in CODEX_ROOTS if roots is None else roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*.jsonl"):
            try:
                with path.open(encoding="utf-8", errors="replace") as fh:
                    meta = json.loads(fh.readline()).get("payload") or {}
            except (OSError, json.JSONDecodeError):
                continue
            if meta.get("id"):
                out[meta["id"]] = fork_provenance(meta)
    return out


def annotate_forks(
    ledger: Path,
    records: list[dict],
    size_at_load: int,
    metas: "dict[str, dict] | None" = None,
) -> "dict[str, int]":
    """Add fork provenance to existing Codex rows in place; keys and values untouched.

    The one write that touches existing rows. Rewrites the ledger atomically (temp
    file in the same directory, then rename) and refuses if the file changed size
    between the read and the write, since the live hook appends concurrently. A row
    the hook lands inside that window would otherwise be lost; the next mine run
    would re-add it, but refusing is cheaper than relying on that.
    """
    if metas is None:
        metas = codex_session_meta()
    stats = {"annotated": 0, "unchanged": 0, "no_meta": 0}
    for r in records:
        if r.get("runtime") != "codex":
            continue
        fork = metas.get(str(r.get("session")))
        if fork is None:
            stats["no_meta"] += 1
            continue
        desired = {"sidechain": fork["subagent"], **fork_fields(r.get("ts"), fork)}
        current = {"sidechain": bool(r.get("sidechain"))}
        for k in ("forked_from", "copied"):
            if r.get(k):
                current[k] = r[k]
        if desired == current:
            stats["unchanged"] += 1
            continue
        for k in ("forked_from", "copied"):
            r.pop(k, None)
        r.update(desired)
        stats["annotated"] += 1
    if not stats["annotated"]:
        return stats
    size_now = ledger.stat().st_size
    if size_now != size_at_load:
        raise SystemExit(
            f"annotate failed: ledger changed during rewrite, re-run. "
            f"Got: {size_at_load} -> {size_now} bytes"
        )
    tmp = ledger.with_name(ledger.name + ".annotate-tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    if ledger.stat().st_size != size_at_load:
        tmp.unlink()
        raise SystemExit(
            f"annotate failed: ledger changed during rewrite, re-run. "
            f"Got: {size_at_load} -> {ledger.stat().st_size} bytes"
        )
    os.replace(tmp, ledger)
    return stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", type=Path, default=LEDGER_DEFAULT)
    ap.add_argument(
        "--summary-only",
        action="store_true",
        help="summarize existing ledger; no mining",
    )
    ap.add_argument(
        "--annotate-forks",
        action="store_true",
        help="add fork provenance to existing Codex rows in place, then summarize; no mining",
    )
    args = ap.parse_args()

    size_at_load = args.ledger.stat().st_size if args.ledger.exists() else 0
    existing = load_ledger(args.ledger)
    if args.summary_only:
        summarize(existing)
        return 0
    if args.annotate_forks:
        astats = annotate_forks(args.ledger, existing, size_at_load)
        print(
            f"annotated {astats['annotated']} Codex rows with fork provenance "
            f"({astats['unchanged']} already current, {astats['no_meta']} with no rollout on disk)\n"
        )
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
