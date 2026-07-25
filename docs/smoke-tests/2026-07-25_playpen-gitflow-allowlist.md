# 2026-07-25 — playpen gitflow allowlist swap: differential hook proof

Evidence for the 2026-07-25 `contract-decisions.md` entry (playpen relaxation-zone hardening). Proves the config half of that decision: replacing the playpen's session-global branch-guard disarm (`PROTECTED_BRANCHES=__none__`) with the hook's path-scoped bypass (`GITFLOW_ALLOW_FILES=/Users/jp/playpen/**`) restores main-branch protection for foreign repos in playpen-rooted sessions while preserving the playpen's if-it-ever-becomes-a-git-repo freedom.

Method: the live hook (`~/.claude/hooks/require-gitflow.py`) invoked directly with synthesized PreToolUse stdin payloads and per-case explicit environment (`env -u` plus overrides), against a throwaway scratchpad repo on `main` and the real `~/.agents` checkout on `main`. Relevant hook mechanics, code-read: env parsed at `require-gitflow.py:179-180` (`__none__` yields a protection set matching no real branch); branch resolved from the edited file's repo, not the session cwd (`:367` nearest-existing-ancestor plus `run_git(cwd=target_dir)`); allowlist union `GITFLOW_ALLOW_FILES` + `GITFLOW_ALLOW_FILES_EXTRA` designed so a user-level allowlist survives per-project overrides (`:189-195`).

## Cases, verbatim

```text
== CASE A: testrepo on main, default env (expect BLOCK)
Cannot edit '...b5ed23439ee0/scratchpad/gitflow-test/repo/f.txt' on 'main' — this is a protected branch.

Create a working branch first:

  git checkout -b feature/<name>    # new functionality
  git checkout -b fix/<name>        # bug fix
  git checkout -b chore/<name>      # maintenance
exit=2
== CASE B: testrepo on main, GITFLOW_ALLOW_FILES=testrepo/** (expect ALLOW)
exit=0
== CASE C: ~/.agents on main, NEW playpen env (expect BLOCK - guard restored)
Cannot edit '/Users/jp/.agents/AGENTS.md' on 'main' — this is a protected branch.

Create a working branch first:

  git checkout -b feature/<name>    # new functionality
  git checkout -b fix/<name>        # bug fix
  git checkout -b chore/<name>      # maintenance
exit=2
== CASE D: ~/.agents on main, OLD playpen env PROTECTED_BRANCHES=__none__ (expect ALLOW - the defect)
Cannot edit files — branch 'main' doesn't follow GitFlow conventions.

Expected patterns:
  feature/*  feat/*  fix/*  bugfix/*  hotfix/*  release/*
  docs/*  style/*  refactor/*  perf/*  test/*  build/*  ci/*  chore/*
  dependabot/*  renovate/*  deps/*  codex/*  spike/*  experiment/*  poc/*

Create a valid branch:
  git checkout -b feature/<description>

Or rename current branch:
  git branch -m feature/main
exit=2
```

## Interpretation

- **A (block)** baselines the guard and the test harness: protection fires from the edited file's repo, regardless of where the invoking session sits.
- **B (allow)** proves the `GITFLOW_ALLOW_FILES` path-scoped bypass end to end — and is the future-proof case: a git-ified playpen on `main` passes both the protection layer and the strict-conventions layer under the new env.
- **C (block)** is the decision's point: under the new playpen env, an edit into `~/.agents` on `main` is blocked by protection, unconditionally.
- **D (block, different layer)** corrected the pre-test prediction and reproduces terminal-launched reality: profile-inherited `GITFLOW_STRICT=1` backstopped `main` edits even under the old disarm. The old exposure was therefore conditional, not absolute — live in GUI-launched sessions (which do not inherit shell-profile env) and for paths inside the profile's base allowlist. The swap removes both conditions from the guard.

## Environment notes

Shell profile injects `GITFLOW_STRICT=1`, a base `GITFLOW_ALLOW_FILES` (docs/CLAUDE.md/skills-path conveniences), and `GITFLOW_ALLOW_FILES_EXTRA=/Users/jp/personal/**`; user `settings.json` env carries only the `_EXTRA` pair. Project settings env overrides same-named vars, so under the new setting a playpen session's effective allowlist is `/Users/jp/playpen/**` + `/Users/jp/personal/**` — the profile's cross-repo docs/CLAUDE.md main-edit conveniences deliberately do not apply from playpen sessions, aligned with the same decision's graduation-regime clause.

## Proof boundary

Simulated stdin invocations of the real hook binary with explicit env. Not exercised live: project-settings env propagation into hook processes inside a real playpen session — the same documented mechanism the old setting relied on — and the CLAUDE.md prose changes, which have no in-session invocation here.
