---
name: markdown-synthesis
description: "Use when the user asks to synthesize, consolidate, combine, distill, or rewrite multiple Markdown sources into one stronger standalone Markdown document on disk. Supports exact files, folders, globs, broad relevant-docs inputs, clean prose documents, and structure-rich Markdown when source structure carries meaning. Do not use for structure-only Markdown cleanup, preserving original wording/order, simple summaries, or non-Markdown outputs."
---

# Markdown Synthesis

Turn multiple Markdown sources into one cohesive, source-grounded Markdown
document written to disk.

This is not formatting cleanup. Use `markdown-reformat` when the user wants to
preserve wording, order, detail, and voice. Use this skill when the user wants a
new upgraded document that rewrites and reorganizes the source material.

## Core Contract

- Produce one standalone finished Markdown file on disk.
- Infer the natural document shape from the request and sources.
- Bias toward clean prose when source structure is incidental.
- Preserve source-essential Markdown structure when it helps the reader trust,
  use, or inspect the result, but gate exact code, configuration, frontmatter,
  and tool-facing structure under Markdown Structure Handling.
- Do not include source notes, citations, "derived from" sections, or visible
  file-by-file traces unless the user explicitly asks.
- Rewrite freely when it improves clarity, flow, structure, or quality, while
  preserving source-supported meaning.
- Add framing, transitions, and organization when they help the document cohere;
  do not invent substantive claims beyond what the sources support.
- Distill duplicated, lightly inconsistent, or low-quality material into
  high-quality material that fits the whole document.
- If the sources cannot support a confident finished document, stop before
  writing and ask for the smallest needed decision.
- Never stage or commit the synthesis file unless the user explicitly asks.

## Setup Questions

Do not ask setup questions as the first move when exact or obvious sources are
available. Inspect those sources first, then infer the likely purpose, audience,
tone, document shape, and structure policy.

Ask one compact correction question only when an inferred default would be risky
or would materially change the finished document. If the user already supplied a
field, do not ask again for that field.

Use a clean, direct, source-grounded tone by default when tone is not material to
the output. Offer tone choices only when tone is a real decision; keep the menu
short, such as plainspoken, neutral professional, executive brief, tutorial,
field guide, academic, warm expert, or custom.

## Source Selection

- Exact files: use the named Markdown files directly when they exist. If a
  named file is missing, stop and ask instead of substituting another file.
- Clear selection rules, such as exact globs or "all Markdown files in this
  folder except archive", can proceed after applying the rule.
- Broad requests such as "all relevant docs in this area": inspect candidate
  Markdown files, choose the relevant set, then ask the user to confirm the
  selected files before drafting.
- For broad source confirmation, keep the question compact and include:
  selected files, excluded groups, confidence or why the selected set is enough,
  and one question such as "Use this set, or change it?"
- If broad source selection is risky, explain the risk plainly and ask for a
  tighter scope.
- Ignore generated or local artifact directories unless the user explicitly
  includes them.
- Read all confirmed source files before drafting.

## Output Path

If the user gives an output path, write there unless it would overwrite an
existing file without explicit overwrite permission.

If no output path is given:

1. Infer a short topic from the user request and source material.
2. Use `<topic>-synthesis.md`.
3. Place it beside the source docs when they share one source directory.
4. If the sources span multiple directories and no single destination is
   obvious, ask for the output location before writing.
5. If the chosen path already exists, choose the next non-destructive variant,
   such as `<topic>-synthesis-2.md`, `<topic>-synthesis-3.md`, and so on.

Do not overwrite existing files unless the user explicitly asks.

## Synthesis Workflow

1. Resolve the source set:
   - exact files can proceed directly;
   - clear selection rules can proceed after applying the rule;
   - broad relevance inputs require source confirmation before drafting.
2. Read every selected source file fully enough to understand its meaning,
   quality, structure, overlaps, contradictions, and reusable material.
3. Infer purpose, audience, tone, document shape, and structure policy from the
   request and sources.
4. Ask one compact correction question only when the inference is unsafe or a
   meaning-level choice belongs to the user.
5. Identify the central through-line and the document shape that would serve the
   purpose and audience.
6. Collapse repetition, reconcile light editorial inconsistencies, and upgrade
   weak wording into cohesive Markdown.
7. Apply the confidence gate before writing.
8. Write the output file to a non-destructive path.
9. Reread or inspect the finished file for coherence, appropriate Markdown
   structure, and source-grounded meaning.
10. Reply with the output path, document shape, source count, notable preserved
   structure if any, and verification performed.

## Confidence Gate

Proceed when the problems are editorial: repetition, weak organization, uneven
tone, scattered points, incidental structure, minor inconsistencies, or missing
transitions.

Stop before writing when the sources contain unresolved contradictions, missing
core context, uncertain source selection, or ambiguity that would force a
meaning-level decision. In that case:

- Explain the blocker in plain language.
- Name the smallest decision needed from the user.
- Ask how to proceed.
- Do not hide unresolved source conflicts inside polished prose.
- Do not write a caveated or TODO-filled "finished" document unless the user
  explicitly asks for that format.

## Markdown Structure Handling

The finished document should feel intentionally written, not like a technical
dump or a pasted bundle of source fragments.

- Use headings and paragraphs for the main spine by default.
- Translate or omit source structures when they are incidental, decorative,
  redundant, or only evidence of source formatting.
- Preserve, rebuild, or summarize source-essential structures when they help the
  reader trust, use, or inspect the result.
- Keep links when the destination matters to the reader's next action or trust.
- Preserve exact code blocks, commands, configuration, frontmatter, or other
  tool-facing structure only when the user requested a structure-rich artifact,
  the source purpose clearly requires exact structure, or you ask first.
- Keep tables, lists, or checklists when comparison, scanning, or step-by-step
  use would be worse in prose.
- Ask only when preserving or dropping structure would change meaning, purpose,
  audience, or expected use.
- Do not add synthetic citations, source-file notes, or visible provenance
  sections unless the user explicitly asks.

## Quality Bar

The output is done when:

- It reads as one intentional document, not a merged pile of notes.
- A human reader can follow the argument or explanation without knowing the
  source files existed.
- The document shape fits the purpose, audience, and source material.
- Headings are useful, shallow, and coherent.
- Paragraphs have clear transitions and no duplicated filler.
- Preserved structure earns its place by helping the reader trust, use, or
  inspect the result.
- Incidental source scaffolding is removed or turned into clearer prose.
- The tone matches the user's selected option, supplied style, or safely inferred
  default.
- The document does not overstate, flatten, or invent source meaning.
- The file was written to a non-destructive path and left uncommitted by
  default.

## Final Response

After writing the file, keep the chat response concise and include:

- Output path.
- Document shape, such as prose brief, field guide, reference page, operating
  guide, or structure-rich Markdown artifact.
- Source count.
- Notable preserved structure, or `None` when no source structure was worth
  preserving visibly.
- Verification performed.
