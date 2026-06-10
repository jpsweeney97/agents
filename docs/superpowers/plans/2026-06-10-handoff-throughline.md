# Handoff Throughline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the `throughline` skill in `plugins/handoff/` per the approved spec — one derived `THROUGHLINE.md` per project condensing the handoff pile — plus the spec'd edits to the three sibling skills, README, and plugin manifest.

**Architecture:** Prose behavior contracts, not code. A new skill directory (`SKILL.md` + `agents/openai.yaml`), a new format reference, three small sibling-skill edits, README/manifest updates, version bump to 3.1.0. The only machinery is the frontmatter coverage pair (`covers_through` + `sources_folded`).

**Tech Stack:** Markdown skill contracts, YAML frontmatter, JSON manifest. Validation per the repo Validation Ladder: structural parses plus fixture-pile forward tests run by context-isolated subagents.

---

## Ground Rules (read before Task 1)

- **Spec is authority:** `docs/superpowers/specs/2026-06-10-handoff-throughline-design.md`. It survived four review-adjudication rounds. Do not relitigate settled decisions (see its Agent-Facing-Design Audit section and the round-4 commit message `ff5a5c4`). In particular, do NOT add: source-set digests/hashes, normalized source keys, search exclusion or output splitting, /load hard size or staleness guards, validators, thresholds, statuses, or scoring.
- **Branch:** all work on `feature/handoff-throughline`. A user-level hook blocks Edit/Write on `main` in this repo. Before Task 1, run `git status --short --branch` and confirm the branch and a clean tree.
- **TDD adaptation:** these are prose contracts; there is no meaningful "red" test run before the contract file exists. Per the repo Validation Ladder (which governs here), each task is: write the surface → structural validation → fixture forward test (where the spec demands one) → commit. Forward tests are context-isolated subagent proxies (Agent tool, `general-purpose`), which is this repo's standard behavior-proof for skill contracts.
- **One derived clarification** (consequence of spec arithmetic, not a new decision — flag it in the commit message for Task 3): a bounded-batch partial fold must take the **oldest unfolded sources first**. The drift check compares "count of files at or below `covers_through`" to `sources_folded`; a non-prefix batch (e.g. newest-first) makes that comparison false immediately. The SKILL.md text states this in one sentence.
- **Do not publish:** no `scripts/codex-plugins-sync.sh --publish`, no GitHub mirror update, no push. Claude Code delivery is automatic via the existing plugin-dir symlink.
- **Deletion:** `trash <path>` only, never `rm`.
- **Commits:** end every commit message with the trailer line `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` (shown in each commit step).
- **Subagent prompts:** forward-test subagents must Read the SKILL.md file and follow it as a contract. They must NOT use the Skill tool (the new skill is not registered in the running session) and must NOT read the other handoff skills unless the test says so.

## File Structure

| Path | Action | Responsibility |
| --- | --- | --- |
| `plugins/handoff/skills/throughline/SKILL.md` | Create | The throughline behavior contract (source set, refresh, coverage honesty, boundaries, reply shape) |
| `plugins/handoff/skills/throughline/agents/openai.yaml` | Create | Companion metadata, matching siblings' minimal shape |
| `plugins/handoff/references/throughline-format.md` | Create | Frontmatter + section prompts (symmetry with `handoff-format.md`) |
| `plugins/handoff/skills/load-handoff/SKILL.md` | Modify | 3 edits: implicit-selection exclusion; explicit-load redirect; `Throughline:` response line + corroboration rule |
| `plugins/handoff/skills/save-handoff/SKILL.md` | Modify | 2 edits: arc-delta capture guidance; optional one-line `/throughline` nudge in the reply contract |
| `plugins/handoff/skills/search-handoffs/SKILL.md` | Modify | 1 edit: THROUGHLINE.md matches are derived pointers |
| `plugins/handoff/README.md` | Modify | Skills-table row; boundary-line revisions |
| `plugins/handoff/.claude-plugin/plugin.json` | Modify | 3.0.0 → 3.1.0; interface descriptions; defaultPrompt entry |
| `/tmp/throughline-fixtures/` | Create (throwaway) | Fixture piles for forward tests; trashed in Task 9 |

---

### Task 1: Fixture piles

**Files:**
- Create: `/tmp/throughline-fixtures/` (eight fixture piles; throwaway, never committed)

- [ ] **Step 1: Preflight**

Run: `git -C /Users/jp/.agents status --short --branch`
Expected: `## feature/handoff-throughline` and no dirty files. If on `main`, stop — do not edit on main.

- [ ] **Step 2: Create the fixture piles**

Run this entire script with the Bash tool (one call):

