# Evidence the user supplied for the pipeline decision

Ten excerpts. "Non-defect failure" means a failed run where no code defect was found afterwards.

## E1. Failure taxonomy, last 200 non-defect failures (platform team's classification, August)

| Where | Count | Error text |
| --- | --- | --- |
| Integration stage | 181 | `ERROR: relation "..." already exists` (117) or `ERROR: deadlock detected` (64), both raised during the suite's setup migration before any test runs |
| End-to-end stage | 9 | browser timeouts, all while the third-party staging environment was degraded |
| Runner provisioning | 7 | runner failed to start |
| Unclassified | 3 | |

## E2. Pipeline configuration (excerpt from `.ci/pipeline.yaml`)

```yaml
integration:
  parallel: 4                     # shards
  services:
    - postgres:15                 # one service container for the stage
  variables:
    DATABASE_URL: postgres://ci@postgres/app_test
  before_script:
    - bin/migrate                 # runs in every shard
  script:
    - bin/test --suite integration --shard $CI_NODE_INDEX
```

## E3. Test framework configuration and documentation

`test/config.yaml` (excerpt):

```yaml
database_per_worker: false
```

Framework documentation, version 5 and later: "`database_per_worker: true` creates and migrates a separate database `app_test_<n>` for each worker or shard and points that worker at it. Requires only that the service account can create databases." The project is on framework version 5.4.

## E4. Auto-retry experiment (two weeks in June)

One automatic retry reduced reported failures from 31% to 12% of runs. Integration-stage runner minutes doubled during the experiment (about $2,400 more per month at that rate). In the retro, engineers said they had stopped reading failures and "just wait for the retry"; the experiment was reverted.

## E5. Ten most frequently failing tests, last month

All ten are integration tests. Every recorded failure of each is one of the two errors in E1, raised in setup before the test body runs. Each of the ten passes 200 of 200 runs when run alone on a runner.

## E6. Runner metrics, last month

CPU 35% average, memory 50% average across the pipeline. The seven provisioning errors and the nine end-to-end timeouts occurred on the two days the third-party staging environment was degraded, per its status page.

## E7. Timeline

The non-defect failure rate was about 4% through April. In the week of May 20 the integration stage was changed from one shard to four to cut its duration from 38 minutes to 11; the whole pipeline went from 52 minutes to 17. The failure rate rose to about 30% that week and has stayed there. A trial in July at two shards ran the stage in 21 minutes with failures at about 18%.

## E8. Dependency state

The lockfile has pinned exact versions since 2024. Dependency caching has been enabled since 2023; cache hit rate 97%.

## E9. Assessments on file (June)

- Mocking: the integration suite exists to test the ORM and query layer against a real Postgres; the platform team's estimate is that mocking the database removes about 80% of the suite's assertions.
- Rewrite: six engineer-weeks, platform team estimate.

## E10. Merge policy (engineering handbook)

Unit, integration, and end-to-end checks must pass on the exact merge SHA. Pipeline wall-clock budget for the merge queue: twenty minutes.
