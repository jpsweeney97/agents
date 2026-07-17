# worktree-task-cycle — Claude proving rows 1, 2, 5, 6 rerun at git-cycle 1.5.2

- **Status at this commit (cycle A):** the 1.5.2 repair is landed on `main`; row 2 (helper path resolution) is recorded below; cycle A (row 1's uninterrupted cycle) is open and lands this file — its own tail verbatims can only appear in the next cycle's commit. Rows 5 and 6 follow in cycles B and C; a documentation-only closing cycle lands the final verbatims. Row 4 is carried forward, not rerun — boundary stated below.
- **Date:** 2026-07-17
- **Authorization:** JP's 2026-07-17 Gate-B readiness review: Gate A granted for the narrow 1.5.1 → 1.5.2 symlink-record repair; "Rerun Claude rows 1, 2, 5, and 6 because they exercise record creation or helper identity. Row 4 may carry forward if lease/state behavior remains untouched and that proof boundary is stated explicitly." Gates B and C remain withheld; no publish, mirror, or push in any of these runs.
- **Target:** rows 1, 2, 5, 6 of the proving matrix (design v3 §7) for `worktree-task-cycle` at **git-cycle 1.5.2**, landed on `main` at `78b4418e983a3c10ccbd56bc10710d3d761dab2c`. The prior full Claude record at 1.5.1 is `docs/smoke-tests/2026-07-17_worktree-task-cycle-claude-proving-rows.md`.
- **Helper under proof:** invoked strictly at the installed path `/Users/jp/.claude/skills/git-cycle/skills/worktree-task-cycle/scripts/worktree_cycle.py` for every verb.
- **Environment:** macOS 26.5.2; helper interpreter `python3` = Python 3.14.2 (system PATH; the helper's floor is 3.9); the 80-test suite ran under uv-managed CPython 3.13.12 at the 1.5.2 landing.
- **Honest bounds:** every row here is **Claude-only**; rows 0/3 and all Codex halves remain post-Gate-B in a fresh Codex session. The stale-foreign variant remains proven only by composition of rows 4+5 at 1.5.1. The Codex cache holds git-cycle 1.4.2 throughout; the session-start canary reporting `NOT-INSTALLED` is the expected open Gate-B window.
- **Evidence discipline:** every fenced block below is verbatim stdout of a command run this session on this machine, captured to a log at execution time; nothing is retyped from memory.

## The 1.5.2 repair this rerun proves against

JP's review adjudicated a 1.5.1-disclosed ridden minor as a blocking fail-open: a dangling symlink at a validation-record path was classified absent and `record-validation` wrote the record **through** it, creating a file outside the validation store while printing `RESULT: ok`. The 1.5.2 guards (full record in the `78b4418` commit message, CHANGELOG § 1.5.2, and the ledger entry): lstat-based `symlink` classification at record paths with every consumer failing closed; default-deny record dispatch; `O_NOFOLLOW` + non-regular-file + hardlink pre-open write guards; `delete-branch` symlink refusal before branch mutation; FIFO/non-regular classification as `unreadable` (1.5.1 hung); and a `discover`-time store-integrity gate (real, non-symlink `skill-worktree/` and `validations/` on every verb).

Red-first record: seven black-box defect pins proven red against the extracted 1.5.1 helper (sha256 `7fa1cfd9abfba94754bd9fc65a6e77ac8d313df44e4b7a1a70e1b586652dc683`) in the exact reported modes — final rig run: **9 failed, 1 passed** (the two in-process write-guard pins red-by-absence; the create+supersede control green); the FIFO pin's red form is a liveness hang, proven by a 5s-timeout probe (`1.5.1-extracted: HANG — load_record blocked past the 5s timeout`; `1.5.2-fixed: completed in <5s: load_record -> ('unreadable', None)`). Suite after fix: **80/80 green**. Per-guard mutants: six killed by black-box pins; the two write-guard mutants that survived black-box testing are killed by the new in-process pins; the delete-branch refusal mutant killed. Three-lens adversarial review (fail-open, regression, mutation-teeth): no blocker; ridden, disclosed: hardlinked records classify `ok` on read paths (shared-inode bytes are genuine store content), the leases-dir symlink item, and two minor deltas (open() failures refuse exit-2 instead of tracebacking exit-1; 0o644 create mode under non-022 umask).

## The 1.5.2 landing cycle (context, not a proving row)

The repair landed through the `decision-record` satellite using the helper's own verbs (branch `fix/wtc-symlink-record-1.5.2`, validated tip = landed commit `78b4418`). Byte-honesty note: the installed path resolves through the primary's checkout, so `lease-acquire`, `activate`, `record-validation`, and `land` of the landing cycle executed **1.5.1** helper bytes; the ff-only merge flipped the primary's file, so that cycle's `park`, `delete-branch`, and closing `inspect` (`STATE: PARKED`, exit 0) already executed **1.5.2** bytes. The proving rows below run wholly under 1.5.2.

## Row 2 — helper path resolution (Claude half)

Captured at cycle A open, before any row verbs:

```text
invoked path: /Users/jp/.claude/skills/git-cycle/skills/worktree-task-cycle/scripts/worktree_cycle.py
symlink hop: /Users/jp/.agents/plugins/git-cycle
fully resolved: /Users/jp/.agents/plugins/git-cycle/skills/worktree-task-cycle/scripts/worktree_cycle.py
helper sha256: 4efb4c9a26bdcfbd90764517fd5cabb00f710bb1d059190609c1817d828fcdcf
landed sha256: 4efb4c9a26bdcfbd90764517fd5cabb00f710bb1d059190609c1817d828fcdcf
```

The invoked helper is byte-identical to `main`'s landed 1.5.2 blob. **Row 2 (Claude half): PASS.** The Codex half remains the row-0 unknown, post-Gate-B.

## Row 1 — normal full cycle, no interruption (satellite `decision-record`, cycle A — this file's commit is the row's real task)

Baseline `inspect`, `lease-acquire`, and `activate` at cycle A open, all exit 0, every verb the 1.5.2 helper at the installed path:

```text
FACT: base pinned: primary checkout is on 'main'
FACT: satellite 'decision-record' at /Users/jp/.agents-worktrees/decision-record locked=True reason='parked skill workspace (permanent)'
FACT: head: detached at 78b4418e983a3c10ccbd56bc10710d3d761dab2c
FACT: op markers: none
FACT: tree: clean (porcelain 0, unknown-ignored 0, reported-ignored 0)
FACT: ancestry: HEAD is ancestor of 'main'; ahead 0
FACT: lease wt-decision-record.lease: absent
STATE: PARKED
RESULT: ok

FACT: worktree lease for 'decision-record': acquired (branch 'chore/wtc-152-rows-a')
RESULT: ok

PROOF: SELF worktree lease held for 'decision-record' with matching scope
FACT: base pinned: primary checkout is on 'main'
PROOF: detached HEAD at 78b4418e983a3c10ccbd56bc10710d3d761dab2c
POLICY: satellite ignored residue: none present
PROOF: clean per ignored-state policy
PROOF: HEAD is ancestor of main
PROOF: rev-list --count main..HEAD = 0
PROOF: branch name 'chore/wtc-152-rows-a' is free
PROOF: activated 'chore/wtc-152-rows-a' from explicit 'main' ref; tip == 78b4418e983a3c10ccbd56bc10710d3d761dab2c
RESULT: ok
```

The row's real task is this evidence file's first commit; the uninterrupted tail (`record-validation` → `land` → `park` → `delete-branch`, then closing `inspect`) runs after this commit and its verbatims land in cycle B's commit.

### Row 1 — the uninterrupted tail (recorded in cycle B's commit)

The real task committed as `b03b96393c1b49edd7c918c6c7a551af868ac544`; the tail then ran uninterrupted, every verb exit 0:

```text
PROOF: SELF worktree lease held for 'decision-record' with matching scope
POLICY: satellite ignored residue: none present
PROOF: validation record bound: 'chore/wtc-152-rows-a' @ b03b96393c1b49edd7c918c6c7a551af868ac544
RESULT: ok

PROOF: SELF worktree lease held for 'decision-record' with matching scope
PROOF: integration lease held
PROOF: primary is on 'main' (re-read live under the integration lease)
PROOF: primary clean (status --porcelain empty)
PROOF: no operation markers in primary
FACT: upstream read: ahead 7, behind 0 (ahead-only is the allowed steady state)
PROOF: freshness: 'main' is ancestor of 'chore/wtc-152-rows-a'
PROOF: branch tip == validated_tip (b03b96393c1b49edd7c918c6c7a551af868ac544)
POLICY: satellite ignored residue: none present
PROOF: satellite clean
FACT: satellite currently on: 'chore/wtc-152-rows-a'
PROOF: landed: b03b96393c1b49edd7c918c6c7a551af868ac544 is ancestor of 'main'
FACT: integration lease released
RESULT: ok

PROOF: SELF worktree lease held for 'decision-record' with matching scope
FACT: base pinned: primary checkout is on 'main'
POLICY: satellite ignored residue: none present
PROOF: containment: HEAD is ancestor of 'main'
PROOF: detached HEAD at b03b96393c1b49edd7c918c6c7a551af868ac544
POLICY: satellite ignored residue: none present
PROOF: clean per ignored-state policy
PROOF: HEAD is ancestor of main
PROOF: rev-list --count main..HEAD = 0
FACT: worktree lease for 'decision-record' released (proven re-park)
RESULT: ok

FACT: base pinned: primary checkout is on 'main'
PROOF: 'chore/wtc-152-rows-a' is not checked out in any worktree
PROOF: 'chore/wtc-152-rows-a' is ancestor of 'main'
PROOF: branch 'chore/wtc-152-rows-a' safe-deleted
FACT: validation record for 'chore/wtc-152-rows-a' trashed
RESULT: ok

FACT: base pinned: primary checkout is on 'main'
FACT: satellite 'decision-record' at /Users/jp/.agents-worktrees/decision-record locked=True reason='parked skill workspace (permanent)'
FACT: head: detached at b03b96393c1b49edd7c918c6c7a551af868ac544
FACT: op markers: none
FACT: tree: clean (porcelain 0, unknown-ignored 0, reported-ignored 0)
FACT: ancestry: HEAD is ancestor of 'main'; ahead 0
FACT: lease wt-decision-record.lease: absent
STATE: PARKED
RESULT: ok
```

**Row 1 (Claude half, 1.5.2): PASS.**

## Row 4 — carried forward from the 1.5.1 record (not rerun): the explicit proof boundary

Row 4 (fabricated-foreign-lease adjudication on `work-router`) is carried forward on JP's stated condition. The boundary, verified two ways: (1) the 1.5.2 diff (`main..78b4418`, files `plugins/git-cycle/skills/worktree-task-cycle/scripts/worktree_cycle.py` + `tests/test_worktree_cycle.py` + the three lockstep docs) touches exactly five helper regions — the `discover` store gate, `load_record`'s symlink/non-regular classification, the new `write_record`, `record-validation`'s dispatch and write call, and `delete-branch`'s record handling; `read_owner`, `classify_owner`, `scope_matches`, `acquire_lease`, `require_self_wt_lease`, `session_identity`, and every lease verb carry zero hunks — lease classification, scope matching, and state mapping are byte-identical to 1.5.1; (2) the independent regression-lens review confirmed the same from the diff ("Row-4 carry-forward: CONFIRMED"). The only new code on row 4's execution path is the `discover`-time store-integrity gate, which is upstream of and orthogonal to lease adjudication, passes trivially against the real store, and is separately exercised by the symlinked-root/store regressions. Row 4's 1.5.1 PASS therefore stands for 1.5.2 lease/state behavior; it is a carried result, never a 1.5.2 execution claim.

## Rows 5 and 6 — plan (executed in cycles B and C, recorded in the following commits)

- Row 5 (interrupted COMMITTED-UNLANDED reconstruction, satellite `decision-record`): real task commit + `record-validation`, then the lease-absent state manufactured by explicitly authorized direct fixture manipulation (design v3 §7 row 5's authorized `trash` of the session's own lease dir — deliberately not `lease-release`, which refuses mid-task by design; JP's rerun instruction re-invokes that row as defined); fresh `inspect` must map `COMMITTED-UNLANDED`; re-lease; `land`; `park`; `delete-branch`.
- Row 6 (interrupted LANDED-UNPARKED resume, satellite `work-router`): real task commit, `record-validation`, `land`, deliberate stop before `park`; fresh `inspect` must map `LANDED-UNPARKED`; resume `park`; `delete-branch`.
- Closing documentation-only cycle: lands cycle C's verbatims, the completed-status header flip, and the ledger completion update — so no commit ever claims its own future landing.
