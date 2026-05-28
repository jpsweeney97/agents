---
name: simplify-code
description: >-
  Use when user asks to simplify, clean up, tidy, or refactor-for-clarity code
  while preserving behavior. Do not use for implementation, fixes, reviews,
  format-only, vague maintainability, or redesigns.
---

# Simplify Code

Simplify scoped code while preserving behavior. No implicit cleanup.

## Use

Trigger: cleanup intent + target: paths/files, subsystem, current/staged diff,
or commit/range.

Clarify ambiguous `refactor` / `make maintainable` asks unless paired with
simplification, cleanup, clarity, or preservation.

Status first. Same-file unrelated changes stop editing; ask whether to narrow,
proceed with backup, or stop. Ignore/report other files.

Broad: reconnaissance; patch/verify one high-value slice; report other
candidates.

Monorepos: repo root for git/backup; target root for instructions/check.

## Gates

Value: rank by defect-risk reduction, cognitive load, duplication, local
patterns, test/debug ease, then aesthetic ride-alongs. Deprioritize taste-only
work.

Evidence: `strong` = tests/probes plus no public/external contract diff;
`moderate` = tight reasoning plus typecheck, lint, snapshot/caller audit, or
manual probe; `weak` = static-only, no independent check, missing baseline, or
blocked verification. Weak needs approval; no tests/type/lint means weak.

Baseline required for broad scopes, weak evidence, high-risk-adjacent slices,
cheap obvious checks.

Backup every edit to
`<repo-root>/.backup/YYYYMMDD-HHMMSS-<branch-or-no-branch>-<scope-slug>-simplify-code.patch`;
create `.backup/` and prefer `.gitignore` setup. If blocked/dirty, fall back to
`.git/info/exclude`, then `/Users/jp/backup/<repo-or-dir-slug>/`; stop if no
backup works. Include scoped editable/untracked text; exclude/report unrelated,
ignored, large/binary, secrets, generated/vendor unless scoped. No post patch by
default.

Read-only by default: migrations, schemas/persistence, security/auth/billing/
permission/data-loss, concurrency, generated/vendor, manifests, external
contracts, release/packaging, binaries.

Sensitive paths need opt-in, strong evidence, baseline, narrow scope; fast mode
cannot bypass. Internal APIs may change only when all callers are in scope and
evidence is strong. External contracts require opt-in.

Generated/vendor edits need confirmation; prefer generator/source. Do not edit
binaries; use asset workflow. Tests editable only when scoped or test-only;
never relax expectations. New abstractions must be small, local, evidence-backed,
and justified by duplication or a stable concept.

Intentional behavior change is not simplification. Stop and label it `not a
simplification: behavior change required`.

## Execute

Patch coupled in-scope files coherently; otherwise use verified slices. Avoid
half-migrations, restatement comments, and broad formatter/linter runs. Comment
only non-obvious intent, invariants, compatibility, constraints, or tradeoffs.

If verification fails, do root-cause analysis before test changes or rollback.
Adjust only when cause and repair path are clear; label pre-existing failures.

Do not auto-commit. Leave unstaged unless user asks or local instructions require
a commit.

## Closeout

Closeout: `What changed`, `Why this was the chosen slice`,
`Behavior-preservation evidence`, `Verification performed`, `Files changed`,
`Remaining risks`, `Commit readiness`, plus a copy-ready read-only same-machine
Codex/Claude prompt with absolute paths/files, claim, evidence, commands/results,
backup path, risks/exclusions, and blockers-first review. No
rollback command.
