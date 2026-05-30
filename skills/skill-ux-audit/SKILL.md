---
name: skill-ux-audit
description: "Use when the user asks to audit, improve, or apply UX improvements to a Codex skill, SKILL.md, agents/openai.yaml, skill reference, or skill example. Trigger only for explicit UX language or clear user-facing synonyms such as usability, ease of use, chat output, readability, interaction flow, or friction. Do not trigger for general skill improvement, rigor, validation, correctness, or safety work unless the user explicitly frames it as UX. Produces a concise read-only UX improvement plan by default and edits only when the user explicitly says apply, implement, or approves a specific plan."
---

# Skill UX Audit

Improve how a skill feels to use while preserving the skill's rigor and behavior
contract.

Read [ux-rubric.md](references/ux-rubric.md) before any substantive audit or
apply pass. Use [agent-smoke-test.md](examples/agent-smoke-test.md) as the
lightweight forward-test shape after behavior-contract changes.

## Trigger Boundaries

- Trigger only when the request is explicitly about UX or a user-facing synonym
  such as usability, ease of use, chat output, readability, interaction flow, or
  friction.
- Do not trigger for general skill improvement, rigor, validation, correctness,
  or safety work unless the user explicitly frames it as UX.

## Defaults

- Make the user's chat experience the primary UX surface.
- Treat the agent's execution experience as the supporting layer that makes the
  user experience reliable.
- Default to read-only audit mode. Do not edit files unless the user explicitly
  says `apply`, `implement`, `make the changes`, or approves a specific plan.
- Optimize for a ranked short list of 3-5 high-leverage improvements, not a
  full rubric dump.
- Put detailed rubric notes under `Details` only when they materially affect
  confidence or scope.
- Ask only when the target skill is unclear or an apply request would touch a
  protected surface without explicit approval.

## Target And Context

- If the user names a skill path, use that path as the target.
- If the user names a file inside a skill, treat the containing skill directory
  as the target unless the request is explicitly file-scoped.
- If the current directory is a skill directory and no target is named, infer it
  as the target.
- Inspect `SKILL.md`, `agents/openai.yaml` when present, and directly referenced
  `references/` or `examples/` files needed to understand the output contract.
- Avoid broad repo scans unless the user asks for a cross-skill audit.

## Safe UX Surfaces

These are usually safe to recommend or edit in apply mode:

- chat output
- interactiveness
- output ordering
- digestibility
- assumption visibility
- low-friction user modifiers
- examples and smoke prompts
- correction paths
- clearer stop conditions

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

Protected does not mean untouchable. It means the change may alter the skill's
behavior contract, so the user must see and approve that risk before edits.

## Audit Workflow

1. Identify the target skill and whether the request is read-only audit mode or
   explicit apply mode.
2. Read the target bundle enough to understand its trigger, defaults, output
   shape, safety boundaries, evidence requirements, validation expectations, and
   examples.
3. Apply the UX rubric from [ux-rubric.md](references/ux-rubric.md), prioritizing
   first-screen readability, visible assumptions, user control, interaction fit,
   safe defaults, and preserved rigor.
4. Produce 3-5 ranked opportunities. Each opportunity must include a compact
   evidence note from the target skill and a rigor guardrail.
5. Separate safe UX changes from `Contract-risky` changes.
6. In apply mode, re-read the live files before editing, keep changes scoped, and
   preserve protected surfaces unless the user has explicitly approved the
   specific contract-risky change.
7. After edits, validate the edited skill surfaces using the local repo's
   validation path. At minimum, parse changed YAML/frontmatter, check referenced
   paths, run the available skill validator when present, run whitespace checks,
   and do a realistic dry run when practical.

## Default Audit Report

Start with:

```markdown
**Result Brief**
Target: <skill path>
Mode: read-only audit
Bottom Line: <one-sentence UX diagnosis>

Top Opportunities:
1. <change> (Safe UX|Contract-risky)
   Why it helps: <user-visible improvement>
   Evidence: <specific file/section signal>
   Rigor guardrail: <what must remain true>

Next Step: <apply plan, ask for approval, or no-op>
```

Then add `Details` only when needed for coverage, contract-risky rationale,
unresolved assumptions, or skipped surfaces.

If no high-leverage improvements are found, say that directly and list any
remaining confidence limits.

## Apply Mode Closeout

When edits are made, close with:

```markdown
**What changed**
<concise file-level summary>

**Why it changed**
<UX effect and protected-surface guardrails>

**Verification performed**
<commands and dry-run checks>

**Remaining risks**
<unverified behavior or contract-risky items not applied>
```

Do not describe a `Decision Summary`, `Result Brief`, or other readable preface
as a substitute for evidence, validation, or user approval. Presentation changes
must make the rigorous packet easier to consume, not remove it.
