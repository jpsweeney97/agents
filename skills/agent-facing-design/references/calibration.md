# Agent-Facing Design Calibration

Use these examples to sharpen judgment when the main skill is not enough. They
are not required checks.

## Quick Distinction

Context helps an agent make a contextual call:

- examples and counterexamples
- ownership boundaries
- recoverable state
- evidence the agent can inspect
- clear preconditions and failure behavior

Machinery makes the call for the agent or forces a path:

- required fields and schema shape
- status enums and workflow stages
- validators that judge meaning
- routers and classifiers
- scoring and confidence fields
- semantic decision scripts
- hard rules such as "always" or "never" outside a real safety boundary

Length is not the test. A long page of examples can be context. A one-line hard
rule can be machinery.

## Keep

Keep structure when a wrong value or wrong step degrades the work itself.

- A confirmation gate before destructive deletion protects real user data.
- A credential scanner blocks secret exposure.
- A deterministic parser protects a file format the agent must read correctly.
- Ticket fields such as `title`, `body`, `priority`, and `tags` help readers
  understand and choose work.
- A recovery marker can prevent stale state from silently overwriting current
  work.
- A hook that blocks edits to a protected branch can prevent branch damage.

## Prefer Lighter Context

Prefer context when the structure mostly serves the process around the work.

- A `process_stage` enum used only to satisfy a validator is usually overfit.
- A confidence score passed between workflow phases usually performs certainty
  without improving the work.
- A router that classifies user intent into rigid buckets is usually weaker than
  letting an agent decide from the same conversation.
- A mandatory multi-stage workflow for every task makes simple tasks perform the
  process instead of doing the work.
- Heavy prose that forces review theater is still machinery when it replaces the
  visible decision.

## Borderline Cases

### Required Fields

Ask who uses the field. If a reader uses it to understand, choose, recover, or
trust the work, it may belong in the artifact. If only validators, audit logs, or
pipelines care, keep it transient or remove it.

Moving a value from schema to audit logs does not make it lighter if agents still
must populate it correctly. Deriving a value only helps when it is computed on
demand and discarded, not when it becomes another staged obligation.

### Semantic Scripts

Before writing a script that classifies, scores, triages, routes, or validates
meaning, ask whether an agent with the same context could make that decision in
plain language. If yes, keep deterministic mechanics in code and leave the
semantic decision to the agent.

Good deterministic mechanics include file I/O, parsing, persistence, idempotent
state mutation, indexing, hashing, and transformations where the algorithm
itself is the value.

### Infrastructure

Operational constraints can justify code when code is the point: synchronous
hooks, security guards, policy guards, deterministic parsers, and branch or
permission protection. Latency, token cost, tidy audits, and process completeness
do not justify semantic machinery on their own.

### Skills And Workflows

A skill that offers a checklist as optional calibration is context. A skill that
forces every request through fixed stages is machinery.

When a workflow starts feeling disproportionate, ask whether it still helps the
agent do the user's work or whether the machinery has become the customer.

## Whole-Surface Check

Small additions can accumulate into a rigid surface. Step back when a surface has
grown materially, has seen heavy recent change, or makes you hesitate.

If the surface feels larger than the work it protects, simplify before adding
more structure.
