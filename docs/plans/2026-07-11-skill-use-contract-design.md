# Skill-Use Contract + Composition Data Layer — Design

Status: patched per the first 2026-07-11 scrutiny review (seven changes) and the second 2026-07-11 review as adjudicated by `review-reviewer` (six changes plus two refinements; see Review Disposition), awaiting JP's design approval. This document is also the durable evidence artifact the charter Admission will cite.

## Problem

Two observed failure modes in how Claude Code and Codex leverage the global skill library (~90 skills served from `~/.agents`):

- **Silence** — no skill invoked when one fits the task. Observed repeatedly by JP across sessions (specific instances unrecorded); notably, on the Claude side these failures happened *with* the harness's own skill-matching instruction loaded (see Premise, below).
- **Missed composition** — a single skill invoked when a sequence or parallel combination would serve better. One directly observed case plus seven never-observed-leveraged sequences, inventoried below.

Non-goals: routing speed; rival-vs-rival misrouting (never observed). Constraints fixed during shaping: the mechanism must be ambient/always-loaded (silence cannot be fixed by anything the agent must remember to invoke — a router skill is ruled out) and must reach both runtimes. Bar: highest plausibility of success, not formal verification. Accepted trades: every-turn context cost in both runtimes, and the charter gate for always-loaded contracts.

## Evidence Inventory (the durable record)

The composition sequences JP has never observed leveraged, with the per-chain status of existing routing data at design time:

1. `diagnose` → `tdd` → `keep-green` — the `diagnose`→`tdd` edge **already exists** in `diagnose`'s description ("once the cause is known, locking the fix in test-first belongs to `tdd`") and has never fired — though `diagnose` itself has zero ledger records, so the edge has had no recorded opportunity; `tdd`→`keep-green` has no edge.
2. `test-trust-audit` → `characterization-tests` → `simplify-code` — `characterization-tests` names `test-trust-audit` only as a non-use boundary; no forward exits anywhere in the chain.
3. `contract-change-propagation` → `migration-campaign` — one-directional boundary only: `migration-campaign`'s description names `contract-change-propagation`, while `contract-change-propagation`'s description carves out the rollout job ("apply the rollout across many sites") without naming `migration-campaign`; no forward handoff.
4. `red-team` → `authorization-design` + `injection-safe-inputs` (parallel fan-out) — `authorization-design`'s description names `red-team` as a non-route; `injection-safe-inputs`'s description does not mention it, but its body already names this composition (`SKILL.md:67`: "red-team's attack paths make excellent must-block rows") — existing compose data in a skill too new to have any ledger fires; `red-team` has no forward fan-out to either.
5. `incident-response` → `diagnose` → `postmortem` → `runbook-authoring` — `incident-response`'s description **already names** the `diagnose` and `postmortem` handoffs and the chain has never been observed — though `incident-response` and `postmortem` both have zero ledger records, so these edges have had no recorded opportunities; `postmortem`→`runbook-authoring` has no edge.
6. `observability-instrumentation` → `deploy-plan` → `outcome-check` — descriptions cross-reference only as contrasts ("not for..."); no forward exits.
7. `skill-squad` → `scrutinize-skill` → `behavior-smoke-test` → `skill-benchmark` — non-route mentions only; no forward chain. Mixes Claude-only (`skill-squad`, `skill-benchmark`) and dual-runtime skills.
8. Observed case: `making-recommendations` fired alone on a wide-solution-space recommendation ask; its description names `outcome-shaping` and `design-exploration` for the no-options case but **lacks the thin-field → `ideate` edge**; `ideate` names `making-recommendations` only as an exclusion.

