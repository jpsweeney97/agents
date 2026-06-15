---
name: implementation-planning
description: "Use when the user wants to turn a settled design, spec, PRD, or approved approach into a written implementation plan: ordered tasks an executor with no codebase context could follow exactly. Do not use for design exploration, tracker issue slicing, acceptance-check mapping, strategic sequencing of findings, ad hoc implementation, or executing the plan."
---

# Implementation Planning

Write an implementation plan a skilled engineer with zero context for this
codebase could execute without guessing. Assume they know their craft but
nothing about this repo's toolset, domain, or conventions. The plan document
is the deliverable; executing it belongs to `execute-plan` or another
executor.

## Trigger Boundaries

- Requires settled source material: an approved design, spec, PRD, or
  equivalent decision. If the design is still open, name `design-exploration`
  and ask before switching.
- Tracker issue slicing is `to-issues`; observable acceptance checks are
  `acceptance-map`; dependency-aware sequencing of findings is `/next-steps` or
  `$next-steps`, which the user must invoke explicitly. This lane owns the
  executable plan document.
- Writing the plan grants no execution authority. Do not start implementing.

## Plan Standards

- If the source design covers multiple independent subsystems, flag it and
  split into one plan per subsystem; each plan should yield working,
  verifiable software on its own.
- Map the file structure before tasks: which files are created or modified
  and each one's single responsibility. Follow existing repo patterns.
- Decompose into tasks that produce self-contained, verifiable changes.
  Within tasks, bite-sized steps — one action each: write the failing test,
  run it and watch it fail, implement minimally, run and watch it pass,
  commit. Keep test-shaped steps consistent with the `tdd` skill.
- Exact file paths always. Complete code in every code step. Exact commands
  with expected output.
- No placeholders. "TBD", "add appropriate error handling", "write tests for
  the above", and "similar to Task N" are plan failures: show the actual
  content, and repeat it rather than cross-referencing — the executor may
  read tasks out of order. Reference no type, function, or method that no
  task defines.

## Self-Review

After drafting, check the plan against the source material with fresh eyes:

1. Coverage: every requirement maps to a task. List gaps and add tasks.
2. Placeholder scan for the failure patterns above.
3. Consistency: names, signatures, and types match across tasks.

Fix issues inline and move on.

## Artifact And Handoff

Save the plan to `docs/plans/YYYY-MM-DD-<topic>.md` unless the user or repo
convention names another location; state the path. Commit only per repo
convention or user request. Then name the executor: `execute-plan` for
in-session execution, or `to-issues` when the user wants tracker slices
instead of a plan run.
