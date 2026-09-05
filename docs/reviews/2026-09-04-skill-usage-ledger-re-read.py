#!/usr/bin/env python3
"""2026-08-01 ledger re-read (run 2026-09-04): suffix-aware, read against the 2026-07-02 branches.

Sibling of docs/reviews/2026-09-04-skill-usage-ledger-re-read.md; its raw output is the .txt beside it.
Reuses the miner's own load/collapse/alias/roster code so the view matches the summary tool.
Run from anywhere: python3 docs/reviews/2026-09-04-skill-usage-ledger-re-read.py
"""

import importlib.util
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/Users/jp/.agents")
spec = importlib.util.spec_from_file_location(
    "miner", REPO / "scripts/skill-usage-miner.py"
)
assert spec is not None and spec.loader is not None, "miner import failed"
miner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(miner)

# Challenge record landed 2026-07-02T00:47:27-04:00 (commit 756501f) -> the first read's moment.
T0 = datetime(2026, 7, 2, 4, 47, 27, tzinfo=timezone.utc)
T1 = datetime(2026, 8, 1, 0, 0, 0, tzinfo=timezone.utc)

ROSTER_0702 = [
    "acceptance-map",
    "agent-facing-design",
    "baseline",
    "behavior-smoke-test",
    "caveman",
    "claude-code-docs",
    "contract-change-propagation",
    "decision-record",
    "dependency-upgrade",
    "deploy-plan",
    "design-exploration",
    "diagnose",
    "doc-drift-audit",
    "email-writing",
    "execute-plan",
    "explain-codebase",
    "grill-me",
    "grill-with-docs",
    "ideate",
    "implementation-planning",
    "improve-codebase-architecture",
    "incident-response",
    "keep-green",
    "making-recommendations",
    "markdown-reformat",
    "markdown-synthesis",
    "migration-campaign",
    "migration-safety",
    "next-steps",
    "observability-instrumentation",
    "orient-status",
    "outcome-check",
    "outcome-interviewer",
    "postmortem",
    "premortem",
    "prototype",
    "red-team",
    "reflect",
    "regex-craft",
    "research-capture",
    "runbook-authoring",
    "scope-cut",
    "simplify-code",
    "skill-ux-design",
    "spec-drift-reconcile",
    "steelman",
    "tdd",
    "tech-debt-scan",
    "to-issues",
    "to-prd",
    "triage",
    "working-slice-review",
    "writing-principles",
    "zoom-out",
    "friction-to-guards",
    "openai-docs",
    "setup-matt-pocock-skills",
    "skill-benchmark",
    "skill-squad",
    "closeout-check",
    "exiting-worktrees",
    "gh-address-comments",
    "gh-pr-review-loop",
    "git-hygiene",
    "merge-branch",
    "pr-description",
    "release-cut",
    "load-handoff",
    "save-handoff",
    "search-handoffs",
    "throughline",
    "implementation-review",
    "review-reviewer",
    "scrutinize-skill",
    "scrutinize",
    "system-design-review",
]
assert len(ROSTER_0702) == 76, len(ROSTER_0702)


def bare(token: str) -> str:
    t = miner.ALIASES.get(token, token)
    return t.rsplit(":", 1)[-1]


def cwd_class(cwd):
    if not cwd:
        return "unknown"
    if cwd.startswith(("/private/tmp", "/tmp", "/var/folders", "/private/var")):
        return "tmp"
    if cwd == "/Users/jp/.agents" or cwd.startswith(
        ("/Users/jp/.agents/", "/Users/jp/.agents-worktrees")
    ):
        return "agents"
    return "other"


raw = miner.load_ledger(miner.LEDGER_DEFAULT)
fires, cstats = miner.collapse(raw)
roster_now = miner.roster_names()
archived = miner.archived_names()


# ---- per-skill accumulation ----
class Acc:
    def __init__(self):
        self.pre = 0
        self.post = 0
        self.post_t1 = 0
        self.post_by = defaultdict(
            int
        )  # keys: claude/codex, user/model, main/subagent, cwd class
        self.post_cwds = set()
        self.tokens = set()
        self.last = ""
        self.first = ""


