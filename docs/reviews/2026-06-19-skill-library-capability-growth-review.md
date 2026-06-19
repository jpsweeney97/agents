---
type: review
date: 2026-06-19
scope: "All 48 live skills — skills/ (29), skills-claude/ (4), plugins/git-cycle/skills/ (6), plugins/handoff/skills/ (4), plugins/review-family/skills/ (5) — plus AGENTS.md, docs/agents/contract-decisions.md, the 2026-06-17 apparatus-review artifact, plugin manifests, and marketplace.json."
reviewed_commit: 0a3c11d
method: "35-agent capability-growth workflow (wf_7301d22c-498): 9 cluster deep-readers + 6 external researchers + 3 cross-cutting gap-hunters -> consolidation -> adversarial verification of every candidate against the contract-decisions ledger and existing skills. Headline citations re-verified firsthand by the orchestrator."
posture: "Read-only; biased toward expansive capability growth (new categories, workflows, reusable capabilities). Deliberately distinct from the 2026-06-17 quality/consolidation review."
---

# Skill-Library Capability-Growth Review — 2026-06-19

Read-only review of the 48-skill library for opportunities to increase the value
it provides, biased toward capability growth rather than consolidation. The
2026-06-17 apparatus review
(`docs/plans/artifacts/skill-library-apparatus-review-2026-06-17.md`) already
covered quality/trust-bar machinery drift and found the library healthy; this
pass deliberately looks for missing or underpowered *capabilities* instead.

A cross-cutting constraint shapes every recommendation: **the charter admits
skills on observed friction, not structural plausibility** (charter.md:79-89; the
ledger parked/rejected `frontend-design`, `claude-automation-recommender`, and
`explanatory-output-style` precisely for zero observed work). The verification
pass flagged "no observed friction" on most new-skill candidates. So the gradient
is: ship near-zero-cost prose glue now, *pilot* the highest-leverage new skills on
the next real task that exercises them, and *park with a named trigger* the
speculative ones — not mass-author on spec.

## 1. Executive Summary — 5 highest-value opportunities

| # | Opportunity | Kind | Why it is top-tier |
|---|---|---|---|
| **1** | **`integrate-branch`** — carry a diverged branch / resolve conflicts before landing | **New skill** (high-confidence gap) | The clearest *operational* dead-end. All five `git-cycle` landing skills are fast-forward-only and abort the moment the base moves — `merge-branch` stops and hands back "rebase / merge-commit / abort" with **no owner** (merge-branch/SKILL.md:155-164); `exiting-worktrees`, `gh-pr-review-loop`, `git-hygiene` all refuse. The most common real task between "done" and "landed" is ownerless. |
| **2** | **`library-health` / routing-audit** — survey the 48-skill corpus for dead routing pointers, orphans, description-vs-body drift, half-done retirements | **New skill** (system-level, uniquely apt) | This repo *is* a live dual-runtime skill library whose value depends on routing-graph integrity, yet every health pass — including this one and the 2026-06-17 review — is run by hand. The ledger records maintenance actually getting dropped: the `jp-writing-style` retirement left a dangling symlink un-reaped and "the retirement record left half-done" (contract-decisions.md:292-305). |
| **3** | **Evidence/observability expansion bundle** — `execute-plan` run-ledger + `acceptance-map` verify-mode + `implementation-review` falsification-execution + a new post-hoc **adherence-audit** lane | **Existing-skill expansions + 1 new lane** | Directly serves the stated value criteria (less supervision, stronger evidence). Today these lanes are trust-me: `execute-plan` reports completion in chat with no resumable ledger; `acceptance-map` builds a checklist it never stamps; `implementation-review` is told to *record* unverified findings, never run a safe probe. This bundle turns the build/verify spine auditable and resumable. |
| **4** | **Connective-tissue / lifecycle-completion glue** — `from-issue` intake bridge + review->action findings carrier + handoff routing-in | **1 thin new skill + system-level prose routing** | The lifecycle has two silent seams. `to-issues` hands work to "execution's to pick up" (to-issues/SKILL.md:97-98) — a lane that does not exist. And review-family findings + lifecycle-ending lanes never route into their consumers (`closeout-check` lists `handoff` as a Next Move value at line 242 but never names `save-handoff`). These are the highest-frequency manual copy-paste bridges in the library. |
| **5** | **New build-category frontier** — `codemod-migration`, `characterize-legacy`, `eval-driven-dev` (+ `postmortem`, `release-notes`, `dependency-upgrade` as the next tier) | **New skills** (experiments) | The pure capability bet. The library has *zero* coverage of repo-wide mechanical transforms, legacy-behavior pinning before refactor, and treating an LLM/prompt feature (not human software) as the product under test. Each is a genuinely unowned category, not an adjacency. |

## 2. Coverage and Limits

**Inspected (live working tree, re-checked at commit `0a3c11d`):**

