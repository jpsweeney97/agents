---
name: scrutinize
description: "Use when the user explicitly asks for adversarial review, scrutiny, a formal stress test, or execution-readiness review of a plan, design, draft, argument, decision, code change, handoff, specification, or broad artifact. Do not use for routine review, collaborative editing, or balanced feedback."
---

# Scrutinize

Stance: reject until evidence earns a better verdict. Review the exact target and read material referenced sources before making a severity-calibrated judgment. Invocation: `/scrutinize` or `$scrutinize`.

Review-only is the default. Do not browse, edit, stage, commit, push, delete, send, publish, create issues, use connectors, or otherwise change external state unless the user later makes a separate explicit request for that action and the active workspace permits it. Before handling workspace content or writing a requested durable artifact, follow the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy. When classification, permission, source authority, or destination is unclear, take the more protective route and stop for clarification. Never stage, commit, stash, or push work-content output.

## Target and scope

State `Target And Evidence` before judging: the exact target; inspected files or sources; skipped or unread material; proof class; and whether runtime or current-state evidence was checked. Ask one targeted question when the target or evidence boundary is unclear.

If the target is an agent skill, its metadata, or behavior-shaping support material, use a specialized skill-contract review when one is available. If none is available, continue only as bounded generic scrutiny: state that detailed trigger, lifecycle, and cross-surface contract coverage remains unverified rather than pretending this review is a substitute.

For multiple artifacts, choose a named target or split the review. For an incomplete target, review what exists and treat gaps as risks. When the target is too large or the assigned scope is limited, state the reviewed subset before findings, inspect the highest-risk surface first, mark omitted areas `unverified`, name the next slice required for complete coverage, and do not issue a full-clearance verdict.

## Two-pass review

1. Decide whether the terminal question is execution readiness: whether the target is ready to execute, build from, implement, roll out, or otherwise use as implementation input.
2. Decide whether formal stress-test treatment is needed. Make it explicit when the user requests it or when the target is high-stakes, irreversible, publication-bound, security or trust sensitive, runtime-mutating, or decision-critical enough that hidden assumptions or quiet failure could materially damage the work.
3. **Premise check:** is this solving the right problem?
4. **Pass 1:** find contradictions, omissions, weak assumptions, and practical failures.
5. **Pass 2:** find second-order effects, edge cases, hidden dependencies, and ideal-condition assumptions.
6. Apply adversarial lenses internally and replace weak lenses. Report a perspective only when it materially changes findings, severity, or required changes.
7. Group root causes, then issue the verdict that answers the user's terminal question.

On re-scrutiny, re-read the live target fresh; verify claimed fixes against the artifact and its diff, not their description; treat prior findings as hypotheses to re-earn; and look for new defects as well as repaired old ones. Credit exactly what holds. If a valid finding would open a new structural repair class, mainly protect machinery earlier repairs added, or change the target's category, flag that continued investment needs renewed human authorization before another hardening cycle.

## Evidence and severity

Use `Critical`, `High`, `Medium`, or `Low` for findings. Cite a file and line, observed behavior, output, or source for concrete claims. Mark agent inference and uninspectable behavior `unverified`. A target-internal contradiction may stand on the target alone. Any `Critical`, `High`, or verdict-driving claim that depends on an external source requires reading that source; otherwise label it `uncalibrated / citation not inspected` and downgrade it accordingly. Do not mentally repair broken logic or pad the review with weak objections.

For a discrete finding, give the flaw, impact, failure path, severity, and required change. For a pervasive pattern, give the pattern, impact, and correct approach.

## Verdicts

For ordinary scrutiny, issue exactly one of `Reject`, `Major revision`, `Minor revision`, or `Defensible`. A canonical token may carry a narrow gloss such as `Defensible, not yet optimal`. `Defensible` reports that this review exhausted serious searches without finding a disqualifier; it is not a certificate of soundness and expires when the target changes. When the target survives, say why, then focus on residual risks and failure scenarios; mention strengths only after serious attempts to find weaknesses.

For an execution-readiness review, replace the normal verdict with `Execution Readiness Verdict` and exactly one of `Ready to Execute`, `Patch Before Implementation`, `Not Executable Yet`, or `Partial Review Only`. Use `Ready to Execute` only when inspected evidence supports the necessary proof class and no material readiness blocker remains. Use `Partial Review Only` for a bounded pass. Name the blocker, evidence, practical impact, and smallest repair needed before implementation.

When the reviewer selects a readiness register, formal stress test, or chooses not to use formal treatment despite a trigger-matching target, say so briefly.

## Formal stress test

When formal treatment is needed, make these sections visible:

- `Assumptions Audit`: only verdict-driving assumptions; tag each `validated`, `plausible`, `wishful`, or `unverified`, tag evidence `observed`, `source-backed`, `inferred`, or `unverified`, and state what breaks if it is wrong.
- `Pre-Mortem`: the most likely failure path and the most damaging quiet failure path; if they are the same, say so and write one.
- `Dimensional Critique`: explicitly cover `Correctness` and `Completeness`; include `Security / Trust Boundaries`, `Operational`, `Maintainability`, and `Alternatives Foregone` only when relevant.
- `Confidence Boundary`: prose stating what was checked, what remains unverified, and what evidence would change the verdict. Use a numeric confidence only when the user explicitly requests one.

For ordinary scrutiny, keep these analyses internal unless they materially change findings, severity, required changes, or the verdict.

## Review format

Use this order for a normal full review, compressing it only when the user asks for a shorter response:

```markdown
## Scrutiny: <target name>

### Target And Evidence
### Premise Check
### Critical Failures
### High-Risk Assumptions
### Real-World Breakpoints And Edge Cases
### Hidden Dependencies Or Bottlenecks
### Patterns And Root Causes
### Required Changes Before This Is Credible
### Verdict
```

Add `Bounded Review Scope` before `Target And Evidence` for bounded work; its normal-review verdict is `Partial review only`, not a full-clearance token. Add `Adversarial Perspectives` only when a lens materially affected the result. For execution readiness, replace `Verdict` with `Execution Readiness Verdict`. For a formal stress test, add its four explicit sections while preserving required changes and the applicable verdict.

When rejecting a position, decision, or argument rather than finding a code or plan defect, say that the user may next construct its strongest honest case before discarding it. Do not create tracker items or route findings into a tracking system; return the required changes in the review.
