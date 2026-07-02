---
name: ideate
description: "Use when the user wants to GENERATE a wide field of genuinely different options before any narrowing: brainstorm broadly, widen the solution space, get unstuck from one idea, see what is possible. Produces a deliberately un-ranked field and stops there. Do not use to pick among options already on the table (`making-recommendations`), shape or approve one design (`design-exploration`), clarify a still-muddy goal (`outcome-shaping`), or stress-test a settled plan (`grill-me`)."
---

# Ideate

Widen a clear-enough prompt into a deliberately un-narrowed field of genuinely different options, then stop before any ranking. Invocation: `/ideate` or `$ideate`.

ideate is the library's one *divergent* skill. Everything around it converges — `making-recommendations` ranks, `design-exploration` shapes and approves, the review and grilling lanes adjudicate. ideate runs the other direction: it generates breadth and hands it off un-narrowed. It never ranks, scores, picks, or develops one option into a design.

## The owned job (why it is a distinct skill)

A capable agent told "brainstorm widely" already produces a list, so ideate earns its place two ways: it *guarantees* the behaviors that bare list silently drops under load (below), and it is the one owner whose **product is breadth**. It is defined by inverting its two nearest neighbors, both of which also generate:

- `making-recommendations` generates options, but admits only *serious, could-win* ones because it is decision-bound. ideate deliberately admits the **non-serious, won't-win, frame-breaking** option — in this lane breadth is the deliverable, not a means to a pick. ideate is not "making-recommendations with the ranking deleted"; it has the opposite admission rule.
- `design-exploration` proposes a few genuinely different approaches too, but with **convergent gravity**: it leads with a recommendation and develops one toward an approved design. ideate has the opposite gravity — it widens and refuses to converge, leaving the field un-narrowed for a downstream lane to narrow.

## Mixed skill — apply the bar per part

- **Provoked (judgment).** What options to generate, whether two are genuinely distinct, which frame the prompt smuggles in. The skill poses forcing moves; it never fills them in for the agent and never hardens into a template completed to feel done.
- **Firm (trust).** The un-ranked output shape, the no-leak hard stop, the boundary, the no-coverage-certificate rule. Their value is a predictable shape the next lane can consume; a missing part is a defect, not a style choice.

## The moves — a rhythm, not a fill-in template

1. **Name the frame; confirm you can generate.** State in one line the frame the prompt assumes — its load-bearing assumption, implied unit, owner, or success metric. If the *goal* is too muddy to say what would even count as an option, hand to `outcome-shaping`; the only reframing ideate owns is of the solution space, never the goal.
2. **Generate widely from rotating provocations, held as private scratch.** Vary the core mechanism; relax, move, or invert a constraint assumed fixed (budget, deadline, must-reuse-X); walk the ambition ladder (tolerate → cheap patch → standard build → radical rebuild → buy-or-borrow); transplant a mechanism from a distant domain; restate the problem as a different frame and generate under it. Use the ones that bite; drop the rest. A provocation is a tool that produces an option, never a label on it.
3. **Run two anti-modal moves — mandatory.** The exact opposite of your first instinct, and the option you would be slightly embarrassed to propose. These are the divergence an eager model skips, and they are what make the field wider than `design-exploration`'s natural two or three. They land in the field described like any other option — no "opposite" or "embarrassing" tag survives to output.
4. **De-cluster on mechanism, not clothes.** Two options collapse to one if they would succeed or fail for the same reason — if they share the same load-bearing mechanism or assumption (Postgres and MySQL both bet on a single relational node: one option, not two). A different provocation that produced the same mechanism is still one option. Where the *whole field* shares one hidden assumption, name it aloud and generate an option that violates it.
5. **Stop on a stable field, not a count.** Halt when another pass yields nothing mechanism-distinct and the frame-break plus both anti-modal moves are present. Quantity is a raw generation target, never the done-test.

## Output and the no-certificate rule

A flat, **un-ranked** field. Each option: a short handle, a one-line core idea, and the distinct bet or mechanism that sets it apart — descriptive, never evaluative. No per-option "source" or "lens" tag (it manufactures the surface difference the de-cluster exists to strip). No scores, no ordering by quality, no "I'd lean," no developing an option into a design. Cluster lightly only for scannability; clustering is presentation, never proof of coverage.

Close with **one honest line naming which of the prompt's own fixed points the field still leaves untouched** — anchored to the prompt's stated constraints, not to axes you drew. That is the only coverage signal allowed.

**Never certify coverage over a frame you chose.** A coverage ledger, a per-option provenance tag, a gap-map, or a "stop at N" box-count all manufacture false confidence worse than honest ignorance — the field looks complete relative to a map you drew, exactly where that map is blindest. The two honest coverage signals are both externally anchored: the prompt-anchored frame-break, and the untouched-fixed-points line.

## Hard stop and handoff

Stop the instant a stable field exists — even when the same message asks "so which?" Crossing into evaluation is the failure this skill exists to prevent. Hand off by naming the lane and stopping, never silently continuing:

- **`making-recommendations`** — the user wants to pick among the options now on the table.
- **`design-exploration`** — the user wants a few approaches shaped and developed toward an approved design.
- **`outcome-shaping`** — generating revealed the goal itself is too muddy to know what counts as an option.

## When not to widen

- The options are already on the table and the user wants a pick → `making-recommendations`.
- The goal is still muddy — you cannot say what a good option would even do → `outcome-shaping`.
- The prompt has one right answer and a wide field is just noise → say so and stop; do not manufacture diversity. Knowing when *not* to widen is part of the skill.

## Build-and-prune note

Chat-first; no artifact by default. Divergent generation fires often and locally, so this is not first-to-prune — but watch it actually earn its four guarantees over a bare brainstorm, and fold or prune if in practice it only restyles a list a capable agent already produces. The honest differential is reliability plus modest cognitive-offload, not a new capability.
