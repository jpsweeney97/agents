---
name: drift-audit
description: Perform a rigorous read-only drift audit of a directory against its current authoritative baseline. Use when the user asks to audit a directory, tree, skill, package, or current work area for drift; asks to compare live state against contracts, specs, docs, tests, manifests, releases, or another baseline; says "audit this directory for drift", "run a drift audit", "check this tree for contract/source/doc/test drift"; or asks for baseline-vs-live drift analysis. Do not trigger for ordinary code review, tech-debt scans, doc cleanup, generic "is this up to date?" questions, or broad repo audits unless the user explicitly asks for drift or baseline-vs-live analysis.
---

# Drift Audit

Audit a target directory for drift between current live state and the right baseline for each claim. Do not report confirmed drift until you name the baseline source and why it outranks conflicting evidence.

Read [report-contract.md](references/report-contract.md) before drafting the audit report. It defines the mandatory output sections, quality gate, taxonomy checklist, and certification failure rules. For behavior-change validation, use [agent-smoke-test.md](examples/agent-smoke-test.md) as the low-friction forward-test prompt.

Default to doing the audit from available context. Infer the target, scope, and baseline before asking the user for missing inputs. Ask only when two or more plausible interpretations would materially change the audit and the repo context cannot resolve them.

## Defaults

- If the user names a path, use it as the target. If the user says `this directory`, `this tree`, `current work area`, or omits a path, use the current working directory or the most specific directory already in the request/context.
- Do not require the user to provide a baseline. Resolve baselines from local authority sources using the baseline order below. If no defensible baseline exists, complete the audit as an investigation result with `baseline unresolved` rather than asking the user to invent authority.
- Default scope mode is `directory-wide`: inspect the full target inventory, authority surfaces, docs, manifests, tests, and representative source paths, but do not promise every line was semantically reviewed.
- Use `targeted` when the user names a narrow surface or claim.
- Use `exhaustive` only when the user asks for exhaustive coverage. The coverage ledger must then prove every file class was read or explicitly excluded.
- Default to chat report only. Write a durable audit artifact only when the user explicitly asks. If asked to save and the repo already has `docs/audits/`, suggest `docs/audits/YYYY-MM-DD-<target>-drift-audit.md` unless the user gives another path.
- Default to read-only discovery. You may run read-only inspection commands such as `rg`, `find`, `ls`, `sed`, `git status`, `git log`, and non-mutating `git diff`. Do not run tests, builds, linters, app-server/runtime probes, smoke tests, cache refreshes, install commands, or mutation commands unless the user explicitly asks for verification.
- Always suggest exact verification commands that would raise confidence when useful, and list them under `Verification Commands Suggested But Not Run` unless the user asked you to run them.

## Optional User Modifiers

Honor compact modifiers when the user includes them:

- `quick`: inspect narrow authority and top live surfaces only. Keep the report honest about skipped areas.
- `targeted: <claim/path>`: inspect one claim, path, or file class.
- `exhaustive`: prove every file class was read or explicitly excluded.
- `with verification`: run focused safe checks that directly support the audit. Do not install dependencies, mutate caches, or run broad verification unless separately authorized.
- `save report`: write the durable audit artifact after the audit. If no path is supplied and the repo has `docs/audits/`, suggest `docs/audits/YYYY-MM-DD-<target>-drift-audit.md`; otherwise ask for the output path before writing.

## Baseline Rules

- Resolve a baseline per claim. A directory can have different baselines for source behavior, installed runtime behavior, public docs, tests, manifests, evidence, and historical compatibility.
- Treat a baseline as the highest-authority, current-facing source of intended truth for that claim, with explicit scope and freshness.
- Prefer baseline sources in this order:
  1. Explicit user-supplied baseline: path, commit, spec, release, runtime, or comparison directory.
  2. Current repo instructions and directory-local authority rules.
  3. Files that explicitly claim canonical, accepted, active, or current status: contracts, ADRs, active specs, manifests, release docs, precedence sections.
  4. Runtime/source authority appropriate to the claim: source files for source behavior, live runtime inventory for installed behavior, generated fixture checks only for their declared scope.
  5. Tests when they are contract-backed and current; otherwise tests are audited surfaces that can drift.
  6. README, skill docs, and other public-facing docs, below canonical contracts when precedence is declared.
  7. Historical plans, handoffs, reviews, and git history as evidence of why intent changed, not baseline unless marked active/current.
  8. Sibling patterns only as weak inferred baseline for consistency findings.
- If no defensible baseline exists, report `baseline unresolved`. This is a valid investigation result but failed certification. Do not convert candidate mismatches into confirmed drift.
- Confirmed drift gets `Severity: critical|high|medium|low`.
- Candidate mismatches get `Risk if true: critical|high|medium|low` and `Confidence: confirmed|probable|possible|unresolved`. Do not use `Severity` for candidate mismatches.

## External Reads

Inspect outside the target directory only for authority resolution, and label these files as `External Baseline Sources`.

Allowed external reads:

- Parent `AGENTS.md` or equivalent repo instruction files.
- Directly referenced contracts, specs, ADRs, manifests, and release notes.
- Tests that target the directory.
- Explicit evidence files named by target files.
- Runtime/source manifests needed to classify source-vs-installed claims.

Avoid broad repo-wide scans unless the user explicitly asks. If outward authority resolution becomes broad, stop expanding and disclose the boundary in `Skipped Areas / Limits`.

## Workflow

1. Infer the target directory, scope mode, and omitted baseline hints from the request, current working directory, repo instructions, nearby manifests, and target-local files. Ask one clarifying question only if unresolved ambiguity would materially change the audit boundary.
2. Inventory the target directory enough to understand file classes, public surfaces, source surfaces, tests, manifests, generated fixtures, docs, and local history artifacts.
3. Resolve baseline sources per claim, including narrow external baseline sources when needed.
4. Inspect live state in the target directory and compare it to the relevant baseline for each claim.
5. Classify coverage using the taxonomy checklist in [report-contract.md](references/report-contract.md). Use the taxonomy to avoid missed classes, not as a substitute for evidence.
6. Draft findings only after each confirmed drift has a baseline source, precedence rationale, live contradiction, evidence, impact, and recommendation.
7. Keep unresolved or weak-baseline mismatches separate as candidate mismatches.
8. Suggest exact verification commands. Run them only if the user explicitly asked for verification or asks after reading the suggestions.
9. Produce the report using the mandatory shape in [report-contract.md](references/report-contract.md).

## Quality Bar

The report must include `Audit Certification: passed|failed` near the top.

Fail certification if any of these are true:

- Any confirmed drift finding lacks baseline source plus precedence rationale.
- The baseline is unresolved for any target claim that the report tries to certify.
- `Audit Coverage` is missing.
- External baseline reads are not labeled.
- Verification commands were run without user request.
- Candidate mismatches are promoted to confirmed drift.
- Skipped areas could hide material drift and are not disclosed.
- A `no confirmed drift` result lacks a complete coverage ledger.

If the user explicitly asks for a delegation prompt or request packet, include `Delegation Request Packet` after the main report. The default task is still to perform the audit, not to stop at prompt writing.
