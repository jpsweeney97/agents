---
type: results
experiment: judgment-trust test 4 — cut-then-use (recommendation → action → verification)
project: agents
branch: feature/test4-cut-then-use
seal: "2ce0935 (judgment-trust-test4-cutthenuse-prereg-seal-2026-06-16.md)"
verdict: "AT-LEAST-AS-GOOD — acting on the bar's recommended cut produced an at-least-as-good skill; both scorer families + the tie-break agree on direction"
apparatus: UNCHANGED
---

# Test 4 — cut-then-use — RESULTS

**Verdict: AT-LEAST-AS-GOOD.** Removing `next-steps`' Pre-Final Checklist — a cut the bar recommended through a cold, blind discovery pass — left the skill at least as good in practice, and under the stricter cross-model scorer slightly *cleaner*. The substitutive-recap theory (the bar's claim) holds; the salience-reinforcement challenge is refuted for this cut. This is the first test in the arc to close the full **recommendation → action → verification** loop, and it closes it in the bar's favour.

## 1. What was tested

The bar says a closing checklist whose every item merely restates a body obligation is *substitutive* (it makes the agent perform the contract instead of doing the work) and can be cut at no cost. The challenge: such a checklist does *salience* work — restating obligations at finalization catches omissions the buried body obligations miss (especially the easy-to-forget last step). Single variable: `next-steps` WITH the 8-item Pre-Final Checklist (before, sha256 `e7c3167e`) vs WITHOUT it (the cut, `22b6a74d`). Provenance and method are sealed in `…-test4-cutthenuse-prereg-seal-2026-06-16.md` (`2ce0935`).

## 2. Procedure (as sealed)

- **60 blind hermetic runs** of `claude-opus-4-8`: 10 finding-sets × 2 arms × 3 reps. Each run applied the variant contract (neutral `/tmp` kit, no test/arm/checklist tells) to one input.
- **Blind per-plan scoring**, two families, neither told the arm, the contract, or that a checklist existed: (a) **Claude panel** (primary), (b) **Codex gpt-5.5** (cross-model de-biasing, inlined, tools forbidden, batched). Rubric = 8 plan-quality properties (satisfied/violated/n.a.) + holistic 1–5 + early-exit correctness; reasoning-over-label.
- Denominators: 21 plan-type plans/arm (FS1–7 × 3), 9 early-exit plans/arm (FS8–10 × 3).

## 3. Results

**Claude family (primary): AT-LEAST-AS-GOOD.** Both arms hit a perfect ceiling — 1.00 on every property (P1–P8 = 21/21), holistic 5.0, early-exit 9/9 — *identical* with vs without the checklist. Spot-checked against raw plans (not a scorer artifact): every cut-arm plan genuinely includes the save offer (P8), "scheduling-critical: not claimed" (P6), `(inferred)` dep labels (P4), and all early-exit cases correctly decline/redirect. The body obligations alone produce fully-compliant plans; the checklist added no compliance.

**Codex family (cross-model, far more discriminating — it found real variance, so it was not rubber-stamping): AT-LEAST-AS-GOOD, with the cut arm slightly better on every dimension that moved.**

| property | WITH (before) | WITHOUT (cut) | Δ |
|---|---|---|---|
| P1 source | 1.00 | 1.00 | 0 |
| P2 mapped | 1.00 | 1.00 | 0 |
| **P3 nothing invented** | **0.67** | **0.86** | **+0.19** |
| P4 deps grounded/inferred | 0.95 | 1.00 | +0.05 |
| P5 phase ordering | 0.90 | 0.90 | 0 |
| P6 critical-path subclaims | 1.00 | 1.00 | 0 |
| **P7 parked justified** | **0.90** | **1.00** | **+0.10** |
| P8 save offer | 1.00 | 1.00 | 0 |
| **overall (micro-avg)** | **0.929** | **0.970** | **+0.042** |
| holistic mean | 4.24 | 4.57 | +0.33 |
| early-exit correct | 9/9 | 9/9 | 0 |

