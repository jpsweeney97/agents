---
name: skill-ux-audit
description: "Use when the user asks to audit, improve, design, or apply UX improvements to a Codex skill, SKILL.md, agents/openai.yaml, skill reference, or skill example. Trigger only for explicit UX language or clear user-facing synonyms such as usability, ease of use, chat output, user-facing/chat/report readability, interaction flow, or friction. Do not trigger for general skill improvement, plain instruction-doc prose quality, rigor, validation, correctness, or safety work unless the user explicitly frames it as UX. Translates the target skill into likely chat-experience friction, proposes patch-shaped fixes, and may edit once the target and low-risk Safe UX fix are clear."
---

# Skill UX Audit

Improve how a skill feels to use in chat while preserving the skill's rigor and
behavior contract.

Read [ux-rubric.md](references/ux-rubric.md) before any substantive design,
audit, or edit pass.

## Trigger Boundaries

- Trigger only when the request is explicitly about UX or a user-facing synonym
  such as usability, ease of use, chat output, user-facing/chat/report
  readability, interaction flow, or friction.
- Do not trigger for general skill improvement, plain instruction-doc prose
  quality, general readability, rigor, validation, correctness, or safety work
  unless the user explicitly frames it as UX.
- Route plain `SKILL.md`, `agents/openai.yaml`, skill reference, `AGENTS.md`, or
  `CLAUDE.md` prose-quality and readability work to `writing-principles` unless
  the user frames the problem as skill UX or user chat experience.

## Defaults

- Make the user's chat experience the primary UX surface.
- Treat the agent's execution experience as the supporting layer that makes the
  user experience reliable.
- Default to chat-experience design mode: translate the target skill into likely
  user-facing friction, then propose exact replacement or addition text.
- Edit once the target and a low-risk `Safe UX` fix are clear, unless the user
  requests `read-only`, asks only for an audit/report, or the fix touches a
  protected surface.
- When editing is not safe yet, make the next move patch-shaped instead of
  abstract: show the concrete text to add, remove, or replace.
- Optimize for 1-3 high-leverage fixes, not a full rubric dump.
- Put detailed rubric notes under `Details` only when they materially affect
  confidence or scope.
- Ask only when the target skill is unclear, the desired chat experience is
  unclear enough that editing would guess at intent, the fix would touch a
  protected surface without explicit approval, or `apply accepted plan` is
  requested without an accepted plan visible in the current context.

## Mode Modifiers

Honor compact modifiers when the user includes them:

- `quick`: inspect `SKILL.md`, `agents/openai.yaml` when present, and the top
  output/defaults surfaces. Read only the referenced or nearby behavior-shaping
  files needed for the top 1-3 fixes. Label skipped surfaces as
  `not inspected`.
- `targeted: <surface>`: inspect only the named UX surface, claim, file class,
  or output path plus the files needed to support or contradict it. State the
  targeted boundary in the response or closeout.
- `exhaustive`: enumerate the target skill bundle and either inspect or
  explicitly exclude every file class. Put the coverage ledger under `Details`.
- `with verification`: run focused safe validation or dry-run checks that
  directly support the audit or applied edit. Do not install dependencies,
  mutate caches, run broad suites, or run unavailable tooling. Label the proof
  class in the result, such as `Verification: structural only`,
  `Verification: behavior dry run`, or `Verification: runtime not inspected`.
- `save report`: write the final audit report only when the user supplies an
  output path or the local repo has an obvious report convention. Otherwise ask
  for the path before writing.
- `read-only`: force no-edit behavior. Do not edit target files or apply a plan,
  even if the request also discusses possible changes.
- `apply accepted plan`: apply only `Safe UX` items from the accepted plan.
  Apply `Contract-risky` items only when the user explicitly approves those
  named items. If no accepted plan is visible in the current context, stop and
  ask for the accepted plan or rerun/read out the audit first. Do not invent
  plan items.

## Target And Context

- If the user names a skill path, use that path as the target.
- If the user names a file inside a skill, treat the containing skill directory
  as the target unless the request is explicitly file-scoped.
- If the current directory is a skill directory and no target is named, infer it
  as the target.
- Inspect `SKILL.md`, `agents/openai.yaml` when present, and referenced or
  behavior-shaping nearby files needed to understand the UX contract. Nearby
  files include examples, references, report contracts, rubrics, and scripts
  whose names or references indicate they affect skill behavior.
- Avoid broad repo scans unless the user asks for a cross-skill audit.

