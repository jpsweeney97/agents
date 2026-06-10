# Design: `throughline` Skill for the Handoff Plugin

Date: 2026-06-10
Status: approved (brainstorming session, 2026-06-10)
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
- **Rewrite + coverage marker mechanics**: each refresh rewrites the whole
  document; a `covers_through` frontmatter marker makes refreshes incremental;
  full-pile rebuild is the recovery path.

## 1. Identity and Invocation

New skill at `plugins/handoff/skills/throughline/`:

- `SKILL.md` — behavior contract
- `agents/openai.yaml` — companion metadata, matching the existing three skills

Invoked as `/throughline` or `$throughline`. Both runtime tokens are named in
skill text per repo convention. The name collides with no Codex-bundled or
Claude-bundled skill.

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
covers_through: "2026-06-10_01-19-11"
---
```

`covers_through` holds the filename timestamp of the newest handoff folded in.

Body sections are prompts, not a schema (same spirit as
`references/handoff-format.md`):

- **Project Narrative** — the eras: what each phase was about, how we got here
- **Decisions That Hold** — settled choices and load-bearing constraints; the
  "don't relitigate this" layer
- **Abandoned Paths** — what was tried and dropped, and why
- **Frontier (as of `<updated_at>`)** — open threads at last refresh,
  explicitly deferring to the newest handoff and live state for current truth

Size discipline is prose guidance, not a validator: short enough to load
alongside a handoff without dominating context. The capital filename signals
"not a session handoff" in directory listings.

## 3. Refresh Behavior

- **First run** (no `THROUGHLINE.md`): read the whole pile —
  `.agents/handoffs/` plus legacy `.claude/handoffs/` and `.codex/handoffs/`
  read-only — synthesize, write the document.
- **Subsequent runs**: read the existing document, read only handoffs newer
  than `covers_through` (by filename timestamp), then rewrite the whole
  document, folding in new material and compressing older material as needed.
  Rewrite, not append — that is what keeps the document concise forever.
- **Recovery**: marker missing, document inconsistent with reality, or user
  asks for a rebuild → re-read the full pile and regenerate. The marker is an
  optimization hint, never truth.
- **Reply shape**:

```text
Throughline updated: <absolute path> (folded N handoffs, covers through <timestamp>)
```

No full document reproduced in chat.

## 4. Light Nudges in Existing Skills

- **`load-handoff`** (two small edits):
  1. Exclude `THROUGHLINE.md` from handoff selection. Needed regardless of
     nudges: the mtime fallback could otherwise pick it as "newest handoff".
  2. When the document exists, read it as background arc context and add one
     line to the response shape, noting when it is behind the newest handoff
     (compare `covers_through` to the newest handoff filename timestamp).
- **`save-handoff`** (one line): after saving, if the throughline is missing
  or several handoffs behind, suggest `/throughline`. Judgment phrasing, no
  numeric threshold.
- **`search-handoffs`**: no edit. Its `rg` over the directory already covers
  the new file.

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
- Claude Code delivery is live via the skills-dir symlink
  (`scripts/claude-skills-sync.sh --check` to verify).
- Codex delivery requires an explicit
  `scripts/codex-plugins-sync.sh --publish handoff` — a separate,
  explicitly-requested step per repo rules. The GitHub release mirror update
  is likewise explicit-publish-time only.

## Agent-Facing-Design Audit

The only machinery is the `covers_through` marker: a deterministic pointer
that keeps refresh cost from growing with the pile, fully recoverable (rebuild
path), living in the derived document rather than on the handoffs. Everything
else — content sections, size, nudge timing, staleness judgment — stays
prose-and-judgment. No validators, thresholds, statuses, or scoring.

## Out of Scope

- Archiving, pruning, or any mutation of existing handoffs.
- Cross-project or global throughlines.
- Automatic regeneration triggered by hooks or session events.
- Publishing (Codex cache republish, GitHub mirror) — separate explicit step.
