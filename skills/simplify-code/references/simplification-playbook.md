# Simplification Playbook

Follow after `simplify-code` triggers. Higher-priority `AGENTS.md` rules win.

## Checklist

1. Scope: require cleanup intent plus target. Ask once for plain `refactor`,
   vague maintainability, or missing target. Do not use this workflow for
   implementation, fixes, reviews, formatting-only work, redesigns, or routine
   self-review. If the useful change intentionally changes behavior, stop:
   `not a simplification: behavior change required`; explain benefit and
   consequence and ask whether to switch tasks.
2. Roots/status: run status first. Same-file unrelated changes block edits; ask
   whether to narrow scope, create backup and proceed carefully, or stop.
   Ignore/report unrelated dirty files elsewhere. Repo root is for git diff,
   rollback patch, and `.backup/`; target/project root is for instructions,
   config, formatter/linter, tests, and verification. Pick the nearest ancestor
   with local instructions or package config; if unclear, say so and use the
   explicit target root.
3. Boundaries: read-only unless explicitly opted in for migrations, schemas,
   persistence, auth/security, billing, permissions, data-loss,
   concurrency/locking, generated/vendor, dependency manifests, external/public
   contracts, release/packaging, and binaries. Sensitive paths also require
   strong evidence, baseline verification, and narrow scope; fast mode never
   bypasses this. Generated/vendor edits need confirmation, overwrite-risk
   warning, and generator/source preference. Do not edit binaries; ask for an
   asset workflow. Edit tests only
   when scoped or test-only; never relax expectations.
4. Broad scopes: do read-only reconnaissance. List candidate slices with files,
   call sites, simplification, risk, verification, and evidence label. Patch one
   coherent slice. Value order: defect risk, cognitive load, meaningful
   duplication, local patterns, test/debug ease, then aesthetic ride-alongs.
5. Evidence: default `weak`. `strong` = focused tests/probes cover changed
   behavior plus no public/external contract diff. `moderate` = tight reasoning
   plus independent typecheck, lint, snapshot, caller audit, or manual probe.
   `weak` = static-only, no independent check, missing risky baseline, or
   blocked verification. Weak requires approval before editing; ask whether to
   proceed, pick a safer slice, or stop. Baseline is
   required for broad, weak, high-risk-adjacent, and cheap obvious checks. For
   narrow moderate/strong edits, state attribution is weaker if skipped.
6. Backup: always create a pre-edit rollback patch at
   `<repo-root>/.backup/YYYYMMDD-HHMMSS-<branch-or-no-branch>-<scope-slug>-simplify-code.patch`.
   Create and ignore `.backup/`. Prefer `.gitignore` as separate setup; if
   dirty/blocked, use `.git/info/exclude`, then
   `/Users/jp/backup/<repo-or-dir-slug>/`. Stop only if no backup works.
   Include scoped editable files plus scoped untracked text when practical.
   Exclude/report unrelated, ignored, large/binary, secret-like, and
   generated/vendor files unless scoped. No post-change patch by default.
7. Patch/verify: keep tightly coupled files in one coherent patch; otherwise use
   sequential verified slices. Internal signatures may change only when all
   callers are scoped and evidence is strong; external contracts need opt-in.
   Add abstractions only for meaningful duplication or an existing stable domain
   concept; keep them small/local. Avoid restatement comments. Run
   formatter/linter only on touched files; stop if it expands scope.
8. Failure/closeout: if verification fails, do root-cause analysis first. Use
   baseline to separate pre-existing from new failure; fix only with clear
   cause/path. Leave changes unstaged unless asked or locally required.
   Closeout labels: `What changed`, `Why this was the chosen slice`,
   `Behavior-preservation evidence`, `Verification performed`, `Files changed`,
   `Remaining risks`, `Commit readiness`. Add a copy-ready read-only
   same-machine Codex/Claude review prompt with absolute paths, changed files,
   backup path, commands/results, behavior claim, evidence label, risks,
   exclusions, call-site inspection, evidence challenge, rollback-adequacy
   check, and blockers-first reporting. No rollback command.
