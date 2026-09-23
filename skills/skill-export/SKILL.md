---
name: skill-export
description: "Use when maintaining this library's skills as uploaded claude.ai Skills — building an upload-ready export from a source skill, or reporting which exports went stale since their source moved. Checking is read-only; rebuilding requires an export/update request. Owns capability re-targeting and cross-reference closure. Do not use to commission work in a fresh tooled session (`stage-prompt`), to hand-carry a payload to another model (`courier`), or to author or review the source skill itself."
argument-hint: "[skill name to export | check]"
---

# Skill Export

This repo serves its skills to Codex by in-place scan and to Claude Code by symlink. claude.ai is a third target, and the only one with no delivery mechanism from this repo: nothing pushes a repo change to claude.ai, so a skill uploaded there changes only when a human exports it again and re-uploads by hand. The reverse direction does exist: Claude Code downloads the skills enabled on claude.ai into `~/.claude/skills/synced/` and loads them as `anthropic-skills:<name>` unless `syncClaudeAiSkills` is `false`, so where sync is on, an upload left enabled appears beside the repo skill in Claude Code sessions. JP's machine sets it to `false`. This skill owns that lane — the build, the provenance that makes staleness visible, and the rebuild.

Invocation: `/skill-export <name>` or `$skill-export <name>` to build one export; `/skill-export check` (or a bare invocation) to report which existing exports have gone stale.

Exports live in `exports/<name>/` at the repo root. That directory is inert to both delivery paths — `scripts/claude-skills-sync.sh` and `scripts/check-library-integrity.sh` each hard-list `skills/`, `skills-claude/`, and `plugins/` — so an export is never mistaken for live skill source by the tooling. Keep it that way: do not add `exports/` to either script.

## What the far side actually is

Re-targeting starts from what changes, and most of what a skill assumes survives the trip. The format is identical: `SKILL.md` with YAML frontmatter, a Markdown body, bundled reference files and scripts, the same progressive disclosure. claude.ai Skills run in a code-execution VM with **bash, a container filesystem, and code execution**; network access varies by user and admin setting. So "the far side has no tools" is the wrong default and produces the wrong port — a rule that reaches for a file or runs a check may survive intact by pointing at the container instead of the repo.

What is genuinely absent is everything *local*: this repo and every path in it, git and its history, the user's machine and home directory, MCP servers, Claude Code-only capabilities (subagents, workflows, hooks, plan mode), and any sibling skill that is not itself in the exported set.

## Export

**Resolve the source.** Use the requested source path, or resolve the name among `skills/<name>/`, `skills-claude/<name>/`, and `plugins/<plugin>/skills/<name>/`. Confirm its `SKILL.md` exists; ask which source only if the request leaves multiple matches. Do not use an export, archive, or installed cache as source. Keep the actual repo-relative source directory separate from the export name, including when the name must change for upload.

**Pin clean source.** Before building, run `git status --porcelain --untracked-files=all -- "$source_dir"` from the repo root. A query failure or any staged, unstaged, or untracked source change stops the export before writing provenance or packaging; report the paths and leave those changes alone. Do not auto-commit or discard source changes to make an export possible. Record `git log -1 --format=%H -- "$source_dir"`, require a successful nonempty result, and build from that clean committed source. Check the same status and commit again before packaging; if either changed, stop without claiming a completed export. Apply the same clean-source check to any external local reference files copied or inlined during the census.

**Census.** Walk the source and name every capability it assumes — a path it reads, a command it runs, a fact it checks, a sibling skill it hands off to, a file it writes. Do this before editing anything; the census is what the rest of the pass disposes of, and a capability never named is one silently dropped.

**Disposition.** Give every censused item exactly one of three, and be able to say which:

- **Keep** — environment-independent, or satisfiable by the container. Most prose is this.
- **Re-mechanize** — the purpose survives but the mechanism does not, so carry the purpose across in a form the far side can honour. `stage-prompt`'s "cite nothing you did not verify" has no local tree to verify against, so it becomes "cite nothing you were not given," plus an explicit list of what the reader must confirm.
- **Drop and declare** — the purpose dies with the mechanism. Say so in the export's own text, so the far side is not left holding half a rule.

The failure this ordering exists to prevent is silent degradation: when a rule's mechanism is unavailable, the cheap move is to delete the rule, and the result reads complete while quietly licensing the thing the rule forbade. A dropped verification rule does not produce a cautious export — it produces a confident one. Never drop a rule as a side effect of dropping its mechanism; decide it on purpose.

Sometimes the dispositions add up to *do not export*. When what lands in the drop column is the skill's reason to exist — `stage-prompt` without the git store it writes to, `git-hygiene` without a repo — the honest output is a recommendation against the export and the one sentence saying why, not a hollowed copy that triggers on claude.ai and cannot do the job its description promises. Say that before building rather than after.

