---
name: methodology-critique
description: "Use when JP commissions the methodology-and-philosophy treatment of a skill in this library: max-effort pressure on the skill's epistemology, stance, and implicit theory of its own method, tested against its full history and recovered fire corpus, adjudicated by JP, then whatever repairs the critique warrants, landed and pushed with a docs/reviews brief. Claude-only, expensive by design — the fire-tested treatment methodology-check escalates to when how the target fires in its real transcripts is the crux. Do not use for execution-altitude skill-contract review (scrutinize-skill), the cheap text-and-census methodology pass (methodology-check), quantitative benchmarking (skill-benchmark), routine skill editing, or targets outside this library."
---

# Methodology Critique

The treatment: pressure on a skill's methodology and philosophy — the epistemology, the stance, the implicit theory of what the method is and what it can know — honestly adjudicated, then whatever rebuild the critique actually warrants. The target is the method itself, tested against its own text, its history, and its recorded fires; frontmatter and routing scrutiny belong to other lanes.

The genre's record lives in `docs/reviews/*-methodology-critique.md`. Read it fresh each run; never carry the tally or the precedents' findings from memory or from this file. A hold and an inversion are equally legitimate results, and the deliverable is an adjudicated written critique that becomes the design brief for same-session repairs.

Run at maximum effort, single register — there is no light mode. The cheaper passes already exist: `scrutinize-skill` detects premise-class doubts at contract altitude and routes them to `methodology-check`, which adjudicates the method on text and a fire census and escalates here when how the target fires in its real transcripts is the load-bearing question.

## Phase 0 — Commission (seal before evidence)

Work on a working branch (`git status --short --branch` first). Pin the target's current commit; every line citation resolves against it.

1. Verify the bundle shape yourself — list the target directory; never assume `references/`, `examples/`, or `agents/openai.yaml`. Determine the delivery flow from the path: `skills/` and `skills-claude/` are live-served source with no publish train (do not invent one); `plugins/` follows the Plugin Layout publish path. Grep `scripts/` for CANON assertions on the target's text.
2. Compute the honest record: enumerate the precedent briefs, tally inversions and holds, read every TLDR, the two nearest-register briefs in full, the latest treatment handoff, and the throughline's treatment-arc paragraph — as calibration of register, depth, and honesty, never as a findings template.
3. Before reading any fire or transcript, write the commission dossier to a scratch file, present it in chat, and treat it as sealed. The run continues by default; JP interrupts if the commission is off. The dossier carries:
   - The pressure questions this target's own text invites. Its self-descriptions — what it owns, why it deserves to exist, how it classifies itself — are claims to test, not facts.
   - Pre-registered expectations: what you currently guess the evidence will show. The critique must later say, in writing, where the evidence corrected these.
   - The named groove hazard for this run: after consecutive holds, hunger for an inversion; after inversions, a genre signature that writes the verdict; a target adjoining prior findings' territory, the remix trap. Name the one that applies now.
   - The circularity traps, concretely: never route the critique through `scrutinize-skill`; never conduct the critique as the target's own genre — name what that would look like for this target and refuse it; never cheaply re-litigate a law that was adversarially won, since overturning it needs evidence of the weight that won it.
   - Privacy boundaries for the expected fire venues, per the evidence recipe.
   - The settled-decisions fence: the charter dispositions, mining decisions, and carve boundaries that stand undisturbed without new evidence.

Fold in any emphases JP passed at invocation.

## Phase 1 — Evidence

Load [references/evidence-recipe.md](references/evidence-recipe.md) and follow it: the full commit history back to founding, the complete fire corpus on both runtimes, consumers and blast radius, and the method context around the target. Fan out with a small dynamic workflow crewed on cheap models — the recipe's rig sets the size and model rules; re-verify firsthand anything the verdict will lean on. Body-loaded proves the body was in context, not a completed run — classify what each transcript actually contains.

## Phase 2 — Critique

Single-mind and never delegated: subagents gather evidence; the judgment is yours. Write the critique as pressure on the method itself. Questions that have earned their keep across the genre — provocations, not sections to fill:

- What is the implicit theory: of the activity the skill performs, and of what its method can know?
- Where do its verdicts, outputs, or artifacts claim more than the method can warrant?
- Do its instruments fire in the fires and change outcomes, or decorate them?
- What authority do its artifacts carry downstream, and did the method earn it?
- Where is the thinking provoked — what would a bare careful agent lose without this text?

Earn every finding from this target's text and these fires; a finding that arrives only by analogy to a precedent is a hypothesis to test or drop, never a conclusion to import. End where the evidence ends.

Floors the brief must carry: line citations against the pinned commit; where the record holds no observed casualty of the method, that is said plainly; the sealed commission corrected in writing wherever the evidence disagreed with it; a close naming what survives and the honest reframe; frontmatter per `docs/reviews/README.md`; an Evidence Boundary and Bounds section that owns what was not inspected and acknowledges the critique is itself a single-judge argued pass — JP's adjudication is its verification layer.

## Phase 3 — Adjudication (hard stop)

Deliver the critique in chat and stop. JP endorses, amends, or rejects it; the endorsed critique is the design brief for the repairs. Do not begin repairs, and do not write the brief to `docs/reviews/`, before the adjudication.

## Phase 4 — Repairs

Scale to what the endorsed critique warrants — edge repairs for a hold, a rebuild for an inversion, occasionally nothing but the brief. Run every change through the `agent-facing-design` gate, classifying per part yourself: judgment parts get a lens, not a score; trust parts stay reliable and single-sourced. Prefer honesty over machinery. Findings on shared seams transfer to siblings: record the transfer in the critique and keep edits scoped to the target — sibling repairs are follow-ons for JP to commission. Rename only if the philosophy demands it, pricing the blast radius by grepping the whole repo first.

## Phase 5 — Validation

Validate every edited surface per the AGENTS.md ladder. Forward-test with blind, non-mutating subagent proxies aimed at whatever instruments changed; a proxy pass is uptake evidence, never value evidence, and simulated assent is noise twice over. Grade whatever proxies cannot reach as untested, honestly, in the commit message.

## Phase 6 — Landing

Repairs commit first; then a `docs(reviews)` commit preserving the critique as `docs/reviews/<date>-<target>-methodology-critique.md` with the landed repair hash filled in; ff-merge to `main`; push — this lane carries standing push authority for its own landing train (JP's per-admission grant; nothing else inherits it). Then save a handoff and refresh the throughline. If validation fails or the adjudication is pending, nothing lands.
