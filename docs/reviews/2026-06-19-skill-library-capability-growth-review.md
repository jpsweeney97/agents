---
type: review
date: 2026-06-19
scope: >-
  All 48 live skills (skills/ 29, skills-claude/ 4, plugins/git-cycle 6,
  plugins/handoff 4, plugins/review-family 5), plus docs/agents/charter.md,
  the 345-line docs/agents/contract-decisions.md ledger, and AGENTS.md.
reviewed_commit: 0755adc
method: >-
  62-agent multi-agent Workflow (wf_703c90e6-b4f): parallel readers mapped every
  skill with path:line citations; 7 parallel external web sweeps (32 cited
  ideas); 8 gap-axis lenses; consolidation to 36 unique candidates; each
  candidate adversarially verified against the live charter + ledger and
  adjacent SKILL.md files for duplication / settled-out status.
posture: >-
  Read-only, capability-growth biased (favor new high-leverage skills over
  pruning), judged under the relaxed build-and-prune charter (skills/commands
  need no observed-friction proof, park, or ledger entry).
---

# Capability-Growth Review — `.agents` Skill Library

This is the clean re-run of the outward capability-growth review under the now-relaxed build-and-prune charter (`charter.md` `## Reversibility Class`, `f8964f1`). The two prior `docs/reviews/` capability-growth artifacts were removed because each was shaped by a since-superseded rule — 2026-06-18 by the Codex skill-list-truncation mechanism (`0a3c11d`), 2026-06-19 by the observed-friction admission bar (`0755adc`). This record re-derives findings from live source rather than resurrecting either artifact.

---

## 1. Executive Summary — the 5 highest-value opportunities

The library is **mature on thinking, review, and continuity; genuinely thin on MAKE / MAINTAIN / SHIP** — confirmed by the map, not assumed. Under build-and-prune (`charter.md:42-54`), a new skill needs no friction proof, park, or ledger entry, so the bias is toward building and watching. Verdict spread across 36 verified candidates: **18 build-now, 6 expand-existing, 8 design-first, 4 reject**.

| # | Opportunity | Kind | Why it's top-tier |
|---|---|---|---|
| **1** | **Stand up the SHIP lane** — `pr-description`, `release-cut`, `change-communication` | **3 new skills** (build-now; first two high) | The git-cycle family spans dirty-tree → closeout → land → worktree-exit → PR-*response*, but **nothing authors a PR body, derives a version bump/changelog, or shapes an outward change update**. `implementation-review` even *consumes* a PR description as a spec input it never produces (`plugins/review-family/skills/implementation-review/SKILL.md:37`). Thinnest, highest-frequency zone. |
| **2** | **Build `explain-codebase`** — read-only whole-repo onboarding map | **New skill** (build-now, **high**) | The missing *first move* in any unfamiliar repo. `orient-status` reports where work *stands* (`skills/orient-status/SKILL.md:137-157`); `zoom-out` is one named area, not the whole repo (`skills/zoom-out/SKILL.md:8,20-25`); neither produces a structural orientation map + where-to-start checklist. |
| **3** | **Build the large-mechanical-change lane** — `migration-campaign` + `contract-change-propagation` | **2 new skills** (build-now, **high**) | No skill owns sharding a codemod/rename/framework-bump into pilot-first, burndown-tracked, per-shard-verified units, or classifying an interface diff (breaking vs additive) and enumerating consumers. `to-issues` slices *vertically* — the opposite shape (`skills/to-issues/SKILL.md:44-48`). |
| **4** | **Build `fan-out-attempts`** — parallel N-attempt best-of with objective fan-in | **New skill** (build-now, **high**) | A genuinely *new reusable agent capability*: `execute-plan` runs one subagent per plan task in sequence (`skills/execute-plan/SKILL.md:21`); nothing dispatches N independent attempts at one gradeable task and selects by an objective signal. Both runtime primitives (subagents, worktrees) are live. |
| **5** | **Close the artifact-persistence & cross-skill-handoff gap** | **System-level** (a cluster of expand-existing edits + one design-first skill) | The biggest *connective-tissue* weakness: nearly every review/judgment skill **dies in chat** — `implementation-review` (`:176-194`), `scrutinize` (`:138`), `system-design-review` (`:66-70`), `baseline` (`:33-36`) — none route a blocker/finding to `to-issues`/`triage`, and `acceptance-map`'s central artifact has **no consumer** (`skills/acceptance-map/SKILL.md:291-293`). |

Beyond the top 5, **12 more build-now skills** are ready (knowledge-authoring: `adr-authoring`, `postmortem`, `research-capture`, `runbook-authoring`, `doc-drift-audit`; MAINTAIN: `dependency-upgrade-triage`, `dependency-upgrade-execute`, `keep-green`, `spec-drift-reconcile`; plus `requirements-capture`, `library-integrity-check`).

---

## 2. Coverage And Limits

