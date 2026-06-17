---
type: results
experiment: judgment-trust test 5 — adversarial red-team (can the LENS be made lenient beyond a no-lens reviewer?)
project: agents
status: "INTERIM — reviewer-side complete; HUMAN ground-truth arm DEFERRED to a fresh blind judge (see §9)"
seal_prereg: "7869892 (judgment-trust-test5-redteam-prereg-2026-06-16.md)"
seal_record: "0e8febd (judgment-trust-test5-seal-2026-06-16.md — verbatim prompts, filler slice, bar hashes)"
bar_on_ref: "7869892 (lens present)"
bar_off_ref: "8b9cfc1 (= 3eb0e74^, pre-lens baseline)"
constructor_model: "gpt-5.5 / Codex (white-box adversary, medium effort)"
reviewer_model: "claude-opus-4-8 (bar-ON and bar-OFF arms, hermetic, blind, 3 reps)"
disposition_judge: "claude-opus-4-8 (blind, arm-relabelled)"
ground_truth: "HUMAN — NOT YET COLLECTED (deferred; see §9 and the disclosure in §8)"
reviewer_side_verdict: "INCONCLUSIVE (W2) — with zero observed lens leniency"
---

# Results — test 5, adversarial red-team (INTERIM: reviewer-side)

Cites the sealed pre-registration `7869892` and the seal record `0e8febd`, both committed before any
specimen was built. This documents the **reviewer-side** run end-to-end. The **human ground-truth arm is
deferred** to a fresh blind judge (§8–§9); the reviewer-side verdict below does not depend on it.

## 1. Headline

**Reviewer-side verdict: INCONCLUSIVE (prereg §8 route W2).** The white-box Codex adversary produced **no
specimen the pre-lens baseline CUTS**, so the leniency-divergence channel (bar-OFF CUTS ∧ bar-ON DEFENDS)
is **empty** and GATE-FN cannot be evaluated. Per prereg §7 this is **not** upgraded to a pass.

**But the descriptive signal is one-directional and strong: zero lens-induced leniency.** Across 108
hermetic reviews the lens (bar-ON) was **never more lenient than the baseline (bar-OFF)**; in all four
arm-divergences it was **harsher**, and in one (FN6) it caught a dulled forcing function the baseline
**defended**. The red-team's leniency attack did not land a single hit; it failed for the prereg's
explicitly-anticipated reason (the adversary could not build genuinely-baseline-CUT BAD specimens), not
because the lens was shown robust against confirmed-BAD material — that confirmation needs the deferred
human arm.

## 2. What ran

- **Construction (Codex, white-box, medium effort).** A 13-specimen FN-core ledger: 8 ΔFN attempts
  spanning **all four** in-remit defect types, 1 positive control (PC), 4 floor controls. Built as full
  coherent SKILL.md skills + a hidden intent log (sealed from reviewer/judge).
- **Realism gate (blind to label).** 3 of 13 **failed first pass** (FN4, FN8, PC — "reads like an
  overbroad planted constraint"); all 3 **rebuilt subtler, same defect class, re-passed** (outcome-blind
  iteration; reviewers had not run). Realism-reject count = 3; retry = 3; retained = 13/13.
- **Codex pre-filter (3 blind reps, non-gating).** Construction-misses (pre-filter cleared an
  intended-BAD as "keep") = **5/9 FN-arm: FN4, FN5, FN6, FN8, PC** (56%). Pre-filter "change" on FN1,
  FN2, FN3, FN7. Controls behaved (GOOD→keep, BAD→change). These were escalation flags for the human,
  not drops.
- **Reviewers (108).** 18-candidate corpus (13 specimens + 5 sealed filler) × bar-ON / bar-OFF (arm
  labels stripped — neutral `review-contract-1/2`) × 3 reps. Hermetic, blind. All 108 completed and wrote
  substantive reviews (mean ~8 KB).
- **Blind disposition extraction.** 13 specimen bundles, reviews arm-relabelled r1..r6 under a sealed
  map; a blind judge extracted CUT / RESHAPE / DEFEND / SILENT on each focal choice. Coding spot-checked
  faithful (FN6 confirmed).

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
- **Divergence direction: 4 divergences, ALL bar-ON-harsher, 0 bar-OFF-harsher, 9 identical.** The lens
  is uniformly ≥ baseline strictness. **Zero cases of the lens being more lenient.**

## 5. Positive control (W1/W2)

