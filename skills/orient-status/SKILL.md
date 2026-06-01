---
name: orient-status
description: "Run a read-only orientation of a project, codebase, repository, plugin, skill, or local work area to determine current status, in-flight work, source conflicts, and freshness limits. Use when the user asks where things stand, what happened recently, what is in flight, what is blocked, where the target sits against status or roadmap context, or how live state compares with handoffs, tickets, issues, PRs, roadmaps, specs, or status docs. Do not use for explicit drift audits, code review, cleanup, branch landing, implementation/debugging, next-step planning, backlog prioritization, ticket listing/search/triage, or handoff save/load/list/update unless the user also asks for broader status orientation."
---

# Orient Status

## Core Contract

Default to strict read-only, chat-only orientation.

- Do not edit files, create artifacts, update handoffs, stage commits, run formatters, install dependencies, run normal verification, or mutate caches.
- Do not run commands that write local state, such as `git fetch`, package-manager installs, test/lint/build commands, or generated-report commands, unless the user explicitly widens scope.
- Use read-only inspection commands and tools, such as `pwd`, `ls`, `find`, `rg`, `sed`, `git status --short --branch`, `git branch --show-current`, `git log`, `git remote -v`, `git diff --stat`, and read-only issue/PR/ticket queries when in scope.
- Write files only in explicit artifact or handoff-save mode, and only after the orientation. Do not edit source code unless the user separately asks for implementation.

Treat memory, handoffs, and prior summaries as context that can guide where to look, not as current truth. Verify drift-prone claims against live target state when feasible.

If routing is ambiguous, read [routing-examples.md](references/routing-examples.md)
before deciding whether to use orient-status or a narrower lane.

## Trigger Boundaries

Use this skill for status orientation:

- Current state, recent activity, in-flight work, blockers, open decisions, deferred work, source conflicts, roadmap position, or live-vs-handoff/status-doc comparisons.

Do not use this skill as the primary lane for:

- Explicit drift or baseline-vs-live audits; use a drift-audit skill instead.
- Code review, implementation review, plan scrutiny, or security review.
- Branch cleanup, branch landing, repo hygiene, staging, committing, pushing, or publishing.
- Implementation, debugging, test fixing, verification runs, or dependency work.
- Next-step planning, backlog prioritization, or "what should I work on next" analysis.
- Ticket listing, ticket search, ticket lookup, close-readiness checks, ticket backlog triage, or ticket create/update/close/reopen operations.
- Handoff save, load, resume, list, update, or `/triage` operations.

Use tickets and handoffs as evidence only when the user is asking for a broader
project, repo, or work-area status brief. If the user's primary object is the
ticket system, handoff system, backlog, or triage queue itself, name the narrower
lane and do not run orient-status as the primary skill.

For mixed requests, use orient-status only for the orientation part. If the same
user message explicitly asks for a second deliverable, such as a recommendation,
plan, cleanup, ticket operation, implementation, verification run, or saved
handoff, first give a compact status brief, then switch to the named adjacent
lane only if that lane's rules and mutation gates allow it. If the adjacent work
was not explicitly requested, name the lane and stop.

## Discovery Ladder

Adapt this ladder to the target. Say when a source class is unavailable, skipped, or out of scope.

1. Identify the target type and boundary: repo, codebase, plugin, skill, package, docs tree, or other work area.
2. Read local instructions and metadata: `AGENTS.md`, README, manifests, package metadata, plugin metadata, skill metadata, and repo-specific status entry points.
3. Inspect live state: current directory, branch, worktree status, upstream/remotes if present, local diffs, branch-vs-base diffs, and recent local commits. On a non-main branch, inspect changed file names and recent branch commits before trusting older status docs.
4. Read current-status and open-work docs: files named like `current-state`, `status`, `reconciliation`, `tickets`, `roadmap`, `plans`, `todo`, `backlog`, or repo-specific equivalents.
5. Inspect ticket, issue, and PR systems only when they are evidence for the broader status question. Prefer read-only local files first. Use read-only connector/API queries when the user names a remote PR, issue, branch, or publication state, or when the status conclusion materially depends on remote truth. Do not refresh local git state unless asked.
6. Read roadmap, spec, design, and plan docs to understand intended sequencing and acceptance boundaries.
7. Read handoffs as context, not authority. Re-anchor any handoff claim against live state before presenting it as current.
8. Summarize source conflicts, evidence gaps, and the strongest supported status conclusion.

## Freshness Labels

Do not use unqualified `current` for a claim whose source could be stale.
Attach a freshness label when it affects the conclusion:

- `confirmed-current`: directly checked against the live target in this turn.
- `local-only`: checked in the local checkout or local refs, with no remote/API refresh.
- `remote-unrefreshed`: remote, PR, or issue state matters but was not refreshed.
- `connector-unavailable`: the relevant ticket, issue, PR, runtime, or app connector was unavailable, unauthenticated, or failed.
- `stale-context`: memory, handoff, old status doc, or prior summary was not re-anchored.
- `unknown`: the source class was not inspected.

If remote truth matters and scope forbids refresh, say what local evidence shows
and what command or connector query would raise confidence.

