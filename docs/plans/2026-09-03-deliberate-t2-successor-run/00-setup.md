# 00-setup — deliberate run on the T2 decision

Run started 2026-09-03. Runtime: Claude Code; each stage dispatched as a fresh agent via the Agent tool, session model inherited (judgment stages).

## Decision question

What should be done with T2, the shallow-prune safety experiment, now that the deliberate skill has been rebuilt light as version 2.0 and still contains a shallow Prune stage?

Background the user stated: T2 asked whether deliberate's Prune stage, which cuts options at sketch depth before any option is developed, systematically excludes options that full development would have shown to be winners. It was pre-registered and sealed 2026-07-22, run to 322 of 400 planned agent dispatches, stopped at its 15-operator-hour ceiling 2026-07-25, and closed INCONCLUSIVE: positive control undetermined, adjudication unrun. The rebuilt skill keeps a shallow Prune stage, so the question T2 asked is still live.

## User's candidates (marked as theirs)

- "Close T2 as unanswerable at acceptable cost and rely on watching real runs of the rebuilt skill instead." — `inferred` as a candidate: the user stated it as their lean rather than in a candidate list. Stages before Recommend see it as a user candidate only, never as the lean.

## Hard constraints (user confirmed)

1. Whatever replaces or continues T2 must cost well under T2's 15 operator hours. What it costs: rules out running the original protocol's unrun adjudication layer and human arm as sized, and any successor at T2's scale; the design that could give the strongest answer may be unaffordable.
2. Any new blind evaluation must follow the blind-evaluation rule in `/Users/jp/.agents-worktrees/deliberate/AGENTS.md` (lines 57-59): never reveal apparatus state (reviewer or model outputs, intermediate scores, predictions, arm identities) in any channel a current or potential ground-truth judge, human or separate model, can see, until their independent judgment is recorded; lost blinding is unrecoverable and the judgment must be re-administered to a fresh judge. What it costs: any design that uses JP as a judge must sequester results from JP until his judgment is recorded; any design that uses agents as judges must confine what they can read; every blind dispatch adds operator overhead.
3. No web research in any stage (user stated).

## Values (user stated)

- Knowing whether Prune is safe matters more than closing the question tidily.
- The user will not spend another week of operator time on it.

## Evidence stages may read

- `/Users/jp/.agents-worktrees/deliberate/docs/plans/2026-07-19-deliberate-shallow-prune-control-preregistration.md` — frontmatter (lines 1-9), Question (lines 21-23), Results (lines 274-386). `inferred`: the user pointed to frontmatter and Question and called the rest protocol detail; Results is included because it records the run's measured rates, the positive-control failure, and the successor-design notes, which bear directly on this decision. Lines 25-272 are protocol and amendments; read only when a live question needs them.
- `/Users/jp/.agents-worktrees/deliberate/docs/plans/2026-07-21-deliberate-t2-design-panel-report.md` — whole.
- `/Users/jp/.agents-worktrees/deliberate/docs/reviews/2026-09-03-deliberate-shape-assessment.md` — whole.
- `/Users/jp/.agents-worktrees/deliberate/plugins/decide/skills/deliberate/SKILL.md` — whole; this is version 2.0 of the skill, the one under test.
- `/Users/jp/.agents-worktrees/deliberate/AGENTS.md` lines 57-59 — the blind-evaluation rule.

Research: not allowed.

## Survivor count

About four (default).

## User's visible lean

"Close T2 as unanswerable at acceptable cost and rely on watching real runs of the rebuilt skill instead." Given to Recommend and Contest only.
