---
name: scrutinize
description: "Use when explicitly asked for adversarial review, a stress test, or execution-readiness review of a plan, design, draft, decision, or code. Not for agent skills, routine review, or balanced feedback."
---
<!-- export: plugins/review-family/skills/scrutinize/ @ 96479fc7f4d4da2d3925ee946490a70aa07796d4 | 2026-09-23 | claude.ai -->

# Scrutinize

Stance: reject until evidence earns a better verdict. Review the exact target; read referenced files before severity-calibrated judgment.

## Routing

A request that names this skill wins, but a generic adversarial request does not override target-type handoff to `scrutinize-skill`. This skill wins natural-language adversarial requests — "scrutinize", "be brutal", "tear this apart", "reject until proven otherwise" — and execution-readiness reviews, when no narrower target-type lane applies:

- Agent skill or skill-support target → `scrutinize-skill`, even when the user said "scrutinize" (target shapes listed in the Workflow).
- Completed code or an artifact against a plan/spec, an architecture or system-design lens, or adjudication of a supplied review or pasted claims: no dedicated skill for these is in this skill set, so review them here with this workflow and say in `Target And Evidence` that no dedicated lane was applied.
- Otherwise-wrong lane: name the better skill the user has available; if the user asked for this skill by name, ask one routing question.

## Workflow

1. State `Target And Evidence` before judging: exact target and the anchor the verdict binds to (a commit, version, or date the artifact carries — the datum by which a later reader can tell whether the artifact has changed; state when none is determinable, as for an unlabeled paste), inspected files or sources, skipped or unread material, proof class, and whether runtime or current-state evidence was checked. Ask one targeted question if the target or evidence boundary is unclear.
2. If the target is an agent skill, skill directory, `SKILL.md`, skill metadata file, skill reference, example, or proposed skill contract, use `scrutinize-skill` instead of this generic workflow. Do not ask whether the user wants the dedicated lane unless the target could reasonably be reviewed as something other than a skill behavior contract.
3. Decide whether the user's terminal question is execution readiness. Treat it as an execution-readiness review when the user asks whether the target is ready to execute, ready to build from, ready to implement, ready to roll out, or otherwise safe to use as implementation input.
4. Decide whether to make a formal stress test explicit. Use it when the user asks for a formal stress test, assumptions audit, pre-mortem, confidence check, confidence boundary, exhaustive adversarial packet, or equivalent heavier review; also use it when the target is high-stakes, irreversible, publication-bound, security/trust-sensitive, runtime-mutating, or decision-critical enough that hidden assumptions or quiet failure modes could materially damage the work.
5. Premise check: is this solving the right problem?
6. `Pass 1`: contradictions, omissions, weak assumptions, practical failures.
7. `Pass 2`: second-order effects, edge cases, hidden dependencies, ideal-condition assumptions.
8. Apply relevant adversarial lenses internally; replace weak ones. Report perspectives only when they materially changed findings, severity, or required changes; keep lenses internal otherwise, including for small or straightforward reviews.
9. Group root causes, then end with the verdict that matches the user's terminal question: readiness verdicts for execution-readiness reviews, normal scrutiny verdicts otherwise.

Normal scrutiny verdicts are exactly one of `Reject`, `Major revision`, `Minor revision`, `Defensible`, or `Partial review only`, with severity labels `Critical`, `High`, `Medium`, or `Low`; a canonical token may carry a scoping gloss ("Defensible, not yet optimal"). `Partial review only` means bounded review mode was used: the reviewed subset was judged, the full target was not. If more than one verdict could apply, choose the first matching in this order: `Reject`, `Major revision`, `Partial review only`, `Minor revision`, `Defensible` — a disqualifying finding in the reviewed slice renders its verdict, scoped to the slice, and is never hidden behind an incomplete-pass label. A verdict reports this pass's search, not a certified property of the artifact: `Defensible` and `Ready to Execute` are clearance verdicts, and a clearance verdict claims serious search was exhausted without a disqualifying find — it does not certify soundness, and it expires when the artifact changes. When the target survives scrutiny, say why it survives, then focus on residual risks and failure scenarios; note strengths briefly only after exhausting serious attempts to find weaknesses. When the reviewer rather than the user chose the register — readiness vocabulary, a formal stress test, or declining one on a trigger-matching target — say so in a clause.

On re-scrutiny of a revised target: re-read the live artifact fresh; verify claimed fixes against the artifact and the actual change between versions (a diff the user supplies, or one you compute from both versions), never the description of them; treat prior findings as hypotheses to re-earn, not conclusions to defend; hunt for new defects, not only compliance with your own required changes; and credit exactly what held. When a valid re-scrutiny finding opens a new structural repair class, mainly polices machinery earlier repairs added, or would change the target's category, say before prescribing another hardening cycle that continued investment needs a renewed decision from the user: this review owns whether the finding is real, not whether further hardening is still worth its cost.

## Execution-Readiness Reviews

Ask for an execution-readiness review when the user needs to know whether a plan, spec, handoff, rollout note, or other artifact is ready to build from.

Use readiness criteria internally and report them when they materially affect the decision: bad proof, bad scope, stale authority, source/runtime mismatch, weak gates, missing owner, hidden dependency, and implementation-readiness blockers.

For execution-readiness reviews, replace the normal scrutiny verdict with `Execution Readiness Verdict` and exactly one of:

- `Ready to Execute`
- `Patch Before Implementation`
- `Not Executable Yet`
- `Partial Review Only`

