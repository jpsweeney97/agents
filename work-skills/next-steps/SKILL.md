---
name: next-steps
description: "Use only when the user explicitly invokes `/next-steps` or `$next-steps` to turn existing findings into a dependency-aware strategic action plan with decision gates and a critical path. Do not use for ordinary next-step suggestions, choosing among options, implementation plans, tracker creation, or direct execution."
disable-model-invocation: true
---

# Next Steps

Turn findings already in hand into a small dependency-aware strategic action plan. This skill is explicit-only: use it only when the user selects `/next-steps` or `$next-steps`.

## Boundary

- Plan only from supplied findings or findings clearly present in an artifact the user placed in scope. Do not invent findings, dependencies, risks, owners, or parked items.
- Before reading work content, follow the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy. If classification, access, or destination permission is unclear, take the more protective route and ask for clarification.
- Keep the plan in chat by default. Do not execute it, create tracker items or issues, publish, send, browse, use connectors, or take another external action.
- A later explicit request for a durable plan artifact is separate: check the active workspace and a user-supplied permitted destination before writing. Do not stage, commit, stash, or push work-content output while Git retention is unapproved.
- Keep the supplied findings source visible. Preserve source pointers for claims affecting decisions, owners, numbers, or deadlines, and mark agent-derived dependencies, tasks, or sequencing `unverified`.

## Use

- Use for review findings, audit results, retrospectives, brainstorming notes, or similar analysis that needs sequencing.
- Use a recommendation method instead when the user wants to choose, prioritize, or rank options.
- Do not turn this into step-by-step coding or session-sized implementation planning.
- Exit early when appropriate:
  - With no findings, ask which artifact or discussion to plan from.
  - With one obvious next step, state it instead of fabricating phases.
  - With implementation-ready work, say that it is ready for detailed implementation planning, then stop.

## Build

1. Identify the finding source. Read a user-named artifact before planning; otherwise use the latest explicit findings block. If more than one plausible finding set exists, ask one source question rather than merging them.
2. Preserve existing finding IDs. Assign simple IDs such as `F1`, `F2`, and `F3` only when none exist.
3. Build the dependency map before phases. Use concrete rows such as `T1: <task> - covers: F1, F3 - depends on: none`. Mark a dependency `unverified (inferred)` when its source did not state it directly.
4. If dependencies are cyclic, contradictory, or cannot be derived without inventing context, state that limit and return the smallest useful partial plan rather than force phases.
5. Group only genuinely parallelizable tasks in the same phase; where parallelism is not obvious, say why they can proceed together.
6. Keep tasks strategic: state what changes and why, not implementation steps. Each `done when` must name an observable decision, owner, artifact, or entry criterion.
7. Park only supplied, non-critical findings. For every parked item, include a `revisit when` condition.

## Output

For a non-early-exit case, return these sections:

1. `Current State`
2. `Dependency Map`
3. `Sequenced Plan`
4. `Decision Gates`
5. `Critical Path`
6. `Out of Scope (Parked)`

In `Current State`, name the exact supplied findings block or artifact used. Tag any task, dependency, sequencing claim, owner, number, or deadline that is not explicit in that source `unverified`.

In `Decision Gates`, say `None - all tasks have a single forward path.` when applicable.

In `Critical Path`, include:

- `Dependency-critical chain`
- `Scheduling-critical status` — use `not claimed - no durations or deadlines supplied` unless durations or deadlines are supplied.
- `Highest-risk task` — name one only when supplied evidence supports it; otherwise use `unknown` or `tied` and explain why.

For no parked findings, say `None - no supplied findings are parked.` End in chat with the plan itself, not an implied action.
