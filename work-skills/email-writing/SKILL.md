---
name: email-writing
description: "Use when drafting or revising professional email text for outreach, scheduling, follow-ups, replies, or similar work correspondence. Applies only to the draft wording, subject line, and brief style note; do not use for mailbox management, sending, publishing, resumes, cover letters, application answers, interview preparation, or non-email long-form prose."
---

# Email Writing

Draft professional emails that are warm but plain: clear without stiffness, and human without padding.

This skill owns draft text only. It never sends an email, opens a mail connector, accesses or changes mailbox state, archives threads, applies labels, or performs another external action. A request to draft is not authorization for any of those actions.

## Workspace Boundary

Before handling work content, read the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy. If classification, permitted handling, or authority is unclear, take the more protective route and ask for clarification rather than inferring permission. Keep the response in chat unless the user separately requests a permitted durable artifact. If a permitted durable draft is written, leave the work-content change unstaged, uncommitted, unstashed, and unpushed until Git retention is approved.

## Before Drafting

Ask one or two focused questions when a missing detail would materially change the email: the recipient relationship, purpose, concrete ask, date or deadline, or a sensitive context affecting directness. When only minor details are absent, use clear placeholders and note the assumption after the draft.

## Draft Shape

Default to one complete draft, not a menu of full variants. Include:

1. A plain subject line.
2. The body in a fenced Markdown code block for copying.
3. A brief note outside the draft naming the main style choice or one or two useful alternate phrasings.

Keep the subject and note outside the code block. The fence is chat presentation, not mail-tool input. Use the sender's actual name in the sign-off; default to `Best, [Name]` when none is supplied.

## Subject And Body

Use a practical, plain subject line such as `Following up on [topic]`, `Scheduling [meeting]`, `Quick question about [topic]`, `Checking in on [topic]`, or `Meeting details for [date/topic]`. Avoid subjects that oversell, conceal the purpose, or carry needless emotion.

Open with a short relationship or context note, then give the practical detail or request. Do not strip a routine email to the bare minimum unless the user asks for a very short draft.

## Tone

Aim for warm but plain. Natural phrases such as `I hope you're doing well`, `just wanted to`, a specific thank-you, an occasional exclamation point, or `excited` can work when they fit the real exchange. Avoid formality for its own sake, stacked praise, repeated gratitude, generic compliments, placating warmth, or filler.

Match the sender's actual energy. Use warmth that responds to something real in the thread or situation, not decorative friendliness. Do not turn a simple social acknowledgment into status reporting, scheduling logic, or an offer that the message does not need. Check implied referents so smooth phrasing does not misstate who did what.

For a first-time ask, prefer a conversational request such as `If you're open to it, I'd be glad to...` or `Would it be possible to...`. For follow-ups, be clear without becoming transactional. State a real deadline plainly; do not bury it in apology or vague pressure.

## Calibration

Prefer `Tuesday at 2 works well for me. Thanks for coordinating.` over a ceremonious confirmation. Prefer `Thanks again for making the time. I'm looking forward to talking.` over repeated generic gratitude. A useful routine follow-up is `Just wanted to follow up here. Happy to send anything else that would be useful.`

## Done When

The user has a copyable draft that makes the purpose and ask clear, sounds natural for the relationship, and remains only a draft in chat. If a later request asks to send, open a connector, or change mailbox state, treat it as a separate action requiring separate authority.
