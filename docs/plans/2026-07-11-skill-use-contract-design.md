# Skill-Use Contract + Composition Data Layer — Design

Status: patched per the 2026-07-11 scrutiny review (verdict: Patch Before Implementation; all seven required changes applied below), awaiting JP's design approval. This document is also the durable evidence artifact the charter Admission will cite (review change #5 / M3).

## Problem

Two observed failure modes in how Claude Code and Codex leverage the global skill library (~90 skills served from `~/.agents`):

- **Silence** — no skill invoked when one fits the task. Observed repeatedly by JP across sessions (specific instances unrecorded); notably, on the Claude side these failures happened *with* the harness's own skill-matching instruction loaded (see Premise, below).
- **Missed composition** — a single skill invoked when a sequence or parallel combination would serve better. One directly observed case plus seven never-observed-leveraged sequences, inventoried below.

Non-goals: routing speed; rival-vs-rival misrouting (never observed). Constraints fixed during shaping: the mechanism must be ambient/always-loaded (silence cannot be fixed by anything the agent must remember to invoke — a router skill is ruled out) and must reach both runtimes. Bar: highest plausibility of success, not formal verification. Accepted trades: every-turn context cost in both runtimes, and the charter gate for always-loaded contracts.

## Evidence Inventory (the durable record)

The composition sequences JP has never observed leveraged, with the per-chain status of existing routing data at design time:

1. `diagnose` → `tdd` → `keep-green` — the `diagnose`→`tdd` edge **already exists** in `diagnose`'s description ("once the cause is known, locking the fix in test-first belongs to `tdd`") and has never fired; `tdd`→`keep-green` has no edge.
2. `test-trust-audit` → `characterization-tests` → `simplify-code` — `characterization-tests` names `test-trust-audit` only as a non-use boundary; no forward exits anywhere in the chain.
3. `contract-change-propagation` → `migration-campaign` — mutual exclusion boundaries exist in both descriptions; no forward handoff.
4. `red-team` → `authorization-design` + `injection-safe-inputs` (parallel fan-out) — the two design skills name `red-team` as a non-route; `red-team` has no forward fan-out to either.
5. `incident-response` → `diagnose` → `postmortem` → `runbook-authoring` — `incident-response`'s description **already names** the `diagnose` and `postmortem` handoffs and the chain has never been observed; `postmortem`→`runbook-authoring` has no edge.
6. `observability-instrumentation` → `deploy-plan` → `outcome-check` — descriptions cross-reference only as contrasts ("not for..."); no forward exits.
7. `skill-squad` → `scrutinize-skill` → `behavior-smoke-test` → `skill-benchmark` — non-route mentions only; no forward chain. Mixes Claude-only (`skill-squad`, `skill-benchmark`) and dual-runtime skills.
8. Observed case: `making-recommendations` fired alone on a wide-solution-space recommendation ask; its description names `outcome-shaping` and `design-exploration` for the no-options case but **lacks the thin-field → `ideate` edge**; `ideate` names `making-recommendations` only as an exclusion.

Corroborating facts verified first-hand during the 2026-07-11 scrutiny pass: all data-layer target skills exist in the roster; the `diagnose`→`tdd` never-fired claim holds; `work-router` has zero fires in the entire usage ledger (4,276 records) and its own text disclaims ambient wrapping ("Do not use this skill as a silent wrapper around every ambiguous request"); no live skill routes to `work-router` (grep: historical docs/plans mentions and its own files only); `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` are plain files, not under version control.

**The decisive inference:** chains 1 and 5 have edges in the descriptions that never fire — data alone does not produce composition. And the Claude harness's own skill-matching instruction was loaded during the observed silence failures — a bundled request-time push alone does not prevent silence. Neither layer works alone; the design pairs a procedure (ambient contract) with data (exits in skill bodies).

## Premise (honest headwind, named)

On the Claude runtime, the harness system prompt already carries a strong request-time skill-matching instruction ("when a skill matches the user's request... BLOCKING REQUIREMENT: invoke the relevant Skill tool BEFORE..."), and the observed silence failures happened with that text loaded. So "more ambient instruction → more invocation" is not self-evident for the start-of-work check; it is precisely the open question the pre-landing probes must answer differentially. The seam-handoff and composition obligations (bullets 2–3) have no existing owner in either runtime and face no such headwind. On Codex, no equivalent bundled terrain exists at all.

## Design

### 1. The contract (procedure layer)

A byte-identical `## Skill Use` section in both `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`. Draft — final wording passes the `agent-facing-design` gate and a `writing-principles` pass at build (flag for that pass: confirm "in parallel" cannot be read as license for unrequested multi-agent fan-out, which stays user-opt-in):

