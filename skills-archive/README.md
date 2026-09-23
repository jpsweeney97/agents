# skills-archive

Skills parked out of service, kept retrievable. Nothing here is live: Codex scans only `skills/`, and `scripts/claude-skills-sync.sh` links only `skills/`, `skills-claude/`, and `plugins/` into `~/.claude/skills`.

To restore a skill: `git mv skills-archive/<name> skills-claude/<name>` (or `skills/<name>` for dual-runtime), then run `scripts/claude-skills-sync.sh --link <name>`.

## Agent-team skills (archived 2026-06-12)

`design-review-team` and `tech-debt-audit` were moved here unchanged from `skills-claude/` in `9d2ef7a`, parking both Claude-only agent-team skills outside the Codex scan path and the sync link sources. Restore target: `skills-claude/`.

## write-a-skill (archived 2026-06-12)

`write-a-skill` was moved here unchanged from `skills/` in `a880b78`: its 100-line rule contradicted repo practice and official guidance, and its description doctrine duplicated `AGENTS.md` and `skill-creator`. Restore target: `skills/`.

## deliberate v1 (archived 2026-09-03)

`deliberate-v1` is the v1 bundle of `plugins/decide/skills/deliberate/` (validator, run-state store, capsules, and tests), archived in `cebf8e9` when decide 2.0.0 rebuilt `deliberate` as a light orchestrator; its `ARCHIVED.md` records the move. It is history, not a restore candidate: the live `deliberate` replaced it.

## Prune tranche 1 (archived 2026-09-05)

`postmortem`, `incident-response`, `migration-safety`, and `dependency-upgrade` were moved here unchanged from `skills/` under the 2026-07-02 framework challenge's prune branch: no typed fire on either runtime and never chosen by Codex outside this repository, ever, under the miner repaired on 2026-09-05. Why and how: `docs/plans/2026-09-04-skill-prune-tranche-1.md` (the approved list and every route edit) and the erratum in `docs/reviews/2026-09-04-skill-usage-ledger-re-read.md` (the corrected numbers). The generic restore instructions above apply to all four; their satellites were retired and come back through `scripts/satellite-fleet.py create-missing`.

## The young never-used set (archived 2026-09-21)

`decision-flip` and `incentive-map` were moved here unchanged from `skills/`, and `skill-squad` from `skills-claude/`, on JP's approval of `docs/plans/2026-09-21-skill-prune-young-never-used.md`. Unlike tranche 1 these are among the roster's youngest skills, and they were cut on a different evidence shape: none carries an inbound route from any live surface, so the move needed no route hygiene at all. `skill-squad` fired 13 times inside its own build week in June and never again in the 81 days after; `decision-flip` carries no ledger row of any kind and `incentive-map` only a synthetic probe row, and for those two the deciding input was JP's own call that the work they serve — an estimate-driven conclusion to defend, a structure other people will live under — is not coming. The census behind all three is `docs/reviews/2026-09-21-never-used-skill-census.md`. The generic restore instructions above apply; `skill-squad` restores to `skills-claude/` (Claude-only), the other two to `skills/`.
