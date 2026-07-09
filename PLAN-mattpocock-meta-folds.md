# PLAN: Land the two carried-forward mattpocock meta-folds

Rank: 3 of 5. The Era-84 re-adoption closed with two roadmap recommendations-of-record explicitly un-actioned (named in the throughline Frontier and verified still absent on disk on 2026-07-09): the tautological-test anti-pattern → `tdd`, and the Negation/positive-prompting lens → `writing-principles`. Both were adversarially verified in the 38-skill roadmap evaluation (`docs/plans/2026-07-08-mattpocock-skills-extraction-roadmap.md`, items at lines ~42–48 and ~115–123); the first is HIGH confidence, the second MEDIUM-HIGH with a wording caution this plan resolves. Both are folds of third-party material → each is a charter case-(d) event with a one-line ledger entry at landing.

## Goal

Fold two upstream disciplines into their first-party owners, each proven by a cheap behavior forward-test, each recorded with a one-line case-(d) ledger entry.

1. Tautological tests (a test whose assertion recomputes the expected value the way the code does passes by construction) → `skills/tdd/tests.md` + a one-line peer mention in `skills/tdd/SKILL.md`.
2. Negation (steering by prohibition drags the forbidden behavior into context; prompt the positive instead) → a 9th Challenge-Order lens in `skills/writing-principles/SKILL.md`, worded to exempt routing non-use boundaries and hard guardrails.

## Ground rules (repo invariants — do not skip)

- Branch first (`feature/roadmap-meta-folds`); hook blocks `main` edits. Never `rm`; use `trash`. Markdown one logical line per bullet.
- Both target skills live in `skills/` (dual-runtime, served in place). They are NOT plugin-distributed: no version bump, no CHANGELOG, no Codex republish, no mirror step. A weaker model pattern-matching on Era-84's publish trains would wrongly run one here.
- The ledger (`docs/agents/contract-decisions.md`) is append-only: add new entries at the end of the Decisions list; never rewrite settled entries.
- Fold the CONCEPT, not the donor's packaging (the roadmap's explicit instruction: "Fold the *concept*, not the glossary"). No "_Avoid_:" alias lines, no "leading word" jargon, no glossary format.
- Upstream is pinned: the donor checkout is `/Users/jp/scratch-workspace/mattpocock-skills` and must be at commit `d574778f94cf620fcc8ce741584093bc650a61d3`. Do not pull/update it. Do not chase upstream past `d574778` (a settled Era-84 boundary).

## Exact files to touch

1. `skills/tdd/tests.md` — add a Tautological-tests block to `## Bad Tests` and one red-flag bullet.
2. `skills/tdd/SKILL.md` — one peer sentence in the Philosophy section's "Bad tests" paragraph.
3. `skills/writing-principles/SKILL.md` — add lens 9 to `## Challenge Order`.
4. `docs/agents/contract-decisions.md` — two appended one-line entries.

Read-only: donor files `skills/engineering/tdd/tests.md` (ll. ~63–77), `skills/engineering/tdd/SKILL.md` (l. ~29), `skills/productivity/writing-great-skills/GLOSSARY.md` (ll. ~161–165) under the scratch checkout; `docs/agents/charter.md`; `skills/agent-facing-design/SKILL.md`.

## Steps, in order

### Step 1 — branch, pin check, absence re-verification

```bash
cd /Users/jp/.agents && git status --short --branch
git checkout -b feature/roadmap-meta-folds
git -C /Users/jp/scratch-workspace/mattpocock-skills rev-parse HEAD   # must print d574778f94cf620fcc8ce741584093bc650a61d3
grep -riE 'tautolog|by construction|recompute' skills/tdd/            # must return nothing
grep -riE 'negation|prohibition|elephant' skills/writing-principles/  # must return nothing
grep -c '^[0-9]\.' skills/writing-principles/SKILL.md                 # sanity: Challenge Order currently has exactly 8 numbered lenses (verify by reading the section)
```

If any absence check hits, STOP — the fold may have landed since this plan was written; report instead of double-folding.

### Step 2 — charter pre-check (do not skip, do not over-do)

Read `docs/agents/charter.md` (Reversibility Class, Admission, Decision Record). Both folds are case-(d) "fate of third-party contract material": gated regardless of packaging, so each needs the Admission frame answered and a ledger entry — but the answers are already established by the roadmap's adversarial verification, so this step is a re-confirmation, not a fresh investigation. The frame, answered:

- Work owned: `tdd` owns test-quality discipline (tests.md is its bad-test catalog); `writing-principles` owns instruction-prose challenge lenses. Each fold lands inside its owner — no new lane, One-Owner clean.
- What lighter context wouldn't prevent: the tautological failure mode is orthogonal to the implementation-coupling anti-pattern tests.md already covers (a by-construction-passing test survives every existing red flag); the Negation discipline appears nowhere first-party (the 8 existing lenses cover justification, clarity, scope, proof, conflict, duplication — none covers prohibition-vs-positive phrasing).
- House standards: both land as house-shaped prose in the owner's existing format (Step 3/4 texts below).
- Neither fold trips always-loaded, unattended-fire, or irreversible-tool triggers.

