# PLAN: Build `assumption-check` (Band-A opener)

Rank: 2 of 5 — highest absolute capability leverage. `assumption-check` is the single strongest recommendation of the frozen Era-62 capability review (`docs/reviews/2026-07-01-skill-library-capability-growth-review.md`): the only candidate all 3/3 blind controls named unprompted, the named first build of the banked engineering backlog ("Build `assumption-check` … the fastest proof the pre-build de-risking lane is real", line ~209). The library currently has nothing that cheaply proves a plan's load-bearing beliefs before commit — it generates (`ideate`), critiques (review family), and imagines failure (`premortem`), but no forward de-risking lane exists.

## Goal

Author a new dual-runtime skill `skills/assumption-check/` that, given a settled plan/design/decision, enumerates its load-bearing assumptions (including implicit ones), ranks them qualitatively by how load-bearing and how uncertain each is, and attaches the cheapest confirm-or-kill probe to each — as a durable artifact. Forward-looking, non-adversarial, renders no verdict.

## Ground rules (repo invariants — do not skip)

- Branch first (`feature/assumption-check`); the hook blocks edits on `main`. Never `rm`; use `trash`.
- This is a **build-and-prune** skill: it cannot fire unattended (invoke-only advisory), wields no irreversible-effect tools (writes one Markdown artifact), and is first-party. Therefore: NO charter consult, NO admission test, NO ledger entry. A weaker model tends to over-trigger the charter here — `docs/agents/charter.md:3` explicitly warns that gating ordinary skill authoring over-triggers it. Do not ledger this build.
- Do NOT edit `AGENTS.md` (the roster is implicit; AGENTS.md lines are always-loaded contracts and ARE charter-gated — adding one would turn a free build into a gated event).
- Do NOT edit the frozen capability review or the frozen challenge record. Read-only.
- Markdown: one logical line per paragraph/bullet, no hard wrap.

## Required pre-reads, in order (each shapes a specific decision)

