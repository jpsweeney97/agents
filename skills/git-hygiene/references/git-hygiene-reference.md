# Git Hygiene Reference

Load this file when exact command shape, preview format, `.git-hygiene.json`, or examples matter.

## Commands

Preflight:

```bash
git rev-parse --show-toplevel
git rev-parse --git-dir
git branch --show-current
git status --short --branch --untracked-files=all
git remote -v
git worktree list --porcelain
git branch --list
git rev-parse --is-shallow-repository
```

Use the git directory from `git rev-parse --git-dir` to inspect rebase, merge, cherry-pick, and bisect markers. Use `git status --porcelain=v1 --untracked-files=all` for counts. Preview stale remote refs with `git remote prune <remote> --dry-run`.

Branch checks:

```bash
git symbolic-ref --quiet --short refs/remotes/origin/HEAD
git branch --merged <default-branch>
git branch --no-merged <default-branch>
git worktree list --porcelain
```

Safe execution:

```bash
git switch -c codex/cleanup/YYYY-MM-DD-HHMMSS
git add .gitignore
git commit -m "chore: update ignore rules"
git add <approved-paths>
git commit -m "<approved-message>"
git remote prune <remote>
```

Destructive execution, only after approval:

```bash
trash <approved-file>
git branch -d <approved-branch>
```

Use `git branch -d`, not `-D`, unless the user separately requests force deletion and the safety case is clear.

## Preview Template

```text
Mode: audit

Lane: untracked-and-ignore
  .gitignore additions:
    + *.pyc
  Files to delete with trash:
    - tmp/debug.log
  Unknown files:
    ? notes.md - track, ignore, delete, or leave
  Protected files:
    ! credentials.local.json - delete only with explicit per-file confirmation

Lane: commit-shaping
  1. chore: update .gitignore with Python artifacts
  2. fix(auth): validate token expiration before refresh

Lane: branch-pruning
  Remote tracking to prune:
    - origin/feature/deleted-upstream
  Local branches to delete:
    - feature/old-experiment

Lane: config-learning
  Proposed saved patterns:
    + ignorePatterns: ["*.pyc"]
```

Shorten the preview under time pressure, but still show every lane with pending decisions.

## Final Report Shape

```text
Mode completed: apply-safe
Cleanup branch: codex/cleanup/2026-03-20-143052
Lane results:
  commit-shaping:
    commits created: 2
Recommended next step:
  apply-destructive for approved deletions
```

Use `Cleanup branch: none` when no branch was created. For partial execution, list completed work, failed operation, and unattempted work.

## Config

Read `.git-hygiene.json` only from repo root. If malformed, report and ignore it for this run.

Fields:

- `ignorePatterns`: candidate `.gitignore` additions, not silent file deletion.
- `protectedPatterns`: extra patterns that require per-file deletion approval.
- `groupingHints`: path prefixes to concern labels for commit grouping.
- `branchProtection`: branch names or globs never proposed for deletion.
- `defaultCommitPrefix`: Conventional Commits type for ambiguous real changes.

Config rules can strengthen safety rules, never weaken them.

## Example and Anti-patterns

Example flow: audit, present lanes, collect approvals, execute `apply-safe`, pause before `apply-destructive`, report lane results.

| Anti-pattern | Fix |
| ------------ | --- |
| One big cleanup operation | Split by lane. |
| One branch-cleanup approval for remote and local deletion | Approve separately. |
| `git add .` plus one cleanup commit | Propose semantic groups first. |
| `git clean -fd` | Preview first; use `trash` only for approved files. |
| Treating "quickly" as consent | Shorten preview; do not skip it. |
| Mixing `.gitignore` with code changes | Commit ignore rules separately and first. |
| Branch deletion without worktree checks | Check worktrees first. |
