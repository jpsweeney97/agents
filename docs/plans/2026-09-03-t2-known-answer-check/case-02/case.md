# Decision case: the failing main-branch pipeline

## Decision question

How should the platform team bring the main-branch CI pipeline's non-defect failure rate down, from about thirty percent of runs to under five percent, within the next month?

## Background, as the user stated it

Sixty engineers merge through one pipeline with unit, integration, and end-to-end stages. A red pipeline blocks the merge, so engineers re-run failed pipelines by hand and wait. Over the last month about thirty percent of main-branch runs failed without any code defect being found afterwards. Runner minutes cost about $9,000 a month. Engineers have started treating a red pipeline as noise.

## User's candidates (marked as theirs, quoted exactly)

- **Retry failed jobs automatically** — "Configure the pipeline to re-run any failed job up to two times before reporting a failure." (user's)

## Hard constraints the user confirmed, with what each costs

1. The merge policy stands: every required check (unit, integration, end-to-end) must pass on the exact commit before merge, and the pipeline's twenty-minute wall-clock budget for the merge queue stands. What it costs: options that skip a required check, make it advisory, or push the pipeline past twenty minutes are out.
2. No new CI vendor or hosted test service this quarter; there is a procurement freeze. What it costs: platform moves are out.
3. The platform team has two engineer-weeks for this in the month. What it costs: rewriting a test suite is out.

## Values the user stated

- Engineers must be able to trust a red pipeline again: a failure should mean a defect.
- Fix causes rather than symptoms where a cause can be found.
- Keep runner cost roughly flat.

## Survivor count

About four.

---

# Field

Grouped by what each option changes: how failures are handled, the tests themselves, the infrastructure they run on, the process around them. Order within a group is not a quality order.

## Change how failures are handled

**Retry failed jobs automatically** (user's) — "Configure the pipeline to re-run any failed job up to two times before reporting a failure."
Sets it apart: the fastest change available; accepts the failures and hides them from the merge queue.

**Quarantine flaky tests into a non-blocking stage** — Move tests that fail intermittently into a separate stage whose result does not block merge, and work through them over time.
Sets it apart: restores a trustworthy red on the blocking stages immediately; the quarantined tests stop protecting anything until fixed.

**Add a flaky-test detector that quarantines on repeat failure** — Track each test's pass history and automatically move a test to the non-blocking stage after it fails then passes on the same commit.
Sets it apart: the quarantine option with the judgment automated; keeps working after the platform team moves on.

**Widen test timeouts** — Raise the per-test and per-stage timeouts so slow-but-correct runs stop being reported as failures.
Sets it apart: a one-line change; helps only if the failures are timeouts.

## Change the tests

**Fix the ten flakiest tests by hand** — Take the ten tests that fail most often, find what makes each intermittent, and fix them one at a time.
Sets it apart: the direct route; treats the failures as test defects to be found and repaired.

**Rewrite the integration suite** — Replace the integration tests with a new suite designed for isolation from the start.
Sets it apart: the deepest change; pays off for years if the current suite's design is the problem.

**Mock the external services the integration tests call** — Replace real dependencies in the integration stage with in-process fakes so the tests stop depending on anything outside the runner.
Sets it apart: removes environmental variance entirely; the tests then exercise less of the real system.

**Move the end-to-end tests to a nightly schedule** — Take the end-to-end stage out of the per-commit pipeline and run it once a night against main.
Sets it apart: shortens and steadies the per-commit pipeline; a defect the end-to-end tests would catch lands on main for up to a day.

## Change the infrastructure

**Use larger runners** — Move the pipeline to runners with more CPU and memory.
Sets it apart: a configuration change; bets the failures come from resource pressure.

**Cache dependencies between runs** — Store installed dependencies so each run does not fetch and build them again.
Sets it apart: speeds every run; affects failures only if installs are what fail.

**Pin all dependency versions** — Lock every dependency to an exact version so runs are reproducible.
Sets it apart: removes one source of run-to-run variance; changes nothing if versions are already locked.

**Isolate the integration shards' databases** — Run each integration shard against its own database instance rather than one shared across the stage.
Sets it apart: the narrowest change in the field; touches the stage's setup and nothing else.

**Reduce the number of shards** — Run the integration stage with fewer parallel shards.
Sets it apart: reduces contention by doing less at once; makes the stage take longer.

**Switch to a different CI vendor** — Move the pipeline to a CI product with better parallelism and flakiness tooling.
Sets it apart: replaces the platform rather than repairing it; the largest move in the field.

## Change the process

**Require engineers to reproduce a failure locally before re-running** — Stop by-hand re-runs; a failed pipeline must be reproduced and explained before the job is run again.
Sets it apart: costs no engineering; turns every failure into an investigation, whether or not one is warranted.
