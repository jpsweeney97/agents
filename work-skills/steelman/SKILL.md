---
name: steelman
description: "Use when the user wants the strongest one-sided case FOR a position — 'argue the other side', 'make the best case for X', or 'the strongest case against my choice'. Builds a committed advocate's brief with load-bearing assumptions visible and an honest surviving-counter close; it picks no winner. Do not use to rank options and pick a winner, attack an artifact for flaws, ask one question at a time, or generate many options."
---

# Steelman

Build the genuine strongest case *for* one position — usually one the user is inclined to dismiss — then stop without picking. Respond in chat by default.

## Workspace and Safety Boundary

Before handling work content or creating a durable artifact, read the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy. That workspace controls access, classification, permitted sources and destinations, and retention. When classification, permission, source authority, or destination is unclear, take the more protective route and stop for clarification.

A steelman request does not authorize browsing, connector use, file writes, tracker changes, sending, publication, installation, or Git operations. Do not stage, commit, stash, or push target-work content. If the user separately asks for a durable artifact, first confirm a destination permitted by the active workspace; otherwise return the brief in chat.

## The Moves — a Rhythm, Not a Fill-In Template

1. **Pin the position; gate on harm.** State the position in one sentence in its strongest, most charitable form. Ask at most one scoping question, only when readings genuinely diverge. If advancing it would require real harm, illegality, deception, irreversible damage, or fabrication, name that and decline or heavily caveat rather than producing a slick brief.
2. **Build the genuine affirmative case.** Develop the 2 to 4 strongest distinct arguments, ordered strongest-first, from premises that could actually be true. Include arguments orthogonal to the user's objections where they matter. Frame genuine grounds; never invent facts, data, citations, or authority.
3. **Surface what the case rests on.** Name the load-bearing assumptions and show how much a skeptic already grants. Isolate the genuinely contested crux and argue why it is more defensible than it first appears. Preserve source pointers for claims affecting decisions, owners, numbers, or deadlines; mark agent inference `unverified`.
4. **Conditionally engage stated reasons.** After the affirmative case stands, address specific reasons the user gave for leaning against the position: concede valid but non-dispositive points, show what the case overcomes, and say where it wins on another consideration. Skip this when the user gave no reasons.
5. **Close honestly.** Declare that this is one-sided advocacy, not a recommendation. Name the single strongest surviving counter and leave it standing, un-rebutted. Give a committed read of how strong the best case is and whether it is safe to advance. Do not drift into a balanced analysis or pick a winner.

## Honesty Mechanism

- The bounded honest close is the primary guard: a real steelman hands over the live weakness it cannot beat and labels itself advocacy.
- Put effort into the best case, not ranking rivals, while remaining candid about how strong that case actually is.
- Anchor the case and counter in a real precedent, established principle or decision rule, the actual reasoning class of people who take the position, or the strongest version an informed proponent would endorse. Do not grade a case solely by your own unsupported preference.
- A conclusion that the case `stays weak` is a successful run. Do not inflate it to make advocacy look useful.

## Output and Route Closure

Return a reasoned brief: pinned position, affirmative case, visible load-bearing structure, and honest close. No ranking, winner, or even-handed comparison.

If the user wants a pick among options, say a weighed recommendation comparison is needed. If they want an artifact torn down, say an adversarial review is needed; for an interactive question-by-question pressure test, say that a pressure-test conversation is needed; for many unranked options, say the field needs widening; for design approval, say design exploration is needed; and for motivated-adversary or accidental-failure analysis, say a threat-model or prospective-failure exercise is needed. Name an available neighboring skill only when it exists in the active environment; otherwise describe the narrower next step in plain language. Do not silently switch workflows.

If the position needs no defense or no honest case can be built, say so and stop. A separate explicit request may authorize a durable artifact only after the active workspace and destination permit it; this skill never writes, stages, commits, or publishes one by default.
