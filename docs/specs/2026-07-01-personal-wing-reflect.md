---
type: design-spec
created: 2026-07-01
status: settled — approved; ~/personal and skills/reflect built in the same session (see Build and Proof)
source: outcome-interviewer → design-exploration session (2026-07-01), grounded in skills/email-writing/SKILL.md, docs/specs/2026-07-01-speakeasy.md, and a direct read of /Users/jp/career
---

# Personal wing — corpus convention + `reflect` (settled design)

The settled design for the **personal wing** of the skill library: a long-term family of skills for JP's recurring personal work and thinking — communication, career, life admin, and thought-partner procedures — judged by JP's freed attention rather than any-repo developer merit, while still shipping globally like every other skill. This doc fixes the wing's one shared piece of architecture (the private corpus convention) and the design of its first skill, **`reflect`**.

## Context and provenance

Produced design-first via an outcome interview and a design-exploration pass in one session. The interview also settled the frontier move this wing represents: the 2026-07-01 capability-growth review **stays valid and frozen — it is deprioritized, not superseded**. Its five engineering openings remain banked backlog; the personal wing is the live frontier. Its candidates were judged legitimate but the wrong *kind* of cognitive-offload for the current focus.

The wing's quality bar comes from a diagnosed prior attempt: `/Users/jp/career` (JP's private career repo, 15 repo-scoped skills + a `profile/` corpus) disappointed on three axes — **too much machinery, outputs not trustworthy, and design predating the library's current standards**. Repo-scoping was explicitly *not* the complaint. Those three axes are the wing's binding standards: minimal machinery held to the judgment bar, output quality as the test that matters, and full current design discipline. The career repo stays where it is; its rebuild is a later band, done to this wing's standards once proven.

What this is: a set of approved design judgments. What this is not: behavior-validated at scale — `reflect`'s output quality is judged by JP's real use (the `email-writing` precedent: only JP can grade it).

## Settled decisions (the interview forks — not for re-litigation in later builds)

- **Merit lens:** wing skills are judged by JP's freed attention (cognitive-offload to JP), not any-repo developer merit. They still ship globally.
- **All sixteen mapped areas are real** (high-stakes messages, self-presentation, distill & capture, long-form prose; application tailoring, interview prep, offer & negotiation, networking upkeep; purchase research, money decisions, bureaucracy & disputes, trip & event planning; personal decisions, reflection & review, goals & direction, worry triage & unsticking). Heat does not discriminate — the wing is a long-term build-out ordered by other principles.
- **Architecture:** lean global procedures + a **private, home-anchored corpus** the skills reference. Wing skill text (this public-ish workshop repo) carries procedure only — zero personal facts.
- **First move:** fix the corpus home + reference convention once, then build organically — each skill brings only the corpus slice it needs; no upfront schema design (fill-in-to-feel-done risk at corpus scale).
- **Corpus home:** a new dedicated private repo at `~/personal` with a private GitHub remote (`jpsweeney97/personal`). Rejected: generalizing the career repo (inherits the machinery JP is unhappy with); local-only (weakest durability).
- **Substrate:** fresh start — no existing vault or journal to seed from.
- **First skill:** reflection & review (**`reflect`**), chosen as corpus-generative: sessions write the values, stories, and lessons later skills draw on. Rejected as the opener: career band first (time-sensitive but not corpus-foundational), substrate-first seeding (upfront elicitation effort with no organic grounding).

## The corpus convention (what every wing skill inherits)

Home: `~/personal/`, its own git repo, private GitHub remote. The path is written into each wing skill — cheap to rename now, expensive later.

```
~/personal/
  AGENTS.md      # one page: what the repo is + these rules (CLAUDE.md is an @AGENTS.md shim)
  journal/       # raw layer: append-only dated entries, YYYY-MM-DD-slug.md
  corpus/        # distilled layer: living slices (values.md, stories.md, …), promoted deliberately
```

