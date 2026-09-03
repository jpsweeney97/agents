---
name: work-router
description: "Use when the user asks which skill, lane, workflow, or next owner should handle a request, backlog item, audit finding, review finding, issue, or ambiguous follow-up. Produces a read-only route recommendation with nearby non-routes and handoff boundaries; does not execute, inspect broad repo status, create plans/issues, rank product options, or run downstream skills."
---

# Work Router

Choose the skill lane that owns a piece of work, then stop. This skill is a read-only route advisor, not an orchestrator. Invoke it with `/work-router` (`$work-router`), or let it fire when a request is itself a routing question.

## Use

Use only when routing is itself the task: the user asks what skill, lane, workflow, or next owner should handle a request, audit finding, backlog item, review finding, issue, plan fragment, or ambiguous follow-up.

Good triggers:

- "What skill owns this?"
- "Route these debt findings."
- "Which lane should handle this backlog item?"
- "This seems between `simplify-code` and `improve-codebase-architecture`; decide the lane."
- "What comes next from this review finding?"

Do not use this skill as a silent wrapper around every ambiguous request. If the user directly asks for implementation, diagnosis, review, status, issue work, planning, or cleanup and the owning lane is clear from the request and available skill descriptions, use that lane directly.

If the user explicitly invokes another skill and asks to execute that skill, do not override the invocation unless the user also asks for a routing check. If the route looks dangerous, name the concern briefly and ask before switching.

## Process

1. Identify the work item or items to route. If the item is missing or too vague to classify, ask one narrow question or route to the lane that owns outcome clarification (`outcome-shaping`).
2. Inspect available skill descriptions first. When the route depends on a boundary, deep-read only the likely overlapping `SKILL.md` files and directly referenced routing examples needed to decide.
3. Pick one primary owning lane when the evidence supports it. If no current skill owns the work, say so and name the closest fallback or the missing lane.
4. Name nearby non-routes: the skills that seem plausible but should not own this item, with the reason each loses.
5. Name prerequisites before action: missing target, required approval, authority decision, evidence, explicit invocation, or external access.
6. Render the reader-first route note and stop. Do not run the downstream skill, mutate files, open issues, create plans, or perform broad status orientation.

Use current, inspected sources for routing claims. Skill descriptions and source files show source-level routing intent; they do not prove a skill is installed, cached, or active in a separate runtime unless that runtime surface was actually inspected.

## Output

Optimize for readability: owner first, reason second, traps third, next action last. Do not emit a confidence score. Use `Limits` or "could change if..." language instead.

For a normal single route:

```markdown
## Use `<skill-name>`

<One sentence restating the work and why this lane owns it.>

Why this fits:
- <1-3 bullets, plain language>

Do not use:
- `<nearby-skill>`: <why it loses>
- `<nearby-skill>`: <why it loses>

Before starting:
- <missing target / approval / evidence / decision, or `None`>

Next move:
<One concrete next action.>

Checked:
<skill descriptions / specific SKILL.md files / named artifact inspected>

Limits:
<what was not inspected or why the route could change>
```

For an obvious single route, use a compact prose answer:

```markdown
Use `simplify-code`.

This is a scoped behavior-preserving cleanup of a concrete target. Do not use `improve-codebase-architecture`; there is no architecture-deepening question yet. Before starting, make sure the exact files are named. Next move: invoke `simplify-code` on `<target>`.
```

For multiple items, group by owner instead of defaulting to a dense table:

```markdown
## Route These To `dependency-upgrade`

- **React major bump**: chosen upstream dependency bump; confirm target version before pulling.

## Route These To `simplify-code`

- **Large parser function**: scoped behavior-preserving cleanup; exact file target is known.
- **Duplicate local helper**: cleanup is local, not a repo-wide campaign.

## Needs A Decision First

- **Auth policy split**: could be `improve-codebase-architecture` or `contract-change-propagation`; decide whether the intended change alters a shared interface.
```

Use a table only when it is more readable than grouping by owner, such as many short items with the same columns.

## Routing Boundaries

- Choosing among product, design, or strategy options already on the table is `making-recommendations`; this skill chooses the owning lane, not the winning product option.
- A whole delegated decision run — generate options, cut the field with recorded reasons, develop the survivors, recommend, check the cuts against the recommendation, from one invocation without steering each step — is `deliberate` (`/deliberate` or `$deliberate`; `/decide:deliberate` on Claude). The phase skills (`ideate`, `option-shaping`, `making-recommendations`) stay right when the user wants a single phase or wants to steer each step.
- Dependency-aware sequencing of existing findings with gates and critical path is `next-steps`, and only when explicitly invoked.
- Evidence gathering and backlog discovery are the audit skill's job, such as `tech-debt-scan`; this skill routes existing items.
- Current-state orientation is `orient-status`; this skill does not inspect a repo broadly to say where things stand.
- Issue creation, labeling, and tracker state are `triage` or `to-issues`; this skill only names those lanes.
- Design shaping before implementation is `design-exploration`; this skill can route to it but does not develop the design.
- Review of skill contracts or the skill inventory is `scrutinize-skill`; this skill can route to it but does not audit the library.

When a route would require unsafe or high-stakes action, name the risk property and the approval or safety lane needed before any execution. Do not let a readable route note imply permission to proceed.
