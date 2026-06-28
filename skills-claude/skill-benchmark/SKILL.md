---
name: skill-benchmark
description: "Use when the user wants to quantitatively benchmark a skill's performance: with/without-skill eval runs, pass-rate, token, and time deltas with variance across repeated trials, or trigger-accuracy description optimization. Claude-only (needs the `claude -p` CLI). Do not use for a single qualitative forward test that a changed skill is followed (behavior-smoke-test), adversarial skill-contract critique (scrutinize-skill), skill UX review (skill-ux-design), or authoring or constructing a skill."
---

# Skill Benchmark

Measure whether a skill actually helps, and whether it triggers, with numbers instead of vibes. This Claude-only lane owns quantitative skill evaluation: it runs a skill against realistic scenarios with and without the skill in context, grades the outputs against objective assertions, and reports the delta with variance — plus trigger-accuracy optimization of the `description` that decides when the skill fires. On Codex the bundled `skill-creator` owns this work; this lane is the Claude-side owner and pays no Codex budget.

It is a measurement lane, not an authoring or review lane. Construct skills by hand-authoring against `agent-facing-design` and `skill-ux-design`; critique a contract with `scrutinize-skill`; prove a single changed skill is followed with `behavior-smoke-test`. Reach here when the question is "is it measurably better?" or "does the description trigger reliably?"

## Requirements

This workflow runs its trials as `claude -p` subprocesses — both the performance arms and the description-trigger runs — because only a subprocess can control which skills load: an in-session subagent inherits the full skill set and cannot exclude the target (see Measurement harness). It also needs the model under test reachable from that CLI. Where the `claude -p` CLI is unavailable, say so and fall back to a single qualitative `behavior-smoke-test` rather than reporting a benchmark you could not run.

## Isolation and authorization

Spawning the trial runs costs tokens and can touch the filesystem, so gate them the way `behavior-smoke-test` gates its proxy:

- **Authorization.** Invoking this skill is not by itself authorization to spawn the trials. Spawn only when the current subagent and CLI tool policy permits; when authorization is unclear, ask one permission question before launching the repeated trial set, since the runs are repeated and potentially costly. Bound the cost with `--max-budget-usd`.
- **File-mutation isolation.** Keep each run non-mutating with respect to the tree you are benchmarking from. A run that exercises a file-mutating target must execute against a disposable workspace or worktree copy — never the live tree, especially where that tree is itself the served skill source. If the target is inherently mutating and no isolated, non-mutating harness is available, report `not run` rather than benchmarking against live files.
- **Applying a winning description** is a separate, normal edit made after the run through your repo's usual change control — never an in-place edit of the skill under test mid-benchmark, which corrupts both the measurement and the source.

## Measurement harness

The numbers only mean something if the apparatus did what it claims. Three things must be **observed from the run's own output**, not assumed. Run each trial as a `claude -p` subprocess with `--output-format stream-json` — this skill owns that subprocess construction, because an in-session subagent inherits the full skill set and cannot exclude the target. For grading independence, follow `behavior-smoke-test`'s anti-self-grade and no-leak rules rather than restating a thinner copy; for file-mutation safety, the Isolation and authorization rules above are authoritative.

- **Isolation signal.** The `system/init` event carries a `skills` array of everything loaded. Confirm the target is **absent** from the baseline run's `skills` and **present** in the with-skill run's by parsing that array on both arms, every run. Match the present-check to how that arm loaded the target: a `--plugin-dir` performance arm registers it **namespaced** as `<plugin-name>:<skill-name>`, so match by skill-name suffix, not bare-exact; the trigger arm over the served skill set loads it under its bare name. A baseline you did not parse is a baseline you cannot trust.
- **Grading signal.** The parent run grades each output against the assertions. The trial never grades itself and is never told the assertions, the expected answer, or whether it is the with-skill or the baseline arm.
- **Fire signal.** A skill fires when the run emits an `assistant` `tool_use` block named `Skill` naming the target. No such block is no fire; a soft "would this trigger?" judgment is not a fire.

