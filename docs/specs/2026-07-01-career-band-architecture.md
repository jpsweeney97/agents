---
type: design-spec
created: 2026-07-01
status: settled — approved; stage 1 executed 2026-07-03 (corpus migration + fleet retirement landed in career + personal); stage 2 deferred until a search looms
source: outcome-interviewer → design-exploration session (2026-07-01), grounded in a full diagnostic read of /Users/jp/career, skills/reflect/SKILL.md, skills/email-writing/SKILL.md, and docs/specs/2026-07-01-personal-wing-reflect.md
---

# Career band — architecture: corpus migration + collaboration/capture convention (settled design)

The settled architecture for the personal wing's career band: where career substance lives, how career-band skills collaborate and capture, and what happens to `/Users/jp/career`. This doc is the band's constitution; band skills are built later, organically, against it. It extends the wing constitution (`docs/specs/2026-07-01-personal-wing-reflect.md`) and does not modify it.

## Context and provenance

The 2026-07-01 wing spec deferred the career repo rebuild as a later band. JP pulled it forward the same day. A full diagnostic of `/Users/jp/career` (15 repo-scoped skills ≈ 2,150 lines duplicated across two identical trees, ~9,500 lines of `tools/` write-safety and enablement-proof machinery, a 265-line AGENTS.md) confirmed the wing spec's three-axis diagnosis and localized it: the machinery is concentrated in the pursuit-state write system (`pipeline`, `role-scout`, `tools/stage_*`, the AGENTS.md proof floors), while the content-skill layer has good bones and `profile/` (754 lines, five files) is genuine corpus substance.

The interview then found the deeper root. The outputs that disappointed JP failed on voice/generic trust and judgment trust equally — never on facts. The machinery guarded the one thing that was never broken. And `email-writing`, the library's best prior attempt at the voice problem, underdelivers on all four failure faces at once (off-script collapse, surface mimicry, one flat register, off choices) — which is one root wearing four faces: the skills had samples of JP's words but almost none of JP — his stances, relationship context, situation-reads. Voice is not a styling layer over content; it is judgment expressed in prose.

## Settled decisions (interview + design forks — not for re-litigation)

- **Root diagnosis:** substance gap, not style gap. `email-writing` is evidence about the problem, not a pattern to copy.
- **The accumulation bet:** the fix is a living corpus grown from real use — stances, relationship context, and especially corrections, which today evaporate with every heavy rewrite. Trust in routine artifacts is earned over months, not declared at build time. (Rejected: the ceiling bet — design everything as permanent collaboration and stop chasing autonomy; rejected as the primary frame, though high-stakes artifacts keep the collaboration design below.)
- **Split by artifact:** routine correspondence aims at factory grade via accumulation; high-stakes self-presentation (resume, cover letter, interview positioning) is collaborative by design, permanently.
- **Scope order:** architecture now (this doc); employed-era pieces built organically as real needs fire after 2026-07-20; the application factory rebuilds to this architecture only when a search actually looms. Rationale: accumulation needs live use to feed it, and post-acceptance the live use is employed-era work.
- **Capture posture:** invisible-by-default with judgment-gated corpus-write proposals, plus `reflect`-style periodic distillation as backstop. JP accepts slower accretion as the price of low friction.
- **Surfaces:** career and personal state are effectively local-only now. No write-safety machinery is rebuilt in any form; approval gates + commit-after-write cover it.
- **Privacy tier:** one tier — everything commits to `~/personal` (private repo, private remote), consistent with what JP already accepted for `reflect`'s journal. The `*.local.md` convention retires for `~/personal`; legacy workspace `*.local.md` files stay gitignored where they are.
- **Architecture shape:** flat integration (chosen over a namespaced `corpus/career/` sub-tree and over full absorption of the career repo). Career substance becomes ordinary `corpus/` slices beside the rest of JP — because the root diagnosis is that the skills didn't know the person, and the person is one person: work stories are life stories; a relationship model serves a networking email and a personal high-stakes message alike.

## The migration map (stage 1 executes this)

`career/profile/` migrates near-1:1 into `~/personal/corpus/` — content moves, no re-authoring during migration:

| From `career/profile/` | To `~/personal/corpus/` | Note |
|---|---|---|
| `profile.md` | `career-profile.md` | renamed — `profile.md` is ambiguous inside a corpus |
| `stories.md` | `stories.md` | seeds the general stories slice `reflect` already expects |
| `projects.md` | `projects.md` | as-is |
| `narratives.md` | `narratives.md` | approved phrasings; serves beyond career |
| `opportunity-thesis.md` | `opportunity-thesis.md` | provenance header updated to slice paths |

