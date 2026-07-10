# PLAN: Build the `money-decimal` skill

Rank: #4 of 5. Fourth item in the Era-62 factory queue: the exact-decimal correctness domain, whose footguns (binary float for money, hardcoded cents-per-unit, penny-losing splits) are severe, well-cataloged, and invisible to happy-path tests.

## Goal

Create `skills/money-decimal/` — a dual-runtime skill that designs or vets how code represents and computes money and other exact decimal quantities: identify the stack's decimal facilities first, choose the representation (integer minor units or a decimal type — never binary float), make the currency exponent and the rounding mode explicit policy rather than defaults, keep allocation/splitting sum-preserving, guard the serialization and database boundaries where floats sneak back in, and prove it with an executed arithmetic table where a runtime exists, honestly marked authored-not-executed where none does.

Authority: the frozen Era-62 review (`docs/reviews/2026-07-01-skill-library-capability-growth-review.md`, Opening C, §9 move 5) — `money-decimal` is the factory queue's fourth item ("rounding/precision"). Build-and-prune: NOT a charter event, NO ledger entry (Era-85/86 precedent).

## Files to touch

- CREATE: `skills/money-decimal/SKILL.md` (single file; no `agents/openai.yaml`, no `references/`).
- RUN (not edit): `scripts/claude-skills-sync.sh`.
- READ ONLY: `skills/regex-craft/SKILL.md` (the mold), `skills/injection-safe-inputs/SKILL.md` (freshest sibling), `skills/agent-facing-design/SKILL.md`, `skills/skill-ux-design/SKILL.md`, `AGENTS.md` (Skill Editing + Validation Ladder).

## House rules (apply throughout)

- Branch first: `git checkout -b feature/money-decimal` (a hook blocks edits on `main`).
- Never `rm`; use `trash`. Never push; no PRs; do not touch `plugins/`, the Codex cache, or the mirror.
- Markdown: one logical line per paragraph/bullet. Description has colons → double-quote it.
- Name check: `money-decimal` collides with no Codex-bundled (`openai-docs`, `skill-creator`, `skill-installer`, `plugin-creator`, `imagegen`, `pdf`, `doc`, `codex-primary-runtime`) or Claude-bundled (`code-review`, `debug`, `loop`, `claude-api`, `run`, `verify`, `security-review`) name.
- Dual-runtime tokens: `/money-decimal` or `$money-decimal`.

## Implementation order

### Step 1 — Read the mold and the gates

Read `skills/regex-craft/SKILL.md` and `skills/injection-safe-inputs/SKILL.md` end to end; then the two gates and AGENTS.md Skill Editing rules. Mirror the shared skeleton: summary+invocation → owned job → mixed-skill bars → shape → prove it → modes and scope → proof boundary → fences → done when → build-and-prune note.

### Step 2 — Write `skills/money-decimal/SKILL.md`

Use this description verbatim (quoted):

```yaml
---
name: money-decimal
description: "Use when designing or vetting how code represents and computes money or other exact decimal quantities — prices, totals, tax, discounts, interest, currency conversion, or splitting amounts: choose the representation (integer minor units or a decimal type, never binary float), make the currency exponent and rounding mode explicit policy, keep allocation sum-preserving, guard the serialization and database boundaries, and prove it with an executed arithmetic table. Not for float tolerance in scientific/ML code (approximation is correct there), general numeric performance, or accounting-product feature design."
---
```

Body requirements, section by section (real prose in the house voice; do not copy sibling sentences):

