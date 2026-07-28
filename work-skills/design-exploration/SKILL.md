---
name: design-exploration
description: "Use when the user wants to explore and settle a design before acting: turn a clear-enough outcome into genuinely distinct approaches and an explicitly approved design for a business process, operating system, policy, service, technical system, or mixed target. Do not use to clarify a still-muddy outcome, choose between already-comparable options, pressure-test an existing design, or implement work."
---

# Design Exploration

Turn a clear-enough outcome into an approved design through collaborative exploration. This skill owns the generative middle between outcome clarification and planning: propose real approaches, develop the chosen one into a design, and obtain explicit approval before any implementation or execution begins.

## Authority and safety

Before handling work content, read the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy. Treat them as the authority for what may be read, discussed, retained, or written. If the classification, permission, or destination is unclear, use the more protective route and stop for clarification; do not infer authority.

Work in chat by default. Do not browse, access a connector, install anything, create a file, stage, commit, stash, push, publish, create a tracker item, or make any other external change unless the user separately requests that action and the active workspace permits it. Keep decision-relevant source claims traceable, and label organizing inference `unverified`.

## Boundaries

- Use this skill when the desired outcome is clear enough to design against and the user wants approaches explored or a design shaped.
- If the outcome itself is still muddy, pause to clarify the desired outcome before designing.
- If serious, comparable options already exist and the user wants a decision, use a decision-making method rather than reopening the design space.
- If the user wants an adversarial stress test of an existing design, perform or request a review rather than design exploration.
- If a question can only be resolved through a real run, real data, or actual files, name that uncertainty and offer a separately authorized experiment. Do not perform it implicitly.
- This skill does not implement, execute the designed process, enact a policy, or create production artifacts. A simple request still receives a concise design and explicit approval.

## Core workflow

1. **Explore context first.** Read only the in-scope material the active workspace permits: its instructions, relevant documents, existing process or system boundaries, prior decisions, terminology, constraints, and current state. State what was inspected and what remains unverified. Do not design from an unverified summary alone when primary material is available.
2. **Check scope before detail.** If the request spans independent systems or decisions, say so and divide it into coherent design slices. Design the first slice rather than producing a falsely unified plan.
3. **Clarify only what changes the design.** Ask concise, batched questions about outcome, users or operators, constraints, authority, failure tolerance, interfaces, timing, and evidence. Adapt the inquiry to the target: a business process may need roles and handoffs; a policy may need authority and exceptions; a service may need service boundaries; a technical system may need interfaces and data flow; a mixed target may need the relevant combination. Do not force any target into a fixed partnership, process, or software schema.
4. **Propose genuinely distinct approaches.** Usually develop two or three approaches when they truly exist. Explain each approach's trade-offs and state a labeled lean, not a disguised settled verdict. Give the strongest rival its honest case and identify any value, risk, or meaning trade the user must own. Do not invent weak alternatives to meet a count: when only one serious approach exists, say so and name what evidence could make a real rival worth developing; if no approach is serious enough, widen the field before converging.
5. **Develop the selected approach into a right-sized design.** Cover the material decisions for this target, such as purpose and success conditions; actors, roles, and boundaries; components or stages; information, data, or artifact flow; authority and exception handling; dependencies and interfaces; failure handling; measurement or validation; and rollout or adoption. Use only the sections that genuinely clarify the design. Keep units understandable in isolation, with clear responsibilities and interfaces, and remove features the outcome does not need.
6. **Check in at correctable decisions.** Name the decisions the user may want to correct while they are still cheap to change. Batch independent decisions; do not save all correction for a fluent final draft that invites unexamined assent.
7. **Self-review before asking for approval.** Resolve placeholders, contradictions, ambiguous requirements, unsupported claims, and scope creep. State unresolved uncertainty rather than filling it with confidence.

## Approval and next action

The design is approved only when the user explicitly says so. A request to build, execute, publish, or move to a next step is not approval by itself; summarize the proposed design in one line and ask for approval before proceeding.

For a hard-to-reverse design, offer one separately requested pressure or review pass before settling. On approval, close in chat with a compact handoff capsule: the approved approach, deliberately deferred or open questions, binding constraints, the actual settlement level of major decisions, and the user-chosen next action. Do not assume a planning workflow, tracker, file, connector, or other neighboring capability is available; describe the narrower next action in plain language and continue only after an explicit request.

## Artifacts and proof boundary

Chat is the default deliverable. Create a durable design artifact only when the user explicitly requests it and the active workspace permits the destination; confirm the destination when its convention is not clear. Never stage, commit, stash, or push work-content output unless the active workspace explicitly authorizes that retention and the user separately asks.

The result is a reasoned proposed design, not proof that it will work, that its inputs are complete, or that it is approved until the user says so.
