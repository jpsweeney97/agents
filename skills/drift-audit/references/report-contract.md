# Drift Audit Report Contract

Use this contract for every `drift-audit` report. The report can be concise, but it must preserve the named sections and evidence boundaries below. Do not require the user to supply a baseline before reporting; infer authority from available context and mark unresolved authority as an investigation limit.

## Required Report Shape

```markdown
**Audit Result**
Scope Mode: targeted|directory-wide|exhaustive
Target: <path>
Audit Certification: passed|failed
Certification Rationale: <one to three sentences>

**Baseline**
| Claim Area | Baseline Source | Why It Outranks Conflicting Evidence | Scope / Freshness | Confidence |
|---|---|---|---|---|

**External Baseline Sources**
- <path or none> - <why read>

**Audit Coverage**
- Target Directory Inventory: <file classes and notable surfaces inspected>
- Baseline Sources Inspected: <contracts/specs/ADRs/manifests/docs/etc.>
- External Baseline Sources Inspected: <parent instructions, referenced specs, tests, evidence>
- Live Surfaces Inspected: <source/docs/tests/manifests/generated fixtures/etc.>
- Tests/Docs/Manifests Checked: <specific files or classes>
- Skipped Areas / Limits: <what was not inspected and why>
- Verification Commands Suggested But Not Run: <exact commands, or none>
- Verification Commands Run At User Request: <exact commands and result, or none>

**Confirmed Drift Findings**
1. <title>
   Category: <one or more taxonomy labels, optional>
   Severity: critical|high|medium|low
   Baseline Source: <path plus line/section when possible>
   Baseline Precedence: <why this source wins>
   Live State: <path plus line/section when possible>
   Evidence: <short concrete evidence>
   Impact: <user/runtime/review/maintenance risk>
   Recommended Disposition: fix live|fix docs|fix tests|rebaseline|verify runtime|other

**Candidate Mismatches**
1. <title>
   Category: <one or more taxonomy labels, optional>
   Risk if true: critical|high|medium|low
   Confidence: confirmed|probable|possible|unresolved
   Candidate Baseline: <source or unresolved>
   Live State: <path plus line/section when possible>
   Missing Authority: <what would confirm or reject drift>
   Recommended Next Step: <specific follow-up>

**Verification Gaps**
- <missing runtime proof, stale evidence, unrun tests, inaccessible files, unresolved authority>

**Non-Drift Historical Context**
- <old paths, compatibility layers, archived plans, or retained artifacts that are intentionally historical>

**Recommended Next Steps**
- <ordered, concrete next actions>
```

If there are no confirmed findings, keep `Confirmed Drift Findings` and write `None confirmed.` A `no confirmed drift` result is invalid unless `Audit Coverage` is complete.

## Certification Gate

Set `Audit Certification: failed` when any of these are true:

- A confirmed drift finding lacks a baseline source.
- A confirmed drift finding lacks a precedence rationale explaining why the baseline outranks conflicting evidence.
- The baseline is unresolved for a claim the report tries to certify.
- `Audit Coverage` is missing or too vague to show what was inspected.
- External baseline reads are present but not labeled under `External Baseline Sources`.
- Verification commands were run without explicit user request.
- A candidate mismatch is presented as confirmed drift.
- Skipped areas could hide material drift and are not disclosed.
- The report says there is no confirmed drift without a complete coverage ledger.

`Audit Certification: failed` does not mean the audit is useless. It means the report is an investigation result, not a certified drift result.

## Baseline Source Guidance

Resolve baseline per claim. Do not assume one file controls the whole directory.

If the user did not provide a baseline, resolve one from the target's repo instructions, current contracts, active specs, manifests, source files, docs, tests, and narrow external authority sources. Ask for a baseline only when two plausible authorities conflict and choosing between them would change confirmed findings.

Strong baseline sources:

- Explicit user-provided baseline, such as a path, spec, commit, release, runtime, or comparison directory.
- Current repo or directory instructions that define source authority and proof classes.
- Contracts, accepted ADRs, active specs, manifests, and release docs that explicitly claim canonical/current status.
- Source files for source behavior claims.
- Live runtime inventory for installed-runtime claims, when the user requested and authorized runtime verification.
- Generated inventory or fixture checks only for the rows and strings they declare.

Weak or scoped baseline sources:

- Tests, when they are not backed by a current contract.
- README and public docs when a canonical contract declares higher precedence.
- Historical plans, reviews, handoffs, closeouts, and git history unless marked active/current.
- Sibling patterns, which support consistency observations but rarely prove intent alone.

When sources conflict, name the conflict and explain precedence. If precedence cannot be resolved, put the issue under `Candidate Mismatches` or `Verification Gaps`.

## Taxonomy Checklist

Use these labels as a coverage checklist, not as required enum machinery:

- `contract-vs-implementation`
- `docs-vs-source`
- `tests-vs-current-behavior`
- `source-vs-installed-runtime`
- `evidence-freshness`
- `historical-vs-current`
- `naming/path drift`
- `workflow/rollout drift`

Findings may use multiple labels or no label when another description is clearer. The baseline/evidence chain is the contract.

## Severity And Confidence

Confirmed drift:

- Use `Severity`.
- Choose severity by impact if the baseline is correct: data loss, runtime failure, user-facing misdirection, safety regression, test falsehood, maintenance cost, or review risk.

Candidate mismatch:

- Use `Risk if true` plus `Confidence`.
- `confirmed`: the mismatch itself is proven, but the baseline does not justify calling it confirmed drift.
- `probable`: strong baseline signal exists, but one required authority or verification step is missing.
- `possible`: plausible mismatch, but baseline or live state is partial.
- `unresolved`: no defensible baseline, inaccessible source, or conflicting authorities with no precedence rule.

Do not use severity labels for candidate mismatches.

## Verification Commands

Default behavior is read-only discovery. Suggest exact commands but do not run verification unless the user asks.

Useful suggested commands may include:

- Focused tests for the target directory.
- Contract or fixture regeneration checks.
- YAML/frontmatter parsing.
- Lint or format checks.
- App-server, plugin, skills, hooks, or installed-runtime inventory when the claim is about installed behavior.

If the user asks you to run verification, record exact commands and results under `Verification Commands Run At User Request`.

## Delegation Request Packet

Include this section only when the user explicitly asks to delegate the audit.

```markdown
**Delegation Request Packet**
Target: <path>
Scope Mode: targeted|directory-wide|exhaustive
Required Baseline Sources: <known contracts/specs/instructions>
Allowed External Reads: <narrow authority-resolution paths>
Read-Only Boundary: <commands allowed / verification commands withheld>
Required Output: Use `$drift-audit` report contract; fail certification on unresolved baseline or missing coverage.
Special Concerns: <known drift risks or claim areas>
```