```bash
set -euo pipefail
F=/tmp/throughline-fixtures
if [ -e "$F" ]; then trash "$F"; fi
mkdir -p "$F/proj-first/.agents/handoffs/archive" \
         "$F/proj-first/.agents/handoffs/deep" \
         "$F/proj-first/.claude/handoffs"

# ---- proj-first: 9 sources; exclusions; mixed precision; collision pair; side branch; echo ----

cat > "$F/proj-first/.agents/handoffs/2026-01-05_10-00_init-minute-precision.md" <<'EOF'
---
created_at: "2026-01-05T10:00:00Z"
type: handoff
title: "Project init"
project: fixture-project
branch: main
---

# Handoff: Project init

## Session Context

Started the fixture project: a small CLI that converts notes to Markdown.

## Next Action

Decide on storage format.
EOF

cat > "$F/proj-first/.agents/handoffs/2026-01-05_10-00-30_init-followup.md" <<'EOF'
---
created_at: "2026-01-05T10:00:30Z"
type: handoff
title: "Init follow-up"
project: fixture-project
branch: main
---

# Handoff: Init follow-up

## Session Context

Saved thirty seconds after the init handoff: added the repo scaffold notes.

## Next Action

Decide on storage format.
EOF

cat > "$F/proj-first/.agents/handoffs/2026-03-10_09-15-00_settle-storage-format.md" <<'EOF'
---
created_at: "2026-03-10T09:15:00Z"
type: handoff
title: "Storage format settled"
project: fixture-project
branch: main
---

# Handoff: Storage format settled

## Session Context

Compared SQLite and plain Markdown for note storage. An SQLite index was
prototyped and dropped: too much machinery for the gain.

## Decisions

- Storage format settled: plain Markdown files on disk. Project-level decision.

## Next Action

Build the converter core.
EOF

cat > "$F/proj-first/.agents/handoffs/2026-06-01_12-00-00_side-branch-experiment.md" <<'EOF'
---
created_at: "2026-06-01T12:00:00Z"
type: handoff
title: "Cache experiment on side branch"
project: fixture-project
branch: feature/exp-cache
---

# Handoff: Cache experiment on side branch

## Session Context

Prototyped a content-hash cache for converted notes on this branch only.

## Decisions

- Adopted a cache layer keyed by content hash for this branch's prototype.

## Next Action

Benchmark before proposing for main.
EOF

cat > "$F/proj-first/.agents/handoffs/2026-06-02_08-30-00_wrap-up.md" <<'EOF'
---
created_at: "2026-06-02T08:30:00Z"
type: handoff
title: "Docs session wrap-up"
project: fixture-project
branch: main
---

# Handoff: Docs session wrap-up

## Session Context

Wrote the README quickstart. No code changes this session.

## Project Arc

Storage format is Markdown; caching is settled project-wide.

## Next Action

Write user docs for the converter flags.
EOF

cat > "$F/proj-first/.agents/handoffs/2026-06-02_08-30-00_wrap-up-2.md" <<'EOF'
---
created_at: "2026-06-02T08:30:00Z"
type: handoff
title: "Docs session wrap-up (second save)"
project: fixture-project
branch: main
---

# Handoff: Docs session wrap-up (second save)

## Session Context

Second save in the same second: added the GLOSSARY stub to the README.

## Next Action

Write user docs for the converter flags.
EOF

cat > "$F/proj-first/.agents/handoffs/archive/2025-11-20_14-00-00_prototype-era.md" <<'EOF'
---
created_at: "2025-11-20T14:00:00Z"
type: handoff
title: "Prototype era"
project: fixture-project
branch: main
---

# Handoff: Prototype era

## Session Context

ALPHA-PROTOTYPE era: built the first CLI prototype as a single script.

## Next Action

Restructure into a package.
EOF

cat > "$F/proj-first/.agents/handoffs/archive/2025-12-01_09-00_drop-yaml-config.md" <<'EOF'
---
created_at: "2025-12-01T09:00:00Z"
type: handoff
title: "Dropped YAML config"
project: fixture-project
branch: main
---

# Handoff: Dropped YAML config

## Session Context

Tried a standalone YAML config file and dropped it; frontmatter covers the need.

## Decisions

- Configuration lives in note frontmatter, not a separate YAML file.
EOF

cat > "$F/proj-first/.agents/handoffs/deep/2026-05-05_05-05-05_should-not-ingest.md" <<'EOF'
---
created_at: "2026-05-05T05:05:05Z"
type: handoff
title: "Should not be ingested"
project: fixture-project
---

# Handoff: Should not be ingested

## Session Context

ZEBRA-DEEP: this file lives in a non-archive subdirectory and must never be
folded into the throughline.
EOF

cat > "$F/proj-first/.agents/handoffs/notes.txt" <<'EOF'
ZEBRA-NOTES: not a handoff, not Markdown, must never be folded.
EOF

cat > "$F/proj-first/.claude/handoffs/2026-02-14_11-30_legacy-claude-handoff.md" <<'EOF'
---
created_at: "2026-02-14T11:30:00Z"
type: handoff
title: "CI migrated"
project: fixture-project
branch: main
---

# Handoff: CI migrated

## Session Context

Migrated CI from Jenkins to GitHub Actions.

## Decisions

- CI runs on GitHub Actions.
EOF

# ---- proj-refresh: 5 sources; valid coverage pair (3 folded); 2 newer ----

mkdir -p "$F/proj-refresh/.agents/handoffs/archive"
cp "$F/proj-first/.agents/handoffs/2026-03-10_09-15-00_settle-storage-format.md" \
   "$F/proj-first/.agents/handoffs/2026-06-01_12-00-00_side-branch-experiment.md" \
   "$F/proj-first/.agents/handoffs/2026-06-02_08-30-00_wrap-up.md" \
   "$F/proj-refresh/.agents/handoffs/"
cp "$F/proj-first/.agents/handoffs/archive/"*.md "$F/proj-refresh/.agents/handoffs/archive/"

cat > "$F/proj-refresh/.agents/handoffs/THROUGHLINE.md" <<'EOF'
---
type: throughline
updated_at: "2026-03-15T10:00:00Z"
project: fixture-project
covers_through: "2026-03-10_09-15-00_settle-storage-format.md"
sources_folded: 3
---

# Throughline: fixture-project

## Project Narrative

ALPHA-PROTOTYPE era produced a single-script CLI; it was restructured into a
package, and storage debates followed.

## Decisions That Hold

- Storage format: plain Markdown files on disk (settled 2026-03-10).
- Configuration lives in note frontmatter, not a separate YAML file.

## Abandoned Paths

- Standalone YAML config: dropped; frontmatter covers the need.
- SQLite index: prototyped and dropped; too much machinery.

## Frontier (as of 2026-03-15)

- Open: whether a cache layer is worth it at all. Defer to the newest handoff
  and live state for current truth.
EOF

# ---- proj-drift: proj-refresh + one late-arriving older file below the marker ----

mkdir -p "$F/proj-drift" "$F/proj-drift/.codex/handoffs"
cp -R "$F/proj-refresh/.agents" "$F/proj-drift/"
cat > "$F/proj-drift/.codex/handoffs/2026-01-15_08-00-00_late-arrival.md" <<'EOF'
---
created_at: "2026-01-15T08:00:00Z"
type: handoff
title: "Late-arriving legacy handoff"
project: fixture-project
branch: main
---

# Handoff: Late-arriving legacy handoff

## Session Context

DELTA-LATE: copied from another machine; records an early spike on watch mode.

## Decisions

- Watch mode deferred until after v1.
EOF

# ---- proj-malformed: proj-refresh with sources_folded stripped from frontmatter ----

mkdir -p "$F/proj-malformed"
cp -R "$F/proj-refresh/.agents" "$F/proj-malformed/"
python3 - <<'EOF'
p = "/tmp/throughline-fixtures/proj-malformed/.agents/handoffs/THROUGHLINE.md"
text = open(p).read()
lines = [l for l in text.splitlines(True) if not l.startswith("sources_folded:")]
open(p, "w").write("".join(lines))
EOF

# ---- proj-partial: full copy of proj-first (9 sources) ----

mkdir -p "$F/proj-partial"
cp -R "$F/proj-first/.agents" "$F/proj-partial/"
cp -R "$F/proj-first/.claude" "$F/proj-partial/"

# ---- proj-load: stale throughline with a planted next-action trap ----

mkdir -p "$F/proj-load/.agents/handoffs"
cp "$F/proj-first/.agents/handoffs/2026-03-10_09-15-00_settle-storage-format.md" \
   "$F/proj-load/.agents/handoffs/"
cat > "$F/proj-load/.agents/handoffs/2026-06-05_10-00-00_newest-session.md" <<'EOF'
---
created_at: "2026-06-05T10:00:00Z"
type: handoff
title: "Delta parser groundwork"
project: fixture-project
branch: main
---

# Handoff: Delta parser groundwork

## Session Context

Sketched the delta parser interface; no tests yet.

## Current State

Parser stub written (fixture claim; this directory is not a git repository).

## Next Action

Write tests for the delta parser.
EOF
cat > "$F/proj-load/.agents/handoffs/THROUGHLINE.md" <<'EOF'
---
type: throughline
updated_at: "2026-03-15T10:00:00Z"
project: fixture-project
covers_through: "2026-03-10_09-15-00_settle-storage-format.md"
sources_folded: 1
---

# Throughline: fixture-project

## Project Narrative

Early CLI work settled on Markdown storage.

## Decisions That Hold

- Storage format: plain Markdown files on disk (settled 2026-03-10).

## Abandoned Paths

- SQLite index: prototyped and dropped.

## Frontier (as of 2026-03-15)

- Next action: ship the GAMMA feature.
EOF
touch "$F/proj-load/.agents/handoffs/THROUGHLINE.md"

# ---- proj-save-missing / proj-save-current ----

mkdir -p "$F/proj-save-missing/.agents/handoffs" "$F/proj-save-current/.agents/handoffs"
for f in 2026-03-10_09-15-00_settle-storage-format.md \
         2026-06-01_12-00-00_side-branch-experiment.md \
         2026-06-02_08-30-00_wrap-up.md; do
  cp "$F/proj-first/.agents/handoffs/$f" "$F/proj-save-missing/.agents/handoffs/"
  cp "$F/proj-first/.agents/handoffs/$f" "$F/proj-save-current/.agents/handoffs/"
done
cat > "$F/proj-save-current/.agents/handoffs/THROUGHLINE.md" <<'EOF'
---
type: throughline
updated_at: "2026-06-02T09:00:00Z"
project: fixture-project
covers_through: "2026-06-02_08-30-00_wrap-up.md"
sources_folded: 3
---

# Throughline: fixture-project

## Project Narrative

Early CLI work settled on Markdown storage; a cache experiment ran on a side
branch; the latest session was docs-only.

## Decisions That Hold

- Storage format: plain Markdown files on disk (settled 2026-03-10).

## Abandoned Paths

- SQLite index: prototyped and dropped.

## Frontier (as of 2026-06-02)

- Cache layer: branch-scoped experiment on feature/exp-cache, not adopted
  project-wide.
EOF

echo "FIXTURES OK"
find "$F" -type f | wc -l
```

