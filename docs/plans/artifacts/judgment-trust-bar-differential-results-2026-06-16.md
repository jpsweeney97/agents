---
type: experiment-results
experiment: judgment-trust bar-on/bar-off differential
project: agents
date: 2026-06-16
sealed_prereg: ee7c3bd (docs/plans/artifacts/judgment-trust-bar-differential-prereg-2026-06-16.md)
bar_on_ref: main @ 87da163 (review-family 0.3.10)
bar_off_ref: 3eb0e74^ (8b9cfc1 — pre-lens single-variable baseline)
workflow_run: wf_c2317bb2-4e1 (77 agents: 66 reviewers + 11 blind judges; 2.75M tokens)
---

# Results — judgment-vs-trust bar differential (test 3 of 5)

## Verdict (one line)

**LOAD-BEARING, decisively — and broader than its own design story.** The bar is **not** inert decoration (the cheapest falsification test is passed). But its effect is not the narrow "drop conformance on judgment skills" I pre-registered: it overlays a per-part judgment/trust **classification + vocabulary on every review** (11/11 targets diverged systematically, controls included), which is *mostly* correct in direction (suppresses trust-shape complaints on judgment skills, defends fixed structure on trust skills, applies trust failure-modes) **but mis-calibrated toward over-cutting organizing structure on two judgment skills and leaks anti-conformance leniency onto at least one trust skill.** It also **falsifies the follow-on (1) sub-narrative**: a fresh reviewer under the bar flags `system-design-review`'s finding-cap as *substitutive* (→ cut), contradicting the human KEEP. The "near-zero cuts" outcome was a property of the human adjudication, not of the bar.

Rubric mapping: not INERT; not cleanly LOAD-BEARING+CORRECT (controls moved, divergence not concentrated); not cleanly LOAD-BEARING+WRONG (direction is right where it counts). The honest call is a fourth box the rubric didn't anticipate: **LOAD-BEARING + BROADER THAN DESIGNED + MOSTLY-CORRECT-DIRECTION + PROVOKE-SIDE CALIBRATION RISK.**

## Integrity controls (held)

- **Pre-registration sealed at `ee7c3bd` BEFORE any run.** Predictions below are scored against that sealed file, not back-fitted.
- **Single variable confirmed:** bar-on vs bar-off differ only by the lens apparatus (staging sanity: 1 vs 0 "Two Kinds of Skill"; 25 vs 4 "judgment"). Baseline `3eb0e74^` is the true pre-lens commit.
- **Hermetic + fenced:** both configs reviewed identical frozen target snapshots from `/tmp/bar-differential/`; reviewers fenced from the live tree and `docs/plans/`.
- **Blind scoring:** 6 paired reviews per target relabeled A/B (random by index parity, mapping hidden from the judge); judge detected systematic A-vs-B difference and its direction in neutral structural-vs-substance terms, never told which group was the bar. Unblinded only at analysis via the retained mapping.
- **`review-reviewer` is EXPLORATORY** (staged but inadvertently omitted from the sealed prereg table) — reported, excluded from confirmatory counts.
- n = 3 reps per cell (66 reviews) + 11 blind judges.

## Per-target results (unblinded)

Δcount = mean(bar-on findings) − mean(bar-off findings). "Structural-leaner" = which config the blind judge said raises more structural/output-shape/conformance findings.

