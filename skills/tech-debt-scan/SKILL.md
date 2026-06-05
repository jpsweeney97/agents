---
name: tech-debt-scan
description: "Use when a user asks for a technical debt scan, audit, cleanup backlog, or debt-prioritization pass over a repo, service, package, subsystem, or interface. Produces a saved evidence-led audit with a concise chat summary across code health, architecture, dependency, test, operational, and knowledge debt."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Tech Debt Scan

Debt audit. Produce a saved, evidence-led continuation artifact plus a concise
chat summary. Start by saying: "I'm using the tech-debt-scan skill for a
robust evidence-led debt audit."

Use for cleanup planning, refactoring backlogs, handoffs, pre-scaling checks, and
"where is our worst debt?" Do not use for PR/file review, incident RCA,
greenfield design, docs-only review, git hygiene, branch cleanup, dirty-worktree
cleanup, or security vulnerability discovery.

## Output

Pick the output mode before recording findings:

- `artifact` default: write
  `docs/audits/YYYY-MM-DD-<target-slug>-debt-scan.md`.
- `chat-only`: only when the user explicitly asks for no file changes,
  read-only output, or chat only, or when the target has no writable artifact
  location. Label the missing artifact as a proof limit.
- `handoff`: explicit ownership transfer, continuation, or team tracking; write
  the artifact with owners, next probes, truncation, and follow-ups.

The saved artifact is for a future Codex or agent continuing the work. Its
authority order is:

1. `Evidence Trail`: anchors, corroboration, present cost, and source notes.
2. `Ranked Backlog`: current synthesis of the evidence trail.
3. `Coverage Gaps / Next Probes`: trust boundaries that say what not to
   over-trust yet.

Chat output is an executive summary only. It must include:

- `Top Debt Calls`: 1-3 strongest corroborated conclusions, not every finding.
- `Do First`: the smallest high-leverage next action.
- `Why It Matters`: present user, runtime, review, or delivery cost.
- `Audit Path`: artifact path, or `none` with the exact reason.
- `Coverage Limits`: skipped categories, capped findings, singleton evidence,
  or reduced confidence.

Do not put singleton evidence in `Top Debt Calls`. Keep singleton or weakly
checked observations in `Watch List`, `Coverage Gaps`, or `Next Probes`.

The artifact preserves the rubric report sections, finding fields, scoring,
caps, metrics, sanity checks, and fidelity check. The first screen of the chat
summary stays readable even when the artifact is long.

References:

- [`references/debt-taxonomy.md`](references/debt-taxonomy.md): archetypes,
  weights, lenses, tensions.
- [`references/category-playbooks.md`](references/category-playbooks.md):
  category surfaces, sentinels, cross-links, disconfirmation.
- [`references/severity-leverage-rubric.md`](references/severity-leverage-rubric.md):
  scoring, caps, report contract, fidelity.
- [`examples/agent-smoke-test.md`](examples/agent-smoke-test.md): forward test
  for default artifact output with concise chat summary.

## Workflow

Run `Frame -> Triage -> Evidence Sweep -> Synthesize -> Deliver`.

1. **Frame:** state scope (`system`, `subsystem`, `interface`), output mode, top
   1-2 archetypes, stakes, artifact path, and evidence map. Use the taxonomy.
   Choose higher stakes when uncertain. Pause only when stakes are high and
   scope/archetype is uncertain.
2. **Triage:** mark categories `primary`, `secondary`, `background`, or
   `inapplicable`. Every relevant category must get at least a first-pass check
   before ranking top calls. Announce scanned, skipped, and deep-emphasis
   categories, with reasons.
3. **Evidence Sweep:** scan dependency, code-health, test-debt,
   architecture-drift, operational, and knowledge debt. For active categories,
   read the relevant repo instructions, manifests, dependency or lock files,
   tests and CI surfaces, architecture docs or imports, operational setup, and
   knowledge sources before promoting findings. Keep named-cost debt only.
4. **Record:** record evidence in the artifact as you go. Do not create
   `.tech-debt-scan-notes.md`, edit `.gitignore`, or create scratch files unless
   the user explicitly asks for that separate file. Record cross-links and
   no-finding coverage notes immediately.
5. **Synthesize:** dedupe with cross-links. Preserve recorded `anchor` and
   `recommendation`. Use `evidence_corroborated` only for 2+ distinct source
   classes or independently observed signals; otherwise use `singleton`. Top
   Debt Calls require `evidence_corroborated` plus a present-tense cost. Score
   severity/leverage/effort, bucket once, map real anchor conflicts, and compute
   rubric metrics.
6. **Deliver:** use the rubric report contract, caps, sanity checks, and fidelity
   check. `artifact`/`handoff` write the audit file before claiming completion.
   `chat-only` answers in chat and labels the missing artifact. If capped with
   material findings left, label the artifact truncated and name the next
   continuation slice. If writing fails, report the blocker, include the concise
   summary, and do not claim the saved audit exists.
