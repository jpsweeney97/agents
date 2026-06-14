# Skill UX Design Rubric

Use this rubric to find friction in the user's journey through invoking and
using a Claude or Codex skill. The goal is better skill UX without weakening the skill's
behavior contract.

This rubric is the diagnostic method. The binding contract it diagnoses against —
triggers, mode semantics, the `Safe UX`/protected-surface boundaries, and the
output and closeout templates — is defined in `SKILL.md`; this rubric references
those surfaces rather than restating them, so when they differ, `SKILL.md` wins.

## Priority Order

1. Preserve rigor, safety, evidence, authority, validation, permission,
   mutation, persistence, external-access, behavior-smoke, and plugin/runtime
   surface boundaries.
2. Name the user's likely friction in plain language.
3. Use the six UX phases as a coverage lens, not as a required report schema.
4. Make the user's assumptions visible and cheap to correct.
5. Let the user steer scope, depth, edit behavior, proof level, and artifacts in
   ordinary language.
6. Give the agent enough context, examples, defaults, and stop conditions to produce
   the intended user experience reliably.

## Six-Phase Lens

Use the phase names to notice where friction can appear. Do not require one
finding, score, field, or recommendation per phase unless the user asks for
`audit`, `exhaustive`, full coverage, or a surface-by-surface pass.

Use the six UX phases defined in `SKILL.md` — Before use, Starting state, During
use, Proof and safety, Durable aftermath, Agent support — as the coverage lens.
Default mode scans only far enough to find the top 1-3 frictions; `audit` and
`exhaustive` must inspect-or-exclude every phase and its material sub-surfaces
per `SKILL.md` (a phase is not covered by naming it).

## Friction Translation

Translate instruction text into what the user will experience.

Look for moments where the user may have to:

- discover or remember the right skill name
- guess whether this skill should win over a neighboring skill
- correct an inferred target, mode, source of truth, or mutation boundary
- wait through broad inspection without knowing cost or scope
- decode agent-facing terminology
- ask for concrete text after receiving abstract themes
- tell whether a recommendation is direct-edit safe or proposal-first
- understand whether proof is structural, behavior smoke checked,
  plugin/runtime checked, or not checked
- recover when the skill guesses wrong or hits a boundary
- track saved artifacts, commits, tickets, installs, refreshes, or runtime
  activation after the run

Useful fixes name the friction directly, then change the skill text that causes
it. Prefer exact replacement or addition text over broad advice.

## Visible Setup

Check whether the skill shows important inferred choices when they affect user
control:

- target path or object
- mode and coverage depth
- baseline, authority, or source of truth
- edit/mutation boundary
- skipped context
- proof or verification boundary
- output or persistence mode, such as chat-only, saved artifact, ticket, handoff,
  commit, install, or runtime activation

Useful fixes include inferred setup language, correction paths, or labels such
as `inferred`, `user-supplied`, `unresolved`, and `not inspected`.

## User Control

Check whether the user can steer the skill in ordinary language without learning
a private command language. The steerable modes and their semantics are defined
in `SKILL.md`; diagnose against that contract rather than restating them.

Steering must not bypass proposal-first protected surfaces, evidence standards,
approval gates, external-access boundaries, behavior-smoke boundaries, or
plugin/runtime proof boundaries.

## Interaction Fit

Check whether the skill's rhythm matches the user's intent. The mode rhythms
(default bounded scan, `read-only`, `audit`, `targeted`), progress timing, and
the rule that editing runs distinguish direct `Safe UX` changes from
proposal-first protected changes are defined in `SKILL.md`; check that the chosen
rhythm fits the user's intent.

Avoid adding ceremony when the task is small. A concise one-line result can be
enough for low-risk edits.

## Safe UX Preservation

For each direct edit, verify that it only clarifies already-existing behavior.

The `Safe UX` whitelist (what may be edited directly), the proposal-first
protected-surface list (what may not), the wrong-edit test that separates them,
and the rule that a mixed fix must be split — apply the separable safe portion,
propose the protected portion as a named patch-shaped change — are all defined in
`SKILL.md`. Verify each edit against that contract.

## Agent Support

Agent support is an explicit secondary surface. It matters even when user impact
is indirect or speculative.

Check whether another agent instance can execute the intended UX reliably:

- trigger and non-trigger boundaries are clear in frontmatter
- defaults cover omitted target, scope, proof, artifact, edit, and persistence
  choices
- mode semantics are concrete enough to follow
- examples show realistic prompts, output shape, correction paths, and
  boundaries
- referenced paths exist and behavior-critical instructions remain reachable
- validation instructions match the repo's real tools
- stop and handoff conditions are explicit

Do not add scripts, schemas, scoring, validators, or workflow machinery unless a
wrong value or step can damage the user's work product. Prefer examples,
boundaries, and recoverable state.

## Fix Format

Default no-edit proposals stay compact. Use the no-edit output template defined
in `SKILL.md` (`Bottom line` / `Coverage` / numbered `Suggested fixes`, each
tagged `Safe UX | Proposal-first` with `Why it matters`, `Change shape`, and
`Approval needed` when proposal-first).

Mention the UX phase only when it clarifies the issue, skipped scope, or fix.
For audit/exhaustive mode, include enough coverage detail to show which phases
and material sub-surfaces were inspected or excluded.

## Common Anti-Patterns

- Treating the six phases as a required report schema.
- Reporting abstract UX themes without showing the text-level change.
- Asking for approval again when the target is clear, the fix is `Safe UX`, and
  the user did not request read-only behavior.
- Applying trigger, proof, authority, mutation, external-access, persistence,
  behavior-smoke, or plugin/runtime changes as casual UX edits.
- Treating `audit` as a synonym for `read-only` instead of full read-only
  coverage of material sub-surfaces.
- Satisfying audit coverage by naming the six phases while skipping applicable
  sub-surfaces such as external access, persistence, behavior-smoke proof, or
  plugin/runtime surfaces.
- Forcing users to memorize exact modifiers when ordinary language was clear.
- Hiding inferred target, mode, authority, edit boundary, skipped context, or
  proof boundary.
- Leading with a full evidence ledger when default mode only needs the top
  frictions.
- Replacing rigorous evidence or validation with a friendly summary.
- Treating local live skill source, metadata changes, marketplace state, plugin
  cache, distributed copies, and live runtime behavior as the same thing.
