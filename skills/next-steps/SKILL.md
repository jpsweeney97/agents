---
name: next-steps
description: Use when the user explicitly invokes `/next-steps` or `$next-steps` to turn existing findings into a strategic action plan with dependencies, gates, and critical path.
---

# Action Plan

Turn existing findings into a small dependency-aware strategic plan. This skill
is explicit-only; use it only when the user selects `/next-steps` or `$next-steps`.

Read [references/example.md](references/example.md) only when the user asks for an example or needs output or edge-case calibration.

## Use

- For review findings, audit results, retrospectives, brainstorming notes, or similar analysis.
- For sequencing supplied findings. Use `making-recommendations` instead when
  the user wants to choose among options, prioritize options, or rank trade-offs.
- Not for step-by-step coding plans, direct execution, or session-sized implementation plans.
- These are early exits that do not need the full output packet:
  - No findings: ask what artifact or discussion to plan from.
  - One obvious next step: say so instead of fabricating phases.
  - Implementation-ready work: say this is ready for `superpowers:writing-plans`
    or another explicit implementation-planning lane, then stop.

## Build

- Use only supplied findings or findings clearly present in the target artifact. Do not invent findings, dependencies, risks, or parked items.
- Determine the finding source before planning:
  - If the user points to a file or artifact, read it before planning.
  - If relying on conversation, use the latest explicit findings block.
  - If multiple plausible finding sets exist, ask one source question instead of merging them.
- Preserve existing finding IDs. Assign IDs if needed, such as `F1`, `F2`, and `F3`.
- Build the dependency map before phases. Use concrete rows:
  - `T1: <task> - covers: F1, F3 - depends on: none`
  - `T2: <task> - covers: F2 - depends on: T1`
  - `T3: <task> - covers: F4 - depends on: T1 (inferred), T2`
- Mark inferred dependencies as inferred when the source does not state them directly.
- If dependencies are cyclic, contradictory, or not derivable without inventing context, state the limit and return the smallest useful partial plan instead of forcing phases.
- Same-phase tasks must be parallelizable. If parallelism is not obvious, briefly state why they can run together.
- Keep tasks strategic: what changes and why, not implementation steps.
- Each `done when` must name an observable decision, owner, artifact, or entry criterion.
- Park only real non-critical findings instead of padding the active plan.

## Output Sections

For non-early-exit cases, return: `Current State`, `Dependency Map`, `Sequenced Plan`, `Decision Gates`, `Critical Path`, and `Out of Scope (Parked)`.
After those sections, add one concise sentence offering to save the plan to a file. Do not save automatically. If the user accepts without naming a path, ask one path question before writing.

- `Decision Gates`: use `None - all tasks have a single forward path.` when applicable.
- `Critical Path`: include `Dependency-critical chain`, `Scheduling-critical status`, and `Highest-risk task`.
- `Critical Path`: treat dependency-critical and scheduling-critical as separate claims. Use `not claimed - no durations or deadlines supplied` for scheduling-critical status unless durations or deadlines are supplied.
- `Critical Path`: name the highest-risk task only when supplied evidence supports it; otherwise use `unknown` or `tied` and explain why.
- `Out of Scope (Parked)`: list only real parked findings with `revisit when`; use `None - no supplied findings are parked.` when applicable.

## Pre-Final Checklist

Before finalizing, verify: finding source selected; active findings mapped; no findings, risks, or parked items invented; dependencies closed or marked inferred; phase ordering valid; critical path subclaims separated or limits stated; parked items justified; save offer included for non-early-exit plans.
