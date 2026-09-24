---
type: review
date: 2026-09-24
scope: "plugins/decide/skills/design-exploration (decide 2.6.0) — SKILL.md, the bundle's only file; repo consumers by grep; fire census over ~/.claude/projects, ~/.codex/sessions, ~/.codex/archived_sessions, and the skill-usage ledger"
reviewed_commit: 13778761bd658135c9c4fceaf1d9efb930466371
method: "methodology-check — single-agent, single-pass, read-only: sealed anchor, text read, consumer grep, marker census (five body markers plus the one-day-old seam marker), ledger classification by runtime, kind, era, and venue, name-keyed route co-occurrence, turn-count classification of candidate transcripts. No transcript read end to end. No subagents."
posture: "read-only, evaluation-only — no target file edited; nothing invoked"
---

# Methodology check: decide:design-exploration

## Evidence Boundary

Text plus census only. Behavioral direction was not inspected: no fire was read end to end, and every classification below is a ledger field, a turn count, or a name-keyed skill invocation, not a judgment of how an instrument fired. This is a single-judge cheap pass whose only check is JP's reading. It is not a fire-tested adjudication; the fire-tested treatment of this skill is `docs/reviews/2026-07-03-design-exploration-methodology-critique.md`, and this brief does not revise it.

## Verdict (on text + census)

The method holds as the July treatment left it. The premise (explore approaches, develop one, get explicit approval, hand off warm) was adjudicated against fourteen real fires on 2026-07-03, and the repairs that critique wrote as its design brief landed the same day (`9fc5332`). What this pass adds: a post-repair field corpus now exists and has never been read, and the receipt rule landed today (decide 2.6.0, `fed8d98`) has a warrant thinner than its wording. The open question is no longer the text.

## Anchor, sealed before evidence

Central epistemic claim: a design approved through this procedure, grounded in code, scope-checked, offered as an honest count of real rivals with a labeled lean, checked in at named decisions, and approved explicitly, is settled by the user's correction rather than by assent to a fluent draft, and the handoff capsule carries that settledness to the next lane.

Provisional verdict: holds as a procedure, with two soft joints. The routing boundary ("clear enough" versus "still muddy") has no test beyond the agent's judgment, and the count of "genuinely different" approaches is judged by the same agent that authored the field.

Census prediction: all-body target, no on-demand surface, so no per-instrument probe is cheaply available. The skill fires thinly: on the order of a dozen Claude fires and a few Codex reads across the surviving windows. The seam clause (added today) greps zero by vintage and proves nothing.

Where the evidence corrected the anchor:

- The fire count was wrong by a lot. The ledger holds 31 Claude invocations, 16 Codex invocations, and 72 Codex shell reads. This is one of the library's more-used judgment lanes, and Codex reads outnumber Claude invocations.
- Both soft joints were already fire-tested in July. The boundary was vindicated (six clean permissioned entries from the shaping lane, no observed misroute); the count was found to be a staged race and repaired to an honest count with an `ideate` exit. My prior re-named settled questions.
- The seam marker did not grep zero: five hits, all dated 2026-09-24, of which at most two are real fires and the rest are today's `claude -p` proxies and smoke-test fixtures.
- One name-keyed instrument was probeable after all: the route-outs (`prototype`, `grill-me`, `scrutinize`, `ideate`) are skill invocations the ledger records by name, so their co-occurrence after a fire is countable, with the mention-not-behavior caveat below.

## Census, graded: contextualizes

| Measure | Value |
|---|---|
| Claude invocations (ledger, all time) | 31 rows, 31 sessions |
| Codex invocations / Codex shell reads (ledger) | 16 / 72 rows (68 sessions) |
| Invoke sessions after the repairs (since 2026-07-03), both runtimes | 34 (Claude 24, Codex 10) |
| Post-repair Claude field fires with a surviving transcript | 11 (cross-model 4, athena-kb-local 5, playpen 2) |
| Post-repair Claude sessions whose transcript is gone | 11 of 24 |
| Post-repair Codex field invocations | 8 |
| Claude transcript window (content date) | from 2026-07-12 |
| Codex rollout window | from 2026-01-04; archived from 2026-02-08; whole skill life |
| Seam-rule real fires (since 2026-09-24) | ≤2 |
| Sessions with `outcome-shaping` in the same session (all time) | 8 of 47 |
| Transcripts with a body marker in context | 56 Claude files (13 top-level fires, 4 proxies, the rest `.agents` maintenance and subagent files), 103 Codex files |

Route co-occurrence, post-repair, skill invoked later in the same session as a `design-exploration` invoke (34 sessions): `scrutinize` 10, `implementation-planning` 7, `grill-with-docs` 4, `making-recommendations` 4, `ideate` 3, `to-issues` 2, `decision-record` 2, `prototype` 1, `option-shaping` 1, `grill-me` 0, `to-prd` 0, `premortem` 0, `deliberate` 0. July's record: `prototype` 0 of 14; the stress-test route-out never taken as `grill-me` on three occasions.

Grade: contextualizes. Enumeration is complete on both surfaces. Classification is by ledger fields and turn counts, not by reading; the Codex classifier's fire and maintenance flags over-trigger on roster injection and were discarded in favor of the ledger's own `kind` field. No body instrument is grep-provably dead (whole-body floor). The seam instrument is inconclusive: thin corpus, not absence.

Confounds cleared:

