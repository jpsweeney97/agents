---
name: writing-principles
description: "Use for obligation-focused edits, tightening, or review of pasted or uploaded agent instruction docs (AGENTS.md, CLAUDE.md, SKILL.md). Not for new skills, user-facing docs, or formatting."
---
<!-- export: skills/writing-principles/ @ 041beb0e9c63dff561b4b13a51e669cd2a42804c | 2026-09-23 | claude.ai -->

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

Then ask what user work that obligation protects. Preserve protected user work, not original wording or assumed intent — and where intent is recorded (a commit message, design brief, ledger entry, or linked incident), read it before overriding it rather than assuming it. This conversation has no access to the user's repository or its history, so the record is whatever the user has pasted or uploaded; when it is not here, ask for it before overriding.

## Scope

Use for existing agent-facing instruction docs the user has pasted or uploaded:

- `AGENTS.md` and `CLAUDE.md`
- `SKILL.md`
- skill references, examples, or support Markdown when they shape agent behavior
- `agents/*.md` and `agents/*.yaml`

Do not use for user-facing docs, ordinary Markdown formatting, conversational replies, code comments, creative writing, broad adversarial skill review, skill UX review, full proof-gate review, or completed-code review.

Use the neighboring lane when it owns the work:

- `agent-facing-design`: deciding whether to add net-new or materially expanded agent-facing obligations. Always route a machinery addition, or a net-new or materially expanded obligation, through this lane before making it; the expansion categories and the machinery list that trip the lane are defined under the Edit Gate
- skill construction — a new skill bundle, bundle structure, resources, scripts, or generated metadata: a separate authoring job, with `agent-facing-design` governing the capability decisions and a deliberate pass on the skill's use experience (invocation, steering, output, recovery). Defining or changing an agent-facing capability routes through `agent-facing-design`
- skill benchmarking: quantitatively benchmarking a skill or optimizing its triggering description — a measured with-and-without run in the agent runtime, not prose editing
- `scrutinize-skill` (skill contracts) or `scrutinize` (plans, designs, drafts, code changes, and other artifacts): behavior-contract review, broad adversarial review, execution-readiness review, full proof-gate, certification, or proof-chain review, or plan review
- completed-work review: completed implementation review, PR review, or review of finished work against its plan or spec
- skill UX review: skill UX, usability, invocation, steering, output, recovery, or durable-aftermath review
- `markdown-reformat`: structure-only Markdown cleanup that preserves wording and order
- Markdown synthesis: rewriting multiple Markdown sources into a new standalone document

A lane named above without a skill has no skill alongside this one. Name that work as a separate job for the user to ask for; do not absorb it here.

## Edit Gate

Default to direct edits when the user asks to improve, tighten, simplify, rewrite, refactor, or edit instruction docs, after any needed `agent-facing-design` pre-gate.

Use this skill to draft or create instruction prose only inside an already-owned target: an uploaded file, a pasted instruction text target, or an existing document the user already shared and asked to edit. Do not construct new skill bundles or define new agent-facing capabilities here; route construction and capability decisions to the skill-construction and `agent-facing-design` lanes named under Scope.

Before editing, read the live target and nearby authority needed to understand what controls the obligation: repo instructions, companion metadata, referenced examples, validators, workflows, or neighboring docs. From this conversation, that means the files the user has uploaded or pasted: ask for controlling surfaces you have not seen, and when you edit without one, name plainly what was not seen. Keep edits scoped to the requested instruction surface.

Use this authority map:

- `AGENTS.md` or `CLAUDE.md`: read applicable higher-priority and repo-local instruction files plus linked references that control the requested edit, asking for any not yet shared.
- Skill bundles: read `SKILL.md`, `agents/openai.yaml`, and behavior-shaping references or examples that define triggers, instructions, evidence, output, validation, or handoff behavior, asking for any not yet shared.
- Metadata-only edits such as `agents/openai.yaml`: compare `display_name`, `short_description`, and `default_prompt` against the current `SKILL.md`, asking for the `SKILL.md` when it was not shared.
- Pasted instruction text: treat the paste as the target, and do not require a file.

If the user pastes instruction text instead of uploading a file, treat the pasted text as the target. Do not demand a file just to use this skill. Return the rewritten instruction text in chat, normally in a fenced `markdown` block — or, when the user uploaded a file and asks for it patched, as a revised copy of that file for download — and state that nothing outside this conversation was edited: applying the rewrite to their own files is the user's move.

