---
type: pre-registration
experiment: judgment-trust test 1 — foreign-material element-discrimination differential
project: agents
sealed_at: "2026-06-16 (committed before any reviewer run)"
bar_on_ref: main @ f048687 (review-family 0.3.10 — same lens apparatus as test 3)
bar_off_ref: 3eb0e74^ (8b9cfc1 — pre-lens baseline, single-variable; same as test 3)
primary_reviewer_model: claude-opus-4-8 (production reviewer; held fixed for test-3 comparability)
disposition_judge_model: gpt-5.5 / Codex (different family — reduces same-model scoring circularity)
secondary_reviewer_arm: gpt-5.5 / Codex (OPTIONAL, labeled robustness arm; see §9)
corpus_seal: SHA-256 of the 13 frozen anonymized files recorded in §3 (hermetic)
---

# Pre-Registration — test 1, foreign-material element-discrimination differential

**This file is sealed by its commit. It is written and committed BEFORE any reviewer is
run.** The results artifact will cite this file's commit SHA as proof the predictions and
element key preceded the data. Do not edit after the runs begin; record all outcomes in a
separate results artifact.

This is **test 1** of the 5-test apparatus menu (test 3, the home-corpus differential, PASSED
— `f048687`). Test 1 removes the **authorship confound**: the bar reviews skills the
library did not author. Design refined across a Claude 12-agent panel + a Codex 4-lens panel +
a Codex blind element-classification cross-check (all 2026-06-16; artifacts in
`.agents/scratch/test1-refine/`). Both model families converged on the redesign below.

## 1. What is being tested

The single variable is the same judgment-vs-trust **lens apparatus** as test 3 (the `## Two
Kinds of Skill` section in `agent-facing-design` + the bar-keyed step-3/severity rules in
`scrutinize-skill`). Bar-ON vs bar-OFF reviewer configs are **identical to test 3** (see
frontmatter refs). Only the **corpus** changed: home skills → **foreign material + 2 seeded
substitutive probes + 1 home-replication cell**.

The binding question test 3 raised and could not answer (authorship + same-model circularity):
**is the bar's push-to-cut organizing structure on judgment skills CORRECT (sharpening) or
OVER-CUTTING (mis-calibration)?** Test 1 attacks the authorship half on unfamiliar material.

**Key design change from test 3 (both panels, unanimous):** bar-OFF is **demoted from
"non-circular anchor" to a contrast arm**. Pass/fail rides on bar-ON vs a **sealed,
function-grounded, element-level key** (§4), scored at the element level by a **different-model
blind judge** (§5). bar-OFF only shows the bar's marginal effect, never ground truth.

## 2. Reviewer / judge protocol

- **Primary reviewer = Claude** (production reviewer), scrutinize-skill, bar-ON vs bar-OFF, each
  anonymized skill, **n = 3 reps per cell**. Held fixed to the production reviewer for
  single-variable comparability with test 3.
- **Disposition judge = Codex/gpt-5.5** (different family). For each **scored** element (neutral
  enumeration only — NOT its label or the predictions), extracts the reviewer's disposition from
  the review text: **CUT** (flagged as structure to remove/weaken), **DEFEND** (kept/endorsed),
  **SILENT** (not mentioned). Blind to condition (outputs labeled A/B at random) and to this key.
- **Form/substance coding.** Each CUT is tagged **form-keyed** ("it's a template/cap/list/section")
  vs **substance-keyed** ("it makes the choice for the agent because…"). **Only substance-keyed
  cuts count** toward the gates (a form-heuristic cut is logged, not scored as a real over-cut).
- **Disposition counts only at ≥2 of 3 reps agreement** (same target, same disposition). One-offs
  are logged as noise.

## 3. Frozen corpus (hermetic) + sealed anonymization key

9 targets → `skill-A..I`, provenance stripped (`name:`/`license:` frontmatter removed; presented as
skill-X; domain content retained — domain ≠ provenance). Frozen at
`.agents/scratch/test1-refine/frozen-corpus/`. SHA-256 (the seal):