Expected: `FIXTURES OK` and a file count of `51`.

- [ ] **Step 3: Sanity-check the load-bearing counts**

Run:

```bash
F=/tmp/throughline-fixtures
echo "proj-first sources (expect 9):"
ls "$F/proj-first/.agents/handoffs/"*.md "$F/proj-first/.agents/handoffs/archive/"*.md "$F/proj-first/.claude/handoffs/"*.md | grep -cv THROUGHLINE
echo "proj-refresh sources (expect 5):"
ls "$F/proj-refresh/.agents/handoffs/"*.md "$F/proj-refresh/.agents/handoffs/archive/"*.md | grep -cv THROUGHLINE
echo "proj-drift sources (expect 6):"
ls "$F/proj-drift/.agents/handoffs/"*.md "$F/proj-drift/.agents/handoffs/archive/"*.md "$F/proj-drift/.codex/handoffs/"*.md | grep -cv THROUGHLINE
```

Expected: 9, 5, 6. No commit (fixtures live in `/tmp`, never in the repo).

---

### Task 2: `references/throughline-format.md`

**Files:**
- Create: `plugins/handoff/references/throughline-format.md`

- [ ] **Step 1: Write the file**

Write exactly this content to `/Users/jp/.agents/plugins/handoff/references/throughline-format.md`:

````markdown
# Throughline Format

The throughline is one derived Markdown document per project:

```text
<project_root>/.agents/handoffs/THROUGHLINE.md
```

The capital filename signals "not a session handoff" in directory listings.

## Frontmatter

```yaml
---
type: throughline
updated_at: "2026-06-10T14:30:00Z"
project: fixture-project
covers_through: "2026-06-10_01-19-11_plan-patched-inline-execution-ready.md"
sources_folded: 47
---
```

`covers_through` holds the basename of the newest source handoff folded in. It
is a high-water mark of what was folded, not proof of complete coverage.
`sources_folded` holds the total count of source files folded; together the
pair lets a refresh detect drift below the water line.

The detection class is count drift — files appearing or vanishing — not
in-place content edits of same-named files: handoffs are write-once by
contract, and content-edit staleness is handled by the rebuild recovery path,
not by detection.

## Body Prompts

```markdown
# Throughline: <project>

## Project Narrative
## Decisions That Hold
## Abandoned Paths
## Frontier (as of <updated_at>)
```

These headings are prompts, not a schema.

- **Project Narrative** — the eras: what each phase was about, how we got here.
- **Decisions That Hold** — settled choices and load-bearing constraints; the
  "don't relitigate this" layer. Only truly project-level settled choices
  belong here; side-branch decisions stay branch-scoped.
- **Abandoned Paths** — what was tried and dropped, and why.
- **Frontier (as of `<updated_at>`)** — open threads at last refresh,
  explicitly deferring to the newest handoff and live state for current truth.

## Size

Short enough to load alongside a handoff without dominating context. This is
prose guidance, not a validator.

## Evidence Boundary

The throughline is derived evidence, not authority: on conflict, the
underlying handoffs and live state win.
````

- [ ] **Step 2: Validate**

The file is untracked, so `git diff --check` cannot see it; check trailing whitespace directly:

Run: `grep -nE ' +$' /Users/jp/.agents/plugins/handoff/references/throughline-format.md; echo "exit: $?"`
Expected: no matching lines, `exit: 1`.

- [ ] **Step 3: Commit**

