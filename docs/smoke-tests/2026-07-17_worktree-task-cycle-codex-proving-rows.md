# worktree-task-cycle — Codex proving rows 0, 1, 2, and 3 at git-cycle 1.5.4

- **Status at this commit:** **Codex rows 0, 2, and 3 complete — PASS; the normal row-1 cycle is pending.** Cycle C is the designated final normal task: after this commit, it must run `record-validation` → `land` → `park` → `delete-branch` without interruption. A later documentation task records that tail and the dated Gate-B ledger completion.
- **Date:** 2026-07-17
- **Authorization:** JP granted Gate B at `git-cycle` 1.5.4 in the 2026-07-17 Claude session transcript. The grant ratifies the app-server auto-synced publish, confirms the installed cache is byte-identical to `main` at `b81cea9`, and authorizes rows 0, 3, and the Codex halves of rows 1/2. Gate C (mirror and push) remains withheld and separate.
- **Target:** the Codex half of the design-v3 §7 proving matrix, as reconstructed in `docs/smoke-tests/2026-07-17_worktree-task-cycle-claude-proving-rows.md`, against the two existing pilot satellites only.
- **Helper under proof:** invoked strictly at `/Users/jp/.codex/plugins/cache/turbo-mode/git-cycle/1.5.4/skills/worktree-task-cycle/scripts/worktree_cycle.py` for every lifecycle verb.
- **Evidence discipline:** every fenced block is verbatim stdout from a command run in this Codex session on this machine, captured at execution time. The helper has no `--version` verb; version identity is proven by the cache manifest and byte hashes below.

## Row 0 — Codex at-fire installed-cache path probe

The active Codex session supplied `CODEX_THREAD_ID` `019f713e-9c94-75d0-8122-152804f7abf2`. This task used the installed skill contract at the following physical cache path, not a repo-relative or Claude symlink path:

```text
/Users/jp/.codex/plugins/cache/turbo-mode/git-cycle/1.5.4/skills/worktree-task-cycle/SKILL.md
```

`scripts/codex-plugins-sync.sh --check git-cycle` exited 0 with no stdout. Source/cache identity was then independently recorded:

```text
a6a757a7df7a559ad251b3fc188ada5a0b7c86d7c1c2730690c06802162005fc  plugins/git-cycle/.claude-plugin/plugin.json
a6a757a7df7a559ad251b3fc188ada5a0b7c86d7c1c2730690c06802162005fc  /Users/jp/.codex/plugins/cache/turbo-mode/git-cycle/1.5.4/.claude-plugin/plugin.json
614019ea922e38a6168d5e68ab8d9bb8a52c79b90c482ab6e4fe1dd771949a33  plugins/git-cycle/skills/worktree-task-cycle/scripts/worktree_cycle.py
614019ea922e38a6168d5e68ab8d9bb8a52c79b90c482ab6e4fe1dd771949a33  /Users/jp/.codex/plugins/cache/turbo-mode/git-cycle/1.5.4/skills/worktree-task-cycle/scripts/worktree_cycle.py
```

The 1.5.3 → 1.5.4 delta is documentation-only (`plugin.json` version, `CHANGELOG.md`, and `README.md`); the helper hash is unchanged, so the 1.5.3 Claude rows remain carried evidence. This proves the at-fire Codex installed-path boundary and byte identity. It does not independently assert plugin activation beyond this session's loaded cache path, and it does not open Gate C.

## Preflight — two existing pilot satellites

Primary status before either lifecycle mutation:

```text
## main...origin/main [ahead 17]
```

Both satellites began `PARKED`, locked with the canonical reason, clean, and lease-free:

```text
FACT: base pinned: primary checkout is on 'main'
FACT: satellite 'decision-record' at /Users/jp/.agents-worktrees/decision-record locked=True reason='parked skill workspace (permanent)'
FACT: head: detached at b81cea9054f44b64f613e29e1bb55dcca5165429
FACT: op markers: none
FACT: tree: clean (porcelain 0, unknown-ignored 0, reported-ignored 0)
FACT: ancestry: HEAD is ancestor of 'main'; ahead 0
FACT: lease wt-decision-record.lease: absent
STATE: PARKED
RESULT: ok
```

```text
FACT: base pinned: primary checkout is on 'main'
FACT: satellite 'work-router' at /Users/jp/.agents-worktrees/work-router locked=True reason='parked skill workspace (permanent)'
FACT: head: detached at 84f556f5647c3509c7d45904ebea2b142fb72a63
FACT: op markers: none
FACT: tree: clean (porcelain 0, unknown-ignored 0, reported-ignored 0)
FACT: ancestry: HEAD is ancestor of 'main'; ahead 0
FACT: lease wt-work-router.lease: absent
STATE: PARKED
RESULT: ok
```

## Rows 1 + 2 and row 3 — cycles A and B opened from the same base

Both satellites were activated before either task committed, each from explicit `main` at `b81cea9`. Cycle A (`decision-record`) is the normal row-1/2 task; cycle B (`work-router`) is the row-3 stale-base task. Its `land` must refuse with `STATE: STALE-BASE` after A lands, then B must rebase, revalidate, and land. Later commits record those outputs.

