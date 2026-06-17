---
type: prereg-seal
experiment: judgment-trust test 4 — cut-then-use (recommendation → action → verification)
project: agents
branch: feature/test4-cut-then-use
base_commit: "4902cc8 (main; apparatus UNCHANGED)"
variant_before_sha256: "e7c3167ef9e05b8963946e8a4210475703079145c3faeff59f84d3b35591e0fa  (next-steps WITH the Pre-Final Checklist)"
variant_after_sha256: "22b6a74d27590b143db99a98db92232c57f4109a276937b930b689f97619a85c  (next-steps WITHOUT the Pre-Final Checklist — the cut)"
corpus_sha256: "473502bd5ee74d07e3f3e0f996c2103ea7d4789a4e21e9300642433b16861eea  (finding-sets.md)"
trapkey_sha256: "bbc8811eaf2235b08e59f73a2c2056166304533c526b55d455c94f1b376db5f3  (trap-key.md — sealed; not shown to runners or scorers)"
bar_provenance_sha256:
  - "70037a32d07b22029e9439ebd92b692d7b22d11a45693a9032ead3a9d6a38d98  agent-facing-design/SKILL.md (= test-5 seal bar-ON; unchanged)"
  - "7545f4ca3021403f1023240f100e060ef9775c46ed23cc93e9a31faeea5e0274  scrutinize-skill/SKILL.md (= test-5 seal bar-ON; unchanged)"
written_before: "any scored runner output or any scoring — committed BEFORE the run phase"
---

# Test 4 — cut-then-use — PREREG + SEAL (committed before any scored run)

The fourth item of the 5-test menu and the only one that closes the full loop
**recommendation → action → verification**: the bar recommends removing a piece of
substitutive structure, we *actually make the cut*, then we *use the cut skill* and
measure whether acting on the recommendation produced an at-least-as-good skill in
practice. Every prior test stopped at "the bar changes/【doesn't over-cut】reviews"; this
one asks whether a bar-recommended **cut**, once acted on, holds up in use.

## 0. What this tests, and the two competing theories

The whole testing arc found the apparatus **reshapes and almost never cuts** (test 5),
and the few cuts it did produce (the finding-cap) were **over-cuts two blind humans
reversed**. So acting on a bar cut is exactly the under-tested, higher-risk move. This
test adjudicates two theories that make opposite predictions about one real cut:

