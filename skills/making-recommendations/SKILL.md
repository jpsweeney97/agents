---
name: making-recommendations
description: Use when the user explicitly asks for a recommendation, comparison, trade-off analysis, or decision between viable options. Trigger on "recommend", "which is better", "help me decide", or "should I choose X or Y" when the ask is about choosing among serious options. Do not use for factual questions, trivial choices, or broad "best way to build/design/fix" requests where the real work is still clarification, brainstorming, or implementation design.
---

# Structured Recommendations

Recommend only after comparing real options and ranking trade-offs.

Use this skill when the user wants a decision between viable options. If the
request is really asking to clarify a muddy outcome, design a solution, build a
feature, fix a bug, or plan implementation, hand off to the appropriate skill
instead of forcing a ranking.

Read [examples/behavior-examples.md](examples/behavior-examples.md) when routing,
stakes, or output calibration is unclear.

## Trigger Boundaries

- Use for explicit recommendation, comparison, trade-off, ranking, or choice
  requests where the user wants judgment between serious options.
- Use for "best way to..." only when the user is clearly asking to choose among
  approaches, not when they need outcome clarification, brainstorming,
  debugging, design, or implementation.
- Do not use for factual questions, simple lookups, trivial preferences, or
  status orientation.
- If the desired outcome or serious options are still muddy, ask one clarifying
  question or hand off to `outcome-interviewer` or `superpowers:brainstorming`.

## First Move

Before ranking, check whether the decision, serious options, constraints,
failure modes, and stakes are clear enough to compare.

- If one missing detail would materially change the recommendation, ask one
  question and stop.
- If the ask needs clarification rather than choice, hand off to
  `outcome-interviewer`.
- If the ask needs design exploration before a choice can exist, hand off to
  `superpowers:brainstorming`.
- If enough is clear to proceed, state any assumptions before evaluating.
- Do not generate a full ranking from a muddy prompt.

## Workflow

1. State the decision and decision type.
2. Set stakes from reversibility and blast radius: `low`, `medium`, or `high`.
3. Generate before evaluating: user options, distinct alternatives, and the null option.
4. For medium/high stakes, name gaps and what could resolve or flip them.
5. Evaluate options against criteria from the user's constraints and failure modes.
6. Rank every serious option, recommend one only if evidence supports it, and
   label readiness.

## Rules

- Keep generation and evaluation separate.
- Verify unstable facts before ranking when the answer depends on current prices, laws, availability, schedules, APIs, or similar details.
- Do not invent weak alternatives; say when only one serious option exists.
- If the recommendation does not follow from the ranking, fix the ranking or explain the exception.
- If verification is needed but not practical in the current turn, name the gap
  and use an honest exit or `best available` readiness instead of overstating
  certainty.

## Stakes

- `Low`: reversible and narrow. Skip gaps/sensitivity and say why.
- `Medium`: partially reversible or meaningful blast radius. Name gaps and 1-2 realistic flips.
- `High`: hard to reverse or broad blast radius. Use `references/high-stakes.md`; include commitment point, rollback/blast-radius risk, gaps, and flip conditions.

## Readiness

- `verifiably best`: option space is complete, material gaps are resolved/non-material, and ranking is stable.
- `best available`: current information supports the choice, but named gaps or conditions could still flip it.
- `not enough to recommend yet`: material facts, criteria, or options are missing
  and one focused check or answer could change the recommendation.
- `decision needed`: evidence can frame the trade-off, but a human must choose
  because values, ownership, policy, product meaning, or risk tolerance controls
  the answer.
- `options not comparable`: the options optimize for different outcomes or need
  different criteria; clarify the decision before ranking.

## Output

Use this shape for normal chat answers:

1. `Decision`
2. `Stakes`
3. `Options Considered`
4. `Criteria`
5. `Ranking`
6. `Recommendation`
7. `Readiness`
8. `Gaps / What Could Flip`

For high-stakes decisions, also include:

- `Commitment Point`
- `Rollback / Blast Radius`
