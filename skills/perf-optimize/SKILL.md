---
name: perf-optimize
description: "Use when a named target — an endpoint, command, query, render, build — has always been slow and the user wants it measurably faster: one measured optimization loop with a pre-registered target, baseline, profiling, one change at a time, and keep-or-revert on the number. Do not use for a slowdown with an unknown cause or a suspected regression (`diagnose`), a repo-wide debt scan (`tech-debt-scan`), or benchmarking a skill rather than code (`skill-benchmark`)."
---

# Perf Optimize

One optimization loop over one named target that was always slow: pre-register the goal, measure a stable baseline, profile to localize, change one thing, re-measure the identical way, keep or revert on the number, record every attempt, leave a guard. The product is a measured delta the user can trust — never a plausible story about speed.

## Boundaries

- A slowdown with an unknown cause, a suspected regression, or anything with a repro belongs to `diagnose`; it hands over here from its profiling phase when nothing broke — the code was always this slow. Hand back the moment the profile shows something actually broke: a bug, a cache that used to hit and stopped, a saturated resource with an unexplained cause.
- A scored debt backlog across a repo is `tech-debt-scan`; module seams and shallow abstractions are `improve-codebase-architecture`; one ship's rollout gauge is `deploy-plan`; whether a shipped change moved its production goal is `outcome-check`; creating metrics, traces, or logs rather than reading them is `observability-instrumentation`; benchmarking a skill rather than application code is `skill-benchmark` (Claude-only). Route to whichever of these the session has; name the gap when it lacks one.
- When the target is a web page in a browser, also read [references/browser-performance.md](references/browser-performance.md) for Core Web Vitals and the field/lab/trace labeling discipline; skip it for every other target.

## The Loop

**1. Pre-register the target.** One named target, one primary metric the user actually feels (p95 latency, wall-clock, render time, memory ceiling), and the number that counts as done — written down before the first measurement and not moved once data is in.

**2. Baseline.** Measure the current number under stated conditions: exact command, hardware, load, warm or cold state, and a fixed budget (sample count or duration). Repeat enough runs to see the run-to-run spread — that spread is the noise floor every later delta must clear. Prefer a paired two-standard-error margin over any fixed percentage; a "±5%" rule is an illustration, not a constant. If the needed tool — profiler, tracer, benchmark harness — is unavailable in this session, say so and stop; never narrate a measurement that was not taken.

**3. Localize.** Profile before changing anything: a sampling profile or flame graph shows where the time actually goes, so the fix lands on the hot path rather than the suspected one. Optimizing an unprofiled guess is the failure this skill exists to prevent.

**4. Change one thing.** One optimization per measurement; changes landed together produce one unattributable number. If several must ship together, measure each in isolation first. When the fix is a cache, four rules decide correctness: cache only what is expensive to produce and read far more often than it changes; put every input the response varies on into the key (a key omitting the viewer serves one user's data to another, shipped as a performance win); pick one invalidation strategy and state its acceptable staleness window; guard the stampede by coalescing concurrent misses or serving stale while one request recomputes. Never cache anything whose staleness is a correctness bug.

**5. Re-measure identically and decide.** Same command, same conditions, same budget as the baseline — a warm-cache result against a cold-cache baseline measures the cache, not the change. Then decide strictly:

| Result vs baseline | Action |
|---|---|
| Clears the noise floor toward the target, tests green | **Keep** — commit with the before/after numbers and conditions in the message |
| Within noise (no measurable change) | **Revert** — neutral is a revert, not a keep |
| Worse | **Revert** |
| Better number, any test red | **Revert** — a win that drops needed work is a regression wearing a win's clothing |

Correctness gates the metric: the suite stays green *and* the number moves, or the change goes back. Kept code is maintained forever; make it pay for itself.

**6. Record every attempt, including the reverted ones.** Reverted work leaves no trace in git history, which is exactly how a dead idea gets retried next quarter. Keep a short ledger — idea, baseline → result, verdict, why — as a section in the PR description by default. Write a repo file (such as `PERF.md`) only when the user asks; then check `git status` first, surface unrelated dirty state instead of writing over it, and leave the file uncommitted for review.

**7. Guard the metric that justified the fix.** Add a check sized to the primary metric — a benchmark test, a budget assertion, an alert — repeating runs or comparing medians so normal variance does not make it flaky. Name CI wiring (budget configs, benchmark jobs) as a recommendation and wire it only on request: CI changes are config changes the user did not necessarily ask for. When a guard later fires, return to step 2 and establish a fresh baseline before proposing another fix.

## Rationalizations That Fail The Loop

- "It didn't help much, but it doesn't hurt" — neutral is a revert; the change costs maintenance forever and bought nothing.
- "We already wrote it, may as well keep it" — sunk cost; the measurement does not care how long the change took to write.
- "The improvement is obvious, no need to re-measure" — then re-measuring is cheap and proves it; unmeasured wins are how neutral complexity lands.

## Proof Boundary

State what was measured, with what command, on what hardware, under what load — and what stays unverified until production; an agent usually cannot read the production metric, so say so rather than extrapolating. A finding from reading code without a measurement is a potential impact, never a measurement — label it that way. Report real measured numbers with their variance; never synthesize a performance score or readiness grade.

## Git Floor

Do this work on a working branch, never on a protected branch (repo-defined protected branches first; absent a definition, `main`, `master`, `develop`, and `release/*`). Committing kept work follows the repo's own commit conventions.