> ## Skill Use
>
> - Before starting substantive work — and when a mid-task finding changes what the work needs — check whether an available skill owns it; when one plausibly fits, invoke it rather than improvising the same job unaided. Skipping a fitting skill is the failure mode. Trivial or purely conversational turns need no check, and the check is silent — don't narrate it.
> - When an invoked skill completes and names a follow-on lane — an exit, handoff, or next-step pointer — take it, or offer it explicitly; don't drop the chain and improvise the next step.
> - When a task or its findings span more than one skill's job, compose them — in sequence or in parallel — rather than stretching one skill past its boundary.
> - A governing skill's explicit stop, containment, or sequencing instruction overrides these defaults, and delegated agents follow their brief.

Design choices: "plausibly fits" sets the invocation threshold deliberately low (the failure is silence, not misrouting); the trivial-turn carve-out and silent check are the over-firing guards; "take it, or offer it" lets time-separated chains surface as offers; the mid-task clause makes the contract's owned moment explicit (request-time matching on Claude stays fixed-terrain's job — see Admission); the final bullet is the governing-skill precedence clause (review H2 — the same clause class the Markdown auto-commit default needed retrofitted after a verified live contradiction, 2026-07-02 ledger amendment 2) plus the delegated-agent scoping (review M2).

### 2. The data layer (exits in bodies, edges in descriptions)

Forward handoffs land in skill **bodies** as exits (the `outcome-shaping` Exits-table pattern, `SKILL.md:78`); **descriptions** change only where selection-critical, per the existing frontmatter convention. Touched skills, from the eight sequences: `diagnose`, `tdd`, `test-trust-audit`, `characterization-tests`, `contract-change-propagation`, `red-team` (parallel fan-out), `incident-response`, `postmortem`, `observability-instrumentation`, `deploy-plan`, `ideate`, `skill-squad`, `behavior-smoke-test`, `scrutinize-skill`; description edit for `making-recommendations` (thin-field → `ideate`). Special cases: `scrutinize-skill` is plugin-distributed (`review-family`) — Class-B publish path (version bump → Codex republish → mirror) on JP's ask; chain-7 exits naming Claude-only skills get availability-conditional phrasing. These edits are build-and-prune, not charter events.

### 3. The convention (repo `AGENTS.md`, Skill Editing section)

One line, roughly: when a skill's work has a natural upstream or downstream lane, name the handoff in the body — an exits line or section, availability-conditional for single-runtime lanes — and add it to the description only when selection-critical. Repo-local always-loaded edit; rides the same Admission package. Scope note for the admission: this is editing guidance about *where* handoffs live; `agent-facing-design` keeps the routing-design judgment job untouched.

## Charter Package

One Admission run covering the contract and the convention line; one ledger entry in `contract-decisions.md`.

**Q1 — closest existing contract (review H1):** On the Claude runtime, the closest contract is the harness's own fixed-terrain skill-matching instruction (runtime-bundled; counts as an owner per charter.md:9). The delta the admission argues: the fixed-terrain instruction covers only request-time matching of the user's request and demonstrably under-delivers (observed silence with it loaded); this contract owns the moments it does not reach — mid-task fit checks, seam handoffs at skill completion, and composition across skills — and on Codex, where no equivalent terrain exists, the whole job. The collision with fixed terrain resolves on the local side by that scoping: request-time matching on Claude stays the harness's job; the contract's bullet 1 owns mid-task and finding-time checks. `work-router` is *not* the closest contract and never owned this job (zero ledger fires; its own text disclaims ambient wrapping); its retirement is an incidental build-and-prune cut, noted in passing, not the One-Owner resolution.

**Q2 — what failure, that lighter context wouldn't prevent:** the observed silence failures and eight never-leveraged sequences; this *is* the lightest ambient form (an instruction-file section), and two chains prove description-level data alone does not fire.

**Q3 — houses standards:** the contract states plainly what an agent must do, carries its own carve-outs and precedence clause, and is runtime-neutral.

**Subagent exposure (review M2), priced and accepted:** user-global instruction files are injected into subagent contexts, so the contract binds Explore workers, workflow agents, and future eval control arms; the delegated-agents clause scopes narrowly-tasked delegation to its brief, the residual exposure is named here for the admission, watched via the usage ledger (which captures subagent fires) — and pre-registered evaluations in this repo must account for the ambient contract when defining control baselines.

**Durability:** the canonical contract text lives as `CANON` in a new drift-check script (`check-protected-set.sh` pattern) checking both global files byte-identically, wired into the SessionStart canary family; this committed design doc is the admission's evidence pointer for the observed failures and sequence analysis (review M3).

