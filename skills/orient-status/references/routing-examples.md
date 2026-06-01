# Orient Status Routing Examples

Load this file when a request mixes status orientation with adjacent work, or
when the right lane is unclear from the trigger text alone.

## Use Orient Status

- User: "Where do things stand in `/repo`?"
  Behavior: Run read-only orientation and answer in chat.
- User: "Compare the current repo state with the latest handoff."
  Behavior: Use handoffs as evidence, re-anchor claims against live state, and
  label stale or unverified claims.
- User: "Write a status note at `docs/status/current.md`."
  Behavior: Use `artifact` mode; run orientation, then write only that named
  status artifact.

## Orient First, Then Switch Only If Explicit

- User: "Where do things stand, and what should I do next?"
  Behavior: Give a compact status brief, then switch to the appropriate planning
  or recommendation lane because the second deliverable was explicit.
- User: "Show current blockers, then clean up stale branches."
  Behavior: Give a compact status brief, then switch to git hygiene only if its
  preview, approval, and destructive-action gates are satisfied.

## Do Not Use Orient Status As The Primary Lane

- User: "Audit this directory for drift against the spec."
  Better lane: `drift-audit`.
- User: "Review this implementation against the plan."
  Better lane: implementation review or the explicitly invoked review skill.
- User: "List open tickets" or "triage the backlog."
  Better lane: ticket listing, search, review, or update skills.
- User: "Save a handoff for this session."
  Better lane: the relevant handoff save workflow.
- User: "Show me open tickets."
  Better lane: ticket listing or search. If that lane is unavailable, say so
  and do not substitute a broad status orientation.

## Handoff Distinction

- User: "Give me a handoff-style status brief."
  Behavior: Use `handoff-style`; answer in chat only.
- User: "Save/update the handoff file after the status brief."
  Behavior: Run orientation, then switch to `handoff-save` for the explicit file
  mutation.
