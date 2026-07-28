---
name: premortem
description: "Use when a committed or nearly committed plan, design, or decision needs prospective failure-imagination before execution: assume it failed, generate mechanism-distinct accidental past-tense causes, and turn each into a pre-mitigation and observable leading indicator. Returns an inline owned action ledger and no readiness verdict. Do not use for go/no-go decisions, intentional attacks, post-incident analysis, or widening options."
---

# Premortem

Stand in a future where the committed plan has already failed, then work backward to the accidental causes. This prospective-hindsight move exposes failure modes that commitment optimism can hide while there is still time to prevent, detect, or blunt them. Invocation: `/premortem` or `$premortem`.

The plan remains chosen. This skill does not re-decide it, adjudicate readiness, or deliver a go/no-go verdict. Its deliverable is a wide, mechanism-distinct field of mitigated accidental failure modes and an inline action ledger.

## Authority and safety

Before handling work content, read the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy. Those instructions control what may be read, discussed, retained, or written. If classification, permission, or a proposed destination is unclear, take the more protective route and stop for clarification.

Work in chat by default. Do not browse, access a connector, install anything, create or update tracker items, write a file, stage, commit, stash, push, publish, or make any other external change unless the user separately requests it and the active workspace permits it. Keep decision-relevant source claims traceable, and mark organizing inference `unverified`.

## The moves

1. **Pin the committed plan.** State the plan, design, or decision being premortemed and confirm it is settled enough to fail. If it is not chosen, stop: first clarify the outcome, widen options, choose among them, or shape the design. If the goal is too muddy to say what failure means, clarify it first.
2. **Assert failure as accomplished fact.** Pick a horizon that fits the plan and state the frame in past tense: "It is <horizon> later; this was carried out and failed." Do not soften this into generic risk language; the already-failed premise is the debiasing mechanism.
3. **Generate a wide field of accidental causes.** Work backward from the failure. Rotate the provocations that uncover distinct mechanisms: a load-bearing assumption proved false; a dependency drifted or underperformed; a handoff or interface broke; people were unavailable or misaligned; ownership was absent; incentives or context changed; authority or access arrived too late; or gradual erosion accumulated. Use the lenses that bite. This is the indifferent-universe lane, not an attacker model.
4. **De-cluster by mechanism.** Combine causes that would fire for the same underlying reason. When several causes depend on one hidden assumption or dependency, name that common mechanism rather than padding the field with cosmetic variants.
5. **Turn every surviving cause toward action.** For each mechanism, identify the pre-mitigation that could prevent or blunt it. Where a genuine early signal exists, name a dated, observable leading indicator and the action it should trigger. Do not invent an indicator just to complete a row. Tag the intervention as prevention, detection, or mitigation.

## Default inline owned action ledger

Return the actionable field inline in chat. Use an owner named by the user or source when available; otherwise state `Owner needed` rather than inventing accountability. Include a date or timing trigger only when known, and mark it `unassigned` when it needs a human decision.

```markdown
| Accidental failure cause | Pre-mitigation | Leading indicator and timing | Owner | Action type |
| --- | --- | --- | --- | --- |
| <past-tense, mechanism-distinct cause> | <prevention, detection, or mitigation> | <observable signal by date/timing, or no early signal> | <named owner or Owner needed> | <prevention / detection / mitigation> |
```

The table is the authoritative ledger for this run. Do not create tracker items, issue drafts, task lists in another system, or connector actions. If the user later explicitly asks to persist an item, first check the active workspace's instructions and permitted destination; do not infer permission from this premortem.

## Close — no verdict

Stop when another pass produces no mechanism-distinct cause. Close with one honest residual observation anchored to the plan's stated assumptions or fixed points: identify what the field may still leave untouched. Never claim all failure modes were found or present a matrix as complete or precise.

Do not conclude "go," "no-go," "ready," or "not ready." If the user wants a readiness decision or formal adversarial review, that is a separate, explicitly requested activity. If a requested follow-up needs unavailable or unapproved access, say it is unverified here and name the permitted evidence or responsible human needed to resolve it.

## When not to use

- The plan is not chosen yet; clarify, widen, select, or shape it first.
- The user wants a go/no-go or readiness verdict, or a formal adversarial stress test.
- The threat is a motivated adversary, not accidental failure.
- A real incident has already happened; analyze facts after the fact instead.
- The goal is too muddy to define failure.
