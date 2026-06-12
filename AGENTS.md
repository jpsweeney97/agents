# AGENTS.md

Repo-specific instructions for `/Users/jp/.agents`. This repo is the single
source for the skills served to both Codex and Claude Code, plus plugin
sources, skill metadata, references, and the personal plugin marketplace
manifest. Primary work is day-to-day skill editing.

## Source Authority

- The checked-out working tree is the live skill source for both runtimes.
  Branch switches, rebase, stash, and bisect mutate the served skills
  immediately; edits in an isolated worktree go live only when they land on
  the checked-out branch.
- `CLAUDE.md` is an import shim (`@AGENTS.md`). Edit `AGENTS.md`, not the
  shim; instructions added only to `CLAUDE.md` never reach Codex.
- Do not edit files under `~/.claude/skills`; entries there are symlinks into
  this repo. Edit the repo source.

## Skill Layout And Delivery

- `skills/` is dual-runtime: Codex (>=0.137) scans `$HOME/.agents/skills` in
  place; Claude Code serves each skill through a symlink in
  `~/.claude/skills`.
- `skills-claude/` holds Claude-only or Codex-excluded skills. Codex must
  never scan it; it reaches Claude through the same symlinks.
- `skills-archive/` holds retired skills. It is outside both delivery paths
  (not scanned by Codex, never linked into `~/.claude/skills`); treat it as
  history, not live skill source.
- After adding or renaming a skill, run
  `scripts/claude-skills-sync.sh --link <name>`; verify delivery with
  `--check` (it never deletes). Remove stale `~/.claude/skills` entries with
  `trash`. Bootstrap and recovery live in the script header; `--link-all`
  rebuilds the symlink farm.
- Codex gives skills a ~2% context budget and silently truncates the skill
  list when over it: keep skill count and description growth in mind.
  Claude-side symlink discovery and live reload are undocumented behavior,
  canary-guarded at session start.
- Name new skills to avoid Codex-bundled names (`~/.codex/skills/`, including
  `.system/`: `openai-docs`, `skill-creator`, `skill-installer`,
  `plugin-creator`, `imagegen`, `pdf`, `doc`, `codex-primary-runtime`) and
  Claude Code bundled names (`code-review`, `debug`, `loop`, `claude-api`,
  `run`, `verify`, and similar).
- In skill text, name invocation tokens for both runtimes (`/skill-name` or
  `$skill-name`), name instruction files jointly (`AGENTS.md` or `CLAUDE.md`),
  and phrase routing to single-runtime skills availability-conditionally.

## Plugin Layout And Delivery

- `plugins/<name>/` holds the canonical dual-runtime plugin sources (currently
  `handoff`, `review-family`) in Claude format: `.claude-plugin/plugin.json`
  plus `skills/`. One source serves both runtimes; never create per-runtime
  copies.
- Claude Code loads each plugin dir in place through its `~/.claude/skills`
  symlink as a skills-directory plugin (`<name>@skills-dir`) — no marketplace,
  install, or cache. `SKILL.md` edits are live next session; hook/MCP/agent
  component changes need `/reload-plugins`. This discovery is also
  undocumented, canary-guarded behavior.
- Codex discovers `plugins/marketplace.json` implicitly as the personal
  `turbo-mode` marketplace but serves installed plugins from the versioned
  cache (`~/.codex/plugins/cache/turbo-mode/<name>/<version>`), not from
  source. After editing plugin source, republish with
  `scripts/codex-plugins-sync.sh --publish <name>`; `--check` reports
  source-vs-cache drift and runs in the SessionStart canary. Bootstrap and
  recovery live in the script header.
- Bump the manifest `version` on behavior changes: the Codex cache is
  version-keyed, and version history is the only release signal the caches
  and mirror carry.
- Handoff storage contract: handoff skills write
  `<project_root>/.agents/handoffs/` (shared by both runtimes) and read legacy
  `.claude/handoffs/` and `.codex/handoffs/` as read-only fallbacks.
- The GitHub release mirror in `codex-tool-dev/plugins/turbo-mode/` is updated
  only at explicit publish time by copying from this repo's sources.

## Marketplace Metadata

- `plugins/marketplace.json` is editable local metadata that Codex parses at
  runtime as a marketplace manifest; invalid entries are skipped silently. It
  is not proof of installation, activation, or runtime plugin state.
- Keep `source.path` entries relative (`./.agents/plugins/<name>`): the
  implicit personal marketplace root is `$HOME`, and Codex silently skips
  absolute paths. After edits, verify each referenced path exists and confirm
  resolution with `codex plugin list`.
- Codex reads `.claude-plugin/plugin.json` natively; the manifest `interface`
  block and `skills` field are Codex-facing and ignored by Claude Code.
- Make runtime claims (installation, activation, loaded skills, hooks) only
  from a runtime inspection path: installed cache, app-server `plugin/read`,
  `plugin/list`, `skills/list`, or `hooks/list`.

## Agent skills

### Contracts charter

Admission, extraction, and retirement of behavior contracts are governed by the
contracts charter. Consult it before authoring a new skill or adopting
third-party contract material. See `docs/agents/charter.md`.

### Issue tracker

Issues are tracked in GitHub Issues for `jpsweeney97/agents`. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default five-label triage vocabulary. See `docs/agents/triage-labels.md`.

### Domain docs

This repo uses a single-context domain-doc layout. See `docs/agents/domain.md`.

## Working Defaults

