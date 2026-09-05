---
type: plan
date: 2026-09-04
revised: 2026-09-05
scope: first prune tranche over the never-fired skills named in docs/reviews/2026-09-04-skill-usage-ledger-re-read.md, re-proposed from that record's 2026-09-05 erratum
status: PROPOSED — nothing moves until JP approves the list
reviewed_commit: 5bcec49
---

# Skill prune, tranche 1: proposal (revised 2026-09-05)

JP took the prune branch of the 2026-08-01 ledger re-read on 2026-09-04. The commitment (`docs/reviews/2026-07-02-framework-challenge.md:62`) says: tranche-based pruning of never-fired skills, oldest and least-storied first, archive not delete. This is the first tranche, proposed for approval. No file has moved.

## Revision note

The first version of this proposal (`0c7ab2d`) named nine skills from a population of 21 "never fired anywhere". JP then said he had used `regex-craft` in Codex, and he had. The ledger's miner could not see a Codex skill the model chose itself (it loads the skill by reading its file, writing no `<skill>` block) and had never scanned `~/.codex/archived_sessions`. Both were repaired on 2026-09-05 (`5bcec49`), the ledger was refreshed, and the record gained an erratum with the corrected numbers (`docs/reviews/2026-09-04-skill-usage-ledger-re-read.md`, "Erratum", with `2026-09-05-skill-usage-ledger-re-read-erratum.py` and `.txt` beside it). The population shrank from 21 to 10: skills with no typed fire anywhere and no chosen read outside this repository, ever. Three of the nine first proposed left it on the strength of chosen reads: `regex-craft` (four Codex sessions), `runbook-authoring` (three markdown-reader sessions in July), and `zoom-out` (one cross-model session in June). This revision re-proposes from the 10.

## Proposed tranche: six skills

All six live in `skills/`, were born between 2026-06-25 and 2026-06-28, have no typed fire on either runtime, and were never read by Codex outside this repository except inside a roster scan. Every read of them on record happened inside this repository or its review copies, where reads are edits, reviews, and censuses.

| # | skill | born | size | reads on record | story (what history it carries) | own lifecycle note |
|---|---|---|---|---|---|---|
| 1 | `postmortem` | 06-25 | 74 lines | 6 in this repo, 1 scan outside | 3 commits, all June/July sweeps; no ledger mention | none |
| 2 | `deploy-plan` | 06-27 | 48 lines | 6 in this repo | 4 commits; received one Stage B fold clause on 2026-09-01 (`3da8e35`, the feature-flag lifecycle line at `deploy-plan:16`) | first-to-prune |
| 3 | `incident-response` | 06-27 | 102 lines | 2 in this repo | 3 commits; no ledger mention | first-to-prune |
| 4 | `migration-safety` | 06-27 | 59 lines | 6 in this repo | 3 commits; named once in the ledger as a route target inside `to-issues` | first-to-prune |
| 5 | `observability-instrumentation` | 06-27 | 52 lines | 7 in this repo | 5 commits; received Stage B fold clauses on 2026-09-01 (`3da8e35`, alert hygiene and percentiles) | first-to-prune |
| 6 | `dependency-upgrade` | 06-28 | 54 lines | 4 in this repo | 3 commits; `work-router` carries a routing section for it | first-to-prune on observed mis-fire |

Why these six and not the other four of the 10:

- Rows 1 to 5 are the operations cluster minus `runbook-authoring`, which stays because Codex chose it three times in markdown-reader. The five route to each other densely, so archiving them together removes the cross-routes in one move.
- Row 6 is the one remaining `skills/` member of the population whose inbound routes all live in bare skills.
- Their lifecycle notes (`docs/agents/skill-lifecycle-notes.md`) say "first-to-prune" for five of the six. Those notes also say local silence is not evidence against a portable skill. The evidence here is not local: it is every Codex and Claude session on this machine, both session stores, with model-invoked loads now visible.

