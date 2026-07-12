# Skill-Use Contract + Composition Data Layer — Design

Status: patched per three 2026-07-11 review rounds, including two `review-reviewer` adjudications; the latest patch narrows the shared contract to mid-task checks, handoffs, and composition and repairs the proof design (see Review Disposition). Awaiting JP's design approval. This document is also the durable evidence artifact the charter Admission will cite.

## Problem

Two observed failure modes in how Claude Code and Codex leverage the global skill library (~90 skills served from `~/.agents`):

- **Silence** — no skill invoked when one fits the task. Observed repeatedly by JP across sessions (specific instances unrecorded); notably, on the Claude side these failures happened *with* the harness's own skill-matching instruction loaded (see Premise, below).
- **Missed composition** — a single skill invoked when a sequence or parallel combination would serve better. One directly observed case plus seven never-observed-leveraged sequences, inventoried below.

Non-goals: request-time skill matching, which is fixed runtime terrain; routing speed; rival-vs-rival misrouting (never observed). Constraints fixed during shaping: the mechanism must be ambient/always-loaded for the moments it owns (mid-task re-checks, handoffs, and composition) and must reach both runtimes. Bar: highest plausibility of success, not formal verification. Accepted trades: every-turn context cost in both runtimes, and the charter gate for always-loaded contracts.

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

Corroborating facts verified first-hand during the 2026-07-11 scrutiny pass: all data-layer target skills exist in the roster; the `diagnose`→`tdd` never-fired claim holds; `work-router` owns explicit routing questions and disclaims ambient wrapping ("Do not use this skill as a silent wrapper around every ambiguous request"); `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` are plain files, not under version control. Re-verified in the 2026-07-11 adjudication recompute: the ledger's aggregate source split is 3,686 user-initiated vs 590 model-initiated; `making-recommendations` has 241 records (15 model-initiated) across 121 sessions while `outcome-shaping`, `design-exploration`, and `ideate` total 7, 20, and 5 records; `diagnose`, `incident-response`, `postmortem`, and `keep-green` each have zero records; 47 records carry `sidechain: true`.

**The bounded hypothesis the ledger motivates:** the fired-source specimen is `making-recommendations` — 241 ledger records across 121 sessions (only 15 model-initiated), while nearby lanes fire much less often (`outcome-shaping` 7, `design-exploration` 20, `ideate` 5 records). The ledger records invocations, not semantically eligible handoff opportunities, and `making-recommendations` already names the thin-field `ideate` handoff in its body; five ledger sessions contain both skills. Those aggregates therefore do not prove missed composition. One directly observed missed-composition case plus the aggregate pattern justify a prospective experiment, while chains whose source skill has zero records illustrate candidate edges without supplying opportunity evidence. The design pairs a procedure (ambient contract) with data (exits in skill bodies), and Admission weight stays bounded to what the probes establish.

## Premise (honest headwind, named)

Both runtimes carry request-time skill-matching terrain at design time: Claude's harness system prompt has a blocking request-time matching instruction, and the current Codex runtime requires use of an available matching skill. The local contract therefore does not restate or reinforce request-time matching. It owns the moments that terrain does not: a finding changes the needed work mid-task, an invoked skill reaches a named handoff, or one task spans multiple skill jobs. Ledger context: fires are 86% user-initiated in the 4,276-record review snapshot (3,686 user vs 590 model), but the split varies sharply by skill — `tdd` fires 23/25 model-initiated — so model-initiated invocation is possible; the open question is whether the local mid-task/handoff/composition obligations materially improve followership.

## Design

### 1. The contract (procedure layer)

A byte-identical `## Skill Use` section in both `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`. This draft has passed the current `agent-facing-design` and `writing-principles` gates; re-run them if later review changes the obligations:

> ## Skill Use
>
> - When a mid-task finding changes what the work needs, re-check whether an available skill owns the newly revealed work; when one plausibly fits, invoke it rather than improvising the same job unaided. The check is silent — don't narrate it.
> - When an invoked skill completes and names a follow-on lane — an exit, handoff, or next-step pointer — take it only when the current request and governing skill authorize continuation; otherwise offer it explicitly. Don't drop the chain and improvise the next step.
> - When a task or its findings span more than one skill's job, compose the skills rather than stretching one past its boundary. Composition may be sequential or concurrent, but it does not itself authorize subagent fan-out.
> - A governing skill's explicit stop, containment, or sequencing instruction overrides these defaults, and delegated agents follow their brief.

