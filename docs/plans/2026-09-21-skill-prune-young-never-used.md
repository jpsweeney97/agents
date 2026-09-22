---
type: plan
date: 2026-09-21
scope: prune deliberation over the five never-used skills that carry no inbound SKILL.md route, drawn from docs/reviews/2026-09-21-never-used-skill-census.md
status: EXECUTED 2026-09-21 — JP approved archiving `skill-squad`, and overrode the proposal to archive `decision-flip` and `incentive-map` as well; `plan-queue` and `perf-optimize` kept
reviewed_commit: 4fc80ed
---

# Prune deliberation: the young never-used skills

The 2026-09-21 census found 24 live skills that have never actually been used. Five of them carry no inbound route from any other `SKILL.md`: `decision-flip`, `incentive-map`, `perf-optimize`, `plan-queue`, `skill-squad`. JP asked for the prune deliberation on those five. This document opens it and decides nothing.

These five are not the tranche-1 population. That program works the oldest and least-storied skills first, and took `postmortem`, `incident-response`, `migration-safety`, and `dependency-upgrade` on 2026-09-05 at `1c84ea3`, holding `deploy-plan` and `observability-instrumentation` for tranche 2. **These five are the roster's youngest, born between 2026-06-24 and 2026-09-01.** An argument to cut them is an argument against a skill that has existed for three weeks to three months, and is weaker for it.

## What the charter requires of each

Four of the five are build-and-prune: "trash it the moment it stops earning its place — no evidence ceremony, and archiving to `skills-archive/` is optional" (`docs/agents/charter.md:64`). No ledger entry is owed for them.

`plan-queue` is not. Its lifecycle note puts it in the gated class because its burn verb ends in a local fast-forward merge, so it took the Admission test and carries a `contract-decisions.md` entry (`docs/agents/skill-lifecycle-notes.md:127`, ledger entry 2026-07-26). Retiring it takes the same evidence discipline as admitting it, names observed-work evidence rather than route-absence, and gets its own ledger entry.

## The correction this deliberation starts with

The five were introduced to JP as "clean-cut": zero fires and zero inbound routes. That was measured over `SKILL.md` files only, and it is wrong for one of them.

`plan-queue` is a `plan-cycle` plugin member. Removing it edits `README.md`, `PRIVACY.md`, `.claude-plugin/plugin.json` (the `longDescription`), and `CHANGELOG.md`, then takes a version bump, a Codex republish, and a mirror sync. **It is the most expensive of the five to remove, not the cleanest.** The other four have no inbound reference on any live surface — skill bodies, metadata, scripts, exports, or `AGENTS.md`.

## Per-skill cases

### `skill-squad` — recommend archiving

| | |
|---|---|
| Source | `skills-claude/` (Claude-only), 70 lines, 5 commits |
| Born | 2026-06-24 |
| Fire record | 13 real fires, all inside `.agents` between 06-24 and 07-01; nothing in 81 days |
| Inbound routes | 0, on every live surface |
| Class | build-and-prune; no ledger entry owed |

**The case to cut.** This is the only one of the five with a real fire history that started and then stopped, which is different from never starting. It ran during its own build week, designed at least one skill on the record (`dependency-upgrade`, credited in `ae5f916` as a "skill-squad same-shape BEAT"), and that skill was itself archived in tranche 1. Nothing routes to it, and the documented Claude-side lane for skill work does not mention it: `AGENTS.md` sends new bundles to hand-authoring against `agent-facing-design` and `skill-ux-design`, and says there is no Claude-side constructor skill by design. It is also expensive by construction — a multi-agent discovery run — against a standing preference for restraint in workflow size.

**The case to keep.** Its value is discovery, which by definition does not show up as routine fire; a skill you reach for twice a year can still earn its slot the two times it runs. The build-and-prune class cuts both ways: it is as cheap to restore from `skills-archive/` as to cut.

**Why cut wins.** Eleven weeks of silence across every repository, zero inbound routes, an undocumented lane, and a cheap reversal. This is the case the charter's "trash it the moment it stops earning its place" was written for.

### `plan-queue` — recommend keeping, with a dated reopen trigger

| | |
|---|---|
| Source | `plugins/plan-cycle/`, 74 lines |
| Born | 2026-07-26 |
| Fire record | 0 real fires; **19 roster-scan reads**, every one a pass-over |
| Inbound routes | 0 in skill bodies; 4 plugin packaging surfaces name it |
| Class | gated — Admission-tested, ledger entry 2026-07-26 |

**The case to cut is the strongest in the set, on evidence.** The demand that justified it is dated and is documented in its own admission entry: a ~200-word generation prompt retyped verbatim on 2026-07-09 and 2026-07-10, with a third session spent hunting for the old copy. That demand is visible in this repository's history as three committed queues — `b53c0ee` (07-09), `e4b6754` (07-10), `954f97e` (07-10), five `PLAN-*.md` files each. **The skill was built on 2026-07-26, and not one queue has been generated in the 57 days since.** Meanwhile Codex read its `SKILL.md` 19 times while choosing a route and picked something else every time. That is not silence; it is repeated rejection.

