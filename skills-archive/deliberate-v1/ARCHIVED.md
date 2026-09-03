# deliberate v1 (archived 2026-09-03)

The complete 1.x bundle of the `deliberate` skill from the `decide` plugin, moved here unchanged when decide 2.0.0 rebuilt the skill as a light orchestrator: the 97-line `SKILL.md`, the four reference documents and `references/contract-data.yaml`, the bundled validator under `scripts/` with its fixtures, the test suite under `tests/`, and the companion `agents/openai.yaml`. Nothing here is served to either runtime.

Why it was retired: `docs/reviews/2026-09-03-deliberate-shape-assessment.md`. What replaced it: `plugins/decide/skills/deliberate/SKILL.md` and the 2.0.0 entry in `plugins/decide/CHANGELOG.md`. Its design history: `docs/specs/2026-07-13-deliberate.md` (spec, versions 1 through 30), `docs/reviews/2026-07-18-deliberate-methodology-critique.md`, and the T2 experiment record under `docs/plans/2026-07-19-deliberate-*` and `2026-07-21-deliberate-*`.

The generic restore instructions in `../README.md` do not apply to this bundle: it was a plugin skill, not a standalone one, and its validator expected sibling skills at fixed relative paths. Restoring it would mean reverting the 2.0.0 rebuild in `plugins/decide/skills/deliberate/`.
