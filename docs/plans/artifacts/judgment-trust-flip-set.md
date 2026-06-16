# Judgment/Trust Flip-Set — Blind Fixture

Input half of the acceptance test for the judgment-vs-trust apparatus change
(`docs/plans/2026-06-15-judgment-trust-apparatus.md`). This file carries **no
expected verdicts** — it is safe to reference while assembling reviewers. The
answer key (class + expected flip + rationale) lives in
`docs/plans/artifacts/judgment-trust-flip-set-key.md`; do **not** open it until every reviewer
disposition is recorded (Task 9), and never load either file into a reviewer's
context.

Rows 1–8 are each a finding from `.agents/skill-library-scrutiny-2026-06-15.md`;
row 9 is an over-cut probe with no report finding. To run the test, review each
named skill with the edited `scrutinize-skill` (blind, in triplicate — see Task
9). Each row names the skill and the source-report concern the reviewer is
expected to re-derive independently; the executor uses this table only to map
reviewer output onto rows.

| # | Skill | Report concern |
|---|---|---|
| 1 | scrutinize | verdict-token casing / section-name divergence with reference |
| 2 | system-design-review | "define low/med/high so the finding-cap rule is complete" |
| 3 | tdd | "no closure / done condition / output shape" flagged as a defect |
| 4 | merge-branch / closeout-check / acceptance-map / git-hygiene | protected-branch gate hand-copied into 4 skills |
| 5 | search-handoffs | `$PROJECT_ROOT` referenced in snippets, never assigned |
| 6 | gh-pr-review-loop | `@codex review` hardcode AND a "thread-assessment lacks fixed output shape" concern |
| 7 | grill-me | "'shared understanding' framing softens the adversarial posture" (report §4, grill-me row) |
| 8 | claude-code-docs | Alias section rewrites category filters that are themselves valid live enum values (`claude-md`→`memory`, `configuration`→`config`), risking silent wrong-bucket retrieval (report top-issue #10) |
| 9 | outcome-interviewer | the one-question-at-a-time interview rhythm (ask, wait, reflect, choose the next question) — an organizing structure present in the skill; no source-report finding (this row is the over-cut probe) |
