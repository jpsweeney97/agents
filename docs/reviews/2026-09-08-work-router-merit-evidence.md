# Is `work-router` useful? Evidence run, 2026-09-08

> Status: durable copy of the evidence run that answered JP's question 'how useful is work-router?'. The recommendation (keep; apply the gap-review fixes; add the tracker prerequisite) was accepted and landed on `main` as commit `1becbe0` on 2026-09-09. Companion review: `2026-09-08-work-router-gap-review.md`. Scratchpad paths named below were temporary.

Question from JP: how useful is Work Router, does it really route to all of my skills, and what is it actually doing?

## Short answer

- **What it does in practice:** it is the thing that answers "which skill should handle this?" and "what's next?" questions with a reasoned note (owner, why, the plausible skills that lose and why, prerequisites, next move). Claude fires it on its own for such questions: 36 of 39 plain "Which skill should handle this?" probes invoked it without anyone typing its name.
- **Coverage:** on a 36-skill sample spanning every visibility class (described, listed by bare name only, hidden on purpose, plugin, Claude-only), it named the right skill 34/36 times when typed on Claude, 34/35 when asked plainly on Claude, and 32/36 on Codex. Bare-name and plugin skills were found 8/8 in every arm. The misses were one hidden skill (`plain-language`) in all arms, one hidden plugin skill on one arm, and Claude-only skills on Codex (which cannot see them).
- **Weak spot:** when nothing owns the work, it usually forces an owner or invents a sequence (hit 1/3, 1/3, 2/3 across arms).
- **Real use so far:** of 21 past Codex sessions where the file was read, 7 were real routing uses (all model-initiated, mostly on "What's next?" or a pasted completion report), 5 were sessions editing the skill, 3 were reviews of it, 6 were bulk reads. In 6 of the 7 routing uses the routed skill was invoked next; in 1 the route (`triage`) was infeasible because the repository had no remote and the router never checked.
- **Recommendation:** keep it. Its value is the reasoned note you get for free on routing questions, not better matching than the runtime alone (that comparison could not be isolated, see caveats). Apply the gap-review fixes; consider one extra line from the corpus (check tracker/remote availability before routing to `triage`).

## Method

- Corpus: 4 extractors read the 21 available Codex transcripts (the 1 Claude fire has no transcript on disk) and classified each read. An independent auditor re-read 6 and disagreed on 1 non-routing classification (other → library-editing); routing-use count unchanged.
- Eval set: 1 author wrote 39 realistic requests (no skill names, no description wording) for 36 skill targets + 3 no-owner situations. Strata: S1 described-and-visible standalone (8), S2 bare-name-only standalone (8), S3 hidden explicit-only (7), S4 plugin skills (8), S5 Claude-only (5), S6 no owner (3). Targets: `eval/targets.json`; requests: `eval/requests.json`.
- Probes: 4 runners ran each request 3 ways as read-only-intended subprocesses from the scratchpad: `/work-router <request>` on Claude, `Which skill should handle this? <request>` on Claude, `$work-router <request>` on Codex. 117 runs, 0 timeouts, 1 budget error. Raw outputs: `probes/`.
- Grading: 4 blind graders scored each run (owner named = target?). Auditor re-graded 19 runs blind: 0 disagreements.
- Agents: 14 total. Cost of the Claude probes: about $70 (median $0.82 per run); Codex cost not reported by its CLI.

## Results

Hit = the note names the intended skill as the primary owner (bare or namespaced spelling). T32-claude-plain excluded (budget error; its text did name the target).

| Stratum | Claude, typed `/work-router` | Claude, plain question | Codex, typed `$work-router` |
|---|---|---|---|
| S1 described, visible (8) | 8/8 | 8/8 | 8/8 |
| S2 bare name only (8) | 8/8 | 8/8 | 8/8 |
| S3 hidden explicit-only (7) | 5/7 | 6/7 | 6/7 |
| S4 plugin skills (8) | 8/8 | 8/8 | 8/8 |
| S5 Claude-only (5) | 5/5 | 4/4 | 2/5 |
| **Real-skill total (36)** | **34/36 (94%)** | **34/35 (97%)** | **32/36 (89%)** |
| S6 no owner (3) | 1/3 | 1/3 | 2/3 |
| Non-routes named per note (mean) | 3.6 | 3.3 | 1.8 |
| Median duration | 54 s | 50 s | 20 s |

