# Skill-Library Backlog — Re-triaged Through the Judgment-vs-Trust Bar

Task 10 of `docs/plans/2026-06-15-judgment-trust-apparatus.md`. Re-dispositions every item in the source report's §6 Prioritized Remediation Backlog (`.agents/skill-library-scrutiny-2026-06-15.md`) through the judgment-vs-trust distinction now single-sourced in `agent-facing-design` (`## Two Kinds of Skill`). Grounded in §6 (the item list) plus §4 (verdict headlines) and §5 / §3.x (the evidence behind each item), not §6 alone.

## How to read this

- **Class** — the bar that governs the item: `trust`, `judgment`, `mixed`, `delivery` (delivery hygiene: invocation tokens, naming, Codex budget, parseability — uniform across both bars), `routing` (composability/One-Owner, reviewed on its own merits, not as a judgment-conformance nit), or `charter` (durable-record/delivery drift, lens-independent).
- **New disposition** — `preserve` (do as written; the bar does not touch it), `keep`, `escalate`, `drop`, `reverse`, or `split` (per part).
- **Tie-break tag** — `budget-driven` or `conformance-driven` is recorded wherever the budget-vs-conformance tie-break is live (per Task 10 step 2: an over-cap description on a judgment skill is *both*, and the budget reading wins while it is over the Codex cap — preserve as budget, drop the residual as conformance only once back under the cap). Items where neither reading applies are tagged `n/a — <class>`; forcing the binary onto a symlink fix or a trust reliability bug would be the improvisation the rule exists to prevent.
- **Evidence** — for every item whose disposition **changes** under the new bar, the originating §5 / §3.x finding plus a live skill line (verified this pass).

**Headline result:** the new bar relaxes **nothing** in P0 and almost nothing in P1 — every correctness/safety/reliability and delivery-hygiene item is preserved or kept, several escalated. The flips are concentrated in the judgment-conformance tail (P2 + rolled-up minors): the `system-design-review` numeric finding-cap, the `review-reviewer` section-order nit, and the over-cap-description trims, which are re-read as budget recovery rather than quality nits. One trust item escalates: the protected-branch gate duplicated across four skills moves from P2 polish to a real brittle-duplication finding.

## P0 — correctness/safety drift

