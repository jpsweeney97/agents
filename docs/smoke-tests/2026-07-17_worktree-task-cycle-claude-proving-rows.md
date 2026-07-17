# worktree-task-cycle — Claude proving rows 1, 2, 4, 5, 6

- **Status at this commit:** rows 4 and 5 PASS; row 6's real task in flight (this commit); rows 1, 2 pending. Rows 0/3 and all Codex halves remain post-Gate-B.
- **Date:** 2026-07-17
- **Target:** the Claude half of the proving matrix (design v3 §7; commissioned by JP's 2026-07-17 review: "run and durably record Claude rows 1, 2, 4, 5, and 6 against the pilot satellites") for `worktree-task-cycle` at **git-cycle 1.5.1**, landed on `main` at `56e382988c330235e5afa8c122f8edf92c02d277`.
- **Helper under proof:** invoked strictly at the installed path `/Users/jp/.claude/skills/git-cycle/skills/worktree-task-cycle/scripts/worktree_cycle.py` for every verb (row 2's path-resolution record is in §Rows 1+2).
- **Environment:** macOS 26.5.2; helper interpreter `python3` = Python 3.14.2 (system PATH; the helper's floor is 3.9); the 69-test suite ran under uv-managed CPython 3.13.12 at the 1.5.1 landing.
- **Honest bounds:** every row here is **Claude-only** — never claim cross-runtime coverage from this file. Row 0 (Codex at-fire path probe) and row 3 (stale-base) are Codex rows and run only after Gate B in a fresh Codex session against the republished cache. The stale-*foreign* variant is proven by composition of rows 4+5, stated as composition, not claimed whole. The Codex cache is at git-cycle 1.4.2 throughout; `codex-plugins-sync.sh --check` reporting `NOT-INSTALLED: git-cycle@1.5.1` is the expected Gate-B canary window, and no publish, mirror, or push happened in these runs (Gates B and C withheld).
- **Evidence discipline:** every fenced block below is the verbatim stdout/stderr of a command run this session on this machine, captured to a log at execution time; nothing is retyped from memory.

## Row 4 — foreign-lease refusal (satellite `work-router`)

Authorization for the fixture, quoted from JP (2026-07-17): "The previously scoped fabricated-lease manipulations remain authorized only for those proving fixtures, never for a real foreign lease." The lease below is a fabricated proving fixture (session id `fabricated-session-row4`), planted directly in the lease root; no real foreign lease was touched.

Baseline `inspect <work-router> --base main` (exit 0):

```text
FACT: base pinned: primary checkout is on 'main'
FACT: satellite 'work-router' at /Users/jp/.agents-worktrees/work-router locked=True reason='parked skill workspace (permanent)'
FACT: head: detached at 4ccfa078315db1135a37abf357e2f50f68682736
FACT: op markers: none
FACT: tree: clean (porcelain 0, unknown-ignored 0, reported-ignored 0)
FACT: ancestry: HEAD is ancestor of 'main'; ahead 0
FACT: lease wt-work-router.lease: absent
STATE: PARKED
RESULT: ok
```

Fabricated lease planted at `.git/skill-worktree/leases/wt-work-router.lease` (owner.json: session_id `fabricated-session-row4`, runtime `claude-code`, branch `chore/row4-fabricated`). `lease-acquire <work-router> --branch chore/wtc-row4-probe --purpose "row-4 probe"` then **refused, exit 2**, printing the owner facts:

```text
REFUSE: lease wt-work-router.lease is held by a FOREIGN session: session_id='fabricated-session-row4' runtime='claude-code' worktree='work-router' branch='chore/row4-fabricated' purpose='row-4 proving fixture (fabricated)' acquired_at='2026-07-17T00:00:00Z'; fail closed — only an explicit user-authorized break may remove it
RESULT: refused
```

`inspect <work-router> --base main` mapped the state (exit 0):

```text
FACT: base pinned: primary checkout is on 'main'
FACT: satellite 'work-router' at /Users/jp/.agents-worktrees/work-router locked=True reason='parked skill workspace (permanent)'
FACT: head: detached at 4ccfa078315db1135a37abf357e2f50f68682736
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
FACT: worktree lease for 'work-router': acquired (branch 'chore/wtc-row4-probe')
RESULT: ok

FACT: base pinned: primary checkout is on 'main'
PROOF: detached HEAD at 4ccfa078315db1135a37abf357e2f50f68682736
POLICY: satellite ignored residue: none present
PROOF: clean per ignored-state policy
PROOF: HEAD is ancestor of main
PROOF: rev-list --count main..HEAD = 0
FACT: worktree lease for 'work-router' released (satellite proven PARKED)
RESULT: ok
```

Lease root empty after release (`ls` count 0). **Row 4: PASS.** Note the `FACT: base pinned` line in the release output — the 1.5.1 helper live.

## Row 5 — interrupted COMMITTED-UNLANDED reconstruction (satellite `decision-record`, this file's first commit is the row's real task)

Design v3 §7 row 5: real task, commit + record-validation, then manufacture the lease-absent state by explicitly authorized direct fixture manipulation — `trash` of the lease dir under the proving plan's authority, quoted in the transcript — not via `lease-release` (which refuses mid-task release by design); fresh `inspect` maps the state; re-lease; land.

The row's real task was the evidence commit `ad5928a618e36ad6ded0ef532713c370a0bd97c2` on branch `chore/wtc-claude-proving-rows` (activated from explicit `main` at `56e38298…`; the file's prior commit records the truth boundary). `record-validation` bound the record to that exact tip (exit 0):

```text
PROOF: SELF worktree lease held for 'decision-record' with matching scope
POLICY: satellite ignored residue: none present
PROOF: validation record bound: 'chore/wtc-claude-proving-rows' @ ad5928a618e36ad6ded0ef532713c370a0bd97c2
RESULT: ok
```

The lease-absent interruption was then manufactured by the agent `trash`ing its own lease dir directly (authority: design v3 §7 row 5's explicitly authorized direct fixture manipulation, re-authorized by JP 2026-07-17 — "The previously scoped fabricated-lease manipulations remain authorized only for those proving fixtures"; deliberately **not** `lease-release`, which refuses mid-task by design). Fresh `inspect <decision-record> --base main` mapped the state (exit 0):

```text
FACT: base pinned: primary checkout is on 'main'
FACT: satellite 'decision-record' at /Users/jp/.agents-worktrees/decision-record locked=True reason='parked skill workspace (permanent)'
FACT: head: branch 'chore/wtc-claude-proving-rows' at ad5928a618e36ad6ded0ef532713c370a0bd97c2
FACT: op markers: none
FACT: tree: clean (porcelain 0, unknown-ignored 0, reported-ignored 0)
FACT: ancestry: HEAD is NOT ancestor of 'main'; ahead 1
FACT: lease wt-decision-record.lease: absent
FACT: validation record for 'chore/wtc-claude-proving-rows': ok, tip-match=True
STATE: COMMITTED-UNLANDED
FACT: lease state at interruption: absent
RESULT: ok
```

Re-lease succeeded (`worktree lease for 'decision-record': acquired`, exit 0), then `land` completed the reconstruction (exit 0):

```text
PROOF: SELF worktree lease held for 'decision-record' with matching scope
PROOF: integration lease held
PROOF: primary is on 'main' (re-read live under the integration lease)
PROOF: primary clean (status --porcelain empty)
PROOF: no operation markers in primary
FACT: upstream read: ahead 2, behind 0 (ahead-only is the allowed steady state)
PROOF: freshness: 'main' is ancestor of 'chore/wtc-claude-proving-rows'
PROOF: branch tip == validated_tip (ad5928a618e36ad6ded0ef532713c370a0bd97c2)
POLICY: satellite ignored residue: none present
PROOF: satellite clean
FACT: satellite currently on: 'chore/wtc-claude-proving-rows'
PROOF: landed: ad5928a618e36ad6ded0ef532713c370a0bd97c2 is ancestor of 'main'
FACT: integration lease released
RESULT: ok
```

`park` re-parked with all four proofs and released the lease (`worktree lease for 'decision-record' released (proven re-park)`, exit 0); `delete-branch` ancestry-proved the `-d` and trashed the record (`branch 'chore/wtc-claude-proving-rows' safe-deleted`, exit 0). **Row 5: PASS.** Composition note: together with row 4 this proves the stale-*foreign* reconstruction variant by composition (foreign-lease adjudication + lease-absent reconstruction), stated as composition, not claimed as a whole-path run.

## Row 6 — interrupted LANDED-UNPARKED resume (satellite `work-router`, this file's second commit is the row's real task)

Design v3 §7 row 6: after a real landing, stop before park; fresh `inspect` maps the state (record still present → provenance proven); resume park + delete-branch.

Status at this commit (truth boundary): lease-acquire and activation of `chore/wtc-claude-proving-rows-2` from explicit `main` at `ad5928a…` have run, and this commit is the row's real task. The landing, the deliberate stop, the LANDED-UNPARKED mapping, and the resume necessarily happen **after** this commit; their verbatim outputs land in the next evidence commit (cycle D, rows 1+2's task).

## Rows 1 + 2 — normal full cycle + helper path resolution (satellite `decision-record`) — pending; runs as cycle D

Cycle plan for the remaining evidence commits: cycle C (row 6) lands row 5's verbatims; cycle D (rows 1+2) lands row 6's verbatims; a final documentation-only cycle E lands cycle D's own post-commit verbatims and the ledger completion line — each commit only claims what has already happened at its commit time.
