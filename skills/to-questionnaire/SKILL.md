---
name: to-questionnaire
description: "Use when a knowledge gap only one named person can close should become a Markdown questionnaire that person fills in — async, or walked through together — invoked as /to-questionnaire or $to-questionnaire. Do not use to route a decision to its accountable owner (`decision-owner-map` — its recipient decides; this one's recipient supplies knowledge), for a reply that returns as claims to adjudicate against local evidence (`courier`), to commission work another session executes (`stage-prompt`), or to interview the user themselves (`outcome-shaping`, `grill-me`)."
disable-model-invocation: true
---

# To Questionnaire

Turn a knowledge gap only one named person can close into a Markdown document that person fills in — async, or walked through together. The recipient holds knowledge the user lacks; the questionnaire pulls it out of them, and the user still decides what to do with it.

## Boundaries

- The recipient supplies knowledge; they do not decide. When the point is routing a decision to its accountable owner, that is `decision-owner-map`. When its packet names missing information held by one person you can ask, this skill composes the ask.
- The return leg is authority, not allegation. A filled-in questionnaire from the domain expert *is* the knowledge the user lacked; do not route it through `courier`, whose inbound contract treats a reply as claims to confirm or refute against local evidence — inverted here, since there is no local evidence to check the expert against. Use `courier` when the reply will come back as claims to adjudicate; use this skill when it comes back as knowledge to absorb.
- A commission another session or agent executes is `stage-prompt`. Interviewing the user about their own want or plan is `outcome-shaping` or `grill-me`. The email wrapped around the send is `email-writing`'s job (where available); this skill owns the document inside it.

## Grill The Send, Not The Subject

Interview the user only about the send — the axis they can always answer. Interviewing them about the substance is asking for knowledge they told you they lack, and it harvests confabulation.

1. **Who is it going to?** In one exchange: the recipient's role, expertise, and relationship to the user. This fixes the document's tone and how much context it must carry. Done when you know what the recipient knows that the user doesn't.
2. **What do you need back?** In one exchange: the specific facts the user cannot resolve alone, or the things they must walk away able to do or decide. Done when you hold a concrete list.
3. **Write the questionnaire.** Draft questions aimed at the gap between steps 1 and 2, in the shape below. Done when every item from step 2 is covered by a question.

## The Document

Frame it as a discovery questionnaire — the user lacks context, the recipient holds it — and build it from these parts:

- **Purpose line:** why the questionnaire exists and what rides on the answers.
- **From / To / How your answers will be used:** one line each.
- **Context:** one paragraph orienting a recipient who was not in the user's head — enough to answer well, not a page.
- **How to answer:** the deadline, the rough effort expected, and explicit permission for partial answers and "I don't know" — flag uncertainty rather than skip the question. This block is what actually gets async questionnaires returned.
- **Themed `##` sections, most-important-first:** async usually gets one pass, so the questions that matter most go first.
- **One idea per question, never compound,** with a blank answer stub directly beneath, and a one-line *why this matters* only where a question could be misread or invite a throwaway answer.
- **A closing catch-all:** anything we didn't ask that we should know?

## Artifact And Lifecycle

- In a git repository, write to `docs/questionnaires/<recipient-or-topic-slug>-<YYYY-MM-DD>.md`, creating the directory if absent and deferring to a questionnaire home set in the project's `AGENTS.md` or `CLAUDE.md` when one exists. Outside a repository, use the destination the user names, or the working directory.
- Before writing, if the project is a git repository, run `git status`; if the path or its parent carries unrelated dirty state, surface that rather than write over it. Leave the artifact uncommitted for the user. Never commit on a protected or default branch.
- Close by reporting the path and the step-2 list each question traces to. The send itself — email, message, meeting — is the user's move.
