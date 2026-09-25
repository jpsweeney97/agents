I picked A (SQLite FTS5) and wrote the design below. It is not approved until you say so.

**Not settled:** I could not confirm that the shipped binaries' SQLite includes FTS5. I did not try to settle it. The design turns it into a release test. If that test fails, A needs a bundled SQLite (a new dependency) or we switch to B, and I would bring that back to you.

**Design**
- **Storage:** an FTS5 table `notes_fts` that indexes note bodies. It points at the `notes` table instead of copying bodies. Three triggers (insert, update, delete) keep it in sync.
- **When it is created:** the first time `search` runs, not at startup. That step also indexes existing notes. A SQLite without FTS5 then breaks only `search`, and users who never search see no schema change.
- **Query:** `search(query, limit=20)` in `store/index.py`, ordered by `bm25()` (FTS5's built-in relevance score). Each word is quoted before it reaches FTS5, so `foo-bar` or a stray `"` does not raise a syntax error. There are no user-facing operators (AND, OR, NEAR) in this version.
- **CLI:** `notes search <query> [--limit N]`. It prints results in rank order with note id, date, and a snippet around the match.
- **Errors:** if FTS5 is missing, `search` raises `"full-text search failed: SQLite lacks FTS5. Got: {sqlite3.sqlite_version!r}"`. There is no fallback to a slower substring scan.
- **Release check:** after the PyInstaller build on each runner, run the built binary on a temporary index. Add one note, search for a word in it, and expect one hit. A failure blocks the release.
- **Tests:** the index stays in sync on insert, update, and delete. A note with more matches ranks first. Punctuation in a query does not raise. The missing-FTS5 error message is correct.
- **Out of scope:** attachment text, search operators, match highlighting.

After approval, the next lane is `implementation-planning`.

Need from you:
1. Approve this design as written, or name what to change.
2. Two choices you may want to flip (default is as written):
   - (a) Quote every word, versus pass raw FTS5 syntax through.
   - (b) Create the index on first `search`, versus at startup.