The two with the freshest investment are `deploy-plan` and `observability-instrumentation`: third-party fold clauses landed in them four days before this revision. The folds move to the archive with the skill; the ledger entry that records them (`docs/agents/contract-decisions.md:143`) stays true and is not edited. If JP wants the tranche to be strictly least-storied, pull those two and they join tranche 2.

## Held for a later tranche: four skills, still in the population

| skill | born | why held |
|---|---|---|
| `friction-to-guards` | 06-12 | Claude-only, so Codex could never have loaded it; charter-ledgered admission (2026-06-12, the route-absence correction); `soundcheck` routes durable rule authoring to it |
| `research-capture` | 06-25 | named in three descriptions (`shelf-life`, `reflect`, `decision-record`) and four bodies as the capture lane for persisted findings; two of those lines are in the `decide` plugin |
| `steelman` | 06-27 | exported to claude.ai (`exports/steelman/`); routed from `decide` and `review-family`; its note predicted frequent fire and it was read 14 times in this repo |
| `scope-cut` | 06-30 | plugin member (`decide`); its note predicted frequent fire; 18 in-repo reads, mostly the plugin's own work |

## Out of the population now

These were in the first version's 21 and left it under the repaired instrument. None is a tranche candidate under either branch of the commitment.

- Chosen by Codex outside this repository, before or after 2026-07-02: `baseline`, `contract-change-propagation`, `keep-green`, `prototype`, `reflect`, `regex-craft`, `runbook-authoring`, `search-handoffs`, `to-prd`, `working-slice-review`, `zoom-out`.
- `outcome-check` was never chosen outside this repository but carries one in-repo typed fire (2026-07-18), so the record counted it as fired.

`steelman` and `scope-cut` still deserve one sentence: their lifecycle notes said "fires often and locally, so this is not first-to-prune". Neither was ever chosen. That failed prediction is input for tranche 2, not a reason to skip the age-and-story order now.

## What archiving forecloses

The 2026-09-02 bundle plan (`docs/plans/2026-09-02-plugin-bundle-candidates.md`, section 5) listed `ops-cycle` as a tier-2 bundle "to build when you want them as a unit", with this cluster plus `runbook-authoring` and `outcome-check` as members. Archiving five of its seven members turns that option into "restore first, then bundle". The plan is not edited; this note is the record.

## Route hygiene: every live line that names one of the six

The charter's Retirement section requires updating every contract that routes to a removed surface. Inbound mentions were swept across `skills/`, `skills-claude/`, `plugins/`, `exports/`, `scripts/`, and `AGENTS.md` at `8c71da7`; no live surface changed between then and `5bcec49`.

Bare-skill lines, edited in the same commit as the move (15 lines in 11 files):

| file:line | names | edit |
|---|---|---|
| `skills/premortem/SKILL.md:3` | `postmortem` | drop the not-for clause from the description |
| `skills/premortem/SKILL.md:18` | `deploy-plan` | drop the closing contrast clause (a mention, not a route) |
| `skills/premortem/SKILL.md:33` | `postmortem` | drop the boundary line |
| `skills/diagnose/SKILL.md:161` | `postmortem` | drop the hand-off sentence, keep the Phase 6 note |
| `skills/reflect/SKILL.md:3` | `postmortem` | drop it from the description's not-list |
| `skills/reflect/SKILL.md:51` | `postmortem` | drop it from the not-list |
| `skills/runbook-authoring/SKILL.md:3` | `postmortem` | drop it from the description |
| `skills/runbook-authoring/SKILL.md:54` | `postmortem` | drop the boundary line |
| `skills/outcome-check/SKILL.md:3` | `deploy-plan` | drop the last not-for clause of the description |
| `skills/perf-optimize/SKILL.md:13` | `deploy-plan`, `observability-instrumentation` | drop both clauses; the line already says to name a gap |
| `skills/agent-facing-design/SKILL.md:74` | `deploy-plan` | drop the example (a mention, not a route) |
| `skills/contract-change-propagation/SKILL.md:54` | `migration-safety` | drop the hand-off bullet |
| `skills/characterization-tests/SKILL.md:28` | `dependency-upgrade` | drop it from the list |
| `skills/document-to-markdown/SKILL.md:29` | `dependency-upgrade` | drop the "where available" sentence |
| `skills/work-router/SKILL.md:79-82` | `dependency-upgrade` | delete the routing section |

