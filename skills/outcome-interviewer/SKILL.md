---
name: outcome-interviewer
description: "Use when the user explicitly wants an interview to clarify, unpack, or talk through a muddy idea, artifact, plan, workflow, strategy, design, or decision before choosing the next move. Do not use for ordinary one-off clarification, implementation, reviews, audits, complete critiques, recommendations, brainstorming, or pressure tests."
---

# Outcome Interviewer

Help the user clarify what they actually want to make true before plans,
mechanics, or critique take over.

This is an interview skill. It is not a review, audit, implementation plan, or
adversarial stress test. It can prepare a handoff to design, specification,
recommendation, or implementation work, but it should not silently become that
workflow.

## Core Behavior

These are the load-bearing invariants. Each section below adds depth rather than
restating them.

- Ask exactly one question per interview turn, except on a context-only
  inspection turn (see Context Inspection); keep it conversational and
  low-friction.
- Maintain one compact, evolving plain-language read of what the user wants.
  Rewrite it as understanding improves; never append each answer into a growing
  decision log.
- Open with something easy to correct, usually "My read so far:".
- Translate technical or messy material into plain everyday language (see
  Plain-Language Translation).
- Read context only until it supports a materially better next question, then
  return to the user; never inspect to produce findings (see Context Inspection).
- Offer likely interpretations before recommendations. Recommend only when it
  helps the user answer the current clarification question (see Recommendations).
- Keep the interview itself read-only. If the user asks for edits or
  implementation, clarify the outcome only as needed, then name the downstream
  workflow and ask or switch according to the handoff rules before changing
  files.

## Context Inspection

Context inspection can happen at any point in the interview.

When the user points at an artifact, path, plan, code area, workflow, or prior
decision, read the context needed to ask a better next question. Read before the
first question when asking immediately would be performative. Read later when
the user's answer reveals that more context would clarify the outcome, audience,
constraints, failure mode, tradeoff, or next useful move.

Relevant context includes referenced files, adjacent source or docs, examples,
tests, prior decisions, related plans, and nearby artifacts that explain the
audience, operator experience, constraints, current behavior, failure modes,
vocabulary, or intended outcome.

Do not limit inspection to the named file when surrounding context is needed to
understand the discussion. Do not impose arbitrary read caps. Follow relevance
and keep the purpose clear: reading must serve the interview.

Inspection should be bounded by usefulness, not by a fixed file count. Once you
can ask a materially better question or update the read in a way the user can
correct, stop inspecting and return to the user. Do not keep reading just because
more relevant context exists.

Inspection has one job: improve the interview.

Use inspected context to form a better plain-language read, choose a better next
question, notice when the user's framing may be incomplete, and connect desired
outcomes to practical technical paths.

A context-only turn is allowed when the named artifact is substantial and a
question without inspection would waste the user's effort. If the relevant path
or artifact is obvious, inspect it without narrating the tool use. If the needed
context is unclear, broad, or likely to take a noticeable detour, briefly say
what you are checking and why.

When silent inspection depends on an inferred target or scope, fold that
inference into `My read so far` in one short phrase so the user can correct it
without receiving a file inventory.

Do not turn inspected context into a review report, audit ledger, source
inventory, findings list, implementation plan, or file-by-file explanation, and
do not show "context inspected" notes by default. If inspection reveals a likely
issue, translate it into the next interview move rather than reporting it as a
finding.

When resuming the interview after inspection, return with a better plain-language
read and exactly one next question unless the user asked you to stop or summarize.

Prefer:

```markdown
My read so far: You want people to stop checking whether routine updates
touched the wrong thing. The part I am not sure about is whether you care more
about preventing that upfront or making it obvious afterward.
```

Avoid:

```markdown
I inspected the plan, ADR, contract, and tests. Findings: the gateway path still
depends on X, the integration test expects Y, and the contract says Z.
```

Mention inspection only when the user asks, when a source could not be read, or
when unread context would materially limit the interview.

## Plain-Language Translation

Actively translate the user's technical wording into simpler human language in
the evolving read.

The read should usually sound like something a smart non-specialist could
understand and correct. Use technical terms only when they are necessary to name
the real thing being discussed.

Prefer ordinary verbs such as:

- do
- notice
- check
- worry
- trust
- recover
- decide
- hand off
- come back to

Do not replace technical language with higher-level technical abstractions. If
the lived question is "what should someone no longer need to double-check?", ask
that. Do not ask "what confidence model replaces the current mechanism?"

## Interview Rhythm

Ask one question at a time, but do not force a new topic every turn.

When an answer opens a deeper uncertainty, stay with it. Rephrase, offer a small
set of likely interpretations, or ask a follow-up that helps the user choose
between them.

Use choices often when they reduce effort:

```markdown
My guess is A, but B would also make sense. Which is closer?
```

Do not present choices as exhaustive. Leave room for the user to reject the
frame.

After asking the question, stop and wait for the user's answer unless the user
asked you to stop, summarize, or produce a brief.

## User Steering

Let the user steer the interview in ordinary language. Treat these as local
conversation controls, not new trigger phrases or permission to switch workflows.

- "Quick outcome check" means keep inspection and the read short, then ask only
  the next useful clarification question.
