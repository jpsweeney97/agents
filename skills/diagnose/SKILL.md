---
name: diagnose
description: "Use when the user asks to diagnose/debug a bug whose cause is unclear, hard to reproduce, intermittent, spans multiple components, or involves a performance regression. Do not use for straightforward implementation, known fixes, obvious single-test failures, code review, or post-fix architecture improvement; once the cause is known, locking the fix in test-first belongs to `tdd`."
---

# Diagnose

A discipline for hard bugs. Skip phases only when explicitly justified.

When exploring the codebase, use the project's domain glossary to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Phase 1 — Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a fast, deterministic, agent-runnable pass/fail signal for the bug, you will find the cause — bisection, hypothesis-testing, and instrumentation all just consume that signal. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one — try them in roughly this order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

Build the right feedback loop, and the bug is 90% fixed.

### Iterate on the loop itself

Treat the loop as a product. Once you have _a_ loop, ask:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop. A 2-second deterministic loop is a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not — keep raising the rate until it's debuggable.

**Classify the non-determinism before brute-forcing the rate — the cause-class names the knob that raises it and the probe to build.** Blindly looping wastes the budget the rate is supposed to buy you. One call the cause-class does *not* settle: is the *test* non-deterministic (test is wrong, code is correct → fix the test) or the *code* (the test correctly flakes on a real defect → fix the code)? You often can't tell until the rate is up and you've instrumented — so the knobs below are rate-raising **diagnostics first**: isolating, seeding, or clock-freezing the *test* makes a flaky test pass but **masks** a flaky-code defect. Apply a knob as the *fix* only once the evidence says the test, not the code, was wrong.

| Cause-class | Tell | Knob that raises the rate → where the fix lives |
|---|---|---|
| **Order / pollution** | Passes alone, fails in-suite (or vice versa) | Shuffle/bisect execution order → isolate the polluting predecessor; reset shared state between cases |
| **Shared mutable state** | Fails under parallelism or on repeat; passes isolated | Raise parallelism/repeat → give each run a fresh fixture (transaction rollback, temp dir, fresh process) or serialise |
| **Concurrency / async race** | Rate tracks load, CPU contention, or injected delay | Stress and inject sleeps at the suspected window to *raise* the rate → find the unsynchronised access |
| **Time / wall-clock** | Fails near midnight, month/DST boundaries, or under another timezone | Freeze or mock the clock; run under the failing TZ |
| **Unseeded randomness** | Fails a fixed % with no load correlation; differs every run | Seed the RNG; pin hash ordering (e.g. `PYTHONHASHSEED`); assert order-independently |
| **External / network** | Tracks network conditions; intermittent timeouts | Replay a captured trace or mock the boundary; pin the dependency |
| **Resource leak / exhaustion** | Fails *later* in a long run, not early; clears after a restart | Run the loop long and watch the resource curve → bisect to the leak site |

Match the bug to a class, then point Phase 1's loop at that class's knob. When two classes are plausible, the next thing to build is the probe that separates them.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to whatever environment reproduces it, (b) a captured artifact (HAR file, log dump, core dump, screen recording with timestamps), or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

Do not proceed to Phase 2 until you have a loop you believe in.

## Phase 2 — Reproduce

Run the loop. Watch the bug appear.

Confirm:

- [ ] The loop produces the failure mode the **user** described — not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

Do not proceed until you reproduce the bug.

## Phase 3 — Hypothesise

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is AFK.

## Phase 4 — Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan) first — measure, don't guess — then bisect. Measure first, fix second.

**Localise before optimising.** A sampling profile or flame graph shows *where* the time actually goes, so you fix the hot path and not the suspected one. Two regression shapes need two lenses, and profiling tells them apart:

- **Work-bound** — an algorithm got slower (O(n²) creep, an N+1 query, a lost cache, a needless re-render). The flame graph names the hot frame; cut the wasted work.
- **Resource-bound** — something is saturated. Sweep the **USE method**: for each resource (CPU, memory, disk/IO, network, connection pool, locks) check **U**tilisation, **S**aturation (queue depth or wait time), and **E**rrors. The first saturated resource is the bottleneck.

Profile to tell work-bound from resource-bound before reaching for either fix — they have opposite remedies.

## Phase 5 — Fix + regression test

Write the regression test **before the fix** — but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

Fix where the bad value or wrong behavior originates, not the layer where the symptom surfaced.

If the fix fails, return to Phase 3 with the new evidence instead of stacking another change on top. When roughly three fixes have failed — especially when each one reveals a new problem somewhere else — the architecture is the hypothesis now: stop and raise that with the user before attempting a fourth.

## Phase 6 — Cleanup + post-mortem

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes removed with `trash` (never `rm`), or moved to a clearly-marked debug location
- [ ] The hypothesis that turned out correct is stated in the commit / PR message — so the next debugger learns

**Then ask: what would have prevented this bug?** If the answer involves architectural change (no good test seam, tangled callers, hidden coupling) hand off to the `improve-codebase-architecture` skill with the specifics. Make the recommendation **after** the fix is in, not before — you have more information now than when you started.

For a durable, dated, blameless retrospective that outlives this commit-line — an incident with real impact, a timeline worth recording, or non-code aspects — hand off to `/postmortem` (`$postmortem`). This Phase 6 note is the one-line version, not that.