Design choices: the first bullet is mid-task-only, leaving request-time matching to fixed runtime terrain; "plausibly fits" keeps the re-check sensitive to the observed silence failure, while the mid-task trigger and silent check bound its reach. The second bullet preserves permissioned handoffs: continuation requires authority, otherwise the skill is offered by name. The third describes workflow composition without granting delegation authority. The final bullet makes governing-skill stops and delegated briefs controlling.

### 2. The data layer (exits in bodies, edges in descriptions)

Forward handoffs land in skill **bodies** as exits (the `outcome-shaping` Exits-table pattern, `SKILL.md:78`); **descriptions** change only where selection-critical, per the existing frontmatter convention. Touched skills, from the eight sequences: `diagnose`, `tdd`, `test-trust-audit`, `characterization-tests`, `contract-change-propagation`, `red-team` (parallel fan-out), `incident-response`, `postmortem`, `observability-instrumentation`, `deploy-plan`, `ideate`, `skill-squad`, `behavior-smoke-test`, `scrutinize-skill`; description edit for `making-recommendations` (thin-field → `ideate`). Special cases: `scrutinize-skill` is plugin-distributed (`review-family`) — Class-B publish path (version bump → Codex republish → mirror) on JP's ask; chain-7 exits naming Claude-only skills get availability-conditional phrasing. These edits are build-and-prune, not charter events.

### 3. The convention (repo `AGENTS.md`, Skill Editing section)

One line, roughly: when a skill's work has a natural upstream or downstream lane, name the handoff in the body — an exits line or section, availability-conditional for single-runtime lanes — and add it to the description only when selection-critical. This repo-local always-loaded edit may share the contract's Admission consult but remains a distinct decision. Scope note for the admission: this is editing guidance about *where* handoffs live; `agent-facing-design` keeps the routing-design judgment job untouched.

## Charter Package

One Admission consult may cover both gated edits, but it must adjudicate them as two distinct decisions and record one ledger entry per decision in `contract-decisions.md`.

### Decision A — runtime skill-use contract

**Q1 — closest existing contract:** the closest contracts are the runtimes' own request-time skill-matching instructions. They retain that job. The local contract begins only when a mid-task finding changes the work, when an invoked skill reaches a named handoff, or when one task spans multiple skill jobs. `work-router` owns explicit routing questions and is neither duplicated nor retired by this design.

**Q2 — what failure lighter context would not prevent:** one directly observed composition miss occurred despite the relevant handoff already existing in a skill body, while the broader ledger pattern supplies only a hypothesis because it lacks an opportunity denominator. The proposed four-bullet instruction section is the lightest ambient form that can govern the unowned mid-task and seam moments. Admission remains conditional on the prospective probes; aggregate counts alone do not clear it.

**Q3 — houses standards:** the contract is runtime-neutral, names its three owned moments, preserves authorization and governing-skill stops, and says plainly what an agent must do.

### Decision B — repo skill-authoring convention

**Q1 — closest existing contract:** `agent-facing-design` owns whether a routing or handoff relationship belongs in a skill; the repo convention owns only where an already-decided handoff is written — body by default, description only when selection-critical, and availability-conditioned for single-runtime lanes. It does not make the routing decision.

**Q2 — what failure lighter context would not prevent:** the inventory shows handoff data split inconsistently between bodies, descriptions, and non-route boundaries. One line in repo `AGENTS.md` is the lightest durable context for future skill authors; no validator or additional workflow is justified.

**Q3 — houses standards:** the line points routing-design judgment back to `agent-facing-design`, states the body/description placement rule, and carries the dual-runtime availability boundary.

