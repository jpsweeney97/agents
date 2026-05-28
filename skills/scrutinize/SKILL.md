---
name: scrutinize
description: Use when the user explicitly asks for adversarial review of a plan, design, draft, argument, decision, code change, or artifact. Trigger on "scrutinize", "be brutal", "tear this apart", "assume this is wrong", or "reject until proven otherwise". Do not use for routine review, collaborative editing, or balanced feedback.
---

# Scrutinize

Stance: reject until evidence earns a better verdict. Review the exact target; read referenced files before severity-calibrated judgment.

## Workflow

1. State target and scope; ask one targeted question if unclear.
2. If the target is a skill directory, inspect the bundle surface before judging: `SKILL.md`, `agents/*.yaml`, and behavior-shaping references such as files linked from `SKILL.md`, `references/*`, or nearby docs/config that define invocation, constraints, evidence rules, examples, or output expectations.
3. Premise check: is this solving the right problem?
4. `Pass 1`: contradictions, omissions, weak assumptions, practical failures.
5. `Pass 2`: second-order effects, edge cases, hidden dependencies, ideal-condition assumptions.
6. Apply at least 3 relevant adversarial perspectives; replace weak ones.
7. Group root causes, then verdict: `Reject`, `Major revision`, `Minor revision`, or `Defensible`.

## Guardrails

- Multiple artifacts: choose or split by named target.
- Incomplete target: review existing material and treat gaps as risks.
- Skill bundle scope: do not stop at `SKILL.md`; cite where main instructions, agent metadata, and material references agree or conflict. Do not bulk-review irrelevant assets, generated runs, or examples unless they affect invocation, instructions, evidence, or expected outputs. State skipped-file and materiality tradeoffs explicitly.
- Mixed critique and implementation: finish scrutiny first.
- Evidence: cite file/line, output, source, or observed behavior for concrete claims; label inference or uninspectable behavior as uncertainty.
- Citation calibration: target-internal contradictions may be reported from the target alone. Any `Critical`, `High-Risk`, or final verdict that depends on an external citation must read the cited resource; otherwise downgrade the claim to `uncalibrated / citation not inspected`.
- Do not mentally repair broken logic or pad with weak objections.

## Output

Default sections: `Premise Check`, `Critical Failures`, `High-Risk Assumptions`, `Real-World Breakpoints`, `Hidden Dependencies`, `Adversarial Perspectives`, `Patterns And Root Causes`, `Required Changes`, `Verdict`.

Use relevant lenses: plan logistics, writing evidence, code correctness/security/failure modes/tests, strategy assumptions/incentives/tradeoffs. Read `references/review-format.md` only for complex targets, full structured reviews, or repeated severity/citation formatting.
