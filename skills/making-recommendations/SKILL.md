---
name: making-recommendations
description: "Use when the user asks for a recommendation, comparison, trade-off, ranking, or decision between two or more serious options already on the table (`which is better`, `help me decide`, `should I choose X or Y`). Do not use for factual questions, trivial preferences, or partitioning one already-shaped scope into keep/defer/cut under a deadline, risk, or capacity constraint (`scope-cut`); when no concrete options are named yet, clarifying a muddy goal is `outcome-interviewer` and shaping a design is `design-exploration`."
---

# Structured Recommendations

Recommend only after comparing real options and ranking trade-offs.

Use this skill when the user wants a decision between viable options. If the request is really asking to clarify a muddy outcome, design a solution, build a feature, fix a bug, or plan implementation, name the better lane and stop or ask before switching instead of forcing a ranking.

Read [examples/behavior-examples.md](examples/behavior-examples.md) when routing, stakes, or output calibration is unclear.

## Trigger Boundaries

- Use for explicit recommendation, comparison, trade-off, ranking, or choice requests where the user wants judgment between serious options.
- Low-stakes recommendation requests still trigger when the options are serious enough that judgment would help; only trivial preferences are out of scope.
- Use for "best way to..." only when the user is clearly asking to choose among approaches, not when they need outcome clarification, brainstorming, debugging, design, or implementation.
- Do not use for factual questions, simple lookups, trivial preferences, or status orientation.
- If the desired outcome or serious options are still muddy, use a pre-ranking exit or permissioned handoff instead of ranking.

## First Move

Before ranking, check whether the decision, serious options, constraints, failure modes, and stakes are clear enough to compare.

- If one missing detail would materially change the recommendation, ask one question and stop.
- If the user asks to be grilled, stress-tested, challenged, or drilled on a decision, name `grill-me` as the better lane and switch only when the same message explicitly asks for that workflow.
- If the ask needs clarification rather than choice, name `outcome-interviewer` as the better lane, say why, and ask before switching.
- If the ask needs design exploration before a choice can exist, name `design-exploration` as the better path, say why, and ask before switching.
- If the ask is really a constraint-driven descope — partitioning one already-shaped scope into keep/defer/cut under a deadline, risk, or capacity limit — name `scope-cut` as the better lane, say why, and ask before switching instead of ranking "what to cut" as if the cut items were rival options for one slot.
- If enough is clear to proceed, state any assumptions before evaluating.
- Do not generate a full ranking from a muddy prompt.

## Pre-Ranking Exits

Use these exits before the normal workflow. Do not include a full ranking when an exit applies.

- `material missing detail`: A missing fact, constraint, criterion, owner, deadline, or stake would materially change the recommendation. Ask one focused question, mark readiness `not enough to recommend yet`, and stop.
- `options not comparable`: The options optimize for different outcomes or need different criteria. State the mismatch, ask the decision-frame question, mark readiness `options not comparable`, and stop.
- `only one serious option`: Only one option remains viable after applying the user's constraints. Name the viable option, explain why the other named options are not serious, and do not invent a weak alternative just to rank. You may recommend the viable option with honest readiness, or say what check could reveal a second serious option.

## Handoffs

Handoffs are permissioned and non-silent.

- Do not silently continue under another skill after `making-recommendations` triggers.
- When another lane is better, name the lane, say why recommendation cannot proceed yet, ask whether to switch, and stop.
- If the user already explicitly asked for the adjacent workflow in the same message, you may switch after naming the move.
- Use `outcome-interviewer` when the desired outcome, criteria, or real decision is still muddy.
- Use `grill-me` when the user wants an interactive pressure test of a decision, not a one-shot recommendation.
- Use `design-exploration` when the user needs design exploration before serious options exist.
- Use `scope-cut` when the request partitions one scope into keep/defer/cut against a binding constraint, not a pick-one ranking among rival options.
- Use the relevant review, status, baseline, debugging, planning, or implementation skill when the request is not primarily a choice.

