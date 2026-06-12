# Contract Decisions

Ledger required by the charter's Decision Record section (`charter.md`): one
entry per admission, fold, rejection, park, or retirement — date, surface,
outcome, evidence pointer, and the reopen trigger for parks. Append new
entries; do not rewrite settled ones.

## Decisions

- 2026-06-12 — superpowers (pass 1): folded into `tdd` (+`mocking.md`),
  `diagnose`, `behavior-smoke-test`, and a global evidence-before-claims rule;
  admitted `design-exploration`, `implementation-planning`, `execute-plan`;
  requesting-review meta-skill rejected (collides with review lanes;
  checkpoint habit folded into `closeout-check`). Plugin removed. Evidence:
  commits `360fc77`, `966f903`, `d7351ec`.
- 2026-06-12 — commit-commands (pass 2): folded `[gone]` deletion-candidate
  discipline and a squash-merge proof path into `git-hygiene`;
  `commit`/`commit-push-pr` rejected (one-message/no-review mandates weaker
  than house discipline). Plugin removed. Evidence: commit `3b4cbc1`.
- 2026-06-12 — pr-review-toolkit + code-simplifier rider (pass 3): folded
  error-suppression and test-inadequacy lenses into `implementation-review`
  (review-family 0.3.2) and a clarity-over-brevity guardrail into
  `simplify-code`; six agent lanes rejected (numeric confidence/criticality
  scoring is rejected machinery; foreign CLAUDE.md leakage). Both plugins
  removed. Evidence: commit `5f64a54`.
- 2026-06-12 — feature-dev (pass 4): folded exploration grounding into
  `design-exploration` (read subagent-named key files first-hand before
  designing); command and three agents rejected (lane decomposition owns the
  workflow; settled no-numeric-confidence precedent). Plugin removed.
  Evidence: commit `2dc1b95`.
- 2026-06-12 — hookify (pass 5): zero folds — engine adjudicated capability
  tooling (charter-exempt as a category) but removed as unused; all six
  contract surfaces rejected (runtime-bundled `update-config` owns hook-backed
  automation). Plugin removed. Evidence: handoff
  `2026-06-12_18-35-34_feature-dev-hookify-mined-charter-amended-audit-reopens.md`.
- 2026-06-12 — discard audit (after the route-absence amendment, `6f7833d`):
  reopened two prior rejections — comment-accuracy lens folded into
  `implementation-review` (review-family 0.3.3, commit `1d0091a`);
  `friction-to-guards` admitted Claude-only in `skills-claude/` (commit
  `a5e6642`). All other prior discards held.
- 2026-06-12 — gh-address-comments: admitted (owns PR-comment addressing
  without publish authority); authoring deferred, tracked as
  jpsweeney97/agents#2.

## Parks

- type-design invariant lens — parked by JP's explicit choice (2026-06-12);
  reopen only on JP's ask.
- feature-dev approach-triad example — parked by JP's explicit choice
  (2026-06-12); reopen only on JP's ask.
- code-comprehension lane — parked (2026-06-12); reopen on an observed
  comprehension failure in real work.

## Mining Queue

Unmined contract-shipping surfaces, on amended charter terms (rejection
evidence named per discard):

1. frontend-design (next)
2. claude-code-setup
3. skill-creator
4. code-review (ships `commands/`; in active use)
5. security-guidance (hook-injected instruction text)
6. explanatory-output-style (hook-injected instruction text)

Unassessed: the `github` plugin — verify whether it ships contract text beyond
MCP tooling before queueing or exempting it.
