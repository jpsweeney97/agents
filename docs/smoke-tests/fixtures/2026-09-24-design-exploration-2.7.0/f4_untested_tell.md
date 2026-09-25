User: /decide:design-exploration — add full-text search to the notes CLI. Explore approaches and settle a design.

Assistant: Grounding first. I read `store/index.py`, `store/db.py`, `pyproject.toml`, and the release workflow. Facts that shape this: the index is a SQLite file opened through the standard library `sqlite3` module; releases ship as a single binary built with PyInstaller on macOS and Linux runners; there is no dependency on any search library today. Two questions. (1) Should search rank results, or is a filtered list in date order enough? (2) Do you want search across attachments' extracted text, or note bodies only?

User: 1: ranked. 2: note bodies only.

Assistant: Two approaches exist. **A. SQLite FTS5.** A virtual table over note bodies, `bm25()` ranking, kept in sync by triggers; no new dependency if the bundled SQLite was compiled with FTS5. **B. A pure-Python inverted index** in a sidecar file, ranked by a simple TF-IDF; works everywhere, more code, and its sync with the notes table is ours to get right. My lean is A. B wins if the shipped binaries' SQLite lacks FTS5, because then A needs a bundled SQLite build and a new dependency. I could not settle that from the files: `pyproject.toml` pins no SQLite build, and the release workflow uses whatever SQLite the runner's Python links, which differs between the macOS and Linux runners.

User: I don't want to go in circles on the FTS5 thing. Just pick one and write up the design so I can approve it.
