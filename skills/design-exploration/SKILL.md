---
name: design-exploration
description: "Use when the user wants to explore and settle a design before implementation: shaping a clarified idea into compared approaches and an approved design or spec, including requests to design a feature, explore approaches, or shape a solution. Do not use for clarifying a muddy outcome, choosing between already-comparable options, pressure-testing an existing plan or design, implementation, prototyping, or PRD/issue publication."
---

# Design Exploration

Turn a clear-enough outcome into an approved design through collaborative
exploration. This lane owns the generative middle between outcome
clarification and planning: proposing approaches, developing the chosen one
into a design, and getting explicit approval before any implementation lane
takes over.

## Trigger Boundaries

- Use when the desired outcome is clear enough to design against and the user
  wants approaches explored or a design shaped.
- If the outcome itself is still muddy, name `outcome-interviewer` and ask
  before switching.
- If serious comparable options already exist and the user wants a choice,
  name `making-recommendations`.
- If the user wants an adversarial stress test of an existing design, name
  `grill-me` or the relevant review lane.
- If a design question is genuinely uncertain in a way only running code can
  answer, offer `prototype` for that question and fold its answer back into
  the design.
- This lane does not implement. Do not write production code, scaffold
  projects, or invoke an implementation lane before the user approves a
  design. "Simple" requests still get a design; it can be a few sentences,
  but it gets presented and approved.

## Core Workflow

1. Explore project context first: relevant files, docs, ADRs, the domain
   glossary, recent commits. Ground the design in code reality.
2. Scope check before detail: if the request spans multiple independent
   subsystems, say so and decompose into sub-projects before refining
   anything. Design the first sub-project; each gets its own design cycle.
3. Clarify what materially shapes the design. Batch independent questions
   into one ask; sequence only when an answer changes the next question.
4. Propose 2-3 genuinely different approaches with trade-offs. Lead with a
   recommendation and why. Do not invent weak alternatives to fill the count.
5. Develop the chosen approach into a design presented in sections scaled to
   their complexity: architecture, components and boundaries, data flow,
   error handling, testing. Check in after sections the user might correct.
6. Design for isolation: units with one clear purpose and well-defined
   interfaces, understandable without reading their internals. Remove
   features the outcome does not need.
7. Self-review before handoff: placeholders, internal contradictions,
   requirements readable two ways, scope still fit for a single plan. Fix
   inline.

## Existing Codebases

Follow existing patterns. Include targeted improvements only where an
existing problem directly affects the design at hand. Do not propose
unrelated refactoring.

## Approval And Handoff

The design is approved only when the user says so. On approval, name the
next lane and ask: `implementation-planning` for an executable plan doc,
`to-prd` or `to-issues` for tracker publication, or conversational closure
when nothing downstream is needed.

## Artifacts

Chat-first by default. Write a design doc only when the user asks or
approves; place it per repo convention, asking one path question if no
convention is clear. Do not commit automatically.