Corroborating facts verified first-hand during the 2026-07-11 scrutiny pass: all data-layer target skills exist in the roster; the `diagnose`→`tdd` never-fired claim holds; `work-router` has zero fires in the entire usage ledger (4,276 records) and its own text disclaims ambient wrapping ("Do not use this skill as a silent wrapper around every ambiguous request"); no live skill routes to `work-router` (grep: historical docs/plans mentions and its own files only); `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` are plain files, not under version control. Re-verified in the 2026-07-11 adjudication recompute: the ledger's aggregate source split is 3,686 user-initiated vs 590 model-initiated; `making-recommendations` has 241 records (15 model-initiated) across 121 sessions while `outcome-shaping`, `design-exploration`, and `ideate` total 7, 20, and 5 records; `diagnose`, `incident-response`, `postmortem`, and `keep-green` each have zero records; 47 records carry `sidechain: true`.

**The decisive inference, grounded in the ledger:** the fired-source specimen is `making-recommendations` — 241 ledger records across 121 sessions (only 15 model-initiated), while the neighbors its own description names barely fire at all (`outcome-shaping` 7, `design-exploration` 20, `ideate` 5 records; none appear among its top co-fired skills). A heavily fired skill whose description-named edges are almost never taken is direct evidence that description-level data alone does not reliably produce composition. (Chains 1 and 5 above also carry never-fired edges, but their source skills have zero ledger records — zero opportunities — so they illustrate the gap without proving it.) And the Claude harness's own skill-matching instruction was loaded during the observed silence failures — a bundled request-time push alone does not prevent silence. Neither layer suffices alone; the design pairs a procedure (ambient contract) with data (exits in skill bodies).

## Premise (honest headwind, named)

On the Claude runtime, the harness system prompt already carries a strong request-time skill-matching instruction ("when a skill matches the user's request... BLOCKING REQUIREMENT: invoke the relevant Skill tool BEFORE..."), and the observed silence failures happened with that text loaded. So "more ambient instruction → more invocation" is not self-evident for the start-of-work check; it is precisely the open question the pre-landing probes must answer differentially. The seam-handoff and composition obligations (bullets 2–3) have no existing owner in either runtime and face no such headwind. On Codex, no equivalent bundled terrain exists at all. Ledger context for the same point: fires are 86% user-initiated in aggregate (3,686 user vs 590 model of 4,276 records), but the split varies sharply by skill — `tdd` fires 23/25 model-initiated — so model-initiated invocation is demonstrably possible; the failure is its rarity and unevenness, not impossibility.

## Design

### 1. The contract (procedure layer)

A byte-identical `## Skill Use` section in both `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`. Draft — final wording passes the `agent-facing-design` gate and a `writing-principles` pass at build (flag for that pass: confirm "in parallel" cannot be read as license for unrequested multi-agent fan-out, which stays user-opt-in):

> ## Skill Use
>
> - Before starting substantive work — and when a mid-task finding changes what the work needs — check whether an available skill owns it; when one plausibly fits, invoke it rather than improvising the same job unaided. Skipping a fitting skill is the failure mode. Trivial or purely conversational turns need no check, and the check is silent — don't narrate it.
> - When an invoked skill completes and names a follow-on lane — an exit, handoff, or next-step pointer — take it, or offer it explicitly; don't drop the chain and improvise the next step.
> - When a task or its findings span more than one skill's job, compose them — in sequence or in parallel — rather than stretching one skill past its boundary.
> - A governing skill's explicit stop, containment, or sequencing instruction overrides these defaults, and delegated agents follow their brief.

Design choices: "plausibly fits" sets the invocation threshold deliberately low (the failure is silence, not misrouting); the trivial-turn carve-out and silent check are the over-firing guards; "take it, or offer it" lets time-separated chains surface as offers; the mid-task clause names the moment the contract uniquely claims on Claude, while at request time bullet 1 deliberately overlaps the harness's fixed-terrain instruction as reinforcement — an overlap the Admission presents openly for the consult to accept or reject (see Charter Package); the final bullet is the governing-skill precedence clause (review H2 — the same clause class the Markdown auto-commit default needed retrofitted after a verified live contradiction, 2026-07-02 ledger amendment 2) plus the delegated-agent scoping (review M2).