```bash
git -C /Users/jp/.agents add plugins/handoff/references/throughline-format.md
git -C /Users/jp/.agents commit -m "feat(handoff): add throughline format reference" -m "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: The `throughline` skill

**Files:**
- Create: `plugins/handoff/skills/throughline/SKILL.md`
- Create: `plugins/handoff/skills/throughline/agents/openai.yaml`

- [ ] **Step 1: Write SKILL.md**

Write exactly this content to `/Users/jp/.agents/plugins/handoff/skills/throughline/SKILL.md`:

````markdown
---
name: throughline
description: "Maintain THROUGHLINE.md, the derived rolling history of the project's handoff pile. Use when user runs `/throughline` or `$throughline`, or asks to create, refresh, or rebuild the project throughline."
---

# Throughline

Maintain one derived, concise Markdown document per project that condenses the
handoff pile into a readable history: project narrative, decisions that hold,
abandoned paths, and the current frontier.

Invoked as `/throughline` or `$throughline`.

The throughline is derived evidence, not authority: on conflict, the
underlying handoffs and live state win. It is regenerable at any time from the
pile.

When a separate `markdown-synthesis` skill is available, ad hoc multi-document
synthesis into standalone files belongs to it; this skill owns only the
canonical, maintained project handoff arc at its fixed path.

## The Artifact

One document per project:

```text
<project_root>/.agents/handoffs/THROUGHLINE.md
```

Project root resolution:

1. Use `git rev-parse --show-toplevel` when the current directory is inside a git repository.
2. Otherwise use the current working directory.

Frontmatter and section prompts live in `../../references/throughline-format.md`.
The frontmatter coverage pair — `covers_through` (basename of the newest
source handoff folded in) and `sources_folded` (total count of source files
folded) — is the only machinery. It is a high-water mark of what was folded,
not proof of complete coverage, and never truth: when it conflicts with the
listed source set or live reality, rebuild rather than trust it.

## Source Set

Source material is timestamped session handoffs — `*.md` files with the
`YYYY-MM-DD_*` filename shape — in:

```text
<project_root>/.agents/handoffs/
<project_root>/.claude/handoffs/   (legacy, read-only)
<project_root>/.codex/handoffs/    (legacy, read-only)
```

Top-level files plus files in each directory's `archive/` subdirectory, one
named level only. Archived handoffs are often most of a project's history.

`THROUGHLINE.md` itself, other subdirectories, and non-handoff files are never
source material: the throughline must not ingest its own derived content.

Ordering: compare by the parsed timestamp portion of the basename, never raw
string order — `-` and `_` sort differently at the precision boundary, so
lexicographic comparison misorders mixed-precision names. Treat
minute-precision legacy names conservatively; when two names tie at the
available precision — including `-2`/`-3` collision suffixes — include each
tied file for reading and break remaining ties by full basename. Skipping is
the dangerous direction; re-reading one file is cheap. `covers_through`
defines a cut line, not a file identity: basenames equal to the marker are
re-read regardless of which source directory holds them.

## Refresh Behavior

- **First run** (no `THROUGHLINE.md`): read the full source set, synthesize,
  write the document.
- **Subsequent runs**: read the existing document, then list the full source
  set — listing is cheap; reading is the cost. Check for drift: if the count
  of source files at or below `covers_through` does not match
  `sources_folded`, older files have appeared or vanished below the water
  line (restored archive, copied legacy handoffs, branch switch) — fall back
  to a full rebuild. Otherwise read only source handoffs newer than
  `covers_through`, then rewrite the whole document, folding in new material
  and compressing older material as needed. Rewrite, not append — that is
  what keeps the document concise forever.
- **Recovery**: coverage frontmatter missing or malformed, document
  inconsistent with reality, or user asks for a rebuild → re-read the full
  source set and regenerate.
- **Coverage honesty**: advance `covers_through` and `sources_folded` only
  over handoffs actually read in full. If the source set cannot be fully read
  (size, unreadable files), either fold a bounded batch or stop and report
  the blocked rebuild. A bounded batch folds the oldest unfolded sources
  first, so the coverage pair stays a true claim about everything at or below
  the water line. Never claim coverage past what was read.

## Synthesis

- Preserve branch and project qualifiers from handoff frontmatter: a decision
  made on a side branch is recorded as branch-scoped unless it demonstrably
  governs the project. Only truly project-level settled choices belong under
  "Decisions That Hold".
- Weigh concrete session and evidence sections over broad "Project Arc"
  restatements: handoffs saved after the throughline exists may echo the
  throughline itself, and an echo is not independent confirmation.
- Keep the document short enough to load alongside a handoff without
  dominating context. Size discipline is judgment, not a validator.

## Boundaries

- Never edit, move, archive, delete, or mark handoffs — the pile is untouched
  source material.
- No index files, no per-handoff state, no content hashes, no per-branch
  throughlines. One throughline per project.
- Never run automatically from save or load; those skills only nudge.
- Do not reproduce the full document in chat.

## Reply

```text
Throughline updated: <absolute path> (folded N handoffs, covers through <newest folded handoff>)
```

For a bounded-batch fold, use the partial wording instead — never the normal
reply:

```text
Throughline updated (partial): <absolute path> — N of M sources folded; run /throughline again to continue
```
````

- [ ] **Step 2: Write agents/openai.yaml**

Write exactly this content to `/Users/jp/.agents/plugins/handoff/skills/throughline/agents/openai.yaml`:

```yaml
interface:
  display_name: "Throughline"
```

- [ ] **Step 3: Structural validation**

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/jp/.agents/plugins/handoff/skills/throughline
ruby -ryaml -e 'YAML.load_file(ARGV[0])' /Users/jp/.agents/plugins/handoff/skills/throughline/agents/openai.yaml
ls /Users/jp/.agents/plugins/handoff/references/throughline-format.md
```

Expected: validator passes, YAML parses silently, referenced path exists. If the validator rejects the frontmatter, fix the frontmatter — do not waive.

- [ ] **Step 4: Commit**

```bash
git -C /Users/jp/.agents add plugins/handoff/skills/throughline
git -C /Users/jp/.agents commit -m "feat(handoff): add throughline skill contract" -m "Bounded-batch folds are specified oldest-first: a non-prefix batch would break the spec's drift arithmetic (count at/below covers_through vs sources_folded). Derived consequence of the spec, not a new decision." -m "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Forward tests — throughline core behavior

Each test spawns one `general-purpose` subagent via the Agent tool. After each subagent returns, run the verification block. If a check fails because the SKILL.md contract is ambiguous or wrong, fix the SKILL.md wording, re-run that test, and commit the fix as `fix(handoff): tighten throughline contract after forward test` (same trailer). If it fails because the fixture or test harness is wrong, fix the fixture (no commit). Do not weaken a check to make it pass.

**Files:**
- Test: fixture piles under `/tmp/throughline-fixtures/`
- Possibly modify: `plugins/handoff/skills/throughline/SKILL.md` (only on contract failures)

- [ ] **Step 1: Test 4.1 — first run (source-set boundaries, ordering, collisions, branch scoping, echo)**

Agent prompt (verbatim):

```text
You are forward-testing a skill behavior contract against a fixture, as a proxy for a future agent session.

1. Read /Users/jp/.agents/plugins/handoff/skills/throughline/SKILL.md and /Users/jp/.agents/plugins/handoff/references/throughline-format.md. Follow SKILL.md exactly as your behavior contract. Do not use the Skill tool and do not read any other skill files.
2. Your project root is /tmp/throughline-fixtures/proj-first. It is not a git repository; treat it as the current working directory for project-root resolution. All file reads and writes happen under that directory.
3. Execute the equivalent of the user running /throughline.
4. Then return a verification report containing: (a) the exact user-facing reply the skill prescribes; (b) every source file you read in full, as absolute paths, in the order you folded them; (c) every file you deliberately excluded from the source set, with a one-line reason each.
```

Verification:

```bash
python3 - <<'EOF'
import re
t = open('/tmp/throughline-fixtures/proj-first/.agents/handoffs/THROUGHLINE.md').read()
m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
assert m, "frontmatter missing"
fm = dict(re.findall(r'^([A-Za-z_]+):\s*(.+)$', m.group(1), re.M))
assert fm['type'] == 'throughline', fm
assert int(fm['sources_folded']) == 9, f"sources_folded: {fm.get('sources_folded')}"
assert 'wrap-up' in fm['covers_through'], f"covers_through: {fm.get('covers_through')}"
for tok in ('ZEBRA-DEEP', 'ZEBRA-NOTES'):
    assert tok not in t, f"derived doc ingested excluded content: {tok}"
