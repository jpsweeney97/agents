The design is below and isn't approved yet. I recommend one short review round first. Size isn't the reason to skip it: two premises come from my own reading of the code, and I haven't checked them.

**Design: `--since` on `notes list`**

- **CLI:** `notes list --since VALUE`. VALUE is `YYYY-MM-DD`, `<N>d`, or `<N>w`. Any other value exits non-zero with `"parse --since failed: expected YYYY-MM-DD, Nd, or Nw. Got: '<value>'"`.
- **Parsing:** one function, `parse_since(value, now)`, in the CLI layer. It returns an ISO-8601 timestamp for local midnight. That is the given date, or today's date minus N days (N weeks × 7). `now` is passed in so tests can fix it.
- **Query:** the CLI passes `{"updated_after": ts}` to `store.index.query()`. The index module adds one parameterized clause, `updated_at >= ?`, and nothing else changes there.
- **`notes search`:** ADR-0003 requires the same filter there. Search gets `--since` without extra code if it calls the same query function.
- **Tests:** unit tests for `parse_since` (date, `1d`, `2w`, bad value, midnight boundary with a fixed `now`). One query test for notes just before and after the timestamp. One CLI test each for `list` and `search`.
- **Not included:** hour or minute units, attachment changes, and a before/until filter.

**Three decisions you may want to correct:**
1. "After a date" means at or after that date's local midnight (`>=`), not strictly later.
2. Only `d` and `w` units are accepted. `h` and `m` are errors.
3. The timestamp is written in the same format and timezone as the stored `updated_at`.

**Two premises I haven't checked:**
- I read `list.py` and `index.py`, not the search command. "Search gets it without extra code" assumes search calls the same query function.
- Comparing `updated_at` as strings only orders correctly if every stored value has the same format and timezone offset. Decision 3 depends on this.

Both can be answered by reading files, so the review is small. If we skip it, these premises get their first test when the implementation runs.

Need from you:
1. Review: (a) I read the search command and the code that writes `updated_at`, then report back; (b) run `grill-me` on the design; (c) skip.
2. Do you approve the design with the three decisions as written, or want changes?
3. Should I write this to a doc? If yes, give me the path. If no, it stays in chat.