New slices the old repo never had — `people.md` (relationship models: who someone is, JP's history with them, the register he uses) and `voice.md` (distilled correction patterns) — are deliberately not created now. Per the wing convention, a slice is seeded the first time a skill has something real to put in it. `jp-writing-style`'s raw writing samples stay in career git history; migrate them only when voice work first needs them.

## The collaboration/capture convention (what every career-band skill inherits)

Single-sourced here; each band skill authors its inherited copy inline per wing rule 1. No ambient contract; no charter event.

- **Collaboration shape (high-stakes artifacts):** the skill leads with its thinking, not just prose — the thesis it built, the stories it picked and why — so JP's steering takes seconds. JP's rewrite is treated as signal, never noise.
- **Invisible capture:** when a session clearly surfaces durable substance — a stance, a relationship fact, a correction pattern — the skill proposes one concrete corpus diff at a natural pause or session end. Silent skip is the default; never a mid-flow interruption; at most one capture ask per session. Approval-gated like every corpus write.
- **Corrections:** when JP hand-rewrites a draft, the skill may — judgment-gated — offer to keep the distilled pattern (e.g. "strips warm openers with recruiters") in the relevant slice. One-off corrections are allowed to evaporate; that is the accepted price of low friction. No raw-pair archive.
- **Periodic backstop:** `reflect`'s periodic mode already covers it — career events land in the journal like anything else and distill on review. No career-specific ritual is built now.

The failure mode this convention exists to prevent is the capture ceremony: every draft ending in "shall I log that?", every conversation becoming data entry — `pipeline` reborn wearing a friendlier face. If capture friction is ever what JP notices, the convention is being violated.

## Old repo disposition (staged)

- **Stage 0 (now):** nothing moves. Offers are live (athenahealth terms expire 2026-07-06; Accordion response requested by 2026-07-07); the repo keeps working as-is.
- **Stage 1 (on JP's go, after the offer decision):** migrate the five slices; replace `career/profile/` with a short pointer note; retire the fleet — all 15 skills, both duplicate skill trees (`.agents/skills/` and `.claude/skills/`), `tools/stage_*`, both runtime matrices and their checkers, and the 265-line AGENTS.md, replaced by a one-page AGENTS.md (workspace map + surviving floor rules). `tools/md_to_docx.py` survives. Deletion is `trash` + git history; nothing is lost.
- **Stage 2 (when a search looms):** the factory band rebuilds as global wing skills reading corpus slices and writing the pursuit workspace. Explicitly not designed here.

The career repo survives stage 1 as pursuit workspace only — `pursuits/`, `PIPELINE.md`, `resumes/`, exports — working files, not corpus, until the current search closes.

## Rules that travel

- **Hanlon exclusion** moves with the substance: a boundary note at the top of `corpus/career-profile.md` (the Hanlon CPA clerical role never appears in resume-line positioning), so any future consumer inherits it.
- **Facts-never-invented** becomes a property of the corpus itself: slices hold only JP-confirmed substance; a claim a slice cannot back is a gap to report, not a line to write.
- **Company-facts-sourced-never-from-memory** travels into future band skills that make company or market claims.
- **Verbatim-JD capture and pursuit lifecycle** go dormant with the factory; stage 2 revives what it needs from career git history.

## First feeders

The offer-decision session (`making-recommendations`, before 2026-07-06) seeds decision criteria and stances. `reflect` sessions seed journal entries and promotions. Stage-1 migration lands the five slices whole. `email-writing` is the first routine-band rebuild candidate — organically, when it next disappoints — gaining `people.md` reads and this capture convention.

## Non-goals

No new skills built now. No corpus schema beyond the migration map. No capture ceremony. No write-safety tooling. No speakeasy changes (its spec stands as-is). No edits to the frozen wing spec or the live career repo during stage 0.

## Open / deferred

- **Stage-1 execution date** — JP's call, after the offer decision.
- **Stage-2 factory design** — its own design pass when a search looms; the diagnostic map (this session) and career git history are its inputs.
- **`people.md` / `voice.md` seeding** — organic, first real need.
- **`email-writing` rebuild** — organic, on its next real disappointment.
- **A career-flavored periodic review** — only if `reflect`'s periodic mode proves insufficient for career distillation.