**Subagent exposure (review M2), priced and accepted:** user-global instruction files load into most subagent contexts — general-purpose, custom, and workflow agents; the built-in Explore and Plan agents are the documented exceptions and skip CLAUDE.md entirely (sub-agents doc, "What loads at startup") — so the contract binds those delegated workers and any eval control arms run through them; the delegated-agents clause scopes narrowly-tasked delegation to its brief, the residual exposure is named here for the admission and watched via the usage ledger, which demonstrably captures subagent fires (47 `sidechain: true` records at design time) — and pre-registered evaluations in this repo must account for the ambient contract when defining control baselines.

**Durability:** the canonical contract text lives as `CANON` in a new drift-check script (`check-protected-set.sh` pattern) checking both global files byte-identically. The build must wire that script into tracked `.codex/hooks.json`, ignored `.claude/settings.local.json`, and the recovery recipe in `scripts/claude-skills-sync.sh`; losing the ignored Claude settings must not silently remove the check. This committed design doc is the Admission evidence pointer for the observed failures, bounded ledger analysis, and probe design.

## Proof Plan (pre-landing probes)

Pattern: `docs/agents/contract-evaluation-methodology.md` moves 1, 2, 3, 6, and 7 — pilot before seal, adversarial prereg review, seal-by-commit, single-variable differential, blinding, immutable surfaces, and replicated escalation. The prior plugin admissions were single-arm forward tests and are not precedent here. Spec:

- **Controlled delivery:** each trial is a `claude -p` subprocess with `--output-format stream-json`, a fixed model, fixed setting sources, fixed permissions/tools/environment, and one of two scratch `CLAUDE_CONFIG_DIR` trees. The trees contain identical seeded settings, skills, and skills-directory plugins; the only arm difference is the contract block in the user-global instruction replica. Both arms retain the runtime's fixed request-time matching terrain.
- **Roster and surface proof:** parse every run's `system/init` event and require the exact expected target-skill roster before scoring. Before the pilot and again before sealed runs, hash both instruction replicas, every loaded target skill source, plugin manifests, settings, task fixtures, and the workspace fixture manifest. A roster or hash mismatch invalidates the run rather than counting as contract failure.
- **Immutable fixtures:** each trial starts from a fresh disposable copy or reset worktree of one frozen fixture, with the same cwd and no state inherited from an earlier trial. Trial output and logs write outside the fixture. A mutating probe without a disposable fixture is `not run`.
- **Blinding and grading:** use neutral arm names and keep the arm map outside trial-visible paths. Trial prompts do not contain the expected skill names, assertions, arm identity, or intended answer. A scorer blind to arm grades captured outputs against the sealed observable rules; inspect the produced artifacts for arm or intent leaks before unblinding.
- **Observable events:** `take` means a captured assistant `tool_use` block naming the exact target Skill. `offer` means the response explicitly names the target invocation token and proposes a clear handoff; a generic suggestion such as “add tests” does not count. The mid-task probe requires an actual take. The seam probe accepts a take when continuation is authorized or an offer when it is not. The composition probe requires both target skills to be taken or explicitly offered under the same authorization rule.
- **Unsealed pilots:** before sealing, run a cheap paired pilot for each of the three probes using separate pilot-only tasks. Confirm the roster, observable event, scoring key, baseline rate, and absence of ceiling. If a channel is empty, ambiguous, or ceilinged, redesign it or drop it to characterization-only; do not seal it and do not treat inconclusive as GO.
- **Probes:** (1) *mid-task re-check* — the agent is underway when a finding changes what the work needs, such as discovering an untested legacy module that must be characterized before the refactor; (2) *seam handoff* — the agent is handed a just-found bug cause and must take or offer `tdd` according to authorization; (3) *composition* — findings span authorization and untrusted-input design and require both owning skills. There is no request-time probe.
- **Trials and escalation:** start with 3 trials per arm per probe. If either arm splits 2–1, extend both arms for that probe to 5 before unblinding; the blind scorer grades all five trials as one batch.
- **Pass criteria:** at 3 trials, the with-arm must satisfy the observable rule in at least 2/3 trials and strictly exceed the without-arm. After escalation, it must satisfy the rule in at least 4/5 trials — preserving the initial two-thirds floor — and strictly exceed the without-arm.
- **Ceiling and aggregation:** any sealed without-arm ceiling is **inconclusive-by-ceiling**, not a pass. GO for the complete contract requires all three probes to pass. A fail or inconclusive result returns the affected clause and the combined block for redesign and re-run; results from the other probes may be retained as bounded evidence but cannot authorize the full block.
- **Seal:** after pilots are resolved and an adversarial preregistration review is complete, commit the full preregistration — fresh sealed tasks, arm construction, hashes, fixtures, roster, observable scoring, blinding, trial counts, escalation, ceiling, and aggregation. The commit SHA is the seal; pilot tasks and outputs are excluded from sealed scoring, and there is no post-hoc adjustment.
- **Honest bound:** these probes exercise Claude-side behavior. Codex receives the same narrowed text, with behavior bounded initially by source inspection and the live watch rather than represented as experimentally proven.

