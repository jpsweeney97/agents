---
name: tech-debt-scan
description: >-
  Use when a user asks for a fast technical debt scan of a repo, service,
  package, subsystem, or interface. Produces a prioritized cleanup backlog
  across code health, architecture, dependency, test, operational, and knowledge
  debt. For PR/file review use code review; for exhaustive high-stakes scans
  recommend tech-debt-audit.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Tech Debt Scan

Debt triage. Produce a focused backlog, not exhaustive
coverage. Start by saying: "I'm using the tech-debt-scan skill for a fast
single-pass debt scan."

Use for cleanup planning, refactoring backlogs, handoffs, pre-scaling checks, and
"where is our worst debt?" Do not use for PR/file review, incident RCA,
greenfield design, or docs-only review. Recommend `tech-debt-audit` for large,
high-stakes, 4+ category, or outpacing-one-agent scans. If continuing anyway,
label reduced coverage.

## Output

Pick the lightest mode before recording findings:

- `chat-only` default: quick scans, rankings, opinions, reviews; no repo files.
- `artifact`: requested audit, backlog, saved file, or repo-ready plan; write
  `docs/audits/YYYY-MM-DD-<target-slug>-debt-scan.md`.
- `handoff`: ownership transfer, continuation, or team tracking; write artifact
  with owners, next probes, truncation, and follow-ups.

No-file-change requests force `chat-only`. If chat confidence runs out, label
reduced coverage and recommend `artifact` or `tech-debt-audit`.

Default chat reports start with `Result Brief`, then put the rigorous backlog
under `Details`. The brief must include:

- `Top Debt Calls`: 1-3 strongest conclusions, not every finding.
- `Do First`: the smallest high-leverage next action.
- `Why It Matters`: present user, runtime, review, or delivery cost.
- `Coverage Limits`: skipped categories, capped findings, or reduced confidence.

`Details` preserves the rubric report sections, finding fields, scoring,
caps, metrics, sanity checks, and fidelity check. Artifact and handoff modes
may use the full report shape directly, but must still keep the first screen
readable.

References:

- [`references/debt-taxonomy.md`](references/debt-taxonomy.md): archetypes,
  weights, lenses, tensions.
- [`references/category-playbooks.md`](references/category-playbooks.md):
  category surfaces, sentinels, cross-links, disconfirmation.
- [`references/severity-leverage-rubric.md`](references/severity-leverage-rubric.md):
  scoring, caps, report contract, fidelity.
- [`examples/agent-smoke-test.md`](examples/agent-smoke-test.md): low-friction
  forward test for chat-first output.

## Workflow

Run `Frame -> Triage -> Sweep -> Synthesize -> Deliver`.

1. **Frame:** state scope (`system`, `subsystem`, `interface`), output mode, top
   1-2 archetypes, stakes, and evidence map. Use the taxonomy. Choose higher
   stakes when uncertain. Pause only when stakes are high and scope/archetype is
   uncertain.
2. **Triage:** mark categories `primary`, `secondary`, `background`, or
   `inapplicable`. Announce scanned, skipped, and deep-emphasis categories.
3. **Sweep:** scan dependency, code-health, test-debt, architecture-drift,
   operational, knowledge. Read only active playbook sections. Keep named-cost debt.
4. **Record:** `chat-only` keeps context notes and never creates
   `.tech-debt-scan-notes.md` or edits `.gitignore`. `artifact`/`handoff` system
   scans may use `.tech-debt-scan-notes.md` at repo root and add it to
   `.gitignore`; smaller artifact scans can keep inline notes. Record cross-links
   and no-finding coverage notes immediately.
5. **Synthesize:** dedupe with cross-links. Preserve recorded `anchor` and
   `recommendation`. Use `evidence_corroborated` only for 2+ distinct sources;
   otherwise `singleton`, with present-tense cost required for singleton `P0`.
   Score severity/leverage/effort, bucket once, map real anchor conflicts, and
   compute rubric metrics.
6. **Deliver:** use the rubric report contract, caps, sanity checks, and fidelity
   check. `chat-only` answers in chat. `artifact`/`handoff` write the audit file
   before claiming completion. If capped with material findings left, label
   truncated and recommend `tech-debt-audit`. If writing fails, keep scratch notes
   and report.
