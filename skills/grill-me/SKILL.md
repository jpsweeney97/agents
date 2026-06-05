---
name: grill-me
description: Use when the user explicitly asks to be grilled, stress-tested interactively, or challenged one question at a time about a plan, design, architecture, strategy, or decision. This is an interactive drill mode where each turn asks one high-leverage question and includes the agent's recommended direction. Do not trigger for incidental mentions of "grill me", meta-discussion of this skill, neutral "interview me", "talk this through", "help me clarify", or "figure out what I want" requests, or requests for a complete critique/report unless the user explicitly wants an interactive grilling session. Route neutral clarification interviews to outcome-interviewer unless the user also asks to be challenged or stress-tested.
---

# Grill Me

Stress-test the user's plan or design until the important decisions, assumptions,
risks, and dependencies are clear.

## Core Behavior

- Ask exactly one question at a time.
- Include your recommended answer or recommended direction with each question.
- After asking the question and giving your leaning, stop and wait for the user's answer unless the user asked you to stop or summarize.
- Frame the leaning as tentative when user goals, values, or constraints are missing.
- Prefer the highest-leverage unresolved issue over a fixed checklist order.
- Challenge weak, vague, or inconsistent answers before moving to a new topic.
- Across turns, track resolved decisions, unresolved assumptions, and the current blocker.
- Lead with the user-visible decision, behavior, or outcome the answer will
  settle, then connect it to technical choices.
- When the user names a file, plan, doc, PR, or code area, read the named target
  and the obvious adjacent authority needed to avoid a fake high-leverage
  question before asking the first drill question. If inspection would become
  broad or unavailable, state the boundary and ask the best grounded question.
- Otherwise inspect only enough to avoid asking for information already
  available.
- Artifact and codebase inspection is read-only unless the user explicitly asks for edits.

## Conversation Style

- Treat the drill as requirements alignment, not a formal audit. When the
  desired outcome is unclear, make the user clarify what they want to be true
  before framing how to build, verify, or trade off that choice.
- Match the user's register. Use technical terms when the user is being
  technical, and use plain direct language when they are not.
- Prefer concrete questions and examples over abstract categories. For example,
  ask what breaks for users if the plan fails before asking for a risk taxonomy.
- Keep the active drill conversational and compact. Save formal structure for
  stop summaries or requested artifacts.

## Defaults

- If the target is unclear, ask one clarifying question about what plan, design, decision, or strategy to drill.
- If several targets are present, ask which target to drill first unless one target clearly blocks the others; if choosing, explain that choice in one sentence.
- If the user asks for a complete critique, report, or review, prefer the relevant review skill unless they explicitly asked for an interactive grilling session.
- If the user asks to stop, summarize the resolved decisions, remaining risks, and recommended next step.

## How to Choose the Next Question

Choose the next question based on what would most improve or threaten the plan:

- an unstated goal or non-goal
- a hidden dependency
- an architectural or sequencing choice
- a failure mode
- a tradeoff the user appears to be avoiding
- an assumption contradicted by evidence
- a missing verification or rollout path

Do not mechanically exhaust this list. Use it to guide judgment.

## Turn Shape

Use natural conversation, but make each turn contain:

- the decision, behavior, or user-visible outcome being tested when it is useful
- the question
- why it matters, when not obvious
- your recommended answer or leaning

Keep the format compact. Use explicit labels only when they improve clarity.
Do not turn each drill turn into a report.

Illustrative shape, not a template:

```markdown
Decision to settle: Whether rollback must protect customer-facing availability
or only preserve data integrity.

Question: If the migration fails under load, what must users still be able to do?

Why it matters: This decides whether rollback rehearsal is a release gate or a
cleanup task.

My leaning: Treat customer-visible recovery as the bar unless you have a clear
non-user-facing failure mode.
```

## Stopping Point

Continue until the main decision path is chosen, the blocking assumption is named, the remaining risk is explicitly deferred, or the user stops the drill. When stopping, summarize the resolved decisions, remaining risks, and recommended next step.
