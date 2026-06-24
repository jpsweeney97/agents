---
name: friction-to-guards
description: "Use when the user asks to review recurring corrections, repeated feedback, or session friction and make it durable, including asks like 'I keep correcting this', 'make this stick', or 'turn this feedback into a guard'. Do not use for one-off feedback, hook or settings mechanics alone (update-config owns those), memory bookkeeping, or skill edits without a friction review."
---

# Friction To Guards

Turn recurring corrections into durable guards. This lane owns the judgment step between repeated feedback and permanence: finding what keeps recurring, choosing the right durable tier for each item, and proposing — never applying — the change. The cost of skipping this step is real in both directions: corrections that evaporate at session end, and corrections over-promoted to global rules that every future session must read.

## Gather Evidence

Collect candidate friction from the surfaces available, and say which were checked:

- Corrections and pushback in the current conversation.
- Memory entries, especially `feedback`-type files, in the project memory directory.
- Recent handoffs under `<project_root>/.agents/handoffs/` when present.
- Anything the user names directly.

## Separate Recurring From One-Off

A correction is recurring when it appears in two or more independent contexts — separate sessions, separate tasks, or a memory entry plus a fresh occurrence. One-off corrections do not escalate: act on them in-session and at most save a feedback memory. Do not manufacture guards to have something to propose; finding no recurring friction is a valid result — say so.

## Choose The Tier

For each recurring item, propose the lightest durable tier that actually prevents recurrence — not the strongest tier available:

1. **Memory entry** — advisory, cross-session. Default for preferences, context, and anything an informed future session would honor.
2. **Instruction line** — global `CLAUDE.md` or repo `AGENTS.md`/`CLAUDE.md`. For behavior rules every session must follow. Each line taxes every future context load; a line must earn that.
3. **Owning-skill edit** — when an existing lane owns the work and the correction belongs in its contract, not in global prose.
4. **Hook** — enforcement that bites. Only when a lighter tier has already failed for this same correction, or when one more recurrence causes damage advice cannot be trusted to prevent.

A lighter tier's documented failure is the evidence that justifies the next tier. Escalating past a tier that was never tried needs an explicit reason.

## Propose, Then Stop

Present the proposals and apply nothing without the user's approval. For each recurring item give: the correction, the recurrence evidence, the proposed tier and target surface, and why a lighter tier would not hold.

Route approved applications through the owning lane rather than editing directly from here: `update-config` for hooks and settings when available, `writing-principles` for `AGENTS.md`/`CLAUDE.md` prose, the owning skill's editing path for contract changes, and the agent-facing design gate before any materially new agent-facing obligation. Memory entries may be written directly.
