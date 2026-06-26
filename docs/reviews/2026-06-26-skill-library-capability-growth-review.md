---
type: review
date: 2026-06-26
scope: >-
  All 60 live skills (skills/ 38, skills-claude/ 5, plugins/git-cycle 8,
  plugins/handoff 4, plugins/review-family 5), plus docs/agents/charter.md, the
  live docs/agents/contract-decisions.md ledger, AGENTS.md, and reconciliation
  against the superseded 2026-06-19 capability-growth review.
reviewed_commit: 1c07409
method: >-
  57-agent read-only multi-agent workflow (13 cluster-readers mapped all 60
  skills with path:line citations; 9 external web sweeps -> 50 cited ideas; 7
  ideation lenses; adversarial One-Owner verification of every candidate against
  the live charter + ledger; synthesis), plus a 15-agent recovery run for 3
  ideation lenses lost to an over-strict StructuredOutput schema, plus manual
  re-verification of ~15 load-bearing citations. Honest process note in section 2.
posture: >-
  Read-only, capability-growth biased (favor new high-leverage skills and
  cognitive-offload breadth over pruning; expect the library to grow), judged
  under the build-and-prune charter (skills need no observed-friction proof,
  park, or ledger entry).
---

# Capability-Growth Review — `.agents` Skill Library (2026-06-26)

