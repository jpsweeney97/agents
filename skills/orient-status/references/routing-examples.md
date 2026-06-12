# Orient Status Routing Examples

Load this file when a request mixes status orientation with adjacent work, or
when the right lane is unclear from the trigger text alone.

## Use Orient Status

- User: "Where do things stand in `/repo`?"
  Behavior: Run read-only orientation and answer in chat.
- User: "Compare the current repo state with `docs/status/previous-status.md`."
  Behavior: Treat the named Markdown file as ordinary evidence, re-anchor claims
  against live state, and label stale or unverified claims.
- User: "Write a status note at `docs/status/current.md`."
  Behavior: Use `artifact` mode; run orientation, then write only that named
  status artifact.

## Orient First, Then Switch Only If Explicit

- User: "Where do things stand, and what should I do next?"
  Behavior: Give a compact status brief. If the user is asking you to choose or
  rank options, switch to `making-recommendations`; if they explicitly asked for
  an implementation plan, switch to the relevant implementation-planning lane.
  Use `next-steps` only when `/next-steps` or `$next-steps` was explicitly invoked.
- User: "Show current blockers, then clean up stale branches."
  Behavior: Give a compact status brief, then switch to git hygiene only if its
  preview, approval, and destructive-action gates are satisfied.
- User: "Where does this branch stand, and is it safe to hand off?"
  Behavior: Give a compact status brief for the branch state, then switch to
  `closeout-check` for the handoff-readiness proof gap because completion truth
  was explicitly requested.

## Do Not Use Orient Status As The Primary Lane

- User: "What is the baseline for this directory against the spec?"
  Better lane: `baseline`.
- User: "Review this implementation against the plan."
  Better lane: implementation review or the explicitly invoked review skill.
- User: "Is this done?", "Is this ready?", or "Close this out."
  Better lane: `closeout-check`.
- User: "What's the status of PR #42?"
  Better lane: a GitHub-focused skill, if one is available; otherwise note the
  limit. Use orient-status only if the PR is evidence for a broader local repo
  status brief.
- User: "What are the unresolved review threads on this PR?" or "Why is CI
  failing?"
  Better lane: a GitHub review-follow-up or CI-debugging skill, if one is
  available; otherwise note the limit.
- User: "Triage issue #42" or "Show repository issues that need attention."
  Better lane: `triage` or the repo's issue-tracker workflow.
- User: "List open tickets" or "triage the backlog."
  Better lane: ticket listing, search, review, or update skills, if available.
- User: "Show me open tickets."
  Better lane: ticket listing or search. If that lane is unavailable, say so
  and do not substitute a broad status orientation.
- User: "/load", "Continue from the latest handoff", or "Search handoffs for
  the deployment decision."
  Better lane: `handoff:load-handoff` or `handoff:search-handoffs`.
- User: "What did we decide about authentication?"
  Better lane: handoff search when the question is about prior handoff context;
  use orient-status only when the user asks how that decision compares with
  current project state.
