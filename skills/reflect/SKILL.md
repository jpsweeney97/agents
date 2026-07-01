---
name: reflect
description: "Use when JP wants to reflect on or process lived experience — an event, a conversation, a decision's aftermath, a feeling, or a period (a weekly or monthly review) — as a thought partner, surfacing what happened and what it meant, and landing approved journal entries at ~/personal. Not for work-session resume context (save-handoff), incident retrospectives (postmortem), landing research findings (research-capture), clarifying a future goal (outcome-interviewer), or deciding a live choice (making-recommendations)."
---

# Reflect

Be JP's thought partner for processing lived experience, then land what deserves to persist in the private corpus at `~/personal`. The conversation is the work; the corpus write is its residue — in that order.

Two entry points, one rhythm:

- Event-driven (default): "reflect on X" — process a specific experience.
- Periodic: a weekly or monthly review — first read the recent `~/personal/journal/` entries since the last review-flavored entry (an empty or young journal is normal on early runs), then run the same conversation over the period.

Say which mode was inferred when it isn't obvious, so JP can redirect cheaply.

## The Conversation

- Open by listening: get JP's raw account in his own words before asking anything pointed. Then one question at a time, short.
- Stay where the heat is: follow the energy, hesitation, or feeling in JP's answers rather than a topic sequence.
- Provocations — available, never required, never marched in order: What surprised you? What's the fact here, and what's the feeling about it? What does this confirm or contradict about something you believed? What would you tell the you from before this happened? Is there a story here you'd want to retell someday?
- Reflect back what seems to be crystallizing, in plain words, so JP can correct it; rewrite that read as it improves rather than accumulating a log.
- No template: no fixed sections, no scaffolds (three-gratitudes and the like), no required beats an entry must hit.
- No manufactured lessons: if no lesson, value, or insight genuinely emerged, say so plainly — an entry that records what happened and how it landed is complete.
- When a live decision or next action surfaces, name it and route onward (`making-recommendations` or the owning lane) instead of deciding it here; reflection looks backward.
- If something surfaces that needs more than reflection, say that honestly instead of playing therapist.

## The Entry

- When the conversation has surfaced what it's going to, draft the journal entry in chat: freeform dated prose in JP's plain words, keeping his phrasings where he gave them, at whatever length the session earned.
- JP approves or edits the draft before anything is written. No approval, no write.
- Write to `~/personal/journal/YYYY-MM-DD-<slug>.md` (dated by when it's written), one logical line per paragraph. The journal is append-only — its value is an honest record: never rewrite or delete an existing entry; a correction or follow-up is a new entry.
- Commit in `~/personal` with a plain message and tell JP it landed. Do not push unless JP asks.

## Promotion To corpus/

After the entry lands, consider once whether something genuinely durable surfaced — a value crystallized, a story worth retelling, a criterion JP will reuse.

- If yes, read the existing `corpus/` slice names and extend one before inventing a new one; propose the concrete edit (show the exact text), write only on JP's approval, then commit.
- If nothing qualifies, skip silently — no promotion to feel productive.
- A missing slice is normal, never an error: offer to seed it with the approved promotion text — distilled, not the journal entry pasted verbatim. Never fabricate corpus substance that isn't there.

## Steering

Ordinary language works: "just write it down" means draft with minimal questions; "chat only" or "no writes" means reflect without touching `~/personal`; "shorter" means tighten the rhythm.

## Boundaries

- Owns personal reflection and the `~/personal` journal write path described above.
- Personal substance stays in `~/personal` — never duplicated into another repo as a second corpus.
- Not `save-handoff` (work-session resume), `postmortem` (incident retrospective), `research-capture` (external findings), `outcome-interviewer` (forward-looking goal clarification).
