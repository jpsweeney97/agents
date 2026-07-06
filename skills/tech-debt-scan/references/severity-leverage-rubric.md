# Severity, Leverage, And Effort Rubric

Severity: `P0` bleeding today; `P1` compounding; `P2` latent; `P3` cosmetic. If >30% are `P0`, name today's cost and demote future risk.

Leverage: `high` unblocks 2+ findings/cause; `medium` removes one downstream pain; `low` self-contained. Effort: `small` <1 day; `medium` 1-5 days; `large`
> 1 week/cross-module/breaking/coordinated. Round up uncertainty.

Buckets: `quick-wins` = `P0`/`P1` + `small`; `high-leverage` = `high` + `small`/`medium`; `strategic` = `P0`/`P1` + `large`; `watch` = `P2` or useful `P3`. Drop non-debt observations.

Use `audit-report-template.md` for the artifact status lifecycle, section order, finding field template, metrics packet, and fidelity check. For the Result Brief roster and per-field descriptions, follow SKILL.md (Output).

Chat summary order: Result Brief only, plus the artifact path. Do not reproduce the full backlog in chat unless the user explicitly asks.

Finding id prefixes: `CH`, `AD`, `DP`, `TD`, `OP`, `KN`, `SY`.

Top-call gate: see SKILL.md (Synthesize) — a `Top Debt Calls` entry needs `evidence_corroborated`, two distinct source classes or independently observed signals, and a present-tense cost; singleton evidence may be a finding, watch item, coverage gap, or next probe, but not a top call. `evidence_corroborated` here means breadth — distinct source classes read by the same judge — not independence between separate minds; a top call is multiply-sourced, not independently confirmed.

Caps: base depth caps and the truncation rule are in SKILL.md (Output); the raw-vs-canonical ceiling before canonicalization is low /10, medium /18, high /24.

Metrics: raw/canonical findings, merged clusters, corroborated count, contradictions, skipped categories, singleton count, quick wins, strategic items, tradeoffs. The Metrics packet is local-run synthesis metadata, not durable proof and not audit evidence; the findings' warrant is the Evidence Trail, not these counts.

Sanity: >50% quick-wins means low effort; >30% strategic means high severity; zero high-stakes quick wins needs small-fix pass; >40% watch means observation leakage.

Fidelity: before marking the artifact complete, compare each report `anchor`, `recommendation`, and top-call summary with the evidence trail; restore drifted symbols, paths, flags, config, qualifiers, and confidence limits.
