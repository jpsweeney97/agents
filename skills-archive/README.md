# skills-archive

Skills parked out of service, kept retrievable. Nothing here is live: Codex
scans only `skills/`, and `scripts/claude-skills-sync.sh` links only `skills/`,
`skills-claude/`, and `plugins/` into `~/.claude/skills`.

To restore a skill: `git mv skills-archive/<name> skills-claude/<name>` (or
`skills/<name>` for dual-runtime), then run
`scripts/claude-skills-sync.sh --link <name>`.
