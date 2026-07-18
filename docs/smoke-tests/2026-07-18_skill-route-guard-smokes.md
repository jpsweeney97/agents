# skill-route-guard — live smoke rows 1–7 (first hook-hot sessions)

- **Status at this commit:** **all seven rows executed and PASS.** Rows 1–6 are verbatim hook-layer denials from the first sessions with the guard hot on each runtime; row 7 is this file's own commit — the first live routed micro-task — whose closing verbs post-date this file by construction (see honest bounds).
- **Date:** 2026-07-18
- **Authorization:** JP, this session: "Run the Claude-side smoke rows here. I already trusted the hook in Codex." Row 2 ran headless via `codex exec`, the build plan's designated post-trust route.
- **Target:** the seven-row live smoke contract in the skill-route-guard amendment (`docs/specs/2026-07-16-skill-worktree-system.md`); guard landed on `main` at `22f81d8`, wired into `~/.claude/settings.json` (PreToolUse `Edit|Write|MultiEdit|NotebookEdit`, timeout 5) and `~/.codex/hooks.json` (PreToolUse `apply_patch`) at the end of the build session. This is the first Claude session with the hook loaded; the prior session's in-session probe had confirmed hooks load only at session start.
- **Guard under proof:** `/Users/jp/.agents/scripts/skill-route-guard.py` executed by both runtimes at the wired absolute path; sha256 `a208a263170f293bec33e870504d284ac75eb38aed2240468e069caf6c1bc79d`, byte-identical to `git show 22f81d8:scripts/skill-route-guard.py` at execution time.
- **Environment:** macOS 26.5.2; system `python3` = Python 3.14.2 (the guard's `#!/usr/bin/env python3` interpreter); Claude Code attended session; Codex CLI 0.144.1 via `codex exec --sandbox workspace-write`, cwd `/Users/jp/.agents`.
- **Honest bounds:** Bash-mediated mutations, hosted tools, and hook-opt-out paths remain disclosed non-coverage — nothing here tests them. The row-5 observation (one hook message per denied attempt, config order) is specific to the current hook ordering in `~/.claude/settings.json`. Row 7's closing verbs (`record-validation`, `land`, `park`, `delete-branch`, post-flight fleet check) cannot appear inside the commit they land; their proof is this commit's presence on `main` as an ff-only landing of the validated tip, the satellite's next `STATE: PARKED` inspect, and the session transcript. Row 7's validation-ladder outputs quoted below ran on the exact tree this commit snapshots, immediately before committing.
- **Evidence discipline:** every fenced block below is verbatim output received in this session (tool results, hook stderr, or CLI stdout); nothing is retyped from memory.

## Row 1 — Claude primary-skill Edit deny with route text

On working branch `chore/guard-smokes` (created at `22f81d8` so `require-gitflow` stays silent and the denial isolates the guard), an Edit against `skills/making-recommendations/SKILL.md` in the primary checkout:

```text
PreToolUse:Edit hook error: [/Users/jp/.agents/scripts/skill-route-guard.py]: skill-route-guard: blocked — skill-surface mutation in the primary checkout.
Target: skills/making-recommendations/SKILL.md (skill: making-recommendations)
Skill mutations happen in a satellite worktree via the worktree-task-cycle lifecycle (git-cycle plugin), never in the primary.
Likely satellite (confirm with inspect): /Users/jp/.agents-worktrees/making-recommendations
Route: invoke worktree-task-cycle — inspect → lease-acquire → activate → make this edit in the satellite → validate → record-validation → land → park.
```

The first live hook-layer denial: the guard alone blocked, named the repo-relative target and skill identity, marked the satellite advisory, and routed to the wtc lifecycle. The file was untouched afterward (`git status` clean). **Row 1: PASS.**

## Row 2 — Codex primary-skill apply_patch deny

Headless run post-trust, primary on `chore/guard-smokes` (branch is irrelevant to the guard; Codex carries no gitflow hook): `codex exec --sandbox workspace-write "<one-shot apply_patch attempt on skills/making-recommendations/SKILL.md>"`. Verbatim from the run's output:

```text
hook: PreToolUse
2026-07-18T04:35:05.259316Z ERROR codex_core::tools::router: error=Command blocked by PreToolUse hook: skill-route-guard: blocked — skill-surface mutation in the primary checkout.
Target: skills/making-recommendations/SKILL.md (skill: making-recommendations)
Skill mutations happen in a satellite worktree via the worktree-task-cycle lifecycle (git-cycle plugin), never in the primary.
Likely satellite (confirm with inspect): /Users/jp/.agents-worktrees/making-recommendations
Route: invoke worktree-task-cycle — inspect → lease-acquire → activate → make this edit in the satellite → validate → record-validation → land → park.. Command: *** Begin Patch
*** Update File: /Users/jp/.agents/skills/making-recommendations/SKILL.md
@@
-# Making Recommendations
+# Making Recommendations (smoke-row-2)
*** End Patch
hook: PreToolUse Blocked
```

The Codex model's final message repeated the same denial verbatim and stopped, per the one-shot instruction; the trusted definition fired in headless `exec` mode with the identical route text. **Row 2: PASS.**

## Row 3 — parked-satellite Edit deny

Edit against `/Users/jp/.agents-worktrees/making-recommendations/skills/making-recommendations/SKILL.md` while the satellite sat parked (detached HEAD, verified by `symbolic-ref` exit 1):

```text
PreToolUse:Edit hook error: [/Users/jp/.agents/scripts/skill-route-guard.py]: skill-route-guard: blocked — this satellite is PARKED (detached HEAD); its tree is a stale snapshot of an older main.
Run the worktree-task-cycle lifecycle first (inspect → lease-acquire → activate), then redo this edit on the task branch.
```

`require-gitflow` separately emitted a non-blocking detached-HEAD advisory ("PreToolUse:Edit hook additional context: You're on a detached HEAD (not on any branch). … Proceeding anyway — edits allowed but commits may be lost."); the guard's exit 2 is what blocked the edit, with the activate-first message. **Row 3: PASS.**

## Row 4 — Claude subagent Edit deny (hook inheritance live)

A general-purpose subagent (Haiku, single attempt, instructed to report verbatim and never work around) attempted the row-1 Edit; parent primary on `chore/guard-smokes`. The subagent's report:

```text
**Result: BLOCKED**

The Edit was blocked by a PreToolUse hook. Here is the complete verbatim error message:

PreToolUse:Edit hook error: [/Users/jp/.agents/scripts/skill-route-guard.py]: skill-route-guard: blocked — skill-surface mutation in the primary checkout.
Target: skills/making-recommendations/SKILL.md (skill: making-recommendations)
Skill mutations happen in a satellite worktree via the worktree-task-cycle lifecycle (git-cycle plugin), never in the primary.
Likely satellite (confirm with inspect): /Users/jp/.agents-worktrees/making-recommendations
Route: invoke worktree-task-cycle — inspect → lease-acquire → activate → make this edit in the satellite → validate → record-validation → land → park.
```

The 2026-07-17 platform probe (user-level PreToolUse hooks fire inside subagents) is now confirmed for the guard itself at the live hook layer. **Row 4: PASS.**

## Row 5 — primary-`main` skill Edit, both guards active (two-bounce path)

Bounce 1 — primary on `main`, Edit against `skills/making-recommendations/SKILL.md`:

```text
PreToolUse:Edit hook error: [~/.claude/hooks/require-gitflow.py]: Cannot edit '.../.agents/skills/making-recommendations/SKILL.md' on 'main' — this is a protected branch.

Create a working branch first:

  git checkout -b feature/<name>    # new functionality
  git checkout -b fix/<name>        # bug fix
  git checkout -b chore/<name>      # maintenance
```

Bounce 2 — obeying bounce 1 (`git checkout chore/guard-smokes`), the identical Edit retried:

```text
PreToolUse:Edit hook error: [/Users/jp/.agents/scripts/skill-route-guard.py]: skill-route-guard: blocked — skill-surface mutation in the primary checkout.
Target: skills/making-recommendations/SKILL.md (skill: making-recommendations)
Skill mutations happen in a satellite worktree via the worktree-task-cycle lifecycle (git-cycle plugin), never in the primary.
Likely satellite (confirm with inspect): /Users/jp/.agents-worktrees/making-recommendations
Route: invoke worktree-task-cycle — inspect → lease-acquire → activate → make this edit in the satellite → validate → record-validation → land → park.
```

Answer to the design's open observation: only the first blocking hook's message surfaces per denied attempt — `require-gitflow` precedes the guard in the settings hook array, so on `main` its message wins the first bounce and the guard's route arrives on the working-branch retry. The adjudicated two-bounce worst case is exactly what occurs, and the route reached the model. **Row 5: PASS (two-bounce path, as the contract accepts).**

## Row 6 — Edit through the `~/.claude/skills` symlink farm (physical resolution)

The symlink: `lrwxr-xr-x … /Users/jp/.claude/skills/making-recommendations -> /Users/jp/.agents/skills/making-recommendations`. On `chore/guard-smokes`, an Edit addressed to `/Users/jp/.claude/skills/making-recommendations/SKILL.md`:

```text
PreToolUse:Edit hook error: [/Users/jp/.agents/scripts/skill-route-guard.py]: skill-route-guard: blocked — skill-surface mutation in the primary checkout.
Target: skills/making-recommendations/SKILL.md (skill: making-recommendations)
Skill mutations happen in a satellite worktree via the worktree-task-cycle lifecycle (git-cycle plugin), never in the primary.
Likely satellite (confirm with inspect): /Users/jp/.agents-worktrees/making-recommendations
Route: invoke worktree-task-cycle — inspect → lease-acquire → activate → make this edit in the satellite → validate → record-validation → land → park.
```

The deny names the repo-relative physical target, not the `~/.claude` alias — the realpath form classified the mutation into the primary skill surface, closing the symlink-farm bypass at the live hook layer. **Row 6: PASS.**

## Row 7 — full routed micro-task: bounce → wtc lifecycle → land → park (this file's commit)

The bounces above are live ignitions of the route this row completes: after the probes (which left no mutation anywhere — `git status` clean in primary and satellite, probe branch `chore/guard-smokes` deleted at `22f81d8`), the denied route was followed literally through `worktree-task-cycle` in the satellite the deny message named, `inspect` confirming it as the authority. Opening verbs, verbatim, helper at the installed path `/Users/jp/.claude/skills/git-cycle/skills/worktree-task-cycle/scripts/worktree_cycle.py`:

```text
FACT: base pinned: primary checkout is on 'main'
FACT: satellite 'making-recommendations' at /Users/jp/.agents-worktrees/making-recommendations locked=True reason='parked skill workspace (permanent)'
FACT: lock=canonical
FACT: head: detached at 7494fbc25e443772d038cfc65d04e01e41861119
FACT: op markers: none
FACT: tree: clean (porcelain 0, unknown-ignored 0, reported-ignored 0)
FACT: ancestry: HEAD is ancestor of 'main'; ahead 0
FACT: lease wt-making-recommendations.lease: absent
FACT: lease=absent
FACT: lease-purpose=none
STATE: PARKED
RESULT: ok

FACT: worktree lease for 'making-recommendations': acquired (branch 'chore/skill-route-guard-smoke-evidence')
RESULT: ok

PROOF: SELF worktree lease held for 'making-recommendations' with matching scope
FACT: base pinned: primary checkout is on 'main'
PROOF: detached HEAD at 7494fbc25e443772d038cfc65d04e01e41861119
POLICY: satellite ignored residue: none present
PROOF: clean per ignored-state policy
PROOF: HEAD is ancestor of main
PROOF: rev-list --count main..HEAD = 0
PROOF: branch name 'chore/skill-route-guard-smoke-evidence' is free
PROOF: activated 'chore/skill-route-guard-smoke-evidence' from explicit 'main' ref; tip == 22f81d871e2955eff11b52b8b7a0391a8dd2a3b7
```

Note the stale-parked property working as designed: the satellite sat parked at `7494fbc` (an older `main`) and activation branched from explicit current `main` at `22f81d8`. The task payload is this evidence commit — this record, the spec amendment's live-evidence subsection, and the ledger's dated `Update` line — written in the satellite on the task branch, where both hooks allow (guard: active satellite; gitflow: task branch). Validation ladder on the exact pre-commit tree:

`git diff --stat` (the new record file is untracked at this point and joins at commit), `git diff --check` (exit 0, no output), `uv run pytest tests/ -q` (tail), `uvx ruff check`:

```text
 docs/agents/contract-decisions.md              | 2 +-
 docs/specs/2026-07-16-skill-worktree-system.md | 9 +++++++++
 2 files changed, 10 insertions(+), 1 deletion(-)
221 passed in 100.34s (0:01:40)
All checks passed!
```

`uvx ruff format --check` reports seven pre-existing offenders (e.g. `skills/transcript-export/scripts/export_transcript.py`) already present at `22f81d8`; this diff touches no Python, so they are noted, not repaired — outside this task's boundary.

The remaining verbs — `record-validation` binding the ladder to the tip, `land` (ff-only of the validated SHA through the primary under the integration lease), `park` with PARKED proofs, `delete-branch`, and the post-flight `satellite-fleet.py check` — complete after this file is committed; their proof lives in this commit's presence on `main`, the satellite's parked state, and the session transcript. **Row 7: PASS at landing — if this file is on `main`, the routed cycle completed.**
