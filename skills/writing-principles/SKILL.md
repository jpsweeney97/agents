---
name: writing-principles
description: "Use when the user asks for obligation-only edits, tightening, rewriting, or obligation-focused review of existing or pasted agent-facing instruction docs such as AGENTS.md, CLAUDE.md, SKILL.md, skill support docs, or agents/*.yaml. Do not use for new skill construction, capability or bundle changes, UX/routing audits, broad adversarial review, user-facing docs, Markdown formatting, code comments, or material agent-facing design decisions."
---

# Writing Principles

Reflexive edit gate for agent-facing instruction documents.

This skill is not a prose-polish checklist. Treat instruction text as a set of obligations future agents must carry.

## Core Move

Name the obligation. Challenge whether it earns its place. If it fails, remove or lighten it. If it earns its place, make it concrete.

For each material instruction, ask:

```text
What does this make a future agent do, decide, avoid, verify, remember, or
maintain?
```

Then ask what user work that obligation protects. Preserve protected user work, not original wording or assumed intent.

## Scope

Use for existing or pasted agent-facing instruction docs:

- `AGENTS.md` and `CLAUDE.md`
- `SKILL.md`
- skill references, examples, or support Markdown when they shape agent behavior
- `agents/*.md` and `agents/*.yaml`

Do not use for user-facing docs, ordinary Markdown formatting, conversational replies, code comments, creative writing, broad adversarial skill review, skill UX review, full proof-gate review, or completed-code review.

Use the neighboring lane when it owns the work:

- `agent-facing-design`: deciding whether to add net-new or materially expanded agent-facing obligations. Always route a machinery addition, or a net-new or materially expanded obligation, through this lane before making it; the expansion categories and the machinery list that trip the lane are defined under the Edit Gate
- skill construction — a new skill bundle, bundle structure, resources, scripts, or generated metadata: the bundled `skill-creator` on Codex, or hand-authoring against `agent-facing-design` and `skill-ux-design` on Claude (no Claude-side constructor skill, by design). Defining or changing an agent-facing capability routes through `agent-facing-design`
- `skill-benchmark` (Claude-only): quantitatively benchmarking a skill or optimizing its triggering description
- `scrutinize-skill` or another review-family skill: behavior-contract review, broad adversarial review, completed implementation review, execution-readiness review, full proof-gate, certification, or proof-chain review, PR review, plan review, or completed-work review
- `skill-ux-design`: skill UX, usability, invocation, steering, output, recovery, or durable-aftermath review
- `markdown-reformat`: structure-only Markdown cleanup that preserves wording and order
- `markdown-synthesis`: rewriting multiple Markdown sources into a new standalone document

## Edit Gate

Default to direct edits when the user asks to improve, tighten, simplify, rewrite, refactor, or edit instruction docs, after any needed `agent-facing-design` pre-gate.

Use this skill to draft or create instruction prose only inside an already-owned target: a named existing file, a pasted instruction text target, or an existing document the user already asked to edit. Do not construct new skill bundles or define new agent-facing capabilities here; route construction and capability decisions to the skill-construction and `agent-facing-design` lanes named under Scope.

Before editing, read the live target and nearby authority needed to understand what controls the obligation: repo instructions, companion metadata, referenced examples, validators, workflows, or neighboring docs. Keep edits scoped to the requested instruction surface.

Use this authority map:

- `AGENTS.md` or `CLAUDE.md`: read applicable higher-priority and repo-local instruction files plus linked references that control the requested edit.
- Skill bundles: read `SKILL.md`, `agents/openai.yaml`, and behavior-shaping references or examples that define triggers, instructions, evidence, output, validation, or handoff behavior.
- Metadata-only edits such as `agents/openai.yaml`: compare `display_name`, `short_description`, and `default_prompt` against the current `SKILL.md`.
- Pasted instruction text: treat the paste as the target, and do not require a file path unless the user asks to patch a file.

If the user pastes instruction text instead of naming a file, treat the pasted text as the target. Do not demand a path just to use this skill. Return the rewritten instruction text in chat, normally in a fenced `markdown` block, and state that no source file was edited unless the user also asks to patch a file.