**Inspected (live working tree, `main @ 0755adc`):**

- All **48 live skills** — `SKILL.md` read in full + `agents/openai.yaml` where present + behavior-affecting `references/`/`examples/`/`scripts/` skimmed.
- Governance: `docs/agents/charter.md` (incl. `## Reversibility Class`), the 345-line `docs/agents/contract-decisions.md`, `AGENTS.md`. Every candidate grepped against both for settled-out/parked/rejected status.
- The five SessionStart `--check` canaries (for `library-integrity-check` scoping).

**Did NOT inspect / out of scope:**

- **Behavior validation** — no forward tests, dry runs, or `skill-benchmark` runs. Every "build-now" is a *design* judgment, not proof the skill fires well.
- Full line-by-line reads of long reference/playbook files (skimmed for behavior).
- `skills-archive/` (history). The **global `deep-research` skill** is not in this repo and is treated as an available out-of-repo capability — not double-counted; candidates checked against it to avoid duplication.
- Gated contracts (rules/AGENTS.md lines/hooks) — deliberately excluded; this is a *skill* capability-growth review.

**External search:** 7 parallel sweeps (agentic work-loops, dev-tool automation, AI-assistant skill ecosystems, code-review, knowledge-management, AI-reliability/eval, lifecycle workflows) → 32 ideas with cited URLs. Opportunistic, not exhaustive.

**Data caveat:** the gap-lens agents proposed *clusters* of sibling skills, so several candidates cite each other as "adjacent skills" that don't exist yet (`keep-green`, `dependency-upgrade-triage`, `migration-campaign`, `triage-failures`, `eval-design` were all named as adjacents before any exists). The verification pass caught every one against live files — verdicts are sound, but **treat each candidate's scope as standalone**, not as relying on an unbuilt sibling.

---

## 3. Current Library Map

| Cluster | Skills | Health |
|---|---|---|
| **Shaping & decision** (judgment) | outcome-interviewer, design-exploration, making-recommendations, grill-me, grill-with-docs | **STRONG** — handoffs are cold prose; design-exploration thinnest (74 lines, no examples) |
| **Planning & decomposition** | implementation-planning, to-prd, to-issues, acceptance-map, next-steps | **STRONG** — forward-only (no spec-drift reconciliation); acceptance-map has no consumer |
| **Build & fix (MAKE)** | execute-plan, tdd, prototype, diagnose, simplify-code | **MODERATE** — construction & cause-finding covered; **missing**: drive-known-change-to-green loop, parallel best-of, failure triage |
| **Codebase understanding & maintenance (MAINTAIN)** | improve-codebase-architecture, tech-debt-scan, orient-status, zoom-out | **THIN** — no whole-repo onboarding, no doc-drift audit, no dependency upgrades, no migration orchestration |
| **Review & proof (SAFETY)** | implementation-review, review-reviewer, scrutinize, scrutinize-skill, system-design-review, behavior-smoke-test, baseline | **STRONG** — best-developed; **systemic flaw: every reviewer dies in chat, no finding→tracker handoff** |
| **Git lifecycle & PR (SHIP)** | closeout-check, exiting-worktrees, gh-address-comments, gh-pr-review-loop, git-hygiene, merge-branch | **STRONG on local landing & PR-response; THIN on PR-body authoring, release/changelog, post-deploy comms** |
| **Continuity & handoff** | load-handoff, save-handoff, search-handoffs, throughline | **STRONG** — most mature cluster |
| **Agent-facing / skill meta** | agent-facing-design, skill-ux-design, writing-principles, skill-benchmark, friction-to-guards | **STRONG** — validated to completion (Era 4) |
| **Knowledge & doc authoring** | markdown-reformat, markdown-synthesis (+ caveman comms) | **THIN** — no ADR, research-capture, runbook, postmortem |
| **External docs reference** | claude-code-docs, openai-docs (+ global deep-research) | **ADEQUATE** |
| **Setup / triage / config** | setup-matt-pocock-skills, triage | adequate (config-dependent) |

**Strong:** thinking, review/proof, continuity, agent-meta. **Thin (growth frontier):** MAKE-drive-to-done, MAINTAIN, SHIP, upstream onboarding, durable knowledge authoring.

---

## 4. Existing-Skill Upgrade Opportunities

Strongest theme: **persistence and connective tissue** — high-value skills that produce ephemeral chat output or hand off cold.