No property collapsed (sealed rule: no per-property drop > 0.15). Codex's verdict on the sealed criterion: C1–C4 all pass → AT-LEAST-AS-GOOD.

**Cross-family agreement:** 445/480 = **92.7%** per-property; 4 plans with ≥2 disagreements.

**Pre-registered tie-break (2nd blind Claude scorer on the 4 disagreement plans):**
- The two FS9 plans (cut arm, early-exit): re-confirmed correct decline/redirect, holistic 5 — the Claude-vs-Codex gap there was the NA-vs-scored convention on early-exit cases, not quality.
- A-FS4-r2 (WITH): held clean by Claude consensus (sided with the first Claude scorer).
- **A-FS6-r2 (WITH): P7 violation confirmed** (failed to park the explicitly "down the line" translation item, and "someone floated" dark-mode), agreeing with Codex — i.e. the primary Claude family was mildly *lenient on the WITH arm*. The cut arm carried no equivalent defect.

The tie-break therefore only **strengthens** AT-LEAST-AS-GOOD: every stricter look surfaces real defects in the WITH arm that the cut arm does not share, and none the other way.

## 4. Mechanism (suggestive, small-n)

Codex docked the WITH arm for invention/padding far more than the cut arm: **7 P3 (nothing- invented) violations vs 3, and 2 P7 (parking) violations vs 0.** Its reasons describe the WITH arm as "invents a handler-level dependency," "over-serializes … by inventing dependencies," "invents unsupported priority/cost claims," and "keeps explicitly down-line or floated items active instead of parking them." This is precisely the *perform-the-contract / fill-to-feel-done* failure mode the bar predicts substitutive structure induces — the closing checklist's "findings mapped / parked items justified" items appear to have nudged the model toward padding the active plan to look complete. Caveat: small n, P5 was symmetric (2 vs 2), and this is a correlation across 21 plans/arm, not a proven causal pathway.

## 5. Verdict and decision

Per the sealed total order (INCONCLUSIVE → REGRESSED → AT-LEAST-AS-GOOD, first match wins): not inconclusive (both families scored cleanly and agree on direction); not regressed (no criterion failed in the regression direction on either family; the cut arm is non-inferior-or- better throughout) → **AT-LEAST-AS-GOOD**.

Acting on the bar's cut recommendation produced an at-least-as-good `next-steps`. Per the sealed decision rule, the cut is validated and should be **kept/landed** (a lighter skill at equal-or- better quality); the **apparatus is UNCHANGED** (the bar's recommendation was sound).

The run phase doubles as a behavior smoke test of the cut skill: **30 live invocations of the cut variant produced fully-compliant plans and correct early-exits** — the cut skill is followed.

## 6. Honest limits

- **n = 1 cut, and a small one** (a recap checklist) — the only clean, naturally-occurring, currently-kept, never-adjudicated cut a cold 48-skill discovery pass produced. That scarcity is itself a finding (the bar's cuts on a curated library are rare and modest). The verdict speaks to this cut; generality to larger/structural cuts is not claimed.
- The runner and the primary scorer are both Claude (same-model). The **Codex cross-model arm and the tie-break** are the de-biasing checks; both agreed. This test escapes authorship circularity (the cut came from a cold blind pass) but not fully same-model circularity on the *use* side — no human ground-truth arm was run (unlike tests 2 and 5).
- Plan-quality of a planning skill is more objectively checkable than "is this critique better," which is why a quantitative measure is admissible here where `skill-benchmark` refuses to number pure-judgment quality; holistic quality remains a judgment call, reported with reasoning.

## 7. Scoreboard

5-test menu: **1 ✓ · 2 ✓ · 3 ✓ · 4 ✓ (AT-LEAST-AS-GOOD) · 5 ◐.** Test 4 is the first to close recommendation → action → verification, and the first direct evidence that **acting on a bar-recommended cut is safe** (here, mildly beneficial). Run data (git-ignored): `.agents/scratch/test4-run/` (variants, corpus, 60 plans, Claude + Codex scores, tie-break, arm map, aggregates).
