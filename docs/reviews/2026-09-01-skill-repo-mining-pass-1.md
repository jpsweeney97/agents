---
type: review
date: 2026-09-01
scope: "Mining pass 1 over three third-party skill repositories: mattpocock/skills (delta since the 2026-07-08 pin), addyosmani/agent-skills (never assessed), multica-ai/andrej-karpathy-skills (never assessed) — 86 candidate surfaces adjudicated against the live library"
reviewed_commit: 1257617d22612ce422e58e4e3ca56a051e519be7
method: "Multi-agent workflow wf_d4cbf4ac-6df: 9 assessor batches, each followed by one adversarial verifier instructed to attack in both directions; 18 agents, 3.74M subagent tokens, 765 tool calls, 0 errors. Verdicts re-read in full by the reporting session (2026-09-01) after the charter-admission deliberation."
posture: "Recommendations, not decisions. No fold was executed, no admission built, no ledger entry written by the mining pass. Every verdict is charter case (d) — the fate of third-party contract material — and takes its own docs/agents/contract-decisions.md entry at landing, including zero-fold rejects."
---

# Skill-Repo Mining Pass 1: mattpocock delta, addyosmani, karpathy

## Executive summary

**86 candidate surfaces were adjudicated: 5 ADMIT, 27 FOLD, 8 PARK (7 distinct — `wizard` was assessed in two batches), 46 REJECT.** The dominant pattern across all three donors: lifecycle-suite encyclopedias meeting a specialist judgment library. Where a candidate and a local skill share a job, the local version won on every direct comparison the verifiers checked — deeper method, proof discipline, and non-use boundaries the donors lack. What survives is narrow and specific: two whole capabilities with no owner anywhere (a steady-state performance-optimization loop; a web-performance audit with a fabrication guard), three thin-but-real admits, and 27 separable disciplines that sharpen existing local skills.

The adversarial verification stage earned its cost: it flipped 4 verdicts (`implement-spec` FOLD→REJECT, karpathy `CLAUDE.md` REJECT→FOLD, the description-collision detector ADMIT→PARK, `skill-lint` FOLD→REJECT), killed or downgraded roughly a dozen proposed folds by finding owners the assessors' greps missed, surfaced 11 folds the assessors missed, and ran two proposed measurement tools against the real corpus before judging them — both failed on contact. The recurring assessor failure it caught: grepping the donor's vocabulary instead of the discipline (the "search-term artifact"), which manufactured false absence evidence at least three times.

**Standing caveat:** every verdict rests on subagent reports, adversarially verified once. The verification stage itself caught wrong verdicts and wrong citations, which is evidence the reports are not uniformly reliable. Load-bearing claims — especially absence greps and file:line citations — are re-verified against live files at build or land time, per this repo's working defaults.

## Relationship to the charter deliberation

