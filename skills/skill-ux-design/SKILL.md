---
name: skill-ux-design
description: "Use when the user explicitly asks to design, audit, improve, or apply UX improvements to a Claude or Codex skill or skill support surface, including invocation, steering, output experience, validation trust, recovery, or durable aftermath. Do not use for general skill improvement, instruction prose quality, rigor, validation, correctness, safety, routing cleanup, or adversarial review unless the user frames it as skill UX."
---

# Skill UX Design

Improve the user's journey through invoking and using a Claude or Codex skill. Treat instruction quality and agent execution as supporting causes, not the goal.

Read [ux-rubric.md](references/ux-rubric.md) before any substantive design, audit, or edit pass.

Use [examples/calibration.md](examples/calibration.md) when routing, edit safety, audit depth, targeted scope, or split Safe UX/proposal-first behavior is unclear. Do not load examples for every routine run.

## Trigger Boundaries

- Trigger only when the request is explicitly about UX or a user-facing synonym such as usability, friction, user journey, discovery/invocation, steering, output experience, edit control, validation trust, recovery, durable aftermath, or skill-use experience.
- Do not trigger for general skill improvement, plain instruction-doc prose quality, general readability, rigor, validation, correctness, safety work, or trigger-boundary cleanup unless the user explicitly ties it to the user's journey through the skill.
- Once this skill is active, inspect instruction quality and agent execution as explanations for UX friction, not as independent goals.

## Neighboring Skills

This skill owns the user experience of using a Claude or Codex skill. It does not own all instruction quality, skill correctness, adversarial review, or agent-facing design decisions.

Route the primary request elsewhere when the user's main intent is different:

- Use `writing-principles` for plain instruction clarity, prose quality, or instruction-doc editing not framed as skill UX.
- Use the relevant review-family or skill-focused scrutiny lane for adversarial review of a skill behavior contract.
- Use `agent-facing-design` for "should we add machinery?" questions.
- Use `outcome-shaping` for open-ended outcome clarification.
- Use `grill-me` for pressure-testing a proposed design.

Inside a `skill-ux-design` run, neighboring concerns may still be inspected as causes of UX friction. Prose quality matters when it changes what the user understands. Trigger scope matters when the user cannot predict invocation. Agent-facing machinery matters when it creates visible rigidity, slowness, noisy reporting, missed context, or over-questioning.

For mixed requests, follow the user's primary framing. If UX is primary, stay in `skill-ux-design` and treat neighboring issues as UX evidence. If correctness, adversarial review, machinery design, or prose quality is primary, route to the owning skill and mention UX only as secondary.

Do not silently become a neighboring workflow. If the best next move is no longer UX design, name the neighboring lane and stop or ask before switching.

## Defaults

- Default to a bounded whole-journey scan: inspect across the six UX phases only far enough to find the highest-leverage 1-3 user frictions.
- Do not produce surface-by-surface coverage unless the user asks for exhaustive/full coverage or clearly requests a complete audit.
- Make the user journey the primary UX surface. Treat chat output as one major surface within that journey, not as the whole scope.
- Treat agent support as an explicit secondary surface, including internal execution issues whose user impact is indirect or speculative.
- Edit directly once the target and a low-risk `Safe UX` fix are clear, unless the user requests no edits, asks for audit/full read-only coverage, or the fix touches a proposal-first protected surface.
- When editing is not safe yet, make the next move patch-shaped: show the concrete text to add, remove, replace, or approve.

## UX Phase Lens

Use these six phases as the internal UX lens, not as required output sections:

1. **Before use**: discovery, name, trigger wording, neighboring-skill routing, and default prompt.
2. **Starting state**: inferred target, mode, authority, mutation boundary, skipped context, and correction path.
3. **During use**: interaction rhythm, progress visibility, steering depth/cost, context acquisition, and handoffs.
4. **Proof and safety**: validation language, evidence standards, approval gates, external access, privacy, behavior-smoke boundaries, and plugin/runtime surfaces when applicable.
5. **Durable aftermath**: saved artifacts, tickets, handoffs, commits, pushes, installs, refreshes, uncommitted outputs, and next lifecycle step.
6. **Agent support**: whether the skill gives the agent enough context, examples, defaults, and stop conditions to reliably produce the intended user experience.

The phase names are a diagnostic vocabulary. Use them to notice, explain, target, and bound UX issues, but do not emit one section per phase unless the user asks for `audit`, `exhaustive`, full coverage, or a surface-by-surface pass.

The vocabulary names where friction can appear. It does not require one finding, score, field, or recommendation per surface.

