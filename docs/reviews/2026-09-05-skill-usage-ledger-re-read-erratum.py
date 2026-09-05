#!/usr/bin/env python3
"""Erratum re-run of the 2026-09-04 ledger re-read, on the repaired instrument (2026-09-05).

Sibling of the erratum section appended to docs/reviews/2026-09-04-skill-usage-ledger-re-read.md;
raw output in the .txt beside it. The 2026-09-04 script is left as written (it reproduces the
record); this one reads the same pre-registered set through the repaired miner, which now
records Codex model-invoked loads (shell reads of SKILL.md, `kind: "read"`) and scans
~/.codex/archived_sessions. Run from anywhere: python3 docs/reviews/2026-09-05-skill-usage-ledger-re-read-erratum.py
"""

import importlib.util
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

# The 2026-09-04 script runs on import; only its roster constant is wanted here, so the
# list is read from its text rather than executed.
ROSTER_0702 = [
    line.strip().strip('",')
    for line in (REPO / "docs/reviews/2026-09-04-skill-usage-ledger-re-read.py")
    .read_text()
    .split("ROSTER_0702 = [", 1)[1]
    .split("]", 1)[0]
    .splitlines()
    if line.strip().startswith('"')
]
assert len(ROSTER_0702) == 76, len(ROSTER_0702)

T0 = datetime(2026, 7, 2, 4, 47, 27, tzinfo=timezone.utc)
T1 = datetime(2026, 8, 1, 0, 0, 0, tzinfo=timezone.utc)
SCAN = miner.SCAN_READ_BURST


def bare(token: str) -> str:
    t = miner.ALIASES.get(token, token)
    return t.rsplit(":", 1)[-1]


def cwd_class(cwd):
    if not cwd:
        return "unknown"
    if cwd.startswith(("/private/tmp", "/tmp", "/var/folders", "/private/var")):
        return "tmp"
    if cwd == "/Users/jp/.agents" or cwd.startswith(
        ("/Users/jp/.agents/", "/Users/jp/.agents-worktrees", "/Users/jp/.synapsis/")
    ):
        return "agents"
    return "other"


raw = miner.load_ledger(miner.LEDGER_DEFAULT)
fires, cstats = miner.collapse(raw)
roster_now = miner.roster_names()

# ---- instrument delta: what the repair added ----
n_read = sum(1 for r in raw if r.get("kind") == "read")
n_arch = sum(1 for r in raw if r.get("archived"))
n_arch_tag = sum(1 for r in raw if r.get("archived") and r.get("kind") != "read")
print("== instrument delta (raw rows) ==")
print(f"ledger: {len(raw)} raw rows -> {len(fires)} fires after collapse {cstats}")
print(f"codex read rows (kind=read): {n_read}")
print(
    f"rows mined from ~/.codex/archived_sessions: {n_arch} ({n_arch_tag} typed tags, {n_arch - n_arch_tag} reads)"
)
print()

# ---- 0. first-instrument reconstruction must still hold (Claude rows only, before T0) ----
claude_pre: defaultdict[str, int] = defaultdict(int)
for r in fires:
    t = miner.parse_ts(r.get("ts"))
    if r.get("runtime") == "codex" or (t is not None and t >= T0):
        continue
    claude_pre[bare(str(r["skill"]))] += 1
zero_t0 = sorted(n for n in ROSTER_0702 if claude_pre[n] == 0)
print(
    f"== pre-registered set reconstruction: {76 - len(zero_t0)} fired / {len(zero_t0)} never (recorded 36 / 40) =="
)
assert len(zero_t0) == 40, (
    "reconstruction drifted; the erratum must not silently re-frame the set"
)
print()


# ---- per-skill accumulation, tags and reads apart ----
class Acc:
    def __init__(self):
        self.tag_pre = 0
        self.tag_post = 0
        self.tag_post_t1 = 0
        self.read_pre = 0
        self.read_post = 0
        self.read_post_t1 = 0
        self.read_choice_other = 0  # read in a non-scan session outside this repo
        self.read_scan_other = 0
        self.read_agents = 0
        self.read_tmp = 0
        self.tag_other = 0
        self.tag_agents = 0
        self.tag_tmp = 0
        self.arch = 0
        self.last = ""
        self.cwds_other = set()