acc: dict[str, Acc] = defaultdict(Acc)
ts_min_claude = ts_min_codex = None
for r in fires:
    t = miner.parse_ts(r.get("ts"))
    name = bare(str(r["skill"]))
    a = acc[name]
    a.tokens.add(str(r["skill"]))
    ts = r.get("ts") or ""
    a.last = max(a.last, ts)
    if not a.first or (ts and ts < a.first):
        a.first = ts
    is_codex = r.get("runtime") == "codex"
    if t is not None:
        if is_codex:
            ts_min_codex = (
                t if ts_min_codex is None or t < ts_min_codex else ts_min_codex
            )
        else:
            ts_min_claude = (
                t if ts_min_claude is None or t < ts_min_claude else ts_min_claude
            )
    if t is None or t < T0:
        a.pre += 1
        continue
    a.post += 1
    if t >= T1:
        a.post_t1 += 1
    a.post_by["codex" if is_codex else "claude"] += 1
    a.post_by["user" if r.get("source") == "user" else "model"] += 1
    a.post_by["subagent" if r.get("sidechain") else "main"] += 1
    a.post_by[cwd_class(r.get("cwd"))] += 1
    if r.get("cwd"):
        a.post_cwds.add(r["cwd"])


def skill_paths(name: str) -> list[str]:
    """Every home the skill has had; plugin roots expanded here (git's glob pathspec missed them)."""
    paths = [f"skills/{name}", f"skills-claude/{name}", f"skills-archive/{name}"]
    paths += [
        f"plugins/{p.parent.name}/skills/{name}"
        for p in sorted((REPO / "plugins").glob("*/skills"))
    ]
    return paths