### 2. The data layer (exits in bodies, edges in descriptions)

Forward handoffs land in skill **bodies** as exits (the `outcome-shaping` Exits-table pattern, `SKILL.md:78`); **descriptions** change only where selection-critical, per the existing frontmatter convention. Touched skills, from the eight sequences: `diagnose`, `tdd`, `test-trust-audit`, `characterization-tests`, `contract-change-propagation`, `red-team` (parallel fan-out), `incident-response`, `postmortem`, `observability-instrumentation`, `deploy-plan`, `ideate`, `skill-squad`, `behavior-smoke-test`, `scrutinize-skill`; description edit for `making-recommendations` (thin-field → `ideate`). Special cases: `scrutinize-skill` is plugin-distributed (`review-family`) — Class-B publish path (version bump → Codex republish → mirror) on JP's ask; chain-7 exits naming Claude-only skills get availability-conditional phrasing. These edits are build-and-prune, not charter events.

### 3. The convention (repo `AGENTS.md`, Skill Editing section)

One line, roughly: when a skill's work has a natural upstream or downstream lane, name the handoff in the body — an exits line or section, availability-conditional for single-runtime lanes — and add it to the description only when selection-critical. Repo-local always-loaded edit; rides the same Admission package. Scope note for the admission: this is editing guidance about *where* handoffs live; `agent-facing-design` keeps the routing-design judgment job untouched.

## Charter Package

One Admission run covering the contract and the convention line; one ledger entry in `contract-decisions.md`.

**Q1 — closest existing contract (review H1):** On the Claude runtime, the closest contract is the harness's own fixed-terrain skill-matching instruction (runtime-bundled; counts as an owner per charter.md:9). The delta the admission argues: the fixed-terrain instruction covers only request-time matching of the user's request and demonstrably under-delivers (observed silence with it loaded); this contract owns the moments it does not reach — mid-task fit checks, seam handoffs at skill completion, and composition across skills — and on Codex, where no equivalent terrain exists, the whole job. At request time on Claude, bullet 1's text deliberately overlaps the fixed-terrain instruction rather than scoping around it — byte-identity across the two global files is what the drift canary checks, and on Codex the same clause is the sole owner of that moment. One Owner (charter.md:30) treats a broader-recall restatement as the same job, and charter.md:9 resolves fixed-terrain collisions on the local side, so the admission presents this overlap openly as deliberate reinforcement of an instruction that demonstrably under-delivers, for the consult to accept or reject; the named fallback if rejected is runtime-divergent text (the Claude copy scoped to mid-task and finding-time checks), at the cost of the byte-identical canary. `work-router` is *not* the closest contract and never owned this job (zero ledger fires; its own text disclaims ambient wrapping); its retirement is an incidental build-and-prune cut, noted in passing, not the One-Owner resolution.

**Q2 — what failure, that lighter context wouldn't prevent:** the observed silence failures and eight never-leveraged sequences; this *is* the lightest ambient form (an instruction-file section), and the fired-source ledger specimen (`making-recommendations`, Evidence Inventory) shows description-named edges going untaken at scale — description-level data alone does not reliably fire.

**Q3 — houses standards:** the contract states plainly what an agent must do, carries its own carve-outs and precedence clause, and is runtime-neutral.

**Subagent exposure (review M2), priced and accepted:** user-global instruction files load into most subagent contexts — general-purpose, custom, and workflow agents; the built-in Explore and Plan agents are the documented exceptions and skip CLAUDE.md entirely (sub-agents doc, "What loads at startup") — so the contract binds those delegated workers and any eval control arms run through them; the delegated-agents clause scopes narrowly-tasked delegation to its brief, the residual exposure is named here for the admission and watched via the usage ledger, which demonstrably captures subagent fires (47 `sidechain: true` records at design time) — and pre-registered evaluations in this repo must account for the ambient contract when defining control baselines.

