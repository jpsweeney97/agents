# Design: `throughline` Skill for the Handoff Plugin

Date: 2026-06-10
Status: approved (brainstorming session, 2026-06-10); revised after review
adjudications (2026-06-10, rounds 1-4)
Target: `plugins/handoff/` (canonical dual-runtime plugin source)

## Problem

The handoff plugin saves one Markdown handoff per session boundary. Nothing in
the plugin reads the pile as a whole: `load-handoff` picks one file,
`search-handoffs` greps. As handoffs accumulate, the project's history —
decisions that held, directions abandoned, why things are the way they are —
is smeared across N files. A future agent either loads one handoff and misses
the arc, or loads many and burns context.

## Solution Shape

A new `throughline` skill maintains one derived, concise Markdown document per
project that condenses the handoff pile into a readable history. Decisions made
during design:

- **Rolling document**, not on-demand synthesis, not condense-and-archive.
  Old handoffs stay untouched; the throughline is derived and regenerable.
- **Explicit invocation plus light nudges**: a dedicated skill does the work;
  `load-handoff` and `save-handoff` get one-line awareness.
- **Content covers all four axes**: decision arc, abandoned paths, project
  narrative, and current frontier (frontier framed as "as of last refresh").
- **Rewrite + coverage-marker mechanics**: each refresh rewrites the whole
  document; a `covers_through` basename marker plus `sources_folded` count
  make refreshes incremental and drift-detecting; full rebuild is the
  recovery path.

## 1. Identity and Invocation

New skill at `plugins/handoff/skills/throughline/`:

- `SKILL.md` — behavior contract
- `agents/openai.yaml` — companion metadata, matching the existing three skills

Invoked as `/throughline` or `$throughline`. Both runtime tokens are named in
skill text per repo convention. The name collides with no Codex-bundled or
Claude-bundled skill.

Routing boundary: `markdown-synthesis` owns ad hoc multi-document synthesis
into standalone files; `throughline` owns only the canonical, maintained
project handoff arc at its fixed path. The new `SKILL.md` carries one routing
sentence to that effect.

## 2. The Artifact

One derived document per project:

```text
<project_root>/.agents/handoffs/THROUGHLINE.md
```

Project root resolution matches the other handoff skills: `git rev-parse
--show-toplevel` inside a git repository, otherwise the current working
directory.

Frontmatter:

```yaml
---
type: throughline
updated_at: "2026-06-10T14:30:00Z"
project: <project name>
covers_through: "2026-06-10_01-19-11_plan-patched-inline-execution-ready.md"
sources_folded: 47
---
```

`covers_through` holds the basename of the newest source handoff folded in.
It is a high-water mark of what was folded, not proof of complete coverage.
`sources_folded` holds the total count of source files folded; together the
pair lets a refresh detect drift below the water line. The detection class is
count drift — files appearing or vanishing — not in-place content edits of
same-named files: handoffs are write-once by contract, and content-edit
staleness is handled by the rebuild recovery path, not by detection.

Ordering semantics: compare by the parsed timestamp portion of the basename,
never by raw string order — `-` and `_` sort differently at the precision
boundary, so lexicographic basename comparison misorders mixed-precision
names. Treat minute-precision legacy names conservatively; when two names tie
at the available precision — including `save-handoff`'s `-2`/`-3` collision
suffixes — include the file for reading and break remaining ties by full
basename. Skipping is the dangerous direction; re-reading one file is cheap.
The marker defines a cut line, not a file identity: basenames equal to the
marker are re-read regardless of which source directory holds them.

Body sections are prompts, not a schema (same spirit as
`references/handoff-format.md`):

- **Project Narrative** — the eras: what each phase was about, how we got here
- **Decisions That Hold** — settled choices and load-bearing constraints; the
  "don't relitigate this" layer
- **Abandoned Paths** — what was tried and dropped, and why
- **Frontier (as of `<updated_at>`)** — open threads at last refresh,
  explicitly deferring to the newest handoff and live state for current truth

Synthesis preserves branch and project qualifiers from handoff frontmatter: a
decision made on a side branch is recorded as branch-scoped unless it
demonstrably governs the project. Only truly project-level settled choices
belong under "Decisions That Hold".