| Skill | Current value | Limiting factor | Proposed upgrade | Why more power | Evidence |
|---|---|---|---|---|---|
| **acceptance-map** | Observable proof checks from a settled source | Designed as the proof bridge but **no consumer reads it** | Teach `implementation-review` to verify each check's "Passes when" against the diff; teach `implementation-planning` self-review to map tasks→check IDs | Activates the artifact's central value | `skills/acceptance-map/SKILL.md:11,291-293` |
| **implementation-review** | Heavy adversarial findings packet | **Chat-only**; a blocker dies with the session | Opt-in "export findings" → `to-issues`/`triage`, one issue per blocker | Findings reach a tracker | `plugins/review-family/skills/implementation-review/SKILL.md:176-194` |
| **scrutinize / system-design-review** | Execution-readiness / design critique | Verdicts & probes end in chat | Opt-in artifact + route blockers to `acceptance-map`/`to-issues`; SDR offers `design-exploration`/`grill-me` onward | Review value persists & chains | `scrutinize/SKILL.md:138`; `system-design-review/SKILL.md:66-70` |
| **tech-debt-scan** | Ranked evidence-anchored backlog | Terminates at a backlog; names only `next-steps` | Opt-in step converting quick-wins/high-leverage rows → tracker issues, preserving evidence anchor | Closes audit→action loop | `skills/tech-debt-scan/SKILL.md:27-31` |
| **diagnose** | Feedback-loop bug RCA | Perf compressed to one line; loop-construction prose-only | Expand line-89 perf branch into a USE-method resource sweep; promote loop archetypes to copyable templates | Anti-anchoring sweep + scaffolding | `skills/diagnose/SKILL.md:89,21-29` |
| **implementation-review** | Diff/PR adversarial review | No AI-authorship lens | Add `references/ai-code-lens.md` + trigger note (hallucinated/typosquatted deps, happy-path-only, plausible-but-wrong APIs) **with explicit carve-out of line 117** | AI diffs fail differently; user works mostly with agent-written diffs | `implementation-review/SKILL.md:105-124,117` |
| **writing-principles** | Obligation-only minimization | No staleness lens; doesn't name CONTEXT.md | Add a light "stale: contradicted by current code" probe (route depth-work to `baseline`); add CONTEXT.md. **Drop** redundant "minimization mode" (already its Core Move) | Catches docs that lie without bloating a judgment skill | `writing-principles/SKILL.md:13-16,30-35` |
| **making-recommendations** | Constraint-scored ranking | "Verify unstable facts" rule has no path to research/web | Name `deep-research`/web as the resolving move; add optional "Sourcing Options" candidate-discovery path | Turns the honesty rule from disclaimer into action | `skills/making-recommendations/SKILL.md:100,118` |
| **execute-plan** | Reliable per-task execution | All progress in orchestrator context; lost on session break | Optional progress ledger (`.agents/execute-plan/progress.md`) + resume step | Survives context loss mid-plan | `skills/execute-plan/SKILL.md:57` |
| **outcome-interviewer / design-exploration / grill-me** | Shaping & stress-test | Hand off by *naming* a lane, carrying no payload | Optional structured handoff brief the receiver reads first | Eliminates re-interview in the shaping chain | `outcome-interviewer/SKILL.md:250`; `design-exploration/SKILL.md:63` |
| **to-prd / to-issues** | Tracker publication | Safety-critical label mapping rests on model judgment, no post-publish check | Post-publish round-trip verification; pre-publish dependency-cycle/HITL-label validation | Confirms intended state landed | `to-prd/SKILL.md:21`; `to-issues/SKILL.md:68` |
| **merge-branch** | FF-only local landing | Any non-FF case is a dead stop | Add a non-FF decision branch (named rebase / explicit-merge with exact commands) | Covers a large class of real landings | `merge-branch/SKILL.md:161-164` |
| **exiting-worktrees** | Worktree teardown | One-sided lifecycle (exit only) | Companion enter/setup mode with branch-naming guards | Owns the worktree lifecycle end-to-end | `exiting-worktrees/SKILL.md:247-248` |
| **save-handoff / throughline** | Continuity | Capture quality unguarded; drift misses in-place edits | Pre-write "could a cold session resume from this?" gate; structural self-audit of `sources_folded` | Forcing function for resumability & integrity | `save-handoff/SKILL.md:19`; `throughline/SKILL.md:88` |
| **markdown-synthesis** | Multi-source synthesis | No faithfulness/provenance audit even when wanted | Opt-in "faithfulness pass" spot-checking claims against sources (in chat, not the doc) | Audit fidelity without re-reading sources | `markdown-synthesis/SKILL.md:161` |
| **reproduce → diagnose/tdd** | (rejected as new skill) | — | One-line pointer from `tdd`/`triage` into `diagnose` Phase 1 as the canonical repro lane | Exposes the reuse seam without forking diagnose | `diagnose/SKILL.md:14,18-29` |
| **review-large-diff → implementation-review** | (folds in) | Bounded mode is *reactive* slicing | Add a "choose the review unit" step (commit-by-commit / file-group / stacked) before bounded mode | Structure-driven first cut for 1000+-line diffs | `implementation-review/SKILL.md:140-144` |

---

## 5. New Skill Candidates

All verified `is_dup=false` / `is_settled=false` unless noted.

### Build-now (ready to author and watch fire)

