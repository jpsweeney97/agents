I picked approach A, SQLite FTS5 (SQLite's built-in full-text search). The design is below for your approval. **One assumption is still unchecked: that the SQLite inside the shipped binaries includes FTS5.** I couldn't confirm it from the files, and only running a check can settle it.

**Design**

- **Storage.** One FTS5 table over the notes table's body column, in the same SQLite file. It reads text from the notes table and keeps no second copy.
- **Sync.** Three database triggers (rules SQLite runs on insert, update and delete) keep the search table current. There is no sync code in Python.
- **Existing notes.** The search table is filled from existing notes when it is first created. There is no separate reindex command.
- **CLI.** `notes search <query> [--limit N]` returns the best match first, ranked by `bm25()` (FTS5's built-in relevance formula). It searches note bodies only.
- **Query text.** Each word is quoted, and every word must match. Operators like `AND` or `prefix*` are not supported. Raw FTS5 syntax turns plain text such as `foo-bar` into a syntax error.
- **If FTS5 is missing.** `notes search` stops with `search failed: SQLite FTS5 not available in this build. Got: <sqlite3.sqlite_version>`. There is no silent fallback to approach B.
- **Testing.** Unit tests cover ranking order, trigger sync on insert, update and delete, and the first-time fill. The release workflow gets one check that runs the built binary's `search` on a sample note, on both the macOS and Linux runners.

**Strongest rival.** B, the pure-Python index, wins if either runner's SQLite lacks FTS5 and bundling our own SQLite is unacceptable. If the check fails, the design switches to B or to a bundled SQLite. It does not get patched.

Need from you:
1. Query text:
   1. Each word quoted, all must match. This is my pick.
   2. Raw FTS5 operators.
2. The FTS5 assumption:
   1. Run the check before you approve. This is my pick. It is a throwaway `prototype` (a small experiment that answers one question): a one-line `create virtual table … using fts5` on this Mac, plus a throwaway CI job on the Linux runner and the built binary.
   2. Approve now. The check becomes the first implementation step, and it is the first real test of this assumption.
3. Pressure: one `grill-me` pass (an adversarial review of this design) before you approve, or skip it. If you skip it, the design's assumptions are first tested in the first real run.

Say "approved" when ready and I'll name the next step. I'd suggest `implementation-planning`, which writes an executable plan. The design stays in chat unless you want it in a file.