A phase is not covered by naming it. For `audit` or `exhaustive` coverage, inspect the material sub-surfaces within each phase that plausibly apply to the target skill, or explicitly mark them out of scope with a reason.

## Mode And Steering Language

Honor plain language as well as explicit modifiers. Users should not have to remember magic words.

- `read-only`, "do not edit", or "no changes": do not edit; use the normal bounded whole-journey scan unless the user also asks for audit, exhaustive, full coverage, every surface, or a complete pass.
- `audit`: run a read-only exhaustive UX pass; inspect every UX phase and the material sub-surfaces within it, or explicitly mark them out of scope.
- `exhaustive`, "full pass", "every surface", or "complete audit": inspect every UX phase and its material sub-surfaces with an inspect-or-exclude coverage ledger.
- `quick`: narrow inspection and label skipped surfaces.
- `targeted: <surface>` or plain language such as "look at recovery", "just output", or "check validation trust": focus the named UX surface.
- `with verification`: run focused safe validation or dry-run checks that directly support the UX finding or edit. Do not install dependencies, mutate caches, run broad suites, or touch external services unless the user explicitly asks for that access.
- `apply` or `apply accepted plan`: apply only accepted `Safe UX` fixes. Apply proposal-first or protected fixes only when the user explicitly approves those named changes. If an accepted plan is requested but no accepted plan is visible in the current context, stop and ask for the plan instead of inventing fixes.
- `save report`: write the final report only when the user supplies an output path or the local repo has an obvious report convention. Otherwise ask for the path before writing.

Plain `audit` means full read-only coverage across the six phases and their material sub-surfaces. `quick`, `targeted`, or an explicit narrower request can narrow an audit, but the output must label the narrowed coverage.

## Target And Context

- If the user names a skill path, use that path as the target.
- If the user names a file inside a skill, treat the containing skill directory as the target unless the request is explicitly file-scoped.
- If the current directory is a skill directory and no target is named, infer it as the target.
- Inspect `SKILL.md`, `agents/openai.yaml`, and directly referenced examples or references that shape behavior.
- Follow nearby behavior-shaping files only as needed to understand the top likely frictions, unless the user asks for audit or exhaustive coverage.
- Avoid broad repo scans unless the user asks for a cross-skill UX pass.

## Safe UX And Proposal-First Boundaries

Direct edits are allowed only for `Safe UX` fixes: changes that improve how the user understands, steers, corrects, or reads already-existing behavior without changing when the skill runs, what it promises, what it trusts, what it proves, what it may mutate, what external surfaces it may touch, or what durable aftermath it creates.

Usually `Safe UX`:

- clearer output order or first-screen summary
- less abstract wording
- visible inferred setup language
- correction paths
- compact steering phrases
- examples and smoke prompts
- default prompt or metadata alignment that does not change trigger scope
- wording that makes already-existing behavior easier to understand

Treat these as proposal-first protected surfaces:

- routing and trigger scope
- non-trigger boundaries and neighboring-skill handoffs
- promise, scope, and lifecycle guarantees
- validation, proof, certification, and evidence standards
- authority, baseline, and source-of-truth rules
- mutation, edit, destructive-action, and approval boundaries
- external access, privacy, connector, web, GitHub, Gmail, or remote-state behavior
- persistence, saved artifacts, handoffs, tickets, commits, pushes, installs, refreshes, plugin activation, or live runtime behavior
- source/lifecycle coherence claims, including plugin cache, marketplace, metadata, distributed-copy, hook, and live-runtime distinctions
- adding, removing, or changing stop conditions

If an edit is wrong, ask whether it would merely make the skill less clear, or whether it could change what the user reasonably believes the skill will do. If it changes expectation, trust, authority, permissions, persistence, runtime state, or routing, proposal first.

When a UX fix mixes `Safe UX` and protected behavior, split it. Apply only the separable `Safe UX` portion directly. Present the protected portion as a named patch-shaped proposal requiring explicit approval.

## Workflow

1. Identify the target skill and mode: bounded design/edit, read-only, audit, targeted, quick, exhaustive, or apply.
2. Read enough live context to understand the user's journey through the target skill and the likely sources of friction.
3. Use the six UX phases as a coverage lens. In default mode, scan broadly enough to find the highest-leverage 1-3 frictions; in audit/exhaustive mode, inspect or explicitly exclude every phase and material sub-surface.
4. Translate each top issue into concrete user friction: what the user has to guess, decode, correct, wait through, trust, approve, recover from, or follow up on.
5. Separate direct-edit `Safe UX` fixes from proposal-first protected fixes.
6. Before editing, re-read the live files, keep changes scoped, and preserve protected surfaces unless the user has explicitly approved the named change.
7. After edits, validate the edited skill surfaces using the local repo's validation path. At minimum, parse changed YAML/frontmatter, check referenced paths, run the available skill validator when present, run whitespace checks, and do a realistic dry run when practical.
8. Label the proof boundary honestly: structural validation is not behavior proof; name plugin, cache, marketplace, or runtime checks only when those surfaces are part of the claim.

