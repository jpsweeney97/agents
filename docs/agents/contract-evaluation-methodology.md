---
type: methodology
project: agents
created: 2026-06-17
status: stable
source: "judgment-trust apparatus testing arc (tests 1–5, 2026-06-15 → 06-17); artifacts under docs/plans/artifacts/"
---

# Evaluating a Behavior Contract: Is It Load-Bearing and Beneficial?

How to test whether an agent-facing contract — a skill, rule, bar, or lens — actually changes behavior, for the better, and not just on paper. Distilled from the judgment-trust apparatus arc (tests 1–5). This is a **playbook, not an obligation**: reach for it when you need to know whether a contract earns its keep; ignore it for ordinary edits. The one rule it spun off — the **blinding guard** — already lives in `AGENTS.md` (`## Blind Evaluations`); everything else here is method.

## When to use it (and when it's overkill)

Use it when a contract is **consequential and contested** — you are about to keep, cut, or rewrite something agents must follow, and "it feels right" is not enough: you want evidence it is load-bearing (changes reviews/decisions) and beneficial (doesn't introduce a worse failure than it prevents).

It is overkill for ordinary skill edits, wording, or obvious wins. A full sealed run is days of work and many agent-hours; most decisions are settled by the lighter lanes (`scrutinize-skill` for critique, `behavior-smoke-test` for "is it followed", `skill-benchmark` for a quantitative pass-rate delta). Run the full apparatus only when the *value* of a contract is the open question and the answer matters.

## The trap it exists to beat: circularity

The hard part is not rigor — it is that **the thing judging the contract is usually the same kind of thing the contract governs.** A Claude-applied bar, judged by Claude, on Claude-authored skills, "confirms" itself. Every move below is in service of escaping that. Be explicit about which layer of circularity each arm escapes (authorship, model, both) and which it does not.

## The playbook (eight moves)

1. **Pre-register and seal before any data.** Write the question, the arms, the gates, and what counts as pass / fail / inconclusive into a doc; commit it (the SHA is the proof predictions preceded the data). Then **no post-hoc rescue** — scope, gates, and keying are fixed at the seal. If you find yourself wanting to redefine "pass" after seeing results, the seal is doing its job; honor it.

2. **Single-variable differential.** Compare the contract ON vs OFF where the contract is the *only* difference (freeze both surfaces by commit, record SHA-256). An absolute "the bar found problems" run proves nothing — the baseline finds problems too. The unit of evidence is the **ON − OFF divergence**, never the ON-only output.

3. **Blind, hermetic, replicated.** Strip arm/intent tells: neutral filenames (`contract-1/2`, `cand-NN`), sealed arm and unblinding maps kept out of any shared/tmp path, judges blind to arm and to the intended answer. Run **≥3 reps** per cell; escalate on a 2–1 split. Verify the *produced artifact* for leaks, not just the source (a shuffle can introduce a fresh same-category leak).

4. **Cross-model de-biasing.** Add an off-model checker or adversary (here: Codex/gpt-5.5) so the result is not Claude-grading-Claude. Cross-model is the *de-biasing* role — distinct from running the other model *as the experiment's reviewer*, which is a separate, optional portability arm.

5. **Human cold-judge as the correctness anchor — under the blinding guard.** Only a fresh human escapes *both* authorship and model, so a human arm is the one thing that can show the contract's calls are *correct*, not merely *different*. Administer a neutral packet (the contract's own vocabulary never appears) to a judge who has **not** seen apparatus state — and never leak reviewer/score/intermediate results to a current or potential judge until their judgment is recorded (`AGENTS.md` `## Blind Evaluations`; lost blinding is unrecoverable). Humans are expensive and usually n=1 — spend the arm where it adjudicates a real divergence, not on confirmation.

6. **Pilot before you seal.** A cheap **unsealed** pilot must show the falsification channel can actually *fire* before you spend a sealed run. Measure the base rates the gate depends on (does the baseline ever do the thing your gate keys on?). If the channel is empty in pilot, the gate is unfalsifiable — fix the design or drop that arm to characterization-only. An empty pilot can **close the question honestly without a sealed run at all** (that is exactly how the test-5 leniency arm closed).

7. **Adversarial design panel on the prereg.** Before sealing, have independent reviewers attack the *design*: is any verdict pre-ordained? is a gate unreachable? is a divergence cell forbidden by construction? is the motivating premise even true? (In test 5 v2 a panel caught that the whole approach rested on a **misattributed** prior result — the cut it relied on came from the contract arm, not the baseline.) Cheaper than discovering it after the run.

8. **Reasoning over label; accept the null.** Score the *reasoning*, not just the keep/cut label (a 3-way human scale read against a binary key is direction-robust, count-sensitive — report the range). And **accept a null honestly**: an empty or inconclusive channel is *not* a positive proof of the opposite. Bound the claim ("not constructible by any lever tried"), never launder it into "it never happens."

## The failure catalog (traps that wasted real runs)

