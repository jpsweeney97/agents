# worktree-task-cycle — Codex proving rows 0, 1, 2, and 3 at git-cycle 1.5.4

- **Status at this commit:** **Cycle A open.** Row 0's installed-cache probe is recorded below, and this commit is the real task for the Codex row-1/2 normal cycle. The post-commit lifecycle tail and row-3 result are recorded only by later evidence commits; this commit makes no future-completion claim.
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
