---
type: review
title: "Skill-Library Capability-Growth Review"
date: "2026-06-18"
scope: "48 live skills across skills/, skills-claude/, plugins/*/skills/"
reviewed_commit: 584289f
method: "18-agent read-only workflow (8 cluster deep-reads + 5 external-research sweeps + 3 ideation lenses + cross-library-gaps pass + completeness critic) + 10 independent skill reads + line-grep citation verification"
posture: "read-only; capability-growth-biased; net-additive"
status: evidence-not-authority
---

# Skill-Library Capability-Growth Review

Read-only review of the 48-skill library at `/Users/jp/.agents`. Method: an 18-agent workflow (8 cluster deep-reads + 5 external-research sweeps + 3 ideation lenses + cross-library-gaps pass + completeness critic), plus an independent read of 10 skills and direct line-grep verification of every load-bearing citation below. Bias, per the request: expansive capability growth.

---

## 1. Executive Summary — the 5 highest-value opportunities

The library is an exceptionally mature **thinking + safety + continuity** engine. Its weak axis is **"make / maintain / ship"** and **self-maintenance**. The five highest-leverage moves, biased toward capability growth:

1. **A shared structured *findings artifact* + a tiny `findings-ledger` connector** — *system-level + new skill.* Every producer (the 5 review-family skills, `tech-debt-scan`, `diagnose`, `improve-codebase-architecture`) emits prose-only findings; every consumer (`next-steps`, `acceptance-map`, `to-issues`) re-keys them by hand. One single-sourced schema turns the library's strongest asset — evidence discipline — into pipeline input. **Unblocks 5 separately-reported gaps at once** (the critic's #1, and I agree).

