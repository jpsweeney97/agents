---
title: "Cognitive-Offload Metric — Evaluation (not constructible → stays a lens) + tail-guard lens-pass"
date: 2026-06-25
type: evaluation
project: agents
method: "25-agent multi-agent workflow wf_584147a4-446 / task wgjdh65vi (6 design arms × 3 adversarial verify lenses + synthesis)"
status: COMPLETE
---

# Cognitive-Offload Metric — Evaluation + Tail-Guard Lens-Pass

Evidence at a point in time, not authority. This resolves the open frontier question "can a skill's cognitive-offload value be measured by a real metric?" and applies the result to the deferred tail-guard weigh (the 6 MODEL-HANDLED guards left default-to-KEEP by Era 32).

## Bottom line

- **Do not build a cognitive-offload metric.** "Argued, not measured" is the correct resting place; carry the value as the lens already single-sourced in `skills/agent-facing-design/SKILL.md` ("Two Kinds of Skill") and the honest-limit in `docs/agents/contract-evaluation-methodology.md`.
- **Why it cannot be measured:** cognitive-offload value lives in *the prompt the user never had to type* — a property of the invocation interface, orthogonal to whether the model's output changes. Every metric scores output, so each one either re-measures *reliability* (already covered by the cross-model kit and `skill-benchmark`) or reads a confident *false null* on exactly the MODEL-HANDLED skills it would adjudicate (a strong model run on a terse "busy-user" prompt reconstructs the procedure it already knows, so the differential vanishes).
- **Applied result (lens-pass, judgment not score):** all 8 contested tail-guards are now KEEP-disposed. The deferred cognitive-offload weigh is discharged. No skill behavior changed; no cuts.

## The question, and why it was open

Eras 30–31 (the cross-model confound-break kit) measured *reliability* — does a skill's content change what a context-free `gpt-5.5` actor does on one scored hazard. Era 32 then added the **cognitive-offload axis** as analysis: an invoked skill is also a reusable, high-quality prompt summoned by a token, so MODEL-HANDLED ≠ delete-able. That reframe was explicitly "argued, not measured." It left the 6 MODEL-HANDLED guards default-to-KEEP pending a cognitive-offload weigh, and put "build a real cognitive-offload metric" on the frontier as an open option. This evaluation answers whether that metric is worth building.

## The evaluation

Method: a 25-agent workflow — 6 genuinely different operationalizations, each developing the best version of its lens and judging it honestly, then each stress-tested by 3 adversarial verifiers on distinct lenses (circularity/control-validity, charter/premature-bar, redundancy/decision-value), then one synthesis. Prose returns throughout (no StructuredOutput binding — the Era-24 lesson).

Verdict matrix (FATAL = a kill the arm did not survive; FIXABLE = survivable with a named fix; SURVIVES = the lens found no fatal flaw):

| Arm | Circularity / control | Charter / premature-bar | Redundancy / decision-value |
|---|---|---|---|
| Compression / information-leverage | FATAL | FATAL | FATAL |
| Beats-improvised (direct Era-32 framing) | FATAL | FIXABLE | FATAL |
| Completeness-variance / consistency | FATAL | FATAL | FATAL |
| Human-preference anchor | FATAL | FIXABLE | FATAL |
| Decision-model / cost-theoretic | FIXABLE | FIXABLE | FATAL |
| Skeptic-null (build nothing, keep the lens) | FIXABLE | FIXABLE | **SURVIVES** |

Every *build* arm took at least one FATAL; the only arm with none builds nothing, and even its two FIXABLEs were "trim the proposed cheap pilot down until it is just lens-application."

Cross-cutting findings:

- **The control collapses in every build proposal.** Offload's payload is orthogonal to the output differential, so each metric either re-measures reliability (where the kit and `skill-benchmark` already fire) or reads a false null on the exact 6 it must adjudicate. The methodology already says this verbatim: "neither arm is the real-world baseline."
- **The busy-user control is constructible but useless for offload.** The repo owns a cheap non-circular improviser (the cross-model `gpt-5.5` actor), but a strong improviser reconstructs the procedure (false null) and a weak one is just measuring reliability again. The bottleneck is not building the control; it is that offload lives outside any output differential.
- **"Fires-at-the-right-moment" is already owned** by `skill-benchmark`'s trigger/description arm — pricing it again is the R11 drift hazard. The only unowned residue is spared-composition labor (real but small, ≈ proportional to skill length, i.e. the gameable compression measure).
- **Pilot-before-seal settles the decision.** The metric's falsification channel is "is the doubly-low cell occupied — any skill low on offload AND reliability-moot?" The cheap pilot is to judge the open guards with the lens; they are all multi-step guardrailed procedures, so the cell reads empty, and an empty pilot closes the question with no sealed run (exactly how the test-5 leniency arm closed). The pilot's only cheap, non-circular form *is* lens-application.

Two implications worth recording:

- **This is the 4th time measurement was the wrong tool for a judgment.** Era 4 (trust-class bar), Era 11 (observed-friction bar), Era 19 (observed-fire gate) — each tried to mechanize a judgment and found the judgment was the right instrument. A cognitive-offload metric is the same temptation in a new costume; "don't build it" is the *predictable* result given the repo's scar tissue, now established by adversarial construction rather than asserted.
- **A metric would invert the concept's purpose.** Cognitive-offload was introduced to *resist over-cutting* (MODEL-HANDLED ≠ delete-able). The only decision a metric flips is "cut a skill that scores low on offload" — turning a brake on cutting into an accelerator for it. That is why every redundancy/decision-value verdict came back FATAL.