**Durability:** the canonical contract text lives as `CANON` in a new drift-check script (`check-protected-set.sh` pattern) checking both global files byte-identically, wired into the SessionStart canary family; this committed design doc is the admission's evidence pointer for the observed failures and sequence analysis (review M3).

## Proof Plan (pre-landing probes)

Pattern: `docs/agents/contract-evaluation-methodology.md` (moves 1, 2, 3, and 6 — seal-by-commit, single-variable differential, replication with escalation, pilot-before-seal) — the prior plugin admissions were single-arm forward tests and are *not* the precedent here (review M1). Spec:

- **Delivery, hermetic:** each trial is a `claude -p` subprocess with a scratch config dir (`CLAUDE_CONFIG_DIR`) — the `skill-benchmark` pattern: a subprocess is the only way to control what loads, and it prevents the live `~/.claude/CLAUDE.md` double-loading beneath a prompt-embedded replica (non-Explore/Plan contexts auto-load user memory). Task prompts are fixed and pre-written, identical across arms — no invested parent composing delegation prompts.
- **Arms, single-variable:** the with-arm's config carries a realistic user-global instruction file replica containing the contract block; the without-arm carries the byte-identical replica minus the block. Both arms retain the harness's own skill-matching instruction (it ships with the runtime), which is the true Claude baseline. The differential between arms, not absolute rates, is the measure.
- **Trials and escalation:** 3 per arm per probe. If the arms differ by exactly one trial, extend both arms to 5 before reading the probe (move 3's split escalation).
- **Pilot and ceiling rule:** before sealing, run a cheap unsealed base-rate pilot on the silence probe's without-arm (move 6: does the baseline already ceiling?). Sealed ceiling rule: a probe whose without-arm passes every trial reads **inconclusive-by-ceiling** — distinct from fail, counting neither for nor against.
- **Probes:** (1) *silence, centered on the mid-task moment* — the primary shape is the moment the contract uniquely claims on Claude: the agent is midway through work when a finding changes what the work needs (e.g. discovers an untested legacy module that must be made safe before the refactor → `characterization-tests`); a request-time variant runs as a secondary read informing the fixed-terrain reinforcement argument. (2) *seam* — agent handed a just-found bug cause: does `tdd` get taken or offered? (3) *parallel* — findings spanning authz + untrusted input: do both design skills get taken or offered?
- **Pass criteria (per probe):** the with-arm takes-or-offers the target lane in ≥2/3 trials AND strictly exceeds the without-arm's count (post-escalation counts), subject to the ceiling rule.
- **Aggregation rule (sealed with the rest):** GO for the full block requires the seam and parallel probes to pass and the silence probe to pass or read inconclusive-by-ceiling. A true silence-probe fail (no ceiling) returns bullet 1 for redesign while bullets 2–4 may proceed; a seam or parallel fail is NO-GO for the block — revise and re-run.
- **Seal:** the full pre-registration — tasks, arms, trials, escalation, ceiling, pass criteria, aggregation — is committed before the first sealed trial; the commit SHA is the seal (move 1). No post-hoc adjustment.
- **Honest bound:** probes exercise Claude-side behavior; Codex rides the identical text plus the live watch.

## Risks Owned

- **Over-firing** — the contract pushes toward invocation; misrouting is a failure JP does not currently have. Guards: the carve-out, "plausibly," the silent check, the precedence clause. Detector: the watch (below). Wording is tunable post-landing without re-admission.
- **Subagent exposure** — priced in the Charter Package above.
- **Ambient cost** — 145 words (measured) per session in both runtimes (grew from ~117 with the H2/M2 clauses); accepted in shaping, re-priced here.
- **Drift between the twin global files** — the canary script. Pre-existing drift already exists between the two files' `## Behavior Contracts` sections — `~/.codex/AGENTS.md` is missing the capability carve-out clause entirely, a live demonstration of exactly the drift class the canary prevents; filed via `/triage` at build with that clause named, not folded into this design.

## Build Order

1. Working branch in `.agents`; this design doc committed (durable evidence in place before the ledger entry cites it).
2. Final contract wording through `agent-facing-design` + `writing-principles` (with the "parallel" flag).
3. Commit the probe pre-registration (the SHA is the seal); run the unsealed base-rate pilot, then the three probes hermetically per the Proof Plan; record results.
4. **Charter Admission consult run and JP ratification recorded (GO/NO-GO) — before any global-file edit** (review M4; consult-before-event per charter.md:3, precedent: the 2026-07-08 §7.1 GO).
5. Land the `## Skill Use` block in both global files + the canary script wired into the SessionStart family.
6. Seed the data layer (Class A in place; `scrutinize-skill` Class B deferred to JP's publish ask). Convention line in repo `AGENTS.md`.
7. Retire `work-router` (build-and-prune cut; rewire the nil live inbound routes — grep re-run at build to confirm still nil).
8. Ledger entry in `contract-decisions.md` citing this doc + commits + probe records.
9. File the pre-existing global-file `## Behavior Contracts` drift via `/triage`, naming specifically that `~/.codex/AGENTS.md` is missing the capability carve-out clause.
10. Validation ladder: frontmatter parses on every edited skill, `check-library-integrity.sh`, `claude-skills-sync.sh --check`, new canary green, `git diff --check`.
11. **Watch, with a checkpoint:** read at the 2026-08-01 ledger re-read. Pre-named trigger: unwanted fires of expensive-by-design lanes (`skill-squad`, `methodology-critique`, `synapsis`, `deep-research`) — "plausibly fits" lowers the threshold across those too. Also watched: seam-handoff sequences appearing in the ledger; JP corrections.

## Review Disposition (2026-07-11 scrutiny)

Verdict was Patch Before Implementation with seven required changes, all applied: (1) H1 admission rewritten around the fixed-terrain harness instruction, `work-router` demoted to incidental cut; (2) H2 governing-skill precedence clause added to the contract; (3) M1 probes re-cited to `contract-evaluation-methodology.md` with arms, trials, delivery mechanism, and sealed pass criteria specified; (4) M2 subagent exposure scoped in-text and priced in the admission; (5) M3 this doc committed as the durable evidence artifact; (6) M4 charter consult + JP ratification inserted before global-file edits; (7) watch pinned to 2026-08-01 with the expensive-lane trigger named. Low findings absorbed: pre-existing global-file drift routed to `/triage` (build step 9); convention-line scope sentence added to the Charter Package; the "parallel" wording flag attached to the writing pass.

A second 2026-07-11 review (execution-readiness pass on this doc at `1203ac1`) was adjudicated via `review-reviewer` — the review judged `reliable`, all six required changes confirmed against recomputed evidence — and applied: (1) the decisive inference re-grounded on the fired-source ledger specimen (`making-recommendations`), zero-opportunity chains demoted to illustration; (2) the Q1 request-time overlap now openly adjudicated as fixed-terrain reinforcement with a named fallback, and the silence probe re-centered on the mid-task moment; (3) the probe spec patched — symmetric without-arm replica, hermetic `claude -p` delivery, base-rate pilot plus sealed ceiling rule, sealed aggregation rule, and (adjudication refinement) a split-escalation rule; (4) subagent exposure corrected per the official sub-agents doc (Explore/Plan skip user memory) and, per the adjudication, the ledger's 47 sidechain-tagged records cited as capture evidence in place of the review's "unproven" caveat; (5) the chain-3 and chain-4 inventory claims fixed and the `injection-safe-inputs:67` compose edge added; (6) seal-by-commit made explicit in the build order and the `/triage` filing scoped to name the missing capability carve-out. Second adjudication refinement folded: the per-skill variance line in the Premise.