- **Substitutive-recap theory (the bar's claim):** a closing checklist whose every item
  merely restates an obligation already in the skill body is *substitutive* — it makes the
  agent perform the contract (tick boxes) instead of doing the work — and removing it costs
  nothing, because the obligations remain stated where the work happens.
- **Salience-reinforcement theory (the challenge):** restating obligations at the moment of
  finalization is not redundant; it catches omissions the buried-in-body obligations miss
  (especially the easily-forgotten *last* step), so removing it degrades compliance.

T4 settles which holds for this cut, empirically, with a sealed criterion and blind,
cross-model scoring. A clean win for the bar validates acting on its cuts; a regression is
direct evidence the bar's cut recommendations can be too aggressive in practice (and would
echo the arc's "over-cut is the only error mode" finding into the action loop).

## 1. The cut (single variable) and its provenance

**Skill:** `skills/next-steps/SKILL.md` (a judgment-class planning skill: turns findings
into a dependency-aware strategic plan).

**Cut:** remove the entire `## Pre-Final Checklist` section — one sentence enumerating eight
items to "verify before finalizing." Nothing else changes. The diff is 4 lines (the heading,
two blanks, the sentence); `git diff --check` clean.

**Provenance (why this is a bar-recommended cut, not a hand-picked one):** produced by a
**cold 48-skill discovery pass** (workflow `wf_1f336984-079`, run blind to all prior
adjudications), one agent per live skill applying the Two Kinds of Skill bar, then 3-lens
adversarial refutation of every surfaced candidate. Of 48 skills, exactly **two** surfaced any
CUT; `writing-principles` was **disqualified** (its duplicated ladder wants single-sourcing via
a pointer = reshape, and carries a unique obligation removal would drop); **`next-steps`
survived** (all 3 lenses → CUT, 0 regress). Independently confirmed by the orchestrator: every
one of the 8 checklist items restates an obligation already in the `Build` / `Output Sections`
body (source@29; mapped@28,34; nothing-invented@28; inferred-deps@38; phase-ordering@34-40;
critical-path-subclaims@52; parked@43,54; save-offer@48) — pure recap, **no unique obligation**,
the textbook "fixed section the agent fills to feel done." Never previously adjudicated. Full
record: `.agents/scratch/test4-run/discovery-provenance.json`.

That a 48-skill curated library yielded exactly one small recap-checklist cut is itself a
finding (the bar's cuts are rare and modest), and is reported as such regardless of verdict.

## 2. Variant lock (tamper-evident)

The only intended difference between arms is the presence of the checklist. Snapshots pinned
by SHA-256 (verify before the run):

```
e7c3167ef9e05b8963946e8a4210475703079145c3faeff59f84d3b35591e0fa  variants/before.md  (WITH checklist)
22b6a74d27590b143db99a98db92232c57f4109a276937b930b689f97619a85c  variants/after.md   (WITHOUT — the cut)
```

`diff before.md after.md` = the 4-line checklist deletion, nothing else.

## 3. Corpus (sealed)

Ten realistic, domain-varied inputs a user would hand to `/next-steps`
(`corpus/finding-sets.md`, sha256 `473502bd…`): FS1–FS7 are genuine multi-finding planning
inputs; FS8–FS10 are early-exit cases (too-vague / one-obvious-step / implementation-ready).
The corpus is **identical for both arms** and is not adversarial to the checklist — these are
ordinary inputs that exercise the plan-quality properties a good plan must satisfy. Passed a
**3-assessor blind realism + neutrality gate** (FS1–FS5, FS7 rated realism 5/neutral; FS6/FS8/
FS9/FS10 naturalized after the gate flagged telegraphing). The per-FS **trap-key** (which
property each input stresses + expected early-exit handling, sha256 `bbc8811e…`) is **sealed
and withheld** from runners and scorers.

## 4. Runner protocol (hermetic, blind)

- One run = the variant's full `SKILL.md` prepended as the operating contract, then a single
  finding-set, then the request to produce the plan (or to decline/redirect). Wrapper identical
  across arms; the ONLY difference is which variant contract is prepended.
- Runner model: **claude-opus-4-8** (the live runtime that actually uses the skill).
- The runner is **blind**: not told this is a test, not told which arm, not told a checklist
  exists or was removed.
- **10 finding-sets × 2 arms × 3 reps = 60 runs.** Outputs saved to `runs/`.

## 5. Scoring protocol (blind, cross-model, reasoning-over-label)

Each produced plan is scored against a neutral rubric, **blind to arm**: the scorer sees the
finding-set + the produced plan + the rubric, never the skill, the arm, the checklist, or that
this is an apparatus test. Plans are shuffled and provenance-stripped. Blinding-guard compliant
(`AGENTS.md` `## Blind Evaluations`): scorers are the ground-truth channel for "is the plan
good"; no apparatus state reaches them before they score.

Rubric (per plan):

- **Eight properties**, each scored `satisfied` / `violated` / `not_applicable`:
  P1 finding source handled (single source used, or multi-source ambiguity flagged, not silently
  merged); P2 every supplied finding mapped (none dropped); P3 nothing invented (no fabricated
  findings/deps/risks/parked items); P4 dependencies either grounded or explicitly marked
  inferred; P5 phase ordering valid (same-phase tasks parallelizable); P6 critical-path
  subclaims separated and scheduling-critical = "not claimed" when no durations supplied; P7
  parked items are real and carry a `revisit when` (no padding); P8 a save offer is included
  (non-early-exit plans only).
- **Holistic plan quality** 1–5 (would a competent strategist find this a sound, honest,
  useful plan?).
- **Early-exit correctness** (FS8/FS9/FS10 only): did it correctly decline/redirect rather than
  fabricate a plan? `correct` / `incorrect`.
- One line of reasoning per property judgment (reasoning-over-label: the reasoning governs).

Two scorer families, both blind:

- **Primary — blind Claude panel:** one blind scorer per plan; any plan where the Codex
  cross-check disagrees on ≥2 property calls or on the early-exit call is re-scored by a second
  blind Claude scorer (tie-break). Claude-side aggregates are primary.
- **Cross-model — Codex (gpt-5.5), de-biasing checker:** `codex exec --sandbox read-only
  --output-schema`, **all content inlined, tools forbidden** ("Do NOT read any files"), batched.
  Codex scores the same plans blind. Reported as an independent family; the verdict is
  **robust** only if both families agree on direction.

## 6. Pass criterion — "at-least-as-good" (sealed; no post-hoc rescue)

Denominators: 7 plan-type FS × 3 reps = **21 plan-type plans per arm**; 3 early-exit FS × 3
reps = 9 early-exit plans per arm. "Compliance rate" for a property = satisfied / applicable
within an arm.

The cut is **AT-LEAST-AS-GOOD** (validated) iff ALL hold (on the primary Claude family, with
the Codex family agreeing on direction):

1. **Overall non-inferiority:** WITHOUT-arm overall property-compliance ≥ WITHOUT < WITH only by
   ≤ 0.05 (i.e. `without ≥ with − 0.05`).
2. **No property collapse:** for every property, `without ≥ with − 0.15`. (≈ ≤ 3 plans of slack
   on 21; a larger per-property drop is a collapse.)
3. **Holistic non-inferiority:** mean holistic `without ≥ with − 0.3` (on the 1–5 scale).
4. **Early-exit non-inferiority:** WITHOUT handles ≥ as many early-exit cases correctly as WITH.

**REGRESSED** (the cut hurt) iff any of 1–4 fails in the regression direction **and** the effect
is corroborated (not a single-rep blip): same-signed on ≥2 of the 3 reps of the affected FS, or
agreed by both scorer families. Name the specific property/properties that regressed (P8 save-
offer is the a-priori most likely, being the literal last step a closing checklist reminds of).

**INCONCLUSIVE** iff the comparison cannot be scored (degenerate/unparseable runs, a property
with no applicable cases, or scorer-family disagreement on direction that a tie-break cannot
resolve). Note: both arms at ceiling is **not** inconclusive — it means the checklist added no
compliance value, which is AT-LEAST-AS-GOOD.

Total order, first match wins: INCONCLUSIVE → REGRESSED → AT-LEAST-AS-GOOD. INCONCLUSIVE and
REGRESSED are live, acceptable outcomes and must not be massaged into a pass. The in-remit
properties, rubric, scorer protocol, and these thresholds are fixed by this file.

## 7. Decision rule

- **AT-LEAST-AS-GOOD** → acting on the bar's cut is sound; the cut is a real improvement (lighter
  skill, same quality). Land the cut on `main` (fast-forward) pending the standard validation
  ladder; apparatus UNCHANGED (the bar was right).
- **REGRESSED** → acting on the bar's cut demonstrably hurt; **do not land** the cut; the bar's
  cut recommendation was too aggressive here — record it against the bar (the one case that would
  warrant reconsidering the cut-side of the apparatus). Per the menu, apparatus is changed only on
  a demonstrated regression, and only after a deliberate follow-up, not automatically.
- **INCONCLUSIVE** → report honestly (as test 5 was); the cut stays on-branch, unlanded, pending a
  better-powered re-run.

## 8. Honest limits (pre-stated)

- **n = 1 cut**, and a small one (a recap checklist) — the only clean cut a 48-skill curated
  library produced. The verdict speaks to *this* cut; generality to larger/structural cuts is not
  claimed.
- The runner and the primary scorer are both Claude (same-model); **Codex is the cross-model
  de-biasing arm**, not a human ground-truth arm. This test escapes authorship circularity (the
  cut came from a cold blind pass) but not fully same-model circularity on the *use* side.
- Plan-quality scoring of a planning skill is more objective than "is this critique better"
  (the 8 properties are concretely checkable), which is why a quantitative measure is admissible
  here where `skill-benchmark` refuses to number pure-judgment quality — but holistic quality
  remains a judgment call, reported with reasoning.
