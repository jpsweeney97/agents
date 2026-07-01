---
type: design-spec
created: 2026-07-01
status: settled — unbuilt (run the one-time profile-build session first, then hand-author through agent-facing-design + skill-ux-design; prove with a behavior-smoke-test)
source: outcome-interviewer → design-exploration session (2026-07-01); grounded by the design-context-scan Workflow (run wf_3878468e-202, 4 readers) and skills/email-writing/SKILL.md
---

# speakeasy — spoken-voice rewrite skill (settled design)

The settled design for **`speakeasy`**, a new hand-authored Claude skill that rewrites AI-generated writing meant to be read *aloud* so it sounds like JP talking — plain-spoken, reactive, thought-out-loud — and trims it for the ear. Produced design-first via an outcome interview and a design-exploration pass; the skill is not yet built. This doc is the reference the build consumes.

## Provenance and honest margin

The outcome was clarified one question at a time (`outcome-interviewer`), then shaped into this design (`design-exploration`). Repo grounding came from a 4-reader `design-context-scan` Workflow (run wf_3878468e-202). Two of the four readers (the `email-writing` deep-read and the text-transform survey) returned placeholder junk; the `email-writing` sibling was therefore read directly by hand rather than trusted from a subagent summary. The storage and authoring-gate findings held up and are reflected below.

What this is: a set of design judgments. What this is **not**: behavior-validated. Nothing here has fired on real work yet. The single largest unbuilt dependency is the voice profile's *content* (§4), which does not exist until the profile-build session runs.

## Settled decisions (the interview forks)

These were each decided during the outcome interview and are **not** open for re-litigation in the build:

- **Voice target — JP's specific spoken voice**, not a generic "sounds human" voice.
- **Learns once → durable profile → one-button rewrite.** JP feeds samples up front; the voice is distilled once and carried by the skill. After setup, hand it a draft, get back JP's voice. (Rejected: passing fresh samples per run.)
- **Highest-signal source material:** (1) verbatim transcripts of JP actually talking in-register (recorded interview, call, voice memo), unedited — fillers and self-corrections intact, because cleanup destroys the target traits; (2) before/after pairs (AI draft → JP's hand-fix), uniquely valuable because they teach the *transform*, not just the destination. JP's *written* prose (emails, docs) is a poor, misleading source — spoken voice is a different instrument.
- **Transform license — may cut, compress, and reorder for the ear**, not merely re-voice, because a full written draft is too much to say aloud. (Chose the more powerful transform over a strict meaning-preserving voice-pass.)
- **Content-trust guardrail** (JP's stated nerve, "can't silently drop something load-bearing"): default = trim freely but return an auditable "here's what I cut" so JP can catch and restore anything load-bearing; opt-in = JP pins "must-keep" lines the skill won't touch.
- **Failure-mode bias — err toward "too much."** When unsure how hard to lean on the voice, commit rather than play safe; a too-safe rewrite that still faintly smells of AI defeats the whole point. This bias is about *voice intensity*; content fidelity is protected separately by the audit + must-keeps, so there is no contradiction.

## The design

### 1. Identity and placement

One hand-authored Claude skill, a single `SKILL.md`, no runtime mode-switching. Home: `skills/` (dual-runtime, the same home as `email-writing`) — a Markdown voice profile is runtime-agnostic, so default here unless a concrete Claude-only dependency appears.

Name: **`speakeasy`** (chosen by JP). Recorded caveat: the name breaks the repo's function-descriptive naming habit (`email-writing`, `markdown-reformat`) and shares a name with existing dev tools (the `speakeasy` TOTP library / the Speakeasy API company), so it carries no routing signal on its own — the `description` does that work. Nothing depends on the name yet, so a later rename is a cheap dir-rename + `scripts/claude-skills-sync.sh` resync. The "speak-easy → easy to say aloud" reading is thematically apt.

### 2. Routing (frontmatter `description`)

Draft (quote it in YAML — it contains colons):

> Use when rewriting a draft that will be read **aloud** — a script, speech, or notes for a call, meeting, or interview — into JP's spoken voice: plain, reactive, thought-out-loud, trimmed for the ear. Not for text meant to be read on the page (essays, articles, reports), JP's written email voice (`email-writing`), or generic prose polish.

~55 words; within the 25–60 soft budget; names the `email-writing` boundary as the likely misroute.

### 3. What the skill does (the rewrite — a *judgment* part)

Takes a draft meant to be spoken and returns it in JP's voice, doing two things at once:

- **Re-voice:** reactive openers where the line genuinely invites one, short sentences and fragments, contractions, plain concrete words, warm-but-composed register, hands the turn back with a real question where it fits.
- **Trim for the ear:** cut, compress, and reorder, because a written draft is too much to say aloud.

**The intensity dial (JP's "err toward too much"):** when unsure, commit to the voice — go *more* human, not safer. The guard against caricature is not hedging back toward smooth; it is not *manufacturing* tells. Commit hard on real occasions (a line that is actually a reaction earns the "Yeah, that's fair"); do not bolt an opener onto a line that is not one, or fragment a sentence that needs to stay whole to be clear. Commit to the voice; do not fake the occasions for it.

### 4. The voice profile (inline, exemplar-first)

Lives inside `SKILL.md`, built once from JP's samples. Four parts, led by examples:

- **Calibration Examples** — the primary carrier: before/after pairs (AI draft → JP's spoken rewrite). This is where JP's idiosyncrasy lives; the rewrite works mostly by resemblance to these. (Mirrors `email-writing`'s "Calibration Examples" block.)
- **Thin voice rules** — an `Allowed`/`Avoid` sketch for what the pairs do not show.
- **AI-tells to kill** — the page-smell checklist: parallel triads, "it's not just X, it's Y," "here's the thing," corporate abstraction, hedge stacks, robotic uniform sentence length. Doubles as the ear-check list (§6).
- **Intensity note** — the dial from §3, stated once.

Raw transcripts and the full before/after set stay in gitignored scratch (`.agents/scratch/`); only the *distilled* profile is committed inside the skill directory. (Storage is constrained by delivery: skills ship by symlinking the whole skill directory, so any durable data must live inside it and is committed. No skill reads a personal file from outside its own directory.)

### 5. Content trust (the guardrail — a *trust* part)

- **Auditable cuts (default, always on):** after rewriting, show a compact `Trimmed:` list outside the draft — what was cut, merged, or reordered — so JP can restore anything load-bearing at a glance.
- **Must-keeps (opt-in):** JP pins lines that must survive (mark them in the draft, or say "keep: …"); the skill never drops or alters their meaning and confirms them back (`Kept as-is: …`). Off by default so the common case stays one-button; for a flagged high-stakes piece it may ask once.

This machinery is single-sourced in this one `SKILL.md`; it must not be hand-copied into other skills. The profile and the cut-log *provoke and evidence* the rewrite — they must never become fill-in templates that make the voice decision for the agent.

### 6. Ear-check (verification)

Before presenting, the skill re-reads its own draft against the AI-tells list (§4) and reads it for the ear — *does this sound like the after column, not the before?* — fixes what it catches, then hands it over. A self-check pass inside the one flow, not a separate mode or a heavy gate.

### 7. Output shape (follows `email-writing`)

- The rewritten text in a fenced **code block** (easy to copy).
- Below it: the `Trimmed:` cut-list, any `Kept as-is:` confirmations, and at most a one-line style note. A light "read it aloud once to check it lands" nudge.
- Steer, not analyze — no essay about the writing.

### 8. Boundaries / non-goals

For the ear, never the page. Not essays, articles, or reports. Not JP's written email voice (→ `email-writing`). Never silently drops content. Does not send or publish anything.

## Why this shape (approaches considered)

Chosen: **A — rewrite-only skill, inline exemplar-first profile, one-time authoring session.** It is the smallest design that fully meets "learn once → one-button," on the proven `email-writing` shape; exemplars carry JP's idiosyncrasy where rules flatten it into generic "casual," and imitating real samples is the natural guard against caricature.

Rejected for v1:

- **B — two-mode skill (in-skill distiller that writes `references/voice-profile.md`, then rewrites).** Real added machinery for a set-it-once job; the distiller is a judgment task dressed as a procedure. Only earns its keep if JP wants self-service *re-distillation* without an authoring session — he confirmed one-and-done, so this is deferred, not dead.
- **C — pure exemplar / few-shot (only before/after pairs, no rules).** Maximal fidelity but no explicit intensity dial and nothing to lean on for cases the examples do not cover. Approach A already takes C's exemplar-first core while keeping a thin rule layer and an explicit dial.

## Authoring gate (this is a *mixed* skill)

Judged per part, not per skill:

- **Rewrite = judgment bar** ("protect *and* provoke better thinking"): keep the forcing functions sharp; do not over-scaffold; do not let a template perform the voice instead of provoking it.
- **Must-keeps + auditable-cuts = trust bar** ("reliable, single-sourced"): defined steps and safe defaults are the value here. Justified because silently dropping a must-keep is a wrong value the agent cannot see — signal what was cut. "A capable model would keep them anyway" is never on its own a reason to cut the guardrail.

## Open / deferred

- **Profile content does not exist yet** — the rules, the before/after pairs, and the intensity calibration come from JP's raw samples in the one-time build session. This is the build's first job.
- **Must-keep marking convention** — exact syntax (`[[…]]`, "keep: …", etc.) finalizes during authoring.
- **`skills/` vs `skills-claude/`** — defaulted to `skills/`; revisit only if a concrete Claude-only dependency appears.
- **Self-service re-distillation (Approach B)** — parked; revisit only if one-time setup proves insufficient in practice.

## Build and proof (next moves)

1. **Profile-build session** — JP brings a couple of verbatim talking-transcripts and a few AI-draft → hand-fix pairs (parked in gitignored scratch); distill them into the §4 inline profile.
2. **Hand-author `SKILL.md`** through `agent-facing-design` + `skill-ux-design` (no Claude-side constructor); validate with the Codex `quick_validate.py` and `git diff --check` per the repo Validation Ladder.
3. **Prove behavior, not just parsing** — a behavior-smoke-test: feed a real AI draft and confirm it rewrites in-voice, trims, shows the cut-list, honors a must-keep, and runs the ear-check.
