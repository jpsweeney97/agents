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
- Include the null option only if it is distinct from the named options and
  material to the decision.
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

## Options Not Comparable

User asks:

```markdown
Should we optimize the docs site for polished marketing pages or for dense API
reference lookup?
```

Expected behavior:

- Do not rank the options as if they share one success criterion.
- State that the options are not comparable because they optimize for different
  user outcomes.
- Ask the decision-frame question, such as whether the current decision is about
  conversion, developer speed, support load, or another outcome.
- Mark readiness `options not comparable`.

## Only One Serious Option

User asks:

```markdown
Should we keep the current local-only workflow, or add a network service, if the
tool must keep working fully offline?
```

Expected behavior:

- Treat the network service as non-serious under the stated offline constraint.
- Do not invent a weak third option just to create a ranking.
- Recommend the local-only workflow if the offline constraint stands, or name
  the check that could reveal a second serious option.
- Mark readiness `best available` unless the offline constraint itself is still
  unverified or negotiable.

## Muddy Design Request With Permissioned Handoff

User asks:

```markdown
What's the best way to build a collaboration dashboard?
```

Expected behavior:

- Do not force a ranked recommendation from this prompt.
- Name why `making-recommendations` cannot proceed yet: the prompt asks for
  design exploration before serious options exist.
- Name `outcome-interviewer` if the user's desired outcome is unclear.
- Name `design-exploration` if the outcome is clear enough but approaches
  still need design exploration.
- Ask before switching lanes, then stop. For example: "This is not ready for a
  recommendation yet because there are not comparable approaches on the table.
  `design-exploration` is the better lane to shape those approaches. Do you
  want me to switch into that?"
- Use `making-recommendations` only after there are serious approaches to
  compare, such as server-rendered dashboard, client-heavy dashboard, or embedded
  analytics surface.
