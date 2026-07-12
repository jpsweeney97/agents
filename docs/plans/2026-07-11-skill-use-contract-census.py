#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Generated edge census + ledger recompute for the skill-use contract design doc.

Emits the raw evidence behind `2026-07-11-skill-use-contract-design.md` so review
rounds verify a committed artifact's diff instead of re-deriving prose (the fifth
review round found that prose transcription was where every census error entered).

Two sections:

1. Edge census — for every chain edge the design doc names, grep the source
   skill's `SKILL.md` for the target lane name, tagged FRONTMATTER (description
   altitude) or BODY (exit altitude). The pinned rule: a forward edge exists iff
   the BODY directs the follow-on lane by name; the doc adjudicates borderlines.
2. Ledger recompute — suffix-aware (never exact-name: plugin/namespaced keys such
   as `review-family:scrutinize-skill` and `sbonly:skill-benchmark` make exact
   matching silently undercount). The exact-name skill-squad overlap is printed
   alongside deliberately, to document the prefix-blind bug the fifth round found.

Usage: run from anywhere; redirect stdout to the sibling `.txt` artifact.
Optional argv[1] overrides the ledger path (default: ~/.claude/logs/skill-usage-ledger.jsonl).
Output is deterministic given the repo tree and ledger file (no wall-clock reads).
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Chain edges from the design doc's Evidence Inventory. Receiving-side compose
# notes (chain 4) are censused too; the doc records them as non-touched-list data.
CHAIN_EDGES: list[tuple[str, str, str]] = [
    ("1", "diagnose", "tdd"),
    ("1", "tdd", "keep-green"),
    ("2", "test-trust-audit", "characterization-tests"),
    ("2", "characterization-tests", "simplify-code"),
    ("3", "contract-change-propagation", "migration-campaign"),
    ("4", "red-team", "authorization-design"),
    ("4", "red-team", "injection-safe-inputs"),
    ("4", "authorization-design", "red-team"),
    ("4", "injection-safe-inputs", "red-team"),
    ("5", "incident-response", "diagnose"),
    ("5", "incident-response", "postmortem"),
    ("5", "postmortem", "runbook-authoring"),
    ("6", "observability-instrumentation", "deploy-plan"),
    ("6", "observability-instrumentation", "outcome-check"),
    ("6", "deploy-plan", "outcome-check"),
    ("7", "skill-squad", "scrutinize-skill"),
    ("7", "skill-squad", "behavior-smoke-test"),
    ("7", "skill-squad", "skill-benchmark"),
    ("7", "scrutinize-skill", "behavior-smoke-test"),
    ("7", "behavior-smoke-test", "skill-benchmark"),
    ("8", "making-recommendations", "ideate"),
    ("8", "ideate", "making-recommendations"),
]

SKILL_PATH_OVERRIDES: dict[str, str] = {
    "skill-squad": "skills-claude/skill-squad/SKILL.md",
    "scrutinize-skill": "plugins/review-family/skills/scrutinize-skill/SKILL.md",
}

LEDGER_SKILLS: list[str] = [
    "making-recommendations", "outcome-shaping", "design-exploration", "ideate",
    "diagnose", "incident-response", "postmortem", "keep-green", "tdd",
    "characterization-tests", "contract-change-propagation", "test-trust-audit",
    "red-team", "skill-squad", "scrutinize-skill", "behavior-smoke-test",
    "skill-benchmark",
]

FULL_CHAIN_7 = {"skill-squad", "scrutinize-skill", "behavior-smoke-test", "skill-benchmark"}


def skill_path(name: str) -> Path:
    """Resolve a skill name to its SKILL.md path in this repo."""
    rel = SKILL_PATH_OVERRIDES.get(name, f"skills/{name}/SKILL.md")
    path = REPO_ROOT / rel
    if not path.is_file():
        raise FileNotFoundError(f"skill lookup failed: SKILL.md missing. Got: {str(path)!r:.100}")
    return path


def split_frontmatter(lines: list[str], path: Path) -> int:
    """Return the 1-indexed line number of the closing frontmatter fence."""
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"frontmatter parse failed: no opening fence. Got: {str(path)!r:.100}")
    for i, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return i
    raise ValueError(f"frontmatter parse failed: no closing fence. Got: {str(path)!r:.100}")


def census_edge(source: str, target: str) -> list[str]:
    """Grep source skill's SKILL.md for the target name, tagged by altitude."""
    path = skill_path(source)
    lines = path.read_text(encoding="utf-8").splitlines()
    fm_end = split_frontmatter(lines, path)
    pattern = re.compile(rf"(?<![\w-]){re.escape(target)}(?![\w-])")
    hits: list[str] = []
    for lineno, line in enumerate(lines, start=1):
        if pattern.search(line):
            altitude = "FRONTMATTER" if lineno <= fm_end else "BODY"
            hits.append(f"    {lineno}:{altitude}: {line.strip()[:160]}")
    return hits


