# Conciseness Audit — Dispositions

Date: 2026-07-13. JP's decisions on the same-day audit (`2026-07-13-skill-body-conciseness-audit.md`). This is the governing record for the conciseness campaign; the skill edits under it are ordinary build-and-prune churn, not charter events.

## Decisions

- **Green-lit workstreams**: (1) reference-offload of inline lookup payloads (audit pattern 17), (2) neighbor-fence prune (pattern 4), (3) within-file single-sourcing of echoed obligations and restating recap gates (patterns 2 and 15), (4) authoring-lane guards against patch-accretion and template gravity (root causes 3 and 4), landed in `writing-principles` and `agent-facing-design`.
- **Stance prose accepted as-is, no action**: the house voice, x-not-y contrast, failure-mode-inoculation, proof-boundary-liturgy, and the self-containment doctrine copies (root causes 2 and 5 where they are register rather than duplication). Revisit only on specific misfire evidence, or via `contract-evaluation-methodology` if a cluster's value ever becomes the open question.
- **Fence policy — evidence-gated**: a body fence (a "vs `skill`" bullet, boundaries section entry, or routing preamble) survives only with observed misroute or stolen-fire evidence — an origin commit or recorded incident citing a real misroute, or ledger-informed collision history. Speculative fences prune. Frontmatter descriptions keep their selection-critical exclusions per `AGENTS.md`; this policy governs body prose only.
- **Non-goals**: no trimming of label taxonomies, output-packet specs, prohibition inventories, or contingency ladders except where a green-lit workstream incidentally touches one; no frontmatter/routing changes.

## Method notes

- The audit's per-file census artifacts are unrecoverable, so campaign targets are re-identified mechanically (body word counts, fence-section greps, origin-commit looks) anchored on the audit's named files.
- Single-sourcing respects the fire-time-surface convention: restatement that defends a partial read at a genuine landing site may stay; the target is copies with no such job.
- Offloads follow the `git-hygiene` model: payload moves to `references/` named by purpose, with an explicit load trigger in the body.

## Fence-prune evidence record

Origin-look results (git history sweep, 2026-07-13). Fences kept on evidence: the 2026-06-15 collision-sweep winner clauses in `tdd`↔`diagnose`, `simplify-code`↔`improve-codebase-architecture`, `triage`→`to-prd`/`to-issues`, `closeout-check`→`gh-address-comments` (85fa0e1, forward-tested routing collisions); `skill-ux-design`'s authoring-consult routing (b526673, observed misroute); `orient-status`'s clarify-gate failure shape (b41d636, observed); `implementation-planning`'s outside-view fence clause (9b70de8, forward-tested at addition). Judgment refinement applied at execution: an actionable mid-fire redirect ("if the target turns out to be X, switch to `sibling`") is workflow contingency rather than fence — compressed to its action and kept. All other examined fences — the advisory-family boundary skeleton (2583597, 844094f, 1c4aa17), `migration-safety` vs `migration-campaign` (904ad55), `dependency-upgrade`'s collision bullet (ae5f916), the review-family Routing sections and `review-reviewer`/`orient-status` non-trigger lists (047c8ca) — trace to birth or canonicalization commits as design-time carve rationale with no observed misroute; the advisory family has fired ~7 times globally per the usage ledger. These prune.
