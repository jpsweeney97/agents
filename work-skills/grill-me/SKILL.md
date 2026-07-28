---
name: grill-me
description: "Use when the user wants a plan, design, strategy, or decision pressure-tested through a one-question-at-a-time interrogation. Do not use for ordinary clarification, outcome discovery, recommendations, implementation planning, or a complete review report."
---

# Grill Me

Pressure-test a plan, design, strategy, or decision through a focused, one-question-at-a-time interview.

## Boundary

- If no candidate plan, design, strategy, or decision is in context, ask what the user wants to be grilled on before starting.
- Treat the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy as authority before reading work content. If classification, access, or permission is unclear, take the more protective route and ask for clarification.
- Use only the facts and artifacts the user has placed in scope. Do not browse, use connectors, create files, or take another external action unless the user separately and explicitly requests it and the active workspace permits it.
- Keep the exchange in chat. Do not create a written artifact unless the user separately asks for one and supplies a destination permitted by the active workspace.
- Keep a concise source pointer for artifact-backed claims affecting decisions, owners, numbers, or deadlines. Mark agent inference `unverified`.

## Interview

1. Identify the decision tree: desired outcome, constraints, assumptions, alternatives, dependencies, ownership, evidence, reversibility, and failure or recovery paths that materially affect the proposal.
2. Ask the most load-bearing unresolved question first. Ask exactly one question, give a recommended answer with its reasoning, and wait for the user's answer before continuing.
3. Use each answer to choose the next branch. Test hidden assumptions, trade-offs, edge cases, authority, sequencing, and what would falsify the current choice. Do not substitute a checklist for judgment; pursue the branches that could change the plan.
4. If an answer is already available in an artifact the user placed in scope, read that artifact under the active workspace rules rather than asking the user to repeat it. If it is unavailable, say what remains unverified rather than reaching into another system.
5. Continue until the user says the plan feels solid or asks to stop, or until further questions would no longer change the plan.

## Close

On stopping, give a short conversational summary that distinguishes the user's decisions and source-backed answers from `unverified` agent inference, then name the single weakest remaining assumption. Include compact source pointers only where the summary asserts a decision-relevant fact, owner, number, or deadline. Name a clear next move when one follows, in plain language; do not assume another skill, plugin, tracker, or workflow is installed.

Do not execute, publish, send, create tracker items, or change target-work Git state as part of this pressure test. If the user later explicitly requests a durable work artifact, first check the active workspace's instructions and destination permission; do not stage, commit, stash, or push work content while its Git retention is unapproved.
