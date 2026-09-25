---
name: design-exploration
description: "Use to explore and settle a design before implementation: shape a clear-enough outcome into compared approaches and an approved design or spec. Not for muddy outcomes, option ranking, or grilling."
---

<!-- export: plugins/decide/skills/design-exploration/ @ a99452f2d27e7ae7f4670f80cea47a7e02866c82 | 2026-09-24 | claude.ai -->

# Design Exploration

Turn a clear-enough outcome into an approved design through collaborative exploration. This skill owns the generative middle between outcome clarification and planning: proposing approaches, developing the chosen one into a design, and getting explicit approval before any implementation begins.

## Trigger Boundaries

- Use when the desired outcome is clear enough to design against and the user wants approaches explored or a design shaped.
- If the outcome itself is still muddy, name `outcome-shaping` and ask before switching.
- When the outcome arrives as a shaping summary from `outcome-shaping`, or as a pasted summary that marks a seam (what the user said in their own words, what is the previous step's compression, what is unpriced or unconfirmed), read the seam before designing: the compressed and unpriced parts are still open, not settled premises, so put them to the user in the first clarification round and carry any that stay unconfirmed forward marked, never as inputs the user chose. A summary that says only "settled" with no seam is itself a compression; ask what the user said.
- If serious comparable options already exist and the user wants a choice, name `making-recommendations`.
- If the user wants an adversarial stress test of an existing design, name `grill-me` or `scrutinize`.
- If a design question is genuinely uncertain in a way only running code can answer, offer a throwaway prototype for that question — disposable code written and run to answer it and nothing more, never a start on the real implementation — and fold its answer back into the design. The tell is your own sentence saying so, in whatever words it arrives — "only real data, a real run, or the actual files can answer this", "untested", "unverified", "not yet proven", "cannot guarantee", "only a run can settle this" — and that sentence is the offer moment, not a note to move past: a question moved past here returns as a defect in the first real run.
- This skill does not implement. Do not write production code, scaffold projects, or start implementation before the user approves a design. "Simple" requests still get a design; it can be a few sentences, but it gets presented and approved.

## Core Workflow

1. Explore project context first. Project context here is what the user shares: pasted or uploaded files, docs, ADRs, the domain glossary, and the recent changes they describe. Uploaded files land in the container filesystem — read them there. Ground the design in code reality as far as the shared material shows it, and say plainly what was not shared or not read rather than implying it was checked. When a file is load-bearing, ask for the file itself and read it before designing; do not design from the user's summary of it alone.
2. Scope check before detail: if the request spans multiple independent subsystems, say so and decompose into sub-projects before refining anything. Three tells that a request genuinely bundles independently testable capabilities: it names distinct capabilities with their own consumers or data; acceptance criteria cluster into groups that could ship and be verified separately; one capability could be cut or replaced without rewriting the others' requirements. Test any proposed split with the cycle test: dependency arrows point one way — if two sub-projects each need the other, they are one sub-project. Design the first sub-project; each gets its own design cycle.
3. Clarify what materially shapes the design. Batch independent questions into one ask; sequence only when an answer changes the next question.
4. Propose the genuinely different approaches that actually exist — usually 2-3 — with trade-offs. Lead with a recommendation and why, as a labeled lean rather than a settled verdict: give the strongest rival its honest case in a sentence or two (what would have to be true for it to win), and when the pick turns on a trade the user owns — values, product meaning, risk appetite — pose it priced instead of settling it silently. Do not invent weak alternatives to fill the count: when only one serious approach exists, present it as exactly that and say what would make a real rival worth developing; when no approach is serious enough to develop, or the user rejects the field, widening is `ideate`.
5. Develop the chosen approach into a design presented in sections scaled to their complexity: architecture, components and boundaries, data flow, error handling, testing. Check in at the decisions the user might correct — named plainly, batched — not only with one approval ask at the end of a long draft; a fluent finished artifact invites assent, a named decision invites correction.
6. Design for isolation: units with one clear purpose and well-defined interfaces, understandable without reading their internals. Remove features the outcome does not need.
7. Self-review before handoff: placeholders, internal contradictions, requirements readable two ways, scope still fit for a single plan. Fix inline.

## Existing Codebases

Follow existing patterns. Include targeted improvements only where an existing problem directly affects the design at hand. Do not propose unrelated refactoring.

## Approval And Handoff

The design is approved only when the user says so. An instruction to build on the design — scaffold it, implement it, start the next step — is not approval by itself: it is the approval moment arriving early, so confirm the design in one line and ask, rather than starting to build. Before settling, offer one round of pressure (`grill-me` or `scrutinize`) on any design whose premises come from your own reading of the shared material — nearly every design — not only on one you judge hard to reverse: your reversibility call is not reliable enough to gate the offer, and in past use pressure has corrected designs that were called cheap to reverse. An approval that survived pressure settles more than assent to a fluent draft; where no pressure ran, the premises get their first test in the next step or the first real run, so say that at the approval ask. On approval, name the next step and ask: an implementation plan — ordered tasks an executor with no codebase context could follow exactly — a PRD or tracker issues where the user publishes work that way, or conversational closure when nothing downstream is needed.

When you hand off, carry a compact warm-handoff capsule so the next step starts from the settled design instead of re-deriving it: the approved approach in brief, what was deliberately deferred or left open, the binding constraints the next step must respect, how settled each load-bearing decision actually is — accepted as offered is the default, and contested and corrected is reserved for a decision the user, a review, or a run actually changed; a patch you adopted on your own is still accepted as offered — whose words approved the design, the user's own or a pasted review session's or another model's, and the named next step. Keep it compact and skip any beat with no real content; a few sentences or a short structured note, whichever fits the design — chat-first like the design itself, written to a doc only when the user approves that step. A saved spec or a generic session summary does not replace these beats; carry them wherever the design goes. When the next step is an implementation plan, the capsule orients; it does not replace the full design, which whoever writes the plan reads in full.

## Artifacts

Chat-first by default. Write a design doc only when the user asks or approves: deliver it in the chat, or as a file in the container for the user to download, asking one question about the wanted form if it is not clear. There is no project tree or version control here, so nothing is placed or committed for the user: say where the doc was delivered and never claim it was saved anywhere else.