- All 48 SKILL.md across `skills/`, `skills-claude/`, and the three plugins —
  frontmatter for all; full bodies for the cluster sample plus firsthand reads of
  `execute-plan`, `friction-to-guards`, `diagnose`, `orient-status`,
  `throughline`, and targeted spans of `merge-branch`, `acceptance-map`,
  `scrutinize`, `to-issues`, `closeout-check`, `scrutinize-skill`.
- Governance: `AGENTS.md`, `docs/agents/contract-decisions.md` (full ledger incl.
  Parks + Mining Queue), the 2026-06-17 apparatus-review artifact, plugin
  manifests, `marketplace.json`, `skills-archive/README.md`,
  `docs/reviews/README.md`.
- `disable-model-invocation` set verified (5 explicit-only skills: `next-steps`,
  `zoom-out`, `setup-matt-pocock-skills`, `review-reviewer`, `gh-pr-review-loop`).

**Did not inspect (or only lightly):** full bodies of every reference/example/
script (only the behavior-bearing ones in-cluster); plugin caches, the GitHub
mirror, and `~/.claude/skills` symlink internals (review of *source*, per the
2026-06-17 boundary); `docs/plans/` apparatus artifacts beyond the ledger and the
prior review; runtime/installed state (no runtime claims made). `deep-research`
and other bundled skills (`code-review`, `security-review`, `verify`, `run`,
`update-config`, etc.) were treated as already-available externals and excluded
from "new" proposals.

**External search performed:** ~30+ web searches/fetches across six domains —
Anthropic skills/engineering guidance, multi-agent orchestration, dev-tooling/CI/
release, knowledge-management, prompt/skill marketplaces, AI-assisted work loops.
Cited inline in section 7. Opportunistic, not exhaustive.

## 3. Current Library Map

| Cluster | Skills | Strength |
|---|---|---|
| **Discovery & Framing** | outcome-interviewer, design-exploration, making-recommendations, grill-me, grill-with-docs, prototype | **Strong.** Tiles muddy->settled cleanly with permissioned handoffs. Edge gaps: no leading-indicator premortem, thin grill stop-coverage. |
| **Planning & Decomposition** | implementation-planning, acceptance-map, next-steps, execute-plan, to-prd, to-issues, triage | **Strong but open-ended downstream.** The plan->issues arc is rich; the **issue->execution** seam is broken and acceptance-map is write-only. |
| **Build, Test & Refactor** | tdd, diagnose, simplify-code, improve-codebase-architecture | **Adequate, with category holes.** No cross-cutting transform lane, no legacy-pinning, no test-backfill; `simplify-code` is single-slice only. |
| **Review & Scrutiny** | implementation-review, scrutinize, scrutinize-skill, system-design-review, review-reviewer | **Strong (deepest cluster).** Findings have no forward carrier; no execution-of-probes; no production-readiness gate. |
| **Skill & Contract Engineering** | agent-facing-design, skill-ux-design, writing-principles, behavior-smoke-test, skill-benchmark, friction-to-guards, setup-matt-pocock-skills | **Strong on authoring/judgment.** No tool-output-ergonomics rubric; no library-wide health/regression view (only per-skill). |
| **Status, Authority & Debt** | orient-status, baseline, zoom-out, tech-debt-scan | **Adequate.** All one-shot/no-delta: no since-anchor status, no debt-trend re-scan, no whole-repo comprehension map (parked). |
| **Git Lifecycle** | git-hygiene, closeout-check, merge-branch, exiting-worktrees, gh-address-comments, gh-pr-review-loop | **Strong locally, ff-only ceiling.** Diverged-base/conflict integration is refused everywhere; lifecycle stops at "land" (no ship/release stage). |
| **Session Continuity (handoff)** | save-handoff, load-handoff, search-handoffs, throughline | **Strong but one-directional.** Nothing routes *into* save-handoff; cross-session only — no within-task working memory. |
| **Knowledge, Docs & Comms** | markdown-reformat, markdown-synthesis, claude-code-docs, openai-docs, caveman | **Adequate, vendor-bound.** Doc grounding covers only Claude/OpenAI; no general library-docs lane, no doc-freshness audit, no runbook generation. |

**Already-strong clusters:** Discovery & Framing, Review & Scrutiny, Skill &
Contract Engineering, Planning (upstream half). **Thin clusters:** Build/Test/
Refactor (category holes), Git Lifecycle (ff-only ceiling + no ship stage),
Knowledge/Docs (vendor-bound), and the lifecycle **"learn" stage** (no postmortem/
retro producer at all).

## 4. Existing-Skill Upgrade Opportunities

