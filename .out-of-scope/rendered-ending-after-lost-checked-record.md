# Rendered ending after a checked candidate's raw reviewer record is lost

The `cross-model-review` helper does not render any ending (`complete`, `decision`, `exhausted`, or `failed`) once a checked candidate's raw reviewer record is missing, invalid, or disagrees with the accepted response. The host reports the diagnostic and the remaining evidence (candidate snapshots, request and response records) directly to the user.

## Why this is out of scope

The approved first-version design (cross-model `docs/plans/2026-09-06-cross-model-review-skill-design.md`, interruption rule) says: if an inconsistent record prevents reliable continuation, explain what is missing and stop. The adopted SKILL.md says the same for a refused `finish`. The helper's behavior matches both.

The raw record is written with exclusive create (the open fails if the file already exists) and fsync (the bytes are forced to disk) before the validated response record and before progress is saved. It goes missing only through outside interference with the review directory. As of 2026-09-07 this has never happened in a real review.

A rendered ending in this state would need a new claim: the closing check happened (the validated response file exists) but its provenance is gone. That is a new result field and a new thing every host must explain, and it risks presenting the candidate as checked with intact evidence. Reporting `candidate_checked: false` would be untrue, and reconstructing the record is forbidden.

The condition is wider than a lost record at a between-round boundary. Whenever a checked candidate's raw record is lost, a later `failed` ending is refused too, because the same check runs for every ending that names a reviewer record.

Reopen trigger: a real occurrence in a review with a checked candidate. At that point the decision is what a `failed` ending may claim, not whether the check should be skipped.

## Prior requests

- #23 — "cross-model-review: no ending can be rendered after a checked candidate's raw reviewer record is lost"
