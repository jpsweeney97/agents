---
name: outcome-check
description: "Use when a change has been in production a while and you need to check whether it actually achieved the goal it shipped for — name the goal metric, see whether any real-world signal is reachable, and render goal-met / not-moved / unverifiable-here. Closes the loop `outcome-shaping` opens. Not for code-vs-spec review (`implementation-review`), local done-ness (`closeout-check`), pre-push verification (`verify`), or watching a rollout's technical health (`deploy-plan`)."
---

# Outcome Check

For a change that shipped a while ago: did it actually move the goal it existed to move? Name the goal, check whether any real-world signal of it is reachable, and render a verdict — closing the loop `outcome-shaping` opens. Invocation: `/outcome-check` or `$outcome-check`.

The agent usually cannot read the goal metric, so the honest modal verdict is `unverifiable-here` with the exact signal a human must read. That is the deliverable, not a failure. Read-only and advisory: it renders a verdict; it takes no action.

## Fail-fast gate

Before anything else, ask whether **any** real-world signal of the goal is reachable at all. If not, say so in one line — `unverifiable-here: <the exact signal a human must read>` — and stop. Do **not** produce a structured shrug, and do **not** invent a goal so there is something to check. This gate is what keeps the skill honest; without it the skill degrades into either a fabricated all-clear or busywork.

## Shape

- **Name the goal metric** — the one the change existed to move. Pull it from the source: the original clarified outcome (`outcome-shaping`), the `acceptance-map` check IDs, the PR or issue. Do not invent it. If no goal was ever named, say so and route back to `outcome-shaping` rather than manufacture one.
- **Reachability-gate** — can you read that metric from here? (the fail-fast gate above). Read where readable; report only what you actually observed.
- **Verdict** — exactly one of: `goal-met` (the metric moved as intended — with the observation), `not-moved` (it did not — with the observation), or `unverifiable-here` (the metric is unreadable from here — name the exact signal a human must read). Never a green stamp over a metric merely reached for.

When an `acceptance-map` artifact exists, its stable-ID checks are the criteria; render the verdict in `outcome-check`'s own output — no change to `acceptance-map`.

## Proof boundary

An AI agent usually cannot read prod or the live goal metric. Report only what you observed; reachability-gate first; where blind, label `unverifiable-here` with the exact signal a human must read — never assert the goal moved over a metric you could not read.

## Fences

- **vs `outcome-shaping`.** It *opens* the goal loop up front (read-only interview, before plans); `outcome-check` *closes* it, after the ship. A verdict is not an interview.
- **vs `implementation-review`.** Code-vs-spec; `outcome-check` asks whether the goal happened *in the world*.
- **vs `acceptance-map`.** Before-implementation, statusless checks; `outcome-check` is the post-ship consumer of those IDs, weeks later, against the world rather than the code.
- **vs `closeout-check`.** Local-only done-ness (`closeout-check:19`); it cannot ask whether the goal moved in prod.
- **vs built-in `verify`.** Pre-push and local; `outcome-check` is post-ship and about the world.

## Done when

- The goal metric is named (or its absence flagged and routed back to `outcome-shaping`).
- Reachability is gated before any claim.
- The verdict is exactly one of `goal-met` / `not-moved` / `unverifiable-here`, carrying either the observation or the exact signal a human must read.
