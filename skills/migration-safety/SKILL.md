---
name: migration-safety
description: "Use when a specific database schema or data migration is about to run against a live system and needs a safety plan before it ships: expand-contract sequencing tied to deploy order, a per-statement lock/index/backfill hazard scan confirmed against the engine and version, drop-last ordering, and per-step rollback. Advisory only — it authors the plan, never runs the migration, backfill, or rollback. Not for a codemod/rename/call-site sweep across many code sites (`migration-campaign`, despite the shared word), mapping which consumers an interface change breaks (`contract-change-propagation`), or the generic ship go/no-go gauge (`deploy-plan`)."
---

# Migration Safety

Make a specific database schema or data migration safe to run against a live system — *before* it ships. Invocation: `/migration-safety` or `$migration-safety`.

An advisory pass over one concrete migration — a planned DDL change, a backfill, a column or table reshape — that sequences it to ship without an outage or data loss, scans each statement for the lock and reversibility footguns, and stops at the reviewed plan. It authors or reviews the migration plan; it never runs the migration, the backfill, or the rollback.

## Shape — a forcing pass over one migration

First, **confirm the engine and version** — a required first step, not a courtesy. The lock verdict for the *same* statement flips on it: a `NOT NULL`-with-default add rewrites the table on PostgreSQL < 11 but not on 11+; MySQL routes large changes through `INSTANT` / `INPLACE` / `COPY` algorithms or `pt-osc` / `gh-ost`; SQL Server and Oracle differ again. Confirm the engine and version before flagging any statement. Where they cannot be confirmed, give the hazard scan *conditioned* on them ("rewrites on PG < 11, safe on 11+ — confirm your version") and flag it loudly; never emit a flat verdict that silently assumes Postgres. A confidently-wrong lock verdict here is an outage, not a style nit.

Then sequence the change as **expand-contract / parallel-change** and walk each phase. Each phase pairs its DDL or app-deploy step with a reversibility note; the ordering against the rolling deploy *is* the safety. Walk only the phases this migration needs — a purely additive online change (a nullable column, a concurrent index) may be **Expand**-only, while a read/write reshape that replaces an existing column or table needs the full sequence:

- **Expand** — add the new shape additively and online (nullable column, new table, index built `CONCURRENTLY` / online). Nothing reads or writes it yet; fully reversible.
- **Dual-write** — deploy the app to write both the old and new shapes. (An app deploy, not DDL — name it, because its order against the rolling deploy is what keeps every running version correct.)
- **Backfill** — copy existing data in bounded, throttled batches; never one long `UPDATE`. Each batch restartable, the backfill idempotent.
- **Switch reads** — deploy the app to read the new shape, once the backfill is complete and verified.
- **Stop writing old** — deploy the app to stop writing the old shape.
- **Contract** — drop the old shape **last**, only after every still-running version has stopped reading it. This ordering is the most-missed safety: dropping or renaming a shape the old app version still reads breaks the deploy window.

Then **scan each statement for the footguns** and flag every one that fires — each as a forcing question, not a fill-in:

- **Table-rewriting / long-lock DDL** — does this statement take an exclusive lock and rewrite or scan the whole table (engine/version-dependent `NOT NULL`+default adds, type changes, some constraint validations)? On a large or hot table that is downtime. Route to the non-blocking form for your engine: add nullable then backfill then constrain, and validate constraints in a separate non-scanning step (on PostgreSQL, `ADD CONSTRAINT ... NOT VALID` then `VALIDATE`; use the equivalent elsewhere).
- **Blocking index builds** — is any `CREATE INDEX` missing the engine's online/concurrent form? It locks writes for the whole build. Use `CONCURRENTLY` / online DDL, and note the concurrent form cannot run inside a transaction block.
- **Unbatched backfills** — is any data backfill a single large transaction? It holds locks, bloats, and starves replication — the footgun most likely to pass in staging and stall a replica in production. Batch and throttle.
- **Replication lag / long transactions** — do large writes or long-held transactions on the primary lag replicas or risk stalling failover? Bound them.
- **Drop / rename ordering** — is anything dropped or renamed before every running reader has stopped using it? Drop old last.
- **Per-step rollback and the point of no return** — is each step independently reversible, and is each **point of no return named** (`runbook-authoring`'s graded / multi-PONR vocabulary, by reference)? The destructive drop, and often the backfill, are past the clean-rollback line. A migration whose only abort path is "restore from backup" is the finding, not the plan; name each point of no return, never assume there is one.

Close by **checking the footguns off** explicitly: engine/version confirmed (or each verdict conditioned on them), every statement's lock class flagged, backfills batched, indexes online, drop-last ordering held, each step reversible with its point of no return named. An unchecked footgun is the finding.

## Modes and scope

- **Applied vs advisory follows the invocation.** On a live migration file or PR, author the corrected sequence and per-statement fixes as concrete edits (the rewritten DDL, the batched backfill, the `CONCURRENTLY` index, the split phases). On a proposed migration or in review, deliver the plan and findings for a human. Default to the mode the context implies; ask once when genuinely ambiguous.
- **Applied mode does not dissolve the judgment.** When you author edits, surface each engine/version assumption and each ordering choice as a flagged inline decision, not a default silently baked in. The forcing questions become visible judgment calls in the diff; they do not disappear into rewritten SQL.
- **One migration.** Default scope is one migration — one change set against one schema. Pointed at a whole migrations directory, narrow to the riskiest pending migration(s) and *say so* — this is a forcing pass, not an audit. A scored backlog of migration debt is `tech-debt-scan`'s job.

## Proof boundary

This skill authors the plan; it cannot read the live database. It cannot confirm the real table size, current lock contention, replication topology, row count, or that a backfill actually completed — those are live reads a human or an operational tool must do. State what was assumed (treat the table as large and hot unless told otherwise) and what stays unverified until the live DB is checked: *"sequenced expand-contract with a batched backfill; not confirmed against the real table size or replica lag."* Advisory-only: never run the migration, the backfill, or the rollback.

## Fences

- One mechanical *code* edit swept across many call sites → `migration-campaign` (the name collision — zero DB/DDL content there).
- The migration also changes an interface external code reads → hand the consumer-mapping and semver work to `contract-change-propagation`; own only the DB-execution safety here.
- The ship's go/no-go gauge, abort thresholds, and bake window → `deploy-plan`; a risky migration uses both.
- A durable, reusable migration/rollback runbook → `runbook-authoring`, fed by this skill's plan.
- Wide accidental failure-imagination with tripwires and no verdict → `premortem` — a fine complement, not this procedure.

## Done when

- The engine and version are confirmed, or every lock verdict is conditioned on them and flagged.
- The change is sequenced expand-contract / parallel-change, each phase the migration warrants paired with its deploy step and a reversibility note, with drop-old-last ordering held.
- Every statement's footguns are scanned and flagged: table-rewriting / long-lock DDL, blocking index builds, unbatched backfills, replication-lag risk, drop/rename ordering, and per-step rollback with each point of no return named.
- The output is delivered in the mode the invocation implies (applied edits or a reviewed plan), advisory-only, with the proof boundary stated — what was assumed and what stays unverified until the live DB is checked. No verdict beyond *safe-as-sequenced* / *unsafe-here-because*.
