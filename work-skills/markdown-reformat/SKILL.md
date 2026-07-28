---
name: markdown-reformat
description: "Use when the user asks to format rough text, plaintext notes, hard-wrapped prose, outlines, or messy Markdown into Markdown while preserving wording, order, detail, and voice. Do not use for summarization, substantive rewriting, proofreading, non-Markdown output, or synthesis across multiple sources."
---

# Markdown Reformat

Format text into clearer Markdown structure. Change headings, lists, wrapping, spacing, and code fences only; preserve meaning, wording, order, detail, and voice.

Before handling work content or editing a workspace file, read the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy. If classification, permission, or the destination is unclear, take the more protective route and ask. Return pasted-text results in chat by default. A reformatting request does not authorize browsing, connector access, sending, publication, installation, or another external action. Edit a file only when the user explicitly requests that file edit and the active workspace permits it; never stage, commit, stash, or push work-content output.

## Use And Boundaries

Use this for Markdown headings, lists, paragraphs, spacing, code fences, hard-wrapped prose, numbered outlines, or structural cleanup of existing Markdown.

Do not use it to summarize, consolidate, distill, or rewrite content into a new document. Do not choose a hierarchy that changes meaning. When a structural choice is genuinely ambiguous and could change meaning, ask one focused question.

## Workflow

1. Read the full source before assigning headings.
2. Identify title-like lines, section labels, lists, hard-wrapped prose, tables, blockquotes, frontmatter, and code-like text.
3. Preserve content and order unless the user explicitly requests reorganization.
4. Use the shallowest hierarchy that fits and never skip heading levels.
5. Keep prose as prose unless it already behaves like a list. Reflow hard-wrapped prose, never code-like blocks.
6. Preserve spelling, capitalization, punctuation, emphasis, frontmatter, tables, blockquotes, footnotes, links, fenced-block content, commands, paths, regexes, and inline literals.
7. When two structures are plausible, choose the less committal one unless that choice itself changes meaning; then ask.

## Structural Choices

- Turn a clear title-like first line into `# Title`.
- Turn a numbered major section such as `1. Assumptions Audit` into `## 1. Assumptions Audit`.
- Use a heading only when a label clearly governs the following block; otherwise preserve it as paragraph text or a bold lead-in such as `**Correctness.**`.
- Use inline code for a short literal. Fence multi-line code, commands, regexes, configuration, or prompts.
- Preserve existing task-list markers. Create task lists only when the source already has checkbox semantics.
- Preserve repeated lines and emphasis; repetition can be meaningful.

For example, a standalone `Correctness` label before one paragraph can become `**Correctness.** The current parser is too eager.` rather than a speculative subsection. A `Run:` lead-in followed by several shell commands can use a fenced `bash` block, while a multi-line pattern can use a fenced `regex` block.

## Preservation Pass

Before delivery, compare source and output:

- No claim, caveat, example, repeated emphasis, or literal was dropped.
- No claim, conclusion, certainty level, source authority, or section relationship was added.
- Ordering stayed the same unless the user explicitly requested reorganization.
- Already-valid Markdown received only minimal cleanup.

For a file edit, reread the changed output or inspect the diff, then check for trailing whitespace or conflict markers when practical. For pasted text, return copyable Markdown in a fenced `markdown` block unless the user asks for rendered output. Mention conservative choices only when they affect readability or interpretation.

## Done When

The output is valid Markdown with consistent heading depth and no unsupported claim, conclusion, certainty, authority, or hierarchy relationship added.