Plugin lines (two, both in `decide`):

| file:line | names | phrasing |
|---|---|---|
| `plugins/decide/skills/scope-cut/SKILL.md:24` | `deploy-plan` | unconditional: "a downstream `making-recommendations` / `deploy-plan` call" |
| `plugins/decide/skills/decision-record/SKILL.md:68` | `postmortem` | unconditional boundary line |

These need a `decide` patch release (2.4.1: doc-only edit, so a patch under the version rule) or a hold until the next natural `decide` bump. The one `plan-cycle` mention (`to-issues:43`, `migration-safety`) is already availability-conditional ("Where available ... When a needed companion is unavailable, publish ... as one `ready-for-human` issue"), so it needs no edit.

Non-skill surfaces:

- `docs/agents/skill-lifecycle-notes.md`: five of the six have sections. Each gets one appended line naming the archive date and this record. Sections are not deleted.
- `scripts/skill-usage-miner.py` already classifies rows for `skills-archive/` names as "archived"; no edit.
- `~/.claude/skills/<name>`: six symlinks go dangling after the move and are removed with `trash`; the sync script never deletes.
- `~/.agents-worktrees/<name>`: six parked satellites become `RETIRED-PENDING` in the fleet census and are removed one at a time with `scripts/satellite-fleet.py retire <name>`, which refuses unless the skill is absent from the live roots and the satellite is parked with no lease.

## Execution sequence, once approved

1. `git status --short --branch` clean on `main`. Pick one surviving satellite that takes a route edit (`work-router`) and run the `worktree-task-cycle` lifecycle: inspect, lease-acquire, activate. All six moves and every edit above happen on its task branch, because skill surfaces are guarded outside the satellite lifecycle.
2. `git mv skills/<name> skills-archive/<name>` for each of the six. Add one dated section to `skills-archive/README.md` listing the six with the reason pointer (this file, the re-read record, and its erratum). No per-skill `ARCHIVED.md`: the README's generic restore instruction applies to all six, unlike `deliberate-v1`.
3. Apply the fifteen bare-skill edits and the five lifecycle-note lines. If the `decide` patch is approved, apply the two plugin edits, add a 2.4.1 CHANGELOG section, and bump `plugin.json` in the same commit.
4. Validate: `quick_validate.py` on every edited skill; `git diff --check`; a whole-word grep proving no live surface under `skills/`, `skills-claude/`, `plugins/`, `exports/`, or `scripts/` names any of the six; `scripts/check-library-integrity.sh --check`.
5. Land fast-forward onto `main` through the lifecycle; park the satellite.
6. In the primary: `trash ~/.claude/skills/<name>` for the six, then `scripts/claude-skills-sync.sh --check`. `scripts/satellite-fleet.py check`, then `retire <name>` for each of the six, then `check` again to exit 0.
7. Proof of removal: one fresh headless listing per runtime (`claude -p` with the skill list read; `codex exec` with `< /dev/null`) showing none of the six. If the `decide` patch landed, `scripts/codex-plugins-sync.sh --publish decide` is authorized by the landed bump; mirror sync and push stay on JP's word.
8. Report: what moved, what was edited, the listing proof, and the four held skills as the tranche 2 population.

## What this proposal does not claim

- Rows are load markers, not proven value, and a read is a weaker marker than a typed token. The six could carry cognitive-offload value that no ledger sees; the commitment's remedy is defined over never-fired skills and this is that population under the best instrument available.
- In-repo reads were classed as edits and reviews. If one of the six was used for real work on this repository by Codex, that use is invisible here; release cuts are the known case of real in-repo work, and none of the six is a release skill.
- No skill body was read for quality in this pass. The ordering is age and story, as the commitment specified.
- Archiving is reversible by `git mv` back plus `--link`; the satellite comes back through `create-missing`.
