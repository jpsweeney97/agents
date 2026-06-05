# Simplification Playbook

Follow after `simplify-code` triggers. Higher-priority `AGENTS.md` rules win.

## Checklist

1. Scope, routing, and target: require cleanup intent plus target for an actual
   behavior-preserving edit. Ask once for plain `refactor`, vague
   maintainability, or missing target. Do not use this workflow for
   implementation, fixes, reviews, formatting-only work, redesigns, routine
   self-review, cleanup planning, refactoring backlogs, or candidate
   prioritization. For planning/backlog requests, route to `tech-debt-scan`; use
   this workflow after the user chooses a scoped behavior-preserving edit. If the
   useful change intentionally changes behavior, stop: `not a simplification:
   behavior change required`; explain benefit and consequence and ask whether to
   switch tasks.

   Treat current/staged diff, commit, and range targets as discovery inputs only.
   Before editing, expand them to explicit editable paths and report the
   expansion. For current or unstaged diff targets, separate simplification hunks
   from incidental dirty hunks before editing. For staged-diff targets, record
   pre-edit index state and leave new edits unstaged unless the user explicitly
   asks to stage or restage them; never rewrite existing staged hunks without
   approval.

   If a narrower platform, framework, or refactor skill owns the target, use that
   skill unless the user explicitly invokes `simplify-code` or asks for generic
   behavior-preserving cleanup outside the narrower skill's contract.

2. Roots/instructions/status: run status first. From the target directory, or the
   parent directory for a file target, run `git rev-parse --show-toplevel`; if it
   fails, use the explicit target root as a non-git root and state that git
   diff/status evidence is unavailable. Before planning edits, discover and read
   applicable instructions: repo-root `AGENTS.md`, any nearer `AGENTS.md` between
   the root and target path, and local package/tool config that controls
   formatter, linter, tests, or generated files.

   In a git repo, run `git status --short --branch` from the repo root and use
   path-limited checks: `git diff -- <paths>`, `git diff --cached -- <paths>`,
   and `git ls-files --others --exclude-standard -- <paths>`. Same-file
   unrelated changes block edits by default. Partial-scope opt-in requires user
   approval, exact hunks or regions, a whole-file backup, and a before/after
   preservation check showing unrelated edits remain untouched. Ignore/report
   unrelated dirty files elsewhere.

   Repo root is for git evidence and `.backup/`; target/project root is for
   instructions, config, formatter/linter, tests, and verification. Pick the
   nearest ancestor with local instructions or package config; if unclear, say so
   and use the explicit target root.

3. Run the scoped safety scanner before lane selection:

   ```bash
   python skills/simplify-code/scripts/scoped_safety_scan.py <paths>
   ```

   Resolve the script path relative to this skill directory when used outside
   `/Users/jp/.agents`. Use the production default `max_bytes` of `1048576`
   (`1 MiB`) for real simplify-code eligibility. Use `--max-bytes` only for tests
   or when the user explicitly approves a different threshold after the risk is
   named.

   The scanner is a conservative gate over paths and file bytes only; keep git
   tracked/dirty state in the explicit git checks above. It emits JSON only:
   exit `0` for overall `clean`, exit `1` for `positive` or `uncertain`, and exit
   `2` only for usage/internal errors where no valid JSON result can be produced.
   A clean result is necessary but not sufficient for fast lane. A `positive`,
   `uncertain`, unreadable, binary, large, missing-path, symlink, generated/vendor,
   dense-minified, or scanner-error result blocks fast lane.

   Scanner output is file-first:

   ```json
   {
     "schema_version": 1,
     "overall_status": "clean|positive|uncertain",
     "max_bytes": 1048576,
     "files": [
       {
         "path": "/abs/or/input/path",
         "status": "clean|positive|uncertain",
         "categories": {
           "secret_risk": "clean|positive|uncertain",
           "binary_or_unreadable": "clean|positive|uncertain",
           "large_file": "clean|positive",
           "generated_or_vendor_hint": "clean|positive|uncertain"
         },
         "findings": [
           {
             "category": "secret_risk",
             "status": "positive",
             "rule_id": "SECRET_ASSIGNMENT",
             "line": 12,
             "byte_offset": 340,
             "reason": "Secret-like assignment detected; value redacted."
           }
         ]
       }
     ]
   }
   ```

   The scanner must not output matched snippets or raw credential-looking values.
   Findings include file path, category, status, rule ID, line/byte offset when
   available, and redacted reason text. For symlinks, report the link target and
   do not follow it.

