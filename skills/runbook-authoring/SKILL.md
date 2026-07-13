---
name: runbook-authoring
description: "Use when turning a known operational procedure into a durable, repeatable runbook — deploy, rollback, restart, credential rotation, failover, alert response — that a non-author operator re-runs, sometimes under incident pressure; it finds the irreversible steps first and guards them proportionally. Not for a one-time build plan for new code (implementation-planning), a retrospective on an incident that already happened (postmortem), or hunting an unknown cause (diagnose)."
---

# Runbook Authoring

Turn a *known* operational procedure into a durable, repeatable runbook: the document an operator who did not write it follows to carry out a routine-but-consequential operation — deploy, rollback, restart, credential rotation, failover, recover-from-a-known-failure, respond-to-a-known-alert — re-run many times, sometimes under incident pressure. Invocation: `/runbook-authoring` or `$runbook-authoring`.

This skill authors and maintains the document; it never runs the operation.

## What makes a runbook different

What separates a runbook from an ordered checklist or a one-time build plan is that some of its steps are *consequential and irreversible* — there is a point past which the operation cannot be cleanly undone. So the work is **hazard-first**: find the irreversible steps before writing anything, and build the document as *proportional* safety scaffolding around them. Reversible steps stay terse; irreversible steps carry the full guard. A document that lists commands but leaves its irreversible steps unfenced has been transcribed, not authored.

When most steps are irreversible (a production failover, a cutover), the guard *is* most of the document; that is correct, not bloat — proportionality buys terseness only when the dangerous core is small.

## Shape

One durable document, two zones.

**Header (terse, always present).** Operation name; the one-line trigger ("run this when…"); the nearest *do-not-run* boundary; the blast radius (the irreversible steps named up front, so a pressured operator sees the danger before the first command); preconditions to begin (access, environment, window, who to inform); the named escalation owner/role; and `Last validated: <date> against <env>` — or `never run as written` when it has not been exercised.

**Body — the numbered procedure.** Each step is one of two kinds.

- *Reversible step* — terse: the exact copy-pasteable command and the one observable signal it worked.
- *Irreversible step* — guarded:
  1. **Preflight** — the checks that must hold first, each with its confirming command and observable. "Do not proceed unless X."
  2. **Action** — the exact command (secrets referenced by store/variable name, never inlined).
  3. **Reversibility** — how recoverable this step is *and how that recoverability degrades*: clean rollback, lossy-but-available recovery (with its cost), or forward-only past this point. Real operations degrade in stages and one procedure can hold more than one point of no return — name each, never assume a single one.
  4. **Verify** — the check that the action did what it should, with its expected observable, carrying an inline state tag *on that line*: `verified <date>/<env>`, or `UNVERIFIED — <why>` (e.g. `prod-only`). The tag rides the step, because that is where a pressured operator reads it.
  5. **Failure path** — before clean recovery is lost: the concrete reverse procedure. Past that point: never a reverse presented as if state were cleanly recoverable — instead the lossy recovery with its exact cost, or forward-recovery plus "escalate to `<owner>`." "No clean rollback; escalate and do Y" is a complete answer, not an empty one.

Labeled phases (preflight / execute / verify / rollback as sections) appear only when size warrants; a three-step restart stays flat. The failure branch is first-class — the operator often reaches for a runbook precisely because something already went wrong.

## Firm rules

- Every step judged irreversible carries the guard, and its failure path never presents a reverse as clean past the point at which clean recovery is lost.
- Every verify / expected-output line carries an inline `verified` / `UNVERIFIED` tag, and the header `Last validated` reflects the true aggregate — never a stamp for a run that did not happen.
- No fabricated output: an expected result not actually observed is tagged `UNVERIFIED`, never guessed and shown as real (the global evidence-before-claims floor, applied to operational docs).
- No inlined secrets or credentials, in examples too — referenced by store / variable name only.
- The runbook names an escalation owner / role. Unowned is unfinished.

## Judgment (provoke, never template)

- **Which steps are irreversible, and how reversibility degrades** — the core call, surfaced per step as a forcing question: *if this runs and is wrong, can the operator cleanly undo it? Partly, at a cost? Not at all?* Never a classifier the skill answers for them.
- **What you can exercise against** — assessed *before* writing, so the tags and header are honest from the start: state up front whether this was a real validation pass or a labeling pass. The prod-only operations this skill most serves usually land mostly `UNVERIFIED`; that is the honest default, not a failure.
- How terse a reversible step can be while the operator stays certain it worked; whether size warrants labeled phases; which mechanical, error-prone subsequences are worth a one-line automation-candidate note for a future maintainer (flag only — never scored, never built here).

## Fences

- **vs `implementation-planning` (sharpest).** Both are ordered, executable steps. The line is lifecycle plus irreversibility: implementation-planning builds something *new* once for a context-free executor, is consumed on success, and carries no trigger, no point of no return, no rollback, no freshness stamp; a runbook operates something that *already exists* on live state, re-run by non-authors, defined by exactly those markers. *Build a thing once → implementation-planning; operate a thing repeatedly → runbook-authoring.*
- **vs `execute-plan`.** That skill *runs* a plan; this authors the procedure and never executes the operation.
- **vs `postmortem`.** A backward-looking record of an incident that happened; it may *emit* "write a runbook for X" as an action item that feeds here. Different deliverable, opposite time direction.
- **vs `diagnose`.** It hunts an *unknown* cause; a runbook encodes a *known* response. Unknown cause → `diagnose` first; the stabilized result may then be authored here.
- **vs `research-capture` / `migration-campaign`.** Findings, not a procedure → `research-capture`. A tracked one-off change driven across many sites → `migration-campaign`; a runbook is the standing procedure, not the campaign.

## Artifact and lifecycle

- Write to `docs/runbooks/<operation-slug>.md` — keyed by operation, **not** dated in the filename: a runbook is a living document revised in place, and freshness lives in the `Last validated` header (the deliberate divergence from `postmortem`'s dated snapshot, because a stale runbook for a consequential operation is actively dangerous). Create `docs/runbooks/` if absent; defer to a runbook home set in the project's `AGENTS.md or CLAUDE.md` if one exists.
- Before writing, if the project is a git repo, run `git status`; if the path or its parent carries unrelated dirty state, surface that rather than write over it. Leave the artifact **uncommitted** for the user. Never commit on a protected or default branch; landing is deferred to `git-cycle`, done-ness to `closeout-check` — do not re-inline that apparatus.
- Re-run is the maintenance path and is non-destructive: same operation, file clean → revise in place, re-exercise where possible, refresh `Last validated` and the per-step tags. New operation → create. File dirty, hand-edited, or a slug collision with a *different* operation → ask one path question; do not ask on a clean re-validate.
- Report the artifact path, the irreversible steps guarded, the verification status, and the proof boundary: **authoring proves the procedure is written and honestly tagged — not that it has been run against production or that its commands work.** Validating that a runbook actually runs is a separate operational act this skill does not perform and must not claim.