This review supersedes the 2026-06-19 capability-growth review (this document's predecessor, removed in the same change that added this one), whose backlog is now substantially built: 11 of its 18 build-now candidates shipped (`explain-codebase`, `pr-description`, `release-cut`, `migration-campaign`, `contract-change-propagation`, `keep-green`, `postmortem`, `research-capture`, `doc-drift-audit`, `spec-drift-reconcile`, `runbook-authoring`). Findings are re-derived from live source at `1c07409`, not resurrected from the prior artifact.

The library is mature on thinking, review, planning, continuity, and agent-meta. The growth frontier has moved: the new openings are the **Operate arc after "push"**, **divergence and advisory thinking** (the library is almost entirely convergent), and **breadth of domain cognitive-offload prompts**. Roughly 25 net-new candidates survived One-Owner verification.

## 1. Executive Summary — the 10 highest-value opportunities

| # | Opportunity | Kind | Why top-tier |
|---|---|---|---|
| 1 | **Stand up the Operate lane** — `incident-response`, `post-deploy-verification`, `outcome-verification`, `deploy-plan` | **system-level + 4 new** | The single biggest structural gap. `release-cut`'s last word is literally "push" (`release-cut:56`) with "no go/no-go gauge" (`:70`); `closeout-check:19` is local-only. Nothing owns live incidents, the post-ship watch, the rollout plan, or "did the goal get achieved." |
| 2 | **`implementation-review` domain + AI-code lens menu** | **existing-expansion** | Highest single-edit leverage: one conditional reference menu (SQL, perf, accessibility, concurrency) **folds 4 standalone candidates** into the owner that has depth only for security (`:94` flat list vs `:109-113` security depth), and supplies the import/method-resolution pass it explicitly delegates away (`:106`) — exactly where slopsquatted AI-code deps hide. Zero new routing surface. |
| 3 | **`ideate`** — divergent option-generation | **new skill** | The library is all convergence with no divergence producer: `making-recommendations:64` keeps generation/evaluation separate and refuses to widen; `next-steps:15` *consumes* "brainstorming notes" nothing creates. Cleanest gap, chat-first, high local fire-rate. |
| 4 | **The advisory trio** — `steelman`, `risk-register`, `premortem` | **3 new skills** | Genuinely widens the thinking lane with distinct cognitive *products*: one-sided charitable advocacy (vs `making-recommendations` ranking), a durable monitored risk ledger with tripwires (vs one-shot failure stories), prospective-hindsight to tripwires. High cognitive-offload; all hard to improvise under bias. |
| 5 | **`decision-record` / `adr-authoring`** | **new skill** | Carried-forward build-now, **and not charter-killed** (re-verified: no ledger entry). The gap is *genealogy* — status transitions and "superseded by" links so a reversal flips the old record instead of silently contradicting it. Reuses the existing `grill-with-docs/ADR-FORMAT.md`. |
| 6 | **`dependency-upgrade`** | **new skill** | Zero existing content (grep-empty), densest external support of any candidate (Renovate, agent-toolkit 7-step), prior build-now. Risk-tiers bumps; composes with `migration-campaign`'s burndown. |
| 7 | **`research-brief`** — frame a fuzzy research question | **new skill** | The missing "frame" in the frame -> run -> land triad: `deep-research` runs, `research-capture:20` lands ("never searches"), nothing structures the MECE sub-questions + sufficiency criteria *before* the run. |
| 8 | **`test-trust-audit`** — is-green-honest | **new skill (design-first)** | Nothing audits whether "green" proves anything before `keep-green`/`closeout-check` trust the gate (assertion-free tests, suites not wired to CI, swallowed exit codes). Lead with deterministic gate-honesty *facts*; fence vs `tech-debt-scan`. |
| 9 | **`migration-safety`** + `contract-change-propagation` handoff | **new skill + expansion** | DB DDL online-execution safety (locks, rewrites, non-concurrent indexes) — `contract-change-propagation:42` sequences *consumer compat* but never the lock physics that actually takes down prod. |
| 10 | **Close the last connective-tissue gaps** — `triage` batch-intake + `acceptance-map` status field | **system-level (2 expansions)** | The "reviewers die in chat" gap is **already mostly closed** (`plugins/review-family/CHANGELOG.md:11`, findings to triage pointers). What remains: `triage` has no documented batch findings-intake mode, and `acceptance-map`'s artifact has stable IDs but no status field, so `outcome-verification`/`implementation-review` can't consume it mechanically. |

## 2. Coverage And Limits

**Inspected (live, `main @ 1c07409`):** all 60 `SKILL.md` files (mapped by 13 cluster-readers with `path:line` citations), `agents/openai.yaml` plus behavior-affecting `references/`/`scripts/` where present, `docs/agents/charter.md`, `docs/agents/contract-decisions.md` (the live ledger), `AGENTS.md`, and the 2026-06-19 review (to reconcile what got built). ~15 load-bearing citations were personally re-verified against live source (every one accurate), and one error in the historical record was resolved (below).

**External search:** 9 parallel web sweeps produced 50 cited ideas (agentic patterns, dev tooling, skill ecosystems, code review, PKM, cognitive offload, autonomous loops, thought-partnering, ideation). Opportunistic, not exhaustive. URLs in section 7.

**Did NOT inspect / out of scope:** behavior validation (no forward tests or `skill-benchmark` runs — every "build-now" is a *design* judgment, not proof the skill fires well); full line-by-line reads of long reference/playbook files; `skills-archive/` (history); gated contracts (rules/hooks/`AGENTS.md` lines — this is a *skill* review). The global `deep-research` skill is treated as an available out-of-repo capability, not double-counted.

**Process honesty:** the first workflow used over-strict `StructuredOutput` schemas (`additionalProperties:false` plus many required nested fields) — the "don't bind large free-text judgments to strict schemas" trap. About 10 agents hit the retry cap and returned null; the run still completed on survivors (60/60 mapped, full synthesis) but lost 3 of 7 ideation lenses. Those lenses (upstream-discovery, cross-skill-glue, advisory/consulting) were recovered in a second run with loose schemas, and the residue was verified by hand. Net coverage is complete, but a few recovered candidates carry manual verification rather than an independent agent's.

**Correction to the historical record:** the project throughline claimed `adr-authoring`/`requirements-capture`/`change-communication` were "charter-killed." They are not — the live ledger (`contract-decisions.md`) has no entry for them. They were prior-review *build-now* candidates that were never built. Genuinely rejected ideas (`diff-security-review`, `post-merge-cleanup`, `commit-range-audit`, the Oracle/second-opinion subagent) were 2026-06-19 review rejections and were excluded here.

## 3. Current Library Map

| Cluster | Skills | Health |
|---|---|---|
| **Shaping & decision** | outcome-interviewer, design-exploration, making-recommendations, grill-me, grill-with-docs | **STRONG, one hole** — clarify -> explore/rank -> grill pipeline, but no *divergence* producer (`making-recommendations:64` refuses to generate; `design-exploration:24` jumps to 2-3) and no advisory variety |
| **Planning & decomposition** | implementation-planning, to-prd, to-issues, acceptance-map, next-steps | **STRONG** — settled-design -> PRD -> plan -> issues fully owned; `acceptance-map` artifact has IDs but no consumable status; no pre-impl trace-coverage audit |
| **Build & fix (MAKE)** | execute-plan, tdd, prototype, diagnose, simplify-code, keep-green | **MODERATE** — strong execution/stop-discipline; THIN on machine-readable status handoff (`execute-plan:26` prose-only) and gate-honesty |
| **Understand & maintain (MAINTAIN)** | explain-codebase, zoom-out, orient-status, improve-codebase-architecture, tech-debt-scan, doc-drift-audit | **STRONG discovery**, thin synthesis/continuity (no cross-finding orchestrator, no library-integrity sweep) |
| **Review & proof** | implementation-review, review-reviewer, scrutinize, scrutinize-skill, system-design-review, behavior-smoke-test, baseline | **STRONG, narrow** — best-developed cluster; domain depth only for security (`:94` vs `:109-113`); no AI-code lens (`:106` delegates it away); no spec-less peer review |
| **Git lifecycle / SHIP-prep** | closeout-check, merge-branch, pr-description, release-cut, gh-address-comments, gh-pr-review-loop, exiting-worktrees, git-hygiene | **STRONG to "push," then a cliff** — safe gatekeepers but no Operate arc beyond (`release-cut:56,70`) |
| **Operate (push -> operate -> learn)** | *(none)* | **MISSING ENTIRELY** — no incident, rollout, post-ship watch, observability, or outcome check |
| **Continuity & handoff** | load-handoff, save-handoff, search-handoffs, throughline | **STRONG**, brittle at scale (no format validator; `save-handoff:52` no transaction) |
| **Agent-meta / skill-building** | agent-facing-design, skill-ux-design, writing-principles, skill-squad, skill-benchmark, friction-to-guards, scrutinize-skill | **STRONG** — complete pre-deployment lifecycle; `skill-benchmark` judging uncalibrated |
| **Knowledge & doc authoring** | markdown-reformat, markdown-synthesis, research-capture, runbook-authoring, postmortem, caveman | **MODERATE** — strong one-off authoring; no research-*framing*, no requirements extraction, no doc-health refresh |
| **Change-management & cross-cutting** | contract-change-propagation, migration-campaign, spec-drift-reconcile | **STRONG internally**, assumes a mature artifact chain; DDL online-safety unowned |
| **Advisory / consulting / thought-partner** | *(only premortem-adjacent fragments inside scrutinize/grill)* | **THIN** — no steelman, risk-register, red-team, assumption-register |
| **Domain cognitive-offload prompts** | *(none)* | **MISSING** — no SQL, regex, concurrency, accessibility, observability expert-prompt |
| **External-docs / setup / triage** | claude-code-docs, openai-docs, setup-matt-pocock-skills, triage | **ADEQUATE** |

Strong: thinking, review/proof, planning, continuity, agent-meta. The growth frontier: Operate, advisory/divergence, domain cognitive-offload, and a few connective-tissue upgrades.

## 4. Existing-Skill Upgrade Opportunities

| Skill | Current value | Limiting factor | Proposed upgrade | Why more power | Evidence |
|---|---|---|---|---|---|
| **implementation-review** | Deep adversarial diff review | Domain depth only for security (`:94` flat list); delegates import-resolution away (`:106`) | Conditional `references/{sql,perf,accessibility,concurrency,ai-code}-lens.md` menu loaded by touched surface; AI-code lens carves the `:106` exclusion for agent-written diffs | Folds **4 standalone candidates** into the owner; gives each domain the depth security has; catches slopsquatted deps | `implementation-review:94,99,106,109-113` |
| **implementation-review** | Bounded Review Mode -> "Partial" | No "too big to review safely" verdict; test-adequacy is "negative cases?" not "would it fail if I broke it?" | Add a "split here" verdict with concrete seams + a mutation-testing heuristic | Actionable split; behavior-protection over line-coverage thinking | `implementation-review:97,129-133`; PR-size curve |
| **triage** | Creates/classifies one issue per finding | No documented *batch* findings-intake mode | Add a batch-intake mode: ingest a finding list from any reviewer/audit, dedup, classify, one issue each | Completes the findings -> tracker loop the reviewers already point at | `plugins/review-family/CHANGELOG.md:11`; reviewer tail pointers `implementation-review:185`, `scrutinize:85`, `tech-debt-scan:14`, `postmortem:52` |
| **acceptance-map** | Observable checks with stable IDs | Artifact has IDs but no status field — no mechanical consumer | Add a per-check status (pending/passed/failed/unverified) so `implementation-review`/`outcome-verification` consume it | Activates the artifact's central value | `acceptance-map:83-130,224` |
| **outcome-interviewer / design-exploration** | Shaping -> settled state | Settled state lives in the transcript; receiver re-interviews | Emit a compact "settled / open / chosen-direction / constraints / next-skill" capsule tail; absorb `explain-back` reflect-back mode; add handoff rows to reframe/requirements-capture | The warm-handoff brief (this **supersedes the rejected `shaping-brief` candidate**) | `outcome-interviewer:44,167-173,200-211` |
| **release-cut** | Semver + changelog, stops at push | Dead-ends at "push," disclaims go/no-go | Risk-branch the operate next-move: risky -> `deploy-plan`/`post-deploy-verification`; routine -> stop | Closes the SHIP -> OPERATE seam (one line, scope unchanged) | `release-cut:56,70` (plugin publish path) |
| **postmortem** | Tags items prevention/detection/mitigation | Tags don't drive routing | detection -> observability, mitigation -> runbook-authoring, recurring -> premortem; keep `/triage` as tracker | Turns tickets into a hardened operate posture | `postmortem:45,52` |
| **contract-change-propagation** | Interface blast-radius + compat sequence | Treats DDL as interface only, not lock/online physics | Hand DDL changes to `migration-safety`; name the axis split in both | A correct compat plan can still lock the table | `contract-change-propagation:14,42` |
| **making-recommendations** | Constraint-scored ranking | Guards bias but not noise; no transparent matrix; absorbs descope requests | Add the *Noise* Mediating-Assessments Protocol + a tradeoff-matrix output mode + route backlog-partition to `scope-cut` | Reproducible rankings, user owns the weighting | `making-recommendations:57,60,64,82`; MAP |
| **diagnose** | Feedback-loop RCA | Inherits flaky-test work but no non-determinism taxonomy; perf bisects without profiling | `references/non-determinism-taxonomy.md` (folds `deflake-test`) + optional USE-method profiling branch | Named playbook for test-internal non-determinism + disciplined profiling | `diagnose:43-45,107`; `keep-green:39` |
| **implementation-planning** | Ordered executable plan | Inside-view estimates only | Reference-class / outside-view step before trusting estimates | Most-validated planning debias (Flyvbjerg/Kahneman) | reference-class forecasting |
| **scrutinize** | Adversarial stress test | Surfaces assumptions implicitly; no constructive-advocacy counterpart | Rated Key Assumptions Check lens + a `steelman` handoff from its reject stance | Falsifiable assumptions pass; routes to the new advocacy lane | `scrutinize:54,58,59` |
| **skill-benchmark** | Variance-disciplined eval | Uncalibrated, metric-first judging | LLM-judge calibration (Cohen's kappa ~0.8) + error-analysis-from-traces before metrics | Trustworthy judge under every quantitative claim | Hamel evals |
| **agent-facing-design** | Gates added machinery | No concrete tool/response-design guidance | `references/tool-response-ergonomics.md` | Single-sources the most common surface it gates | writing tools for agents |
| **handoff (save/load/throughline)** | Session continuity | No format validation; garbage propagates (`save-handoff:52`) | Frontmatter validator at save/load + optional long-run progress-ledger/session-init smoke check | Stops silent corruption; serves the long-running-agent case | `save-handoff:52`; `throughline:29`; `load-handoff:59`; effective harnesses |
| **research-capture** | Lands research with provenance | No frame stage named | Name `research-brief` as the "frame" in a frame -> run -> land fence; share the provenance core with `requirements-capture` | Completes the research lifecycle, single-sources machinery | `research-capture:8,20,89-93` |

## 5. New Skill Candidates

Bias toward inclusion; confidence labelled. "Why separate (nearest owner)" folds in adjacents. All verified `is_dup=false` against live source unless noted.

### Build-now (genuine gaps — author and watch fire)

| Skill | Problem / trigger | Why separate (owner) | First-version scope | Risk | Confidence |
|---|---|---|---|---|---|
| **ideate** | Open problems get the first 2 obvious solutions / "brainstorm", "give me options" | Inverse of every convergence skill; `making-recommendations:64` refuses to generate, `next-steps:15` consumes notes nothing makes | Judgment-suspend flip + quantity target + provocation lenses (SCAMPER/inversion) + dedup to 3-5 + name downstream | Loader misroute (carve vs making-recommendations/design-exploration) | **high-confidence** |
| **incident-response** | Live incident, adrenaline tunnels on cause / "prod is down", "we're in an incident" | `postmortem:26` refuses the live moment, `diagnose:51` is loop-first (opposite of mitigate-first), `runbook-authoring:10` never runs | Severity + mitigate-first; live timeline (postmortem seed); rollback-vs-forward; comms; exit -> diagnose -> postmortem. Hard fence: stop at stabilized | Seam-bleed; advisory-not-actor (proof-boundary load-bearing); portable not local | **promising-experiment** |
| **post-deploy-verification** | Shipped, then walked away / "watch this rollout", "is the canary healthy?" | `closeout-check:19` local-only; built-in `verify` is pre-push; `behavior-smoke-test` is a contract proxy | Smallest signal set + bake window + per-signal abort threshold up front; watch where readable; healthy/abort verdict; blind -> label UNVERIFIED | Agent often can't read prod (resolve blind-deliverable fork); portable | **promising-experiment** |
| **outcome-verification** | Shipped to move a metric; nobody checks it did / "did it actually work?" | Closes `outcome-interviewer:8`'s loop; `closeout-check`=local-done, `implementation-review`=code-vs-spec — none ask "did the goal happen" | Fail-fast gate: any real-world signal reachable? If not, one-line "unverifiable-here," stop. Else one observable criterion + verdict | Becomes a structured shrug if no signal (gate mitigates); goal-invention | **promising-experiment** |
| **decision-record / adr-authoring** | Decisions evaporate; reversals silently contradict / "record this decision", "this supersedes X" | `grill-with-docs` offers ADRs as a by-product (`:82-90`); nothing owns capture-from-any-source + lifecycle genealogy. **Not charter-killed** | Capture a settled decision into a numbered ADR (reuse `ADR-FORMAT.md`) + maintain status transitions and "superseded by" links | Boundary vs grill-with-docs; must reuse not fork the format | **high-confidence** (carried-forward) |
| **dependency-upgrade** | Risk-blind bumps / "upgrade our dependencies safely", "is this major safe" | Grep-empty; `migration-campaign` owns mechanical multi-site, not tiering/changelog/soak; `tech-debt-scan` flags read-only | Risk-tier (patch auto / minor review / major migration-guide), group co-deps, soak, coverage as net; compose `migration-campaign` for breakage | Boundary vs migration-campaign; local fire uncertain (portable) | **high-confidence** (carried-forward) |
| **research-brief** | Fuzzy question, improvised decomposition / "help me scope this research" | `deep-research` runs (different product: a no-search approvable plan), `research-capture:20` never searches | Restate -> 3-7 MECE sub-questions + sufficiency line each + source types + scope + sequence; names deep-research/research-capture; never searches | Over-trigger vs deep-research's thin preface; route muddy-goal -> outcome-interviewer | **promising-experiment** |
| **steelman** | Confirmation bias; dismissed option never gets a fair hearing / "argue the other side", "best case against my choice" | One-sided by contract (vs `making-recommendations:60` even-handed ranking); *defends* (vs `scrutinize` attacks); argues (vs `grill-me` asks) | Charitable restatement + 2-4 strongest arguments + load-bearing assumptions + mandatory "this is advocacy, here's the strongest surviving counter" | Drift into balanced analysis; manufactured confidence (mitigations built in) | **high-confidence** |
| **premortem** | Commitment momentum suppresses failure modes / "premortem", "assume this already failed" | Prospective hindsight (past-tense causes -> tripwires); distinct from `scrutinize` (adjudicates) and `postmortem` (after) | Frame "it's N months later and it failed" -> past-tense causes -> pre-mitigations + dated tripwires -> route to triage; **no verdict** | Word collides with `scrutinize:28,54` pre-mortem lens — carve required | **promising-experiment** (carve) |
| **sql-review** | Query/ORM/migration footguns (N+1, SARGability, cartesian joins) / "review this query", "why is this slow" | `implementation-review:32` needs a spec + diff; `diagnose` needs a repro. Single-artifact audit vs schema+plan is a different evidence model | One SQL artifact + optional schema/EXPLAIN + dialect -> named-rule footgun checklist -> ranked findings + safer rewrite; read-only | Margin vs bundled `/code-review`; dialect drift (keep thin) | **promising-experiment** |
| **regex-craft** | ReDoS, unanchored, greedy/lazy, "works on 3 examples" / "write/vet a regex", "this regex hangs" | No owner (only incidental mentions); not a spec review or repro hunt | Build or vet in a named dialect; **must-match/must-not-match table executed** (not eyeballed); ReDoS check; flags justified | Verification theater if it asserts instead of runs (execution mandate load-bearing) | **promising-experiment** |
| **migration-safety** | DDL locks/rewrites/breaks running code / "is this migration safe to deploy?" | `contract-change-propagation:42` is compat-level not lock-level; `migration-campaign` is codemods not DDL | DDL + engine -> unsafe-ops catalog -> safe expand-migrate-contract rewrite per op -> name the PONR; never run | Engine-specific (pin it); co-fires with contract-change-propagation (name the axis split) | **promising-experiment** |
| **observability-instrumentation** | Code ships under-instrumented; next incident starts by adding logging / "what should I log/trace here" | `diagnose` consumes telemetry, `runbook-authoring` owns alert *response*, `system-design-review`/`tech-debt-scan` review read-only — none author it | Name real units-of-work deserving spans + failure modes a future incident must see; PII + cardinality guards; conventions as appendix | Niche/improvisable if it leads with the checklist (judgment must be the spine) | **promising-experiment** |
| **what-if / scenario-storming** | Ship blind to edge/adversarial/scale/temporal cases / "what are all the cases", "edge cases for X" | Sibling to `ideate` but generates *situations* not solutions; `behavior-smoke-test:34` asks the author to invent them by hand | One pass -> labeled scenario set across a fixed taxonomy -> rank the 2-5 most likely to break this design -> name downstream | Blur vs `grill-with-docs:70`; generic-checklist non-job | **promising-experiment** |
| **red-team** | Designed from the defender's chair; abuse surface invisible / "how would an attacker/competitor break this" | Adversarial *intent* (vs `premortem` accidental); forward/design-time (vs `implementation-review:109` post-code); generative actor -> path (vs `system-design-review` quality screen) | Name adversaries+goals -> attack paths (entry -> step -> payoff) -> rank by ease x payoff -> raise-cost mitigations; **not a repo/secret scan** | Security-park adjacency (carve to non-scan abuse-modeling, or park beside them) | **promising-experiment** |
| **requirements-capture** | Raw source -> traceable classified requirements / "pull the requirements out of this transcript" | `to-prd:8` says don't-interview-just-synthesize + publishes; `research-capture` lands *findings* not requirements; `markdown-synthesis:18` strips provenance | Extract statements -> provenance + explicit-vs-inferred -> MoSCoW/functional classify -> flag conflicts/gaps. **Single-source `research-capture`'s provenance core** | High machinery overlap with research-capture (build as shared core + two templates) | **high-confidence** (carried-forward) |
| **library-integrity-check** | Nothing sweeps the 60-skill library for cross-ref/orphan/symlink/parse drift / "audit the skill library" | `doc-drift-audit` is doc-vs-code; the sync/validate scripts are single-skill — none orchestrate a library-wide sweep | Resolve every skill -> skill reference, detect orphans/dangling, parse-check all 60, symlink consistency, bundled-name collisions -> `/triage` | Must compose the existing scripts, not reinvent; uniquely self-applicable here | **medium / high-confidence** (carried-forward) |

### Design-first (real gap — settle one boundary before building)

| Skill | Problem | Why separate / what to settle | Confidence |
|---|---|---|---|
| **deploy-plan** | Risky change ships all-at-once with no abort criteria | Owns rollout-strategy + go/no-go that `release-cut:70` refuses; **must single-source `runbook-authoring`'s rollback/irreversibility machinery**, not copy it | promising-experiment |
| **risk-register** | One-shot failure stories aren't a monitored ledger | Durable L x I + tripwire + owner ledger for one committed plan; `scrutinize:59` pre-mortem *generates*, this *scores+monitors*. Settle the premortem -> register feed | promising-experiment |
| **test-trust-audit** | "Green" can be hollow before keep-green/closeout trust it | Lead with deterministic gate-honesty *facts* (doc-drift-audit-shaped); demote mutation heuristic to a labeled judgment tier; **fence vs `tech-debt-scan` test-debt** | promising-experiment |
| **skill-router** | 60 skills won't fit in working memory for a compound goal | Sequences *the toolbox* into an ordered chain (vs `next-steps` sequencing findings); explicit-invoke (`next-steps:4` precedent); reads live descriptions | promising-experiment |
| **concurrency-review** | Races/deadlocks can't be caught by testing | Static shared-state x accessor audit, no spec/repro; **settle vs `tech-debt-scan` first** — fold as a category playbook, or narrow standalone only if it misroutes today | promising-experiment |
| **trace-coverage** | Orphans before any drift or code exists | Pre-impl bidirectional PRD <-> check <-> issue completeness audit; distinct from `spec-drift-reconcile` (drift) and `implementation-review:67` (needs code); narrow/portable | promising-experiment |
| **assumption-check** | Load-bearing assumptions stay implicit pre-commit | `scrutinize:58` already tags 3 of 4 fields adversarially; the unowned slice is a *forward, non-adversarial, per-assumption cheap-test plan*. Decide standalone vs scrutinize-mode | promising-experiment (collision-narrow) |
| **scope-cut** | Drawing the v1 cut-line under a constraint | Partitions a backlog ship/defer/drop (vs `making-recommendations:3` picking one, `next-steps` sequencing in-scope). Decide standalone vs making-recommendations mode | speculative |

### Parked / better-as-an-upgrade

| Candidate | Disposition | Why |
|---|---|---|
| **security-audit** | **PARKED — do not build** | Whole-repo security scanning is a **live JP-ratified park** (`contract-decisions.md`, pass 10); reopen trigger = first observed pre-existing-code vuln a diff review missed. Build only when it fires |
| **api-design** | **Fold -> `design-exploration`** | Designing an API contract *is* design-exploration specialized (`:8,25`); add `references/api-contract-checklist.md` |
| **shaping-brief** | **Fold -> `outcome-interviewer`/`design-exploration` capsule upgrade** | Every shaping skill already closes with this capsule (`outcome-interviewer:200-211`); collision-kill as a standalone |
| **explain-back** | **Fold -> `outcome-interviewer` reflect-back mode** | Thin; collides with the always-loaded trust-but-verify rule (`CLAUDE.md:25`) |
| **problem-reframe** | **Fold -> `outcome-interviewer` reframe mode** (or `ideate`'s problem side) | Highest overlap — `outcome-interviewer:8,38` already notices incomplete framing |
| **reproduce-claim** | **Reject — owned** | `CLAUDE.md:24` (trust-but-verify) + `review-reviewer:17,54` (re-runs checks) + `diagnose` Phase 1 already own it |

## 6. Cross-Library Power Gaps

1. **The Operate arc has no owners and dead-ends at "push."** Pain: after `release-cut:56`, risky changes ship with no rollout strategy, no live watch, no incident lane, no outcome check — regressions are caught by users, not a gate. Fix: build the Operate lane (section 5) and wire `release-cut` -> `deploy-plan`/`post-deploy-verification` -> `outcome-verification`, with `postmortem` tag-routing into it.
2. **No divergence producer feeds the convergence skills.** Pain: `next-steps:15` and `making-recommendations` *consume* options nothing *produces*. Fix: `ideate` (solutions) + `what-if` (situations).
3. **The advisory lane is one-note.** Pain: the library can rank and adjudicate but can't *advocate* (steelman), *monitor risk* (register), or *attack with intent* (red-team). Fix: the advisory trio.
4. **Nothing audits whether "green" proves anything.** Pain: `keep-green`/`closeout-check` trust a gate that hollow tests pass silently. Fix: `test-trust-audit` + the `implementation-review` mutation heuristic.
5. **No review prior for machine-written code.** Pain: `implementation-review:106` excludes the import/method-resolution pass — exactly where hallucinated/slopsquatted APIs hide. Fix: the AI-code lens fold.
6. **The MAKE cluster emits no machine-readable status artifact.** Pain: you can't ask "what's still broken / untested?" and get a consumable answer (`execute-plan:26` prose-only). Fix: a small shared DONE/CONCERNS/BLOCKED status-ledger convention, routed through `agent-facing-design`.
7. **DB migrations have no online-safety review.** Pain: a correct compat sequence (`contract-change-propagation:42`) can still lock a table. Fix: `migration-safety`.
8. **The research lifecycle is missing its "frame."** Pain: fuzzy questions go straight to an expensive wandering search. Fix: `research-brief` (frame -> run -> land).
9. **Findings -> tracker is *mostly closed*** (a finishing touch, not a gap). Pain: the last 10% — `triage` has no batch-intake mode and `acceptance-map` has no consumable status. Fix: the two section-4 upgrades. (Credit: `plugins/review-family/CHANGELOG.md:11` already closed the systemic version.)

## 7. External Inspirations

| Idea (source) | Maps to |
|---|---|
| MADR's value is lifecycle/genealogy, not templating (adr.github.io/madr) | `decision-record` |
| Klein project premortem — past-tense causes, ~30% more surfaced | `premortem` |
| SCAMPER / lateral-thinking provocation lenses (IxDF) | `ideate` |
| Risk-tier bumps, soak releases, coverage-as-net (softaworks/agent-toolkit, Renovate) | `dependency-upgrade` |
| `strong_migrations` unsafe-DDL catalog + safe multi-deploy path (github.com/ankane/strong_migrations) | `migration-safety` |
| AI-code review runs the mechanical import/slopsquat pass humans skip (~5.2% pkg-hallucination) (tenki.cloud) | `implementation-review` AI-code lens |
| Mutation-testing as a review heuristic (codecov) | `test-trust-audit` + impl-review |
| PR size/quality curve, split at ~200 LOC (em-tools.io) | impl-review Bounded Mode |
| Noise Mediating-Assessments Protocol (theuncertaintyproject.org) | `making-recommendations` |
| Reference-class forecasting / outside view (Wikipedia) | `implementation-planning` |
| Error-analysis-first eval + calibrated judge (hamel.dev) | `skill-benchmark` |
| Effective long-running-agent harness — progress ledger + session-init smoke check (anthropic.com) | `handoff` plugin |
| Writing tools for agents (anthropic.com) | `agent-facing-design` ref |
| CIA Key Assumptions Check / "what would have to be true" (Roger Martin) | `assumption-check`, `scrutinize` lens |
| MECE issue-trees / hypothesis-driven consulting | `research-brief`, `steelman`, `risk-register` |
| STRIDE / attack-trees, abuse-case-driven design | `red-team` |
| Diataxis doc-quadrant audit + Google "keep docs alive, trim like bonsai" (diataxis.fr) | *not-now* — a `doc-health` refresh skill (Knowledge lifecycle gap; lower priority) |
| Trail of Bits ~20 audit-workflow security skills (github.com/trailofbits/skills) | `security-audit` (parked-pending-trigger) |

## 8. Recommended Next Moves

Ordered to test the highest-power *new* ideas fastest, cheapest-and-cleanest first.

1. **[implementation-planning-ready] Build `ideate`** (dual-runtime `skills/`), then `behavior-smoke-test` it on a "give me options for X" prompt under convergence pressure. Cleanest gap, highest local fire, no collision — the fastest proof the divergence lane works.
2. **[implementation-planning-ready] Author the `implementation-review` domain + AI-code lens menu** as single-sourced references (folds `sql-review`/`accessibility`/`concurrency-review`/`review-ai-code` + the slopsquat pass). Highest leverage; follows the review-family plugin publish path.
3. **[implementation-planning-ready] Build the `steelman` + `decision-record` pair** — both high-confidence, clean gaps, chat-first, fast to smoke-test. `decision-record` reuses `grill-with-docs/ADR-FORMAT.md` (single-source, no fork).
4. **[design-discussion] Settle the Operate lane as one system** before authoring any of it: resolve `deploy-plan` <-> `runbook-authoring` single-sourcing (rollback machinery shared, not copied) and the `release-cut` -> `post-deploy-verification` -> `outcome-verification` wiring. Design `incident-response`, `post-deploy-verification`, `outcome-verification`, `deploy-plan` together (they share seams); all first-to-prune/portable.
5. **[implementation-planning-ready] Build `dependency-upgrade` + `research-brief`** — both lower-collision, research-backed, carried-forward. Re-verify `dependency-upgrade`'s boundary vs `migration-campaign` at build time.
6. **[design-discussion] Settle the three `tech-debt-scan`-adjacent design-firsts** (`test-trust-audit`, `concurrency-review`, `assumption-check`): each needs one carve (fence vs tech-debt-scan / scrutinize:58) before authoring. Decide fold-vs-standalone per the observed-misroute test.
7. **[implementation-planning-ready] Land the two connective-tissue upgrades** — `triage` batch findings-intake + `acceptance-map` status field — and fold the rejected `shaping-brief`/`explain-back`/`problem-reframe` into `outcome-interviewer` as capsule/reflect/reframe modes.
8. **[read-only-review] Gate-check before any Operate/security build:** confirm `security-audit`'s park trigger has actually fired (an observed pre-existing-code vuln a diff review missed) — else leave it parked. Assess local fire-rate for the portable domain skills (`sql-review`, `regex-craft`, `migration-safety`, `observability-instrumentation`) — all first-to-prune.
9. **[design-discussion] Decide `red-team`'s placement** — non-scan abuse-modeling standalone vs parked beside the security parks — and the advisory `risk-register`/`scope-cut` carves vs `making-recommendations`.
10. **[read-only-review] Run `library-integrity-check`'s job manually once** (cross-ref/orphan/symlink sweep across all 60+ skills) after 3-5 new skills land — validates the concept and surfaces real drift before deciding whether to author it as a standing skill.

## Evidence Boundary

The library map (60/60), the synthesis, and the recovered lenses were produced by read-only agents under `path:line` citation discipline. About 15 load-bearing citations were personally re-verified against live source (all accurate), along with the `adr`/`requirements`/`change-communication` non-kill and the already-closed findings-to-triage gap (`plugins/review-family/CHANGELOG.md:11`). Four recovered candidates (`steelman`, `requirements-capture`, `scope-cut`, `problem-reframe`) carry manual verification rather than an independent agent's. No behavior was validated — every "build-now" is a design judgment, not proof the skill fires well; under build-and-prune that is the intended bar (build, watch it fire, prune freely). Citations are true at `1c07409`; re-verify against live source before acting.