**The case to keep.** The burst ended two weeks *before* the skill existed, so the skill has never seen the conditions it was built for; its first real test has not happened. Its own lifecycle note names a different fold signal than the one observed — "if real queues are reliably one or two plans, the queue machinery is ceremony" — and no queue at all does not meet it. Cutting is expensive in a way the other four are not: a gated retirement with its own evidence case and ledger entry, four packaging surfaces, a version bump, a Codex republish, and a mirror sync. Rebuilding is expensive too — the admission carries JP-settled design decisions, an attended fence, and three forward tests against git fixtures.

**Why keep wins, for now.** The cost is asymmetric. Holding it costs 74 lines in a plugin that already ships; removing it costs a gated retirement and a release cycle, and rebuilding costs more than that. **Proposed reopen trigger: on 2026-11-01, if no `PLAN-*.md` queue has been generated anywhere and the pass-over count has grown, retire it as a gated decision.** That converts an expensive irreversible-ish call into a cheap dated one.

### `perf-optimize` — recommend keeping on age alone

| | |
|---|---|
| Source | `skills/`, 53 lines plus `references/browser-performance.md` |
| Born | 2026-09-01 |
| Fire record | 0 real; 2 synthetic probe rows |
| Inbound routes | 0 inbound; it routes *outward* to six skills |
| Class | build-and-prune |

**Twenty days old.** It was an admitted build of the third mining program (opened 2026-08-31), and no prune argument survives an age that short: the census cannot distinguish "nobody wants this" from "no slow endpoint came up in three weeks". Two of its outward routes, `deploy-plan` and `observability-instrumentation`, are themselves held for tranche 2, so a decision here should wait for that tranche rather than lead it. Revisit no earlier than 2026-11-01.

### `decision-flip` and `incentive-map` — JP's call, genuinely borderline

| | `decision-flip` | `incentive-map` |
|---|---|---|
| Source | `skills/`, 23 lines | `skills/`, 21 lines |
| Born | 2026-08-06 | 2026-08-06 |
| Fire record | **no row of any kind** | 1 synthetic probe row |
| Inbound routes | 0 | 0 |
| Class | build-and-prune | build-and-prune |

Both arrived in one commit (`fcddae0`, "the judgment set") with `decision-owner-map`, `fence-archaeology`, `outside-view`, and `soundcheck`. Of that six, `outside-view`, `fence-archaeology`, and `soundcheck` are now in real use; these two and `decision-owner-map` are not.

**What makes them different from the other three: they were never even considered.** `plan-queue` was read and passed over 19 times; `decision-flip` carries no ledger row of any kind, and its only mentions outside this repository are two `playpen` sessions that printed its path in a directory listing. That is the absence of the triggering situation, not a router verdict against the skill. `decision-flip` wants an estimate-driven conclusion about to circulate — a business case, a forecast, a capacity plan. `incentive-map` wants a structure other people will live under — a metric, a quota, a review gate, a policy.

**The deciding question is not in the ledger: is that kind of work coming?** If athenahealth or career work brings a forecast to defend or a policy to ship, both skills are 20-line procedures that do exactly that job and nothing routes around them. If JP's work stays agent tooling, neither will ever fire, and they are inventory.

The cost of holding them is two files totalling 44 lines and a slightly longer roster scan. Neither is worth a tranche on its own.

## Proposed disposition

| skill | proposal | JP's decision, 2026-09-21 | reversibility |
|---|---|---|---|
| `skill-squad` | archive to `skills-archive/` | **archived** | restore from archive; no ledger entry |
| `plan-queue` | keep; reopen 2026-11-01 on the trigger above | kept | — |
| `perf-optimize` | keep; revisit with tranche 2, no earlier than 2026-11-01 | kept | — |
| `decision-flip` | JP decides: hold or archive | **archived** | restore from archive |
| `incentive-map` | JP decides: hold or archive | **archived** | restore from archive |

JP archived all three archivable candidates, which on `decision-flip` and `incentive-map` answers the open question this document could not: the estimate-heavy and structure-design work those two serve is not coming. None of the three needed route hygiene — no live surface named any of them, which is why they were the unrouted set in the first place.

**Executed 2026-09-21.** The three moved unchanged to `skills-archive/` through the satellite lifecycle. The landing sequence also removes their now-dangling `~/.claude/skills` symlinks with `trash`, and leaves their three satellites standing for a separate retirement pass through `scripts/satellite-fleet.py`, which is the owning repo's decision rather than this plan's. No ledger entry is owed: all three are build-and-prune class.

## Evidence boundary

- Rests on `docs/reviews/2026-09-21-never-used-skill-census.md` and inherits every limit in its own boundary section, including that a zero means no recorded invocation rather than proven never run.
- The inbound-route counts here were taken across skill bodies, metadata, scripts, exports, and `AGENTS.md` — wider than the census's `SKILL.md`-only count, which is what caught the `plan-queue` packaging surfaces.
- Not inspected: whether any repository outside this machine uses these skills, and the `references/` tree of `perf-optimize` beyond its existence.
