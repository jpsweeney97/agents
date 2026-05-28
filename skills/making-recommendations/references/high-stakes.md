# High-Stakes Recommendations

Load this only for high-stakes decisions: hard-to-reverse choices, broad blast radius, durable decision records, or when the user asks for a deeper recommendation.

## Extra Checks

- Include explicit `Commitment point` and `What could flip` sections unless the user asks for a very short answer.
- Define the commitment point: when the decision becomes costly to reverse.
- Name owners, affected systems or people, and rollback options.
- Separate must-have constraints from preferences.
- For each material unknown, state the cheapest check that could resolve it before commitment.
- For each non-recommended option, state the smallest realistic change that would make it win.
- Mark the result `best available` unless gaps are non-material or resolved.

## Durable Record

Write `docs/decisions/YYYY-MM-DD-<slug>.md` only when the user asks or the repo already uses decision records.

Use this structure:

1. Decision
2. Stakes and commitment point
3. Options, including null
4. Criteria
5. Information gaps
6. Evaluation
7. Sensitivity analysis
8. Ranked options
9. Recommendation
10. Readiness and upgrade conditions

After writing a record, summarize:

```markdown
**Recommendation:** [option]
**Why:** [2-3 sentences]
**Trade-offs accepted:** [costs]
**Readiness:** verifiably best / best available - [reason]
**Full analysis:** [link]
```
