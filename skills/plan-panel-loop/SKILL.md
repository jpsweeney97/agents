---
name: plan-panel-loop
description: "Use when the user explicitly wants an iterative adversarial panel to review a specific plan, patch that plan, and re-review the patched result. Do not use for read-only scrutiny, unclear outcome shaping, routine editing, or implementation from a plan."
---

# Plan Panel Loop

Run a bounded plan-improvement loop: resolve the plan target, run a read-only adversarial panel, patch only the named plan, and re-review the patched result against carried-forward findings until the inspected scope is defensible or the loop hits a stop condition.

The panel should provoke sharper thinking; the patch loop may mutate a user artifact, so target resolution, edit boundaries, stop conditions, and proof language must be explicit.

## Trigger Boundary

Use this skill only when the user wants all three parts: adversarial panel review, plan patching, and re-review after the patch.

Do not use it for a read-only adversarial review; use `review-family:scrutinize` instead when that skill is available. Do not use it to clarify a muddy goal before there is a plan; hand off to the appropriate outcome or design workflow. Do not implement the plan itself.

If the user names a plan file or pasted plan and invokes this skill, treat patching that plan as authorized after you state the target and mutation boundary and no ambiguity remains. If the target is ambiguous, the plan is a folder with multiple plausible files, the user says read-only/no edits, or patching would touch anything beyond the named plan, ask one question before running the loop.

## First Move

Start by making the setup visible and cheap to correct:

- Target: the exact plan file, pasted plan, issue, PR body, or other artifact being reviewed. For issues, PR bodies, and other remote artifacts, default to a patch-shaped replacement in chat unless the user explicitly authorizes editing that remote surface.
- Authority: the plan's stated source of truth and any nearby context that controls whether a proposed patch is valid.
- Mutation boundary: what may be edited, what must stay untouched, and whether the final output is a file patch or a proposed replacement in chat.
- Loop cap: default to two review/patch/re-review cycles unless the user explicitly asks for more.
- Proof boundary: whether panel feedback came from subagents, separate model/tool calls, or a single-agent simulation.
- Reviewer containment: if subagents are used, state that they are read-only reviewers and may not edit files, launch nested panels, or change external state.

Read the plan in full before designing the panel. Read referenced context only when it can change a finding, patch, or stop decision; do not broaden into implementation research unless the plan itself depends on that authority.

## Panel Design

Choose lenses from the plan's real risk surfaces, not generic personalities. Good lenses usually map to the plan's concrete failure modes: source-of-truth drift, execution sequencing, proof and validation, user/operator experience, data or security boundaries, dependency risk, rollout/recovery, or maintainability.

Use three to five lenses by default. Fewer is fine for a narrow plan; more is fine only when the plan has genuinely separate risk surfaces. Do not rotate the panel merely for variety. Keep any lens whose prior finding remains unresolved, and add or replace a lens only when the next pass needs a new risk surface.

Each panel member needs a compact brief:

- the plan target and relevant authority
- the specific lens and what would falsify the plan from that lens
- any accepted findings from prior passes that must be rechecked
- an instruction to report no material issue when none is found
- an instruction not to invent hypothetical blockers unsupported by the plan or its authority

Ask reviewers for stable anchors from the current snapshot. Prefer heading or surrounding text plus current line numbers when available. Line numbers are useful evidence on the current snapshot, but the patching agent must re-read before editing because line numbers can drift.

Do not claim an independent panel if you did not actually run one. If no subagent or separate-call mechanism is available, run the lenses yourself, label the result as single-agent simulated panel feedback, and lower the proof claim accordingly.

When using subagents, read [references/subagent-brief.md](references/subagent-brief.md) and include its containment language in every reviewer prompt.

## Subagent Containment

Subagents are reviewers, not co-executors. The main agent alone consolidates findings, decides which findings are accepted, patches the artifact, stages or commits when repository policy requires it, and chooses whether another cycle is needed.

Every subagent reviewer brief must explicitly say:

- READ ONLY: do not edit files, apply patches, stage, commit, push, open PRs, create handoffs, or change external state.
- Do not launch other agents, panels, recursive reviews, or background workflows.
- Do not wait on other agents or make the loop depend on another reviewer.
- Read only the target and relevant authority needed for the assigned lens.
- Return one bounded review packet with verdict, material findings, evidence anchors, and no-file-change patch suggestions when useful.

Reviewers may reason adversarially, but they must not run `plan-panel-loop`, `review-family:scrutinize`, another adversarial panel, or any other multi-agent workflow inside their review.

Before dispatching subagents, snapshot the target artifact state with `git status --short --branch --untracked-files=all` when in a git worktree and, for file targets, a target-scoped diff command such as `git diff --name-only -- <target>`.

After every panel returns, times out, or is canceled, re-check the worktree and target artifact before consolidating findings. If any reviewer changed files or external state, stop the normal loop, inspect the diff or state change, label it as an unauthorized reviewer mutation, and decide explicitly whether to adopt it as the main patch, replace it, revert it with user approval when required, or ask the user. Do not launch the next panel until the artifact state is normalized.

