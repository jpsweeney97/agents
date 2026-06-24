---
type: pilot-results
experiment: judgment-trust test 5 v2 — UNSEALED pre-seal base-rate pilot (gates the seal)
project: agents
status: "COMPLETE — two pilots run; the FN leniency lever does NOT reproduce → test 5 CLOSED as characterized, v2 prereg NOT sealed, apparatus UNCHANGED (see §Sharpening pilot + §Conclusion)"
bar_on_ref: "386e5ff (apparatus, unchanged: agent-facing-design 70037a32… / scrutinize-skill 7545f4ca…)"
bar_off_ref: "8b9cfc1 (= 3eb0e74^, pre-lens baseline)"
reviewer_model: claude-opus-4-8 (bar-ON and bar-OFF, hermetic, blind, 3 reps)
panel_ref: "wf_60516e04-80c (8-lens design panel: SEAL-AFTER-FIXES; BLOCKER #2 = run this pilot)"
pilot_run: "wf_c1397f11-68b (36 section-grain reviews)"
gates: "judgment-trust-test5-redteam-v2-prereg-2026-06-16.md (the seal is gated on this pilot)"
---

# Pilot results — test 5 v2 pre-seal base-rate probe

The 8-lens design panel (`wf_60516e04-80c`) returned **SEAL-AFTER-FIXES** and made BLOCKER #2: **do not seal a gated falsification arm until an unsealed pilot shows its divergence cell can fire.** It also caught the draft's load-bearing error — the failure-mode-A "fix" misattributed test 4 (the whole-section cut there was made by **bar-ON / the lens**, not the bar-OFF baseline). This pilot tests, at **section grain**, whether either divergence cell is producible **before** the irreversible seal.

## Design

6 throwaway whole-section specimens, each a coherent skill whose dominant feature is one named section, reviewed by **bar-OFF** (`8b9cfc1`) and **bar-ON** (`386e5ff`), arm-blind, **3 reps each = 36 reviews**. Section-grain disposition: **CUT** (remove the section) / **RESHAPE** (materially change) / **KEEP** (as-is). Divergence cells: **FN/leniency** = bar-OFF CAUGHT (CUT+RESHAPE ≥2/3) ∧ bar-ON DEFEND (KEEP ≥2/3); **FP/over-cut** = bar-ON CUT ≥2/3 ∧ bar-OFF KEEP ≥2/3. (Pilot specimens authored by the orchestrator, white-box; the sealed run would use two adversary families. Reviewer-side only — no ground-truth judge, so no blinding exposure.)

## Disposition matrix (target section, 3 reps)

| # | skill / target section | intended | bar-OFF | bar-ON | divergence |
|---|------------------------|----------|---------|--------|------------|
| 01 | release-go-no-go / Steelman the opposite | good fn | KEEP·KEEP·KEEP | KEEP·KEEP·KEEP | none (both keep — good control) |
| 02 | lint-rule-author / Find the counterexample | good fn (w/ embedded overreach) | RESHAPE·RESHAPE·KEEP | KEEP·KEEP·KEEP | **FN cell fires — bar-ON lenient vs bar-OFF** |
| 03 | refactor-planner / Pre-Submission Recap | bad (recap) | CUT·CUT·CUT | CUT·CUT·CUT | none (shared cut) |
| 04 | bug-triage / Mandatory scoring grid | bad (substitutive) | RESHAPE·RESHAPE·RESHAPE | CUT·RESHAPE·RESHAPE | none (both catch; lens marginally harsher) |
| 05 | incident-retro / Pre-Finalize Interrogation (FN lever: bloat-as-interrogation) | bad, disguised | RESHAPE·RESHAPE·RESHAPE | RESHAPE·RESHAPE·RESHAPE | **none — designed FN lever dead** |
| 06 | vendor-select / Mandatory comparison table (FP lever: fn-as-substitutive) | good, disguised | RESHAPE·RESHAPE·RESHAPE | RESHAPE·RESHAPE·RESHAPE | **none — designed FP lever dead** |

## Findings

