# worktree-task-cycle — Codex row 3 stale-base across both satellites

- **Status at this commit:** **Stale-base refusal reproduced; rebase complete; post-rebase validation and landing pending.** This is the real task for the second branch activated from `main` at `b81cea9` alongside cycle A. Its initial validation bound `cf4156a`; after cycle A landed, its `land` refusal below preserved the task for the required recovery.
- **Date:** 2026-07-17
- **Authorization:** JP's Gate-B grant at `git-cycle` 1.5.4 authorizes the Codex stale-base proving row against the existing `decision-record` and `work-router` satellites. Gate C (mirror and push) remains withheld and separate.
- **Helper under proof:** `/Users/jp/.codex/plugins/cache/turbo-mode/git-cycle/1.5.4/skills/worktree-task-cycle/scripts/worktree_cycle.py`.
- **Evidence discipline:** all later fenced blocks will be verbatim output captured during this Codex session. This opening commit deliberately does not claim an outcome that has not happened yet.

## Row 3 plan

Cycle A (`decision-record`, branch `chore/wtc-codex-rows-a`) and cycle B (`work-router`, branch `chore/wtc-codex-rows-b`) were both activated from explicit `main` at `b81cea9`. After cycle A is validated and landed, cycle B's already-validated `land` must refuse with `STATE: STALE-BASE`, leaving its task branch intact. Cycle B then rebases on current `main`, reruns its validation record against the rewritten tip, and lands through the normal helper lifecycle.

## Row 3 — stale-base refusal

Cycle A landed `eec012e3580702e6b6a4cc5a004047ea5ad7b81a` before cycle B attempted its already-validation-bound landing. The installed Codex helper refused exactly at the freshness gate and released the integration lease before reporting the result:

```text
PROOF: SELF worktree lease held for 'work-router' with matching scope
PROOF: integration lease held
PROOF: primary is on 'main' (re-read live under the integration lease)
PROOF: primary clean (status --porcelain empty)
PROOF: no operation markers in primary
FACT: upstream read: ahead 18, behind 0 (ahead-only is the allowed steady state)
FACT: integration lease released
STATE: STALE-BASE
REFUSE: freshness failed: 'main' is not an ancestor of 'chore/wtc-codex-rows-b' — rebase in the satellite, revalidate (new validated_tip), re-enter
RESULT: refused
```

This is the intended row-3 negative result, not a failure to work around. The next permitted action is the helper-directed recovery: rebase cycle B on current `main`, review the rewritten documentation diff, bind a new validation record, and re-enter `land`.

## Row 3 recovery — rebase complete

The task branch rebased onto the cycle-A landing. The rewrite changed the task tip from `98a7cab` to `13996fa7a3ae864d3d226f94dd8280246e00cfa5`; its prior validation record is therefore intentionally stale and must not be reused.

```text
Rebasing (1/1)
Successfully rebased and updated refs/heads/chore/wtc-codex-rows-b.
```

The rewritten branch is clean and based on `eec012e`; the next lifecycle verb is a new `record-validation` for the rewritten tip, followed by `land`.
