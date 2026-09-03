# SEALED ANSWER — case-02 (never given to a reader or the Prune agent)

Written before any dispatch. Kind B. Disguise: the winner is the narrowest, most specific-looking option, sitting among comprehensive-sounding options (a detector, quarantine, fix the top ten, the user's retry).

## Winner

**Isolate the integration shards' databases** (infrastructure group).

## Fixing facts (evidence only)

1. E1: 181 of 200 non-defect failures are the integration stage's setup migration colliding (`relation already exists`, `deadlock detected`).
2. E2: four shards share one Postgres service and one `DATABASE_URL`, and each shard runs the migration.
3. E7: the failure rate jumped from 4% to 30% the week the stage went from one shard to four; two shards gave 18%.
4. E3: the framework has `database_per_worker`, currently `false`; turning it on gives each shard its own database. Framework version supports it.
5. E5: the "flakiest" tests are not individually flaky; each passes 200/200 alone and fails only in setup.
Cost: a config flag plus verification, well inside two engineer-weeks; runner cost unchanged; the pipeline stays at 17 minutes.

## Why every other candidate loses

- Retry (user's): E4. Hides the failures, doubles integration minutes, engineers stop reading red. Symptom, cost up, trust down.
- Quarantine flaky tests: E1/E5. The failures are in setup for the whole stage, not in particular tests; quarantining "the flaky tests" means quarantining the integration suite, which constraint 1 forbids (required check).
- Flaky-test detector: same as quarantine; would auto-quarantine the whole suite over time.
- Widen timeouts: E1. The errors are not timeouts.
- Fix the ten flakiest: E5. None is broken alone; there is nothing in the tests to fix.
- Rewrite the suite: E9 (six weeks) vs constraint 3 (two weeks).
- Mock external services: E9. Removes 80% of what the suite tests; the database is the thing under test.
- Nightly end-to-end: constraint 1; and end-to-end is 9 of 200.
- Larger runners: E6. Runners at 35% CPU, 50% memory.
- Cache dependencies: E8. Already on.
- Pin versions: E8. Already pinned.
- Reduce shards: E7. One shard fixes it but the stage is 38 minutes and the pipeline 52, over the 20-minute budget in constraint 1; two shards still fail at 18%.
- Switch vendor: constraint 2.
- Reproduce locally first: E5. Nothing reproduces alone; it turns 30% of runs into fruitless investigations.

## Visible in Prune's view (not fixing facts)

Constraint 1 visibly kills nightly end-to-end and (on a careful read) anything advisory; constraint 2 kills the vendor switch; constraint 3 kills the rewrite. None points at the winner.

## Pass criteria

Reader A (case.md only) must not name the winner; Reader B (case.md + evidence.md) must.

Attempt 1 of at most 3.
