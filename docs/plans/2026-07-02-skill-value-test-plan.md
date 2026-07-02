---
type: plan
created: 2026-07-02
status: designed, banked, NOT RUN — pre-register (seal exact prompts, sample, judges, and thresholds) before the first trial; this document is the design note, not the pre-registration
source: commissioned by the 2026-07-02 framework challenge (docs/reviews/2026-07-02-framework-challenge.md, change-set item 2); method per docs/agents/contract-evaluation-methodology.md
---

# Skill value test — design note

The first experiment that measures skill VALUE rather than obedience (forward tests), design convergence (squad controls), or coherence (consistency audits). Question: **on messy, realistic prompts, does routing through a skill change output quality or discipline-consistency relative to the bare model — and by how much, with what variance?**

## Why this test exists

The framework challenge adjudicated that no prior experiment measured live value, and that the instrument already existed: `skill-benchmark` (Claude-only; with/without-skill eval runs, pass-rate/token/time deltas with variance across repeated trials) was built in Era 12 and never pointed at the value question. The defense of the library (cognitive-offload, value-in-variance) predicts a specific measurable signature; this test checks for it.

## Design

- **Sample (3–5 skills, fixed at pre-registration):** one cross-model-certified keeper as positive control (`release-cut` or `gh-address-comments` — if the test cannot detect value here, the test is broken, not the skill); one high-traffic judgment skill (`making-recommendations` or `diagnose`); one zero-fire tail skill from the Era-36–58 wave (e.g. `migration-safety` or `regex-craft` — footgun-dense, so discipline is checkable); optionally `scope-cut` (VIABLE/first-to-prune verdict strength, the honest marginal case).
- **Arms:** (A) bare model, messy prompt only; (B) same prompt with the skill loaded/invoked. Same model, same effort tier, N ≥ 5 repetitions per arm per scenario.
- **Messy prompts, not briefs (the Era-50 threat, inverted):** the known failure is the test author pre-loading the control by distilling the skill into the prompt. Mitigations, all three: source scenarios from real past sessions (the handoff pile and transcript ledger name real asks) or realistic external task descriptions; have a fresh-context agent (no skill text in context) author the final prompt wording; ban the skill's own vocabulary from prompts (no "expand-contract," no "must/must-not table").
- **Measures:** (1) discipline-consistency — for each skill, pre-register the 3–5 load-bearing behaviors its value claim rests on (e.g. regex-craft: engine identified first, fix legality checked against engine, executed must/must-not table, backtracking probe run) and score presence per rep; the offload/variance theory predicts arm B pins behaviors arm A hits stochastically. (2) Blind output-quality grading — graders see paired outputs, arm-blinded and order-randomized. (3) Token/time cost per rep.
- **Judges:** blind grading by a model arm that has never seen this repo's vocabulary (the Antigravity third-model precedent, Eras 30–31) plus JP cold-grading a small subset (2–3 pairs) as the human anchor. Blinding discipline per AGENTS.md `## Blind Evaluations` — no apparatus state reaches any judge before their judgment is recorded.
- **Author-contamination bound:** this design was written by an agent steeped in the framework; the pre-registration step should have a fresh-context agent adversarially review the sealed prompts for kernel-preloading before any trial runs.

## Branch commitments (recorded before any data exists)

- **Skills materially pin discipline** (arm B consistency ≫ arm A across reps, positive control included): the reliability/variance defense is vindicated; forward tests remain a legitimate cheap proxy for future builds; the tail's value question narrows to routing (does it fire?) which the usage ledger already covers.
- **No consistency or quality delta on messy prompts** (including the positive control behaving no better): first check the test (positive-control failure means instrument failure); if the instrument is sound, the reliability story for the tested tier dies, the tail's defense collapses to revealed preference alone, and prune pressure rises accordingly.
- **Mixed** (positive control and judgment skill pin discipline; tail skill doesn't): the likeliest world — value concentrates where use concentrates; feeds the 2026-08-01 ledger re-read as converging evidence for tranche pruning of the tail.
- No post-hoc reframing: whichever branch the data lands in is reported in those terms in the results doc, alongside any honest surprises.

## Cost and when

Roughly 3 skills × 2 scenarios × 2 arms × 5 reps = ~60 headless runs plus grading — well under one Era-62-scale review. Run it when JP re-prioritizes the engineering lane, or earlier on ask; it pairs naturally with the 2026-08-01 ledger re-read so the prune deliberation gets both instruments at once. Results land as a dated doc in `docs/plans/` or `docs/reviews/`, and the pre-registration seals before the first trial.
