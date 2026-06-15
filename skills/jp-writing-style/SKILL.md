---
name: jp-writing-style
description: "Use when writing or rewriting first-person self-presentation prose in JP's voice — writing where JP narrates his own experience or makes his own case: personal and reflective essays, personal statements, cover letters, autobiographical narratives, and application or interview responses. Do not use for workplace or third-party writing (memos, recommendation letters for others, professional or analytical narratives, case write-ups), general explanatory prose, casual, humor-first, or marketing copy, minimalist technical instructions, obligation-only edits to agent-instruction docs (use writing-principles), or prose that would require inventing facts the user has not supplied."
---

# JP Writing Style

Write prose in JP's voice — formal, reflective, analytical, earnest, and
causality-driven — grounded in his actual writing, not a generic "sound formal"
register. The voice is reverse-engineered from real samples in
`references/corpus.md`; that corpus, not this file's adjectives, is the ground
truth. The content of the user's request always outranks stylistic imitation:
shape wording, structure, tone, and rhetorical movement, never the facts.

## Integrity gate — read first

This is the one hard rule. The skill's named use cases (personal statements,
cover letters, application responses) are high-stakes: an invented detail
there is fraud.

Every fact, credential, experience, emotion, outcome, and causal claim in the
output must come from the user's source material or be confirmable with them. If
a beat the structure wants — a cause, a lesson, a feeling, a forward resolution —
has no basis in what the user gave you, **do not write it.** Leave the gap, mark
it, and ask. Fidelity to the user's real facts always outranks completing the
arc.

JP's strongest pieces are built on specific, true detail: named stakeholders and
a quantified cost in the case analysis, the actual diagnosis timeline in the
personal statement. The arc reads as honest because the facts are real.

## How to work

1. **Read the corpus.** Open `references/corpus.md` and pattern-match against the
   real sentences before writing anything.
2. **Gather the real material.** If the prompt is thin, ask for the concrete
   facts the piece needs — what happened, who was involved, the real stakes,
   feelings, and outcome — rather than inventing them to fill the arc. Elicit,
   then write.
3. **Draft in the voice,** using the moves, diction, and genre guidance in
   `references/patterns.md`.
4. **Run the quality check** below, starting with integrity.

## When to use

Use this skill for first-person self-presentation in JP's voice — writing where
JP narrates his own experience or makes his own case: personal and reflective
essays, personal statements, cover letters, autobiographical narratives, and
application or interview responses, anywhere tone, structure, and rhetorical
movement matter.

Do not use it for workplace or third-party writing — memos, recommendation
letters for someone else, professional or analytical narratives, case write-ups,
or general explanatory prose — even when those would read better in a formal
register; this voice is tuned for self-presentation, not neutral exposition. The
analytical case write-up in the corpus stays as voice grounding (its moves
transfer to self-presentation), but the skill no longer writes that genre. Also
skip it for casual texting, humor-first writing, punchy marketing copy,
minimalist technical instructions, or legal/medical/financial advice where
neutrality outweighs voice. For obligation-only edits to agent-instruction docs
(AGENTS.md, CLAUDE.md, SKILL.md), use `writing-principles`. For code comments or
docs that need direct technical clarity, keep the explanatory reasoning but drop
the ornament.

## The voice

Formal, reflective, analytical, earnest, and academically inflected; controlled
even when sincere. Confident but not arrogant, personal but not confessional,
serious without melodrama. The prose feels deliberate, not spontaneous: it
prefers developed reasoning over terse summary, and explains not just what
happened but why it happened, why it mattered, and what follows.

One signature move grounds the voice and keeps it human: a short, blunt fragment
dropped after a formal sentence, carrying real feeling — "Literally.",
"Basically, I feel stuff really hard.", "I felt like myself again." Rare and
intentional; overuse kills it.

## The default movement (vary it)

Most of JP's reflective pieces move through:

1. Establish the premise.
2. Define the terms or standard that matter.
3. Diagnose the root cause or core tension.
4. Trace the consequences, with concrete specifics.
5. Reassess with greater clarity.
6. Resolve toward a lesson, correction, or forward action.

This is JP's habit, not a mold. Vary the order, merge beats, or skip them when
the material calls for it. If a piece could be swapped beat-for-beat with another
on a different topic, it has lost the voice — distinctiveness comes from the
real specifics, not the template. And never manufacture a beat the facts don't
support; the integrity gate governs every step.

`references/patterns.md` holds the catalog of moves (open / define / diagnose /
trace / qualify / reassess / correct / resolve), each anchored to a real corpus
line, plus the diction, transitions, and per-genre adaptation. Load it while
drafting.

## Drafting principles

- **Paragraphs do interpretive work.** Each is a mini-argument — claim or
  transition, explanation, concrete evidence or context, then implication. Don't
  list facts; interpret them. Prefer developed paragraphs over many short ones
  unless a concise or web-native format is asked for.
- **Sentences layer reasoning.** Mostly medium-to-long, with clauses that
  qualify, contrast, or extend — moving from observation to implication. Use the
  occasional emphatic fragment sparingly.
- **Diction is elevated but his.** Reach for JP's real vocabulary (see the
  corpus and pattern bank) inside his constructions, not sprinkled to inflate.
  Don't force an elevated word the corpus never uses; simpler formal language
  that's clearer wins.
- **Emotion is interpreted.** Sincere, controlled, never raw, sarcastic, or
  melodramatic. State the feeling, then make sense of it.
- **First person is accountable, not defensive.** Reflective, self-aware,
  improvement-oriented. Explain circumstances without making excuses; connect a
  setback to insight and what follows — only where the facts support it.
- **Contractions are fine** when they read naturally ("I don't mean to say…")
  without making the voice casual.
- **Default to a formal register,** but when the output is a chat reply rather
  than a saved artifact, follow any higher-priority instruction to match the
  user's register and lead with the plain answer; apply the full formal voice to
  the prose deliverable itself.

## Rewriting existing text

Preserve every factual claim unless asked to change content. Replace casual
phrasing with polished, reflective language; make existing causal links
explicit; define vague terms that are central; strengthen the conclusion toward
action or insight. Do **not** add unsupported experiences, emotions, credentials,
or causal connections — turning a bare list of events into "cause, consequence,
and insight" must use only causation the source actually supports; where it
doesn't, keep the events as sequence and ask for the connecting reasoning.
Imitate the voice, not the source's typos or errors.

## What to avoid

Chatty, breezy, comedic, minimalist, or internet-native styles. Specifically:
excessive bullets, overly short paragraphs, jokes, sarcasm, slang, hype, buzzword
overload, generic motivational clichés, vague emotional claims without
interpretation, dramatic confession without analysis, abrupt or unearned
conclusions, and needless complexity that reduces clarity. Above all, invented
facts, feelings, biographical details, or causal links — see the integrity gate.

## Quality check

Before finalizing, verify:

1. **Integrity (first, blocking):** every fact, credential, cause, emotion, and
   outcome traces to the user's material; nothing was invented to complete the
   arc. If anything fails this, stop and ask.
2. The opening states a clear premise, thesis, or direction.
3. Terms or standards that carry weight are defined.
4. The reasoning shows a visible cause-and-effect chain built on concrete
   specifics, not abstraction.
5. The tone is formal, reflective, earnest, and controlled; any emotion is
   interpreted, not raw.
6. Diction is elevated but readable, and elevated words sit in JP's
   constructions rather than being sprinkled.
7. The structure varies from the default arc, no opening or closing stem is
   reused verbatim, and the piece could not be swapped beat-for-beat with a
   generic earnest essay on another topic.
8. Each paragraph performs interpretive work.
9. The conclusion resolves toward a lesson, correction, or forward action — only
   where the facts support one.
