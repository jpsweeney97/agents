I've updated the design to use `--after` instead of `--since`, but I haven't started building. The approval came from the review session, not from you, so I need your yes first. Also, `--after` was the reviewer's rename, not your original `--since`.

**Design now**
- `--after` on `notes list` and `notes search`. Values are ISO dates or `Nd`/`Nw` (`3d` means 3 days ago).
- The parser helper in `cli/args.py` is renamed `parse_after()`.
- `store.index.query()` gets an `updated_after` filter, compiled to `updated_at > ?`.
- Tests cover the parser's forms, the midnight boundary, and the search path.

**Not yet confirmed by you**
1. Dates anchor at local midnight.
2. A future date gives an error instead of an empty list.
3. New with the rename: `--after 2026-09-20` includes notes edited on the 20th, because the cutoff is midnight at the start of that day. "After" can read as excluding the 20th.

**Not yet checked:** I haven't confirmed that the search grammar uses `--after`. That is the reviewer's claim, and I can check it in the code.

**Not yet tested:** The review session approved with one rename. It did not stress-test the design. If you skip a pressure round, the premises (the midnight anchor, the search grammar match) first get tested in the plan or in the first real run.

Need from you:
1. Approve the design with `--after` and decisions 1–3, or tell me which to change.
2. Pick the next step:
   - (a) Run `grill-me` (an adversarial review) on the design first.
   - (b) Go straight to `implementation-planning`, which writes an executable plan.
   - (c) Stop here.
