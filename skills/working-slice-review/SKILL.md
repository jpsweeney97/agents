---
name: working-slice-review
description: "Use when reviewing a technical design, spec, plan, or architecture draft whose main risk is overbuilding before a working slice exists: too many invariants, edge-case mitigations, proof gates, abstractions, or future-facing guardrails delaying feedback. Produces evidence-grounded critique plus a lightweight illustrative build sequence. Do not use for broad architecture review, adversarial execution-readiness review, issue slicing, dependency-aware next-step sequencing, test-first implementation, prototype implementation, completed implementation review, or full implementation planning."
---

# Working Slice Review

Review technical drafts for premature completeness before they have a working slice. Use `/working-slice-review` or `$working-slice-review` when the useful critique is not "is every risk covered?" but "what should exist first so the team can learn whether this direction works?"

This is a judgment skill. Its value is a pragmatic lens, not a checklist: preserve foundations that protect the first feedback loop, and challenge machinery that delays learning before the core loop works.

## Core Lens

Ask:

```text
What is the smallest robust working slice that would teach us whether this direction is right?
```

Then separate:

- **Robust foundation**: choices that make the first working slice easier to build, verify, recover, or extend.
- **Premature machinery**: invariants, abstractions, proof systems, edge-case handling, lifecycle gates, or future-facing guardrails that delay learning before the core loop exists.
- **Real risk**: failure modes likely enough, damaging enough, or hard enough to unwind that they deserve early handling.
- **Hypothetical risk**: future cases that can be blocked, deferred, documented, or handled after the first slice proves the direction.
- **Learning loop**: whether the design reaches observable behavior early enough to steer the next decision.

Do not treat pragmatism as sloppiness. The point is to spend early complexity only where it protects the first real feedback loop.

## Workflow

1. Read the target material enough to make evidence-grounded critique. If the artifact is available and manageable, read it in full before judging. If it is too large or only partially available, state the bounded scope before findings.
2. Anchor substantive claims to concrete sections, paths, line numbers, or quoted user-supplied text when available. If the target is verbal or lacks stable anchors, label evidence as user-supplied or inferred.
3. Identify the few highest-leverage course corrections. Prefer 3-5 strong points over an exhaustive defect catalog.
4. For each point, explain how the current design delays learning, creates early complexity, protects the wrong thing, or preserves a foundation worth keeping.
5. End with a lightweight working-slice example that illustrates a better direction without replacing the source design.

Stay read-only by default. Do not edit, rewrite, save, ticket, implement, or create a replacement spec or plan unless the user explicitly asks after the review.

## Working-Slice Example Boundary

The working-slice example is capability/order-level only. It is a nudge and an example, not a plan.

Do not include exact file paths, commands, owners, issue bodies, acceptance checklists, dependency maps, test-first task loops, or executor-ready steps. If the user wants those, hand off to the owning lane.

Good example shape:

```markdown
Lightweight working-slice example:
1. Import one known-good source and persist the smallest project state needed to reopen it.
2. Show the edited state in the UI with one real operation wired end to end.
3. Export that same narrow case and verify the user-visible promise it depends on.
```

Bad example shape:

```markdown
1. Create src/export/Verifier.swift with these methods...
2. Add tests in Tests/ExportVerifierTests.swift...
3. Run swift test and expect...
```

## Output

Use this shape by default:

```markdown
Bottom line: <one sentence on whether the design is overbuilt, under-founded, or well-balanced>

Top feedback:
1. <highest-leverage critique>
   Evidence: <section/path/line anchor, or clearly labeled inferred/user-supplied evidence>
   Why it matters: <how this delays learning, increases early complexity, protects the wrong thing, or preserves a foundation worth keeping>
   Nudge: <small course correction, not a rewrite>

2. ...

Lightweight working-slice example:
1. <capability/order-level step>
2. <capability/order-level step>
3. <capability/order-level step>

Boundary: This is critique plus an illustrative path, not a replacement spec, implementation plan, issue breakdown, or test plan.
```

If the draft is well-balanced, say that directly and name what makes the sequencing healthy. Do not invent overbuilding findings to satisfy the skill.

## Handoffs

Hand off instead of silently becoming another workflow:

- `system-design-review`: broad architecture review across boundaries, data, reliability, operations, ownership, and tradeoffs.
- `scrutinize`: adversarial review, formal stress test, or execution-readiness verdict.
- `prototype`: throwaway code to answer a design, state, logic, or UI question.
- `implementation-planning`: executor-ready implementation plan with paths, commands, tasks, and verification.
- `/next-steps` or `$next-steps`: dependency-aware sequencing of findings or follow-up work.
- `to-issues`: tracker-ready issue slicing.
- `tdd`: test-first or tracer-bullet implementation.
- `design-exploration`: shaping an unsettled idea into a design/spec before reviewing it.

If the user asks for one of those downstream artifacts after the critique, name the handoff and ask or switch according to the user's request.
