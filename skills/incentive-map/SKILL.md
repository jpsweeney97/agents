---
name: incentive-map
description: "Use when proposing or vetting a structure other people will live under — a metric, quota, review gate, policy, process, automation, leaderboard, SLA, a partner-program tier, a listing or intake requirement — to predict how ordinary participants will adapt before it ships. Enumerates actors and what each is actually paid (in money, status, or comfort) to do, predicts each actor's cheapest adaptation and the equilibrium after everyone adjusts, and flags Goodhart paths (metric moves, goal doesn't) and cobra paths (intervention worsens its own target) with tripwires. Renders no ship/don't-ship verdict. Not for motivated external adversaries attacking the system (red-team, where available), accidental failure of a committed plan (premortem, where available), or access-control design."
---

# Incentive Map

red-team owns attackers; premortem owns the indifferent universe. This owns the middle neither touches: ordinary participants responding rationally to what a structure actually rewards. Nobody in an incentive map is a villain — that is the point, and the reason this failure class survives both neighboring skills.

## The moves

1. **Pin the structure and its stated goal.** What behavior it is supposed to produce, in one line.
2. **Enumerate the actors.** Everyone whose behavior the structure touches — including whoever measures it, whoever maintains it, and whoever inherits it.
3. **Name each actor's real payoff.** What they are actually paid — in money, status, or comfort — not what the structure hopes they want. Where stated intention and real payoff diverge, write both; the payoff is the one that predicts. (A reviewer paid in risk-avoidance will rationally over-flag; a seller paid in bookings will rationally push borderline deals through — neither is misbehaving.)
4. **Predict adaptations.** For each actor, the cheapest response that maximizes their payoff under the structure. Always include the two adaptations optimism skips: the null adaptation (ignore it) and compliance theater (satisfy the letter, dodge the spirit).
5. **Run the equilibrium.** After every actor adjusts — and adjusts to each other's adjustments — what does the structure actually produce? Compare it with the stated goal. Name the Goodhart paths (the measured number improves while the goal it proxies does not) and the cobra paths (the targeted behavior gets worse).
6. **Attach tripwires to the worst paths.** The observable that says "the adaptation has begun," dated where a real early signal exists — same discipline as premortem's tripwires, same trap: inventing a tripwire where no signal leads.

## The close

No verdict; the map is the deliverable — input for whoever owns the structure, since analyzing an incentive structure is never approval of one. Close with one honest line naming the actor whose real payoff the map is least sure of — that is where the map is most likely wrong.
