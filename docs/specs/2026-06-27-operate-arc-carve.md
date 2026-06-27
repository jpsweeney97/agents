---
type: design-spec
created: 2026-06-27
status: settled — builds in progress
source: Phase-0 carve-discovery Workflow (run wf_0f0753c3-b42, 19 agents) + docs/reviews/2026-06-26-skill-library-capability-growth-review.md (§5, item 4)
---

# The OPERATE arc — settled carve

The settled design for the library's missing **operate-after-push** lane, produced design-first as one system before any skill is authored. This is the reference the per-skill builds consume.

## Provenance and honest margin

Derived by a `skill-squad`-rig carve discovery: a blind careful-default control ensemble vs four genuinely-incompatible carves (four-atomic / one-lifecycle / cognitive-job / aggressive-fold), `scrutinize-skill` adversarial kills, then a swapped blind head-to-head (two judges, A/B flipped) + a validity critic.

Outcome: a **reliable, position-controlled BEAT** over the blind control (both swapped judges picked the crown; no position confound; validity `marginReliable: true`) — but **same-shape and thin**: the careful default independently reached the same three-skill carve, so the win is execution discipline, not a different shape. The structural correction (four candidates → three) came from the **adversarial kills and the crown re-kill**, not the head-to-head.

What this is NOT: behavior-validated. The carve and its per-skill briefs are design judgments; none has fired on un-prompted real work. All three skills are portable and **first-to-prune locally** (they fire in ops/product repos, not in this authoring repo).

## The discovery — four candidates collapse to three

The 2026-06-26 review proposed four new skills (`incident-response`, `post-deploy-verification`, `outcome-verification`, `deploy-plan`). The carve collapses them to **three**: `post-deploy-verification` is **not a standalone skill** — it folds into `deploy-plan` as the gauge-read, because *a go/no-go gauge you cannot read is not a gauge; reading the gauge through the bake is constitutive of owning it.* Plan + watch are one job. Only the *goal* altitude (`outcome-check`) is genuinely unowned.

The carve adds **three new skills, zero existing-skill expansions, three one-line inbound routes.** All live in `skills/` (portable, dual-runtime); names dodge both runtimes' bundled sets.

## Per skill — trigger, owned job, One-Owner fence, confidence

### `deploy-plan` — *promising-experiment* (thin; first-to-prune)

- **Trigger.** A specific risky change is about to ship and needs a rollout decision — shape, go/no-go, abort criteria — pre-push.
- **Owns.** The one-time, this-change go/no-go gauge **end-to-end**: rollout shape (all-at-once / canary / staged / flag-gated); the go/no-go decision `release-cut` explicitly disclaims; the pre-registered abort thresholds + bake window + smallest signal set; **and** the post-push read of those very thresholds through the bake (reachability-gate the named signals, read where readable, render `healthy` / `abort` / `UNVERIFIED` against the pre-registered thresholds). Reuses `runbook-authoring`'s rollback machinery by reference (see Single-sourcing).
- **Fence.** vs `runbook-authoring` (sharpest): "Build a thing once → implementation-planning; operate a thing repeatedly → runbook-authoring" (`runbook-authoring:57`); `deploy-plan` is the build-once side of *deploy* — this push's go/no-go, consumed once. vs `release-cut`: that owns semver + CHANGELOG and "is not a release-readiness scorer — there is no go/no-go gauge" (`release-cut:70`); `deploy-plan` owns exactly the gauge `release-cut` refuses, touches neither version nor changelog.

### `outcome-check` — *promising-experiment* (heavily proof-bounded; first-to-prune)

- **Trigger.** A change has been in production a while and someone asks "did it actually achieve what it shipped for?" — the goal, not the health.
- **Owns.** The post-ship goal read: name the goal metric the change existed to move, reachability-gate it, read where readable, render `goal-met` / `not-moved` / `unverifiable-here` (days-to-weeks horizon). Closes `outcome-interviewer`'s loop. Consumes `acceptance-map`'s stable-ID checks as criteria and renders the verdict in its own output — no change to `acceptance-map`.
- **Fence.** vs `outcome-interviewer`: that *opens* the goal loop up front (read-only interview); `outcome-check` *closes* it — a verdict is not an interview. vs `implementation-review`: code-vs-spec; this asks "did the goal happen in the world." vs `acceptance-map`: before-implementation, statusless; `outcome-check` is the post-ship consumer of those IDs, weeks later, against the world. vs `closeout-check`: local-only (`closeout-check:19`); cannot ask "did the goal move in prod." vs built-in `verify`: pre-push, local.

### `incident-response` — *high-confidence* (the unanimous, genuinely-unowned survivor)

- **Trigger.** Prod is burning *now* — unplanned, cause possibly unknown.
- **Owns.** The live-fire moment: severity call, **mitigate-first** (stabilize before you understand), a timestamped live timeline kept as it happens, the rollback-vs-forward decision, comms cadence. **Hard fence: stop at "stabilized."** Does not hunt cause; does not retrospect.
- **Fence.** vs `diagnose`: that is loop-first/cause-first (`diagnose:51`) — the opposite reflex; `incident-response` mitigates before understanding and exits *into* diagnose once stabilized with cause unknown. vs `postmortem`: that refuses the burning moment (`postmortem:26`); `incident-response` owns it, and its live timeline becomes postmortem's Beat-1 facts. vs `runbook-authoring`: that authors and never runs (`runbook-authoring:10`); `incident-response` *follows* an existing rollback runbook under fire, advisory-to-operator, never re-authoring.

## Seams / wiring

