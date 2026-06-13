---
name: skill-benchmark
description: "Use when the user wants to quantitatively benchmark a skill's performance: with/without-skill eval runs, pass-rate, token, and time deltas with variance across repeated trials, or trigger-accuracy description optimization. Claude-only (needs subagents and `claude -p`). Do not use for a single qualitative forward test that a changed skill is followed (behavior-smoke-test), adversarial skill-contract critique (scrutinize-skill), skill UX review (skill-ux-design), or authoring or constructing a skill."
---

# Skill Benchmark

Measure whether a skill actually helps, and whether it triggers, with numbers
instead of vibes. This Claude-only lane owns quantitative skill evaluation: it
runs a skill against realistic scenarios with and without the skill in context,
grades the outputs against objective assertions, and reports the delta with
variance — plus trigger-accuracy optimization of the `description` that decides
when the skill fires. On Codex the bundled `skill-creator` owns this work; this
lane is the Claude-side owner and pays no Codex budget.

It is a measurement lane, not an authoring or review lane. Construct skills by
hand-authoring against `agent-facing-design` and `skill-ux-design`; critique a
contract with `scrutinize-skill`; prove a single changed skill is followed with
`behavior-smoke-test`. Reach here when the question is "is it measurably
better?" or "does the description trigger reliably?"

## Requirements

This workflow needs Claude Code subagents (to run with-skill and baseline trials
independently) and, for description optimization, the `claude -p` CLI. Where
both are unavailable, say so and fall back to a single qualitative
`behavior-smoke-test` rather than reporting a benchmark you could not run.

## Performance benchmark

Measure the skill's effect on task outcomes.

1. **Build the eval set.** Collect 2-5 realistic scenarios a real user would
   actually hit — the prompt, any input files, and what a good result looks
   like. Keep them concrete; overfit-prone toy prompts measure nothing.
2. **Define assertions per scenario.** Objective, independently checkable
   claims about a correct output, each with a descriptive name. Skip
   assertions for genuinely subjective outputs (writing voice, visual design)
   and judge those qualitatively — do not force a number onto a judgment call.
3. **Run with-skill and baseline together.** For each scenario, spawn the
   with-skill run and the baseline run in the same turn so they finish
   together. Baseline = no skill for a new skill, or the prior version when
   measuring an improvement (snapshot it first). Run each configuration
   several times — 3 is a reasonable default — so you can report variance, not
   a single noisy sample.
4. **Grade and aggregate.** Check each assertion against each output (pass/fail
   with the evidence), then aggregate per configuration: pass rate, tokens, and
   wall-clock, each as mean ± stddev, plus the with-vs-baseline delta. The math
   is simple enough to do inline or with a throwaway script; do not stand up a
   permanent harness.
5. **Put outputs in front of the user.** Numbers hide regressions a human eye
   catches. Show the qualitative outputs alongside the deltas before
   concluding.

## Trigger / description optimization

The `description` frontmatter decides whether the skill fires. Measure and
improve it separately from task performance.

1. **Build a trigger eval set** of ~20 realistic queries, mixed should-trigger
   and should-not-trigger. The valuable negatives are near-misses — queries
   that share keywords but need something else — not obvious non-matches. Have
   the user sign off; bad queries yield bad descriptions.
2. **Measure the current description.** Run each query several times to get a
   stable trigger rate (a skill fires probabilistically, and Claude skips
   skills for tasks it can handle directly, so single runs mislead). Use the
   model id powering the current session for `claude -p` so the rate matches
   what the user experiences.
3. **Iterate on a held-out split.** Split the eval set, propose description
   revisions against the train queries, and re-score on the held-out queries.
   Select by held-out score, not train score, so you do not overfit the wording
   to the examples.
4. **Apply and report.** Show the before/after description and the score change.

## Proof discipline

A benchmark measures the outputs and triggering you sampled, not that the
contract is universally followed. Small samples are noisy — report the variance
and the trial count, and do not promote a few green runs into "the skill works."
A pass-rate delta is evidence the skill helped on these scenarios; generalize
only as far as the eval set's realism supports.

## Output

Report: the eval set and trial count; per-configuration pass rate, tokens, and
time as mean ± stddev with the delta; the qualitative read; and a recommendation
(ship, iterate, or insufficient signal). For description work, report
before/after and held-out trigger rates. Recommend another iteration when the
signal says the skill is not yet pulling its weight, and do not overfit to the
eval set.
