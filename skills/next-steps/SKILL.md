---
name: next-steps
description: Use when the user explicitly invokes `$next-steps` to turn existing findings into a strategic action plan with dependencies, gates, and critical path.
---

# Action Plan

Turn existing findings into a small dependency-aware strategic plan. This skill is explicit-only; use it only when the user selects `$next-steps`.

Read [references/example.md](references/example.md) only when the user asks for an example or needs output calibration.

## Use

- For review findings, audit results, retrospectives, brainstorming notes, or similar analysis.
- Not for step-by-step coding plans, direct execution, or session-sized implementation plans.
- These are early exits that do not need the full output packet:
  - No findings: ask what artifact or discussion to plan from.
  - One obvious next step: say so instead of fabricating phases.
  - Implementation-ready work: say this is ready for implementation planning and ask which planning workflow to use.

## Build

- Use only supplied findings or findings clearly present in the target artifact. Do not invent findings, dependencies, risks, or parked items.
- Preserve existing finding IDs. Assign IDs if needed, such as `F1`, `F2`, and `F3`.
- Build the dependency map before phases; each row must use `T1: <task> - covers: F1, F3 - depends on: none|T2|T2, T3|T2 (inferred)`.
- Mark inferred dependencies as inferred when the source does not state them directly.
- If dependencies are cyclic, contradictory, or not derivable without inventing context, state the limit and return the smallest useful partial plan instead of forcing phases.
- Same-phase tasks must be parallelizable.
- Keep tasks strategic: what changes and why, not implementation steps.
- Each `done when` must name an observable decision, owner, artifact, or entry criterion.
- Park only real non-critical findings instead of padding the active plan.

## Output Sections

For non-early-exit cases, return: `Current State`, `Dependency Map`, `Sequenced Plan`, `Decision Gates`, `Critical Path`, and `Out of Scope (Parked)`.

- `Decision Gates`: use `None - all tasks have a single forward path.` when applicable.
- `Critical Path`: include the dependency-critical chain. Treat it as scheduling-critical only when durations or deadlines are supplied.
- `Critical Path`: name the highest-risk task only when supplied evidence supports it; otherwise use `unknown` or `tied` and explain why.
- `Out of Scope (Parked)`: list only real parked findings with `revisit when`; use `None - no supplied findings are parked.` when applicable.

## Pre-Final Checklist

Before finalizing, verify: active findings mapped; no findings, risks, or parked items invented; dependencies closed or marked inferred; phase ordering valid; critical path derivable or limits stated; parked items justified.
