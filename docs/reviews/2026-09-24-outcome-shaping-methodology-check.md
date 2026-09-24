---
type: review
date: 2026-09-24
scope: "plugins/decide/skills/outcome-shaping (decide 2.2.x) — SKILL.md, agents/openai.yaml, examples/interaction-examples.md; repo consumers by grep; fire census over ~/.claude/projects, ~/.codex/sessions, ~/.codex/archived_sessions, and the skill-usage ledger"
reviewed_commit: 4bd53960708f28077dd3b77db1541b002e9182cb
method: "methodology-check — single-agent, single-pass, read-only: sealed anchor, text read, consumer grep, marker census (three body markers, one examples-file marker, one output marker), keyword-level classification of candidate transcripts. No transcript read end to end. No subagents."
posture: "read-only, evaluation-only — no target file edited; nothing invoked"
---

# Methodology check: decide:outcome-shaping

## Evidence Boundary

Text plus census only. Behavioral direction was not inspected: no fire was read end to end, and every classification below is a keyword probe over assistant output, not a judgment of how an instrument fired. This is a single-judge cheap pass whose only check is JP's reading. It is not a fire-tested adjudication; that lane is `methodology-critique`, which this brief recommends and did not invoke.

## Verdict (on text + census)

The method holds as a governor of model behavior, and its instruments are live in real use. The strong form of its central claim, that the interview constructs a want that is the user's rather than the model's, is not decidable from text. Three instruments carry structural riders that only fire-reading can settle.

## Anchor, sealed before evidence

Central epistemic claim: an interview run through one evolving, correctable read, with the user's words kept, each negotiable part priced by a hypothetical trade, and convergence defined as the user restating the want unprompted, constructs a want that is the user's rather than the model's fluent draft. A second claim rides on it: mud can be typed into four kinds, and only "missing words" is interview-soluble.

Provisional verdict: the method is unusually honest about the confabulation hazard but applies that hazard unevenly. Mud-typing and hypothetical trade-pricing are both model reads about the user's inner state, and the text exempts them from the suspicion it applies to the read itself.

Census prediction: the one on-demand surface, the examples file, is near-dead. Body instruments are not separately probeable. Expected fire count: roughly 5 to 20 Claude fires plus some Codex reads.

Where the evidence corrected the anchor:

- The examples file is live, not near-dead: it loaded in 9 of 53 genuine fires, about one in six.
- Codex carries most of the use (33 classified fires, 168 ledger rows), not Claude (20 fires, 21 ledger rows).
- The provisional verdict on trade-pricing and mud-typing survived the full text read.

## Census, graded: contextualizes

| Surface | Count |
|---|---|
| Ledger rows, name-keyed (`~/.claude/logs/skill-usage-ledger.jsonl`) | 189 (Codex 168, of which 41 `kind: read`; Claude 21) |
| Transcripts with a body marker in context, all corpora | 89 Claude, 88 Codex sessions, 10 Codex archived |
| Of those, genuine fires (a produced "My read so far", not maintenance) | 53 (20 Claude, 33 Codex) |
| Real-world fires (cwd outside `.agents` and scratchpads) | 28, of which 17 in one repo (athena-kb-local, Codex) |
| Examples file loaded inside genuine fires | 9 of 53 |
| Field fires naming a forward route in output | design-exploration 23, making-recommendations 9, all other exits 0 |
| Field fires with a restatement request ("in your words", "say back") | 5 of 28 |
| Field fires with trade language | 21 of 28 by a loose probe, 2 of 28 by a strict one |
| Field fires with testimony language (stated vs. revealed contradiction named) | 0 of 28 (0 of 53 overall) |

Confounds cleared:

- Corpus reach: Claude transcripts survive from 2026-07-16; Codex sessions from 2026-01-04, archived from 2026-02-08. All absence claims are bounded to those windows.
- Marker vintage: the three body markers ("harvests confabulation", "A want elicited in a cost vacuum is a wish", "Deference with eyes open") and the examples marker ("vigilance transposition") all entered the text in commit 26d7ae9 on 2026-07-02, the rebuild from `outcome-interviewer`. That is older than the Claude window, so vintage does not manufacture false absence there. Codex fires before 2026-07-02 belong to the predecessor and are out of scope.
- Contamination: none of the markers sits in the description. "My read so far" appears in no other live skill body. Maintenance sessions were filtered by path mentions plus edit or review vocabulary; the Codex filter is loose, so some of the 65 Codex sessions labeled maintenance may be fires inside `.agents`.
- Whole-body injection: per-instrument deadness of body instruments is not probeable from in-context markers. The per-instrument counts above are output probes, which upgrade "in context" to "produced this kind of output", nothing more.
- Proxies: the 2026-09-03 scratchpad sessions are the gap review's own blind proxies and were bucketed as local, not field. Twenty-eight Claude files carried the body only inside tool results (persisted output from other reads) and were dropped as noise.

