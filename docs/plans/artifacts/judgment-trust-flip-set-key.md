# Judgment/Trust Flip-Set — Answer Key (SEALED)

> Do **not** load this file into any reviewer's context, and do **not** open it
> until every reviewer disposition from Task 9 is recorded. Pairs with the blind
> fixture `docs/plans/artifacts/judgment-trust-flip-set.md`.

Acceptance test for the judgment-vs-trust apparatus change
(`docs/plans/2026-06-15-judgment-trust-apparatus.md`). Rows 1–8 are each a finding
from `.agents/skill-library-scrutiny-2026-06-15.md`; row 9 is an over-cut probe
(no report finding — its pass is that the reviewer raises *none*). After the
apparatus edits land and `review-family` is republished, re-score each row by
reviewing the named skill with the edited `scrutinize-skill`. **Pass = the reviewer
applies the right bar to each finding — not one label to each skill.** Judgment
*conformance* findings drop/reverse; judgment *thinking* findings
(under-provocation — including a softened/dulled forcing function — and structure
that strangles thinking) keep/escalate; trust findings — including the
mechanical/lookup tail (row 8) — keep/escalate; the mixed row splits per part; the
over-cut probe (row 9) draws no substitutive-structure finding. The signal is
correct discrimination, not a uniform direction per class.

Construction rule: only findings clear enough that the verdict reproduces under
judgment belong here. Borderline provoke-vs-substitute cases are deliberately
excluded — they would make the signal non-reproducible. The one over-cut probe
(row 9) is admitted on the same standard from the other direction: the organizing
structure it protects must be *clearly* the eliciting kind, so that flagging it as
substitutive is reproducibly wrong.