**The baseline is not empty.** The matched contrast that toggles only the target still leaves the built-in skills loaded in both arms (read the baseline run's `init.skills` for the exact built-in set). Call the baseline "built-ins-only," never "no skill," and when the target's job overlaps a loaded built-in (for example a review-style target against a built-in reviewer), say so — the delta is then measured against that substitute and understates the target.

**Validity gate.** Before reporting any delta or rate, confirm all three signals: the baseline excluded the target, grading was done by the parent, and every counted trigger was an observed fire. If any cannot be confirmed, report `not run` / `insufficient signal` rather than a number.

Worked recipe (as of claude 2.1.x — confirm by reading `init.skills` on both arms, not by trusting flags; `claude --help` lists flag names, not these behaviors):

```text
with-skill: claude -p --setting-sources project,local --plugin-dir <plugin-dir-with-only-the-target> \
              --model <session-model> --output-format stream-json --max-budget-usd <cap>
baseline:   claude -p --setting-sources project,local \
              --model <session-model> --output-format stream-json --max-budget-usd <cap>
```

Both arms hold the built-ins constant; only `--plugin-dir` toggles the target. `--plugin-dir` needs an actual plugin directory, not a bare skill folder: the path must contain `.claude-plugin/plugin.json` with the skill under `skills/<name>/SKILL.md`. A lone `<name>/SKILL.md` loads nothing — the with-skill arm then comes back identical to the baseline and the isolation signal correctly reports the target absent, so confirm the layout before trusting a null result. `--disable-slash-commands` and `--safe-mode` look like baselines but suppress `--plugin-dir` too, so they cannot form a matched pair. Pin `--model` to the model under test and confirm it from `init.model`.

## Performance benchmark

Measure the skill's effect on task outcomes.

1. **Build the eval set.** Collect 2-5 realistic scenarios a real user would actually hit — the prompt, any input files, and what a good result looks like. Keep them concrete; overfit-prone toy prompts measure nothing.
2. **Define assertions per scenario.** Objective, independently checkable claims about a correct output, each with a descriptive name. Skip assertions for genuinely subjective outputs (writing voice, visual design) and judge those qualitatively — do not force a number onto a judgment call.
3. **Run with-skill and baseline together.** For each scenario, run the with-skill and baseline subprocesses in the same turn so they finish together, isolating them per the Measurement harness. Baseline = the built-ins-only arm for a new skill, or the prior version when measuring an improvement (snapshot it first). Run each configuration several times — 3 is a reasonable default — so you can report variance, not a single noisy sample.
4. **Grade and aggregate.** The parent run checks each assertion against each output (pass/fail with the evidence; the trial does not grade itself), then aggregates per configuration: pass rate, tokens, and wall-clock, each as mean ± stddev, plus the with-vs-baseline delta. The math is simple enough to do inline or with a throwaway script; do not stand up a permanent harness.
5. **Put outputs in front of the user.** Numbers hide regressions a human eye catches. Show the qualitative outputs alongside the deltas before concluding.

## Trigger / description optimization

The `description` frontmatter decides whether the skill fires. Measure and improve it separately from task performance.

1. **Build a trigger eval set** of ~20 realistic queries, mixed should-trigger and should-not-trigger. The valuable negatives are near-misses — queries that share keywords but need something else — not obvious non-matches. Have the user sign off; bad queries yield bad descriptions.
2. **Measure the current description against the skill as served.** Trigger rate depends on the description and on the skill's served name and packaging, so run the skill under its real installed name and scope — `claude -p` over the served skill set (the normal user/project/local scope, e.g. `--setting-sources user,project,local`), never a renamed `--plugin-dir` copy. Confirm from `init.skills` that the bare-named target loaded, count a fire with the fire signal (see Measurement harness), and run each query `t` times — `t` = 5 is a reasonable default here, above the performance arm's 3 because a fire is a single binary event noisier than a graded output — to get a stable rate (a skill fires probabilistically, and Claude skips skills for tasks it can handle directly, so single runs mislead). The should-not-trigger queries are the negative control — each passes only at a near-zero fire rate across its runs, not on a single non-fire. Pin `--model` to the model under test so the rate reflects it.
3. **Select by a paired noise margin on the full set — don't split ~20 queries.** Score every candidate on the **full** set (a split strands the scarce negatives on a noisy half); guard wording-overfit by protocol — freeze at most 3 candidate descriptions before scoring, never tune-then-rescore within a round, and split only above ~40 queries. Score the incumbent and each candidate on the same queries at the same `t` trials (step 2), then, inline or with a throwaway script:
   - Per query, form `d = score_candidate - score_incumbent` (should-trigger: fire rate; should-not-trigger near-miss: `1 - fire rate`).
   - Take `mean(d)`, sample `stdev(d)` (n-1 form), `SE = stdev(d) / sqrt(N)`. **Select only if `mean(d) - 2*SE > 0`** — a two-SE noise margin, not a raw score gap; the `2` rounds the ~2.1-2.2 these N really warrant, so bias close calls to a tie.
   - **Re-confirm the lone winner on fresh runs** against the served skill, again requiring `mean(d) - 2*SE > 0` (an independent re-score strips the winner's-curse inflation from trying several candidates). If `stdev(d)` rounds to 0 (`SE < 1/t`), require the gain to exceed one fire-step (`1/t`) there, else `insufficient signal`.

**Below 12 usable queries, with one class only, or when nothing clears the margin -> `insufficient signal`:** keep the served description, and widen the set or raise `t`. At ~20 queries this test is deliberately low-power — a real but moderate win often reads as `insufficient signal`, the cue to widen or raise `t`, not proof the candidate is no better. Never ship the highest point score.
4. **Apply and report.** Show the before/after description and the score change.

## Proof discipline

A benchmark measures the outputs and triggering you sampled, not that the contract is universally followed. Beyond the validity gate above, small samples are noisy — report the variance and the trial count, and do not promote a few green runs into "the skill works." A pass-rate delta is evidence the skill helped on these scenarios; generalize only as far as the eval set's realism supports.

## Output

Report: the eval set and trial count; per-configuration pass rate, tokens, and time as mean ± stddev with the delta; the qualitative read; and a recommendation (ship, iterate, or insufficient signal). Name the baseline's built-in floor and any capability overlap with the target. For description work, report the before/after trigger rates on the full set and the paired margin (`mean(d) - 2*SE`) behind the ship / tie / `insufficient signal` call. Recommend another iteration when the signal says the skill is not yet pulling its weight, and do not overfit to the eval set. For an *invoked* skill, a null or low ON−OFF delta is not by itself grounds to discount it: the differential is blind to cognitive-offload (the skill as a summonable pre-written prompt), so read MODEL-HANDLED as *the reliability claim is moot*, never *the skill is valueless* (`contract-evaluation-methodology.md`, MODEL-HANDLED; `AGENTS.md` "What The Skills Are For").