for h in ('## Project Narrative', '## Decisions That Hold', '## Abandoned Paths', '## Frontier'):
    assert h in t, f"missing section: {h}"
print("PASS 4.1 artifact checks")
EOF
```

Then check the subagent's report by inspection:
- Read-in-full list has all 9 sources: 6 top-level `.agents` files (including BOTH `wrap-up` collision files and BOTH same-minute `init-*` files), 2 `archive/` files, 1 `.claude/handoffs` file.
- Excluded list names `notes.txt`, `deep/2026-05-05_05-05-05_should-not-ingest.md`, and (if mentioned) `THROUGHLINE.md`.
- In the written document, the cache decision is branch-scoped (attributed to `feature/exp-cache` or listed outside "Decisions That Hold") — NOT a project-level decision, despite the unsupported "caching is settled project-wide" echo line in `wrap-up.md`'s Project Arc.
- The reply matches `Throughline updated: <absolute path> (folded N handoffs, covers through <basename>)`.

- [ ] **Step 2: Test 4.2 — incremental refresh (reads only above the cut line, boundary re-read, rewrite)**

Agent prompt: identical to 4.1 but with project root `/tmp/throughline-fixtures/proj-refresh`, and add to item 4: `(d) state whether you did an incremental refresh or a full rebuild, and why.`

Verification:

```bash
python3 - <<'EOF'
import re
t = open('/tmp/throughline-fixtures/proj-refresh/.agents/handoffs/THROUGHLINE.md').read()
m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
fm = dict(re.findall(r'^([A-Za-z_]+):\s*(.+)$', m.group(1), re.M))
assert int(fm['sources_folded']) == 5, f"sources_folded: {fm.get('sources_folded')}"
assert 'wrap-up' in fm['covers_through'], f"covers_through: {fm.get('covers_through')}"
print("PASS 4.2 artifact checks")
EOF
```

Report inspection:
- Mode reported: incremental refresh (count at/below marker is 3, matching `sources_folded: 3` — the minute-precision archive file `2025-12-01_09-00_drop-yaml-config.md` must be counted as below the seconds-precision marker).
- Read-in-full list contains `2026-06-01_12-00-00_side-branch-experiment.md` and `2026-06-02_08-30-00_wrap-up.md`; it must NOT contain the two `archive/` files. The marker file itself (`2026-03-10_09-15-00_settle-storage-format.md`) may appear (basename-equal re-read is allowed).
- `THROUGHLINE.md` is treated only as the existing derived document — read and rewritten, never listed as a source handoff in the read/fold list. (The `sources_folded == 5` assert already fails arithmetically if it were counted as a source.)
- Echo check: "Decisions That Hold" in the rewritten document still does NOT claim project-wide caching; the cache stays branch-scoped or frontier material.

- [ ] **Step 3: Test 4.3 — drift below the water line forces full rebuild**

Agent prompt: identical to 4.2 but with project root `/tmp/throughline-fixtures/proj-drift`.

Verification:

```bash
python3 - <<'EOF'
import re
t = open('/tmp/throughline-fixtures/proj-drift/.agents/handoffs/THROUGHLINE.md').read()
m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
fm = dict(re.findall(r'^([A-Za-z_]+):\s*(.+)$', m.group(1), re.M))
assert int(fm['sources_folded']) == 6, f"sources_folded: {fm.get('sources_folded')}"
assert 'wrap-up' in fm['covers_through'], f"covers_through: {fm.get('covers_through')}"
print("PASS 4.3 artifact checks")
EOF
```

Report inspection: mode reported is full rebuild, reason names the count mismatch (4 files at/below the marker vs `sources_folded: 3`); read-in-full list has all 6 sources including `.codex/handoffs/2026-01-15_08-00-00_late-arrival.md` and both `archive/` files; `THROUGHLINE.md` is not among the listed sources — its prior content is replaced, not folded as a source (the `== 6` assert fails if it is counted).

- [ ] **Step 4: Test 4.4 — malformed coverage frontmatter forces full rebuild**

Agent prompt: identical to 4.2 but with project root `/tmp/throughline-fixtures/proj-malformed`.

Verification:

```bash
python3 - <<'EOF'
import re
t = open('/tmp/throughline-fixtures/proj-malformed/.agents/handoffs/THROUGHLINE.md').read()
m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
fm = dict(re.findall(r'^([A-Za-z_]+):\s*(.+)$', m.group(1), re.M))
assert int(fm['sources_folded']) == 5, f"sources_folded: {fm.get('sources_folded')}"
assert 'wrap-up' in fm['covers_through'], f"covers_through: {fm.get('covers_through')}"
print("PASS 4.4 artifact checks")
EOF
```

Report inspection: mode is full rebuild because `sources_folded` was missing; all 5 sources read; the rewritten frontmatter carries a complete, valid coverage pair.

- [ ] **Step 5: Test 4.5 — partial-read honesty (bounded batch, partial reply wording)**

Agent prompt: identical to 4.1 but with project root `/tmp/throughline-fixtures/proj-partial` and this extra constraint appended as item 5:

```text
5. Hard constraint for this run: you may read at most 4 source handoffs in full. Treat all other source files as unreadable this run. The skill contract tells you what an honest partial fold looks like.
```

Verification:

```bash
python3 - <<'EOF'
import re
t = open('/tmp/throughline-fixtures/proj-partial/.agents/handoffs/THROUGHLINE.md').read()
m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
fm = dict(re.findall(r'^([A-Za-z_]+):\s*(.+)$', m.group(1), re.M))
assert int(fm['sources_folded']) == 4, f"sources_folded: {fm.get('sources_folded')}"
cov = fm['covers_through']
assert ('init-minute-precision' in cov) or ('init-followup' in cov), f"covers_through not at the honest prefix boundary: {cov}"
assert 'wrap-up' not in cov and 'settle' not in cov, f"coverage claimed past what was read: {cov}"
print("PASS 4.5 artifact checks")
EOF
```

Report inspection: the batch is the oldest four by parsed timestamp (`2025-11-20_14-00-00_prototype-era.md`, `2025-12-01_09-00_drop-yaml-config.md`, then both same-minute `2026-01-05` files); the reply uses the partial wording, naming `4 of 9` sources and suggesting running `/throughline` again — not the normal updated reply.

- [ ] **Step 6: Test 4.6 — continuation run completes coverage across the minute-precision cut line**

Run only after 4.5 passes (it consumes 4.5's written state). Agent prompt: identical to 4.2 (refresh framing, report mode) but with project root `/tmp/throughline-fixtures/proj-partial` and no read constraint.

Verification:

```bash
python3 - <<'EOF'
import re
t = open('/tmp/throughline-fixtures/proj-partial/.agents/handoffs/THROUGHLINE.md').read()
m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
fm = dict(re.findall(r'^([A-Za-z_]+):\s*(.+)$', m.group(1), re.M))
assert int(fm['sources_folded']) == 9, f"sources_folded: {fm.get('sources_folded')}"
assert 'wrap-up' in fm['covers_through'], f"covers_through: {fm.get('covers_through')}"
for tok in ('ZEBRA-DEEP', 'ZEBRA-NOTES'):
    assert tok not in t, f"ingested excluded content: {tok}"