| # | Skill | Class | Report finding | Expected flip |
|---|---|---|---|---|
| 1 | scrutinize | judgment | verdict-token casing / section-name divergence with reference | DROP — cosmetic; no effect on critique quality |
| 2 | system-design-review | judgment | "define low/med/high so the finding-cap rule is complete" | REVERSE — question whether numeric finding-caps belong on a thinking skill, do not complete the rule |
| 3 | tdd | judgment | "no closure / done condition / output shape" flagged as a defect | REVERSE — absence of a mandated output shape is often correct for a judgment skill, not a defect |
| 4 | merge-branch / closeout-check / acceptance-map / git-hygiene | trust | protected-branch gate hand-copied into 4 skills | KEEP + ESCALATE — shared machinery is the value; duplication is real brittleness |
| 5 | search-handoffs | trust | `$PROJECT_ROOT` referenced in snippets, never assigned | KEEP — silent no-op breaks reliability |
| 6 | gh-pr-review-loop | mixed | `@codex review` hardcode (trust part) AND a "thread-assessment lacks fixed output shape" concern (judgment part) | PER-PART SPLIT — KEEP/escalate the hardcode (trust part); DROP the output-shape concern (judgment part). Passes only if the reviewer classifies per part, not the whole skill |
| 7 | grill-me | judgment | "'shared understanding' framing softens the adversarial posture" (report §4, grill-me row) | KEEP/ESCALATE — grill-me's whole value is adversarial provocation; softening that posture is lost thinking, the judgment bar's *provoke* failure. A reviewer that drops this as "just a soft prose nit on a judgment skill" has gone lenient, not discriminating. This is the tripwire row |
| 8 | claude-code-docs | trust (mechanical/lookup) | Alias section rewrites category filters that are themselves valid live enum values (`claude-md`→`memory`, `configuration`→`config`), risking silent wrong-bucket retrieval (report top-issue #10) | KEEP/ESCALATE — claude-code-docs is a mechanical/lookup skill, and that tail sits on the *trust* side (reliable, correct retrieval is its value, not better thinking). A silent wrong-bucket bug is the exact reliability failure the trust bar exists to catch. A reviewer that treats lookup/transform skills as outside both bars, or waves this off as "not a real skill," has mis-sorted the tail |
| 9 | outcome-interviewer | judgment (over-cut probe) | The one-question-at-a-time interview rhythm (ask, wait, reflect, choose the next question) could be read as a mandated output shape / fixed-section conformance to cut | DO NOT FLAG — the rhythm *is* the forcing function that elicits one decision at a time; it organizes and provokes thinking rather than making the judgment for the agent. A reviewer that flags it as "substitutive structure, cut it" has over-swung from over-flagging conformance to over-cutting legitimate organizing structure. Expected: no substitutive-structure finding raised against the interview rhythm |

Why row 6 is load-bearing: whole-skill classification fails it both ways —
classify-all-trust wrongly demands output shape on the judgment part;
classify-all-judgment wrongly drops a real lifecycle bug. It is the only row that
exercises per-part classification, the mechanism that made "no class field" the
right design choice.

Why row 7 is load-bearing: rows 1–3 are all designed to drop, so a reviewer that
reflexively drops *every* judgment finding passes them — and, with rows 4–5
keeping, satisfies a naive "asymmetry by class" check while having stopped
reviewing judgment skills at all. Row 7 is the only judgment finding that must
KEEP. It separates "stopped over-flagging conformance" (the goal) from "went
lenient on judgment" (the new failure mode). Without it the test cannot fail on
leniency. Row 7's defect is a *softened* forcing function — grill-me's adversarial
posture diluted by "shared understanding," not a total absence of provocation — so
the loaded rubric (Tasks 2/4) must name the dulled/softened-provocation shape or a
blind reviewer cannot reach it; that naming is part of this plan. Caveat carried
knowingly: the source report logged this finding as Minor and listed grill-me under
"zero confirmed material findings," so row 7's KEEP is a deliberately sharpened
edge case — which is exactly why Task 9 scores silence across three independent
reviewers as leniency rather than trusting a single pass. Row 7 meets the
construction rule as a clear softened-provoke case on a skill whose value is
provocation, not a borderline provoke-vs-substitute call.

Why row 8 is load-bearing: it is the only row drawn from the mechanical/lookup
tail — knowledge-lookup and pure-transform skills (claude-code-docs, openai-docs,
markdown-reformat) that are neither "better thinking" nor a supervised task. The
binary is most likely to mis-sort exactly here. Row 8 pins the intended answer:
the tail is governed by the trust bar (reliable, correct execution is its value),
so a real reliability defect KEEPS. Without it the flip-set proves the distinction
only on the two families it was built around and stays silent where its soundness
is most in question.

Why row 9 is load-bearing: rows 1–3 and 7 test the over-flag axis (does the
reviewer stop docking conformance, yet still keep a real thinking defect?). None
tests the symmetric hazard the apparatus introduces — that a reviewer now told to
treat mandated shape, exhaustive rules, and fixed sections as defects over-swings
and CUTS organizing structure that should stay (Task 2: judgment skills "may carry
plenty of structure ... as long as it organizes thinking"). Row 9 is the only
over-cut probe: its pass is the reviewer NOT raising a substitutive-structure
finding against outcome-interviewer's eliciting rhythm. Unlike rows 1–8 it is not a
re-scored report finding but a no-finding-expected probe; if a future reviewer
genuinely cannot tell the organizing rhythm from substitutive scaffolding, that
inability is itself the finding. Without row 9 a reviewer that has swung to
"structure on a judgment skill is always a defect" passes the set clean.

Anti-leniency check: the pass condition is correct discrimination, not fewer
findings. Score row 7 by what the reviewer does with the provoke concern, not by
whether the word "keep" appears: if the reviewer raises the softened-adversarial-
posture concern and then KEEPS/ESCALATES it, that is the pass; if it raises the
concern and then drops or downgrades it, the apparatus has gone lenient on
judgment — FAIL, even if rows 1–6 all land exactly as predicted. The test runs
three independent reviewers (Task 9): if **all three** stay silent on the concern,
that is a leniency FAIL by default — a certified provoke defect no independent
reviewer surfaces means the apparatus is not making reviewers look, not that the
row is borderline. Marginality is earned only by a separate manual re-read
concluding the row is genuinely borderline (or by a raised/never-raised split among
the three), never assumed from silence.
