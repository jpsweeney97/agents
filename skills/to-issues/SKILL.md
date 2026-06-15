---
name: to-issues
description: "Use when the user wants to convert an existing plan, spec, PRD, or approved design into independently grabbable implementation issues and publish them to the project issue tracker. Do not use for creating the PRD/spec, implementation, issue triage, status orientation, recommendations, or next-step planning without issue publication."
---

# To Issues

Break a plan into independently-grabbable issues using vertical slices (tracer bullets).

The issue tracker and triage label vocabulary should have been provided to you.
If they are missing, use `/setup-matt-pocock-skills` or
`$setup-matt-pocock-skills` when that skill is available; otherwise ask the
smallest setup question needed before publishing.

## Side Effects And Proof Boundary

This skill publishes approved slices to the configured issue tracker. Do not
publish until the user has approved the slice breakdown or explicitly asked to
use an already-approved breakdown.

After publishing, report the created issue identifiers or URLs, parent links,
labels applied, source artifact used, and proof boundary. Issue publication
proves the tracker artifacts were created; it does not prove implementation,
acceptance satisfaction, or tracker state beyond the actions performed.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes an issue reference (issue number, URL, or path) as an argument, fetch it from the issue tracker and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Issue titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

### 3. Draft vertical slices

Break the plan into **tracer bullet** issues. Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Slices may be 'HITL' or 'AFK'. HITL slices require human interaction, such as an architectural decision or a design review. AFK slices can be implemented and merged without human interaction. Prefer AFK over HITL where possible.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?

Iterate until the user approves the breakdown.

### 5. Publish the issues to the issue tracker

For each approved slice, publish a new issue to the issue tracker. Use the issue body template below. Apply the triage label that matches the slice's Type: `ready-for-agent` for AFK slices, `ready-for-human` for HITL slices. Do not stamp every slice `ready-for-agent` — an HITL slice mislabeled that way can be grabbed by an autonomous agent that cannot do its human-in-the-loop work. (These canonical roles map to your tracker's label strings via the triage label vocabulary.)

Publish issues in dependency order (blockers first) so you can reference real issue identifiers in the "Blocked by" field.

<issue-template>
## Parent

A reference to the parent issue on the issue tracker (if the source was an existing issue, otherwise omit this section).

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- A reference to the blocking ticket (if any)

Or "None - can start immediately" if no blockers.

</issue-template>

Do NOT close or modify any parent issue.
