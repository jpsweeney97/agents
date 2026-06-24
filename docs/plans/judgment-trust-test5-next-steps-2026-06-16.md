---
type: action-plan
project: agents
created: 2026-06-16
source: "test-5 red-team interim results (feca720) §§6–10 + run findings"
status: "ALL DONE. Phase 1 (T1+T2+T3) complete; G1 resolved. T6 (test 4, cut-then-use) DONE — AT-LEAST-AS-GOOD. T5 (red-team v2) DONE — CLOSED as characterized: an 8-lens design panel caught the test-4-lever misattribution and gated the seal on a pilot; two pre-seal pilots showed the FN leniency channel empty (0/6 sharpened levers) and the FP over-cut channel empty on neutral material → no sealed run warranted, apparatus UNCHANGED. The 5-test menu is COMPLETE (1✓2✓3✓4✓5✓)."
---

# Action plan — after test-5 (red-team), reviewer-side INCONCLUSIVE

Dependency-aware sequencing of the findings surfaced by the test-5 reviewer-side run (`docs/plans/artifacts/judgment-trust-test5-redteam-results-2026-06-16.md`, `feca720`). The actionable cluster is *closing test 5 honestly* + *fixing the design flaw that made it INCONCLUSIVE*; the rest is characterization, parked.

## Current State

Test 5 is **fully run**. Reviewer-side: **INCONCLUSIVE (W2) with zero observed lens leniency** (ΔFN=0; bar-OFF CUT 0/27 FN-arm reps; all 4 arm-divergences bar-ON-harsher). **T1 DONE** (`3464918`, results §11: re-keyed DEFEND-vs-any-change, zero leniency, triangulated 3 ways). **T2 DONE** (results §12: a fresh blind administrator scored the packet — zero ground-truth leniency, GATE-FN=0, human↔bar 9/13 both arms, lens corrects baseline on FN6, genuinely-BAD 5/9). Verdict + apparatus UNCHANGED. **T3 DONE** — blinding guard authored in repo `AGENTS.md` (`## Blind Evaluations`) + charter ledger entry; forward-tested (the rule withholds and seals; the no-rule control reproduces the breach). **Phase 1 is complete.** `main` is +9 unpushed (push only on explicit ask).

Findings sequenced:

- **F1** — Human ground-truth arm deferred (fresh blind judge must administer the preserved packet).
- **F2** — Blinding breach: orchestrator narrated results before certification → needs a durable guard.
- **F3** — CUT-vs-RESHAPE keying flaw: leniency keyed on CUT, a disposition opus reviewers rarely emit; re-key on DEFEND-as-is vs any-change.
- **F4** — FN8 softened on its realism rebuild (crude-overreach attack limit).
- **F5** — Pre-filter 56% construction-miss (adversary's own family didn't agree its attacks were bad).
- **F6** — Reviewer-side circularity unescaped (only the human arm is off-model).
- **F7** — Test 4 (cut-then-use) unrun.
- **F8** — Apparatus unchanged (verify no inadvertent edit).
- **F9** — +5 commits unpushed on `main`.

## Dependency Map

```
T1: Re-score the existing 108 reviews under the corrected leniency key
    (DEFEND-as-is = lenient; CUT-or-RESHAPE = caught)     - covers: F3, F8 - depends on: none
T2: Complete the human arm — fresh blind judge on the preserved packet - covers: F1, F6 - depends on: none
T3: Durable guard — seal apparatus results from the human-judge channel
    until the ground-truth arm completes                  - covers: F2 - depends on: none
T4: Push decision for the +5 commits                      - covers: F9 - depends on: T2 (inferred)
T5: Design/run red-team v2 (re-keyed leniency; optional
    Claude-built adversary + FP-scale-up)                 - covers: F3, F4, F5 - depends on: T1, T2
T6: Test 4 (cut-then-use)                                 - covers: F7 - depends on: none (priority-deferred)
```

## Sequenced Plan

**Phase 1 — close test 5 (parallel; all independent)**

- **T1 — Re-score existing reviews under the corrected key. ✅ DONE** (`3464918`, results §11). Re-keyed DEFEND-as-is vs any-change: **lens-leniency = 0**, lens-stricter = FN6/GOOD1; triangulated by an independent 13-agent blind re-code (96.2% arm-class agreement, still 0) and a 4-way adversarial refutation (no counterexample). Zero leniency **confirmed**.
- **T2 — Fresh blind human judge. ✅ DONE** (results §12). A fresh administrator (saw only packet + sheet) returned 13 calls; scored deterministically + independently (3 scorers identical, 4 auditors). **GATE-FN = 0** (no human-flagged flaw the lens defended); human↔bar **9/13 both arms** (8/12 without item A); **FN6: lens corrects baseline toward human**; genuinely-BAD **5/9** (detection-engagement 5/5); over-cut lens-specific only at GOOD1; 0 "remove" votes. Verdict **INCONCLUSIVE** unchanged.
- **T3 — Author the blinding guard. ✅ DONE.** Landed as a general rule in repo `AGENTS.md` (`## Blind Evaluations`): in any blind evaluation, never reveal apparatus state to a current/potential ground-truth judge until their independent judgment is recorded; lost blinding is unrecoverable. Charter ledger entry added; `agent-facing-design` gate + One-Owner check passed (no collision with `skill-benchmark`); forward-tested (with-rule withholds and seals, no-rule control reproduces the breach).

