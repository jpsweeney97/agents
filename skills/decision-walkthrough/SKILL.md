---
name: decision-walkthrough
description: "Use when the user wants to work through an existing answer sheet or finite question list together, one question at a time, recording each clear answer in the named sheet. Do not use to invent questions, shape an open-ended goal, pressure-test a plan, prepare questions for another person, or apply answers to downstream source material."
---

# Decision Walkthrough

Walk through an existing question set with the user and record only what they decide. Keep the conversation small enough that they never have to reconstruct the whole sheet to answer the next question.

## Starting point

- Identify the current question list, its existing answers, and the named writable answer sheet. Use the user's requested question ID or the first unanswered item. Verify live files before trusting a handoff or recap. If a list was pasted but no answer sheet is named, ask where answers should be recorded before starting a recording walkthrough; do not invent a destination.
- Read the question's exact wording and enough of its cited source to give concise, relevant context. Do not create new questions or turn the source into an unapproved answer. If a question belongs to another decision owner, say so rather than asking the user to decide it by guesswork.
- State the answer-sheet path and the starting question once, so the user can correct a mistaken target. Only the named answer sheet is writable in this workflow; transcripts, raw sources, cards, glossaries, work lists, and other downstream artifacts remain unchanged.

## One question at a time

Present one question per reply: its ID, exact wording, brief context, and the existing options when useful. Show a source-supported interpretation as a candidate only, with its evidence and uncertainty; never write it as the user's answer without confirmation. Make “I don't know,” “leave,” or “unresolved” available without treating them as failure.

After the user replies:

1. Match the reply to the current question and preserve its exact scope. A clear answer authorizes updating that entry without another approval prompt. If the reply could refer to two questions, people, occurrences, or choices, ask one clarification about the same question before writing or advancing.
2. Record a clear uncertainty or leave instruction as such. Do not infer a correction, normalize an unresolved marker, or turn “still needed” into a confirmed commitment. Do not re-ask a recorded unresolved item without new evidence or the user's request.
3. Edit only the answer for that question, using its ID and nearby wording to locate the correct entry. Preserve the sheet's existing structure and other answers. Reread the edited entry and inspect the diff for unintended changes; follow the repository's applicable commit rules. If saving or required verification fails, stop and report the unsaved answer instead of moving on.
4. Briefly acknowledge what was recorded, then present the next unanswered question in the same reply. If the user pauses, give the last saved ID and the next ID instead. At the end, report the saved sheet, unresolved answers, and any commit state from fresh inspection.

## Boundaries

The sheet records decisions and clarifications; it does not execute them. Applying answers to transcripts, work lists, cards, glossaries, or other files is a separate task. `outcome-shaping` owns unclear goals, `grill-me` owns pressure-testing an existing plan, and `to-questionnaire` prepares a question document for someone else. Do not replace this one-question recording rhythm with any of those workflows.
