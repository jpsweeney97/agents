---
name: orient-status
description: "Run a read-only orientation of a project, codebase, repository, plugin, skill, or local work area to determine current status, in-flight work, source conflicts, and freshness limits. Use when the user asks where things stand, what happened recently, what is in flight, what is blocked, where the target sits against status or roadmap context, or how live state compares with named docs, tickets, issues, PRs, roadmaps, specs, or status docs. Do not use for explicit source-of-truth, baseline, or baseline-vs-live authority questions, code review, completion/readiness/closeout truth, GitHub-focused PR/issue/repo triage, handoff load/save/search/resume/list/update, cleanup, branch landing, implementation/debugging, next-step planning, backlog prioritization, or ticket listing/search/triage unless the user also asks for broader status orientation."
---

# Orient Status

## Core Contract

Default to strict read-only, chat-only orientation.

- Do not edit files, create artifacts, stage commits, run formatters, install dependencies, run normal verification, or mutate caches.
- Do not run commands that write local state, such as `git fetch`, package-manager installs, test/lint/build commands, or generated-report commands, unless the user explicitly widens scope.
- Use read-only inspection commands and tools, such as `pwd`, `ls`, `find`, `rg`, `sed`, `git status --short --branch`, `git branch --show-current`, `git log`, `git remote -v`, `git diff --stat`, and read-only issue/PR/ticket queries when in scope.
- Write files only in explicit artifact mode, and only after the orientation. Do not edit source code unless the user separately asks for implementation.

Treat memory, older notes, and prior summaries as context that can guide where to look, not as current truth. Verify drift-prone claims against live target state when feasible.

If routing is ambiguous, read [routing-examples.md](references/routing-examples.md)
before deciding whether to use orient-status or a narrower lane.

## Trigger Boundaries

Use this skill for status orientation:

- Current state, recent activity, in-flight work, blockers, open decisions, deferred work, source conflicts, roadmap position, or live-vs-status-doc comparisons.

Do not use this skill as the primary lane for:

- Explicit source-of-truth, baseline, or baseline-vs-live authority questions;
  use the baseline skill instead.
- Code review, implementation review, plan scrutiny, or security review.
- Completion truth, readiness, or proof-gap closeout questions such as "is this
  done?", "is this ready?", "is this verified?", "safe to hand off?", or "close
  this out"; use `closeout-check`.
- GitHub-focused repository, PR, or issue summaries; review-thread status; CI
  status; labels, comments, or reactions; and repository triage. Use `github` or
  its specialist skills unless GitHub state is only evidence for a broader local
  status brief.
- Handoff load, save, search, resume, list, or update operations, including
  `/load`, `/save`, "continue from handoff", "search handoffs", and "what did
  we decide"; use the handoff skills.
- Branch cleanup, branch landing, repo hygiene, staging, committing, pushing, or publishing.
- Implementation, debugging, test fixing, verification runs, or dependency work.
- Next-step planning, backlog prioritization, or "what should I work on next" analysis.
- Ticket listing, ticket search, ticket lookup, close-readiness checks, ticket backlog triage, or ticket create/update/close/reopen operations.

Use tickets, issues, PRs, handoffs, and named status/source documents as
evidence only when the user is asking for a broader project, repo, or work-area
status brief. If the user's primary object is the ticket system, issue tracker,
PR, review thread, CI check, handoff archive, backlog, or triage queue itself,
name the narrower lane and do not run orient-status as the primary skill.

For mixed requests, use orient-status only for the orientation part. If the same
user message explicitly asks for a second deliverable, such as a recommendation,
plan, cleanup, closeout/readiness check, GitHub operation, handoff operation,
ticket operation, implementation, verification run, or other non-status action,
first give a compact status brief, then switch to the named adjacent lane only
if that lane's rules and mutation gates allow it. If the adjacent work was not
explicitly requested, name the lane and stop.

If a narrower lane is unavailable, name that limit and keep the answer inside
orient-status. Do not approximate ticket, GitHub, handoff, closeout, cleanup,
review, audit, or planning workflows under a status-orientation label.

## Discovery Ladder

Adapt this ladder to the target. Say when a source class is unavailable, skipped, or out of scope.

1. Identify the target type and boundary: repo, codebase, plugin, skill, package, docs tree, or other work area.
2. Read local instructions and metadata: `AGENTS.md`, README, manifests, package metadata, plugin metadata, skill metadata, and repo-specific status entry points.
3. Inspect live state: current directory, branch, worktree status, upstream/remotes if present, local diffs, branch-vs-base diffs, and recent local commits. Identify the default/base branch from explicit user direction, repo instructions, existing local remote-HEAD metadata, or a single obvious local default branch; do not fetch solely to identify it unless the user authorizes refresh. On a branch other than the verified default/base branch, inspect changed file names and recent branch commits before trusting older status docs. If the default/base branch cannot be identified locally and branch context matters, say so as an evidence gap.
4. Read current-status and open-work docs: files named like `current-state`, `status`, `reconciliation`, `tickets`, `roadmap`, `plans`, `todo`, `backlog`, or repo-specific equivalents.
5. Inspect ticket, issue, handoff, and PR systems only when they are evidence for the broader status question. If the primary target is a GitHub repo, PR, issue, review thread, or CI state, route to `github` or its specialist skills before running this ladder. Prefer read-only local files first. Use read-only connector/API queries when the user names a remote PR, issue, branch, or publication state, or when the status conclusion materially depends on remote truth. Do not refresh local git state unless asked.
6. Read roadmap, spec, design, and plan docs to understand intended sequencing and acceptance boundaries.
7. Read older notes and status summaries as context, not authority. Re-anchor any stale claim against live state before presenting it as current.
8. Summarize source conflicts, evidence gaps, and the strongest supported status conclusion.