## Progress Visibility

Inherit the host agent's normal progress-update behavior; do not invent a special progress protocol.

Give a short update when inspection is broad, validation is running, or edits are about to happen. Name the user-experience surface being checked or changed, not every file being opened.

Do not narrate every read, maintain a running audit ledger, or show coverage notes by default. For long `audit` or `exhaustive` runs, mention the current UX phase and remaining uncertainty only when it helps the user understand scope, cost, or confidence.

Before file edits, say what UX fix is being made and whether it is `Safe UX` or proposal-first. Do not edit protected surfaces unless the user has explicitly approved the named change.

Progress updates are part of the `During use` UX surface: they should reduce uncertainty about scope, cost, edits, and proof, not expose the agent's internal reading log.

## Default Output

When no edit is made, keep the response compact and patch-shaped:

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

Mention the UX phase only when it helps the user understand the issue, skipped scope, or proposed fix. Add `Details` only for coverage limits, proposal-first rationale, unresolved assumptions, or audit/exhaustive ledgers.

If no high-leverage fixes are found, say that directly and list any confidence limits.

## Edit Closeout

For direct `Safe UX` edits, close with:

```markdown
Changed: <files/sections>
Safe UX because <one sentence explaining why this clarified existing behavior without changing protected surfaces>
Verified: <frontmatter/YAML parse, referenced paths, available validator, diff check, etc.>
Proof boundary: <what was and wasn't proven — e.g. structural/source validation only, no behavior smoke test; or note the realistic dry run / smoke test if one was run>.
Not touched: <protected surfaces intentionally left alone>
```

When the skill edits directly without prior approval, the closeout must include one sentence beginning `Safe UX because...`. The sentence must explain why the edit clarified already-existing behavior without changing routing, promise, proof, authority, mutation, external access, persistence, behavior-smoke claims, plugin/runtime claims, or lifecycle expectations. If that sentence is hard to write honestly, the change was proposal-first.

For approved proposal-first or protected edits, do not use `Safe UX because...` as the edit-path receipt. Close with an approval and lifecycle rationale instead:

```markdown
Changed: <files/sections>
Approved change: <named user-approved proposal-first/protected change>
Lifecycle/protected-surface rationale: <what expectation, authority, proof, mutation, persistence, behavior-smoke, plugin/runtime, or lifecycle surface changed>
Verified: <frontmatter/YAML parse, referenced paths, available validator, diff check, etc.>
Proof boundary: <what was and wasn't proven — structural/source validation, and whether a realistic dry run / behavior smoke test was run>. Plugin/cache/marketplace/runtime surfaces were not checked unless named above.
Not touched: <protected surfaces intentionally left alone>
```

For mixed edits, split the closeout: use `Safe UX because...` only for the separable safe portion, and use the approval/lifecycle rationale for the approved proposal-first or protected portion.

Always include a proof boundary after edits, including low-risk text changes. Keep it one line by default. Expand it when the edit touches skill identity, metadata, default prompts, marketplace entries, plugin caches or copies, validation trust, hook behavior, remote state, or live runtime behavior.

For edits involving skill identity, metadata, default prompts, marketplace entries, plugin caches or copies, hooks, remote state, or live runtime behavior, the closeout must explicitly name each touched and untouched lifecycle layer.

## Validation And Lifecycle Boundary

Validate the exact surfaces edited.

- Parse edited `SKILL.md` frontmatter and edited YAML metadata.
- Check referenced paths such as [ux-rubric.md](references/ux-rubric.md) and [calibration.md](examples/calibration.md).
- Run the available local skill validator when present.
- Run whitespace checks such as `git diff --check`.
- Inspect metadata alignment across `display_name`, `short_description`, and `default_prompt`.
- Search for stale identity references after renames.
- Search for stale conceptual framing after large rewrites, such as old narrow-scope or report-first terms, and review any hits instead of assuming zero hits is required.

Do not claim plugin install, marketplace, cache, distributed-copy, hook, remote, or live runtime behavior changed unless that path was verified. When the edited file is itself the live source, treat it as such and separate structural validation from behavior smoke testing instead of inventing a runtime proof layer.
