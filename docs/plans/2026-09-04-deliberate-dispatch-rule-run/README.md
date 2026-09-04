# deliberate 2.x run on the dispatch-rule conflict (2026-09-04)

The complete output of the first interactive run of the rebuilt `deliberate` skill (decide 2.2.1) on a real decision, preserved here because the run directory it wrote lived in a session scratchpad that does not survive. JP chose the decision from a list of four open items; the run was also the first time the `deliberate` orchestrator dispatched every stage as a fresh Opus agent from a Fable session, as decide 2.1.0 specifies.

**The question.** How to resolve the conflict between the always-loaded rule in `~/.claude/CLAUDE.md` ("Judgment stages: inherit the session model") and `deliberate`'s own rule since decide 2.1.0 ("On Claude Code, pass `model: opus` on every stage dispatch unless the user names a model"), and where the resolution should live. JP stated no lean and confirmed no constraint; every constraint and value in `00-setup.md` is marked inferred from the repo record. The evidence packet the stages read is `00-evidence.md`.

**The recommendation, in one paragraph.** Clear call for "Record the decision and change no instruction": one entry in `docs/agents/contract-decisions.md`, written as a park of the always-loaded amendment with a reopen trigger, and both texts left as written. No wrong dispatch has been observed; the cost being paid was the question carried open across six handoffs. Runner-up: ask JP directly, because every constraint the run used was inferred. What would flip it: an observed wrong dispatch, JP asking for the carve-out in his global rule, or a third skill naming its own dispatch model. Contest found three live challenges among the 19 cuts (all labelled judgment call); the one most worth contesting is the volume-keyed exception, "Add the case the rule does not cover." JP accepted the call on 2026-09-04; the ledger entry landed with this record.

**Files, in run order.**

| File | Stage | What it holds |
| --- | --- | --- |
| `00-setup.md` | setup | question, seeds from the record, four inferred constraints with costs, values, evidence scope, survivor count, stage model, lean |
| `00-evidence.md` | setup | verbatim excerpts E1 to E10: both rules, the 2.1.0 changelog and handoff, cost facts, the charter's gating text, standing decisions, the grep of skills naming a model |
| `01-field.md` | Generate (`ideate`) | 22 options, grouped by where the resolution would live |
| `02-prune.md` | Prune | 4 survivors, 18 cut records |
| `03-shaped.md` | Shape (`option-shaping`) | seven live questions answered per survivor, facts table, evidence gaps |
| `04-close.md` | Recommend (`making-recommendations`) | the close, plus one cut record for "Let skills govern their own dispatches" |
| `05-contest.md` | Contest | the one-line exclusion check |
| `06-orchestrator-close.md` | close | the delivered close: Recommend's close as written, the 19-row cut table, exclusion check, timings |

**Timings.** Run directory created 00:04, Contest finished 00:40: about 36 minutes wall clock. Generate 5 minutes, Prune 12, Shape 7, Recommend 6, Contest 3. Cost not measured.

**What the run did not do.** It did not verify facts the stages marked as assumptions, did not read the skill-usage ledger, and did not develop the 18 excluded options. The stages were isolated, so the record's inferred lean reached only Recommend and Contest.

**What came out of delivering it.** The close was pasted into the chat in full and JP rang "too loud"; the soundcheck traced it to the skill's Close section ("the Recommend stage's close, as written") competing with JP's reply contract, and decide 2.3.0 moved the full close to a file with a short summary in the chat.

To resume from any stage, edit that stage's file and re-run the stages after it; the earlier files stand.
