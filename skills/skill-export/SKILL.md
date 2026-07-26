---
name: skill-export
description: "Use when maintaining this library's skills as uploaded claude.ai Skills — building an upload-ready export from a source skill, or finding which exports went stale since their source moved. Owns capability re-targeting, cross-reference closure, and the drift-then-rebuild cycle. Do not use to commission work in a fresh tooled session (`stage-prompt`), to hand-carry a payload to another model (`courier`), or to author or review the source skill itself."
argument-hint: "[skill name to export | check]"
---

# Skill Export

This repo serves its skills to Codex by in-place scan and to Claude Code by symlink. claude.ai is a third target, and the only one with no delivery mechanism at all: Anthropic's documentation states that custom Skills **do not sync across surfaces**, so a skill uploaded there changes only when a human exports it again and re-uploads by hand. This skill owns that lane — the build, the provenance that makes staleness visible, and the rebuild.

Invocation: `/skill-export <name>` or `$skill-export <name>` to build one export; `/skill-export check` (or a bare invocation) to report which existing exports have gone stale.

Exports live in `exports/<name>/` at the repo root. That directory is inert to both delivery paths — `scripts/claude-skills-sync.sh` and `scripts/check-library-integrity.sh` each hard-list `skills/`, `skills-claude/`, and `plugins/` — so an export is never mistaken for live skill source by the tooling. Keep it that way: do not add `exports/` to either script.

## What the far side actually is

Re-targeting starts from what changes, and most of what a skill assumes survives the trip. The format is identical: `SKILL.md` with YAML frontmatter, a Markdown body, bundled reference files and scripts, the same progressive disclosure. claude.ai Skills run in a code-execution VM with **bash, a container filesystem, and code execution**; network access varies by user and admin setting. So "the far side has no tools" is the wrong default and produces the wrong port — a rule that reaches for a file or runs a check may survive intact by pointing at the container instead of the repo.

What is genuinely absent is everything *local*: this repo and every path in it, git and its history, the user's machine and home directory, MCP servers, Claude Code-only capabilities (subagents, workflows, hooks, plan mode), and any sibling skill that is not itself in the exported set.

## Export

**Census.** Walk the source and name every capability it assumes — a path it reads, a command it runs, a fact it checks, a sibling skill it hands off to, a file it writes. Do this before editing anything; the census is what the rest of the pass disposes of, and a capability never named is one silently dropped.

**Disposition.** Give every censused item exactly one of three, and be able to say which:

- **Keep** — environment-independent, or satisfiable by the container. Most prose is this.
- **Re-mechanize** — the purpose survives but the mechanism does not, so carry the purpose across in a form the far side can honour. `stage-prompt`'s "cite nothing you did not verify" has no local tree to verify against, so it becomes "cite nothing you were not given," plus an explicit list of what the reader must confirm.
- **Drop and declare** — the purpose dies with the mechanism. Say so in the export's own text, so the far side is not left holding half a rule.

The failure this ordering exists to prevent is silent degradation: when a rule's mechanism is unavailable, the cheap move is to delete the rule, and the result reads complete while quietly licensing the thing the rule forbade. A dropped verification rule does not produce a cautious export — it produces a confident one. Never drop a rule as a side effect of dropping its mechanism; decide it on purpose.

Sometimes the dispositions add up to *do not export*. When what lands in the drop column is the skill's reason to exist — `stage-prompt` without the git store it writes to, `git-hygiene` without a repo — the honest output is a recommendation against the export and the one sentence saying why, not a hollowed copy that triggers on claude.ai and cannot do the job its description promises. Say that before building rather than after.

**Closure.** Cross-references only resolve if the named skill is also in the exported set. For each one: in the set, keep it; not in the set, inline the substance it was borrowing or cut the pointer. A dangling `courier` or `apply-findings` reference is a dead end the far side cannot follow and cannot even discover is missing.

**Constraints.** These are hard — a violation is a rejected upload, not a style note:

- `name` — 64 characters max, lowercase letters, digits, and hyphens only, and it **may not contain `claude` or `anthropic`**. In this library that blocks `claude-code-docs` and `claude-home-audit`; give each an export name and record it in the provenance line.
- `description` — 1024 characters max. The library currently clears this (longest 835 characters), but re-check after editing.
- Frontmatter — `name` and `description` only. Strip the Claude Code fields: `argument-hint`, `disable-model-invocation`, `allowed-tools`.
- Body — target under 5k tokens, roughly 3,750 words.
- Package — a zip containing the skill **folder** at its root, with the folder name equal to the frontmatter `name`. Both are named upload-failure causes.

Build the zip **outside the repo** — a temp or scratch directory — and report its absolute path. It is a rebuildable artifact of a tracked directory, so it has no business in the tree, and a stray one is not merely untidy: skill work in this repo runs through a satellite worktree whose lifecycle refuses to land while an unknown ignored path sits in the tree, so a zip built into `exports/` blocks the very commit that carries the export.

**Blind read-back.** Read the finished export as the far side, with this repo and this conversation gone. Every surviving reference to a local path, a sibling skill, a commit, or a convention that exists only here is a defect found now instead of after the upload.

## Provenance

Write one HTML comment as the first line of the exported body, directly under the frontmatter:

```markdown
<!-- export: skills/<name>/ @ <sha> | <YYYY-MM-DD> | claude.ai -->
```

`<sha>` is the last commit that touched the source directory at export time — `git log -1 --format=%h -- skills/<name>/` — not `HEAD`, which moves for unrelated reasons and would report drift that never happened. The comment uploads harmlessly and costs a few tokens; it is what makes staleness a question anyone can answer later.

## Check

`scripts/exports-drift.sh` reads each export's provenance line and reports whether its source has moved since. It only reports — it never rewrites an export or advances a sha.

Staleness is not by itself a reason to rebuild: source edits that never reached the exported text leave the upload correct. Read what actually changed in the named commits, then say for each stale export whether the change reached the exported surface. Rebuild the ones where it did, and say plainly which ones you are leaving alone and why.

A rebuild is a fresh export pass, not a patch: run the census again, because the source may have gained a capability assumption the last pass never saw. End by naming what the user must now re-upload — nothing changes on claude.ai until they do.

## Boundaries

- Not a commission to a fresh tooled session — that is `stage-prompt`, whose payload is a task, consumed once and archived.
- Not a hand-carried payload to another model with a reply coming back — that is `courier`.
- Not authoring or reviewing the source skill. An export re-targets what the source says; it does not improve it. If the pass exposes a real defect in the source, say so and leave it to `agent-facing-design` or `scrutinize-skill` rather than fixing it only in the copy — that would make the export the better version and guarantee the two disagree.

## Output

```markdown
Exported: exports/<name>/ from skills/<name>/ @ <sha>
Dispositions: <n> kept, <n> re-mechanized, <n> dropped — <what was dropped>
Closure: <resolved within set | rewritten | cut>
Constraints: <pass | what was changed to pass>
Upload: <zip path> — re-upload at Settings > Capabilities > Skills
```
