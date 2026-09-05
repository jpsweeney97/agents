---
type: plan
date: 2026-09-04
scope: first prune tranche over the never-fired skills named in docs/reviews/2026-09-04-skill-usage-ledger-re-read.md
status: PROPOSED — nothing moves until JP approves the list
reviewed_commit: 8c71da7
---

# Skill prune, tranche 1: proposal

JP took the prune branch of the 2026-08-01 ledger re-read on 2026-09-04. The commitment (`docs/reviews/2026-07-02-framework-challenge.md:62`) says: tranche-based pruning of never-fired skills, oldest and least-storied first, archive not delete. This is the first tranche, proposed for approval. No file has moved.

## Proposed tranche: nine skills

All nine live in `skills/`, all were born between 2026-06-05 and 2026-06-28, and none has a row on either runtime in its whole life (`docs/reviews/2026-09-04-skill-usage-ledger-re-read.md`, "still zero"). Every one is model-invocable except `zoom-out`, which is explicit-only, so its silence measures JP's recall rather than routing.

| # | skill | born | size | story (what history it carries) | own lifecycle note |
|---|---|---|---|---|---|
| 1 | `zoom-out` | 06-05 | 30 lines, 2 files | explicit-only; JP never typed `/zoom-out` or `$zoom-out` in three months; 7 commits, last a June reflow | none |
| 2 | `postmortem` | 06-25 | 74 lines | 3 commits, all June/July sweeps; no ledger mention | none |
| 3 | `runbook-authoring` | 06-26 | 63 lines | 3 commits; the 2026-09-01 mining pass gave `to-questionnaire` the same artifact lifecycle (`docs/agents/contract-decisions.md:141`), so that pattern survives elsewhere | first-to-prune |
| 4 | `deploy-plan` | 06-27 | 48 lines | 4 commits; received one Stage B fold clause on 2026-09-01 (`3da8e35`, the feature-flag lifecycle line at `deploy-plan:16`) | first-to-prune |
| 5 | `incident-response` | 06-27 | 102 lines | 3 commits; no ledger mention | first-to-prune |
| 6 | `migration-safety` | 06-27 | 59 lines | 3 commits; named once in the ledger as a route target inside `to-issues` | first-to-prune |
| 7 | `observability-instrumentation` | 06-27 | 52 lines | 5 commits; received Stage B fold clauses on 2026-09-01 (`3da8e35`, alert hygiene and percentiles) | first-to-prune |
| 8 | `dependency-upgrade` | 06-28 | 54 lines | 3 commits; `work-router` carries a routing section for it | first-to-prune on observed mis-fire |
| 9 | `regex-craft` | 06-28 | 55 lines, 2 files | 4 commits; no ledger mention | first-to-prune on observed mis-fire |

Why these nine and not others from the 21:

- Six of them (rows 2 to 7) are the whole operations cluster. They route to each other densely, so archiving them together removes the cross-routes in one move instead of leaving half a cluster with dangling hand-offs. The seventh cluster member named in the 2026-09-02 bundle plan, `outcome-check`, has fired and is outside any tranche.
- Rows 8 and 9 are the two remaining `skills/` members of the same age band whose inbound routes all live in bare skills, so no plugin release is needed to unroute them.
- Row 1 is the oldest skill in the population and the only explicit-only one.
- Their lifecycle notes (`docs/agents/skill-lifecycle-notes.md`) say "first-to-prune" for seven of the nine. Those notes also say local silence is not evidence against a portable skill. The evidence here is not local: it is two months of zero fires across every repository on both runtimes, which `AGENTS.md` names as legitimate prune input.

The two with the freshest investment are `deploy-plan` and `observability-instrumentation`: third-party fold clauses landed in them three days before this proposal. The folds move to the archive with the skill; the ledger entry that records them (`docs/agents/contract-decisions.md:143`) stays true and is not edited. If JP wants the tranche to be strictly least-storied, pull those two and they join tranche 2.

## Held for a later tranche: twelve skills

