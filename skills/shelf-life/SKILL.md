---
name: shelf-life
description: "Use at two moments: writing a durable conclusion — a diagnosis, a `safe because X` judgment, a measured number, a verdict — stamp it with an anchor footer naming the commit and load-bearing files; and meeting an anchored conclusion you are about to rely on — run the one-command freshness diff before trusting it, re-deriving expired claims instead of patching them. Do not use for name-level doc-set auditing (`doc-drift-audit`), resolving which authority governs a claim (`baseline`), or landing research with calendar freshness dates (`research-capture` — compose with it, not replace it)."
---

# Shelf Life

Every durable claim — "the bug is in the retry loop," "this migration is safe," "p95 is 40ms" — is true of one commit. "Verify before claiming" governs new claims; nothing governs the decay of old verified ones, so a conclusion outlives the code it described and future sessions keep trusting it. The fix is structural: a conclusion ships with its own dependency list at write time, converting staleness from an unaskable judgment question into a one-command check any future session can run.

Invocation: `/shelf-life` or `$shelf-life`; also fires unprompted at two moments — **stamping**, when writing a conclusion into anything durable (a diagnosis summary, a "safe because X" judgment, a measured number, a research doc, a verdict file, a handoff conclusion), and **checking**, when about to rely on a previously anchored conclusion wherever it surfaces: a doc, a loaded handoff, a code comment, or pasted back by the user. The footer format below is deliberately greppable so a future session trips over it without being told.

## 1. Stamp at write time

Append an anchor footer to the conclusion:

```text
[anchored: 4a5b6c7; load-bearing: src/retry.py:80-140, config/timeouts.yaml]
```

- `anchored:` — the short sha of `HEAD` at write time (`git rev-parse --short HEAD`).
- `load-bearing:` — the files, with line ranges when they sharpen it, whose change would invalidate the claim. This is the minimal honest set, not everything read while deriving it: a footer naming half the repo expires on every commit and trains readers to ignore footers. When the claim depends on nothing in the tree — a vendor fact, a calendar fact — say that instead of anchoring; a false anchor is worse than none.

One footer per claim, not per document: a doc carrying three conclusions carries three anchors, each with its own dependency list.

## 2. Check at reuse time

Before leaning on an anchored conclusion, run the freshness diff:

```text
git diff --stat <sha>..HEAD -- <load-bearing paths>
```

- **Empty diff** — the seal holds: say so in one line and proceed on the conclusion.
- **Non-empty** — the conclusion is expired: name which dependency moved, then re-derive it from the current tree before relying on it. Re-derive, never patch: an expired claim is re-established and re-anchored at the new sha — even when it re-derives to the same value — never edited to look current.
- **Sha unreachable** — rebase, shallow clone, wrong repo: say the anchor cannot be checked from here and treat the conclusion as unverified. A failed check never passes as a clean one.

Both triggers are one contract: stamping without checking is decoration, and checking has nothing to run on without stamps. Reading a footer obligates the check.

## Boundaries

- Single semantic claims, not doc sets: batch, name-level auditing of whether a documentation set still matches the code is `doc-drift-audit`. This stamps one claim at write time and checks it at the moment of reuse.
- Freshness, not authority: which source of truth governs a claim, and what to trust when authorities conflict, is `baseline`. This dates one claim against the code it stands on.
- Composes with calendar freshness, never replaces it: `research-capture` stamps dated provenance, and the handoff-loading lane (where available) mandates a live-state check — neither gives the check a mechanical form. An anchor footer can live inside either artifact; this skill is the runnable form of the check they call for.