## Proof Plan (pre-landing probes)

Pattern: `docs/agents/contract-evaluation-methodology.md` (pre-register/seal, single-variable differential) — the prior plugin admissions were single-arm forward tests and are *not* the precedent here (review M1). Spec:

- **Arms:** with-contract vs. without-contract. Text delivery: the contract block embedded inside a realistic full user-global instruction file replica, not as a standalone or prompt-subject instruction. Named bound: any injection overstates salience relative to true ambient placement; the differential between arms, not absolute rates, is the measure — especially for the silence probe, where the Claude harness instruction pushes both arms toward invocation.
- **Trials:** minimum 3 per arm per probe, fresh subagent each trial.
- **Probes:** (1) *silence* — a task a skill clearly owns, never named (e.g. "this untested legacy module needs to be made safe before I refactor" → `characterization-tests`), including at least one mid-task variant since that is the moment the contract claims to own; (2) *seam* — agent handed a just-found bug cause: does `tdd` get taken or offered? (3) *parallel* — findings spanning authz + untrusted input: do both design skills get taken or offered?
- **Pass criteria, pre-registered before any trial runs:** per probe, the with-arm invokes-or-offers the target lane in ≥2/3 trials AND strictly exceeds the without-arm's count. Criteria are sealed in the build plan before the first trial; no post-hoc adjustment.
- **Honest bound:** probes exercise Claude-side behavior; Codex rides the identical text plus the live watch.

## Risks Owned

- **Over-firing** — the contract pushes toward invocation; misrouting is a failure JP does not currently have. Guards: the carve-out, "plausibly," the silent check, the precedence clause. Detector: the watch (below). Wording is tunable post-landing without re-admission.
- **Subagent exposure** — priced in the Charter Package above.
- **Ambient cost** — ~140 words per session in both runtimes (grew from ~117 with the H2/M2 clauses); accepted in shaping, re-priced here.
- **Drift between the twin global files** — the canary script. Pre-existing, unrelated drift already exists between the two files' `## Behavior Contracts` sections; filed via `/triage` at build, not folded into this design.

## Build Order

1. Working branch in `.agents`; this design doc committed (durable evidence in place before the ledger entry cites it).
2. Final contract wording through `agent-facing-design` + `writing-principles` (with the "parallel" flag).
3. Pre-register probe pass criteria; run the three probes, 3+ trials per arm; record results.
4. **Charter Admission consult run and JP ratification recorded (GO/NO-GO) — before any global-file edit** (review M4; consult-before-event per charter.md:3, precedent: the 2026-07-08 §7.1 GO).
5. Land the `## Skill Use` block in both global files + the canary script wired into the SessionStart family.
6. Seed the data layer (Class A in place; `scrutinize-skill` Class B deferred to JP's publish ask). Convention line in repo `AGENTS.md`.
7. Retire `work-router` (build-and-prune cut; rewire the nil live inbound routes — grep re-run at build to confirm still nil).
8. Ledger entry in `contract-decisions.md` citing this doc + commits + probe records.
9. File the pre-existing global-file `## Behavior Contracts` drift via `/triage`.
10. Validation ladder: frontmatter parses on every edited skill, `check-library-integrity.sh`, `claude-skills-sync.sh --check`, new canary green, `git diff --check`.
11. **Watch, with a checkpoint:** read at the 2026-08-01 ledger re-read. Pre-named trigger: unwanted fires of expensive-by-design lanes (`skill-squad`, `methodology-critique`, `synapsis`, `deep-research`) — "plausibly fits" lowers the threshold across those too. Also watched: seam-handoff sequences appearing in the ledger; JP corrections.

## Review Disposition (2026-07-11 scrutiny)

Verdict was Patch Before Implementation with seven required changes, all applied: (1) H1 admission rewritten around the fixed-terrain harness instruction, `work-router` demoted to incidental cut; (2) H2 governing-skill precedence clause added to the contract; (3) M1 probes re-cited to `contract-evaluation-methodology.md` with arms, trials, delivery mechanism, and sealed pass criteria specified; (4) M2 subagent exposure scoped in-text and priced in the admission; (5) M3 this doc committed as the durable evidence artifact; (6) M4 charter consult + JP ratification inserted before global-file edits; (7) watch pinned to 2026-08-01 with the expensive-lane trigger named. Low findings absorbed: pre-existing global-file drift routed to `/triage` (build step 9); convention-line scope sentence added to the Charter Package; the "parallel" wording flag attached to the writing pass.
