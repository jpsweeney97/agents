I picked A (SQLite FTS5, its built-in full-text search) and wrote the design below. **One premise is unverified: that the SQLite inside the shipped binaries has FTS5 on both the macOS and Linux runners.** Only a real run on both runners can settle that, so the design includes a build check for it.

**Design: `notes search <query>`**

- **Index.** A virtual table `notes_fts` with FTS5, "external-content": it indexes the notes table's body without storing a second copy. Three triggers (rules the database runs on insert, update, and delete) keep it in sync.
- **Existing notes.** When the db opens and `notes_fts` is missing, create it and run FTS5's `rebuild` once to index the notes already stored.
- **Query.** Each word is quoted, and all words must match. Punctuation can't cause FTS5 syntax errors. No operators (OR, NEAR, prefix `*`) in v1.
- **Ranking.** `ORDER BY bm25(notes_fts)`. bm25 is a standard relevance formula: more and rarer word matches rank higher. Best match first, 20 results by default, `--limit N` to change.
- **Output.** One line per note: id, date, title. No matches prints nothing and exits 0.
- **Errors.** Fail fast, no fallback search.
  - FTS5 missing: `search failed: SQLite FTS5 module unavailable. Got: sqlite3 <version>`.
  - Empty query: `search failed: query is empty. Got: ''`.
- **Testing.**
  - Unit tests: insert, update, and delete each change results. A note with more matches ranks above one with fewer. Queries containing `"`, `*`, or `-` don't error. Opening a db with existing notes indexes them.
  - Release workflow: after the PyInstaller build on each runner, run the built binary's `search` against a temp db. If FTS5 is missing, that step fails with the error above.
- **Deferred.** Attachment text (you said bodies only), query operators, result snippets.
- **Open for planning.** Confirm the notes table has an integer key that FTS5 can point at.

If a runner lacks FTS5, this design is wrong and we return to B or a bundled SQLite. I'm not reopening that now.

**Need from you:** pick one.
1. Approve as written. No pressure test has run, so the FTS5 premise gets its first test from the release check in the first build.
2. Run `prototype` first: a throwaway script that builds a binary on both runners and creates an FTS5 table. This settles the FTS5 question before planning.
3. Run one round of `grill-me` on the design, then approve.
4. Change something. The choices you're most likely to correct are plain-word queries with no operators, triggers plus a copy-free index, and the default of 20 results.

After approval the next lane is `implementation-planning`. Tell me if you want the design saved as a doc then.
