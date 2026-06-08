---
name: writing-principles
description: "Use when the user asks to improve, tighten, simplify, rewrite, edit, draft obligation text inside, or run an obligation-focused review of existing or pasted Codex-facing instruction docs such as AGENTS.md, SKILL.md, skill support docs, agents/*.md, or agents/*.yaml. Acts as an obligation edit gate: challenge what the text makes future agents do, decide, avoid, verify, remember, or maintain; remove or lighten obligations that do not protect meaningful user work; clarify obligations that earn their place. Do not use for constructing new skill bundles, changing skill capabilities or bundle structure, user-facing docs, ordinary Markdown formatting, creative writing, code comments, completed-code review, broad adversarial skill review, UX review, full proof-gate review, or material agent-facing design decisions owned by agent-facing-design."
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

Use for existing or pasted Codex-facing instruction docs:

- `AGENTS.md`
- `SKILL.md`
- skill references, examples, or support Markdown when they shape agent behavior
- `agents/*.md` and `agents/*.yaml`

Do not use for user-facing docs, ordinary Markdown formatting, conversational
replies, code comments, creative writing, broad adversarial skill review, skill
UX review, full proof-gate review, or completed-code review.

Use the neighboring lane when it owns the work:

- `agent-facing-design`: deciding whether to add net-new or materially expanded
  agent-facing obligations, proof standards, authority rules, lifecycle
  behavior, mutation boundaries, persistence, routing, or machinery; always use
  it before adding fields, statuses, workflow stages, validators, routers,
  classifiers, scoring, confidence fields, hard rules, or semantic decision
  scripts
- `skill-creator` or `write-a-skill`: constructing a new skill bundle, defining
  or changing an agent-facing capability, changing bundle structure, adding or
  changing resources or scripts, or generating metadata
- `scrutinize-skill` or another review-family skill: behavior-contract review,
  broad adversarial review, completed implementation review, execution-readiness
  review, full proof-gate, certification, or proof-chain review, PR review, plan
  review, or completed-work review
- `skill-ux-design`: skill UX, usability, invocation, steering, output,
  recovery, or durable-aftermath review
- `markdown-reformat`: structure-only Markdown cleanup that preserves wording
  and order
- `markdown-synthesis`: rewriting multiple Markdown sources into a new
  standalone document

## Edit Gate

Default to direct edits when the user asks to improve, tighten, simplify,
rewrite, refactor, or edit instruction docs, after any needed
`agent-facing-design` pre-gate.

Use this skill to draft or create instruction prose only inside an already-owned
target: a named existing file, a pasted instruction text target, or an existing
document the user already asked to edit. Do not construct new skill bundles or
define new agent-facing capabilities here; route those to `skill-creator`,
`write-a-skill`, or `agent-facing-design` as appropriate.

This skill wins for obligation-only prose edits inside an existing `SKILL.md`,
`AGENTS.md`, support doc, `agents/*.md`, or `agents/*.yaml` when the requested
change removes, lightens, narrows, or clarifies what future agents must do.
Neighboring skill-authoring workflows win when the change alters the capability,
bundle shape, resources, scripts, generated metadata, or install/runtime
surface.

Before editing, read the live target and nearby authority needed to understand
what controls the obligation: repo instructions, companion metadata, referenced
examples, validators, workflows, or neighboring docs. Keep edits scoped to the
requested instruction surface.

Use this authority map:

- `AGENTS.md`: read applicable higher-priority and repo-local instruction files
  plus linked references that control the requested edit.
- Skill bundles: read `SKILL.md`, `agents/openai.yaml`, and behavior-shaping
  references or examples that define triggers, instructions, evidence, output,
  validation, or handoff behavior.
- Metadata-only edits such as `agents/openai.yaml`: compare `display_name`,
  `short_description`, and `default_prompt` against the current `SKILL.md`.
- Pasted instruction text: treat the paste as the target, and do not require a
  file path unless the user asks to patch a file.

