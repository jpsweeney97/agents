# PLAN: Build the `test-trust-audit` skill

Rank: #4 of 5. Era-62 review §9 move #3 (test-safety pair, first half).

## Goal

Create `skills/test-trust-audit/` — a dual-runtime skill that sweeps an existing GREEN test suite for the ways green lies: skipped/xfail/quarantine accumulation, assertion-free and tautological tests, mocks asserting mocks, snapshot rubber-stamping, coverage-without-assertion — plus an optional, strictly-contained sampled mutation probe that checks whether the suite catches a deliberate behavior change. Output: an evidence-led findings list with file:line citations, no score, no trust certificate.

Authority: the frozen Era-62 review (`docs/reviews/2026-07-01-skill-library-capability-growth-review.md`, Band A) — "read-only sweep of an existing green suite for the ways green lies", §9 move #3. This matters beyond any one repo: the whole library's proof discipline leans on "green = evidence", and this is the skill that checks when that equation is a lie. Build-and-prune: attended, advisory, mutation probe is temporary-and-reverted → NOT a charter event, NO ledger entry.

## Files to touch

- CREATE: `skills/test-trust-audit/SKILL.md` (single file, minimal bundle).
- RUN: `scripts/claude-skills-sync.sh`.
- READ ONLY: `skills/regex-craft/SKILL.md` (mold), `skills/tdd/tests.md` (the tautological-test anti-pattern landed there 2026-07-09 — cross-reference its definition, do not restate it divergently), `skills/keep-green/SKILL.md` and `skills/tdd/SKILL.md` (fence targets), `skills/agent-facing-design/SKILL.md`, `skills/skill-ux-design/SKILL.md`, `AGENTS.md`.

## House rules (apply throughout)

- Branch first: `git checkout -b feature/test-trust-audit` (hook blocks edits on `main`).
- Never `rm`; use `trash`. Never push; no PRs; `plugins/`, cache, mirror untouched.
- One logical line per paragraph/bullet; quoted description.
- Dual-runtime tokens (`/test-trust-audit` or `$test-trust-audit`); availability-conditional routing for plugin/Claude-only neighbors.

## Implementation order

### Step 1 — Read the mold, the fences, and the tautological-test source

Read `regex-craft` (skeleton), then `skills/tdd/tests.md` and find its tautological-test block (a test passing by construction; expected values must come from an independent source of truth). The new skill DETECTS that pattern in existing suites; `tdd` prevents it when authoring. Same concept, two jobs — the audit skill should name the pattern consistently and point authoring-time prevention at `tdd`.

### Step 2 — Write `skills/test-trust-audit/SKILL.md`

Description, verbatim (quoted):

```yaml
---
name: test-trust-audit
description: "Use when asking whether a green test suite can be trusted — before leaning on it for a refactor, upgrade, or release: sweep for skipped and quarantined growth, assertion-free and tautological tests, mocks asserting mocks, rubber-stamped snapshots, and coverage that executes without checking, optionally probing a sample with deliberate mutations. Read-only findings with citations, no score, no certificate. Not for fixing failures (keep-green), authoring tests (tdd), or reviewing a diff (implementation-review)."
---
```

Body requirements:

1. **Summary + invocation.** The suite is green; this asks whether green means anything. Findings list, evidence-led, read-only by default. Invocation tokens.
2. **The owned job.** `keep-green` drives a broken suite back to green after your change — it never asks if green is honest; `tdd` authors new tests test-first; `implementation-review` reviews a change against a spec; a debt backlog is `tech-debt-scan`. Nobody audits the existing green suite's evidentiary value. Value: a hollow suite silently converts every future "tests pass" into a false proof — the cost lands exactly when someone trusts it (a refactor, an upgrade); the human is spared composing the hollow-green checklist and reading hundreds of tests.
3. **Mixed skill — bar per part.** Firm (trust): the finding classes swept every run, file:line evidence per finding, the mutation probe's containment protocol (below), the no-score/no-certificate close, read-only default. Provoked (judgment): whether a mock boundary is legitimate isolation or the test testing itself, whether a snapshot is a contract or a rubber stamp, which functions are load-bearing enough to earn a mutation sample.
4. **Shape — the sweep.** Finding classes, each with its detection route and its judgment question: (a) **Skip/quarantine drift** — count and age skipped/xfail/disabled tests (`skip`, `xfail`, `todo`, `.skip`, quarantine lists); a skip with no linked reason or an xfail that now passes is a finding. (b) **Assertion-free tests** — test bodies with no assertion reached, or asserting constants/truthiness of unconditional values; ran ≠ checked. (c) **Tautological tests** — expected value derived from the code under test (calling the same function to compute the expectation, re-asserting the mock's return); consistent with `tdd`'s definition: passing by construction, expectation not from an independent source of truth. (d) **Mocks asserting mocks** — the assertion inspects only mock state while every collaborator that would exercise real code is mocked; the test proves the mocking framework works. (e) **Snapshot rubber-stamping** — bulk snapshot-update commits (many snapshots changed in one commit with no source change review), giant snapshots nobody could review; git history is evidence here (`git log` on snapshot dirs). (f) **Coverage-without-assertion** — where coverage data exists, high-coverage files whose covering tests assert little; never compute coverage as the product — it is a pointer to where to read. (g) **Optional, opt-in: the sampled mutation probe** — see below.
5. **The mutation probe (contained).** Off by default; run when the user opts in AND the working tree is clean AND the test runner is confirmed. Protocol, stated as hard steps in the skill text: verify `git status --short` is clean before starting; pick 3–5 load-bearing, well-covered functions; for each, introduce ONE deliberate behavior mutation (flip a comparison, off-by-one a boundary, invert a branch); run only the covering tests (not the whole suite); record caught/survived; then restore and PROVE restoration with `git diff --exit-code` (or `git checkout -- <file>` then the proof) before touching the next site. A surviving mutation is a concrete finding naming the mutation and the tests that stayed green. Never commit a mutation; never leave one behind on any exit path, including test-runner failure; if restoration cannot be proven, say so as the first line of the report. Findings from the probe are SAMPLED — "3 of 5 sampled mutations survived", never "the suite catches N%".
6. **Output.** A findings list ordered by how badly each undermines trust, each finding: class, file:line, the evidence (the test body excerpt, the git log line, the surviving mutation), and one sentence on what it falsely proves. No score, no grade, no "trustworthy"/"untrustworthy" verdict — the close names what was swept, what was sampled, and what was not inspected (the no-certificate law: the suite's worst lie may be in the tests nobody read). Route fixes out: authoring fixes → `tdd`; per-finding tracker items → `/triage` (or `$triage`) where available.
7. **Modes and scope.** Default read-only static sweep; mutation probe opt-in. Scope: one suite or package per run; pointed at a monorepo, narrow and say so.
8. **Fences.** vs `keep-green` (a RED suite goes there; this skill takes green ones); vs `tdd` (prevention at authoring time; compose — findings hand fix-work there); vs `implementation-review` (spec+diff review of a change); vs `tech-debt-scan` (scored repo-wide backlog; this is one suite, evidence-led, unscored); vs coverage tooling (this reads what coverage points at; it never certifies a number).
9. **Done when.** All six static classes swept with the detection route named per class; every finding carries file:line evidence; probe (if opted-in) ran under the containment protocol with restoration proven; close names sweep boundaries and renders no certificate; nothing was fixed, committed, or pushed.
10. **Build-and-prune note.** Portable to every repo with a test suite; the offload is the complete hollow-green checklist plus the discipline of evidence-per-finding. First-to-prune on mis-fire. Failure shapes: drifting into a scored health grade (that is `tech-debt-scan`'s register), or the probe growing into a mutation-testing framework (use a real tool at that point and say so).

### Step 3 — Validate structurally

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/test-trust-audit
git diff --check
```

### Step 4 — Link and verify

```bash
scripts/claude-skills-sync.sh --link test-trust-audit
scripts/claude-skills-sync.sh --check
```

Both exit 0.

### Step 5 — Behavior smoke test

Build a tiny fixture in the scratchpad (NOT in the repo): a Python package with `calc.py` (two small functions) and `test_calc.py` containing five tests: one honest, one with no assertion, one asserting `calc.add(2,2) == calc.add(2,2)` (tautological), one `@pytest.mark.skip` with no reason, one asserting only on a `Mock` object's return. Confirm `pytest` is green on the fixture first. Then spawn one fresh subagent with the new SKILL.md as active guidance and the task: "Our tests are all passing, but before we refactor this package I want to know if the suite would actually catch anything. Take a look." Grade five behaviors: (1) flagged the assertion-free test; (2) flagged the tautological test and pointed authoring-time prevention at tdd; (3) flagged the reasonless skip and the mock-asserting-mock; (4) every finding cited file:line evidence; (5) close rendered NO trust score/certificate and offered routed next steps rather than fixing. 4/5 → proceed; one tighten-and-rerun; else stop at branch and report. Clean up the fixture with `trash`.

### Step 6 — Commit and land

```bash
git add skills/test-trust-audit
git commit -m "feat: add test-trust-audit skill (Era-62 review Band A, move #3)"
git checkout main && git merge --ff-only feature/test-trust-audit
git status --short --branch
```

No push. No ledger entry.

## Edge cases a weaker model would miss

- **The mutation probe is the dangerous part — contain it in the skill text, not just in practice.** It edits PRODUCT code on purpose. The containment protocol (clean tree precondition, one site at a time, restoration proven with `git diff --exit-code` per site, never committed, failure paths restore too) must be written as obligations in the SKILL.md; a skill that says "try a mutation" without the protocol will one day leave a flipped comparison in someone's working tree.
- **Read-only by default, and the probe is opt-in.** The description says read-only; the probe must therefore be explicitly opt-in in the body, or the description lies about the skill's side effects.
- **Coverage is a pointer, never the product.** A weaker author makes the skill compute a coverage number; the review's phrase is coverage-WITHOUT-assertion — coverage data only tells you where to read.
- **No certificate, sampled-and-said.** "The suite is sound" is exactly the lie this skill exists to catch — the close reports classes swept and samples run, and explicitly does not certify the rest (this is the library-wide no-certificate law; see `regex-craft`'s scoped verdict for the register).
- **Tautological-test single-sourcing.** `skills/tdd/tests.md` already defines the anti-pattern (landed 2026-07-09). Detect it consistently and route prevention to `tdd`; do not paste a rival definition that can drift.
- **Framework specificity vs encyclopedia drift.** Name a few skip/mocking anchors (pytest `skip`/`xfail`, jest `.skip`/`todo`, Go `t.Skip`) as examples of the class, not as an exhaustive per-framework reference — the mold's named drift applies.
- **xfail-that-passes is a distinct finding** (XPASS): the test was marked expected-to-fail and now passes silently — the mark is stale and hides signal.
- **Smoke-test fixture goes in the scratchpad, never the repo**, and gets `trash`ed after; a leftover fixture in `.agents` is a hygiene regression.

## Acceptance criteria

1. `skills/test-trust-audit/SKILL.md` on `main`; frontmatter parses; description quoted, matches Step 2.
2. `quick_validate.py` passes; `git diff --check` clean; `claude-skills-sync.sh --check` exits 0 with the new symlink present.
3. Body contains: six static finding classes each with a detection route; the mutation probe marked opt-in with the full containment protocol including `git diff --exit-code` restoration proof; file:line evidence obligation; a no-score/no-certificate close; fences for `keep-green`, `tdd`, `implementation-review`, `tech-debt-scan`; build-and-prune note with both failure shapes.
4. Grep guards: `grep -c 'git diff --exit-code' skills/test-trust-audit/SKILL.md` ≥ 1; `grep -ci 'opt-in' skills/test-trust-audit/SKILL.md` ≥ 1; `grep -in 'trust score\|health grade' skills/test-trust-audit/SKILL.md` hits only in never-do-this context.
5. Smoke test: fixture built in scratchpad, pytest green pre-audit, 5 behaviors graded, ≥4 passed, fixture trashed after.
6. Landed via `--ff-only`; tree clean; nothing pushed; no ledger entry.

## Out of scope

Fixing any finding; authoring tests (`tdd`, or plan #5's `characterization-tests`); running mutation-testing frameworks; scoring; editing existing skills; publishing.