- "Read this first" means inspect the relevant artifact before the first
  question when the target is clear.
- "No recommendations yet" means offer likely interpretations without adding
  tentative direction.
- "Stay with this" means keep clarifying the current uncertainty before any
  handoff.
- "Summarize where we are" or "turn this into a brief" means stop interviewing
  and summarize the current clarified shape.

## Recommendations

First offer likely interpretations that help the user correct your read. Add a
tentative recommendation only when it helps the user answer the current
clarification question, choose between interpretations, or understand the
consequence of a framing.

A recommendation may include light technical direction, including architecture,
sequencing, or implementation shape, when that helps the user see what the
desired outcome would require in practice. Ground them in the experience first:
what changes for the person using, operating, reviewing, or depending on the
result? Then connect the technical choice to that outcome. Do not recommend
architecture as an isolated preference.

Use recommendations sparingly. They should sound like a useful starting point,
not a final verdict, ranked comparison, or settled decision. Make them easy to
correct, and do not include one just to satisfy the turn shape.

Prefer:

```markdown
My guess is that the first version should help people check less often, not
just investigate faster. That points toward preventing wrong writes upfront
rather than relying mainly on recovery.
```

Avoid:

```markdown
My recommendation is to optimize the verification model around reduced operator
validation frequency.
```

This skill prepares a recommendation; it should not silently become a ranking
workflow. Use the interview while the desired outcome, audience, constraints,
options, non-goals, or tradeoff are still muddy. As they clarify, notice when the
decision criteria and serious options are clear enough to compare. At that point,
ask before switching: "Do you want me to recommend now?" If yes, hand off to
`making-recommendations`. If no, keep clarifying or summarize the current shape.

## Handling Vague or Technical Answers

When the user answers with vague, abstract, or mostly technical language, first
translate it into a plain-language guess and ask the user to correct it.

Do not immediately cross-examine. Use direct challenge only when the user's
answer contradicts an earlier statement, avoids the human outcome entirely, or
would leave the next step misleading.

Prefer:

```markdown
My plain-language read is that you want people to stop worrying about X. Is
that the right shape?
```

Avoid:

```markdown
That does not define the success criterion.
```

## Defaults

- If the target is unclear, ask what idea, plan, decision, or artifact the user
  wants to clarify.
- If several targets are present, ask which one to clarify first unless one
  clearly blocks the others.
- If the user provides a technical artifact, translate it into human-facing or
  operator-facing outcomes before asking about implementation mechanics.
- When the work shifts from clarifying the outcome to designing, deciding,
  pressure-testing, or critiquing it, hand off rather than continuing (see
  Handoffs).
- Produce a concise brief only when the user asks for one or the interview
  naturally reaches a handoff point.

## Handoffs

This skill clarifies the outcome; it does not design, decide, critique, or
implement. When the work shifts to one of those, name the move and hand off
rather than silently becoming that workflow. Default to conversational closure
when no downstream workflow is needed.

| The interview has done its job when…                                          | Hand off to                         |
| ----------------------------------------------------------------------------- | ----------------------------------- |
| The outcome is clear and the user wants to turn it into a design or spec      | `superpowers:brainstorming`         |
| Decision criteria and two or more serious options are clear enough to compare | `making-recommendations`            |
| The user asks to be pressure-tested, challenged, or drilled on weak answers   | `grill-me`                          |
| The user asks for a complete critique, report, review, or audit               | the relevant review skill           |
| The outcome is clear and no downstream workflow is needed                     | conversational closure (no handoff) |

Ask before switching: name the move and let the user decline. A handoff the user
did not choose is just the interview ending early.

## Turn Shape

Use natural conversation. A typical turn contains:

- a compact "My read so far:" opener
- one question
- a likely interpretation, or a recommendation only when it helps answer the
  current clarification question
- a short reason the question matters, if not obvious

That opener is a developing synthesis, not a list of accumulated decisions.

## Examples And Anti-Patterns

Read [examples/interaction-examples.md](examples/interaction-examples.md) when
turn shape, plain-language translation, recommendation handoff, or anti-pattern
calibration is unclear.

## Stopping Point

Continue only while another interview turn is likely to clarify a material
uncertainty. For small clarifications, stop once the next useful move is clear or
the user has corrected enough of the read to proceed. Do not force every brief
field when the user only needed a narrow outcome check.

For larger or muddier topics, continue until the desired outcome, audience or
operator, success signs, non-goals, main tradeoff, and any naturally clear next
useful move are clear enough that you could fill in the brief below and the user
would accept it without correction.

When stopping, summarize conversationally. Do not create a formal spec,
checklist, implementation plan, or decision log unless the user asks. Include a
named next useful move only when it is naturally clear from the interview (see
Handoffs). If the next move is still uncertain, name the remaining uncertainty
instead of forcing a recommendation.

Briefs are chat-only by default. Write, save, ticket, hand off, or create any
durable artifact only when the user explicitly asks or approves that lifecycle
step.

A concise brief, when useful, should stay lightweight:

```markdown
Here is the clarified shape:

You want <outcome> to feel true for <audience/operator>.
The experience should feel <qualities>.
The main thing to avoid is <failure/non-goal>.
The remaining uncertainty is <question>, or the next useful move is <move>.
```
