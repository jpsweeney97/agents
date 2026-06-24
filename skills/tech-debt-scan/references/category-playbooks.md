# Category Playbooks

Give every relevant category a first-pass check before ranking top calls. Read deeply only in active categories. Keep named-cost debt and cross-link causes.

| Category | Check and record threshold |
| --- | --- |
| dependency | deps, locks, imports, licenses, workspaces; record version skew, unused deps, upgrade drag, lockfile drift, license, compatibility, and maintenance cost only. For CVE/GHSA/exploitability/package-audit/vulnerability signals, apply the SKILL.md security boundary (route out, never use as debt evidence) |
| code-health | churned files, TODOs, lint, generated code, broad exceptions, duplication; record slow review, bugs, onboarding drag, unsafe cleanup, repeated edits |
| test-debt | tests, coverage, CI, mocks, critical paths, runtime; record hidden regressions, blocked refactors, slow delivery, deploy distrust |
| architecture-drift | imports, ADRs, boundaries, shared state, utilities, seams; record coordinated changes, blocked tests, duplication, deploy coupling, false docs |
| operational | CI/deploy, infra, telemetry, alerts, runbooks, setup, capacity; record oncall toil, opacity, risky deploys, setup tax, scaling cliff |
| knowledge | READMEs, onboarding, ADRs, ownership, history, comments; record stale/missing knowledge that slows change, blocks handoff, raises oncall risk, or hides decisions |

Disconfirm tiny unused surfaces, tidiness-only code, prototype gaps, architecture without boundary/cost, and solo bus factor without handoff evidence/blocker.
