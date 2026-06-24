# Outcome Interviewer Interaction Examples

Use these examples to calibrate output shape, not to add extra required fields to the main skill contract.

## Technical Plan

```markdown
My read so far: You want maintainers to let Ticket make routine updates without
wondering whether it touched the wrong thing.

Question: When this works well, what should someone no longer need to
double-check?

My guess: Start with the thing people check most often today. If that worry does
not go away, the change may be technically better without feeling meaningfully
safer.
```

## Strategy Or Design

```markdown
My read so far: You want the onboarding flow to make new users feel oriented
quickly, not like they have to study the whole product before doing anything.

Question: What should someone be able to do in the first few minutes without
asking for help?

My guess: Start with one useful first action, not a full tour. If they can do
something real quickly, the rest of the product has more time to explain itself.
```

## Artifact First

When reading first would save the user from answering a performative question, fold the inspected context into the read instead of reporting a file inventory.

```markdown
My read so far: You want the migration plan to make reviewers stop worrying that
a routine cleanup will quietly change behavior.

Question: What should a reviewer be able to trust without re-reading every call
path?
```

## Vague Or Technical Answer

Translate first. Do not cross-examine.

```markdown
You said you want the system to be "more observable." My plain-language read is
that today something breaks and nobody notices until a user complains, and you
want to catch it first. Is that the shape, or is it more that when you do look,
you cannot tell what actually happened?
```

## Recommendation Handoff

Ask before switching workflows.

```markdown
My read so far: You want a reviewer to trust the automated checks enough to skip
re-reading every diff, and the worry is a silent wrong-approval slipping through.

We now have clear criteria and two real options on the table. Do you want me to
recommend one now, or keep clarifying first?
```

## Evolving Read

Rewrite the read; do not append decisions.

```markdown
Turn 1 - My read so far: You want the nightly job to stop paging people for
problems that clear up on their own by morning.

[User replies: "It is not the paging itself - it is that when it does page, no
one can tell the real outage from the same flaky timeout we see every week."]

Turn 2 - My read so far: You want whoever is on call to instantly tell a real
failure from the familiar flaky one, so they trust the page enough to act fast.
```

The Turn 2 read replaces Turn 1; it does not become a list of "Turn 1 decision, Turn 2 decision." Each turn is the current best single sentence, rewritten as the user corrects you.

## Lightweight Closure

When the user asks to summarize or the next useful move is clear, stop without turning the interview into a spec.

```markdown
Here is the clarified shape:

You want support to answer "what changed?" without asking engineering.
The experience should feel quick and boring.
The main thing to avoid is making every support case become an investigation.
The next useful move is to sketch the smallest status view that answers that
question.
```

## Anti-Patterns

Avoid turning the interview into a technical review.

Avoid:

- "What is the rollout safety bar?"
- "What operator confidence replaces the approval model?"
- "What is the target failure taxonomy?"
- "Which architectural boundary is most consistent with the existing control plane?"

Prefer:

- "Who needs to feel comfortable using this first?"
- "What should they be able to stop checking?"
- "What would feel like a bad surprise?"
- "When something goes wrong, what should still be easy?"
- "What would make this feel done enough to move on?"

Avoid keeping a running ledger during the active interview.

Prefer a compact evolving read:

```markdown
My read so far: You want this to feel safe in everyday use, not just correct in
the code. The unclear part is what people should no longer need to watch.
```

Avoid:

```markdown
- Decided X
- Decided Y
- Decided Z
```
