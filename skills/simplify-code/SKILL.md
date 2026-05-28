---
name: simplify-code
description: >-
  Use when user asks to simplify, clean up, tidy, or refactor-for-clarity code
  while preserving behavior. Do not use for implementation, fixes, reviews,
  format-only, vague maintainability, or redesigns.
---

# Simplify Code

Behavior-preserving simplification for an explicit target. Before any edit, load
[`references/simplification-playbook.md`](references/simplification-playbook.md)
and follow it as the execution procedure.

## Use

Trigger only on cleanup intent plus target. Intent: simplify, clean up,
tidy, make easier to read, refactor for clarity, or explicit
behavior-preserving refactor. Target: paths/files, subsystem, current/staged
diff, commit, or range.

Clarify plain `refactor`, vague maintainability, or missing target. Do not use
for implementation, fixes, reviews, formatting-only work, redesigns, or routine
self-review.

Status first. Same-file unrelated changes stop editing. Weak evidence needs
approval. Always create a pre-edit rollback patch. Do not auto-commit unless
asked or locally required.

Read-only unless opted in: migrations, schemas/persistence, security/auth/
billing/permissions/data-loss, concurrency, generated/vendor, manifests,
external contracts, release/packaging, and binaries. Behavior change is not
simplification; stop and label it `not a simplification: behavior change
required`.

Broad scopes need reconnaissance first: patch and verify one high-value coherent
slice, then report remaining candidates.

## Closeout

Closeout: `What changed`, `Why this was the chosen slice`,
`Behavior-preservation evidence`, `Verification performed`, `Files changed`,
`Remaining risks`, `Commit readiness`, plus a copy-ready read-only same-machine
Codex/Claude prompt with absolute paths/files, claim, evidence, commands/results,
backup path, risks/exclusions, and blockers-first review. No
rollback command.
