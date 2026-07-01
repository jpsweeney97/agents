# Recommendation Behavior Examples

Use these examples to calibrate routing, output shape, and honest exits. They are illustrative, not templates.

## Normal Comparison

User asks:

```markdown
Should we keep the current Markdown parser or switch to `markdown-it` for this
small docs tool?
```

Expected behavior:

- Treat this as a recommendation request because the user is choosing between viable options.
- Include the null option only if it is distinct from the named options and material to the decision.
- Rank by the user's constraints and obvious failure modes, such as maintenance cost, plugin support, compatibility, and migration risk.
- Recommend one option if the evidence supports it.
- Mark readiness `best available` if compatibility or package-state details were not verified.

## Multi-Criteria Comparison With A Tradeoff Matrix

User asks:

```markdown
Should we use Postgres, MySQL, or SQLite for this new multi-tenant SaaS app?
Weigh cost, our team's ops familiarity, and scaling headroom.
```

Expected behavior:

- Score each database on one criterion at a time across all three options (cost first for all three, then ops familiarity for all three, then scaling headroom for all three) before forming any overall impression — do not evaluate Postgres start-to-finish, then MySQL, then SQLite.
- State the basis for each criterion's scale, such as "ops familiarity scored against this team's current stack experience," so the score is reproducible.
- Because three criteria are scored, render `Ranking` as a tradeoff matrix: rows are Postgres/MySQL/SQLite, columns are cost/ops familiarity/scaling headroom, cells are the per-criterion scores.
- Name the weighting basis used to turn the matrix into a single ranking (for example, "ops familiarity weighted highest because the team ships faster on familiar tooling"), so the user can see it and reweight if they disagree.
- Recommend one option only if the weighted ranking is stable; otherwise mark `decision needed` if the weighting itself is a values call the user should make.

## High-Stakes Decision With Gaps

User asks:

```markdown
Should we migrate the production billing database this weekend or wait for the
next release window?
```

Expected behavior:

- Treat this as high stakes because reversal is costly and the blast radius is broad.
- Include `Commitment Point` and `Rollback / Blast Radius`.
- Name owners, affected users or systems, rollback options, and the cheapest checks that could resolve material unknowns.
- Use `not enough to recommend yet` only if the core safety facts — backup validation and rollback rehearsal — are both unconfirmed: without them there is no defensible basis to weigh the risk at all. If those are known and only a secondary fact like incident staffing or the release-window timing is unconfirmed, proceed with that as a stated assumption, name it under `Gaps / What Could Flip`, and mark `decision needed` or `best available` instead.
- Use `decision needed` when the evidence is clear but the answer depends on business risk tolerance or ownership.

## Options Not Comparable

User asks:

```markdown
Should we optimize the docs site for polished marketing pages or for dense API
reference lookup?
```

Expected behavior:

- Do not rank the options as if they share one success criterion.
- State that the options are not comparable because they optimize for different user outcomes.
- Ask the decision-frame question, such as whether the current decision is about conversion, developer speed, support load, or another outcome.
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
- Recommend the local-only workflow if the offline constraint stands, or name the check that could reveal a second serious option.
- Mark readiness `best available` unless the offline constraint itself is still unverified or negotiable.

## Partial Information — Rank With Stated Assumptions, Don't Bail

User asks:

```markdown
We can only ship ONE of these two features this sprint, not both — should we
build the CSV export or the bulk-delete feature?
```

Expected behavior:

- Notice that real criteria are available even though the deciding business fact (which feature users actually need most right now) is missing: build effort, risk profile (bulk-delete is destructive and typically needs confirmation/undo/audit-log work; CSV export is usually additive and self-contained), and failure-mode severity.
- Do not invoke `material missing detail` just because one fact (demand or urgency) is unknown — a defensible ranking is still possible on the criteria that are available, so this is not the "no defensible basis at all" case the exit is reserved for.
- State the missing fact as an assumption up front, evaluate criterion-by-criterion on what is known, and produce a real `Ranking` and `Recommendation`.
- Mark readiness `decision needed` (the unresolved factor is a values/priority call a human should make) or `best available` (the named gaps don't block a defensible call), not `not enough to recommend yet`.
- Name the missing fact in `Gaps / What Could Flip` so the user can override the call with the one piece of information that would change it.

## Muddy Design Request With Permissioned Handoff

User asks:

```markdown
What's the best way to build a collaboration dashboard?
```

Expected behavior:

- Do not force a ranked recommendation from this prompt.
- Name why `making-recommendations` cannot proceed yet: the prompt asks for design exploration before serious options exist.
- Name `outcome-interviewer` if the user's desired outcome is unclear.
- Name `design-exploration` if the outcome is clear enough but approaches still need design exploration.
- Ask before switching lanes, then stop. For example: "This is not ready for a recommendation yet because there are not comparable approaches on the table. `design-exploration` is the better lane to shape those approaches. Do you want me to switch into that?"
- Use `making-recommendations` only after there are serious approaches to compare, such as server-rendered dashboard, client-heavy dashboard, or embedded analytics surface.

## Descope Request Misread As Ranking

User asks:

```markdown
We're not going to hit the deadline with everything in this release. What
should we cut?
```

Expected behavior:

- Recognize this is not a pick-one ranking among rival options — every feature in the release is a candidate for keep, defer, or cut against the deadline, and more than one can survive.
- Do not silently rank the features as if only one could "win."
- Name `scope-cut` as the better lane: it partitions one scope into keep/defer/cut against a binding constraint (here, the deadline) and preserves every cut item with a re-entry condition, instead of forcing a single winner.
- Ask before switching, then stop. For example: "This reads as a descope under a deadline, not a choice between rival options — `scope-cut` is built for partitioning one scope into keep/defer/cut and keeping a re-entry ledger for what's deferred. Do you want me to switch into that?"
- Use `making-recommendations` instead only if the real ask turns out to be choosing one approach among genuinely rival options (for example, "should we cut feature A or feature B, not both" when only one slot exists), not partitioning the whole release.
