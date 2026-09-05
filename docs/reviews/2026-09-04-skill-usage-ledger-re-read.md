---
type: review
date: 2026-09-04
scope: the skill-usage ledger (~/.claude/logs/skill-usage-ledger.jsonl) read against the two branches pre-registered in the 2026-07-02 framework challenge; the 76-skill roster of 2026-07-02 and the 124-skill roster of today
reviewed_commit: 8fcc585
method: ledger refreshed with scripts/skill-usage-miner.py, then read by the sibling script 2026-09-04-skill-usage-ledger-re-read.py (suffix-aware name matching, the miner's own collapse and alias code); raw output in the sibling .txt
posture: read-only; the branch call is left to JP; no skill was pruned, archived, or edited
---

# Skill-usage ledger re-read: the 2026-08-01 commitment, run 2026-09-04

The 2026-07-02 framework challenge committed to re-read the skill-usage ledger on or after 2026-08-01 (`docs/reviews/2026-07-02-framework-challenge.md:62`). Nothing ran on that date. This record is the read, made 35 days late, against the two branches exactly as they were written. It renders no prune decision: JP asked for the read and the record only.

## Outcome in short

- **The pre-registered set of 40 never-fired skills was reconstructed exactly**, by counting only what the 2026-07-02 instrument could see (Claude rows, suffix-aware, before the challenge commit).
- **24 of the 40 have still never fired on either runtime since 2026-07-02.** 21 of those have never fired anywhere in their life; the other 3 had Codex fires before 2026-07-02 that the first read could not see and none since.
- **16 of the 40 have fired since 2026-07-02.** 15 fired in repositories other than this one. 11 fired after 2026-08-01, past the July window in which methodology treatments were known to summon fires. 5 fired only in July.
- **Both branch conditions have support on different parts of the set**, and the record set no threshold for "broadly". That call is JP's and is not made here.

## The commitment as written

From `docs/reviews/2026-07-02-framework-challenge.md:62`: "**Commitment: re-read the ledger on or after 2026-08-01.** If the zero-fire set is still broadly zero after a month of live hook coverage, tranche-based pruning of never-fired skills begins (oldest and least-storied first, archive not delete); if firing has spread, the tail earns partial vindication and pruning stays light. Either way the data is read as recorded — no post-hoc reframing of the branches."

Three later obligations attach to the same read:

- Matching must be suffix-aware, so that a plugin-qualified row such as `review-family:scrutinize-skill` counts as a fire of `scrutinize-skill`. An exact-name count had undercounted for exactly this reason (`docs/plans/2026-07-11-skill-use-contract-design.md:29` and `:152`).
- The read must carry the miner's blindness footnote and must treat fire surges that followed a methodology treatment as partly caused by the treatment (`.agents/handoffs/2026-07-19_15-36-11_methodology-critique-self-treatment-closed-r1-r5-landed-pushed.md:61`; the footnote lives in `scripts/skill-usage-miner.py`, `FOOTNOTE`).
- The parked Skill Use contract names this read as one of its reopen triggers (`docs/agents/contract-decisions.md:87`), and the sealed skill value test was scheduled to pair with it (`docs/plans/2026-07-10-skill-value-test-preregistration.md:14`).

## Method

**Refresh.** `scripts/skill-usage-miner.py` was run first. It mined 5,489 transcripts and added 197 fires, bringing the ledger to 7,150 raw rows, which the miner's collapse reduces to 7,050 fires (8 fork replays and 92 rapid re-invokes removed). The live Claude hook had written rows through this session; Codex rows arrive only by mining, and the launchd job's last run before this one was 2026-09-01, so today's refresh closed that gap.

**What changed in the instrument since the first read.** The first read saw Claude transcripts only. Codex rollout mining was added 2026-07-03 and now reaches back to 2026-01-07, while Claude rows begin 2026-05-19 because of transcript retention. Alias merging and roster classification were added 2026-07-09, and the collapse plus the blindness footnote on 2026-07-19. The instrument today is stronger than the one the branches were written against, so the pre-registered set had to be reconstructed under the first instrument's view.

**Reconstructing the pre-registered set.** T0 is the challenge commit, `756501f`, 2026-07-02T04:47:27Z. Counting Claude rows before T0 with suffix-aware matching gives 36 fired and 40 never, the recorded figures exactly. Two cross-checks: exact-token matching gives 30 and 46, wrongly leaving out `load-handoff`, `save-handoff`, `throughline`, `pr-description`, `review-reviewer`, and `scrutinize-skill`, which is the 2026-07-11 hazard reproduced; and adding the Codex rows gives 45 and 31, because nine of the 40 had fired on Codex before T0 where the first read could not see them (`gh-pr-review-loop` 90 fires, `grill-me` 56, `system-design-review` 19, `gh-address-comments` 7, `implementation-review` 5, `setup-matt-pocock-skills` 2, `markdown-synthesis` 2, `acceptance-map` 1, `email-writing` 1). The read below uses the 40 as pre-registered and marks those nine.

**Suffix-aware matching.** A skill's name is the last colon-separated segment of the row's token after the miner's aliases are applied. 23 roster names had plugin-qualified tokens folded into them this way; the full list is at the end of the sibling `.txt`.

**Classifying fires since T0.** Each fire is split by runtime (Claude or Codex), source (typed by JP or invoked by the model), subagent or main session, and working directory: `tmp` for the session scratch directories where headless forward tests run, `agents` for this repository and its satellite worktrees, `other` for any other directory. A separate column counts fires on or after 2026-08-01, which separates the July window of methodology treatments (2026-07-03 to 2026-07-21) from what followed.

**Roster and birth dates.** The 76-name roster of 2026-07-02 was listed from the tree at `756501f`; today's 124 names come from the miner's own roster scan of `skills/`, `skills-claude/`, and `plugins/*/skills/`. A skill's birth date is the first commit touching any directory it has lived in.

## Results

### The pre-registered 40: what fired

| skill | fires since 07-02 | since 08-01 | runtime | where (tmp / this repo / other) | last fired | notes |
|---|---|---|---|---|---|---|
| implementation-review | 40 | 26 | Claude 31, Codex 9 | 2 / 3 / 35 | 2026-09-03 | 5 Codex fires before 07-02; other repos: cross-model, markdown-reader, athena-kb-local, claude-code-docs, playpen |
| decision-record | 26 | 15 | Claude 25, Codex 1 | 4 / 2 / 20 | 2026-09-02 | the 4 tmp fires are the Era 148 stage-2 smoke runs; other repos: cross-model, markdown-reader, athena-kb-local |
| release-cut | 13 | 11 | Claude 13 | 0 / 11 / 2 | 2026-09-04 | 12 model-invoked; the in-repo fires are the plugin release cuts |
| diagnose | 8 | 2 | Claude 5, Codex 3 | 0 / 2 / 6 | 2026-08-24 | other: markdown-reader, athena-kb-local, home directory |
| system-design-review | 5 | 2 | Claude 2, Codex 3 | 0 / 2 / 3 | 2026-08-26 | 19 Codex fires before 07-02 |
| tech-debt-scan | 4 | 1 | Claude 2, Codex 2 | 0 / 1 / 3 | 2026-09-01 | other: cross-model, markdown-reader, athena-kb-local |
| ideate | 9 | 1 | Claude 4, Codex 5 | 0 / 1 / 8 | 2026-08-07 | other: cross-model, markdown-reader, playpen |
| email-writing | 2 | 1 | Claude 1, Codex 1 | 0 / 0 / 2 | 2026-08-10 | 1 Codex fire before 07-02; other: athena-kb-local, career |
| setup-matt-pocock-skills | 1 | 1 | Claude 1 | 0 / 0 / 1 | 2026-08-22 | 2 Codex fires before 07-02; explicit-only on both runtimes |
| gh-pr-review-loop | 92 | 1 | Claude 1, Codex 91 | 0 / 0 / 92 | 2026-08-06 | 90 Codex fires before 07-02; explicit-only on both runtimes; other: cross-model, markdown-reader |
| improve-codebase-architecture | 33 | 1 | Claude 2, Codex 31 | 0 / 1 / 32 | 2026-08-19 | methodology treatment 2026-07-14; the footnote names this skill's surge as an observer effect |
| simplify-code | 37 | 0 | Codex 37 | 0 / 2 / 35 | 2026-07-15 | all fires in July; the 2026-07-18 treatment ran a harness-driven census, so these are mostly self-caused |
| migration-campaign | 2 | 0 | Claude 1, Codex 1 | 1 / 0 / 1 | 2026-07-27 | one scratch-fixture fire, one in markdown-reader |
| gh-address-comments | 2 | 0 | Codex 2 | 0 / 0 / 2 | 2026-07-09 | 7 Codex fires before 07-02; other: cross-model |
| doc-drift-audit | 1 | 0 | Codex 1 | 0 / 0 / 1 | 2026-07-06 | other: cross-model |
| outcome-check | 1 | 0 | Claude 1 | 0 / 1 / 0 | 2026-07-18 | one fire in this repo, inside the treatment window |

Totals for the 16: 276 fires since 07-02, 62 of them on or after 08-01. Three skills carry 52 of those 62 (`implementation-review`, `decision-record`, `release-cut`).

### The pre-registered 40: still zero

24 skills, with birth dates. None has a row on either runtime since 2026-07-02.

- Never fired anywhere, ever (21): `baseline` (2026-06-04), `prototype` (06-05), `to-prd` (06-05), `zoom-out` (06-05, explicit-only on both runtimes), `search-handoffs` (06-09), `friction-to-guards` (06-12), `contract-change-propagation` (06-19), `keep-green` (06-25), `postmortem` (06-25), `research-capture` (06-25), `runbook-authoring` (06-26), `deploy-plan` (06-27), `incident-response` (06-27), `migration-safety` (06-27), `observability-instrumentation` (06-27), `steelman` (06-27), `working-slice-review` (06-27), `dependency-upgrade` (06-28), `regex-craft` (06-28), `scope-cut` (06-30), `reflect` (07-01).
- Codex fires before 2026-07-02 only, none since (3): `grill-me` (born 05-28; 56 Codex fires, last 2026-06-09), `markdown-synthesis` (06-05; 2 fires, last 06-07), `acceptance-map` (06-08; 1 fire, 06-09).

The 21 were born between 2026-06-04 and 2026-07-01, so each has had 9 to 13 weeks of exposure, 64 days of it under live Claude hook coverage and all of it under Codex mining.

### Context outside the pre-registered set

These numbers are not branch input. They are recorded so the next read has them.

- Of the 36 skills that had fired by 2026-07-02, five have not fired since: `premortem`, `red-team`, and `spec-drift-reconcile` (one subagent fire each in late June), `skill-benchmark` (3 fires, last 06-15), `skill-squad` (13 fires, last 07-01).
- The roster grew from 76 to 124. `outcome-interviewer` left it on 2026-07-02 when `outcome-shaping` was born; 49 skills were added.
- 44 of today's 124 skills have never fired anywhere: the 21 above plus 23 born after 2026-07-02. Of those 23, 17 were born by 2026-07-26 (`assumption-check`, `authorization-design`, `bug-epidemiology`, `characterization-tests`, `claude-home-audit`, `co-change-radar`, `injection-safe-inputs`, `plan-panel-loop`, `plan-queue`, `reality-check`, `resolve-conflicts`, `shelf-life`, `skill-export`, `substitution-ledger`, `teach`, `test-trust-audit`, `transcript-export`), 5 on 2026-08-06 (`decision-flip`, `decision-owner-map`, `fence-archaeology`, `incentive-map`, `outside-view`), and 1 on 2026-09-01 (`document-to-markdown`).
- Fires since 2026-07-02 total 3,972. The largest: `load-handoff` 876, `save-handoff` 585, `throughline` 298, `outcome-shaping` 137, `making-recommendations` 106, `review-reviewer` 101, `gh-pr-review-loop` 92, `scrutinize` 90, `merge-branch` 64, `relay-by-reference` 64, `implementation-planning` 63, `triage` 55, `execute-plan` 40, `implementation-review` 40, `agent-facing-design` 38. The hot-core shape of the first read holds.

## Reading against the branches as written

**Branch B, "firing has spread":** true in the plain sense for 16 of the 40. Fifteen of the 16 fired in other repositories, so the spread is not an artifact of work inside this repository. Eleven fired after the July treatment window. The spread is uneven: three skills account for most of the post-August fires, and two of the largest July counts (`simplify-code`, `improve-codebase-architecture`) are the observer-effect cases the footnote warns about.

**Branch A, "the zero-fire set is still broadly zero":** true for 24 of the 40, and in the strongest form for 21 of them, which have never fired on either runtime in their whole life after two months of full coverage.

**What the record does not settle.** It set no threshold for "broadly", and it did not say how to read a set that splits 24 to 16. Read as a whole, 60 percent of the set is still zero; read per skill, firing has spread to 40 percent of it. Both readings are honest. This record does not pick one, because picking one now would be the post-hoc reframing the commitment forbids. One observation, offered as an observation and not a verdict: the prune branch's remedy is defined over never-fired skills, oldest and least-storied first, and the 24 (or the 21) are exactly that population; the vindication branch's "pruning stays light" is compatible with a first tranche limited to that population. Under either branch, the 16 that fired are outside any tranche.

**The other two obligations tied to this date.** The parked Skill Use contract's reopen trigger asks whether silence or missed composition recurred in lived work. A fire ledger cannot see a skill that should have fired and did not, so this read neither fires nor clears that trigger; it stays observable only through JP's corrections. The sealed skill value test has not run, so the pairing the prereg described did not happen; this read predicts nothing about that test (`docs/plans/2026-07-10-skill-value-test-preregistration.md:171`).

## What this read does not establish

- Rows are invocation and load markers, not proven fires, in both directions. The miner's standing footnote applies in full: Codex rows record a capsule load, some of which the agent then declined; Claude-side skills exercised without a Skill call or typed command leave no row; the live hook records Skill-tool calls only, so typed commands and all Codex fires land only when the miner runs; a fire census is an intervention, and post-treatment surges are partly caused by the treatment.
- The working-directory classes are a heuristic. A scratch-directory fire is certainly a test; a fire in this repository may be real work (the release cuts are) or a test; a fire in another repository can still be a forward test run there (the Era 148 `decision-record` capture in cross-model was one).
- Explicit-only skills (`zoom-out`, `gh-pr-review-loop`, `setup-matt-pocock-skills` in the 40) cannot be routed to by the model, so their rows measure JP's recall, not routing, as the challenge record already noted.
- Fire counts do not measure the value the always-loaded instructions name as cognitive offload. `AGENTS.md`, "What The Skills Are For", says sustained global silence is legitimate prune input and never an automatic verdict; this record is input of that kind.
- Codex Desktop sessions are visible only through `~/.codex/sessions`; nothing else was inspected.

## Evidence boundary

Inspected: the ledger after today's refresh (7,150 rows); `scripts/skill-usage-miner.py` at `2dc5b21` (current); the roster at `756501f` and at `8fcc585`; the challenge record, the design and implementation plans, the decisions ledger, the value-test prereg, and the two July handoffs cited above. The sibling script and its raw output are committed beside this record and reproduce every number in it from the ledger; the ledger itself lives outside the repository and grows, so a re-run later will differ. No transcript body was read for any fire. Citations are true at `8fcc585`; later edits can invalidate them.

## Next moves, none taken here

1. JP reads the branch call from the numbers above.
2. If the prune branch is taken, a separate step proposes the first tranche over the 21 (or 24), oldest and least-storied first, by `git mv` into `skills-archive/`, never deletion, for approval before anything moves.
3. Whether to run the sealed value test, which was meant to pair with this read, is a separate JP decision.
4. If a further read is wanted, name its date; the 23 skills born after 2026-07-02 with no fires would be that read's population, and this record is the baseline for it.