### Step 3 — fold 1: tautological tests → `tdd`

In `skills/tdd/tests.md`, `## Bad Tests` currently has one named block (`**Implementation-detail tests**: Coupled to internal structure.`) followed by a `Red flags:` list and a bypasses-interface example pair. Insert a new block AFTER the implementation-detail example block and BEFORE `Red flags:`:

```markdown
**Tautological tests**: The assertion recomputes the expected value the way the code computes it, so the test passes by construction and can never disagree with the code.

​```typescript
// BAD: Expected value is recomputed the way the code computes it
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: Expected value is an independent, known literal
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
​```

Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec. A snapshot derived by hand the same way the code works, or a constant asserted equal to itself, is the same defect in disguise.
```

(Strip the zero-width characters guarding the inner fences above; write real triple-backtick fences.)

Then add one bullet to the existing `Red flags:` list: `- Expected value recomputed by the same algorithm the code uses (passes by construction)`.

In `skills/tdd/SKILL.md`, the Philosophy section has a `**Bad tests**` paragraph covering implementation coupling. Append one peer sentence to that paragraph (keep its voice): `A second failure mode is the tautological test: the assertion recomputes the expected value the same way the code does, so it passes by construction — expected values must come from an independent source of truth (a known literal, a worked example, the spec).`

### Step 4 — fold 2: Negation lens → `writing-principles`

First run the `agent-facing-design` gate: this fold ADDS an obligation (a new challenge lens future agents must apply), which is exactly the gate's trigger. Read `skills/agent-facing-design/SKILL.md` and check the fold against it. Expected verdict, which the ledger entry must record in your own confirmed words: context/lens addition, no machinery — no new field, score, classifier, or workflow stage; it extends an existing scan list in the owner skill. If your reading of the gate disagrees, STOP and report rather than landing.

Then, in `skills/writing-principles/SKILL.md` `## Challenge Order`, the list currently ends at lens 8 (**Duplicated**). Append lens 9 (match the exact formatting of lenses 1–8 — bold name, colon, one logical line):

```markdown
9. **Negated**: the instruction steers by prohibition where a positive instruction would do the work — naming the forbidden behavior drags it into context and makes it more available, not less. Rewrite to state the target behavior; keep a prohibition only as a hard guardrail you cannot phrase positively, and pair it with its positive target. Routing non-use boundaries ("Do not use for...") in descriptions are exempt: they are selection contracts, not behavior steering.
```

