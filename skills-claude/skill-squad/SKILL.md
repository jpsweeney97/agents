---
name: skill-squad
description: "Use when you want to design a new skill (or materially redesign one) by orchestrating a multi-agent discovery run — fan out genuinely different approaches, beat them against a blind careful-default control, adversarially verify, and return a chosen design with an honest discovery-vs-control differential. Claude-only; expensive by design. Do not use for conversational or general design (design-exploration), judging whether proposed structure is justified (agent-facing-design), measuring an already-built skill (skill-benchmark), adversarial critique of an existing skill (scrutinize-skill), or hand-authoring the SKILL.md itself."
---

# Skill Squad

Design a skill by sending a squad of agents to *discover* one — not to confirm the design you already have. The value is discovery: surfacing an approach, or a flaw, you would not reach alone. Everything else here serves that, including the one hard rule that keeps a discovery honest — it has to beat a control that never saw it.

This skill runs an expensive, multi-agent **Workflow**, and is Claude-only. It stops at an approved *design* and hands off to hand-authoring; it does **not** write the `SKILL.md`.

## When To Reach For It

Reach for it when a skill is worth designing well and you suspect your first instinct is not the ceiling — a genuinely open design space, a skill you have rewritten before, or one where getting the shape wrong is costly. For a small or obvious skill, hand-author against `agent-facing-design` and skip the squad; the run is not worth its cost.

## Before You Spawn

Invoking this skill is not authorization to spawn the squad. A real run is many agents and can cost hundreds of thousands of tokens (a comparable design run was 14 agents; a library sweep, 62). So:

- State the intended scale and rough budget before launching.
- Scale the discovery fleet to the design's openness and the budget you have — more genuinely-different approaches for a wide-open skill, fewer for a narrow one. The control ensemble stays fixed (below).
- If multi-agent orchestration is not already authorized for this session, ask once before launching.

## The Run

Author a fresh Workflow for the design in front of you — do not reach for a fixed pipeline. Five moves; the order matters, the agent counts do not.

**1 — Set the bar, blind.** Before anything else, an independent arm writes the design a careful agent reaches *with no squad* — the control. Keep it blind: it sees only the design problem, never the squad's approaches. Run the control as an ensemble of 2–3, not one, so the bar is not a single lucky or unlucky draw; the bar to beat is the *strongest* control, not the average. This baseline is not empty — it is a careful agent plus this repo's doctrine; call it the "careful-default," never "no skill." (This is the same honesty `skill-benchmark` keeps about its baseline — borrow the principle, not its `claude -p` machinery, which needs a built skill this stage does not have.)

**2 — Spread genuinely-incompatible approaches.** Fan out generators, each seeded with a governing commitment the others would call *wrong* — not a restatement in new words. The forcing question for the spread: would the author of approach B say approach A is the wrong shape, or merely a variation of theirs? If they are variations, the spread failed — widen it.

**3 — Try to kill each survivor.** Hand the approaches to independent skeptics — delegate to `scrutinize-skill` for the adversarial read; do not hand-roll a critique. Two rules make it honest: an approach is never graded by its own author (kills the blind spot the authors cannot see), and the skeptic favors the simple-and-right over the elaborate-and-clever (kills the dazzle that lets the best-argued beat the best). A design advances only by surviving a real refutation, never a rubber-stamp.

**4 — Pick the strongest, then run the decisive comparison.** Pick the strongest single surviving approach. A *merge* is allowed only under the Hybrid rule below — never as a default compromise. The head-to-head is *relative*, not a kill: before it, the crown must already have survived a dedicated skeptic on the exact design you are crowning — and a synthesized hybrid has not (it was built after move 3), so it returns to move 3 first. Then put the winner head-to-head against the blind control, judged by an arm that saw neither side's authorship — and *blind means blind*: the finalist must reach the judge stripped of the squad's selection narration, kill list, and graft commentary, which are themselves an authorship tell. The product of this move is not "the design" — it is the margin: because the comparison is relative, say whether the winner beats the careful-default on a genuinely different *shape* or only by enriching a spine it already reached, and on which axes?