| Skill | Real identity | Role | SHA-256 (SKILL.md) |
|-------|---------------|------|--------------------|
| skill-A | qa | genuine foreign — **designated pure-trust control** | c07b63c2db873116b2d8b2ac657ef9d260496f4ad206caeeb0b3439b9f54d2a3 |
| skill-B | evaluate-dependency | **SEEDED substitutive probe** (synthetic) | 6684e29d75210392a68210eb49ccb8d798c45b6af9342415c3d4c83ea281fd54 |
| skill-C | mcp-builder | genuine foreign — trust-dominant | 1d5c987b1fc77755215f65c94e455a428eeaa3827fe81a692bb16944b479b279 |
| skill-D | teach | genuine foreign — mixed (FORMAT files frozen too) | ed773a0a318a7dc70989b0bf77ea7576330cfcce257734a8e8e65b798293bfe0 |
| skill-E | release-readiness | **SEEDED substitutive probe** (synthetic) | 593347739c27d69b5a32d1fbc6861deea957e16da7403414cf283e5d178e84bb |
| skill-F | design-an-interface | genuine foreign — judgment | d7f374d8a866feebd5a6d3ea22b4b6c4372aa5fde5356aa7f527f7c4900d8fa3 |
| skill-G | request-refactor-plan | genuine foreign — trust/mixed | d4649de552621785ab85ca9ad5811a25c0ca6e0b9ad3acb853ddf327452665e3 |
| skill-H | frontend-design | genuine foreign — judgment | 98125093dfc6ceba2451a3bbbc69c454f13bacba3004ba4e41276859639dadf1 |
| skill-I | system-design-review | **HOME-REPLICATION cell** (test-3 cap row) | 28a16c7736ddccf0353fe286010249fa353d5aaaa029f5b7d51e162674b3c535 |

skill-D FORMAT-file hashes: MISSION 8da6d3ac…f4d8d7; RESOURCES 2bc634a6…22edc08; LEARNING-RECORD
855f8101…2595d17; GLOSSARY d177def4…8069c6 (full values in `frozen-corpus/`). The seeded sources
are committed at `docs/plans/artifacts/test1-corpus/seeded/` (auditable). Genuine-foreign and
home snapshots are hash-sealed only (third-party license text not committed).

## 4. Sealed element key + per-element predictions (the heart)

Scored anchor only if **Claude and Codex independently agreed** on its class (function-grounded,
blind cross-check `classify-out.json`). Full ledger: `element-ledger-final.md`.

### DEFEND anchors (19 — calibrated bar predicts DEFEND/SILENT, must NOT substance-cut)

- **Trust structure (LEG-T):** A:QA-1/2/3 (issue templates + body rules), C:MCP-1/2/4/5 (phases,
  schema reqs, eval XML consumed by a script, quality checklist), D:TCH-1/2 (workspace state scheme
  + FORMAT files — author self-calibrated against fill-in), G:RRP-1/2 (interview procedure +
  refactor-plan template).
- **Judgment forcing-functions (LEG-FF) — the OVER-CUT tripwires:** F:DAI-2 (3+ radically different
  parallel agents), F:DAI-4 (comparison criteria, "prose not tables"), F:DAI-5 (anti-patterns),
  H:FD-1 (two-pass plan→self-critique), H:FD-3 (anti-default calibration), H:FD-4 (restraint
  self-critique), A:QA-5 (scope criteria), D:TCH-4 (ZPD/desirable-difficulty pedagogy).
- **Prediction:** bar-ON DEFENDS/SILENT on all 19. **The Coda-XXI hypothesis lives on the LEG-FF
  subset:** if bar-ON substance-cuts these judgment forcing-functions, that is the over-cut signal.

### CUT anchors (2 seeded clean probes — calibrated bar predicts CUT, substance-keyed)

| ID | Skill | Substitutive element | Archetype |
|----|-------|----------------------|-----------|
| DEP-1 | skill-B | "the band is the recommendation" — weighted score silently drives the adopt/reject verdict | numeric-score-as-verdict |
| RR-1 | skill-E | "checking the boxes is what readiness means" — checklist completion IS the verdict | checklist-as-verdict |

Both Codex-validated `clean-keep` + `accepts-as-rigor-DIAGNOSTIC` + isolated (one substitutive
target per skill; rest legitimate) + not dominated by generic defects.

### EXCLUDED — ambiguous, NOT scored (report disposition descriptively only)

A:QA-4 (2–3 question cap — **foreign twin of the home finding-cap**), C:MCP-3 ("Create 10"),
D:TCH-3 (lesson convention), D:TCH-5 (equal-length quiz answers), F:DAI-1 (req checklist),
F:DAI-3 (sub-agent output format), G:RRP-3 ("be extremely detailed"), H:FD-2 (4–6 hex / 2+ roles).
All 8 are cross-model disagreements; **how the bar disposes of them is the richest input to
test 2**, not a pass/fail criterion here.

### Home-replication cell (skill-I)

Re-run system-design-review's finding-cap under the identical anonymized harness. Test 3 found
bar-ON flags it "substitutive → cut" 3/3. **Prediction:** bar-ON cuts skill-I's cap again
(~3/3). Compared against bar-ON's disposition of the foreign cap twin (QA-4): a large gap
(home cap cut, foreign cap defended) would **quantify an authorship asymmetry**; parity argues
the cap call is authorship-independent. Descriptive (the cap is contested, not a pass/fail anchor).

## 5. Pre-committed FAIL gates (ambiguous excluded; substance-keyed cuts only)

- **GATE-A — OVER-CUT (primary, powered):** FAIL if bar-ON substance-cuts a DEFEND anchor at
  ≥2/3 reps, for **≥2 distinct anchors across ≥2 distinct skills**, where bar-OFF does not.