| # | Target | Bucket | Sealed prediction | Blind: systematic? | Δcount (on−off) | Structural-leaner (real) | Scorecard |
|---|--------|--------|-------------------|--------------------|-----------------|--------------------------|-----------|
| 1 | system-design-review | PD | DIVERGE **HIGH**, OFF raises cap / ON drops | yes (med) | **+2.3** | **bar-ON** | **DIRECTION FLIPPED** — ON escalates cap as "substitutive / strangles thinking" 3/3; OFF calls caps "defensible soft bounds" |
| 2 | tdd | PD | DIVERGE mod, OFF raises missing-shape / ON drops | yes (**high**) | −2.3 | bar-OFF | **MATCH** — OFF raises "missing closure/output-shape" 3/3, ON 0/3; ON applies trust-bar to the loop |
| 3 | scrutinize | PD | DIVERGE mod-low, OFF raises section/token conformance | yes (med) | +0.3 | bar-OFF | **PARTIAL** — OFF raises severity-location + reference-file findings 3/3; ON raises the "9 mandated sections → fill-to-feel-done" finding |
| 4 | diagnose | PD | DIVERGE low-mod, OFF raises missing-shape / ON drops | yes (**high**) | +0.7 | bar-OFF | **MATCH** — OFF raises "no output shape" 3/3 + stricter verdict; ON defends phased structure, 2/3 Defensible |
| 5 | making-recommendations | PD | DIVERGE **uncertain**: ON may ADD substitutive-structure finding | yes (**high**) | −0.7 | bar-ON | **MATCH (over-cut branch)** — ON flags 8-section packet + machinery volume as "substitutive / performing the contract" 3/3; OFF never flags the packet |
| 6 | merge-branch | NC | **NO divergence** | yes (med) | −0.3 | bar-OFF | **MISS (control moved)** — ON goes 2/3 **Defensible** citing "conformance over-flagging the bar warns against" → leniency leak onto a trust skill |
| 7 | to-issues | NC | NO/minimal | yes (**high**) | +0.3 | bar-OFF | **MISS (but mixed)** — ON rates the partial-publish gap **High** 3/3 (OFF Medium 3/3) + judgment/trust framing; OFF raises section-conformance placeholders |
| 8 | git-hygiene | NC | **NO divergence** | yes (med) | +0.3 | bar-OFF | **MISS (control moved, bar correct)** — ON affirms fixed Decision Summary as "the value for a trust skill, not over-ruling" 3/3; OFF flags mode/lane counts + fixed structure |
| 9 | gh-pr-review-loop | MX | NO/low | yes (med) | −2.0 | bar-OFF | **MISS (mixed shows signature)** — OFF flags "structural-only proof / no dry run" 3/3 + caps higher; ON defends proof-deferral, 1 Defensible |
| 10 | acceptance-map | MX | NO/low (over-cut watch) | yes (med) | −1.3 | bar-ON | **PARTIAL** — ON applies the trust failure-mode lens ("copied-not-single-sourced / drift", "crude-rule overreach") 3/3; defensible, not over-cut |
| 11 | review-reviewer | PD (exploratory) | — | yes (med) | +0.7 | bar-OFF | ON defends heavy packets as "load-bearing, not substitutive" + lens vocabulary; OFF flags ceremony weight, machinery counts, "no default packet" (High) |

## What the bar actually does (the mechanism, corrected)

