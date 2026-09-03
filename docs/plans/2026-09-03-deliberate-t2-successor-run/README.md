# deliberate 2.0 run on the T2 question (2026-09-03)

The complete output of the first end-to-end run of the rebuilt `deliberate` skill (decide 2.0.0), preserved here because the run directory it wrote lived in a session scratchpad that does not survive. The run doubled as the skill's first smoke test; the test record and pass/fail table are in `docs/smoke-tests/2026-09-03_deliberate-2.0-first-smoke.md`. This directory holds the deliberation itself, so the T2 question can be picked up in a later session.

**The question.** What to do with T2, the shallow-prune safety experiment (`docs/plans/2026-07-19-deliberate-shallow-prune-control-preregistration.md`, closed INCONCLUSIVE 2026-07-25 at 322 of 400 dispatches), now that deliberate 2.0 keeps a shallow Prune stage. The invoking prompt, including the planted lean and the constraints the smoke operator wrote, is `invocation-prompt.txt`; the lean and constraints were the operator's, not JP's.

**The recommendation, in one paragraph.** `check first`: spend 30 to 60 minutes trying to author one known-answer decision case (a field of about fifteen options whose best option is fixed by the case's evidence but not visible at sketch depth, checked by two fresh reads, one with Prune's view and one with Shape's). If a case can be built within three attempts, run about ten such cases through 2.0's Prune alone and count how often the known winner is cut (1 to 3 hours), then close T2's pre-registration with one status line pointing at the new test. If no case can be built in three attempts, close T2 as the lean proposed, with the attempt on record. Contest flagged "Test Contest, not Prune" as the cut most worth reviving.

**Files, in run order.**

| File | Stage | What it holds |
| --- | --- | --- |
| `00-setup.md` | setup | question, candidates, constraints at their price, values, evidence, survivor count, the lean and who saw it |
| `01-field.md` | Generate (`ideate`) | the un-ranked field of 20 options |
| `02-prune.md` | Prune | six survivors, fourteen cut records, the two unpriced trades that blocked further cuts |
| `03-shaped.md` | Shape (`option-shaping`) | the six survivors developed to comparable depth |
| `04-close.md` | Recommend (`making-recommendations`) | the full close: Decision, The Call, Why, The Case Against, What Would Flip It, door, one own cut record |
| `05-contest.md` | Contest | the one-line exclusion check |
| `06-orchestrator-close.md` | close | the final message as delivered, with the cut ledger table and the re-run offer |
| `invocation-prompt.txt` | invocation | the exact prompt the headless run received |

**To act on it in a new session.** Read `06-orchestrator-close.md` first; it is the whole result in one place. The run's own re-run offer applies: name a cut to revive, a constraint to change, or a survivor to develop further, and `deliberate` restarts from that stage using these files as the earlier stages' output. The decision is still open; nothing here has been acted on.