**5 — Report the margin, including the honest null.** Two outcomes, both wins:
- **Beat** — a design that genuinely beats the careful-default, with the margin and the axes it won on.
- **Marginal** — the careful-default holds. Say so plainly, and show the proof: the best thing the squad surfaced, and why it did not clear the bar. A run that honestly reports "your instinct was right, here is what survived trying to beat it" has done its job.

## Hybrids: One Spine, Not A Blend

The best design is often a hybrid — but only one kind is real, and the difference decides whether you crown it or kill it:

- **A blend of spines is mush.** Averaging philosophies and grafting everyone's good parts produces something more elaborate than any single approach — exactly the dazzle move 3 exists to kill. Reject it.
- **One spine plus justified grafts is a resolution.** One approach's philosophy wins and governs; rival elements are imported only as subordinated, individually-justified grafts. A real resolution often *subtracts* — it is simpler than the approaches it drew from, not a superset of them.

Three rules keep a hybrid honest:

1. It is a candidate, not a compromise — *before* the head-to-head it re-enters move 3 and faces the skeptics like any approach; the head-to-head is not that kill. Synthesis does not launder it past the kill step.
2. You must name its single spine in one sentence, and say why each graft is a deliberate import. If you cannot, it is mush.
3. It must beat the best *parent* it was built from, not only the control. A hybrid that beats the careful-default but ties or loses to the strongest single approach is needless elaboration — the parent wins, and the hybrid is reported as considered-and-rejected.

## What This Skill Will Not Do

The discovery and the margin are judgments the squad argues, not numbers it computes. This skill does not score approaches, does not classify "is this a discovery," and does not make you fill fixed fields to feel done. If you find yourself building a rubric or a scoreboard, you have turned a discovery engine into the bureaucracy it exists to replace. For the same reason, let the squad's designs and critiques come back as prose you read and weigh rather than as rigid output schemas — reserve a structured return for the few genuinely small things (a yes/no, a vote); forcing a long judgment through a strict schema is a quiet way to corrupt a run, because the model drops or stubs whatever will not fit and the loss stays invisible. The only hard machinery is the integrity discipline — a blind, ensemble, validity-checked control, and a kill step you can prove actually happened — because a corrupted control or a faked kill fakes the discovery, and that is the one failure that destroys the run's whole point.

**Validity check before you trust the margin.** Confirm the control was genuinely independent (it never saw the squad's work) and genuinely hard (a real careful attempt, not a strawman the squad could trivially beat). Confirm the kill step was real, too: you must be able to quote back the actual refutation each surviving approach faced — a critique you cannot quote back, because it came back empty, garbled, or as a placeholder, is not a critique, and an approach nothing genuinely attacked has not survived anything. Re-dispatch it or fail loudly; never let a missing or stubbed critique pass silently into the pick. The quote-back binds the *crown* you are about to trust, not only the approaches along the way: you must be able to quote the dedicated refutation the crowned design itself faced — and a synthesized hybrid that met only the head-to-head faced none, so its margin is unverified until it re-enters the kill. Confirm the head-to-head was genuinely blind, too: a finalist that reached the judge carrying its selection narration, kill list, or graft commentary tipped which side was the squad's, and a judge that could infer that did not judge blind. If any of this is in doubt, report the differential as unreliable rather than claiming a margin.

## Where It Stops

The deliverable is an approved *design*: the chosen approach and its shape, the key decisions and open risks, the margin (or the honest null), and what got killed and why — so the breadth is visibly real. It stops there.

It does not write the skill. Hand the design to hand-authoring against `agent-facing-design` and `skill-ux-design` (this repo keeps no Claude-side constructor by design). After the skill is authored, prove it with `behavior-smoke-test` and, if you want numbers, `skill-benchmark`. Skill-squad is the front of that pipeline, not the whole of it.
