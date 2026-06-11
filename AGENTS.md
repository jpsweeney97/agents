# AGENTS.md

Repo-specific instructions for `/Users/jp/.agents`.

This repo is the single source for skills used by both Codex and Claude Code,
plus skill metadata, references, and personal plugin marketplace metadata.
Higher-priority global instructions still apply.

## Primary Work

Optimize for day-to-day skill editing first.

Primary source surfaces:

- `skills/**/SKILL.md`
- `skills/**/agents/openai.yaml`
- `skills/**/references/*.md`
- `skills/**/examples/*.md`
- `skills/**/scripts/*`
- `skills-claude/**` (same shapes, Claude-only or Codex-excluded skills)
- `plugins/<name>/**` (canonical dual-runtime plugin sources)
- `plugins/marketplace.json`

Treat `.plugin-eval/`, `.DS_Store`, bytecode, and virtual environments as local
or generated artifacts unless the user explicitly asks to inspect them.

## Skill Layout And Delivery

- `skills/` is dual-runtime by contract. Codex scans it in place at
  `$HOME/.agents/skills`; Claude Code serves each skill through a symlink in
  `~/.claude/skills`. Editing source here edits the live skill for both
  runtimes.
- `skills-claude/` holds Claude-only or Codex-excluded skills. Some depend on
  Claude-specific tooling, and some intentionally stay out of Codex's native
  scan, such as bootstrap helpers or names that would collide with Codex-bundled
  skills. Codex must never scan them; they reach Claude through the same
  `~/.claude/skills` symlinks.
- After adding or renaming a skill, run
  `scripts/claude-skills-sync.sh --link <name>`. Run
  `scripts/claude-skills-sync.sh --check` to verify delivery; it never deletes.
  Remove stale `~/.claude/skills` entries with `trash`.
- Bootstrap and recovery are documented in the `scripts/claude-skills-sync.sh`
  header; `--link-all` rebuilds the `~/.claude/skills` symlink farm.
- The checked-out working tree is the live skill source. Branch switches,
  rebase, stash, and bisect here mutate the skills served to both runtimes
  immediately; edits made in an isolated worktree do not go live until they
  land on the checked-out branch.
- External contracts: Codex (>=0.137) scans `~/.agents/skills` natively with a
  ~2% skills context budget and truncates the skill list silently when over
  it, so keep skill count and description growth in mind. Claude Code symlink
  discovery in `~/.claude/skills` and within-session live reload through
  symlinks are undocumented behaviors, proven session-to-session only.
- When naming a new skill, avoid names already used by Codex-bundled skills
  (`~/.codex/skills/`, including `.system/`: `openai-docs`, `skill-creator`,
  `skill-installer`, `plugin-creator`, `imagegen`, `pdf`, `doc`,
  `codex-primary-runtime`) or Claude Code bundled skills (`code-review`,
  `debug`, `loop`, `claude-api`, `run`, `verify`, and similar).
- Do not edit files under `~/.claude/skills`; entries there are symlinks into
  this repo, so edit the repo source.
- In skill text, name invocation tokens for both runtimes (`/skill-name` or
  `$skill-name`), name instruction files jointly (`AGENTS.md` or `CLAUDE.md`),
  and phrase routing to single-runtime skills availability-conditionally.

## Plugin Layout And Delivery

- `plugins/<name>/` holds the canonical dual-runtime plugin sources (currently
  `handoff`, `review-family`) in Claude format: `.claude-plugin/plugin.json`
  plus `skills/`. One source serves both runtimes; never create per-runtime
  copies. The retired per-runtime trees (`claude-code-tool-dev/packages/plugins`,
  `~/.codex/plugins/{handoff,review-family}`) must not come back.
- Claude Code delivery: each plugin dir is symlinked into `~/.claude/skills` by
  `scripts/claude-skills-sync.sh` and loads in place as a skills-directory
  plugin (`<name>@skills-dir`) — no marketplace, no install, no cache.
  `SKILL.md` edits are live for the next session; hook/MCP/agent component
  changes need `/reload-plugins`. Symlinked plugin-dir discovery is
  undocumented behavior (forward-tested 2026-06-09), canary-guarded like the
  skills farm.
- Codex delivery: Codex discovers `plugins/marketplace.json` implicitly as the
  personal `turbo-mode` marketplace, but serves installed plugins from the
  versioned cache (`~/.codex/plugins/cache/turbo-mode/<name>/<version>`), not
  from source. After editing plugin source, republish with
  `scripts/codex-plugins-sync.sh --publish <name>`; `--check` reports
  source-vs-cache drift and runs in the SessionStart canary.
