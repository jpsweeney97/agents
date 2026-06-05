# High-Stakes Recommendations

Load this only for high-stakes decisions: hard-to-reverse choices, broad blast radius, durable decisions, or when the user asks for a deeper recommendation.

## Extra Checks

- Include explicit `Commitment Point`, `Rollback / Blast Radius`, and
  `Gaps / What Could Flip` sections unless the user asks for a very short
  answer.
- Define the commitment point: when the decision becomes costly to reverse.
- Name owners, affected systems or people, and rollback options.
- Separate must-have constraints from preferences.
- For each material unknown, state the cheapest check that could resolve it before commitment.
- For each non-recommended option, state the smallest realistic change that would make it win.
- Do not rank when options are not comparable, only one serious option exists,
  or a material missing detail would change the recommendation. Use the matching
  pre-ranking exit from `SKILL.md`.
- Mark the result `best available` unless gaps are non-material or resolved;
  use `not enough to recommend yet`, `decision needed`, or `options not
  comparable` when the high-stakes facts do not support a recommendation.
