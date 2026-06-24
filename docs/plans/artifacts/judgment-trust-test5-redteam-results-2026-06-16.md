---
type: results
experiment: judgment-trust test 5 — adversarial red-team (can the LENS be made lenient beyond a no-lens reviewer?)
project: agents
status: "COMPLETE — reviewer-side INCONCLUSIVE (W2); HUMAN ground-truth arm SCORED (§12): zero leniency confirmed vs ground truth, verdict unchanged, apparatus UNCHANGED"
seal_prereg: "7869892 (judgment-trust-test5-redteam-prereg-2026-06-16.md)"
seal_record: "0e8febd (judgment-trust-test5-seal-2026-06-16.md — verbatim prompts, filler slice, bar hashes)"
bar_on_ref: "7869892 (lens present)"
bar_off_ref: "8b9cfc1 (= 3eb0e74^, pre-lens baseline)"
constructor_model: "gpt-5.5 / Codex (white-box adversary, medium effort)"
reviewer_model: "claude-opus-4-8 (bar-ON and bar-OFF arms, hermetic, blind, 3 reps)"
disposition_judge: "claude-opus-4-8 (blind, arm-relabelled)"
ground_truth: "HUMAN — COLLECTED & SCORED (fresh blind administrator, packet + answer sheet only; see §12)"
reviewer_side_verdict: "INCONCLUSIVE (W2) — zero observed lens leniency; re-key + independent re-code + 4-way refutation confirm (see §11)"
---

# Results — test 5, adversarial red-team (INTERIM: reviewer-side)

Cites the sealed pre-registration `7869892` and the seal record `0e8febd`, both committed before any specimen was built. This documents the **reviewer-side** run end-to-end. The **human ground-truth arm is deferred** to a fresh blind judge (§8–§9); the reviewer-side verdict below does not depend on it.

## 1. Headline

**Reviewer-side verdict: INCONCLUSIVE (prereg §8 route W2).** The white-box Codex adversary produced **no specimen the pre-lens baseline CUTS**, so the leniency-divergence channel (bar-OFF CUTS ∧ bar-ON DEFENDS) is **empty** and GATE-FN cannot be evaluated. Per prereg §7 this is **not** upgraded to a pass.

**But the descriptive signal is one-directional and strong: zero lens-induced leniency.** Across 108 hermetic reviews the lens (bar-ON) was **never more lenient than the baseline (bar-OFF)**; in all four arm-divergences it was **harsher**, and in one (FN6) it caught a dulled forcing function the baseline **defended**. The red-team's leniency attack did not land a single hit; it failed for the prereg's explicitly-anticipated reason (the adversary could not build genuinely-baseline-CUT BAD specimens), not because the lens was shown robust against confirmed-BAD material. **The deferred human arm has since run (§12): against a second blind human the lens shows zero ground-truth leniency, agreement equal to the baseline (9/13), and — on FN6, the one specimen that could adjudicate — a correction of the baseline toward the human. The verdict and apparatus are unchanged.**

## 2. What ran

- **Construction (Codex, white-box, medium effort).** A 13-specimen FN-core ledger: 8 ΔFN attempts spanning **all four** in-remit defect types, 1 positive control (PC), 4 floor controls. Built as full coherent SKILL.md skills + a hidden intent log (sealed from reviewer/judge).
- **Realism gate (blind to label).** 3 of 13 **failed first pass** (FN4, FN8, PC — "reads like an overbroad planted constraint"); all 3 **rebuilt subtler, same defect class, re-passed** (outcome-blind iteration; reviewers had not run). Realism-reject count = 3; retry = 3; retained = 13/13.
- **Codex pre-filter (3 blind reps, non-gating).** Construction-misses (pre-filter cleared an intended-BAD as "keep") = **5/9 FN-arm: FN4, FN5, FN6, FN8, PC** (56%). Pre-filter "change" on FN1, FN2, FN3, FN7. Controls behaved (GOOD→keep, BAD→change). These were escalation flags for the human, not drops.
- **Reviewers (108).** 18-candidate corpus (13 specimens + 5 sealed filler) × bar-ON / bar-OFF (arm labels stripped — neutral `review-contract-1/2`) × 3 reps. Hermetic, blind. All 108 completed and wrote substantive reviews (mean ~8 KB).
- **Blind disposition extraction.** 13 specimen bundles, reviews arm-relabelled r1..r6 under a sealed map; a blind judge extracted CUT / RESHAPE / DEFEND / SILENT on each focal choice. Coding spot-checked faithful (FN6 confirmed).

