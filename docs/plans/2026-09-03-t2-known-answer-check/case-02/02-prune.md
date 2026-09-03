# Prune: the failing main-branch pipeline

## Survivors (field order, exact wordings)

1. **Retry failed jobs automatically** (user's) — "Configure the pipeline to re-run any failed job up to two times before reporting a failure."
2. **Add a flaky-test detector that quarantines on repeat failure** — Track each test's pass history and automatically move a test to the non-blocking stage after it fails then passes on the same commit.
3. **Fix the ten flakiest tests by hand** — Take the ten tests that fail most often, find what makes each intermittent, and fix them one at a time.
4. **Isolate the integration shards' databases** — Run each integration shard against its own database instance rather than one shared across the stage.

Four survivors; the count asked for was about four. Fifteen options in the field, eleven cut, each with a record below.

## Notes carried to Develop

- Two survivors sit near constraint 1 and need the user's reading of it, not mine. The detector moves individual tests out of a required check into a non-blocking stage; the check itself stays blocking, and whether that counts as "making it advisory" is the user's call. Automatic retry adds wall-clock on every failed run, which can push a long job past the twenty-minute budget.
- Every cut marked "survivor count" below is a bet on one specific cause (runner resources, dependency installs, version drift, external services) that no fact in the case confirms or rules out. The first step of "Fix the ten flakiest tests by hand" is finding what makes each test intermittent; that finding is the evidence that would revive the matching bet.

## Cut records

```text
Option:         Quarantine flaky tests into a non-blocking stage
Cut:            same reason, judgment call
Reason:
  This and "Add a flaky-test detector that quarantines on repeat failure" work by the same move: take intermittently failing tests out of the blocking stages so a red on those stages means a defect again. They succeed together if quarantine is acceptable under constraint 1 and the values, and fail together if it is not. One is kept. The detector is kept because it decides membership from evidence (a test that failed then passed on the same commit is, by definition, a non-defect failure) and keeps working after the platform team's two weeks end; this option depends on someone judging what is flaky and keeping the list current.
Strongest case: The cheapest way to restore a trustworthy red: a stage move and a list, no tracker to build, leaving nearly all of the two engineer-weeks for fixing the quarantined tests, which this wording alone commits to ("work through them over time").
Revive if:
  The detector cannot be built within the two engineer-weeks, or the team wants a human to decide what leaves the blocking path, or the fixing commitment in this wording is what the user values and the detector wording drops it.

Option:         Widen test timeouts
Cut:            same reason, judgment call
Reason:
  This and "Retry failed jobs automatically" both leave the failing runs as they are and change only when the pipeline reports a failure: retry by running again, this by waiting longer. They succeed together if hiding non-defect failures without finding a cause is acceptable, and fail together against the value of fixing causes rather than symptoms. Retry is the user's candidate, so the user's wording is kept. Retry also covers every kind of intermittent failure; this covers only failures that are timeouts.
Strongest case: A one-line change with no extra runs; if the thirty percent is mostly slow-but-correct runs killed at a limit, it removes most of the failures on its own without re-running anything.
Revive if:
  The failures turn out to be mostly timeouts, or retry's added runner minutes break the flat-cost value where this would not.

Option:         Rewrite the integration suite
Cut:            constraint, fact-established
Reason:
  Constraint 3 gives the platform team two engineer-weeks and states what that costs: rewriting a test suite is out. This option is a rewrite of a test suite.
Strongest case: If the current suite's design is the source of the failures, this is the only option that removes the source for good rather than working around it.
Revive if:
  The engineering budget changes, or the user re-scopes the rewrite to something the two weeks can hold.

Option:         Move the end-to-end tests to a nightly schedule
Cut:            constraint, fact-established
Reason:
  Constraint 1 says every required check, end-to-end included, must pass on the exact commit before merge. A nightly run against main runs once a day against whatever main is then, not on each commit before it merges, so the end-to-end check no longer passes on the exact commit before merge. The option's own description states the cost: a defect the end-to-end tests would catch lands on main for up to a day.
Strongest case: The end-to-end stage is usually the slowest and least stable stage; taking it out of the per-commit path could remove much of the failure rate and most of the wall-clock pressure in one move.
Revive if:
  The user changes the merge policy so end-to-end is no longer a required pre-merge check.

Option:         Use larger runners
Cut:            survivor count, judgment call
Reason:
  A low-confidence cut to reach the count. Whether this is serious could not be resolved at sketch depth: it pays off only if the failures come from resource pressure on the runners, and nothing in the case says whether they do. It also treats the pressure by buying capacity rather than finding what consumes it, and larger runners cost more per minute, which puts the flat-cost value at risk unless faster runs offset it.
Strongest case: A configuration change that touches all three stages at once; if the failures are memory or CPU starvation, it removes them within days and may shorten wall-clock enough to give the other options room under the twenty-minute budget.
Revive if:
  Investigating the flakiest tests shows out-of-memory kills, CPU starvation, or timeouts under load as a leading cause.

Option:         Cache dependencies between runs
Cut:            survivor count, judgment call
Reason:
  A low-confidence cut to reach the count. Whether this is serious as an answer to the question could not be resolved at sketch depth: its own description says it affects failures only if installs are what fail, and nothing in the case says how many failures happen at install. It shortens every run, which is a benefit, but the question asks how to bring the non-defect failure rate down.
Strongest case: A small change that saves runner minutes and wall-clock on every run, which helps the flat-cost value and the twenty-minute budget whatever else is chosen, and removes install failures if there are any.
Revive if:
  Install or fetch failures are a material share of the failures, or a surviving option needs wall-clock or runner-minute headroom to fit constraint 1 or the cost value.

Option:         Pin all dependency versions
Cut:            survivor count, judgment call
Reason:
  A low-confidence cut to reach the count. Whether this is serious could not be resolved at sketch depth: its own description says it changes nothing if versions are already locked, and the case does not say whether they are. The stated pattern, runs that fail and then pass on re-run with no defect found, fits intermittent failure better than version drift, which tends to fail every run for a while once a new version appears.
Strongest case: If versions are not locked, this removes a whole class of run-to-run difference at almost no cost, and it is good practice regardless.
Revive if:
  Versions turn out not to be locked, or investigating the flakiest tests shows failures that started when a dependency changed.

Option:         Mock the external services the integration tests call
Cut:            survivor count, judgment call
Reason:
  A low-confidence cut to reach the count. Whether this is serious within the month could not be resolved at sketch depth: it pays off only if the integration stage's failures come from the external services it calls, and building an in-process fake for each service is the largest build among the remaining options, with no fact in the case saying how many services there are or whether two engineer-weeks would cover them. Its own description also names a cost the values do not price: the tests then exercise less of the real system, so a green integration stage would mean less than it does now.
Strongest case: If the variance is external, this removes it entirely rather than reducing it, and the integration stage becomes fast and deterministic for good.
Revive if:
  Investigating the flakiest tests shows external-service latency or availability as a leading cause, and the number of services is small enough to fake within the budget.

Option:         Reduce the number of shards
Cut:            same reason, judgment call
Reason:
  This and "Isolate the integration shards' databases" both bet that the integration failures come from shards interfering with each other through shared state; they succeed together if that is the cause and fail together if it is not. One is kept. Isolation is kept because it removes the interference where it happens instead of making it rarer by doing less at once, and because this option's own description says fewer shards makes the stage take longer, which works against the twenty-minute budget in constraint 1.
Strongest case: A single configuration number, no setup work, and if contention is the cause it reduces failures at once while the platform team spends its two weeks elsewhere.
Revive if:
  Giving each shard its own database turns out to exceed the two engineer-weeks, or the contention is over something other than the database, where fewer shards helps and separate databases do not.

Option:         Switch to a different CI vendor
Cut:            constraint, fact-established
Reason:
  Constraint 2 says no new CI vendor this quarter, with a procurement freeze, and states what that costs: platform moves are out. This option is a move to a new CI vendor.
Strongest case: Vendor flakiness tooling and better parallelism could address several causes at once without the platform team building any of it.
Revive if:
  The procurement freeze lifts and the decision is re-opened for next quarter.

Option:         Require engineers to reproduce a failure locally before re-running
Cut:            survivor count, judgment call
Reason:
  A low-confidence cut to reach the count. Whether this is serious as an answer to the question could not be resolved at sketch depth. It changes what engineers do after a red, not how often a red happens without a defect, so on its own it leaves the thirty percent where it is; it lowers the rate only if the investigations it forces turn into fixes someone lands, and the option does not say who lands them. At the stated rate it would also put an investigation in front of roughly one merge in three across sixty engineers, for failures that by their nature often do not reproduce locally.
Strongest case: It costs nothing from the platform team's two engineer-weeks, stops the by-hand re-runs that spend runner minutes and teach engineers to treat red as noise, and turns every failure into a diagnosis, which is the raw material for fixing causes.
Revive if:
  The user wants the investigation load carried by the sixty engineers rather than the platform team, or a surviving option needs a steady supply of diagnosed failures and this is chosen as its feed.
```
