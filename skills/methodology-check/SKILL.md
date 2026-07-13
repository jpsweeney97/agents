---
name: methodology-check
description: "Use when you want a cheap, single-pass read on whether a skill's method is sound — its premise, epistemology, implicit theory — from the skill's text plus a fire census (does it run; which declared instruments are dead). Dual-runtime, single-agent; the default methodology pass — heavier than scrutinize-skill's contract-altitude detection, lighter than methodology-critique's fire-tested treatment, which it escalates to when how the target fires in real transcripts is the crux. Not for contract/execution review (scrutinize-skill), benchmarking (skill-benchmark), or routine editing."
---

# Methodology Check

The cheap adjudicator of a skill's method: one read-only pass over the target's text plus a cheap census of its real fires, rendering the methodology verdict the neighboring lanes don't — above `scrutinize-skill`'s contract altitude, below `methodology-critique`'s fire-tested treatment.

It is dual-runtime and single-agent, and it touches nothing: no edits, no commits, no invocation of other skills. It delivers a verdict and stops.

## What counts as a finding — the altitude test

The failure this lane exists to avoid is drifting down into `scrutinize-skill`: filing contract findings — vague wording, unclear output shape, routing hygiene — dressed in methodology vocabulary. One test holds the altitude. A finding belongs here only if all three hold:

1. It bears on the target's **central epistemic claim** — what the method asserts it can *do or know*.
2. A `scrutinize-skill` contract pass **would not already catch it**. State this per finding, out loud: "not a contract finding because ___." If you cannot complete that sentence, the finding is scrutinize-skill's, not yours — drop it.
3. It is **decidable on text + census** — not on how the method fires in real transcripts.

A finding that fails (1) or (2) is the drift; refuse it. A finding that fails only (3) is real but not yours to decide — it escalates (see Findings).

## First move: the anchor

Before any census, in two or three sentences, state and seal:

- the target's **central epistemic claim** in one sentence — what it asserts it can do or know (e.g. "MAP scoring measures option quality"; "grilling a plan against the codebase hardens it beyond bare grilling");
- your **provisional verdict** on whether that claim holds;
- which of the target's instruments **the census can adjudicate** — its on-demand surfaces (a `references/*` file, a conditional branch loaded only when its case triggers) — you expect live vs. dead in real use; for an all-body target, predict instead whether the skill genuinely fires at all.

This is your prior, sealed. The verdict must later say where the evidence corrected it — a reversed prior stated in writing is the most honest thing this lane produces, not an embarrassment. If you cannot state the central claim, you are not yet at methodology altitude; read more of the target until you can.

## Evidence — text, then census

**Text.** Read the target bundle and grep the repo for its consumers — who routes to it, and what authority its outputs carry downstream. Interrogate the method's implicit theory: of the activity it performs, and of what its method can know; where its verdicts or artifacts claim more than the method warrants; what a bare careful agent would lose without this text. These are provocations, not sections to fill.

**Census.** Enumerate the target's real fires cheaply. The census has two layers with different reach:

- *Enumeration (grep — complete for any corpus size).* Pick 2–3 distinctive **body-sentence markers** from the target's `SKILL.md` — never the skill name (roster injection puts the name in every session). Grep them across the Claude session transcripts (`~/.claude/projects/`) and the Codex rollouts (`~/.codex/sessions/`) — the two surfaces where skill bodies actually appear in context. A marker that appears **zero** times across the complete grep of both transcript surfaces proves that instrument dead — you cannot be in-context-but-not-run if you were never in context at all.
- *Classification (skim — sample if the corpus is too big for one pass).* Upgrade "the marker appeared" into "the method genuinely ran." When candidates exceed one pass, bound only this layer: state the sampled subset, read the highest-signal first (user-typed invocations, then recent, then full-cycle runs), mark the rest `unverified`, and never report the genuine-fire count as complete. Grep-proven absence is never downgraded to sampled.

**Grade the census** honestly by what it can carry:

- **drives** — a zero-fire skill, or a large corpus with a grep-proven dead instrument;
- **contextualizes** — a mid-size corpus: it confirms the skill is used but sharpens nothing on its own;
- **inconclusive** — a thin corpus, where absence is *not* proof of deadness. Do not call an instrument dead on a thin corpus.

