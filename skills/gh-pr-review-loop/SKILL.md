---
name: gh-pr-review-loop
description: >
  Use only when the user explicitly invokes `$gh-pr-review-loop` or explicitly
  asks for the full GitHub PR review-response loop: discover unresolved PR
  review threads, independently verify each comment, fix all real actionable
  issues, run focused verification, create one coherent commit when code changes
  are needed, push once, reply to and resolve appropriate threads, then request
  another `@codex review`. Do not use for ordinary "address comments" requests,
  first-pass PR reviews, CI debugging, issue triage, or GitHub comment summaries
  that do not authorize push, thread resolution, and re-review.
---

# GH PR Review Loop

Run an end-to-end PR-level review response for an open GitHub PR. This is an
orchestration skill: own the policy, evidence standards, checkpoints, and
publication order; use the GitHub app, `gh`, and existing GitHub
review-comment workflows for the mechanics when available.

## Boundaries

- Explicit-only: use this skill only when the user invokes
  `$gh-pr-review-loop` or clearly requests the full commit, push,
  reply/resolve, and re-review lifecycle.
- Full-loop authorization: explicit invocation authorizes local edits, one
  coherent commit when needed, one push, thread replies and resolution, and a
  top-level `@codex review` request when all checkpoint conditions are clear.
- Non-trigger: ordinary "address PR comments", comment summaries, first-pass PR
  reviews, CI triage, issue triage, or requests that do not clearly authorize
  GitHub write actions. Use the narrower `gh-address-comments` workflow for
  those cases when available.
- Scope: default to all unresolved review threads on the current or specified
  PR. Include top-level PR comments only when they are clearly review feedback
  the user wants handled in the same loop.
- Human-reviewer caution: verify and fix human-authored threads, but resolve
  them only when the thread is clearly mechanical or repo practice supports
  author resolution. Otherwise reply with evidence and leave the thread open.

## Preflight

1. Resolve the PR.
   - Use a supplied PR URL, repo and number, or the current branch PR.
   - Confirm the local branch is the PR head branch before committing or
     pushing. Checkpoint if the PR or head branch is not confidently identified.
2. Inspect local state.
   - Run `git status --short --branch`.
   - Checkpoint before publishing if unrelated dirty changes are present.
3. Fetch thread-aware review data.
   - Prefer the available GitHub app plus `gh` workflow, and use
     `gh-address-comments` or its thread-aware fetch path when available.
   - Do not treat flat PR comments as a complete source for unresolved review
     thread state, inline anchors, or resolution status.
4. If no unresolved review threads exist, report that no review-thread work is
   needed. Do not create an empty commit, push, resolve anything, or request
   `@codex review` unless the user explicitly asked for a fresh review request.

## Verify And Classify

Verify every unresolved thread independently before editing. Read the referenced
code, diff hunk, tests, docs, runtime behavior, or PR context needed to decide
whether the comment is real.

Classify each thread:

- `fixed`: real actionable issue fixed in this pass.
- `not-reproducible`: plausible concern could not be reproduced after named
  checks.
- `incorrect`: the claim contradicts inspected evidence.
- `already-addressed`: current PR head already handles the concern.
- `needs-user-decision`: the thread is ambiguous, conflicts with another
  requirement, needs product judgment, would broaden scope, or cannot be settled
  with available evidence.

Prepare a concise evidence-backed reply for every reviewed thread, but post
replies only during the publication step. Do not use `not-reproducible`,
`incorrect`, or `already-addressed` without a concrete evidence pointer such as
a file and line, command result, diff hunk, commit, or document section.

## Fixing Policy

- Fix all real actionable issues that can be addressed without a checkpoint.
- Keep changes traceable to the thread or cluster they address.
- Avoid unrelated refactors and opportunistic cleanup.
- Default to one coherent commit for the PR-level pass. Checkpoint before
  committing if verified fixes are unrelated enough that they would normally
  deserve separate commits.
- If any thread is `needs-user-decision`, stop before publishing. You may keep
  safe local fixes for unambiguous threads, but do not commit, push, resolve, or
  request re-review until the user decides.

## Verification

Before any push, thread resolution, or re-review request, run evidence tied to
the touched behavior:

- Run the narrowest meaningful tests or checks for the changed files and
  behavior.
- Also run any cheap, established repo-standard quick check when one exists.
- Do not wait for remote CI unless the user asks or the repo's normal review
  loop depends on it.

Checkpoint instead of publishing when verification fails, is skipped, cannot be
identified, or only covers an unrelated surface.

## Publication Order

When all publish preconditions hold:

1. Review `git diff --stat` and the relevant diff.
2. If code changed, create one coherent commit summarizing the review-response
   scope. Do not create an empty commit.
3. If a commit was created, push once to the PR head branch.
4. Reply to every reviewed thread with its disposition and concise evidence.
5. Resolve appropriate threads:
   - Resolve bot/Codex threads classified as `fixed`, `incorrect`,
     `already-addressed`, or strongly evidenced `not-reproducible`.
   - Resolve human-authored threads only when clearly mechanical or normal for
     the repo; otherwise reply and leave open.
   - Never resolve `needs-user-decision` threads.
6. If all review threads are resolved and the PR is otherwise ready, post a new
   top-level PR comment exactly containing `@codex review`, unless repo
   documentation specifies a different trigger. Do not include the trigger in
   per-thread replies.

No-code-change path: when all threads classify as `incorrect`,
`already-addressed`, or strongly evidenced `not-reproducible`, skip commit and
push, then reply, resolve eligible threads, and request `@codex review` only if
all threads are resolved and the PR is otherwise ready.

## Checkpoints

Stop and ask before committing, pushing, resolving, or requesting re-review when
any of these apply:

- The PR or head branch cannot be confidently resolved.
- Unrelated dirty worktree changes make safe staging ambiguous.
- A thread is ambiguous, contradictory, too broad, or classified
  `needs-user-decision`.
- Fixes span unrelated areas that may need separate commits.
- Verification fails, is skipped, or cannot be matched to the touched behavior.
- GitHub authentication, rate limits, missing permissions, or tool failures make
  thread state or write actions uncertain.
- Human-thread resolution is socially or procedurally unclear.

At a checkpoint, summarize thread dispositions, local changes, verification
status, and the exact decision needed.

## Final Response

Report:

- Threads handled and their dispositions.
- Files changed and commit hash, when a commit was created.
- Push target, when pushed.
- Verification commands and results.
- Threads replied to, resolved, or intentionally left open.
- Whether a top-level `@codex review` request was posted.
