---
name: making-recommendations
description: Use when the user explicitly asks for a recommendation, comparison, trade-off analysis, or decision between viable options. Trigger on "recommend", "which is better", "help me decide", "best way to", or "should I choose X or Y". Do not use for factual questions or trivial choices.
---

# Structured Recommendations

Recommend only after comparing real options and ranking trade-offs.

## Workflow

1. State the decision and decision type.
2. Set stakes from reversibility and blast radius: `low`, `medium`, or `high`.
3. Generate before evaluating: user options, distinct alternatives, and the null option.
4. For medium/high stakes, name gaps and what could resolve or flip them.
5. Evaluate options against criteria from the user's constraints and failure modes.
6. Rank every option, recommend one, and label readiness.

## Rules

- Keep generation and evaluation separate.
- Verify unstable facts before ranking when the answer depends on current prices, laws, availability, schedules, APIs, or similar details.
- Do not invent weak alternatives; say when only one serious option exists.
- If the recommendation does not follow from the ranking, fix the ranking or explain the exception.

## Stakes

- `Low`: reversible and narrow. Skip gaps/sensitivity and say why.
- `Medium`: partially reversible or meaningful blast radius. Name gaps and 1-2 realistic flips.
- `High`: hard to reverse or broad blast radius. Use `references/high-stakes.md`; include commitment point, rollback/blast-radius risk, gaps, and flip conditions.

## Readiness

- `verifiably best`: option space is complete, material gaps are resolved/non-material, and ranking is stable.
- `best available`: current information supports the choice, but named gaps or conditions could still flip it.