- External contracts (verified 2026-06-09 on Codex 0.137): marketplace plugin
  source paths must be relative (`./.agents/plugins/<name>`) because the
  implicit marketplace root is `$HOME` and absolute paths are silently
  skipped; Codex reads `.claude-plugin/plugin.json` natively; the manifest
  `interface` block and `skills` field are Codex-facing and ignored by Claude
  Code (documented unknown-field tolerance).
- Bump the manifest `version` on behavior changes: the Codex cache is
  version-keyed, and `codex plugin add` refreshes even an unchanged version,
  but version history is the only release signal the mirror and caches carry.
- Handoff storage contract: handoff skills write `<project_root>/.agents/handoffs/`
  (shared by both runtimes) and read legacy `.claude/handoffs/` and
  `.codex/handoffs/` as read-only fallbacks.
- The GitHub release mirror in `codex-tool-dev/plugins/turbo-mode/` is updated
  only at explicit publish time by copying from this repo's sources.
- Bootstrap and recovery live in the headers of `scripts/claude-skills-sync.sh`
  and `scripts/codex-plugins-sync.sh`.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues for `jpsweeney97/agents`. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default five-label triage vocabulary. See `docs/agents/triage-labels.md`.

### Domain docs

This repo uses a single-context domain-doc layout. See `docs/agents/domain.md`.

## Working Defaults

- Start file-changing work with `git status --short --branch`.
- Read the live target files before editing. Match the existing skill shape.
- Keep edits scoped to the requested skill, metadata file, reference, script, or
  marketplace entry.
- If the user asks for review, analysis, planning, or a grill-me session, stay
  read-only until they explicitly ask for edits.
- For behavior changes, inspect `SKILL.md`, companion metadata when present,
  referenced files, and related scripts together before patching.
- A minimal local skill can be only `SKILL.md` when the value is the behavior
  contract itself. Add metadata, references, examples, or scripts only when they
  reduce real load in the main skill file or support a concrete integration.

### Routine Existing Skill Edits

For accepted edits to existing skills, use this repo's normal file-changing
defaults instead of inventing a separate skill-construction workflow.

- Use `writing-principles` for obligation-only prose edits inside an existing
  skill, support doc, `AGENTS.md`, `CLAUDE.md`, or `agents/*.yaml`.
- Use `agent-facing-design` before adding or materially expanding agent-facing
  obligations, proof standards, authority rules, lifecycle behavior, mutation
  boundaries, persistence, routing, or machinery.
- Use `scrutinize-skill` for review-only skill-contract critique. After the
  review is accepted, patch the owning skill surfaces directly.
- Use `write-a-skill` or `skill-creator` for new skill bundles, generated
  metadata, bundle-shape changes, or new helper resources and scripts.
- When changing trigger, side-effect, proof, authority, or lifecycle behavior,
  update companion metadata when present and validate the touched surfaces.

## Skill Editing

`SKILL.md`:

- Keep YAML frontmatter parseable. Quote descriptions that contain colons or
  other punctuation likely to confuse YAML.
- Treat `description` as loader-facing routing text, not a compressed skill
  body. It should answer only the selection questions: "When should I read this
  skill?" and "When should I choose a different skill or no skill?"
- Prefer `Use when...` phrasing. Describe user intent, target scope, concrete
  symptoms or phrases, and the smallest non-use boundary that prevents the
  likely misroute.
- Do not summarize workflow steps, validation ladders, output formats, internal
  phases, or rationale in frontmatter. Put those in the skill body.
- Name neighboring skills, broad exclusions, examples, or constraints only when
  they are selection-critical for this skill; do not include them as a fixed
  checklist.
- Use a soft 25-60 word budget. Descriptions over about 90 words should prevent
  a specific likely misroute.
- State the expected behavior, defaults, stop conditions, and output shape.
- Keep long rubrics, examples, and rationale in `references/` or `examples/`
  when they would make `SKILL.md` heavy.

`agents/openai.yaml`:

- Treat this as companion metadata, not a substitute for the skill contract.
- It may be absent for local skills that do not need companion metadata.
- Keep the display name, short description, and default prompt aligned with the
  current `SKILL.md`.
- Minimal metadata is acceptable for local skills.

References and examples:

- Use reference files for detailed rubrics, worked examples, and rationale.
- Keep references named by purpose, and make every referenced path exist.
- Do not move behavior-critical instructions into a reference unless
  `SKILL.md` clearly says when to load it.

Scripts:

