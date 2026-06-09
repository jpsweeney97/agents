---
name: agent-facing-design
description: Keep agent-facing systems judgment-supporting instead of overbuilt. Use when creating or materially changing prompts, skills, agent rules, workflows, schemas, validators, routers, hooks, tools, commands, scripts, or persistent artifacts that an agent must read, populate, follow, or call. Especially use before adding required fields, statuses, workflow stages, validators, classifiers, scoring, confidence, hard rules, or semantic decision scripts. Do not use for ordinary product code or user-facing docs unless they create obligations for agents.
---

# Agent-Facing Design

Keep agent-facing systems useful in the moment. This skill is not a ritual; it
is a pause before adding structure that future agents must obey.

## Core Move

Start with the user's work product: the artifact, behavior, recovery path,
review, ticket, handoff, or decision someone will rely on.

If the target already exists, inspect the live target and nearby authority before
deciding. Read only enough to name the current obligation, the work product at
stake, and the surface that controls it: prompt text, skill body, metadata,
referenced examples, schema, validator, hook, script, repo instruction, or
workflow doc. If a needed surface is unavailable, say what is unverified.

If there is no existing target and no concrete proposed structure yet, do not
run the gate as an abstract design exercise. Name the likely work product, then
ask one question or hand off to the owning design, creation, interview, or
writing workflow.

Then ask:

```text
Am I adding context that helps an agent think, or machinery that makes the
decision for it?
```

Context supports judgment: examples, boundaries, counterexamples, recoverable
state, ownership, structured evidence, preconditions, and failure behavior.

Machinery removes or narrows judgment: required fields, status systems, fixed
workflow stages, validators, routers, classifiers, scoring, confidence fields,
semantic decision scripts, and hard rules.

If the change is only context, keep it clear and proceed.

If the change adds machinery, ask the smaller question:

```text
What real damage happens if this is wrong, and could lighter context produce the
same result?
```

Use machinery when a wrong value or wrong step can damage the work: deletion,
credential exposure, corrupted state, broken recovery, stale authority, unsafe
actions, security or permissions failures, or loss of user trust.

Otherwise, prefer the smaller clearer design: prose, examples, a boundary,
recoverable state, or a deterministic mechanic that does not make the semantic
decision.

If the user explicitly asked for a field, status, schema, validator, router,
classifier, score, hard rule, or semantic script and the gate says it is not
justified, do not silently substitute a lighter design. Say what you would not
add, why the failure mode does not justify it, and what lighter path would
preserve the work. Ask before applying the substitute unless the user already
asked you to choose the smaller design.

## When Machinery Survives

Keep the surviving machinery narrow. Be able to say plainly:

- what user work it protects or improves
- why lighter context is insufficient
- what failure mode it prevents
- what future agents must understand, populate, follow, or maintain

Most of that reasoning belongs in chat or your own working notes. Write it into
the artifact only when the choice is high-risk, becomes part of a durable
contract, or would be hard for a future agent to reconstruct.

Passing the test justifies this guard, not a framework around it.

## Workflow Boundary

This skill is a design gate, not the owner of every agent-facing edit. Use it to
decide whether the proposed structure is justified, then continue with the
workflow that owns the requested work.

Examples:

- use `writing-principles` for instruction-doc writing or editing
- use `skill-creator` or `write-a-skill` for skill construction
- use the relevant review-family skill for critique or review
- use the domain or implementation skill that owns the product change

Do not silently become a UX audit, design interview, review report, skill-writing
workflow, or implementation workflow. If the user only asked for this gate's
judgment, stop after the brief answer. If the user asked for an edit and the
owning workflow is already clear, apply the smaller clearer design there.

## Calibration

Read [references/calibration.md](references/calibration.md) when the case is
borderline, the surface has grown, or you are about to add schemas, workflow
stages, validators, routers, classifiers, scoring, confidence fields, semantic
decision scripts, or hard rules.

Use the examples for judgment, not checklist compliance.

## Output Shape

For implementation work, apply the smaller clearer design directly only when the
owning edit path is already clear. After direct edits, validate through that
owning workflow and state the proof boundary. Structural source checks prove
parsing and shape, not that a realistic invocation followed the behavior. For
local skills, do not invent a separate installed-runtime layer; plugin caches,
marketplace metadata, and distributed copies need their own checks only when
that surface is part of the claim.

For obvious gate decisions, a single crisp sentence is enough. For review or
design discussion where the reasoning matters, answer briefly:

```markdown
My read: <context or machinery, and what work product is at stake>.
Evidence: <live target/context inspected, or what is unverified>.
The lighter path is <prose/example/recoverable state/deterministic mechanic>.
Machinery is justified only if <specific damage or failure mode>.
Next move: <apply directly | hand off to owning skill | ask one question>.
```
