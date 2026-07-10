# PLAN: Land the Era-62 §6 free folds (doc-drift-audit widening + four fold-visibility notes)

Rank: #5 of 5. The review's §9 move 7 — near-zero-cost owner-expansions that close six already-adjudicated fold candidates so they cannot resurface in the next capability review, and give `doc-drift-audit` a genuinely new input class (groundedness-screening fresh agent output). Cheapest plan in the queue; independent of the other four.

## Goal

Land the five §6 expansions from the frozen Era-62 review (`docs/reviews/2026-07-01-skill-library-capability-growth-review.md`, §6): (1) widen `doc-drift-audit`'s input frame to fresh agent-produced artifacts that assert code facts — this folds the `groundedness-screen`/`hallucination-screen` candidate; (2) one fold-visibility sentence in `implementation-review`'s error-suppression lens (folds `error-handling-audit`/`silent-failure-hunt`) — a PLUGIN edit taking the patch-release path; (3) one CI-gate note in `keep-green` (folds `ci-triage`); (4) a removal/safe-delete limiting-case paragraph in `contract-change-propagation` (folds `prune-dead-code`'s reachability half); (5) an escalation section in `email-writing` (folds `escalation-framing`). All build-and-prune edits to first-party skills: NO ledger entries. The `perf-optimize`→`diagnose` item from §6 is deliberately NOT in scope — the review classes it design-first-carve, and that boundary decision has not been made.

## Files to touch

- EDIT: `skills/doc-drift-audit/SKILL.md` (description + body), `skills/keep-green/SKILL.md` (one paragraph), `skills/contract-change-propagation/SKILL.md` (one paragraph), `skills/email-writing/SKILL.md` (one short section).
- EDIT (plugin path): `plugins/review-family/skills/implementation-review/SKILL.md` (one sentence), `plugins/review-family/.claude-plugin/plugin.json` (version `0.8.0` → `0.8.1`), `plugins/review-family/CHANGELOG.md` (new entry).
- RUN (not edit): `scripts/claude-skills-sync.sh`, `scripts/codex-plugins-sync.sh`, `scripts/check-review-family.sh`, `scripts/check-library-integrity.sh`.
- READ ONLY: the review's §6 (authority), `AGENTS.md` (Plugin Layout And Delivery + Validation Ladder).

## House rules (apply throughout)

- Branch first: `git checkout -b chore/era62-free-folds` (a hook blocks edits on `main`).
- Never `rm`; use `trash`. Never push. Do NOT sync the GitHub mirror (`/Users/jp/Projects/active/codex-tool-dev`) — mirror sync is JP-ask only; the Codex CACHE republish below is the normal local delivery step and IS in scope.
- Markdown: one logical line per paragraph/bullet; no hard wrapping.
- Each edit is additive and surgical: quote-anchor exactly as specified below; change nothing else in each file.
- `implementation-review` is canary-guarded: do NOT touch its read-only-boundary text or its Bounded Review section (the CANON cores) — the edit below sits in workflow Step 3, outside both. `scripts/check-review-family.sh` must stay green after the edit.

## Implementation order

### Step 1 — Read the authority and the five live targets

Read the review's §6 and all five target SKILL.md files end to end before editing. Verify the anchor sentences below still exist verbatim (`grep -F -e '<anchor>'` — the `-e` matters: one anchor begins with a dash and is otherwise parsed as an option); if any anchor has drifted, find the equivalent live sentence, adapt the insertion point, and note the deviation in the final report — do not skip the edit.

### Step 2 — Widen `doc-drift-audit` (the substantial edit)

(a) Replace the frontmatter description with this, verbatim (quoted):

```yaml
---
name: doc-drift-audit
description: "Use when auditing whether prose that asserts code facts still matches the code — a documentation set (README, API/reference docs, CLI or config docs) or a fresh agent-produced artifact (PR description, design doc, review comment, commit message, or a chat answer asserting code facts): checking that the symbols, paths, signatures, endpoints, config keys, and flags named in the prose still resolve against the current code tree, surfacing only high-confidence stale references and routing fixes to `/triage`. Read-only; detects, never edits or fixes. Not for resolving which source-of-truth governs a claim (`baseline`), driving the fix when intent changed (`spec-drift-reconcile`), a scored debt audit (`tech-debt-scan`), or checking runtime behavior (`verify`/`behavior-smoke-test`)."
---
```

(b) In the summary paragraph (currently begins "Audit a documentation set against the code it describes:"), replace that opening clause with: "Audit prose that asserts code facts — a standing documentation set or a fresh agent-produced artifact — against the code it describes:" (rest of the paragraph unchanged).

(c) Insert a new section titled `## Two input frames` immediately after the `## Core contract` section, with exactly this content:

> The engine is one; the input is either:
>
> - **Standing docs** (the default) — README, `docs/`, API/reference, CLI/config docs. Full artifact output as specified below.
> - **Fresh agent output** — a PR description, design doc, review comment, commit message, or chat answer that asserts code facts, checked before it is trusted or merged. Same referent rules, same probe ladder, same cardinal honesty. Two frame-specific defaults: the artifact may be skipped for a quick screen — deliver the chat-only report and label the missing artifact a proof limit — and findings route back to the artifact's author or thread instead of `/triage` when the prose under audit is not committed documentation.
>
> Either way the audit checks that the prose's *nouns resolve*, never that its *verbs are true*. A groundedness or hallucination screen over agent-produced prose is this skill in the fresh-artifact frame, not a separate job — only the input surface differs.

(d) In the `## Workflow` section, step 2 (**Inventory**), append this sentence: "In the fresh-artifact frame, the supplied artifact is the whole doc set — name it and skip directory enumeration."

Everything else — the probe ladder, the FP discipline, read-only boundaries, output shape, fences, build-and-prune note — stays byte-identical.

### Step 3 — The three one-paragraph dual-runtime folds

(a) `skills/keep-green/SKILL.md`, section `## Freeze the gate`: insert this as a new paragraph immediately after the paragraph ending "Green = lint and test both exit clean on a full run.":

> A red CI check on the change's own fresh push or PR is the same gate showing remotely: pull the failing job's log, map it to the frozen local gate, reproduce locally, and drive it green here — CI-red triage on a just-made change is this skill's job, not a separate lane. A remote-only failure that cannot be reproduced locally is cause-unknown: escalate it like any other.

(b) `skills/contract-change-propagation/SKILL.md`, section `## 3. Enumerate consumers`: insert this as a new paragraph at the end of the section (immediately after the paragraph ending "...causes the exact breakage this skill exists to prevent."):

> **Removal is the limiting case.** When the proposed change is a deletion — remove this function, endpoint, config key, or flag — the blast-radius question collapses to "who still consumes it?": run the same multi-way enumeration, and zero confirmed consumers plus an honestly-stated could-not-reach gap yields **"safe to remove, residual named"** — never "proven unused", because the search cannot see reflective, serialized, or out-of-repo consumers. The removal edit itself belongs to the owning change (or `simplify-code` for pure cleanup); this skill still stops at the plan.

(c) `skills/email-writing/SKILL.md`: insert a new `## Escalations` section between `## Asks, Follow-Ups, And Urgency` and `## Calibration Examples`, with exactly this content:

> When JP needs to raise a blocker, risk, or problem to someone with more authority:
>
> - Lead with the concrete impact and when it bites, before the history of how it happened.
> - Stay blame-free. Describe the situation and the constraint, not fault: `the integration is blocked on sandbox credentials`, not a line about who dropped the ball.
> - Make one specific ask — a decision, a resource, or a deadline change — and name the date an answer is needed by.
> - Keep supporting detail one link or attachment away instead of inline, so the email stays short enough to act on.
> - State urgency plainly, once. No apology stacking, no manufactured pressure, no extra formality as a cushion.

### Step 4 — The plugin fold (patch-release path)

(a) `plugins/review-family/skills/implementation-review/SKILL.md`, workflow Step 3, the bullet beginning "- Error suppression: empty or overly broad catches, errors logged then swallowed, and defaults or fallbacks that mask the underlying failure.": append this sentence to that bullet (same line, after the period):

> A standalone error-handling or silent-failure audit is this lens pointed at a chosen scope — route such a request into a review bounded to that scope, not to a separate skill.

(b) `plugins/review-family/.claude-plugin/plugin.json`: bump `"version": "0.8.0"` → `"0.8.1"` (additive prose = PATCH per the repo's release discipline).

(c) `plugins/review-family/CHANGELOG.md`: add above the `## 0.8.0` entry, using the actual execution date:

> ## 0.8.1 - YYYY-MM-DD
>
> ### Changed
>
> - `implementation-review`'s error-suppression lens now states its ownership plainly: a standalone error-handling / silent-failure audit is this lens pointed at a chosen scope, not a separate skill. One sentence, closing the 2026-07-01 capability review's §6 fold-visibility note so the folded candidate does not resurface. Both CANON cores (read-only, bounded-review), the routing frontmatter, and every other organ are unchanged.

### Step 5 — Validate

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/doc-drift-audit
python3 -c "import yaml; [yaml.safe_load(open(p).read().split('---')[1]) for p in ['skills/doc-drift-audit/SKILL.md','skills/keep-green/SKILL.md','skills/contract-change-propagation/SKILL.md','skills/email-writing/SKILL.md','plugins/review-family/skills/implementation-review/SKILL.md']]; print('all frontmatter parses')"
python3 -c "import json; print(json.load(open('plugins/review-family/.claude-plugin/plugin.json'))['version'])"
git diff --check
scripts/check-review-family.sh
scripts/check-library-integrity.sh
scripts/claude-skills-sync.sh --check
```

All must pass (`0.8.1` printed; canaries green). Prove the doc-drift-audit description character-exact against this plan's yaml block (same python comparison as plan #1, paths substituted). For the four one-sentence/one-section folds, verification is the read-back of each inserted text plus these checks — a per-line behavior smoke is deliberately not run (proportionate to additive prose); say exactly that in the final report per the Validation Ladder's item 5.

### Step 6 — Behavior smoke test (doc-drift-audit only — the one behavior change big enough to prove)

Build a fixture in the scratchpad: `git init` a tiny repo with one file `app.py` containing `def load_config(path):` and `def render_report(data):` (bodies trivial), committed. Then spawn ONE fresh subagent with the updated `doc-drift-audit` SKILL.md as active guidance and this task verbatim: "An agent just wrote this PR description for our repo at <fixture path>. Before we post it, check it against the code: 'This PR refactors config loading. `load_config` now delegates to `validate_schema()` in `src/utils/config.py`, and retries loading three times on transient errors.'" Grade five behaviors: (1) accepted the PR description as the audit target under the fresh-artifact frame without balking that it is not a documentation set; (2) pinned the fixture's HEAD SHA and ran the probe ladder (recorded commands) before calling anything a miss; (3) flagged `validate_schema` and `src/utils/config.py` as high-confidence misses while NOT flagging the resolving `load_config`; (4) surfaced "retries three times" as a behavioral claim routed out (to the author/verification), not verified and not silently dropped; (5) delivered the chat-only report carrying the mandatory disclaimer (references resolve ≠ docs accurate), labeled the skipped artifact a proof limit, and edited nothing. 4/5 → proceed; below → tighten the new frame text once and re-run; still below → STOP at the committed branch and report honestly. Trash the fixture afterward.

### Step 7 — Commit, land, republish the Codex cache

```bash
git add skills/doc-drift-audit skills/keep-green skills/contract-change-propagation skills/email-writing
git commit -m "feat: land Era-62 §6 free folds — doc-drift-audit fresh-artifact frame; CI-gate, removal-mode, escalation notes"
git add plugins/review-family
git commit -m "feat(review-family): error-suppression fold-visibility note — cut 0.8.1"
git checkout main && git merge --ff-only chore/era62-free-folds
git branch -d chore/era62-free-folds
scripts/codex-plugins-sync.sh --publish review-family
scripts/codex-plugins-sync.sh --check
git status --short --branch
```

Publish the cache AFTER the ff-merge so the cache matches `main`. `--check` must exit 0. Do NOT push; do NOT touch the mirror; do NOT add ledger entries.

## Edge cases a weaker model would miss

- **The plugin edit does not follow the local-skill flow.** `implementation-review` lives in `plugins/review-family/` — Codex serves it from a version-keyed cache, so without the version bump + `codex-plugins-sync.sh --publish`, Codex keeps serving 0.8.0 forever while Claude silently serves the new text. Claude-side needs nothing (served in place through the symlink).
- **The mirror will now trail by design.** The GitHub mirror already lacks 0.8.0's LICENSE (a known, recorded residue); after this plan it also trails 0.8.1. That is correct — mirror sync is JP-ask only. State it in the final report as the standing residue, do not "helpfully" sync it.
- **The CANON cores are drift-guarded.** A SessionStart canary (`check-review-family.sh`) asserts the read-only core is consistent across the five review skills and the bounded-review core across three. The error-suppression bullet is outside both cores, but any stray edit to boundary text breaks the canary at every future session start — run the script and keep the diff surgical.
- **doc-drift-audit's description is now >90 words — deliberately.** The Era-85 out-of-scope hold says description length is a routing-clarity input, never a conformance score; do not trim it to fit the soft budget, and do not reflow it.
- **The fresh-artifact frame must not weaken the FP discipline or read-only stance.** The probe ladder, the distinctive-token gate, and never-editing still bind; the only frame differences are the optional chat-only output and author-routing. The planted `load_config` in the smoke fixture exists precisely to catch an over-eager executor whose widened skill starts crying drift on resolving references.
- **`keep-green`'s note must not expand its scope** to babysitting arbitrary CI: it covers red CI on the change's OWN fresh push/PR; remote-only irreproducible failures escalate as cause-unknown. The insertion text above encodes both halves — use it verbatim.
- **`email-writing`'s new section must match that file's register** — plain prose, no producer-skill vocabulary (no "fences", "verdicts", "proof"). The text above is written in-register; use it verbatim.
- **Anchors may have drifted** since this plan was written: `grep -F` each anchor sentence first; adapt the insertion point if needed and record the deviation — never silently skip an edit, never rewrite surrounding text to force a match.
- **Two commits, not one:** the dual-runtime skill edits and the plugin cut are separate concerns; the version bump rides the commit that carries the plugin change (release discipline: the landing commit carries the bump).

## Acceptance criteria

1. All five target files contain their specified insertions verbatim (adapted anchors documented if any); nothing else in them changed (`git diff` per file shows only the specified hunks).
2. `doc-drift-audit`'s description is character-exact to this plan's yaml block; `quick_validate.py skills/doc-drift-audit` passes; all five edited frontmatters parse.
3. `plugins/review-family/.claude-plugin/plugin.json` reads `0.8.1`; CHANGELOG has the 0.8.1 entry above the 0.8.0 entry with the real execution date.
4. `scripts/check-review-family.sh`, `scripts/check-library-integrity.sh`, `scripts/claude-skills-sync.sh --check`, and `git diff --check` all pass; `scripts/codex-plugins-sync.sh --check` exits 0 AFTER the publish (cache at 0.8.1).
5. Smoke test recorded: 5 behaviors on the fresh-artifact frame, ≥4 passed, fixture task plan-verbatim, fixture trashed after.
6. Both commits landed on `main` via `--ff-only`; branch deleted; tree clean; nothing pushed; mirror untouched (trailing residue stated in the report); no ledger entries.
7. Final report names the six §6 candidates now closed in-text (groundedness-screen, hallucination-screen, error-handling-audit, silent-failure-hunt, ci-triage, prune-dead-code's reachability half, escalation-framing) and the one §6 item deliberately left open (`perf-optimize` → design-first-carve).

## Out of scope

The `perf-optimize`/`diagnose` proactive-perf branch (design-first-carve — a boundary decision, not a free fold); mirror sync; any Opening-D build (`dependency-adoption`, `secret-leak-response` — next queue's material); rewording any existing prose beyond the specified insertions; ledger entries; publishing.
