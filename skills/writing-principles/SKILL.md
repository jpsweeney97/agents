---
name: writing-principles
description: "Use when the user asks to write, improve, tighten, simplify, rewrite, review, or edit Codex-facing instruction docs such as AGENTS.md, SKILL.md, skill support docs, agents/*.md, or agents/*.yaml. Acts as an obligation edit gate: challenge what the text makes future agents do, decide, avoid, verify, remember, or maintain; remove or lighten obligations that do not protect meaningful user work; clarify obligations that earn their place. Do not use for user-facing docs, ordinary Markdown formatting, creative writing, code comments, completed-code review, broad adversarial skill review, or machinery-design decisions owned by agent-facing-design."
---

# Writing Principles

Reflexive edit gate for Codex-facing instruction documents.

This skill is not a prose-polish checklist. Treat instruction text as a set of
obligations future agents must carry.

## Core Move

Name the obligation. Challenge whether it earns its place. If it fails, remove
or lighten it. If it earns its place, make it concrete.

For each material instruction, ask:

```text
What does this make a future agent do, decide, avoid, verify, remember, or
maintain?
```

Then ask what user work that obligation protects. Preserve protected user work,
not original wording or assumed intent.

## Scope

Use for Codex-facing instruction docs:

- `AGENTS.md`
- `SKILL.md`
- skill references, examples, or support Markdown when they shape agent behavior
- `agents/*.md` and `agents/*.yaml`

Do not use for user-facing docs, ordinary Markdown formatting, conversational
replies, code comments, creative writing, broad adversarial skill review, or
completed-code review.

Use the neighboring lane when it owns the work:

- `agent-facing-design`: deciding whether to add fields, statuses, workflow
  stages, validators, routers, classifiers, scoring, hard rules, or semantic
  decision scripts
- `skill-creator` or `write-a-skill`: constructing a skill bundle
- `scrutinize-skill` or another review-family skill: adversarial review of a
  skill, artifact, PR, plan, or completed work
- `markdown-reformat`: structure-only Markdown cleanup that preserves wording
  and order
- `markdown-synthesis`: rewriting multiple Markdown sources into a new
  standalone document

## Edit Gate

Default to direct edits when the user asks to write, improve, tighten,
simplify, rewrite, refactor, create, or edit instruction docs.

Before editing, read the live target and nearby authority needed to understand
what controls the obligation: repo instructions, companion metadata, referenced
examples, validators, workflows, or neighboring docs. Keep edits scoped to the
requested instruction surface.

Challenge before clarifying:

- If no meaningful protected work is visible, delete the obligation.
- If meaningful protected work is visible, replace the obligation with the
  lightest form that protects it: a boundary, default, example, precondition, or
  failure behavior.
- If the obligation earns its place, make the trigger, action, boundary,
  evidence, and stop condition concrete enough for a future agent to follow.

Do not preserve an obligation just because it already exists. Do not polish a
bad obligation into a clearer bad obligation.

Stop and ask when the target, requested scope, or controlling authority is
missing, or when the needed edit would cross into an unrequested file,
destructive behavior, publishing, runtime activation, or an unresolved conflict
between higher-priority instructions.

## Challenge Order

Use this order as a fast scan, not a report template:

1. **Unjustified**: the obligation does not protect meaningful user work.
2. **Vague**: it lacks a concrete trigger, action, evidence, boundary, or stop
   condition.
3. **Unclear**: a future agent cannot tell exactly what to do or what satisfies
   the instruction.
4. **Overbuilt**: lighter context, examples, defaults, or boundaries would do
   the job without extra machinery.
5. **Unbounded**: scope, time, lifecycle, ownership, or downstream responsibility
   spreads farther than the user asked.
6. **False-proof**: the required evidence does not support the claim, or
   structural checks are allowed to imply behavior, runtime, install, sync, or
   activation proof.
7. **Conflicting**: another authority, skill, workflow, or user request can beat
   it, but the text does not say how to resolve the conflict.

## Review-Only

Use review-only behavior only when the user asks for review, audit, critique,
findings, analysis, or no edits.

Lead with obligation failures, ordered by impact. For each finding, name the
user-visible failure and the edit shape: delete, lighten, clarify, narrow, add
evidence, or resolve conflict. Do not pad with generic writing advice.

## Output

After direct edits, report briefly:

- what obligation changed
- whether it was deleted, lightened, or clarified
- verification performed
- remaining risk or proof boundary

After review-only work, report findings first and wait.

Always separate proof classes. Source validation does not prove installed,
cached, marketplace, runtime-loaded, hook, sync, or behavior state unless that
surface was actually checked.

## Validation

Validate the exact surfaces edited:

1. Parse edited `SKILL.md` frontmatter and edited YAML metadata.
2. Check any referenced paths from edited surfaces.
3. Run the available local skill validator when the target is a skill bundle.
4. Run whitespace checks such as `git diff --check`.
5. For material behavior changes, add a realistic dry run when practical.

Do not claim the rewritten instruction works if validation fails or the behavior
contract is still ambiguous.