print("PASS 4.6 artifact checks")
EOF
```

Report inspection: the five genuinely newer sources (`settle-storage-format`, the `.claude` legacy file, `side-branch-experiment`, both `wrap-up` files) are all in the read list — none skipped by raw lexicographic comparison against the marker. Mode depends on which marker 4.5 set: with the seconds-precision marker (`init-followup`), expect incremental and the two oldest `archive/` files NOT re-read; with the minute-precision marker (`init-minute-precision`), a conservative tie count at the cut line may legitimately report drift and rebuild — accept a rebuild only if the report names the boundary tie as the reason. In both modes the five newer sources must all be read and the final coverage pair must match the asserts; reply uses the normal wording.

- [ ] **Step 7: Commit contract fixes, if any were needed**

If SKILL.md changed during this task:

```bash
git -C /Users/jp/.agents add plugins/handoff/skills/throughline/SKILL.md
git -C /Users/jp/.agents commit -m "fix(handoff): tighten throughline contract after forward tests" -m "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

If no changes: skip.

---

### Task 5: `load-handoff` edits + forward tests

**Files:**
- Modify: `plugins/handoff/skills/load-handoff/SKILL.md`
- Test: `/tmp/throughline-fixtures/proj-load/`

- [ ] **Step 1: Edit 1 — exclude THROUGHLINE.md from implicit selection**

In `/Users/jp/.agents/plugins/handoff/skills/load-handoff/SKILL.md`, replace:

```text
`.agents/handoffs/` is the shared primary location. The legacy directories stay in the implicit scope so older handoffs remain loadable, but nothing is ever written, moved, or migrated there.
```

with:

```text
`.agents/handoffs/` is the shared primary location. The legacy directories stay in the implicit scope so older handoffs remain loadable, but nothing is ever written, moved, or migrated there.

`THROUGHLINE.md` in a handoffs directory is the derived arc document maintained by `/throughline` (or `$throughline`), not a session handoff. Never select it as the implicit handoff, even when file modification time would make it the newest entry.
```

- [ ] **Step 2: Edit 2 — explicit-load redirect**

Replace:

```text
For explicit `/load <path>`, read exactly that path if it exists. Read a path outside the default scope, such as `docs/handoffs/` or an archive directory, only when the user explicitly provides that path.
```

with:

```text
For explicit `/load <path>`, read exactly that path if it exists. Read a path outside the default scope, such as `docs/handoffs/` or an archive directory, only when the user explicitly provides that path.

If the explicit path is a `THROUGHLINE.md`, do not apply resume-pointer framing or the response shape below. Reply briefly that it is the derived arc document, not a session handoff — read it directly or refresh it with `/throughline` — and stop.
```

- [ ] **Step 3: Edit 3a — Throughline Context section**

Replace:

```text
## Response Shape
```

with:

```text
## Throughline Context

When `THROUGHLINE.md` exists in the handoffs directory, read it in full as background arc context — its size discipline keeps a full read cheap. Add a labeled `Throughline:` line to the response: the as-of date, plus a stale note when its `covers_through` is behind the newest handoff filename timestamp.

Arc context only: never base the recommended next move on throughline content unless the selected handoff or live files corroborate it.

## Response Shape
```

- [ ] **Step 4: Edit 3b — response template line**

Replace:

```text
- Git: <branch/HEAD/worktree summary, or "unavailable: not a git repository">

Handoff says:
```

with:

```text
- Git: <branch/HEAD/worktree summary, or "unavailable: not a git repository">

Throughline: <as of <updated_at>; note staleness when covers_through is behind the newest handoff; omit this line when no THROUGHLINE.md exists>

Handoff says:
```

- [ ] **Step 5: Structural validation**

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/jp/.agents/plugins/handoff/skills/load-handoff
git -C /Users/jp/.agents diff --check -- plugins/handoff/skills/load-handoff
```

Expected: validator passes; no whitespace errors.

- [ ] **Step 6: Test 5.1 — implicit /load (exclusion, staleness line, corroboration)**

Agent prompt (verbatim):

```text
You are forward-testing a skill behavior contract against a fixture, as a proxy for a future agent session.

1. Read /Users/jp/.agents/plugins/handoff/skills/load-handoff/SKILL.md. Follow it exactly as your behavior contract. Do not use the Skill tool and do not read any other skill files.
2. Your project root is /tmp/throughline-fixtures/proj-load. It is not a git repository; treat it as the current working directory. Where the contract calls for git commands, report git state as unavailable per the contract.
3. Execute the equivalent of the user running /load with no path argument.
4. Return: (a) which file you selected as the handoff and why; (b) the full response exactly as you would give it to the user.
```

Checks on the returned response:
- Selected file is `2026-06-05_10-00-00_newest-session.md`, NOT `THROUGHLINE.md` (whose mtime is newest — the fixture touches it last).
- Response contains a `Throughline:` line noting staleness (covers through `2026-03-10...` while a `2026-06-05` handoff exists).
- "Recommended next move" follows the selected handoff (delta parser tests). The word `GAMMA` — planted only in the throughline's Frontier — must NOT appear in the recommended next move.

- [ ] **Step 7: Test 5.2 — explicit /load of THROUGHLINE.md redirects**

Agent prompt: identical to 5.1 except item 3 becomes:

```text
3. Execute the equivalent of the user running: /load /tmp/throughline-fixtures/proj-load/.agents/handoffs/THROUGHLINE.md
```

Checks: the response is a brief redirect — it identifies the file as the derived arc document, mentions `/throughline` for refreshing, and does NOT contain the resume template sections (`Loaded:`, `Handoff says:`, `Reality check:`, `Recommended next move:`).

- [ ] **Step 8: Commit**

```bash
git -C /Users/jp/.agents add plugins/handoff/skills/load-handoff/SKILL.md
git -C /Users/jp/.agents commit -m "feat(handoff): throughline awareness in load-handoff" -m "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

