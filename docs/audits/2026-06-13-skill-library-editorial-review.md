# Skill Library Editorial Review — `/Users/jp/.agents`

- **Date:** 2026-06-13
- **Scope:** `skills/` (34 dual-runtime), `skills-claude/` (5 Claude-only), `plugins/handoff/` (4), `plugins/review-family/` (5) — 48 skills total.
- **Mode:** Read-only editorial review. No skill edits, moves, renames, publishes, or runtime mutations were made to produce it.
- **Authority:** Point-in-time snapshot. The checked-out working tree was the source of truth; `AGENTS.md` was the repo-local authority for layout, placement, proof, and skill-editing norms. This is derived analysis, not current truth — re-anchor any claim against live source before acting on it.
- **Method:** A multi-agent workflow (65 agents: 48 per-skill structured assessments → 6 cross-cutting lenses over the full corpus → 11 adversarial verifications that tried to *refute* every merge/split/archive/relocate/rewrite recommendation), cross-checked against 18 independent full-body reads and objective measurements (description word counts, referenced-path existence, support-file orphans, cross-skill routing graph, `.DS_Store`/pyc git-tracking). Only the 11 structural recommendations were adversarially stress-tested; `INVESTIGATE`/policy findings are decisions, not verified directives.

---

## Executive Summary

1. **The pruning thesis doesn't hold — and that's the headline.** Across 48 skills, 65 review agents, and 18 independent reads, there are **zero archive candidates, zero "not worth keeping" skills** (43 yes / 5 borderline / 0 no), and **47/48 descriptions are clean**. Cluster boundaries are reciprocal and source-confirmed, not nominal. Don't go looking for cuts; the real work is tightening and connecting.

2. **Body bloat — not redundancy — is the systemic defect.** 13/48 bodies are overbuilt; the house style restates routing/boundary/stop rules 3–4× per skill. This is where "context pollution / unnecessary process" actually lives. Worst offenders: `skill-ux-design` (335 lines + a 216-line rubric ~70% duplicating the body, `skill-ux-design/references/ux-rubric.md`), `review-reviewer` (384, two parallel packets), `outcome-interviewer` (310, ~2× needed), `markdown-synthesis` (175, ~2.5× its sibling), `orient-status` (boundary text stated four times).

3. **The library's one genuine mutation-lifecycle hole:** `grill-with-docs` and `improve-codebase-architecture` write durable repo files (`CONTEXT.md`, `docs/adr/*`) inline with **no dirty-check, no commit posture, no proof boundary, no "files I touched" report** — while *every* other durable-writer (acceptance-map, tech-debt-scan, to-prd, to-issues, design-exploration) governs its writes. This is the single most valuable substantive fix. (CONFIRMED by adversarial verification.)

4. **A small set of confirmed connective/routing fixes**, each a few lines: `gh-pr-review-loop` is publish-authorized yet silently model-invocable (missing the explicit-only flags its sibling `review-reviewer` sets); `to-prd` is a pipeline dead-end with no forward pointer to `to-issues`; the **entire 5-skill review-family plugin is functionally unreachable by name from the dual-runtime build pipeline**; `acceptance-map` mis-routes its post-implementation handoff to `closeout-check` (which never consumes the map) instead of `implementation-review`; `scrutinize-skill`'s Codex-branded companion contradicts its runtime-neutral skill.

5. **The adversarial layer earned its cost: it overturned 7 of 11 structural recommendations.** It *refuted* the `grill-me`/`grill-with-docs` merge (grill-with-docs is a producer node with live downstream consumers), *refuted* the `friction-to-guards` relocation (a sibling precedent makes "Codex-excluded by choice" legitimate), *refuted* a `to-prd` "rewrite" entirely, and *narrowed* several "rewrites" to one-line edits. Treat the lens recommendations as raw; treat the verdicts as the answer.

