---
name: simplify-code
description: "Use when the user asks to simplify, tidy, clean up, or refactor code for clarity through a scoped behavior-preserving edit to a concrete target. Do not use for cleanup planning, backlog creation, new implementation, bug fixes, reviews, format-only changes, vague maintainability work, redesigns, or architecture-deepening surveys (`improve-codebase-architecture`)."
---

# Simplify Code

Behavior-preserving simplification for an explicit target. Before any edit, load [`references/simplification-playbook.md`](references/simplification-playbook.md) and follow it as the execution procedure.

## Use

Trigger only on cleanup intent plus target for an actual edit. Intent: simplify, clean up, tidy, make easier to read, refactor for clarity, or explicit behavior-preserving refactor. Target: paths/files, subsystem, current/staged diff, commit, or range. Diff, commit, and range targets are discovery inputs; expand them to explicit editable paths before patching.

Ask once to clarify a plain `refactor`, vague maintainability, or missing target. Do not use for implementation, fixes, reviews, formatting-only work, redesigns, routine self-review, cleanup planning, refactoring backlogs, or candidate prioritization. For planning/backlog requests, route to `tech-debt-scan`; for architecture-deepening surveys rather than a scoped edit, route to `improve-codebase-architecture`; use `simplify-code` after the user chooses a scoped behavior-preserving edit.

If a narrower platform, framework, or refactor skill owns the target, use that skill unless the user explicitly invokes `simplify-code` or asks for generic behavior-preserving cleanup outside the narrower skill's contract.

Status and applicable instructions first. Select either fast lane or full-safety lane before editing. Fast lane is only for clean tracked text files in a git repo with clean scoped pre-edit diff, `scripts/scoped_safety_scan.py` reporting `clean`, no protected/generated/vendor/secret-adjacent surface, small inspectable post-edit diff, and at least one runnable independent check. Fast lane uses the tracked git baseline as recovery and creates no backup artifact.

Use full-safety lane for dirty or untracked files, non-git roots, broad scopes, protected surfaces, weak verification, generated/vendor files, secret-adjacent files, or unclear fast-lane eligibility. Same-file unrelated changes, weak planned verification, possible secret content, generated/binary overwrite risk, or protected-surface risk require approval or stop. Full-safety lane creates a secret-safe, restorable pre-edit backup artifact before editing.

Read-only unless explicitly opted in after the exact risk property is named: migrations, schemas/persistence, security/auth/billing/permissions/data-loss, concurrency/locking, generated/vendor, dependency, package, plugin, app, project, or release manifests, external/public contracts, release/packaging, and binaries. Naming one of these paths as the target is not enough opt-in by itself. Behavior change is not simplification; stop and label it `not a simplification: behavior change required`, explain the benefit and consequence, and ask whether to switch tasks.

Broad scopes need reconnaissance first: patch and verify one high-value coherent slice, then report remaining candidates.

## Closeout

Closeout starts with:

- `Simplification Result`: what changed and why this slice was chosen.
- `Behavior Claim`: behavior-preservation claim plus evidence.
- `Verification`: commands/results, or why verification is weaker than desired.
- `Commit Readiness`: ready/not ready, with the blocking reason.
- `Review Packet`: details for follow-up review.

Keep the first four sections concise: user-visible result first, then evidence and readiness. `Review Packet` is the details section and includes files changed, remaining risks, exclusions, and lane-specific evidence. Always render the review packet content inside a fenced Markdown code block labelled `markdown`, even for compact fast-lane packets, so the user can copy it without reformatting. Fast-lane closeout adds a compact review hook with absolute paths, behavior-preservation claim, command/result, and why fast-lane eligibility held. Full-safety closeout keeps the copy-ready read-only same-machine Codex/Claude prompt under `Review Packet`, with absolute paths/files, claim, evidence, commands/results, planned verification strength, observed evidence label, backup helper command/result, backup path, retention/cleanup expectation, risks/exclusions, call-site inspection, evidence challenge, backup-adequacy check, and blockers-first review. No rollback command.

`Commit Readiness` and `Review Packet` must agree with the real index state. If no commit is requested or repo-required, say the scoped changes are intentionally unstaged and make any staging advice conditional for a future commit; do not ask reviewers to block on unstaged files as though that is an avoidable implementation defect. If commit-package review is requested, or if the review packet asks reviewers to verify staging, stage the complete scoped package first and report the cached file list as evidence.