1. **Summary + invocation.** A forcing pass over one codebase area's money/decimal handling; picks the representation, makes rounding a policy, and proves the arithmetic at the boundaries; advisory-until-asked. `/money-decimal` or `$money-decimal`.
2. **The owned job.** No neighbor owns it: `diagnose` hunts an unknown cause (here the hazard class is known — a `$1,234.5600000001` on an invoice is not mysterious); `time-handling` (if present) is the sibling correctness domain for a different value class; `injection-safe-inputs` guards content at a trust boundary, not arithmetic; `implementation-review` (when available) needs a spec plus a diff. Value framing: money bugs are trust-destroying and often regulatory (a rounding mode is sometimes law), they accumulate silently across thousands of transactions, and the fix after data has been written is a migration — the human is spared holding the representation/exponent/rounding/allocation catalog in mind and auditing that the boundary cases actually ran.
3. **Mixed skill — bar per part.** Firm (trust): the identify-the-facilities gate, the never-binary-float rule, the exponent-from-currency-data rule, the rounding-as-explicit-policy rule, the sum-preservation requirement on splits, the executed arithmetic table with both honest states, the scoped verdict vocabulary. Provoked (judgment): which representation fits THIS stack and team (minor-units integers vs a decimal type is a real trade), where rounding must happen for THIS domain's rules (per line or on the total is a business/regulatory decision, not a preference), which boundaries this data actually crosses — forcing questions, never a template.
4. **Shape — the forcing pass**, in order: (a) **Identify the stack's decimal facilities FIRST** (the identify-the-engine analogue — required): Python has `Decimal` (with a context and default `ROUND_HALF_EVEN`); JavaScript has NO built-in decimal — `Number` is binary float64, so money is integer minor units (or `BigInt`, or a vetted decimal library); Java has `BigDecimal` (where `new BigDecimal(0.1)` is already poisoned — construct from `String` or use `valueOf`); the database has `NUMERIC`/`DECIMAL` (exact) vs `FLOAT`/`REAL`/`DOUBLE` (not) — and the ORM's default column mapping can silently choose float; JSON has only one number type, which most parsers read as float64 BEFORE application code sees it. The same design flips on the stack — verify on the actual versions, never assume. (b) **Choose the representation:** integer minor units (cents) or the stack's exact decimal type; binary float is never the answer for money — `0.1 + 0.2 ≠ 0.3`, and a stored `0.615` is actually `0.61499…` so it rounds "wrong" before any rounding-mode discussion begins. State where the representation is enforced (constructors/types at the edges, not vigilance). (c) **The currency exponent is data, not a constant.** Minor-units-per-major-unit is NOT always 100: JPY has 0 decimal places (a hardcoded `/100` inflates yen 100×), BHD/KWD/TND have 3, and the exponent must come from currency metadata (ISO 4217), not from an assumption baked into a helper. Any `* 100` or `/ 100` literal near money is a finding. (d) **Rounding is an explicit policy with a named mode and a named place.** The mode (half-up retail intuition, half-even/banker's for bias-free accumulation, floor/ceiling meaning in-whose-favor) is a business/regulatory decision to be looked up or asked, never left to the language default — and the defaults differ across stacks (Python `Decimal` and IEEE default to half-even; many devs assume half-up). The place matters as much: tax per line item vs on the subtotal produces different legal totals — pick one, cite why, and round as late as possible with full-precision intermediates. (e) **Allocation must be sum-preserving.** Splitting $100.00 three ways, distributing a discount across line items, or slicing installments must neither create nor destroy a cent: naive per-share rounding drifts; the largest-remainder / distribute-the-remainder pattern (allocate the floor, hand out the leftover cents deterministically) is the named fix, and "who gets the extra cent" is a stated rule, not an accident. (f) **Currency safety:** an amount without its currency is a bug waiting to add USD to EUR — carry currency with amount (a Money value or a convention enforced at boundaries); conversion is a business operation with a rate, a timestamp, and a rounding step, never a cast. (g) **Guard the boundaries:** DB columns `NUMERIC(precision, scale)` sized to the domain (and the ORM mapping checked); JSON APIs carry money as a string or as integer minor units — a JSON number goes through float64 in most consumers; user input parsed with locale awareness (`1.234,56`) and validated at the edge; display formatting is a locale concern separate from storage.
5. **Prove it — the executed arithmetic table.** Rows keyed to the real stack, run where a runtime exists: the float demonstration in the repo's own language (`0.1 + 0.2` and the `2.675`/`0.615`-style two-place rounding surprise) next to the exact-type versions; a three-way split of a prime-cent amount summing exactly to the original; a JPY (exponent-0) amount surviving the minor-units path without a 100× error; a round-trip through the JSON/DB boundary preserving exactness; one rounding-mode case where half-up and half-even visibly differ. Two honest states per row set: **executed** (a scratch script in the repo's language is enough; report observed results) or **authored, not executed** (exact run instructions; never claim it ran).
6. **Verdict vocabulary.** Exactly one of: **exact-as-proven** (scoped to the rows run), **designed-not-yet-proven**, **gap-found-because** (a float in the money path, a hardcoded exponent, a sum-breaking split, an unguarded boundary). Never "financially correct" or "precise" unqualified; the verdict never outruns the table.
7. **Modes and scope.** Applied vs advisory follows the invocation. One area: pointed at a whole app, narrow to the named or riskiest money path (checkout, invoicing, payouts) and say so.
8. **Proof boundary (the inherited floor).** Never assert an arithmetic result or a library/DB behavior you did not run — the float surprises are exactly the claims that must be executed, not recalled; bound the residual (e.g., "table executed on Python 3.12 Decimal + Postgres NUMERIC; residual: the React display layer's parsing unverified").
9. **Fences.** vs scientific/ML float use (tolerance and approximation are CORRECT there — this skill is for quantities where exactness is the contract; do not evangelize Decimal into numerics code); vs `diagnose` (unknown cause vs known class); vs `time-handling` (if present: the sibling domain — interest *accrual over periods* touches both; the date arithmetic is its job, the rounding of the resulting amount is this one's); vs accounting-product design (ledgers, double-entry, revenue recognition — product architecture, not representation correctness); vs `migration-safety` (executing the float→NUMERIC column migration this skill recommends).
10. **Done when.** Checklist mirroring the shape: facilities identified and verified; representation chosen and enforced at the edges; exponent sourced from currency data with no bare `100` literals; rounding mode AND place stated as cited policy; every split sum-preserving with the extra-cent rule stated; currency carried with amount; DB/JSON/input boundaries guarded; table delivered with honest per-row-set labels; one scoped verdict; advisory-until-asked held.
11. **Build-and-prune note.** Thin in this authoring repo; portable to every repo that touches prices, billing, payouts, or quantities with exactness contracts. First-to-prune on observed mis-fire. Failure shapes: collapsing into a one-line "use Decimal" reflex (fold signal — the exponent/rounding/allocation content is the actual job), or accreting a per-currency/per-locale formatting encyclopedia (drift, not the job).

### Step 3 — Validate structurally

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/money-decimal
git diff --check
python3 -c "import yaml; d=yaml.safe_load(open('skills/money-decimal/SKILL.md').read().split('---')[1]); print(d['name'], len(d['description'].split()))"
```

Then prove the description character-exact against this plan's yaml block (same comparison snippet as plan #1, paths substituted). Only the documented "unexpected key" complaint is waivable; expect zero complaints.

### Step 4 — Link and verify delivery

```bash
scripts/claude-skills-sync.sh --link money-decimal
scripts/claude-skills-sync.sh --check
```

Both must exit 0.

### Step 5 — Behavior smoke test (forward test)

ONE fresh subagent; prompt = the full new `SKILL.md` as active guidance plus this scenario verbatim (no skill vocabulary): "Our invoicing app is Python + Postgres with a JSON API consumed by a React frontend. Customers are seeing totals like $1,234.5600000001 on invoices, and one customer who pays in Japanese yen was charged 100 times too much. Invoices have per-line percentage discounts, and customers can pay in up to 4 installments. Work out how we should handle amounts before we add more billing features." Grade against five pre-named behaviors: (1) named binary float as the cause of the trailing-digits total and moved the money path to `Decimal`/integer-minor-units, enforced at the edges (not "round for display"); (2) attributed the yen bug to a hardcoded two-decimal assumption and sourced the exponent from currency metadata instead; (3) made the rounding mode and the rounding place (per-line vs subtotal for the percentage discounts) an explicit, cited policy decision rather than the language default; (4) made the 4-installment split sum-preserving with a deterministic extra-cent rule (remainder distribution), not independent per-installment rounding; (5) guarded the boundaries — Postgres `NUMERIC` (not float) and JSON money as string or minor-units integer with the float64-parser hazard named — and delivered an arithmetic table with at least one row actually executed in Python (or all rows honestly labeled authored-not-executed), plus a scoped verdict. Record pass/fail per behavior. 4/5 → proceed; below → tighten wording once and re-run; still below → STOP at the committed branch and report honestly.

### Step 6 — Commit and land

```bash
git add skills/money-decimal
git commit -m "feat: add money-decimal skill (Era-62 review Opening C, factory move #3)"
git checkout main && git merge --ff-only feature/money-decimal
git branch -d feature/money-decimal
git status --short --branch
```

Do NOT push. Do NOT add a ledger entry.

## Edge cases a weaker model would miss

- **The currency exponent is the sleeper footgun.** Everyone knows "don't use float for money"; far fewer know minor units are not universally 2 (JPY 0, BHD 3) — the yen-×100 bug in the smoke scenario is real-world common. The skill must make exponent-from-currency-data a firm rule and flag bare `100` literals.
- **The float is often poisoned before your code runs:** a JSON number passes through the parser's float64 on the way in, and `new BigDecimal(0.1)`-style constructors capture the poison exactly. Exactness must be guarded at the boundary, not just in the arithmetic layer.
- **Rounding mode defaults disagree with human intuition:** Python `Decimal` defaults to half-even, so `Decimal('2.5').quantize(Decimal('1'))` is `2`, not `3`. The skill must say the mode is a policy to look up/ask, and the proof table must include a row where modes visibly differ.
- **Rounding place is a business decision:** per-line tax vs subtotal tax legitimately differ; a weaker author "fixes" one to match the other without asking which the spec/regulation requires. The skill forces the question instead of answering it.
- **Sum-preservation needs an algorithm, not care:** independently rounding each share of a split systematically drifts; largest-remainder distribution and a deterministic who-gets-the-extra-cent rule are the named pattern.
- **Scientific/ML code is the mirror-image boundary:** recommending Decimal there is wrong (performance and semantics) — the fence must protect both directions, or the skill misfires on numerics repos.
- **Executed means executed:** the float demonstrations are one-liner scripts in the repo's language; the plan's proof discipline forbids reciting them from memory — the executed table is the skill's evidentiary spine.
- **The smoke scenario must not teach the test** — it never says "float", "Decimal", "rounding mode", "minor units", or "exponent". Use it verbatim.
- **quick_validate:** only the documented "unexpected key" complaint is waivable; never delete a documented-valid field to satisfy it.

## Acceptance criteria

1. `skills/money-decimal/SKILL.md` exists on `main`; frontmatter parses; description double-quoted and character-exact to this plan's yaml block.
2. `quick_validate.py skills/money-decimal` passes clean; `git diff --check` clean.
3. `scripts/claude-skills-sync.sh --check` exits 0; `ls -la ~/.claude/skills/money-decimal` shows a symlink into this repo.
4. The body contains: an identify-the-facilities-first gate; the never-binary-float rule with boundary enforcement; the exponent-from-currency-data rule; rounding mode AND place as explicit policy; sum-preserving allocation with a deterministic remainder rule; currency-carried-with-amount; DB/JSON/input boundary guards; both table states; a three-term verdict vocabulary; Done-when; Build-and-prune with fold signal + encyclopedia drift.
5. Grep guards: `grep -ci 'minor unit' skills/money-decimal/SKILL.md` ≥ 2; `grep -ci 'JPY\|yen' skills/money-decimal/SKILL.md` ≥ 1; `grep -ci 'remainder' skills/money-decimal/SKILL.md` ≥ 2; `grep -ci 'half-even' skills/money-decimal/SKILL.md` ≥ 1; `grep -n 'rm ' skills/money-decimal/SKILL.md` returns nothing.
6. Smoke test recorded: 5 behaviors, ≥4 passed, scenario plan-verbatim, fresh context.
7. Landed via `--ff-only`; branch deleted; tree clean; nothing pushed; no ledger entry.

## Out of scope

Double-entry/ledger architecture; payment-provider integration; tax-law content beyond "the place of rounding is a cited decision"; currency-conversion rate sourcing; editing existing skills (including `time-handling` — its interest-accrual seam is one fence line here, nothing more); benchmarking; publishing.
