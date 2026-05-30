# Drift Audit Smoke Prompt

Use this example as a lightweight forward test after behavior changes to the
`drift-audit` skill.

## Prompt

```markdown
User: Run a drift audit here.
```

## Expected Behavior

- Infer the target from the current working directory.
- Infer baseline sources from `AGENTS.md`, local contracts, active specs,
  manifests, docs, tests, and narrow external authority sources.
- Stay read-only unless the user explicitly asks for verification.
- Report confirmed drift only when baseline precedence and live contradiction
  are both named.
- Put unresolved authority under `Candidate Mismatches` or `Verification Gaps`.
- Include `Inferred Audit Setup` so the user can correct the target or baseline
  boundary without restating the whole request.
