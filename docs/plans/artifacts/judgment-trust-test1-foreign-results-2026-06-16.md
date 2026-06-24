---
type: results
experiment: judgment-trust test 1 — foreign-material element-discrimination differential
project: agents
prereg: judgment-trust-test1-foreign-prereg-2026-06-16.md @ d6cf84e (sealed before any run)
bar_on_ref: main @ f048687 (review-family 0.3.10)
bar_off_ref: 3eb0e74^ (8b9cfc1)
primary_reviewer: claude-opus-4-8 (54 hermetic runs; wf_3fc0f134-e56)
disposition_judge: gpt-5.5 / Codex (9 blind per-target judges)
verdict: LOAD-BEARING + CALIBRATED (PASS — neither gate tripped)
---

# Results — test 1, foreign-material element-discrimination differential

Predictions and the element key were sealed at `d6cf84e` before any reviewer ran. Data: 54 hermetic Claude reviews (9 anonymized skills × bar-on/bar-off × 3 reps), dispositions extracted per scored element by 9 blind Codex judges (different model family), scored against the sealed key. Disposition counts at ≥2/3 reps; substance-keyed cuts only for the gates.

## Verdict: **LOAD-BEARING + CALIBRATED (PASS)** — and stronger than the gates alone show

Neither gate tripped. On inspection of the judge evidence the result is cleaner than the raw score: the bar did **not** genuinely over-cut any legitimate structure at consensus, and on the foreign judgment skills it was **net-protective** — it defended judgment forcing-functions that the uniform baseline reviewer over-cut. **This directly answers the Coda-XXI binding question on foreign material (authorship removed): the bar does NOT over-cut organizing structure on judgment skills — the no-lens baseline does, and the bar corrects it.**

## GATE-A — over-cut: PASS (and the headline finding)

| Measure | bar-ON | bar-OFF |
|---|---|---|
| DEFEND-anchor substance-cut-rate (19 anchors × 3 reps) | **23%** | **25%** |
| DEFEND anchors substance-cut ≥2/3 | TCH-2, RRP-1 | QA-5, TCH-1, RRP-1, DAI-2 |
| **config-SPECIFIC over-cuts** (this config cut, the other defended) | **1: TCH-2** | **3: QA-5, TCH-1, DAI-2** |

GATE-A FAIL needs ≥2 bar-ON-specific over-cuts across ≥2 skills. Only **1** (TCH-2) → **PASS**.

**The reversal (the result that matters).** The Coda-XXI worry predicted bar-ON would over-cut foreign judgment forcing-functions. The opposite happened — on the two judgment forcing-functions where the configs diverged, **bar-OFF over-cut and bar-ON defended**:
- **QA-5** (single-vs-breakdown scope criteria): bar-OFF cut 3/3 substance ("a semantic decision the skill makes for the agent"); **bar-ON defended 2/3** ("provoking, not substitutive — keep").
- **DAI-2** (3+ radically-different parallel sub-agents): bar-OFF cut 3/3 ("mandatory fan-out removes the agent's judgment"); **bar-ON defended 2/3** ("substantially meets the provoke bar").
- Plus **TCH-1** (teaching-workspace state scheme): bar-OFF cut 2/3, bar-ON defended.

The bar's only consensus over-cut, **TCH-2**, is on inspection a **reference-wiring finding, not a substitutive over-cut**: all three bar-ON cuts say *"GLOSSARY-FORMAT.md is orphaned/unreferenced → link it into SKILL.md, or cut the doc"* — a delivery-hygiene defect (bar-OFF raised it too). The judge coded the "or cut" alternative as CUT/substance; the substance of the finding is "this format file isn't wired in," which is uniform delivery hygiene, not a judgment-bar over-cut. So the genuine bar-specific over-cut count is effectively **0**.

The other 6 judgment forcing-functions (DAI-4/5, FD-1/3/4, TCH-4) were defended by both configs. Trust structure (qa/mcp/rrp templates, eval XML, schema reqs) was defended by both.

## GATE-B — leniency / discrimination: PASS (with an honest nuance)

