# worktree-task-cycle — Claude proving rows 1, 2, 4 rerun at git-cycle 1.5.3

- **Status at this commit:** **Claude rerun complete — rows 1, 2, 4 all PASS at 1.5.3; rows 5 and 6 carried forward under the stated boundary.** This commit is the documentation-only closing cycle; rows 0/3 and all Codex halves remain post-Gate-B (see the closing note).
- **Date:** 2026-07-17
- **Authorization:** JP's 2026-07-17 second Gate-B readiness review: Gate B withheld on the confirmed lease-root symlink fail-open; Gate A granted for the narrow 1.5.2 → 1.5.3 repair; "Rerun Claude rows **1, 2, and 4**: row 1 proves the normal lease lifecycle; row 2 proves installed-path identity for the new bytes; row 4 directly covers lease adjudication. Rows 5 and 6 may carry forward if the patch touches only the shared discovery invariant and their record/state-routing logic remains byte-identical, with that boundary stated explicitly." Gate B returns after 1.5.3 and these reruns; Gate C remains separate and withheld; no publish, mirror, or push in any of these runs.
- **Target:** rows 1, 2, 4 of the proving matrix (design v3 §7) for `worktree-task-cycle` at **git-cycle 1.5.3**, landed on `main` at `ccf43655406a0ebbeae750612aff50eba5d955cb`. Prior records: 1.5.1 full Claude matrix at `docs/smoke-tests/2026-07-17_worktree-task-cycle-claude-proving-rows.md`; 1.5.2 rerun at `docs/smoke-tests/2026-07-17_worktree-task-cycle-claude-proving-rows-1.5.2.md`. Both stand unmodified.
- **Helper under proof:** invoked strictly at the installed path `/Users/jp/.claude/skills/git-cycle/skills/worktree-task-cycle/scripts/worktree_cycle.py` for every verb.
- **Environment:** macOS 26.5.2; helper interpreter `python3` = Python 3.14.2 (system PATH; the helper's floor is 3.9); the 82-test suite ran under uv-managed CPython 3.13.12 at the 1.5.3 landing.
- **Honest bounds:** every row here is **Claude-only**; rows 0/3 and all Codex halves remain post-Gate-B in a fresh Codex session. Rows 5 and 6 are **carried** results at 1.5.3 (see the carry-forward section), as row 4 was at 1.5.2 — never 1.5.3 execution claims. The stale-foreign variant remains proven only by composition of rows 4+5, and at 1.5.3 that composition mixes a rerun row 4 with a carried row 5. The Codex cache holds git-cycle 1.4.2 throughout; the session-start canary reporting `NOT-INSTALLED` is the expected open Gate-B window.
- **Evidence discipline:** every fenced block below is verbatim stdout of a command run this session on this machine, captured to a log at execution time; nothing is retyped from memory.

## The 1.5.3 repair this rerun proves against

JP's second Gate-B readiness review confirmed the 1.5.2-disclosed leases-dir symlink item as a live out-of-store mutation path: in a hermetic repo with a valid locked satellite, `skill-worktree/` and `validations/` real but `skill-worktree/leases/` replaced by a symlink to an external empty directory, a normal `lease-acquire` created the lease dir and `owner.json` outside the git state store — exit 0, `RESULT: ok`. The 1.5.2 `discover` proved `store` and `validations` non-symlink but never `leases`; its later `leases.is_dir()` followed the link; `acquire_lease` then staged and renamed through it. The 1.5.3 repair (full record in the `ccf4365` commit message, CHANGELOG § 1.5.3, and the ledger entry): `topo.leases` joins the same `discover`-time non-symlink invariant — every owned state-root component (`skill-worktree/`, `leases/`, `validations/`) must be a real directory under the resolved git common dir, enforced before any mutation on every verb; explicitly not broadened into general filesystem-threat hardening.

Red-first record: JP's counterexample reproduced against the extracted 1.5.2 helper (sha256 `4efb4c9a26bdcfbd90764517fd5cabb00f710bb1d059190609c1817d828fcdcf`): exit 0, `wt-skill-a.lease/owner.json` created outside the store; the dangling variant's red form is the untruthful `no skill-worktree store` refusal (exit 2, target left absent). Final rig run of the landed test bytes vs the extracted 1.5.2 helper: **2 failed, 1 passed** (live + dangling pins red; the real-lease-root control `test_lease_release_when_parked` green). Suite after fix: **82/82 green**. The guard-excision mutant (`topo.leases` removed from the tuple) is killed by both pins. Teeth note: the pins assert the gate's own phrases (`store integrity failed`, `is a symlink`) because pytest embeds the test name in `tmp_path` and these tests' names contain "symlink" — a bare substring assert self-satisfies via the path echo in the refusal message; the same latency exists in prior symlink tests' message asserts (their teeth are exit-code- and mutation-proven; noted in the ledger, not repaired — out of the authorized boundary).

## The 1.5.3 landing cycle (context, not a proving row)

The repair landed through the `decision-record` satellite using the helper's own verbs (branch `fix/wtc-lease-root-1.5.3`, validated tip = landed commit `ccf4365`). Byte-honesty note: the installed path resolves through the primary's checkout, so `lease-acquire`, `activate`, `record-validation`, and `land` of the landing cycle executed **1.5.2** helper bytes; the ff-only merge flipped the primary's file, so that cycle's `park`, `delete-branch`, and closing `inspect` (`STATE: PARKED`, exit 0) already executed **1.5.3** bytes. The landing cycle's `record-validation` and `park` reported the session's own test-run cache residue (`.pytest_cache/`, `.ruff_cache/`, `tests/__pycache__/`) under the report-and-record ignored-state policy; it was `trash`ed before the closing inspect, which read `tree: clean (porcelain 0, unknown-ignored 0, reported-ignored 0)`. The proving rows below run wholly under 1.5.3.

## Row 2 — helper path resolution (Claude half)

Captured at cycle A open, before any row verbs:

```text
invoked path: /Users/jp/.claude/skills/git-cycle/skills/worktree-task-cycle/scripts/worktree_cycle.py
symlink hop: /Users/jp/.agents/plugins/git-cycle
fully resolved: /Users/jp/.agents/plugins/git-cycle/skills/worktree-task-cycle/scripts/worktree_cycle.py
helper sha256: 614019ea922e38a6168d5e68ab8d9bb8a52c79b90c482ab6e4fe1dd771949a33
landed sha256: 614019ea922e38a6168d5e68ab8d9bb8a52c79b90c482ab6e4fe1dd771949a33
```

The invoked helper is byte-identical to `main`'s landed 1.5.3 blob. **Row 2 (Claude half, 1.5.3): PASS.** The Codex half remains the row-0 unknown, post-Gate-B.

## Row 1 — normal full cycle, no interruption (satellite `decision-record`, cycle A — this file's commit is the row's real task)

Baseline `inspect`, `lease-acquire`, and `activate` at cycle A open, all exit 0, every verb the 1.5.3 helper at the installed path:

```text
FACT: base pinned: primary checkout is on 'main'
FACT: satellite 'decision-record' at /Users/jp/.agents-worktrees/decision-record locked=True reason='parked skill workspace (permanent)'
FACT: head: detached at ccf43655406a0ebbeae750612aff50eba5d955cb
FACT: op markers: none
FACT: tree: clean (porcelain 0, unknown-ignored 0, reported-ignored 0)
FACT: ancestry: HEAD is ancestor of 'main'; ahead 0
FACT: lease wt-decision-record.lease: absent
STATE: PARKED
RESULT: ok

FACT: worktree lease for 'decision-record': acquired (branch 'chore/wtc-153-rows-a')
RESULT: ok

PROOF: SELF worktree lease held for 'decision-record' with matching scope
FACT: base pinned: primary checkout is on 'main'
PROOF: detached HEAD at ccf43655406a0ebbeae750612aff50eba5d955cb
POLICY: satellite ignored residue: none present
PROOF: clean per ignored-state policy
PROOF: HEAD is ancestor of main
PROOF: rev-list --count main..HEAD = 0
PROOF: branch name 'chore/wtc-153-rows-a' is free
PROOF: activated 'chore/wtc-153-rows-a' from explicit 'main' ref; tip == ccf43655406a0ebbeae750612aff50eba5d955cb
RESULT: ok
```

The row's real task is this evidence file's commit; the uninterrupted tail (`record-validation` → `land` → `park` → `delete-branch`, then closing `inspect`) runs after this commit and its verbatims land in the closing cycle's commit.

### Row 1 — the uninterrupted tail (recorded in the closing cycle's commit)

The real task committed as `448c9c3f6ffa8c8c118d688d9d213ad48de3228c`; the tail then ran uninterrupted, every verb exit 0:

```text
PROOF: SELF worktree lease held for 'decision-record' with matching scope
POLICY: satellite ignored residue: none present
PROOF: validation record bound: 'chore/wtc-153-rows-a' @ 448c9c3f6ffa8c8c118d688d9d213ad48de3228c
RESULT: ok

PROOF: SELF worktree lease held for 'decision-record' with matching scope
PROOF: integration lease held
PROOF: primary is on 'main' (re-read live under the integration lease)
PROOF: primary clean (status --porcelain empty)
PROOF: no operation markers in primary
FACT: upstream read: ahead 12, behind 0 (ahead-only is the allowed steady state)
PROOF: freshness: 'main' is ancestor of 'chore/wtc-153-rows-a'
PROOF: branch tip == validated_tip (448c9c3f6ffa8c8c118d688d9d213ad48de3228c)
POLICY: satellite ignored residue: none present
PROOF: satellite clean
FACT: satellite currently on: 'chore/wtc-153-rows-a'
PROOF: landed: 448c9c3f6ffa8c8c118d688d9d213ad48de3228c is ancestor of 'main'
FACT: integration lease released
RESULT: ok

PROOF: SELF worktree lease held for 'decision-record' with matching scope
FACT: base pinned: primary checkout is on 'main'
POLICY: satellite ignored residue: none present
PROOF: containment: HEAD is ancestor of 'main'
PROOF: detached HEAD at 448c9c3f6ffa8c8c118d688d9d213ad48de3228c
POLICY: satellite ignored residue: none present
PROOF: clean per ignored-state policy
PROOF: HEAD is ancestor of main
PROOF: rev-list --count main..HEAD = 0
FACT: worktree lease for 'decision-record' released (proven re-park)
RESULT: ok

FACT: base pinned: primary checkout is on 'main'
PROOF: 'chore/wtc-153-rows-a' is not checked out in any worktree
PROOF: 'chore/wtc-153-rows-a' is ancestor of 'main'
PROOF: branch 'chore/wtc-153-rows-a' safe-deleted
FACT: validation record for 'chore/wtc-153-rows-a' trashed
RESULT: ok

FACT: base pinned: primary checkout is on 'main'
FACT: satellite 'decision-record' at /Users/jp/.agents-worktrees/decision-record locked=True reason='parked skill workspace (permanent)'
FACT: head: detached at 448c9c3f6ffa8c8c118d688d9d213ad48de3228c
FACT: op markers: none
FACT: tree: clean (porcelain 0, unknown-ignored 0, reported-ignored 0)
FACT: ancestry: HEAD is ancestor of 'main'; ahead 0
FACT: lease wt-decision-record.lease: absent
STATE: PARKED
RESULT: ok
```

**Row 1 (Claude half, 1.5.3): PASS.**

## Rows 5 and 6 — carried forward from the 1.5.2 record (not rerun): the explicit proof boundary

JP's condition: rows 5 and 6 may carry forward "if the patch touches only the shared discovery invariant and their record/state-routing logic remains byte-identical." The boundary, diff-verified: the 1.5.3 diff (`30c32ea..ccf4365`, files `plugins/git-cycle/skills/worktree-task-cycle/scripts/worktree_cycle.py` + `tests/test_worktree_cycle.py` + the three lockstep docs) touches exactly **one helper hunk**, inside `discover` — the `topo.leases` addition to the store-integrity tuple plus the refusal message's trailing clause. `load_record`, `write_record`, `record_file`, `record-validation`'s dispatch, `land`'s record consumption, `delete-branch`'s record handling, `inspect`'s state mapping, `read_owner`, `classify_owner`, `scope_matches`, `acquire_lease`, `require_self_wt_lease`, and every verb function carry zero hunks — record handling and state routing are byte-identical to 1.5.2. The only new code on rows 5/6's execution paths is the `discover`-time lease-root check, which passes trivially against the real store and is separately exercised by the two new regression pins. Rows 5 and 6's 1.5.2 PASS therefore stands for 1.5.3 record/state-routing behavior; they are carried results, never 1.5.3 execution claims. (Row 4's 1.5.1→1.5.2 carry rested on the same argument shape; at 1.5.3 row 4 is instead **rerun directly**, below.)

## Row 4 — foreign-lease adjudication rerun (satellite `work-router`, recorded in this closing commit)

Fixture authority: design v3 §7's "previously scoped fabricated-lease manipulations remain authorized only for those proving fixtures, never for a real foreign lease", re-invoked by JP's 2026-07-17 instruction "Rerun Claude rows 1, 2, and 4" — the row is defined by that fixture. The lease below is a fabricated proving fixture (session id `fabricated-session-row4`), planted directly in the live lease root; no real foreign lease was touched. Unlike at 1.5.2, this is a direct 1.5.3 execution, per JP's ruling that row 4 directly covers lease adjudication.

Baseline `inspect <work-router> --base main` read `STATE: PARKED` (exit 0, detached at `84f556f…`, lease absent). Fabricated lease planted at `.git/skill-worktree/leases/wt-work-router.lease` (owner.json: session_id `fabricated-session-row4`, runtime `claude-code`, branch `chore/row4-fabricated`). `lease-acquire <work-router> --branch chore/wtc-row4-probe-153 --purpose "row-4 probe (1.5.3)"` then **refused, exit 2**, printing the owner facts:

```text
REFUSE: lease wt-work-router.lease is held by a FOREIGN session: session_id='fabricated-session-row4' runtime='claude-code' worktree='work-router' branch='chore/row4-fabricated' purpose='row-4 proving fixture (fabricated)' acquired_at='2026-07-17T00:00:00Z'; fail closed — only an explicit user-authorized break may remove it
RESULT: refused
```

`inspect <work-router> --base main` mapped the state (exit 0):

```text
FACT: base pinned: primary checkout is on 'main'
FACT: satellite 'work-router' at /Users/jp/.agents-worktrees/work-router locked=True reason='parked skill workspace (permanent)'
FACT: head: detached at 84f556f5647c3509c7d45904ebea2b142fb72a63
FACT: op markers: none
FACT: tree: clean (porcelain 0, unknown-ignored 0, reported-ignored 0)
FACT: ancestry: HEAD is ancestor of 'main'; ahead 0
FACT: lease wt-work-router.lease: FOREIGN — session_id='fabricated-session-row4' runtime='claude-code' worktree='work-router' branch='chore/row4-fabricated' purpose='row-4 proving fixture (fabricated)' acquired_at='2026-07-17T00:00:00Z'
STATE: LEASE-ORPHANED
POLICY: lease present but not verified SELF (foreign, unreadable, or owner unknown without session identity); surface the owner facts — only the user may authorize the break
RESULT: ok
```

User-authorized break (authorization quoted above; the fabricated fixture was `trash`ed by the agent in the visible transcript), then re-acquire and release, both exit 0:

```text
FACT: worktree lease for 'work-router': acquired (branch 'chore/wtc-row4-probe-153')
RESULT: ok

FACT: base pinned: primary checkout is on 'main'
PROOF: detached HEAD at 84f556f5647c3509c7d45904ebea2b142fb72a63
POLICY: satellite ignored residue: none present
PROOF: clean per ignored-state policy
PROOF: HEAD is ancestor of main
PROOF: rev-list --count main..HEAD = 0
FACT: worktree lease for 'work-router' released (satellite proven PARKED)
RESULT: ok
```

Lease root empty after release (`ls -A` count 0). **Row 4 (Claude half, 1.5.3): PASS** — the composition note in Honest bounds stands: the stale-foreign variant now composes a rerun row 4 with a carried row 5.

## Closing note — this commit (documentation-only cycle, satellite `decision-record`)

This commit lands row 1's tail verbatims, row 4's verbatims, the completed-status header, and the ledger completion update through the same lifecycle on `decision-record` (branch `chore/wtc-153-rows-docs`); its own lifecycle outputs live in the session transcript only. Across the 1.5.3 landing cycle plus the two rerun cycles the helper executed 3 landings, 3 parks, 3 branch deletions, and 1 foreign-lease adjudication, every proof line green, no refusal improvised around. Both satellites end `STATE: PARKED` with the lease root and validations dir empty. Rows 0/3 and every Codex half remain open pending Gate B (local `codex-plugins-sync.sh --publish git-cycle`, then a fresh Codex session against the republished 1.5.3 cache); Gate C (mirror + push) follows the completed matrix.