4. Boundaries and opt-in: read-only unless explicitly opted in for migrations,
   schemas, persistence, auth/security, billing, permissions, data-loss,
   concurrency/locking, generated/vendor, dependency, package, plugin, app,
   project, or release manifests, external/public contracts, release/packaging,
   and binaries. State the exact protected risk property before asking for
   opt-in, such as auth behavior, package resolution, persistence shape, external
   contract, release metadata, or generated-source overwrite. Merely naming a
   protected path as the target is not enough.

   Sensitive paths also require a strong verification plan, baseline
   verification, and narrow scope. Generated/vendor edits need confirmation,
   overwrite-risk warning, and generator/source preference. Do not edit binaries;
   ask for an asset workflow. Edit tests only when scoped or test-only; never
   relax expectations.

5. Choose lane:

   - Fast lane: only for clean tracked text files in a git repo, no same-file
     dirty or staged diff, empty path-limited pre-edit diff, scanner overall
     `clean`, no protected/generated/vendor/secret-adjacent surface, narrow scope,
     small post-edit diff that can be inspected, and at least one runnable
     independent check such as a focused test, typecheck, touched-file lint,
     snapshot, or equivalent local probe. Caller/call-site inspection can support
     the claim but cannot unlock fast lane by itself. Fast lane creates no backup
     artifact; recovery is the tracked git baseline.
   - Full-safety lane: use for dirty or untracked files, non-git roots, broad
     scopes, protected surfaces, weak verification, generated/vendor files,
     secret-adjacent files, positive/uncertain scanner output, or unclear
     fast-lane eligibility. Automatically fall back to full-safety lane when it
     can proceed safely. Stop and ask when uncertainty affects whether edits are
     allowed at all: possible secret content, binary/generated overwrite risk,
     protected-surface opt-in, weak verification, or same-file unrelated changes.

6. Broad scopes: do read-only reconnaissance. List candidate slices with files,
   call sites, simplification, risk, planned verification strength, lane
   eligibility, and remaining candidates. Patch one coherent slice. Value order:
   defect risk, cognitive load, meaningful duplication, local patterns,
   test/debug ease, then aesthetic ride-alongs. Closeout must state when the
   original broad request was not exhausted.

7. Verification plan and evidence: before editing, assign planned verification
   strength. `strong plan` = focused tests/probes already cover the changed
   behavior or can be run, needed baselines are available, and no public/external
   contract diff is expected. `moderate plan` = tight reasoning plus an
   independent typecheck, lint, snapshot, caller audit, or manual probe can cover
   the changed surface. `weak plan` = static review only, no independent check,
   missing risky baseline, blocked verification, or high-risk-adjacent work
   without focused coverage.

   Weak planned verification requires approval before editing; ask whether to
   proceed, pick a safer slice, or stop. Baseline is required for broad,
   weak-plan, high-risk-adjacent, and cheap obvious checks. For narrow
   moderate/strong-plan edits, state attribution is weaker if baseline was
   skipped. After editing, report observed behavior-preservation evidence
   separately as `strong`, `moderate`, or `weak` based only on checks actually run
   and results observed. Do not present lint/typecheck-only results or caller
   audit alone as behavioral proof; label them as static or structural support
   unless a behavior-focused test, snapshot, probe, or equivalent manual check
   exercised the changed behavior.

