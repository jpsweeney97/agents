I picked **A, SQLite FTS5** (SQLite's built-in full-text search module). The design is below. One assumption is still unconfirmed, so the design has the build check it instead of asking you again.

**Storage.** One FTS5 table, `notes_fts`, indexes note bodies only. It reads its text from the notes table, so bodies are not stored twice. Three triggers (database rules that run on insert, update and delete) keep it in sync. On first open after upgrade, a one-time rebuild indexes existing notes, using however `store/db.py` handles schema changes.

**Query.** `notes search <words> [--limit N]` orders results by `bm25()`, SQLite's relevance score, where lower means a better match. The default limit is 20. Each result shows note id, date, and a short snippet around the match.

**Input handling.** Raw FTS5 query syntax raises errors on characters like `"` and `-`. In v1, input is treated as plain words: each word is quoted and all words must match. There are no operators and no phrase search.

**Errors.** If FTS5 is missing, index setup fails with `"create full-text index failed: SQLite has no FTS5. Got: <sqlite3.sqlite_version>"`. There is no silent switch to approach B. An empty query is an error. No matches prints "No matches" and exits 0.

**Testing.**
- Unit tests: insert, update and delete keep the index in sync.
- Unit tests: a note with more matches ranks first.
- Unit tests: quotes and dashes in a query don't raise.
- Unit tests: the one-time rebuild indexes existing notes.
- One release-workflow check on both the macOS and Linux runners. It runs the built binary, tries to create an FTS5 table, and fails the build if that doesn't work.

**Unconfirmed: the shipped binaries' SQLite has FTS5.** I couldn't settle this from the files, and only a real run can. The release-workflow check answers it. If it fails, the design changes to B, and I'll bring that back to you rather than switch silently. B wins only in that case.

Need from you:
1. Approve the design, or name what to change. The three decisions most worth a look are plain-words-only input, the default limit of 20, and the snippet in the output.
2. For the FTS5 check, pick one:
   - (a) Leave it to the release-workflow check in the plan (my recommendation).
   - (b) I run a throwaway check first, before planning.
3. Do you want this saved as a design doc? If yes, give me a path.

Once you approve, I'd suggest `implementation-planning` as the next step.