- **Wrong-disposition keying.** v1 keyed leniency on *CUT*, a disposition opus reviewers almost never emit for an embedded choice (they RESHAPE). The channel read empty for a measurement reason, not a real one. *Fix:* key on the disposition the reviewer actually produces (change-vs-defend), and confirm it in pilot.
- **Single-family adversary / low genuinely-bad rate.** One model building all the specimens yields a corpus its own family won't even agree is bad (56% miss in v1). *Fix:* over-generate, cross-family + human **certify badness before** spending reviewer runs.
- **Pre-ordained or forbidden-by-construction gate.** A divergence cell that cannot occur given the contract's nature (e.g. asking the baseline to be *stricter* than a bar that is uniformly ≥ baseline). *Fix:* the design panel + the pilot.
- **Confounded gate promoted to a verdict.** Gating on a measure whose base rates are skewed by the very asymmetry you are studying. *Fix:* keep it descriptive, or de-confound and require off-model corroboration before any mandate.
- **Unescaped circularity sold as proof.** A clean result from same-model arms is consistent with robustness *and* with the judge sharing the contract's blind spot. *Fix:* say so; reserve strong claims for the human/off-model arms.
- **Laundered null.** "We couldn't make it fail" rewritten as "it never fails." *Fix:* move 8.

## Verdict vocabulary (so results stay comparable)

- **LOAD-BEARING** — the contract changes reviews/decisions vs OFF (non-inert).
- **CALIBRATED / net-protective** — ON does not over-cut vs a no-contract baseline (and may protect).
- **INCONCLUSIVE (W2)** — the falsification channel was empty / underpowered; no substantive verdict, and *not* a pass.
- **RESILIENT / not-constructible** — the attack found nothing across powered probes; claim bounded to the levers tried.
- **FALSIFIED** — the gate tripped; the contract has the defect; mandates a (separately scrutinized) fix.

## Worked case studies (the evidence base — read these for concrete templates)

| test | what it asked | method highlight | result | method lesson |
|------|---------------|------------------|--------|---------------|
| 3 differential | does the bar change reviews? | sealed ON/OFF, 77 agents | LOAD-BEARING (11/11 divergence) | single-variable differential beats an ON-only run |
| 1 foreign | does it over-cut unseen skills? | Codex evaluator, anonymized, form-vs-class diagonal | CALIBRATED / net-protective | cross-model de-biasing; de-circularize the answer key |
| 2 human | are its calls *correct*? | blind A–N packet, fresh human, verify the artifact | bar↔human 12/14 | the human cold-judge is the only both-escape anchor |
| 4 cut-then-use | is acting on a CUT safe? | seal → cut → 60 blind runs → cross-model score + tie-break | AT-LEAST-AS-GOOD | close the recommendation→action→verification loop |
| 5 red-team | can it be made lenient? | adversary + design panel + **pilot-before-seal** | not constructible (5 probes); closed at pilot | a pilot can close a channel without a sealed run |

Artifacts: `docs/plans/artifacts/judgment-trust-test{1..5}-*-2026-06-1{5,6,7}.md` (preregs, seals, results, pilots) and the master plan `docs/plans/2026-06-15-judgment-trust-apparatus.md`. Reusable harness templates (hermetic ON/OFF reviews, blind disposition, Codex scoring) live in the git-ignored `.agents/scratch/test{4,5,5v2-pilot}-run/` dirs.

## Honest limits of the method itself

- **It proves do-no-harm more easily than does-good.** "Not inert", "not lenient", "doesn't over-cut", "safe to act on" are reassurance; a positive *uplift* result (e.g. test 1's protective margin) is harder to get and tends to be small. Don't oversell a clean defensive sweep as a quality multiplier.
- **Circularity is only ever fully escaped by the human arm**, which is n=1, whole-packet, and expensive. Same-model arms dominate the evidence; weight the human/off-model arms accordingly.
- **Effect sizes are usually small.** A validated contract is most often a cheap guardrail removing a tail risk, not a dramatic average lift. State the magnitude, not just the direction.
- **The followership differential is blind to cognitive-offload.** For an *invoked* skill (summoned by a token like `/release-cut`), much of the value is that you never have to compose the careful guardrailed prompt under pressure — the skill *is* that pre-written prompt. The ON − OFF differential cannot price this: both arms carry the full body or lack it, so neither is the real-world baseline (*what a busy user actually types*), and a binary hazard outcome ignores the completeness and consistency of what gets delivered. A skill can read **MODEL-HANDLED** (its content does not move a strong model on the scored hazard) yet keep its full worth as a summonable, complete, repeatable procedure — so read MODEL-HANDLED on an invoked skill as *the reliability claim is moot*, never *the skill is valueless*. (An always-loaded rule has no invocation and no composition cost, so this limit is specific to invoked skills.)
- **The method's own value is high precisely because it is honest about all of the above** — its job is to stop you believing a contract is good (or bad) on circular evidence.
