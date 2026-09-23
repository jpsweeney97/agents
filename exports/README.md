# exports

Skills re-targeted for **claude.ai**, uploaded by hand. Not live skill source.

Nothing here is served to a runtime. Codex scans `skills/` only; `scripts/claude-skills-sync.sh` links `skills/`, `skills-claude/`, and `plugins/` only; `scripts/check-library-integrity.sh` validates those same three. A `SKILL.md` under `exports/` is a build artifact of the skill it names, not a skill in its own right — edit the canonical source under `skills/`, `skills-claude/`, or `plugins/<plugin>/skills/` and export again, never the copy here.

Nothing delivers repo changes to claude.ai, so an uploaded skill only changes when a human re-uploads it. The reverse direction does exist: Claude Code downloads the skills enabled on a claude.ai account into `~/.claude/skills/synced/` and loads them as `anthropic-skills:<name>`, unless `syncClaudeAiSkills` is `false`; this machine sets it to `false` in `~/.claude/settings.json` (2026-09-23), so uploads stay on claude.ai here. That makes drift the standing hazard, and provenance the thing that makes it visible: each export carries its source commit on the first line of its body.

```markdown
<!-- export: <repo-relative-source-directory>/ @ <sha> | <YYYY-MM-DD> | claude.ai -->
```

Run `scripts/exports-drift.sh` to report committed source changes, dirty source directories, and query failures. A `CURRENT` result covers the named directory only, not external shared references or the uploaded copy. `/skill-export check` or `$skill-export check` is report-only; building or rebuilding requires an export/update request. Export only from clean committed source, recording its actual directory and commit. The `skill-export` skill owns capability adaptation, reference closure, and destination-specific package checks; local validation does not prove claude.ai accepted an upload.

Upload zips are built outside the repo and never live here: a zip is a rebuildable artifact, and an untracked one in the tree blocks the satellite worktree lifecycle from landing skill work at all.
