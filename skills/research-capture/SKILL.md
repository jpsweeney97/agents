---
name: research-capture
description: "Use when the user wants to land research they already have — pasted notes, ad-hoc findings, or deep-research output — as a durable, source-traced doc under `docs/research/` with a freshness date, per-claim provenance, and an open-questions section. It persists, never searches. Not for running the research (`deep-research`) or merging Markdown into a citation-stripped read (`markdown-synthesis`)."
---

# Research Capture

Land research the user already holds — pasted notes, ad-hoc findings, or a deep-research report — into a durable, source-traced `docs/research/<topic>.md` carrying a freshness date, per-claim provenance, and a standing open-questions section. It persists what is in hand; it never searches for more.

This is a faithful record, not a polished essay, and not independently re-verified. Invocation: `/research-capture` or `$research-capture`.

## Core contract

Every run produces one durable doc at `docs/research/<topic>.md` with the same five-part shape: a header block, Summary, Findings, Open Questions, and Sources. Capture the research as handed in; do not search, fact-check, or fill gaps.

## Input and the no-search boundary

Valid input is research already in hand: pasted notes, ad-hoc findings, prior deep-research output, or several of these on one topic. Read the whole input first.

Then the hard rule, stated once: never search, fetch, or browse — capture only what is in front of you. A missing source becomes an `[unsourced — …]` marker or an open question; if the user wants a gap researched, name `deep-research` where it is available and stop. Never quietly go search.

## What every capture preserves

These three disciplines are the value; do not thin them because a capable model could improvise them.

- **Provenance, per claim.** Every substantive claim carries a marker: a source key (`[S1]`), or an explicit `[unsourced — user]` (the user asserted it without attribution) or `[unsourced — capture]` (your own organizing inference, present in no source). Never leave a claim silently unmarked; never fabricate a citation. The two-way unsourced split is load-bearing — it stops you laundering your own inferences as user fact.
- **Freshness.** Stamp `Captured: <today>` with the real current date; give per-source dates when the input has them (a publication date in the source-date slot, and an access/read date as `— read <YYYY-MM-DD>` on that source's line), else `undated`. Refreshing means a new `deep-research` pass plus a re-capture, never an inline re-verify.
- **Open questions, always present, opportunistically filled.** Record gaps, unresolved contradictions, and load-bearing unsourced claims that the input or your single read already exposes. Write `None surfaced at capture time.` only when genuinely empty. Record a contradiction with both source keys and flag it here — never silently reconcile it.

## Document shape

Write this template. The top-level sections are fixed; structure within Findings follows the material (themed `###` groups when multi-topic, flat when single). The skeleton wraps preserved content — keep the user's wording inside the bullets, keep source seams visible, and wrap already-structured input (a deep-research report, an outline) under the sections rather than flattening it into re-voiced bullets.

```markdown
# Research: <Topic>

Captured: <YYYY-MM-DD>
Inputs: <pasted notes | ad-hoc findings | deep-research report (dated <YYYY-MM-DD>)>
Status: capture — persisted as handed in, not independently re-verified or re-searched

## Summary

<Short plain-language synthesis of the research in hand. Restates only; introduces no claim no source supports.>

## Findings

- <Claim, in the user's wording where possible.> [S1]
- <Claim the user asserted without a source.> [unsourced — user]
- <Claim inferred while organizing, in no source.> [unsourced — capture]
- <Point where sources disagree.> [S2][S3] (see Open Questions)

## Open Questions

- <Unresolved gap, contradiction, or claim needing a search pass — route searching to deep-research; do not search here.>
- <Write "None surfaced at capture time." only when genuinely none.>

## Sources

- S1 — <title/author> — <URL or where it came from> — source date <YYYY-MM-DD | undated> — captured <YYYY-MM-DD>
- S2 — ...
```

## Output path

Write to `docs/research/<topic>.md` from a short slug; create `docs/research/` if absent (this skill establishes the convention). If `AGENTS.md` or `CLAUDE.md` documents a different research home, follow that.

Re-run is non-destructive. New topic → create. Same topic, file clean → extend in place: append new findings, merge and dedup sources (reconciling `[S#]` numbering so inline markers do not collide), refresh `Captured`, and reconcile Open Questions. File dirty, manually edited, ambiguous, or a slug collision with a different topic → ask one path question. Do not ask on a common clean re-run.

## Workflow

1. Read the full input.
2. Extract claims and their sources; mark each claim's provenance.
3. Build the Sources ledger with dates.
4. Collect Open Questions.
5. Write the template to the path (reconciling `[S#]` on an extend-in-place).
6. Reread against Done When; report.

## Done when

- Every substantive claim is marked.
- The five-part shape is present.
- The Open Questions section is present.
- The file is written to the path.

## Commit

After writing and verifying, create a default local commit: stage the research doc only, message `docs(research): capture <topic>` (or `docs(research): update <topic> capture` on a re-run). On a protected or default branch, or when unrelated dirty state makes staging ambiguous, write the file and skip the commit, saying so — defer branch and worktree safety to the repo's protected-branch floor and `git-cycle`; do not re-inline that apparatus. Never push, open a PR, or publish.

## Fence

- vs `markdown-synthesis`: the inverse on every axis — provenance is the deliverable (synthesis strips citations), seams stay visible (synthesis hides them), contradictions are recorded and flagged (synthesis smooths them), the doc is dated and tracks unknowns (synthesis does neither). A clean readable merge that drops sources → `markdown-synthesis`; a traceable record you can revisit → `research-capture`.
- vs `deep-research` (availability-conditional — it is a global skill, absent from this repo): `deep-research` generates research by searching, fetching, and verifying; `research-capture` does zero searching and takes research already in hand, including a finished deep-research report as feedstock. A missing source becomes a marker or an open question and, where `deep-research` is available, names it and stops.
- vs `markdown-reformat`: just tidying notes into Markdown with no provenance, freshness, or open-questions → `markdown-reformat`.