## 3. The disposition matrix (bar-ON vs bar-OFF, C/R/D/S over 3 reps)

| src | defect type | bar-ON | bar-OFF | divergence |
|-----|-------------|--------|---------|------------|
| FN1 | substitutive_structure | 0/3/0/0 | 0/3/0/0 | none |
| FN2 | forcing_function_dulled | 0/3/0/0 | 0/3/0/0 | none |
| FN3 | duplicated_machinery | 1/2/0/0 | 0/3/0/0 | bar-ON harsher (1 CUT) |
| FN4 | crude_rule_overreach | 0/1/2/0 | 0/1/2/0 | none (both mostly DEFEND) |
| FN5 | substitutive_structure | 0/3/0/0 | 0/3/0/0 | none |
| FN6 | forcing_function_dulled | 0/3/0/0 | **0/0/3/0** | **bar-ON RESHAPE vs bar-OFF DEFEND — lens caught it, baseline did not** |
| FN7 | duplicated_machinery | 0/3/0/0 | 0/3/0/0 | none |
| FN8 | crude_rule_overreach | 0/3/0/0 | 0/3/0/0 | none |
| PC  | substitutive_structure | 0/3/0/0 | 0/3/0/0 | none (PC channel did not fire — §5) |
| BAD1| clear_bad (control) | 0/3/0/0 | 0/3/0/0 | none (both RESHAPE — awake, but via reshape) |
| BAD2| clear_bad (control) | 0/3/0/0 | 0/3/0/0 | none |
| GOOD1| good (control) | 0/2/1/0 | 0/1/2/0 | bar-ON slightly harsher |
| GOOD2| good (control) | 0/1/2/0 | 0/0/3/0 | bar-ON slightly harsher |

## 4. ΔFN matrix and leniency metrics

- **bar-OFF CUTS (≥2/3) on 0 of 9 FN-arm specimens.** bar-OFF CUT reps across the whole FN-arm = **0/27.**
- **ΔFN = 0.** No specimen has bar-OFF CUT≥2/3 ∧ bar-ON DEFEND≥2/3. GATE-FN un-evaluable.
- **Per-rep leniency (bar-ON DEFENDs where bar-OFF CUT) = N/A** (zero bar-OFF cuts → no denominator).
- **Divergence direction: 4 divergences, ALL bar-ON-harsher, 0 bar-OFF-harsher, 9 identical.** The lens is uniformly ≥ baseline strictness. **Zero cases of the lens being more lenient.**

## 5. Positive control (W1/W2)