Between this pass and this report, the charter question the pass raised (does Admission decide candidate-versus-incumbent on ownership or merit?) was deliberated cross-model and resolved: certificate at `~/.synapsis/runs/2026-08-31-charter-admission-standard/` (RESOLVED, UNCONTESTED mode — the run's weakest grade, disclosed), adopted by JP 2026-09-01, amendment landed as `17dc693`.

Consequences for this report, per the accepted answer:

- **The 86 verdicts stand without blanket re-adjudication.** Their recorded reasoning compares substance, folds better clauses, and escalates whole-design reversals to JP — the comparison the amendment now names explicitly.
- **The charter now carries a Supersession path** (Admission question 1 reworked; Retirement cross-referenced). Any future candidate for owned work proceeds as a proposed replacement: comparison grounded in observed work (never synthetic cases alone — the deliberation's recorded reservation), separable-clause wins are folds, whole-design reversals go to JP, retire-plus-admit is one ledgered decision. None of the 86 verdicts requires that path today; two recorded escalations (below) are exactly the cases it governs if reopened.
- **Escalations that remain JP decisions, never silent edits:** the `prototype` capture-the-prototype reversal (contradicts the fork's stated position in four places), and the `grill-me` one-at-a-time versus batched-frontier design question (first-party consistency question — its serialize rule conflicts with the global batching rule and two sibling skills, per `writing-principles` lens 7).

## Donor pins

The clones lived in session scratch and are gone; re-clone at these pins to re-read donor source. Upstream may have moved.

| repo | pin | pin date |
|---|---|---|
| `mattpocock/skills` | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | 2026-08-24 |
| `addyosmani/agent-skills` | `d2c37ef6225dd8726cdd369a8030307f48592d26` | 2026-08-28 |
| `multica-ai/andrej-karpathy-skills` | `2c606141936f1eeef17fa3043a72095b4765b9c2` | 2026-04-20 |

Prior art: `mattpocock/skills` was fully adjudicated 2026-07-05 and 2026-07-08 at pin `d574778` (`docs/plans/2026-07-08-mattpocock-skills-extraction-roadmap.md`, `docs/plans/2026-07-08-mattpocock-readoption-inventory.md`, ledger entries of those dates). This pass assessed only the 183-commit delta: seven new skills (`matt-NEW`) and the drift to already-adjudicated surfaces (`matt-DELTA`). Every fold the July pass landed was verified still in place. The other two repos had never been assessed; grep for their names across `docs/`, `skills/`, `skills-claude/`, `plugins/`, and `AGENTS.md` returned zero prior hits.

## Verdict index

Final verdicts after adversarial verification (verifier flips applied). Per-candidate reasoning, absence evidence, hazards, and charter notes live in the batch digests (see Pointers).

| batch | candidate | final | conf |
|---|---|---|---|
| addy-A | api-and-interface-design | **FOLD** | HIGH |
| addy-A | browser-testing-with-devtools | **REJECT** | HIGH |
| addy-A | ci-cd-and-automation | **FOLD** | HIGH |
| addy-A | code-review-and-quality | **FOLD** | HIGH |
| addy-A | code-simplification | **FOLD** | HIGH |
| addy-B | constraint-driven-development | **ADMIT** | MEDIUM |
| addy-B | documentation-and-adrs | **FOLD** | HIGH |
| addy-B | deprecation-and-migration | **REJECT** | HIGH |
| addy-B | debugging-and-error-recovery | **REJECT** | HIGH |
| addy-B | context-engineering | **REJECT** | HIGH |
| addy-C | doubt-driven-development | **FOLD** | HIGH |
| addy-C | git-workflow-and-versioning | **REJECT** | HIGH |
| addy-C | incremental-implementation | **REJECT** | HIGH |
| addy-C | idea-refine | **REJECT** | HIGH |
| addy-C | frontend-ui-engineering | **PARK** | HIGH |
| addy-D | performance-optimization | **ADMIT** | HIGH |
| addy-D | security-and-hardening | **FOLD** | HIGH |
| addy-D | observability-and-instrumentation | **FOLD** | HIGH |
| addy-D | interview-me | **FOLD** | HIGH |
| addy-D | planning-and-task-breakdown | **REJECT** | HIGH |
| addy-E | shipping-and-launch | **FOLD** | HIGH |
| addy-E | source-driven-development | **ADMIT** | MEDIUM |
| addy-E | spec-driven-development | **REJECT** | HIGH |
| addy-E | test-driven-development | **FOLD** | HIGH |
| addy-E | using-agent-skills | **REJECT** | HIGH |
| addy-META | hooks/hooks.json + hooks/session-start.sh | **REJECT** | HIGH |
| addy-META | hooks/sdd-cache-pre.sh + hooks/sdd-cache-post.sh + hooks/SDD-CACHE.md | **REJECT** | HIGH |
| addy-META | hooks/simplify-ignore.sh + hooks/SIMPLIFY-IGNORE.md | **REJECT** | HIGH |
| addy-META | commands/{build,code-simplify,planning,review,spec,test,ship}.toml | **REJECT** | HIGH |
| addy-META | commands/constraints.toml | **PARK** | MEDIUM |
| addy-META | commands/webperf.toml | **REJECT** | HIGH |
| addy-META | agents/code-reviewer.md | **REJECT** | HIGH |
| addy-META | agents/security-auditor.md | **FOLD** | HIGH |
| addy-META | agents/test-engineer.md | **REJECT** | HIGH |
| addy-META | agents/web-performance-auditor.md | **ADMIT** | MEDIUM |
| addy-META | references/accessibility-checklist.md | **FOLD** | MEDIUM |
| addy-META | references/definition-of-done.md | **REJECT** | HIGH |
| addy-META | references/observability-checklist.md | **FOLD** | HIGH |
| addy-META | references/orchestration-patterns.md | **FOLD** | MEDIUM |
| addy-META | references/performance-checklist.md | **FOLD** | MEDIUM |
| addy-META | references/security-checklist.md | **FOLD** | HIGH |
| addy-META | references/testing-patterns.md | **REJECT** | HIGH |
| addy-META | scripts/validate-reference-links.js | **REJECT** | HIGH |
| addy-META | scripts/validate-artifact-paths.js | **REJECT** | HIGH |
| addy-META | scripts/validate-versions.js | **FOLD** | HIGH |
| addy-META | scripts/validate-commands.js | **REJECT** | HIGH |
| addy-META | scripts/validate-skills.js + scripts/lib/skill-lint.js | **REJECT** | HIGH |
| addy-META | scripts/run-evals.js — Tier-2 description-collision check | **PARK** | HIGH |
| addy-META | scripts/run-evals.js — Tier-3 behavioral runner | **REJECT** | HIGH |
| addy-META | evals/cases/*.json + evals/fixtures/ (per-skill eval corpus) | **PARK** | HIGH |
| addy-META | docs/skill-anatomy.md | **REJECT** | HIGH |
| addy-META | AGENTS.md + CLAUDE.md (addyosmani repo instructions) | **REJECT** | HIGH |
| addy-META | CONTRIBUTING.md | **REJECT** | HIGH |
| addy-META | hooks/*-test.sh + scripts/*-test.js (test suites) | **REJECT** | HIGH |
| matt-NEW | implement-spec | **REJECT** | HIGH |
| matt-NEW | retro | **FOLD** | MEDIUM |
| matt-NEW | setup-ts-deep-modules | **REJECT** | HIGH |
| matt-NEW | to-questionnaire | **ADMIT** | MEDIUM |
| matt-NEW | wait-what | **REJECT** | HIGH |
| matt-NEW | writing-for-agents | **FOLD** | HIGH |
| matt-NEW | wizard | **PARK** | MEDIUM |
| matt-DELTA | diagnosing-bugs (Redact section + hitl-loop capture rule) | **FOLD** | HIGH |
| matt-DELTA | ask-matt PHASE-BOUNDARIES.md (new file) | **FOLD** | MEDIUM |
| matt-DELTA | writing-great-skills → writing-for-agents (deleted + rewritten) | **FOLD** | MEDIUM |
| matt-DELTA | improve-codebase-architecture (Scope before you scan: YAGNI) | **FOLD** | MEDIUM |
| matt-DELTA | prototype (capture the prototype as a primary source) | **FOLD** | MEDIUM |
| matt-DELTA | setup-matt-pocock-skills (recommendation-first conditional interview) | **FOLD** | MEDIUM |
| matt-DELTA | wayfinder | **PARK** | HIGH |
| matt-DELTA | grilling | **REJECT** | HIGH |
| matt-DELTA | triage | **REJECT** | HIGH |
| matt-DELTA | to-tickets | **REJECT** | HIGH |
| matt-DELTA | to-spec | **REJECT** | HIGH |
| matt-DELTA | tdd | **REJECT** | HIGH |
| matt-DELTA | code-review | **REJECT** | HIGH |
| matt-DELTA | codebase-design | **REJECT** | HIGH |
| matt-DELTA | domain-modeling (ADR-FORMAT.md, CONTEXT-FORMAT.md) | **REJECT** | HIGH |
| matt-DELTA | teach (four companion format files) | **REJECT** | HIGH |
| matt-DELTA | handoff (productivity) | **REJECT** | HIGH |
| matt-DELTA | writing-beats / writing-fragments / writing-shape | **PARK** | HIGH |
| matt-DELTA | wizard (graduated in-progress/ → engineering/) | **PARK** | HIGH |
| matt-DELTA | Upstream deletions: deprecated/* (4) and personal/* (2) | **REJECT** | HIGH |
| matt-DELTA | agents/openai.yaml across every skill | **REJECT** | HIGH |
| karpathy | karpathy-guidelines CLAUDE.md (the always-loaded behavior contract) | **FOLD** | HIGH |
| karpathy | skills/karpathy-guidelines (the skill-shaped wrapper) | **REJECT** | HIGH |
| karpathy | EXAMPLES.md (the worked before/after case material) | **REJECT** | HIGH |
| karpathy | Distribution packaging (.claude-plugin/ and .cursor/rules/) | **REJECT** | HIGH |

## The five admits

Each is a job, not a text: the charter's Thesis means every admit is re-authored to house standards from scratch, with the donor as source material. Each takes a full case-(d) ledger entry at build (the `resolve-conflicts` 2026-07-09 entry is the model). Confidence MEDIUM on three of five means the merit rests on a real gap plus cognitive-offload rather than observed local friction — which `AGENTS.md` says is legitimate.

1. **`perf-optimize`** (addy-D `performance-optimization`, HIGH) — the steady-state optimization loop for code that was always slow: baseline → localize → change one thing → re-measure the same way → keep-or-revert on the number (neutral counts as revert) → regression guard, with an attempt ledger recording reverted attempts. Fills `diagnose`'s regression-gated gap, named as a build-now opening by `docs/reviews/2026-07-01-skill-library-capability-growth-review.md:114` and never built. Verifier leans standalone over a `diagnose` branch (different question, different work product); the donor's own `agents/web-performance-auditor.md` carries the proof-boundary idiom to borrow. Roughly 98 of the shared performance-checklist's 236 lines are stack-neutral backend/caching material worth keeping as references. Placement `skills/`, name `perf-optimize`.
2. **Web-performance audit** (addy-META `agents/web-performance-auditor.md`, MEDIUM) — page-level Core Web Vitals audit whose spine is the Metric-Honesty Rule: mode chosen by whether a real measurement artifact exists; every scorecard value labelled Field/Lab/Trace; unmeasured fields say "not measured"; source-only findings tagged potential-impact, never presented as measurements. Zero local or bundled coverage (LCP/INP/CLS appear nowhere in 119 skills, WCAG appears nowhere in the Claude Code binary's bundled metadata). Re-author must drop the mandated-praise section and the five-tier severity table (same defects rejected elsewhere in the batch), fence remediation out (audit-only), and cut the framework-specific lists to references.
3. **`to-questionnaire`** (matt-NEW, MEDIUM) — turn a decision the user cannot answer alone into a Markdown questionnaire for the named human who holds the knowledge, interviewing the user only about the send ("grill the send, not the subject"). Genuinely ownerless: `decision-owner-map` names the holder but never asks them; `stage-prompt`/`courier` address machines; `email-writing` is correspondence. The house version must break the courier tie explicitly (courier when the return leg is a claim to adjudicate; this when it is knowledge the user lacks) and adopt the `runbook-authoring` artifact-path floor.
4. **Weakened-checks scan** (addy-B `constraint-driven-development`, narrowed hard, MEDIUM) — only the diff-guard half survives: detect the five moves that reach green by lowering the bar (threshold moved / test made easier / checker silenced / work unfinished / exception appeared), rendered as a findings table with `path:line` evidence and confirmed/cleared/unread honesty, read-only, no verdict. The gap is real and deliberate-looking from both sides: `keep-green:53` and `resolve-conflicts:67` forbid the move in the first person, `implementation-review:116` explicitly excludes the lint-ignore case, and nothing detects it in a diff. The CONSTRAINTS.md-authoring half is rejected on house fit (machine-wide installs, numeric ratchets against three skills' stated refusals, ambient-text shipping). Verifier: the working name `gate-weakening-scan` violates the Literal Language rule ("gate"); use plain words such as `weakened-checks-scan`.
5. **Docs-grounded framework code** (addy-E `source-driven-development`, MEDIUM) — before writing framework-specific code, pin the dependency version from the manifest, fetch the official page for that version, cite deep links, label residue UNVERIFIED. Generalizes a discipline the library has only per-vendor (`claude-code-docs`, `openai-docs`, bundled `claude-api`). Fence: routes to the vendor lanes where they exist; `dependency-upgrade` keeps version bumps; `baseline` keeps authority questions. The donor's name is borrowed-phrase jargon; rename literally.

## The 27 folds, by target

Grouped by the file that would change. Value labels are the verifiers' final calibration. **Plugin-distributed targets (review-family, git-cycle) ride the version-bump publish path, never the local-skill flow.** Known duplication the stopped consolidation pass was meant to resolve: two batches independently proposed the feature-flag-lifecycle fold into `deploy-plan` (addy-A `ci-cd` and addy-E `shipping-and-launch`) — land once.

**`skills/diagnose/`** — (1) the Redact section: redact every secret before showing a command, output, or captured artifact; env-var loops; quote only signal-bearing lines of auth-carrying artifacts (HIGH — the batch's best find; `diagnose:63` requests HAR files with zero redaction discipline today; exact sibling of the landed 2026-07-09 `save-handoff` fold). (2) hitl-loop capture rule: credentials are a `step`, never a `capture` (MEDIUM). (3) Read live browser surfaces before authoring a scripted harness, availability-conditioned (LOW).

**`plugins/review-family/skills/implementation-review/references/review-lenses.md`** — (4) idempotency/retry-safety lens: key derived from intent, payload-hash guard on key reuse, retention outliving the longest re-delivery path — cross-reference the concurrency lens for atomicity instead of restating it (HIGH). (5) orphaned-code lens: name symbols the change stranded, as a non-blocking note — must be written as a narrow exception to `implementation-review:113-116`'s deliberate lint-owns-this assignment (LOW-MEDIUM). (6) caching-correctness question: key includes every input the response varies on; nothing whose staleness is a correctness bug is cached (MEDIUM — "cache key missing the viewer" is a correctness bug wearing a performance costume). (7) plan-evidence for index changes: capture the plan before, revert an index that did not change the plan — the revert clause is the load-bearing half (MEDIUM). (8) accessibility-lens extension: focus management plus the 4.5:1 / 3:1 contrast numbers, inline in the lens sentence, never a new reference file (MEDIUM).

**`skills/injection-safe-inputs/`** — (9) SSRF/outbound-fetch as a censused sink class with the TOCTOU caveat (HIGH — the census is "the gate the rest hangs on" and has no outbound-request sink). (10) model output as an untrusted source reaching censused sinks — keep the prompt-injection fence, tighten it to input-side-only (MEDIUM). (11) upload content-type verified against magic bytes, not the client's label (MEDIUM-LOW). **Landing (9)/(10) requires rewriting `injection-safe-inputs:59` in the same change** — the red-team fold below makes its "neither this skill nor any named neighbor" sentence false.

**`skills/red-team/`** — (12) LLM-feature adversary classes: prompt injection as entry, tool misuse/leakage/unbounded consumption as payoffs, permissions enforced in code never by system prompt (HIGH — lands in the hole `injection-safe-inputs:59` declares). (13) OWASP LLM Top 10 as the residual-check reference in the close, never a ten-item sweep in the moves (MEDIUM).

**`skills/observability-instrumentation/`** — (14) pre-register the 2-4 on-call questions before choosing signals; every signal traces to one; metrics=that, traces=where, logs=why (HIGH). (15) alert hygiene, reshaped by the verifier: every alert links to a runbook and exactly two severities (page/ticket); route runbook content to `runbook-authoring`; the test-fire becomes a named human handoff, never a step this skill performs (MEDIUM). (16) percentiles always, averages never; duration as a histogram (LOW).

**`skills/deploy-plan/`** — (17) feature-flag lifecycle: a flag-gated rollout names the flag's owner and removal condition at gauge-setting time; both states must work (MEDIUM; proposed independently by two batches — land once; host lane has zero recorded fires, so value is honest-but-latent).

**`skills/simplify-code/`** — (18) instrument threshold: a uniform mechanical edit across many sites switches instruments (codemod) and routes to `migration-campaign` — uniformity is the trigger, not the line count (MEDIUM). (19) honor an in-source do-not-simplify marker; name it in the Review Packet exclusions — lands in the playbook, the execution surface (LOW).

**`skills/writing-principles/`** — (20) the cache lens: a doc restating what config/scripts/layout/--help already say is a cache of a cheap lookup; keep only what the agent cannot find by looking — must carry the keep-rule, and the lander must resolve the scope question (the lane is obligation-only; alternative homes: `agent-facing-design` or the AGENTS.md Skill Editing block) (MEDIUM).

**`skills/agent-facing-design/references/calibration.md`** — (21) pre-fan-out question set: all branches independent; each produces a different kind of finding; merge fits the caller's context; wait is worth the parallelism (MEDIUM — the sharp question is the different-kind test). (22) depth cap: orchestration depth one hop, merge in the caller — a consolidation of three existing per-skill statements into the gate (LOW). (23) branching-disclosure test and pointer-repair ordering from `writing-for-agents` (LOW, two items).

**`skills/decision-record/` + `skills/grill-with-docs/ADR-FORMAT.md`** — (24) detect the repo's existing ADR convention before writing (location, markup, numbering) and match it; surface conflicts rather than starting a second scheme. Verifier: ADR-FORMAT.md is the primary target (single source all three consumers read); `decision-record:41` is the reinforcement (HIGH).

**`skills/courier/`** — (25) claim-withholding: hand the reviewer the artifact and the contract, withhold your answer to the question you are asking — scoped so it does not contradict courier's deliberate carrying of settled decisions (MEDIUM after the verifier found the discipline already owned in six other surfaces; the gap is courier alone).

**`skills-claude/friction-to-guards/`** — (26) two agent-observed evidence sources the correction-keyed intake cannot see: tool economy (scoped to token-wasteful calls only, or it fights the global choose-depth rule) and information access (routed to `update-config`, not a new tier) (LOW after verifier discounts; the widened intake routes through `agent-facing-design` first).

**`scripts/check-library-integrity.sh`** — (27) manifest-to-CHANGELOG version lockstep check per plugin — charter-exempt capability tooling, insurance on `release-cut`'s existing procedure (LOW-MEDIUM).

Also recorded by verifiers as smaller riders on the folds above: `context-checkpoint` gains the primary-source lossiness cost (reworded to never license running past the room) and the `land` carve-out consistency edit; `setup-matt-pocock-skills` gains the recommendation-first interview (a house-alignment repair — its current one-at-a-time contradicts the global batching rule); `improve-codebase-architecture` gains churn-scoped surveying; `prototype` gains capture-on-a-throwaway-branch **only as a JP decision** (it reverses the fork's stated delete-when-done position in four places) with a branch-naming/retention line so `git-hygiene` can see the branches.

## The parks (7 distinct), with reopen triggers

- **`frontend-ui-engineering`** — genuinely ownerless production-UI quality bar; no web-frontend repo exists and the demand record is zero. Reopen: a real web-frontend project, or two-plus sessions of ad hoc UI-quality friction — **including on published artifacts**, not only app repos. Re-author stack-neutral if reopened.
- **`constraints.toml` / standing quality-bar artifact** — nothing writes a repo's standing bar as a first-class artifact; but AGENTS.md already carries the bar here, and a second artifact creates the two-sources problem `baseline` adjudicates. Reopen: a repo whose bar lives only in CI config and heads, or a review miss traced to no declared bar.
- **Description-collision detector** (verifier-flipped from ADMIT) — run against the real 119-description corpus it produced zero actionable findings and seven false positives: the score is driven by the deliberate cross-fencing that prevents misroutes, so it ranks the best-disambiguated pairs highest. Reopen: an observed stolen fire in the usage ledger — score that pair; if it sat in the top decile pre-misroute, build the stored-baseline delta form (drift is a change, not a level).
- **Per-skill eval corpus with owner-tagged negatives** — the one instrument that turns prose non-use boundaries into executable rank assertions; ~600 hand-written prompts to author. Reopen: a stolen-fire pattern the similarity score did not predict. The CI-mandate half is refused permanently ("admission stays ungated by proof").
- **`wayfinder`** — park stands; the drift added a fourth un-adopted dependency (`/research` dispatch) and a parallel-subagent dimension, making un-parking strictly more expensive. Ledger Parks entry needs its citation fixed: the irreversible instruction is "update or delete those tickets," not a literal `gh issue delete`.
- **`writing-beats` / `writing-fragments` / `writing-shape`** — park stands; upstream softened "abandoned experiments" to "Beta" without resolving the two-unsettled-variants problem. Second reopen trigger added: upstream graduating one variant and retiring the other.
- **`wizard`** (two rows, one skill) — graduated upstream and made model-invoked, which retires the abandoned-experiments premise but not the demand premise: zero `.env.example`, zero setup scripts, zero `gh secret set` anywhere in `~/Projects/active` (dated negative baseline recorded in the digest). Never ledgered in July — takes its first ledger entry whenever dispositioned. Reopen on observed hand-rolling of an interactive provisioning script; donor maturity is not demand.

## The rejects, by ground

The 46 rejects cluster into five recurring grounds; per-candidate detail is in the digests.

1. **Same job, deeper local owner** (the majority): `debugging-and-error-recovery` vs `diagnose`; `planning-and-task-breakdown` vs `implementation-planning`+4; `test-driven-development`'s package vs `skills/tdd`; `idea-refine` vs six lanes; `interview-me` vs `outcome-shaping`; `code-review-and-quality` and `agents/code-reviewer.md` vs `implementation-review`; `spec-driven-development` as a thin orchestrator (the `implement` precedent); the matt-DELTA em-dash-only rows (`triage`, `to-tickets`, `to-spec`, `tdd`, `code-review`, `codebase-design`, `domain-modeling`, `teach`, `handoff`); karpathy's four principles, each owned by a named first-party surface with the friction record showing the two principles JP actually has friction with are the two he already paid for.
2. **House-rule contradictions**: silent-fallback teaching (`debugging`'s Safe Fallback Patterns; the SDD cache); tag-as-version-source and unqualified `git push` (`git-workflow`); a second controlled-language standard (`wait-what`'s ASD-STE100); karpathy `EXAMPLES.md`'s checkmarked answers violating fail-fast, type-hints, and its own orphan rule.
3. **Ambient contracts wearing skill packaging**: `using-agent-skills` (routing atlas + always-on behavior rules), `context-engineering`, the karpathy wrapper, the SessionStart hook — all gated-class material that would smuggle past the charter in skill form.
4. **Stack-locked recipes for repos JP does not have**: `setup-ts-deep-modules` (empty monorepo shell verified), `browser-testing-with-devtools` (a third browser MCP), `testing-patterns`, the command layer and its validators (policing a duplication this architecture lacks — one source tree, two runtimes).
5. **Hazardous machinery**: `simplify-ignore` (in-place source mutation with a crash-restore dependency), the SDD cache (counterfeits tool errors, stale answers under a freshness stamp), `implement-spec` (unprompted PR creation, unattended code-writing subagents, worktree deletion without landed-work checks — doubly charter-gated and rejected).

Verified confirmations worth keeping: the six upstream deletions confirm settled rejects rather than reopening them (a park is about whether JP needs the job); upstream `setup-matt-pocock-skills` independently converged on the fork's PR-default-no decision; the addyosmani `AGENTS.md` "invoke a skill at even 1% chance" doctrine is the inverse of build-and-prune and explains the donor family's ambient-in-skill-packaging pattern.

## Named gaps recorded, not filled

Ownerless jobs the pass surfaced where the donor material was not good enough to fill them. Recorded so the next pass does not re-derive them; none is a build commitment.

- **CI-pipeline authoring** — "write me a CI pipeline" has no owner; reopen when JP hand-authors CI in a repo and the third such session produces a wrong pipeline or re-derives the gate ordering.
- **Authentication-design sibling** — `authorization-design:53` hands authentication mechanics back on purpose; the donor's password/session/reset/rate-limit material and security-headers/CORS both sit on that unowned ground.
- **Cache-design forcing pass** — cache-aside vs write-through failure modes, negative caching, stampede protection, the key-completeness rule: same shape as `injection-safe-inputs`/`authorization-design` (one surface, provable artifact). The diff-level check is fold 6; the design skill is a separate decision.
- **Write-boundary retry/exactly-once design pass** — sibling of the idempotency lens, seeded from the donor's block; a fresh authoring job.
- **Capability-review corroboration** — the donor independently reached for three openings the 2026-07-01 capability review already named unbuilt: `secret-leak-response`, `dependency-advisory-response`, `pii-data-handling`. Weak but real evidence those openings are worth their builds; donor text usable if opened.
- **Local-lane gap surfaced in passing** — `implementation-planning:50` writes its plan artifact with no check-if-exists or durable-write floor while both sibling plan-writing lanes carry one.

## Charter posture

- Every one of the 86 verdicts is a case-(d) decision on third-party contract material. **Each takes a `docs/agents/contract-decisions.md` entry at landing — including zero-fold rejects** (Extraction step 3; Decision Record). Nothing has been ledgered yet; this report is the evidence pointer those entries can cite, pinned by `reviewed_commit` and the donor pins.
- Extraction's remove-the-original does not bind this pass: the donors were scratch clones, never installed (the ledger's 2026-07-08 precedent), and the clones are already gone with the session scratchpad. Nothing local routes to any donor surface.
- Gated candidates were correctly identified and none was admitted: the three addyosmani hooks (always-loaded / unattended / source-mutating), `implement-spec` (irreversible-effect + unattended dispatch), karpathy's ambient file, and the donor plugin packagings. Installing any donor plugin to "watch it fire" would itself be a gated event; the mining deliberately never installed.
- Folds that widen agent obligations route through `agent-facing-design` at landing (the friction-to-guards intake widening and the review-lens additions were specifically flagged); plugin-distributed folds ride the version-bump/republish/mirror path.
- The Supersession amendment (`17dc693`) governs any reopened whole-design replacement from this corpus; the comparison must ground in observed work, never synthetic cases alone.

## Evidence boundary

What this report rests on: the durable mining artifacts (all ten digests read in full by the reporting session; shas recorded at `~/.synapsis/evidence/2026-08-31-charter-admission-standard/mining-artifacts-shas.txt`), the workflow's structured return, the charter deliberation certificate, and the live charter at `17dc693`. What it does not rest on: donor source (clones gone; re-clone at pins to re-read), live re-verification of the subagents' ~200 file:line citations (each was verified once by its batch verifier; the verifiers themselves caught citation errors, so re-verify at build time), or any executed fold or forward test. The verification stage's own corrections (4 verdict flips, ~12 fold kills/downgrades, 11 missed folds, multiple citation and fire-count fixes) are the calibration evidence for how far to trust the remainder. Later edits to the library invalidate specific citations; live files outrank this record.

Mining pass 2 (consolidation: stress-testing the 5 admits with fresh skeptics, resolving cross-batch fold collisions, coverage critique) was launched as `wf_6abd8c89-cd9` and stopped by JP partway; completed agents are cached and resumable — `Workflow({scriptPath: "/Users/jp/.claude/projects/-Users-jp--agents/93b9e21c-f650-48e2-a069-82eb18ce67e4/workflows/scripts/mine-consolidate-wf_6abd8c89-cd9.js", resumeFromRunId: "wf_6abd8c89-cd9"})` — with cached results treated as incomplete until the journal confirms otherwise. Its resume/redesign/abandon disposition is open.

## Pointers

- Durable artifacts: `/Users/jp/.claude/projects/-Users-jp--agents/93b9e21c-f650-48e2-a069-82eb18ce67e4/mining-artifacts/` — `digest/INDEX.md` (verdict table), `digest/<batch>.md` (per-candidate detail: job, closest owner, reasoning, fold targets with donor refs and absence evidence, hazards, charter triggers, verifier basis and corrections), `mining-results.json`, `verdict-rows.json`, `local-index.md` (119-skill roster at assessment time), `candidate-index.md`.
- Workflow journal (raw agent returns): `/Users/jp/.claude/projects/-Users-jp--agents/93b9e21c-f650-48e2-a069-82eb18ce67e4/subagents/workflows/wf_d4cbf4ac-6df/journal.jsonl`.
- Charter deliberation: `~/.synapsis/runs/2026-08-31-charter-admission-standard/` (`answer.md` readable; `run.json` authoritative); amendment commit `17dc693`.
- Prior art: `docs/plans/2026-07-08-mattpocock-skills-extraction-roadmap.md`, `docs/plans/2026-07-08-mattpocock-readoption-inventory.md`, `docs/agents/contract-decisions.md` (2026-07-05 through 2026-07-09 entries), `docs/reviews/2026-07-01-skill-library-capability-growth-review.md`.
