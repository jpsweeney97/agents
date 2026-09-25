The design is now approved with the flag named `--after`. I'm treating the review session's approval as yours. I haven't started building, because this skill stops at the design.

**Handoff note**
- **Approach:** filter in the index query. `parse_after()` (renamed from `parse_since()`) in `cli/args.py` accepts ISO dates and `Nd`/`Nw`, anchored at local midnight. `store.index.query()` gains an `updated_after` filter compiled to `updated_at > ?`. Both `notes list` and `notes search` pass `--after` through. A future value is an error. Only the note's own `updated_at` counts.
- **Constraints:** ADR-0003 (every list filter must also work in `notes search`). Follow existing patterns. No unrelated refactoring.
- **Tests:** the parser's forms, the midnight boundary, and the search path.
- **How settled each decision is:**
  - **Yours:** relative forms as well as dates, and `updated_at` only.
  - **Accepted as offered:** filtering in the index query.
  - **Not confirmed by you:** `--after` came from the review session's redline, not from you. I haven't read the search grammar, so I haven't checked that `--after` doesn't collide with an existing flag.
  - **Not discussed by you:** the review approved the midnight anchor and the future-value error without comment, and you haven't spoken to either.

The rename opens one question. **With a date-only value, `--after 2026-09-20` as designed includes notes edited on the 20th itself.** Some people read "after the 20th" as excluding that day.

Need from you:
1. Next step:
   - (a) `implementation-planning`, where I write the step-by-step plan.
   - (b) `to-prd` or `to-issues`, to publish to the tracker.
   - (c) Stop here.
2. Reading of a date-only value:
   - (a) Include the 20th (my default, unchanged).
   - (b) Exclude the 20th, anchored at the start of the 21st.