| skill | born | why held |
|---|---|---|
| `baseline` | 06-04 | most-routed of the 21: nine skills name it as the owner of authority resolution, four of them across three plugins (`closeout-check`, `spec-drift-reconcile`, `acceptance-map`, `making-recommendations`); a ledger park entry cites it; unrouting it is three plugin releases |
| `prototype` | 06-05 | a restored mattpocock fork (ledger 2026-07-05); JP's C1 decision on 2026-09-01 declined a change to it on a stated position; routes from three `decide` skills |
| `to-prd` | 06-05 | plugin member (`plan-cycle`), a node in the forward chain the plugin documents; retiring it is a `plan-cycle` major |
| `search-handoffs` | 06-09 | plugin member (`handoff`); named in the SessionStart hook script `scripts/check-handoff-paths.sh`; retiring it is a `handoff` major plus a hook-script edit |
| `friction-to-guards` | 06-12 | charter-ledgered admission (2026-06-12, the route-absence correction); `soundcheck` routes durable rule authoring to it |
| `contract-change-propagation` | 06-19 | ten inbound routes including two in `plan-cycle` |
| `keep-green` | 06-25 | two ledger mentions; routed to from four `git-cycle` and `plan-cycle` skills |
| `research-capture` | 06-25 | named by `shelf-life` as a composing partner and by `decision-record` (`decide`) |
| `steelman` | 06-27 | exported to claude.ai (`exports/steelman/`); routed from `decide` and `review-family`; its note predicted frequent fire |
| `working-slice-review` | 06-27 | routed from `scope-cut` (`decide`) and `recheck-investment` |
| `scope-cut` | 06-30 | plugin member (`decide`); its note predicted frequent fire |
| `reflect` | 07-01 | youngest of the 21; JP-personal; JP had it restated in literal words on 2026-09-04 (`791c285`) |

`steelman` and `scope-cut` deserve one sentence: their lifecycle notes said "fires often and locally, so this is not first-to-prune". Neither fired once. That prediction failed, which is input for tranche 2, not a reason to skip the age-and-story order now.

## What archiving forecloses

The 2026-09-02 bundle plan (`docs/plans/2026-09-02-plugin-bundle-candidates.md`, section 5) listed `ops-cycle` as a tier-2 bundle "to build when you want them as a unit", with exactly this cluster as members. Archiving the cluster turns that option into "restore first, then bundle". The plan is not edited; this note is the record.

## Route hygiene: every live line that names one of the nine

The charter's Retirement section requires updating every contract that routes to a removed surface. Inbound mentions were swept across `skills/`, `skills-claude/`, `plugins/`, `exports/`, `scripts/`, and `AGENTS.md` at `8c71da7`.

Bare-skill lines, edited in the same commit as the move (14 lines in 13 files):

| file:line | names | edit |
|---|---|---|
| `skills/premortem/SKILL.md:18` | `deploy-plan` | drop the closing contrast clause (a mention, not a route) |
| `skills/premortem/SKILL.md:33` | `postmortem` | drop the boundary line |
| `skills/diagnose/SKILL.md:161` | `postmortem` | drop the hand-off sentence, keep the Phase 6 note |
| `skills/reflect/SKILL.md:51` | `postmortem` | drop it from the not-list |
| `skills/outcome-check/SKILL.md:3` | `deploy-plan` | drop the last not-for clause of the description |
| `skills/perf-optimize/SKILL.md:13` | `deploy-plan`, `observability-instrumentation` | drop both clauses; the line already says to name a gap |
| `skills/agent-facing-design/SKILL.md:74` | `deploy-plan` | drop the example (a mention, not a route) |
| `skills/contract-change-propagation/SKILL.md:54` | `migration-safety` | drop the hand-off bullet |
| `skills/characterization-tests/SKILL.md:28` | `dependency-upgrade` | drop it from the list |
| `skills/document-to-markdown/SKILL.md:29` | `dependency-upgrade` | drop the "where available" sentence |
| `skills/injection-safe-inputs/SKILL.md:55` | `regex-craft` | drop the hand-off bullet |
| `skills/explain-codebase/SKILL.md:38` | `zoom-out` | drop it from the hand-off list |
| `skills-claude/setup-matt-pocock-skills/SKILL.md:3` | `zoom-out` | drop "or zoom-out" from the description |
| `skills/work-router/SKILL.md:79-82` | `dependency-upgrade` | delete the routing section |