- Treat scripts as behavior surfaces when a skill invokes or references them.
- When editing a script, inspect its callers or references and run a targeted
  script check, behavior check, or dry run when practical.

## Validation Ladder

Validate the exact surfaces you edited.

1. For standalone instruction Markdown such as `AGENTS.md` or support docs,
   inspect the final diff, check added or changed referenced paths, and run
   whitespace checks such as `git diff --check` on the edited files.
2. Parse edited `SKILL.md` frontmatter and edited YAML metadata when present.
3. Inspect every referenced path from the edited surfaces; each path must exist
   and match the role claimed by the instruction.
4. For metadata-only changes, parsing plus shape/alignment checks can be enough.
5. For script changes, run a focused script check or explain why no practical
   check exists.
6. For skill behavior changes, run the available local validator when one exists.
   Treat `quick_validate.py` as structural frontmatter validation only. If no
   validator is available, state that and name the checks that replaced it.
7. For material behavior changes, add one live invocation, forward-test, or
   realistic dry run where practical.
8. If validation fails or is blocked, do not claim the change works and do not
   create the automatic local commit.

`plugin-eval` was intentionally uninstalled for this repo and should not be
used. Do not run `plugin-eval`, repair its wrapper, reinstall the plugin, or
treat its absence as an environment problem. If older notes or memories mention
`plugin-eval` as part of local skill validation, treat those notes as stale for
this repo.

Useful checks:

```bash
# When skills/<skill>/agents/openai.yaml exists:
ruby -ryaml -e 'YAML.load_file(ARGV[0])' skills/<skill>/agents/openai.yaml
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/<skill>
git diff --check -- skills/<skill>
```

For skill behavior changes, supplement static checks with a realistic dry run or
forward test when practical. Do not waive loader errors, invalid YAML, missing
referenced files, test failures, script/runtime errors, or behavior-contract
failures.

For local skills in `skills/` and `skills-claude/`, the edited source is the
live local skill source for future Codex and Claude Code invocations. Do not
invent a separate installed-runtime proof layer for those files. Keep the proof boundary narrower: structural checks show
the files parse, while a realistic invocation, forward test, or dry run shows
whether the changed behavior is followed. Installed/cache/marketplace proof is
only relevant for plugin-distributed skills or other copied runtime surfaces.

## Marketplace Metadata

`plugins/marketplace.json` is editable local metadata that Codex parses at
runtime as a marketplace manifest; invalid entries are skipped silently. It is
not proof of installation, activation, or runtime plugin state.

- Edit it when the task asks for personal marketplace metadata changes.
- Keep `source.path` entries relative (`./.agents/plugins/<name>`): the
  implicit personal marketplace root is `$HOME`, and Codex (0.137) silently
  skips absolute paths. Verify each referenced path exists, and confirm
  resolution with `codex plugin list` after edits.
- Do not claim installation, activation, loaded skill state, hook behavior, or
  runtime plugin behavior from this file alone.
- Before making runtime claims, verify through the relevant Codex or plugin
  inspection path, such as installed cache inspection, app-server `plugin/read`,
  `plugin/list`, `skills/list`, `hooks/list`, or another task-specific runtime
  check.
- Keep publishing explicit. Do not sync, push, publish, or mutate remote
  marketplace state unless the user asks for that.

## Design Gate

The canonical behavior lives in `skills/agent-facing-design/SKILL.md`. Use
the `agent-facing-design` skill when creating or materially changing prompts, skills,
agent rules, workflows, schemas, validators, routers, hooks, tools, commands,
scripts, or persistent artifacts that an agent must read, populate, follow, or
call.

Default to context that helps agents exercise judgment: examples, boundaries,
recoverable state, structured evidence, preconditions, and failure behavior.
Before adding required fields, statuses, workflow stages, validators,
classifiers, scoring, confidence, hard rules, or semantic decision scripts, use
the skill to check whether the machinery protects the user's work product more
than lighter context would.

## Communication

- Follow the global communication rules. In this repo, remember those rules
  apply to chat, not to authored skill or instruction artifacts.

## Git And Cleanup

- Before staging or committing, review `git diff --stat` and the relevant diff.
- For completed, focused, file-changing work in this repo, create a local commit
  by default after focused verification when a coherent commit can be made.
- Do not create the automatic local commit if the user asked not to commit, the
  turn was review-only or exploratory, validation is failing or blocked, the work
  is incomplete, or unrelated/overlapping dirty files make safe staging
  ambiguous.
- Do not push commits, add remotes, create pull requests, sync marketplaces, or
  otherwise publish changes unless the user asks for that.
- Use `trash <path>` for deletion. Do not use `rm`.