*(Parallel rationale: T1 is local analysis, T2 is external-human, T3 is contract authoring — no shared state.)*

**Phase 2 — consolidate**

- **T4 — Push decision.** *Done when:* push of the finalized record is authorized (or explicitly deferred). Inferred-deps on T2 so pushed history carries the final, not interim, results.
- **T5 — Red-team v2. ✅ DONE — CLOSED as characterized** (no sealed run; channel proven empty pre-seal). Drafted a both-arms v2 prereg → hardened by an 8-lens design panel (`wf_60516e04-80c`, SEAL-AFTER-FIXES) which caught the load-bearing error (the test-4 whole-section cut was **bar-ON's**, not the baseline's, so the FN divergence cell was forbidden by construction) and made BLOCKER #2: gate the seal on an unsealed base-rate pilot. Pilot (`wf_c1397f11-68b`, 36 reviews): the designed FN/FP levers were dead; one borderline FN flicker via a new lever (a crude overreach embedded in a forcing function). Sharpening pilot (`wf_5b2a2271-e04`, 48 reviews): **0/6 levers reproduce** — bar-ON catches the embedded overreach using the lens's own vocabulary; controls clean. **Verdict: leniency not constructible (5 probes), over-cut empty on neutral material, apparatus UNCHANGED.** Record: `docs/plans/artifacts/judgment-trust-test5-v2-pilot-results-2026-06-16.md`.

**Independent track (no dependency; priority-deferred)**

- **T6 — Test 4 (cut-then-use). ✅ DONE — AT-LEAST-AS-GOOD** (results `…-test4-cutthenuse-results-2026-06-16.md`; seal `2ce0935`). A cold, blind 48-skill discovery pass + 3-lens adversarial verification surfaced exactly one clean bar-recommended cut (`next-steps`' 8-item Pre-Final Checklist — pure recap of body obligations); `writing-principles` disqualified (reshape, not cut). Cut made on-branch, sealed, then 60 blind hermetic runs (2 arms × 10 inputs × 3 reps) blind-scored by a Claude panel + cross-model Codex (gpt-5.5). Claude: both arms perfect ceiling (identical). Codex (discriminating): cut arm non-inferior **and slightly cleaner** (overall 0.929→0.970; P3 invent 0.67→0.86; P7 park 0.90→1.00; holistic 4.24→4.57; no collapse). Tie-break confirmed a real P7 defect in the WITH arm the cut arm lacks. Both families + tie-break agree: **acting on the bar's cut is safe (mildly beneficial)**; substitutive-recap theory holds, salience-reinforcement refuted for this cut. Apparatus UNCHANGED. Decision: keep/land the cut (JP go).

## Decision Gates

- **G1 (after T1 + T2): RESOLVED — split, resolving toward "close it."** Zero leniency is confirmed **both** ways (corrected key §11 and the blind human §12: GATE-FN = 0). Genuinely-BAD came in **5/9**, not "mostly fine" — and the "reviewers reshaped fine material" reading lands only on FN5/FN8/PC, where it is **symmetric across both arms** (a reviewer-vs-human strictness gap, **not** a lens property; the one lens-specific over-call is GOOD1). So **test 5 closes as "INCONCLUSIVE channel, zero leniency confirmed vs ground truth."** T5 (red-team v2) is **OPTIONAL**, warranted only to attack the structural wall — a corpus that is genuinely-BAD **and** baseline-CUT — which prereg §7's RESILIENT-ceiling already flags may be intrinsic to a same-model reviewer that reshapes rather than cuts.
- **G2 (T4):** Push authorized (interim vs final history).

## Critical Path

- **Dependency-critical chain:** T2 → T5 (the human arm gates whether a v2 re-run is worth it), with T1 → T5 in parallel. Closing test 5 itself bottlenecks on **T2**.
- **Scheduling-critical status:** not claimed — no durations or deadlines supplied.
- **Highest-risk task:** **T2** — the gating anchor; depends on an *uncontaminated* human being available plus clean administration, and risks re-confirming no leniency channel exists (real but non-fatal). T1/T5 are lower-risk (reviewer-side, repeatable).

## Out of Scope (Parked)

- **F4 (FN8 softening)** — revisit when designing T5's specimen set (sharper plausible-but-bad crude-overreach construction).
- **F5 (56% construction-miss)** — revisit at T5 (over-generate; gate on cross-family agreement that specimens are bad).
- **F6 residual (cross-model *reviewer* arm)** — T2 fixes the ground-truth side; the reviewer being Claude is only addressed by the optional test-1-§9 cross-model-reviewer arm. *Revisit when* a model-family portability check is wanted.