| # | Item (skills) | Orig. | Class | New disp. | One-line reason | Tag | Evidence |
|---|---|---|---|---|---|---|---|
| 1 | Remove dangling symlink (jp-writing-style) | P0 | charter/delivery | preserve | Live broken symlink in the Claude delivery farm; lens-independent delivery drift | n/a — delivery | unchanged (§3.4 S1 / top-issue #1) |
| 2 | Reconcile ledger/archive (jp-writing-style) | P0 | charter | preserve | Durable record asserts a contract that does not exist on disk; charter health, lens-independent | n/a — charter | unchanged (§3.4 S2 / §3.5 G1) |
| 3 | Fix `@codex review` hardcode (gh-pr-review-loop) | P0 | trust | keep | Trust reliability: spurious public comment on non-Codex PRs — exactly the wrong-action failure the trust bar catches | n/a — trust | unchanged (§5 gh-pr-review-loop, SKILL.md:82-85) |
| 4 | Fix benchmark recipe (skill-benchmark) | P0 | trust | keep | Trust/mechanical: the literal copied recipe errors out before any init event; correct execution is the value | n/a — trust | unchanged (§5 skill-benchmark, SKILL.md:95-100) |
| 5 | Fix `$PROJECT_ROOT` snippets (search-handoffs) | P0 | trust | keep | Trust reliability: unset var → silent no-op; flip-set row 5 (keep) | n/a — trust | unchanged (§5 search-handoffs, SKILL.md:39,55) |
| 6 | Resolve fix-timing conflict (gh-address-comments) | P0 | trust | keep | Trust lifecycle: two passages give opposing literal instructions on the central act | n/a — trust | unchanged (§5 gh-address-comments, SKILL.md:71-74 vs 101-103) |

## P1 — followability & dual-runtime correctness

| # | Item (skills) | Orig. | Class | New disp. | One-line reason | Tag | Evidence |
|---|---|---|---|---|---|---|---|
| 7 | Dual-runtime tokens (load/save/search-handoffs) | P1 | delivery | preserve | Invocation-token hygiene is uniform across both bars | n/a — delivery | unchanged (§3.3 C1 / §5 load-handoff) |
| 8 | Dual-runtime token (caveman) | P1 | delivery | preserve | Same — `$caveman` missing; uniform token hygiene | n/a — delivery | unchanged (§3.3 C2) |
| 9 | Harness discovery tokens (behavior-smoke-test) | P1 | delivery | preserve | Dual-runtime tool-token hygiene (`tool_search`/`ToolSearch`); uniform | n/a — delivery | unchanged (§5 behavior-smoke-test, SKILL.md:71-74,80-82) |
| 10 | Subagent dispatch (execute-plan) | P1 | trust | keep | Trust followability: the mode default gates the whole contract yet detection/dispatch is unspecified (corroborated live this session — the executor had to choose mode unaided) | n/a — trust | unchanged (§5 execute-plan, SKILL.md:21-22) |
| 11 | Alias enum re-derivation (claude-code-docs) | P1 | trust (lookup) | keep | Trust/lookup reliability: silent wrong-bucket retrieval; flip-set row 8 (keep) | n/a — trust | unchanged (§5 claude-code-docs, SKILL.md:96-102) |
| 12 | Label-override delivery (setup-matt-pocock-skills) | P1 | trust | keep | Trust reliability: override path silently fails to deliver mapped strings → mismatched labels | n/a — trust | unchanged (§5 setup-matt-pocock-skills, SKILL.md:47-59,100-103) |
| 13 | Throughline staleness in load (load-handoff) | P1 | trust (dedup) | keep | Trust duplicated machinery: load-side reimplements throughline's source-set enumeration, drifting + heavier | n/a — trust | unchanged (§5 load-handoff, SKILL.md:65 vs throughline:43-57) |
| 14 | Codex budget accounting (AGENTS.md + 9 over-budget skills) | P1 | delivery/budget | preserve | Codex budget is uniform delivery hygiene; pin the ceiling and trim for budget, not quality | budget-driven | unchanged action; framing recorded (§3.2 D1) |

## P2 — routing symmetry, dedup, polish

| # | Item (skills) | Orig. | Class | New disp. | One-line reason | Tag | Evidence |
|---|---|---|---|---|---|---|---|
| 15 | Grilling-loop overlap (grill-me, grill-with-docs, improve-codebase-architecture) | P2 | routing | keep | Composability/One-Owner: two owners of the grilling loop, no cross-boundary — a real routing finding, not a judgment-conformance nit | n/a — routing | unchanged (§3.1 O1) |
| 16 | Protected-branch dedup (closeout-check, merge-branch, acceptance-map, git-hygiene) | P2 | trust | **keep + escalate** | Trust duplicated machinery — the same gate hand-copied into four skills is the canonical brittle-duplication the trust bar escalates; not P2 polish | n/a — trust | **CHANGED** (§3.1 O4): live `main`/`master`/`develop`/`release/*` gate at closeout-check:172, merge-branch:62, acceptance-map:226 (+ git-hygiene:18-22 per O4) |
| 17 | diagnose/tdd test-first seam (diagnose, tdd) | P2 | routing | keep | Composability/overlap: description vs body disagree on test-first ownership; a real routing seam | n/a — routing | unchanged (§3.1 O5, diagnose:92-105) |
| 18 | markdown-synthesis/throughline (markdown-synthesis) | P2 | routing | keep | Composability/overlap: missing arc-synthesis non-use boundary; real routing asymmetry | n/a — routing | unchanged (§3.1 O9) |
| 19 | Stakes ternary (system-design-review) | P2 | judgment | **reverse** | Judgment-conformance: "complete the low/med/high rule" asks a thinking skill to finish a numeric finding-cap dial; the new bar questions whether the cap belongs, not completes it; flip-set row 2 | conformance-driven | **CHANGED** (§5 system-design-review; SKILL.md:33): live cap table `system-design-dimensions.md:39` ("Finding targets: low 3-5 … Hard caps: low 6, medium 9, high 12") — capping a reviewer's finding count is substitutive structure on a judgment skill |
| 20 | review-family section order (review-reviewer) | P2 | judgment | **drop** | Judgment-conformance: matching sibling section order is cosmetic uniformity with no effect on adjudication quality (mild routing-aid counterpoint noted, not decisive) | conformance-driven | **CHANGED** (§3.3 C4): live `## Review-Family Routing` at review-reviewer:42, below `## Boundaries`:12, vs siblings leading with it — section-ordering does not make the judgment for the agent |
| 21 | Description trims (orient-status, gh-pr-review-loop, + 9 over-cap: skill-benchmark, baseline, gh-address-comments, making-recommendations, outcome-interviewer, skill-ux-design, agent-facing-design, improve-codebase-architecture, tdd) | P2 | judgment / budget | **preserve (as budget)** | Budget/conformance tie-break: over-cap descriptions are both; while over the Codex cap the budget reading wins, so the trim is preserved as cheapest budget recovery, **not** dropped as a judgment-conformance nit; the conformance-only residual drops once each is back under cap | budget-driven (while over cap) | **CHANGED framing** (§3.2 D2 char/word counts; D1 aggregate at ceiling) — the trim survives, but as budget, not quality |
| 22 | Misc per-skill minors (many) | P2 | mixed | **split per part** | Apply the bar per minor when each skill is next touched: trust/delivery minors keep, judgment-conformance minors drop/reverse. Named examples that **drop/reverse**: the `scrutinize` verdict-token casing nit (cosmetic; flip-set row 1) and the `tdd` "no closure/done condition/output shape" minor (absence of a mandated output shape is correct for a judgment skill; flip-set row 3) | conformance-driven (for the judgment-conformance subset) | **CHANGED for the judgment-conformance subset** (§4: scrutinize "verdict-token casing"; tdd "no closure/output shape (impact minor)") — no effect on critique/build quality |

## What flipped, and why it matters

- **Nothing in P0/P1 relaxed.** Every reliability, correctness, lifecycle, and delivery-hygiene item is preserved or kept. The judgment bar is not a leniency dial — it drops *conformance* pressure on thinking skills, never reliability pressure on trust skills. (Trust rows 3–6, 11–13 and delivery rows 1–2, 7–9, 14 all stand.)
- **One escalation (item 16).** Under conformance, the protected-branch gate duplicated 4× read as P2 dedup polish. Under the trust bar, single-sourced machinery *is* the value and copied-and-drifting machinery is real brittleness — so it escalates, not drops.
- **The genuine drops/reverses are judgment-conformance (items 19, 20, 22).** A numeric finding-cap, a section-order uniformity nit, and cosmetic/output-shape minors on thinking skills — exactly the over-flagging the apparatus exists to stop. These match flip-set rows 1–3 (the conformance-drop axis).
- **The tie-break did real work (items 14, 21).** Over-cap descriptions on judgment skills (making-recommendations 63w, outcome-interviewer 62w, agent-facing-design 61w, tdd 61w, …) are *not* dropped as conformance nits while over the Codex cap — the trim is preserved as the cheapest budget recovery, with only the post-cap residual dropping. Budget hygiene stays uniform; quality conformance does not.

This artifact closes the loop from "apparatus learned" toward "pain relieved": it is the filtered worklist the Follow-on `to-issues` slice draws from once Task 9 proves the apparatus.