1. **It applies a per-part judgment/trust classification + vocabulary to *every* review.** Bar-ON reviews are trivially distinguishable by eye — "substitutive structure," "provoke half passes," "judgment part vs trust part," "crude-rule overreach," "single-sourced vs copied machinery." This overlay is present in 11/11 targets and is why the blind judge found systematic divergence even on trust controls. (Corollary: the blinding is procedurally clean but *imperfect* — the bar-ON style self-identifies. That very fact is the strongest possible LOAD-BEARING evidence: you don't need statistics to tell the groups apart.)

2. **Finding-COUNT divergence, by contrast, is concentrated** (|Δ|≥1.3 on only 4 targets: system-design-review +2.3, tdd −2.3, gh-pr-review-loop −2.0, acceptance-map −1.3). The other 7 are count-ties whose "systematic" call rests on framing/vocabulary, not on which findings were raised. So: **vocabulary/classification effect = universal; substantive finding-set effect = concentrated.**

3. **Direction, where it is substantive, is mostly the designed one:**
   - *Suppresses trust-shape complaints on judgment skills* — tdd (no "missing output shape," 0/3 vs 3/3), diagnose (defends phased structure, no missing-shape finding).
   - *Defends fixed structure on trust skills* — git-hygiene ("fixed output shape is the value, not over-ruling," 3/3).
   - *Applies trust failure-modes* — acceptance-map (frames commit machinery as "copied-not-single-sourced / drift," the exact trust-skill defect the bar names).
   - *Escalates real substance on a mixed skill* — to-issues (partial-publish gap High vs Medium).

4. **The provoke side over-fires on organizing structure (the calibration risk):**
   - **system-design-review** — bar-ON frames the finding-cap as "substitutive machinery that strangles thinking" (→ cut) 3/3; bar-OFF calls it "defensible soft bounds." This **contradicts follow-on (1)'s human KEEP** (the cap as a forcing function).
   - **making-recommendations** — bar-ON flags the stakes-scaled 8-section packet as "substitutive structure / performing the contract" (→ cut) 3/3; bar-OFF never flags it. A cut the library has not made.

5. **One anti-conformance leniency leak onto a trust skill:** merge-branch bar-ON reached "Defensible" 2/3 citing "holding the firm rules against it would be the conformance over-flagging the bar warns against" — applying a judgment-skill anti-conformance posture to a skill whose firm rules ARE the value. Mild, but it is the bar leaking in the wrong direction.

## Prediction scorecard (honest)

- **A1 (divergence concentrates in PD rows; controls inert): WRONG.** Divergence was universal (11/11). There are no true controls — the bar reframes every review. This is my biggest miss and the most important correction.
- **A2 (verdicts stable; divergence at finding level): CORRECT.** Verdicts were near- identical; the only wobble is bar-ON's slightly-more-frequent "Defensible" on diagnose / merge-branch / gh-pr-review-loop. All substantive divergence is sub-verdict.
- **A3 (system-design-review is the cleanest signal): half-right.** Strong signal, but the **direction flipped** — bar-ON is the more structural/aggressive reviewer there, not bar-OFF.
- **A4 (over-cut watch on rows 5/10): CORRECT, mis-located.** Over-fire appeared strongly on row 5 (making-rec, as named) and row 1 (the cap); row 10 (acceptance-map) diverged but defensibly.
- **A5 (2–4 of rows 1–5 diverge): understated.** All 5 diverged.
- **Per-target direction:** MATCH on tdd(2), diagnose(4), making-rec(5, uncertain→over-cut branch); PARTIAL on scrutinize(3), acceptance-map(10); FLIPPED on system-design-review(1); MISS (controls/mixed moved) on merge-branch(6), to-issues(7), git-hygiene(8), gh-pr-review-loop(9).

## Honest limits (carried from the sealed prereg, sharpened)

- **C1 (INERT ambiguity) — N/A.** The bar is strongly load-bearing; the decoration vs already-internalized question does not arise.
- **C2 (same-model circularity) — sharpened, NOT escaped.** A passing differential shows the bar is non-inert, never that its calls are *correct*. The system-design-review result makes this concrete: the bar (applied by a fresh reviewer) and the human follow-on (1) adjudication — **both outputs of the same author's apparatus** — reach **opposite** conclusions on the cap (cut vs keep). The differential cannot adjudicate that. Only test 1 (foreign material) and test 2 (human cold-judge) can.
- **C3 (stochasticity):** controlled by ≥2/3 rep-consistency + blind scoring; the count ties (7 targets) are correctly *not* treated as substantive divergence.
- **Fencing caveat:** 2/3 bar-OFF merge-branch reviewers claimed empirical git verification ("verified in isolated repos: is-ancestor exits 0…"). My fence forbade reading the *contract* via git but not throwaway empirical testing; this is a config-orthogonal behavioral difference (likely stochastic), noted not corrected.
- **Blinding is imperfect** (the bar-ON vocabulary self-identifies); the procedural blinding (A/B labels, neutral direction terms) held, and unblinding was clean via the retained mapping.

## What this changes / next moves

1. **The cheapest, most-likely-to-falsify test is PASSED — the apparatus is not decoration.** Stop worrying about inertness; the bar measurably and consistently changes reviews.
2. **Open the cap question, properly.** The bar pushes toward cutting `system-design-review`'s finding-cap; follow-on (1) kept it. These are the same apparatus disagreeing with itself. **Do NOT silently re-cut** — this is exactly what tests 1/2 exist to adjudicate. Candidate for a human cold-judge (test 2).
3. **Run test 1 (foreign material) next** — the highest-value remaining test. The provoke-side over-fire (rows 1, 5) is the live hypothesis to probe: does the bar over-cut organizing structure on skills it did NOT help author? Foreign skills remove the authorship confound the cap disagreement just exposed.
4. **Consider a calibration note in the apparatus** (separate, gated work — not done here): the lens currently reads "substitutive structure is the cost," which a fresh reviewer applies aggressively to numeric caps and output packets. The forcing-function vs substitutive distinction is the hard call the bar is supposed to *help* make, yet here it pushed uniformly toward "substitutive." Whether that is a wording fix or a correct sharpening is itself a judgment/cold-judge question, not a differential one.