Stay in this skill for edits that remove, lighten, narrow, clarify, or make explicit an existing obligation when the edit does not expand future agent duties, proof standards, authority, lifecycle behavior, mutation, persistence, routing, machinery, or external-surface expectations. If the edit would add a net-new obligation or materially expand what a future agent must do, decide, avoid, verify, remember, or maintain, use `agent-facing-design` first, even when the proposed change is prose, context, an example, a boundary, or failure behavior. Then return to this edit path only if the pre-gate says the obligation earns its place. If the edit would add or materially change fields, statuses, workflow stages, validators, routers, classifiers, scoring, confidence fields, hard rules, or semantic decision scripts, treat that as machinery and apply the stricter `agent-facing-design` test.

Editing false-proof wording in an existing instruction doc stays in this skill when the user is asking for obligation or prose tightening, such as preventing a structural check from implying any of the proof classes separated under Output. Route to review-family when the user asks whether a proof gate, execution-readiness claim, certification, release claim, or proof chain is valid.

Challenge before clarifying:

- If no meaningful protected work is visible, delete the obligation.
- If meaningful protected work is visible, replace the obligation with the lightest form that protects it: a boundary, default, example, precondition, or failure behavior.
- If the obligation earns its place, make the trigger, action, boundary, evidence, and stop condition concrete enough for a future agent to follow.

Do not preserve an obligation just because it already exists. Do not polish a bad obligation into a clearer bad obligation.

Stop and ask when the target, requested scope, or required controlling authority is missing, or when the needed edit would cross into an unrequested file, destructive behavior, publishing, runtime activation, or an unresolved conflict between higher-priority instructions.

## Challenge Order

Use this order as a fast scan, not a report template:

1. **Unjustified**: the obligation does not protect meaningful user work.
2. **Vague**: it lacks a concrete trigger, action, evidence, boundary, or stop condition.
3. **Unclear**: a future agent cannot tell exactly what to do or what satisfies the instruction.
4. **Overbuilt**: lighter context, examples, defaults, or boundaries would do the job without extra machinery.
5. **Unbounded**: scope, time, lifecycle, ownership, or downstream responsibility spreads farther than the user asked.
6. **False-proof**: the required evidence does not support the claim, or structural checks are allowed to imply any of the proof classes separated under Output.
7. **Conflicting**: another authority, skill, workflow, or user request can beat it, but the text does not say how to resolve the conflict.

## Review-Only

Use review-only behavior only when the user asks for obligation-focused instruction review, audit, critique, findings, analysis, or no edits.

Lead with obligation failures, ordered by impact. For each finding, name the user-visible failure and the edit shape: delete, lighten, clarify, narrow, add evidence, or resolve conflict. Do not pad with generic writing advice.

If the requested review is about skill behavior, UX, completed implementation, adversarial critique, execution readiness, or proof gates, route to the owning neighboring skill instead of stretching this review-only path.

After findings, close with the target and scope inspected, an explicit `No edits made` statement, and the proof boundary. Wait for the user before editing.

## Output

After direct edits, report briefly:

- what obligation changed
- whether it was deleted, lightened, or clarified
- verification performed
- remaining risk or proof boundary

After review-only work, report findings first, include the target/scope inspected, state `No edits made`, name the proof boundary, and wait.

Always separate proof classes. Structural source validation proves parsing, shape, references, or static checks only; it does not prove behavior, certification, sync, plugin install, cache, marketplace, hook, distributed-copy, remote, or live runtime, and does not show that a realistic invocation followed the behavior unless one was run. When the edited file is itself the live source, those structural checks are its proof; install, cache, distributed-copy, and other runtime surfaces need their own checks only when that surface is part of the claim.

## Validation

Validate the exact surfaces edited:

1. **Standalone instruction Markdown such as `AGENTS.md`, `CLAUDE.md`, or support docs**: inspect the final diff, check referenced paths that were added or changed, and run whitespace checks such as `git diff --check` on the edited files.
2. **Skill bundle behavior or trigger changes**: parse edited `SKILL.md` frontmatter, inspect `agents/openai.yaml` alignment even when metadata was not edited, check referenced paths, run the available local skill validator, run whitespace checks, and add a realistic dry run when practical.
3. **Metadata-only changes such as `agents/openai.yaml`**: parse YAML, compare `display_name`, `short_description`, and `default_prompt` against the current `SKILL.md`, and run whitespace checks.
4. **Multi-surface or cross-document changes**: validate each changed surface by its own rules, then inspect the combined diff for routing, proof, trigger, and lifecycle consistency.

Do not claim the rewritten instruction works if validation fails or the behavior contract is still ambiguous.