- **DEP-1** (score-band IS the verdict) and **RR-1** (checklist-completion IS the verdict): bar-ON substance-cut **both 3/3**. The bar is **not lenient** — it catches both seeded substitutive probes.
- Discrimination separation = SUB cut-rate 100% − DEFEND cut-rate 23% = **77 pts** (> 50 → pass).
- **Nuance (honest):** bar-OFF also cut both probes 3/3 substance. So the seeded probes function as **leniency tripwires** (bar-ON isn't lenient) but are **not bar-discriminating** — the uniform baseline catches blatant substitution too. This is exactly what Codex's red-team validation predicted (a competent non-bar reviewer would also flag them). The probes prove non-leniency, not bar superiority, on substitution detection.

## Home-replication cell (skill-I) — the cap dispute gets a decisive data point

| | bar-ON | bar-OFF | test-3 (home, named) |
|---|---|---|---|
| SDR finding-cap | **DEFEND 2/3** (0/3 substance; 1/3 form-softening) | CUT 2/3 (form) | bar-ON CUT 3/3 "substitutive" |
| QA-4 (foreign cap twin) | **DEFEND 3/3** | DEFEND 3/3 | — |

**The test-3 cap over-cut does NOT replicate under the anonymized harness.** bar-ON defends the system-design-review cap as a *"coverage ledger and depth budget that organizes attention without making the architectural call — keep,"* cutting only 1/3 and only **form-keyed softening** (0/3 substance). The foreign cap twin (QA-4) is defended 3/3 by both. Where the cap is cut at all, it's **bar-OFF** being harsher. → On a level, anonymized playing field the bar treats numeric caps as legitimate budgets, **substantially weakening the "the bar over-cuts the cap" reading** that the GENUINELY-OPEN frontier item rests on. Caveat: one cell, n=3, and the hermetic single-contract harness differs from test-3's setup, so authorship-vs-harness attribution is not clean — but the in-test fact is unambiguous.

## Sealed-prediction reconciliation

| | Sealed prediction | Outcome |
|---|---|---|
| A1 | PASS at low-moderate confidence | **CONFIRMED** (PASS) |
| A2 | If over-cut fires, on the LEG-FF judgment forcing-functions | **WRONG / REVERSED** — bar-ON *defended* them; bar-OFF over-cut QA-5 & DAI-2 |
| A3 | Discrimination separation > 50 pts | **CONFIRMED** (77 pts) |
| A4 | Home cap cut ~3/3 (replicates test 3) | **WRONG** — defended 2/3, 0/3 substance |
| A5 | 0–2 LEG-FF over-cut | **CONFIRMED** (0 genuine; TCH-2 wiring miscode is LEG-T, not LEG-FF) |

Two sealed predictions falsified (A2, A4), both in the bar's favour: I expected the bar to over-cut judgment structure and to replicate the cap cut; on foreign material it did neither.

## What this shows / does NOT show (sealed limits, carried)

- **Shows:** with authorship removed, the bar is calibrated on the over-cut axis — net-protective of legitimate structure (23% vs baseline 25%; 3 baseline over-cuts corrected, 0 genuine bar over-cuts), and not lenient (cuts both seeded probes). The Coda-XXI over-cut hypothesis is **not supported on foreign material**.
- **Does NOT show (C1 — same-model circularity NOT escaped):** the reviewer is still Claude; this is non-over-cutting + non-leniency, not proof the bar's calls are *correct*. Test 2 (human cold-judge) remains the correctness anchor.
- **C2:** the key is the cross-model Claude∩Codex intersection (function-grounded, partly bar-shaped).
- **C3:** GATE-B is low-power (2 synthetic probes) and the probes aren't bar-discriminating (baseline catches them too). The leniency claim is "not lenient," not "uniquely good at catching substitution."
- **C4:** blinding tell present, but the **by-condition pattern** (bar-OFF cuts forcing-functions, bar-ON defends) confirms the unblinding/scoring is correct — the mechanism sorts exactly by config.
- **C5/C6:** n=3; partial anonymization (frontmatter only); home-vs-foreign harness differs (cap caveat).

## Carry-forward to test 2 (human cold-judge docket)

1. **The cap** — test 3 (home) and test 1 (anonymized) disagree on whether the bar over-cuts the system-design-review cap. The disagreement is now *between two of the apparatus author's own runs*; only a human cold-judge resolves whether the cap is a forcing function or substitutive.
2. **teach's FORMAT files (TCH-2)** — flagged for wiring by the bar; is GLOSSARY-FORMAT genuinely orphaned, or is that a reviewer artifact? A cheap human check.
3. **The seeded probes aren't bar-discriminating** — to show the bar *adds* substitution-detection value over baseline would need harder, subtler substitutive material than the 2 clean probes.

## Provenance

Prereg `d6cf84e`. Reviews `wf_3fc0f134-e56` (54/54). Judges `bxdcog0qz` (9/9, Codex gpt-5.5). Working artifacts (frozen corpus + hashes, configs, judge bundles, label map, scoring) in `.agents/scratch/test1-refine/` and `/tmp/codex-test1/` (latter ephemeral). Apparatus UNCHANGED.
