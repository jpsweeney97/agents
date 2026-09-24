# 2026-09-24 — capsule receipt rules in `design-exploration` (decide 2.6.0) and `implementation-planning` (plan-cycle 1.4.0): forward tests

Uptake evidence for the two receiving-lane repairs the outcome-shaping methodology-critique brief handed to JP (section 5 and repair 5; `docs/reviews/2026-09-24-outcome-shaping-methodology-critique.md`) and JP commissioned the same day. Each receiving skill gained one rule: read the seam of an incoming capsule (the user's words versus the previous lane's compression, unpriced, unconfirmed, deferred, accepted as offered) and treat the compressed parts as open, never as premises.

Method: eight headless runs, `claude -p --model sonnet --permission-mode default` with every tool disallowed, prompt piped on stdin, run from the session scratchpad, one fresh session per run. Each run received one skill's full `SKILL.md` inline and a conversation in which the user pastes a seam-marked capsule and asks the lane to proceed. Arm A is the text at `6119eed`; arm B is the repaired text. Two runs per arm per skill. Fixtures, runner, and raw outputs are in `fixtures/2026-09-24-capsule-receipt/`.

## Result

| Skill | Arm A (old) | Arm B (new) | Reading |
| --- | --- | --- | --- |
| `design-exploration`, capsule with three compressions and one unpriced trade | 2/2 refused to design, put all four to the user, and said unconfirmed items stay marked | 2/2 same; both also caught a wording conflict between the settled sentence and compression (b) | No discrimination. The old text's clarification step already reaches an explicitly seam-marked capsule on a one-turn fixture. |
| `implementation-planning`, approved capsule with accepted-as-offered, unconfirmed, unpriced, and deferred parts | 2/2 listed what they would not build on yet and asked before writing those tasks | 2/2 same; one run said it would list the accepted-as-offered part under `Planner decisions` as "accepted-as-offered, not confirmed", the new rule's own instruction | Not discriminating on refusal-to-build. The new rule's routing into `Planner decisions` appears 1/2 in B and 0/2 in A. |

## What this shows and does not show

- Neither repair discriminates on a fixture where the capsule's seam is explicit and the user's ask is one turn old. The fires that motivated them (08-26: a `design-exploration` session whose decisions-you-might-correct were its own design sub-decisions, not the shaping's compressions; 08-31: an `implementation-planning` run on three unconfirmed compressions) were long sessions where the capsule sat many turns back. A one-turn proxy cannot reproduce that distance.
- Both repairs are graded untested for discrimination; uptake of the specific new instruction is 1/2 for `implementation-planning` and not visible for `design-exploration` beyond behavior the old text already produced.
- The first real handoff from a 2.5.0 `outcome-shaping` capsule into either lane is the evidence to read.
