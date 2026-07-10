# PLAN: Author the skill-value-test pre-registration (seal — do NOT run trials)

Rank: #1 of 5. Do this first.

## Goal

Produce the sealed pre-registration for the banked skill value test: one new document that fixes the skill sample, the exact scenario prompts, the judges, and the numeric decision thresholds — so the test can later run against a seal instead of being shaped by its own results. The banked design note (`docs/plans/2026-07-02-skill-value-test-plan.md`) says in its own frontmatter: "pre-register (seal exact prompts, sample, judges, and thresholds) before the first trial; this document is the design note, not the pre-registration". This plan authors that missing pre-registration. It does NOT run any trial.

Why this is #1: the pre-registration is the only remaining blocker on the library's first *value* measurement (everything else measures obedience, convergence, or usage), and it pairs with the committed 2026-08-01 skill-usage-ledger re-read — "so the prune deliberation gets both instruments at once" (design note, Cost and when). Landing it now, well before 08-01, is the whole point.

## Files to touch

- CREATE: `docs/plans/2026-07-10-skill-value-test-preregistration.md` (adjust the date prefix to the actual execution date).
- READ ONLY (never edit): `docs/plans/2026-07-02-skill-value-test-plan.md`, `docs/reviews/2026-07-02-framework-challenge.md`, `docs/agents/contract-evaluation-methodology.md`, `AGENTS.md` (the `## Blind Evaluations` section), the three sampled skills' `SKILL.md` files.
- Nothing else. Do not edit the design note's status line; the new doc references it.

## House rules (apply throughout)

- Work on a branch: `git checkout -b chore/value-test-prereg` BEFORE creating any file. A user-level hook blocks edits on `main`.
- Never run `rm`; use `trash <path>` if you must delete something.
- Markdown: one logical line per paragraph and per bullet — never hard-wrap prose at a fixed column.
- Do not push, do not open PRs, do not touch `plugins/`, the Codex cache, or the release mirror.
- Blind-evaluation discipline (AGENTS.md `## Blind Evaluations`): never reveal apparatus state — arm identities, the seal's contents, predictions — in any channel a current or potential judge (human or separate model) can see before their judgment is recorded. In this plan that means: subagents you spawn to author or review prompt wording must NEVER receive skill text, the seal draft, this plan, or the repo's framework vocabulary.

## Implementation order

### Step 1 — Read the governing docs

Read, in this order: `docs/plans/2026-07-02-skill-value-test-plan.md` (the design you are instantiating — every design decision below comes from it), `docs/reviews/2026-07-02-framework-challenge.md` (the pre-registered 2026-08-01 branches you must not disturb), `AGENTS.md` `## Blind Evaluations`.

### Step 2 — Fix the sample with ledger evidence

Run `python3 /Users/jp/.agents/scripts/skill-usage-miner.py --summary-only` and capture the output. Fix the three-skill sample per the design note's categories:

1. **Positive control** (cross-model-certified keeper): use `git-cycle:release-cut`. Rationale to record: scenario is stageable headless against a small fixture repo (a manifest + CHANGELOG), unlike `gh-address-comments` which needs a live PR with review threads.
2. **High-traffic judgment skill**: use `making-recommendations` — confirm from the summary output that it has fires; if it is somehow zero-fire, use `diagnose` instead and record why.
3. **Zero-fire tail skill** (Era-36–58 wave, footgun-dense): use `regex-craft` if the summary shows it at zero (or near-zero) fires; else `migration-safety` if that is zero; else any Era-36–58 domain producer the summary shows at zero. Record the actual counts in the seal.