## Workflow

1. State the decision and decision type.
2. Set stakes from reversibility and blast radius: `low`, `medium`, or `high`.
3. Generate before evaluating: user options first, plus distinct alternatives or the null option only when they are serious and material to the decision.
4. For medium/high stakes, name gaps and what could resolve or flip them.
5. Evaluate criterion-by-criterion: decompose criteria from the user's constraints and failure modes, then score every option against one criterion before moving to the next, holding off on a holistic impression until every criterion is scored (the noise-reducing Mediating Assessments Protocol).
6. Aggregate the per-criterion scores into a ranking using a weighting or priority basis you name, rank every serious option, recommend one only if evidence supports it, and label readiness.

## Rules

- Keep generation and evaluation separate.
- Score one criterion across every option before scoring the next, never option-by-option — an early overall impression of one option should not leak into its score on an unrelated criterion.
- State the scale or basis each criterion is scored on so the same inputs would reproduce the same score later, not an unanchored gut rating.
- Name the weighting or priority basis behind the aggregated ranking so the user can see it and override it; if a final judgment call overrides the mechanical aggregation, say why instead of silently swapping in a different ranking.
- Verify unstable facts before ranking when the answer depends on current prices, laws, availability, schedules, APIs, or similar details.
- Do not add alternatives or a null/no-change option unless they could realistically win, reveal a constraint, or change the recommendation.
- Do not invent weak alternatives; use the `only one serious option` exit when only one option is viable.
- If the recommendation does not follow from the ranking, fix the ranking or explain the exception.
- If verification is needed but not practical in the current turn, name the gap and use an honest exit or `best available` readiness instead of overstating certainty.

## Stakes

- `Low`: reversible and narrow. Skip gaps/sensitivity and say why.
- `Medium`: partially reversible or meaningful blast radius. Name gaps and 1-2 realistic flips.
- `High`: hard to reverse or broad blast radius. Use `references/high-stakes.md`; include commitment point, rollback/blast-radius risk, gaps, and flip conditions.

## Readiness

- `verifiably best`: option space is complete, material gaps are resolved/non-material, and ranking is stable.
- `best available`: current information supports the choice, but named gaps or conditions could still flip it.
- `not enough to recommend yet`: material facts, criteria, or options are missing and one focused check or answer could change the recommendation.
- `decision needed`: evidence can frame the trade-off, but a human must choose because values, ownership, policy, product meaning, or risk tolerance controls the answer.
- `options not comparable`: the options optimize for different outcomes or need different criteria; clarify the decision before ranking.

## Output

Match output weight to stakes and user request.

- Pre-ranking exits: use `Decision`, `Why No Ranking`, `Next Move`, and `Readiness`.
- Use the fuller packet below whenever any of these hold: stakes are medium/high, 3 or more criteria are scored, or the user asks for depth, a matrix, a table, or a side-by-side comparison — low stakes alone does not override these. Otherwise use a concise shape: usually `Recommendation`, `Why`, `Trade-off`, and `Readiness`, with gaps included only when they matter.

Fuller packet:

1. `Decision`
2. `Stakes`
3. `Options Considered`
4. `Criteria`
5. `Ranking` — render as a tradeoff matrix (options as rows, criteria as columns plus the weighting basis, cells the per-criterion scores from move 5) when 3 or more criteria are scored or the user asked for a matrix, table, or side-by-side comparison; otherwise a ranked list with one line of reasoning per option is enough.
6. `Recommendation`
7. `Readiness`
8. `Gaps / What Could Flip`

For high-stakes decisions, also include:

- `Commitment Point`
- `Rollback / Blast Radius`

If the user explicitly asks for a very short high-stakes answer, compress these risk dimensions — `Commitment Point`, `Rollback / Blast Radius`, and `Gaps / What Could Flip` — into prose instead of silently dropping them.
