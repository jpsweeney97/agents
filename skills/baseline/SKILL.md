---
name: baseline
description: "Resolve source-of-truth and baseline questions. Use when the user asks what to trust, what the baseline is, what source of truth controls a claim, which doc/spec/test/source/runtime state is authoritative, whether something is still authoritative, or how to establish a baseline decision when authority is missing or competing. Also use for baseline-vs-live contradiction questions when the main need is authority resolution. Do not use for ordinary code review, status orientation, tech-debt scans, doc cleanup, implementation, or broad audits where source-of-truth authority is not the central question."
---

# Baseline

Resolve what should be trusted for a claim before judging whether anything
matches it.

This skill is a source-of-truth resolver. It is not a default audit report,
implementation plan, or broad status orientation. Its job is to answer "what do
I trust here?" compactly, then show enough evidence for the user to correct or
approve the authority boundary.

## Core Behavior

- Default to read-only discovery. Do not edit files, write baseline docs, run
  verification commands, mutate caches, stage commits, or update runtime state
  unless the user explicitly asks for that separate action.
- Infer the target and likely claim area from the request, current directory,
  named files, repo instructions, manifests, specs, docs, tests, source, runtime
  references, and recent context. Ask only when two plausible interpretations
  would materially change the answer and local context cannot resolve them.
- Treat baselines as claim-scoped. One directory can have different baselines
  for source behavior, public docs, tests, runtime behavior, release state,
  ownership, policy, and historical compatibility.
- Answer the likely claim first when context strongly supports one. If the
  request is broad, ambiguous, or multiple authority surfaces matter, include a
  compact claim-area map underneath.
- Name trust gaps explicitly. A trust gap is a specific reason the answer cannot
  honestly say "this matches the intended truth" yet.
- When a usable baseline clearly contradicts live state, report a `Baseline
  contradiction`. Do not turn that into a certified drift audit or imply global
  cleanliness.

## Baseline Statuses

Use these as answer categories, not heavy report machinery:

- `Usable baseline`: safe to rely on for the named claim and scope.
- `Weak baseline`: useful signal, but incomplete, stale, indirect, or too
  narrowly scoped to trust alone.
- `Competing baselines`: two or more plausible authorities conflict and no
  inspected precedence rule clearly chooses one.
- `Missing baseline`: no current authority source was found for the claim.
- `Proposed baseline decision`: evidence is strong enough to recommend what
  should become authoritative, and the choice is not policy-, product-,
  ownership-, or future-behavior-sensitive.
- `Decision needed`: a human must choose because the baseline decision affects
  policy, product meaning, ownership, compatibility, or future behavior, or
  because evidence is insufficient.

## Authority Guidance

Resolve authority by claim type instead of applying one global source order.
Use the strongest current-facing source available for the claim:

1. Explicit user-supplied baseline, such as a path, spec, commit, release,
   runtime, or comparison directory.
2. Current repo instructions and directory-local authority rules.
3. Files that explicitly claim canonical, accepted, active, or current status:
   contracts, ADRs, specs, manifests, release docs, precedence sections, or
   decision records.
4. Source files for source-behavior claims.
5. Live runtime or installed-state inspection for runtime claims, only when the
   user requested or authorized that verification.
6. Tests when they are contract-backed and current; otherwise tests are evidence
   surfaces that may themselves need a baseline.
7. README, public docs, and examples, below canonical contracts when precedence
   is declared.
8. Historical plans, handoffs, reviews, and git history as rationale for why
   intent changed, not authority unless marked active/current.
9. Sibling patterns as weak inferred evidence for consistency, not standalone
   authority.

When sources conflict, name the conflict and precedence basis. If precedence
cannot be resolved, classify it as `Competing baselines` or `Decision needed`.

## Trust Gaps

Use trust gaps to keep uncertainty visible without overstating drift:

- `Baseline gap`: no defensible authority source is known for the claim.
- `Coverage gap`: relevant surfaces were not inspected deeply enough to trust a
  broad conclusion.
- `Proof gap`: the claim needs stronger evidence, such as runtime inspection or
  focused tests, than the current pass has.
- `Freshness gap`: the evidence may be stale or was not re-anchored against
  live state.
- `Scope gap`: the conclusion would be broader than the inspected claim area.
- `Conflict gap`: credible sources disagree and precedence is unresolved.
- `Repeatability gap`: the judgment lacks a clear command, check, or inspection
  path that someone else could use to reproduce it.

## Baseline Decisions

When the baseline is unknown or weak, help the user move forward:

- Draft a `Proposed baseline decision` when inspected evidence strongly points
  to one authority source and the choice is not sensitive.
- Stop at `Decision needed` when the choice is policy-, product-, ownership-,
  compatibility-, or future-behavior-sensitive, or when the evidence is not
  strong enough to recommend a new authority.
- A proposed decision is not established authority. Do not update docs or source
  until the user explicitly approves the write step.
- If the user asks to write or update a baseline decision, write only the
  approved decision to the named path. If no path is supplied and no repo
  convention clearly resolves it, ask one path question before writing.

## Workflow

1. Identify the target, likely claim area, and whether the request is narrow or
   broad.
2. Inspect local authority surfaces needed for the claim: repo instructions,
   target files, manifests, current specs, docs, tests, source, examples, and
   narrow external sources directly needed for authority resolution.
3. Classify the baseline status for the primary claim.
4. If the request is broad or multiple baselines matter, add a compact
   claim-area map for the relevant areas only.
5. Note baseline contradictions only where a usable baseline and live
   contradiction are both clear.
6. Name trust gaps and the exact verification or decision that would close
   them.
7. If a baseline decision is needed, either draft a proposed decision or ask the
   exact human decision question.

## Output

Start with a compact answer. Keep supporting detail short unless the user asks
for a deeper packet.

```markdown
Best current baseline: <path/source, proposed decision, or none found>
For: <claim area and scope>
Status: usable baseline|weak baseline|competing baselines|missing baseline|proposed baseline decision|decision needed
Why trust it: <one to three sentences>
Decision needed: <none, proposed decision, or exact human decision question>
```

Then include only sections that add value:

- `Supporting Evidence`: concrete sources inspected and why they matter.
- `Trust Gaps`: baseline, coverage, proof, freshness, scope, conflict, or
  repeatability gaps.
- `Claim-Area Map`: compact rows for source behavior, docs, tests, runtime,
  release state, ownership, policy, or other relevant areas.
- `Baseline Contradictions`: live contradictions against a usable baseline.
- `Verification To Raise Confidence`: exact commands or checks suggested but
  not run, unless the user asked for verification.

Do not use a formal audit packet by default. If no usable baseline exists, say
that directly instead of stretching weak evidence into authority.
