# Severity, Leverage, And Effort Rubric

Severity: `P0` bleeding today; `P1` compounding; `P2` latent; `P3` cosmetic.
If >30% are `P0`, name today's cost and demote future risk.

Leverage: `high` unblocks 2+ findings/cause; `medium` removes one downstream
pain; `low` self-contained. Effort: `small` <1 day; `medium` 1-5 days; `large`
>1 week/cross-module/breaking/coordinated. Round up uncertainty.

Buckets: `quick-wins` = `P0`/`P1` + `small`; `high-leverage` = `high` +
`small`/`medium`; `strategic` = `P0`/`P1` + `large`; `watch` = `P2` or useful
`P3`. Drop non-debt observations.

Default artifact report order: Result Brief; Scan Snapshot; Focus & Coverage;
Evidence Trail; Ranked Backlog; Quick Wins; High-Leverage Fixes; Strategic
Items; Watch List; Tradeoff Map; Coverage Gaps / Next Probes; Metrics; Fidelity
Check. Result Brief contains `Top Debt Calls`, `Do First`, `Why It Matters`,
`Audit Path`, and `Coverage Limits`.

Chat summary order: Result Brief only, plus the artifact path. Do not reproduce
the full backlog in chat unless the user explicitly asks.

Finding fields: `id`, `severity`, `category`, `subcategory`, `anchor`,
`problem`, `impact`, `recommendation`, `effort`, `leverage`, `confidence`,
`corroboration`, `evidence_sources`, optional `cross_link`, optional
`next_probe`. Prefixes: `CH`, `AD`, `DP`, `TD`, `OP`, `KN`, `SY`.

Top-call gate: each `Top Debt Calls` entry needs `evidence_corroborated`, at
least two evidence sources or independently observed signals, and a present-tense
cost. Singleton evidence may be a finding, watch item, coverage gap, or next
probe, but not a top call.

Caps: low 4-8/10; medium 8-15/18; high 12-20/24. If capped with material
findings left, label truncated and name the next continuation slice.

Metrics: raw/canonical findings, merged clusters, corroborated count,
contradictions, skipped categories, singleton count, quick wins, strategic
items, tradeoffs.

Sanity: >50% quick-wins means low effort; >30% strategic means high severity;
zero high-stakes quick wins needs small-fix pass; >40% watch means observation
leakage.

Fidelity: before writing, compare each report `anchor`, `recommendation`, and
top-call summary with the evidence trail; restore drifted symbols, paths, flags,
config, qualifiers, and confidence limits.