Wording constraints (these resolve the roadmap's "needs careful wording" caution — do not weaken them):

- The exemption for `Do not use for...` routing boundaries is mandatory. The house DELIBERATELY uses non-use boundaries in every skill description; a lens without this carve-out would order agents to strip them, which is a self-inflicted misroute factory.
- The hard-guardrail carve-out is mandatory: prohibitions like "never `rm`" or "never commit on `main`" are safety floors that cannot be phrased positively without losing force; the lens directs pairing them with a positive target (e.g. "use `trash`"), not deleting them.
- Do not renumber, reorder, reword, or "improve" lenses 1–8 while in the file. `writing-principles` is under a methodology hold (Era 70: an obligation's value exceeds one pass; cheapest-origin look before deletion) — the fold adds, it must not restructure.

### Step 5 — behavior forward-tests (one per fold, cheap, subagent)

Fold 1 test: spawn a fresh subagent, give it the full updated `tests.md` framed as active guidance, plus: `Write jest tests for this function: export const cartTotal = (items) => items.reduce((s, i) => s + i.price * i.qty, 0);`. PASS = no test recomputes the expected value via a reduce/map over the inputs; expected values are literals or hand-worked constants. FAIL = any assertion derives `expected` with the same arithmetic shape as the implementation.

Fold 2 test: spawn a fresh subagent, give it the full updated `writing-principles` SKILL.md framed as active, plus this target doc to review: `## Team rules\n- Do not write verbose comments.\n- Never use print debugging.\n- Do not use for production incidents; use the incident runbook instead.` PASS = the review flags the first two rules under the Negated lens with positive rewrites offered, and does NOT flag the third (a routing non-use boundary). FAIL = third line flagged, or the first two missed.

If a test fails, tighten the folded wording that permitted it and re-run once. Report results honestly either way, including that these are obedience proxies, not field validation.

### Step 6 — ledger entries

Append two one-line entries to the END of the Decisions section in `docs/agents/contract-decisions.md` (before the `## Parks` heading), dated the day you land them. Drafts (adjust dates/commit hashes to reality; keep each to one logical line):

> - 2026-07-NN — tdd tautological-test fold (`skills/tdd/tests.md` + one peer sentence in `skills/tdd/SKILL.md`): folded the by-construction-passing-test anti-pattern from `mattpocock/skills:skills/engineering/tdd/{tests.md,SKILL.md}` @ `d574778` into the first-party bad-test catalog — the assertion must never recompute the expected value the way the code does; expected values come from an independent source of truth. Charter case-(d) fold into the already-ledgered tdd fork (the roadmap's Tier-1 #1, HIGH confidence, absence re-verified at landing); behavior forward-test passed (fresh subagent wrote literal-expected tests, no recomputation). Evidence: roadmap `docs/plans/2026-07-08-mattpocock-skills-extraction-roadmap.md` §Tier-1 #1, donor @ pin, this commit.

> - 2026-07-NN — writing-principles Negated lens fold (`skills/writing-principles/SKILL.md`, 9th Challenge-Order lens): folded the Negation/positive-prompting discipline from `mattpocock/skills:skills/productivity/writing-great-skills/GLOSSARY.md:161-165` @ `d574778` — steering by prohibition drags the forbidden behavior into context; prompt the positive, keep prohibitions only as hard guardrails paired with their positive target — worded with the mandatory exemption for routing non-use boundaries (the house's deliberate `Do not use for...` convention) per the roadmap's Tier-2 wording caution. Charter case-(d) (fate of third-party material into a first-party skill); routed through the `agent-facing-design` gate: context/lens, not machinery. Behavior forward-test passed (lens fired on two prohibition rules, exempted the routing boundary). Evidence: roadmap §Tier-2, donor @ pin, this commit.

### Step 7 — validate and commit

```bash
python3 /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/tdd
python3 /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/writing-principles
scripts/check-library-integrity.sh   # structural sweep; all-PASS expected (frontmatter step may report SKIP only if the validator path vanished again — say so if so)
git diff --check
git add skills/tdd/tests.md skills/tdd/SKILL.md skills/writing-principles/SKILL.md docs/agents/contract-decisions.md
git commit -m "feat: fold tautological-test into tdd and Negated lens into writing-principles (roadmap carry-forwards) + case-(d) ledger entries"
```

Do not merge or push unless JP asks.

## Edge cases found during exploration (a weaker model would miss these)

- Frontmatter untouched in both skills: these are body-only folds, so descriptions, budgets, and routing stay as-is. Any description edit here is scope creep.
- `skills/tdd` was itself restored/rebased during Era-84's program — its current content is the governing first-party text. Fold into what's on disk now; do not consult or resurrect any older tdd variant.
- The donor's tautological bullet lives in a SKILL.md bullet list upstream, but first-party `tdd/SKILL.md` has no such list — its Philosophy section is prose paragraphs. The peer mention must be a sentence in the existing paragraph, not a new bullet list imported from upstream's structure.
- The Negation donor text is a glossary entry with `_Avoid_:` alias lines and a "leading word" vocabulary. None of that survives the fold — concept only, in Challenge-Order lens format.
- Naming the lens **Negated** (not "Negation") matches the grammatical shape of the existing eight (Unjustified, Vague, Unclear, Overbuilt, Unbounded, False-proof, Conflicting, Duplicated).
- Deep irony hazard: the lens itself must not be worded as a pure prohibition. The draft above leads with the failure description and the positive cure ("Rewrite to state the target behavior") — keep that shape if you adjust wording.
- The scratch checkout is disposable third-party material OUTSIDE the environment (Extraction's remove-the-original does not bind it — established in the Era-84 ledger entry). Do not copy it anywhere, do not delete it, do not treat its presence as a defect.
- If `check-library-integrity.sh` flags anything unrelated to your two skills, report it; do not fix drive-by findings in this branch.

## Acceptance criteria (verify each; do not claim done without output)

1. Pin check printed `d574778f94cf620fcc8ce741584093bc650a61d3`; both absence greps were empty BEFORE editing and hit exactly the new text AFTER (`grep -ri tautolog skills/tdd/` → 2 files; `grep -ri 'Negated' skills/writing-principles/SKILL.md` → 1 hit in Challenge Order).
2. `writing-principles` Challenge Order has exactly 9 lenses; lenses 1–8 byte-unchanged (`git diff` shows only additions in that section).
3. Both forward-tests run with PASS evidence quoted in the report (or an honest FAIL→fix→re-run trail).
4. Ledger gains exactly two appended entries, each one logical line, each naming donor@pin, charter class, gate verdict (fold 2), test result, and evidence pointers; no existing ledger line modified.
5. quick_validate passes on both skills (or unavailability reported with manual parse); `check-library-integrity.sh` structural checks pass; `git diff --check` clean.
6. One commit on `feature/roadmap-meta-folds` touching exactly the four intended files; no version bumps, no plugin/publish artifacts in the diff.