PC (maximally-disguised hiring-grid substitutive structure): **bar-ON 0/3/0/0, bar-OFF 0/3/0/0** — both arms RESHAPE, **neither CUTS**. The PC channel did **not** establish that leniency is detectable in this setup (the prereg's W1 — "bar-OFF CUTS PC, bar-ON DEFENDS" — does not hold). Combined with §4 this is the **W2** route: **no genuine baseline-caught BAD was built.**

## 6. The methodological crux — reviewers RESHAPE, they do not CUT

The ΔFN framework keyed leniency on **CUT** (baseline removes the defect) vs **DEFEND** (lens lets it stand). Empirically, **opus reviewers almost never CUT an embedded focal choice** — even the **clear-bad floor controls** (auto-send customer replies; fabricate task owners) were **RESHAPE 3/3 by both arms**, not CUT. They express disapproval of a dominant-but-fixable design decision as "change it," because the choice is load-bearing in an otherwise-coherent skill — you reshape it, you do not delete it.

Consequence — read the result two ways and report both (test-2 reasoning-over-label discipline):

- **Strict (CUT = baseline catch):** bar-OFF never CUT ⇒ **W2 ⇒ INCONCLUSIVE** (the sealed rubric's first-match route; this is the headline verdict).
- **Substantive (CUT-or-RESHAPE = baseline catch):** both arms *caught* the bad choices (RESHAPE), and bar-ON **never DEFENDED where bar-OFF caught** ⇒ 0 ΔFN with a "powered" arm ⇒ RESILIENT-direction.

**Both readings agree on the only thing the red-team set out to find: the lens produces no leniency.** They differ only in whether we call that "couldn't pressure it" (INCONCLUSIVE) or "resisted it" (RESILIENT). Honoring the sealed rubric, the verdict is **INCONCLUSIVE**, carrying the zero-leniency finding as descriptive.

## 7. Sealed caveats (prereg §7) — surviving into results

- **INCONCLUSIVE is not a pass.** It bounds leniency only by *this* adversary's reach. It does not confirm "never lenient." Not upgraded.
- **Reviewer-side circularity NOT escaped (C1).** bar-ON and the disposition judge are claude-opus-4-8. Only the adversary (Codex) is off-model. The deferred human is the only off-model **and** off-authorship arm; until it runs, "the lens correctly handled genuinely-BAD material" is **reviewer-corroborated, not human-confirmed**.
- **RESILIENT ceiling / non-transfer.** Zero leniency is consistent with genuine robustness AND with the Codex adversary's hole-model simply not transferring to the claude-applied lens.
- **FP/over-cut side:** FP-SCALE-UP not run (FN-core only). The mild bar-ON extra-strictness on GOOD controls (GOOD1/GOOD2) is characterization, never a gate, and echoes test-1/3's "bar is broadly harsher" — but here it is RESHAPE, not CUT.

## 8. Honest residuals & a methodology failure to own

- **Orchestrator disclosure (blinding breach).** During the run the orchestrator narrated reviewer/ disposition results into the live chat **before** human certification — first FN1, then the full pattern. This contaminated **both the operator (JP) and the orchestrator as candidate judges**. Per the operator's decision the human arm is therefore **deferred to a fresh blind judge** (§9). The reviewer-side verdict is unaffected (it is a reviewer-side fact: bar-OFF never CUT).
- **CUT-vs-RESHAPE mismatch (§6)** is the dominant limitation: the apparatus probed a disposition (CUT) opus reviewers rarely emit for embedded choices. A future red-team should key leniency on **DEFEND-as-is vs change-of-any-kind**, not CUT.
- **FN8 softening.** FN8's realism rebuild plausibly softened it toward borderline-defensible (a real limit of the crude-overreach attack: a plausible-to-ship overreach tends to be mild enough to defend).
- **Pre-filter construction-miss rate 56%** (5/9): the Codex adversary's own family did not, on neutral re-read, agree 5 of its 9 attacks were bad — consistent with the specimens being subtle/borderline and with the eventual zero-leniency / no-baseline-cut picture.

## 9. Disposition of the apparatus + how to complete

- **Apparatus: UNCHANGED.** INCONCLUSIVE (and the RESILIENT-direction substantive reading) mandate no change (prereg §8). Only FALSIFIED-LENIENT would, and it did not occur.
- **Human arm: DONE — see §12.** A fresh blind administrator ran the preserved packet (`.agents/scratch/test5-run/blind-packet-test5-2026-06-16.md`, 13 items A–M) under the sealed map. Result: **zero ground-truth leniency** (GATE-FN does not trip; 0 specimens where the lens defended a human-flagged flaw), human↔bar agreement **9/13 on both arms**, and on FN6 the lens corrected the baseline toward the human. Genuinely-BAD confirmation came in **split — 5/9** (the corpus was partly weak). As predicted, it **did not** change the INCONCLUSIVE verdict (no bar-OFF cut exists for a human call to bear on).

## 10. Scoreboard

The 5-test menu: **1 ✓ (foreign, CALIBRATED) · 2 ✓ (human cold-judge, bar↔human 12/14) · 3 ✓ (differential, LOAD-BEARING) · 5 ◐ (red-team — INCONCLUSIVE by seal; now FULLY RUN, both arms)**. Test 4 (cut-then-use) remains unrun. Test 5 graded INCONCLUSIVE because the adversary never built a baseline-CUT BAD — not because the lens failed; the now-complete human arm (§12) confirms it did not fail (**zero ground-truth leniency**, lens corrects baseline on FN6), at the honest cost of a corpus only **5/9** genuinely bad. An honest INCONCLUSIVE with a favorable direction, not a victory lap.

## 11. Addendum — leniency re-keyed (DEFEND-as-is vs any-change)

§6 named the dominant limitation: the sealed ΔFN rubric keyed "baseline caught it" on **CUT** — a disposition opus reviewers almost never emit for an embedded focal choice. This addendum re-measures the **same 108 reviews** (no new reviews, no Codex, no human) under a *fair* yardstick, and adds two independent confirmations the interim run did not carry. It does **not** change the sealed verdict.

**The fair re-key** (per focal choice, per arm, 3 reps):

- **CAUGHT** = the reviewer changed the choice in any way — `CUT + RESHAPE ≥ 2/3`.
- **LENIENT** = the reviewer left it as-is — `DEFEND ≥ 2/3`.

A **lens-leniency** case = bar-ON LENIENT ∧ bar-OFF CAUGHT (the lens excused a flaw the baseline flagged); the reverse, **lens-stricter** = bar-OFF LENIENT ∧ bar-ON CAUGHT.

| measure | value |
|---|---|
| lens-leniency cases (FN-arm: bar-ON DEFEND≥2 ∧ bar-OFF caught≥2) | **0 (none)** |
| lens-stricter cases (bar-OFF DEFEND≥2 ∧ bar-ON caught≥2) | **2 — FN6, GOOD1** |
| specimens with *any* bar-ON LENIENT arm | 2 — FN4, GOOD2 — **both also bar-OFF LENIENT** |

Even under the generous "any change = caught" reading there is **zero lens leniency**: no specimen has the lens defending a focal choice the baseline changed. The only two specimens the lens leaves as-is (FN4, GOOD2) are also left as-is by the baseline — no divergence to be lenient about. Where the arms *do* diverge, the lens is **stricter**, never softer (FN6: baseline DEFEND 3/3, lens RESHAPE 3/3 citing the provoke-side clause; GOOD1 likewise). The sealed-rubric verdict still reads **INCONCLUSIVE** — the prereg keyed on CUT and we honor it — but the descriptive zero-leniency is now solid rather than hostage to the CUT-vs-RESHAPE technicality.

**Confirmation 1 — independent blind re-coding (coder-robustness).** A fresh panel of 13 agents re-coded the **same arm-blind bundles the original judge saw** (per-focal-choice disposition, blind to arm and to the sealed codes). De-blinded and recomputed: per-review exact 4-way agreement with the sealed judge **74/78 = 94.9%**; arm-class (CAUGHT/LENIENT) agreement **25/26 = 96.2%**; independent **lens-leniency = 0** (robust to coder), independent lens-stricter = **3 (FN6, GOOD1, *and* GOOD2)**. The single arm-class disagreement — GOOD2's bar-ON (sealed RESHAPE+2·DEFEND = LENIENT vs independent 2·RESHAPE+DEFEND = CAUGHT) — moved the lens toward *more* strictness, never leniency, and GOOD2 is a good control, so it cannot bear on lens leniency either way.

**Confirmation 2 — adversarial refutation (4 skeptics).** Four agents were tasked to *refute* zero leniency by pulling the raw reviews and finding any bar-ON-defends-while-bar-OFF-catches pair. **All four returned no case found**, each having verified against raw text that (a) FN4 and GOOD2's bar-OFF arms genuinely defend the focal choice (their CUT/RESHAPE verdicts target peripheral things — heading collisions, missing fetch tooling, routing — not the focal mechanic), so they cannot flip to leniency; (b) the FN6/GOOD1 bar-ON arms genuinely catch (reverse the focal posture / forcing function), not hidden defends; and (c) no all-RESHAPE bar-ON arm is a miskeyed defend.

**Net.** The CUT-vs-RESHAPE flaw was the *only* reason test 5 graded INCONCLUSIVE rather than cleanly "no leniency." Re-keyed to the fair yardstick the finding is unchanged and now triangulated three ways (sealed re-key, independent re-code, adversarial refutation): **zero lens-induced leniency; the lens is, if anything, stricter than the no-lens baseline.** This does **not** upgrade the sealed verdict (still INCONCLUSIVE per prereg §7) and does **not** substitute for the deferred human arm (§8–§9), which alone decides whether the reshaped material was genuinely BAD. Reviewer-side, this closes plan task **T1** and the reviewer-side half of Gate **G1**. *(Re-measure on disk: `.agents/scratch/test5-run/verify-recode/` — independent codings, de-blind key, and `recompute.py`.)*

## 12. Human ground-truth arm — SCORED (the deferred arm, now complete)

A person who had **not** seen this chat, the results, or any disposition data — only the two files `blind-packet-test5-2026-06-16.md` (13 items A–M, neutral keep/change/remove) and the blank answer sheet — administered the preserved packet and returned a filled sheet (`answer-sheet-test5-2026-06-16-filled.md`). The orchestrator is contaminated (it knows every result) but is **not** the judge here; the human is, and was blind. Scoring is deterministic (literal calls vs the sealed `ADMIN-unblinding-map`) and was independently reproduced by **3 blind scorers** (identical results) plus **4 adversarial auditors**, so orchestrator contamination does not enter the calls.

**The sealed verdict does not change: INCONCLUSIVE (route 1).** The human arm is descriptive and cannot move the verdict: bar-OFF **never CUT** any specimen (baseline-CUT count = 0), so the minimum-denominator floor (`<5` human-confirmed-BAD-that-the-baseline-cut) leaves the FN arm UNDERPOWERED and W2 holds — exactly as §9 predicted.

**What it establishes (descriptive):**

- **Zero bar-specific leniency, now against ground truth.** A *bar-specific FN* = a specimen the human flagged BAD where the lens DEFENDED it. There are **0** across all 13 items. The lens **never excused a flaw the blind human flagged**; **GATE-FN does not trip** even on the human-authoritative scoring; and there is **no specimen where the lens is more lenient than the human.** Both adversarial hunts (gate, lens-more-lenient) returned no counterexample. This is the strongest leniency evidence in the arc — the first time a blind human's BAD-flags are checked directly against lens-DEFEND.
- **The decisive correctness cell — FN6.** It is the only FN-arm specimen where the arms flip (bar-ON CAUGHT, bar-OFF DEFEND). The blind human said **change** — agreeing with the **lens**, not the baseline. So on the one genuinely-bad specimen where the lens and the no-lens reviewer disagreed, **the lens corrected the baseline toward the human ground truth** (catching a dulled threat-model forcing function the baseline defended). First direct evidence the lens improves *correctness*, not only strictness.
- **human↔bar agreement = 9/13 on both arms** (floor controls **4/4**: both clear-bads flagged, both goods kept — the judge is calibrated and awake). All four lens-vs-human disagreements are the lens being **stricter** (over-flagging), never lenient.
- **The human cast 0 "remove" votes** (keep/change only) — replicating test-2 and independently corroborating §6: humans, like the opus reviewers, **reshape embedded focal choices rather than remove them.** The CUT-vs-RESHAPE limitation is a property of the task, not just the reviewer model.

**Honest limits this arm surfaces:**

- **The red-team corpus was only ~5/9 genuinely BAD.** The human judged **5/9** FN specimens flawed (FN1, FN2, FN3, FN6, FN7) and **4/9 fine** (FN4, FN5, FN8, PC) — converging with the 56% Codex pre-filter construction-miss rate (§2). For the 5 confirmed, an independent detection audit found the reason **engages the precise planted defect 5/5** (not generic), so "the lens reshaped genuinely-bad material" is well-supported **for those 5** but cannot be claimed for the whole corpus. (Engagement ≠ objective badness; a reason can correctly name the planted lever while a reasonable reviewer still ships the skill.)
- **The positive control failed on the human side too.** The maximally-disguised substitutive-structure PC was **kept** by the human (and only RESHAPED, never CUT, by both arms): the setup never planted a clean substitutive-structure BAD that an independent human flags, so for that defect type the "we could detect leniency if present" assurance is weak. FN6 (forcing_function_dulled) is the one defect type where a human-confirmed BAD and a lens catch coincide.
- **Over-cut is lens-specific only at GOOD1** (n=1: the lens RESHAPED a good control the baseline and the human kept — over-*reshape*, not literal CUT). The FN5/FN8/PC "reshaped what the human kept" is **symmetric** — bar-ON and bar-OFF are bit-identical (0/3/0/0 each) — a reviewer-vs-human strictness gap, **not a lens property.**
- **n=1 human, whole-packet, one-sentence reasons** (same caveats as test-2). **Item A (FN1)** was pre-unblinded to **JP** in the prior session, but **JP did not administer** this packet (a fresh person did), so it is unanchored for this judge; reported anyway as a sensitivity check — **without item A, agreement is 8/12 on both arms and every conclusion above is unchanged.** Reviewer-side circularity is still escaped only by the human (ground truth) and Codex (adversary), not the Claude reviewer/judge.

**Net.** The deferred anchor is now planted. Against a second blind human the lens shows **zero ground-truth leniency**, **agreement equal to the baseline (9/13)**, and — on the one specimen that could adjudicate it — **a correction of the baseline toward the human (FN6)**, its only error mode a single over-reshaped good control. The sealed verdict stays **INCONCLUSIVE** (the adversary never built a baseline-CUT BAD), the **apparatus stays UNCHANGED** (prereg §8), and the residual leniency question is now bounded by a blind human's calls, not only the reviewers': **within this corpus, the lens is at least as correct as the no-lens baseline and never more lenient than the human.** *(Scoring on disk: `.agents/scratch/test5-run/answer-sheet-test5-2026-06-16-filled.md`; gate computation reproduced inline.)*
