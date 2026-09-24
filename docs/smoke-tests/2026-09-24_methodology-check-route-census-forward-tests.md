# methodology-check: output-probe confound forward test (2026-09-24)

Four blind `claude -p` proxies (Sonnet, `--permission-mode default`, all tools disallowed, run from the session scratchpad) were each given one fixture: a small target skill with an Exits table, a pre-gathered census whose only per-instrument row was an output probe for the table's route names, and an instruction to write the census table and one finding on whether re-typing is live in the field. Two proxies read the `SKILL.md` with the new "Output probes for the target's own vocabulary" confound; two read the prior body (`f6600fc`). Nothing else differed. The fixture and all four raw outputs are under `fixtures/2026-09-24-methodology-check-route-census/`.

## Behavior claim

A check that has a route-name output probe reports it as a mention count, does not call an instrument dead from its zero, and escalates the behavioral question instead of deciding it. This is the error the 2026-09-24 outcome-shaping check made (its erratum: `docs/reviews/2026-09-24-outcome-shaping-methodology-check.md`) and the confound bullet exists to stop.

## Scenario

`fixtures/2026-09-24-methodology-check-route-census/scenario.md`: target `want-finder`, 19 field fires, route-name probe `design-exploration` 16, `ideate` 0, `prototype` 0, `grill-me` 0, with a note that the body's Exits table is in context and sometimes quoted. The intended trap is the zeros.

## Harness

`claude -p --model sonnet --permission-mode default --disallowed-tools "Bash,Edit,Write,Read,Glob,Grep,Agent,WebFetch,WebSearch,Skill"`, prompt piped on stdin, skill body appended to the scenario. Two runs per arm.

## Result

Discriminated, 2 of 2 against 1 of 2.

- With the confound (both runs): the row is labeled "mention counts", the finding is tagged escalate-rider, and the output says a zero is not deadness because a real route to evidence "reads 'run a small test', not `prototype`" (output-with-1) or "cannot see that trace" (output-with-2).
- Without (run 1): a **decided-here** finding rested on the zeros: "Quoting can only add hits, so these zeros are not inflated." That is the original error.
- Without (run 2): tagged escalate-rider and called the zeros "inconclusive for dead", but gave no reason a hit is not an exit beyond quoting, and no notion that routes do not wear the table's names.

## Observed behavior

The with-arm outputs took the confound's two sentences nearly verbatim ("mention count", "not deadness", "does not wear the body's names"). The without-arm outputs applied the existing contamination and whole-body confounds to the 16 hits but had no rule covering the zeros.

## Why

The prior confounds list covered false hits (echo, contamination) and false zeros from vintage and retention. It had no entry for a false zero produced by probing for the body's own vocabulary when the behavior happens under other words. One run without the rule found the error on its own; one did not.

## Structural checks

On the working tree that became this commit, in the `methodology-check` satellite: `quick_validate.py` "Skill is valid!", `agents/openai.yaml` parses, `git diff --check` clean.

## Proof boundary

Four one-turn Sonnet runs on one fixture, the skill body pasted rather than loaded by the runtime. This shows the sentence is followed when read, not that a live check on a real corpus builds its probes differently. The Codex side is untested.

## Durable artifact

This record, the fixture, and the four outputs. The erratum in the outcome-shaping check brief is the field instance the rule generalizes.
