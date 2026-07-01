# High-Stakes Recommendations

Load this only for high-stakes decisions: hard-to-reverse choices, broad blast radius, durable decisions, or when the user asks for a deeper recommendation.

## Extra Checks

- For the high-stakes risk sections (`Commitment Point`, `Rollback / Blast Radius`, `Gaps / What Could Flip`) and the rule to compress them into prose rather than silently dropping them in a very short answer, follow the Output section in `SKILL.md`.
- Define the commitment point: when the decision becomes costly to reverse.
- Name owners, affected systems or people, and rollback options.
- Separate must-have constraints from preferences.
- For each material unknown, state the cheapest check that could resolve it before commitment.
- For each non-recommended option, state the smallest realistic change that would make it win.
- Apply the Pre-Ranking Exits from `SKILL.md` (`options not comparable`, `only one serious option`, `material missing detail`) before ranking — high stakes does not loosen or tighten when they apply; re-read their definitions there rather than relying on a restated threshold here.
- Mark the result `best available` unless gaps are non-material or resolved; escalate to `not enough to recommend yet` only when no defensible ranking is possible at all (per `SKILL.md`'s Pre-Ranking Exits), to `decision needed` when a human values or ownership call controls the answer, or to `options not comparable` when the options need different criteria.
