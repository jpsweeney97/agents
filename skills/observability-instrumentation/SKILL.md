---
name: observability-instrumentation
description: "Use when adding or improving telemetry in code before incidents — deciding what to log, what metrics and traces to emit, and what to alert on for one service or diff, with the cardinality, correlation-ID, PII, and symptom-vs-cause footguns checked off. Do not use for reactively hunting an unknown failure (`diagnose`), reading signals that already exist for one ship's go/no-go (`deploy-plan`), checking whether a shipped change moved its goal (`outcome-check`), or authoring an alert-response procedure (`runbook-authoring`)."
---

# Observability Instrumentation

Lay down the right signals *before* the incident that needs them. Invocation: `/observability-instrumentation` or `$observability-instrumentation`.

A proactive pass over one concrete target — a service or a live diff — that decides and authors the telemetry the system will need, then checks the production footguns off before it ships. It authors or recommends instrumentation; it never runs the system, reads a live signal, or hunts a bug.

## The owned job

This is the **producer** in a library full of telemetry **consumers**. `diagnose` reads signals to find a cause, `deploy-plan` reads them for a ship's go/no-go, `outcome-check` reads them to see whether a goal moved, `incident-response` reads them under fire — and `system-design-review` / `tech-debt-scan` only *flag* that instrumentation is thin. None of them author it. `observability-instrumentation` owns exactly that: putting the signals in place, ahead of time, so the consumers have something correct to read.

Its center of gravity is **time-asymmetric**. A correlation ID not threaded, or a metric label left unbounded, cannot be added cheaply after the 3am incident — by then the request that needed the trace is gone and the series has already cost its damage. The value is laying the signals down *now*, while there is still time to do it well and while the human is spared composing the careful telemetry prompt and auditing afterward that nothing was skipped.

## Mixed skill — apply the bar per part

- **Firm (trust).** The footgun checks below — a bounded label set under a cardinality budget, correlation/trace IDs threaded across boundaries, a no-PII/no-secrets floor on log content, symptom-not-cause alerting, no hot-path log spam, and RED/USE coverage complete for the in-scope paths and resources (the full RED triple — rate, errors, *and* duration — not a half-remembered subset, and not a mandate to instrument everything). These have right/wrong answers and a predictable shape; a skipped check is a defect, because the value is the *complete* pass, not a plausible one.
- **Provoked (judgment).** *What* is worth logging at a given decision point, and *what* is page-worthy for this system. The skill poses these as forcing questions keyed to the target; it never answers them with boilerplate telemetry and never hardens into a template filled to feel done.

## Shape — a forcing pass over one target

First, **confirm the stack**: the language, and the metrics / tracing / logging backend (Prometheus, Datadog, OpenTelemetry, ELK, …) — cardinality cost and propagation mechanics differ by backend. Confirm rather than assume one backend's defaults, but do not block on the answer: proceed on a clearly-labeled default and flag what would change under another backend. Then the principles below apply concretely instead of as an encyclopedia.

Then walk the concerns the target warrants — each as a forcing question, not a fill-in:

- **Log events** — structured, named fields, at the decision points a future debugger will need. *Which events would you wish existed while reading this code at 3am?* Floor: no PII or secrets in fields; no per-request spam on the hot path.
- **Metrics** — RED (rate, errors, duration) for request paths, USE (utilization, saturation, errors) for resources, under a **fixed label set with an explicit cardinality budget**. *What is the smallest label set that still answers the questions you will ask — and does any label (user ID, URL, raw input) make the series unbounded?*
- **Traces / correlation IDs** — generate an ID at the entry point and thread it through every boundary (async, queue, RPC). *Where does the request cross a boundary that would drop the trace?* This is the check most often skipped and least retrofittable.
- **Alerts** — page on the **symptom the user feels** (error rate, latency, SLO burn), never on a bare cause (CPU, one host). *If this paged at 3am, is it worth waking someone — and does it tell them what the user is experiencing?* Reference SLO / error-budget burn for framing; this skill does not define the SLO.

Close by **checking the footguns off** explicitly: cardinality bounded, IDs threaded, no PII/secrets, alerts symptom-framed, no hot-path spam, RED/USE complete for the in-scope paths and resources. An unchecked footgun is the finding.

## Modes and scope

- **Applied vs advisory follows the invocation.** On a live diff or during implementation, author the instrumentation as concrete edits. On existing code or in a review, deliver recommendations for a human. Default to the mode the context implies; when genuinely ambiguous, ask once.
- **Applied mode does not dissolve the judgment.** When you author edits, surface each non-obvious choice — the cardinality allowlist, which alerts are page-worthy, any hot-path sampling — as a flagged inline decision, not a default silently baked in. The forcing questions become visible judgment calls in the diff; they do not disappear into boilerplate.
- **One target.** Default scope is one service, one handler, or one diff. Invoked on a whole repo, narrow to the highest-traffic / highest-risk entry points and *say so* — this is a forcing pass, not an audit. A scored repo-wide instrumentation backlog is `tech-debt-scan`'s job.

## Proof boundary

This skill authors the signals; it cannot confirm they actually emit, scrape, or render in production — that is a live-signal read (`deploy-plan` / `outcome-check`), and an AI agent usually cannot do it. State plainly what was instrumented and what stays unverified until the telemetry is seen flowing: *"added the correlation-ID middleware and the RED metrics; not confirmed they reach the dashboard."* Do not claim observability is *working* from the fact that it was *written*. This is the library-wide evidence-before-claims floor specialized to the author-don't-observe surface; the skill obeys it, it does not own it.

## Fences

- **vs `diagnose`.** Proactive vs reactive. This lays signals down before the bug; `diagnose` consumes them — or their absence — to find a cause. A "we have no signal here" gap surfaced mid-diagnosis can route back to this skill afterward.
- **vs `deploy-plan` / `outcome-check`.** Both *read* signals that already exist — `deploy-plan` for one ship's health gauge, `outcome-check` for whether a goal moved. This *creates* the signals they read; it sets no go/no-go and reads no live metric.
- **vs `incident-response`.** It fights the fire with whatever telemetry exists; this skill is *why* that telemetry exists. Inverse time direction.
- **vs `runbook-authoring`.** That authors the human *response* to an alert; this authors the *alert and the signal beneath it*.
- **vs `system-design-review` / `tech-debt-scan`.** They flag that instrumentation is missing or thin; this does the authoring. A review finding "no observability here" is a valid trigger for this skill.

## Done when

- The stack/backend is confirmed, and the pass covers the concerns the target warrants (logs, metrics, traces, alerts — only those it needs), each posed as a per-system judgment rather than filled in with boilerplate.
- Every footgun is explicitly checked: cardinality bounded, correlation/trace IDs threaded, no PII/secrets in logs, alerts symptom-framed and page-worthy, no hot-path spam, RED/USE complete for the in-scope paths and resources.
- The output is delivered in the mode the invocation implies (applied edits or recommendations), with the proof boundary stated — what was instrumented, and what stays unverified until it is seen flowing.
- When the instrumented change ships as a risky rollout, hand forward to `/deploy-plan` (or `$deploy-plan`) — the signals just laid down are the gauge it pre-registers and reads.

## Build-and-prune note

Thin in this authoring repo; the value is **portable** to backend, service, distributed-system, and data-pipeline repos, where these footguns recur and land their cost months later. Watch it fire on real instrumentation work; prune without ceremony if it never earns more than "add some logging." Never let it accrete into a multi-backend best-practices encyclopedia — the moment it stops being a tight forcing pass over one target, it has become the reference it was built not to be.