If a reviewer runs long enough to block the loop, cancel or drop that reviewer, run the mutation audit, and record the missing lens. Continue only if the remaining panel still covers the material risk surfaces; otherwise launch one replacement reviewer with a narrower read-only brief. Do not wait indefinitely for a reviewer whose lens is already covered by other evidence.

## Loop Contract

1. Resolve the target, authority, mutation boundary, loop cap, and proof boundary.
2. Run the first pass as read-only scrutiny. If `review-family:scrutinize` is available and the target is an ordinary plan, use its standards for evidence, severity, and execution-readiness thinking. This skill adds panel composition and the patch/re-review loop; it does not replace scrutiny with a weaker review method.
3. Consolidate panel feedback before editing. Re-read the plan around each claim, discard unsupported issues, merge duplicates, and preserve disagreement when the correct patch depends on a user decision.
4. Track accepted findings as open until a later pass verifies them closed. A new panel cannot erase an older accepted finding by ignoring it.
5. Patch only the named plan artifact. Do not edit authority files, implementation files, tests, tickets, handoffs, or unrelated docs unless the user explicitly expands the mutation boundary. One further mutation class is authorized inside the named plan: recording a human-supplied `recheck-investment` ruling as a brief note, written only at the human's direction and scoped to the ruling's named boundary.
6. After patching, re-read the changed plan and re-review every open finding plus any new risk introduced by the patch.
7. Stop when a stop condition below is reached. Do not keep looping just because another panel could be invented.

## Finding Ledger

Maintain a carried-forward finding ledger during the run. Keep it lightweight, but make every material accepted finding traceable until closed:

- ID
- lens
- finding summary
- accepted, rejected, or needs user decision
- patch location or rejection evidence
- re-review status

A later panel's ready verdict is valid only if every accepted ledger item is closed or deliberately rejected with evidence. A new panel may add findings, but it cannot close an older accepted finding merely by omitting it.

## Patch Safety

When the target is a file, inspect the worktree state when a git worktree exists. Preserve user changes and patch around them. If the target file has unrelated edits that make the patch unsafe to apply confidently, stop and ask.

Keep the edit as small as the accepted findings allow. Prefer precise replacement over whole-file rewrite unless the plan is too structurally broken to patch locally. If the plan is pasted in chat, return a revised plan or patch-shaped replacement instead of implying a file was changed.

After any file edit, summarize the changed sections and run the smallest relevant validation available for the plan format. At minimum, run a whitespace/diff check when the file is in a git worktree. Follow host and repo instructions for staging or committing; when a Markdown auto-commit rule applies, stage only the Markdown files changed by this request and commit them.

## Stop Conditions

Stop with `defensible for inspected scope` only when every accepted material finding has either been patched or deliberately rejected with evidence, the re-review found no new material blocker, and the proof boundary is stated honestly.

Stop with `needs user decision` when findings conflict, the correct patch depends on priorities the plan does not settle, the target or authority is ambiguous, the mutation boundary would need to expand, or patching would risk overwriting unrelated work.

Stop with `iteration cap reached` when the default or user-specified cap is reached while material findings remain. Summarize the remaining findings and the smallest next decision rather than launching another panel.

When the cap is reached with material findings remaining, a third cycle is proposed without a lower cap, or the smallest responsible patch would add a new subsystem, trust boundary, persistent proof surface, or maintenance obligation, route the continue-question to `recheck-investment` (where available) before running another cycle or applying that patch. The named plan stays unpatched while that check runs; finding validity stays with this loop's panel, and the check owns only whether continued investment needs renewed human authorization.

Stop with `not patchable as given` when the plan lacks enough concrete goal, scope, authority, or execution shape for panel feedback to produce a responsible patch. Name the workflow that should clarify it next.

## Closeout

Close every run with a compact packet:

```markdown
Target: <artifact reviewed and patched>
Cycles run: <count and cap>
Panel proof: <subagents | separate model/tool calls | single-agent simulated>
Reviewer anomalies: <none | canceled/dropped reviewers | unexpected reviewer mutations and disposition>
Changed: <sections/files changed, or chat replacement only>
Resolved findings: <accepted findings closed>
Remaining findings / stop status: <none | needs user decision | iteration cap reached | not patchable as given>
Verified: <commands/checks/readbacks run>
Proof boundary: <what the checks and panel did not prove>
Next move: <none | user decision | another approved cycle | handoff workflow>
```

The closeout is a user-control surface, not a certificate. Structural checks prove structure; readbacks prove the edited source says what it says; only a realistic dry run or later implementation proof can show that the plan actually works.

## Example

See [examples/dry-run.md](examples/dry-run.md) for a compact worked run showing target setup, panel selection, patching, re-review, and bounded stop behavior.
