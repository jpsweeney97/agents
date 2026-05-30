# Skill UX Audit Rubric

Use this rubric to find improvements that make a skill easier for users to
trust, steer, and understand without weakening the skill's behavior contract.

## Priority Order

1. Preserve rigor, safety, evidence, authority, validation, and mutation rules.
2. Make the first screen useful to a human.
3. Make assumptions visible and cheap to correct.
4. Let users steer cost and depth with compact language.
5. Give the agent enough defaults, stop conditions, and examples to produce the
   intended experience reliably.

## Readable First Screen

Check whether the default chat output answers the user's likely first questions:

- What happened?
- What matters most?
- What should I do next?
- What was inspected or skipped?
- Is this result certified, provisional, blocked, or only an investigation?

High-leverage improvements include a short `Result Brief`, `Status Brief`,
`Decision Summary`, or equivalent before detailed findings, ledgers, evidence
packets, and lane reports. The detailed packet should remain available below the
brief.

## Visible Assumptions

Check whether the skill shows important inferred choices:

- target path or object
- scope mode
- baseline, authority, or source of truth
- verification mode
- safety or mutation boundary
- output mode such as chat-only, saved artifact, or handoff

Useful fixes include an inferred setup block, a correction path, or labels such
as `inferred`, `user-supplied`, `unresolved`, and `not inspected`.

## User Control

Check whether a user can steer depth and cost in one phrase without learning the
full contract.

Useful modifiers include:

- `quick`
- `targeted: <claim/path>`
- `exhaustive`
- `with verification`
- `save report`
- `read-only`
- `apply accepted plan`

Modifiers must not bypass protected safety, evidence, or approval gates.

## Interaction Fit

Check whether the skill's interaction pattern matches the job:

- Interactive skills should ask one high-leverage question at a time.
- Audit and review skills should default to read-only reports.
- Editing skills should distinguish plan, apply, verification, and closeout.
- Skills that infer context should show what they inferred.
- Skills that can be heavy should lead with the answer before machinery.

Avoid adding ceremony when the task is small. A concise one-line result can be
enough for low-risk edits.

## Agent Execution Support

Check whether another Codex instance can execute the desired UX reliably:

- Trigger and non-trigger boundaries are clear in frontmatter.
- Defaults cover omitted target, scope, verification, artifact, and mutation
  choices.
- Stop conditions are explicit and cheap to follow.
- References are loaded only when needed and every referenced path exists.
- Examples show realistic low-friction prompts and expected behavior.
- Validation instructions match the local repo's real tools.

Do not add scripts, schemas, stages, or scoring unless deterministic mechanics
are truly needed. Prefer judgment-supporting context.

## Rigor Preservation

For each proposed change, name what must remain true:

- Evidence requirements stay intact.
- Safety and destructive-action gates stay intact.
- Authority precedence stays intact.
- Permission and mutation boundaries stay intact.
- Validation remains explicit.
- Detailed findings, ledgers, or review packets remain available below the
  brief or in durable artifacts.

If preserving rigor requires a new output label, correction path, or clarification
of certification language, prefer that over removing the rigorous section.

## Opportunity Format

Use this shape for each finding:

```markdown
<rank>. <change> (Safe UX|Contract-risky)
Why it helps: <human-readable UX improvement>
Evidence: <specific observed section or missing behavior>
Rigor guardrail: <protected behavior that must remain true>
Apply scope: <files or sections likely touched>
```

Mark a change `Contract-risky` when it touches trigger scope, non-trigger
boundaries, destructive-action gates, evidence standards, validation ladders,
authority precedence, or permission and mutation rules.

## Common Anti-Patterns

- Leading with a full evidence ledger before the result.
- Saying `failed` when the result is really an uncertified investigation.
- Hiding inferred target, baseline, scope, or verification choices.
- Forcing users to know exact prompt wording to choose quick, targeted, saved,
  or verified modes.
- Replacing a rigorous packet with a summary instead of moving the packet below
  the summary.
- Adding a fixed scoring system when ranked judgment and evidence notes are
  enough.
- Treating metadata alignment as proof of runtime behavior.
