# Severity, Leverage, And Effort Rubric

Severity: `P0` bleeding today; `P1` compounding; `P2` latent; `P3` cosmetic.
If >30% are `P0`, name today's cost and demote future risk.

Leverage: `high` unblocks 2+ findings/cause; `medium` removes one downstream
pain; `low` self-contained. Effort: `small` <1 day; `medium` 1-5 days; `large`
>1 week/cross-module/breaking/coordinated. Round up uncertainty.

Buckets: `quick-wins` = `P0`/`P1` + `small`; `high-leverage` = `high` +
`small`/`medium`; `strategic` = `P0`/`P1` + `large`; `watch` = `P2` or useful
`P3`. Drop non-debt observations.

Default chat report order: Result Brief; Details. Result Brief contains `Top
Debt Calls`, `Do First`, `Why It Matters`, and `Coverage Limits`. Details
preserves these report sections: Scan Snapshot; Focus & Coverage; Quick Wins;
High-Leverage Fixes; Strategic Items; Watch List; Tradeoff Map; Open Questions /
Next Probes.

Finding fields: `id`, `severity`, `category`, `subcategory`, `anchor`,
`problem`, `impact`, `recommendation`, `effort`, `leverage`, `confidence`,
`corroboration`, optional `evidence_sources`, optional `cross_link`. Prefixes:
`CH`, `AD`, `DP`, `TD`, `OP`, `KN`, `SY`.

Caps: low 4-8/10; medium 8-15/18; high 12-20/24. If capped with material
findings left, label truncated and recommend `tech-debt-audit`.

Metrics: raw/canonical findings, merged clusters, corroborated count,
contradictions, skipped categories, quick wins, strategic items, tradeoffs.

Sanity: >50% quick-wins means low effort; >30% strategic means high severity;
zero high-stakes quick wins needs small-fix pass; >40% watch means observation
leakage.

Fidelity: before writing, compare each report `anchor` and `recommendation` with
the first finding; restore drifted symbols, paths, flags, config, qualifiers.
