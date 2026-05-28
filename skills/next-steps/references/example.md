# Example

Use only for output-shape calibration.

**User:** "We finished a security review and reliability audit. What should we tackle first?"

### 1. Current State

Active findings are weak service-to-service trust boundaries, incomplete rollback procedures, and unclear recovery ownership. Cosmetic docs cleanup is parked. Production changes wait on trust and rollback decisions.

### 2. Dependency Map

- T1: define service-to-service trust model - covers: F1 - depends on: none
- T2: define rollback strategy - covers: F2 - depends on: none
- T3: assign recovery ownership - covers: F3 - depends on: T2
- T4: decide rollout scope - covers: F1, F2 - depends on: T1, T2

### 3. Sequenced Plan

**Phase 1** (can start now):
- T1: define service-to-service trust model - done when: security-model decision, owner, and design artifact are recorded
- T2: define rollback strategy - done when: rollback decision, owner, and operational-planning entry criteria are recorded

**Phase 2** (after Phase 1):
- T3: assign recovery ownership - done when: owner, escalation criteria, and operations artifact are recorded
- T4: decide rollout scope - done when: go/no-go criteria and implementation-planning entry point are recorded

### 4. Decision Gates

- After T1 and T2: if either decision requires architectural change, re-scope rollout; otherwise continue to implementation planning.

### 5. Critical Path

**Scheduling:** T2 -> T3

**Highest-risk task:** T2 - likelihood: high; impact: high; on critical path: yes; why: rollout cannot safely continue without credible rollback.

### 6. Out of Scope (Parked)

- non-critical docs cleanup - revisit when rollout scope is decided