Use `Ready to Execute` only when inspected evidence supports the required proof class and no material readiness blocker remains. Use `Partial Review Only` for bounded passes that cannot inspect the full readiness surface. If more than one readiness verdict could apply, choose the first matching in this order: `Not Executable Yet`, `Patch Before Implementation`, `Partial Review Only`, `Ready to Execute` — a disqualifying blocker found in a bounded pass renders `Not Executable Yet`, and a patchable in-slice gap renders `Patch Before Implementation`, each scoped to the reviewed subset with the uninspected readiness surface named.

If the user asks for both a formal stress test and an execution-readiness review, include the formal stress-test sections but still end with the readiness verdict.

## Formal Stress Tests

Ask for a formal stress test when the review needs an explicit assumptions audit, pre-mortem, dimensional critique, and confidence boundary.

For a formal stress test, make these pieces visible:

- `Assumptions Audit`: list only verdict-driving assumptions. Tag each as `validated`, `plausible`, `wishful`, or `unverified`; tag evidence as `observed`, `source-backed`, `inferred`, or `unverified`; state what breaks if the assumption is wrong.
- `Pre-Mortem`: name the most likely failure path and the most damaging quiet failure path. If they are the same, say so and write one.
- `Dimensional Critique`: explicitly cover `Correctness` and `Completeness`; add `Security / Trust Boundaries`, `Operational`, `Maintainability`, and `Alternatives Foregone` only when relevant. Name skipped dimensions only when the user expected them or when omission could change the verdict.
- `Confidence Boundary`: use prose, not a default numeric score. State what was checked, what remains unverified, and what evidence would change the verdict. Use numeric confidence only when the user explicitly asks for it.

For ordinary scrutiny, keep assumptions, failure narratives, dimensional lenses, and confidence boundaries internal unless they materially change findings, severity, required changes, or the verdict.

## Guardrails

- Multiple artifacts: choose or split by named target.
- Incomplete target: review existing material and treat gaps as risks.
- Skill bundle scope: do not stop at `SKILL.md`; cite where main instructions, agent metadata, and material references agree or conflict. Do not bulk-review irrelevant assets, generated runs, or examples unless they affect invocation, instructions, evidence, or expected outputs. State skipped-file and materiality tradeoffs explicitly.
- Review-only default: do not edit files, rewrite the artifact, act through connected tools, publish, or implement fixes unless the user explicitly asks for that separate action after the review.
- Mixed critique and implementation: finish scrutiny first, stop after the verdict, and wait for explicit follow-through before changing artifacts.
- Self-authored target: if you authored the target — this session or otherwise — disclose it in `Target And Evidence`, and treat your own absence claims (`none`, no residual risk, a clearance verdict) with declared extra skepticism.
- Bounded review mode: when the target is too large to inspect completely in one pass, state the reviewed subset before findings, review the highest-risk surface first, mark omitted areas `unverified`, give the next slice needed for a complete review, and do not issue a full-clearance verdict for the full target (do not use `Defensible` or `Ready to Execute`). A review whose scope was narrowed externally — a scope the user restricted, an assigned lens, or sampled coverage — is also a bounded review: state the subset, scope the verdict to it, and leave full-clearance tokens unissued. Verdict choice in bounded mode follows the precedence order defined with each enum.
- Evidence: cite file/line, section or quoted phrase, output, source, or observed behavior for concrete claims; label inference or uninspectable behavior as uncertainty.
- Citation calibration: target-internal contradictions may be reported from the target alone. Any `Critical`, `High`/`High-Risk`, or verdict-driving claim — including the final verdict — that depends on an external citation must read the cited resource; otherwise downgrade the claim to `uncalibrated / citation not inspected`.
- Do not mentally repair broken logic or pad with weak objections.

## Output

Default sections: `Target And Evidence`, `Premise Check`, `Critical Failures`, `High-Risk Assumptions`, `Real-World Breakpoints`, `Hidden Dependencies`, `Patterns And Root Causes`, `Required Changes`, `Verdict`. Add `Adversarial Perspectives` only when a lens materially changed findings, severity, or required changes. Add `Bounded Review Scope` before `Target And Evidence` when bounded review mode is used; for bounded ordinary scrutiny, choose the verdict by the precedence order — `Verdict: Partial review only` unless a disqualifying in-slice finding renders `Reject` or `Major revision`, scoped to the slice. If the user asks for a shorter answer, keep the section order and compress the content rather than dropping sections.

For an execution-readiness review, use the same section discipline but replace `Verdict` with `Execution Readiness Verdict`. Name readiness blockers, the supporting evidence, the practical impact, and the smallest repair needed before implementation.

Use relevant lenses: plan logistics, writing evidence, code correctness/security/failure modes/tests, strategy assumptions/incentives/tradeoffs. Read `references/review-format.md` only for complex targets, full structured reviews, or repeated severity/citation formatting. For a formal stress test, add explicit `Assumptions Audit`, `Pre-Mortem`, `Dimensional Critique`, and `Confidence Boundary` sections while preserving required changes and the applicable verdict.

When `Required Changes` or `Execution Readiness Verdict` blockers should become tracked issues rather than a chat-only review, say so and stop: no issue-filing skill is in this skill set, so filing them — one issue per finding — is the user's separate action. Scrutinize stays review-only and does not open issues itself.

When scrutiny rejects a *position, decision, or argument* — a contested stance, not a code or plan defect — name `steelman` to build the strongest honest case for it before the user discards it; scrutinize attacks and never advocates.
