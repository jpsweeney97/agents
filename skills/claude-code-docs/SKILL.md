---
name: claude-code-docs
description: "Search and cite official Claude Code documentation through the claude-code-docs MCP server. Use for Claude Code setup, commands, hooks, agents, plugins, MCP, settings, IDE/CI, troubleshooting, and changelog questions, including asks like PreToolUse schema, plugin marketplace install, /mcp settings, or Claude Code changelog. Do not use for Claude API, Anthropic SDK, general programming, or non-Claude-Code product questions."
---

# Claude Code Docs

Search indexed Claude Code documentation and answer from retrieved results only.

## When to Use

Use this skill when the user needs grounded, current Claude Code documentation, such as:

- Configuration syntax, field names, or schemas
- Setup and installation questions
- Claude Code commands, hooks, agents, plugins, MCP, settings, IDE/CI, troubleshooting, or changelog questions
- Requests that benefit from `chunk_id` and `source_file` citations or explicit documentation coverage checks

Trigger examples:

- `What does PreToolUse return in Claude Code hooks?`
- `How do I configure /mcp in Claude Code?`
- `What changed in the Claude Code changelog?`

## When Not to Use

Do not use this skill for:

- Claude API or Anthropic SDK questions
- General programming or debugging questions unrelated to Claude Code documentation
- Non-Claude-Code product questions

Non-trigger examples:

- `How do I use the Anthropic Python SDK?`
- `Help me debug this React component`

## Default Execution Path

1. Classify the question.
   - If it is a single focused Claude Code docs question, answer inline.
   - If it spans multiple documentation areas or will likely require 3 or more searches, use the inline broad-query path below by default.
   - Delegate to `claude-code-docs-researcher` only when a compatible agent mechanism is actually available and the user explicitly asked for or approved delegation.
2. Confirm the tool surface.
   - In Codex, the expected MCP namespace is `mcp__claude_code_docs`, with `search_docs`, `reload_docs`, and `get_status`.
   - If `mcp__claude_code_docs.search_docs` is not visible, use `tool_search` for `claude-code-docs search_docs`.
   - If discovery still does not expose a search tool, say that authoritative Claude Code documentation lookup is unavailable in the current tool surface.
3. Run `mcp__claude_code_docs.get_status` first when the user asks for latest/current behavior, trust-sensitive authority, stale results, changelog freshness, or server warnings.
   - Use the status result to disclose `source_kind`, relevant warning codes, and any active load error when they affect confidence.
   - If `get_status` is unavailable but search is available, continue with search and say that server status was not inspectable.
4. Run `mcp__claude_code_docs.search_docs` with a concrete query that names the feature, command, or concept.
5. If the first result set is weak or ambiguous, retry in this order:
   - canonical feature name
   - joined or split variant, such as `PreToolUse` and `pre tool use`
   - category refinement when the topic area is clear
6. For broad questions, break the request into 2-6 focused sub-queries and run 3-8 total searches inline. Stop when the retrieved docs are enough to answer directly.
7. Draft the answer from the top 1-3 relevant matches per claim area.
8. Cite the returned `chunk_id` and a compact `source_file` page label or link for every material claim when available.
9. State explicitly when documentation is missing, partial, stale-looking, or weak.

## Query Strategy

- Translate vague asks into the documentation's vocabulary.
- Prefer exact feature names and noun-heavy queries, such as `PreToolUse JSON output`, `plugin marketplace install`, or `mcp stdio settings`.
- Try both joined and split variants, such as `PreToolUse` and `pre tool use`.
- Retry with close synonyms, such as `subagents` and `agents`, or `before tool` and `pre tool`.
- Shorten the query when results are sparse or off-topic.

Common categories:

- `hooks`
- `skills`
- `commands`
- `agents`
- `plugins`
- `plugin-marketplaces`
- `mcp`
- `settings`
- `memory`
- `overview`
- `getting-started`
- `cli`
- `best-practices`
- `interactive`
- `security`
- `providers`
- `ide`
- `ci-cd`
- `desktop`
- `integrations`
- `config`
- `operations`
- `troubleshooting`
- `changelog`

Aliases:

- `subagents` -> `agents`
- `sub-agents` -> `agents`
- `slash-commands` -> `commands`
- `claude-md` -> `memory`
- `configuration` -> `config`

## Failure Modes

If search returns no results:

1. Retry with the exact feature name.
2. Retry with CamelCase or spaced variants.
3. Retry with a category filter if the topic area is obvious.
4. If results are still empty, say: `The Claude Code documentation does not appear to cover this topic.`

If results are broad but relevant:

1. Add or refine the category filter.
2. Use a more specific query.
3. Focus the answer on the top 2-3 chunks instead of summarizing the whole result set.

If the question spans multiple documentation areas or needs 3 or more searches:

1. Break the question into 2-6 focused sub-queries.
2. Run 3-8 searches inline through `mcp__claude_code_docs.search_docs`.
3. Use a compatible researcher agent only when the user explicitly asked for or approved delegation and the current runtime exposes an agent mechanism that can use it.
4. Keep single-lookups inline. Do not delegate a question that one or two searches can answer directly.

If the MCP server appears unavailable:

1. Check whether `mcp__claude_code_docs.search_docs` is visible.
2. If it is not visible, use `tool_search` for `claude-code-docs search_docs`.
3. If `mcp__claude_code_docs.get_status` is visible, run it and inspect load errors, warnings, and source state.
4. Run `mcp__claude_code_docs.reload_docs` only if that tool is visible.
5. Retry the search only after discovery or reload succeeds.
6. If search is still unavailable, say: `I cannot provide authoritative Claude Code documentation right now because the claude-code-docs MCP search tool is inaccessible in this session.`

If results appear stale:

1. Run `mcp__claude_code_docs.get_status` if available.
2. Run `mcp__claude_code_docs.reload_docs` only if reload is visible.
3. Re-run the search before answering.
4. If status or reload is unavailable, say which freshness check could not run.

## Response Contract

- Base the answer on retrieved documentation, not memory.
- Avoid inventing settings, flags, file formats, or behavior not present in results.
- Include `chunk_id` plus a compact `source_file` page label or link inline for material claims when available.
- Use `chunk_id`-only citations only when the user explicitly asks for terse internal citations or the result lacks `source_file`.
- When documentation is incomplete, say so directly instead of inferring coverage.
- Label inference explicitly when the docs imply, but do not directly state, a conclusion.
  - Use `Documented:` for direct statements supported by the retrieved docs.
  - Use `Inference:` only for narrow conclusions drawn from documented facts.

## Quick Check

Before responding, verify all of the following:

- At least one search ran.
- Every material claim is backed by at least one `chunk_id` and `source_file` when available.
- Alternate query terms were tried if the first search failed.
- Status was checked or the missing status tool was disclosed for latest/current, stale, warning, or trust-sensitive questions.
- Missing coverage is stated explicitly instead of guessed.
- Any inference is labeled as inference.
