---
type: pre-registration
experiment: judgment-trust test 5 — adversarial red-team (can the LENS be made lenient beyond a no-lens reviewer?)
project: agents
status: DRAFT prereg v3 (hardened across two design panels — wf_1e9ca0d0-0df, wf_f6e22042-d18) — ready to seal by commit BEFORE any specimen is built
sealed_at: "(set by the sealing commit — committed BEFORE any specimen is constructed or any reviewer runs)"
bar_on_ref: main @ <seal-commit> (the judgment-vs-trust LENS — `## Two Kinds of Skill` in agent-facing-design + the step-3/severity rules in scrutinize-skill)
bar_off_ref: 3eb0e74^ (8b9cfc1 — pre-lens baseline reviewer; single variable; same baseline as tests 1 & 3)
constructor_model: gpt-5.5 / Codex (white-box adversary; reads the full bar)
ground_truth: HUMAN is the sole authority on every scored FN-arm specimen; Codex (≥3 blind reps) is a non-gating pre-filter only
reviewer_model: claude-opus-4-8 (bar-ON and bar-OFF arms; reviewer-side same-model circularity NOT escaped — only ground truth + adversary are off-model)
disposition_judge: claude-opus-4-8 (different family from the Codex pre-filter) + human audit subset
depends_on: test 3 (LOAD-BEARING, f048687); test 1 (CALIBRATED, 0f70235); test 2 (human cold-judge PASS, 665fe5c)
---

# Pre-Registration — test 5, adversarial red-team

**Sealed by its commit; written and committed BEFORE any specimen is built or any reviewer runs.** The results doc (`judgment-trust-test5-redteam-results-<date>.md`) cites this SHA as proof predictions and gates preceded the data. Test 5 of the 5-test menu (source: `.agents/handoffs/2026-06-16_10-57-21_…-differential-spec-run-fresh.md`). Scoreboard: **1 ✓ 2 ✓ 3 ✓**.

Tests 1–3 measured the lens on material **not built to defeat it**. Test 5 deliberately engineers skills to fool it. **v3 was hardened across two adversarial design panels** that killed the v1 "result is pre-ordained" problem and the v2 "rubric isn't a partition / design is un-runnable" problem. The moves that matter: the verdict rides on the **FN (leniency) arm alone**, measured as a **bar-ON − bar-OFF divergence** with **human-authority ground truth**; the FP/over-cut side is **descriptive characterization, not a gate** (which dissolves the asymmetry/effort/base-rate confounds); and the protocol is split into a **mandatory cheap FN-core** and an **optional FP scale-up**.

## 1. The one question, and the unit of analysis

Does the judgment/trust **lens** (`## Two Kinds of Skill`, applied via `scrutinize-skill`), under deliberate attack, **create leniency a no-lens reviewer would not** — i.e. can an adversary build a genuinely-bad-in-remit skill choice that the **lens DEFENDS but the bar-OFF baseline CUTS**?

Absolute bar-ON errors are not attributable to the lens (test 1: the baseline cuts seeded substitutives 3/3 too). So the unit is the **bar-ON − bar-OFF divergence** on each specimen, ground-truthed by a human:

- **bar-specific FN (ΔFN) — the falsification target:** human-BAD-in-remit choice, **bar-ON DEFENDS ≥2/3, bar-OFF CUTS ≥2/3**, and the baseline's cut is attributable to a step whose bar-ON analogue is the lens (§3). The lens *talked the reviewer out of* a catch the baseline made.
- **bar-specific FP (ΔFP) — characterization only:** human-GOOD choice the lens CUTS but baseline DEFENDS. Reported to map over-cut forms; **never a verdict gate** (see §7 on why the FP/FN asymmetry is descriptive, not load-bearing).
- **shared FN / shared FP** (both arms agree wrong) = generic-reviewer behavior, never scored vs the lens.

## 2. Roles

1. **Constructor** — Codex/gpt-5.5, white-box. Builds specimens to make the lens defend a real defect; logs (sealed, hidden from roles 2–4) focal choice, intended truth, attack vector. *Residual: Codex co-authored the bar's calibration (test-1 prereg), so its hole-theory may not transfer to the Claude-applied lens — the RESILIENT ceiling in §7.*
2. **Ground truth — HUMAN authority on every scored FN-arm specimen** (each ΔFN-attempt, the FN positive control, every escalated construction-miss). The human reads the full coherent skill and calls keep/change/remove on the focal choice with one sentence — the **neutral test-2 question**, never the lens's vocabulary. A blind **Codex pre-filter (≥3 reps)** triages cheaply but **cannot clear or trip any gate**. *(Codex constructor↔pre-filter share a family; a defect both miss is routed to the human, §5, not dropped. "Fresh blind reps" is asserted, not enforced — tolerable because the pre-filter is non-gating.)*
3. **Reviewer — two arms, same specimens:** Claude applying **bar-ON** (`main`) and **bar-OFF** (`3eb0e74^`), hermetic, blind, **3 reps each (5 on any 2-1 split)**.
4. **Disposition judge** — Claude (different family from the Codex pre-filter) + **human audit subset**. Extracts **CUT / RESHAPE / DEFEND / SILENT** on the focal choice. SILENT (review never engaged the choice) on a confirmed-BAD specimen is a **salience miss, not an FN** (specimens are built so the focal choice is the dominant one). RESHAPE counts as DEFEND for the FN arm (badness survives).