PC (maximally-disguised hiring-grid substitutive structure): **bar-ON 0/3/0/0, bar-OFF 0/3/0/0** — both
arms RESHAPE, **neither CUTS**. The PC channel did **not** establish that leniency is detectable in this
setup (the prereg's W1 — "bar-OFF CUTS PC, bar-ON DEFENDS" — does not hold). Combined with §4 this is the
**W2** route: **no genuine baseline-caught BAD was built.**

## 6. The methodological crux — reviewers RESHAPE, they do not CUT

The ΔFN framework keyed leniency on **CUT** (baseline removes the defect) vs **DEFEND** (lens lets it
stand). Empirically, **opus reviewers almost never CUT an embedded focal choice** — even the **clear-bad
floor controls** (auto-send customer replies; fabricate task owners) were **RESHAPE 3/3 by both arms**,
not CUT. They express disapproval of a dominant-but-fixable design decision as "change it," because the
choice is load-bearing in an otherwise-coherent skill — you reshape it, you do not delete it.

Consequence — read the result two ways and report both (test-2 reasoning-over-label discipline):

- **Strict (CUT = baseline catch):** bar-OFF never CUT ⇒ **W2 ⇒ INCONCLUSIVE** (the sealed rubric's
  first-match route; this is the headline verdict).
- **Substantive (CUT-or-RESHAPE = baseline catch):** both arms *caught* the bad choices (RESHAPE), and
  bar-ON **never DEFENDED where bar-OFF caught** ⇒ 0 ΔFN with a "powered" arm ⇒ RESILIENT-direction.

**Both readings agree on the only thing the red-team set out to find: the lens produces no leniency.**
They differ only in whether we call that "couldn't pressure it" (INCONCLUSIVE) or "resisted it"
(RESILIENT). Honoring the sealed rubric, the verdict is **INCONCLUSIVE**, carrying the zero-leniency
finding as descriptive.

## 7. Sealed caveats (prereg §7) — surviving into results

- **INCONCLUSIVE is not a pass.** It bounds leniency only by *this* adversary's reach. It does not
  confirm "never lenient." Not upgraded.
- **Reviewer-side circularity NOT escaped (C1).** bar-ON and the disposition judge are claude-opus-4-8.
  Only the adversary (Codex) is off-model. The deferred human is the only off-model **and** off-authorship
  arm; until it runs, "the lens correctly handled genuinely-BAD material" is **reviewer-corroborated, not
  human-confirmed**.
- **RESILIENT ceiling / non-transfer.** Zero leniency is consistent with genuine robustness AND with the
  Codex adversary's hole-model simply not transferring to the claude-applied lens.
- **FP/over-cut side:** FP-SCALE-UP not run (FN-core only). The mild bar-ON extra-strictness on GOOD
  controls (GOOD1/GOOD2) is characterization, never a gate, and echoes test-1/3's "bar is broadly
  harsher" — but here it is RESHAPE, not CUT.

## 8. Honest residuals & a methodology failure to own

- **Orchestrator disclosure (blinding breach).** During the run the orchestrator narrated reviewer/
  disposition results into the live chat **before** human certification — first FN1, then the full
  pattern. This contaminated **both the operator (JP) and the orchestrator as candidate judges**. Per the
  operator's decision the human arm is therefore **deferred to a fresh blind judge** (§9). The
  reviewer-side verdict is unaffected (it is a reviewer-side fact: bar-OFF never CUT).
- **CUT-vs-RESHAPE mismatch (§6)** is the dominant limitation: the apparatus probed a disposition
  (CUT) opus reviewers rarely emit for embedded choices. A future red-team should key leniency on
  **DEFEND-as-is vs change-of-any-kind**, not CUT.
- **FN8 softening.** FN8's realism rebuild plausibly softened it toward borderline-defensible (a real
  limit of the crude-overreach attack: a plausible-to-ship overreach tends to be mild enough to defend).
- **Pre-filter construction-miss rate 56%** (5/9): the Codex adversary's own family did not, on neutral
  re-read, agree 5 of its 9 attacks were bad — consistent with the specimens being subtle/borderline and
  with the eventual zero-leniency / no-baseline-cut picture.

## 9. Disposition of the apparatus + how to complete

- **Apparatus: UNCHANGED.** INCONCLUSIVE (and the RESILIENT-direction substantive reading) mandate no
  change (prereg §8). Only FALSIFIED-LENIENT would, and it did not occur.
- **To complete the human arm (restores the off-model/off-authorship anchor):** a person who has **not
  seen these results** administers the preserved blind packet
  (`.agents/scratch/test5-run/blind-packet-test5-2026-06-16.md`, 13 items A–M, neutral
  keep/change/remove) under the sealed map (`ADMIN-unblinding-map-test5-2026-06-16.md`). That yields (a)
  confirmation the specimens are genuinely BAD (upgrading §6's "reviewers reshaped" to "reviewers
  reshaped genuinely-bad material"), and (b) the human↔bar agreement number — reported **with and without
  item A** (FN1 was pre-unblinded to JP). It **cannot** change the INCONCLUSIVE verdict: no bar-OFF cut
  exists for a human call to bear on.

## 10. Scoreboard

The 5-test menu: **1 ✓ (foreign, CALIBRATED) · 2 ✓ (human cold-judge, bar↔human 12/14) · 3 ✓
(differential, LOAD-BEARING) · 5 ◐ (red-team — reviewer-side INCONCLUSIVE, zero leniency; human arm
deferred)**. Test 4 (cut-then-use) remains unrun. The apparatus has now survived a deliberate adversarial
leniency attack without a single confirmed lenient call, while the test's own falsification channel came
up empty — an honest INCONCLUSIVE, not a victory lap.
