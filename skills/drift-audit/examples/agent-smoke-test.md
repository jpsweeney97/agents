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
- Show honored modifiers and verification mode in `Inferred Audit Setup`.

## Modifier Prompt

```markdown
User: quick targeted: report output Run a drift audit here with verification.
```

## Modifier Expected Behavior

- Treat `quick` as a modifier on inspection depth, not as a fourth scope mode.
- Set scope mode to `targeted` and state that the boundary is report output.
- Show `Modifiers Honored: quick; targeted: report output; with verification`
  or equivalent in `Inferred Audit Setup`.
- Show `Verification Mode` near the top setup block, including whether focused
  safe checks were run or no safe direct check existed.
- Keep skipped surfaces visible under `Skipped Areas / Limits`; fail
  certification if skipped areas could hide material drift.