## Findings

Each finding states why it is not a `scrutinize-skill` contract finding, and carries a tag.

### 1. Priced trades are hypotheticals put to a user the skill says confabulates

"Still worth it if it costs a week?" asks for an answer the user has no experience of. The Type the Mud section says that is exactly the question shape that harvests confident fake answers. The Load-Testing section then treats a survived trade as proof the want is real ("what survives, and what the user gave up to keep it, is the shape"). The text applies the confabulation suspicion to questions and to the read, and exempts the trade.

Not a contract finding because the instrument is clearly specified and its stop condition is stated; the defect is in what a survived hypothetical can know.

Tag: **escalate-rider.** Structure decided here. Whether trades in the field ever kill or reshape a want, or are rubber-stamped, needs the fires. The probe counts (21 of 28 loose, 2 of 28 strict) cannot tell those apart.

### 2. The one diagnosis that selects the whole method is the one the user never gets to correct

The read is offered for cheap correction because recognition beats recall. The mud type is held silently by design ("four shapes to listen for, not a label to declare"), so that same asymmetry is unavailable for the decision that picks the tool. The user can say "no, not that" to a want; they never see the typing.

Not a contract finding because the instruction is unambiguous; the issue is a correctability asymmetry between two instruments.

Tag: **escalate-rider.** In 28 field fires the named exits were design-exploration and making-recommendations only; `prototype`, `ideate`, `grill-me`, `option-shaping`, and `to-questionnaire` were never named, while local proxies named them over 100 times. Either field mud is always missing-words, or re-typing does not happen outside test conditions. Text and census cannot separate the two.

### 3. The own-words convergence test is not discriminating after a long read loop

The skill names its own fluency as a contaminant and treats the user's restatement as clean. By the time restatement is asked for, the user has absorbed the agent's vocabulary across several reads, and the agent has no way to score "words you did not supply."

Not a contract finding because the test is stated precisely; the issue is that it stops discriminating as the interview lengthens.

Tag: **escalate-rider.** The first live fire (`docs/reviews/2026-07-02-outcome-shaping-first-live-fire.md`) recorded a restatement that added genuine content ("reassurance"), so the instrument can work. How often restatements carry new content versus paraphrase the read needs the fires. Restatement was requested in 5 of 28 field fires; the text makes the ask conditional on stakes, so that count proves nothing about deadness.

### 4. The 2026-07-02 critique's reframe held (decided, favorable)

The predecessor's critique (`docs/reviews/2026-07-02-outcome-interviewer-methodology-critique.md`, section 10) read the artifact as restraint engineering wearing a method as cover story, and asked for a skill that knows itself as a governor, batches independent questions, and routes to widening and evidence. The rebuilt text does all three: the Restraints section says so in its first sentence, pacing is by contingency, and Exits run in every direction. The census shows the read, the capsule, and the route beat present in almost every field fire.

Tag: **decided-here.** The weak form of the central claim, that the method keeps the user the author to the extent text can, holds. The strong form (constructs a want that is the user's) is not text-decidable, and the text itself concedes joint authorship.

## Observation, not a finding

Testimony (artifacts as witnesses, named once) shows no output signature in any of the 53 fires. It fires only when a stated-versus-revealed contradiction arises, so absence is not deadness, and as a body instrument it is not cheaply probeable. It has remained unexercised since the first live fire recorded it so on 2026-07-02.

## Not inspected

Any transcript end to end. The direction of any instrument. Whether the 17 athena-kb-local Codex fires are one long-running shaping or seventeen separate ones.

## Recommendation

One `methodology-critique` commission covers all three riders. Axis: in the 28 field fires, do priced trades reshape wants or get rubber-stamped; does mud ever re-type toward evidence or options; do own-words restatements carry content the read did not hold. JP commissions it from a Claude session; this pass did not invoke it.

## Artifacts

Scratchpad only, not persisted: marker file lists, `classified.json`, `classify.py`, `probe.py`, `probe2.py` under the session scratchpad. Re-run cost is a few minutes of grep.
