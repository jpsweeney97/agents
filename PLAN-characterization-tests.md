# PLAN: Build the `characterization-tests` skill

Rank: #5 of 5. Era-62 review §9 move #3 (test-safety pair, second half).

## Goal

Create `skills/characterization-tests/` — a dual-runtime skill that authors a behavior-snapshot net (golden-master / approval tests) over existing, WORKING, UNTESTED code before a refactor, upgrade, or migration touches it: pin the seam, capture what the code actually does now as the expected values (bugs included, flagged), tame nondeterminism first, and prove the net catches change by making a deliberate mutation fail it — then revert the mutation and hand over a green net.

Authority: the frozen Era-62 review (`docs/reviews/2026-07-01-skill-library-capability-growth-review.md`, Band A): "author a behavior-snapshot net... over existing, working, untested code before refactoring/upgrading/migrating, then prove the net fails on a deliberate mutation" — "silently a precondition of `simplify-code` and `dependency-upgrade`, owned by neither". Build-and-prune: attended, writes tests (ordinary file work), mutation is temporary-and-reverted → NOT a charter event, NO ledger entry.

## Files to touch

- CREATE: `skills/characterization-tests/SKILL.md` (single file, minimal bundle).
- RUN: `scripts/claude-skills-sync.sh`.
- READ ONLY: `skills/regex-craft/SKILL.md` (mold), `skills/tdd/SKILL.md` + `skills/tdd/tests.md` (the tension to state — see edge cases), `skills/simplify-code/SKILL.md` and `skills/dependency-upgrade/SKILL.md` (the consumers), `skills/test-trust-audit/SKILL.md` IF plan #4 landed, `skills/agent-facing-design/SKILL.md`, `skills/skill-ux-design/SKILL.md`, `AGENTS.md`.

## House rules (apply throughout)

- Branch first: `git checkout -b feature/characterization-tests` (hook blocks edits on `main`).
- Never `rm`; use `trash`. Never push; no PRs; `plugins/`, cache, mirror untouched.
- One logical line per paragraph/bullet; quoted description.
- Dual-runtime tokens (`/characterization-tests` or `$characterization-tests`); availability-conditional routing.

## Implementation order

### Step 1 — Read the mold and the tension

Read `regex-craft` (skeleton), then `skills/tdd/tests.md` closely: it forbids tests that pass by construction and requires expected values from an independent source of truth — for NEW behavior. Characterization tests deliberately invert this for EXISTING behavior: the running code IS the independent source of truth about what the system currently does, and the net's job is change-detection, not correctness. The new skill must state this tension explicitly and resolve it in its own text (see edge cases), or the two skills will read as contradicting each other.

### Step 2 — Write `skills/characterization-tests/SKILL.md`

Description, verbatim (quoted):

```yaml
---
name: characterization-tests
description: "Use when working code has no tests and a refactor, upgrade, or migration is about to touch it: author a characterization net (golden-master/approval tests) that pins what the code actually does now — bugs included, flagged — taming nondeterminism first, then prove the net works by making a deliberate mutation fail it. Pins current behavior, not correctness. Not for test-first new behavior (tdd), auditing an existing suite (test-trust-audit when available), or doing the refactor itself."
---
```

Body requirements:

