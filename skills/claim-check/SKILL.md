---
name: claim-check
description: "Use when the user asks to verify or falsify one concrete factual claim or a small related set about a project, file, test, runtime, count, or named deliverable using fresh evidence. Do not use for broad readiness, source-of-truth selection, source-to-derivative fidelity, implementation review, supplied-review adjudication, or a challenge to your own same-session claim."
---

# Claim Check

Test the exact project or artifact assertion the user named. Give a current, evidence-backed answer without turning a narrow question into a full review.

## Boundary

- Use for a concrete claim or small related set, not “is everything done?” or “review this implementation.” `closeout-check` owns local readiness, `implementation-review` owns completed work against requirements, `source-fidelity` owns source-to-derivative preservation, and `baseline` owns which source governs a claim when that is the central question.
- A supplied review as a review belongs to `review-reviewer` when explicitly invoked. A user challenge to a factual claim you made this session belongs to `hold-or-fold`.
- Verification only: do not edit source, stage, commit, fix failures, install dependencies, publish, or change external state. Focused safe tests or commands may produce normal temporary test or build artifacts when they are needed to check the claim. If the necessary check cannot be run within the current authority or access, leave that part unverified and name the missing check.

## Check

1. Restate the claim without strengthening it. Split compound claims when one part could be true and another false. Identify the target and time: default to current state unless the claim explicitly concerns an earlier snapshot. If the target or asserted behavior cannot be inferred precisely enough to test, ask one focused question.
2. Identify the easiest observation that would contradict each testable part before accepting supporting evidence. Inspect the smallest current evidence set that can settle it: the relevant file or diff, a focused command and its exit/output, an artifact count, live runtime state, or a read-only remote observation. Use current repo instructions and established authority; if the authority itself is disputed or undecidable, name the gap rather than silently choosing.
3. Read the result of every proving command. Prior test reports, handoffs, summaries, and another agent's verdict can locate evidence but do not prove a present-tense claim. A source or cache match does not prove runtime activation; a test pass does not prove an untested end-to-end behavior. For a historical claim, check its actual snapshot when available; present state alone cannot establish historical truth.
4. Compare the evidence with the claim's exact scope and consequence. Lack of evidence is not contradiction unless the inspected source is complete enough that the alleged item would have appeared. Do not upgrade a partially supported claim to a broader confirmation.

## Answer

Lead with `Confirmed`, `Contradicted`, `Partly supported`, or `Unverified` for the exact claim, using separate results for separable parts. Give the decisive evidence pointer and a short account of the falsification check. State the relevant snapshot or time and any missing access, unrun check, or narrower scope. Keep the answer brief when one observation settles it; stop without repairing or widening into a general audit.