6. **One genuine capability gap:** no owner for **applying a *local or pasted* set of review findings** (verify→classify→fix→stop). The discipline exists but is locked inside GitHub plumbing (`gh-address-comments`) and read-only adjudication (`review-reviewer`'s Current Claim Check). This is an *extraction*, not a net-new skill — and only if a friction search confirms it.

7. **Three placement/policy decisions are yours to make, not mechanical fixes:** (a) `friction-to-guards` and `setup-matt-pocock-skills` are both runtime-neutral yet confined to `skills-claude/` — deliberate "Codex-excluded by choice" or unexamined default? (b) no local code skill (`simplify-code`, `diagnose`, `tech-debt-scan`) fences the Claude-**bundled** functional twins (`/simplify`, `/debug`, `/code-review`), so they silently compete on Claude.

8. **Naming/lineage smell:** the `setup-matt-pocock-skills` / `to-prd` / `to-issues` / `triage` / `grill-with-docs` sub-family carries imported-author provenance (`triage-labels.md:5` "Label in mattpocock/skills"), and the invocation token `/setup-matt-pocock-skills` describes its author, not its job. Borderline-value and worth de-branding.

9. **Two phase-1 corpus errors to *not* act on** (the lenses already caught them, both verified against source): `.DS_Store`/`__pycache__` are **not** committed (gitignored OS noise), and `claude-code-docs:44`'s underscore/hyphen namespace split is **deliberate**, not a bug.

## Coverage And Limits

**Inspected directly:** `AGENTS.md` in full; all 48 `SKILL.md` frontmatter blocks; 18 full `SKILL.md` bodies (baseline, orient-status, zoom-out, grill-me, grill-with-docs, markdown-reformat, markdown-synthesis, outcome-interviewer, making-recommendations, review-reviewer, simplify-code, behavior-smoke-test, acceptance-map, closeout-check, design-exploration, implementation-planning, execute-plan, next-steps, to-prd, to-issues); objective measurements across all 48 (description word counts, referenced-path existence, support-file orphans, cross-skill routing graph, `.DS_Store`/pyc git-tracking).

**Inspected via workflow (65 agents):** every skill's `SKILL.md` + `agents/openai.yaml` + references/examples/scripts/tests (48 structured assessments); 6 cross-cutting lenses reading source directly; 11 adversarial verifications re-reading source to refute each structural recommendation. Plugin manifests, `marketplace.json`, READMEs/CHANGELOGs were covered by the placement lens.

**Limits:**

- **Source-only, as instructed.** No runtime/installation/Codex-availability claims. The one place this bites: the Claude tool namespace for claude-code-docs was verifiable (hyphens, live in-session) but the Codex underscore namespace was not — left as "verify," not asserted.
- **Only the 11 *structural* recommendations were adversarially stress-tested.** The `INVESTIGATE`/policy findings (bundled-twin fencing, placement decisions, the capability gap, the review-family seam) are presented as decisions, not verified directives — they deserve a deliberate call, not a reflexive patch.
- **Phase-1 per-skill assessments carried a few errors** (the `.DS_Store`-committed and namespace-bug claims). The corpus was treated as a map, not proof; load-bearing claims were verified against source. Per-skill prose not personally re-read should be taken as high-confidence-but-unverified.
- The long support files (e.g., `simplify-code`'s ~970 lines of scripts/tests) were confirmed to exist, be referenced, and be git-clean, but not read line-by-line.

## Highest-Priority Findings

### 1. The durable-write mutation-lifecycle hole (the one real substantive gap)

- **Judgment:** rewrite (additive, ~2–4 sentences each) — **CONFIRMED** by adversarial verification.
- **Why it matters:** `grill-with-docs` and `improve-codebase-architecture` eagerly create/modify `CONTEXT.md` and `docs/adr/*` mid-conversation with no worktree gating, no commit-or-leave-dirty statement, no proof boundary, and no post-write report. An agent can scribble into a user's repo with dirty-tree collisions and no trace — the exact failure every other writer in the library is engineered to prevent.
- **Evidence:** `skills/grill-with-docs/SKILL.md:52,74`; `skills/improve-codebase-architecture/SKILL.md:78,79`; a grep of grill-with-docs for `commit|dirty|approv|proof|authority` returns **zero** matches; contrast `skills/acceptance-map/SKILL.md:214-271,282` and `skills/tech-debt-scan/SKILL.md:44-48`.
- **Recommended action:** Add a parallel clause to **both** (worded in parallel — they share `CONTEXT-FORMAT.md`/`ADR-FORMAT.md`): confirm a clean-enough write path; state the posture explicitly as *leave-dirty + report which files were created/edited*; one proof-boundary line; a wrap/stop line. Scope it to the **uncontracted inline `CONTEXT.md` write + lazy file creation** — the ADR offer is already gated (`grill-with-docs:78-86`). Route through `writing-principles`, gated by `agent-facing-design` (new mutation obligation). Do **not** merge or broaden the two skills.

### 2. `gh-pr-review-loop` is publish-authorized but silently model-invocable

- **Judgment:** rewrite → **narrowed to a two-flag additive change** — **CONFIRMED**.
- **Why it matters:** Its description says "Use only when explicitly invoked," and it owns destructive publishing (push, thread resolution, `@codex review`). Yet its frontmatter lacks `disable-model-invocation: true` and its `openai.yaml` lacks `allow_implicit_invocation: false` — so a bare "address these PR comments" can auto-route into the *publishing* loop instead of the safe local-commit sibling `gh-address-comments`. Its sibling `review-reviewer` uses identical phrasing **and** sets both flags.
- **Evidence:** `skills/gh-pr-review-loop/SKILL.md:1-4` (no flag), `:3` (explicit-only claim + publish authority); `skills/gh-pr-review-loop/agents/openai.yaml:1-4` (no policy block); contrast `plugins/review-family/skills/review-reviewer/SKILL.md:4` + `agents/openai.yaml:7`.
- **Recommended action:** Add `disable-model-invocation: true` and the `allow_implicit_invocation: false` policy block. Local dual-runtime skill → ordinary branch-off-main flow, not the plugin path. Verify with a behavior-smoke-test that "address the comments on this PR" routes to `gh-address-comments`. **Do not** turn this into a library-wide flag crusade — 10+ explicit-only skills intentionally rely on the description boundary; this one matters *because* of its publish authority. (`caveman` has the same gap but is harmless and, being dual-runtime, the Claude-only flag wouldn't even fix it on Codex.)

### 3. The review-family plugin is functionally unreachable from the build pipeline

- **Judgment:** investigate → make one availability-conditional reference each (decision for the owner).
- **Why it matters:** Five well-built review skills exist, but `execute-plan` re-implements spec/quality review inline and names no review skill for its final pass, and `closeout-check` defers only to a generic "owning review lane." No `skills/` skill forward-routes to `implementation-review` by name. The plugin is high-quality and orphaned from the pipeline that should feed it.
- **Evidence:** `skills/execute-plan/SKILL.md:45-46`; `skills/closeout-check/SKILL.md:103`; routing graph shows zero dual-runtime→implementation-review edges.
- **Recommended action:** In those two spots, name `review-family:implementation-review` "when available," falling back to the inline review — the AGENTS.md-blessed way to reference a plugin skill from a dual-runtime skill. Confirm intended primary-vs-fallback first.

### 4. `to-prd` is a pipeline dead-end

- **Judgment:** rewrite → **one sentence** — **CONFIRMED**.
- **Why it matters:** Every front-pipeline skill names its successor; `to-prd` publishes and stops, even though its own body says the PRD "is a source artifact still to be sliced into implementation issues" — which is exactly `to-issues`' job. `grep -c to-issues to-prd/SKILL.md` = 0.
- **Evidence:** `skills/to-prd/SKILL.md:26-34,34`; consumer ready at `skills/to-issues/SKILL.md:3,29`; contrast peers `design-exploration:64-67`, `implementation-planning:57-59`, `acceptance-map:283`.
- **Recommended action:** Add one closing handoff line after step 3 naming `to-issues` (+ `triage`, since a fresh PRD carries `needs-triage`). Route through `writing-principles`.

### 5. `acceptance-map`'s post-implementation handoff is mis-wired

- **Judgment:** investigate/edit (obligation-only).
- **Why it matters:** `acceptance-map` names `closeout-check` as the downstream verifier, but `closeout-check` never consumes the acceptance map — it's a done-gate + commit, not an acceptance-runner. The "checks become the thing you verify against" loop never closes; the natural consumer is `implementation-review`.
- **Evidence:** `skills/acceptance-map/SKILL.md:283`; `skills/closeout-check/SKILL.md` (no acceptance-map consumption); composability lens cross-checked against `tdd`/`execute-plan` (neither names acceptance-map as input).
- **Recommended action:** Point post-implementation verification at `implementation-review`; optionally have `closeout-check` surface "unverified acceptance map" as a remaining gap. Confirm the intended direction first.

### 6. `scrutinize-skill` companion is Codex-branded against a runtime-neutral skill

- **Judgment:** rewrite (description hygiene) — **CONFIRMED**; plugin publish path.
- **Why it matters:** `agents/openai.yaml` says "Adversarial review for Codex skills" / "review this skill as a Codex behavior contract" while `SKILL.md` is runtime-neutral and all four sibling companions are neutral. Unique defect across 21 companions; misroutes the job's scope.
- **Evidence:** `plugins/review-family/skills/scrutinize-skill/agents/openai.yaml:3-4` vs `SKILL.md:8`; neutral model at `.../scrutinize/agents/openai.yaml:4`.
- **Recommended action:** Re-author to "agent skill"/"behavior contract." Plugin-distributed → version bump past 0.3.7, `codex-plugins-sync.sh --publish review-family`, mirror; bundle with the next review-family change (don't ship a lone bump). Same publish path applies to the `review-reviewer` de-dup (Finding 8) — batch them.

### 7. `grill-me` dropped its load-bearing pacing clause

- **Judgment:** rewrite → **one clause** — **CONFIRMED** (the merge it was bundled with is REFUTED).
- **Why it matters:** `grill-me:8` reads "Ask the questions one at a time." but lost "...waiting for feedback on each question before continuing" — which its twin keeps. So it advertises one-at-a-time interrogation while permitting an agent to batch questions: a behavior defect against its own description.
- **Evidence:** `skills/grill-me/SKILL.md:8` vs `skills/grill-with-docs/SKILL.md:10`; `grill-me/SKILL.md:3`.
- **Recommended action:** Restore the clause verbatim. Optional one-line pointer to `grill-with-docs` for CONTEXT.md/ADR-backed plans (polish, not required — the discriminator already lives on `grill-with-docs:3`). **Do not merge** the pair: `improve-codebase-architecture:78,80` imports grill-with-docs's format files, and `triage:78` + `setup-matt-pocock-skills/domain.md:11,45` depend on grill-with-docs as "the producer skill."

### 8. `review-reviewer` encodes the same adjudication twice

- **Judgment:** rewrite → **narrowed to a de-dup pass** — **PARTIAL** (headline overstated).
- **Why it matters:** Real duplication and a proven drift hazard — the disposition list is near-verbatim at `:165-171` and `:247-254`, two full output templates exist, and commit `ca92f7c` had to fix only one of the two parallel buckets. **But** the two modes answer genuinely different questions (historical review-reliability vs current actionability) with non-isomorphic outputs, so a full collapse would destroy real distinctions.
- **Evidence:** `plugins/review-family/skills/review-reviewer/SKILL.md:165-171` vs `:247-254`; crosswalk at `:144-148` (labels explicitly *not* 1:1); `:115-117`, `:308-312`, `:323-331` (CCC-vs-full asymmetry).
- **Recommended action:** Factor out the **shared disposition list** into one referenced definition; keep both classification vocabularies and both output packets. Do **not** collapse to one mode-flagged packet. Plugin publish path; batch with Finding 6.

## Skill-By-Skill Editorial Table

Location key: **D** = `skills/` (dual-runtime), **C** = `skills-claude/` (Claude-only), **PH** = `plugins/handoff`, **PR** = `plugins/review-family`. Tier in brackets.

| Skill | Loc | Apparent job | Judgment | Main issue / strength | Best next action | Evidence |
|---|---|---|---|---|---|---|
| agent-facing-design | D | Context-vs-machinery design gate | keep [T1] | Keystone; global+4 siblings route through it | none (opt: trim proof restatement) | `SKILL.md:30-32,104-107` |
| baseline | D | Authority/source-of-truth resolver | keep [T1] | Distinct upstream job; 4 parallel vocabularies make it dense | keep; opt: compress trust-gap list | `baseline/SKILL.md:54-76,85-95` |
| behavior-smoke-test | D | Prove a changed behavior contract is followed | keep [T1] | Hardest-to-fake proof step; mild safety-list repetition | keep; opt: dedup mutation envelope | `behavior-smoke-test/SKILL.md:133-161` |
| closeout-check | D | "Is it done?" + final local commit | keep [T1] | Clean lifecycle terminal; triple-stated repair rule | keep | `closeout-check/SKILL.md:144-152,163-178` |
| design-exploration | D | Outcome→approved design | keep [T1] | At-quality; reciprocally fenced both sides | none | `design-exploration/SKILL.md:64-67` |
| diagnose | D | Disciplined hard-bug investigation | keep [T1] | Strong "repro-loop-first"; portable vs bundled `/debug` | opt: dual-name handoff token `:125` | `diagnose/SKILL.md:125` |
| execute-plan | D | Run a plan task-by-task w/ gates | keep [T1] | Tight executor; re-specs review inline | opt: name `implementation-review` for final pass | `execute-plan/SKILL.md:45-46,64-65` |
| gh-address-comments | D | Fix PR comments, stop at local commit | keep [T1] | Charter-admitted, smoke-tested; 5× no-publish restatement | keep | `gh-address-comments/SKILL.md:3` |
| **gh-pr-review-loop** | D | Publish half of PR loop | keep [T1] | **Publish-authorized but model-invocable** | **add explicit-only flags** | `gh-pr-review-loop/SKILL.md:1-4,3` |
| git-hygiene | D | Local git cleanup, lane-gated | keep [T1] | Sharpest safety discipline; `codex/` prefix hardcoded | opt: runtime-neutral branch prefix | `references/git-hygiene-reference.md:41` |
| implementation-planning | D | Settled design→executable plan | keep [T1] | Lean, well-bounded | none | `implementation-planning/SKILL.md:57-59` |
| making-recommendations | D | Compare-rank-recommend | keep-tighten [T2] | Great model; handoff rule restated 4×, dup'd into 2 files | collapse routing block; trim examples | `making-recommendations/SKILL.md:18-84` |
| merge-branch | D | Local fast-forward land, no PR | keep [T1] | Distinct sharp tool; minor repetition | keep | `merge-branch/SKILL.md` |
| next-steps | D | Findings→dependency-aware plan | keep [T1] | Strong anti-fabrication; checklist dup's body | opt: fold checklist; add reciprocal pointer | `next-steps/SKILL.md:56-58` |
| **to-prd** | D | Conversation→PRD, publish | keep-tighten [T2] | **Pipeline dead-end**; seam-check verb nit | **add forward handoff to to-issues** | `to-prd/SKILL.md:26-34` |
| to-issues | D | Plan→grabbable issues, publish | keep [T2] | Exemplary; complete | keep; opt: dual-name setup token | `to-issues/SKILL.md:3,67` |
| triage | D | Tracker triage state machine | keep [T2] | Well-fenced; value gated on Pocock ecosystem | keep | `triage/SKILL.md:78` |
| orient-status | D | Read-only status brief | keep-tighten [T2] | Strong engine; boundary text stated 4× (+dup's baseline's authority ladder) | collapse boundaries to one home | `orient-status/SKILL.md:109-124` |
| **acceptance-map** | D | Settled source→acceptance checks | keep-tighten [T2] | Well-built; **handoff mis-wired to closeout-check**; openai.yaml overclaims closeout | re-point to implementation-review; fix `openai.yaml:4` | `acceptance-map/SKILL.md:283` |
| outcome-interviewer | D | One-question outcome interview | keep-tighten [T2] | Real job; body ~2× needed, invariants restated | push depth into examples file | `outcome-interviewer/SKILL.md` (310 ln) |
| **grill-me** | D | One-question pressure test | keep-tighten [T2] | **Dropped the waiting clause**; thin | restore clause `:8` | `grill-me/SKILL.md:8` vs `grill-with-docs:10` |
| **grill-with-docs** | D | Grill + DDD glossary/ADR, writes repo | keep-tighten [T2] | **Ungoverned durable writes**; real producer node | add mutation-lifecycle clause | `grill-with-docs/SKILL.md:52,74` |
| **improve-codebase-architecture** | D | Architecture-deepening + HTML report | keep-tighten [T2] | **Ungoverned writes**; `DEEPENING.md` orphaned; glossary copied 3× | add mutation clause; add DEEPENING.md load cue | `.../SKILL.md:78,79`; DEEPENING.md unreferenced |
| simplify-code | D | Scoped behavior-preserving cleanup | keep-tighten [T2] | Strong scripts; SKILL.md duplicates the playbook it loads | trim to routing+load cue; add `/simplify` non-use | `simplify-code/SKILL.md:30-74` |
| tech-debt-scan | D | Evidence-led debt audit artifact | keep-tighten [T2] | Well-scoped; rules stated 2-4×; shares `docs/audits/` ns | dedup; let template own path rules | `tech-debt-scan/SKILL.md:14-16,23-30` |
| markdown-reformat | D | Structure-only Markdown cleanup | keep-tighten [T2] | Clean; body Use-When dup's frontmatter | drop body Use/Do-Not sections `:10-22` | `markdown-reformat/SKILL.md:10-22` |
| markdown-synthesis | D | Multi-source→one new Markdown doc | keep-tighten [T2] | Right job; ~2.5× sibling, dup'd scaffolding | collapse confidence-gate/quality-bar/final-response | `markdown-synthesis/SKILL.md` (175 ln) |
| prototype | D | Throwaway prototype to settle a question | keep-tighten [T2] | Real gap owned; rules restated across LOGIC/UI | dedup shared rules to SKILL.md | `prototype/SKILL.md:21-30` |
| skill-ux-design | D | Audit/improve a skill's UX journey | keep-tighten [T2] | **Worst overbuild**: 335 ln + 216-ln rubric ~70% dup's body | pick one home for phase list/rubric; collapse | `skill-ux-design/references/ux-rubric.md`; `SKILL.md:11` |
| writing-principles | D | Obligation-only edits of agent-facing docs | keep-tighten [T2] | Violates its own thesis; obligation frame stated 3-4× | run writing-principles on itself; collapse Scope+Edit Gate | `writing-principles/SKILL.md:28-65,67-144` |
| tdd | D | Test-first tracer-bullet slices | keep [T1] | Owns horizontal-slicing failure mode; refs earn place | keep (opt: move refs under references/) | `tdd/SKILL.md:16,53,54,100` |
| claude-code-docs | D | Claude Code docs Q&A via MCP | keep-tighten [T2] | Oversized body; namespace split is **deliberate, not a bug** | collapse retry ladder; verify Codex ns before any edit | `claude-code-docs/SKILL.md:44` |
| caveman | D | Persistent terse persona | keep [T3] | Honest small persona; brittle off-switch | opt: broaden disengage trigger | `caveman/SKILL.md:10,33-35` |
| zoom-out | D | Higher-level code map (explicit-only) | keep [T2] | Distinct cartography job; thin value over default | keep; opt: glossary-absent fallback | `zoom-out/SKILL.md:7` |
| **friction-to-guards** | C | Recurring feedback→durable guard | relocate? [T2] | Runtime-neutral but Claude-confined; **relocation REFUTED** | annotate ledger reason (don't relocate by default) | `friction-to-guards/SKILL.md:41,60` |
| setup-matt-pocock-skills | C | Scaffold repo agent-skills config | keep-tighten [T2] | Overstates consumer dependency; author-branded | de-brand; match real mechanism | `setup-matt-pocock-skills/domain.md`; `triage-labels.md:5` |
| skill-benchmark | C | Quantitative skill eval | keep [T1] | Clean; needs subagents+`claude -p` (justified Claude-only) | keep; watch real usage | `skill-benchmark/SKILL.md` |
| openai-docs | C | OpenAI docs Q&A via MCP | keep-tighten [T2] | ~30-40% longer than sibling; hardcoded "161 endpoints" | trim to claude-code-docs length; drop count `:67` | `openai-docs/SKILL.md:67` |
| exiting-worktrees | C | Gated worktree removal | keep-tighten [T2] | Correct; ~30% long, off-scope origin-sync step | shrink step 5; collapse Edge Cases table | `exiting-worktrees/SKILL.md:115-131` |
| save-handoff | PH | Write session handoff | keep [T1] | One of the cleanest in the roster | none | `save-handoff/SKILL.md:21` |
| load-handoff | PH | Load handoff, read-only | keep [T2] | Inlines a slice of throughline's source-set def | drop parenthetical `:65`; rest on `:78` | `load-handoff/SKILL.md:65,78` |
| search-handoffs | PH | Search handoffs (read-only) | keep [T1] | Well-bounded; unbound `$PROJECT_ROOT`, hard `rg` dep | bind var / note rg precondition | `search-handoffs/SKILL.md` |
| throughline | PH | Maintain derived project arc | keep [T2] | Distinct; ordering machinery justified | none | `throughline/SKILL.md:35,59-67` |
| implementation-review | PR | Code-vs-plan adversarial review | keep [T1] | One of the strongest skills; no real defect | keep | `implementation-review/SKILL.md:199` |
| **review-reviewer** | PR | Adjudicate a supplied review | keep-tighten [T2] | **Same adjudication twice**; correctly wired explicit-only | de-dup disposition list; keep both modes | `review-reviewer/SKILL.md:165-171,247-254` |
| scrutinize | PR | Generic adversarial artifact review | keep-tighten [T2] | Clean hub; modes restated 4× | collapse mode sections into reference | `scrutinize/SKILL.md:141` |
| **scrutinize-skill** | PR | Adversarial skill-contract review | keep-tighten [T2] | **Codex-branded companion** vs neutral skill | de-Codex `openai.yaml:3-4` | `scrutinize-skill/agents/openai.yaml:3-4` |
| system-design-review | PR | Architecture/system-design review | keep [T1] | Mature, clean body/reference split | opt: fix "6-10 lenses" wording; add manifest example | `system-design-review/SKILL.md:67` |

## Cross-Skill Patterns

- **House style trends verbose, and it's the dominant cost.** 13/48 bodies overbuilt; the recurring shape is restating the non-use boundary, stop conditions, and authority/proof rules in 3–4 places per skill (e.g., `orient-status` boundary ×4, `making-recommendations` handoff ×4 + both support files, `closeout-check` repair rule ×3, `review-reviewer` adjudication ×2). Descriptions are disciplined (median 48 words, 0 over 90); the bloat is entirely in bodies. A single, well-scoped `writing-principles` pass per overbuilt skill would reclaim the most surface for the least risk.
- **Routing is genuinely excellent.** Reciprocal, by-name, source-confirmed boundaries across all major clusters; zero dangling skill references; zero name collisions with Codex/Claude bundled names. The one asymmetry of note (`grill-me`→`grill-with-docs`) is optional polish.
- **Reference/example discipline is clean.** Every real referenced path exists; support files are almost all load-cued. The lone orphan is `improve-codebase-architecture/DEEPENING.md` (its deepest operational reference, never cued from SKILL.md).
- **Proof/lifecycle is consistent except one hole.** No skill invents installed-runtime proof for a `skills/` source (all such mentions are correct negatives); the `gh-address-comments` (local commit) vs `gh-pr-review-loop` (publish) authority split is the model case. The single exception is the durable-write hole (Finding 1).
- **Two authoring lineages coexist.** A defensive "house style" (baseline, closeout-check, review-reviewer, acceptance-map) and a terser, template-driven "Pocock-imported" family (to-prd, to-issues, triage, tdd, grill-*, zoom-out) orbiting `setup-matt-pocock-skills`. The imported family has been retrofitted with house-style proof boundaries (`to-prd:14-24`) but still leaks provenance (`triage-labels.md:5`) and an author-named invocation token.
- **The dual-runtime/plugin seam is the systemic blind spot.** The 5-skill review-family plugin is unreachable by name from the dual-runtime pipeline (Finding 3), and two runtime-neutral skills sit in `skills-claude/` without a recorded reason. Neither is a bug, but both are unmanaged seams where "it works because of availability fallbacks" masks intent.
- **Phase-1 single-skill review has a characteristic blind spot** worth noting for future runs: it over-flagged cosmetic issues it couldn't see the whole repo for (`.DS_Store` "committed," the namespace "bug") and under-weighted cross-skill coupling (it rated `acceptance-map` handoffs as clean; the composability lens caught the mis-wire). Cross-cutting lenses caught both — keep that two-layer split.

## Merge, Split, Archive, Rewrite

**Strong merge candidates:** *None.* The one structural overlap (`grill-me`/`grill-with-docs`) was adversarially **refuted** — grill-with-docs has live downstream consumers (`improve-codebase-architecture:78,80`, `triage:78`) and the two occupy deliberately-wired read-only vs repo-writing lanes.

**Strong split candidates:** *None.* No skill is doing two jobs that want separating. (`review-reviewer` holds two *modes*, but they're one coherent job; de-dup, don't split.)

**Strong archive candidates:** *None* — 0 Tier-4, 0 "not worth it." The only even-arguable trims, both of which should be **kept**: `caveman` (T3, harmless, self-contained, no competitor) and `zoom-out` (borderline thin value over a competent agent's default "explain this code," but it's a 7-line explicit-only canned prompt with a distinct describe-only contract — `zoom-out/SKILL.md:7`). Manufacturing cuts here would be the wrong move.

**Strong rewrite candidates (all tightening/additive, none destructive):**

- `grill-with-docs` + `improve-codebase-architecture` — add mutation-lifecycle clause (Finding 1). *Highest value.*
- `gh-pr-review-loop` — add explicit-only flags (Finding 2).
- `to-prd` — add forward handoff (Finding 4).
- `review-reviewer` — de-dup disposition list, keep both modes (Finding 8).
- `scrutinize-skill` — de-Codex companion (Finding 6).
- `grill-me` — restore pacing clause (Finding 7).
- Body-tightening backlog (lower urgency, high cumulative value): `skill-ux-design` (worst — 335 + 216-line dup'd rubric), `outcome-interviewer`, `markdown-synthesis`, `orient-status`, `making-recommendations`, `simplify-code`, `tech-debt-scan`, `openai-docs`, `scrutinize`, `claude-code-docs`, `writing-principles` (it violates its own thesis), `exiting-worktrees`, `markdown-reformat`.

**Keep mostly as-is (Tier 1, 19 skills):** agent-facing-design, baseline, behavior-smoke-test, closeout-check, design-exploration, diagnose, execute-plan, gh-address-comments, gh-pr-review-loop (after the flag fix), git-hygiene, implementation-planning, implementation-review, merge-branch, next-steps, save-handoff, search-handoffs, skill-benchmark, system-design-review, tdd.

## New Skill Opportunities

**One genuine candidate — and it's an extraction, not a new skill:**

- **Apply a *local or pasted* set of review findings (verify→classify→fix→stop).** *User need:* a user pastes a review (or has a local review doc) and wants the real findings fixed locally, without GitHub. *Why existing skills miss it:* `gh-address-comments` does exactly this but is GitHub-thread-bound; `review-reviewer`'s Current Claim Check adjudicates pasted claims but is read-only (stops at dispositions, doesn't fix) and explicit-only. The verify-classify-fix-stop discipline exists, fragmented across GitHub plumbing and read-only adjudication. *Shape:* extract the runtime/source-neutral core (five dispositions + evidence-pointer rule + evidence-backed pushback, no performative agreement) into one **dual-runtime** lane that `gh-address-comments` calls for the GitHub case — mirroring how `gh-pr-review-loop` already delegates its inner loop. *Gate:* run the charter friction search first (`docs/agents/contract-decisions.md` discipline); if no friction is observed, **park it with a reopen trigger**, don't admit. Evidence bounding the gap: `gh-address-comments/SKILL.md:3`, `review-reviewer/SKILL.md:109-117`.

**Explicitly *not* opportunities (deliberate non-coverage, correctly so):** a generic "implement this" lane (global CLAUDE.md makes acting-directly the default); a code-comprehension lane (parked with a live reopen trigger, `contract-decisions.md:253`); a scaffold/init lane (`init`/`update-config` bundled); a dual-runtime "run the real app and observe" lane (`run`/`verify` are Claude-bundled; this is a sanctioned runtime asymmetry, not a gap).

## Value-Added Ranking

**Tier 1 — clearly high-value (19):** agent-facing-design, baseline, behavior-smoke-test, closeout-check, design-exploration, diagnose, execute-plan, gh-address-comments, gh-pr-review-loop, git-hygiene, implementation-planning, implementation-review, merge-branch, next-steps, save-handoff, search-handoffs, skill-benchmark, system-design-review, tdd. *Rationale:* each owns a distinct, reciprocally-fenced job with strong bodies and clean proof discipline; review agents found no real defect beyond optional micro-tightening. (`implementation-review` and `behavior-smoke-test` are standouts — the library's hardest-to-fake proof steps.)

**Tier 2 — useful, needs tightening (28):** the remaining `skills/` + `skills-claude/` + plugin skills. *Rationale:* the job is real and the routing is clean, but the body is overbuilt or carries a concrete defect (mutation hole, mis-wired handoff, dead-end, Codex-branding, dropped clause, provenance cruft). All are keepers; all want a `writing-principles`/connective pass.

**Tier 3 — marginal/situational (1):** `caveman` — honest, harmless, no competitor, but a stylistic persona with the thinnest functional value in the roster (`caveman/SKILL.md:10`).

**Tier 4 — archive/replace (0):** none. Stated plainly because the prompt anticipated this tier: after exhaustive review, nothing in this library has earned removal.

## Highest-Value Follow-Ups

Smallest set, highest leverage, cuts/connective-fixes before machinery:

1. **Patch the durable-write hole** in `grill-with-docs` + `improve-codebase-architecture` (Finding 1) — the one real substantive gap; ~2–4 sentences each via `writing-principles` + `agent-facing-design`.
2. **Add the explicit-only flags to `gh-pr-review-loop`** (Finding 2) — closes a real publish-authority misroute; two-flag additive change; verify with a behavior-smoke-test.
3. **Three one-line connective edits:** `to-prd`→`to-issues` handoff (Finding 4); `acceptance-map`→`implementation-review` (Finding 5); name `implementation-review` (availability-conditional) in `execute-plan`+`closeout-check` (Finding 3).
4. **Restore `grill-me:8`'s pacing clause** (Finding 7) — one clause, fixes a behavior-vs-description defect.
5. **Batch the two review-family edits** — `scrutinize-skill` de-Codex + `review-reviewer` disposition-list de-dup — into one version bump + Codex republish + mirror (Findings 6, 8).
6. **Add `improve-codebase-architecture/DEEPENING.md` a load cue** (or delete it) — resolve the one orphan support file.
7. **Run the body-tightening backlog** as routine `writing-principles` passes, starting with `skill-ux-design` (the worst offender). Not urgent; high cumulative payoff against Codex's ~2% routing budget and per-invocation cost.
8. **Make two deliberate decisions** (don't patch reflexively): `friction-to-guards`/`setup-matt-pocock-skills` placement (annotate the ledger or relocate via the charter), and whether to fence the bundled twins (`simplify-code`/`diagnose`/`tech-debt-scan` vs `/simplify`,`/debug`,`/code-review`) or record a no-fence decision.

Optional housekeeping: the 18 on-disk `.DS_Store` files are untracked and already gitignored OS noise — **no cleanup commit needed**.