1. **Summary + invocation.** The safety net you weave BEFORE changing untested code; green net + proven trigger is the deliverable; the change itself is someone else's move. Invocation tokens.
2. **The owned job.** `tdd` owns test-first NEW behavior; `simplify-code` and `dependency-upgrade` both assume behavior-preservation but neither authors the net that would detect a break — this skill is their unstated precondition; an existing suite's honesty audit is a neighboring job (route availability-conditionally to `test-trust-audit` when present). Value: without a net, "the refactor preserved behavior" is an assertion; with one, it is an observation — and the human is spared hand-picking inputs, taming flakiness, and remembering that an unproven net proves nothing.
3. **Mixed skill — bar per part.** Firm (trust): expected values captured by RUNNING the current code (never reasoned from intent), the nondeterminism pass before first capture, the pin-bugs-flag-bugs rule, the mandatory mutation proof with restoration proven, the handover statement of what the net does and does not cover. Provoked (judgment): where the seam is (which boundary is worth pinning), which inputs earn a place in the net (branch-reaching, edge-hitting, not bulk), whether an output difference is nondeterminism to tame or behavior to pin.
4. **Shape — the pass.** (a) **Pin the seam** — the outermost stable boundary the upcoming change will preserve: a public function, CLI invocation, HTTP handler, file-transform. Pin at the seam, not private helpers — a net over internals blocks exactly the refactor it exists to enable. (b) **Tame nondeterminism FIRST** — before any capture, find and control timestamps, UUIDs/random IDs, hash/dict ordering, float formatting, locale, concurrency interleaving: inject clocks/seeds where the seam allows, else normalize outputs (strip/replace volatile fields) in the capture harness. A net captured before taming flakes forever after. (c) **Choose inputs by branch, not bulk** — a handful of inputs that reach different branches and edges (empty, boundary, malformed, the weird-but-real production case) beats hundreds of near-duplicates; name why each input is in the net. (d) **Capture actual behavior as expected** — run the current code; its observed output becomes the assertion (inline expected values or approval/golden files — prefer small, reviewable goldens; a giant unreviewable snapshot is a rubber stamp, not a contract). Where current output looks WRONG, pin it anyway and flag it as a finding in the report — fixing it now changes behavior mid-netting and defeats the net; the fix is follow-up work after the net (and the change) land. Label the tests as characterization in their names or comments ("pins current behavior, not correctness") so a future reader doesn't mistake the pinned bug for a spec. (e) **Run green** — the whole net passes against unmodified current code. (f) **Prove the net — the mutation check, mandatory** — with a clean tree, introduce one deliberate behavior change at the seam's implementation (flip a comparison, change a boundary), run the net, require at least one failure; revert and PROVE restoration (`git diff --exit-code` on product code, net excluded), then require the net green again. A net never seen to fail is decoration. Repeat for 2–3 distinct mutations when the seam has distinct behavior regions. Never commit a mutation; restore on every exit path.
5. **Output and handover.** The committed net (tests + any goldens + capture harness), plus a short handover: the seam pinned, the inputs and why, nondeterminism controls applied, pinned-bug findings flagged for follow-up, the mutations that proved the net and what each caught, and the honest boundary — the net detects changes in the behaviors it pins, nothing more; no "behavior fully covered" claim, ever.
6. **Modes and scope.** One seam per run; pointed at a whole legacy module, pin the seam the imminent change will cross and say what was left unpinned. The skill authors tests only — it never performs the refactor/upgrade it enables (hand to `simplify-code`, `dependency-upgrade`, or the change's own lane).
7. **Fences.** vs `tdd` (new behavior, red-first, expectations from an independent source — state the inversion and why both are right: tdd's rule guards correctness claims for new code; characterization makes no correctness claim at all, so deriving expectations from the code is not the tautology tdd forbids — it is the point; a characterization test asserts "unchanged", not "correct"). vs `test-trust-audit` (when available: audits an existing suite's honesty; this authors a net where no suite exists). vs `verify`/`behavior-smoke-test` (one-off proof of a change; this leaves a durable net). vs `acceptance-map` (maps intended behavior from a spec; this pins actual behavior from execution).
8. **Done when.** Seam named; nondeterminism dispositioned before capture; every input justified; net green on unmodified code; ≥1 deliberate mutation observed to fail the net, restoration proven, net green again; pinned bugs flagged as findings; handover states the honest boundary; no product-code change survives; nothing pushed.
9. **Build-and-prune note.** Portable to every repo with legacy code; the offload is the full weave-tame-capture-prove procedure on one token. First-to-prune on mis-fire. Failure shapes: pinning internals (the net becomes the obstacle), goldens bloating into rubber stamps, or the mutation proof quietly skipped — each is drift from net to decoration.

### Step 3 — Validate structurally

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/characterization-tests
git diff --check
```

### Step 4 — Link and verify

```bash
scripts/claude-skills-sync.sh --link characterization-tests
scripts/claude-skills-sync.sh --check
```

Both exit 0.

### Step 5 — Behavior smoke test

Fixture in the scratchpad (never the repo): a small Python module `pricing.py` with an untested function containing a branch (say, tiered discounts), a `datetime.now()` call affecting output, and one subtle bug (e.g. `>=` where spec-sense says `>`). No tests. Spawn one fresh subagent with the new SKILL.md as active guidance and the task: "We need to upgrade this service's Python version and clean up pricing.py, but it has no tests and we can't break current behavior. Get us to where the cleanup is safe to start." Grade five behaviors: (1) pinned the public function as the seam, not internals; (2) handled `datetime.now()` BEFORE capturing (injection or normalization); (3) captured expected values by running current code, and pinned the buggy `>=` behavior while flagging it as a finding rather than fixing it; (4) ran a deliberate mutation, showed the net fail, restored with proof, net green again; (5) handover claimed only change-detection on pinned behaviors, no coverage certificate, and did not start the cleanup itself. 4/5 → proceed; one tighten-and-rerun; else stop at branch and report. `trash` the fixture after.

### Step 6 — Commit and land

```bash
git add skills/characterization-tests
git commit -m "feat: add characterization-tests skill (Era-62 review Band A, move #3)"
git checkout main && git merge --ff-only feature/characterization-tests
git status --short --branch
```

No push. No ledger entry.

## Edge cases a weaker model would miss

- **The tdd tension is real and must be named in the skill text.** `skills/tdd/tests.md` (updated 2026-07-09) forbids expected values derived from the code under test. A naive reading makes characterization tests forbidden. The resolution belongs IN the new skill's fence: characterization asserts "unchanged", never "correct", so the current code is the legitimate source for a change-detector — and the tests must be labeled so nobody later reads a pinned bug as a spec. If the fence is missing, the two skills contradict and a future roster review will flag it.
- **Pin bugs, flag bugs, never fix mid-netting.** The eager move is fixing the obvious bug while writing its test — which changes behavior exactly when the point is to freeze it. Fix-after-net-lands is the discipline; the flag is the deliverable.
- **Nondeterminism before capture, not after.** Capturing first and patching flaky assertions afterward normalizes garbage into the goldens; the taming pass is ordered before first capture in the skill's shape, and the order is load-bearing.
- **The net must be seen to fail.** A green-only net is indistinguishable from assertion-free tests (exactly what plan #4's audit flags). The mutation proof with per-site proven restoration (`git diff --exit-code` scoped to product code — the net files legitimately differ) is mandatory, not garnish.
- **Seam altitude.** Pinning private helpers freezes the implementation and blocks the refactor; the skill must say pin the boundary the change preserves. This is the #1 way characterization nets fail in practice.
- **Goldens are reviewed artifacts.** Small, named, diffable golden files; a 5,000-line snapshot is a rubber stamp (consistent with test-trust-audit's finding class, if it exists by then).
- **Smoke fixture hygiene**: scratchpad only, pytest available (`uv run pytest` per house Python stack), trashed after.
- **Consumers are routing targets, not dependencies**: `simplify-code` and `dependency-upgrade` get named as the lanes this skill precedes; do not edit them to add reciprocal edges in this plan (a fold decision for a later pass, not a build-time default).

## Acceptance criteria

1. `skills/characterization-tests/SKILL.md` on `main`; frontmatter parses; description quoted, matches Step 2, and contains the phrase "Pins current behavior, not correctness".
2. `quick_validate.py` passes; `git diff --check` clean; `claude-skills-sync.sh --check` exits 0 with the new symlink present.
3. Body contains: seam-not-internals rule; nondeterminism-before-capture ordering; pin-and-flag bug rule; mandatory mutation proof with `git diff --exit-code` restoration scoped to product code; a tdd fence that names and resolves the inversion; handover with an honest no-certificate boundary; build-and-prune note with the three failure shapes.
4. Grep guards: `grep -c 'git diff --exit-code' skills/characterization-tests/SKILL.md` ≥ 1; `grep -ci 'not correctness' skills/characterization-tests/SKILL.md` ≥ 2 (description + body); `grep -in 'fully covered\|full coverage' skills/characterization-tests/SKILL.md` hits only in never-claim-this context.
5. Smoke test: 5 behaviors, ≥4 passed, fresh context, fixture trashed.
6. Landed via `--ff-only`; tree clean; nothing pushed; no ledger entry.

## Out of scope

Performing the refactor/upgrade; fixing pinned bugs; editing `tdd`, `simplify-code`, or `dependency-upgrade`; mutation-testing frameworks; publishing.