```text
FACT: worktree lease for 'decision-record': acquired (branch 'chore/wtc-codex-rows-a')
RESULT: ok

PROOF: SELF worktree lease held for 'decision-record' with matching scope
FACT: base pinned: primary checkout is on 'main'
PROOF: detached HEAD at b81cea9054f44b64f613e29e1bb55dcca5165429
POLICY: satellite ignored residue: none present
PROOF: clean per ignored-state policy
PROOF: HEAD is ancestor of main
PROOF: rev-list --count main..HEAD = 0
PROOF: branch name 'chore/wtc-codex-rows-a' is free
PROOF: activated 'chore/wtc-codex-rows-a' from explicit 'main' ref; tip == b81cea9054f44b64f613e29e1bb55dcca5165429
RESULT: ok

FACT: worktree lease for 'work-router': acquired (branch 'chore/wtc-codex-rows-b')
RESULT: ok

PROOF: SELF worktree lease held for 'work-router' with matching scope
FACT: base pinned: primary checkout is on 'main'
PROOF: detached HEAD at 84f556f5647c3509c7d45904ebea2b142fb72a63
POLICY: satellite ignored residue: none present
PROOF: clean per ignored-state policy
PROOF: HEAD is ancestor of main
PROOF: rev-list --count main..HEAD = 0
PROOF: branch name 'chore/wtc-codex-rows-b' is free
PROOF: activated 'chore/wtc-codex-rows-b' from explicit 'main' ref; tip == b81cea9054f44b64f613e29e1bb55dcca5165429
RESULT: ok
```

## Supporting cycle A — at-fire evidence and row-3 predecessor (not a row-1 pass)

Cycle A's real task was this file's opening commit, `eec012e3580702e6b6a4cc5a004047ea5ad7b81a`, on `decision-record`. Its validation and landing succeeded, but its re-park was deliberately delayed while cycle B observed its stale-base refusal. Cycle A therefore had a `LANDED-UNPARKED` interval and is **not** counted as the uninterrupted normal Codex row-1 execution. The outputs below remain supporting lifecycle evidence only:

```text
PROOF: SELF worktree lease held for 'decision-record' with matching scope
POLICY: satellite ignored residue: none present
PROOF: validation record bound: 'chore/wtc-codex-rows-a' @ eec012e3580702e6b6a4cc5a004047ea5ad7b81a
RESULT: ok

PROOF: SELF worktree lease held for 'decision-record' with matching scope
PROOF: integration lease held
PROOF: primary is on 'main' (re-read live under the integration lease)
PROOF: primary clean (status --porcelain empty)
PROOF: no operation markers in primary
FACT: upstream read: ahead 17, behind 0 (ahead-only is the allowed steady state)
PROOF: freshness: 'main' is ancestor of 'chore/wtc-codex-rows-a'
PROOF: branch tip == validated_tip (eec012e3580702e6b6a4cc5a004047ea5ad7b81a)
POLICY: satellite ignored residue: none present
PROOF: satellite clean
FACT: satellite currently on: 'chore/wtc-codex-rows-a'
PROOF: landed: eec012e3580702e6b6a4cc5a004047ea5ad7b81a is ancestor of 'main'
FACT: integration lease released
RESULT: ok
```

```text
PROOF: SELF worktree lease held for 'decision-record' with matching scope
FACT: base pinned: primary checkout is on 'main'
POLICY: satellite ignored residue: none present
PROOF: containment: HEAD is ancestor of 'main'
PROOF: detached HEAD at 2dfe0bcab163c4b955a0d2f76bca787c464247f2
POLICY: satellite ignored residue: none present
PROOF: clean per ignored-state policy
PROOF: HEAD is ancestor of main
PROOF: rev-list --count main..HEAD = 0
FACT: worktree lease for 'decision-record' released (proven re-park)
RESULT: ok

FACT: base pinned: primary checkout is on 'main'
PROOF: 'chore/wtc-codex-rows-a' is not checked out in any worktree
PROOF: 'chore/wtc-codex-rows-a' is ancestor of 'main'
PROOF: branch 'chore/wtc-codex-rows-a' safe-deleted
FACT: validation record for 'chore/wtc-codex-rows-a' trashed
RESULT: ok
```

## Row 2 — installed helper identity (Codex half): PASS

Row 2 shares row 0's at-fire proof: the active Codex session resolved the physical cache path and ran every lifecycle verb from its installed helper. The cache manifest and helper both matched the landed source byte-for-byte, with helper SHA-256 `614019ea922e38a6168d5e68ab8d9bb8a52c79b90c482ab6e4fe1dd771949a33`. Unlike the prior Claude row, the path is a physical Codex cache directory rather than a Claude symlink.

## Row 3 — stale-base across both satellites (Codex): PASS

Cycles A and B were activated from the same `b81cea9` base. After A landed, B's validation-bound `land` safely refused with `STATE: STALE-BASE`; B then rebased, bound its rewritten tip, and landed. The complete refusal and recovery record is in `docs/smoke-tests/2026-07-17_worktree-task-cycle-codex-stale-base.md`; the second satellite ended re-parked with its branch and validation record safely removed.

## Cycle C — the pending normal row-1 task

This commit is the real work for the normal Codex row-1 task on `decision-record` (branch `chore/wtc-codex-rows-docs`). After it commits, its validation, landing, re-park, and safe deletion must run uninterrupted. A final documentation task will then land Cycle C's verbatim tail plus the dated ledger completion. Gate C remains withheld throughout: no mirror update, push, PR, or other external publication is part of this work.