| Skill | Current value | Limiting factor | Proposed upgrade | Why it increases power | Evidence | Size |
|---|---|---|---|---|---|---|
| **execute-plan** | Faithful task-by-task execution with review gates | Single-shot, in-session; completion is a chat report, no resumable trail | Append-only per-task **run-ledger** (task #, status, evidence pointer, commit); on restart skip completed, resume at first incomplete | Fault-tolerant resumable execution; a fresh session/agent resumes mid-plan; auditable evidence trail vs trust-me — the observability layer for unsupervised runs | execute-plan/SKILL.md (no ledger/resume concept; only "progress" at :59) — **verified firsthand** | large |
| **acceptance-map** | Durable observable-checks artifact pre-implementation | Produces the map but **never consumes it** — verification is deferred away | Optional **verify-against-map** mode: stamp each check pass/fail/blocked + evidence in place; or make the map a first-class spec source in `implementation-review` | Closes the loop in the lane that owns the format; self-contained acceptance record with end-to-end evidence | acceptance-map/SKILL.md:~52, 290-296 ("verify the result against it; closeout-check later"; "implementation not verified") — **verified firsthand** | large |
| **implementation-review** | Evidence-first code-vs-spec review with observed/inferred/unverified split | Told to *record* unverified findings, never run a safe probe | Opt-in **falsification-execution**: for blocker findings where a bounded non-mutating probe converts inferred->observed, run it and attach output (inside the existing ask-before-mutating boundary) | A blocker's strongest evidence is a reproduction; closes the loop the user otherwise runs themselves | implementation-review/SKILL.md:37 + "checks run separately" posture | large |
| **scrutinize-skill** | Adversarial skill-contract critique | Names a "behavioral proof" finding class it can only *wish* for | When a finding is a behavior-proof gap, name the concrete forward test and route to `behavior-smoke-test` (qualitative) / `skill-benchmark` (quantitative) | Turns "behavior unverified" into an actionable proof recipe; wires the critique lane to the two skills that can satisfy it | grep of scrutinize-skill/SKILL.md for proof skills -> **empty (verified firsthand)** | small |
| **merge-branch** | Clean local fast-forward landing | Dead-ends on any non-ff, even a clean one | Guarded opt-in **no-ff merge-commit** mode when `git merge-tree` shows no conflict (same preflight/retention guards); conflicted merges hard-stop -> `integrate-branch` | Recovers the most common real case (branch behind main, merges clean) without entering rebase territory | merge-branch/SKILL.md:155-164 — **verified firsthand** | large |
| **diagnose** | Hard-bug discipline built on a feedback loop | Loop trusted by subjective "belief," no discriminating-power check | "Validate the loop" step: prove it **fails on the bug and passes on a known-good baseline** before trusting it | Eliminates the most expensive failure (hours bisecting a loop that never measured the reported bug) | diagnose/SKILL.md:51 ("a loop you believe in"); Phase 2 flags wrong-bug but no technique | small |
| **diagnose** | (perf scope claimed in frontmatter) | Perf branch is one line; no meter-selection taxonomy | `references/perf-loop.md`: meter-by-symptom (wall-clock/profiler/allocation/query-plan/flamegraph), baseline-with-variance, bisect-on-metric | Decision procedure instead of a reminder for the perf scope the frontmatter already claims | diagnose/SKILL.md:89 (one-paragraph perf branch) vs :3 (frontmatter claims perf) | small |
| **tech-debt-scan** | Evidence-led prioritized debt artifact | Re-scan produces a standalone artifact with no relation to the prior one | **Delta mode**: read prior dated artifact, carry finding IDs, add "Since Last Scan" (resolved / aged / now-worse); re-check Watch List; name `to-issues`/`triage` as the bridge | Shows debt *trend* (improving vs compounding) — the actual decision input — and stops re-litigating resolved debt | tech-debt-scan/references/audit-report-template.md:161,171 (Watch List/Next Probes never re-read); SKILL.md:30 | large |
| **orient-status** | Read-only status orientation | No prior reference point; "recent" is unanchored | Optional **since-anchor** (date/commit/tag/handoff): frame Recent Activity + In Flight as a delta against it | Answers the implicit "since when?"; two orientations a week apart become comparable | orient-status/SKILL.md:152 (unanchored recent-window); :48 (handoffs usable as evidence) | large |
| **making-recommendations** | Stakes-scaled option comparison | Only forward-looking field is *pre*-decision info gaps | High-stakes **premortem field**: most plausible post-commitment failure of the recommended option + earliest observable signal (prose, no scoring) | Costly-to-reverse decisions ship with their own falsification signal | making-recommendations/SKILL.md:150-153; references/high-stakes.md | small |
| **simplify-code** | Scoped behavior-preserving cleanup | Single-slice; repetitive identical edits force N runs with no uniformity proof | **Mechanical-batch** mode: scan all sites, one backup, apply, verify with a structural diff-uniformity check | Extends the trust model to scale; covers the pure-rename slice of `codemod-migration`, leaving that skill for behavior-changing migrations | simplify-code/SKILL.md:47,53 (behavior-change stop; single target) | large |
| **baseline** | Authority/source-of-truth resolution | "Still current?" is a binary flag — a fossil and a fresh doc read identically | Attach a concrete **staleness signal** (last-modified/last-commit age + whether live state moved) | Delivers on the description's "whether an authority is still current" promise; cheap read-only metadata | baseline/SKILL.md:3; binary Freshness gap | small |
| **throughline** | Derived project-arc condensation | Drift check is a single count; blind to in-place content edits | Cheap **integrity nudge**: flag when a folded source's mtime is newer than `updated_at` ("possible below-water-line edit; consider rebuild") — no stored hash | Surfaces the silent-content-edit corruption class without violating the no-hash boundary | throughline-format.md:29; throughline/SKILL.md:80 | small |

## 5. New Skill Candidates

Adversarially verified against the ledger and existing skills. **Verdict** is the
verifier's right-sizing; confidence is `high` / `experiment` (build, but pilot
first) / `speculative` (park with trigger).