- Corpus reach: Claude transcripts survive from 2026-07-12 by content date (mtime says 07-16; the ledger holds Claude rows back to 06-14). Eleven of the 24 post-repair Claude sessions have no transcript to read. Codex rollouts cover the skill's whole life. Absence claims are bounded to those windows.
- Marker vintage: the five body markers entered the text between 2026-06-12 (`966f903`) and 2026-07-03 (`9fc5332`), so the whole post-repair window is covered. The seam marker entered today (`fed8d98`) and can match only today's sessions.
- Contamination: none of the six markers sits in the description. All six are unique to this skill among live sources (the `exports/design-exploration` copy is the same skill re-targeted for claude.ai and is not a transcript surface). Maintenance sessions were classified by `SKILL.md` path mentions in tool inputs; 32 Claude marker files are `.agents` maintenance or subagent files, dropped.
- Whole-body injection: per-instrument deadness of body instruments is not probeable from in-context markers. Nothing below rests on one.
- Output probes for the target's vocabulary: none were run. The route co-occurrence counts are ledger invocations of other skills, which are real fires of those skills but not evidence the route was offered or that the offer caused them; an offer can be honored inline without invoking anything, so a zero is not deadness.
- Proxies: four Claude files under a session scratchpad on 2026-09-24 are today's capsule-receipt forward-test proxies (`docs/smoke-tests/2026-09-24_capsule-receipt-forward-tests.md`); three Codex sessions the same day under `~/Documents/Codex/2026-09-24/` and `~/image-prompts` are Codex Desktop threads, not classified further.

## Findings

Each finding states why it is not a `scrutinize-skill` contract finding, and carries a tag.

### 1. The repairs demand honesty at the drop points but install no detector (escalate-rider)

The July critique found that field fires compressed to one led recommendation ratified as offered, that check-ins collapsed into one approval ask, that the capsule stopped firing, and that every compression complied with the contract as written. The repairs are wording at those five points: honest count with an `ideate` exit, labeled lean carrying the rival's case and the priced trade, check-ins at the decision grain, the action-request approval edge, a capsule that records how contested the design was, and a prototype trigger bound to the agent's own tell. By design no counterparty classifier was added.

Decided here: the lane still has no instrument that tells it whether the counterparty contested. Its only record of contest is the capsule's settledness grade ("contested and corrected during the cycle, or accepted as offered"), written at handoff by the author of the design. The grade is factual rather than a judgment, so it is honest when written; whether it is written in field fires is exactly what July found dropping.

Not a contract finding because the obligations are stated clearly and the output shape is fixed; the question is whether "approved" still means "settled" in a regime where nobody contests, which is a claim about what the approval seat can know.

Rider: whether the post-repair field fires show the labeled lean carrying the rival's case, any rival ever picked (July: the recommendation led in all fourteen fires and lost in none), check-ins landing before the approval ask, and the capsule written. That needs the fires read.

### 2. The seam receipt rule can detect an absent seam, not a wrong one (escalate-rider)

Decide 2.6.0 adds: when the outcome arrives as a capsule or handoff that marks a seam, read the seam before designing; compressed and unpriced parts are open, not settled; put them to the user in the first clarification round; carry unconfirmed ones forward marked; a handoff that says only "settled" is itself a compression, so ask what the user said.

Decided here: the rule treats the seam's "what the user said in their own words" section as verbatim and everything else as open. A seam that misquotes or omits passes. That is what a text-level receipt can warrant when the compression and the seam were written by the same model family, often in the same session. The rule is honest about absence (no seam means ask) and silent about fidelity.

Not a contract finding because the trigger and the required action are unambiguous.

Rider: today's forward tests (`docs/smoke-tests/2026-09-24_capsule-receipt-forward-tests.md`) already show the rule does not discriminate from the old text on an explicit one-turn fixture, and grade the repair untested for discrimination. Real fires since the rule landed: at most two. Do not judge it on this corpus; the first real handoff from a 2.5.0 `outcome-shaping` capsule is the evidence to read.

### 3. The pressure route the text names is not the one that fires (decided-here, census)

The approval section says: on a hard-to-reverse design, offer one round of pressure before settling, naming `grill-me` or the relevant review lane. Post-repair, `grill-me` never fired after a `design-exploration` session; `scrutinize` fired afterward in 10 of 34 and `grill-with-docs` in 4. `prototype` fired once afterward (July: 0 of 14).

Decided here: the pressure the July critique said the lane's best outcomes depended on now has a countable route, and it runs through the review lanes, not the named grilling lane. Whether the lane's offer caused those fires or the user summoned them independently is finding 1's rider. The narrower question, whether the text should name the lane actually used, is routing hygiene and belongs to `scrutinize-skill`; refused here.

### Refused (contract altitude)

The step-2 scope check applies a dependency-cycle test to a proposed sub-project split before any design exists, and the step-7 self-review checks scope fit but not cycles between sub-projects. A `scrutinize-skill` pass would catch that as a missing re-check step; dropped.

## Not inspected

Any transcript end to end. The direction of any instrument. Whether any rival was picked post-repair. Whether the capsule is written in field fires. Whether the Codex shell-read regime (72 reads against 16 invocations) narrates the body as a checklist, the hypothesis the same-day `outcome-shaping` treatment filed as a watch item for that skill.

## Recommendation

One `methodology-critique` commission on finding 1's axis: in the post-repair field fires (11 surviving Claude transcripts, 8 Codex invocations, plus the Codex shell-read sessions in field venues), does the labeled lean carry the rival's case, is a rival ever picked, do check-ins land before the approval ask, does approval survive the action-request edge, and is the capsule written. Finding 2 waits for real capsule fires. JP commissioned the finding-1 axis the same day; this pass did not invoke it.

## Artifacts

Scratchpad only, not persisted: `census.py`, `census2.py`, `census.json`, `census.txt` under the session scratchpad. Re-run cost is a few minutes of grep.
