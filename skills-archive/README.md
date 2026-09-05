# skills-archive

Skills parked out of service, kept retrievable. Nothing here is live: Codex
scans only `skills/`, and `scripts/claude-skills-sync.sh` links only `skills/`,
`skills-claude/`, and `plugins/` into `~/.claude/skills`.

To restore a skill: `git mv skills-archive/<name> skills-claude/<name>` (or
`skills/<name>` for dual-runtime), then run
`scripts/claude-skills-sync.sh --link <name>`.

## Prune tranche 1 (archived 2026-09-05)

`postmortem`, `incident-response`, `migration-safety`, and `dependency-upgrade` were moved here unchanged from `skills/` under the 2026-07-02 framework challenge's prune branch: no typed fire on either runtime and never chosen by Codex outside this repository, ever, under the miner repaired on 2026-09-05. Why and how: `docs/plans/2026-09-04-skill-prune-tranche-1.md` (the approved list and every route edit) and the erratum in `docs/reviews/2026-09-04-skill-usage-ledger-re-read.md` (the corrected numbers). The generic restore instructions above apply to all four; their satellites were retired and come back through `scripts/satellite-fleet.py create-missing`.