acc: dict[str, Acc] = defaultdict(Acc)
for r in fires:
    t = miner.parse_ts(r.get("ts"))
    name = bare(str(r["skill"]))
    a = acc[name]
    a.last = max(a.last, r.get("ts") or "")
    if r.get("archived"):
        a.arch += 1
    is_read = r.get("kind") == "read"
    cc = cwd_class(r.get("cwd"))
    if t is None or t < T0:
        if is_read:
            a.read_pre += 1
        else:
            a.tag_pre += 1
        continue
    if is_read:
        a.read_post += 1
        if t >= T1:
            a.read_post_t1 += 1
        if cc == "other":
            if int(r.get("read_burst") or 1) >= SCAN:
                a.read_scan_other += 1
            else:
                a.read_choice_other += 1
                a.cwds_other.add(r.get("cwd"))
        elif cc == "agents":
            a.read_agents += 1
        elif cc == "tmp":
            a.read_tmp += 1
    else:
        a.tag_post += 1
        if t >= T1:
            a.tag_post_t1 += 1
        if cc == "other":
            a.tag_other += 1
            a.cwds_other.add(r.get("cwd"))
        elif cc == "agents":
            a.tag_agents += 1
        elif cc == "tmp":
            a.tag_tmp += 1


def status(a: Acc) -> str:
    if a.tag_post == 0 and a.read_post == 0:
        return "STILL-ZERO"
    if a.tag_other > 0:
        return "fired-tag-outside"
    if a.read_choice_other > 0:
        return "read-choice-outside"
    if a.read_scan_other > 0:
        return "read-scan-only"
    if a.tag_agents + a.read_agents > 0:
        return "agents-only"
    return "tmp-only"


hdr = (
    f"{'skill':<32} {'tag':>4} {'tag>=08':>7} {'read':>4} {'rd>=08':>6} {'rd-choice':>9} {'rd-scan':>7} "
    f"{'rd-agents':>9} {'tag-other':>9} {'arch':>4}  last        status"
)
print("== T0 zero-fire set (40): fires since T0, tags and reads apart ==")
print(hdr)
counts = defaultdict(int)
still_zero_ever = []
for n in zero_t0:
    a = acc[n]
    st = status(a)
    counts[st] += 1
    if st == "STILL-ZERO" and a.read_pre == 0 and a.tag_pre == 0:
        still_zero_ever.append(n)
    print(
        f"{n:<32} {a.tag_post:>4} {a.tag_post_t1:>7} {a.read_post:>4} {a.read_post_t1:>6} {a.read_choice_other:>9} "
        f"{a.read_scan_other:>7} {a.read_agents:>9} {a.tag_other:>9} {a.arch:>4}  {a.last[:10]:<10}  {st}"
        + (
            f" pre-T0: tag={a.tag_pre} read={a.read_pre}"
            if a.tag_pre or a.read_pre
            else ""
        )
    )
print()
print("status counts:", dict(counts))
print(
    f"never loaded anywhere, ever, under the repaired instrument: {len(still_zero_ever)} -> {' '.join(still_zero_ever)}"
)
print()
print(
    "== cwds outside this repo where T0-zero skills were chosen (tag or non-scan read) =="
)
for n in zero_t0:
    if acc[n].cwds_other:
        print(f"  {n}: {sorted(c for c in acc[n].cwds_other if c)}")
print()

# ---- current roster: never loaded ever ----
never_now = sorted(
    n
    for n in roster_now
    if acc[n].tag_pre + acc[n].tag_post + acc[n].read_pre + acc[n].read_post == 0
)
print(
    f"== current roster ({len(roster_now)}): never loaded anywhere, ever, under the repaired instrument: {len(never_now)} =="
)
print("  " + " ".join(never_now))
print()

# ---- how much the 2026-09-04 record under-counted, by row kind ----
post_tag = sum(a.tag_post for a in acc.values())
post_read = sum(a.read_post for a in acc.values())
print(
    f"post-T0 fires: {post_tag} tags + {post_read} reads = {post_tag + post_read} (the 2026-09-04 record counted 3,972 tags)"
)