**Closure.** Cross-references only resolve if the named skill is also in the exported set. For each one: in the set, keep it; not in the set, inline the substance it was borrowing or cut the pointer. A dangling `courier` or `apply-findings` reference is a dead end the far side cannot follow and cannot even discover is missing.

**Upload evidence and local checks.** Consult the current [claude.ai creation guide](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) and [upload instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude) when exporting. As checked on 2026-09-23, the claude.ai guide documents a 64-character name limit, a 200-character description limit, optional `dependencies` metadata, and a zip containing a matching skill folder. The [API guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide) separately permits 1,024 description characters; that is not evidence of claude.ai upload acceptance. If destination documentation is unavailable or conflicts with observed behavior, report the uncertainty rather than claiming the upload rules were verified.

- Validate the exported `name` and `description` against the destination evidence. Use lowercase letters, digits, and hyphens and avoid `claude` or `anthropic` in the export name as a conservative compatibility convention borrowed from the API rules, not as a verified claude.ai rejection rule.
- Retain `name`, `description`, and relevant documented metadata such as `dependencies`. Strip Claude Code-only fields such as `argument-hint`, `disable-model-invocation`, and `allowed-tools`; do not claim all other metadata causes rejection.
- Keep the body under about 5k tokens when practical; this is a size recommendation, not a proven upload limit.
- Inspect the actual zip: one skill folder at its root, folder name matching `name`, with `SKILL.md` and the referenced bundled files present. Parse frontmatter and measure character limits after editing.

Local checks establish package structure and conformance to the cited documentation. Report upload acceptance as **not tested** unless an authorized upload of this exact package was observed to succeed; a local validator cannot supply that evidence. Exporting does not authorize uploading.

Build the zip **outside the repo** — a temp or scratch directory — and report its absolute path. It is a rebuildable artifact of a tracked directory, so it has no business in the tree, and a stray one is not merely untidy: skill work in this repo runs through a satellite worktree whose lifecycle refuses to land while an unknown ignored path sits in the tree, so a zip built into `exports/` blocks the very commit that carries the export.

**Blind read-back.** Read the finished export as the far side, with this repo and this conversation gone. Every surviving reference to a local path, a sibling skill, a commit, or a convention that exists only here is a defect found now instead of after the upload.

## Provenance

Write one HTML comment as the first line of the exported body, directly under the frontmatter:

```markdown
<!-- export: <repo-relative-source-directory>/ @ <sha> | <YYYY-MM-DD> | claude.ai -->
```

`<sha>` is the clean-source commit recorded during Export, for the actual directory, for example `plugins/review-family/skills/scrutinize/`. Do not substitute `HEAD` or invent `skills/<export-name>/`: unrelated commits and renamed exports do not identify the source. The comment tracks only the named directory; changes to shared references or inlined sibling instructions outside it need separate inspection and are not covered by a `CURRENT` result.

## Check

`scripts/exports-drift.sh` reads each export's provenance line and reports committed changes, dirty source directories, malformed provenance, and query failures. `check` and bare invocation are report-only for the entire skill: do not rewrite exports, advance provenance, build zips, stage, or commit. A dirty source or failed query is unresolved, never `CURRENT`.

Staleness is not by itself a reason to rebuild: source edits that never reached the exported text leave the upload correct. Read what actually changed in the named commits, then report which stale exports need rebuilding and which do not, with reasons. Stop after the report unless the user has also authorized an export/update request covering the named exports.

An authorized rebuild is a fresh export pass, not a patch: run the census again, because the source may have gained a capability assumption the last pass never saw. End by naming what the user must now re-upload — nothing changes on claude.ai until they do.

## Boundaries

- Not a commission to a fresh tooled session — that is `stage-prompt`, whose payload is a task, consumed once and archived.
- Not a hand-carried payload to another model with a reply coming back — that is `courier`.
- Not authoring or reviewing the source skill. An export re-targets what the source says; it does not improve it. If the pass exposes a real defect in the source, say so and leave it to `agent-facing-design` or `scrutinize-skill` rather than fixing it only in the copy — that would make the export the better version and guarantee the two disagree.

## Output

For a check, report each export's status, whether rebuilding is recommended and why, and any unresolved dirty source or query failure. Do not emit a build-success packet. For a completed export:

```markdown
Exported: exports/<name>/ from <actual-source-directory>/ @ <sha>
Dispositions: <n> kept, <n> re-mechanized, <n> dropped — <what was dropped>
Closure: <resolved within set | rewritten | cut>
Local validation: <checks and results; documentation URL and date checked; any uncertainty>
Upload acceptance: <not tested | observed acceptance of this exact package>
Upload: <absolute zip path> — manual upload at Customize > Skills
```