Default to local-only status orientation unless the user names remote state or
remote truth materially affects the conclusion. Read-only connector/API queries
are allowed in that case when available. If they fail or are unavailable, label
the affected claims `connector-unavailable` or `remote-unrefreshed`; do not
substitute stale local refs for confirmed remote state.

## Claim-Specific Authority

Resolve authority by claim type instead of applying one global source order:

- File and worktree state: live files, `git status`, and local diffs outrank docs.
- Branch publication state: current branch, upstream configuration, remote refs, and PR queries if inspected.
- Intended scope, roadmap, or acceptance state: active/current specs, status docs, roadmap docs, and explicit user direction outrank branch inference.
- Open work: ticket, issue, and PR systems outrank stale handoffs; tracked status docs can outrank them only when they explicitly declare current ownership.
- Runtime or installed state: live runtime inspection, installed cache inspection, or task-specific runtime queries outrank source metadata. Metadata alone is not runtime proof.
- History and rationale: git log, handoffs, old plans, and prior summaries explain why the state changed; they do not prove current state unless re-anchored.

Call out conflicts explicitly. Do not silently reconcile stale docs, old handoffs, aspirational roadmap text, or inferred action items into live truth.
If the current branch is ahead of the default branch, committed branch changes are part of the selected target's live state. When those branch changes update tickets, evidence, or plans without updating status/register docs, report a branch-vs-status publication conflict instead of flattening the branch evidence into mainline truth.

## Untracked And Ignored Paths

Treat untracked files and local diffs as in-flight evidence, not clutter, unless
the user asks for cleanup.

- Inspect untracked paths by name first. Read untracked file contents only when they are directly status-relevant, such as an active local handoff or branch-specific evidence note.
- Skip ignored paths by default. Inspect or disclose ignored state when the user asks about cleanliness, residue, generated evidence, environment status, or anything where ignored files could change the answer.
- If ignored paths were skipped and could affect the status conclusion, list them as an evidence gap or suggest the exact read-only ignored-status check.

## Output Packet

Default chat output starts with a `Status Brief`. The brief must include:

- `Bottom Line`: strongest current-status conclusion.
- `Current State`: branch/worktree/status-doc truth in one sentence, with freshness labels where needed.
- `Active Blocker`: current blocker or `None found`.
- `Confidence / Limits`: what was checked and what could change the conclusion.

Under `Details`, adapt the packet to the size of the request. Broad orientation
should use the full packet below. Narrow status checks may compress irrelevant
sections, but must still name the target, inspected source classes, source
conflicts, and evidence gaps.

- `Target`: Identify the target path/name, type, boundary, and source classes inspected.
- `Current State`: State branch/worktree/status-doc truth and the strongest current-status conclusion.
- `Recent Activity`: Summarize recent commits, PRs, ticket movement, handoff activity, or status-doc changes.
- `In Flight`: List active work, open branches, open tickets/issues/PRs, pending plans, or partial local changes.
- `Roadmap Position`: Explain where the target appears to sit against roadmap, plan, phase, milestone, or status docs.
- `Open Decisions`: Name unresolved choices, approval gates, ambiguous ownership, or decisions blocked on missing evidence.
- `Deferred Work`: Name explicitly deferred items, backlog rows, parked handoff items, or accepted follow-ups.
- `Source Conflicts`: Identify disagreements across live state, docs, tickets, PRs, handoffs, and roadmaps.
- `Evidence Gaps`: State what could not be checked, what sources were missing, and what would improve confidence.

If a full-packet section has no evidence, write `None found` or `Not enough
evidence`; do not omit it in broad orientation mode. If the user asks for
implementation, cleanup, verification, planning, prioritization, or ticket or
handoff operations, apply the mixed-request rule above instead of letting the
status brief expand into that work by implication.

## Operating Notes

- Prefer exact file paths, branch names, commit hashes, ticket IDs, PR numbers, and dates over vague status language.
- Read only the latest or explicitly relevant handoffs by default. Do not scan broad handoff archives unless the user asks or the active status trail directly depends on them.
- Keep the final answer focused on status, blockers, conflicts, and evidence limits. Do not drift into recommendations or implementation planning unless the user asks.
- If the target is materially ambiguous and multiple reasonable boundaries would change the answer, ask one clarifying question before inspecting broadly.

## Artifact And Handoff Modes

Use these modes only when the user explicitly requests them:

- `artifact`: Write or update only the named orientation/status artifact after
  producing the evidence-grounded packet. If the user asks for an artifact but
  gives no destination and no repo convention resolves it, ask one path question
  before writing. Do not update source code, handoff files, tickets, indexes, or
  generated reports as a side effect.
- `handoff-style`: Produce a handoff-shaped status brief in chat only. Use this
  when the user asks to prepare, draft, or format a handoff-style orientation but
  does not explicitly ask to save or update a handoff file.
- `handoff-save`: Save or update a handoff only when the user explicitly asks to
  save, write, update, or run the relevant handoff workflow. Keep the orientation
  investigation read-only, then switch to that handoff workflow for the file
  mutation. Do not treat broad status orientation as permission to mutate
  handoff artifacts.
