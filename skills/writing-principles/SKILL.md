---
name: writing-principles
description: "Use when writing, reviewing, or editing Codex instruction docs: AGENTS.md, SKILL.md, skill references, and agents/*.md."
---

# Writing Principles

Codex-only quality gate for instruction documents.

## Scope

Use for `**/AGENTS.md`, `**/skills/**/SKILL.md`, `**/skills/**/*.md`, and `**/agents/*.md`.

Do not use for user-facing docs, conversational replies, code comments, or creative writing.

## Workflow

1. Classify mode:
   - Review-only: report violations; do not edit.
   - Edit/refactor/create: make scoped edits; then report.
2. Calibrate risk:
   - Low: personal, reversible, under 50 lines.
   - Medium: project defaults, coordination, 50-150 lines.
   - High: multi-agent, destructive/downstream, over 150 lines.
   - Unclear: Medium.
3. Apply the principles:
   - Specific, terms, examples, interpretation, boundaries, failures, defaults, preconditions, loopholes, front-loading, grouping, parallelism, outcomes, economy.
4. Verify:
   - Low: passes 1-3.
   - Medium: passes 1-6.
   - High: passes 1-10, items 1-53.
5. Report:
   - Review-only: start with `Result Brief` grouped as `Blocking`,
     `High-Leverage`, `Polish`, and `No Action`; then `Details` with
     `"[Principle #X]: [description] at [location]"`, then wait.
   - Edit/refactor/create: start with one result line, then what changed, why,
     verification, remaining risks.

Load `references/writing-principles.md` for Medium/High risk work, explicit
audits, unclear violations, or full self-checks.

## Hard Rules

- Explicit edit requests override the review-only wait gate.
- Do not ask before fixing when the user requested edits.
- Stop and ask when target, scope, or authority is missing.
- Follow higher-priority instructions when rules conflict; report unresolved conflicts.
- Do not expand scope to unrelated instruction files.
