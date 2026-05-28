# Markdown Reformat Conversions

Use this reference when the core workflow leaves a structural choice unclear.

## Conversions

- Title-like first line -> `# Title`.
- Numbered major section, such as `1. Assumptions Audit` -> `## 1. Assumptions Audit`.
- Clear subsection label, such as `Correctness` or `Operational` -> `###` only when it governs the following block.
- Ambiguous label -> paragraph text or bold lead-in, such as `**Correctness.**`.
- Single short literal, such as `rg pattern src/` -> inline code.
- Multi-line code, commands, regexes, shell snippets, config, or prompts -> fenced block.
- Existing task-list marker, such as `- [ ]` -> preserve as-is; create task lists only for existing checkbox semantics.

## Avoid

| Pattern | Why | Use Instead |
| ------- | --- | ----------- |
| Rewriting for style | Changes voice and meaning | Structural cleanup only |
| Deep heading trees | Adds interpretation | Shallowest fitting hierarchy |
| Fencing every literal | Makes prose noisy | Inline code for short literals |
| Turning prose into lists | Changes emphasis | Paragraphs unless list-shaped |
| Dropping repetition | May remove emphasis | Preserve repeated lines |
