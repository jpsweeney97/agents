---
name: zoom-out
description: "Use only when the user explicitly invokes `/zoom-out` or `$zoom-out` to get a higher-level map of an unfamiliar code area, including relevant modules, callers, and how the area fits the broader system. Do not use for implementation, debugging, code review, status orientation, or architecture improvement recommendations."
disable-model-invocation: true
---

# Zoom Out

Map an unfamiliar code area one layer up: what's here, what reaches in, what it
depends on, and where it sits. Orientation only — do not propose changes, review
code, debug, or plan.

## First move

Identify the target area the user named (module, directory, file, or concept); if
none is named, or the name maps to several candidates, ask which one. Read its
entry points and immediate callers and callees before answering — map from the
code, not from memory — and use the project's domain glossary or `CONTEXT.md`
vocabulary for names rather than inventing terms.

## Default scope

The target plus its direct callers, its direct dependencies, and the seams it
sits behind — one layer up, not the whole repo. Widen only if the user asks. When
the area is large, map the top-level structure and name what you did not expand.

## Output

A short grouped map, not prose:

- **This area** — modules/files in scope, each with a one-line role.
- **Reaches in** — the callers and entry points that lead into this area.
- **Depends on** — what this area calls out to (modules, services, data).
- **Sits in** — how the area fits the broader system, in one or two sentences.

## Stop

Deliver the map and stop. If the user then wants deepening, review, debugging, or
a plan, name the lane (e.g. `improve-codebase-architecture` for deepening,
`diagnose` for a bug, `implementation-planning` for a plan) and hand off.
