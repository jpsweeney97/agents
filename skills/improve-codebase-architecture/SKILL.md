---
name: improve-codebase-architecture
description: "Use when the user wants to find architecture-deepening opportunities in a codebase, such as improving module seams, reducing shallow pass-through abstractions, consolidating tightly coupled code, or making behavior easier to test, with a throwaway HTML report opened from the temp directory; if the user chooses a candidate, the follow-up grilling conversation may record `CONTEXT.md` terms or ADR notes. Do not use for implementation, bug diagnosis, code review, tech-debt backlog scans, or broad refactor planning without an architecture focus."
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

The survey phase only reports through a throwaway HTML file and does not edit code. If the user chooses a candidate to explore, the follow-up grilling phase may write `CONTEXT.md` glossary terms or ADR notes, but still does not implement refactors. For a scoped behavior-preserving cleanup of a known target rather than surfacing architecture opportunities, use `simplify-code`.

## Glossary

Use these terms exactly in every suggestion. Consistent language is the point — don't drift into "component," "service," "API," or "boundary." The ban covers the whole engagement — grilling prose and recommended answers included, which is where drift actually lands; a grep over the report file proves only the report. Full definitions in [LANGUAGE.md](LANGUAGE.md).

- **Module** — anything with an interface and an implementation (function, class, package, slice).
- **Interface** — everything a caller must know to use the module: types, invariants, error modes, ordering, config. Not just the type signature.
- **Implementation** — the code inside.
- **Depth** — leverage at the interface: a lot of behaviour behind a small interface. **Deep** = high leverage. **Shallow** = interface nearly as complex as the implementation.
- **Seam** — where an interface lives; a place behaviour can be altered without editing in place. (Use this, not "boundary.")
- **Adapter** — a concrete thing satisfying an interface at a seam.
- **Leverage** — what callers get from depth.
- **Locality** — what maintainers get from depth: change, bugs, knowledge concentrated in one place.

Key principles (see [LANGUAGE.md](LANGUAGE.md) for the full list):

- **Deletion test**: imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.**
- **One adapter = hypothetical seam. Two adapters = real seam.**

This skill is _informed_ by the project's domain model. The domain language gives names to good seams; ADRs record decisions the skill should not re-litigate.

## Process

### 1. Explore

Read the project's domain glossary and any ADRs in the area you're touching first.

Then walk the codebase — using an exploration subagent when the runtime offers one (in Claude Code, the Agent tool with `subagent_type=Explore`); otherwise explore directly. Exploration subagents return findings, not reports — the survey produces one consolidated report, written by you. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Stamp the report header with the commit the survey read (`git rev-parse --short HEAD`, noting a dirty worktree if there is one): the codebase moves, and an unpinned survey cannot show its own staleness. Open it for the user — `xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows — and tell them the absolute path.

The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a graph/flow/sequence reliably communicates the structure. Mix Mermaid with hand-crafted CSS/SVG visuals — use Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), and hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**. Be visual.

Classify each candidate's dependencies before writing its card, using the taxonomy and exact badge labels in [DEEPENING.md](DEEPENING.md).

For each candidate, render a card with these fields:

- **Files** — which files/modules are involved
- **Problem** — why the current architecture is causing friction
- **Solution** — plain English description of what would change
- **Wins** — explained in terms of locality and leverage, and how tests would improve
- **Before / After diagram** — side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength** — one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge
- **Dependency category** — one exact badge label from [DEEPENING.md](DEEPENING.md), rendered beside recommendation strength

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

What the verdict words claim: a badge grades the observed friction and the evidence behind it, never the proposed after-state — Solutions are one-pass design hypotheses for the follow-up grilling to contest. `Strong` claims strong evidence of a real problem at a real seam; it is not implementation authorization. The Top recommendation means "explore this first," not "build this first." The recorded failure mode of these surveys is over-consolidation — after-states that merge modules whose contracts the code or the domain glossary deliberately keeps distinct — so check a proposed after-state against those distinctions before writing its card.

**Use CONTEXT.md vocabulary for the domain, and [LANGUAGE.md](LANGUAGE.md) vocabulary for the architecture.** If `CONTEXT.md` defines "Order," talk about "the Order intake module" — not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"contradicts ADR-0007 — but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

See [HTML-REPORT.md](HTML-REPORT.md) for the full HTML scaffold, diagram patterns, and styling guidance.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, switch to `grill-with-docs` for the design conversation, seeded with the chosen candidate, its files, dependency category, problem, proposed solution, relevant diagrams, and any domain glossary or ADR anchors already found. Keep this architecture-specific lens in play while grilling: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Do not let the conversation become agreement theater: if the user accepts a run of recommended answers verbatim, say the grilling has become drafting with their consent, then ask the design question whose answer you are least sure of or offer to stop. The naming is not single-shot: if verbatim acceptance resumes afterward, that is the stronger signal — say so again or stop. If a candidate claim, current-code claim, or recommended closed set can be checked in the codebase, check it before treating it as settled.

Side effects happen inline as decisions crystallize, under `grill-with-docs` write discipline:

- **Naming a deepened module after a concept not in `CONTEXT.md`?** Add the term to `CONTEXT.md` — same discipline as `grill-with-docs` (see [CONTEXT-FORMAT.md](../grill-with-docs/CONTEXT-FORMAT.md)). Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `CONTEXT.md` right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing — skip ephemeral reasons ("not worth it right now") and self-evident ones. See [ADR-FORMAT.md](../grill-with-docs/ADR-FORMAT.md).
- **Want to explore alternative interfaces for the deepened module?** See [INTERFACE-DESIGN.md](INTERFACE-DESIGN.md).
- **Does the candidate's premise need proof rather than interface alternatives?** Route to the proving lanes before committing the design — pin current behavior with a characterization net (`characterization-tests`), build a deliberately throwaway spike (`prototype`), compare against the live baseline — then ratify the design with evidence in hand.

For `CONTEXT.md` and ADR writes, follow `grill-with-docs` for the dirty-worktree warning, unrelated-edit protection, incremental writes, commit-mid-session handling, closeout reporting, and proof boundary. (The HTML report stays in the temp directory, per step 2.) Proof boundary: you recorded glossary and decision text, not verified refactors.
