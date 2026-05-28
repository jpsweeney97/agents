# Simplification Playbook

Follow after `simplify-code` triggers. Higher-priority `AGENTS.md` rules win.

## Checklist

1. Scope and target: require cleanup intent plus target. Ask once for plain
   `refactor`, vague maintainability, or missing target. Do not use this workflow
   for implementation, fixes, reviews, formatting-only work, redesigns, or routine
   self-review. If the useful change intentionally changes behavior, stop:
   `not a simplification: behavior change required`; explain benefit and
   consequence and ask whether to switch tasks. Treat current/staged diff,
   commit, and range targets as discovery inputs only. Before editing, expand
   them to explicit editable paths, report the expansion, and apply the rest of
   this checklist to those paths. For staged-diff targets, record pre-edit index
   state and leave new edits unstaged unless the user explicitly asks to stage or
   restage them; never rewrite existing staged hunks without approval.
2. Roots/instructions/status: run status first. From the target directory, or the
   parent directory for a file target, run `git rev-parse --show-toplevel`; if it
   fails, use the explicit target root as a non-git root and state that git
   diff/status evidence is unavailable. Before planning edits, discover and read
   applicable instructions: repo-root `AGENTS.md`, any nearer `AGENTS.md` between
   the root and target path, and local package/tool config that controls
   formatter, linter, tests, or generated files. In a git repo, run
   `git status --short --branch` from the repo root and use path-limited checks:
   `git diff -- <paths>`, `git diff --cached -- <paths>`, and
   `git ls-files --others --exclude-standard -- <paths>`. Same-file unrelated
   changes block edits by default.
   Partial-scope opt-in requires user approval, exact hunks or regions, a
   whole-file backup, and a before/after preservation check showing unrelated
   edits remain untouched. Ignore/report unrelated dirty files elsewhere. Repo
   root is for git evidence and `.backup/`; target/project root is for
   instructions, config, formatter/linter, tests, and verification. Pick the
   nearest ancestor with local instructions or package config; if unclear, say
   so and use the explicit target root.
3. Boundaries and opt-in: read-only unless explicitly opted in for migrations,
   schemas, persistence, auth/security, billing, permissions, data-loss,
   concurrency/locking, generated/vendor, dependency, package, plugin, app,
   project, or release manifests, external/public contracts, release/packaging,
   and binaries. Explicit opt-in means the user authorizes edits to the named
   protected surface after you state the risk, narrow scope, and verification
   plan; merely naming a protected path as the target is not enough. Sensitive
   paths also require a strong verification plan, baseline verification, and
   narrow scope; fast mode never bypasses this. Generated/vendor edits need
   confirmation, overwrite-risk warning, and generator/source preference. Do not
   edit binaries; ask for an asset workflow. Edit tests only when scoped or
   test-only; never relax expectations.
4. Broad scopes: do read-only reconnaissance. List candidate slices with files,
   call sites, simplification, risk, and planned verification strength. Patch
   one coherent slice. Value order: defect risk, cognitive load, meaningful
   duplication, local patterns, test/debug ease, then aesthetic ride-alongs.
5. Verification plan and evidence: before editing, assign planned verification
   strength. `strong plan` = focused tests/probes already cover the changed
   behavior or can be run, needed baselines are available, and no
   public/external contract diff is expected. `moderate plan` = tight reasoning
   plus an independent typecheck, lint, snapshot, caller audit, or manual probe
   can cover the changed surface. `weak plan` = static review only, no
   independent check, missing risky baseline, blocked verification, or
   high-risk-adjacent work without focused coverage. Weak planned verification
   requires approval before editing; ask whether to proceed, pick a safer slice,
   or stop. Baseline is required for broad, weak-plan, high-risk-adjacent, and
   cheap obvious checks. For narrow moderate/strong-plan edits, state attribution
   is weaker if baseline was skipped. After editing, report observed
   behavior-preservation evidence separately as `strong`, `moderate`, or `weak`
   based only on checks actually run and results observed. Do not present
   lint/typecheck-only results or caller audit alone as behavioral proof; label
   them as static or structural support unless a behavior-focused test, snapshot,
   probe, or equivalent manual check exercised the changed behavior.
6. Backup: always create a secret-safe pre-edit backup artifact at
   `<repo-root>/.backup/YYYYMMDD-HHMMSS-<branch-or-no-branch>-<scope-slug>-simplify-code/`
   or, outside git, `/Users/jp/backup/<repo-or-dir-slug>/YYYYMMDD-HHMMSS-<scope-slug>-simplify-code/`
   after verifying the backup root is writable. If the outside-git backup root is
   unavailable or outside the writable sandbox, ask for approval of a writable
   backup location or stop before editing. `Restorable` means every edited text
   file can be reconstructed from copied pre-edit content; files excluded from
   backup are not restorable from the artifact and require explicit user approval
   before editing.
   The artifact must include `manifest.txt` with root, branch or `no-git`, HEAD
   when available, scoped editable paths, excluded paths with reasons and restore
   limits, planned verification strength, and SHA-256 hashes for copied original
   files. For each scoped editable text file, copy the full pre-edit file under
   `files/<relative-path>` unless secret-safety blocks content copy; for scoped
   untracked text, copy the full file when practical. Never copy secret-like
   content, credentials, tokens, private keys, or similarly sensitive scoped
   content into `.backup/` or `/Users/jp/backup` by default. For those files,
   stop and ask for a secure backup mode: user-approved secure location, redacted
   manifest plus hashes only, or exclusion with explicit acknowledgement that the
   file will not be restorable from the artifact.
   In git repos, also save pre-edit `status.txt`, scoped `diff.patch`, scoped
   `cached.diff.patch` when staged changes exist, and scoped `untracked.txt`.
   Use `git rev-parse --git-path info/exclude` to locate the repo-local exclude
   file and add `.backup/` there when missing. Do not edit tracked `.gitignore`
   solely to ignore backup artifacts. Exclude/report unrelated, ignored,
   large/binary, secret-like, and generated/vendor files unless scoped. Before
   editing, verify every scoped editable text file is present in `manifest.txt`
   and either copied under `files/` with a matching hash or explicitly excluded
   with a reason, restore limit, and user approval. Stop if no adequate backup
   works.
7. Patch/verify: keep tightly coupled files in one coherent patch; otherwise use
   sequential verified slices. Internal signatures may change only when all
   callers are scoped and planned verification is strong; external contracts
   need opt-in.
   Add abstractions only for meaningful duplication or an existing stable domain
   concept; keep them small/local. Avoid restatement comments. Run
   formatter/linter only on touched files; stop if it expands scope.
8. Failure/closeout: if verification fails, do root-cause analysis first. Use
   baseline to separate pre-existing from new failure; fix only with clear
   cause/path. Follow repo-local commit instructions. If they require a commit,
   stage only scoped files after successful verification; otherwise leave
   changes unstaged unless asked.
   Closeout labels: `What changed`, `Why this was the chosen slice`,
   `Behavior-preservation evidence`, `Verification performed`, `Files changed`,
   `Remaining risks`, `Commit readiness`. Tiny low-risk changes may keep each
   label compact, but still include every label and the review prompt. Add a
   copy-ready read-only same-machine Codex/Claude review prompt with absolute
   paths, changed files, backup path, commands/results, behavior claim, planned
   verification strength, observed evidence label, risks, exclusions, call-site
   inspection, evidence challenge, backup-adequacy check, and blockers-first
   reporting. No rollback command.
