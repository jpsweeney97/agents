---
type: roadmap
created: 2026-07-08
status: recommendations only — nothing landed; each action still needs the owning-skill edit, the Validation Ladder, and (for third-party folds/admits) a contract-decisions.md ledger entry at landing
scope: evaluate every skill in mattpocock/skills (checkout d574778) for extraction into JP's first-party library; produce a tiered, evidence-backed action list
source: commissioned this session; supersedes nothing — extends the 2026-07-05 mattpocock disposition (ledger 34ea88a) to the ~21 skills that disposition never saw and to the source's drift since
method: 38-skill fan-out evaluation + adversarial verification of every library-changing verdict + a non-skill/meta content scan + a completeness critic (workflow wf_0b65f407-fae); the ADMIT, the failed-verify Negation fold, and the top tdd fold were additionally re-confirmed by hand
---

# mattpocock/skills — extraction roadmap

## Context

This roadmap evaluates all **38 skills** in `mattpocock/skills` (local checkout `/Users/jp/scratch-workspace/mattpocock-skills`, upstream HEAD `d574778`) against JP's live skill inventory, plus a scan of the repo's non-skill material — authoring conventions in `.agents/`, the `.out-of-scope/` rationale docs, cross-cutting reference files, and `CONTEXT.md`/`CLAUDE.md`.

The framing that governs everything below: this is the **same upstream** that was dispositioned on **2026-07-05** (ledger entry `34ea88a`), but that disposition only saw the 11 *new* third-party skills a reinstaller had dropped into `skills/` — it restored 8 clobbered forks, admitted `teach`, folded `diagnosing-bugs`'s repro-minimise step into `diagnose`, and rejected 9 collisions. **Roughly 21 of the 38 skills here were never evaluated at all** (the four `deprecated/` skills, the entire `in-progress/`, `misc/`, and `personal/` buckets, plus `resolving-merge-conflicts`, `wayfinder`, and productivity `handoff`), and **several "settled" skills drifted upstream** since 07-05 — most materially the unified planning skills (`to-prd`→`to-spec`, `to-plan`+`to-issues`→`to-tickets` with a new wide-refactor discipline), the graduated `wayfinder`, the reference-only `tdd`, `triage`'s external-PR extension, and `code-review`'s new Fowler smell baseline.

Every "already owned" and "genuinely absent" verdict was checked by **reading the first-party target file**, not inferred from a roster line, and every recommendation that would change the library got an **adversarial verify pass** whose job was to refute the claimed gap. One verify agent (for the `writing-great-skills` Negation fold) died on a connection drop; I re-confirmed that item — and the sole whole-skill admit, and the top fold — **by hand** (greps recorded in the session), so nothing load-bearing here rests on an unverified agent report.

## How to read this

The merit lens is **One-Owner + cognitive-offload**. A skill earns action only if its job is genuinely ownerless in JP's library (no first-party or bundled skill already does it), **or** it carries a separable, additive discipline an owned skill lacks. "I could just do that myself" is never a reason to reject — it measures the agent, not the human's freed attention.