When deciding what holds, weigh concrete session and evidence sections over
broad "Project Arc" restatements: handoffs saved after the throughline exists
may echo the throughline itself, and an echo is not independent confirmation.

Size discipline is prose guidance, not a validator: short enough to load
alongside a handoff without dominating context. The capital filename signals
"not a session handoff" in directory listings.

## 3. Refresh Behavior

The source set is: timestamped session handoffs (`*.md` with the
`YYYY-MM-DD_*` filename shape) in `.agents/handoffs/` plus legacy
`.claude/handoffs/` and `.codex/handoffs/`, read-only — top-level files plus
files in each directory's `archive/` subdirectory, one named level only.
Archived handoffs are often most of a project's history (a sampled live
project had 69 archived vs 2 top-level), and `search-handoffs` already
reaches them through recursive `rg`. `THROUGHLINE.md` itself, other
subdirectories, and non-handoff files are never source material — the
throughline must not ingest its own derived content.

- **First run** (no `THROUGHLINE.md`): read the full source set, synthesize,
  write the document.
- **Subsequent runs**: read the existing document, then list the full source
  set — listing is cheap; reading is the cost — and check for drift: if the
  count of source files at or below `covers_through` does not match
  `sources_folded`, older files have appeared or vanished below the water
  line (restored archive, copied legacy handoffs, branch switch) — fall back
  to a full rebuild. Otherwise read only source handoffs newer than
  `covers_through` (per the ordering semantics above), then rewrite the whole
  document, folding in new material and compressing older material as needed.
  Rewrite, not append — that is what keeps the document concise forever.
- **Recovery**: coverage frontmatter missing, document inconsistent with
  reality, or user asks for a rebuild → re-read the full source set and
  regenerate. The coverage pair is never truth: when it conflicts with the
  listed source set or live reality, rebuild rather than trust it.
- **Coverage honesty**: advance `covers_through` and `sources_folded` only
  over handoffs actually read in full. If the source set cannot be fully read
  (size, unreadable files), either fold a bounded batch and set both fields
  to reflect only that batch, or stop and report the blocked rebuild. Never
  claim coverage past what was read. A bounded-batch fold must say so in the
  reply — `Throughline updated (partial): <path> — N of M sources folded;
  run /throughline again to continue` — never the normal updated reply.
- **Reply shape**:

```text
Throughline updated: <absolute path> (folded N handoffs, covers through <newest folded handoff>)
```

No full document reproduced in chat.

## 4. Light Nudges in Existing Skills

- **`load-handoff`** (three small edits):
  1. Exclude `THROUGHLINE.md` from implicit handoff selection. Needed
     regardless of nudges: the mtime fallback could otherwise pick it as
     "newest handoff".
  2. Special-case explicit `/load` of `THROUGHLINE.md`: reply briefly that it
     is derived arc context, not a session handoff — read it directly or
     refresh it with `/throughline` — instead of applying resume-pointer
     framing to it.
  3. When the document exists, read it as background arc context and add a
     labeled `Throughline:` line to the response shape (as-of date, plus a
     stale note when `covers_through` is behind the newest handoff filename
     timestamp). A full read is intended — the document's size discipline
     keeps that cheap. Arc context only: never the basis for "Recommended
     next move" unless corroborated by the selected handoff or live files.
- **`save-handoff`** (two edits):
  1. Amend the "Reply only with" response contract to allow one optional
     second line after `Handoff saved: <path>` — when the throughline is
     missing or several handoffs behind, suggest `/throughline`. Judgment
     phrasing, no numeric threshold; when in doubt, omit the nudge.
  2. Revise the project-arc capture guidance: record the session's arc delta
     — what this session changed about the project arc — not a restatement
     of the known arc or of the throughline. This keeps future handoffs
     independent evidence rather than echoes the throughline would
     re-ingest.
- **`search-handoffs`** (one sentence): in the Results guidance, note that
  matches in `THROUGHLINE.md` are the derived arc document, not a session
  handoff — do not suggest `/load <path>` for them, and treat them as derived
  pointers to verify in source handoffs before treating a claim as decided.

## 5. Boundaries

Matching the plugin's explicit-don'ts style:

- Never edit, move, archive, delete, or mark handoffs — the pile is untouched
  source material.
- No index files, no per-handoff state, no content hashes, no per-branch
  throughlines. One throughline per project.
