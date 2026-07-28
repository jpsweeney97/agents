---
name: assumption-check
description: "Use when a plan, design, or decision is settled enough to act on and its load-bearing assumptions need to be surfaced before effort is spent: identify human, environmental, dependency, sequencing, and access assumptions; rank them by load-bearing uncertainty; and attach cheap confirm-or-kill probes. Forward and non-adversarial; do not use to judge readiness, imagine completed failure, model an attacker, or interrogate one question at a time."
---

# Assumption Check

Surface what a settled plan needs to be true before effort is spent: enumerate explicit and implicit assumptions, prioritize the ones that are both load-bearing and uncertain, and attach the cheapest observable confirm-or-kill probe to each. Invocation: `/assumption-check` or `$assumption-check`.

This is a forward-looking check from the plan as written. It does not critique, re-decide, approve, or certify the plan; it makes the beliefs the plan depends on visible so they can be tested cheaply before the work tests them expensively.

## Authority and safety

Before handling work content, read the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy. Those instructions control what may be read, discussed, retained, or written. If data classification, permission, or a proposed destination is unclear, take the more protective route and stop for clarification.

Return the register in chat by default. Do not browse, access a connector, install anything, create a file, run a probe, stage, commit, stash, push, publish, or make another external change unless the user separately requests it and the active workspace permits it. Keep source claims affecting decisions, owners, numbers, or deadlines traceable, and mark organizing inference `unverified`.

## The moves

1. **Pin the plan.** State the plan, design, or decision being checked and confirm that it is settled enough to act on. If it is still being shaped or selected, stop and return to clarification, design exploration, or decision-making rather than treating a moving target as settled.
2. **Enumerate explicit and implicit assumptions.** Treat the plan text as the floor, not the field. Look for assumptions about people and shared understanding, the environment and operating conditions, dependencies and prior work, sequencing and timing, and access, permissions, tools, information, or capacity. Include target-specific assumptions as warranted, such as technical interfaces, policy interpretation, service demand, governance ownership, or data quality.
3. **Rank in words, not scores.** Order assumptions by the combination of how load-bearing and how uncertain they are. Give each a short reason. Do not use numeric scores, weight formulas, or likelihood-impact matrices: the reasoned judgment matters more than performative precision.
4. **Attach a cheap confirm-or-kill probe.** For each ranked assumption, identify the least costly observable test that could settle it: an in-scope document check, permitted local inspection, small authorized experiment, or question to an appropriate person. State both what would confirm the assumption and what would kill it. A probe without a kill condition is reassurance, not a test.

## Default chat register

Use a compact ordered register such as:

```markdown
1. Assumption: <what must be true>
   Why it is early: <load-bearing × uncertainty reason>
   Probe: <cheapest permitted check; not run unless separately requested>
   Confirm: <observable evidence>
   Kill: <observable evidence>
   Status: unprobed
```

`unprobed`, `confirmed`, and `killed` describe the human's observed state; they are not workflow states the agent maintains, audits, or enforces.

Create or update a durable register only when the user explicitly asks and the active workspace permits the exact destination. Confirm the destination if its convention is unclear. Do not treat a request for an assumption check as permission to create folders, use a default path, write a file, or retain work content in Git. Never stage, commit, stash, or push work-content output unless the active workspace explicitly authorizes it and the user separately requests it.

## Close — no verdict

Stop when every ranked assumption has a confirm-or-kill probe, then state what was enumerated and what remains unprobed. Do not conclude that the plan is safe, ready, de-risked, low-risk, or approved, and do not say "do not proceed until". This skill gates nothing.

Offer probe execution as a separate, opt-in action. If a requested probe needs unavailable access or an unapproved route, say that it is unverified here and identify the human or permitted evidence source that could resolve it; do not evade the boundary through a connector or other external route.

## When not to use

- The user wants a readiness verdict or adversarial review of the plan.
- The user wants failure imagined from the future looking back; use a premortem instead.
- The threat is a motivated adversary rather than an accidental failure mode.
- The user wants a one-question-at-a-time interrogation.
- The plan is not settled yet; clarify, shape, or choose it before checking its assumptions.
