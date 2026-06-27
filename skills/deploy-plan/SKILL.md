---
name: deploy-plan
description: "Use when a specific risky change is about to ship and needs a rollout decision before push — rollout shape, an explicit go/no-go, pre-registered abort thresholds and a bake window — plus the post-push read of those thresholds to call the rollout healthy or aborting. Advisory only: it never executes a deploy, traffic shift, or rollback. Not for deriving a version or changelog (`release-cut`), authoring a reusable operational runbook (`runbook-authoring`), checking whether the goal later moved (`outcome-check`), or a live incident already burning (`incident-response`)."
---

# Deploy Plan

For a specific risky change about to ship: choose the rollout shape, set an explicit go/no-go with pre-registered abort criteria, and — after the human pushes — read those criteria to call the rollout healthy or aborting. Invocation: `/deploy-plan` or `$deploy-plan`.

This skill advises the operator and authors the go/no-go gauge; it never executes a deploy, traffic shift, or rollback.

## The owned job

`deploy-plan` owns the **go/no-go gauge end-to-end** for one risky ship: set the gauge before push, read it after. `release-cut` stops at "push" and explicitly disclaims readiness ("not a release-readiness scorer — there is no go/no-go gauge", `release-cut:70`); `deploy-plan` owns exactly the gauge it refuses. The two moments are one job: owning the decision to abort without owning *how you read whether to abort* is an incomplete instrument — a gauge you cannot read is not a gauge.

## Mixed skill — apply the bar per part

- **Firm (trust).** The pre-registration discipline (the abort thresholds, bake window, and smallest signal set are fixed *before* push and never moved after seeing the data); the bake-read verdict shape (`healthy` / `abort` / `UNVERIFIED` against the pre-registered thresholds); and the proof-law (advisory-not-actor; can't-read-prod → `UNVERIFIED`). A missing threshold, or one moved post-hoc to fit the data, is a defect — the value is that the gauge is honest.
- **Provoked (judgment).** The rollout shape, what the thresholds should be, which signals are the smallest sufficient set, and the go/no-go call itself. The skill poses these as forcing questions; it never answers them for the operator and never hardens into a template filled to feel done.

## Shape — two moments, one gauge

**Before push — set the gauge.**

- **Rollout shape** — choose and justify: all-at-once / canary (with % steps) / staged / flag-gated. The forcing question: *what is the smallest blast radius that still ships this?*
- **Rollback path** — characterize how this change is undone and how cleanly, in `runbook-authoring`'s graded / multi-PONR vocabulary **by reference**: clean rollback, lossy-but-available recovery (with its cost), or forward-only past a point — and name each point of no return, never assume one (`runbook-authoring:35,37,51`). When a durable rollback procedure is warranted, route to `runbook-authoring` to author it; never re-derive or copy the taxonomy.
- **Pre-register the gauge** — fix, before push: the **smallest signal set** that would reveal this change is failing; the **abort threshold** per signal (the value that means "roll back, do not wait"); and the **bake window** (how long to watch before calling it). Write the thresholds down now; do not move them once the data is in.
- **Go/no-go** — state it explicitly: GO (with the gauge above), or NO-GO (and what must change first).

**After push — read the gauge (advisory).**

- **Reachability-gate first** — can you actually read each pre-registered signal from here? Read where readable.
- **Verdict against the pre-registered thresholds** — `healthy` (within thresholds through the bake window), `abort` (a threshold breached → recommend the rollback path), or `UNVERIFIED` (the signal is unreadable from here → name the exact signal a human must read). Never a green stamp over a signal merely reached for.
- **Advisory-not-actor** — recommend; the operator executes. On `abort`, point at the characterized rollback path; if prod is actually harmed, route to `incident-response`.

## Proof boundary (the inherited floor)

An AI agent usually cannot read prod. Report only what you actually observed; reachability-gate the named signals first; read where readable; where blind, label `UNVERIFIED` with the exact signal a human must read — never a green stamp over a signal merely reached. Advisory-not-actor: advise the operator; take no production action (no deploy, traffic shift, rollback execution, or paging). This is the library-wide evidence-before-claims floor (`runbook-authoring:45`), specialized to the can't-read-prod surface; the skill obeys it, it does not own it.

## Persistence

The gauge is pre-registered before push and read after — sometimes in a later session. When the push boundary spans sessions, persist the gauge (rollout shape, signals, thresholds, bake window, rollback characterization) to a short note so the post-push read checks the same thresholds it set; otherwise state it inline. The durable thing is the pre-registered values, not a format — do not invent a schema.

## Fences

- **vs `release-cut`.** It derives semver + CHANGELOG and disclaims go/no-go (`release-cut:70`); `deploy-plan` owns exactly the gauge it refuses and touches neither version nor changelog.
- **vs `runbook-authoring` (sharpest).** "Build a thing once → implementation-planning; operate a thing repeatedly → runbook-authoring" (`runbook-authoring:57`). `deploy-plan` is the build-once side of *deploy* — this push's go/no-go, consumed once. It reuses runbook-authoring's rollback vocabulary by reference and routes to it to author a durable runbook; it never re-authors and never runs the operation.
- **vs `outcome-check`.** `deploy-plan` watches technical **health** through the bake (minutes-to-hours); `outcome-check` asks whether the **goal** moved (days-to-weeks). Different signal, different horizon.
- **vs `incident-response`.** `deploy-plan` is the planned, pre-push gauge and its bake-read; `incident-response` is the unplanned live-fire moment. An abort that harms prod hands off to it.
- **vs `verify` / `behavior-smoke-test`.** Pre-push/local, and a contract proxy, respectively; `deploy-plan` is the post-push production gauge.

## Done when

- A rollout shape is chosen and justified, and the rollback path is characterized in runbook-authoring's vocabulary by reference.
- The gauge is pre-registered: the smallest signal set, a per-signal abort threshold, and a bake window — fixed before push.
- An explicit go/no-go is stated; and (post-push) the bake-read renders `healthy` / `abort` / `UNVERIFIED` against the pre-registered thresholds, advisory-only, naming any signal a human must read.

## Build-and-prune note

Thin and **first-to-prune** — risky ships are rare in this authoring repo; the value is **portable** to ops/product repos. Watch it fire on a real risky ship; prune without ceremony if it never earns more than "read your own gauge."