If a forward test exposed a wording problem, fix it before committing; the commit includes the fixed wording.

---

### Task 6: `save-handoff` edits + forward tests

**Files:**
- Modify: `plugins/handoff/skills/save-handoff/SKILL.md`
- Test: `/tmp/throughline-fixtures/proj-save-missing/`, `/tmp/throughline-fixtures/proj-save-current/`

- [ ] **Step 1: Edit 1 — arc-delta capture guidance**

In `/Users/jp/.agents/plugins/handoff/skills/save-handoff/SKILL.md`, replace:

```text
- project-arc context: where the broader project stands, why this session matters, what prior decisions are load-bearing, and what a future session should not forget
```

with:

```text
- project-arc context: the session's arc delta — what this session changed about where the project stands, which decisions became load-bearing or stopped holding, and what a future session should not forget. Record the delta, not a restatement of the already-known arc or of `THROUGHLINE.md`; restated arc text becomes an echo that a later `/throughline` refresh could mistake for independent confirmation.
```

- [ ] **Step 2: Edit 2 — reply contract with optional nudge**

Replace:

````text
7. Reply only with:

```text
Handoff saved: <absolute path>
```

Do not reproduce the full handoff in chat.
````

with:

````text
7. Reply with:

```text
Handoff saved: <absolute path>
```

Optionally add one second line suggesting `/throughline` when `THROUGHLINE.md` is missing from the handoffs directory or clearly several handoffs behind. This is judgment, not a numeric threshold; when in doubt, omit the line. Never add more than one suggestion line.

Do not reproduce the full handoff in chat.
````

(The replaced text spans a fenced block; the Edit old_string must include the inner ` ```text ` and ` ``` ` fence lines exactly.)

- [ ] **Step 3: Structural validation**

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/jp/.agents/plugins/handoff/skills/save-handoff
git -C /Users/jp/.agents diff --check -- plugins/handoff/skills/save-handoff
```

Expected: validator passes; no whitespace errors.

- [ ] **Step 4: Test 6.1 — save with throughline missing (nudge shape, arc delta)**

Agent prompt (verbatim):

```text
You are forward-testing a skill behavior contract against a fixture, as a proxy for a future agent session.

1. Read /Users/jp/.agents/plugins/handoff/skills/save-handoff/SKILL.md. Follow it exactly as your behavior contract. Do not use the Skill tool and do not read any other skill files.
2. Your project root is /tmp/throughline-fixtures/proj-save-missing. It is not a git repository; treat it as the current working directory.
3. Session context to preserve (treat as what just happened this session): "Implemented the delta parser tests and decided to cap converter flags at five. The already-known project arc, for background only: storage is plain Markdown; YAML config was dropped." Save a handoff titled "Delta parser tests".
4. Return: (a) the exact reply you would give the user, every line; (b) the absolute path of the file you wrote.
```

Checks:
- A new file matching `proj-save-missing/.agents/handoffs/20*-*_*.md` exists; its frontmatter parses (`created_at`, `type: handoff`, `title`, `project` present).
- Reply line 1 is exactly `Handoff saved: <that absolute path>`; the reply is at most 2 lines; if a second line exists it suggests `/throughline` and nothing else. (Presence of the nudge is expected here since the throughline is missing, but the hard assertion is shape: 1–2 lines, nothing more.)
- The handoff's Project Arc (or equivalent) records the session's delta (flag cap decision / parser tests) rather than only restating "storage is Markdown; YAML dropped".

- [ ] **Step 5: Test 6.2 — save with current throughline (no nudge)**

Agent prompt: identical to 6.1 with project root `/tmp/throughline-fixtures/proj-save-current`.

Checks: reply is exactly one line, `Handoff saved: <absolute path>` — the throughline exists and covers through the newest prior handoff, so a nudge would be noise ("when in doubt, omit").

- [ ] **Step 6: Commit**

```bash
git -C /Users/jp/.agents add plugins/handoff/skills/save-handoff/SKILL.md
git -C /Users/jp/.agents commit -m "feat(handoff): arc-delta guidance and throughline nudge in save-handoff" -m "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: `search-handoffs` edit + forward test

**Files:**
- Modify: `plugins/handoff/skills/search-handoffs/SKILL.md`
- Test: `/tmp/throughline-fixtures/proj-load/`

- [ ] **Step 1: Edit the Results section**

In `/Users/jp/.agents/plugins/handoff/skills/search-handoffs/SKILL.md`, replace:

```text
For many matches, show a useful handful and offer to narrow. Suggest `/load <path>` when one result looks like the right continuation artifact.
```

with:

```text
For many matches, show a useful handful and offer to narrow. Suggest `/load <path>` when one result looks like the right continuation artifact.

Matches in `THROUGHLINE.md` are from the derived arc document, not a session handoff: do not suggest `/load <path>` for them, and treat them as derived pointers to verify in source handoffs before treating a claim as decided.
```

- [ ] **Step 2: Structural validation**

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/jp/.agents/plugins/handoff/skills/search-handoffs
git -C /Users/jp/.agents diff --check -- plugins/handoff/skills/search-handoffs
```

Expected: validator passes; no whitespace errors.

- [ ] **Step 3: Test 7.1 — THROUGHLINE.md match framed as derived pointer**

Agent prompt (verbatim):

```text
You are forward-testing a skill behavior contract against a fixture, as a proxy for a future agent session.

1. Read /Users/jp/.agents/plugins/handoff/skills/search-handoffs/SKILL.md. Follow it exactly as your behavior contract. Do not use the Skill tool and do not read any other skill files.
2. Your project root is /tmp/throughline-fixtures/proj-load. It is not a git repository; treat it as the current working directory.
3. Execute the equivalent of the user running: /search GAMMA
4. Return the full response exactly as you would give it to the user.
```

Checks: the only match is in `THROUGHLINE.md`; the response notes it is the derived arc document (not a session handoff), does NOT suggest `/load` for it, and points at verifying in source handoffs before treating the claim as decided.

- [ ] **Step 4: Commit**

```bash
git -C /Users/jp/.agents add plugins/handoff/skills/search-handoffs/SKILL.md
git -C /Users/jp/.agents commit -m "feat(handoff): mark THROUGHLINE.md matches as derived in search-handoffs" -m "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 8: README and plugin manifest

**Files:**
- Modify: `plugins/handoff/README.md`
- Modify: `plugins/handoff/.claude-plugin/plugin.json`

- [ ] **Step 1: README — skills table row**

In `/Users/jp/.agents/plugins/handoff/README.md`, replace:

```text
| `/search` | Searches project handoffs with `rg`. Literal search is the default; regex is used only when requested. |
```

with:

```text
| `/search` | Searches project handoffs with `rg`. Literal search is the default; regex is used only when requested. |
| `/throughline` | Maintains `THROUGHLINE.md`, a rolling, regenerable condensation of the project's handoff pile: narrative, decisions that hold, abandoned paths, frontier. Never mutates handoffs. |
```

