# Skill UX Design Rubric

Use this rubric to find friction in the user's journey through invoking and
using a Codex skill. The goal is better skill UX without weakening the skill's
behavior contract.

## Priority Order

1. Preserve rigor, safety, evidence, authority, validation, permission,
   mutation, persistence, external-access, behavior-smoke, and plugin/runtime
   surface boundaries.
2. Name the user's likely friction in plain language.
3. Use the six UX phases as a coverage lens, not as a required report schema.
4. Make the user's assumptions visible and cheap to correct.
5. Let the user steer scope, depth, edit behavior, proof level, and artifacts in
   ordinary language.
6. Give Codex enough context, examples, defaults, and stop conditions to produce
   the intended user experience reliably.

## Six-Phase Lens

Use the phase names to notice where friction can appear. Do not require one
finding, score, field, or recommendation per phase unless the user asks for
`audit`, `exhaustive`, full coverage, or a surface-by-surface pass.

1. **Before use**: discovery, name, trigger wording, neighboring-skill routing,
   and default prompt.
2. **Starting state**: inferred target, mode, authority, mutation boundary,
   skipped context, and correction path.
3. **During use**: interaction rhythm, progress visibility, steering depth/cost,
   context acquisition, and handoffs.
4. **Proof and safety**: validation language, evidence standards, approval gates,
   external access, privacy, behavior-smoke boundaries, and plugin/runtime
   surfaces when applicable.
5. **Durable aftermath**: saved artifacts, tickets, handoffs, commits, pushes,
   installs, refreshes, uncommitted outputs, and next lifecycle step.
6. **Agent support**: whether the skill gives Codex enough context, examples,
   defaults, and stop conditions to reliably produce the intended user
   experience.

Default mode should scan across these phases only far enough to find the top 1-3
likely frictions. `Audit` and `exhaustive` modes should inspect or explicitly
exclude each phase and the material sub-surfaces within it.

A phase is not covered by naming it. In audit/exhaustive mode, inspect the
phase's material sub-surfaces that plausibly apply to the target skill, such as
external access, persistence, behavior-smoke proof, or plugin/runtime surfaces
when they could affect the user's experience. If a sub-surface does not apply,
mark it out of scope instead of silently skipping it.

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
a private command language.

Useful steering phrases include:

- `quick`
- `read-only`
- `audit`
- `exhaustive`
- `targeted: <surface>`
- `apply` or `apply accepted plan`
- `with verification`
- `save report`
- plain language such as "look at recovery", "just output", "do the full path",
  "audit only", "do not edit", or "check validation trust"

Steering must not bypass proposal-first protected surfaces, evidence standards,
approval gates, external-access boundaries, behavior-smoke boundaries, or
plugin/runtime proof boundaries.

## Interaction Fit

Check whether the skill's rhythm matches the user's intent:

- Default UX design should be a bounded whole-journey scan with 1-3 top
  frictions, not a full ledger.
- `read-only` should disable edits without implying exhaustive coverage.
- Plain `audit` should be read-only and exhaustive across material sub-surfaces
  unless narrowed by `quick`, `targeted`, or explicit ordinary-language scope.
- Targeted requests should stay focused and label their boundary.
- Long audit/exhaustive runs should show progress only when it helps the user
  understand scope, cost, confidence, or remaining uncertainty.
- Editing runs should distinguish direct `Safe UX` changes from proposal-first
  protected changes.

Avoid adding ceremony when the task is small. A concise one-line result can be
enough for low-risk edits.

## Safe UX Preservation

For each direct edit, verify that it only clarifies already-existing behavior.

Usually `Safe UX`:

- clearer output order or first-screen summary
- less abstract wording
- visible inferred setup language
- correction paths
- compact steering phrases
- examples and smoke prompts
- default prompt or metadata alignment that does not change trigger scope
- wording that makes already-existing behavior easier to understand

Proposal-first protected surfaces include routing, triggers, non-triggers,
handoffs, promises, lifecycle guarantees, validation/proof/evidence standards,
authority/source-of-truth rules, mutation/edit/approval boundaries, external
access, privacy, persistence, behavior-smoke claims, plugin/runtime claims,
live runtime activation, and stop condition changes.

When a fix mixes `Safe UX` and protected behavior, split it. Apply only the
separable safe portion directly and present the protected portion as a named
patch-shaped proposal.

## Agent Support

Agent support is an explicit secondary surface. It matters even when user impact
is indirect or speculative.

Check whether another Codex instance can execute the intended UX reliably:

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

Default no-edit proposals should stay compact:

```markdown
Bottom line: <main user friction>
Coverage: bounded whole-journey scan, not exhaustive surface-by-surface coverage.

Suggested fixes:
1. <fix>
   Safe UX | Proposal-first
   Why it matters: <user-visible effect>
   Change shape: <concrete patch direction>
   Approval needed: <only if proposal-first>
```

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
