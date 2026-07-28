---
name: making-recommendations
description: "Use when the user asks for a recommendation, comparison, trade-off, ranking, or decision between two or more serious, comparable options. Do not use for factual questions, trivial preferences, or partitioning one scope under a binding constraint. When an option is only a handle or materially less developed than its rivals, develop the fixed field before registering a lean; when the field lacks serious rivals, widen it; when the outcome is muddy or the user wants an approved design, clarify the outcome or shape a design first."
---

# Making Recommendations

Recommend like an honest advisor: build the strongest contestable case, know which premise carries it, and hand back the calls that belong to the user. A recommendation is an argument, not a measurement. Respond in chat by default.

## Workspace and Safety Boundary

Before handling work content or creating a durable artifact, read the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy. That workspace controls access, classification, permitted sources and destinations, and retention. When classification, permission, source authority, or destination is unclear, take the more protective route and stop for clarification.

A recommendation request does not authorize browsing, connector use, experiments, file writes, tracker changes, sending, publication, installation, or Git operations. Do not stage, commit, stash, or push target-work content. If the user separately asks to create a durable decision artifact, first confirm a destination permitted by the active workspace; otherwise return it in chat.

## Core Behavior

- Check field readiness before registering a lean. If candidates are too sketch-level or unevenly understood for the same live questions, ask to develop the entire fixed field before completing the comparison.
- Register your first lean and the user's visible lean before any structured comparison; the comparison's job is to attack the leans, not decorate them.
- Find the decision's structure before weighing anything: constraints filter, dominance ends comparisons, and only genuine trades need judgment.
- Compare in comparative language. Never score options numerically or aggregate by weighted arithmetic.
- When the outcome turns on an exchange rate between things the user values, pose that priced trade; do not settle it silently.
- Give the runner-up its strongest honest case before closing with a pick.
- Match depth to reversibility and blast radius. Sometimes the recommendation is a permitted check rather than a choice.
- Verify unstable facts only through sources the active workspace permits. If they are inaccessible or checking them would expand the request, name the gap, mark resulting inference `unverified`, and let the close carry it.

## Field Readiness

Each candidate must be intelligible enough to answer the same decision-specific questions. If one has a mechanism, operating consequences, and assumptions while another is only a handle or slogan, the extra resolution is not evidence that the first is better. A direct request for a pick does not waive this stop.

Do not fill an uneven field from generic knowledge. Name the underdeveloped options, ask to develop the fixed field without ranking, and stop. If serious rivals are absent rather than shallow, say the field needs widening. If the desired outcome itself is unclear, ask to clarify it before comparing. If an appropriate neighboring skill is available, name it; otherwise explain the necessary next step in plain language and wait rather than silently switching workflows.

## Declare the Lean

After field readiness passes, register which way you lean on first read and why, and the user's visible lean — for example, option order, keep-versus-switch framing, adjectives, or expressed excitement. Attack both leans in the comparison.

If your recommendation matches the user's lean, say what would have to be true for the other option to win. If evidence lands against the lean, say so plainly. If the structured pass never moved you off your first lean, credit the case rather than implying that ceremony earned it.

## Filters, Dominance, and Trades

Start from the user's options. Add a distinct alternative or the null/no-change option only when it could realistically win, reveal a constraint, or change the recommendation.

- **Filters.** A confirmed hard constraint is a gate, not a criterion with a high weight. Test an asserted must-have once before it removes an option, then apply it if the user confirms it at its price.
- **Dominance.** If one surviving option is at least as good on everything that matters and better on something, say so and stop.
- **Trades.** Options that remain better at different things are the genuine decision and deserve the full comparison.

## Compare in Words

Work criterion by criterion across every surviving option so an inconvenient cell cannot be skipped. Use comparative facts in words, never invented numeric ratings or weighted totals. With three or more criteria, or when a side-by-side would help, use a table for display only.

State assumptions as assumptions. Preserve source pointers for claims affecting decisions, owners, numbers, or deadlines. Where a cell depends on an unavailable fact, say what is assumed, mark agent inference `unverified`, and say what changes if it is wrong.

## Whose Call Is It

Ask whether the outcome is stable across reasonable ways of valuing the genuine trades.

- **Stable:** make a clear call and attach the case against it.
- **It flips:** state the concrete exchange rate, give both branches, and add your lean only as a lean on the user's values call — never as evidence that settles it.

Never resolve a flip by inventing a weight and ranking anyway.

## The Case Against

Before any close that contains a pick, write the runner-up's strongest honest case and the smallest realistic change that would make it win. If no serious case exists, say the call is lopsided. A user who wants a full one-sided brief needs a separate advocacy step rather than this weighed comparison.

## Match Depth to the Door

- **Two-way door:** recommend fast when reversal is cheap and the blast radius narrow; the analysis must not cost more than the mistake it prevents.
- **One-way door:** name the commitment point, what remains reversible, owners and affected systems or people, actual rollback options and blast radius, and the cheapest permitted checks for material unknowns. Keep safety must-haves as filters. When a cheap, load-bearing check is available, `check first` is the recommendation.
- **Check first:** when a cheap permitted test settles what argument can only estimate, recommend that test and state what each result implies.

## Honest Exits and Route Closure

- **`options not comparable`:** name the outcome mismatch, ask which outcome governs, and stop.
- **`only one serious option`:** recommend it plainly and say why the alternatives are not serious; do not invent a weak rival.
- **`no basis yet`:** ask the one question that restores a defensible basis and stop. Use this rarely when stated assumptions can support an honest comparison.

When the work is really outcome clarification, fixed-field development, widening a thin field, design approval, scope partitioning, interactive pressure-testing, one-sided advocacy, review, status, baseline, debugging, planning, or implementation, name the narrower next step. If a corresponding skill is available in the active environment, identify it; otherwise explain that step in plain language. Never switch or invoke another workflow without the user's explicit request.

## The Close

Open with exactly one answer shape:

- **`clear call`:** one option wins across reasonable ways of valuing the trades.
- **`conditional call`:** the outcome flips on a named trade or unverified fact; state both branches.
- **`check first`:** the cheapest permitted check beats deciding now; state the check and what each result implies.
- **`your call`:** values, ownership, risk appetite, or product meaning controls the outcome; price both branches and label your lean as a lean.

For genuine trades, one-way doors, or a request for depth, include the decision, call, carrying premises and assumptions, strongest case against, and what would flip it. For a one-way door also include the commitment point and rollback/blast radius. Do not claim the option space is complete or the ranking verified. The close is contestable, not a substitute for the user's authority.
