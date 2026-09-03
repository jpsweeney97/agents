# Decision case: the nightly partner export

## Decision question

How should the Meridian data team stop the nightly `partner-export` job from missing its 06:00 delivery deadline, with a fix in place within the next six weeks?

## Background, as the user stated it

The job runs every night. It builds the day's product feed for four retail partners from two sources: the Corvid Wholesale catalog, read over Corvid's HTTP API, and Meridian's own pricing database. It then writes one file per partner and uploads them. The partners' contract requires delivery by 06:00 local time. Over the last thirty nights the job missed 06:00 nine times, and on four of those nights it was killed by its own five-hour timeout before finishing. Two partners have complained in writing.

## User's candidates (marked as theirs, quoted exactly)

- **Upgrade the worker to a larger instance** — "Move the job to a bigger machine so it finishes faster." (user's)

## Hard constraints the user confirmed, with what each costs

1. The fix must be live within six weeks, before the quarterly partner review. What it costs: anything that needs procurement, a contract change with the supplier or a partner, or a new vendor agreement is out.
2. No partner or supplier data may pass through a new third-party service without a signed data-processing agreement, and getting one signed takes at least eight weeks. What it costs: new hosted pipeline, orchestration, or data-transfer products are out.
3. Engineering capacity for the six weeks is one engineer at half time, about 120 hours. What it costs: a rewrite, a platform migration, or anything needing a second engineer is out.

## Values the user stated

- Delivering by 06:00 every night matters more than making the job fast on an average night.
- The fix must be something the current team of three can maintain without a specialist.
- Monthly cloud spend for the job should not rise by more than about ten percent.

## Survivor count

About four.

---

# Field

Grouped by what each option changes: when the job runs, how the work is arranged, the machine, the catalog fetch, the delivery terms. Order within a group is not a quality order.

## Change when the job runs

**Start the job earlier** — Move the scheduled start from its current slot to several hours earlier in the night so the same work finishes before 06:00.
Sets it apart: no code change at all; bets that the deadline misses are a scheduling problem rather than a duration problem.

**Raise the job's timeout so it is never killed** — Lift the five-hour ceiling so a slow night finishes late rather than dying and having nothing delivered.
Sets it apart: converts a total failure into a late delivery on the worst nights; changes one number.

## Rearrange the work

**Run the pricing aggregation concurrently with the catalog fetch** — The pricing step reads only Meridian's own database, so run it alongside the catalog fetch rather than after it.
Sets it apart: shortens the critical path with no change to any step's own cost; a modest, certain gain.

**Parallelize the fetch across more workers** — Split the catalog fetch into several concurrent workers each pulling a slice of the catalog.
Sets it apart: attacks the longest step directly with a standard scaling move; bets the fetch is limited by the job's own concurrency.

**Get a second Corvid API key and split the catalog between keys** — Obtain another API credential from Corvid and run two fetches, each under its own key.
Sets it apart: doubles whatever per-key ceiling the supplier imposes, if one exists; depends on the supplier saying yes.

## Change the machine

**Upgrade the worker to a larger instance** (user's) — "Move the job to a bigger machine so it finishes faster."
Sets it apart: the fastest thing to try; bets the job is limited by the worker's CPU, memory, or disk.

**Rewrite the export in a faster runtime** — Reimplement the job in a compiled language or a faster framework to reduce per-item processing time.
Sets it apart: the deepest change; pays off only if per-item processing, not waiting, is where the hours go.

## Make the catalog fetch cheaper

**Tune the catalog fetch's request parameters** — Change how the job asks the Corvid API for the catalog: page size, request timeouts, and retry settings, within what the API documents as allowed.
Sets it apart: a configuration change only; buys whatever headroom the API's own limits allow and no more.

**Fetch only items changed since the previous night** — Ask the Corvid API for items modified since the last run and merge them into a locally kept copy of the catalog, so most of the catalog is never re-fetched.
Sets it apart: removes most of the fetch on an ordinary night; the largest possible reduction in API work if the API supports it.

**Keep a local catalog cache and refresh it by diff** — Hold the previous night's catalog locally, re-validate items against the API, and rebuild only what changed.
Sets it apart: like the incremental option but driven from Meridian's side, so it does not depend on the API offering a changed-since filter.

**Poll the catalog hourly during the day and only assemble at night** — Spread the catalog fetch across the day in hourly slices so the night job only assembles already-fetched data.
Sets it apart: moves the long step out of the deadline window entirely; the night job becomes minutes.

**Ask Corvid for a bulk catalog file instead of the API** — Replace the paginated API fetch with a nightly bulk export from Corvid, pulled as one file.
Sets it apart: removes the API from the critical path altogether; the supplier does the heavy work.

## Change the platform

**Move the job to a managed workflow service** — Run the export on a hosted orchestration product with built-in retries, scheduling, and monitoring.
Sets it apart: replaces the team's own scheduler and retry logic with a product; bets the failures come from the harness rather than the work.

## Change what is delivered or when

**Reduce the export to the sections partners actually use** — Drop or slim the heaviest feed sections after checking with partners which ones they consume.
Sets it apart: shrinks the job by shrinking the deliverable; a conversation rather than an engineering change.

**Monitor and alert so an engineer can rerun before 06:00** — Add alerting on the job's progress so a person is woken in time to restart or repair a failing run.
Sets it apart: buys human intervention on bad nights without changing the job; cheap and fast to add.

**Negotiate a later delivery deadline with the partners** — Ask the four partners to accept delivery at 08:00 or later.
Sets it apart: removes the problem by moving the goalpost; costs a negotiation rather than engineering.