## Data-Layer Behavior Proof

Structural validation is necessary but does not prove the new exits are followed. After the skill edits, run a documented representative matrix, with one live invocation, forward test, or realistic dry run for every changed skill where practical and an explicit justification where it is not:

- **Sequential exits:** exercise at least `diagnose` → `tdd` → `keep-green` and `test-trust-audit` → `characterization-tests` → `simplify-code`.
- **Permissioned offers:** show that a handoff is offered rather than taken when the current request or governing skill stops continuation.
- **Parallel composition:** exercise `red-team` → `authorization-design` + `injection-safe-inputs` without treating composition as automatic agent fan-out.
- **Runtime-conditional exits:** verify the chain-7 wording names Claude-only skills only when available and does not create a false Codex route.
- **Description trigger:** test the `making-recommendations` thin-field → `ideate` description change against should-trigger and nearby should-not-trigger prompts.
- **Plugin-distributed behavior:** test `scrutinize-skill` at source before publication; if JP later authorizes Class-B publication, separately prove the version bump, Codex cache, and mirror rather than treating source behavior as cache proof.

Record the matrix, commands or prompts, outcomes, and proof limits in the implementation evidence. A parse, integrity check, delivery check, or cache check cannot substitute for these behavior observations.

## Risks Owned

- **Over-firing** — the contract pushes toward invocation after mid-task findings; misrouting is a failure JP does not currently have. Guards: the mid-task-only trigger, "plausibly," the silent check, authorization-aware handoffs, and the precedence clause. Detector: the watch below. Purely editorial corrections may land without re-running Admission; any change to ownership, obligations, thresholds, carve-outs, or runtime scope is a new gated change and returns to the charter.
- **Subagent exposure** — priced in the Charter Package above.
- **Ambient cost** — 144 words (measured, including the heading) per session in both runtimes; accepted in shaping and re-priced after the latest narrowing.
- **Drift between the twin global files** — the canary script. Pre-existing drift already exists between the two files' `## Behavior Contracts` sections — `~/.codex/AGENTS.md` is missing the capability carve-out clause entirely, a live demonstration of exactly the drift class the canary prevents; filed via `/triage` at build with that clause named, not folded into this design.

## Build Order

1. Work on `feature/skill-use-contract`; keep this design doc committed as the durable evidence surface before any decision ledger entry cites it.
2. Finalize the narrowed contract wording through `agent-facing-design` and `writing-principles`, preserving byte identity and the no-subagent-authority boundary.
3. Build the controlled scratch configurations, frozen fixture, neutral arm map, roster check, hashes, observable scorer, and separate pilot tasks.
4. Run the unsealed paired pilot for all three probes. Resolve every empty, ambiguous, or ceilinged channel before proceeding; do not reuse pilot tasks or outputs in sealed scoring.
5. Write the complete preregistration, obtain an adversarial design review, patch it before data if needed, then commit it; that commit SHA is the seal.
6. Run the sealed probes exactly as preregistered and record the blinded results, validity checks, unblinding step, and bounded interpretation.
7. Run the Charter Admission consult for Decision A and Decision B and record JP's separate GO/NO-GO ratification for each — before any global-file or repo `AGENTS.md` edit.
8. If Decision A is GO, land the `## Skill Use` block in both global files and the drift script; wire the check into `.codex/hooks.json`, `.claude/settings.local.json`, and the `claude-skills-sync.sh` recovery recipe.
9. If Decision B is GO, land the convention line in repo `AGENTS.md`.
10. Seed the Class-A data layer. Keep `scrutinize-skill` Class B deferred until JP explicitly authorizes publication.
11. Run and record the Data-Layer Behavior Proof matrix. Keep source behavior, Claude symlink delivery, Codex plugin cache, and mirror claims separate.
12. Append one `contract-decisions.md` entry for Decision A and one for Decision B, each citing this doc, the relevant decision, commits, and probe records.
13. File the pre-existing global-file `## Behavior Contracts` drift via `/triage`, naming specifically that `~/.codex/AGENTS.md` is missing the capability carve-out clause.
14. Run the structural validation ladder on the exact edited surfaces: frontmatter parses, referenced-path inspection, `check-library-integrity.sh`, `claude-skills-sync.sh --check`, the new canary, and `git diff --check`. Structural green does not replace the behavior matrix.
15. **Watch, with a checkpoint:** read at the 2026-08-01 ledger re-read. Pre-named trigger: unwanted mid-task fires of expensive-by-design lanes (`skill-squad`, `methodology-critique`, `synapsis`, `deep-research`). Also watch seam-handoff sequences, permissioned offers, automatic fan-out attempts, and JP corrections.