- **`journal/` is append-only.** Sessions write new dated files; nothing rewrites history. Entries record what happened and how it landed — nothing more is required for an entry to be complete.
- **`corpus/` holds only JP-confirmed substance.** Every write is propose-diff → JP approval → edit. The approval gate is what makes the distilled layer trustworthy for the skills that later read it.
- **Rules:** (1) a wing skill names the exact corpus paths it reads and writes in its own `SKILL.md`; (2) a missing slice is normal, never an error — proceed without it, offer to seed it, never fabricate corpus substance; (3) personal substance lives only in `~/personal` and is never duplicated into other repos as a second corpus — it flows into work products only when a task calls for it; (4) sessions that write there commit there; push stays on JP's ask.

## The skill: `reflect`

- **Identity:** one hand-authored `SKILL.md`, dual-runtime home `skills/reflect/` (same home as `email-writing`). Summon token `/reflect` or `$reflect`; no collision with bundled names in either runtime or the live roster.
- **Job:** thought-partner processing of lived experience — an event, a decision's aftermath, a stretch of time — surfacing what happened, what it meant, and what deserves to persist in the corpus.
- **Modes:** event-driven ("reflect on X", the default) and periodic ("weekly review" — reads recent `journal/` entries first, then the same conversation over the period). One rhythm, no mode machinery.
- **Rhythm (judgment part):** open by listening — JP's raw account, one question at a time, staying where the heat is rather than marching a question list. Provocations available, never required: what surprised you; fact vs. feeling; what this confirms or contradicts about what JP believed; what you'd tell past-you; is there a story here worth retelling.
- **Hard prohibitions:** no fixed journaling template (no three-gratitudes scaffold, no mandatory sections); no manufactured lessons — an entry that records what happened and how it landed is complete (the no-certificate discipline applied to a life). The promotion pass skips silently when nothing qualifies.
- **Close (trust part):** draft the journal entry in JP's plain words in chat, JP approves or edits, write to `journal/YYYY-MM-DD-slug.md`, commit in `~/personal`. Then one light promotion pass: only if something genuinely durable surfaced, propose the concrete `corpus/` edit for approval.
- **Boundaries:** not `postmortem` (incident retro → repo artifact), not `research-capture` (external findings), not `save-handoff` (work-session resume), not `outcome-interviewer` (forward-looking goal clarification). When a reflection surfaces a live decision, route onward rather than becoming a decision engine.

## Authoring gate (mixed skill, bar per part)

- **The conversation = judgment bar** ("protect and provoke better thinking"): the provocation list must stay a provocation, never a walked checklist; no scaffold may perform the reflection for the agent.
- **The corpus writes = trust bar** ("reliable, single-sourced"): append-only journal, approval-gated promotion, missing-slice behavior, and the commit step are defined, safe defaults — justified because a silently rewritten journal or an unapproved distillate is a wrong value JP cannot see.

## Open / deferred

- **Push-by-default for `~/personal`** — the repo is backup-motivated but push stays on-ask per JP's norms; flip only on JP's say-so.
- **Wing build order beyond `reflect`** — organic; no queue is fixed here. Candidate seams (personal decisions vs `making-recommendations`, goals slice, career band) get their own design passes.
- **Career repo rebuild** — later band, to the wing's standards; `profile/` may migrate into `~/personal` then.
- **speakeasy** — stays settled as-is (inline committed profile per its own spec); a future v2 may adopt the corpus convention, not re-litigated here.
- **`reflect` entry frontmatter/tags** — deliberately none in v1 (filename date + slug only); add only if periodic reads prove to need it.

## Build and proof (executed this session)

1. Create `~/personal`: git init, private GitHub remote, stub `AGENTS.md` (+ `CLAUDE.md` shim), `journal/` + `corpus/` dirs, initial commit. Nothing pushed.
2. Hand-author `skills/reflect/SKILL.md` through `agent-facing-design` + `skill-ux-design`; validate per the repo Validation Ladder (`quick_validate.py`, frontmatter parse, `git diff --check`); link via `scripts/claude-skills-sync.sh --link reflect` and verify with `--check`.
3. Behavior-smoke-test aimed at the discipline, not just parsing: appends rather than rewrites, skips promotion when nothing qualifies, refuses to manufacture a lesson, routes a surfaced decision onward.
4. Output quality is proven only by JP's real use — first real reflection session seeds the journal; watch-and-prune from there.