def first_commit(name: str) -> str:
    out = (
        subprocess.run(
            [
                "git",
                "-C",
                str(REPO),
                "log",
                "--format=%aI",
                "--reverse",
                "--",
                *skill_paths(name),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        .stdout.strip()
        .splitlines()
    )
    return out[0][:10] if out else "?"


def explicit_only(name: str) -> str:
    """'claude-explicit' / 'codex-explicit' when the skill is hidden from the model's list; frontmatter only."""
    flags = []
    for root in (
        REPO / "skills",
        REPO / "skills-claude",
        *sorted((REPO / "plugins").glob("*/skills")),
    ):
        d = root / name
        if not d.is_dir():
            continue
        sk = d / "SKILL.md"
        if sk.is_file():
            parts = sk.read_text(errors="replace").split("---", 2)
            fm = parts[1] if len(parts) >= 3 else ""
            if "disable-model-invocation: true" in fm:
                flags.append("claude-explicit")
        oy = d / "agents" / "openai.yaml"
        if oy.is_file() and "allow_implicit_invocation: false" in oy.read_text(
            errors="replace"
        ):
            flags.append("codex-explicit")
    return ",".join(flags) if flags else "-"


# ---- 0. first-instrument view: Claude rows only before T0 (what 2026-07-02 could see) ----
claude_pre: defaultdict[str, int] = defaultdict(int)  # suffix-aware
exact_pre: defaultdict[str, int] = defaultdict(int)  # exact bare token only
for r in fires:
    t = miner.parse_ts(r.get("ts"))
    if r.get("runtime") == "codex" or (t is not None and t >= T0):
        continue
    claude_pre[bare(str(r["skill"]))] += 1
    tok = str(r["skill"])
    if ":" not in tok:
        exact_pre[tok] += 1
zero_claude_view = sorted(n for n in ROSTER_0702 if claude_pre[n] == 0)
zero_exact_view = sorted(n for n in ROSTER_0702 if exact_pre[n] == 0)
print("== first-instrument reconstruction (Claude rows only, before T0) ==")
print(
    f"suffix-aware: {76 - len(zero_claude_view)} fired / {len(zero_claude_view)} never"
)
print("  never:", " ".join(zero_claude_view))
print(
    f"exact bare token: {76 - len(zero_exact_view)} fired / {len(zero_exact_view)} never"
)
print("  never:", " ".join(zero_exact_view))
print(
    "  exact-view names that suffix-aware credits:",
    sorted(set(zero_exact_view) - set(zero_claude_view)),
)
print(
    "  first-instrument-zero names that Codex rows credit pre-T0:",
    sorted(n for n in zero_claude_view if acc[n].pre > 0),
)
print()
print("== explicit-only flags across the current roster ==")
for n in sorted(roster_now):
    f = explicit_only(n)
    if f != "-":
        print(f"  {n:<32} {f}")
print()

# ---- 1. the 2026-07-02 zero-fire set, reconstructed ----
all_runtime_zero = sorted(n for n in ROSTER_0702 if acc[n].pre == 0)
zero_t0 = (
    zero_claude_view  # the pre-registered 40: what the 2026-07-02 instrument could see
)
fired_t0 = sorted(n for n in ROSTER_0702 if n not in zero_t0)
print(f"ledger: {len(raw)} raw rows -> {len(fires)} fires after collapse {cstats}")
print(f"earliest claude row: {ts_min_claude}   earliest codex row: {ts_min_codex}")
print(
    f"T0 (first read) = {T0.isoformat()}   T1 (committed re-read date) = {T1.isoformat()}"
)
print()
print(
    f"== 2026-07-02 roster: 76 skills; pre-registered set (first-instrument view): {len(fired_t0)} fired / {len(zero_t0)} never (recorded: 36 / 40); all-runtime view at T0 with Codex rows: {76 - len(all_runtime_zero)} fired / {len(all_runtime_zero)} never =="
)
print("never-fired-at-T0 (reconstructed):", " ".join(zero_t0))
print()

# ---- 2. what happened to the T0 zero set since ----
hdr = f"{'skill':<32} {'post':>4} {'>=08-01':>7} {'claude':>6} {'codex':>5} {'user':>4} {'model':>5} {'subag':>5} {'tmp':>3} {'agents':>6} {'other':>5}  last        born       status"
print("== T0 zero-fire set: fires since T0 ==")
print(hdr)
status_counts = defaultdict(int)
zero_rows = []
for n in zero_t0:
    a = acc[n]
    b = a.post_by
    if a.post == 0:
        status = "STILL-ZERO"
    elif b["other"] > 0:
        status = "fired-outside-agents"
    elif b["agents"] > 0:
        status = "fired-in-agents-only"
    else:
        status = "fired-tmp-only"
    status_counts[status] += 1
    born = first_commit(n)
    where = "" if n in roster_now else ("(archived)" if n in archived else "(gone)")
    zero_rows.append((n, a, status, born, where))
    print(
        f"{n:<32} {a.post:>4} {a.post_t1:>7} {b['claude']:>6} {b['codex']:>5} {b['user']:>4} {b['model']:>5} {b['subagent']:>5} {b['tmp']:>3} {b['agents']:>6} {b['other']:>5}  {a.last[:10]:<10}  {born}  {status} {where} codex-pre={a.pre} {explicit_only(n)}"
    )
print()
print("status counts:", dict(status_counts))
print()
print("== cwds seen post-T0 for T0-zero skills that fired ==")
for n, a, status, born, where in zero_rows:
    if a.post:
        print(f"  {n}: {sorted(a.post_cwds)}")
print()

# ---- 3. the T0 fired set: still firing? ----
print("== T0 fired set (36): fires since T0 ==")
print(hdr)
silent_since = []
for n in fired_t0:
    a = acc[n]
    b = a.post_by
    status = (
        "silent-since-T0"
        if a.post == 0
        else (
            "tmp-only"
            if b["other"] == 0 and b["agents"] == 0
            else ("agents-only" if b["other"] == 0 else "outside-agents")
        )
    )
    if a.post == 0:
        silent_since.append(n)
    print(
        f"{n:<32} {a.post:>4} {a.post_t1:>7} {b['claude']:>6} {b['codex']:>5} {b['user']:>4} {b['model']:>5} {b['subagent']:>5} {b['tmp']:>3} {b['agents']:>6} {b['other']:>5}  {a.last[:10]:<10}  pre={a.pre:<4} {status}"
    )
print()
print("fired-at-T0 but silent since:", silent_since)
print()

# ---- 4. current roster ----
new_since = sorted(roster_now - set(ROSTER_0702))
gone_since = sorted(set(ROSTER_0702) - roster_now)
never_ever_now = sorted(n for n in roster_now if acc[n].pre + acc[n].post == 0)
print(
    f"== current roster: {len(roster_now)} skills; new since T0: {len(new_since)}; from T0 roster no longer present: {gone_since} =="
)
print(f"never fired ever (current roster): {len(never_ever_now)}")
for n in never_ever_now:
    print(f"  {n:<32} born {first_commit(n)}")
print()
print("== skills added since T0: fires ==")
print(hdr)
for n in new_since:
    a = acc[n]
    b = a.post_by
    print(
        f"{n:<32} {a.post:>4} {a.post_t1:>7} {b['claude']:>6} {b['codex']:>5} {b['user']:>4} {b['model']:>5} {b['subagent']:>5} {b['tmp']:>3} {b['agents']:>6} {b['other']:>5}  {a.last[:10]:<10}  {first_commit(n)}"
    )
print()

# ---- 5. totals & hot core (post-T0, suffix-merged) ----
post_total = sum(a.post for a in acc.values())
post_roster = sorted(
    ((n, a.post) for n, a in acc.items() if n in roster_now and a.post),
    key=lambda x: -x[1],
)
print(f"post-T0 fires: {post_total} across all tokens; roster-suffix-merged top 15:")
for n, c in post_roster[:15]:
    print(f"  {n:<32} {c}")
print()
print("== suffix merges applied to roster names (tokens folded) ==")
for n in sorted(acc):
    if n in roster_now and len(acc[n].tokens) > 1:
        print(f"  {n}: {sorted(acc[n].tokens)}")
