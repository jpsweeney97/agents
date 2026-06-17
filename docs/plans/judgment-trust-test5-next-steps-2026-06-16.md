---
type: action-plan
project: agents
created: 2026-06-16
source: "test-5 red-team interim results (feca720) §§6–10 + run findings"
status: "plan — not executed"
---

# Action plan — after test-5 (red-team), reviewer-side INCONCLUSIVE

Dependency-aware sequencing of the findings surfaced by the test-5 reviewer-side run
(`docs/plans/artifacts/judgment-trust-test5-redteam-results-2026-06-16.md`, `feca720`). The actionable
cluster is *closing test 5 honestly* + *fixing the design flaw that made it INCONCLUSIVE*; the rest is
characterization, parked.

## Current State

Test 5 is reviewer-side complete: **INCONCLUSIVE (W2) with zero observed lens leniency** (ΔFN=0; bar-OFF
CUT 0/27 FN-arm reps; all 4 arm-divergences bar-ON-harsher). Apparatus UNCHANGED. `main` is +5 unpushed.
The human ground-truth arm is deferred to a fresh blind judge after an orchestrator disclosure
contaminated JP + self as judges.

Findings sequenced:

- **F1** — Human ground-truth arm deferred (fresh blind judge must administer the preserved packet).
- **F2** — Blinding breach: orchestrator narrated results before certification → needs a durable guard.
- **F3** — CUT-vs-RESHAPE keying flaw: leniency keyed on CUT, a disposition opus reviewers rarely emit;
  re-key on DEFEND-as-is vs any-change.
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

- **T1 — Re-score existing reviews under the corrected key.** Cheap (data already on disk); checks
  whether bar-ON ever DEFENDED-as-is where bar-OFF wanted any change. *Done when:* a re-keyed leniency
  table is appended to the results doc and zero-leniency is confirmed or overturned.
- **T2 — Fresh blind human judge.** A person who has not seen the results administers the preserved A–M
  packet under the sealed map. *Done when:* 13 calls recorded; genuinely-BAD confirmation + human↔bar
  agreement (with/without item A) computed and results doc §§8–9 amended.
- **T3 — Author the blinding guard.** Generalize the breach into a rule: in blind-human experiments the
  orchestrator must not reveal reviewer/apparatus results in any channel the human judge can see until
  the ground-truth arm completes. *Done when:* the rule lands in the owning contract surface.

*(Parallel rationale: T1 is local analysis, T2 is external-human, T3 is contract authoring — no shared
state.)*

**Phase 2 — consolidate**

- **T4 — Push decision.** *Done when:* push of the finalized record is authorized (or explicitly
  deferred). Inferred-deps on T2 so pushed history carries the final, not interim, results.
- **T5 — Red-team v2 (only if warranted by Gate G1).** Re-keyed leniency + optionally a Claude-built
  adversary (off the Codex hole-model) and FP-scale-up. *Done when:* designed + sealed and either run or
  explicitly deferred with rationale.

**Independent track (no dependency; priority-deferred)**

- **T6 — Test 4 (cut-then-use).** The other unrun menu item; schedule once test 5 is closed. *Done when:*
  designed/sealed or explicitly deferred.

## Decision Gates

- **G1 (after T1 + T2):** Do the corrected key *and* the blind human agree the specimens were genuinely
  bad with still-zero leniency? **Yes →** test 5 closes as "INCONCLUSIVE channel, zero leniency
  confirmed"; T5 optional. **Human says specimens were mostly fine →** the "reviewers reshaped fine
  material" reading bites → T5 warranted.
- **G2 (T4):** Push authorized (interim vs final history).

## Critical Path

- **Dependency-critical chain:** T2 → T5 (the human arm gates whether a v2 re-run is worth it), with
  T1 → T5 in parallel. Closing test 5 itself bottlenecks on **T2**.
- **Scheduling-critical status:** not claimed — no durations or deadlines supplied.
- **Highest-risk task:** **T2** — the gating anchor; depends on an *uncontaminated* human being available
  plus clean administration, and risks re-confirming no leniency channel exists (real but non-fatal).
  T1/T5 are lower-risk (reviewer-side, repeatable).

## Out of Scope (Parked)

- **F4 (FN8 softening)** — revisit when designing T5's specimen set (sharper plausible-but-bad
  crude-overreach construction).
- **F5 (56% construction-miss)** — revisit at T5 (over-generate; gate on cross-family agreement that
  specimens are bad).
- **F6 residual (cross-model *reviewer* arm)** — T2 fixes the ground-truth side; the reviewer being
  Claude is only addressed by the optional test-1-§9 cross-model-reviewer arm. *Revisit when* a
  model-family portability check is wanted.
