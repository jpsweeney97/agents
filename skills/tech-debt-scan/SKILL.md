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

Debt audit. Produce a saved, evidence-led audit artifact plus a concise chat
summary. The first visible move must frame target, scan depth, finding cap,
artifact path, draft status, and the security boundary.

Use for cleanup planning, refactoring backlogs, pre-scaling checks, and "where is
our worst debt?" Do not use for PR/file review, incident RCA, greenfield design,
docs-only review, git hygiene, branch cleanup, dirty-worktree cleanup, handoff
planning, dependency-aware sequencing, ticket work, or security vulnerability
discovery.

If the user asks to choose among already-supplied debt options without asking for
an audit or evidence gathering, use `making-recommendations`. Use
`tech-debt-scan` when evidence gathering, debt discovery, or backlog synthesis is
needed.

This is an audit-and-backlog skill, not an implementation, handoff, ticket, or
planning skill. Unless the user separately asks for implementation after the
scan, write only the audit artifact. Do not edit source files, tests, manifests,
lock files, dependency files, docs outside the audit artifact, `.gitignore`, or
cleanup artifacts. `Do First` is a recommendation, not permission to start the
work. If the user wants dependency-aware sequencing, owners, gates, or
continuation planning after the audit, name `$next-steps` as the right lane and
stop. Do not execute it unless the user explicitly invokes or selects that skill.

## Output

Pick the output mode before recording findings:

- `artifact` default: write
  `docs/audits/YYYY-MM-DD-<target-slug>-debt-scan.md`.
- `chat-only`: only when the user explicitly asks for no file changes,
  read-only output, or chat only, or when the target has no writable artifact
  location. Label the missing artifact as a proof limit.

Read repo instructions first for artifact conflicts, but do not require an
existing repo audit convention. `tech-debt-scan` owns the default
`docs/audits/YYYY-MM-DD-<target-slug>-debt-scan.md` convention.
If the default parent directory is missing and repo instructions do not forbid
it, create the parent directory before writing the artifact. If parent-directory
creation or artifact writing fails, fall back to `chat-only`, label the missing
artifact as a proof limit, and do not claim the saved audit exists.

Also pick scan depth before recording findings:

- `low`: narrow target or quick pass; cap findings at 4-8 and name omitted
  categories.
- `medium` default: normal repo or subsystem scan; cap findings at 8-15.
- `high`: broad or high-stakes scan; cap findings at 12-20 and name the next
  evidence slice before deep reading.

Depth controls how much evidence to gather, not the proof bar. If the selected
depth cannot cover every relevant category, label the scan truncated and keep
uncovered categories in `Coverage Gaps / Next Probes`.

For a broad "run a tech debt scan here" request, default to `medium` over the
current repo or workspace target. Ask only when multiple plausible target
boundaries would materially change findings, or when a high-stakes or broad
monorepo scan would mislead without an explicit boundary.

The saved artifact is for a future Codex or agent continuing from evidence. Its
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

The artifact uses the proprietary report convention in
`references/audit-report-template.md`, including `Status: draft - incomplete`
while evidence is being recorded. Change the artifact to `Status: complete` only
after synthesis, caps, metrics, coverage limits, and fidelity checks pass. The
first screen of the chat summary stays readable even when the artifact is long.

References:

- [`references/debt-taxonomy.md`](references/debt-taxonomy.md): archetypes,
  weights, lenses, tensions.
- [`references/category-playbooks.md`](references/category-playbooks.md):
  category surfaces, sentinels, cross-links, disconfirmation.
- [`references/severity-leverage-rubric.md`](references/severity-leverage-rubric.md):
  scoring, caps, report contract, fidelity.
- [`references/audit-report-template.md`](references/audit-report-template.md):
  proprietary artifact convention, status lifecycle, section template, finding
  fields.
- [`examples/agent-smoke-test.md`](examples/agent-smoke-test.md): forward test
  for default artifact output with concise chat summary.

## Workflow

Run `Frame -> Triage -> Evidence Sweep -> Synthesize -> Deliver`.

1. **Frame:** read repo instructions for artifact conflicts, infer the target,
   and state scope (`system`, `subsystem`, `interface`), output mode, top 1-2
   archetypes, stakes, scan depth, finding cap, artifact path, draft status, and
   evidence map. Use the taxonomy. Choose higher stakes when uncertain. Pause
   only when target boundaries would materially change findings or a high-stakes
   or broad-monorepo scan would mislead without a boundary. Use a plain opener
   like: "I'm using `tech-debt-scan`; I'll run a medium scan over `<target>`,
   write `<path>` as a draft while collecting evidence, cap findings at 8-15, and
   keep security vulnerability work out of scope."
2. **Triage:** mark categories `primary`, `secondary`, `background`, or
   `inapplicable`. Every relevant category must get at least a first-pass check
   before ranking top calls. Announce scanned, skipped, and deep-emphasis
   categories, with reasons.
3. **Evidence Sweep:** scan dependency, code-health, test-debt,
   architecture-drift, operational, and knowledge debt. For active categories,
   read the relevant repo instructions, manifests, dependency or lock files,
   tests and CI surfaces, architecture docs or imports, operational setup, and
   knowledge sources before promoting findings. Keep named-cost debt only.
   Dependency review is maintenance-only: version skew, unused dependencies,
   upgrade drag, lockfile drift, license, compatibility, and maintenance cost. If
   dependency review surfaces CVEs, GHSAs, exploitability, package-audit output,
   or vulnerability claims, stop that branch and route it to
   `codex-security:security-scan`; do not use the security signal as debt
   evidence.
4. **Record:** record evidence in the artifact as you go using
   `references/audit-report-template.md`. Keep the artifact status as
   `draft - incomplete` until the final checks pass. Do not create
   `.tech-debt-scan-notes.md`, edit `.gitignore`, or create scratch files unless
   the user explicitly asks for that separate file. Record cross-links and
   no-finding coverage notes immediately.
5. **Synthesize:** dedupe with cross-links. Preserve recorded `anchor` and
   `recommendation`. Use `evidence_corroborated` only for 2+ distinct source
   classes or independently observed signals; otherwise use `singleton`. Top
   Debt Calls require `evidence_corroborated` plus a present-tense cost. Score
   severity/leverage/effort, bucket once, map real anchor conflicts, and compute
   rubric metrics.
6. **Deliver:** use the audit report template, rubric caps, sanity checks, and
   fidelity check. For `artifact`, write the audit file before claiming
   completion, creating the default parent directory when allowed, and change
   status to `complete` only after final checks pass. `chat-only` answers in chat
   and labels the missing artifact. If capped with material findings left, label
   the artifact truncated and name the next evidence slice. If writing fails,
   report the blocker, include the concise summary, label the missing artifact as
   a proof limit, and do not claim the saved audit exists.
