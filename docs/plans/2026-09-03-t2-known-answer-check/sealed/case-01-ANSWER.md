# SEALED ANSWER NOTE — case-01 (never given to a reader agent)

Written 2026-09-03 15:18 by the session, before any reader was dispatched.

## Kind of case

Kind B, as the Recommend stage defined it: the facts that fix the winner sit only in `evidence.md`, which 2.0's Prune never receives. Prune's view is `case.md` alone (question, background, user's candidate marked, constraints at their price, values, survivor count, the field). Shape's view is `case.md` plus `evidence.md`.

Why Kind B: it is the T2 question in its conditional form ("given a candidate whose case lives only in evidence, how often is it cut"), and it matches how 2.0 dispatches Prune. Kind A (fixing facts in constraints or values Prune sees) would measure whether Prune reads carefully, a different question; and its Agent A test is incoherent, because an agent asked directly for the best option will find facts that are in front of it.

## The winner

**Tune the catalog fetch's request parameters** (field position 7 of 16, group "Make the catalog fetch cheaper").

## The facts that fix it, and where each sits

1. E4: the job requests the catalog at `page_size: 50`, the client library default, never changed.
2. E2: the API allows `page_size` up to 1000.
3. E5: last night's fetch was 2,093,412 items in 41,869 requests, 4h07m. At page size 1000 that is about 2,094 requests, a twentyfold reduction; at the observed effective rate (about 170 requests per minute under the 300-per-minute limit at concurrency 4) the fetch drops from about four hours to under half an hour even if larger pages are several times slower each.
4. E1 and E6: the fetch is the entire problem (steps 2 to 4 total about 40 minutes) and the worker is idle (CPU 6%), so the time is spent waiting on requests, which is exactly what fewer requests removes.
5. Constraints: a one-line configuration change plus testing fits inside 120 hours, needs no procurement, no new vendor, and no spend.

Expected job after the change: roughly 30 min fetch + 24 + 9 + 5 min, finishing before 03:00 on a bad night, against a 06:00 deadline.

## Why every other candidate loses on the evidence (Shape's view)

- Start earlier: E2 and E7. The catalog is final at 01:00 and the feed must reflect it; the job already starts at 01:15.
- Raise the timeout: the deadline is 06:00 (E7); a run that is allowed to finish at 06:40 is still late. Removes the kill, not the miss.
- Run pricing concurrently: E1. Saves at most about 24 minutes against a fetch that runs over four hours; a real but insufficient gain. (A sensible complement, not the answer.)
- Parallelize the fetch: E9 and E2. The 300-per-minute limit is per key; more workers only produce more 429s. Tried.
- Second API key: E3. Not offered on this tier; and constraint 1 forbids a contract change.
- Bigger instance (user's): E6. CPU 6%, memory 31%, network 3 Mbps. The worker is waiting, not working.
- Rewrite: E6 and constraint 3. Processing is not where the time goes; a rewrite is out of capacity anyway.
- Incremental fetch: E2 and E8. No changed-since filter, no ETags, identifiers regenerate nightly; the March attempt saved nothing.
- Local cache by diff: E2. Identifiers regenerate nightly, so nothing can be re-validated item by item; a cache is a full fetch under another name.
- Poll hourly by day: E2 and E7. Daytime requests return the previous day's catalog; the feed must reflect the 01:00 finalization. (Also, at the current page size, hourly polling would be about a million requests a day against a 250,000 quota.)
- Bulk file from Corvid: E3. Enterprise tier only, ten to twelve weeks and about $48k a year; constraint 1 and the spend value both fail.
- Managed workflow service: constraint 2 (eight-week DPA); and E8 shows the failures are duration, not harness errors, so the product would not shorten the fetch.
- Reduce the sections: E7 requires all six; and the fetch pulls the whole catalog regardless of which sections are built.
- Monitor and rerun: E9. A rerun takes over four hours; one started at 06:00 finishes after 10:00.
- Negotiate the deadline: E7. Declined in April and written into the July renewal; constraint 1 forbids a contract change anyway.

## What is visible in Prune's view, so it is not part of the fixing facts

Constraints 1 and 2 visibly disqualify the second key, the bulk file, the managed service, and the negotiation. The values visibly weigh against the rewrite and the bigger instance. None of this points at the winner; from Prune's view the winner reads as the modest member of the fetch group, sitting beside four candidates that promise to remove most of the fetch.

## Pass criteria for the check (from the Recommend stage's step 2)

- Reader A (Prune's view, `case.md` only): must NOT name the winner as best. If it does, the winner is visible at sketch depth; rewrite. Note separately whether A lists it among runners-up.
- Reader B (Shape's view, `case.md` + `evidence.md`): must name the winner as best. If it does not, the evidence does not fix the winner; rewrite.

## Attempt counter

Attempt 1 of at most 3.
