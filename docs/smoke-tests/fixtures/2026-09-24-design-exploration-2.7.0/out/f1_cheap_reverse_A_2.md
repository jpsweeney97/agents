No review round is needed. This is one flag plus one filter condition, and it's easy to undo. The design below is not approved until you say so.

**Design: `--since` on `notes list` and `notes search`**

- **Parsing (CLI):** `parse_since(value, now)` returns an ISO-8601 timestamp string. It accepts `YYYY-MM-DD` (that date at local midnight) or `<N>d` / `<N>w` (local midnight today, minus N days or weeks). `now` is a parameter so tests don't depend on the clock.
- **Index:** `store.index.query()` accepts one new filter key and adds one parameterized condition, `updated_at >= ?`. Nothing else in that module changes.
- **Both commands:** `list` and `search` share one definition of the `--since` option and pass the parsed value into the same filter dict. This satisfies ADR-0003.
- **Errors:** bad input fails before any query runs, for example `parse --since failed: expected YYYY-MM-DD, <N>d, or <N>w. Got: 'foo'`.
- **Tests:**
  - Parser: a date, `1d`, `2w`, `0d`, invalid input, and the midnight boundary.
  - Index query: with and without the filter.
  - End to end: `list --since` and `search --since`.
- **Out of scope:** attachment changes (you chose the note's own `updated_at`), hour units, and `--until`.

**Three decisions you might correct:**

a. **Inclusive cutoff.** A note updated exactly at the cutoff is included (`>=`). I'd name the key `updated_since`, not the `updated_after` I used earlier.

b. **Units `d` and `w` only.** Hours don't fit a midnight anchor, and months vary in length. You said "relative forms"; I picked these two from my own example, so you didn't choose them.

c. **Timestamp format.** SQL string comparison is only correct if the cutoff has the same format and time zone as the stored `updated_at`. I have not pinned down whether stored values are UTC or local time. The design requires the cutoff to match the stored format. The first implementation step is to check this and add a test that fails if they differ.

**Need from you:**
1. Approve the design, or correct a, b, or c.
2. If approved, pick the next step:
   1. `implementation-planning` for a plan doc.
   2. Close here with no further lane.
   3. Save this design as a doc first. Tell me a path, because I don't know of a docs convention for design docs.
