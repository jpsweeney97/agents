---
name: baseline
description: "Use when the user asks what source of truth or baseline controls a claim, what to trust, whether an authority is still current, or how to resolve competing or missing authority. Also use for baseline-versus-live contradictions when authority resolution is the main need. Do not use for ordinary status orientation, implementation, broad audits, or work that needs a decision rather than authority resolution."
---

# Baseline

Resolve what should be trusted for a claim before judging whether anything matches it. Treat the claim as an allegation: verify it against the strongest source that is both current and permitted in the active workspace, and say only what the check showed. Invocation: `/baseline` or `$baseline`.

This is a source-of-truth resolver, not a default audit report, implementation plan, or broad status orientation. Its job is to answer “what do I trust here?” compactly, then show enough evidence for the user to correct or approve the authority boundary.

## Safety and authority

- Default to read-only discovery in the active workspace. Before handling work content or a work artifact, follow its live `AGENTS.md` or `CLAUDE.md` and applicable policy.
- Do not browse, access a connector or external system, run verification commands, edit files, write baseline documents, mutate caches, stage, commit, stash, or push unless the user separately and explicitly requests that action and the active workspace permits it.
- Return the answer in chat by default. A durable artifact is a separate explicit request; confirm the permitted destination before writing it. Never stage, commit, stash, or push target-work content while its Git retention is unapproved.
- If classification, permission, or authority is unclear, take the more protective route: do not inspect or disclose the uncertain material, state the specific uncertainty, and ask for clarification.
- Keep a source pointer for claims affecting decisions, owners, numbers, or deadlines. Mark agent inference `unverified` rather than letting it read as authority.

## Core behavior

- Infer the target and likely claim area from the request, permitted current-directory context, named files, workspace instructions, manifests, specs, docs, tests, source, runtime references, and recent context. Ask only when two plausible interpretations would materially change the answer and permitted local context cannot resolve them.
- Treat baselines as claim-scoped. One directory can have different baselines for source behavior, public docs, tests, runtime behavior, release state, ownership, policy, and historical compatibility.
- Answer the likely claim first when context strongly supports one. If the request is broad, ambiguous, or multiple authority surfaces matter, include a compact claim-area map underneath.
- Name trust gaps explicitly. A trust gap is a specific reason the answer cannot honestly say “this matches the intended truth” yet.
- When a usable baseline clearly contradicts live state, report a `Baseline contradiction`. Name both sides and stop: the contradiction never says which side is wrong — live divergence may be a bug or deliberate new intent, and that direction call belongs to the human. Do not turn the report into a certified drift audit or imply global cleanliness.

## Baseline statuses

Use these as answer categories, not heavy report machinery:

- `Usable baseline`: safe to rely on for the named claim and scope. It certifies precedence — this source governs the claim — not that live state matches it or that the source is fresh.
- `Weak baseline`: useful signal, but incomplete, stale, indirect, or too narrowly scoped to trust alone.
- `Competing baselines`: two or more plausible authorities conflict and no inspected precedence rule clearly chooses one.
- `Missing baseline`: no current authority source was found for the claim.
- `Proposed baseline decision`: evidence is strong enough to recommend what should become authoritative, and the choice is not policy-, product-, ownership-, or future-behavior-sensitive.
- `Decision needed`: a human must choose because the baseline decision affects policy, product meaning, ownership, compatibility, or future behavior, or because evidence is insufficient.

## Authority guidance

Resolve authority by claim type instead of applying one global source order. Use the strongest current-facing source available and permitted for the claim:

1. Explicit user-supplied baseline, such as a path, spec, commit, release, runtime, or comparison directory.
2. Current workspace instructions, applicable policy, and directory-local authority rules.
3. Files that explicitly claim canonical, accepted, active, or current status: contracts, ADRs, specs, manifests, release docs, precedence sections, or decision records.
4. Source files for source-behavior claims.
5. Live runtime inspection for runtime claims, only when the user explicitly requested or authorized it and the workspace permits it. Use installed-state inspection only for plugin, cache, marketplace, distributed-copy, or other install-surface claims.
6. Tests when they are contract-backed and current; otherwise they are evidence surfaces that may themselves need a baseline.
7. README, public docs, and examples, below canonical contracts when precedence is declared.
8. Historical plans, handoffs, reviews, and Git history as rationale for why intent changed, not authority unless marked active or current.
9. Sibling patterns as weak inferred evidence for consistency, not standalone authority.

When sources conflict, name the conflict and precedence basis. If precedence cannot be resolved, classify it as `Competing baselines` or `Decision needed`.

## Trust gaps and decisions

Use `Baseline gap`, `Coverage gap`, `Proof gap`, `Freshness gap`, `Scope gap`, `Conflict gap`, and `Repeatability gap` to keep uncertainty visible without overstating drift.

When the baseline is unknown or weak, draft a `Proposed baseline decision` only when inspected evidence strongly points to one authority and the choice is not sensitive. Stop at `Decision needed` when it is policy-, product-, ownership-, compatibility-, or future-behavior-sensitive, or the evidence is insufficient. A proposed decision is not established authority. Do not update docs or source until the user explicitly approves a permitted write step.

## Workflow

1. Identify the target, likely claim area, and whether the request is narrow or broad.
2. Inspect only the authority surfaces needed for the claim and permitted by the active workspace.
3. Classify the baseline status for the primary claim.
4. If the request is broad or multiple baselines matter, add a compact claim-area map for the relevant areas only.
5. Note baseline contradictions only where a usable baseline and live contradiction are both clear.
6. Name trust gaps and the exact verification or decision that would close them.
7. If a baseline decision is needed, either draft a proposed decision or ask the exact human decision question.

## Output

Start with a compact answer:

```markdown
Best current baseline: <path/source, or none found>
For: <claim area and scope>
Status: usable baseline|weak baseline|competing baselines|missing baseline|proposed baseline decision|decision needed
Why trust it: <one to three sentences>
Decision needed: <none, proposed decision, or exact human decision question>
```

When no current authority exists and the answer is a fresh choice, open with `Proposed baseline decision:` or `Decision needed:` instead of `Best current baseline:`. Then include only sections that add value: `Supporting Evidence`, `Trust Gaps`, `Claim-Area Map`, `Baseline Contradictions`, or `Verification To Raise Confidence`. Suggested verification is not run unless explicitly authorized. If an issue should be tracked, say that the user may use an available tracker workflow or record it manually; do not create an issue or assume such a workflow exists.
