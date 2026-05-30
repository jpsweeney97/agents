# Skill UX Audit Smoke Prompt

Use this example as a lightweight forward test after behavior changes to the
`skill-ux-audit` skill.

## Prompt

```markdown
User: Audit the UX of skills/drift-audit.
```

## Expected Behavior

- Infer `skills/drift-audit` as the target skill.
- Stay read-only because the user asked for an audit, not implementation.
- Read the target `SKILL.md`, `agents/openai.yaml`, and relevant referenced
  report/example files as needed.
- Produce a concise `Result Brief` before any rubric detail.
- Recommend 3-5 ranked UX improvements with compact evidence notes.
- Label changes that touch triggers, evidence rules, validation, authority,
  safety, or mutation permissions as `Contract-risky`.
- Preserve the target skill's rigor and quality requirements; do not suggest
  removing evidence, certification, coverage, or validation requirements merely
  to shorten the report.
- Put optional rubric coverage or skipped-surface notes under `Details` only
  when they materially affect confidence.