- Never auto-run from save/load; nudges only.
- The throughline is derived evidence, not authority: on conflict, the
  underlying handoffs and live state win (mirrors the existing Evidence
  Boundary in `handoff-format.md`).
- Do not reproduce the full document in chat.

## 6. Metadata and Delivery

- Bump `plugin.json` version `3.0.0` → `3.1.0` (behavior addition; the Codex
  cache is version-keyed and version history is the release signal).
- Add a `defaultPrompt` entry and mention the throughline in the interface
  descriptions. The `"skills": "./skills/"` field picks up the new skill
  directory automatically.
- Add a short `references/throughline-format.md` for the frontmatter and
  section prompts, keeping `SKILL.md` light (symmetry with
  `handoff-format.md`).
- Update `README.md`: add `/throughline` to the skills table, and revise the
  boundary lines that currently disclaim "durable learning extraction" and
  retire `/summary` and `/distill` — state explicitly that `throughline` is a
  new derived-arc contract (rolling, regenerable, never mutating handoffs),
  not a revival of the retired entry points, which stay retired.
- Claude Code delivery is live via the skills-dir symlink
  (`scripts/claude-skills-sync.sh --check` to verify).
- Codex delivery requires an explicit
  `scripts/codex-plugins-sync.sh --publish handoff` — a separate,
  explicitly-requested step per repo rules. The GitHub release mirror update
  is likewise explicit-publish-time only.

## Agent-Facing-Design Audit

The only machinery is the coverage pair `covers_through` + `sources_folded`.
These are load-bearing coverage semantics, not a cost optimization: future
agents will trust the marker as a coverage claim, and a silently false claim
is a stale-authority failure — the damage class that justifies narrow
machinery. The guard stays minimal: one basename and one integer in the
derived document (not a content hash, not an index, no per-handoff state),
a deterministic drift check, and full rebuild as the recovery path. The
source-set definition, ordering semantics, and partial-read stop condition
are preconditions and failure behavior — context, not validators. Everything
else — content sections, size, nudge timing, staleness judgment — stays
prose-and-judgment. No validators, thresholds, statuses, or scoring.

## Validation

Beyond the repo Validation Ladder's structural checks (parse the new
`SKILL.md` frontmatter, `agents/openai.yaml`, and `plugin.json`), the
implementation plan must include realistic dry runs or forward tests against
fixture piles for:

- source-set boundaries: on rebuild, handoffs inside `archive/` are ingested,
  while `THROUGHLINE.md`, other subdirectories, and non-handoff files are not
- explicit `/load` of `THROUGHLINE.md`: returns the derived-arc redirect
  response, not resume-pointer framing
- mixed filename precision: `covers_through` comparisons stay honest across
  legacy `YYYY-MM-DD_HH-MM_*` and current `YYYY-MM-DD_HH-MM-SS_*` names
- collision suffixes: same-second `-2`/`-3` names order and fold correctly
- late-arriving older handoffs: files appearing below `covers_through`
  (restored archive, copied legacy handoffs, branch switch) trigger a full
  rebuild via the `sources_folded` drift check
- save recursion: a handoff that restates old throughline content does not
  make a stale claim "hold" without independent session evidence
- `/load` corroboration: throughline context alone cannot drive the
  recommended next move without selected-handoff or live-file corroboration
- malformed or missing coverage frontmatter (`covers_through`,
  `sources_folded`): refresh falls back to a full rebuild instead of guessing
- partial-read honesty: a blocked full read does not advance `covers_through`
  past what was actually read, and a bounded-batch fold uses the explicit
  partial reply wording
- `/load` staleness notice: a throughline behind the newest handoff is
  reported
- `/save` nudge shape: the reply stays `Handoff saved: <path>` plus at most
  one suggestion line
- branch-qualified decisions: a side-branch decision lands branch-scoped, not
  as a project-level "Decision That Holds"

Runtime and cache proof (Codex publish, GitHub mirror) stays separate until
explicit publish.

## Out of Scope

- Archiving, pruning, or any mutation of existing handoffs.
- Cross-project or global throughlines.
- Automatic regeneration triggered by hooks or session events.
- Publishing (Codex cache republish, GitHub mirror) — separate explicit step.
