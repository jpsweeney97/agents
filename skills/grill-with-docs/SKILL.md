---
name: grill-with-docs
description: "Use when the user wants to stress-test a plan or design against a project's existing domain language, code reality, CONTEXT.md, or ADRs, with terminology/doc updates as decisions crystallize. Do not use for ordinary grilling without repo docs, outcome clarification, complete review/audit reports, or implementation planning."
---

<what-to-do>

If no plan, design, or decision is already in context, first ask what I want to be grilled on — and orient on any existing `CONTEXT.md`/`CONTEXT-MAP.md` and `docs/adr/` for the area — before starting.

If I invoke this skill after the decisions are already made, with nothing left to interrogate, say so — capture is not grilling. Record only terms I confirm in this conversation, and route standalone decision capture to `decision-record`, which owns it.

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer, always in a fenced Markdown code block in chat for easy copying.

Ask the questions one at a time, waiting for feedback on each question before continuing.

A run of answers accepted verbatim is information, not success: the grilling has stopped grilling and become drafting with my consent. Say so plainly, then either ask the question whose recommended answer you are least sure of, or offer to stop.

If a question can be answered by exploring the codebase, explore the codebase instead.

Stop when I say the plan feels solid or ask to stop, or when further questions stop changing the plan. On stopping, give a short conversational summary of the decisions we reached and the single weakest remaining assumption, scan those decisions for any that cleared the ADR gate without being offered a record, and report which `CONTEXT.md`/ADR files you created or edited. If a clear next move follows, name it — for example, handing off to `implementation-planning` to turn the hardened plan into tasks. If I pivot or interrupt mid-grilling, still report in one line which files you wrote and the question left open.

</what-to-do>

<supporting-info>

## Domain awareness

During codebase exploration, also look for existing documentation:

### File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

The same check binds your own recommended answers: before recommending a closed set or a claim about what the code currently does, read the file that could contradict it. A decision settled by assent that the code already contradicted is this skill's worst product.

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

### Writing to the repo

`CONTEXT.md` and `docs/adr/*` are durable repo files. Before the first write, run `git status`; if the worktree is dirty, tell the user your writes will land alongside their uncommitted changes, and never write over unrelated edits in a file you touch. Update incrementally as decisions crystallize, but do not commit — leave the changes for the user to review. If a governing instruction or the user directs commits mid-session, stage `CONTEXT.md`/ADR changes in their own commits — never folded into unrelated work — and name the skipped review checkpoint when you close. When you pause or finish, report which files you created or edited. These files record this session's assents, not decisions that have survived use; the user's review before commit is the ratification step, so if commits already happened, say the records landed unreviewed. Proof boundary: you recorded glossary and decision text, not verified implementation.

Note: `CONTEXT-FORMAT.md` is also consumed by `improve-codebase-architecture`. `ADR-FORMAT.md` here is a git-tracked symlink to the canonical file at `plugins/decide/references/ADR-FORMAT.md`, owned by the `decide` plugin, consumed there by `decision-record` and through this alias by `improve-codebase-architecture`; an edit made through the alias lands in the canonical and is a `decide` release. If this skill is renamed, moved, packaged, or archived, the alias cannot travel with it: decide the canonical-plus-copy topology then (a byte-identical copy with a drift check is the precedent, `scripts/check-protected-set.sh`) and update every consumer's reference.

</supporting-info>