## Safe UX Surfaces

These are usually safe to recommend or edit in design/edit mode:

- chat output
- interactiveness
- output ordering
- digestibility
- assumption visibility
- low-friction user modifiers
- examples and smoke prompts
- correction paths
- clearer wording for already-stated stop conditions
- examples that show the intended chat rhythm
- metadata wording that aligns with the UX contract

## Protected Surfaces

Treat these as protected. Label any recommendation that touches them
`Contract-risky`, and do not apply it without explicit user approval for that
specific change:

- trigger scope
- non-trigger boundaries
- destructive-action gates
- evidence standards
- validation ladders
- authority precedence
- permission or mutation rules
- adding, removing, or changing stop-condition behavior

Protected does not mean untouchable. It means the change may alter the skill's
behavior contract, so the user must see and approve that risk before edits.

## Chat-Experience Design Workflow

1. Identify the target skill and whether the request is design/edit mode,
   read-only mode, or explicit `apply accepted plan` mode.
2. Read the target bundle enough to understand its trigger, defaults, output
   shape, safety boundaries, evidence requirements, validation expectations, and
   examples.
3. Translate the contract into the user's likely chat experience. Name the
   friction in plain language: what the user has to double-check, correct, wait
   through, decode, or ask for again.
4. Apply the UX rubric from [ux-rubric.md](references/ux-rubric.md), prioritizing
   first-screen usefulness, visible assumptions, user control, interaction fit,
   safe defaults, and preserved rigor.
5. Produce 1-3 patch-shaped fixes. Each fix must include the user-visible
   friction, the concrete text-level change, a compact evidence note from the
   target skill, and the rigor guardrail that must remain true. Evidence must be
   a file path plus line number when available, a named file plus section
   heading, or an explicit `not inspected` label with the reason.
6. Separate `Safe UX` changes from `Contract-risky` changes.
7. Edit directly only when the target is clear, the change is `Safe UX`, the
   replacement/addition text is clear, and the user has not requested read-only
   behavior. Otherwise, stop with the patch-shaped proposal and the exact
   approval needed.
8. If the top issues are mostly non-UX contract, validation, correctness, or
   safety issues, report them as out of scope or `Contract-risky` and route to
   the appropriate broader skill instead of applying them in this lane.
9. Before editing, re-read the live files, keep changes scoped, and preserve
   protected surfaces unless the user has explicitly approved the specific
   contract-risky change.
10. After edits, validate the edited skill surfaces using the local repo's
   validation path. At minimum, parse changed YAML/frontmatter, check referenced
   paths, run the available skill validator when present, run whitespace checks,
   and do a realistic dry run when practical. When the repo supplies concrete
   validation commands, run or report those commands instead of generic labels.
   Label whether the proof is structural only, behavior dry run, runtime not
   inspected, or runtime proof.

## Default Chat Response

When no edit is made, start with the friction in plain language and keep the
proposal patch-shaped:

```markdown
**Chat Experience Read**
Target: <skill path>
Mode: <design|read-only|targeted|quick|exhaustive>
Scope: <inspected surfaces; skipped surfaces or none>
Verification: <structural only|behavior dry run|runtime not inspected|not requested>
Bottom Line: <one-sentence description of the chat friction>

Patch-Shaped Fixes:
1. <fix> (Safe UX|Contract-risky)
   User friction: <what the user has to decode, correct, wait through, or ask again>
   Change shape: <exact section and replacement/addition/removal>
   Evidence: <file:line, file section, or not inspected + reason>
   Rigor guardrail: <what must remain true>

Next Step: <approve named Contract-risky item, clarify target, run requested edit, or no-op>
```

Then add `Details` only when needed for coverage, contract-risky rationale,
unresolved assumptions, or skipped surfaces.

If no high-leverage fixes are found, say that directly and list any remaining
confidence limits.

## Apply Mode Closeout

When edits are made, close with:

```markdown
**What changed**
<concise file-level summary>

**Why it changed**
<chat-experience effect and protected-surface guardrails>

**Verification performed**
Verification: <structural only|behavior dry run|runtime not inspected>
<commands and dry-run checks>

**Remaining risks**
<unverified behavior or contract-risky items not applied>
```

Do not describe a `Chat Experience Read`, `Decision Summary`, `Result Brief`, or
other readable preface as a substitute for evidence, validation, or required
user approval. Presentation changes must make the rigorous packet easier to
consume, not remove it.