Stay in this skill for edits that remove, lighten, narrow, clarify, or make explicit an existing obligation when the edit does not expand future agent duties, proof standards, authority, lifecycle behavior, mutation, persistence, routing, machinery, or external-surface expectations. If the edit would add a net-new obligation or materially expand what a future agent must do, decide, avoid, verify, remember, or maintain, use `agent-facing-design` first, even when the proposed change is prose, context, an example, a boundary, or failure behavior. Then return to this edit path only if the pre-gate says the obligation earns its place. If the edit would add or materially change fields, statuses, workflow stages, validators, routers, classifiers, scoring, confidence fields, hard rules, or semantic decision scripts, treat that as machinery and apply the stricter `agent-facing-design` test.

Editing false-proof wording in an existing instruction doc stays in this skill when the user is asking for obligation or prose tightening, such as preventing a structural check from implying any of the proof classes separated under Output. Route to `scrutinize-skill` (skill targets) or `scrutinize` (other artifacts) when the user asks whether a proof gate, execution-readiness claim, certification, release claim, or proof chain is valid.

Challenge before clarifying:

- If no meaningful protected work is visible, take the cheapest origin look before deleting: the line's history, commit message, linked incident, design brief, or ledger entry where the repo keeps them — from here, that is whatever origin material is already in the conversation, or a request to the user for it. Absence after the look is real grounds to delete; absence before it, including a look the user could not take, is only the editor's first impression. Weigh the reader the obligation protects — a weaker model or foreign runtime may need the guard the strongest reader finds unjustified.
- If the look still cannot settle whether the work is real — a rare-case guard, a foreign runtime's reader, a domain outside the editor's judgment — say so and hold the edit, naming what evidence or owner could settle it. Deleting on sight and keeping out of superstition are the same failure in opposite directions.
- If meaningful protected work is visible, replace the obligation with the lightest form that protects it: a boundary, default, example, precondition, failure behavior, or a graded form of a rule too crude for its cases.
- If the obligation earns its place, make the trigger, action, boundary, evidence, and stop condition concrete enough for a future agent to follow — for trust prose; judgment prose takes the per-part bar below instead.

Set the bar per part before applying remedies, using the judgment-vs-trust lens whose canonical home is `agent-facing-design` (Two Kinds of Skill; do not restate it). Trust prose — lifecycle, safety, proof, routing — takes the full concreteness ladder. Judgment prose — a provoking question, a forced comparison, a framing that organizes thinking — is protected work whose value is the provocation: sharpen it or leave it, never proceduralize it, and treat concreteness that pre-makes the call as damage, not clarity. Open space in judgment prose can be the design; challenge it only when it fails to provoke.

Do not preserve an obligation just because it already exists. Do not polish a bad obligation into a clearer bad obligation.

Stop and ask when the target, requested scope, or required controlling authority is missing, or when the needed edit would cross into an unrequested file, destructive behavior, publishing, runtime activation, or an unresolved conflict between higher-priority instructions.

## Challenge Order

Use this order as a fast scan, not a report template:

1. **Unjustified**: the obligation does not protect meaningful user work.
2. **Vague**: it lacks a concrete trigger, action, evidence, boundary, or stop condition (trust prose; judgment prose is graded by the per-part bar under Edit Gate).
3. **Undemanding**: a completion criterion is clear but requires nothing — the checkable bound can be met without the legwork it exists to force, so it invites premature completion. Demand is a property distinct from clarity. The ordered defense: sharpen the bound first; split the sequence only when the bound is irreducibly fuzzy and the rush is actually observed — and hiding later steps works only across a real context boundary, never an inline call.
4. **Unclear**: a future agent cannot tell exactly what to do or what satisfies the instruction.
5. **Overbuilt**: lighter context, examples, defaults, or boundaries would do the job without extra machinery.
6. **Unbounded**: scope, time, lifecycle, ownership, or downstream responsibility spreads farther than the user asked.
7. **False-proof**: the required evidence does not support the claim, or structural checks are allowed to imply any of the proof classes separated under Output.
8. **Conflicting**: another authority, skill, workflow, or user request can beat it, but the text does not say how to resolve the conflict.
9. **Duplicated**: the same rule lives in more than one place — another section, file, or companion surface — and the copies have drifted or are free to. Single-home the rule and point to it, carrying every copy's scope into the home before collapsing any; copies already diverged are the strongest signal.
10. **Negated**: the instruction steers by prohibition where a positive instruction would do the work — naming the forbidden behavior drags it into context and makes it more available, not less. Rewrite to state the target behavior; keep a prohibition only as a hard guardrail you cannot phrase positively, and pair it with its positive target. Routing non-use boundaries ("Do not use for...") in descriptions are exempt: they are selection contracts, not behavior steering.
11. **Accreted**: qualifiers, parentheticals, or a two-sided fence stacked clause by clause, each patching one past misfire or finding. Rewrite the governing sentence to carry its cases natively instead of appending another clause; one-logical-line formatting hides this growth in diffs, so look for it deliberately.