Plugin lines (two, both in `decide`):

| file:line | names | phrasing |
|---|---|---|
| `plugins/decide/skills/scope-cut/SKILL.md:24` | `deploy-plan` | unconditional: "a downstream `making-recommendations` / `deploy-plan` call" |
| `plugins/decide/skills/decision-record/SKILL.md:68` | `postmortem` | unconditional boundary line |

These need a `decide` patch release (2.4.1: doc-only edit, so a patch under the version rule) or a hold until the next natural `decide` bump. The one `plan-cycle` mention (`to-issues:43`, `migration-safety`) is already availability-conditional ("Where available ... When a needed companion is unavailable, publish ... as one `ready-for-human` issue"), so it needs no edit.

Non-skill surfaces:

- `docs/agents/skill-lifecycle-notes.md`: seven of the nine have sections. Each gets one appended line naming the archive date and this record. Sections are not deleted.
- `scripts/skill-usage-miner.py` already classifies rows for `skills-archive/` names as "archived"; no edit.
- `~/.claude/skills/<name>`: nine symlinks go dangling after the move and are removed with `trash`; the sync script never deletes.
- `~/.agents-worktrees/<name>`: nine parked satellites become `RETIRED-PENDING` in the fleet census and are removed one at a time with `scripts/satellite-fleet.py retire <name>`, which refuses unless the skill is absent from the live roots and the satellite is parked with no lease.

## Execution sequence, once approved

1. `git status --short --branch` clean on `main`. Pick one surviving satellite that takes a route edit (`work-router`) and run the `worktree-task-cycle` lifecycle: inspect, lease-acquire, activate. All nine moves and every edit above happen on its task branch, because skill surfaces are guarded outside the satellite lifecycle.
2. `git mv skills/<name> skills-archive/<name>` for each of the nine. Add one dated section to `skills-archive/README.md` listing the nine with the reason pointer (this file and the re-read record). No per-skill `ARCHIVED.md`: the README's generic restore instruction applies to all nine, unlike `deliberate-v1`.
3. Apply the fourteen bare-skill edits and the seven lifecycle-note lines. If the `decide` patch is approved, apply the two plugin edits, add a 2.4.1 CHANGELOG section, and bump `plugin.json` in the same commit.
4. Validate: `quick_validate.py` on every edited skill; `git diff --check`; a whole-word grep proving no live surface under `skills/`, `skills-claude/`, `plugins/`, `exports/`, or `scripts/` names any of the nine; `scripts/check-library-integrity.sh --check`.
5. Land fast-forward onto `main` through the lifecycle; park the satellite.
6. In the primary: `trash ~/.claude/skills/<name>` for the nine, then `scripts/claude-skills-sync.sh --check`. `scripts/satellite-fleet.py check`, then `retire <name>` for each of the nine, then `check` again to exit 0.
7. Proof of removal: one fresh headless listing per runtime (`claude -p` with the skill list read; `codex exec` with `< /dev/null`) showing none of the nine. If the `decide` patch landed, `scripts/codex-plugins-sync.sh --publish decide` is authorized by the landed bump; mirror sync and push stay on JP's word.
8. Report: what moved, what was edited, the listing proof, and the twelve held skills as the tranche 2 population.

## What this proposal does not claim

- Fire counts are load markers, not proven value. The nine could carry cognitive-offload value that no ledger sees; the commitment's remedy is defined over never-fired skills and this is that population.
- No skill body was read for quality in this pass. The ordering is age and story, as the commitment specified.
- Archiving is reversible by `git mv` back plus `--link`; the satellite comes back through `create-missing`.
