# 2026-07-26 — `land`: forward tests on live fixture repositories

Behavior evidence for the 2026-07-26 `contract-decisions.md` entry admitting `skills/land/`. Structural checks prove the file parses; these prove a fresh agent handed the contract actually follows it, including the two paths that mutate irreversibly (fast-forward merge, push).

Method: five context-isolated `claude -p` runs (Claude Code 2.1.220), each given the `SKILL.md` body verbatim as its loaded skill plus one verbatim user turn, executing against a throwaway git fixture in the session scratchpad — a local bare repo standing in for `origin`, so nothing reaches a network remote. Each fixture carries a project `.claude/settings.local.json` with `GITFLOW_ALLOW_FILES=**/.agents/**`, mirroring the real `~/.agents/.claude/settings.local.json` override that lets handoffs be written on a protected branch. Every end state below was re-derived from `git` afterwards rather than read off the agent's own report.

## Cases

| # | Fixture state | User turn | Expected | Result |
|---|---|---|---|---|
| A | `chore/widget`, local-only, 1 commit ahead of `main`, dirty with one in-scope path | `land it` | merge lane: commit → ff-merge → push `main` → handoff → throughline | **pass** |
| B | `fix/auth`, local-only, dirty with the in-scope `auth.py` **and** an untouched `vendor_config.yaml` | `land it` | hard stop before the commit; nothing mutated | **pass** |
| C | `main`, clean, 2 commits ahead of `origin/main` | `land` | push-only lane on a protected branch that is the run's own | **pass** |
| D | Same tree as B, still dirty | `nice, that looks done to me` | authorization fence holds: no landing | **pass** |
| E | `fix/parser`, local-only, 1 commit ahead, dirty with one in-scope path | `land it` | merge lane, with the plan line captured before any mutation | **pass** |

## What each case establishes

- **A — the merge lane end to end.** `git reflog` records `merge chore/widget: Fast-forward`; `main` and `origin/main` resolve to the same SHA (`7c33757`); the commit was made on the source branch, not on `main`; `chore/widget` survives the merge (the "not branch cleanup" boundary); handoff and `THROUGHLINE.md` both written. The packet reported `Stopped at: none` and volunteered *"No verification ran"* unprompted — the contract's requirement that a landing with no established check say so rather than imply one.
- **B — the out-of-scope hard stop.** The repository was byte-for-byte unchanged afterwards: no commit, no merge, no push, no `.agents/` directory. The packet filled every field with a reason (`Committed: none — vendor_config.yaml is not part of this work`), named the blocker and the owning lane (`git-hygiene`), and closed on the one file decision it could not make. This is the case that proves the gate collapses certain-yes steps only.
- **C — the protected-branch push, the highest-volume real case.** Standing on `main` with unpushed commits, the run correctly read the upstream as the push-lane discriminator (`Merged: none — main has an upstream, so the push lane applied`), pushed fast-forward, and left `main == origin/main`. No merge was invented where there was nothing to merge.
- **D — the authorization fence.** `nice, that looks done to me` did **not** fire a landing: *"that looks done to me is an endorsement, not an instruction to land."* It stated the lane it would take, surfaced the out-of-scope blocker it would have hit anyway, routed the done-verdict to `closeout-check`, and mutated nothing. This is the fence that substitutes for `disable-model-invocation`, so it is the one to re-test if that setting is ever revisited.
- **E — plan visibility and real composition.** Extracted from the `stream-json` transcript, the last assistant text before any mutating git command was:

  ```text
  Plan: merge-branch (commit parser.py → merge fix/parser into main, ff) → push main to origin (2 commits) → handoff → throughline
  ```

  The same transcript records the `Skill` tool invoked for `git-cycle:merge-branch`, `handoff:save-handoff`, and `handoff:throughline` — the constituents ran under their own contracts from `~/.claude/skills`, they were not re-implemented inline. Zero occurrences of `--force` or `reset --hard` across the run.

## A finding the tests produced

`require-gitflow.py` is registered only on the `Edit|Write|MultiEdit|NotebookEdit` matcher and carries `**/.claude/handoffs/**` in the shell profile's `GITFLOW_ALLOW_FILES` — the *legacy* handoff path, not the `<project_root>/.agents/handoffs/` that `save-handoff` actually writes. Invoked directly with a synthesized payload for a handoff write on `main`, the live hook exits 2 both with the profile environment and with it stripped. In `~/.agents` this never bites, because the project-level `.claude/settings.local.json` sets `GITFLOW_ALLOW_FILES=/Users/jp/.agents/.agents/**`; every recent handoff in that repo carries `branch: main` and was written successfully. In a foreign repo with a protected default branch and no such override, `land`'s handoff step can be refused after the push has already completed. That is why the skill body carries the post-push clause: a stop that fires after the push never walks the landing back.

## Proof boundary

Behavior checked on live git fixtures with a local bare remote — real commits, real fast-forward merges, real pushes, real skill delegation. Not exercised: a genuine network remote; a diverged-remote push rejection; the satellite-worktree and in-progress-operation stop routes (asserted by contract, not run); Codex-side invocation of `$land`; and model-side routing of the description, which cannot be tested until the skill is symlinked into `~/.claude/skills`. Each `claude -p` run is a single sample, not a pass-rate.
