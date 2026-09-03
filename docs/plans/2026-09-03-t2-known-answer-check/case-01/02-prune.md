# Prune: the nightly partner export

## Survivors (field order)

1. Start the job earlier
2. Parallelize the fetch across more workers
3. Upgrade the worker to a larger instance (user's)
4. Keep a local catalog cache and refresh it by diff
5. Poll the catalog hourly during the day and only assemble at night

Five survive against a count of about four. Each makes a different bet about where a bad night's hours go: the window the job gets, the job's own concurrency, the machine, how much of the catalog changes, and whether the fetch has to sit inside the night at all. All five are serious at sketch depth, so a survivor-count record saying otherwise would be false; choosing among them means seeing which bet is right, which is Develop's job. No cut was blocked by an unpriced value trade.

## Cut records (field order)

```text
Option:         Raise the job's timeout so it is never killed
Cut:            same reason, judgment call
Reason:         This and "Start the job earlier" make the same bet: a bad night's run is bounded within a few hours over the window it currently gets, so more wall-clock room is enough. Both fail together if bad-night duration is growing or unbounded, since a stalled fetch runs until whatever ceiling exists. "Start the job earlier" is kept because it is the one that can reach 06:00; lifting the ceiling on its own turns a killed run into a late one and never makes the deadline. If lifting the ceiling proves necessary, it is the second half of the earlier-start move, not a competing option.
Strongest case: On the four killed nights nothing was delivered at all. Lifting the five-hour ceiling is a one-number change that guarantees a complete file eventually, a late file may be worth far more to a partner than none, and it is the only option in the field that is safe to apply tonight.
Revive if:      Develop finds bad nights run past five hours but would finish before 06:00 from an earlier start (then lift the ceiling inside "Start the job earlier"), or the partners confirm that a late complete file materially beats no file, which makes this a standing backstop alongside any survivor.
```

```text
Option:         Run the pricing aggregation concurrently with the catalog fetch
Cut:            survivor count, judgment call
Reason:         A low-confidence cut to reach the count; its seriousness could not be resolved at sketch depth. The field describes it as a modest, certain gain whose ceiling is the pricing step's own duration, and the pricing step reads only Meridian's own database. Whether that step is a large enough share of a bad night's overrun to close a gap that killed the job at five hours on four of thirty nights is something the sketch cannot show.
Strongest case: It is the one change in the field with no bet in it: it shortens the critical path by the full length of the pricing step, costs a few hours of engineering, adds nothing to maintain, and combines with every survivor.
Revive if:      Timing evidence shows the pricing step is a large share of bad-night duration (roughly an hour or more), or a survivor is adopted and this is folded in as a companion change.
```

```text
Option:         Get a second Corvid API key and split the catalog between keys
Cut:            survivor count, judgment call
Reason:         A low-confidence cut to reach the count; its seriousness could not be resolved at sketch depth. It pays off only if Corvid caps throughput per key, and three unknowns stand in front of it: whether such a ceiling exists, whether Corvid would issue a second key inside six weeks, and whether Corvid's terms let one customer split its load across keys, since a per-key ceiling usually exists to cap exactly that. If the ceiling is not per-key, "Parallelize the fetch across more workers" is the same move with no supplier dependency. Issuing a credential is routine account use, not a supplier agreement, so this is not a constraint cut.
Strongest case: If the fetch is capped per key, this is the only option in the field that raises that cap without a supplier project: one credential request, two fetch processes, and the catalog split in half.
Revive if:      Develop shows the fetch is throttled per key by Corvid, and Corvid's documentation or account terms allow multiple keys per customer with the second key obtainable without a plan or contract change.
```

```text
Option:         Rewrite the export in a faster runtime
Cut:            constraint, fact-established
Reason:         Constraint 3 rules out a rewrite by name: one engineer at half time, about 120 hours, and "a rewrite, a platform migration, or anything needing a second engineer is out." Reimplementing the job in a compiled language or a faster framework is a rewrite. It also runs against the maintainability value: a runtime the team of three does not already work in needs a specialist.
Strongest case: If the hours go to per-item processing rather than waiting on the API, this is the only option that attacks that cost directly, and the gain would hold on every night regardless of the API's behavior.
Revive if:      The capacity constraint is lifted (a second engineer or a later deadline) and profiling shows per-item processing, not network waiting, is where bad-night hours go.
```

```text
Option:         Tune the catalog fetch's request parameters
Cut:            survivor count, judgment call
Reason:         A low-confidence cut to reach the count; its seriousness could not be resolved at sketch depth. The gain is bounded by how far the current page size, timeout, and retry settings sit from what the API allows, and the case gives no view of the current settings; the option's own description caps it at "whatever headroom the API's own limits allow and no more." Retry and timeout settings may also matter more for the killed nights than page size does, which is a different question the sketch cannot see.
Strongest case: It is a configuration change only, reversible in minutes, fully within the team's control, and if the job currently fetches in small pages with aggressive retries it could recover hours at no cost in spend or maintenance.
Revive if:      Develop finds the current request settings far below the API's documented limits, or finds that retry storms or hung requests, rather than raw volume, drive the killed nights.
```

```text
Option:         Fetch only items changed since the previous night
Cut:            same reason, judgment call
Reason:         This and "Keep a local catalog cache and refresh it by diff" make the same bet: most of the catalog does not change night to night, so hold a local copy and pull only the changes. Both fail together if the catalog churns heavily or a locally held copy is unacceptable for the partner feed. The cache-and-diff wording is kept because its success does not depend on the Corvid API offering a modified-since filter, which the case does not establish. If that filter exists, it becomes the refresh mechanism inside the kept option rather than a separate option.
Strongest case: If Corvid's API supports a modified-since query, this is the largest reduction in API work available: one small request per night instead of a full catalog fetch, with nothing to re-validate item by item.
Revive if:      Corvid's API documents a modified-since filter reachable with current credentials. Then adopt it as the refresh mechanism of the kept option, replacing per-item re-validation.
```

```text
Option:         Ask Corvid for a bulk catalog file instead of the API
Cut:            constraint, judgment call
Reason:         Constraint 1 rules out anything that needs a contract change with the supplier and requires the fix live within six weeks. This option asks Corvid to produce and serve a new nightly export, which is a supplier commitment on a timeline the team does not control; at the depth I can see, that is a supplier agreement, not use of an existing feature. The judgment call: the case does not say whether Corvid already offers a bulk catalog file. If it does and the current credentials reach it over Corvid's own endpoint, this is not a supplier change at all. A file delivered through a new transfer service would also touch constraint 2.
Strongest case: It removes the API from the critical path entirely. The supplier does the heavy work once, the team downloads one file, and the fetch stops being the long step on every night.
Revive if:      Corvid documents an existing bulk catalog export reachable with the current credentials over Corvid's own endpoint, with no new agreement or transfer service.
```

```text
Option:         Move the job to a managed workflow service
Cut:            constraint, fact-established
Reason:         Constraint 2 names hosted orchestration products as out: partner and supplier data would pass through a new third-party service, and a data-processing agreement takes at least eight weeks against a six-week deadline. Constraint 3 separately rules out a platform migration.
Strongest case: If the misses come from the harness (scheduling drift, failed retries, no visibility) rather than the work, a product with built-in retries and monitoring fixes the failure class rather than one instance of it.
Revive if:      A data-processing agreement with such a service is already signed, or the deadline moves out past the eight weeks a new one needs.
```

```text
Option:         Reduce the export to the sections partners actually use
Cut:            constraint, judgment call
Reason:         The partner feed is the contracted deliverable. Dropping or slimming its sections changes what Meridian delivers under that contract, which constraint 1 rules out as a contract change with a partner. The judgment call: the case states the contract's deadline but not whether it lists the feed's sections; if it does not, this is a conversation, not an amendment. A second point the sketch cannot resolve: the field identifies the catalog fetch as the long step, and slimming output sections shortens assembly, not the fetch, unless whole catalog segments become unnecessary.
Strongest case: It is the only option that makes the job smaller rather than faster, and it needs no engineering at all if partners confirm they ignore the heaviest sections.
Revive if:      The contract fixes only the deadline and format, partners confirm in writing which sections they do not consume, and the dropped sections remove catalog fetching rather than only output work.
```

```text
Option:         Monitor and alert so an engineer can rerun before 06:00
Cut:            dominated, judgment call
Reason:         "Start the job earlier" is at least as good on everything the user named and better on some. On delivery by 06:00: a rerun only helps if it fits before 06:00, which needs the room an earlier start gives every night automatically, and a rerun of a job that already ran five hours cannot finish in time. On maintainability: this adds alerting plus a night-time on-call expectation to a team of three; an earlier start adds nothing. On spend: equal or worse. What this covers that an earlier start does not is a failure a person can repair, such as a crash or bad input. The judgment: the case describes the misses as duration (slow nights and the five-hour kill), which a rerun cannot shorten.
Strongest case: It is cheap to add, it catches every failure kind rather than only slowness, and on a night when the job dies early a woken engineer can deliver something before 06:00.
Revive if:      Develop finds that some of the nine misses were early failures a restart would have fixed in time, rather than duration.
```

```text
Option:         Negotiate a later delivery deadline with the partners
Cut:            constraint, fact-established
Reason:         The 06:00 deadline is a term of the partners' contract, as the user stated. Moving it is a contract change with a partner, which constraint 1 rules out. Two partners have also complained in writing and the fix must be in place before the quarterly partner review, so the negotiation would run inside the window the constraint closes.
Strongest case: It is the only option that removes the problem rather than the delay. A two-hour later deadline would have absorbed most of the nine misses at zero engineering cost.
Revive if:      A partner offers the change unprompted, or the constraint is lifted after the quarterly review.
```