8. Full-safety backup: create the secret-safe pre-edit backup artifact with the
   helper:

   ```bash
   python skills/simplify-code/scripts/create_simplify_backup.py \
     --scope-slug <scope-slug> \
     --planned-verification "<strong|moderate|weak plan>" \
     --retention "<retention/cleanup expectation>" \
     <explicit-editable-paths>
   ```

   Resolve the script path relative to this skill directory when used outside
   `/Users/jp/.agents`. In git repos the helper creates the artifact under
   `<repo-root>/.backup/`, writes git evidence, and adds `.backup/` to the
   repo-local exclude file from `git rev-parse --git-path info/exclude` when
   missing. Outside git it uses `/Users/jp/backup/<repo-or-dir-slug>/` by default;
   if that root is unavailable or outside the writable sandbox, ask for approval
   of a writable `--backup-root` or stop before editing.

   Exit `0` means every scoped editable file has a restorable copied pre-edit
   file. Exit `1` means an artifact was created but one or more scoped files were
   excluded and are not restorable from that artifact; get explicit approval for
   the named restore limit, choose a secure backup mode, pick a safer target, or
   stop. Exit `2` means no valid backup artifact was produced; stop before
   editing.

   `Restorable` means every edited text file can be reconstructed from copied
   pre-edit content. Files excluded from backup are not restorable from the
   artifact and require explicit user approval before editing. The artifact must
   include `manifest.txt` with root, branch or `no-git`, HEAD when available,
   scoped editable paths, scanner summary, excluded paths with reasons and restore
   limits, planned verification strength, retention/cleanup expectation, and
   SHA-256 hashes for copied original files.

   Copy the full pre-edit file under `files/<relative-path>` only when the
   scanner result for that file is `clean` and no secret risk is otherwise
   apparent. For `positive` or `uncertain` scanner results, possible secret
   content, credentials, tokens, private keys, binary/large files, or similarly
   sensitive content, do not copy content into `.backup/` or `/Users/jp/backup` by
   default. Use hash-only/redacted manifest, a user-approved secure backup
   location, or explicit exclusion with acknowledgement that the file will not be
   restorable from the artifact.

   The helper also writes `scanner.json`, and in git repos saves pre-edit
   `status.txt`, scoped `diff.patch`, scoped `cached.diff.patch`, and scoped
   `untracked.txt`. Do not edit tracked `.gitignore` solely to ignore backup
   artifacts. Before editing, verify every scoped editable text file is present in
   `manifest.txt` and either copied under `files/` with a matching hash or
   explicitly excluded with a reason, restore limit, and user approval. Stop if no
   adequate backup works.

9. Patch/verify: keep tightly coupled files in one coherent patch; otherwise use
   sequential verified slices. Internal signatures may change only when all
   callers are scoped and planned verification is strong; external contracts need
   opt-in. Add abstractions only for meaningful duplication or an existing stable
   domain concept; keep them small/local. Avoid restatement comments. Run
   formatter/linter only on touched files; stop if it expands scope.

10. Failure/closeout: if verification fails, do root-cause analysis first. Use
    baseline to separate pre-existing from new failure; fix only with clear
    cause/path. Follow repo-local commit instructions. If they require a commit,
    stage only scoped files after successful verification; otherwise leave changes
    unstaged unless asked.

    Closeout starts with `Simplification Result`, `Behavior Claim`,
    `Verification`, `Commit Readiness`, and `Review Packet`. Keep the first four
    labels concise: user-visible result, behavior-preservation evidence,
    commands/results, and readiness/blocker. `Review Packet` is the details
    section: include files changed, remaining risks, exclusions, and
    lane-specific evidence. Fast-lane closeout adds a compact review hook with
    absolute paths, behavior-preservation claim, command/result, and one sentence
    naming why fast-lane eligibility held. Full-safety closeout puts the
    copy-ready read-only same-machine Codex/Claude review prompt under `Review
    Packet`, with absolute paths, changed files, backup helper command/result,
    backup path, backup retention/cleanup expectation, commands/results,
    behavior claim, planned verification strength, observed evidence label,
    risks, exclusions, call-site inspection, evidence challenge,
    backup-adequacy check, and blockers-first reporting. No rollback command.

## Script Maintenance

Run these focused tests after any edit touching `scripts/`, scanner output
schema, lane eligibility, backup handling, or secret/generated/vendor screening
language:

```bash
uv run pytest skills/simplify-code/tests/test_scoped_safety_scan.py \
  skills/simplify-code/tests/test_create_simplify_backup.py
```

For unrelated wording-only edits, YAML parsing and reference/path checks are
enough.

## Behavior Proof

Structural checks such as YAML parsing, `quick_validate.py`, and the focused
pytest files do not prove that an agent will follow the behavior contract. After
any behavior-contract change, run the manual smoke test in
[`../examples/agent-smoke-test.md`](../examples/agent-smoke-test.md) as the
behavior proof path, or explicitly report `Behavior smoke test: not run` with
the reason and do not claim behavior proof.
