# Tech Debt Audit Report Convention

Use this reference when writing the saved `tech-debt-scan` artifact.

The report is the durable evidence and ranked debt backlog. For what
`tech-debt-scan` is and is not (an audit-and-backlog skill, not implementation,
handoff, ticket, or planning), follow the scope rule in SKILL.md.

## Default Path

Write the default artifact to:

```text
docs/audits/YYYY-MM-DD-<target-slug>-debt-scan.md
```

Read repo instructions first for conflicts. Do not require the repo to already
use `docs/audits/`; this skill owns that convention. If repo instructions forbid
or redirect audit artifacts, follow the repo instruction or ask one path question
when the conflict cannot be resolved safely.

For parent-directory creation and the write-failure fallback (fall back to
chat-only, label the missing artifact a proof limit, and do not claim the saved
audit exists), follow the Output section in SKILL.md.

## Status Lifecycle

Start the artifact with:

```markdown
Status: draft - incomplete
```

and flip it to:

```markdown
Status: complete
```

only per the lifecycle rule in SKILL.md (Output) — after synthesis, caps,
metrics, coverage limits, and fidelity checks pass. If interrupted or blocked
before those checks, leave the status as `draft - incomplete` and record the
blocker or next evidence slice in `Coverage Gaps / Next Probes`.

## Authority Order

The artifact's authority order (`Evidence Trail` > `Ranked Backlog` > `Coverage
Gaps / Next Probes`) is governed by SKILL.md (Output); follow it.

Do not let a ranked finding, top call, or chat summary contradict the evidence
trail. If a synthesis sentence drifts, fix the synthesis or lower confidence.

## Hard Exclusions

Do not include owners, dependency chains, decision gates, ticket mutations,
implementation steps, or security vulnerability claims. For continuation,
sequencing, owners, or gates after the audit (route to `/next-steps` or
`$next-steps`, do not execute unless the user clearly asks) and for the security
boundary (route CVE/GHSA/exploitability/package-audit/vulnerability findings to a
security-scan skill, never use them as debt evidence), follow SKILL.md.

## Report Template

```markdown
# <Target> Tech Debt Scan

Status: draft - incomplete
Date: <YYYY-MM-DD>
Target: <repo, subsystem, package, or interface>
Depth: low|medium|high
Finding Cap: <selected cap>
Artifact Path: docs/audits/YYYY-MM-DD-<target-slug>-debt-scan.md

## Result Brief

### Top Debt Calls

- <1-3 corroborated conclusions with present-tense cost>

### Do First

- <smallest high-leverage next action; recommendation only>

### Why It Matters

- <present user, runtime, review, delivery, or operational cost>

### Audit Path

- <artifact path>

### Coverage Limits

- <skipped categories, capped findings, singleton evidence, reduced confidence,
  or none found>

## Scan Snapshot

- Scope: system|subsystem|interface - <boundary>
- Archetype: <top 1-2 archetypes>
- Stakes: low|medium|high - <reason>
- Output Mode: artifact|chat-only
- Security Boundary: dependency maintenance only; vulnerability work routes to
  a security-scan skill, not this audit
- Repo Instructions Checked: <paths or none found>

## Focus & Coverage

| Category | Disposition | Evidence Checked | Notes |
| --- | --- | --- | --- |
| dependency | primary|secondary|background|inapplicable | <paths/classes> | <reason> |
| code-health | primary|secondary|background|inapplicable | <paths/classes> | <reason> |
| test-debt | primary|secondary|background|inapplicable | <paths/classes> | <reason> |
| architecture-drift | primary|secondary|background|inapplicable | <paths/classes> | <reason> |
| operational | primary|secondary|background|inapplicable | <paths/classes> | <reason> |
| knowledge | primary|secondary|background|inapplicable | <paths/classes> | <reason> |

## Evidence Trail

### <ID>: <short evidence title>

- Anchor: <file:line, command output, doc section, manifest, or runtime note>
- Category: dependency|code-health|test-debt|architecture-drift|operational|knowledge
- Observation: <what is present>
- Present Cost: <who pays now and how>
- Corroboration: singleton|evidence_corroborated
- Source Notes: <supporting sources or limits>
- Promoted Finding: <finding id or none>

## Ranked Backlog

### <ID>: <finding title>

- Severity: P0|P1|P2|P3
- Category: dependency|code-health|test-debt|architecture-drift|operational|knowledge|systemic
- Subcategory: <specific lens>
- Anchor: <primary source anchor>
- Problem: <named debt, not tidiness>
- Impact: <present cost>
- Recommendation: <smallest credible repair direction>
- Effort: small|medium|large
- Leverage: low|medium|high
- Confidence: low|medium|high
- Corroboration: singleton|evidence_corroborated
- Evidence Sources: <2+ source classes for corroborated findings>
- Cross Link: <optional related finding ids>
- Next Probe: <optional evidence needed>

## Quick Wins

- <P0/P1 + small findings, or none found>

## High-Leverage Fixes

- <high leverage + small/medium findings, or none found>

## Strategic Items

- <P0/P1 + large findings, or none found>

## Watch List

- <P2/P3 findings, singleton evidence, or weak observations worth preserving>

## Tradeoff Map

- <real anchor conflicts only, such as refactor/ship, coverage/deploy,
  upgrade/shim, observability/simplicity, local/strategic repair, docs location,
  or bus-factor/speed>

## Coverage Gaps / Next Probes

- <uncovered categories, capped material findings, next evidence slice, or none
  found>

## Metrics

- Raw Findings:
- Canonical Findings:
- Merged Clusters:
- Corroborated Count:
- Singleton Count:
- Contradictions:
- Skipped Categories:
- Quick Wins:
- Strategic Items:
- Tradeoffs:

## Fidelity Check

- Anchors match evidence trail: yes|no - <note>
- Recommendations preserve evidence qualifiers: yes|no - <note>
- Top calls are corroborated with present cost: yes|no - <note>
- Coverage limits are visible in Result Brief: yes|no - <note>
- Status updated to complete only after final checks: yes|no - <note>
```

## Mini Example

```markdown
### DP-1: Lockfile drift hides upgrade cost

- Severity: P1
- Category: dependency
- Subcategory: lockfile drift
- Anchor: package.json and package-lock.json disagree on workspace package ranges
- Problem: dependency state requires manual reconciliation before safe upgrades
- Impact: every dependency update now starts with lockfile archaeology and review
  uncertainty
- Recommendation: regenerate the lockfile from the declared manifest set and add
  a focused check that fails on manifest/lock drift
- Effort: small
- Leverage: medium
- Confidence: medium
- Corroboration: evidence_corroborated
- Evidence Sources: package manifest, lockfile, CI install command
```

This finding can appear in `Top Debt Calls` only if the evidence trail records at
least two distinct source classes or independently observed signals and a
present-tense cost. Otherwise keep it in `Ranked Backlog`, `Watch List`, or
`Coverage Gaps / Next Probes`.
