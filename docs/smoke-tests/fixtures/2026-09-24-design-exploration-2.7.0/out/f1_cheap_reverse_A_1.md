**No review round needed.** This is one optional flag and changes no stored data, so it is easy to undo. Below is the design in chat; it is not approved until you say so.

**Design: `--since` on `notes list` (approach A)**

- **Parsing:** `parse_since(value, now)` is a small function that returns an ISO-8601 cutoff string. It doesn't read the clock itself, because `now` is passed in.
  - `YYYY-MM-DD` gives local midnight of that date.
  - `Nd` or `Nw` (N is a whole number) gives local midnight of today minus N days, or minus N×7 days.
  - Anything else fails with `parse --since failed: expected YYYY-MM-DD, Nd, or Nw. Got: 'foo'`.
- **Index:** `store.index.query()` gets a new filter, `updated_since`, which adds `updated_at >= ?` with the cutoff as a bound value. It is inclusive, so `--since 2026-09-20` includes a note changed at exactly 00:00 that day. I renamed the key from `updated_after` so the name matches.
- **CLI:** `notes list --since` calls `parse_since` and passes the result to the query.
  - **Correction to my earlier "for free":** the query layer is shared, but ADR-0003 also needs the `--since` option declared on `notes search`, using the same parser. I haven't read the search command, so I don't know how it declares options.
- **Out of scope:** attachment changes, hour or minute units, `--until`.
- **Tests:**
  - Parser: a date, `1d`, `2w`, an invalid value, and a fixed `now`.
  - Query: notes before, at, and after the cutoff.
  - CLI: one test each for `list` and `search`.

**Decisions you might correct:**
1. Only `d` and `w` units. Hours would be confusing when the anchor is midnight.
2. The cutoff is inclusive (`>=`).
3. An invalid value exits with an error. It does not fall back to listing all notes.

**Unconfirmed:** I don't know whether stored `updated_at` strings are UTC or local, or whether they carry an offset. SQL compares them as text, so the cutoff must be written in the same form. I'd check this first when building.

**Need from you:**
1. Approve the design, or name which of the three decisions to change.
2. After approval, which next step do you want?
   - (a) `implementation-planning`, for a plan doc.
   - (b) Stop here, since nothing downstream is needed.
3. Do you want this saved as a file? If yes, give a path. I don't know of a design-doc location, and `docs/adr/` holds ADRs.