Do not add a fourth skill (the design note's optional `scope-cut` is omitted to match its own ~60-run cost model). Record the ledger evidence (the relevant summary lines, verbatim) in the seal document.

### Step 3 — Pre-register each skill's load-bearing behaviors

For each sampled skill, read its `SKILL.md` and extract the 3–5 load-bearing behaviors its value claim rests on — the firm/trust obligations, not vibes. They must be objectively scoreable as present/absent in a transcript. Anchors:

- `regex-craft` (the design note's own example): engine identified first; fix legality checked against that engine; an executed must-match/must-not-match table; a backtracking probe actually run; exactly one scoped verdict (safe-as-proven / unsafe-here-because / unverified).
- `release-cut`: version derived from the real landed change class (not guessed, not a git tag); the authoritative manifest bumped; a dated CHANGELOG section written in lockstep; stops at a staged local bump (no push/tag/publish).
- `making-recommendations`: both leans declared before arguing; a mandatory case-against the recommended option; comparison in words with no numeric scores or weighted sums; no invented alternatives; an honest exit if the options don't separate.

Verify each behavior against the live `SKILL.md` text before sealing it — quote or cite the line it comes from. If a skill's live text no longer supports a listed behavior, substitute one it does support.

### Step 4 — Draft scenario kernels (facts only, no vocabulary)

For each skill, write 2 scenario kernels: a short factual situation description a real user could be in, sourced from realistic task shapes (past handoffs under `.agents/handoffs/` may inspire situations, but strip ALL repo/framework vocabulary). A kernel states: the situation, the artifacts that exist (e.g. "a Python service with this validation function"), and what the user wants — never how to do it.

**The vocabulary ban is per-skill and absolute** (design note: "ban the skill's own vocabulary from prompts"). Examples of banned terms: for `regex-craft` — "ReDoS", "catastrophic backtracking", "must-match table", "engine", "probe", "pump"; for `release-cut` — "change class", "semver derivation", "manifest not tag", "staged bump"; for `making-recommendations` — "case against", "dominance", "filters", "declare your lean", "trade-off structure" as instructions. The kernel may describe symptoms ("this regex sometimes makes the endpoint hang") but never the discipline.

Each kernel must also name its **fixture**: the minimal files/repo state the run session will construct so the prompt is answerable headless (e.g. "a directory with `package.json` at version 1.3.0 and a CHANGELOG.md with two prior releases"). Fixture construction happens at run time; only its specification is sealed.

### Step 5 — Fresh-context prompt authoring

For each kernel, have a FRESH-CONTEXT agent author the final prompt wording (design note: "have a fresh-context agent (no skill text in context) author the final prompt wording"). Mechanics: spawn a subagent (or run `claude -p` headless) whose entire input is the kernel plus: "Write a realistic, slightly messy user request an engineer would type to an AI coding assistant in this situation. One paragraph. Do not structure it as a checklist." The subagent must receive NO skill text, NO mention of which skill is being tested, NO seal draft, NO framework vocabulary. Collect the six prompts verbatim.

### Step 6 — Adversarial kernel-preloading review

Spawn a second, separate fresh-context agent per the design note's author-contamination bound ("the pre-registration step should have a fresh-context agent adversarially review the sealed prompts for kernel-preloading before any trial runs"). Give it ONLY the six prompts and this task: "These prompts will compare an AI assistant with and without a specialized procedure loaded. Flag any prompt that smuggles in the procedure itself — steps, ordering, named techniques, or vocabulary that tells the assistant what a careful expert would do. Quote the offending phrases." Fix flagged prompts by re-running Step 5 for that kernel (never by hand-patching in your own words — you are the contaminated author), then re-review. Record the review verdict in the seal.

### Step 7 — Seal thresholds and write the document

Create `docs/plans/<date>-skill-value-test-preregistration.md` with frontmatter (`type: pre-registration`, `status: "SEALED <ISO date> — append-only below the seal line; amendments only as dated appendices"`, `design_note: docs/plans/2026-07-02-skill-value-test-plan.md`) and these sections:

1. **Sample** — the three skills, category each fills, ledger evidence verbatim.
2. **Per-skill load-bearing behaviors** — the Step-3 lists with `SKILL.md` citations.
3. **Sealed prompts** — all six, verbatim, each with its fixture spec and its authoring provenance (fresh-context authored, adversarially reviewed, review verdict).
4. **Arms and reps** — copied from the design note: (A) bare model, (B) same prompt with the skill loaded; same model, same effort tier; N ≥ 5 reps per arm per scenario (~60 runs).
5. **Measures and thresholds** (numeric, fixed now): per rep, discipline-consistency = fraction of that skill's pre-registered behaviors present. Per skill, let ΔD = mean(arm B) − mean(arm A). Sealed mapping to the design note's three branch commitments, verbatim quotes included: "skills materially pin discipline" requires ΔD ≥ 0.30 AND mean(arm B) ≥ 0.80 for the positive control and at least one other skill; "no consistency or quality delta" is |ΔD| < 0.10 for all three AND blind quality preference for arm B ≤ 55% of pairs; anything else lands in "mixed", read per the design note (positive-control failure means instrument failure, not skill failure). Blind quality grading: paired outputs, arm-blinded, order-randomized; grader picks the better output or ties.
6. **Judges** — a model arm that has never seen this repo's vocabulary (the Antigravity/Gemini-family precedent, Eras 30–31) for the paired grading, plus JP cold-grading 2–3 pairs as the human anchor. Restate: no apparatus state reaches any judge before their judgment is recorded.
7. **What this seal does not do** — no trial has run; running is a separate, later, explicitly-authorized session; results land as a dated doc per the design note; no post-hoc reframing of branches.

### Step 8 — Validate, commit, land

- `git diff --check` on the branch (no whitespace errors).
- Verify every internal path the new doc cites exists (`ls` each).
- Re-read the six sealed prompts one final time for banned vocabulary (grep the doc for the banned terms listed in Step 4; every hit must be inside the ban-list section itself, not a prompt).
- Commit only the new file: `git add docs/plans/<date>-skill-value-test-preregistration.md && git commit -m "docs(plans): seal skill-value-test pre-registration (sample, prompts, judges, thresholds)"`.
- Land: `git checkout main && git merge --ff-only chore/value-test-prereg`. Verify `git status` clean. Do NOT push.

## Edge cases a weaker model would miss

- **The seal is not the run.** Do not execute a single arm-A/arm-B trial, "just to check the prompts work". The design note's whole point is that the seal exists before any data does. A dry run contaminates the experiment.
- **You are the contaminated author.** You have read the skills and this repo's vocabulary, so you may not write final prompt wording or hand-fix a flagged prompt — only fresh-context agents do (Steps 5–6). Your job is kernels (facts) and assembly.
- **Handoffs are saturated with framework vocabulary.** If you source situations from `.agents/handoffs/`, extract only the mundane engineering facts; a single term like "expand-contract" or "case-against" surviving into a prompt pre-loads the control arm and voids that scenario.
- **Do not touch the 2026-08-01 machinery.** The ledger re-read branches in the frozen challenge record are separate, pre-registered, and untouchable; this seal must not predict, reference-as-likely, or reframe them. Reference the pairing only as scheduling.
- **The ledger summary is the evidence, not your memory.** If `regex-craft` turns out to have fires, switching to `migration-safety` is correct and must be recorded with the numbers — do not keep a stale pick to match this plan.
- **Miner is read-only here.** Use `--summary-only`; do not run a full mine (a launchd job owns mining on its own schedule).
- **Frontmatter with colons must be quoted** in the new doc's YAML.

## Acceptance criteria

1. `docs/plans/<date>-skill-value-test-preregistration.md` exists on `main` with all seven sections, sealed status line, and quoted-YAML frontmatter.
2. The sample has exactly 3 skills, one per category, each with verbatim ledger-summary evidence.
3. Each sampled skill has 3–5 behaviors, each citing a live `SKILL.md` line.
4. Six prompts, each marked fresh-context-authored and adversarially reviewed, each with a fixture spec; a recorded reviewer verdict with zero unresolved flags.
5. Grepping the doc for each banned term finds hits only inside the ban-list section: run `grep -n -i 'backtracking\|must-match\|expand-contract\|case against\|change class' docs/plans/<date>-*preregistration.md` and confirm every hit's line number falls in the ban-list/behaviors sections, not the sealed-prompts section.
6. Thresholds are numeric and map one-to-one onto the design note's three branch commitments (quoted).
7. No trial output, no arm transcripts, no results exist anywhere in the commit.
8. Landed on `main` via fast-forward merge; `git status` clean; nothing pushed.

## Out of scope

Running trials; editing the design note, the frozen challenge record, or any skill; building fixtures; contacting judges; anything involving the 2026-08-01 re-read itself.
