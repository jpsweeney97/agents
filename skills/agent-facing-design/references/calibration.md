# Agent-Facing Design Calibration

Use these examples to sharpen judgment when the main skill is not enough. They are not required checks.

## Quick Distinction

Apply the context-vs-machinery distinction from the gate definition in `SKILL.md` ("Context supports judgment..." / "Machinery removes or narrows judgment..."); these examples calibrate that distinction, they do not restate or override it.

Length is not the test. A long page of examples can be context. A one-line hard rule can be machinery.

## Keep

Keep structure when a wrong value or wrong step degrades the work itself.

- A confirmation gate before destructive deletion protects real user data.
- A credential scanner blocks secret exposure.
- A deterministic parser protects a file format the agent must read correctly.
- Ticket fields such as `title`, `body`, `priority`, and `tags` help readers understand and choose work.
- A recovery marker can prevent stale state from silently overwriting current work.
- A hook that blocks edits to a protected branch can prevent branch damage.

## Prefer Lighter Context

Prefer context when the structure mostly serves the process around the work.

- A `process_stage` enum used only to satisfy a validator is usually overfit.
- A confidence score passed between workflow phases usually performs certainty without improving the work.
- A router that classifies user intent into rigid buckets is usually weaker than letting an agent decide from the same conversation.
- A mandatory multi-stage workflow for every task makes simple tasks perform the process instead of doing the work.
- Heavy prose that forces review theater is still machinery when it replaces the visible decision.

## Rejected Requested Machinery

Make the deviation visible when the user asks for machinery and the gate rejects it.

Example: the user asks to add a `confidence_score` field to every handoff so the next agent knows whether to trust it. If the real risk is that the next agent cannot tell what was inspected, do not add the field silently or replace it silently.

Say:

- "I would not add `confidence_score`; it performs certainty without giving the next agent better evidence."
- "The failure mode is missing inspection context, so the lighter path is a short `Evidence checked` line with concrete files, commands, or unverified surfaces."
- "I can patch that evidence line instead, but I will not substitute it for the requested field unless you want the smaller design."

## Borderline Cases

### Required Fields

Ask who uses the field. If a reader uses it to understand, choose, recover, or trust the work, it may belong in the artifact. If only validators, audit logs, or pipelines care, keep it transient or remove it.

Moving a value from schema to audit logs does not make it lighter if agents still must populate it correctly. Deriving a value only helps when it is computed on demand and discarded, not when it becomes another staged obligation.

### Semantic Scripts

Before writing a script that classifies, scores, triages, routes, or validates meaning, ask whether an agent with the same context could make that decision in plain language. If yes, keep deterministic mechanics in code and leave the semantic decision to the agent.

Good deterministic mechanics include file I/O, parsing, persistence, idempotent state mutation, indexing, hashing, and transformations where the algorithm itself is the value.

### Infrastructure

Operational constraints can justify code when code is the point: synchronous hooks, security guards, policy guards, deterministic parsers, and branch or permission protection. Latency, token cost, tidy audits, and process completeness do not justify semantic machinery on their own.

### Skills And Workflows

A skill that offers a checklist as optional calibration is context. A skill that forces every request through fixed stages is machinery.

When a workflow starts feeling disproportionate, ask whether it still helps the agent do the user's work or whether the machinery has become the customer.

### Tool Returns

A tool's response is context the calling agent acts on next, so the same distinction runs on it: return what helps the agent decide, not machinery that decides for it. Read your own response back from the caller's chair — no memory of the call, no human to ask — and see whether the next step falls out of it.

- A return that hands the agent evidence, state, and the identifiers its next call needs is context. A return that hands back a verdict, a mandated next step, or a classification the agent should have made itself has decided for the caller.
- A raw dump the agent must wade through or decode — the whole result set inline, raw storage rows, internal enums — is heavier than the work; prefer the agent-meaningful view plus a handle to the rest.
- Silent truncation or a dropped page is a wrong value the agent cannot see; signal what was cut. This is the Keep case on a return: the wrong value degrades the work.
- An error that names what to try next is context; one that only reports what broke leaves the agent guessing. The repo's `{operation} failed: {reason}. Got: {input!r:.100}` is one such shape, not a required one.

### Fan-Outs And Orchestration

Before designing a parallel fan-out, answer four questions: can every branch run at once with no ordering dependency; does each branch produce a different *kind* of finding rather than the same finding from another angle; will merging their outputs fit in the caller's remaining context; is the wall-clock wait long enough for parallelism to be worth the extra contexts? Any "no" means one agent, or a sequence.

Cap orchestration depth at one hop and keep the merge in the calling agent: a delegate that itself delegates must summarize to hand off, so each added layer costs context fidelity and tokens while adding no decision. When a fan-out's results need combining, the caller combines them; it does not spawn a combiner. This consolidates what `plan-panel-loop` (no nested panels), `improve-codebase-architecture` (subagents return findings; the caller writes the report), and `design-exploration` (read the load-bearing files yourself; never design from summaries alone) each already state for their own lane.

### Reader Capability

The presumption against machinery prices agent judgment as worth preserving, which presumes a reader whose judgment is strong. Ask who actually reads the surface, at what capability, under what load: a small subagent in a fan-out, a degraded end-of-context session, or a cross-model reader may need firmer shapes than a frontier main loop would tolerate, and structure that would insult the strongest reader can be load-bearing for the weakest. Schema-forced returns at machine seams — a subagent's structured output, a typed findings report — are this case working as designed: deterministic transport of judgments still made in prose, not a violation of the gate. The bet runs in both directions: as the readers of a surface strengthen, so does the presumption against machinery, and a shape built for a weaker reader is worth revisiting when the reader changes.

## Whole-Surface Check

This check now lives in `SKILL.md`'s Core Move, where the gate runs per edit and round by round through a review loop — the place a run of individually justified additions actually accretes. Consult it there; this reference no longer carries it.