### Build-worthy (verdict: keep-new, narrowed where noted)

| Proposed skill | User problem | Likely trigger | Why separate | Adjacent | First-version scope | Risks | Evidence / inspiration | Conf |
|---|---|---|---|---|---|---|---|---|
| **integrate-branch** | Diverged base / conflicts between "done" and "landed" — refused by every git-cycle skill, no owner | "rebase onto main", "update branch with main", "PR has conflicts / push rejected" | Enters an in-progress rebase/merge state machine the ff-only siblings are built to *abort* on; per-resolution evidence + force-with-lease gating | merge-branch, exiting-worktrees, gh-pr-review-loop, git-hygiene | Local-only non-protected: fetch base, preview ahead/behind + `merge-tree`, choose rebase-vs-merge, conflict loop one file at a time w/ evidence, re-verify, **stop before push** | Conflict resolution is where an agent silently corrupts intent; must be a bounded sibling, not leak into ff-only skills | merge-branch/SKILL.md:155-164 (verified); ledger clear | exp |
| **library-health** (routing-audit) | Nothing keeps the 48-skill corpus healthy: dead routing pointers, orphans, desc-vs-body drift, half-done retirements | "audit the skill library", "check for routing drift / orphans" | Library-wide *graph* view neither tech-debt-scan (general debt) nor scrutinize-skill (single skill) owns | tech-debt-scan, scrutinize-skill, friction-to-guards | Read-only: build inventory across all dirs, parse inter-skill route mentions, report dangling/orphan/asymmetric routes, cross-check `--check` scripts read-only, flag half-done retirements vs ledger; findings only, no auto-fix | Must not become a scored gate; route fixes to writing-principles/owning skill | contract-decisions.md:292-305 (dropped maintenance, verified); this review itself was hand-run | exp |
| **from-issue** | `to-issues` builds an agent-brief, then hands to "execution" — a lane that does not exist; the brief has no consumer | "work on #42", "grab the next ready-for-agent issue" | Starting evidence is a tracker agent-brief (not a plan doc); owns fetch-brief->treat-as-spec->route-by-size bridge | to-issues, triage, execute-plan, implementation-planning, implementation-review | **Thin bridge**: fetch brief, treat as governing spec, branch, then *delegate* (small->execute-plan inline; large->implementation-planning), name implementation-review + closeout-check as exit | Do not re-implement execute-plan's executor; keep it intake-only, pilot once before sealing the size-fork | to-issues/SKILL.md:97-98 (verified); triage/AGENT-BRIEF.md:3 (briefs unowned) | exp |
| **codemod-migration** | Repo-wide mechanical transforms (dep/framework upgrades, deprecated-API, rename sweeps) fall between simplify-code (single-slice) and tdd | "upgrade X across a breaking version", "run a codemod", "repo-wide rename" | Evidence model is *transform uniformity* + suite-green before/after; tolerates intentional behavior change — opposite of simplify-code's stop | simplify-code, tdd, improve-codebase-architecture, tech-debt-scan | Build around the **uniformity check** + ast-grep/codemod/OpenRewrite **tool-selection judgment** (not a step-list narration): dry-run on sample, baseline, sweep, verify, report orphans | Can become a thin verify-wrapper if not built around the judgment core; gate via agent-facing-design | github.com/codemod/codemod; ledger clear | exp |
| **characterize-legacy** (backfill-tests) | Before refactoring untested code, need golden-master tests pinning *current* behavior (incl. bugs) — tdd explicitly excludes after-the-fact tests | "pin current behavior", "safety net before I refactor this" | Inverts tdd's red-green (assert whatever the code returns now, then snapshot); golden-master not spec-first | tdd, improve-codebase-architecture, simplify-code, codemod-migration | Identify public seam, generate fixtures, record current outputs as approved snapshots (**loudly label "pins possibly-buggy behavior"**), report seam coverage + non-determinism blockers | Snapshotting bugs entrenches them if not labeled; pilot on a real low-coverage refactor | tdd/SKILL.md:3 (excludes after-impl tests, verified); arxiv 2403.16218 (CoverUp) | exp |
| **postmortem** | The only post-mortem is one line in diagnose Phase 6 (per-bug, architecture-only); no project/incident retrospective producer | "write up the incident", "retro on this", "what would we change" | Timeline-driven blameless causal synthesis -> durable PIR w/ owned action items; diagnose finds a current cause, system-design-review *excludes* postmortems | diagnose, next-steps, friction-to-guards, save-handoff | Blameless timeline (from commits/handoffs/diffs), what worked/hurt, contributing factors (never blame), follow-ups split mitigative-vs-preventative; route outputs to owning lanes | Risks thin orchestrator — kernel must be the timeline+causal synthesis; **no numeric scoring**; drop phantom `capture-decision` route | diagnose/SKILL.md:115-125 (verified); incident.io SRE PIR; system-design-review excludes postmortems | exp |
| **release-notes** | Lifecycle dead-ends at "land"; nothing turns a commit range into user-facing notes / CHANGELOG | "write the release notes", "update the changelog for this release" | Operates at release/tag granularity, audience-facing; semver + breaking-change + noise-filter judgment | merge-branch, closeout-check, markdown-synthesis, throughline | Read diff+subjects, group by type, **name breaking changes + propose major/minor/patch as a categorical decision** (never a numeric breaking-ness score), write to repo's existing convention, stop before tag/push | Lower fit for a skills-only repo; semver "inference" must not harden into a scored gate | keepachangelog.com; ComposioHQ/awesome-claude-skills changelog-generator; ledger clear (distinct from rejected commit cmds) | exp |
| **delegate-brief** (narrowed) | No discipline for writing a single subagent brief for ad-hoc fan-out, nor checking concurrent briefs are non-overlapping/gap-free | "brief a subagent", "compose these parallel tasks" | Agent-to-agent execution contract (vs save-handoff's human-resume); owns the **fan-out non-overlap/gap check** nothing does | save-handoff, execute-plan, implementation-planning | **Narrow to the uncovered job**: verify concurrent briefs are non-overlapping + gap-free before dispatch; source per-brief shape *by reference* to triage/AGENT-BRIEF.md (do not re-author) | Single-brief craft already in AGENT-BRIEF.md — narrow or it duplicates; routing collision w/ triage/execute-plan | anthropic.com/engineering/multi-agent-research-system; triage/AGENT-BRIEF.md:1-168 | exp |
| **library-docs** | Doc grounding is bound to Claude+OpenAI only; every other library answered from stale memory — context7 MCP is wired but uncontracted | "how does <third-party lib> work", writing code importing a package | Different evidence source (general package MCP) + resolve-the-right-library risk; must NOT fire for Claude/OpenAI | openai-docs, claude-code-docs, deep-research | **Thin** (single SKILL.md): resolve-before-query, version pin, library-id/source citation per claim, fetch budget, gap-handling, hard do-not-use boundary to the two vendor skills; availability-conditional on context7 | context7 already injects its own block — must earn its slot on the *increment*; author thin, do not pad | settings.json context7 enabled (verified); ledger clear | exp |

### Right-sized into existing skills (verdict: fold/expand — do NOT build standalone)

| Candidate | Verdict | Why | Where it goes |
|---|---|---|---|
| **reproduce-bug** | fold-into diagnose | Its entire scope *is* diagnose Phase 1+2 (the part diagnose calls "the skill"); a 3rd bug-lane creates suspected-bug->reproduce/diagnose/tdd routing ambiguity | Sharpen diagnose's description to advertise stopping at Phase 2 (red artifact + "ready for tdd/fix") |
| **premortem** | fold-into scrutinize | scrutinize already owns "pre-mortem" as a trigger token + a Pre-Mortem section (SKILL.md:54, 99-106, verified). A standalone splits the trigger | Extend scrutinize's Pre-Mortem to pair each failure path with an earliest leading indicator + cheapest mitigation (review-family publish path) |
| **second-opinion-review** | fold-into scrutinize | The novel part (ship-biased + reject-biased passes, reconciled) is a one-line affordance; review-reviewer already handles multiple targets. Ledger-adjacent to the rejected requesting-review meta-skill | Optional high-stakes multi-stance mode in scrutinize; reuse review-reviewer's reconciliation vocabulary; counts descriptive only |
| **capture-decision** | expand grill-with-docs + park separate skill | acceptance-map already owns the settled->durable-artifact lifecycle; grill-with-docs owns ADR-FORMAT.md. No observed instance of a lost decision | Add a standalone on-demand ADR path to grill-with-docs + an AGENTS.md route; park the separate skill (trigger: first observed lost-rationale) |

### Park with a named trigger (verdict: ledger-blocked / speculative)

| Candidate | Status | Trigger to reopen |
|---|---|---|
| **map-codebase** (whole-repo comprehension) | **Ledger-blocked** — matches the parked `code-comprehension lane` (contract-decisions.md:314); real uncovered gap but the registered trigger ("observed comprehension failure in real work") has not fired; `zoom-out` partially covers | Surface as the strongest candidate to *fire* that park; build on a real whole-repo comprehension failure |
| **mcp-builder** | **Speculative/park** — 3 of 4 phases decompose into owned lanes (impl-planning/execute-plan/tdd/verify); its "~10 eval questions" count was already flagged *substitutive* in the blind evals (sealed-key.md:18); MCP servers are charter-exempt tooling | First real observed MCP-server build task; if reopened, author only the Inspector + tool-eval residue, drop the fixed count |
| **eval-driven-dev** (LLM-feature golden-set/scorer/regression-gate) | **Speculative-ok** — genuinely unowned (skill-benchmark is SKILL-scoped, Claude-only); but this repo is a skill library, not an LLM-product codebase | First real LLM/prompt/agent-feature eval need; reuse skill-benchmark's anti-self-grade discipline, keep all selection qualitative |
| **working-memory** (in-task scratchpad surviving compaction) | **Speculative/park** — zero coverage (handoff is cross-session) but fails the lighter-context test: plausibly an AGENTS.md line | First observed in-task working-memory loss across a compaction; meanwhile cover with one Working-Defaults line |

### Surfaced by research, not yet candidate-verified (bias-to-inclusion backlog)

`production-readiness` review (pre-launch go/no-go gate — fits review-family;
sreschool.com PRR) · `ci-triage` (failing pipeline -> regression/flake/infra,
feeds diagnose) · `dependency-upgrade` (impact-aware safe-upgrade *sequence*,
distinct from tech-debt-scan; fossa/ombulabs) · `doc-runbook` (operational runbook
generation; eriklieben) · `doc-freshness-audit` (tech-debt-scan shape applied to
docs; datahub) · `onboarding-bootstrap` (human onboarding doc + walkthrough —
overlaps the parked comprehension lane) · `flag-cleanup` (feature-flag
terminal-state-aware collapse; atlassian) · `fan-out-investigate` (parallel
orchestrator-workers — likely an execute-plan mode, not a skill) ·
`long-running-harness` (multi-session autonomous build w/ progress file +
recovery; anthropic long-running-agents). All `experiment`/`speculative`; most
want observed friction before admission.

## 6. Cross-Library Power Gaps

The five system-level gaps (each verified against live source) — the
connective-tissue and lifecycle holes no single skill owns, and the
highest-leverage place to act because most are cheap prose routing, not new
machinery.

1. **No library self-maintenance (routing-graph integrity).** *Pain:* this repo's
   value *is* its routing graph, but health passes are hand-run and the ledger
   proves maintenance gets dropped (dangling symlink + half-done retirement,
   contract-decisions.md:292-305). *Fix:* the `library-health` lane (section 5) —
   read-only routing/orphan/drift audit. The single most apt new capability,
   because the artifact under test is this very library.

2. **No library routing-regression suite.** *Pain:* editing one skill's
   description can silently steal a neighbor's fires — a collision the *per-skill*
   skill-benchmark cannot see; the blind-eval apparatus proves the *method* exists
   but leaves no standing rerunnable artifact. *Fix:* a small versioned
   routing-assertion corpus (query->expected skill / expected non-fire) + a few
   behavior canaries, run via skill-benchmark's harness *across* skills as a
   guard; add a collision-aware mode to skill-benchmark. (Experiment — curation
   cost needs observed regressions.)

3. **No post-hoc adherence audit.** *Pain:* after an autonomous run, no cheap way
   to ask "did it actually obey the rules?" — protected-branch commits,
   claimed-done-without-evidence, skipped gates surface only by luck. The global
   evidence-before-claims rule and AGENTS.md floors *exist* but nothing audits
   compliance. *Fix:* a read-only adherence-audit lane (transcript/commit-range +
   controlling contracts -> obligation->evidence ledger, no numeric score). Pairs
   with the execute-plan run-ledger upgrade as its input. The missing feedback
   signal that would let you trust longer unsupervised runs.

4. **Handoff continuity is one-directional and unrouted.** *Pain:* the most
   context-hungry, interruptible lanes never nudge `save-handoff` —
   `closeout-check` lists `handoff` as a Next Move value (line 242) but never names
   the skill; `execute-plan` names closeout/merge/PR but not handoff. So mid-arc
   state is lost at exactly the boundaries the handoff plugin exists to protect.
   *Fix:* one-line route additions to execute-plan Stops, gh-pr-review-loop
   Checkpoints, and closeout-check's "not ready" path. Pure prose, near-zero cost.

5. **Review findings have no durable, routable carrier.** *Pain:* handing an
   accepted review to next-steps / acceptance-map / to-issues / tdd is manual
   copy-paste that flattens severity, evidence anchors, and disposition — the
   highest-frequency manual bridge given how central review is. *Fix:* a
   lightweight shared findings hand-off shape (a tiny reference both review-family
   and consumers name) + a "Next Move" tail on review output grouped by
   disposition (act / narrow / verify-first / defer). The *inverse* of the
   rejected requesting-review meta-skill (post-review fan-out, not pre-review
   orchestration) — single-sources publishing through to-issues, never
   re-implements it.

## 7. External Inspirations

Useful ideas found via search, mapped to a local move. URLs are sources the
research agents actually retrieved.

| Inspiration | Source | Local mapping |
|---|---|---|
| **Eval-driven dev / eval gates for LLM features** (build evals before docs; golden sets; grader selection code-vs-LLM-judge-vs-human) | anthropic.com/engineering/demystifying-evals-for-ai-agents; appscale.blog AI-native CI/CD | New `eval-driven-dev` — **park** until a real LLM-feature need; keep qualitative to avoid the scored-gate ban |
| **Codemod / OpenRewrite recipe migrations** | github.com/codemod/codemod | New `codemod-migration` — build around uniformity + tool-selection judgment |
| **Coverage-guided characterization tests (CoverUp)** | arxiv.org/html/2403.16218v3 | New `characterize-legacy` — the deliberate inverse of tdd |
| **Blameless SRE/PIR postmortems** | incident.io/blog/sre-incident-postmortem-best-practices; borghei/Claude-Skills incident-commander | New `postmortem`; also the adherence-audit framing |
| **Production-readiness review (PRR)** | sreschool.com/blog/production-readiness-review-prr | New `production-readiness` in review-family (research backlog) |
| **Keep a Changelog / conventional commits** | keepachangelog.com; ComposioHQ/awesome-claude-skills | New `release-notes` — closes the post-"land" ship stage |
| **Multi-agent: per-subagent objective/boundary/output briefs; orchestrator-workers; self-consistency** | anthropic.com/engineering/multi-agent-research-system; building-effective-agents | `delegate-brief` (narrowed to fan-out check); second-opinion folds into scrutinize; fan-out as a possible execute-plan mode |
| **Context engineering: structured note-taking / external working memory** | anthropic.com/engineering/effective-context-engineering-for-ai-agents; effective-harnesses-for-long-running-agents | `working-memory` — **park** + one Working-Defaults line; `long-running-harness` backlog |
| **Agent Decision Records (ADR + agent/model/trigger metadata)** | github.com/me2resh/agent-decision-record; github/awesome-copilot | Expand grill-with-docs with a standalone on-demand ADR path; park separate `capture-decision` |
| **Codebase onboarding / repo-knowledge map** | github.com/affaan-m/everything-claude-code codebase-onboarding | `map-codebase` — **ledger-blocked** (parked code-comprehension); surface as a trigger candidate |
| **context7 general library-docs MCP** | settings.json (verified enabled) | New thin `library-docs` — adds house citation/budget discipline over the bare MCP |
| **Writing tools for agents (tool-output ergonomics)** | anthropic.com/engineering/writing-tools-for-agents | Expand `agent-facing-design` with a tool-output-ergonomics rubric (or a reference) — not a new skill |
| **Dependency-upgrade AI workflows; feature-flag cleanup; CI flake triage; doc-freshness; runbooks** | fossa.com; atlassian; medium flaky-tests; datahub continuous-context; eriklieben | Research backlog (`dependency-upgrade`, `flag-cleanup`, `ci-triage`, `doc-freshness-audit`, `doc-runbook`) — experiments pending observed friction |
| **Rejected/declined as covered** | spec-kit constitution; cursorrules anti-over-engineering & clarify-first; Zettelkasten/second-brain | Already owned (charter.md; global CLAUDE.md; outcome-interviewer+grill-me; deep-research+markdown-synthesis) — explicitly *not* proposed |

## 8. Recommended Next Moves

Ordered to test the highest-power ideas fastest while respecting the charter's
observed-friction bar. Tags: **[ship]** ready for implementation planning ·
**[pilot]** build a v1 and exercise on the next real task · **[design]**
discussion/decision needed first · **[review]** read-only review.

1. **[ship] Connective-tissue prose glue (Gaps #4 + #5).** Near-zero cost, no new
   machinery: add `save-handoff` routes to execute-plan Stops / gh-pr-review-loop
   Checkpoints / closeout-check "not ready"; add a disposition-grouped "Next Move"
   tail + shared findings shape to review-family. Highest power-to-cost ratio in
   the whole report. (Plugin publish path for the review-family/git-cycle/handoff
   edits.)

2. **[pilot] `integrate-branch` (new skill).** The clearest operational dead-end,
   strongest structural case. Build the bounded sibling (local-only,
   force-push-gated, conflict-loop, stop-before-push) and route the four ff-only
   skills' "rebase/merge needed" stops into it. Pilot on the next diverged-branch
   landing. (git-cycle publish path; gate the design through agent-facing-design
   first.)

3. **[ship] Evidence/observability expansions (section 4): execute-plan
   run-ledger + acceptance-map verify-mode + scrutinize-skill proof-recipe.** All
   three are within-lane upgrades that directly buy "less supervision, stronger
   evidence." The run-ledger is also the input for move #6.

4. **[pilot] `from-issue` (thin intake bridge).** Closes the only broken seam in
   the discovery->...->closeout chain. Keep it intake-only (delegate to
   execute-plan/implementation-planning); pilot once on a real `ready-for-agent`
   issue before sealing the size-fork wording.

5. **[design] `library-health` routing-audit lane (Gap #1).** Decide scope
   (Claude-only/repo-scoped) and the read-only audit surface. Uniquely apt here;
   the ledger already documents the friction. A design discussion because it is a
   new agent-facing contract over the corpus itself — run it through
   agent-facing-design.

6. **[design] Post-hoc adherence-audit lane (Gap #3) + the fold/expand
   right-sizings.** Decide whether adherence-audit is its own lane or part of
   `postmortem`; and approve the four fold/expand calls (reproduce-bug->diagnose,
   premortem->scrutinize, second-opinion->scrutinize,
   capture-decision->grill-with-docs) so no standalone slots get built by mistake.

7. **[pilot] New build-category experiments, in leverage order:
   `codemod-migration`, then `characterize-legacy`.** Build each only around its
   judgment core (uniformity + tool-selection; golden-master labeling) and pilot
   on the next repetitive-refactor / legacy-refactor task. `simplify-code`
   mechanical-batch mode first covers the pure-rename slice — sequence that ahead.

8. **[design] Fire-or-hold the parked candidates.** Bring `map-codebase` (parked
   code-comprehension), `eval-driven-dev`, `working-memory`, and `mcp-builder` to
   an explicit decision: each is a real gap whose reopen trigger has not fired.
   Decide whether current work counts as the trigger, or record fresh park
   entries — do not author on spec.

9. **[review] Downstream/ship-stage backlog triage.** A read-only pass to decide
   which of `release-notes`, `postmortem`, `production-readiness`,
   `dependency-upgrade`, `doc-freshness-audit`, `ci-triage` match *actual*
   workflow (several assume production services / user-facing releases this skills
   repo may not have). Admit only those with a plausible observed-friction path.

10. **[design] `library-routing-regression` corpus (Gap #2).** Lowest urgency,
    highest infrastructure value: a standing rerunnable guard that would replace
    the recurring manual health review. Worth a design discussion once
    `library-health` (#5) exists, since they share inventory machinery.

## Evidence Boundary

- **Inspected vs not:** as listed in section 2. This is a review of *source*
  `SKILL.md` + referenced files at commit `0a3c11d`; plugin caches, the GitHub
  mirror, `~/.claude/skills` symlink internals, and runtime/installed state were
  not inspected, and no runtime claims are made.
- **Independently verified firsthand** (orchestrator re-read the live files, not
  agent-relayed): merge-branch/SKILL.md:155-164 (non-ff dead-end);
  acceptance-map/SKILL.md ~52 + 290-296 (produces but never consumes the map);
  scrutinize/SKILL.md:54, 99-106 (Pre-Mortem already owned -> premortem fold);
  to-issues/SKILL.md:97-98 (hands to a non-existent "execution" lane);
  closeout-check/SKILL.md:242 lists `handoff` but the body never names
  `save-handoff`/`/save`; scrutinize-skill/SKILL.md has zero reference to
  `behavior-smoke-test`/`skill-benchmark`; execute-plan/SKILL.md has no
  ledger/resume concept; diagnose/SKILL.md:115-125 (lightweight inline
  post-mortem only).
- **Verified by the workflow pass, not re-opened personally:** the remaining
  `path:line` citations in sections 4-6. Each candidate cleared an adversarial
  verifier that re-read the live files and the ledger, but treat these as
  workflow-verified rather than orchestrator-verified.
- **Value confidence:** new-skill *value* is mostly inferred from structural gaps
  + ecosystem prevalence, not from observed in-repo friction (the charter's actual
  admission bar) — hence the `experiment`/`speculative` labels and the
  pilot/park-with-trigger framing throughout.
- **Status:** evidence, not authority, true at commit `0a3c11d`. Later edits can
  invalidate a specific citation — re-verify against live source. No skills,
  metadata, or runtime state were mutated producing this record.

## References

- Workflow run: `wf_7301d22c-498` (35 agents; 9 cluster maps + 6 research sets +
  3 cross-cutting lenses -> consolidation -> 16 verified candidates).
- Prior passes this review builds on, not duplicates:
  `docs/plans/artifacts/skill-library-apparatus-review-2026-06-17.md`
  (quality/trust-bar consolidation) and `docs/agents/contract-decisions.md`
  (admission/park/rejection ledger).
- Convention: `docs/reviews/README.md`.