## The lens-pass (immediate application)

Discipline: judgment in the moment, one-line prose reason per guard, **no score, no threshold, no reusable per-skill scalar**. This is "infer the bar from what the skill does, apply it, move on" (`agent-facing-design`), captured as dated evidence — *not* installed as a rubric or a standing classification. The eval predicted no doubly-low skill; this pass verifies that by reasoning per guard, including the margin case, rather than assuming it. The discriminating question per guard: does it encode a verify/analysis step the hurried improvisation would drop (KEEP), or restate something the user would type in five seconds (cut candidate)?

The 5 still-open MODEL-HANDLED guards — all **KEEP**:

- **`load-handoff`** — `/load` expands into deterministic newest-branch-matching selection + a live git-reality check + throughline-staleness reconciliation + a fixed resume shape; the improvisation reads the file and skips the live-state check (the verify-claim-before-build hazard). High compression.
- **`git-hygiene`** — expands into a categorize→preview→confirm→clean audit across untracked/mixed/stale-branch state; the improvisation runs an ad-hoc `git clean`/`branch -d` and drops the preview-before-delete guard. High compression.
- **`closeout-check`** — "are we done?" expands into evidence-gather → run the proving command → completeness check → local commit; the improvisation asserts done from memory (the assert-done-without-evidence hazard itself). High compression.
- **`contract-change-propagation`** — expands into delta-classification (breaking/additive/preserving) + consumer enumeration + rollout/deprecation sequencing; the improvisation greps once and misses consumers (the grep-blindness axis). Also the weakest MODEL-HANDLED evidence in the set (a soft-hazard annex, qualitative) — least safe to call reliability-moot, an independent reason to keep.
- **`exiting-worktrees`** — closest to the margin: the lowest-compression of the five, since "remove the worktree" is near-improvisable. KEEP anyway, because the skill guarantees the verify-landed + confirm-before-destroy step a hurried `git worktree remove` drops (the destroy-before-verify hazard), plus weak-model coverage and sole ownership of the worktree-exit lane. The guaranteed-good-behavior-every-time is exactly the consistency value the lens credits.

Already-resolved, recorded for completeness:

- **`merge-branch`** — disposition resolved earlier this arc (Era 33): FIXED, not a pending weigh. Its MODEL-HANDLED + counterproductive-on-staleness finding resolved to a pure-local read-only base-freshness check (git-cycle 1.2.2), restoring the suppressed guard while keeping the local/no-fetch contract.
- **`release-cut`, `gh-address-comments`** — KEEP stands on *certified* reliability (gap 1.00, controls valid). The offload axis bears only on the optional re-medium-to-code: a code path must orchestrate the full run, or the skill stays as the invocable front end to it — so codifying the gate does not discard the summon-the-procedure value.

Net: 8/8 tail-guards KEEP, by three routes — 2 certified load-bearing, 5 model-handled-but-offload-positive, 1 fixed. No cuts.

## What this evaluation does not settle

- **n=1 user.** Offload value is defined against one person's habits; there is no population to sample, and "more subjects" is a category error. The idiosyncrasy is correct, not a defect.
- **n=1 model** on the reliability side. MODEL-HANDLED is a verdict about one off-model actor (`gpt-5.5`) on one task set; a weaker model or different distribution could move a guard back to LOAD-BEARING, so the 5's reliability-moot status is not permanent.
- **Do-no-harm is easier than does-good.** The evaluation shows decisively that a metric *does harm* (false-null, redundancy, ossification); it cannot prove the lens *does positive good*. The offload value is carried (argued), not positively measured — the methodology's own stated asymmetry, accepted not closed.
- **Circularity is fully escaped only by the human arm** — n=1, expensive, and here contaminated, since the user authored the procedures whose offload is in question.

## Status

Analysis/evidence only. No skill behavior changed; no cuts; no charter event (a `docs/plans` evidence artifact). No `AGENTS.md` line added — consistent with Era 32's own decision: the lens already lives in `agent-facing-design` and the methodology, an `AGENTS.md` line would duplicate the owned distinction (the R11 drift hazard), and it is a gated event with no observed-friction evidence (the 3× premature-bar anti-pattern). The lens-pass dispositions are evidence at this date, not a standing classification; a future cut still goes through build-and-prune ("watch it fire, trash it"), never through a number derived here.

## References

- Eval workflow: run `wf_584147a4-446`, task `wgjdh65vi` (script persisted under the session workflows dir).
- Source framing: `skills/agent-facing-design/SKILL.md` ("Two Kinds of Skill"); `docs/agents/contract-evaluation-methodology.md` (the cognitive-offload honest-limit + pilot-before-seal).
- Already-owned apparatus: `skills-claude/skill-benchmark/SKILL.md` (trigger/description optimization = "fires-at-right-moment"; performance delta = the built-ins-only reliability differential).
- Reliability arm: `docs/plans/2026-06-24-cross-model-tail-guard-results.md` (the 8-guard verdict table) and `docs/plans/2026-06-24-cross-model-tail-guard-kit.md` (sealed at `695fc55`).
- Premature-bar history: Eras 4 / 11 / 19 (project throughline).
