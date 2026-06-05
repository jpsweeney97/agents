---
name: markdown-synthesis
description: Use when the user asks to synthesize, consolidate, combine, distill, or rewrite multiple Markdown sources into one stronger standalone prose Markdown document on disk. Supports exact files, folders, globs, and broad "relevant docs" inputs. Do not use for structure-only Markdown cleanup, preserving original wording/order, simple summaries, non-Markdown outputs, or outputs that need tables, code blocks, links, images, or frontmatter.
---

# Markdown Synthesis

Turn multiple Markdown sources into one cohesive, source-grounded prose
Markdown document written to disk.

This is not formatting cleanup. Use `markdown-reformat` when the user wants to
preserve wording, order, detail, and voice. Use this skill when the user wants a
new upgraded document that rewrites and reorganizes the source material.

## Core Contract

- Produce one standalone finished Markdown file on disk.
- Write prose Markdown: headings and paragraphs by default.
- Do not include tables, code blocks, links, images, frontmatter, source
  notes, citations, "derived from" sections, or visible file-by-file traces.
- Rewrite freely when it improves clarity, flow, structure, or quality, while
  preserving source-supported meaning.
- Add framing, transitions, and organization when they help the document cohere;
  do not invent substantive claims beyond what the sources support.
- Distill duplicated, conflicting, or low-quality material into high-quality
  material that fits the whole document.
- If the sources cannot support a confident finished document, stop before
  writing and ask for the smallest needed decision.
- Never stage or commit the synthesis file unless the user explicitly asks.

## Setup Questions

Before synthesis, collect the document's purpose, audience, and tone. If the
user already supplied any of these, do not ask again for that field. If any are
missing, ask one compact setup question that requests the missing fields.

Offer this tone menu when tone is missing:

1. Plainspoken: clear, direct, human, low-jargon.
2. Neutral professional: polished, balanced, and credible without sounding
   promotional.
3. LinkedIn / corporate professional: public-facing, upbeat, brand-safe, and
   business-friendly.
4. Executive brief: concise, strategic, decision-oriented, and written for busy
   senior readers.
5. Editorial / magazine-style: fluid, engaging, and polished with stronger
   narrative flow.
6. Thought-leadership: confident, thesis-driven, elevated, and insight-forward.
7. Tutorial / explanatory: patient, structured, and designed to teach the
   reader step by step.
8. Field guide / practical: action-oriented, concrete, and focused on usable
   takeaways.
9. Academic / analytical: precise, careful, formal, and argument-driven.
10. Warm expert: approachable and reassuring while still authoritative.
11. Custom blend: the user may combine options or describe a tone in their own
    words.

## Source Selection

- Exact files: use the named Markdown files directly when they exist. If a
  named file is missing, stop and ask instead of substituting another file.
- Folders, globs, or broad requests such as "all relevant docs in this area":
  inspect candidate Markdown files, choose the relevant set, then ask the user
  to confirm the selected files before synthesizing.
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

1. Clarify purpose, audience, and tone if missing.
2. Resolve the source set:
   - exact files can proceed directly;
   - broad inputs require source confirmation before synthesis.
3. Read every selected source file fully enough to understand its meaning,
   quality, structure, overlaps, contradictions, and reusable material.
4. Identify the central through-line and the document shape that would serve the
   stated purpose and audience.
5. Collapse repetition, reconcile light inconsistencies, and upgrade weak
   wording into cohesive prose.
6. Apply the confidence gate before writing.
7. Write the output file to a non-destructive path.
8. Reread or inspect the finished file for coherence, prose-only Markdown, and
   source-grounded meaning.

## Confidence Gate

Proceed when the problems are editorial: repetition, weak organization, uneven
tone, scattered points, minor inconsistencies, or missing transitions.

Stop before writing when the sources contain unresolved contradictions, missing
core context, or ambiguity that would force a meaning-level decision. In that
case:

- Explain the blocker in plain language.
- Name the smallest decision needed from the user.
- Ask how to proceed.
- Do not hide unresolved source conflicts inside polished prose.
- Do not write a caveated or TODO-filled "finished" document unless the user
  explicitly asks for that format.

## Prose-Only Handling

The finished document should be readable prose, not a technical dump.

- Translate code, commands, URLs, tables, diagrams, metadata, and structured
  source details into prose when that preserves the point.
- Omit source structures that are not needed for the document's purpose.
- Stop and ask when code, commands, URLs, tables, links, images, or structured
  data seem essential rather than illustrative.
- Do not include Markdown link syntax. If a URL matters and the user wants it
  retained, ask whether to allow an exception or describe it in prose.

## Quality Bar

The output is done when:

- It reads as one intentional document, not a merged pile of notes.
- A human reader can follow the argument or explanation without knowing the
  source files existed.
- Headings are useful, shallow, and coherent.
- Paragraphs have clear transitions and no duplicated filler.
- The tone matches the user's selected option or custom blend.
- The prose does not overstate, flatten, or invent source meaning.
- The file was written to a non-destructive path and left uncommitted by
  default.
