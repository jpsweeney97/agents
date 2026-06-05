# Tech Debt Scan Smoke Prompt

Use this example as a lightweight forward test after behavior changes to the
`tech-debt-scan` skill.

## Prompt

```markdown
User: Run a tech debt scan here.
```

## Expected Behavior

- Select `artifact` by default and write
  `docs/audits/YYYY-MM-DD-<target-slug>-debt-scan.md` unless the user explicitly
  asks for chat-only, read-only, or no file changes.
- Return a concise chat `Result Brief`, including `Top Debt Calls`, `Do First`,
  `Why It Matters`, `Audit Path`, and `Coverage Limits`.
- Treat the saved artifact as the durable continuation surface for a future
  Codex or agent.
- Make the artifact's `Evidence Trail` the authority; treat the ranked backlog
  as synthesis and coverage gaps / next probes as trust boundaries.
- Give every relevant debt category at least a first-pass check before ranking
  top calls.
- Include only corroborated findings in `Top Debt Calls`; keep singleton
  evidence in findings, watch list, coverage gaps, or next probes.
- Preserve severity, leverage, effort, confidence, corroboration, caps, metrics,
  sanity checks, and fidelity requirements.
- Label reduced coverage, capped findings, and omitted categories instead of
  implying exhaustive coverage.
