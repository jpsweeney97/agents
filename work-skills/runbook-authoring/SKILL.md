---
name: runbook-authoring
description: "Use when turning a known consequential recurring procedure into a durable, repeatable runbook for an operator who did not author it. It finds irreversible steps first, guards them proportionally, and authors but never executes the procedure. Not for a one-time build plan, an incident retrospective, or diagnosing an unknown cause."
---

# Runbook Authoring

Turn a known recurring operational procedure into a runbook that another operator can follow under ordinary or incident pressure. Invocation: `/runbook-authoring` or `$runbook-authoring`.

This skill authors or revises the runbook; it never runs the operation. Before handling workspace content or writing a durable artifact, read the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy. When data classification, permission, execution authority, or a destination is unclear, take the more protective path and stop for clarification. A runbook request does not authorize browsing, connector access, installation, sending, publication, tracker mutation, or execution of any procedure step. Never inline credentials or secrets. Never stage, commit, stash, or push work-content output.

## Hazard first

Find consequential and irreversible steps before drafting anything. Ask for each step: if it runs and is wrong, can an operator cleanly undo it, partly recover at a stated cost, or only move forward? Build proportional safeguards around the answer. Reversible steps stay concise; irreversible steps receive the full guard. A procedure that lists actions but leaves its points of no return unfenced is not a complete runbook.

## Draft shape

Start with a terse header containing:

- operation name and one-line trigger;
- the nearest do-not-run boundary;
- blast radius and the irreversible steps named before the procedure;
- preconditions: access, environment, change window, and people or roles to inform;
- escalation owner or role; and
- `Last validated: <date> against <environment>`, or `never run as written`.

Use only an escalation owner or role established by the user-scoped procedure sources; otherwise write `Owner needed`. Keep a concise source pointer for any asserted owner, number, deadline, consequential action, or recovery claim.

Then write a numbered procedure using exact executable actions. A command is appropriate only when the correct action is a command; otherwise give the exact interface action, decision, or communication required. For every action, state the observable result that shows it worked. Do not invent expected output: pair an observed result with `Evidence: <source or check>`, and mark anything not actually observed `UNVERIFIED — <why>`.

For a reversible step, give the exact action and one observable success signal.

For an irreversible step, provide:

1. **Preflight:** each required condition, the exact check, and the observable that confirms it. State “Do not proceed unless…” where it is a true stop condition.
2. **Action:** the exact executable action. Reference a secret store or variable name rather than inlining a secret.
3. **Reversibility:** whether recovery is clean, lossy with its explicit cost, or forward-only; name every point where recovery degrades.
4. **Verify:** the exact check and expected observable, with an inline `verified <date>/<environment>; Evidence: <source or check>` or `UNVERIFIED — <why>` tag on that line.
5. **Failure path:** the concrete reverse procedure before clean recovery is lost. Past that point, give the exact lossy or forward-recovery action and escalation; never describe a clean rollback that is no longer possible.

Use labeled phases only when they improve a larger runbook. Keep a short procedure flat. Make the failure branch first-class: operators often open a runbook because the normal path has already failed.

## Required judgment

- Identify every irreversible step and how its recoverability degrades.
- Decide before drafting whether any real validation can occur. State whether this is a real validation pass or a labeling pass; a production-only procedure will often remain mostly `UNVERIFIED`, which is honest rather than deficient.
- Keep reversible actions as short as certainty permits, and flag a mechanical error-prone subsequence as an automation candidate only when useful. Do not build automation here.

The runbook is incomplete without a named escalation owner or role. Its header and every verification line must state only what was actually validated.

## Boundaries

Use this method for a known, repeatable operation on existing state. A one-time build plan, an incident retrospective, or investigation of an unknown cause needs a different method; stabilize an unknown response before documenting it as a runbook.

Return the draft in chat by default. Write a durable artifact only when the user explicitly requests it and the active workspace permits the chosen destination. On an explicit durable request, confirm the operation identity and destination, preserve an existing clean runbook through an in-place revision when appropriate, and stop for a hand-edited file or collision with a different operation rather than overwriting it. Authoring proves only that the procedure is written and honestly tagged; it does not prove that the operation, commands, or recovery path have run successfully in a real environment.
