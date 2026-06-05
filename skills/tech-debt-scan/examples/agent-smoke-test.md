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
- Write only the audit artifact. Do not edit source, tests, manifests, lock
  files, dependency files, `.gitignore`, or docs outside the artifact unless the
  user separately asks for implementation after the scan.
- State scan depth, finding cap, artifact path, and any truncation limit before
  recording findings.
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
- Treat CVEs, GHSAs, exploitability questions, and vulnerability discovery as
  out of scope for this skill; route that work to
  `codex-security:security-scan` and keep only proof-limited dependency
  maintenance debt in the audit.

## Routing Checks

```markdown
User: Audit our dependencies for tech debt.
```

Expected: use `tech-debt-scan` for upgrade, compatibility, deployment, license,
unused dependency, and maintenance-risk debt. If the work turns into advisory
validation, exploitability, or vulnerability discovery, stop that part and name
`codex-security:security-scan` as the right lane.

```markdown
User: What should we clean up first?
```

Expected: use `tech-debt-scan` when the user wants prioritization or a cleanup
backlog. Do not start edits; return `Do First` as the recommended next action.