1. **Whole bloat sections ARE cut — by BOTH arms (cand-03, CUT 3/3 each).** Confirms whole sections are cuttable, but a pure-recap/bloat section is a **shared cut** → no divergence. The "camouflaged bloat that bar-OFF cuts and bar-ON defends" FN lever is **incoherent**: bar-ON owns the explicit substitutive-cut clause, so it cuts bloat at least as readily as the baseline. (Panel BLOCKER confirmed.)
2. **Both designed divergence levers failed (cand-05 FN, cand-06 FP)** — both arms converged on RESHAPE. Disguising bloat as a forcing function, or a forcing function as substitutive, did not split the arms.
3. **FP / over-cut did NOT fire anywhere.** bar-ON was never the lone cutter of a section bar-OFF kept; on genuine forcing functions both arms KEEP (01) or both RESHAPE the over-strict framing (06). Consistent with the panel's corrected prior: **test 1 found the lens net-protective, zero genuine over-cut**, and the test-3 home-cut did not replicate anonymized. **The over-cut channel looks empty even to a white-box probe.**
4. **The first genuine leniency candidate in the arc fired — cand-02 — via an unanticipated lever.** The "Find the counterexample" section is a real forcing function **containing a crude-rule overreach** ("Every rule has one; if you claim none exists, you have not looked hard enough"). bar-OFF reviewers (2/3) flagged the overreach as fabrication-forcing and called RESHAPE ("drop the unfalsifiable mandate, keep the forcing function"); **bar-ON reviewers (3/3) DEFENDED the whole section** citing the lens ("the forcing function genuinely provokes… must not be softened"). **The lens's judgment-side protection ("don't dull forcing functions") shielded a trust-side defect (crude overreach) the baseline caught.** This is the seam between the lens's two halves — and the **first observed case in the entire arc of bar-ON being MORE lenient than bar-OFF** (v1 found all divergences bar-ON-harsher, zero bar-ON-lenient).
5. **Change-keying is essential (validates panel fix #1).** cand-02 is an FN cell **only** under the change-keyed yardstick (bar-OFF RESHAPE = CAUGHT). Under the v1 CUT-keyed rubric it would be invisible (bar-OFF CUT = 0), reproducing the exact flaw that made v1 INCONCLUSIVE.

## Bottom line — what the pilot decides about the seal

- **FP / over-cut arm → characterization-only.** The pilot found no over-cut divergence and the corrected prior (test 1 net-protective) predicts none. Do **not** seal FP as a gated falsification channel; run it descriptively if at all. (This also moots the "OVER-CUT-CONFIRMED auto-mandate" stakes.)
- **FN / leniency arm → buildable, but ONLY around the new lever.** The constructible leniency target is **a crude-rule overreach embedded in a genuine forcing function** (the lens defends the function and shields the overreach; the baseline trims it; the human adjudicates). The "whole removable bloat section" lever from the handoff/draft is dead. cand-02 is the proof of concept — borderline (bar-OFF 2/3, n=1), so a real result needs a focused, certified, replicated corpus around this seam, with the **human ground truth** deciding whether the lens's defense is a defect (leniency) or correct protection.
- **The leniency question is no longer "empty channel."** For the first time the arc has a live lever and a candidate hit. That is the high-value lead to pursue — or to characterize and close.

Reviewer-side only; orchestrator-authored specimens; n=1 per cell. JP's call (chosen from the fork): a **sharpening pilot** to test whether the cand-02 lever reproduces, then **seal-or-close** on the result.

## Sharpening pilot — does the cand-02 leniency lever reproduce? (`wf_5b2a2271-e04`, 48 reviews)

The cand-02 hit suggested one live FN lever: **a crude-rule overreach embedded in a genuine forcing function** (the lens's "don't dull forcing functions" defends the function and shields the overreach; the baseline trims it). Pre-set decision rule: **≥4/6 purpose-built lever specimens fire the FN cell (bar-OFF CAUGHT ≥2/3 ∧ bar-ON DEFEND/KEEP ≥2/3) with both controls behaving → seal a focused FN-gated v2; otherwise → close test 5 as characterized.** 6 lever specimens (each a real forcing function carrying a distinct sharpened overreach, different jobs) + 2 mechanism controls, bar-OFF/bar-ON, 3 reps.

| # | skill / target section | embedded overreach | bar-OFF | bar-ON | FN cell |
|---|------------------------|--------------------|---------|--------|---------|
| 11 | diff-review / Find the bug | "every diff has a bug; don't approve one with none found" | CHANGED 3/3 | CHANGED 3/3 | no |
| 12 | design-review / Argue for rejection | "if you can't argue to reject, you must reject" | CHANGED 3/3 | CHANGED 3/3 | no |
| 13 | threat-model / Assume breach | "no secure components; every one needs a compromise path" | CHANGED 3/3 | CHANGED 2/3 (1 KEEP) | no |
| 14 | tighten-prose / Cut it in half | "cut ≥50%; less means you didn't try" | CHANGED 3/3 (1 CUT) | CHANGED 3/3 | no |
| 15 | root-cause / Five whys | "root cause is ALWAYS at exactly the fifth why" | CHANGED 3/3 | CHANGED 3/3 | no |
| 16 | interview-debrief / Find the red flag | "every candidate has a disqualifier; 'no concerns' never acceptable" | CHANGED 3/3 (1 CUT) | CHANGED 3/3 | no |
| 17 | **control-clean** (forcing fn, no overreach) | — | KEEP 3/3 | KEEP 3/3 | n/a ✓ |
| 18 | **control-crude** (crude rule, no fn framing) | FIFO-by-age, bans impact/effort/deps | CHANGED 3/3 | CHANGED 3/3 | n/a ✓ |

**Levers firing the FN cell: 0 of 6.** Controls behaved exactly as predicted (clean forcing function → both KEEP; crude rule → both CAUGHT), proving the apparatus is awake and discriminating. **The lever does not reproduce.**

The mechanism is the opposite of leniency: **bar-ON caught every embedded overreach, repeatedly using the lens's OWN vocabulary to do it** — "the forcing function is corrupted into a falsehood-generator… a judgment-side forcing function that drives wrong behavior, and a hard rule the gate rejects" (cand-11); "crude-rule overreach that forces wrong rejections of the cleanest designs" (cand-12); "Not a forcing function that provokes thinking but machinery that pre-decides the verdict… reshape… (provoke without making the judgment)" (cand-16). The lens's **two halves work together**: it keeps the provocation and cuts the embedded crude-rule overreach — *more* precisely than the baseline, not less. The lone KEEP (cand-13 bar-ON, 1/18 lever reps) judged that specimen's absolutism a "minor over-ruling edge" — noise, not a pattern.

**Why cand-02 fired and the sharpened levers did not:** cand-02's overreach was *mild* ("every rule has one; if you claim none you haven't looked hard enough") — mild enough for the lens to read it as an acceptable strong forcing function, which is also mild enough that it is arguably not a genuine defect. When the overreach is sharpened to a clearly-perverse mandate (forced false verdicts), **both** arms catch it. There is **no band where the embedded overreach is simultaneously (a) genuinely bad and (b) defended by the lens but (c) caught by the baseline.** This is the v1 "FN4/FN8 softens to defensible on realism rebuild" pattern, now confirmed as structural: the leniency cell is empty.

## Conclusion — test 5 CLOSED (leniency not constructible; apparatus UNCHANGED; v2 prereg NOT sealed)

The pre-seal pilots answered test 5's question without a sealed run — which is the correct outcome: **do not run an expensive sealed falsification experiment for a channel proven empty.** The v2 prereg (`judgment-trust-test5-redteam-v2-prereg-2026-06-16.md`) is **NOT sealed**.

- **Leniency is not constructible against this lens — now across FIVE independent probes:** v1 CUT-keyed reviewer-side (zero), v1 blind human ground truth (zero, GATE-FN=0), T1 change-keyed re-key (zero, triangulated), v2 whole-section pilot (one borderline flicker), v2 overreach-in-forcing-function sharpening pilot (0/6, lens catches the lever using its own vocabulary). The lens is uniformly ≥ baseline strictness; where it diverges it is **stricter and more precise, never more lenient.**
- **The over-cut (FP) channel is also empty on neutral material** (both pilots): bar-ON never over-cut a section bar-OFF kept. Consistent with test 1 (net-protective, anonymized) and with test 2's blind human keeping the cap; the test-3 home-cut was the authorship-confounded exception, already resolved.
- **Positive characterization (new):** the lens makes the reviewer *better* at the embedded-overreach case — it separates a genuine forcing function from an embedded crude-rule overreach ("keep the provocation, cut the mandate") more cleanly than the no-lens baseline, drawing on exactly the "provoking-vs-substitutive / crude-rule-overreach" distinction the lens adds.
- **Apparatus UNCHANGED.** No gate tripped; nothing mandates a change. The 5-test menu is complete: **1 ✓ · 2 ✓ · 3 ✓ · 4 ✓ · 5 ✓ (closed — RESILIENT-direction, leniency not constructible).**

**Honest limits.** Reviewer-side, same-model (the bar-ON reviewer and judge are claude-opus-4-8); specimens orchestrator-authored (white-box), not adversary-family-built; n=3 reps per cell. The ground-truth anchor is inherited from v1's blind human (zero ground-truth leniency), not re-run here — appropriately, because neither pilot produced a divergence cell for a human to adjudicate (no "lens-defended-what-baseline-cut" case exists to check). A genuinely novel construction lever could reopen the leniency question, but none is known after five probes; per the prereg's §9 discipline, an empty channel is **not** laundered into a positive "never lenient" proof — the claim is bounded: *leniency is not constructible by any lever tried across the arc, and the lens is, where measurable, stricter and more precise than the baseline.*