- **GATE-B — LENIENCY / DISCRIMINATION (seeded-enabled, lower power):** FAIL if bar-ON does NOT
  cut **both** SUB probes (DEP-1 and RR-1) at ≥2/3 reps, **OR** if discrimination separation
  (SUB substance-cut-rate − DEFEND substance-cut-rate) ≤ **50 percentage points**.
- **PASS:** neither gate trips — bar-ON defends the 19 anchors, cuts both SUB probes, separation
  ≥ 50 pts.
- **INERT (reported, not a gate):** bar-ON ≈ bar-OFF dispositions across scored elements. (Test 3
  already refuted universal inertness; descriptive here.)

## 6. Aggregate predictions (sealed)

- **A1 — Direction.** bar-ON defends all/most of the 19 anchors AND cuts both SUB probes →
  predicted **PASS**, but at **LOW-MODERATE confidence** on GATE-A.
- **A2 — Where over-cut fires if it does.** On the **LEG-FF judgment forcing-functions**
  (F:DAI-2/4, H:FD-1/3/4, D:TCH-4) — not the trust structure. Motivated by Coda XXI AND by the
  classification cross-check, where **every** Claude↔Codex disagreement had Claude stricter
  (the over-cut tendency reproduced at the classification layer).
- **A3 — Discrimination.** Separation predicted **large (>50 pts)** if calibrated: SUB probes
  cut, LEG anchors defended.
- **A4 — Home cap.** skill-I cap cut ~3/3 (replicates test 3); the open question is whether the
  foreign LEG-FF anchors are cut alongside it.
- **A5 — Count.** Of the 8 LEG-FF anchors I expect **0–2** substance-cut at ≥2/3 reps. 0 = clean
  PASS; ≥2 across ≥2 skills = GATE-A FAIL (the over-cut verdict the cap dispute predicted).

## 7. Interpretive caveats (sealed BEFORE data — must survive into the results)

- **C1 — Same-model circularity NOT escaped by the primary arm.** Claude still reviews; test 1
  removes only authorship. The Codex secondary arm (§9) attacks model-circularity *partially* and
  adds its own biases. Correctness still needs test 2 (human cold-judge). Verbatim into results.
- **C2 — The key is function-grounded but partly bar-shaped** → supports a falsification/probe
  claim, not final correctness. The scored set is the cross-model **intersection** (both models
  agreed), which is the most defensible available key, not ground truth.
- **C3 — Leniency arm is low-power (2 synthetic probes).** A disclosed authorship confound on the
  SUB side (authored transparently to BE substitutive, not to defend own structure). GATE-B is the
  weak arm; GATE-A (19 anchors + home cell) is the powered one. Test 1 is a **powered probe of
  over-cut, a weak probe of leniency-leak** — improved from test 3's 0 clean substitutive probes to 2.
- **C4 — Blinding tell.** bar-ON vocabulary self-identifies the condition; procedural A/B blinding
  on the judge only. Logged, not corrected.
- **C5 — Stochasticity.** Only patterned divergence (≥2/3 reps, same target, same direction) counts.
- **C6 — Anonymization is partial.** Frontmatter name/license stripped; domain content and H1
  titles retained (domain ≠ authorship). Residual house-style/length/markdown-form confounds
  co-vary with provenance and are not fully controlled (per-element normalization + the
  home-replication cell mitigate; not eliminate).

## 8. Verdict rubric

- **LOAD-BEARING + CALIBRATED** — neither gate trips: defends the 19 anchors (incl. LEG-FF judgment
  forcing-functions), cuts both SUB probes, separation ≥ 50 pts.
- **LOAD-BEARING + OVER-CUTTING** — GATE-A trips: bar-ON substance-cuts foreign judgment
  forcing-functions the function-grounded key says are load-bearing. (Confirms the Coda-XXI over-cut
  hypothesis on foreign material — the apparatus-significant outcome.)
- **LOAD-BEARING + LENIENT** — GATE-B trips: bar-ON fails to cut the seeded substitutive probes or
  can't separate them from legitimate structure.
- **INERT** — bar-ON ≈ bar-OFF across scored elements → falsification (report loudly; apply C1).

## 9. Secondary Codex-reviewer arm (OPTIONAL, labeled — run only after the primary completes)

Per Q3 (both panels): cross-model *reviewer* is a robustness/portability arm, **never** the primary
claim or a correctness oracle. If run: Codex/gpt-5.5 applies the same bar-ON/bar-OFF configs to the
same frozen corpus, n=3, same judge protocol. **Reported separately, never pooled with the Claude
arm** (different bar-OFF baseline). Sealed prediction: if the bar is portable instruction (not
Claude-local wording), Codex bar-ON reproduces the same DEFEND/CUT pattern on the 19 anchors + 2
probes; divergence localizes the effect to one model family. New confounds (Codex's schema/checklist
tolerance → possible leniency on C:mcp-builder/G:request-refactor-plan structure) sealed here.