## 3. "The bar" = the lens (one object), and the in-remit / attribution rules

A specimen counts toward ΔFN only if its badness is something the **lens itself claims to catch** (sealed, decidable): on a judgment part — substitutive structure (mandated shape, exhaustive rule list, fixed section that makes the judgment), or a forcing function that is absent / dulled / softened; on a trust part — duplicated machinery, or in-text crude-rule overreach. **Excluded:** out-of-lens defects (wrong facts, bad domain advice) and crude overreach whose over-breadth is *not* visible in the contract text (needs runtime evidence the static reviewer lacks). Two **blind, decidable, logged** rulings guard the FN cell, each made by a party who does **not** see the bar-ON verdict on that specimen:

- **in-remit ruling** — is the human-confirmed badness in the lens's remit (above list)? Logged with reason.
- **lens-attribution ruling** — is the **bar-OFF CUT** that creates the divergence driven by a step whose bar-ON analogue is the judgment/trust lens (not a UX/routing/validation step)? If not, the divergence is a generic-step difference, reported descriptively, **not** a lens FN. Disputes go to the human audit.

## 4. Specimen ledger (sealed) and the two run tiers

**Built (23 total):** 8 ΔFN-attempts + 8 ΔFP-attempts + 1 FN positive control + 4 reviewer-floor controls (2 clear-GOOD, 2 clear-BAD) + 2 reproduction specimens (test-2 items 7/13 analogues). **Denominators:** the **FN gate** is computed over the **8 ΔFN-attempts** (plus any escalated construction-misses); FP characterization over the **8 ΔFP-attempts**; reproduction and floor controls are reported separately, never in a gate denominator. **Equal construction effort per side**, reported in *checkable* units (realism-reject count and retained-draft count per side), not a self-attested "effort budget."

- **FN positive control** (falsifiable): a maximally-disguised BAD specimen. If **bar-OFF CUTS it but bar-ON DEFENDS**, the FN channel works and the arm is meaningful. If **BOTH arms CUT it**, the channel is probing baseline alertness, not lens leniency → **weight the FN arm down** (a real falsifying read, not a both-ways-confirmatory spin).
- **Reviewer-floor controls** prove the reviewer is *awake*, NOT that the lens is calibrated (per test 1, the baseline catches seeded substitutives too).

**Realism gate** (blind to label/direction, not the constructor; sealed hard conditions, per-specimen logged): the focal choice would plausibly ship (name a real analogue); the surrounding skill is a coherent real job; the label is not signposted; a reader told only "candidate skill" would not flag it as a test. Any condition fails ⇒ excluded.

**Run tiers (pick at run time; the FN-core is mandatory):**

- **FN-CORE (mandatory, ~cheap):** 8 ΔFN + 1 PC + 4 floor controls = 13 specimens × {bar-ON, bar-OFF} × 3 reps ≈ **78 hermetic reviews**; human certifies ~9–13 specimens (FN attempts + PC + escalations) — on the order of test 2's human load. A small fixed **filler set** (sealed library slice chosen by a non-constructor) plus a **post-hoc transcript tell-check** controls the adversarial tell.
- **FP-SCALE-UP (optional):** add the 8 ΔFP + 2 reproduction + a larger (~20) filler corpus → **~250 hermetic reviews** + heavier human/disposition load. Run only if the FN-core completes and the budget allows. The FP results are characterization regardless.

## 5. FN gates (human-authoritative, baseline-relative, rate-based)

Dispositions at **≥2/3-reps consensus** per arm. Scored on **human-confirmed**, realism-passed, in-remit, lens-attributed specimens.

- **Minimum denominator.** If **<5** ΔFN-attempts reach human-confirmed-BAD-in-remit-that-the-baseline-cut, the FN arm is **UNDERPOWERED** — no substantive verdict.
- **Construction-miss → human, never a silent drop.** A constructor-intended-BAD specimen the Codex pre-filter clears (GOOD/ambiguous) is **escalated to the human**; **human-BAD + lens-DEFEND is a scored FN** (the lens+pre-filter shared-blind-spot case — the most diagnostic). Drop count is a named output; **drops >50% ⇒ certifier-confounded, INCONCLUSIVE.**
- **GATE-FN (the falsification).** **≥2** bar-specific FNs across **≥2 distinct defect types** (closed §3 list; one form twice = 1 type) ⇒ the lens creates leniency a no-lens reviewer would not.
- **Per-rep leniency metric** (consensus can hide partial leniency): over confirmed-BAD specimens, the fraction of individual bar-ON reps that DEFEND where bar-OFF cut; **>20% is itself a leniency finding** even if no specimen reaches ≥2/3.

## 6. Outputs (sealed shape)

