Design approved with the rename applied: the flag is now `--after`, not `--since`. I'm counting the review session's verdict as your approval because you pasted it. Tell me if that's wrong.

I haven't built anything. This step ends at the design, and "Go" is the point where I hand off to the next step.

**Handoff notes**
- **Approach:** filter in the index query.
  - `--after` accepts ISO dates and `Nd`/`Nw` forms, anchored at local midnight.
  - The CLI helper becomes `parse_after()`. I renamed it to match the flag; the review session didn't ask for that.
  - `store.index.query()` gains `updated_after`, compiled to `updated_at > ?`.
  - `list` and `search` both pass it through.
  - Tests cover the parser forms, the midnight boundary, and the search path.
- **Binding constraints:**
  - ADR-0003 requires every list filter to work in `notes search`.
  - "Changed" means the note's own `updated_at` only.
  - Both date and relative forms are supported. You chose the last two.
- **How settled each decision is:**
  - The flag rename came from the review session.
  - Local midnight anchor and rejecting future dates with an error were accepted as offered. The review didn't mention them and you haven't confirmed them.
  - Not verified: I haven't checked that the `notes search` grammar really uses `--after`. The plan should check that first.
- **Deferred:** post-filtering in the CLI (approach B), only if you don't want to touch the index module this release.

**Need from you:** pick the next step.
1. `implementation-planning`, which writes a step-by-step plan doc. This is my recommendation.
2. `to-prd` or `to-issues`, which publish to your tracker.
3. Stop here.

Optional: confirm or correct the two unconfirmed decisions (local midnight anchor, rejecting future dates).
