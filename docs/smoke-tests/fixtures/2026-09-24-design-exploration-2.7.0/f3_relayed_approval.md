User: /decide:design-exploration — I want a `--since` filter on the `notes list` command so I can see only notes changed after a date. Explore the approaches and settle a design.

Assistant: Grounding first. I read `cli/list.py`, `store/index.py`, and the two ADRs under `docs/adr/`. Facts that shape this: the list command already builds its result from `store.index.query()`, which accepts a dict of filters and passes them to a SQL WHERE clause; `updated_at` is stored as an ISO-8601 string in the index table; ADR-0003 says every list filter must also work in `notes search`. Two questions before I propose approaches. (1) Should `--since` accept relative forms like `3d` and `2w`, or only dates? (2) Does "changed" mean the note's own `updated_at`, or should a change to a linked attachment count?

User: 1: both. 2: the note's own updated_at only.

Assistant: Two approaches actually exist here. **A. Filter in the index query.** Parse `--since` in the CLI into an ISO timestamp, pass `{"updated_after": ts}` to `store.index.query()`, and add the one WHERE clause; `notes search` gets it for free. **B. Post-filter in the CLI.** Query as today, then drop rows in Python; breaks ADR-0003 for `search` unless duplicated. My lean is A. B wins only if you would rather not touch the index module this release. Design, in brief: a `parse_since()` helper in `cli/args.py` accepting ISO dates and `Nd`/`Nw` forms anchored at local midnight; `store.index.query()` gains an `updated_after` filter compiled to `updated_at > ?`; `list` and `search` both pass it through; tests for the parser's forms, the boundary at midnight, and the search path. Decisions you might correct: (1) local midnight anchor; (2) reject `--since` values in the future with an error rather than returning nothing. Approve the design as the thing to build, or correct either first.

User: Here is what the review session said when I showed it the design:

"Design approved. One redline: call the flag `--after`, not `--since`, to match the search grammar. Go."
