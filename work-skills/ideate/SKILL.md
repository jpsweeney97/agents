---
name: ideate
description: "Use when the user wants to generate a wide field of genuinely different options before any narrowing: brainstorm broadly, widen the solution space, get unstuck from one idea, or see what is possible. Produces a deliberately un-ranked field and stops there. Do not use to compare, choose, design, or clarify a still-muddy goal."
---

# Ideate

Widen a clear-enough prompt into a deliberately un-narrowed field of genuinely different options, then stop before any ranking. Invocation: `/ideate` or `$ideate`.

Ideate widens the solution space and hands the field off un-narrowed. It never ranks, scores, picks, or develops one option into a design.

## Safety and workspace boundary

- Deliver the field in chat by default. Do not browse, invoke a connector, create a ticket, write an artifact, send, publish, install, or take another external action unless the user separately and explicitly requests it and the active workspace permits it.
- Before reading work content or an artifact, follow the active workspace’s live `AGENTS.md` or `CLAUDE.md` and applicable policy. If classification or permission is unclear, take the more protective route and ask for clarification.
- A durable record is a separate explicit request. Confirm its permitted destination before writing it, and never stage, commit, stash, or push target-work content while Git retention is unapproved.

## The moves — a rhythm, not a fill-in template

1. **Name the frame; confirm you can generate.** State in one line the prompt’s load-bearing assumption, implied unit, owner, or success metric. If the goal is too muddy to say what would count as an option, explain that clarification is needed or suggest an available outcome-shaping method; ideate reframes the solution space, never the goal.
2. **Generate widely from rotating provocations, held as private scratch.** Vary the core mechanism; relax, move, or invert a fixed constraint; walk the ambition ladder (tolerate → cheap patch → standard build → radical rebuild → buy-or-borrow); transplant a distant-domain mechanism; or restate the problem under a different frame. Use what bites. Include the non-serious, unlikely-to-win, frame-breaking option: breadth is the deliverable.
3. **Run two anti-modal moves — mandatory.** Generate the exact opposite of the first instinct and the option that feels slightly embarrassing to propose. Output them as ordinary options, without labels.
4. **De-cluster on mechanism, not clothes.** Collapse two options only when they would succeed or fail for the same named load-bearing reason. If that reason cannot be named, keep both. Where the whole field shares a hidden assumption, name it and generate an option that violates it.
5. **Stop on a stable field, not a count.** Halt when another pass yields nothing mechanism-distinct and the frame-break plus both anti-modal moves are present. A stable field is a fact about this search, not proof that the space is covered.

## Output and the no-certificate rule

Return a flat, un-ranked field. Each option has a short handle, a one-line core idea, and the distinct bet or mechanism that sets it apart — descriptive, never evaluative. Do not include per-option source or lens tags, scores, quality order, a stated lean, or design-level development. Order by a non-quality axis and reword handles or one-liners that reveal a favorite. Light clusters are for scanning, never proof of coverage.

Close with one honest line naming which of the prompt’s own fixed points the field leaves untouched. Never certify coverage over a frame you chose: no coverage ledger, per-option provenance tag, gap map, or “stop at N” box count. The only honest coverage signals are the prompt-anchored frame-break and the untouched-fixed-points line.

## Hard stop and route closure

Stop as soon as a stable field exists, even if the same request asks which option to choose. If the user next wants options developed to comparable depth, a choice among serious options, a few approaches developed toward a design, or clarification of a muddy goal, name that next need in plain language. If a suitable neighboring skill is available in the active workspace, it may be invoked at the user’s request; do not assume it is installed or silently continue into its work.

## When not to widen

- Options are already on the table and the user wants a choice: say comparison or recommendation is the needed next move.
- The goal is too muddy to know what a good option would do: clarify the goal before generating.
- The prompt has one right answer and a wide field would be noise: say so and stop. Knowing when not to widen is part of the skill.
