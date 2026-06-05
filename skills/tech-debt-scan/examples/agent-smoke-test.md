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
- Read repo instructions first for artifact conflicts, but do not require an
  existing audit convention before using the default path.
- If the default parent directory is missing and repo instructions do not forbid
  it, create the parent directory before writing the artifact.
- If parent-directory creation or artifact writing fails, fall back to chat-only,
  label the missing artifact as a proof limit, and do not claim the saved audit
  exists.
- Write only the audit artifact. Do not edit source, tests, manifests, lock
  files, dependency files, `.gitignore`, or docs outside the artifact unless the
  user separately asks for implementation after the scan.
- Start with a concrete frame naming target, depth, finding cap, artifact path,
  draft status, and security boundary.
- Default to `medium` over the current repo or workspace target. Ask only when
  target boundaries would materially change findings, or when high-stakes or
  broad-monorepo scope would mislead without a boundary.
- Return a concise chat `Result Brief`, including `Top Debt Calls`, `Do First`,
  `Why It Matters`, `Audit Path`, and `Coverage Limits`.
- Treat the saved artifact as the durable continuation surface for a future
  Codex or agent.
- Mark the in-progress artifact `Status: draft - incomplete`; switch to
  `Status: complete` only after synthesis, caps, metrics, coverage limits, and
  fidelity checks pass.
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
- Keep dependency review maintenance-only: version skew, unused deps, upgrade
  drag, lockfile drift, license, compatibility, and maintenance cost.
- Treat CVEs, GHSAs, exploitability questions, package-audit output, and
  vulnerability claims as out of scope for this skill; route that work to
  `codex-security:security-scan` and do not use the security signal as debt
  evidence.
- Do not include owners, dependency-aware sequencing, decision gates, ticket
  mutations, or handoff planning. Name `$next-steps` as the right lane and stop
  only when the user asks for those after the audit; do not execute it unless the
  user clearly asks for that planning work.

## Routing Checks

```markdown
User: Audit our dependencies for tech debt.
```

Expected: use `tech-debt-scan` for version skew, unused deps, upgrade drag,
lockfile drift, license, compatibility, and maintenance-risk debt. If CVEs,
GHSAs, exploitability, package-audit output, or vulnerability claims surface,
stop that branch, name `codex-security:security-scan` as the right lane, and do
not record the security signal as debt evidence.

```markdown
User: Run a tech debt scan here.
```

Expected: default to `medium` over the current repo or workspace target, read
repo instructions for artifact conflicts, then write
`docs/audits/YYYY-MM-DD-<target-slug>-debt-scan.md` as
`Status: draft - incomplete` while collecting evidence, creating the default
parent directory when allowed. Do not ask for an artifact path merely because the
repo has no existing audit convention.

```markdown
User: What should we clean up first?
```

Expected: use `tech-debt-scan` when the user wants prioritization or a cleanup
backlog. Do not start edits; return `Do First` as the recommended next action.

```markdown
User: Which of these three debt items should we do first?
```

Expected: use `making-recommendations` when the user supplied the options and
asks for a choice without asking for a new audit, evidence gathering, or backlog
discovery.

```markdown
User: Turn this debt scan into an owner-based plan with dependencies and gates.
```

Expected: do not expand `tech-debt-scan` into handoff or planning mode. Finish
or reference the audit artifact, then name `$next-steps` as the right lane for
dependency-aware sequencing, owners, and gates, and stop unless the user
clearly asks for that planning work.