For large targets, start bounded: inspect the named path or repo root,
instructions, branch/worktree state, recent commits, and the most directly
named or discoverable status sources. Expand into tickets, issues, PRs,
roadmaps, note archives, or broad doc searches only when the user's question
depends on them. If the status conclusion would change with omitted sources,
mark those sources as evidence gaps instead of silently expanding forever.

## Freshness Labels

Do not use unqualified `current` for a claim whose source could be stale.
Attach a freshness label when it affects the conclusion:

- `confirmed-current`: directly checked against the live target in this turn
  for the stated source class, such as local files, remote PR state, or runtime
  state. Do not use it to imply uninspected source classes are also current.
- `local-only`: checked in the local checkout or local refs, with no remote/API refresh.
- `remote-unrefreshed`: remote, PR, or issue state matters but was not refreshed.
- `connector-unavailable`: the relevant ticket, issue, PR, runtime, or app connector was unavailable, unauthenticated, or failed.
- `stale-context`: memory, older note, old status doc, or prior summary was not re-anchored.
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
- Open work: ticket, issue, and PR systems outrank stale notes; tracked status docs can outrank them only when they explicitly declare current ownership.
- Runtime and install-surface state: live runtime inspection outranks source
  metadata for runtime claims. Installed cache or copied-surface inspection
  applies only to plugin, marketplace, distributed-copy, or other install-surface
  claims. Metadata alone is not runtime or install-surface proof.
- History and rationale: git log, old plans, status notes, and prior summaries explain why the state changed; they do not prove current state unless re-anchored.

Call out conflicts explicitly. Do not silently reconcile stale docs, old notes, aspirational roadmap text, or inferred action items into live truth.
If the current branch is ahead of the default branch, committed branch changes are part of the selected target's live state. When those branch changes update tickets, evidence, or plans without updating status/register docs, report a branch-vs-status publication conflict instead of flattening the branch evidence into mainline truth.

## Untracked And Ignored Paths

Treat untracked files and local diffs as in-flight evidence, not clutter, unless
the user asks for cleanup.

- Inspect untracked paths by name first. Read untracked file contents only when they are directly status-relevant, such as an active local note or branch-specific evidence note.
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
- `Recent Activity`: Summarize recent commits, PRs, ticket movement, note activity, or status-doc changes.
- `In Flight`: List active work, open branches, open tickets/issues/PRs, pending plans, or partial local changes.
- `Roadmap Position`: Explain where the target appears to sit against roadmap, plan, phase, milestone, or status docs.
- `Open Decisions`: Name unresolved choices, approval gates, ambiguous ownership, or decisions blocked on missing evidence.
- `Deferred Work`: Name explicitly deferred items, backlog rows, parked note items, or accepted follow-ups.
- `Source Conflicts`: Identify disagreements across live state, docs, tickets, PRs, status notes, and roadmaps.
- `Evidence Gaps`: State what could not be checked, what sources were missing, and what would improve confidence.

If a full-packet section has no evidence, write `None found` or `Not enough
evidence`; do not omit it in broad orientation mode. If the user asks for
implementation, cleanup, closeout/readiness, verification, planning,
prioritization, GitHub operations, handoff operations, ticket operations, or
other non-status actions, apply the mixed-request rule above instead of letting
the status brief expand into that work by implication.

## Operating Notes

- Prefer exact file paths, branch names, commit hashes, ticket IDs, PR numbers, and dates over vague status language.
- Read only the latest or explicitly relevant status notes by default. Do not scan broad note archives unless the user asks or the active status trail directly depends on them.
- Keep the final answer focused on status, blockers, conflicts, and evidence limits. Do not drift into recommendations or implementation planning unless the user asks.
- If the target is materially ambiguous and multiple reasonable boundaries would change the answer, ask one clarifying question before inspecting broadly.

## Artifact Mode

Use this mode only when the user explicitly requests it:

- `artifact`: Write or update only the named orientation/status artifact after
  producing the evidence-grounded packet. If the user asks for an artifact but
  gives no destination and no repo convention resolves it, ask one path question
  before writing. Do not update source code, tickets, indexes, or
  generated reports as a side effect. After writing or updating the artifact,
  report the absolute path and proof boundary; do not broaden into source edits,
  commits, normal verification, or other workflow actions.
