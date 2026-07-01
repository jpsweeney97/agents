---
type: review
date: 2026-07-01
scope: >-
  All 75 live skills (skills/ 53, skills-claude/ 5, plugins/git-cycle 8,
  plugins/handoff 4, plugins/review-family 5), read against docs/agents/charter.md,
  AGENTS.md, the live docs/agents/contract-decisions.md ledger, and the superseded
  2026-06-26 capability-growth review. Judged on GLOBAL merit (leverage in any repo
  + cognitive-offload to the human), with cognitive-offload weighted heaviest.
reviewed_commit: 1011287
method: >-
  213-agent read-only multi-agent workflow (wf_92421e75-32b): 5 live cluster-readers
  mapped all 75 SKILL.md files with path:line citations; 8 blind divergent generators
  (SDLC-seam, cognitive-offload-procedure, technical-domain, external-practice,
  adjacency, negative-space, non-code, AI/data-app) + 3 blind careful-default controls;
  canonicalized to 69 candidates; each pipelined through a strict One-Owner + kill-list
  gate -> default-to-refute skeptic -> merit score; a completeness critic + 5-candidate
  second pass. The built/folded/killed/parked lists were inlined into every agent.
posture: >-
  Read-only, capability-growth biased (favor new high-leverage skills and cognitive-offload
  breadth over pruning; expect the library to grow), cognitive-offload weighted heaviest,
  judged under the build-and-prune charter (skills need no observed-friction proof, park,
  or ledger entry). NOTE the honest method limit in section 2: the scorer under-discriminated
  (59 of 62 One-Owner survivors scored near-uniformly high), so this review's discrimination
  rests on control convergence + the completeness critic + live-source grounding, NOT the raw
  per-candidate scores.
---

# Capability-Growth Review — `.agents` Skill Library (2026-07-01)