## Review Disposition (2026-07-11 scrutiny)

Verdict was Patch Before Implementation with seven required changes, all applied: (1) H1 admission rewritten around the fixed-terrain harness instruction, `work-router` demoted to incidental cut; (2) H2 governing-skill precedence clause added to the contract; (3) M1 probes re-cited to `contract-evaluation-methodology.md` with arms, trials, delivery mechanism, and sealed pass criteria specified; (4) M2 subagent exposure scoped in-text and priced in the admission; (5) M3 this doc committed as the durable evidence artifact; (6) M4 charter consult + JP ratification inserted before global-file edits; (7) watch pinned to 2026-08-01 with the expensive-lane trigger named. Low findings absorbed: pre-existing global-file drift routed to `/triage` (build step 9); convention-line scope sentence added to the Charter Package; the "parallel" wording flag attached to the writing pass.

A second 2026-07-11 review (execution-readiness pass on this doc at `1203ac1`) was adjudicated via `review-reviewer` — the review judged `reliable`, all six required changes confirmed against recomputed evidence — and applied: (1) the decisive inference re-grounded on the fired-source ledger specimen (`making-recommendations`), zero-opportunity chains demoted to illustration; (2) the Q1 request-time overlap now openly adjudicated as fixed-terrain reinforcement with a named fallback, and the silence probe re-centered on the mid-task moment; (3) the probe spec patched — symmetric without-arm replica, hermetic `claude -p` delivery, base-rate pilot plus sealed ceiling rule, sealed aggregation rule, and (adjudication refinement) a split-escalation rule; (4) subagent exposure corrected per the official sub-agents doc (Explore/Plan skip user memory) and, per the adjudication, the ledger's 47 sidechain-tagged records cited as capture evidence in place of the review's "unproven" caveat; (5) the chain-3 and chain-4 inventory claims fixed and the `injection-safe-inputs:67` compose edge added; (6) seal-by-commit made explicit in the build order and the `/triage` filing scoped to name the missing capability carve-out. Second adjudication refinement folded: the per-skill variance line in the Premise.

A third 2026-07-11 execution-readiness review at `3500a5d` was adjudicated via `review-reviewer` as partially reliable: its core verdict and seven of eight required changes held, while its prescribed `3/5` escalation threshold was not methodologically required. This patch applies the confirmed findings and the adjudication's three missed issues: (1) request-time matching removed from both copies while byte identity is preserved; (2) pilot-before-seal, all-probe pilots, correct split escalation, explicit `4/5` post-escalation scoring, non-passing ceilings, and observable take/offer rules; (3) identical seeded config/skill/plugin trees, roster capture, hashes, immutable fixtures, blinded grading, and artifact leak checks; (4) the ledger claim narrowed to a hypothesis without an opportunity denominator; (5) a post-edit behavior-proof matrix; (6) separate Admission treatment and decision records for the runtime contract and repo convention; (7) `work-router` retirement removed; (8) all three canary caller/recovery surfaces named; and (9) material post-landing contract changes returned to the charter. No probes or global instruction edits were performed as part of this patch.
