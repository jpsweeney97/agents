# Evidence the user supplied for the partner-export decision

Nine excerpts. All measurements are from the last thirty nights unless stated.

## E1. Job timing profile (scheduler logs, last thirty nights)

The job starts at 01:15 every night, after Corvid finalizes its catalog at 01:00. Its timeout is five hours (killed at 06:15).

| Step | Median | Worst finished night | Notes |
| --- | --- | --- | --- |
| 1. Fetch Corvid catalog over the API | 4h 05m | 4h 51m | Four further nights were killed mid-fetch at the timeout |
| 2. Aggregate Meridian pricing (Postgres) | 24m | 31m | Reads only Meridian's own database; runs after step 1 today |
| 3. Build the four partner files | 9m | 12m | |
| 4. Compress and upload | 5m | 7m | |

Nights delivered after 06:00: 9 of 30 (4 killed at the timeout, 5 finished between 06:02 and 06:40). Nights delivered between 05:30 and 06:00: 11 of 30.

## E2. Corvid catalog API, version 3 reference (excerpt)

- `GET /v3/catalog/items` returns the catalog in pages. `page_size`: default 50, maximum 1000 (the maximum was raised from 200 in v3.2, released 2026-06-09).
- Rate limit: 300 requests per minute per API key. Daily quota: 250,000 requests per key, resetting at 00:00 UTC. Exceeding either returns HTTP 429.
- There is no `modified_since` or delta filter and no ETag or conditional GET support. Item identifiers are regenerated on every nightly catalog build, so an item's identifier does not persist from one night to the next.
- The catalog is finalized at 01:00 local time each night. Requests before that return the previous day's catalog.

## E3. Corvid support ticket #4471 (opened 2026-08-12, closed 2026-08-19), summary

- Bulk catalog export (nightly CSV over SFTP): available on the Enterprise tier only. Moving tiers requires a new agreement; Corvid quotes ten to twelve weeks and about $48,000 per year.
- Additional API keys on the same account: not offered on our tier.
- Rate-limit or daily-quota increases: not offered on our tier.
- A delta or changed-since endpoint: "on the roadmap, no date."

## E4. Job configuration (excerpt from `partner-export/config.yaml`)

```yaml
corvid:
  base_url: https://api.corvid.example/v3
  page_size: 50          # client library default, unchanged since the job was written
  concurrency: 4
  retry:
    max_attempts: 5
    backoff: exponential
timeout_hours: 5
```

## E5. Job log, most recent night, fetch summary line

```
corvid fetch complete: 2,093,412 items in 41,869 requests, elapsed 4h07m, 429 responses: 312 (all succeeded on retry)
```

## E6. Worker metrics (thirty-day averages)

- Instance: m6-standard-2 (2 vCPU, 8 GB), $71 per month. Total monthly spend attributable to the job: $118.
- CPU during the fetch: 6% average, 14% peak. Memory: 31% of 8 GB. Network: 3.1 Mbps average during the fetch.
- Postgres during step 2: 40% CPU on the database host for the 24 minutes; no lock waits.

## E7. Partner contract (renewal signed July 2026, twelve-month term), excerpt

- Delivery by 06:00 local time each day.
- The feed must reflect Corvid's catalog as finalized at 01:00 that day.
- All six feed sections are required, including inventory and pricing, the two largest.
- Minutes of the Q2 review (2026-04-22): the partners declined a later delivery time; the 06:00 time was carried into the July renewal at their request.

## E8. March incident note (excerpt)

- 2026-03-03: retries with exponential backoff added after two nights of failures on HTTP 429. Since then no run has failed on an error; every failure has been the five-hour timeout.
- 2026-03-10: tried diffing the fetched catalog against the previous night's snapshot so that only changed items are processed downstream. The diff itself ran in under a minute, but the full catalog still had to be fetched first because identifiers do not persist, so no time was saved on the fetch.

## E9. Team notes

- Raising fetch concurrency above 4 was tried in March: the rate of 429 responses rose and total throughput did not, because the 300-per-minute limit applies to the key, not to each connection.
- A rerun after a failed night takes as long as the original run. A rerun started at 06:00 has finished after 10:00 on both occasions it was tried.
- Nobody on the team has changed the Corvid client's request settings since the job was written in 2025.
