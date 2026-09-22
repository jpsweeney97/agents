---
type: review
date: 2026-09-21
scope: the 122-skill live roster (skills/, skills-claude/, plugins/*/skills/) read against the skill-usage ledger, asking which skills have never been used
reviewed_commit: be684bd
method: ledger refreshed with scripts/skill-usage-miner.py, then read by the sibling 2026-09-21-never-used-skill-census.py (the miner's own collapse/alias code, plus synthetic-cwd, roster-scan, and external-token filters); the miner's Claude-side blind spot closed by scanning all 2,126 ~/.claude/projects transcripts for unmined SKILL.md reads; raw output in the sibling .txt
posture: read-only; no skill was pruned, archived, or edited; every prune call is left to JP
---

# Never-used skill census, run 2026-09-21

JP asked which skills he never uses. This record is the census and renders no prune verdict. It is the successor read to `docs/reviews/2026-09-04-skill-usage-ledger-re-read.md` and its 2026-09-05 erratum, run against the whole current roster rather than the 40-skill set the 2026-07-02 framework challenge pre-registered.

## Outcome in short

- **24 of 122 live skills have never actually been used**, split into four tiers by how certain that is: 1 with no row of any kind, 2 with only synthetic probe rows, 12 seen in a roster scan and never chosen, and 9 that fired only inside this repository.
- **The miner's Claude-side blind spot was checked rather than assumed.** All 2,126 Claude transcripts were scanned for `skills/<name>/SKILL.md`. Every mention outside this repository turned out to be command output, not an invocation. No Tier 0-2 skill has a hidden fire.
- **Inbound routing is the constraint a prune has to respect.** The census counts, per skill, how many *other* live `SKILL.md` files name it. `red-team` is named by 8, `deploy-plan` by 6, `premortem` by 6, `research-capture` by 5. Five never-used skills have zero inbound routes.
- **A further 15 skills were genuinely used and then went cold** for 8 weeks or more, including `grill-me` (66 fires, silent 103 days) and `git-hygiene` (54 fires, silent 67 days). They are reported for completeness, not as prune candidates.

## How a row was classified

The ledger's raw rows over-count in three ways that matter to a never-used claim. Each is filtered, and the filter named so the next read can disagree with it.

- **synthetic** — the row's cwd is a session scratchpad. These come from `claude -p` proxy probes, chiefly the work-router merit run of 2026-09-09, which recorded loads that JP never asked for. Not his use.
- **scan-read** — a Codex `SKILL.md` read with `read_burst >= 4`: the model was reading many skills at once to choose a route. The skill was seen and passed over. This is the erratum's own cut, reused unchanged.
- **external token** — a plugin-qualified token whose prefix is not a local plugin is never credited to the local skill of the same bare name. Three tokens were excluded on this rule: `handoff:triage` (26), `github:gh-address-comments` (7), `sbonly:skill-benchmark` (1).

What survives all three is a **real** fire: a typed or model-invoked call, or a Codex read outside a scan, in a working directory that is not a probe scratchpad.

## Tier 0 — no row of any kind (1)

| skill | source | born | real | synth | scan | inbound routes |
|---|---|---|---|---|---|---|
| `decision-flip` | skills | 2026-08-06 | 0 | 0 | 0 | 0 |

## Tier 1 — only synthetic probe rows (2)

Every row came from a proxy probe. No real invocation.

| skill | source | born | real | synth | scan | inbound routes |
|---|---|---|---|---|---|---|
| `incentive-map` | skills | 2026-08-06 | 0 | 1 | 0 | 0 |
| `perf-optimize` | skills | 2026-09-01 | 0 | 2 | 0 | 0 |

## Tier 2 — seen in a roster scan, never chosen (12)

| skill | source | born | real | synth | scan | inbound routes |
|---|---|---|---|---|---|---|
| `claude-home-audit` | skills-claude | 2026-07-16 | 0 | 0 | 1 | 1 |
| `document-to-markdown` | skills | 2026-09-01 | 0 | 0 | 1 | 0 |
| `friction-to-guards` | skills-claude | 2026-06-12 | 0 | 0 | 2 | 1 |
| `resolve-conflicts` | plugins/git-cycle | 2026-07-09 | 0 | 2 | 2 | 4 |
| `authorization-design` | skills | 2026-07-10 | 0 | 0 | 3 | 1 |
| `decision-owner-map` | skills | 2026-08-06 | 0 | 0 | 3 | 1 |
| `reality-check` | skills | 2026-07-02 | 0 | 0 | 3 | 2 |
| `deploy-plan` | skills | 2026-06-27 | 0 | 2 | 6 | 6 |
| `injection-safe-inputs` | skills | 2026-07-10 | 0 | 0 | 7 | 1 |
| `observability-instrumentation` | skills | 2026-06-27 | 0 | 0 | 7 | 1 |
| `research-capture` | skills | 2026-06-25 | 0 | 0 | 9 | 5 |
| `plan-queue` | plugins/plan-cycle | 2026-07-26 | 0 | 0 | 19 | 0 |

`plan-queue` is the sharpest case in the table: 19 scans, every one of them a pass-over, and no other skill routes to it.

## Tier 3 — real fires, but only inside this repository (9)

These fired, and only in the workshop that authors them. `AGENTS.md` is explicit that absence from `.agents` is not evidence against a skill; this table says the converse, that presence *only* in `.agents` is the whole fire record.

| skill | source | born | real | scan | inbound routes | last real fire |
|---|---|---|---|---|---|---|
| `red-team` | skills | 2026-06-27 | 1 | 6 | 8 | 2026-06-27 (85d) |
| `to-questionnaire` | skills | 2026-09-01 | 1 | 6 | 2 | 2026-09-03 (17d) |
| `steelman` | skills | 2026-06-27 | 1 | 16 | 4 | 2026-06-27 (85d) |
| `scope-cut` | plugins/decide | 2026-06-30 | 1 | 20 | 3 | 2026-07-28 (54d) |
| `outcome-check` | skills | 2026-06-27 | 2 | 10 | 5 | 2026-07-28 (54d) |
| `assumption-check` | skills | 2026-07-09 | 2 | 12 | 3 | 2026-07-28 (54d) |
| `premortem` | skills | 2026-06-27 | 2 | 13 | 6 | 2026-07-28 (54d) |
| `methodology-check` | skills | 2026-07-07 | 2 | 16 | 3 | 2026-07-07 (75d) |
| `skill-squad` | skills-claude | 2026-06-24 | 13 | 7 | 0 | 2026-07-01 (81d) |

`skill-squad` is the outlier: 13 fires, all inside its own build week in June, none since.

## Tier 4 — used, then went cold for 8 weeks or more (15)

Reported so the cold end of the roster is visible in one place. These are used skills and not prune candidates on this record's evidence.

| skill | source | real | inbound routes | last real fire |
|---|---|---|---|---|
| `grill-me` | skills | 66 | 9 | 2026-06-09 (103d) |
| `git-hygiene` | plugins/git-cycle | 54 | 6 | 2026-07-15 (67d) |
| `simplify-code` | skills | 40 | 4 | 2026-07-15 (67d) |
| `search-handoffs` | plugins/handoff | 16 | 1 | 2026-07-10 (72d) |
| `methodology-critique` | skills-claude | 15 | 3 | 2026-07-19 (63d) |
| `the-gang-explains` | skills | 12 | 0 | 2026-07-26 (56d) |
| `caveman` | skills | 8 | 0 | 2026-07-04 (78d) |
| `acceptance-map` | plugins/plan-cycle | 3 | 6 | 2026-06-11 (101d) |
| `plan-panel-loop` | skills | 2 | 0 | 2026-07-08 (74d) |
| `skill-benchmark` | skills-claude | 2 | 8 | 2026-06-15 (97d) |
| `teach` | skills | 1 | 2 | 2026-07-24 (58d) |
| `zoom-out` | skills | 1 | 2 | 2026-06-07 (105d) |
| `transcript-export` | skills | 1 | 0 | 2026-07-03 (79d) |
| `reflect` | skills | 1 | 1 | 2026-07-02 (80d) |
| `doc-drift-audit` | skills | 1 | 2 | 2026-07-06 (76d) |

## The Claude-side blind spot was checked, not assumed

The miner does not mine a Claude session that reads a `SKILL.md` directly instead of calling the Skill tool, and the footnote names that gap. It could hide real use, so all 2,126 Claude transcripts were scanned for `skills/<name>/SKILL.md` for every Tier 0-2 skill.

Every mention outside `/Users/jp/.agents` was command output rather than an invocation: `ls` and `find` listings, and handoff text citing a path. The two clusters are one `cross-model` session that listed seven of these skills at once and two `playpen` sessions that listed three. No Tier 0-2 skill has a hidden fire.

One case is worth keeping. `document-to-markdown` is cited three times in `/Users/jp/athena-os` as the converter that repository's local `ingest` skill delegates to. Those sessions never invoked it — their Skill calls were `agent-facing-design`, `synapsis`, and `connect` — but it is a named dependency of a downstream skill. Zero fires there does not mean zero value.

## Relation to the standing prune program

The 2026-07-02 framework challenge committed to tranche-based pruning of never-fired skills, oldest and least-storied first, archiving rather than deleting. Tranche 1 executed on 2026-09-05 at `1c84ea3`: four skills archived, with `deploy-plan` and `observability-instrumentation` held for tranche 2, and `friction-to-guards`, `research-capture`, `steelman`, and `scope-cut` held as a later tranche (`docs/plans/2026-09-04-skill-prune-tranche-1.md`).

Six of this census's never-used skills are that program's already-known held population. What this read adds is the part the program has not seen: **the never-used skills born after the tranche-1 population was drawn**, chiefly `decision-flip`, `incentive-map`, `decision-owner-map` (2026-08-06), `perf-optimize`, `document-to-markdown`, `to-questionnaire` (2026-09-01), and `plan-queue` (2026-07-26). These are the youngest skills on the roster, which cuts directly against the commitment's oldest-first ordering. A prune argument against them is an argument about a six-week-old skill, and is weaker for it.

Two of them carry a lifecycle constraint a prune must handle rather than assume away:

- `plan-queue` is gated class, not build-and-prune. Its burn verb ends in a local fast-forward merge, so it took the Admission test and carries a `contract-decisions.md` entry (`docs/agents/skill-lifecycle-notes.md:127`). Retiring it is a charter event, not free churn.
- `perf-optimize` was an admitted build of the third mining program (2026-08-31 to 09-01), and `skills/perf-optimize/SKILL.md:13` routes outward to `deploy-plan` and `observability-instrumentation`, both themselves held for tranche 2.

## Evidence boundary

- Inspected: the ledger at its 2026-09-21 refresh, the live roster at `be684bd`, all 2,126 Claude transcripts, and the lifecycle notes and tranche plan cited above. Not inspected: Codex rollouts directly (they reach this read only through the miner) and the `references/` trees of individual skills.
- **A zero here means no recorded invocation, not proven never run.** The miner's T1 blindness footnote is reproduced at the end of the sibling `.txt` and governs every number above. Handoff-resumed arcs can run a skill's procedure with no fresh invocation, and a Codex load that read only a skill's `references/` leaves no row.
- This census is itself an intervention. Running it added transcript mentions of the skills it names — `perf-optimize` and `document-to-markdown` each gained one session between two runs of the sibling script an hour apart. Do not credit a skill for fires a census summoned.
- The scan-read cut at four reads in 180 seconds is a judgment inherited from the 2026-09-05 erratum, not a measurement. A real-work session that consulted three skills in two minutes counts as chosen; a scan that read three counts as chosen too.