2. **Open a whole "durable repo knowledge" category, led by `to-adr`** — *new category, new skills.* Today `outcome-interviewer`, `making-recommendations`, `design-exploration`, `grill-with-docs`, `improve-codebase-architecture`, and `baseline` all produce settled decisions that evaporate at session end. `to-adr` (decision records) is the lead; the category also wants `to-changelog`/release-notes and `onboard-codebase` (a *durable* onboarding doc, distinct from `zoom-out`'s one-layer ephemeral map at `skills/zoom-out/SKILL.md:9-12`).

3. **Open a "recurring engineering maintenance" category** — *new skills.* The clearest single signal in the whole library: `tech-debt-scan/SKILL.md:136-137` and `implementation-review/SKILL.md:120-123` both route security findings **out to a skill that does not exist**. Lead members: a **vuln/security review** skill (must be named to avoid the bundled `security-review` command), **`dependency-upgrade`**, **`coverage-backfill`**, and **`codemod-migration`**. This is the library's biggest "find-and-recommend but never make" hole.

4. **A library self-maintenance category, led by the mandated-but-unowned `charter-decision`** — *new skills.* The repo *is* a 48-skill dual-runtime farm, and **no skill maintains it.** The charter names four mandatory events and requires a ledger entry per event (`docs/agents/charter.md:6,135`), yet **no skill references `docs/agents/contract-decisions.md`** (verified). Siblings: `skill-farm-audit` (routing/description-budget drift), `farm-delivery-check` (symlink/cache/version drift), `retire-skill` (nothing in the library can *remove* anything).

5. **Close the verified lifecycle-edge seams** — *new skills + expansions.* `open-pr` (the git plugin's tagline claims "merged-and-shared" but `gh-pr-review-loop` only pushes to an *existing* PR head, `…/SKILL.md:60,69`); a **divergence/rebase-resolution** lane (three git skills *detect* non-fast-forward and uniformly stop); **`execute-issue`** (`to-issues/SKILL.md:97-98` hands off to "execution" — a consumer that doesn't exist; `execute-plan` only eats plan *documents*); and a **behavior-changing-refactor-under-safety** executor (the "no correct seam" dead-end strands `diagnose` and `improve-codebase-architecture` outputs).

New skills: ~#2/#3/#4/#5. System-level: #1. Net direction is additive, as requested.

---

## 2. Coverage and Limits

**What was inspected (live working tree):**
- All 48 live `SKILL.md` files via the 8-cluster workflow (full read of each, plus support files: `references/`, `examples/`, `scripts/`, `agents/openai.yaml`).
- `AGENTS.md` (re-read live) and the charter pair (`docs/agents/charter.md`, `contract-decisions.md`).
- **Independent full reads (10):** `agent-facing-design`, `next-steps`, `zoom-out`, `scrutinize`, `baseline`, `orient-status`, `implementation-planning`, `tech-debt-scan`, `merge-branch`, `throughline`.
- **Direct citation verification (line-grep):** `tech-debt-scan`, `implementation-review`, `to-issues`, `exiting-worktrees`, `gh-pr-review-loop`, the charter, and the `security-review` name collision. All checked claims held (a few ±1-line offsets, substantively exact).

**What was NOT inspected:** the full body text of ~38 skills not personally read end-to-end (relied on cluster-agent reads + sampled-and-verified citations — found reliable, but not every cited line personally confirmed); the `references/` deep content of most skills; runtime/installed state (out of scope; no runtime mutation); `skills-archive/` (history, not live); the GitHub tracker (asserted-empty per handoff, not re-checked this turn).

**External search performed (5 angles, real URLs in §7):** mature skill/subagent ecosystems (Anthropic Skills, VoltAgent, awesome-claude-code, Claude-Command-Suite); code-review/PR automation (CodeRabbit, Greptile, Graphite, Qodo PR-Agent, Danger, Semgrep, Moderne); knowledge management (ADRs, runbooks, doc-drift, CONTEXT.md/memory); SDLC automation (Renovate, flaky-test lifecycle, CI triage, codemod, postmortems, semantic-release); AI work-loop meta-patterns (eval sets, context engineering, orchestrator-worker, generator-critic). The research agents ran the searches/fetches; the URLs were not independently re-fetched page-by-page — treat them as agent-sourced leads, verified for plausibility.

---

## 3. Current Library Map (by kind of work)

| Cluster | Skills | Maturity |
|---|---|---|
| **Adversarial review & critique** | `scrutinize`, `implementation-review`, `system-design-review`, `scrutinize-skill`, `review-reviewer` | **Strong.** Single-pass critique core; uniform evidence discipline + bounded-review mode. Thin *downstream* of the verdict. |
| **Skill/contract authoring, governance & proof** | `agent-facing-design`, `writing-principles`, `skill-ux-design`, `skill-benchmark`, `behavior-smoke-test`, `friction-to-guards` | **Strong** on a single target. **No** library-wide or charter-lifecycle operations. |
| **Framing, decision & interrogation** | `outcome-interviewer`, `design-exploration`, `making-recommendations`, `grill-me`, `grill-with-docs`, `zoom-out` | **Strong** routing lattice. **Decisions evaporate** (chat-only, no persistence). |
| **Planning → issues → execution → next** | `implementation-planning`, `to-prd`, `to-issues`, `triage`, `acceptance-map`, `execute-plan`, `next-steps` | **Strong** publication lanes. **Broken issue→execution seam**; acceptance-map output is not consumed. |
| **Code build / fix / quality** | `tdd`, `diagnose`, `prototype`, `simplify-code`, `improve-codebase-architecture`, `tech-debt-scan` | **Strong diagnose/survey.** Almost entirely *find-and-recommend*; one narrow executor (`simplify-code`). |
| **Git lifecycle** | `closeout-check`, `merge-branch`, `exiting-worktrees`, `gh-address-comments`, `gh-pr-review-loop`, `git-hygiene` | **Strong** local/safety half. **No open-PR, no divergence-resolution, no worktree *creation*.** |
| **Continuity, status & authority** | `load-handoff`, `save-handoff`, `search-handoffs`, `throughline`, `orient-status`, `baseline` | **Strong** session continuity. **No archival/pruning** of the pile; no durable knowledge. |
| **Knowledge, docs, external reference** | `markdown-reformat`, `markdown-synthesis`, `claude-code-docs`, `openai-docs`, `caveman`, `setup-matt-pocock-skills` | **Strong** OpenAI/Claude-Code doc grounding. **No Anthropic-API or arbitrary-library grounding; no knowledge capture.** |

**Already strong (don't over-invest):** adversarial review, authority/status resolution, decision *framing*, git *safety*, handoff continuity, skill *governance-as-judgment*.
**Thin (where growth pays):** durable repo knowledge; recurring engineering maintenance; the make/execute end of code work; ship-out (PR/release/changelog); library self-maintenance; cross-skill connective tissue.

---

## 4. Existing-Skill Upgrade Opportunities

| Skill | Current value | Limiting factor | Proposed upgrade | Why more power | Evidence |
|---|---|---|---|---|---|
| `implementation-review` | Falsification review → Blocked/Partial/Ship + ledgers | Rich ledger fields exist but output is prose-only; no carry-forward | **Opt-in structured ledger emit** (id, location, severity, status, requirement-link, fix) | Makes review pipeline-consumable; enables a fix-reverify loop | `…/SKILL.md:184-185` (fields already defined) |
| `implementation-review` | (as above) | Each invocation rebuilds ledgers from scratch | **`--reverify` mode**: ingest prior findings + new diff, re-adjudicate only blocked items | Converts review from snapshot to enforceable gate across iterations | `…/SKILL.md:171,173` (verdict taxonomy has no carry-forward) |
| `implementation-review` | (as above) | Security = one attacker/victim heuristic | **Promote a security sub-lens** (taint→sink, authz matrix) — or hand to the new vuln-review skill | Security is recurring and currently shallow | `…/SKILL.md:120-123` |
| `review-reviewer` | Adjudicates a *supplied* review with anti-anchoring | Explicit-invoke-only; can't commission *fresh* independent reviews | **Optional "panel" mode**: spawn N independent lenses, reconcile | The cluster has no multi-perspective review; this is the natural home | cluster thinness: "no way to run several adversarial lenses…and reconcile" |
| `acceptance-map` | Source-traceable observable checks | Nothing *consumes* the map to record pass/fail | **Make it a verification contract** `execute-plan`/`implementation-review` ingest | The map's leverage currently evaporates at verify time | gap: "acceptance-map produces…nothing consumes it" |
| `diagnose` | Hard-bug discipline → regression test | Stops at the seam: "no seam" is a dead-end finding | **Add a log/observability-forensics sub-mode**; route "no seam" to a refactor executor | Extends to running-system signals; unblocks the strand | research (SRE agent); critic "no correct seam" |
| `tech-debt-scan` | Capped, ranked, evidence-led audit artifact | Read-only; routes security + sequencing OUT | **Emit the shared findings schema** so `next-steps`/`to-issues` consume the Ranked Backlog directly | Removes the manual re-keying hop | `…/SKILL.md:136-137` (security out); gap: backlog not piped |
| `grill-with-docs` / `improve-codebase-architecture` | Persist ADR/terminology as a *side effect* | ADR format is buried, duplicated across two skills | **Single-source the ADR format**, consumed by a new `to-adr` | Stops format drift; opens a clean ADR-only path | ideation: "single-source the ADR format…not fork a third" |
| `save-handoff` / `throughline` | Session continuity quartet | No archival/pruning; `throughline` *assumes* `archive/` exists | **Add a handoff-hygiene step** that creates/prunes `archive/` | Closes a lifecycle hole the quartet already depends on | `throughline/SKILL.md:53-56` (assumes archive subdirs) |
| `skill-benchmark` / `behavior-smoke-test` | Two proof rungs | Both forbid a kept harness → proof rots silently on next edit | **Store *pointers* (target + proof-type + last-verified rev)** for a staleness check (not a daemon) | Catches silent regression without smuggling in a banned harness | gap: "both proof rungs point-in-time, no regression watch" |
| `next-steps` | Dependency-aware sequencing of findings | Requires hand-supplied findings | **Accept the shared findings schema as input** | Auto-flows review/audit output into sequencing | `skills/next-steps/SKILL.md:28-32` (findings must be supplied) |
| `openai-docs` / `claude-code-docs` | Provider-doc grounding | Stops at OpenAI + Claude-Code; a `context7` MCP server is present but unused for libraries | **Add an Anthropic-API + arbitrary-library grounding lane** (use context7) | Closes the third-provider + general-library gap | cluster thinness; context7 MCP in environment |
| `grill-me` / `grill-with-docs` | Near-identical pressure-test prose | Reachable only by direct invocation; not referenced inbound | **Add inbound routes** from `scrutinize`/`implementation-planning`; *consider* (don't rush) consolidating the shared body | Raises reach without losing the doc-aware variant | cluster thinness: "near-duplicate…neither referenced inbound" |

*(Consolidation note: the grill pair overlaps, but per the review posture it is flagged as a watch-item, not a prune — `grill-with-docs` adds real doc-awareness; merge only if maintenance drag shows up.)*

---

## 5. New Skill Candidates

De-duplicated across lenses; confidence-labeled. Names chosen to avoid bundled collisions (the critic caught that `security-review` is the **Claude built-in command** — renamed below).

| Proposed skill | User problem | Likely trigger | Why separate (not an expansion) | Adjacent skills | First-version scope | Risks | Confidence / inspiration |
|---|---|---|---|---|---|---|---|
| **`findings-ledger`** | Producers emit prose; consumers re-key by hand | "save these findings", "pipe the review into next-steps" | The missing *data plane* — not a producer or consumer | review-family, `tech-debt-scan`, `next-steps`, `to-issues`, `acceptance-map` | Append/read one Markdown(+JSON-fence) ledger: id, claim, severity, evidence pointer, observed/inferred/unverified, disposition | Machinery risk — `agent-facing-design` exists to stop required-field ledgers; keep it lightweight, context-not-machinery | **high-confidence**; critic #1 |
| **`to-adr`** | Settled decisions evaporate at session end | "record this decision / write an ADR" | Not `grill-with-docs` (interrogation w/ ADR side-effect) or `baseline` (resolves authority, can't write it) | `design-exploration`, `baseline`, `making-recommendations`, `grill-with-docs` | Write one ADR (context/decision/alternatives/consequences) to repo ADR dir; create-and-supersede | Must single-source the ADR format shared with two skills | **high-confidence**; ADR-with-AI refs |
| **`to-changelog`** | No release-notes/version-derivation from a commit range | "write the changelog", "what changed since last tag" | Not `merge-branch` (refuses remote/release) or `markdown-synthesis` (needs existing .md files) | `merge-branch`, `closeout-check`, `markdown-synthesis` | `last-tag..HEAD` → grouped changelog + next-semver + breaking-change flags | Degrades on unstructured commit messages — must flag low signal | **high-confidence**; semantic-release/conventional-changelog |
| **`onboard-codebase`** | No *durable* comprehension doc for an unfamiliar repo | "help me understand this repo", "write an onboarding guide" | Not `zoom-out` (ephemeral, one-layer, chat-only) or `orient-status` (status, not structure) | `zoom-out`, `orient-status`, `improve-codebase-architecture` | Read-only sweep → onboarding doc: purpose, subsystems+seams, build/test/run, entry points; every claim path-anchored + timestamped | Onboarding docs rot fast — must anchor + date-stamp | **high-confidence**; agentic codebase-QA refs |
| **`vuln-review`** (NOT `security-review`) | Two skills route security OUT to a non-existent owner | "security review this", "check for vulnerabilities" | `implementation-review` security = one heuristic; `tech-debt-scan` explicitly excludes it | `implementation-review`, `tech-debt-scan`, `scrutinize` | Scope a diff/module: secret scan + taint→dangerous-sink trace + authz/SSRF/deserialization lenses; honest coverage statement | **Name collision** with bundled `security-review`; false-negatives costly — never imply "clean" from a bounded pass | **high-confidence**; `tech-debt-scan/SKILL.md:136-137` |
| **`dependency-upgrade`** | A pile of bumps with no disciplined upgrade lane | "upgrade these deps", "we're behind on X" | The only candidate that *mutates manifests/lockfiles* under a build/test proof gate | `tech-debt-scan`, `simplify-code`, `diagnose` | One ecosystem's manifest+lockfile; group by risk; read breaking-change notes; apply + prove via build/test | A "safe" minor can still break at runtime — proof gate is load-bearing | **high-confidence**; Renovate |
| **`coverage-backfill`** | Untested code needs characterization tests | "add tests to this module", "pin down before refactor" | Inverted evidence model from `tdd` (pin *observed* behavior incl. bugs, not drive new) | `tdd`, `diagnose`, `improve-codebase-architecture` | One module: identify public surface + highest-value untested branches; write characterization tests | Encoding bugs as "correct" — must separate pinned-vs-asserted | **high-confidence**; coverage-gap refs |
| **`codemod-migration`** | Large mechanical transforms owned by nobody | "rename X→Y everywhere", "migrate all callers" | `simplify-code` is single-scoped and refuses multi-target | `simplify-code`, `improve-codebase-architecture`, `tdd` | One transform rule; **preview all sites (dry-run)** → apply → per-batch build/test | Over-broad matching corrupts sites — preview gate is load-bearing | **promising-experiment**; Moderne/codemods |
| **`charter-decision`** | The mandated four-event lifecycle + ledger has no owner | "admit/fold/retire this contract", "log the charter decision" | `agent-facing-design` is the *gate*, not the lifecycle/ledger runner | `agent-facing-design`, `scrutinize-skill`, `friction-to-guards` | Walk admission/fold/rejection-park/retirement; write the required `contract-decisions.md` entry with evidence pointer | Repo-specific; must match charter wording exactly | **high-confidence**; `charter.md:6,135` + no skill refs the ledger (verified) |
| **`skill-farm-audit`** | No skill surveys the whole farm for drift/collisions | "audit the library for routing collisions / budget" | Every governance skill is single-target by contract | `scrutinize-skill`, `agent-facing-design`, `writing-principles` | Read-only: trigger-collision matrix, dead cross-references, 3-surface description drift, Codex ~2% budget pressure | Heuristic collisions → false positives; label confidence | **high-confidence**; AGENTS.md budget flag |
| **`farm-delivery-check`** | Symlink/cache/marketplace/version drift unowned | "check the skills are delivered/synced" | Distinct from `skill-farm-audit` (hygiene) — this owns *delivery-state* correctness | `claude-skills-sync.sh`, `codex-plugins-sync.sh` | Read-only: symlink-vs-source, cache-vs-source, manifest version vs behavior change | Overlaps existing scripts — should wrap/report, not duplicate | **promising-experiment**; critic additional |
| **`retire-skill`** | Nothing in the library can *remove* anything | "retire this skill", "demote this rule", "sweep dead refs" | Every other skill *adds*; retirement is its own evidence discipline (charter Retirement) | `charter-decision`, `friction-to-guards`, `scrutinize-skill` | Move a skill → `skills-archive/`, sweep inbound references, write ledger entry | Must respect the no-recovery-for-sensitive precedent | **promising-experiment**; critic additional |
| **`open-pr`** | Git plugin can't *open* a PR (only respond/merge) | "open a PR", "push and file the PR" | Not `gh-pr-review-loop` (existing PR head) or `merge-branch` (local-only) | `closeout-check`, `gh-pr-review-loop`, `merge-branch` | From a committed branch: pre-push scan → push → draft intent-first PR body/template → (optional) reviewers | Publish authority must be hard-gated (explicit-invoke) | **high-confidence**; `gh-pr-review-loop/SKILL.md:60,69` |
| **`execute-issue`** | `to-issues`' "execution picks up" consumer doesn't exist | "do issue #42", "implement this ticket" | `execute-plan` consumes plan *documents* only | `to-issues`, `triage`, `execute-plan`, `acceptance-map` | Fetch a ready-for-agent issue + its agent brief; implement under `execute-plan`'s two-stage gates; report back | Boundary with `execute-plan` — could expand it instead | **high-confidence**; `to-issues/SKILL.md:97-98` |
| **`resolve-divergence`** | 3 git skills detect non-FF and uniformly stop | "rebase this", "the branch diverged", "fix conflicts" | The detect-and-stop skills route *into* it; rebase/squash/reword absent everywhere | `merge-branch`, `git-hygiene`, `exiting-worktrees` | Conflict-resolution assistance + interactive-style rebase/squash/reword with reflog-based recovery | Highest-risk git case — recovery path must be bulletproof | **promising-experiment**; critic gap |
| **`refactor-under-safety`** | "No correct seam" strands `diagnose`/`improve-codebase-architecture` | "build the seam", "do this deepening refactor" | `improve-codebase-architecture` surveys only; `simplify-code` refuses behavior/architecture change | `diagnose`, `improve-codebase-architecture`, `simplify-code` | Consume one deepening candidate or "no seam" finding; behavior-changing extract/seam-build under test + restorable backup | Behavior-changing edits — needs `simplify-code`-grade safety machine | **promising-experiment**; critic #3 |
| **`pre-mortem`** | `outcome-interviewer`/`scrutinize`/`grill-me` all gap on a standalone failure-imagination + assumption ledger | "pre-mortem this", "imagine this failed — why?" | Each adjacent skill routed it as "expand/not-now"; none owns a *durable* assumption ledger | `scrutinize`, `grill-me`, `acceptance-map` | "Assume it failed in 6 months" → ranked failure paths + assumption ledger (validated/plausible/wishful/unverified) persisted | Overlap with `scrutinize`'s internal pre-mortem — must be the *standalone durable* version | **speculative**; critic additional |
| **`working-memory`** | No durable mid-task scratchpad distinct from handoffs | "keep notes as you go", "remember this for later in the task" | Handoffs are session-boundary continuity; this is *in-task* memory | `save-handoff`, `load-handoff` | Size-bounded scratch doc the agent writes mid-task and reloads after compaction | Overlaps handoffs — boundary must be in-task vs cross-session | **speculative**; context-engineering refs |
| **`incident-response`** | No live-outage first-response lane | "prod is down", "we have an incident" | `diagnose` is reproducible-bug-first, not live stabilize-then-capture | `diagnose`, `orient-status`, `merge-branch` | Staged: confirm blast radius → record mitigation → stabilize → handoff to `postmortem` | Speculative for a single-user repo-tooling library — may not run prod | **speculative**; PagerDuty/SRE |

*(Folded duplicates: `dependency-upgrade-triage`→`dependency-upgrade`; `release-notes`→`to-changelog`; `postmortem` kept distinct from `incident-response` (after-vs-during). Lower-leverage / deferred per critic: `context-budget` as its own skill (fold into `skill-farm-audit`), EARS phrasing (a refinement of `acceptance-map`, not a skill), `evidence-bank`/`task-context-preflight` (high overlap with `findings-ledger`/`baseline`/`load-handoff`).)*

---

## 6. Cross-Library Power Gaps

The connective tissue is where this library most under-delivers relative to the quality of its parts.

1. **No shared findings data-plane (connective tissue).** Reviews/audits/diagnoses emit prose; `next-steps`/`acceptance-map`/`to-issues` re-key by hand. *Pain:* a 10-finding review becomes 10 manual copy-pastes; severity/file:line/disposition are lost at every hop. *Fix:* the shared findings schema (§1.1).
2. **No closed-loop fix-and-reverify outside GitHub (missing lifecycle step).** The review cluster hard-stops read-only; `gh-address-comments` closes only GitHub PR threads. *Pain:* `implementation-review` returns `Blocked` with 3 fixes; nothing re-runs the falsification pass to confirm they landed. *Fix:* `--reverify` mode consuming the findings artifact.
3. **`acceptance-map` output is produced but never consumed (connective tissue).** *Pain:* you build a careful acceptance map, then the executor/reviewer re-derive verification from prose — the map's leverage evaporates. *Fix:* make it a verification contract `execute-plan`/`implementation-review` ingest.
4. **The issue→execution seam is broken (missing lifecycle step).** `to-issues/SKILL.md:97-98` hands to "execution"; no skill consumes a ticket + brief end-to-end. *Pain:* "do issue #42" is impossible without manual re-conversion. *Fix:* `execute-issue` (or expand `execute-plan`).
5. **Framing decisions have no persistence path (missing lifecycle step).** `outcome-interviewer`/`grill-me`/`design-exploration`/`making-recommendations` end chat-only. *Pain:* a long interrogation's hardened conclusions are gone next session; re-litigation from scratch. *Fix:* route to `save-handoff` / `to-adr`.
6. **Both proof rungs are point-in-time (missing validation/proof).** `behavior-smoke-test` and `skill-benchmark` forbid a kept harness. *Pain:* a proven-followed rule silently regresses on the next edit. *Fix:* a pointer-based staleness check (`proof-watch`), not a daemon.
7. **No library-wide audit (missing reusable workflow).** Nothing sweeps the 48-skill farm for routing collisions, dead cross-refs, 3-surface description drift, or Codex ~2% budget pressure. *Pain:* as the farm grows, undisambiguable trigger overlaps and budget-truncated skill lists go unnoticed. *Fix:* `skill-farm-audit` + `farm-delivery-check`.
8. **The charter lifecycle is mandated but unowned (missing reusable workflow).** Verified: `charter.md:6,135` requires a ledger entry per event; **no skill references `contract-decisions.md`**. *Pain:* the repo's own governance rule has no executor — entries are hand-written each time. *Fix:* `charter-decision`.
9. **Git ship-out and recovery seams (missing lifecycle steps).** No `open-pr`; no `resolve-divergence`; no worktree *creation* (`exiting-worktrees/SKILL.md:248` only exits). *Pain:* the highest-friction git moments (diverged branch, opening a PR) drop you to raw `gh`/`git`.
10. **The code cluster is find-and-recommend with one narrow executor (cross-skill glue).** Audits, architecture candidates, and "no seam" findings have nowhere to land but ad-hoc implementation. *Pain:* every accepted finding becomes unstructured manual work. *Fix:* `refactor-under-safety` + `codemod-migration` + the findings artifact.

---

## 7. External Inspirations

Useful patterns found via search, mapped to a local move. (URLs are agent-sourced leads, verified for plausibility, not re-fetched page-by-page.)

**Skill/subagent ecosystems** — onboarding, postmortem, dependency-migration, security, and release-note skills are near-universal in mature personal libraries; this one lacks all five.
- `everything-claude-code/.../codebase-onboarding` → **`onboard-codebase`** · https://github.com/affaan-m/everything-claude-code
- `anthropics/claude-code-security-review` → **`vuln-review`** · https://github.com/anthropics/claude-code-security-review
- `qdhenry/Claude-Command-Suite` (interface-contract review, release notes) → expand review-family / **`to-changelog`** · https://github.com/qdhenry/Claude-Command-Suite
- VoltAgent 100+ subagents (a11y, parallel exploration) → mostly **not-now** · https://github.com/VoltAgent/awesome-claude-code-subagents

**Code-review / PR automation** — the library has judgment-grade critique but not the *PR-mechanics* layer these tools industrialized.
- Qodo PR-Agent `improve` (ranked committable suggestions) → **findings-to-suggestions** (after the findings schema) · https://github.com/Codium-ai/pr-agent
- Danger JS (mechanical PR-hygiene checks) → **expand `friction-to-guards`** · https://danger.systems/js/
- Moderne large-scale change (vet a transform once, skip per-diff review) → **`codemod-migration`** · https://www.moderne.ai/blog/large-scale-code-changes
- Graphite incremental review (diff against prior review state) → **`implementation-review --reverify`** · https://graphite.com/guides/integrate-ai-code-review-github
- Semgrep custom workflows (assemble a named review pipeline) → **system / not-now** · https://semgrep.dev/blog/2026/introducing-semgrep-custom-workflows/

**Knowledge management** — the clear missing "durable repo knowledge" lane.
- ADRs with AI assistants → **`to-adr`** · https://blog.thestateofme.com/2025/07/10/using-architecture-decision-records-adrs-with-ai-coding-assistants/
- Codebase Q&A / onboarding pattern → **`onboard-codebase`** · https://agentic-patterns.com/patterns/agent-powered-codebase-qa-onboarding/
- Runbook authoring → **`to-runbook`** (speculative) · https://tianpan.co/blog/2026-04-12-ai-assisted-incident-response
- conventional-changelog / semantic-release → **`to-changelog`** · https://github.com/conventional-changelog/conventional-changelog
- CONTEXT.md / MEMORY.md persistent project memory → **system / `working-memory`** · https://explainx.ai/blog/what-is-memory-md-ai-agent-persistence
- ADR-as-fitness-function → **expand `friction-to-guards`** · https://platformtoolsmith.com/blog/operationalizing-adrs-fitness-functions/

**SDLC automation** — the weekly operational loops the library lacks.
- Renovate → **`dependency-upgrade`** · https://github.com/renovatebot/renovate
- CI-failure triage (GitLab AI root-cause) → **`ci-failure-triage`** · https://about.gitlab.com/blog/quickly-resolve-broken-ci-cd-pipelines-with-ai/
- Slack flaky-test auto-detection/suppression → **`flaky-test-lifecycle`** · https://slack.engineering/handling-flaky-tests-at-scale-auto-detection-suppression/
- PagerDuty postmortem template → **`postmortem`** · https://response.pagerduty.com/after/post_mortem_template/
- Cursor coverage backfill (−85% time) → **`coverage-backfill`** · https://engineering.salesforce.com/how-cursor-ai-cut-legacy-code-coverage-time-by-85/

**AI work-loop meta-patterns** — capabilities that multiply the other skills.
- Anthropic "Demystifying evals" (durable graded eval *sets*) → **`author-eval-set`** (pairs with `skill-benchmark`) · https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Anthropic context-engineering (agentic note-taking, JIT retrieval) → **`working-memory`** / context-budget pass · https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic multi-agent research (orchestrator-worker, condensed returns) → **system** (already used via the Workflow tool) · https://www.anthropic.com/engineering/multi-agent-research-system
- Multi-aspect verifier panel (test-time verification) → **expand `scrutinize` / `review-reviewer` panel mode** · https://arxiv.org/pdf/2502.20379

**Rejected / not-now:** accessibility review, alert/SLO triage, perf-regression bisect, C4-diagram generation, teaching/explain lane — real but low-fit for a single-user repo-tooling library right now. `expand:deep-research` is **non-actionable** (deep-research is a bundled Claude skill, not in this library).

---

## 8. Recommended Next Moves (ordered)

Biased toward quickly testing the highest-power new ideas. Every item below creates agent-facing contract text, so two gates apply per the repo rules: the **`agent-facing-design`** minimalism gate and a **charter consult** (`docs/agents/charter.md`) before authoring.

1. **[design discussion]** Settle the **shared findings schema** (§1.1) — `design-exploration` on the smallest schema that review-family + `tech-debt-scan` + `diagnose` emit and `next-steps`/`acceptance-map`/`to-issues` consume. This is the keystone; sequence it first because 5 other moves depend on it. *Watch the machinery risk — keep it context, not a required-field system.*
2. **[ready for implementation planning]** **`to-adr`** + single-source the ADR format out of `grill-with-docs`/`improve-codebase-architecture`. Highest-confidence new skill, opens the durable-knowledge category, closes the "decisions evaporate" gap. Low risk, high reuse.
3. **[ready for implementation planning]** **`open-pr`** in `git-cycle`. Verified false-coverage gap, high-frequency, low-ambiguity, consumes `closeout-check` output. Hard-gate publish authority (explicit-invoke) to match library posture. *(Plugin-distributed → follows the publish path, not the local-skill flow.)*
4. **[read-only review first, then implementation planning]** **`charter-decision`** + `contract-decisions.md` writer. Most repo-specific, mandated-but-unowned. Start read-only: confirm the charter's exact four-event wording and ledger fields, then author to match precisely.
5. **[design discussion]** Scope the **`vuln-review`** skill — and **resolve the name** (avoid the bundled `security-review` command; consider `vuln-review` or a `codex-security` plugin `security-scan` to match the existing dangling reference). Two skills already expect this owner. Decide coverage honesty rules before building.
6. **[behavior smoke-test, then ship]** Pilot **`onboard-codebase`** against this very repo and one foreign repo via the `behavior-smoke-test` lane — fast way to prove the durable-knowledge category earns its keep before expanding it.
7. **[ready for implementation planning]** **`dependency-upgrade`** + **`coverage-backfill`** as the first two "recurring maintenance" members — both high-confidence, both with a clear build/test proof gate. Sequence `coverage-backfill` first (it de-risks every later refactor/migration move).
8. **[read-only review]** Run a one-off **`skill-farm-audit`**-style sweep *manually* now (routing collisions, 3-surface description drift, Codex ~2% budget headroom) to validate the audit's value before committing it as a standing skill; pair with a `farm-delivery-check` dry-run.
9. **[design discussion]** **`execute-issue` vs expand `execute-plan`** — decide whether the issue-consumer is a new skill or a second input contract on `execute-plan`. This closes the broken planning→execution seam (gap #4).
10. **[backlog / promising-experiments]** Queue `to-changelog`, `codemod-migration`, `resolve-divergence`, `refactor-under-safety`, `retire-skill`, `pre-mortem`, and the `--reverify`/panel review expansions — strong but second-wave; most become much cheaper once the findings schema (move 1) exists.

**One sequencing insight:** moves 1 (findings schema) and 2/4 (the two durable-record writers, `to-adr` + `charter-decision`) are the true force-multipliers — the schema converts the strongest asset (evidence discipline) into pipeline fuel, and the record-writers stop hard-won decisions and governance events from evaporating. Everything in the "make/maintain" categories gets cheaper and safer once those three land.

---

## Evidence Boundary

This is a point-in-time review at commit `584289f`, not authority. Citations to existing skills are live `path:line`; load-bearing ones were independently line-grep-verified at review time. ~38 skills were read via cluster-agent proxies with sampled-and-verified citations (reliable, not exhaustively re-confirmed). External URLs are agent-sourced leads. New skills are labeled high-confidence / promising-experiment / speculative; none were rejected for lack of existing proof. The net recommendation is additive — the only consolidation raised (`grill-me`/`grill-with-docs`) is flagged as a watch-item, not a prune. A skill edit after `584289f` can invalidate a specific citation — re-verify against live source before acting.