def base_name(key: str) -> str:
    """Suffix-aware base skill name: strip any namespace prefix."""
    return key.split(":")[-1]


def load_ledger(path: Path) -> list[dict]:
    """Read the JSONL usage ledger."""
    if not path.is_file():
        raise FileNotFoundError(f"ledger read failed: file missing. Got: {str(path)!r:.100}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    print("# Skill-use contract census — generated artifact")
    print(f"# Script: docs/plans/{Path(__file__).name}  (repo root: {REPO_ROOT.name})")
    print()
    print("## Section 1 — edge census (grep of SKILL.md, FRONTMATTER = description altitude, BODY = exit altitude)")
    print("## Pinned rule: forward edge exists iff the BODY directs the follow-on lane by name;")
    print("## contrast-only or boundary mentions do not count — the design doc records those adjudications.")
    print()
    for chain, source, target in CHAIN_EDGES:
        print(f"chain {chain}: {source} -> {target}   [{skill_path(source).relative_to(REPO_ROOT)}]")
        hits = census_edge(source, target)
        print("\n".join(hits) if hits else "    (no mentions at any altitude)")
        print()

    ledger_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / ".claude/logs/skill-usage-ledger.jsonl"
    recs = load_ledger(ledger_path)
    print("## Section 2 — ledger recompute (suffix-aware; snapshot labeled by record count, not wall clock)")
    print(f"ledger: {ledger_path}")
    print(f"total records: {len(recs)}   last record ts: {max(r['ts'] for r in recs)}")
    print(f"source split: {dict(sorted(Counter(r['source'] for r in recs).items()))}")
    print(f"sidechain=true records: {sum(1 for r in recs if r.get('sidechain'))}")
    namespaced = Counter(r["skill"] for r in recs if ":" in r["skill"])
    print(f"namespaced keys (why exact-name matching is prefix-blind): {dict(sorted(namespaced.items()))}")
    print()

    by_base: dict[str, list[dict]] = defaultdict(list)
    for r in recs:
        by_base[base_name(r["skill"])].append(r)

    print("per-skill (suffix-aware): records / sessions / model-initiated  [exact-name records when different]")
    for s in LEDGER_SKILLS:
        rs = by_base.get(s, [])
        exact = sum(1 for r in recs if r["skill"] == s)
        drift = "" if exact == len(rs) else f"   [exact-name: {exact} — PREFIX-BLIND UNDERCOUNT]"
        print(f"    {s}: {len(rs)} / {len({r['session'] for r in rs})} / {sum(1 for r in rs if r['source'] == 'model')}{drift}")
    print()

    squad_sessions = {r["session"] for r in by_base.get("skill-squad", [])}
    print(f"skill-squad sessions: {len(squad_sessions)}")
    overlap_any: list[str] = []
    overlap_post: list[str] = []
    for sess in sorted(squad_sessions):
        sess_recs = sorted((r for r in recs if r["session"] == sess), key=lambda r: r["ts"])
        squad_ts = min(r["ts"] for r in sess_recs if base_name(r["skill"]) == "skill-squad")
        hits = [r for r in sess_recs if base_name(r["skill"]) in ("scrutinize-skill", "behavior-smoke-test")]
        if hits:
            overlap_any.append(sess)
            post = [r for r in hits if r["ts"] > squad_ts]
            if post:
                overlap_post.append(sess)
                fired = sorted({f"{r['skill']} ({base_name(r['skill'])})" for r in post})
                print(f"    session {sess[:8]}: post-squad fires: {', '.join(fired)}")
    exact_overlap = {
        sess for sess in squad_sessions
        if any(r["session"] == sess and r["skill"] in ("scrutinize-skill", "behavior-smoke-test") for r in recs)
    }
    print(f"overlap with scrutinize-skill|behavior-smoke-test — suffix-aware any-order: {len(overlap_any)}, "
          f"post-squad: {len(overlap_post)}, exact-name (the prefix-blind bug): {len(exact_overlap)}")
    full_chain = [s for s in sorted(squad_sessions)
                  if FULL_CHAIN_7 <= {base_name(r["skill"]) for r in recs if r["session"] == s}]
    print(f"full chain-7 sessions (squad+scrutinize+smoke+benchmark): {len(full_chain)}")
    mr = {r["session"] for r in by_base.get("making-recommendations", [])}
    ideate = {r["session"] for r in by_base.get("ideate", [])}
    print(f"shared making-recommendations+ideate sessions: {len(mr & ideate)}")


if __name__ == "__main__":
    main()