Four dispositions: **admit** (build the ownerless skill, house-adapted), **fold** (extract one separable discipline into an already-owned skill — do *not* adopt the donor), **reject** (collision, house hazard, or worthless-to-build), **park** (ownerless but low-value-now — record, don't build).

**Hard rule:** settled 07-05 rejections are **not** re-litigated unless the source materially drifted. Where a skill drifted, the drift is stated and shown either to strengthen the existing verdict or to surface a new fold — never to silently reopen a closed collision.

### The charter dimension (stated once, applied per action)

Adopting or folding third-party material is a **charter case-(d) event** — "deciding the fate of third-party material" — so **landing** any admit or fold below warrants a `docs/agents/contract-decisions.md` ledger entry, exactly as the 07-05 fold of `diagnosing-bugs`→`diagnose` was ledgered at `34ea88a`. The size of the entry scales with the material (a whole-skill admit is a full entry; a one-line fold is a one-line note), but the decision gets recorded.

The one borderline: folding a *newly-evolved* upstream discipline into a fork whose third-party adoption was **already ledgered** on 07-05 (`tdd`, `triage`). A defensible reading is that the material's fate was already decided and these are now ordinary build-and-prune edits to a first-party skill; the conservative reading is that new donor text is new material and gets a one-line ledger note. This roadmap flags those two as the borderline and leaves the call to landing time — it does not assert an exemption. Every other fold below lands third-party text into a skill whose lineage was **not** previously adopted (`diagnose` received a fold but was never itself a third-party adoption; `to-prd`/`to-issues`/`save-handoff`/`writing-principles` are first-party), so each is unambiguously case (d).

No action below trips the *other* charter triggers — none installs an always-loaded contract, fires unattended, or wields an irreversible-effect tool — with one explicit exception called out in Tier 3 (`git-guardrails-claude-code`, which is why it is rejected).

---

## Tier 1 — recommended actions (survived adversarial verification)

Ordered by value. Each names the exact donor passage, the exact target file, the evidence of absence, and the charter class.

### 1 — FOLD: tautological-test anti-pattern → `tdd` · HIGH confidence

- **Action:** add the tautological-test anti-pattern to first-party `tdd/tests.md`, with a one-line peer bullet in `tdd/SKILL.md`.
- **Donor:** `skills/engineering/tdd/tests.md` (the `calculateTotal` BAD/GOOD pair, ll. 63-77) + `SKILL.md` l. 29 — a test whose assertion recomputes the expected value the same way the code does (e.g. via the same `reduce`) passes *by construction* and gives zero confidence, distinct from the implementation-coupling anti-pattern already covered.
- **Target:** `/Users/jp/.agents/skills/tdd/tests.md`.
- **Evidence:** verified absent — a recursive grep across the whole first-party `tdd/` dir for `tautolog|by construction|recompute|independent source|source of truth` returns nothing (re-run by hand this session: zero hits). First-party bad-test coverage is entirely implementation-coupling; a by-construction-passing test is an orthogonal, uncovered failure mode. The other two `tdd` drift candidates (the **seam** vocabulary; mockability/DI) were checked and are already owned — "seam" is a rename of first-party's confirm-which-behaviors + public-interface-only rules, and first-party `mocking.md` is a strict superset of the donor's.
- **Charter:** borderline build-and-prune — a fold into the already-ledgered `tdd` fork; a one-line ledger note at landing is the conservative choice.

### 2 — ADMIT: `resolving-merge-conflicts` → new `git-cycle` sibling · MEDIUM confidence

This is the **only whole-skill admit** in the batch. I re-confirmed its ownerlessness by hand.

- **Action:** build a house-adapted git-conflict-resolution skill as a `git-cycle` sibling — inspect the in-progress merge/rebase state, trace each conflict side to its original intent (commits / PRs / tickets), resolve each hunk preserving both intents without inventing behavior, run the project's checks, then finish and commit the merge/rebase.
- **Donor:** `skills/engineering/resolving-merge-conflicts/SKILL.md` (five-step procedure).
- **Target:** ownerless — confirmed by grepping every first-party skill this session. The only "conflict" hits are unrelated (authority conflicts in `writing-principles`, unresolved-source conflicts in `markdown-synthesis`, conflict-marker lint scans). The three nearest git-cycle siblings each **explicitly decline the job**: `exiting-worktrees` says literally "never resolve merge conflicts inside the worktree" (l. 222), `gh-address-comments` hands off (l. 73-83), `merge-branch` is fast-forward-only and stops on any non-ff/conflict. `git-hygiene`'s preflight aborts on any in-progress merge/rebase; `keep-green` drives a just-made change back to green on *test/lint* signals, not conflicts. This is the textbook ownerless-with-demand pattern.
- **Evidence of merit:** the two disciplines agents most reliably skip — *trace-each-side-to-intent* (step 2) and *re-run-the-project's-checks-after-resolving* (step 4) — are the real cognitive-offload win; merge/rebase conflicts are high-frequency and high-stakes.
- **Charter:** case (d) — third-party adoption; full ledger entry at landing. User-invoked (not unattended); commit/rebase are reflog-reversible (not the irreversible-tool trigger).
- **House-fit conditions (not a verbatim copy):** soften the donor's absolute "always resolve; never `--abort`" — abort is sometimes correct; add the house layer the donor lacks (Use-when / Do-not-use boundary, dual-runtime tokens, protected-branch awareness, `trash`-not-`rm`). Name collides with no bundled skill.

### 3 — FOLD: Phase-1 red-capable completion gate → `diagnose` · verify-CORRECTED to fold

The per-skill eval said reaffirm-settled; the adversarial verify **modified it to fold** — a live, un-folded discipline remains, and reaffirm-settled would wrongly signal nothing-to-do.

- **Action:** add a checkable Phase-1 completion gate to `diagnose`.
- **Donor:** `skills/engineering/diagnosing-bugs/SKILL.md` ll. 51-60 — the "a tight loop that goes red" completion criterion: name one command you have *already run at least once* and paste the invocation + its output, a 4-item checklist (red-capable / deterministic / fast / agent-runnable), and an anti-anchoring stop ("no red-capable command, no Phase 2").
- **Target:** `/Users/jp/.agents/skills/diagnose/SKILL.md`.
- **Evidence:** `diagnose` is the fork of this donor (identical 6-phase spine) and is strictly richer on Phases 1/4/5/6 — but its Phase 1 ends only at a soft line ("Do not proceed to Phase 2 until you have a loop you believe in"), with no checkable gate, no run-once/paste-output evidence discipline, no operationalized anti-anchoring stop. The 07-05 fold took only the Phase-2 *minimise* step (confirmed present at `diagnose` ll. 77-85), so this Phase-1 gate is genuinely un-folded. The `hitl-loop.template.sh` the gate references already exists in the `diagnose` bundle, so the fold dangles nothing.
- **Charter:** case (d) — incremental third-party fold into a skill that was never itself a third-party adoption; ledger note at landing.

### 4 — FOLD ×2: external-PR triage + redundancy check → `triage` · reaffirm-keep whole-skill, two live folds

The whole skill stays a reaffirmed collision (keep the house fork, don't admit the donor), but the source drifted forward with two separable additions.

- **Donor → target:** `skills/engineering/triage/{SKILL.md,AGENT-BRIEF.md,OUT-OF-SCOPE.md}` → `/Users/jp/.agents/skills/triage/*`.
- **(a) External PRs as a triage surface** — "a PR is an issue with attached code" (SKILL.md l. 11): the same state machine with PR deltas, discovery tagging `[PR]`/`[issue]` behind an external-author filter (discovery-only; a named PR is always triaged), step-3 verification generalized to "confirm the diff does what it claims" via checkout + tests, and a PR-shaped agent brief (AGENT-BRIEF.md ll. 148-183).
- **(b) Step-1 redundancy search + "already-implemented" wontfix branch** — search the codebase by domain concept for an existing implementation, with a wontfix branch distinct from "rejected" that points to where the feature lives and must **not** write to `.out-of-scope/` (recording a *built* feature would poison the dedup checks with false rejections; OUT-OF-SCOPE.md l. 88).
- **Evidence:** verified absent from the fork (issue-only throughout; the fork's step 1 does only the prior-rejection check). Verified non-colliding: `gh-address-comments` is the PR *author* answering review threads with no publish authority; `implementation-review` is strictly read-only and opens no issues — neither triages an inbound external PR into tracker states.
- **Charter:** borderline build-and-prune — folds into the already-ledgered `triage` fork; landing call as in the charter note above.
- **Lander caveats:** extend the fork's "do not mutate until the maintainer approves" gate to explicitly cover PR labels/comments/closes; scrub the `/setup-matt-pocock-skills` external-author-config assumptions into the fork's graceful-fallback style; keep the fork's `trash`-not-`rm` over the donor's bare "Delete the file."

### 5 — FOLD: redact secrets/PII before writing a handoff → `handoff:save-handoff` · MEDIUM confidence

The productivity `handoff` skill is a whole-skill collision with the mature first-party handoff plugin (do **not** admit), but it carries one separable safety discipline the plugin lacks.

- **Donor:** `skills/productivity/handoff/SKILL.md` l. 14 — redact API keys, passwords, PII *before* the handoff is written to disk.
- **Target:** `/Users/jp/.agents/plugins/handoff/references/handoff-format.md` (consumed by `save-handoff`).
- **Evidence:** verified absent — `grep -rniE 'redact|secret|sensitive|PII|password|credential|scrub'` across the whole plugin returns zero hits; `PRIVACY.md` covers telemetry/storage policy only, not agent-facing scrubbing. `save-handoff` writes to `<project_root>/.agents/handoffs/`, which host policy "may track or ignore," so a handoff can capture pasted tokens/env and be committed — a real, low-cost gap. A one-sentence reminder fits the format's deliberate anti-schema minimalism ("headings are prompts, not a schema"). The donor's other two disciplines were declined: "suggested skills" fights that minimalism and overlaps `work-router` (and `load-handoff` already emits "Recommended next move"); reference-by-path is already present via the `## References` prompt + `save-handoff`'s delta-not-restatement rule.
- **Charter:** case (d) — ledger note at landing. **Plugin-distributed:** this fold must follow the Plugin Layout publish path (version bump + `codex-plugins-sync.sh --publish` + mirror), **not** the local-skill flow.

### 6 — FOLD: test-seam-count minimization → `to-prd` · HIGH confidence, modest value

`to-spec` is the upstream rename of the skill JP already forked as `to-prd` (git-confirmed lineage) — a whole-skill collision; do **not** admit (adopting it would *regress* `to-prd`, which has a pre-publish consent gate, a Side Effects / Proof Boundary, and the corrected `needs-triage` label that `to-spec` lacks, and re-carries the `ready-for-agent`/skip-triage hazard the fork deliberately reverted).

- **Donor:** `skills/engineering/to-spec/SKILL.md` l. 15 — "The fewer seams across the codebase, the better — the ideal number is one."
- **Target:** `/Users/jp/.agents/skills/to-prd/SKILL.md` (step 2, which currently stops at "propose them at the highest point you can").
- **Evidence:** verified additive, not a reword — `to-prd` encodes prefer-existing and prefer-high-placement but no cap on aggregate seam *count*. Verified never-captured rather than trimmed: the first-party import predates the upstream commit that added the line, and `git log -S "ideal number is one"` first-party is empty. Verified ownerless: the only spec/PRD test-seam text is in `to-prd` itself (`improve-codebase-architecture` owns seams in the distinct module/adapter sense).
- **Charter:** case (d) — ledger note at landing.

### 7 — FOLD: wide-refactor recognize-and-route seam → `to-issues` · MEDIUM confidence

`to-tickets` (the upstream merge of `to-plan`+`to-issues`) is a whole-skill collision with the restored `to-issues` fork; do **not** admit. Fold only the recognition seam, **not** the expand-contract machinery.

- **Action:** add a one-line wide-refactor exception to `to-issues` that recognizes a rename-the-world change and routes to `migration-campaign` / `contract-change-propagation`.
- **Donor:** `skills/engineering/to-tickets/SKILL.md` ll. 39-40 — a rename/retype whose blast radius breaks thousands of call-sites can't land green as a vertical slice; sequence expand-contract instead.
- **Target:** `/Users/jp/.agents/skills/to-issues/SKILL.md` (the vertical-slice rules, currently absolutist with no escape hatch).
- **Evidence:** the expand-contract *machinery* is already fully first-party-owned — `migration-campaign` (horizontal sharding + compat layer), `contract-change-propagation` (additive-first → migrate → deprecate → remove), `migration-safety` (expand / dual-write / backfill / switch / contract-last). Folding the machinery would violate One-Owner. What `to-issues` genuinely lacks is only the **recognize-and-route seam**: its slice rules give no escape hatch and no cross-reference to the sharding lanes, even though `migration-campaign` already draws the reciprocal edge *to* `to-issues`. A pure reject would leave `to-issues` actively wrong — mis-slicing a rename-the-world item into tickets that can never land green.
- **Charter:** case (d) — ledger note at landing.
- **Confidence caveat:** medium — a reasonable evaluator could call this reject-with-a-routing-note given how much substance is already owned. The local-file `tickets.md` publishing mode was correctly excluded as un-adopted `/setup-matt-pocock-skills` infra.

---

## Tier 2 — worth considering / park

### FOLD candidate (needs careful wording): Negation / positive-prompting → `writing-principles` · MEDIUM-HIGH

Surfaced by **both** the `writing-great-skills` per-skill verdict and the meta scan. `writing-great-skills` itself is correctly reaffirmed-rejected (Tier 3), but its evolved source added one separable Steering failure-mode the rejection should not swallow. Its adversarial verify was the one agent that died on a connection drop, so I **re-confirmed the absence by hand this session.**

- **Donor:** `skills/productivity/writing-great-skills/GLOSSARY.md` ll. 161-165 (`Negation`) — steering by prohibition drags the forbidden behavior *into* context ("don't think of an elephant"); the cure is to prompt the positive, keeping a prohibition only as a hard guardrail you cannot phrase positively, paired with its positive target.
- **Target:** `/Users/jp/.agents/skills/writing-principles/SKILL.md`, as a 9th Challenge-Order lens.
- **Evidence (re-confirmed by hand):** `writing-principles`' Challenge Order has **exactly 8 lenses** (Unjustified, Vague, Unclear, Overbuilt, Unbounded, False-proof, Conflicting, Duplicated) — none about prohibition-vs-positive phrasing; a whole-tree grep for `negation|prohibition|positive|elephant|forbidden` finds the discipline nowhere first-party. `agent-facing-design` (a gate) and `skill-ux-design` (a UX lens) are the wrong lane.
- **Why Tier 2, not Tier 1:** it is partly well-worn prompt lore whose no-op status against a capable editor is debatable, and it sits in tension with JP's *deliberate* house use of "Do not use for..." non-use boundaries in descriptions — so any fold must be worded as a lens that **exempts** non-use routing boundaries, matching the donor's own guardrail carve-out. Left for JP's judgment.
- **Charter:** case (d) — `writing-principles` is a first-party JP skill, not an adopted fork, so folding this donor concept is a fate-of-third-party-material decision; ledger note at landing.

### PARK — ownerless but low-value-to-build-now

- **`wayfinder`** (engineering, mattpocock-mature) — genuinely ownerless (multi-session, tracker-backed fog-of-war investigation planning; no incumbent sits at that altitude — `outcome-shaping`/`design-exploration` are single-session and read-only, `implementation-planning`/`to-issues` need a settled input). High offload merit (the fog-of-war frontier model, plan-don't-do, one-ticket-per-session). **But welded to un-adopted mattpocock infra:** its physical mechanism delegates to a `/setup-matt-pocock-skills` "Wayfinding operations" tracker-doc section that does not exist here (grep-confirmed absent, including the kept `skills-claude` copy), and it invokes the rejected `/domain-modeling` and `/grilling`. Adopting means authoring the missing mechanism *and* rewiring references, and the gem (fog-of-war frontier) is not cleanly graftable — it contradicts `implementation-planning`'s completeness-first Outside-View Pass. **The single most interesting candidate to revisit** if JP ever wants a cross-session investigation-map lane; would be a `skill-squad`-class build, not a fold. Charter case (d) if ever adopted.
- **`wizard`** (in-progress) — ownerless (no incumbent generates executable interactive setup scripts; `runbook-authoring` produces a durable doc and never runs the operation). Real offload concentrated in a `template.sh` (cross-platform open order, idempotent `.env` upsert, hidden secret entry, `gh` fallback recording) that a bare agent gets subtly wrong. Parked because mattpocock's own `in-progress/README.md` calls these "abandoned experiments," and the value is niche (web-app CI onboarding). No house hazard (`mktemp`/`mv`, no `rm`). Revisit if JP repeatedly hand-rolls third-party-setup scripts.
- **`writing-shape` / `writing-beats` / `writing-fragments`** (in-progress) — a coherent-but-experimental 3-skill long-form-article-composition pipeline (fragments = explore/mine; shape + beats = structure). Genuinely ownerless (`email-writing` excludes non-email long-form; `markdown-synthesis` is a one-pass multi-source merge; `markdown-reformat` preserves wording; `teach` is discrete HTML pedagogy). Parked because the whole suite is author-flagged in-progress, `shape` and `beats` are two *unsettled variants of the same exploit job* (admitting one means picking between unfinished designs; admitting both is a fresh One-Owner collision), and there is no demonstrated JP demand for an agent-driven article lane. The strongest discipline (the *grounding invariant* — track a running set of grounded concepts, never lean on an ungrounded one) is homeless and travels only with the whole parked capability.
- **`edit-article`** (personal) — ownerless single-article prose editing (`markdown-reformat` bars rewriting; `markdown-synthesis` is multi-source; `writing-principles` is agent-facing docs; `email-writing` is email). Parked because the donor is a thin 2-step sketch with no proof discipline, its one concrete rule (240 chars/paragraph) is mattpocock blog house-style that *conflicts* with JP's one-logical-line convention, and there is no signal JP does recurring general-article editing.

### PARK (marginal, from the meta scan): Fowler 12-smell shared reference

The fuller named-smell catalogue with fix-directions (`code-review/SKILL.md` ll. 43-56) is only *partially* present first-party (`tdd/refactoring.md` has a 5-item list; `simplify-code` uses a value-order, not a named taxonomy). Marginal — each target skill (`simplify-code`, `tech-debt-scan`, `improve-codebase-architecture`) already reaches the same smells through its own lens, and `improve-codebase-architecture`'s "Rejected framings" deliberately refuses competing vocabulary. Not worth a shared reference now.

---

## Tier 3 — reject / reaffirm-settled (coverage proof — every one listed)

### New rejects (never-evaluated this pass)

- **`design-an-interface`** (deprecated) — reject. Superset already owned by `improve-codebase-architecture/INTERFACE-DESIGN.md` (near-verbatim + richer: same Ousterhout "Design It Twice", same parallel sub-agents, plus invariants / error-modes / depth-locality-seam axes the donor lacks). Author-deprecated ancestor of already-extracted content.
- **`qa`** (deprecated) — reject. Issue creation owned by `triage`; dependency-ordered slicing owned by `to-issues`; plus a house **hazard** (l. 49 "Do NOT ask the user to review first — just file" is fire-and-forget tracker mutation both incumbents forbid) and it omits `triage`'s mandatory AI-disclaimer.
- **`request-refactor-plan`** (deprecated) — reject. Chain fully owned (interview → `outcome-shaping`/`design-exploration`; tiny-commits → `implementation-planning`/`to-issues`; publish → `to-prd`/`to-issues`); its durability line + Testing-Decisions block are verbatim in `to-prd`; and it is a *weaker* variant (files with no publish-approval gate).
- **`ubiquitous-language`** (deprecated) — reject. Rules near-verbatim identical to `grill-with-docs/CONTEXT-FORMAT.md`; author-deprecated ancestor of `domain-modeling` (itself rejected 07-05). The one absent element (an example dialogue) violates the incumbent's "CONTEXT.md is a glossary and nothing else" constraint.
- **`claude-handoff`** (in-progress) — reject. Its frame/product differs from the handoff plugin (launches a `claude --bg` autonomous agent vs writing a durable resume note), so the live-dispatch job is ownerless — but thin/carriable, in-progress, Claude-CLI-only (can't live in dual-runtime `skills/`), and **charter-hazardous (unattended** — spawns an editing agent in the CWD with no protected-branch guard, confirmation gate, or stop condition). Un-adopted paradigm vs JP's file-based `/save`/`/load`.
- **`loop-me`** (in-progress) — reject. Structurally depends on the rejected `/grilling` primitive (can't run as shipped), is infra for mattpocock's un-adopted `workflows/*.md` automation product, and collides in frame with `grill-me` + `design-exploration`; its definition-of-done is already owned by `implementation-planning`.
- **`git-guardrails-claude-code`** (misc) — reject. Triple collision (install mechanics → bundled `update-config`; escalate-to-hook judgment → `friction-to-guards`; git-safety policy → the live `require-gitflow.py` hook + AGENTS.md protected-branch floor + git-cycle) + house **hazard** (a blanket `git push` grep-block breaks git-cycle's authorized-push workflow) + **charter (always-loaded, unattended-firing hook, third-party contract material)**. No offsetting novelty.
- **`migrate-to-shoehorn`** (misc) — reject. Hyper-narrow single-vendor recipe (the `@total-typescript/shoehorn` README as a skill); zero offload, zero leverage (grep found no `shoehorn` anywhere in JP's world); mechanical-migration workflow far more richly owned by `migration-campaign`.
- **`scaffold-exercises`** (misc) — reject. Welded to Matt Pocock's proprietary `ai-hero-cli` toolchain (absent from every JP repo, grep-confirmed); both merit sources zero. Same class as the 07-05 `setup-matt-pocock-skills` rejection.
- **`setup-pre-commit`** (misc) — reject. Ownerless-but-unneeded fixed JS/TS tooling recipe (Husky/lint-staged/Prettier); JP's house stack is Python/uv/ruff with no JS toolchain; bakes in mattpocock's Prettier opinions; mild house hazard (stage-all + hardcoded commit, no branch-floor check). Park only if JP ever standardizes on JS.
- **`obsidian-vault`** (personal) — reject. Whole job already owned in JP's runtime by the installed `obsidian:obsidian-cli` + `obsidian:obsidian-markdown` plugin skills, which are strictly richer; the donor hardcodes a personal WSL vault path and drives raw `find`/`grep` instead of the CLI.

### Reaffirm-settled — reject (07-05 rejections, verified still holding)

- **`ask-matt`** — reaffirmed. Static hand-encoded atlas of mattpocock's *own* (partly rejected/nonexistent) topology; collides with `work-router`, which routes dynamically over JP's live roster. Drift = more mattpocock-topology, strengthens reject.
- **`code-review`** — reaffirmed. AGENTS.md-forbidden `skills/`-tier name (bundled `/code-review` is live) + job owned by `implementation-review`/`tech-debt-scan`/`improve-codebase-architecture`. Drift = a new Fowler smell baseline on one axis; fold hunt empty (owned or commodity).
- **`codebase-design`** — reaffirmed. Every section owned near-verbatim by `improve-codebase-architecture` (LANGUAGE/DEEPENING/INTERFACE-DESIGN) + `tdd`; incumbents equal-or-richer. Would add a third copy of single-sourced vocabulary.
- **`domain-modeling`** — reaffirmed. `grill-with-docs` is a strict superset (byte-identical CONTEXT-FORMAT.md, superset ADR-FORMAT.md); `decision-record` owns standalone ADR capture. No drift.
- **`implement`** — reaffirmed. Thin orchestrator whose every step is owned (`execute-plan`/`implementation-planning`/`tdd`/review-family/`closeout-check`) + house **hazard** ("Commit your work to the current branch" defies the protected-branch floor). Drift = cosmetic PRD→spec rename only.
- **`research`** — reaffirmed. Job splits cleanly across bundled `deep-research` (search + adversarial-verify) and first-party `research-capture` (durable per-claim-sourced doc). No drift.
- **`setup-matt-pocock-skills`** — reaffirmed and **hardened**. Self-collision with JP's divergent `skills-claude` fork; upstream drifted *further* from JP's library (references `to-tickets`/`to-spec`/`qa`/`wayfinder` that don't exist here; added "Wayfinding operations" infra for the absent `/wayfinder`). The one genuinely-new discipline (external-PRs-as-triage-surface) is routed to the Tier-1 `triage` fold instead.
- **`grilling`** — reaffirmed. Direct ancestor of the `grill-me` fork (core paragraph verbatim in `grill-me`); the two new lines (confirmation-gate, facts-vs-decisions split) are already covered (`grill-me` never enacts, so the gate is moot; fact-lookup + decisions-are-the-human's are present).
- **`writing-great-skills`** — reaffirmed. Skill-authoring domain-model owned by `agent-facing-design` + `writing-principles` + `skill-ux-design`. Drift = one new Steering failure-mode (Negation), surfaced as the Tier-2 fold candidate. (The prior note's expected "Negative Space" term is **not** in this checkout — grep-confirmed zero real hits.)

### Reaffirm-settled — keep first-party fork (restored/admitted, verified fork ≥ source)

- **`grill-with-docs`** — reaffirmed. Source collapsed to a 2-line delegation stub; the fork is a strict content superset (facts-vs-decisions carried stronger; ADR-FORMAT.md adds "Revisit when"; CONTEXT-FORMAT.md byte-identical).
- **`improve-codebase-architecture`** — reaffirmed. Donor is a *thinner* version delegating to the rejected `/codebase-design`, `/grilling`, `/domain-modeling`; the fork absorbed all of it inline + the house layer. Strict superset.
- **`prototype`** — reaffirmed. Fork is a strict superset (`diff`-confirmed): adds the house layer + an AFK non-interactive scenario-driver discipline the source lacks.
- **`grill-me`** — reaffirmed. Source is now a thin `/grilling` delegator; the fork adds the ask-what-to-grill opening, weakest-assumption + questions-stop-changing stop conditions, and named handoffs. Both new source disciplines already present.
- **`teach`** — reaffirmed. Full diff shows the SKILL.md body and all four companion format files are **byte-identical** to the first-party admitted copy; the only delta is the house description line. Zero new foldable discipline; no new charter event (already ledgered).

---

## Coverage table (all 38)

| # | Skill | Category | Prior status | Verdict | One-owner / target |
|---|-------|----------|--------------|---------|--------------------|
| 1 | design-an-interface | deprecated | never-evaluated | reject | improve-codebase-architecture/INTERFACE-DESIGN.md |
| 2 | qa | deprecated | never-evaluated | reject | triage + to-issues (+ hazard) |
| 3 | request-refactor-plan | deprecated | never-evaluated | reject | to-prd + implementation-planning + to-issues |
| 4 | ubiquitous-language | deprecated | never-evaluated | reject | grill-with-docs/CONTEXT-FORMAT.md |
| 5 | ask-matt | engineering | settled-rejected | reaffirm-reject | work-router |
| 6 | code-review | engineering | settled-rejected | reaffirm-reject | review-family + bundled /code-review (name) |
| 7 | codebase-design | engineering | settled-rejected | reaffirm-reject | improve-codebase-architecture + tdd |
| 8 | diagnosing-bugs | engineering | settled-folded | **FOLD** (verify-modified) | diagnose (Phase-1 completion gate) |
| 9 | domain-modeling | engineering | settled-rejected | reaffirm-reject | grill-with-docs + decision-record |
| 10 | grill-with-docs | engineering | settled-restored | reaffirm-keep | first-party grill-with-docs |
| 11 | implement | engineering | settled-rejected | reaffirm-reject | execute-plan cluster (+ house hazard) |
| 12 | improve-codebase-architecture | engineering | settled-restored | reaffirm-keep | first-party ICA |
| 13 | prototype | engineering | settled-restored | reaffirm-keep | first-party prototype |
| 14 | research | engineering | settled-rejected | reaffirm-reject | deep-research + research-capture |
| 15 | resolving-merge-conflicts | engineering | never-evaluated | **ADMIT** | ownerless → new git-cycle sibling |
| 16 | setup-matt-pocock-skills | engineering | settled-rejected | reaffirm-reject | skills-claude fork (self-collision) |
| 17 | tdd | engineering | settled-restored | reaffirm-keep + **FOLD** | tdd (tautological-test) |
| 18 | to-spec | engineering | never-eval-evolved | **FOLD** | to-prd (seam-count minimization) |
| 19 | to-tickets | engineering | never-eval-evolved | **FOLD** | to-issues (wide-refactor route) |
| 20 | triage | engineering | settled-restored | reaffirm-keep + **FOLD ×2** | triage (external-PR + redundancy) |
| 21 | wayfinder | engineering | never-evaluated | PARK | ownerless (welded to un-adopted infra) |
| 22 | claude-handoff | in-progress | never-evaluated | reject | handoff plugin (+ unattended charter) |
| 23 | loop-me | in-progress | never-evaluated | reject | grill-me + design-exploration |
| 24 | wizard | in-progress | never-evaluated | PARK | ownerless (script-gen) |
| 25 | writing-beats | in-progress | never-evaluated | PARK | ownerless (article composition) |
| 26 | writing-fragments | in-progress | never-evaluated | PARK | ownerless (article explore) |
| 27 | writing-shape | in-progress | never-evaluated | PARK | ownerless (article exploit) |
| 28 | git-guardrails-claude-code | misc | never-evaluated | reject | update-config + friction-to-guards (+ always-loaded charter) |
| 29 | migrate-to-shoehorn | misc | never-evaluated | reject | migration-campaign (single-vendor) |
| 30 | scaffold-exercises | misc | never-evaluated | reject | ownerless-unneeded (ai-hero-cli infra) |
| 31 | setup-pre-commit | misc | never-evaluated | reject | ownerless-unneeded (JS toolchain) |
| 32 | edit-article | personal | never-evaluated | PARK | ownerless (single-article editing) |
| 33 | obsidian-vault | personal | never-evaluated | reject | obsidian:obsidian-cli + obsidian-markdown |
| 34 | grill-me | productivity | settled-restored | reaffirm-keep | first-party grill-me |
| 35 | grilling | productivity | settled-rejected | reaffirm-reject | grill-me |
| 36 | handoff | productivity | never-evaluated | **FOLD** | handoff:save-handoff (redact secrets/PII) |
| 37 | teach | productivity | settled-admitted | reaffirm-keep | first-party teach |
| 38 | writing-great-skills | productivity | settled-rejected | reaffirm-reject (+ Negation fold, Tier 2) | agent-facing-design cluster / writing-principles |

**Tally:** 1 admit · 6 folds (7 fold *actions* — `triage` folds ×2) touching 6 target skills · 1 Tier-2 fold candidate · 6 parks · 24 rejects/reaffirm-rejects/reaffirm-keeps. All 38 accounted for.

---

## Non-skill / meta findings (content scan)

Scope: `.agents/` authoring conventions, `docs/engineering|productivity/` router pages, `.out-of-scope/` rationale docs, `CONTEXT.md`/`CLAUDE.md`, and cross-cutting reference files. Every "already owned" verdict verified by reading the JP-side file.

**Two clean folds (already surfaced above):** the tautological-test anti-pattern → `tdd/tests.md` (the reference-file angle on Tier-1 #1, same donor/target), and Negation/positive-prompting → `writing-principles` (the meta scan independently rated this the second-cleanest fold; treated as Tier 2 for the house-convention tension). Fold the *concept*, not the glossary.

**Marginal / parked (verified largely served under other framing):**
- **Fowler 12-smell taxonomy as a shared reference** — partial first-party coverage; each target already reaches the smells via its own lens. Parked (Tier 2).
- **"Defining constraint" + "It's working if" authoring conventions** (`.agents/writing-docs.md`) — largely served by JP's Fence sections, non-use boundaries, and `behavior-smoke-test`'s observable-signal proof. The rest of `writing-docs.md` is infra for mattpocock's publishing flow (not adopted).
- **"No-Op" verdict, model-relative nuance** (`writing-great-skills/GLOSSARY.md`) — substantially owned; `writing-principles`' Core Move *is* the No-Op test under different framing. Only the "settle by running, not debate" nuance is arguably absent. Marginal.

**Already owned — reaffirm, no fold (verified identical or richer on JP's side):** `.out-of-scope/` rationale-doc discipline (JP `triage/OUT-OF-SCOPE.md` is near-identical); the ADR three-part offer-gate (JP `grill-with-docs/ADR-FORMAT.md` adds "Revisit when"); deepening dependency categories (JP `DEEPENING.md` adds badges); "Design It Twice" (JP `INTERFACE-DESIGN.md` adds a sequential fallback); mocking-at-boundaries (JP `tdd/mocking.md` adds Pitfalls); the CONTEXT.md domain-model format (owned by `grill-with-docs`); the model-vs-user-invoked axis (JP already operates it via `skills/` vs `skills-claude/` + `disable-model-invocation`); and the human-facing `docs/*` pages (thin router nodes with no separable discipline; the site itself is un-adopted infra).

**Charter/house-safety:** the meta folds are inert reference-prose additions to owned skills (no always-loaded contract, no unattended firing, no irreversible tools, no `rm`/protected-branch/silent-fallback hazard) — but per the charter note above, landing a third-party discipline into a *non-adopted* first-party skill (as with Negation → `writing-principles`) is still a case-(d) fate-of-third-party-material decision and gets a ledger note. The only meta-fold into an already-adopted fork is the tautological-test line into `tdd` (the same borderline as the Tier-1 `tdd`/`triage` folds).

---

## Honest limits

- This eval **read** the first-party target files and the mattpocock sources to establish collisions and ownership; it did **not** run any skill, execute any fold, or edit any owned skill. Every Tier-1/Tier-2 action still needs the owning-skill edit to be authored, validated per the repo's Validation Ladder (frontmatter parse, referenced-path check, a realistic dry run), and — per the charter note — a `contract-decisions.md` ledger entry (full for the `resolving-merge-conflicts` admit; a note for each fold; the `tdd` and `triage` folds are the borderline build-and-prune case to confirm at landing).
- The `save-handoff` fold is **plugin-distributed** — it must follow the Plugin Layout publish path (version bump + Codex republish + mirror), not the local-skill flow.
- Confidence is stated per item: **HIGH** on the clean folds (`tdd` tautological, `to-spec` seam-count) and most rejects/reaffirms; **MEDIUM** on the admit (`resolving-merge-conflicts` — thin donor, needs a house rebuild), the `to-tickets` routing fold (defensibly reject-with-note), the `handoff` redaction fold, and the Negation fold (house-convention tension); the parks are MEDIUM by nature.
- The freshest deltas — and therefore the highest-value re-checks if this is revisited — are mattpocock's evolved `to-tickets`/`to-spec`, `wayfinder`, `triage` (external-PR extension), and the reshaped `tdd`. That is where the source moved most since 07-05 and where the actionable folds concentrate.
- Two verify passes **corrected** their eval: `diagnosing-bugs` was upgraded from reaffirm-settled to **fold** (a live un-folded Phase-1 gate remains), and the `to-spec` verify corrected a non-material `disable-model-invocation` misstatement about `to-prd` (recommendation unchanged). One verify agent (`writing-great-skills` → Negation) **died on a connection drop**; that item's absence claim was re-confirmed by hand this session, as were the sole admit and the top `tdd` fold — so no load-bearing recommendation rests on an unverified report.
- Provenance: 38-skill fan-out + per-verdict adversarial verify + meta scan + completeness critic (workflow `wf_0b65f407-fae`, 66/67 agents; the one failure is the Negation verify noted above). The critic's one must-fix (a self-contradiction on whether folds are charter events) is resolved in the charter note above.
