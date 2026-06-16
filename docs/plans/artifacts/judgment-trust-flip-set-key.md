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
| 1 | scrutinize | mixed/per-part (compound) | verdict-token casing / section-name divergence with reference | PER-PART SPLIT — the verdict-token **casing** half is judgment-cosmetic: DROP (no effect on critique quality). The **section-name divergence** half is trust-flavored: the names are duplicated across `SKILL.md` and the reusable `references/review-format.md` template and have drifted (live-confirmed), so a single-sourcing/drift concern KEEPS as a downgraded Minor. Passes if the reviewer does not *escalate* the cosmetic half and reads the template-drift half on the trust bar; relabeled compound after the first run showed the original uniform "judgment" label under-determined the bar (reviewers correctly split judgment/trust) |
| 2 | system-design-review | judgment | "define low/med/high so the finding-cap rule is complete" | REVERSE — question whether numeric finding-caps belong on a thinking skill, do not complete the rule |
| 3 | tdd | judgment | "no closure / done condition / output shape" flagged as a defect | REVERSE — absence of a mandated output shape is often correct for a judgment skill, not a defect |
| 4 | merge-branch / closeout-check / acceptance-map / git-hygiene | trust | protected-branch gate hand-copied into 4 skills | KEEP + ESCALATE — shared machinery is the value; duplication is real brittleness |
| 5 | search-handoffs | trust | `$PROJECT_ROOT` referenced in snippets, never assigned | KEEP — silent no-op breaks reliability |
| 6 | gh-pr-review-loop | mixed | `@codex review` hardcode (trust part) AND a "thread-assessment lacks fixed output shape" concern (judgment part) | PER-PART SPLIT — KEEP/escalate the hardcode (trust part); DROP the output-shape concern (judgment part). Passes only if the reviewer classifies per part, not the whole skill |
| 7 | grill-me | judgment (silence-floor) | "'shared understanding' framing softens the adversarial posture" (report §4, grill-me row) | SILENCE-FLOOR — grill-me's value is adversarial provocation, so the apparatus must make reviewers **surface** the softened-posture concern (unanimous never-raised = leniency FAIL; a weak/token drop with no text-specific reasoning = leniency FAIL). grill-me is a **balanced** case (the softeners "shared understanding"/"recommended answer" are woven into dominant adversarial framing — "relentlessly / every aspect / each branch / weakest assumption"), so the keep/drop *disposition* is a judgment call, **not** a gate: a substantive, text-specific drop is correct discrimination, not leniency. Reclassified from a must-keep tripwire to the silence-floor after the first run (3/3 surfaced it; 2 substantively dropped, 1 kept — the verdict did not reproduce under judgment, i.e. the row was balanced, not a clear keep-case). The clear keep-case the bright-line needs is now row 10 (synthetic) |
| 8 | claude-code-docs | trust (mechanical/lookup) | Alias section rewrites category filters that are themselves valid live enum values (`claude-md`→`memory`, `configuration`→`config`), risking silent wrong-bucket retrieval (report top-issue #10) | KEEP/ESCALATE — claude-code-docs is a mechanical/lookup skill, and that tail sits on the *trust* side (reliable, correct retrieval is its value, not better thinking). A silent wrong-bucket bug is the exact reliability failure the trust bar exists to catch. A reviewer that treats lookup/transform skills as outside both bars, or waves this off as "not a real skill," has mis-sorted the tail |
| 9 | outcome-interviewer | judgment (over-cut probe) | The one-question-at-a-time interview rhythm (ask, wait, reflect, choose the next question) could be read as a mandated output shape / fixed-section conformance to cut | DO NOT FLAG — the rhythm *is* the forcing function that elicits one decision at a time; it organizes and provokes thinking rather than making the judgment for the agent. A reviewer that flags it as "substitutive structure, cut it" has over-swung from over-flagging conformance to over-cutting legitimate organizing structure. Expected: no substitutive-structure finding raised against the interview rhythm |
| 10 | (synthetic) `pressure-test-my-plan` fixture | judgment (synthetic clear-case keep-floor) | A fabricated skill whose name/description promise rigorous adversarial pressure-testing but whose body is *fully* reframed as gentle, supportive, reassuring collaboration with zero counter-pressure — an unambiguous, dominant softening with no countervailing adversarial language | KEEP/ESCALATE — this is the clear softened-provoke case the live library lacks: the forcing function is absent/fully diluted, so a reviewer applying the bar must KEEP it. Raised-then-dropped here IS leniency (the bright-line condition (1) validly applies — no balance to discriminate). The gross-regression floor for keep-disposition; mirror of the row-9 synthetic over-cut probe. Fixture at `docs/plans/artifacts/synthetic-probes/pressure-test-my-plan/SKILL.md` — a TEST FIXTURE, not a live skill |

Why row 6 is load-bearing: whole-skill classification fails it both ways —
classify-all-trust wrongly demands output shape on the judgment part;
classify-all-judgment wrongly drops a real lifecycle bug. It is the only row that
exercises per-part classification, the mechanism that made "no class field" the
right design choice.

Why row 7 is load-bearing (reframed after run 1): rows 1–3 are all designed to
drop, so a reviewer that reflexively drops *every* judgment finding passes them —
and, with rows 4–5 keeping, satisfies a naive "asymmetry by class" check while
having stopped reviewing judgment skills at all. The test still needs a
leniency-detecting row to separate "stopped over-flagging conformance" (the goal)
from "went lenient on judgment" (the new failure mode). Run 1 disclosed that
**grill-me is not a clear keep-case** — its softeners ("shared understanding",
"recommended answer") are woven into dominant adversarial framing ("relentlessly /
every aspect / each branch / weakest assumption"), and three independent reviewers
surfaced the concern but split 2-drop/1-keep, each reasoning text-specifically. The
verdict did not reproduce under judgment, so by this key's own construction rule
grill-me is a **balanced** case, not the clear softened-provoke case originally
asserted. (The source report had already logged this finding as Minor and listed
grill-me under "zero confirmed material findings" — corroboration that it is
borderline.) Row 7 is therefore reframed as the **silence-floor**: it binds the
*reproducible* part of leniency — does the apparatus make reviewers surface and
substantively reason about the provoke concern? (grill-me passes: 3/3 surfaced.)
The non-reproducible part — the keep/drop disposition on a balanced case — is a
judgment call, not a gate. The clear keep-case the bright-line still needs moved to
row 10.

Why row 10 is load-bearing: the bright-line "raised-then-dropped on a clear
keep-case = leniency" must stay *exercised*, but the live library contains no clear
softened-provoke defect (exhaustive search of live skills and the archive found
none — every adversarial skill is sharp; the only softened phrasings, grill-me and
grill-with-docs, are balanced). That absence is itself evidence the apparatus's
premise holds (the library is calibrated on the provoke side). To keep a
keep-disposition floor anyway, row 10 is a **synthetic, clearly-labeled fabricated
fixture** (not a live skill): a skill that promises adversarial pressure-testing
but whose body is fully reframed as gentle/reassuring collaboration with zero
counter-pressure. It is the mirror of row 9 (the synthetic over-cut probe): row 9
proves the reviewer does not over-cut legitimate structure; row 10 proves the
reviewer keeps an unambiguous softened-provoke defect. It tests gross
keep-disposition regression, not the subtle bar (which is unbindable against this
library, and recorded as such).

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

Anti-leniency check (reconciled after run 1 exposed a contract contradiction):
the pass condition is correct discrimination, not fewer findings. Score the
provoke concern by what the reviewer *does*, not by whether the word "keep"
appears. The **bindable leniency FAILs** are: (1) **unanimous never-raised** — no
independent reviewer surfaces the concern, so the apparatus is not making
reviewers look; and (2) **surfaced-then-dropped on weak/non-substantive
reasoning** — a token mention then a shrug that never engages the keep-rule or the
text. On a **clear** (construction-rule-compliant) keep-case, raised-then-dropped
is also a FAIL — dropping a genuine provoke defect is leniency. But a
**substantive, text-specific drop** (cites the line, names the keep-rule, argues
whether the dominant framing overrides the softener) on a case a **separate manual
re-read finds genuinely balanced** is **marginality**, not leniency — it means the
*fixture* row was balanced (a construction-rule violation), not that the apparatus
went lenient. The keep/drop disposition on a balanced case is a judgment call, not
a gate; only the two bindable FAILs above are gates. This corrects the original
flat "raises-then-drops = FAIL," which conflated lazy leniency (the real target)
with correct discrimination on a balanced case, and which contradicted this key's
own marginality clause. Correcting that false-positive path is not weakening: both
bindable FAILs stay intact, and the corrected scoring must be proven on a fresh
re-run, never by relabeling the run that exposed it. Marginality is earned only by
the manual re-read, never assumed from silence (silence is the opposite — a hard
FAIL). The clear keep-case the bright-line still needs is the synthetic floor
(row 10).
