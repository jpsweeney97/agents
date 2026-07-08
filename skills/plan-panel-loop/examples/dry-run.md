# Plan Panel Loop Dry Run

This example shows the intended shape of a run. It is illustrative, not behavior proof.

Prompt: `Use $plan-panel-loop on docs/plans/cache-refresh.md.`

Setup:

- Target: `docs/plans/cache-refresh.md`
- Authority: the plan plus `docs/architecture/cache.md`, because the plan cites it as the source of truth
- Mutation boundary: patch `docs/plans/cache-refresh.md` only
- Loop cap: two cycles
- Panel proof: subagents if available; otherwise label feedback as single-agent simulated
- Reviewer containment: subagents are read-only reviewers, may not edit files, and may not launch nested panels

Cycle 1 panel:

- Source-of-truth drift lens: checks whether the plan contradicts `docs/architecture/cache.md`
- Execution sequencing lens: checks whether the steps can be run in order without hidden setup
- Proof and rollback lens: checks whether validation and recovery are concrete enough to trust

Consolidated findings:

- Accepted: the plan says to refresh all cache shards at once, but the architecture doc requires shard-by-shard rollout.
- Accepted: the validation step says "check metrics" without naming the metric or pass condition.
- Rejected: a proposed database migration blocker was unsupported because the plan never touches schema.

Patch:

- Replace the all-at-once rollout step with shard-by-shard rollout.
- Add the specific metric, expected range, and rollback trigger.
- Leave architecture docs untouched because the mutation boundary is the plan only.

Cycle 1 re-review:

- Source-of-truth drift finding is closed.
- Proof and rollback finding is closed.
- No new material finding appears.

Closeout:

```markdown
Target: docs/plans/cache-refresh.md
Cycles run: 1 of 2
Panel proof: subagents
Reviewer anomalies: none
Changed: rollout and validation sections
Resolved findings: shard rollout mismatch; vague metric gate
Remaining findings / stop status: none
Verified: re-read patched sections; git diff --check
Proof boundary: source and whitespace checks only; no implementation or runtime proof
Next move: none
```

## Canceled Reviewer Mutation

This example shows the recovery move when a reviewer violates containment.

Cycle 2 panel setup:

- Before dispatch, the main agent snapshots `git status --short --branch --untracked-files=all` and `git diff --name-only -- docs/plans/cache-refresh.md`.
- One reviewer is assigned a proof lens with an explicit read-only brief.

Anomaly:

- The reviewer runs long and is canceled.
- The post-panel mutation audit shows `docs/plans/cache-refresh.md` changed.
- The main agent stops the normal loop, inspects the target diff, and labels the change as an unauthorized reviewer mutation.

Disposition:

- If the edit is correct and within the named mutation boundary, the main agent may adopt it as the main patch after re-reading the relevant authority and recording the finding it closes.
- If the edit is wrong, unrelated, outside the mutation boundary, or unsafe to resolve without user authority, the main agent asks before replacing or reverting it.
- The main agent does not launch another panel until the artifact state is normalized and the carried-forward finding ledger is updated.

Closeout excerpt:

```markdown
Reviewer anomalies: one canceled reviewer edited the target; inspected diff and replaced it with the main-agent patch
Verified: post-panel mutation audit; re-read patched sections; git diff --check
Proof boundary: containment recovery was source-checked only; no implementation or runtime proof
```