- Start file-changing work with `git status --short --branch`.
- Read the live target files before editing; match the existing skill shape.
- Keep edits scoped to the requested skill, metadata file, reference, script,
  or marketplace entry.
- For behavior changes, inspect `SKILL.md`, companion metadata when present,
  referenced files, and related scripts together before patching. When
  trigger, side-effect, proof, authority, or lifecycle behavior changes,
  update companion metadata too.
- A minimal local skill can be only `SKILL.md`. Add metadata, references,
  examples, or scripts only when they reduce real load in the main skill file
  or support a concrete integration.

Route skill work through the owning lane instead of inventing a separate
workflow:

- `writing-principles` — obligation-only prose edits inside an existing skill,
  support doc, `AGENTS.md`, `CLAUDE.md`, or `agents/*.yaml`.
- `agent-facing-design` — before adding or materially expanding agent-facing
  obligations, proof standards, authority rules, lifecycle behavior, mutation
  boundaries, persistence, routing, or machinery. The canonical gate is
  `skills/agent-facing-design/SKILL.md`; do not duplicate it here.
- `scrutinize-skill` — review-only skill-contract critique. After the review
  is accepted, patch the owning skill surfaces directly.
- `skill-creator` — new skill bundles, generated metadata, bundle-shape
  changes, or new helper resources and scripts.

## Skill Editing

`SKILL.md`:

- Keep YAML frontmatter parseable; quote descriptions that contain colons or
  similar punctuation.
- `description` is loader-facing routing text answering only "when should I
  read this skill?" and "when should I choose a different skill or none?".
  Prefer `Use when...` phrasing: user intent, target scope, concrete symptoms,
  and the smallest non-use boundary that prevents the likely misroute.
- Keep workflow steps, validation ladders, output formats, internal phases,
  and rationale out of frontmatter; they belong in the body. Name neighboring
  skills or exclusions only when selection-critical.
- Soft 25-60 word description budget; go past ~90 words only to prevent a
  specific likely misroute.
- In the body, state expected behavior, defaults, stop conditions, and output
  shape.
- Keep long rubrics, worked examples, and rationale in `references/` or
  `examples/`, named by purpose. Do not move behavior-critical instructions
  into a reference unless `SKILL.md` clearly says when to load it.

`agents/openai.yaml`:

- Companion metadata, not a substitute for the skill contract. It may be
  absent, and minimal metadata is acceptable. Keep the display name, short
  description, and default prompt aligned with the current `SKILL.md`.

Scripts:

- A script a skill invokes or references is a behavior surface. When editing
  one, inspect its callers or references and run a targeted script check,
  behavior check, or dry run when practical.

## Validation Ladder

Validate the exact surfaces you edited.

1. Standalone instruction Markdown (`AGENTS.md`, support docs): inspect the
   final diff and run whitespace checks such as `git diff --check`.
2. Parse edited `SKILL.md` frontmatter and edited YAML metadata. For
   metadata-only changes, parsing plus shape/alignment checks can be enough.
3. Inspect every referenced path from the edited surfaces; each must exist
   and match the role the instruction claims.
4. For script changes, run a focused script check or explain why no practical
   check exists.
5. For skill behavior changes, run the available local validator when one
   exists, and add one live invocation, forward test, or realistic dry run
   where practical. If no validator is available, say so and name the checks
   that replaced it.
6. `quick_validate.py` is structural frontmatter validation only, and its
   schema lacks some documented-valid Claude Code fields (`argument-hint`,
   `disable-model-invocation`): treat that specific "unexpected key" complaint
   as accepted and never resolve it by deleting the field; treat any other
   failure as real.
7. Do not waive loader errors, invalid YAML, missing referenced files, test
   failures, script/runtime errors, or behavior-contract failures. If
   validation fails or is blocked, do not claim the change works and do not
   create the automatic local commit.

Useful checks:

```bash
# When skills/<skill>/agents/openai.yaml exists:
ruby -ryaml -e 'YAML.load_file(ARGV[0])' skills/<skill>/agents/openai.yaml
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/<skill>
git diff --check -- skills/<skill>
```

Proof boundaries:

- For `skills/` and `skills-claude/`, the edited source is the live local
  skill source for future invocations; do not invent a separate
  installed-runtime proof layer for those files. Structural checks prove the
  files parse; only a realistic invocation, forward test, or dry run shows
  the changed behavior is followed. Installed/cache/marketplace proof matters
  only for plugin-distributed skills or other copied runtime surfaces.
- `plugin-eval` was intentionally uninstalled for this repo: do not run it,
  repair its wrapper, reinstall it, or treat its absence as an environment
  problem. Treat leftover `.plugin-eval/` contents as local artifacts and
  older notes or memories naming `plugin-eval` for local validation as stale.

## Git And Cleanup

- Do file-changing work on a working branch (`chore/`, `fix/`, `feature/`) and
  land it on `main` with a fast-forward merge; a Claude Code user-level hook
  enforces this by blocking edits on `main`.
- Review `git diff --stat` and the relevant diff before staging or committing.
- For completed, focused, file-changing work, create a local commit by default
  after focused verification — unless the user asked not to commit, the turn
  was review-only or exploratory, validation is failing or blocked, the work
  is incomplete, or unrelated dirty files make safe staging ambiguous.
- Do not push commits, add remotes, create pull requests, sync or publish
  marketplace or mirror state, or otherwise publish unless the user asks.
- Delete with `trash <path>`, never `rm`.