- [ ] **Step 2: README — boundary line revision**

Replace:

```text
Handoff does not ship runtime modules, helper scripts, command hooks, validators, transaction state, chain state, archive-on-load behavior, recovery protocols, or durable learning extraction.
```

with:

```text
Handoff does not ship runtime modules, helper scripts, command hooks, validators, transaction state, chain state, archive-on-load behavior, or recovery protocols. The only derived document is the throughline: a rolling, regenerable arc summary that never mutates handoffs and is always rebuildable from them.
```

- [ ] **Step 3: README — retired entry points stay retired**

Replace:

```text
`/quicksave`, `/summary`, and `/distill` are retired behavior. They are not wrappers, aliases, or compatibility entry points in this source bundle.
```

with:

```text
`/quicksave`, `/summary`, and `/distill` are retired behavior. They are not wrappers, aliases, or compatibility entry points in this source bundle, and `/throughline` is not a revival of them — it is a new derived-arc contract.
```

- [ ] **Step 4: README — keep the Boundaries write-line true**

`/throughline` writes a file, so the Boundaries section's write-boundary statement must change. Replace:

```text
- `/save` is the only write-oriented skill.
- `/load` and `/search` are read-only.
```

with:

```text
- `/save` is the only skill that writes session handoffs. `/throughline` writes only the derived `THROUGHLINE.md` and never mutates handoffs.
- `/load` and `/search` are read-only.
```

- [ ] **Step 5: plugin.json — version, descriptions, defaultPrompt**

In `/Users/jp/.agents/plugins/handoff/.claude-plugin/plugin.json`, make exactly these replacements:

```text
  "version": "3.0.0",
```
→
```text
  "version": "3.1.0",
```

```text
    "shortDescription": "Save, load, and search Markdown handoffs",
```
→
```text
    "shortDescription": "Save, load, and search Markdown handoffs; maintain a derived project throughline",
```

```text
    "longDescription": "Save Markdown handoffs for session continuity, load handoffs as read-only resume context, and search project handoffs with plain text search.",
```
→
```text
    "longDescription": "Save Markdown handoffs for session continuity, load handoffs as read-only resume context, and search project handoffs with plain text search. Maintain THROUGHLINE.md, a rolling derived condensation of the project's handoff history.",
```

```text
    "defaultPrompt": [
      "Save a handoff for this session",
      "Load the latest handoff",
      "Search handoffs for a decision"
    ],
```
→
```text
    "defaultPrompt": [
      "Save a handoff for this session",
      "Load the latest handoff",
      "Search handoffs for a decision",
      "Refresh the project throughline"
    ],
```

- [ ] **Step 6: Validate**

```bash
python3 -m json.tool /Users/jp/.agents/plugins/handoff/.claude-plugin/plugin.json > /dev/null && echo "JSON OK"
git -C /Users/jp/.agents diff --check -- plugins/handoff/README.md plugins/handoff/.claude-plugin/plugin.json
grep -c "write-oriented skill" /Users/jp/.agents/plugins/handoff/README.md
```

Expected: `JSON OK`, no whitespace errors, and the `grep -c` returns `0` (exit 1) — no stale "only write-oriented skill" claim survives.

- [ ] **Step 7: Commit**

```bash
git -C /Users/jp/.agents add plugins/handoff/README.md plugins/handoff/.claude-plugin/plugin.json
git -C /Users/jp/.agents commit -m "feat(handoff): bump to 3.1.0; document throughline in README and manifest" -m "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 9: Delivery check, final sweep, cleanup

**Files:**
- No repo modifications expected. Delete: `/tmp/throughline-fixtures/` (via `trash`).

- [ ] **Step 1: Claude Code delivery check**

Run: `bash /Users/jp/.agents/scripts/claude-skills-sync.sh --check`
Expected: passes with the `handoff` plugin entry healthy. No `--link` step is needed: the plugin directory is symlinked whole, so the new skill subdirectory is already inside the live symlink target.

- [ ] **Step 2: Full-bundle structural sweep**

```bash
for s in throughline load-handoff save-handoff search-handoffs; do
  python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py "/Users/jp/.agents/plugins/handoff/skills/$s" || exit 1
done
ruby -ryaml -e 'YAML.load_file(ARGV[0])' /Users/jp/.agents/plugins/handoff/skills/throughline/agents/openai.yaml
python3 -m json.tool /Users/jp/.agents/plugins/handoff/.claude-plugin/plugin.json > /dev/null
git -C /Users/jp/.agents status --short --branch
```

Expected: all validators pass; status shows a clean tree on `feature/handoff-throughline`.

- [ ] **Step 3: Spec-claim spot check**

Confirm every referenced path in the new/edited surfaces exists: `../../references/throughline-format.md` from `skills/throughline/`, and `../../references/handoff-format.md` from `skills/save-handoff/` (pre-existing). Run:

```bash
ls /Users/jp/.agents/plugins/handoff/references/throughline-format.md /Users/jp/.agents/plugins/handoff/references/handoff-format.md
```

- [ ] **Step 4: Clean up fixtures**

Run: `trash /tmp/throughline-fixtures`

- [ ] **Step 5: Report**

State plainly: which forward tests passed, any contract fixes made in Task 4, and that Codex publish (`scripts/codex-plugins-sync.sh --publish handoff`) and the GitHub mirror were deliberately NOT run (explicit-publish-only per repo rules). Do not merge to main; that is a separate user decision.

---

## Spec Validation Coverage Map

| Spec validation item | Covered by |
| --- | --- |
| Source-set boundaries (archive in; THROUGHLINE/other-subdir/non-handoff out) | Test 4.1 (archive in; `deep/` and non-handoff out — no pre-existing THROUGHLINE there), Tests 4.2/4.3 (pre-existing `THROUGHLINE.md` not listed or counted as a source) |
| Explicit `/load THROUGHLINE.md` redirect | Test 5.2 |
| Mixed filename precision honesty | Tests 4.2 (minute file counted below seconds marker), 4.5/4.6 (minute-precision `covers_through` cut line) |
| Collision suffixes (`-2`) order and fold | Test 4.1 (both wrap-up files folded; tolerant covers_through assert) |
| Late-arriving older handoffs → rebuild | Test 4.3 |
| Save recursion / echo does not promote stale claims | Tests 4.1, 4.2 (planted "caching is settled project-wide" echo) |
| `/load` corroboration rule | Test 5.1 (planted GAMMA trap) |
| Malformed/missing coverage frontmatter → rebuild | Test 4.4 |
| Partial-read honesty + partial reply wording | Test 4.5 |
| `/load` staleness notice | Test 5.1 |
| `/save` nudge shape | Tests 6.1, 6.2 |
| Branch-qualified decisions stay branch-scoped | Tests 4.1, 4.2 |
