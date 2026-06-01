# Examples

Use only for output-shape and edge-case calibration.

## Standard Case

**User:** "$next-steps Findings: F1 weak service-to-service trust boundaries; F2 incomplete rollback procedures, marked high likelihood and high impact by the audit; F3 unclear recovery ownership, which the audit says depends on the rollback strategy; F4 decide rollout readiness after F1 and F2 are settled; non-critical cosmetic docs cleanup can wait until rollout readiness is decided. What should we tackle first?"

### 1. Current State

Active findings are F1: weak service-to-service trust boundaries, F2: incomplete rollback procedures, F3: unclear recovery ownership, and F4: decide rollout readiness. Non-critical cosmetic docs cleanup is parked because the user supplied it as non-critical and deferrable until rollout readiness is decided.

### 2. Dependency Map

- T1: define service-to-service trust model - covers: F1 - depends on: none
- T2: define rollback strategy - covers: F2 - depends on: none
- T3: assign recovery ownership - covers: F3 - depends on: T2
- T4: decide rollout readiness - covers: F4 - depends on: T1, T2

### 3. Sequenced Plan

**Phase 1** (can start now):
- T1: define service-to-service trust model - done when: security-model decision, owner, and design artifact are recorded
- T2: define rollback strategy - done when: rollback decision, owner, and rollback procedure artifact are recorded

**Phase 2** (after Phase 1):
- T3: assign recovery ownership - done when: owner, escalation criteria, and operations artifact are recorded
- T4: decide rollout readiness - done when: go/no-go criteria and the next planning workflow choice are recorded

### 4. Decision Gates

- After T1 and T2: decide rollout readiness. If readiness is approved, ask which planning workflow to use; if not, keep the plan at the decision stage.

### 5. Critical Path

**Dependency-critical chain:** tied: T2 -> T3 and T1/T2 -> T4.

**Scheduling-critical status:** not claimed - no durations or deadlines supplied.

**Highest-risk task:** T2 - likelihood: high; impact: high; on critical path: yes; why: the supplied audit marks rollback risk high, and F3 depends on the rollback strategy.

### 6. Out of Scope (Parked)

- non-critical cosmetic docs cleanup - revisit when rollout readiness is decided

## Edge Case: Ambiguous Source

**User:** "$next-steps Use the findings above."

**Context:** The prior conversation includes one review finding set and one later audit finding set, and the user did not name a target artifact.

**Response:** "I see two possible finding sets: the earlier review findings and the later audit findings. Which one should I plan from?"