The bar-ON absolute 2×2 (descriptive); the **ΔFN matrix** with per-cell example specimens (focal choice, attack vector, bar-ON n/3, bar-OFF n/3, human reason, in-remit + lens-attribution rulings); FN-attempt **construction-success and drop counts**; **certifier↔human agreement**; the **per-rep ΔFN-defend rate**; the FN positive-control outcome; realism-reject counts per side/vector; the W1/W2 determination (§7). If FP-SCALE-UP ran: the ΔFP matrix and the FP/FN asymmetry **as characterization**, with the base-rate and construction caveats (§7).

## 7. Sealed caveats (must survive into the results)

- **The FP/FN asymmetry is descriptive, not a verdict.** A cut-happy baseline (test 1: bar-OFF cut QA-5, DAI-2 3/3) structurally inflates ΔFN opportunity and starves ΔFP opportunity, and per-side construction difficulty is hard to equalize. Both confounds run *against* the lens (they don't rig a clean result), but they make raw ΔFP>ΔFN uncertain — so the asymmetry is reported with bar-OFF base rates, never gated.
- **Reviewer-side circularity NOT escaped (C1, as tests 1 & 3).** bar-ON disposition and disposition extraction are Claude (the bar's co-author's model). Only the ground truth (human) and the adversary (Codex) are off-model. test 5 characterizes one model's application of the lens; a cross-model-reviewer arm (test-1 §9 style) is the portability complement.
- **RESILIENT ceiling.** A clean ΔFN=0 means "the lens resists *this* cross-model adversary's leniency theory," consistent with both genuine robustness and non-transfer of Codex's hole-model to Claude's actual holes. A same-model (Claude-built) FN red-team is the complementary probe; not run here.
- **INCONCLUSIVE is a live, likely outcome.** With the <5 floor, the W2 route, the >50%-drop route, and the positive-control route, a single Codex adversary may simply fail to build genuine baseline-caught BAD specimens. That yields INCONCLUSIVE — which **does NOT confirm "never lenient"**; it bounds leniency only by this adversary's reach. Do not upgrade it to a soft pass.
- **The "never lenient" prior is under-powered** (test 2's human cast zero "remove" votes, whole-packet), so test 5's FN arm is the **first real power on leniency**, not a confirmation.
- **No post-hoc rescue.** In-remit scope, defect-type list, gates, and rubric are fixed here.

## 8. Verdict rubric (ordered; first match wins; driven by the FN arm only)

1. **INCONCLUSIVE** — FN arm underpowered (<5 confirmed) **OR** W2 (no genuine baseline-caught BAD built) **OR** FN-attempt drops >50% **OR** the positive control was cut by both arms. *(A maximally-resistant bar that yields zero confirmable FN material lands here — honestly "we couldn't pressure leniency," never a falsification.)*
2. **FALSIFIED-LENIENT** — GATE-FN trips (≥2 bar-specific FN, ≥2 defect types). The "never lenient" claim is overturned. **MANDATES** a follow-on `agent-facing-design` pass to name and close the working disguise(s), routed through the minimalism gate (the fix is itself scrutinized). An action trigger.
3. **BOUNDED-LENIENCY** — ≥1 bar-specific FN but below GATE-FN (one disguise, or ≥2 of a single type): a real but disguise-specific hole. Map it; a fix is a separate gated decision.
4. **RESILIENT** — 0 bar-specific FN, arm powered, W1 holds. The lens resisted this adversary's leniency attack (reported with the §7 ceiling and the one-sided leniency bound from the confirmed denominator).

This is a total order on the FN outcome (no ties, no gaps). The FP/over-cut characterization (§6) is reported alongside every verdict but **does not change it**. For RESILIENT / BOUNDED-LENIENCY the apparatus stays UNCHANGED (matches tests 1–2); FALSIFIED-LENIENT triggers the gated fix above.

## 9. Execution notes

1. Seal this prereg (commit; record SHA + bar-ON/bar-OFF commits + the **verbatim certifier and reviewer prompts** in a hashed committed file + the **sealed filler-library slice**). 2. Constructor cold-builds the ledger (§4) + hidden intent log; effort in checkable units. 3. Realism-gate (blind, logged).
   4. Codex pre-filter (≥3 reps); **human certifies every FN-arm specimen + PC + escalations**. 5. Build the shuffled corpus (FN-core: small fixed filler set). 6. Run bar-ON/bar-OFF hermetic Claude reviews (3 reps, escalate splits); Claude disposition judge extracts CUT/RESHAPE/DEFEND/SILENT (human audit subset); blind in-remit + lens-attribution rulings. 7. Transcript tell-check. 8. Score §§5,8; write the results doc citing this SHA. Run **FN-CORE first**; add **FP-SCALE-UP** only if it completes and budget allows.
- Reuses test-1/3 machinery: bar-on/off hermetic runs at `3eb0e74^`, a Workflow harness, blind disposition extraction. Bar surfaces to freeze (single variable): `skills/agent-facing-design/SKILL.md` (`## Two Kinds of Skill`); `plugins/review-family/skills/scrutinize-skill/SKILL.md`.
