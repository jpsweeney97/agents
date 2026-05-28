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
- No findings: ask what artifact or discussion to plan from.
- One obvious next step: say so instead of fabricating phases.
- Implementation-ready work: switch to normal implementation planning.

## Build

- Assign finding IDs if needed, such as `F1`, `F2`, and `F3`.
- Build the dependency map before phases; each row must use `T1: <task> - covers: F1, F3 - depends on: none|T#`.
- Same-phase tasks must be parallelizable.
- Keep tasks strategic: what changes and why, not implementation steps.
- Each `done when` must name an observable decision, owner, artifact, or entry criterion.
- Park non-critical findings instead of padding the active plan.

## Output Sections

Return: `Current State`, `Dependency Map`, `Sequenced Plan`, `Decision Gates`, `Critical Path`, and `Out of Scope (Parked)`.

- `Decision Gates`: use `None - all tasks have a single forward path.` when applicable.
- `Critical Path`: include chain plus highest-risk task, likelihood, impact, critical-path status, and reason.
- `Out of Scope (Parked)`: 3-5 items with `revisit when`.

## Pre-Final Checklist

Before finalizing, verify: active findings mapped; dependencies closed; phase ordering valid; critical path derivable; parked items justified.