- **The deploy → watch → outcome chain.** `release-cut` (stops at push, `release-cut:56`; disclaims go/no-go, `:70`) → *for a risky change* → `deploy-plan` (shape + go/no-go + pre-registered abort thresholds + bake window; rollback path in `runbook-authoring`'s graded-PONR vocabulary by reference) → **[human pushes]** → `deploy-plan`'s own bake-window read (`healthy` / `abort` / `UNVERIFIED`) → *healthy + a goal was named* → `outcome-check`.
- **The abort / incident path.** `deploy-plan`'s bake read → `abort` → execute the rollback → *if prod is actually harmed* → `incident-response`.
- **The incident exit.** `incident-response` → stop at *stabilized* → cause unknown → `diagnose` → durable record → `postmortem` (consumes the live timeline as Beat-1 facts).
- **postmortem tag-routing feeds back.** `postmortem` files prevention/detection/mitigation items (`postmortem:45`) to `/triage`: a detection gap → sharpen a `deploy-plan` signal; a mitigation gap → harden a rollback runbook (`runbook-authoring`) or add a `deploy-plan` abort criterion; a prevention gap → change the `deploy-plan` rollout shape or go upstream.
- **Inbound routes (one line each; no host fence broken).** `release-cut` at the push boundary → `deploy-plan` (availability-conditional; preserves `release-cut:64` "cutting a release is not deciding readiness"); `closeout-check` "Next Move" → `deploy-plan` / `outcome-check` (preserves local-only `:19`); `outcome-interviewer` handoff table → `outcome-check` (preserves its read-only up-front identity).

## Single-sourcing — one machinery, one owner, referenced (never forked)

Exactly **one** single-sourced machinery: **rollback / irreversibility / graded + multi-PONR reversibility**, owned by **`runbook-authoring`**. The reused asset is its **Irreversible-step guard** (SKILL.md "Shape" body): item 3 `Reversibility` (the graded ladder + multi-PONR rule, `runbook-authoring:35`); item 5 `Failure path` (the concrete reverse procedure, `:37`); and the Judgment bullet "which steps are irreversible, and how reversibility degrades" (`:51`).

`deploy-plan` **references** this to characterize its rollback path in that vocabulary, and routes to `runbook-authoring` to author a durable rollback procedure when warranted — never re-deriving, never copying. `incident-response` makes the rollback-vs-forward call in that same vocabulary by reference and **follows** an existing runbook under fire (`runbook-authoring:10` never-runs; it runs advisory-to-operator). Two referencing callers, one owner — the doctrine, not a fork.

## Shared proof-boundary law (the inherited floor — owned by none, obeyed by all)

The proof discipline is **not** a second machinery to single-source — that was the crown's fatal error the re-kill caught. It is the library-wide evidence-before-claims floor (named verbatim at `runbook-authoring:45`), specialized to the can't-read-prod surface exactly as `runbook-authoring` (`prod-only`), `closeout-check` (`not verified`), and `postmortem` (no-fabrication) already specialize it:

> An AI coding agent usually cannot read prod. So report only what you actually observed, reachability-gate the named signals first, read where readable, and where blind label the result `UNVERIFIED` / `unverifiable-here` with the exact signal a human must read — never a green stamp over a signal merely reached. And **advisory-not-actor**: advise the human operator; take no production action — no deploy, traffic shift, rollback execution, or paging.

No arc skill *owns* this floor; it is inherited, not machinery. There is no logic to fork.

## What got killed (the breadth)

- **The 4-skill split** (spine A): the verification *split* is killed. Health folds into `deploy-plan`'s gauge-read; outcome stands alone. The `acceptance-map`-status-field escape does not exist (its labels are source-provenance, not pass/fail; it runs before implementation).
- **The one-lifecycle monolith** (spine B): killed — collides with multiple owners, violates one-job; "watch one fire before granting it a skill, do not pre-build it inside a monolith."
- **The "two machineries, two owners" structure** (spine C / the naive crown): killed. Machinery #2 ("runtime prod-read proof discipline, owned by verify-in-prod") is the ambient floor relabeled as owned. The skill *count* survives the re-cut; its load-bearing *differentiator* is dead.
- **Spine D's expansions**: subtracted — `acceptance-map` status-field-plus-verify-mode (statusless, before-implementation by identity); `runbook-authoring` rollout-mode (violates build-once-vs-operate-repeatedly, `:57`).

## Build sequence and status

1. **`incident-response` → a per-skill `skill-squad` run** (highest-confidence, genuinely-unowned, real net-new machinery: severity ladder, live-timeline format, mitigate-first stop, rollback-vs-forward aid, comms, the clean hand-to-postmortem). *Status: shape-discovery Workflow in progress (run wf_f2328c41-d1d).*
2. **`deploy-plan` and `outcome-check` → hand-authored against this carve** (thin, first-to-prune, little net-new machinery; `deploy-plan` reuses `runbook-authoring` by reference, `outcome-check` is a narrow loop-closer). Validate with `quick_validate.py` + a `behavior-smoke-test` that the can't-read-prod → `UNVERIFIED` / `unverifiable-here` floor actually fires — the one behavior that must not regress.
3. **No shared-machinery build task.** Rollback machinery already exists (`runbook-authoring`); the proof floor already exists (ambient). Nothing new to single-source.

**Watch-item for the build:** `deploy-plan` fires at two moments (pre-push planning, post-push bake-read). The carve resolves the "pre-push skill doing a post-push action" worry via advisory-not-actor (it reads/advises, never executes). Watch whether the dual-moment trigger reads cleanly to the loader, and prune without ceremony if either thin skill never earns more than "read your own gauge" / "re-read the acceptance map weeks later."
