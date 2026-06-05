# Recommendation Behavior Examples

Use these examples to calibrate routing, output shape, and honest exits. They are
illustrative, not templates.

## Normal Comparison

User asks:

```markdown
Should we keep the current Markdown parser or switch to `markdown-it` for this
small docs tool?
```

Expected behavior:

- Treat this as a recommendation request because the user is choosing between
  viable options.
- Include the null option if distinct from the named options.
- Rank by the user's constraints and obvious failure modes, such as maintenance
  cost, plugin support, compatibility, and migration risk.
- Recommend one option if the evidence supports it.
- Mark readiness `best available` if compatibility or package-state details were
  not verified.

## High-Stakes Decision With Gaps

User asks:

```markdown
Should we migrate the production billing database this weekend or wait for the
next release window?
```

Expected behavior:

- Treat this as high stakes because reversal is costly and the blast radius is
  broad.
- Include `Commitment Point` and `Rollback / Blast Radius`.
- Name owners, affected users or systems, rollback options, and the cheapest
  checks that could resolve material unknowns.
- Use `not enough to recommend yet` if backup validation, rollback rehearsal,
  incident staffing, or release-window constraints are missing and could flip the
  decision.
- Use `decision needed` when the evidence is clear but the answer depends on
  business risk tolerance or ownership.

## Routing Or Handoff

User asks:

```markdown
What's the best way to build a collaboration dashboard?
```

Expected behavior:

- Do not force a ranked recommendation from this prompt.
- If the user's desired outcome is unclear, hand off to `outcome-interviewer`.
- If the outcome is clear but approaches need design exploration, hand off to
  `superpowers:brainstorming`.
- Use `making-recommendations` only after there are serious approaches to
  compare, such as server-rendered dashboard, client-heavy dashboard, or embedded
  analytics surface.
