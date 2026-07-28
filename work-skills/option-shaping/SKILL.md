---
name: option-shaping
description: "Use when two or more named, meaningfully distinct options already exist but remain sketch-level or unevenly understood, and the user wants them developed to comparable resolution before any ranking or choice. Produces a rank-free comparison surface. Do not use to widen the field, clarify a muddy outcome, choose among already-comparable serious options, or develop one approach into an approved design."
---

# Option Shaping

Turn a user-supplied fixed field of sketch-level options into a rank-free comparison surface. Equalize resolution — how much is actually understood about each option — not certainty, word count, or favorability. Respond in chat by default.

## Workspace and Safety Boundary

Before handling work content or creating a durable artifact, read the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy. That workspace controls access, classification, permitted destinations, and retention. When classification, permission, source authority, or destination is unclear, take the more protective route and stop for clarification; do not infer authority.

A shaping request does not authorize browsing, connector use, experiments, file writes, tracker changes, sending, publication, installation, or Git operations. Do not stage, commit, stash, or push target-work content. If the user separately requests a durable artifact, first confirm that the destination is explicitly permitted by the active workspace; otherwise return the comparison in chat.

## Freeze the Field

- Work on exactly the candidates the user selected. Do not choose a promising subset, add alternatives, generate replacements, or silently drop an awkward option.
- Do not merge, split, or rename an option in a way that changes its bet. If two options appear to succeed or fail for the same underlying reason, name the collision and ask whether the user wants them treated as one.
- If a user-confirmed hard constraint would exclude an option, name the consequence and ask the user to confirm the revised field before continuing. Applying filters is not this lane's decision.

## Develop in Rounds

1. Derive the smallest set of live comparison questions from the desired outcome, binding constraints, and candidates. A question is live only when plausible answers could distinguish the options, change an option's basic viability, or expose an assumption that could reverse the eventual choice.
2. Take one question across every option before moving to the next. Give each option equivalent scrutiny, not equal word count.
3. Develop each answer only as far as the available, permitted evidence supports: a grounded fact with its source, an explicit assumption and what follows from it, or a named evidence gap and why it matters. Mark agent inference `unverified`; never fill an empty cell with plausible prose.
4. Make each option's underlying bet intelligible under those questions — its mechanism, consequential dependencies, and evidence gaps — without completing a design or arguing for or against it.
5. Run a bias pass. Check whether one option received more charitable assumptions, implementation detail, vivid language, or effort merely because it felt attractive. Correct the asymmetry; do not certify the result as neutral or unbiased.

Round-robin development is the forcing function. It prevents the favored option from receiving a finished narrative while its rivals remain slogans, but it never decides which answer is better.

## Evidence Boundary

Use evidence the user supplied and sources directly available within the active workspace and permitted by its rules. Inspect them when they can answer a live question, but do not broaden the task into external research or experiments merely to make the options look equally complete. Ask before any separately authorized evidence-gathering action.

Unequal certainty is allowed; hidden uncertainty is not. If a missing fact prevents an option from becoming intelligible or could reverse its basic viability, name the smallest permitted check that would resolve it and why it matters. Comparable means equally interrogated, not equally evidenced.

## Stop Before Judgment

Do not apply filters or eliminate an option without the user's confirmation; declare dominance; resolve value trades; score, rank, lean, or recommend; develop the chosen option into an approved design; or claim the option space, evidence base, or comparison is complete.

If the outcome is too muddy to derive live questions, say that outcome clarification is needed. If the field needs widening, say that additional options are needed. If the user now wants a choice, say that a recommendation comparison is the next distinct step. If an appropriate neighboring skill is available in the active environment, name it; otherwise explain the narrower next step in plain language and wait for the user rather than silently switching workflows.

## Done and Close

The field is developed enough when every option is more than a slogan, every live question has an honest answer state for every option, and no visible decision-controlling question remains unasked. This makes the comparison surface usable; it does not make the options fully designed, validated, equally certain, or exhaustive.

Prefer the smallest surface that makes the live distinctions inspectable. Use adaptive prose or a compact side-by-side; when several questions are in play, organize around the questions or use a table rather than emitting one polished card per option. Preserve the supplied field order unless a clearly non-evaluative organization improves readability.

Close with what can now be compared, the remaining assumptions or evidence gaps, source pointers for any claims affecting decisions, owners, numbers, or deadlines, and the fact that no ranking was performed.
