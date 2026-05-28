---
name: orient-status
description: Run a thorough read-only orientation of a project, codebase, repository, plugin, skill, or local work area to determine current status. Use when the user asks where things stand, what happened recently, what is in flight, what is next, where the target is on the roadmap, what decisions or open questions exist, what work is deferred, or how live state compares with handoffs, tickets, issues, PRs, roadmaps, specs, or status docs. Default to strict read-only, chat-only operation unless the user explicitly asks for an artifact or handoff output mode.
---

# Orient Status

## Core Contract

Default to strict read-only, chat-only orientation.

- Do not edit files, create artifacts, update handoffs, stage commits, run formatters, install dependencies, run normal verification, or mutate caches.
- Do not run commands that write local state, such as `git fetch`, package-manager installs, test/lint/build commands, or generated-report commands, unless the user explicitly widens scope.
- Use read-only inspection commands and tools, such as `pwd`, `ls`, `find`, `rg`, `sed`, `git status --short --branch`, `git branch --show-current`, `git log`, `git remote -v`, `git diff --stat`, and read-only issue/PR/ticket queries when available.
- If the user explicitly asks for `artifact` or `handoff` mode, perform the orientation first, then write only the requested output artifact. Do not edit source code unless the user separately asks for implementation.

Treat memory, handoffs, and prior summaries as context that can guide where to look, not as current truth. Verify drift-prone claims against live target state when feasible.
Inspect untracked paths by name first. Read untracked file contents only when they are directly status-relevant, such as an active local handoff or branch-specific evidence note.

## Discovery Ladder

Adapt this ladder to the target. Say when a source class is unavailable, skipped, or out of scope.

1. Identify the target type and boundary: repo, codebase, plugin, skill, package, docs tree, or other work area.
2. Read local instructions and metadata: `AGENTS.md`, README, manifests, package metadata, plugin metadata, skill metadata, and repo-specific status entry points.
3. Inspect live state: current directory, branch, worktree status, upstream/remotes if present, local diffs, branch-vs-base diffs, and recent local commits. On a non-main branch, inspect changed file names and recent branch commits before trusting older status docs.
4. Read current-status and open-work docs: files named like `current-state`, `status`, `reconciliation`, `tickets`, `roadmap`, `plans`, `todo`, `backlog`, or repo-specific equivalents.
5. Inspect ticket, issue, and PR systems if available and in scope. Prefer read-only local ticket files or connector/API queries; avoid refreshing local git state unless asked.
6. Read roadmap, spec, design, and plan docs to understand intended sequencing and acceptance boundaries.
7. Read handoffs as context, not authority. Re-anchor any handoff claim against live state before presenting it as current.
8. Summarize source conflicts, evidence gaps, and the recommended next step.

## Authority Order

When sources conflict, use this order by default:

1. Live working tree and branch state.
2. Tracked current-status and open-work docs.
3. Issue and ticket systems.
4. Recent commits and PRs.
5. Handoffs, roadmaps, specs, and plans as context only.

Call out conflicts explicitly. Do not silently reconcile stale docs, old handoffs, aspirational roadmap text, or inferred next steps into live truth.
If the current branch is ahead of the default branch, committed branch changes are part of the selected target's live state. When those branch changes update tickets, evidence, or plans without updating status/register docs, report a branch-vs-status publication conflict instead of flattening the branch evidence into mainline truth.

## Output Packet

Use this fixed packet by default. Keep sections concise. If a section has no evidence, write `None found` or `Not enough evidence`; do not omit the section.

- `Target`: Identify the target path/name, type, boundary, and source classes inspected.
- `Current State`: State branch/worktree/status-doc truth and the strongest current-status conclusion.
- `Recent Activity`: Summarize recent commits, PRs, ticket movement, handoff activity, or status-doc changes.
- `In Flight`: List active work, open branches, open tickets/issues/PRs, pending plans, or partial local changes.
- `Roadmap Position`: Explain where the target appears to sit against roadmap, plan, phase, milestone, or status docs.
- `Open Decisions`: Name unresolved choices, approval gates, ambiguous ownership, or decisions blocked on missing evidence.
- `Deferred Work`: Name explicitly deferred items, backlog rows, parked handoff items, or accepted follow-ups.
- `Source Conflicts`: Identify disagreements across live state, docs, tickets, PRs, handoffs, and roadmaps.
- `Evidence Gaps`: State what could not be checked, what sources were missing, and what would improve confidence.
- `Recommended Next Step`: Give the smallest high-leverage next action consistent with the evidence.

## Operating Notes

- Prefer exact file paths, branch names, commit hashes, ticket IDs, PR numbers, and dates over vague status language.
- Separate `confirmed-current`, `likely-current`, `stale-context`, and `unknown` claims.
- Treat untracked files and local diffs as in-flight evidence, not clutter, unless the user asks for cleanup.
- Read only the latest or explicitly relevant handoffs by default. Do not scan broad handoff archives unless the user asks or the active status trail directly depends on them.
- Keep the final answer focused on status and next action. Do not drift into implementation planning unless the user asks.
- If the target is materially ambiguous and multiple reasonable boundaries would change the answer, ask one clarifying question before inspecting broadly.

## Artifact And Handoff Modes

Use these modes only when the user explicitly requests them:

- `artifact`: Write or update a named orientation/status artifact after producing the same evidence-grounded packet. Keep the artifact narrow and avoid source edits.
- `handoff`: Prepare a handoff-style orientation using the relevant project or handoff workflow. Preserve the read-only investigation boundary unless the user explicitly asks to save or update the handoff file.
