User: /decide:design-exploration — I want a `--since` filter on the `notes list` command so I can see only notes changed after a date. Explore the approaches and settle a design.

Assistant: Grounding first. I read `cli/list.py`, `store/index.py`, and the two ADRs under `docs/adr/`. Facts that shape this: the list command already builds its result from `store.index.query()`, which accepts a dict of filters and passes them to a SQL WHERE clause; `updated_at` is stored as an ISO-8601 string in the index table; ADR-0003 says every list filter must also work in `notes search`. Two questions before I propose approaches. (1) Should `--since` accept relative forms like `3d` and `2w`, or only dates? (2) Does "changed" mean the note's own `updated_at`, or should a change to a linked attachment count?

User: 1: both, relative forms and dates. 2: the note's own updated_at only.

Assistant: Two approaches actually exist here. **A. Filter in the index query.** Parse `--since` in the CLI into an ISO timestamp, pass `{"updated_after": ts}` to `store.index.query()`, and add the one WHERE clause. `notes search` gets it for free because it goes through the same query function. **B. Post-filter in the CLI.** Query as today, then drop rows in Python. Simpler diff, but it breaks ADR-0003 for `search` unless duplicated there, and it loads every row to discard most. My lean is A. B wins only if you would rather not touch the index module at all this release. One trade you own: relative forms need a "now" anchor; I'd use local midnight of today so `--since 1d` means "since yesterday's start", which is friendlier than exact-24-hours but less precise.

User: A, and local midnight is fine. Seems small to me. Write up the design; do we even need a review round on something this size?
