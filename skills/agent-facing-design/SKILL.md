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

## Calibration

Read [references/calibration.md](references/calibration.md) when the case is
borderline, the surface has grown, or you are about to add schemas, workflow
stages, validators, routers, classifiers, scoring, confidence fields, semantic
decision scripts, or hard rules.

Use the examples for judgment, not checklist compliance.

## Output Shape

For implementation work, apply the smaller clearer design directly.

For review or design discussion, answer briefly:

```markdown
My read: <context or machinery, and what work product is at stake>.
The lighter path is <prose/example/recoverable state/deterministic mechanic>.
Machinery is justified only if <specific damage or failure mode>.
```
