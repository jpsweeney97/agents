# Skill UX Design Calibration

Use these examples when routing, edit safety, audit depth, targeted scope, or
split `Safe UX`/proposal-first behavior is unclear. Do not load this file for
every routine run.

## Default Bounded Scan With Safe UX Edit

User asks: "Make this skill less frustrating to use."

Expected mode: bounded whole-journey scan, direct `Safe UX` edit allowed.

Why: The user framed the work as UX, did not ask for read-only behavior, and the
likely fix is clearer presentation of already-existing behavior.

Expected behavior:

- Inspect `SKILL.md`, `agents/openai.yaml`, and directly referenced behavior
  files.
- Scan across the six UX phases only far enough to find the top 1-3 frictions.
- Directly edit separable wording, correction-path, setup-visibility, or output
  shape fixes that do not change protected behavior.
- Close with `Safe UX because...` and a source-vs-runtime proof boundary.

## Read-Only Bounded Pass

User asks: "Read-only pass: where is this skill most annoying for users?"

Expected mode: bounded whole-journey scan, no edits.

Why: `read-only` disables edits, but it does not imply exhaustive coverage.

Expected behavior:

- Report the top likely frictions, not one section per UX phase.
- Include `Coverage: bounded whole-journey scan, not exhaustive surface-by-surface coverage.`
- Label any skipped or uninspected context that materially limits confidence.
- Do not write files, stage, commit, install, refresh, or mutate runtime state.

## Plain Audit

User asks: "Audit this skill's UX."

Expected mode: read-only exhaustive UX pass.

Why: Plain `audit` has a stronger meaning than `read-only`: it asks for full
surface coverage with no edits.

Expected behavior:

- Inspect or explicitly exclude every UX phase and material sub-surface: before
  use, starting state, during use, proof and safety, durable aftermath, and
  agent support.
- Include an inspect-or-exclude coverage ledger.
- Present findings as user frictions with patch-shaped fixes.
- Do not edit unless the user later approves a named fix.

## Targeted Surface

User asks: "Check whether users can trust the validation language."

Expected mode: targeted surface review.

Why: The user named a proof-and-safety concern in ordinary language.

Expected behavior:

- Focus proof and safety: validation language, evidence standards,
  certification claims, and runtime/source distinctions.
- Inspect neighboring files only when they affect validation-trust UX.
- Label the targeted boundary in the response.
- Treat proof, evidence, certification, and runtime/source changes as
  proposal-first unless the user explicitly approves the named change.

## Mixed Request Routing

User asks: "Make this skill clearer."

Expected mode: route to `writing-principles` unless surrounding context clearly
frames the problem as skill UX.

Why: Plain clarity/prose quality is not enough to invoke this skill.

Expected behavior:

- Name the better lane when the primary request is instruction clarity, prose
  cleanup, correctness, adversarial review, or machinery design.
- Stay in `skill-ux-design` when the user says "make it easier to steer",
  "users cannot tell what it will edit", or similar UX framing.
- In mixed requests, follow the primary framing and mention secondary UX
  follow-up only when useful.

## Split Safe UX And Proposal-First Fix

User asks: "Users cannot tell when this skill will edit, and I think it should
also auto-commit its changes."

Expected mode: split fix.

Why: Visible edit-boundary language can be `Safe UX`; changing commit behavior
is protected durable aftermath and mutation behavior.

Expected behavior:

- Directly apply the separable `Safe UX` portion if it only clarifies the
  already-existing edit boundary.
- Present auto-commit behavior as a named proposal-first change requiring
  explicit approval.
- Close the direct safe portion with `Safe UX because...`, verification, proof
  boundary, and protected surfaces not touched.
- If the user later approves the auto-commit behavior, close that protected edit
  with an approval/lifecycle rationale instead of a `Safe UX because...`
  receipt.
- Do not bundle the protected change into the safe wording edit.
