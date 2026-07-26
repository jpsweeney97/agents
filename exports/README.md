# exports

Skills re-targeted for **claude.ai**, uploaded by hand. Not live skill source.

Nothing here is served to a runtime. Codex scans `skills/` only; `scripts/claude-skills-sync.sh` links `skills/`, `skills-claude/`, and `plugins/` only; `scripts/check-library-integrity.sh` validates those same three. A `SKILL.md` under `exports/` is a build artifact of the skill it names, not a skill in its own right — edit the source in `skills/<name>/` and export again, never the copy here.

Anthropic's documentation is explicit that custom Skills do not sync across surfaces, so an uploaded skill only changes when a human re-uploads it. That makes drift the standing hazard, and provenance the thing that makes it visible: each export carries its source commit on the first line of its body.

```markdown
<!-- export: skills/<name>/ @ <sha> | <YYYY-MM-DD> | claude.ai -->
```

Run `scripts/exports-drift.sh` to see which exports have a source that moved since. Build and rebuild through the `skill-export` skill, which owns the capability re-targeting and the closure check that a hand copy skips.

Upload zips are built outside the repo and never live here: a zip is a rebuildable artifact, and an untracked one in the tree blocks the satellite worktree lifecycle from landing skill work at all.
