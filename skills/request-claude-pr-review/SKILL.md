---
name: request-claude-pr-review
description: >
  Generate a ready-to-send prompt for Claude Code to review a GitHub pull
  request. Use when the user asks for a Claude PR review prompt, a prompt to
  request PR review, or a review brief for Claude Code.
---

# Request Claude PR Review

Produce a prompt the user can give to Claude Code for a rigorous PR review.
Do not perform the review yourself unless the user asks separately.

## Boundaries

- Output one copyable prompt for Claude Code.
- Assume Claude Code can access the same local files, shell, and GitHub
  authorization as Codex unless the user says otherwise.
- Prefer live repo and PR context over conversation history.
- Do not edit files, stage, commit, push, or change the PR.
- The generated Claude prompt must also be review-only: tell Claude Code not to
  edit files, stage, commit, push, merge, close or reopen the PR, comment on
  GitHub, or otherwise mutate repository or PR state unless the user separately
  asks Claude to do that.
- If the review target cannot be inferred from the current repo or user request,
  ask one targeted question before drafting the prompt.
- If repo or GitHub context is unavailable, say exactly what is missing and ask
  one targeted question instead of drafting a confident prompt from partial data.

## Context To Gather

Run only the checks needed to anchor the prompt:

1. `git status --short --branch`
2. `git rev-parse --show-toplevel`
3. `git rev-parse HEAD`
4. `gh pr view --json <fields>` when a PR is active or a PR number is provided.
   Required fields: `number`, `title`, `url`, `body`, `baseRefName`,
   `headRefName`, `baseRefOid`, `headRefOid`, `isDraft`, `changedFiles`,
   `additions`, `deletions`, and `statusCheckRollup`.
5. `gh pr diff <number> --name-only` or `git diff --name-only <base>...HEAD`
   for changed-file scope.
6. `git diff --stat <base>...HEAD` for local PR size when the local branch and
   PR head match. Otherwise use the PR `changedFiles`, `additions`, and
   `deletions` metadata and say local stat was not authoritative.

If there are local uncommitted changes, distinguish them from the PR diff. Tell
Claude Code the exact dirty paths and whether each is included in the PR diff.
Tell Claude not to review local dirty files unless they are part of the PR or
the user explicitly asks for local-state hygiene review.

Compare local `HEAD` with the PR `headRefOid` when both are available. If they
do not match, include both values in the prompt, warn that the local checkout may
not represent the PR head, and tell Claude to review the PR head from GitHub
metadata or stop and report the mismatch if it cannot access that revision.

When the repo has obvious authority documents for the review, include them as
anchors. Examples: `AGENTS.md`, the PR body, a named implementation plan, a
spec, a ticket, or PR-specific docs. Do not invent anchors that are not present
or relevant. If an expected anchor is missing or unreadable, include that as an
evidence gap in the generated prompt.

## Prompt Requirements

The generated Claude prompt should include:

- PR URL, number, title, base branch, head branch, draft status, PR head SHA,
  current local `HEAD`, and whether local `HEAD` matches the PR head when
  available.
- The main review objective in the user's words.
- A review-only boundary that forbids edits, staging, commits, pushes, merges,
  GitHub comments, or PR state changes.
- A local-state section: dirty paths, which dirty paths are in the PR diff, and
  whether Claude should exclude them.
- Specific files or documents Claude should read first.
- Review aspects, ordered from highest-value domain concerns to general
  correctness.
- Suggested commands for Claude to gather live evidence, including commands that
  re-check repo, PR, and revision identity before reviewing.
- Failure behavior: if Claude cannot access the repo, PR, PR head SHA, or named
  authority documents, it should report the gap before reviewing rather than
  rely on summaries.
- Output format that leads with findings, ordered by severity.
- A request for file and line references, evidence gaps, open questions, test
  gaps, and a final verdict.

Prefer review prompts that ask Claude to verify claims against live files and
GitHub metadata rather than relying on summaries.

## Prompt Skeleton

Use this structure unless the user asks for a different shape:

```markdown
Review PR <number>: <title>

Target:
- PR: <url>
- Base: <baseRefName>
- Head: <headRefName>
- PR head SHA: <headRefOid>
- Local HEAD: <local HEAD>
- Local HEAD matches PR head: <yes/no/unknown>
- Draft: <true/false>

Boundary:
- Review only. Do not edit files, stage, commit, push, merge, comment on
  GitHub, close/reopen the PR, or mutate repository or PR state.
- If repo, PR, revision, or authority-doc access is missing, stop and report the
  gap before reviewing.

Local state:
- Dirty paths: <none/list>
- Dirty paths in PR diff: <none/list/unknown>
- Exclude dirty local-only paths unless explicitly asked to review local hygiene.

Read first:
- <authority docs, PR body, plans, specs, tickets, or AGENTS.md paths>

Review objective:
- <user's objective in their words>

Review focus, in order:
1. <domain-specific requirements and failure modes>
2. <plan/spec compliance>
3. <code correctness, regressions, tests, and operational risk>

Suggested evidence commands:
- `git status --short --branch`
- `git rev-parse HEAD`
- `gh pr view <number> --json <required fields from the prompt>`
- `gh pr diff <number> --name-only`

Output:
- Lead with findings ordered by severity.
- For each finding, include file/line references, evidence, impact, and the
  smallest credible fix.
- Include evidence gaps, open questions, test gaps, and a final verdict.
```

## Output Shape

Return a short lead-in sentence and then one fenced Markdown block containing
the full prompt.

The prompt itself should be direct and self-contained. It should not mention
this skill or Codex's internal reasoning.