1. `docs/reviews/2026-07-02-framework-challenge.md` — the read-before-work authority for any capability work. You are ADDING a skill, which stays legitimate under it (admission is ungated; the ledger governs the keep side), but read it so you don't contradict its evidence-tier language in the skill text.
2. `docs/reviews/2026-07-01-skill-library-capability-growth-review.md` — the sections on Opening A and `assumption-check` (search for `assumption-check`; the load-bearing lines are ~41, ~77, ~123, ~184, ~195, ~209). This is the design brief: "Enumerate a settled plan's load-bearing assumptions, rank each by (load-bearing × uncertainty), and attach the cheapest confirm-or-kill probe to each, as a durable artifact — forward, non-adversarial, renders no verdict."
3. `skills/agent-facing-design/SKILL.md` — the gate for new agent-facing obligations. Apply its questions to your draft before finalizing (it is the house constitution for avoiding machinery). This skill is a judgment skill with a small trust-shaped artifact tail; per the Two Kinds of Skill frame, its structure may organize thinking but must not do the thinking.
4. `skills/skill-ux-design/SKILL.md` — authoring-time UX consult (hand-authored builds route here on Claude per `AGENTS.md`'s lane table).
5. Neighbor descriptions, to sharpen the routing boundary: `skills/premortem/SKILL.md`, `skills/red-team/SKILL.md`, `skills/grill-me/SKILL.md`, `plugins/review-family/skills/scrutinize/SKILL.md` (frontmatter descriptions suffice).

## Exact files to touch

1. `skills/assumption-check/SKILL.md` — the only new file. Minimal bundle: no `references/`, no `examples/`, no `agents/openai.yaml` (add companion metadata only if it demonstrably reduces load in SKILL.md — it will not, at this size).
2. `~/.claude/skills/assumption-check` — created by the sync script, not by hand (Step 5).

## Steps, in order

### Step 1 — branch and pre-reads

`git status --short --branch`, then `git checkout -b feature/assumption-check`, then the five pre-reads above.

### Step 2 — name-collision check (already verified, re-confirm cheaply)

`assumption-check` collides with no Codex-bundled name (`openai-docs`, `skill-creator`, `skill-installer`, `plugin-creator`, `imagegen`, `pdf`, `doc`, `codex-primary-runtime`) and no Claude-bundled name (`code-review`, `debug`, `loop`, `claude-api`, `run`, `verify`, `review`, `init`). Confirm no existing dir: `ls skills/ skills-claude/ plugins/*/skills/ | grep -x assumption-check` returns nothing.

### Step 3 — author `SKILL.md`

Frontmatter (quote the description — it contains commas and parentheses; keep name == dir name):

```yaml
---
name: assumption-check
description: "Use when a plan, design, or decision is settled enough to act on and you want its load-bearing assumptions surfaced before building: enumerate what must be true for the plan to work, rank each by how load-bearing and how uncertain it is, and attach the cheapest confirm-or-kill probe to each, as a durable artifact. Forward and non-adversarial; renders no verdict on the plan. Do not use for adversarial review of an artifact (scrutiny lanes), imagining completed failure (premortem), attacker modeling (red-team), or one-question-at-a-time interrogation (grill-me)."
---
```

That description is ~80 words: over the soft 60 ceiling, under the ~90 boundary, justified because the misroute risk against four adversarial neighbors is the review's own stated carve. Do not add workflow steps to the description.

Body requirements (write to house shape — read 2–3 sibling skills like `premortem` and `scope-cut` for tone before writing):

- **What it does**: a forward de-risking pass over a settled plan. Three moves, in order: enumerate (surface every assumption the plan needs to be true, explicit and implicit — technical, environmental, human, sequencing, and "someone else already solved this" assumptions), rank (qualitative ordering by load-bearing-ness crossed with uncertainty — the assumptions that are both structural and unverified go first), probe (for each ranked assumption, the cheapest observable confirm-or-kill test: a command to run, a file to read, a 10-minute spike, a question to a named human, a doc to check — each probe names what evidence would confirm and what would kill).
- **Ranking is words, not numbers**: an ordered list with a one-clause reason per item. Explicitly forbid numeric scores, weight formulas, and matrices — the house holds against scoring machinery (`making-recommendations` decides by argument, not measurement; `agent-facing-design` rejects classifiers/scores). The review's "(load-bearing × uncertainty)" phrase describes the judgment, not a formula to compute.
- **No verdict**: the skill never says the plan is safe, ready, de-risked, or approved. Closing language reports what was enumerated and what remains unprobed — the no-certificate discipline (`ideate`'s law; "don't manufacture confidence over what you cannot verify"). A run's honest output can be "three load-bearing assumptions, none yet confirmed."
- **Non-adversarial boundary, stated in-body too**: `scrutinize`'s Assumptions Audit *tags* assumptions adversarially while planning no confirmations; `premortem` reasons backward from asserted failure; `assumption-check` reasons forward from the plan and plans confirmations. Name these seams so the skill self-routes.
- **Durable artifact with a default home**: in a git repo, write `docs/plans/YYYY-MM-DD-<topic>-assumptions.md` (create `docs/plans/` if absent), honoring any repo convention that overrides; with no repo or on ask, deliver in chat. The artifact lists each assumption with rank-reason, probe, and a status column the human can fill (`unprobed` / `confirmed` / `killed` — statuses are the artifact's vocabulary for the human, not workflow states the agent enforces).
- **Stop condition**: the run ends when the artifact is written and every ranked assumption has a probe; executing probes is offered, not assumed — run them only on ask (many probes are the human's to run).
- **Dual-runtime phrasing**: name both tokens (`/assumption-check` or `$assumption-check`); refer to instruction files jointly (`AGENTS.md` or `CLAUDE.md`); phrase any routing to single-runtime skills availability-conditionally ("when `review-family:scrutinize` is available…").

### Step 4 — validate structure

```bash
python3 /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/assumption-check
git diff --check
```

Note: that validator path was restored 2026-07-09 (a Codex update recreated `~/.codex/skills/.system/`). If it is absent again, do a manual YAML parse (`python3 -c "import yaml,sys; print(yaml.safe_load(open('skills/assumption-check/SKILL.md').read().split('---')[1]))"`) and say plainly in your report that quick_validate was unavailable and what replaced it. Never claim it ran when it didn't. If quick_validate complains ONLY about an "unexpected key" for `argument-hint` or `disable-model-invocation`, that specific complaint is accepted (validator schema gap) — but this skill uses neither field, so any complaint here is real.

### Step 5 — link into Claude delivery

```bash
scripts/claude-skills-sync.sh --link assumption-check
scripts/claude-skills-sync.sh --check   # must exit 0
ls -la ~/.claude/skills/assumption-check   # symlink → /Users/jp/.agents/skills/assumption-check
```

Codex needs no step — it scans `$HOME/.agents/skills` in place.

### Step 6 — behavior smoke test (obedience proof, not structure proof)

Structural checks prove the file parses; only a realistic invocation shows the contract is followed. Spawn one fresh subagent (Sonnet-class is fine) whose prompt contains (a) the full text of the new SKILL.md, framed as "this skill is active; follow it", and (b) this sample plan, verbatim, with the ask "Here's my plan — run the assumption check on it":

> Plan: migrate our CI from Jenkins to GitHub Actions next sprint. Steps: port the 14 Jenkinsfiles to workflow YAML, move secrets to GitHub environments, cut over the main branch first, then the release branches, decommission the Jenkins box at month end. The team already knows GitHub Actions from side projects, and our deploy scripts should run unchanged since they're plain bash.

Grade the transcript against four checks (all must pass):

1. Enumerates assumptions including at least two IMPLICIT ones the plan never states (candidates a good run finds: runner capacity/concurrency limits, secrets referenced inside scripts not just in Jenkins credentials, "plain bash runs unchanged" assumes same runner OS/tooling, "team already knows" is an untested skill claim, month-end decommission assumes no long-tail jobs live only on Jenkins).
2. Ranking is a reasoned ordering in prose — zero numeric scores, no weighted matrix.
3. Every ranked assumption has a concrete cheapest probe naming its confirm and kill evidence.
4. No verdict language anywhere ("plan looks solid", "ready to proceed", "low risk overall" are all failures).

If any check fails, fix the SKILL.md language that permitted the failure and re-run once. Report the transcript evidence honestly, including what the smoke test does NOT prove (one synthetic run ≠ field validation).

### Step 7 — commit

```bash
git add skills/assumption-check/SKILL.md
git commit -m "feat: add assumption-check skill (Band-A opener, Era-62 review #1 recommendation)"
```

Do not merge or push unless JP asks. Report branch, smoke-test evidence, and validator output.

## Edge cases found during exploration (a weaker model would miss these)

- The review says "rank each by (load-bearing × uncertainty)" — implementing that as a scoring formula would fail the `agent-facing-design` gate and contradict two methodology holds. It is a qualitative judgment instruction.
- The skill must not become a gate. Nothing in it may block, approve, or require sign-off; it is advisory offload. Any "the plan may not proceed until…" phrasing is a defect.
- Probe execution is opt-in. A run that auto-executes probes (running commands against the user's infra unasked) violates the autonomy boundary; the artifact is the deliverable.
- The artifact's status column is for the HUMAN. Do not instruct future agents to maintain, audit, or enforce it — that would be persistent-artifact machinery, exactly what `agent-facing-design` exists to catch.
- `docs/plans/` here is the AUTHORING repo's convention; the skill fires in ANY repo. Word the artifact-home instruction as "the consuming project's docs convention, defaulting to `docs/plans/`" — do not hardcode `.agents` paths into a global skill.
- Frontmatter description must be quoted (it contains a colon after "building"). Unquoted YAML here fails the loader silently on some parsers.
- Name the skill dir and frontmatter `name` identically (`assumption-check`) — the library-integrity check enforces name==dir.
- Do not add `disable-model-invocation`: model-initiated firing on real planning work is wanted (it is how the usage ledger will accumulate keep-evidence by 08-01).

## Acceptance criteria (verify each; do not claim done without output)

1. `skills/assumption-check/SKILL.md` exists; frontmatter parses; `name: assumption-check` == dir name; description is 60–90 words with Use-when phrasing and the four-neighbor non-use boundary.
2. quick_validate passes ("Skill is valid!") or its unavailability is reported with the manual parse shown.
3. `claude-skills-sync.sh --check` exits 0 and `~/.claude/skills/assumption-check` is a symlink to the repo dir.
4. Smoke-test transcript passes all four graded checks, with the transcript (or its location) in the report.
5. No changes to `AGENTS.md`, no ledger entry, no other skill touched; `git diff --cached --stat` shows exactly one new file.
6. One commit on `feature/assumption-check`; `git diff --check` clean.