This review supersedes the 2026-06-26 capability-growth review (its predecessor, removed in the same change that added this one), whose frontier is now substantially built. Shipped since then: the **Operate arc** (`deploy-plan` — absorbing post-deploy-verification as its gauge-read — `outcome-check`, `incident-response`, `observability-instrumentation`); the **advisory/divergence lane** (`ideate`, `steelman`, `premortem`, `red-team`; `risk-register` killed); **four domain producers** (`observability-instrumentation`, `migration-safety`, `dependency-upgrade`, `regex-craft`); `decision-record`; `scope-cut` standalone; and the §4 owner-expansions (`implementation-review` domain + AI-code lenses + Split-required verdict, `making-recommendations` MAP + tradeoff-matrix, `diagnose` non-determinism taxonomy, `implementation-planning` outside-view pass, the shaping warm-handoff capsule, `agent-facing-design`'s Tool Returns lens). Findings are re-derived from live source at `1011287`, not resurrected from the prior artifact.

**The frontier has moved.** All three blind careful-default reviewers and the completeness critic independently reached the same conclusion: opening new *lanes* is largely done. The library is now mature and densely self-fenced on every axis it began with — thinking, shaping, planning, make/fix, review/proof, git-lifecycle, operate, continuity, agent-meta. Growth is no longer a missing spine; it is **new distinct OWNERS in a few thin bands, plus one repeatable producer factory.** With cognitive-offload weighted heaviest, the five openings are: **(A) pre-build de-risking & self-trust auditing**, **(B) design-time application security**, **(C) the domain-producer factory, re-run**, **(D) the reactive security/response corner + the dependency lifecycle**, and **(E) a few clean high-reach singles the ship/change lanes deliberately punt.**

## 1. Executive Summary — the frontier in five openings

The honest top pick, by convergence and boundary-cleanliness (not raw score):

| # | Opening | Standout candidate(s) | Convergence signal | Disposition |
|---|---|---|---|---|
| A | **Pre-build de-risking & self-trust auditing** | **`assumption-check`**, `test-trust-audit`, `characterization-tests` | `assumption-check` is the ONLY candidate all **3/3 blind controls** named + the strongest surfacing of two cluster-readers; `test-trust-audit` 2/3 controls | **build-now** (all three) |
| B | **Design-time application security** | **`authorization-design`**, `injection-safe-inputs` | The critic's *"single strongest addition available"* — the one cognitive-offload hole **every lens missed**; OWASP #1/#3 have no producer | **build-now** |
| C | **The domain-producer factory, re-run** | `resilience-policy`/`idempotency-design`, `cache-design`, `time-handling`, `money-decimal`, `rate-limit-backpressure`, `webhook-design`, `pagination-design` | The `regex-craft`/`migration-safety` mold proved repeatable; the biggest raw cognitive-offload *volume* | **build-now, as ONE lane with a footgun-ordered build queue** |
| D | **Reactive security/response + dependency lifecycle** | `secret-leak-response`, `security-incident-response` (branch), `dependency-adoption`, `dependency-advisory-response` | Fills what the parked whole-repo `security-audit` left empty *without* reopening it; the dependency triad has three moments, only *upgrade* is owned | **build-now / design-first-carve** |
| E | **Clean singles the lanes punt** | **`resolve-conflicts`**, `perf-optimize` (proactive) | `resolve-conflicts` is genuinely unowned across all 75 — every landing skill explicitly bails on non-ff/rebase; high reach, recurring | **build-now / fold-or-carve** |

**The single recommendation, cognitive-offload first:** build **`assumption-check`** (cleanest carve, pure cognitive-offload, 3/3 control convergence), then **`authorization-design`** (+ its sibling `injection-safe-inputs`), then the test-safety pair **`test-trust-audit` + `characterization-tests`**, then **`resolve-conflicts`**. Treat **Opening C as a standing factory** — run the proven producer mold highest-footgun-first on the cheaper hand-author + adversarial-review tier, since the *shape* is already known. Everything in A/B/C/E proves by an executed table or advisory plan, not a coverage verdict — the no-certificate discipline holds throughout.

## 2. Coverage And Limits

**Inspected (live, `main @ 1011287`):** all 75 `SKILL.md` files (mapped by 5 cluster-readers with `path:line` citations, grouped shaping/plan · make/debug/review · understand/change/domain · operate/git · continuity/meta/docs), read against `docs/agents/charter.md`, the live `docs/agents/contract-decisions.md` ledger, `AGENTS.md`, and the 2026-06-26 review (to reconcile what got built). The built-since delta and the full killed/folded/parked list were inlined into every agent, so nothing already-shipped or already-rejected was re-proposed as net-new (the gatekeeper confirmed this per-candidate).

**Method honesty — the over-proposal.** The per-candidate scorer under-discriminated: **59 of the 62 One-Owner survivors scored `cognitive_offload=high` at `rank_hint` 7–9**, because bias-toward-inclusion plus a cognitive-offload-weighted rubric inflates almost every domain procedure to "high offload / build-now." A flat list of 59 build-nows is not a frontier. **This review's discrimination therefore does NOT rest on those scores.** It rests on three sturdier signals: **(1) where the 3 blind careful-default controls independently converge** (the strongest anti-strawman signal — a candidate all three name unprompted is real); **(2) the completeness critic's demotions and its one missed-by-everyone hole**; and **(3) the cluster-readers' live-source grounding** (a thin spot cited to a real `SKILL.md:line` is a real seam). Where those three agree, confidence is high; where only the raw score is high, the candidate is treated as factory-fodder or watch-list, not a headline.

**External search:** the external-practice lens ran from model training knowledge, **not live web sweeps** (a deliberate robustness choice for a long background run). Section 8's inspirations are therefore illustrative, not a fresh 2026 web survey; treat them as directional.

**Did NOT inspect / out of scope:** behavior validation (no forward tests or `skill-benchmark` runs — every disposition is a *design* judgment under the build-and-prune bar, not proof a skill fires well); full reads of long `references/` files; `skills-archive/` (history); gated contracts (rules/hooks/AGENTS.md lines — this is a *skill* review). The global `deep-research` and bundled Claude Code skills (`verify`, `run`, `code-review`, `security-review`) are treated as available capabilities, not double-counted.

## 3. Current Library Map (5 live cluster-readers, `1011287`)

| Cluster | Health | The thin spot that matters |
|---|---|---|
| **Shaping, decision & plan-formation** (outcome-interviewer, design-exploration, making-recommendations, grill-me, grill-with-docs, ideate, steelman, premortem, red-team, scope-cut, implementation-planning, to-prd, to-issues, acceptance-map, next-steps) | **STRONG — saturated** | No **forward, non-adversarial pre-build de-risking** (`grill-me` is interactive/no-artifact, `premortem` works backward from asserted failure, `scrutinize` tags assumptions but plans no cheap confirmations). Also: value-ranking of N *non-rival* items is half-owned (between `making-recommendations`, `next-steps`, `scope-cut`). |
| **Build–debug–review** (execute-plan, tdd, prototype, simplify-code, diagnose, keep-green, implementation-review, review-reviewer, scrutinize, scrutinize-skill, system-design-review, behavior-smoke-test, baseline) | **STRONG — most mature** | **No safety-net over untested legacy code** before a risky change (`simplify-code:18` *requires* a runnable check; `tdd` disowns tests-after; `diagnose` writes one bug test) → `characterization-tests`. **No honest-green audit** of a standing suite (`keep-green:52` guards its own gate forward only; `implementation-review:99` mutation-checks only *changed* tests) → `test-trust-audit`. **Proactive perf** drops out (`diagnose:103-110` is regression-gated). |
| **Understand & evolve** (explain-codebase, zoom-out, orient-status, improve-codebase-architecture, tech-debt-scan, doc-drift-audit, contract-change-propagation, migration-campaign, spec-drift-reconcile, dependency-upgrade, migration-safety, regex-craft, observability-instrumentation) | **STRONG — precise fences** | Same characterization-net gap from the change-safety side. **Prove-truly-unused-then-remove** (safe delete) is half-owned (`contract-change-propagation` maps removal blast-radius but stops at the plan). **Non-DDL data backfill** and **component-level cutover/strangler** fall outside `migration-safety`'s schema scope. |
| **Ship & operate** (closeout-check, merge-branch, pr-description, release-cut, gh-address-comments, gh-pr-review-loop, exiting-worktrees, git-hygiene, deploy-plan, outcome-check, incident-response, postmortem, runbook-authoring) | **STRONG — dense, well-fenced** | **Merge/rebase conflict resolution is unowned across all 75** — `merge-branch:81`, `exiting-worktrees:121`, and `git-hygiene:37` all explicitly bail the moment a branch diverges → `resolve-conflicts`. Remote **CI-red triage on a PR** falls between `keep-green` (local) and `diagnose` (owned by `keep-green` on inspection — see §6). |
| **Continuity, meta & knowledge** (load/save/search/throughline, agent-facing-design, skill-ux-design, writing-principles, skill-squad, skill-benchmark, friction-to-guards, markdown-*, research-capture, decision-record, caveman, triage, claude-code-docs, openai-docs) | **STRONG — lifecycle seams** | Real seams but **tenet-tensioned or already-owned**: nothing populates the `archive/` the handoff skills read (deliberate no-lifecycle tenet); a guard-*retirement* audit's "never-fired" signal is route-absence, which the charter + AGENTS.md explicitly bar; doc-grounding covers only Claude Code + OpenAI. See §6 for why these fold rather than build. |

Every cluster is **STRONG**. There is no missing spine — only adjacencies. That is itself the headline: the library has matured past lane-opening.

## 4. The Five Growth Openings

### Opening A — Pre-build de-risking & self-trust auditing (highest convergence)

The library now readily *produces* plans, checks, code, and green test suites. Nothing asks whether what it cheaply produces is **honest**, or cheaply de-risks a plan's silent bets **before** commitment. This band is the strongest-convergence opening on the board.

- **`assumption-check`** — **the standout of the whole review.** Enumerate a settled plan's load-bearing assumptions, rank each by (load-bearing × uncertainty), and attach the *cheapest confirm-or-kill probe* to each, as a durable artifact — forward, non-adversarial, renders no verdict. All **3/3 blind controls** named it unprompted; two cluster-readers called it their single strongest surfacing. Carved clean from `grill-me` (interactive/adversarial/no-artifact), `premortem` (backward from asserted failure), `red-team` (motivated adversary), and `scrutinize`'s Assumptions Audit (adversarial — *tags* assumptions, plans no confirmations). Pure cognitive-offload: the human otherwise composes the enumerate/rank/probe prompt and checks nothing was skipped. `shape-known` → hand-author.
- **`test-trust-audit`** — read-only sweep of an existing **green** suite for the ways green lies: skipped/xfail, assertion-free/tautological tests, mocks asserting mocks, snapshot rubber-stamping, coverage-without-assertion, flaky-quarantine drift — plus a sampled mutation probe → an evidence-led findings list, **no score** (no-certificate-clean). Controls 1 & 3 + a cluster-reader. Distinct from `keep-green` (guards its own gate forward) and `implementation-review` (mutation-checks only *changed* tests).
- **`characterization-tests`** — author a behavior-snapshot net (golden-master/approval) over *existing, working, untested* code before refactoring/upgrading/migrating, then prove the net fails on a deliberate mutation. It is silently a **precondition of `simplify-code` and `dependency-upgrade`**, owned by neither (`tdd` disowns tests-after). Control 1 + both make/change cluster-readers ranked it their highest-offload local candidate.
- `test-strategy` (design the suite's shape — levels, mock-vs-real, contract boundaries — before writing) — control 2, but fuzzier/planning-shaped and weaker offload → **design-first**.

### Opening B — Design-time application security (the hole every lens missed)

The completeness critic's headline: the entire security lane on the board skews to **response and advisory**. The two highest-frequency, highest-consequence *design-time* footgun families in ordinary backend work have **no producer at all**.

- **`authorization-design`** — the critic's *"single strongest addition available."* Design the access-control model for one resource/endpoint/feature before coding: enumerate `(subject, action, resource)` triples, choose the model (RBAC/ABAC/ownership), place enforcement at the right layer, close the object-level/ownership gap behind IDOR/BOLA, guarantee multi-tenant isolation, map privilege-escalation paths — and **prove it with an executed must-allow/must-deny access matrix** (the validated producer mold). OWASP #1 (broken access control). Broad reach, clean boundary, high offload.
- **`injection-safe-inputs`** — the design-time sibling. Design untrusted-input handling for one trust boundary: identify each sink (SQL, shell, path, HTML/JS, LDAP, template), apply the sink-correct defense (parameterization, output-encoding, canonicalization, allowlist), handle mass-assignment and unsafe deserialization, set size/type limits — **prove it with an executed must-block payload table.** OWASP #3. Distinct from the parked whole-repo `security-audit` (a *scanner*) and from `implementation-review`'s AI-code lens (a *diff* review, not a design producer).
- `auth-session-design` (credential flow, session-vs-JWT, token lifetime/rotation/revocation, CSRF, secure-cookie, logout-all) — **design-first-carve**: ship separately only if the authn footgun catalog is genuinely distinct from authz; else pair as one `app-security-design` producer.

### Opening C — The domain-producer factory, re-run (the biggest cognitive-offload *volume* — treat as ONE lane)

The four built producers proved a **repeatable mold**: a bounded high-footgun domain + a worked-out footgun catalog + an executed proof table (or advisory plan). It generalizes far past the first four. **This is one strategic opening, not twenty frontier items** — counting each producer separately over-counts the frontier. Run it as a standing factory, footgun-density × reach first, on the cheaper hand-author + adversarial-review tier (the shape is known).

Build queue (highest-footgun-first, all `shape-known` → hand-author):

- **Distributed-systems correctness:** `resilience-policy` (timeouts / retry+backoff+jitter / circuit-breaker / fallback / dead-letter for one integration), `idempotency-design` (duplicate-delivery safety: keys, dedup, at-least-once), `cache-design` (key design, invalidation, staleness bounds, stampede protection), `rate-limit-backpressure`, `async-processing-design` (queue/pipeline correctness), `webhook-design`, `pagination-design`.
- **Correctness domains:** `time-handling` (TZ/DST/serialization, executed table), `money-decimal` (rounding/precision).
- **Integration:** `third-party-integration` (wire in a new external API/SDK — its resilience half overlaps `resilience-policy`, its vetting half overlaps `dependency-adoption`; likely a fold or a thin composer).
- **AI/LLM-app sub-cluster (already dense — CONTAIN, do not over-populate):** `llm-eval-design`, `prompt-injection-defense`, `rag-retrieval-design`, `grounding-guards`, `pii-data-handling`, `dataset-curation`, `model-migration`. The critic explicitly warns this fast-moving lane is the best-covered and at risk of *over*-population — resist adding more (e.g. prompt-design, agent-tool-loop-design) until a concrete unowned job surfaces, and prefer folding `structured-output-contract` toward `grounding-guards`/`llm-eval-design` over growing the cluster.

Fold-seams to settle at build time (the critic named these): `resilience-policy` vs `idempotency-design` (keep distinct — caller-failure-handling vs duplicate-delivery-safety — but review the seam); `auth-session-design` vs `authorization-design` (pair unless authn is genuinely distinct); `backfill-safety` vs `migration-safety` (backfill may be `migration-safety`'s non-DDL data mode).

### Opening D — Reactive security/response + the dependency lifecycle

The parked whole-repo `security-audit` deliberately left the *reactive* corner empty. Specific response procedures fill it **without reopening the scanner** (and the gatekeeper confirmed the *detection* variants correctly fold — see §6).

- **`secret-leak-response`** — contain a leaked credential/key/token end-to-end (rotate → revoke → audit misuse → purge → notify) in the correct order. Controls 1 & 3. **Fold-tension with `incident-response`** — settle standalone-vs-branch at build.
- **`security-incident-response`** — a security-breach **branch off `incident-response`**: contain an active compromise without destroying forensic evidence, rotation ordering, don't-tip-the-attacker discipline, scope-capture-before-remediation, disclosure/legal handoff. **design-first-carve** (fold vs branch vs standalone).
- **The dependency lifecycle has three moments — adopt, upgrade, respond-to-advisory — and only *upgrade* is owned** (`dependency-upgrade`). Add **`dependency-adoption`** (vet a *new* dependency before pulling it: health/bus-factor, license, supply-chain/typosquat, transitive weight, does stdlib/an existing dep already suffice — the *adopt* go/no-go, distinct from the version bump; controls 2 & 3) and **`dependency-advisory-response`** (a CVE/GHSA lands on a dep you already ship: is the vulnerable path reachable in our config, how urgent, patch vs mitigate vs accept; control 3).

### Opening E — Clean high-reach singles the ship/change lanes punt

- **`resolve-conflicts`** — resolve a merge/rebase conflict (or the non-fast-forward landing decision) safely: read both sides' intent, avoid silently dropping code, re-verify semantics and tests post-merge. **Genuinely unowned across all 75 skills** — `merge-branch:81`, `exiting-worktrees:121`, and `git-hygiene:37` all explicitly bail here. High reach, recurring, high-risk, strong cognitive-offload + proof discipline. This is arguably the cleanest single build on the board after Opening A.
- **`perf-optimize`** (proactive/steady-state, no regression baseline: baseline → profile → localize → optimize → prove-behavior-preserved for code that was always slow) — controls 1 & 3; fills `diagnose`'s regression-gated perf gap. **fold-or-carve**: `diagnose` is one generalization (drop the regression gate) away from owning it.
- `prove-unused-then-remove` (safe delete) — **fold-leaning** into `contract-change-propagation` (removal mode) + `simplify-code`; the reachability half is real offload, the residue thin.

## 5. New-Skill Candidates By Disposition

### Build-now (clean gaps — author and watch fire)

| Skill | Job it owns | Why distinct (nearest owner) | Tier |
|---|---|---|---|
| **assumption-check** | Forward per-assumption cheapest-test plan before build | `scrutinize`:58 tags adversarially, plans no confirmations; `grill-me` no artifact; `premortem` backward | high — 3/3 control convergence |
| **authorization-design** | Design an access-control model + executed allow/deny matrix | No producer; OWASP #1; distinct from parked `security-audit` scanner | high — critic's top miss |
| **injection-safe-inputs** | Design sink-correct untrusted-input handling + executed must-block table | No producer; OWASP #3; distinct from `implementation-review` diff lens | high |
| **test-trust-audit** | Audit a green suite for fake-green; findings list, no score | `keep-green`:52 forward-only; `implementation-review`:99 changed-tests only | high — 2/3 controls |
| **characterization-tests** | Pin legacy behavior under a net before a risky change | Silent precondition of `simplify-code`:18 + `dependency-upgrade`; `tdd` disowns tests-after | high |
| **resolve-conflicts** | Safely resolve a merge/rebase conflict / non-ff landing | Every landing skill bails (`merge-branch`:81, `exiting-worktrees`:121, `git-hygiene`:37) | high — unowned across all 75 |
| **dependency-adoption** | Vet + decide adopting a NEW dependency (adopt go/no-go) | `dependency-upgrade` owns the *bump*, not the *adopt* decision | moderate — 2/3 controls |
| **dependency-advisory-response** | Decide exposure/urgency/fix when a CVE hits a shipped dep | Third moment of the dependency lifecycle; unowned | moderate |
| **secret-leak-response** | Contain a leaked credential end-to-end in the right order | Response, not detection; fold-tension with `incident-response` | moderate |
| **Opening-C producers** | One footgun-dense domain each, proven by executed table | The `regex-craft`/`migration-safety` mold; each a distinct domain | high volume — run as a factory |

### Design-first-carve (settle one boundary before building)

| Skill | Boundary to settle |
|---|---|
| **security-incident-response** | Branch off `incident-response` vs standalone vs fold with `secret-leak-response` |
| **auth-session-design** | Pair with `authorization-design` as one `app-security-design` producer, or ship separately only if the authn catalog is genuinely distinct |
| **perf-optimize** | Standalone vs a `diagnose` proactive-branch (drop the regression gate) |
| **test-strategy** | Fuzzy/planning-shaped; carve vs `tdd`/`acceptance-map` or hold |
| **backfill-safety** | A distinct non-DDL data-reprocessing safety producer vs a `migration-safety` data mode |
| **scenario-storm / what-if** | Situation-space generator vs redundancy with `ideate`+`premortem` (leftover thread; watch redundancy) |
| **cutover-plan** | Component-level strangler/cutover vs `migration-safety`+`deploy-plan` |

### Fold / demote / park (the honest other half)

| Candidate | Disposition | Why |
|---|---|---|
| **skill-router** | **Fold → `next-steps` + the runtime loader** | Durable half = `next-steps` sequencing (each move names its owner); roster-knowledge half = the loader's job + a router the `agent-facing-design` gate resists; its substance (the roster) is stale-by-design under build-and-prune |
| **groundedness-screen / hallucination-screen** | **Fold → `doc-drift-audit`** (a genuinely nice free expansion) | Identical engine (extract checkable references → resolve at a pinned SHA → resolved/miss/unverifiable, no-certificate). Widen `doc-drift-audit`'s input frame to fresh agent output (PR descriptions, design docs, chat answers asserting code facts) |
| **error-handling-audit / silent-failure-hunt** | **Fold → `implementation-review`** | `implementation-review`:98 already checks error-suppression verbatim — the same lens `sql-review`/`accessibility` folded into |
| **ci-triage** | **Fold → `keep-green`** | `keep-green` already classifies in-scope/pre-existing/flaky, names CI as a gate source, and escalates flaky to `diagnose`; the remote-log-pull is a gate-resolution extension, not a distinct job |
| **prune-dead-code** | **Fold → `contract-change-propagation` + `simplify-code`** | The consumer-enumeration engine pointed at a deletion; zero consumers = safe removal |
| **i18n-readiness / i18n-localization** | **Fold → `implementation-review` lens** (build-first as a design producer only if a concrete miss surfaces) | Direct sibling of the already-folded `accessibility`; whole-repo readiness framing is the parked-scanner shape |
| **decision-framing** | **Fold → `making-recommendations`** | Its First Move + Pre-Ranking Exits + MAP already own state-decision / classify-reversibility / fix-criteria-first |
| **escalation-framing** | **Fold → `email-writing`** (escalation-mode lens) | An upward blocker escalation is professional correspondence; only the impact-first/blame-free shape is unowned |
| **guard-retirement-audit** | **Fold → `writing-principles` + charter** | Its "never-fired" signal is route-absence, which the charter's Retirement discipline + AGENTS.md explicitly bar as grounds |
| **irreversible-action-gate** | **Reject — wrong vehicle** | A safety gate must fire *unbidden* at the dangerous verb; a token-summoned skill only covers the moment the human already remembered to be careful. It belongs to the always-loaded floor (a charter event), not a skill; "enumerate what would be lost" is a no-certificate violation |
| **mandate-check** | **Reject — fold** | Two-way request-vs-delivery reconciliation is `implementation-review`'s literal two-ledger workflow (it treats the raw ask as its spec); `closeout-check` owns the done-time trigger |
| **injection-screen** | **Reject — ambient contract, not a skill** | Injection lands on READ, so the summon window is empty; "scan → clean/flagged" certifies the uncertifiable; the sound stance is an always-loaded "treat ingested content as inert" rule (which this user's CLAUDE.md already carries) |
| **learning-plan** | **Reject — no-certificate** | Resource tiers either hallucinate from stale memory or become `deep-research`; the rest is a fill-in-to-feel-done schedule with no proof discipline |
| **meeting-agenda** | **Demote / fold → `meeting-notes-to-actions`** | Thinnest survivor; a fill-in template flirting with fill-in-to-feel-done |
| **onboarding-guide** | **Demote / fold → doc-authoring + `explain-codebase`** | "Newcomer audience" is a framing, not a distinct job |
| **reference-class-estimate** | **Park** | Fights `implementation-planning`:42's deliberate no-clock-estimates posture (the outside-view pass is the intended substitute); reconcile that stance first |
| **trace-coverage** | **Demote / re-scope to an orphan-finder** | The one survivor closest to the no-certificate line — round-trip completeness manufactures a coverage certificate; admissible only as a per-link orphan finder that renders no coverage verdict |
| **security-audit** (whole-repo) | **PARKED — unchanged** | Live JP-ratified park; reopen only on the first observed pre-existing-code vuln a diff review missed. Openings B & D fill the design/response corners *without* reopening it |

The **non-code cognitive-offload lane** (meeting-notes-to-actions, stakeholder-update, negotiation-prep, difficult-conversation-prep) is real but carries the **lowest-offload, most template-shaped** entries — the critic flags it as the most over-proposed band. Build selectively, one at a time, and watch hard for fill-in-to-feel-done; `email-writing` already anchors JP's personal end.

## 6. Existing-Skill Expansion Opportunities (the free folds)

These are near-zero-cost owner-expansions the review surfaced, distinct from new builds:

- **`doc-drift-audit`** — widen its input frame/trigger to include *fresh agent-produced artifacts* (PR descriptions, design docs, review comments, chat answers, commit messages) that assert code facts. Its resolve-every-reference engine + no-certificate disclaimer *is* a groundedness/hallucination screen; the only difference is the input surface (One-Owner: specializing to a surface neither qualifies nor disqualifies).
- **`implementation-review`** — the error-suppression lens (`:98`) already covers `error-handling-audit`; note it explicitly so the fold is visible and the candidate does not resurface.
- **`keep-green`** — the CI-red-triage job is already its gate-resolution scope; a one-line note that CI logs are a gate source closes `ci-triage`.
- **`diagnose`** — a proactive-perf branch (drop the regression gate) is the cleanest home for `perf-optimize` if the standalone carve does not hold.
- **`contract-change-propagation`** — a removal/safe-delete mode frames the zero-consumer special case that `prune-dead-code` wanted.
- **`email-writing`** — an escalation-mode lens (impact-first ordering, blame-free, cross-channel) absorbs `escalation-framing`.

## 7. Cross-Library Power Gaps

1. **Nothing de-risks a plan before build or audits whether "green" is honest.** The library generates (ideate), critiques (review family), and imagines failure (premortem) — but nothing cheaply proves the load-bearing beliefs before commit, or checks that a green suite proves anything. Fix: Opening A (`assumption-check` + `test-trust-audit` + `characterization-tests`).
2. **Design-time application security has no producer.** The whole security lane is response/advisory; OWASP #1 (access control) and #3 (injection) — the highest-frequency design footguns — are unowned. Fix: Opening B (`authorization-design` + `injection-safe-inputs`).
3. **The producer mold is under-mined.** `regex-craft`/`migration-safety` proved a repeatable, high-offload pattern that generalizes to a dozen more footgun-dense domains. Fix: Opening C as a standing factory.
4. **The dependency lifecycle is one-third owned** (only *upgrade*), and the reactive-security corner the parked scanner left empty has no owner. Fix: Opening D.
5. **Conflict resolution falls through every landing skill.** All eight git-lifecycle skills own the clean path and bail the moment a branch diverges — the actual conflict work is unowned across all 75. Fix: `resolve-conflicts` (Opening E).
6. **Lifecycle/retirement seams are real but tenet-tensioned, not clean builds** — nothing populates the handoff `archive/` (deliberate no-lifecycle tenet), and a guard-retirement audit's core signal is route-absence (charter-barred). These are correctly *not* frontier builds; noting them prevents re-proposal.

## 8. External Inspirations (directional — from training knowledge, not a fresh web sweep)

| Idea | Maps to |
|---|---|
| CIA Key Assumptions Check / "what would have to be true" (Roger Martin) | `assumption-check` |
| OWASP Top 10 #1 Broken Access Control (IDOR/BOLA), #3 Injection | `authorization-design`, `injection-safe-inputs` |
| Mutation testing + assertion-density as green-honesty signals | `test-trust-audit` |
| Golden-master / approval / characterization testing (Feathers, *Working Effectively with Legacy Code*) | `characterization-tests` |
| `strong_migrations`-style worked footgun catalog + executed proof, generalized | Opening C producer mold |
| Idempotency keys, retry+backoff+jitter, circuit breakers, dead-letter queues (SRE/distributed-systems canon) | `resilience-policy`, `idempotency-design` |
| Cache invalidation + stampede/thundering-herd protection | `cache-design` |
| Credential-rotation runbooks; CVE/GHSA reachability triage; SLSA/typosquat supply-chain vetting | Opening D |
| Semantic-merge / three-way conflict discipline | `resolve-conflicts` |

## 9. Recommended Next Moves

Ordered cheapest-cleanest-and-highest-convergence first; build-tier tagged.

1. **[hand-author] Build `assumption-check`** (dual-runtime `skills/`), then `behavior-smoke-test` it on a "here's my plan, what am I assuming?" prompt. The cleanest carve, 3/3 control convergence, pure cognitive-offload — the fastest proof the pre-build de-risking lane is real.
2. **[hand-author] Build `authorization-design`**, then **`injection-safe-inputs`** — the design-time security whitespace, each proven by an executed allow/deny (or must-block) matrix. Settle `auth-session-design` fold-vs-pair before/at build.
3. **[hand-author] Build the test-safety pair `test-trust-audit` + `characterization-tests`** — self-trust auditing + the silent precondition of `simplify-code`/`dependency-upgrade`. Both no-certificate-clean (findings list / behavior net, no coverage verdict).
4. **[hand-author] Build `resolve-conflicts`** — the one thing all 75 skills punt; high reach and recurrence.
5. **[standing factory, hand-author + adversarial review] Run Opening C** highest-footgun-first (`resilience-policy`/`idempotency-design` → `time-handling` → `money-decimal` → `cache-design` → …), settling the named fold-seams per build. The shape is the proven mold — reserve `skill-squad` only where a producer's SHAPE is genuinely open.
6. **[design-first-carve] Settle Opening D** — the security-response corner (`secret-leak-response` standalone-vs-branch; `security-incident-response` off `incident-response`) and the dependency lifecycle (`dependency-adoption`, `dependency-advisory-response`).
7. **[free folds] Land the §6 expansions** — widen `doc-drift-audit`'s input frame (folds groundedness-screen), and add the one-line fold notes to `implementation-review`/`keep-green`/`contract-change-propagation`/`email-writing`.
8. **[watch, do not build] Hold** the non-code comms lane (build one at a time, watch for fill-in-to-feel-done), `reference-class-estimate` (until the anti-estimation posture is reconciled), `trace-coverage` (re-scope to an orphan-finder or drop), `skill-router` (loader duplication), and the AI/LLM sub-cluster (contain — resist over-populating a dense fast-moving domain). Leave `security-audit` parked.

## Evidence Boundary

The library map (75/75), the candidate field, and the fold/kill reasoning were produced by read-only agents under `path:line` citation discipline in workflow `wf_92421e75-32b` (213 agents, ~8.2M tokens). **No behavior was validated** — every disposition is a design judgment under the build-and-prune bar, not proof a skill fires well. The review's discrimination rests on **3-way blind-control convergence + the completeness critic + live cluster-reader grounding, NOT the per-candidate scores**, which under-discriminated (59 of 62 One-Owner survivors scored near-uniformly high — the over-proposal failure mode this section flags). The external inspirations (§8) are from training knowledge, not a live web sweep. Citations are true at `1011287`; re-verify against live source before acting. Live files, drift checks, and a future review outrank this record.