## Review-Only

Use review-only behavior only when the user asks for obligation-focused instruction review, audit, critique, findings, analysis, or no edits.

Lead with obligation failures, ordered by impact. For each finding, name the user-visible failure and the edit shape: delete, lighten, clarify, narrow, add evidence, or resolve conflict. Do not pad with generic writing advice.

If the requested review is about skill behavior, UX, completed implementation, adversarial critique, execution readiness, or proof gates, route to the owning neighboring lane named under Scope instead of stretching this review-only path.

After findings, close with the target and scope inspected, an explicit `No edits made` statement, and the proof boundary. Wait for the user before editing.

## Output

After direct edits, report briefly:

- what obligation changed
- whether it was deleted, lightened, or clarified
- for a deletion or lightening, what the old text carried that the new text no longer does, or the preservation check that showed nothing was dropped
- verification performed
- remaining risk or proof boundary

After review-only work, report findings first, include the target/scope inspected, state `No edits made`, name the proof boundary, and wait.

Always separate proof classes. Structural source validation proves parsing, shape, references, or static checks only; it does not prove behavior, certification, sync, plugin install, cache, marketplace, hook, distributed-copy, remote, or live runtime, and does not show that a realistic invocation followed the behavior unless one was run. A rewrite returned from this conversation is never the live source: it becomes live only when the user applies it, and the live-source checks are theirs to run then. Install, cache, distributed-copy, and other runtime surfaces need their own checks only when that surface is part of the claim. Structural checks also never prove a lightening preserved what it claims to: nothing-lost is a behavior claim, and it takes a preservation walk — one realistic invocation read against the old and new text — or an honest statement of what was dropped.

## Validation

Validate the exact surfaces edited. The container here has a shell and Python but no git and no repository, so split each check honestly: run what the container can run on the files in hand, prescribe exactly what the user runs after applying the rewrite, and never blur the two.

1. **Standalone instruction Markdown such as `AGENTS.md`, `CLAUDE.md`, or support docs**: inspect the final diff (`diff -u` of the uploaded original against the rewrite; a read-through against the pasted text when there is no file), flag referenced paths that were added or changed for the user to confirm they resolve in their repo, and run whitespace checks on the rewritten file, such as `grep -nE '[[:space:]]+$'` for trailing whitespace. The user then runs `git diff --check` on the applied edit.
2. **Skill bundle behavior or trigger changes**: parse the edited `SKILL.md` frontmatter as YAML in the container, inspect `agents/openai.yaml` alignment even when metadata was not edited (asking for it, or naming it as unseen, when it was not shared), flag referenced paths for the user to check, run whitespace checks, and add a realistic dry run when practical — here, one walk of a realistic invocation against the rewritten text. No skill validator ships with this skill; the user runs whatever validator their platform provides after applying the rewrite.
3. **Metadata-only changes such as `agents/openai.yaml`**: parse the YAML in the container, compare `display_name`, `short_description`, and `default_prompt` against the current `SKILL.md` (asking for it when it was not shared), and run whitespace checks.
4. **Multi-surface or cross-document changes**: validate each changed surface by its own rules, then inspect the combined diff for routing, proof, trigger, and lifecycle consistency.

For any edit claiming nothing was lost — a lightening, narrowing, or de-dup — walk one realistic invocation against the old and new text or name in the report what the new text no longer carries; structural checks pass silent drops.

Do not claim the rewritten instruction works if validation fails or the behavior contract is still ambiguous, and bound every claim to what was actually read, run, compared, and walked here.
