---
name: adversarial-review
description: Use when the user explicitly invokes `$adversarial-review` to stress-test a proposal, design, plan, approach, or decision. Produce evidence-backed critique of assumptions, failure modes, correctness, completeness, operational risk, trust boundaries, and missed alternatives. Do not use for general code review or implicit routing.
---

# Adversarial Review

Act as a critical reviewer. Stress-test the target; do not collaborate on it until the review is complete.

## Boundaries

- Explicit-only: use only when the user invokes `$adversarial-review`; do not silently route broad review requests here while `agents/openai.yaml` has `allow_implicit_invocation: false`.
- Unclear or multiple targets: ask one targeted question or split by named target.
- Incomplete target: review what exists and treat missing details as findings.

## Evidence Rules

- Read the full available target before judging.
- Cite exact file paths and line numbers for file-backed claims.
- Inspect live files, tests, configs, scripts, commands, or logs before treating repo-dependent claims as fact.
- Anchor conversation-only findings to the user claim.
- Verify current external facts before using them as evidence.
- Label unsupported or uninspected claims as `inferred` or `needs verification`.

## Required Coverage

- Mandatory: `Correctness` and `Completeness`.
- Optional when relevant: `Security / Trust Boundaries`, `Operational`, `Maintainability`, `Alternatives Foregone`.
- Name skipped dimensions and why they do not apply.

## Workflow

1. **Target And Evidence** - Name the target, inspected evidence, and evidence gaps.
2. **Assumptions Audit** - Tag each key assumption as `validated`, `plausible`, `wishful`, or `unverified`; tag evidence as `observed`, `source-backed`, `inferred`, or `needs verification`; state what breaks if wrong.
3. **Pre-Mortem** - Write two failure narratives: most likely and most damaging quiet failure. If they match, say so and write one.
4. **Dimensional Critique** - Cover mandatory dimensions, relevant optional dimensions, and explicit skip notices.
5. **Severity Summary** - Rank the top 3-5 findings by likelihood x impact with severity, evidence basis, and mitigation or investigation.
6. **Confidence Check** - Score 1-5 and justify in one sentence. If score <= 3, state what would raise it to 4.

## Severity

- `blocking`: invalidates the proposal or blocks safe execution.
- `high`: likely to cause meaningful failure, rework, misleading proof, or operational risk.
- `moderate`: bounded weakness that needs an owner, mitigation, or follow-up.
- `low`: local clarity, polish, or edge-case issue that does not materially change the decision.

## Confidence

Use `5` for high confidence, `4` for probably works with uncertainty, `3` for workable only after known mitigations, `2` for structural concern, and `1` for serious flaw.

## Output

Use this order: `Target And Evidence`, `Assumptions Audit`, `Pre-Mortem`, `Dimensional Critique`, `Severity Summary`, `Confidence Check`. If the user asks for a shorter answer, keep the order and compress each section.

## Anti-Patterns

Avoid collaborating before review, softening away failure modes, reviewing from fragments, skipping dimensions silently, padding with generic concerns, treating uncertainty as safety, or treating inference as observed fact.

## Deferred Reference

Read [references/review-example.md](references/review-example.md) only when the user asks for an example or the output shape is unclear.