**Census confounds — clear every one before resting a finding on the census:**

- The Claude ledger (`~/.claude/logs/skill-usage-ledger.jsonl`) is **invocation-only**: it records that a skill fired, keyed by name, not its body, so it is never a marker-grep surface — its zeros say nothing about deadness. Use it for name-keyed fire *counts* alongside the transcript greps, never for marker absence.
- **Whole-body injection floors body-instruments together.** When a skill fires, its whole `SKILL.md` body enters context, so every body-marker co-occurs at the fire count and *cannot discriminate one body-instrument's deadness from another*. Per-instrument deadness is cheaply probeable only on **on-demand surfaces** — a `references/*` file or conditional branch loaded only when its case triggers, where the *named-vs-loaded* ratio is real signal (a reference named 500 times but loaded 5 times is near-dead). For a body-instrument, say "not cheaply probeable" — do not guess.
- **Contamination.** A marker that also sits in the skill's roster-injected *description* appears everywhere; drop it. Maintenance, authoring, and review sessions that touch the `SKILL.md` path, and markers shared with a sibling skill, are detection noise, not fires — classify them out.
- **Marker vintage.** The grep runs the *current* body's sentences against a historical corpus: a sentence added or reworded after a fire greps zero against every transcript from before the edit, manufacturing false deadness. Before resting an absence claim on a marker, find when it entered the body (`git log -S '<marker>'`) and bound the claim to fires after that date; a marker younger than the corpus proves nothing about the older fires.
- **Corpus retention.** The transcript surfaces are rolling windows, not archives: Claude Code prunes old session transcripts, and each corpus's reach differs — measure it (the oldest file date), never assume it. Grep-proven absence covers only the surviving window; for a skill older than the window, zero hits say nothing about earlier fires. Bound every absence claim to the measured window, exactly as vintage bounds it from the other side.

## Findings — decide what you can, escalate the rest

Tag every finding:

- **Decided-here** — text and census settle it; render the verdict.
- **Escalate-rider** — the *structural* claim is decided here, but its **real-world bite-rate** (whether the instrument actually fires in the wrong direction, and how often) needs how-it-fired evidence you cannot see. Decide the structure and attach the rider. For example: "the code-check has no not-found failure branch, so it *can* upgrade an unfound claim into 'code-checked' — decided; how often it actually does needs the real fires — escalate."

You cannot observe behavioral direction. When a finding's warrant needs *how* a live instrument fired, do not render a verdict on it — tag the rider and stop there. A confident verdict on unseen behavior is the one failure worse than drift.

## Verdict and escalation

Deliver in chat, read-only:

- the anchor, and where the evidence corrected it;
- the admissible findings with their tags;
- the graded census;
- a **verdict bounded to the decided-here set** — say plainly "on text + census," and name what you did not inspect;
- for every escalate-rider, one scoped recommendation: "to settle whether it fires the right way, commission `methodology-critique` on this axis." **Never invoke `methodology-critique` yourself** — it is JP-commissioned, Claude-only, and expensive by design; you recommend, JP decides. The recommendation stands even from a runtime where `methodology-critique` is unavailable — JP commissions it from a Claude session.

## Aftermath

Chat-first. Persist nothing by default — this pass is cheap to re-run, so a quick read stays in chat.

Persist only when the verdict is decision-shaping, and then as its own genre: `docs/reviews/<date>-<target>-methodology-check.md`, **never** `*-methodology-critique.md` (that namespace is the fire-tested treatment's tallied arc, and a text+census verdict dropped there pollutes it). A persisted brief carries a mandatory **Evidence Boundary**: text + census only, behavioral direction not inspected, a single-judge cheap pass whose verification layer is JP's reading — not a fire-tested adjudication.

Repairs, the full treatment, and any edit are separate, user-initiated follow-ons. This lane stops at the verdict.

## Routing

- Contract and execution altitude — "will the skill behave well once it triggers" — is `scrutinize-skill`'s.
- When the crux is how the skill fires in its real transcripts, the lane is `methodology-critique` where available (Claude-only): escalate by recommendation, and on runtimes without it the recommendation is still the deliverable.
