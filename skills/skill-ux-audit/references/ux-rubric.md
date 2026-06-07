# Skill UX Audit Rubric

Use this rubric to translate a skill into likely chat-experience friction, then
find concrete fixes that make the skill easier for users to trust, steer, and
understand without weakening the skill's behavior contract.

## Priority Order

1. Preserve rigor, safety, evidence, authority, validation, and mutation rules.
2. Name the user's likely chat friction in plain language.
3. Make the first screen useful to a human.
4. Make assumptions visible and cheap to correct.
5. Let users steer cost and depth with compact language.
6. Give the agent enough defaults, stop conditions, and examples to produce the
   intended experience reliably.

## Chat Friction Translation

Before recommending or editing, translate the instruction contract into what the
user will feel in chat.

Look for moments where the user may have to:

- decode agent-facing terminology
- correct an inferred target, mode, or next step
- wait through a report when they expected an edit
- ask for concrete text after receiving abstract themes
- double-check whether the agent changed behavior, only presentation, or
  runtime state

Useful fixes name the friction directly, then change the skill text that causes
it. Prefer exact replacement or addition text over broad advice.

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
as `inferred`, `user-supplied`, `unresolved`, and `not inspected`. When the
target and fix are clear and the change is `Safe UX`, editing directly is better
than forcing the user through a second approval loop.

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

When auditing `skill-ux-audit` itself or applying this rubric to another skill,
check whether modifiers have concrete behavior:

- `quick` narrows inspection and labels skipped surfaces.
- `targeted` names the inspected surface and boundary.
- `exhaustive` adds an inspect-or-exclude coverage ledger.
- `with verification` runs only focused safe checks.
- `save report` writes only to an explicit or locally conventional path.
- `read-only` blocks edits.
- `apply accepted plan` applies only `Safe UX` items unless specific
  `Contract-risky` items are approved.

## Interaction Fit

Check whether the skill's interaction pattern matches the job:

- Interactive skills should ask one high-leverage question at a time.
- Explicit audit/review or `read-only` requests should produce read-only
  reports.
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
- References and behavior-shaping nearby files are loaded only when needed, and
  every referenced path exists.
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
- Clarifying already-stated stop conditions is safe UX; adding, removing, or
  changing stop-condition behavior is `Contract-risky`.

If preserving rigor requires a new output label, correction path, or clarification
of certification language, prefer that over removing the rigorous section.

## Opportunity Format

Use this shape for each fix:

```markdown
<rank>. <change> (Safe UX|Contract-risky)
User friction: <what the user has to decode, correct, wait through, or ask again>
Change shape: <exact replacement/addition/removal, or the file and section to edit>
Evidence: <file:line, file section, or not inspected + reason>
Rigor guardrail: <protected behavior that must remain true>
```

Evidence must be specific enough that the user can verify the claim cheaply. Use
file/line evidence when available, a named section when line numbers are not
available, or `not inspected` when the claim depends on a skipped surface. Do
not use vague impressions as evidence.

Mark a change `Contract-risky` when it touches trigger scope, non-trigger
boundaries, destructive-action gates, evidence standards, validation ladders,
authority precedence, permission and mutation rules, or added, removed, or
changed stop-condition behavior.

## Common Anti-Patterns

- Leading with a full evidence ledger before the result.
- Reporting abstract improvement themes without showing the text-level change.
- Saying `failed` when the result is really an uncertified investigation.
- Hiding inferred target, baseline, scope, or verification choices.
- Asking for approval again when the target is clear, the fix is low-risk, and
  the user did not request read-only behavior.
- Forcing users to know exact prompt wording to choose quick, targeted, saved,
  or verified modes.
- Replacing a rigorous packet with a summary instead of moving the packet below
  the summary.
- Adding a fixed scoring system when ranked judgment and evidence notes are
  enough.
- Treating metadata alignment as proof of runtime behavior.
