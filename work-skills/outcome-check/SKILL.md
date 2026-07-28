---
name: outcome-check
description: "Use when a shipped change needs a post-ship check of whether it achieved its intended real-world goal. Name the goal metric, gate on whether an authorized real-world signal is actually reachable, then render exactly `goal-met`, `not-moved`, or `unverifiable-here`. Do not use for code-vs-spec review, local done-ness, pre-push verification, or rollout technical-health monitoring."
---

# Outcome Check

For a change that shipped long enough ago to have an outcome: did it move the goal it existed to move? Name the goal, check whether an authorized real-world signal is reachable, then render one verdict. This is read-only and advisory: it takes no action.

## Fail-fast gate

Before anything else, ask whether any authorized real-world signal of the goal is reachable from the material the user placed in scope. Do not browse, use a connector, or reach into another system to find one unless the user separately and explicitly requests that access and the active workspace permits it.

If no signal is reachable, respond in one line and stop:

`unverifiable-here: <the exact signal a human must read>`

Do not invent a goal, fabricate an all-clear, or add a structured shrug. `unverifiable-here` is the honest deliverable when real-world evidence is inaccessible.

## Method

1. Name the one goal metric the change existed to move. Take it from a supplied original outcome, acceptance criteria, planning artifact, PR or issue, or other user-scoped source. Do not invent it. If no goal was named, say so and ask the user to clarify the original intended outcome before checking.
2. Apply the reachability gate. Before reading work content, follow the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy. If data classification, permission, or access is unclear, take the more protective route and return `unverifiable-here` with the exact signal a human must read; name an owner only when the user-scoped sources establish one.
3. Where the metric is authorized and actually readable in the supplied scope, report only what was observed.
4. Render exactly one verdict:
   - `goal-met`: the metric moved as intended, with the observation and a concise source pointer to the permitted signal read.
   - `not-moved`: the metric did not move as intended, with the observation and a concise source pointer to the permitted signal read.
   - `unverifiable-here`: the metric cannot be read here, with the exact signal a human must read.

If the observation's permitted source cannot be named and read, use `unverifiable-here`; do not turn agent inference into an outcome verdict.

## Proof boundary

Never render a green verdict over a metric that was not observed. A code review, local test, deployment record, or claim that the change shipped is not real-world outcome evidence by itself.

Keep the response in chat. Do not edit, create an artifact, create tracker items, send, publish, stage, commit, stash, push, or otherwise change target-work Git state as part of the check. A later explicit durable-artifact request is separate and must first satisfy the active workspace's instructions and destination permission; work content remains out of Git until retention is approved.

## Routing boundary

Use this only after shipment and for real-world goal movement. For defining a goal before planning, clarify the outcome first. For code-vs-spec review, local completion, pre-push verification, or technical rollout health, use the relevant review or verification process rather than treating it as outcome evidence.
