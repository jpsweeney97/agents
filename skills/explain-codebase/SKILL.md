---
name: explain-codebase
description: "Use when the user wants to understand an unfamiliar codebase as a whole — what it does, how it's structured, how to run and navigate it — a first-pass orientation in a stranger's repo. Do not use to map one named area a layer up (`zoom-out`), report where work stands (`orient-status`), find architecture-deepening opportunities (`improve-codebase-architecture`), debug a specific failure (`diagnose`), or make changes."
---

# Explain Codebase

Build a faithful first-pass model of an unfamiliar codebase: what it is, how it's shaped, how it runs, and how to navigate it. Comprehension only — read, do not change.

## First move

Read the repo's own account of itself before its source. Start with the README, `AGENTS.md`/`CLAUDE.md`, `CONTEXT.md`, `docs/`, and the package/build manifests; let them point you at the entry points. Map from what the repo says and what the code shows — not from memory or filename guesses — and use the project's own vocabulary (its glossary or `CONTEXT.md`) over terms you invent.

Scope to what the user named: a whole repo, or one subsystem within it. If nothing is named, default to the repo root; if the named target maps to several candidates, ask which. When the codebase is large, map the top-level structure first and say what you did not open rather than reading everything — the coverage ledger below makes that honest.

Use an exploration subagent when the runtime offers one (in Claude Code, the Agent tool with `subagent_type=Explore`); otherwise explore directly.

## Stay read-only

You are a guest in someone else's tree. Inspect only: do not edit, format, install, generate, or run the project's build, test, or run commands. When you discover how the project is built, tested, or run, **report those commands — detected, not executed.** Naming the test command is comprehension; running it is a change.

## Trace one path end-to-end

Pick one representative path through the system — a request, a CLI invocation, a job, or the lifecycle of one core data item — and follow it across every layer it touches, from entry point to effect. One real trace shows how the parts actually fit together in a way a module-by-module tour does not. Choose the path that explains the most of the system, and say why you chose it.

## Output

A grouped map, not an essay:

- **What it is** — the codebase's job, in one or two sentences.
- **Shape** — the top-level structure: the main modules or directories, each with a one-line role.
- **How it runs** — entry points, plus the detected (not executed) build / test / run commands and the key configuration.
- **One path traced** — the end-to-end flow from above, layer by layer.
- **Coverage** — an honest ledger of your own reading: what you read closely, what you only skimmed, what you left unopened, and any claim you are not confident about. This is the most useful part for the next reader — do not pad it to look thorough, and do not bury the gaps.

## Stop

Deliver the map and stop. Do not propose or make changes. If the user then wants to go further, name the lane and hand off: `improve-codebase-architecture` to deepen structure, `zoom-out` for one named area a layer up, `diagnose` for a specific bug, `orient-status` for where the work stands, `implementation-planning` to plan a change.
