# AGENTS.md

Repo-specific instructions for `/Users/jp/.agents`.

This repo is local source for Codex-facing skills, skill metadata, references,
and personal plugin marketplace metadata. Higher-priority global instructions
still apply.

## Primary Work

Optimize for day-to-day skill editing first.

Primary source surfaces:

- `skills/**/SKILL.md`
- `skills/**/agents/openai.yaml`
- `skills/**/references/*.md`
- `skills/**/examples/*.md`
- `plugins/marketplace.json`

Treat `.plugin-eval/`, `.DS_Store`, bytecode, and virtual environments as local
or generated artifacts unless the user explicitly asks to inspect them.

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
- Keep edits scoped to the requested skill, metadata file, reference, or
  marketplace entry.
- If the user asks for review, analysis, planning, or a grill-me session, stay
  read-only until they explicitly ask for edits.
- For behavior changes, inspect `SKILL.md`, `agents/openai.yaml`, and referenced
  files together before patching.
- A minimal local skill can be only `SKILL.md` plus `agents/openai.yaml` when
  the value is the behavior contract itself. Add references, examples, or
  scripts only when they reduce real load in the main skill file.

## Skill Editing

`SKILL.md`:

- Keep YAML frontmatter parseable. Quote descriptions that contain colons or
  other punctuation likely to confuse YAML.
- Make the trigger and non-trigger boundaries explicit.
- State the expected behavior, defaults, stop conditions, and output shape.
- Keep long rubrics, examples, and rationale in `references/` or `examples/`
  when they would make `SKILL.md` heavy.

`agents/openai.yaml`:

- Treat this as companion metadata, not a substitute for the skill contract.
- Keep the display name, short description, and default prompt aligned with the
  current `SKILL.md`.
- Minimal metadata is acceptable for local skills.

References and examples:

- Use reference files for detailed rubrics, worked examples, and rationale.
- Keep references named by purpose, and make every referenced path exist.
- Do not move behavior-critical instructions into a reference unless
  `SKILL.md` clearly says when to load it.

## Validation Ladder

Validate the exact surfaces you edited.

1. Parse edited `SKILL.md` frontmatter and edited YAML metadata.
2. Inspect every referenced path from the edited surfaces; each path must exist
   and match the role claimed by the instruction.
3. For metadata-only changes, parsing plus shape/alignment checks can be enough.
4. For skill behavior changes, run the available local validator when one exists.
   If no validator is available, state that and name the checks that replaced it.
5. For material behavior changes, add one live invocation, forward-test, or
   realistic dry run where practical.
6. If validation fails or is blocked, do not claim the change works and do not
   create the automatic local commit.

`plugin-eval` was intentionally uninstalled for this repo and should not be
used. Do not run `plugin-eval`, repair its wrapper, reinstall the plugin, or
treat its absence as an environment problem. If older notes or memories mention
`plugin-eval` as part of local skill validation, treat those notes as stale for
this repo.

Useful checks:

```bash
ruby -ryaml -e 'YAML.load_file(ARGV[0])' skills/<skill>/agents/openai.yaml
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/<skill>
git diff --check -- skills/<skill>
```

For skill behavior changes, supplement static checks with a realistic dry run or
forward test when practical. Do not waive loader errors, invalid YAML, missing
referenced files, test failures, script/runtime errors, or behavior-contract
failures.

For local skills in `skills/`, the edited source is the live local skill source
for future Codex invocations. Do not invent a separate installed-runtime proof
layer for those files. Keep the proof boundary narrower: structural checks show
the files parse, while a realistic invocation, forward test, or dry run shows
whether the changed behavior is followed. Installed/cache/marketplace proof is
only relevant for plugin-distributed skills or other copied runtime surfaces.

## Marketplace Metadata

`plugins/marketplace.json` is editable local metadata. It is not runtime proof.

- Edit it when the task asks for personal marketplace metadata changes.
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
`$agent-facing-design` when creating or materially changing prompts, skills,
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

- In chat, lead with the user-visible behavior, experience, or decision, then
  map to technical choices.
- Match the user's register. If they ask in technical terms, answer in technical
  terms.
- Use plain language for explanations. Save formal structure for artifacts that
  need it, such as tickets, specs, handoffs, commit messages, and review reports.
- These communication rules apply to conversation, not to authored artifacts.

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
