# Codex-Facing Design Reference

This reference supports the compact Design Gate in `../AGENTS.md`. Load it when
adding or materially changing Codex-facing schema, workflow stages, routing
logic, validation machinery, plugin behavior, skill behavior, or scripts that
classify, triage, score, route, validate with semantic judgment, or decide.

## Core Tenet

This repo builds Codex-facing systems: plugins, skills, hooks, agents, commands,
MCP servers, and prompts Codex reads at runtime. For these systems, prefer giving
Codex judgment-supporting context over encoding behavior in rule machinery.

Hard rules remain appropriate where a mistake degrades the work itself: safety,
destructive actions, data integrity, recovery guarantees, stale state, and
similar high-stakes boundaries. Everywhere else, prefer durable context, clear
boundaries, recoverable state, and structured evidence, then let Codex exercise
judgment.

## Test 1: Whose Failure Is It?

If Codex populates a field or follows a rule incorrectly, ask what suffers:

- If the work product suffers, the structure may be justified.
- If only the plugin's own machinery suffers, the structure is probably over-fit.

The work product is the artifact a non-plugin reader consumes: a skill contract,
handoff, ticket, review finding, generated document, or other output that matters
outside the tool's internal pipeline.

A field counts as Codex-facing ontology if Codex has to know about it anywhere:
schema, contract, pipeline stage, audit log, engine interface, or persisted
derived state. Moving a value from schema to audit logs does not fix over-fit if
Codex still has to populate it correctly. Deriving a value at runtime only
removes it from the ontology when the value is computed on demand and discarded.
It does not help when the value is computed once and passed between stages.

Common over-fit fields:

- internal state classifications
- confidence scores passed between pipeline stages
- derived hashes that couple workflow stages
- override flags that only validators care about
- contract version stamps used only by internal machinery

Remove these, demote them to truly transient runtime values, or acknowledge that
they are over-fit and evaluate them under Test 2.

## Test 2: Tooling Or Thinking?

Separate fields that help Codex reason from fields that exist mainly for
tooling.

Thinking fields are small, bounded, and content-shaped. A human reader of the
output would also reference them. Examples include `title`, `body`, `priority`,
`tags`, `summary`, `branch`, or `timestamp` when those fields directly help a
reader understand or use the work.

Tooling fields exist mainly for queries, audits, downstream automation, pipeline
bookkeeping, or validators. These fields multiply without limit when unchecked.
When tooling fields outnumber thinking fields, the artifact has inverted its
purpose: the plugin has become the customer, not the work.

Apply this test both per addition and periodically to the full surface. Balanced
incrementalism can still produce a heavy ontology if every small addition looks
reasonable in isolation.

## Test 3: Could Codex Do This Inline?

Before writing a script that classifies, triages, validates with semantic
judgment, scores, decides, or routes within plugin, skill, or agent workflows,
ask: given the same context the script will consume, could a thinking Codex
produce the same decision in prose?

If yes, the script is replacing judgment with code. Move the decision back to
Codex. Keep only deterministic mechanics in code:

- file I/O
- schema parsing
- persistence
- idempotent state mutations
- search ranking
- indexing
- encoding
- hashing
- deterministic transformations where the algorithm itself is the value

Imperative code that pre-decides for Codex is easy to miss because it may not
add schema fields. It still causes the same harm as over-fit ontology when it
forces a fixed decision path that should remain contextual.

## Infrastructure Exemptions

Test 3 does not block infrastructure code when the operational constraints are
the reason the code exists.

Exempt classes:

- Hooks running synchronously on every Codex tool invocation.
- Security and policy guards, such as credential scanners, destructive-action
  blockers, and branch protection.
- Deterministic computational machinery where the algorithm itself is the value,
  not the semantic decision the algorithm produces.

"Unacceptable latency", "token cost", and "fail-open risk" are valid arguments
only inside these classes. They are not free-standing exemptions, and they do
not justify semantic classifiers, triage scripts, scoring systems, or routers
just because those scripts are called frequently.

## Test 4: Re-Test The Whole Artifact

Tests 1 through 3 fire per addition. Re-run all three on the full Codex-facing
surface when any of these triggers occurs:

- About 25 commits have touched the artifact's directory since the last review.
- The Codex-facing surface has grown by about 50% since the last review.
- Adding the next item makes you hesitate.

The numbers are calibration, not a contract. The deterministic floor exists
because momentum-driven development suppresses hesitation exactly when
re-evaluation is most needed.

If the artifact's Codex-facing surface feels disproportionate to the work it
does, treat that as a redesign signal. Responsibility for Test 4 falls on the
person or agent adding the next item. If you cannot tell when the last full
review happened, run it now.

## Illustrative Shapes

| Shape | Verdict | Why |
| --- | --- | --- |
| A document artifact with `title`, `body`, `priority`, and `tags` | Keep | A non-plugin reader uses each field. |
| The same artifact also carrying `process_stage`, persisted derived hashes, classification confidence, contract version, and hook origin | Over-fit | Only internal machinery cares; derived or audit-log placement does not save it if the value crosses stages or Codex must populate it. |
| A script that classifies user intent into categories and routes to handlers inside a plugin workflow | Over-fit | A thinking Codex with the same input could choose the category in prose. |
| A hook that scans files for credentials and blocks egress | Hard rule | It runs synchronously, is security-critical, and wrong behavior can leak secrets. |
| A hook that blocks edits to protected branches | Hard rule | Wrong behavior can cause real branch or data damage. |
| A skill that forces every case through a fixed N-stage workflow | Over-fit | Simple and complex cases are both forced through the same path. |
| A skill that offers a checklist Codex consults when useful | Keep | Structure is context, not a mandatory workflow. |
| A session-state plugin with `session_id`, `timestamp`, `branch`, and `summary` persisted to disk | Keep | Fields are content-shaped, and wrong values degrade the handoff itself. |

## Relationship To Other Tenets

This design reference sits alongside `/Users/jp/.codex/tenets.md`; it does not
replace it.

The broader methodology tenets cover code design, problem solving, and risk
awareness for irreversible actions. This reference is narrower: it governs the
Codex-facing surface in this repo. Runtime code under a Codex-facing artifact
still follows normal code-design tenets. The Codex-facing surface above that
runtime should stay light enough that normal work does not become heavy.

Where a broader tenet and this reference directly conflict, use the more
specific rule for the surface being changed.