If the user pastes instruction text instead of naming a file, treat the pasted
text as the target. Do not demand a path just to use this skill. Return the
rewritten instruction text in chat, normally in a fenced `markdown` block, and
state that no source file was edited unless the user also asks to patch a file.

Stay in this skill for edits that remove, lighten, narrow, clarify, or make
explicit an existing obligation when the edit does not expand future agent
duties, proof standards, authority, lifecycle behavior, mutation, persistence,
routing, or external-surface expectations. If the edit would add a net-new
obligation or materially expand what a future agent must do, decide, avoid,
verify, remember, or maintain, use `agent-facing-design` first, even when the
proposed change is prose, context, an example, a boundary, or failure behavior.
Then return to this edit path only if the pre-gate says the obligation earns its
place. If the edit would add or materially change fields, statuses, workflow
stages, validators, routers, classifiers, scoring, confidence fields, hard
rules, or semantic decision scripts, treat that as machinery and apply the
stricter `agent-facing-design` test.

Editing false-proof wording in an existing instruction doc stays in this skill
when the user is asking for obligation or prose tightening, such as preventing a
structural check from implying runtime, install, sync, certification, or loaded
behavior proof. Route to review-family when the user asks whether a proof gate,
execution-readiness claim, certification, release claim, or proof chain is valid.

Challenge before clarifying:

- If no meaningful protected work is visible, delete the obligation.
- If meaningful protected work is visible, replace the obligation with the
  lightest form that protects it: a boundary, default, example, precondition, or
  failure behavior.
- If the obligation earns its place, make the trigger, action, boundary,
  evidence, and stop condition concrete enough for a future agent to follow.

Do not preserve an obligation just because it already exists. Do not polish a
bad obligation into a clearer bad obligation.

Stop and ask when the target, requested scope, or required controlling authority
is missing, or when the needed edit would cross into an unrequested file,
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

Use review-only behavior only when the user asks for obligation-focused
instruction review, audit, critique, findings, analysis, or no edits.

Lead with obligation failures, ordered by impact. For each finding, name the
user-visible failure and the edit shape: delete, lighten, clarify, narrow, add
evidence, or resolve conflict. Do not pad with generic writing advice.

If the requested review is about skill behavior, UX, completed implementation,
adversarial critique, execution readiness, or proof gates, route to the owning
neighboring skill instead of stretching this review-only path.

After findings, close with the target and scope inspected, an explicit `No edits
made` statement, and the proof boundary. Wait for the user before editing.

## Output

After direct edits, report briefly:

- what obligation changed
- whether it was deleted, lightened, or clarified
- verification performed
- remaining risk or proof boundary

After review-only work, report findings first, include the target/scope
inspected, state `No edits made`, name the proof boundary, and wait.

Always separate proof classes. Source validation does not prove installed,
cached, marketplace, runtime-loaded, hook, sync, or behavior state unless that
surface was actually checked.

## Validation

Validate the exact surfaces edited:

1. **Standalone instruction Markdown such as `AGENTS.md` or support docs**:
   inspect the final diff, check referenced paths that were added or changed,
   and run whitespace checks such as `git diff --check` on the edited files.
2. **Skill bundle behavior or trigger changes**: parse edited `SKILL.md`
   frontmatter, inspect `agents/openai.yaml` alignment even when metadata was
   not edited, check referenced paths, run the available local skill validator,
   run whitespace checks, and add a realistic dry run when practical.
3. **Metadata-only changes such as `agents/openai.yaml`**: parse YAML, compare
   `display_name`, `short_description`, and `default_prompt` against the current
   `SKILL.md`, and run whitespace checks.
4. **Multi-surface or cross-document changes**: validate each changed surface
   by its own rules, then inspect the combined diff for routing, proof, trigger,
   and lifecycle consistency.

Do not claim the rewritten instruction works if validation fails or the behavior
contract is still ambiguous.