| Proposed skill | User problem | Likely trigger | Why separate | Adjacent | First-version scope | Key risk | Evidence/inspiration |
|---|---|---|---|---|---|---|---|
| **explain-codebase** (high) | "Orient me on this unfamiliar repo" | `/explain-codebase` | Structural map ≠ status (`orient-status`) ≠ one area (`zoom-out`) ≠ change-rec (`improve-codebase-architecture`) | orient-status, zoom-out | Read-only recon ladder (manifests, fingerprints, entry points, dep direction, build/test cmds, hot paths) → map + where-to-start checklist | Routing overlap with orient-status — fence descriptions | `orient-status/SKILL.md:137-157`; [super-productivity onboarding](https://super-productivity.com/blog/ai-codebase-onboarding-guide/) |
| **pr-description** (high) | Authoring a reviewer-oriented PR body | "write the PR description" | Review-response skills assume the body exists; none author it | gh-pr-review-loop, closeout-check, merge-branch | Synthesize diff + governing intent + closeout-check's verification record → structured draft; publish only on explicit authority; lives in git-cycle | "How-verified" fabrication — must source from the real record | `implementation-review/SKILL.md:37`; `closeout-check/SKILL.md:30-31` |
| **release-cut** (high) | Derive semver bump + changelog from commits | "cut a release / bump version" | Nothing consumes the conventional-commit convention git-hygiene writes | closeout-check, merge-branch, git-hygiene | Walk commits since last version (repo has **0 git tags** → anchor on plugin.json/CHANGELOG), map types→bump, flag under-tagged breaks from diff, draft changelog; stop at drafts | Tag assumption (corrected); draft-only must be firm | `AGENTS.md:67-68`; [release-please](https://github.com/googleapis/release-please) |
| **migration-campaign** (high) | Shard a large mechanical change | "roll out this codemod/rename across the repo" | `to-issues` slices *vertically* — opposite shape | to-issues, execute-plan | Partition (dir/CODEOWNERS) → pilot riskiest shard → durable burndown → per-shard verify → optional `to-issues`; compat layer advisory only | Misroute vs to-issues/execute-plan | `to-issues/SKILL.md:44-48`; [Moderne large-scale changes](https://www.moderne.ai/blog/large-scale-code-changes) |
| **contract-change-propagation** (high) | Interface diff blast-radius | "what breaks if I change this API/schema" | Classify breaking-vs-additive + enumerate consumers is unowned | system-design-review, to-issues | Take diff/two versions/ref-range → classify each delta → enumerate call sites (rg) → versioning/deprecation plan; *judgment, not parsers* | 5 formats → keep diff as supplied input | `system-design-review/SKILL.md:44`; [oasdiff/breaking-changes](https://dev.to/flarecanary/how-to-detect-api-breaking-changes-before-they-hit-production-257p) |
| **keep-green** (med, foundational) | Drive a just-made change back to passing lint+test | "get this green" | tdd is red-first new behavior; diagnose is cause-*unknown*; this is known-target convergence | tdd, diagnose, closeout-check | Discover lint/test cmds → run → fix only what the change broke → re-run; **stop conditions are the value** (retry cap, oscillation, same-failure-twice); hand unknown-cause→diagnose | Thin-wrapper without sharp stop rules; boundary vs closeout-check | `tdd/SKILL.md:66-96`; [Aider lint/test loop](https://aider.chat/docs/usage/lint-test.html) |
| **dependency-upgrade-triage** (med) | Risk-rank a bump/bot PR | "should I merge this Dependabot PR" | Fixed dependency-risk procedure; tech-debt-scan punts CVEs | tech-debt-scan, making-recommendations | Ordered factors (semver delta, changelog vs *this repo's* call sites, CI-vs-flake, maintainer trust, soak-age) → merge/hold/escalate + per-factor evidence | Misroute vs making-recommendations; don't become a security scanner | `tech-debt-scan/SKILL.md:135-138`; [robertknight gist](https://gist.github.com/robertknight/7e9a42e1ff9e29001f2cfa44d515cf47) |
| **dependency-upgrade-execute** (med) | Apply a bump + migrate call sites | "upgrade X to vN" | MAINTAIN niche unowned; tech-debt-scan/simplify-code forbid manifest edits | tech-debt-scan, simplify-code | One dep/invocation: classify delta → read changelog as ground truth → enumerate call sites → apply (codemods) → drive green; own the whole arc | Manifest/lock edits protected; doc-grounding can fail silently | `tech-debt-scan/SKILL.md:25-27`; [Fowler codemods](https://martinfowler.com/articles/codemods-api-refactoring.html) |
| **adr-authoring** (med) | Settled decision → numbered, lifecycle-tagged ADR | "record this as an ADR" | Thinking lanes settle decisions but none author the durable record | grill-with-docs, making-recommendations, improve-codebase-architecture | Confirm settled → number → pick weight (Y-statement default) → supersession-by-new-record → maintain index; **point at** existing `ADR-FORMAT.md` | Don't break the 2 existing cross-refs; keep lean | `grill-with-docs/ADR-FORMAT.md:15`; [ADR templates/ops](https://hidekazu-konishi.com/entry/architecture_decision_records_templates_and_operations.html) |
| **postmortem** (med) | Blameless retrospective artifact | "write a postmortem" | diagnose Phase 6 dies in the commit message | diagnose, to-issues, triage | Facts-before-analysis: timeline+timestamps, impact, primary-trigger vs aggravating, where-we-got-lucky, owned/dated action items → `docs/postmortems/`; route items to to-issues | Low fire-frequency; keep sections as provocations | `diagnose/SKILL.md:115-126`; [PagerDuty template](https://response.pagerduty.com/after/post_mortem_template/) |
| **research-capture** (med) | Land external research as a durable source-traced doc | "save this research to the repo" | Durable counterpart to ephemeral `deep-research`; `markdown-synthesis` strips citations | markdown-synthesis, to-prd | `docs/research/<topic>.md` with freshness date, claim→source provenance, open-questions; *lands*, doesn't re-search | May collapse into markdown-synthesis-with-a-flag — watch | `markdown-synthesis/SKILL.md:24,144` |
| **doc-drift-audit** (med) | Verify a doc set against live code | "are these docs still accurate" | Surface-level code-vs-doc verifier ≠ tech-debt-scan's scored audit | tech-debt-scan, orient-status, baseline | Extract checkable refs (symbols/paths/endpoints/config keys) → verify with rg → prioritized fix list; high-confidence exact misses only | Routing vs tech-debt-scan KN lens; grep false positives | `tech-debt-scan/references/debt-taxonomy.md:10`; [doc-drift-in-CI](https://understandingdata.com/posts/doc-drift-detection-ci/) |
| **runbook-authoring** (med) | Operational procedure → actionable runbook | "turn this into a runbook" | MAKE/SHIP authoring the library entirely lacks | implementation-planning, postmortem | 5-A bar checklist; every step a copy-pasteable command; lifecycle phases only when needed; no inlined creds; flag automation candidates | Over-design; low frequency in this repo | [Uptime Labs runbook](https://www.uptimelabs.io/learn/what-is-an-incident-response-runbook) |
| **change-communication** (med) | Audience-shaped change update | "write a release note for X" | No skill turns a landed change into an outward update | markdown-synthesis, to-prd | 3 presets (downstream migration note / release announcement / leadership one-paragraph); impact-first, omit needless detail; draft-only | Close to "summarize for X"; presets+omission must beat the default | `markdown-synthesis/SKILL.md:3,38` |
| **requirements-capture** (med) | Spec/ticket/transcript → traceable requirement set | "extract requirements from this spec" | Thinking lanes consume context as fuel and *forbid* a source inventory | outcome-interviewer, to-prd, markdown-synthesis | 4 buckets (explicit asks / implied constraints / ambiguities / open questions), each with a provenance pointer | Pass-through risk; routing vs outcome-interviewer | `outcome-interviewer/SKILL.md:31,79`; `markdown-synthesis/SKILL.md:24` |
| **spec-drift-reconcile** (med) | Intent changed → which downstream artifacts stale | "the spec changed, what's now stale" | Detectors (baseline, orient-status) *decline* to drive the fix; chain is forward-only | acceptance-map, baseline, to-prd | Map chain → classify each artifact still-valid/stale/gap → fix *source* then regenerate downstream (not the leaf); consume baseline's authority verdict | One-Owner collision with baseline — make it a prerequisite input | `orient-status/SKILL.md:123`; `baseline/SKILL.md:34`; [spec-kit /analyze](https://github.com/github/spec-kit) |
| **library-integrity-check** (med) | Static structural health of *this* library | "audit the skill library wiring" | The 5 canaries cover delivery/cache/drift; nothing checks cross-refs/orphans/parse-drift | orient-status, scrutinize-skill | Dangling `references/`/`scripts/` paths, handoffs naming archived skills, name≠dir, orphan files; **delegate** delivery to existing `--check` scripts; no auto-edit | Don't re-implement the canaries; keep mechanical | `scripts/claude-skills-sync.sh:76-126`; `AGENTS.md` Validation Ladder step 3 |

### Design-first (real gap, settle scope before building)

| Proposed skill | Why design-first | Adjacent | Evidence |
|---|---|---|---|
| **bug-intake-triage** | Repro/classify already split across `diagnose` Phase 1-2 and `triage` step 3 — settle new front-door vs extraction vs a few diagnose routing lines | diagnose, triage | `diagnose/SKILL.md:47-49`; `triage/SKILL.md:77` |
| **triage-failures** (classify a wall of red) | Real gap (`tdd`/`behavior-smoke-test`/`gh-address-comments` all disclaim CI/test triage into a void) but route points at phantom `keep-green`, and **name collides with issue-tracker `triage`** | diagnose, tdd | `tdd/SKILL.md:3`; `behavior-smoke-test/SKILL.md:3` |
| **warm-handoff-packet** | Genuine continuity win but a shared shape consumed by ~10 lanes **breaks the clean-prune property** and tensions chat-only handoff doctrine | outcome-interviewer, diagnose, save-handoff | `outcome-interviewer/SKILL.md:297-301`; `charter.md:47-52` |
| **eval-design** (error-analysis → LLM-judge authoring) | Strong AI-reliability craft but **this repo hosts no LLM-app code/traces** to fire on; settle host-work + the false "acceptance-map already defers to it" claim | skill-benchmark, acceptance-map | `skill-benchmark/SKILL.md:112-184`; [Hamel error-analysis](https://hamel.dev/blog/posts/evals-faq/why-is-error-analysis-so-important-in-llm-evals-and-how-is-it-performed.html) |
| **traces-to-eval-suite** | Real empty SHIP/CI niche but collapse-risk into `skill-benchmark`'s eval machinery; scope a thin first cut, single-source the grading rules | skill-benchmark, acceptance-map | `skill-benchmark/SKILL.md:116-137`; [Datadog agent observability](https://www.datadoghq.com/blog/patterns-agent-observability/) |
| **eval-routing-line** | Sound, but dangles until an eval lane exists to route TO — trivial follow-on once eval scope is fixed | acceptance-map, tdd | `acceptance-map/SKILL.md:138-143` |
| **triage-static-analysis** | Novel slice (ingest SARIF/Semgrep) but FP/lint-exclusion disciplines already in `implementation-review`, and overlaps parked whole-repo-scanning items | tech-debt-scan, implementation-review | `implementation-review/SKILL.md:117-118`; `contract-decisions.md:327-329` |
| **explain-codebase-fanout** | Parallel large-repo comprehension — mis-framed as expanding a not-yet-existing skill and overlaps `deep-research`'s fan-out; decide standalone vs a fold | explain-codebase, zoom-out | `contract-decisions.md:314-315` |

### Rejected — do NOT build (and why)

| Candidate | Reason |
|---|---|
| **diff-security-review** | Re-litigates the JP-ratified pass-10 adjudication: diff-security folded into `implementation-review`, three residuals parked with reopen triggers (`contract-decisions.md:131-167,320-329`). Reopen only on a real observed miss. Its "tech-debt-scan points at an absent skill" premise is wrong (`tech-debt-scan/SKILL.md:136-139` is availability-conditioned). |
| **post-merge-cleanup** | Pure orchestration shell duplicating `closeout-check`'s Next Move routing; matches the rejected requesting-review meta-skill pattern (`contract-decisions.md:13-14`). Fold any gap into `closeout-check`. |
| **commit-range-audit** | Decomposes into `git-hygiene` (commit convention) + `implementation-review` (commit-range severity review); its sole novel slice (changelog reconciliation) has no consumer here; premised on a non-existent `release-cut`. |
| **verifier-fresh-context** | Already fully implemented — `execute-plan/SKILL.md:22,28-31,39` mandates fresh-context verifiers; review-family *is* that role. At most a one-sentence inline-mode tightening. |

Also rejected at the external-idea stage: **git-bisect skill** (already core to `diagnose`), **Oracle/second-opinion subagent** (covered by making-recommendations
+ review-family + deep-research; harness mechanics not a skill), **project-constitution skill** (gated `AGENTS.md`/charter territory), **standalone decision-log** (duplicates save-handoff/throughline).

---

## 6. Cross-Library Power Gaps

1. **Reviews and audits evaporate.** `implementation-review`, `scrutinize`, `system-design-review`, `baseline`, `tech-debt-scan` all end in chat with **no handoff to `to-issues`/`triage`**. *Pain:* a blocker verdict or ranked backlog must be manually re-keyed; findings silently lost at session end. (`implementation-review/SKILL.md:176-194`; `tech-debt-scan/SKILL.md:27-31`)
2. **acceptance-map's artifact has no reader** (`acceptance-map/SKILL.md:291-293`). *Pain:* a careful acceptance map is produced, then nothing verifies against it.
3. **Shaping handoffs are cold** (`outcome-interviewer/SKILL.md:250`). *Pain:* the receiving lane re-derives outcome, constraints, and non-goals just established.
4. **The generation chain is forward-only.** No reconciliation path when intent changes mid-stream. *Pain:* the agent patches the leaf while the PRD/acceptance map silently rot (the `spec-drift-reconcile` gap).
5. **The SHIP lifecycle has a hole at "open the PR."** Every review-response skill assumes the body exists; `implementation-review` depends on it (`:37`). *Pain:* the highest-frequency authoring task in the ship path is unowned.
6. **No eval lane for nondeterministic output** (`acceptance-map/SKILL.md:138-143`). *Pain:* an agent building an AI feature is nudged toward a brittle exact-match test. (Gated by host-work; see design-first cluster.)
7. **Worktree lifecycle is one-sided** (`exiting-worktrees/SKILL.md:247-248`). *Pain:* the entry half relies on raw tooling with no branch-naming/base guards.
8. **Explicit-only skills under-fire.** `next-steps`, `zoom-out`, `review-reviewer`, `gh-pr-review-loop`, `setup-matt-pocock-skills` are `disable-model-invocation`, and peers don't detect-and-suggest them. *Pain:* dependency-aware sequencing, decision re-derivation, and config bootstrap fire only when the user remembers the token (`next-steps/SKILL.md:4`; `setup-matt-pocock-skills/SKILL.md:3`). Cheap fix: have consumers surface a one-line pointer when their precondition is missing.

---

## 7. External Inspirations

| External idea | Source | Maps to |
|---|---|---|
| Grounded self-correction loop (execution-anchored beats intrinsic) | [zylos.ai](https://zylos.ai/research/2026-05-12-agent-self-correction-reflexion-to-prm), [Aider lint/test](https://aider.chat/docs/usage/lint-test.html) | **New: `keep-green`** |
| Parallel fan-out/fan-in solution exploration (~7× cost, caps + selection rubric) | [Simon Willison](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/) | **New: `fan-out-attempts`** |
| Codebase onboarding / `/init`-style orientation | [super-productivity](https://super-productivity.com/blog/ai-codebase-onboarding-guide/), [everything-claude-code skill](https://github.com/affaan-m/everything-claude-code/blob/main/skills/codebase-onboarding/SKILL.md) | **New: `explain-codebase`** |
| Release derivation (commits→semver→changelog) | [release-please](https://github.com/googleapis/release-please) | **New: `release-cut`** |
| Dependency-PR triage (5-factor) + doc-grounded upgrade/migration (codemods) | [robertknight gist](https://gist.github.com/robertknight/7e9a42e1ff9e29001f2cfa44d515cf47), [Fowler codemods](https://martinfowler.com/articles/codemods-api-refactoring.html) | **New: `dependency-upgrade-triage` + `dependency-upgrade-execute`** |
| Large-scale migration campaign + API contract-change propagation | [Moderne](https://www.moderne.ai/blog/large-scale-code-changes), [flarecanary](https://dev.to/flarecanary/how-to-detect-api-breaking-changes-before-they-hit-production-257p) | **New: `migration-campaign` + `contract-change-propagation`** |
| AI-generated-code review failure modes (review slower-per-line) | [clacky.ai](https://clacky.ai/blog/code-review-checklist-ai-generated-code) | **Expand: `implementation-review`** AI-code lens |
| Large-diff review strategy (pick the review unit) | [commit-by-commit review](https://nicholashirsch.medium.com/code-reviews-in-git-commit-by-commit-ae02f8dcd9a0) | **Expand: `implementation-review`** bounded mode |
| USE-method resource sweep | [Brendan Gregg](https://www.brendangregg.com/usemethod.html) | **Expand: `diagnose`** perf branch |
| ADR authoring, doc-drift audit, runbook authoring, blameless postmortem | [ADR ops](https://hidekazu-konishi.com/entry/architecture_decision_records_templates_and_operations.html), [doc-drift-CI](https://understandingdata.com/posts/doc-drift-detection-ci/), [Uptime Labs](https://www.uptimelabs.io/learn/what-is-an-incident-response-runbook), [PagerDuty](https://response.pagerduty.com/after/post_mortem_template/) | **4 new knowledge-authoring skills** |
| Spec-drift reconciliation (fix the spec, regenerate downstream) | [spec-kit](https://github.com/github/spec-kit) | **New: `spec-drift-reconcile`** |
| CONTEXT/AGENTS minimization + staleness (non-minimal context = 0 gain, +20% cost) | [SRI Lab](https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd) | **Expand: `writing-principles`** staleness lens |
| CI-red / failing-test triage (classify before fixing) | [Marco Lancini](https://blog.marcolancini.it/2026/blog-automating-security-operations-with-ai-triage-renovate/) | **Design-first: `triage-failures`** |
| error-analysis → LLM-judge authoring → traces-to-eval-suite | [Hamel](https://hamel.dev/blog/posts/evals-faq/why-is-error-analysis-so-important-in-llm-evals-and-how-is-it-performed.html), [arXiv 2506.22316](https://arxiv.org/html/2506.22316v1), [Datadog](https://www.datadoghq.com/blog/patterns-agent-observability/) | **Design-first: eval cluster** (host-work gated) |
| Diff-based security review (OWASP 6-step) | [OWASP cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html) | **Rejected** — folded into implementation-review (pass-10) |
| SAST/static-analysis triage | [Astra FP triage](https://www.getastra.com/blog/dast/false-positive-triage/) | **Design-first: `triage-static-analysis`** |
| Verifier-in-fresh-context, commit-range audit, git-bisect, Oracle subagent, project constitution, decision-log | Willison subagents; commitlint; LWN; Amp; Thoughtworks | **Rejected** — already implemented or already owned |

---

## 8. Recommended Next Moves

Tags: **[IMPL]** ready for implementation planning, **[DESIGN]** needs a design discussion first, **[REVIEW]** read-only follow-up.

1. **[IMPL] Build `explain-codebase`** — highest leverage, zero open design questions, read-only. The cheapest high-value first fire.
2. **[IMPL] Build the SHIP authoring pair: `pr-description`, then `release-cut`.** Both high-leverage, both fill the thinnest zone, clean boundaries to imitate. Verified scope correction for `release-cut`: repo has **0 git tags** → anchor "last release" on `plugin.json`/`CHANGELOG` headers.
3. **[IMPL] Build `keep-green`** *before* the MAINTAIN skills — the grounded self-correction loop `dependency-upgrade-execute` + `migration-campaign` want to compose with. Keep stop conditions sharp; boundary against `closeout-check` crisp.
4. **[IMPL] Build `fan-out-attempts`** (Claude-only v1, PICK-ONE). Gate hard on "objectively gradeable," cap concurrency, state the ~N× cost before dispatch.
5. **[IMPL] Build the large-mechanical-change lane: `migration-campaign` + `contract-change-propagation`.** Then `dependency-upgrade-triage` + `dependency-upgrade-execute` (latter after `keep-green`). Tighten descriptions against `to-issues`/`execute-plan` misroute.
6. **[IMPL] Build the knowledge-authoring batch:** `adr-authoring`, `postmortem`, `research-capture`, `doc-drift-audit`, `runbook-authoring`. All build-now, cheap, durable-artifact skills. For `adr-authoring`, *point at* the existing `ADR-FORMAT.md` rather than relocating it (3-skill refactor hazard).
7. **[IMPL] Apply the persistence/glue existing-skill upgrades (Section 4).** Wire `acceptance-map` into `implementation-review` + `implementation-planning`; add "export findings → to-issues/triage" to the reviewers + `tech-debt-scan`; add the `review-ai-code` lens (with the line-117 carve-out) and the USE-method perf sweep to `diagnose`. Small edits, outsized leverage, directly close Section 6. *(Plugin-distributed surfaces follow the version-bump + republish path.)*
8. **[IMPL] Build `library-integrity-check`** scoped to the *uncovered* slice (cross-ref/orphan/parse-drift), delegating delivery/cache/contract-drift to the five canaries. Also answers the standing "structural-integrity check" question.
9. **[DESIGN] Settle the eval-for-AI cluster** (`eval-design` / `traces-to-eval-suite` / `eval-routing-line`) and the routing/naming questions (`warm-handoff-packet`, `bug-intake-triage`, `triage-failures` name collision). The eval lane is gated on whether resident LLM-app/trace work exists. Run through `agent-facing-design`.
10. **[REVIEW/NOTE] Do not build the 4 rejects.** If diff-security coverage later feels thin, the charter-sanctioned move is a named reopen trigger (an observed real-work miss), not a fresh build.

**Net:** under build-and-prune, **~17 new skills and ~12 existing-skill upgrades are ready to build and watch fire** — concentrated in the thin zones (MAKE / MAINTAIN / SHIP), plus one system-level theme (kill the chat-only artifact death) that lifts the already-strong review and planning clusters.

---

## Evidence Boundary

- **Inspected:** all 48 live skills (`SKILL.md` in full, `agents/openai.yaml` where present, behavior-affecting references/scripts skimmed); `charter.md`, the 345-line `contract-decisions.md`, `AGENTS.md`; the five SessionStart canaries. Every candidate was grepped against the charter + ledger and read against its named adjacent skills.
- **Not inspected:** behavior validation (no forward tests, dry runs, or `skill-benchmark`); full reads of long reference/playbook files; `skills-archive/`; gated/ambient contracts. The global `deep-research` skill is out-of-repo and was not double-counted.
- **Verification:** each of the 36 candidates was independently checked for duplication (against live adjacent `SKILL.md`) and settled-out status (against live `charter.md` + `contract-decisions.md`); 4 were rejected on that basis.
- **Caveat:** candidates cross-reference sibling skills that do not yet exist (proposed together by the gap lenses); treat each candidate's scope as standalone. Several candidate summaries contained phantom-adjacency or fabricated-rationale errors that the verification pass flagged — those are noted inline.
- **Status:** evidence at `0755adc`, not authority. Later edits can invalidate a citation or finding — re-verify against live source. The build/expand/reject verdicts reflect the relaxed build-and-prune charter as of `f8964f1`; a future charter change could shift them.
