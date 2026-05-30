# Tech Debt Scan Smoke Prompt

Use this example as a lightweight forward test after behavior changes to the
`tech-debt-scan` skill.

## Prompt

```markdown
User: Run a tech debt scan here.
```

## Expected Behavior

- Select `chat-only` unless the user asks for an artifact or handoff.
- Start with `Result Brief`, including `Top Debt Calls`, `Do First`,
  `Why It Matters`, and `Coverage Limits`.
- Put the rigorous debt backlog under `Details`.
- Preserve severity, leverage, effort, confidence, corroboration, caps, metrics,
  sanity checks, and fidelity requirements.
- Label reduced coverage or capped findings instead of implying exhaustive
  coverage.