Misses on real skills:
- `plain-language` (hidden): all three arms. Claude typed: routed to `soundcheck`; Claude plain: "no skill should handle this, the always-loaded instructions own it"; Codex: just did the rewrite itself.
- `review-family:review-reviewer` (hidden plugin): Claude typed said no current skill owns it; the other two arms found it.
- Claude-only skills on Codex: `claude-home-audit`, `context-checkpoint`, `friction-to-guards` not found (Codex never loads `skills-claude/`); `cross-model-review` and `methodology-critique` were found anyway, presumably via library cross-references.

Hidden-skill handling: on Claude, every hit on a hidden skill also said it must be invoked explicitly (7/7 + 6/6). On Codex only 3 of 6 hits said so.

No-owner handling: 4 of 8 graded no-owner runs presented a fallback (or a sequence of skills) as the owner instead of saying no skill owns the work. The auditor notes this grading is phrasing-sensitive; the pattern is consistent with gap-review finding C2.

## What it actually did in the 21 past sessions

| Class | Count | Notes |
|---|---|---|
| routing-use | 7 | 2026-07-09 → `contract-change-propagation` (invoked); 07-12 "What's next?" → `diagnose` (invoked, JP pasted the note as the prompt); 07-28 curation → self-corrected from misusing work-router as an analysis wrapper to `scrutinize-skill`; 08-22 → `triage` (user redirected: repo had no remote); 08-28 "Great. What's next?" → `tdd` (invoked); 09-01 → `implementation-planning` (invoked); 09-02 pasted report → `plan-cycle:triage` (invoked) |
| library-editing | 5 | sessions editing work-router or the deliberate bundle (after auditor correction) |
| review-or-audit-of-work-router | 3 | reviews of the skill itself |
| other | 6 | bulk neighbour reads during design sessions and library-wide surveys |

None of the 7 routing uses was a typed `/work-router` or `$work-router`; all were the model consulting the skill on its own. That matches the probe finding: the runtime reaches for it on routing questions without being told.

## Caveats that bound these numbers

- **No true "without the skill" arm.** The plain-question arm fired work-router in 36/39 runs, so it measures the skill firing implicitly, not routing without it. Isolating a no-skill baseline would need a copy of the served skill set minus the target; not done.
- **Fire detection artifacts.** Typed `/work-router` expands client-side, so the Skill tool never appears; the skill body was in context (template shape in 38/39). Codex "fired" was inferred from file reads and is false-negative in 4 runs that clearly used the skill.
- **Probes were not truly read-only.** `--allowed-tools` did not constrain Bash under the inherited permission mode; one plain-arm probe (T32) executed `claude-home-audit` and wrote five files into `~/.claude/audits/` (see side effects); another (T35) executed `friction-to-guards` and returned a hook proposal instead of a route (no writes observed).
- **Budget pressure** shaped six Claude runs (spent > $1.20 of the $1.50 cap) and killed T32-plain.
- **Sample, not census:** 36 of 122 skills were probed; every visibility class is represented, but per-stratum counts are small (5–8), so treat percentages as indicative.
- **Codex arm read JP's memory file** (`~/.codex/memories/MEMORY.md`) in some runs, a source the Claude arm lacks.

## Side effects of this run (outside the skill under review)

1. `~/.claude/audits/`: `.lock` (session `e145c105`, a probe session), `plan-2026-09-08.json`, `2026-09-08-2305.md`, `snapshots/20260909T030346Z.json` and `.err`, all written by the T32-claude-plain probe. Nothing was trashed or moved (no `~/.Trash` additions in the window; the plan carries no execution status; the report says "Not executed here"). The stale `.lock` may block a future real `claude-home-audit` run.
2. `~/.claude/logs/skill-usage-ledger.jsonl`: 48 synthetic rows (46 `work-router`, 1 `friction-to-guards`, 1 `claude-home-audit`) from probe sessions, identifiable by `cwd` under the scratchpad. The probe sessions' transcripts also exist under `~/.claude/projects/` and would be re-mined unless removed.
3. `~/.agents` untouched (git status clean).

## Files

- This report: `report.md`; workflow result: `result.json`; roster with visibility classes: `roster.json`; transcript manifest: `transcripts.json`; auditor working files: `audit/`.
- Related gap review (same session): `2026-09-08-work-router-gap-review.md` in this folder.
