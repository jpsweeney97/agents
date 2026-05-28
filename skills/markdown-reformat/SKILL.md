---
name: markdown-reformat
description: Use when the user asks to format rough text, plaintext notes, hard-wrapped prose, outlines, or messy Markdown into Markdown while preserving wording, order, and voice. Do not use for summarization, substantive rewriting, proofreading, or non-Markdown output.
---

# Markdown Reformat

Format text into Markdown structure. Change headings, lists, wrapping, spacing, and code fences only; preserve meaning, wording, order, detail, and voice.

## Use When

- Plaintext needs Markdown headings, lists, paragraphs, spacing, or code fences.
- Hard-wrapped prose needs readable paragraphs.
- A numbered outline needs Markdown structure.
- Existing Markdown needs structural cleanup.

## Do Not Use When

- The user wants a summary, rewrite, stronger prose, proofreading, `.docx`, HTML, PDF, or another non-Markdown output.
- Choosing a hierarchy would change meaning. Ask one focused question instead.

## References

- Read `references/conversions.md` when a heading, label, list, literal, or code-fence choice is non-obvious.
- Read `references/examples.md` when a concrete example would prevent guessing.

## Workflow

1. Read the full source before assigning headings.
2. Identify title-like lines, section labels, lists, hard-wrapped prose, tables, blockquotes, frontmatter, and code-like text.
3. Preserve content and order unless the user asks to reorganize it.
4. Use the shallowest hierarchy that fits. Never skip heading levels.
5. Keep prose as prose unless the source already behaves like a list.
6. Reflow hard-wrapped prose; never reflow code-like blocks.
7. Use inline code for short literals and fences for multi-line code, commands, regexes, config, or prompts.
8. Preserve spelling, capitalization, punctuation, emphasis, frontmatter, tables, blockquotes, footnotes, links, and existing fenced-block content.
9. If two structures are plausible, choose the less committal one unless the choice would change meaning; then ask.

## Preservation Pass

Before delivery, compare source and output:

- No claim, caveat, example, repeated emphasis, or literal was dropped.
- No claim, conclusion, certainty level, or section relationship was added.
- Ordering stayed the same unless the user requested reorganization.
- Code blocks, commands, regexes, paths, frontmatter, and inline literals kept their original content.
- Already-valid Markdown received only minimal cleanup.

## Output Contract

- For file edits, patch the file in place with the smallest coherent change.
- For pasted text, return copyable Markdown in a fenced `markdown` block unless the user asks for rendered output.
- Mention conservative choices only when they affect readability or interpretation.

## Defaults

- If numbering and bullets conflict, preserve apparent intent instead of forcing uniformity.
- If a wrapped list item continues on the next line, merge it into one item.
- If formatting requires guessing omitted structure, stop at the highest-confidence cleanup and surface the ambiguity.
- If text could be prose or code, preserve layout or use a neutral fenced block.
- If frontmatter appears at the top, preserve it exactly unless the requested conversion requires changing it.

## Done When

- Output is valid Markdown.
- Heading depth is consistent.
- Source wording, order, caveats, examples, repeated emphasis, and literals are preserved.
- No unsupported claim, conclusion, or hierarchy relationship was added.
