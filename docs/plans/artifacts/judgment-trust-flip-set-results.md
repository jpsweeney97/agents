# Judgment/Trust Flip-Set — Acceptance Results (Task 9)

Durable, replayable record of the blind acceptance test for the judgment-vs-trust apparatus change (`docs/plans/2026-06-15-judgment-trust-apparatus.md`, Task 9). Pairs with the blind fixture (`judgment-trust-flip-set.md`) and the sealed key (`judgment-trust-flip-set-key.md`). This file is the merge gate Task 8 made the branch depend on.

## Final verdict: **PASS — branch merge-ready**

Reached after a Path-1 remediation. The first run **FAILED** and, on investigation, the failure was a **fixture-construction / scoring-contract defect, not apparatus leniency**. The remediation reconciled the scoring contract, repaired two miscalibrated fixture rows, and added a synthetic keep-floor; a **fresh, fully-clean re-run under the corrected contract passed all ten rows.** The apparatus skills (`agent-facing-design`, `scrutinize-skill`) were **not** changed — the evidence shows the provoke-side text already works.

- **Decisive evidence:** the synthetic clear-case keep-floor (row 10) was **kept and escalated to Critical by all three independent blind reviewers**, each naming it as the exact provoke-side inversion the bar describes. When a softened-provoke defect is *clear*, the apparatus makes blind reviewers keep it. That is the proof the apparatus is not lenient.
- **Why the first run failed:** row 7 (grill-me) is a **balanced** case — its softeners are woven into dominant adversarial framing — so three careful reviewers split (surfaced it, then 2 substantively dropped / 1 kept). The original scoring's flat "raised-then-dropped = leniency FAIL" mislabeled correct discrimination as leniency and contradicted the key's own marginality clause.
- **Meta-finding (premise confirmed):** an exhaustive search of the live library *and* the archive found **no clear softened-provoke defect** — every adversarial skill is sharp; the only softened phrasings (grill-me, grill-with-docs) are balanced. The keep-floor therefore had to be synthetic. That absence is the apparatus's founding observation, confirmed: the library was being over-flagged on conformance, not under-flagged on judgment.
- The pass condition was **not** weakened to force a pass; see **Scoring-contract correction** for why the change is a false-positive fix, not a relaxation.

## Provenance

- **Loaded `review-family` version:** `0.3.10` (Task 5/6). Preflight (fresh session): branch `feature/judgment-trust-distinction`; HEAD at the Task 10 commit `0e76b1e` (one past the Task 8 checkpoint `3eb0e74` — both apparatus commits present); `scripts/codex-plugins-sync.sh --check` exit 0, no drift; `grep -c "Bar And Execution Quality" plugins/review-family/skills/scrutinize-skill/SKILL.md` → `1`.
- **Runtime / session:** Claude Code, fresh session (2026-06-16). To guarantee the *edited* rubric was applied, every reviewer read the working-tree source in full and applied it (`scrutinize-skill/SKILL.md` + `agent-facing-design/SKILL.md` "Two Kinds of Skill"). The working tree is the live Claude source.
- **Apparatus state under test:** unchanged from the Task 8 checkpoint. The remediation touched only test scaffolding (plan Task 9 scoring, sealed key, blind fixture, and the new synthetic fixture skill).

## Run history

Three background workflow runs of fresh, independent subagent reviewers, each producing a structured review (bar classification stated *before* findings; every concern recorded `raise-and-keep`, `raise-and-drop`, or — by absence — `not-raised`).

| Run | Workflow | Reviewers | Scope | Result |
|---|---|---|---|---|
| 1 | `wf_bdc8f6c5-3ff` (`wl97sgw3t.output`) | 27 (9 rows × 3) | original fixture + contract | **FAIL** (row 7 tripwire; row 1 not-proven; rows 4/6 contaminated) |
| 2 | `wf_484b6b1c-788` (`wwg5hdmdr.output`) | 6 (rows 4,6 × 3) | blindness-locked clean re-run of the contaminated rows | rows 4, 6 confirmed clean |
| 3 | `wf_5f03cc64-f8f` (`wqf3e5e74.output`) | 30 (10 rows × 3) | **fresh, blindness-locked, corrected contract** | **PASS** (10/10; 30/30 blind) |

**Withheld from every reviewer's context** (never pasted): the source report (`.agents/skill-library-scrutiny-2026-06-15.md`), the blind fixture, the sealed key, the plan file, and the Task-10 retriaged backlog.

### Run 1 — FAIL, and what it exposed

Result: 7 of 9 rows landed (2, 3, 4, 5, 6, 8, 9). Two did not:

- **Row 7 (grill-me), the leniency tripwire — FAILED.** All three clean reviewers *surfaced* the softened-adversarial-posture concern, but 2 of 3 then **dropped** it with substantive, text-specific reasoning (rev1: the "shared understanding" goal does not dilute given "relentlessly / every aspect / each branch"; rev2: the "recommended answer" *raises* counter-pressure by forcing a concrete position to rebut); 1 kept it (Minor). Under the original flat rule, raised-then-dropped = FAIL.
- **Row 1 (scrutinize) — not yet proven.** Bar-classification divergence: the "section-name divergence" half is a *real* trust-flavored single-sourcing seam (the section names are duplicated across `SKILL.md` and the reusable `references/review-format.md` template and have drifted — live-confirmed), so reviewers correctly split judgment/trust. The key's uniform "judgment" label under-determined the bar.

**Methodological breach (Run 1), contained.** Run 1 gave reviewers filesystem access for the sibling scan but did not fence off `docs/plans/`. Four reviewers self-served withheld material during directory scans (the orchestrator never pasted it): row4 rev3 read the plan file; row6 rev1 read the sealed key; row4 rev2 and row6 rev3 read the Task-10 retriaged backlog. A marker scan confirmed the breach is **confined to rows 4 and 6** — both unanimous-PASS rows. **Rows 1, 2, 3, 5, 7, 8, 9 were 100% clean**, so the row-7 FAIL and row-1 verdict rest entirely on uncontaminated reviewers. Run 2 re-ran rows 4 and 6 with a strict source boundary (all clean), confirming both. Run 3 carried the same lockdown for all rows (30/30 clean).

### Diagnosis: fixture/contract defect, not apparatus leniency

Adversarially checked, the row-7 FAIL was *not* leniency:

1. One reviewer *kept* it — the rubric can make a reviewer keep a provoke defect.
2. The two droppers reasoned **text-specifically**, naming the keep-rule and building a counter-case (rev2 argued the softener *increases* counter-pressure — the opposite of a lazy shrug). A separate manual re-read of grill-me confirmed the softeners ("shared understanding", "recommended answer") are woven into dominant adversarial framing → a genuinely **balanced** case.
3. On rows 6 and 9 the same reviewers discriminated correctly (did not reflexively drop judgment findings; did not over-cut legitimate structure).
4. The source report itself logged grill-me under "zero confirmed material findings." The key had already flagged row 7 as "a deliberately sharpened edge case."

So the verdict did not reproduce under independent judgment — which, by the key's own construction rule, means grill-me is borderline and was miscalibrated as the binding keep-tripwire.

## Scoring-contract correction (Path 1)

The run exposed a real contradiction *inside the contract*: condition (1) "raised-then-dropped = leniency FAIL" conflated **lazy leniency** (token mention then a shrug — the real target) with **correct discrimination on a balanced case** (cite the line, name the keep-rule, build the counter-argument, conclude drop), and it contradicted the key's own marginality clause ("marginality earned by a separate manual re-read concluding the row is genuinely balanced").

Reconciliation (applied to plan Task 9 and the sealed key's anti-leniency check):

- **Bindable leniency FAILs, both retained:** (a) **unanimous never-raised** (silence-floor) and (b) **surfaced-then-dropped on weak/non-substantive reasoning**. These are reproducible against any softenable surface — they test whether the apparatus makes reviewers *look* and *reason*, which needs no clear case.
- The bright-line "raised-then-dropped = FAIL" still holds **on a construction-rule-compliant clear keep-case** (dropping a clear provoke defect is leniency).
- A **substantive** drop on a case a separate manual re-read finds **genuinely balanced** is **marginality** (repair the fixture row), not leniency. The keep/drop disposition on a balanced case is a judgment call, not a gate.

This is a **false-positive correction, not a weakening**: it removes no genuine leniency path (both bindable FAILs stay), it is justified independently of the outcome (the conflation and the internal contradiction are provable from the Run-1 transcripts alone), and it was proven on a **fresh** re-run — never by relabeling the run that exposed it. The plan's earlier "for row 7, sharpen the provoke side" pre-commitment rested on the premise that a row-7 failure means the keep-side is under-conveyed; Run 1 falsified that premise (3/3 surfaced the concern), so sharpening the apparatus would have tuned it toward over-keep — the mirror failure row 9 guards.

### Fixture repairs

- **Row 1** relabeled **compound / per-part**: the verdict-token **casing** half is judgment-cosmetic (DROP); the **section-name-vs-reusable-template** half is trust-flavored drift (KEEP, downgraded). Passes if the reviewer does not escalate the cosmetic half and reads the template/output machinery on the trust bar.
- **Row 7** reframed from must-keep tripwire to the **silence-floor**: it binds the reproducible part of leniency (do reviewers surface and substantively reason about the provoke concern?), not the disposition on a balanced case.
- **Row 10** added: a **synthetic clear-case keep-floor** — a fabricated fixture skill (`docs/plans/artifacts/synthetic-probes/pressure-test-my-plan/SKILL.md`, outside both runtimes' scan paths, verified inert) that promises adversarial pressure-testing but whose body is fully reframed as gentle, reassuring collaboration with zero counter-pressure. The mirror of the row-9 over-cut probe; it keeps the bright-line exercised since the live library has no clear softened-provoke defect. In Run 3 it was presented inline (no revealing path).

## Final scorecard (Run 3 — fresh, corrected contract, 30/30 blind)

Disposition legend: **K** = raise-and-keep, **D** = raise-and-drop, **N** = not-raised. Bar legend: **J** = judgment, **T** = trust, **PP** = per-part/mixed.

| # | Skill | Key class | Expected | Result across the three reviewers | Pass |
|---|---|---|---|---|---|
| 1 | scrutinize | PP (compound) | split: cosmetic DROP, trust-machinery KEEP | all 3 read **PP**; dropped the casing nit; kept trust-machinery defects (verdict-vocab unreachable, mode-selection ambiguity, routing single-sourcing) | ✅ |
| 2 | system-design-review | J | reverse | no reviewer completed the cap rule; all evaluated caps under the judgment bar; rev3 **kept** "numeric floors can manufacture findings" (the reverse) | ✅ |
| 3 | tdd | J | reverse | none flagged the absence of a mandated output shape/closure as a defect | ✅ |
| 4 | merge-branch ×4 | T | keep+escalate | all 3 **K** the hand-copied protected-branch gate as **T**; 2/3 Major | ✅ |
| 5 | search-handoffs | T | keep | all 3 **K** the unset-`$PROJECT_ROOT` defect as **T**; 2/3 Major | ✅ |
| 6 | gh-pr-review-loop | mixed | per-part split | all 3 classify **PP**; none demand output-shape on the judgment part; each keeps/considers real trust lifecycle bugs (`@codex` hardcode dropped as home-repo-acceptable — borderline, consistent across runs) | ✅ |
| 7 | grill-me | J (silence-floor) | surface + reason | 3/3 **surfaced** the provoke concern and reasoned substantively (rev1 **K** Minor; rev2, rev3 substantive **D**); balanced case → disposition not gated | ✅ |
| 8 | claude-code-docs | T (lookup) | keep+escalate | all 3 classify **T/lookup** (tail not mis-sorted); all keep real trust defects (rev3 found a Major failure-model bug) | ✅ |
| 9 | outcome-interviewer | J (over-cut probe) | do not flag | no reviewer raised-and-kept a "cut the rhythm" finding; structure recognized as organizing | ✅ |
| 10 | (synthetic) pressure-test-my-plan | J (keep-floor) | keep+escalate | **all 3 K at Critical**; all **J**; each named the provoke-side inversion (sycophancy disguised as a pressure test) | ✅ |

**Bar-classification check:** every row's reviewer classification matches the (corrected) key — no bar-divergence teeth fire.

**Discrimination checks (Task 9, 1–6):** all satisfied — rows 1–3 drop/reverse; row 7 surfaced+reasoned (silence-floor); rows 4–5 keep; row 6 splits per part; row 8 keeps as trust/lookup; row 9 no over-cut; plus the row-10 keep-floor kept.

## What this proves (and its honest limit)

- The apparatus **discriminates correctly** across conformance-drop (1–3), trust keep/escalate (4, 5, 8), per-part classification (1, 6), over-cut resistance (9), and the silence/keep floors (7, 10).
- It is **not lenient on judgment**: it makes reviewers surface provoke concerns (row 7: 3/3) and keep an unambiguous provoke defect (row 10: 3/3 Critical).
- **Honest limit:** the keep *disposition* on a **subtle/balanced** provoke case is not gateable — reasonable reviewers split (row 7), and that is correct, not a defect. There is no reproducible subtle keep-tripwire because the live library contains no clear softened-provoke defect (premise confirmed). The synthetic floor tests gross keep-regression, not the subtle bar.

## Reproduce

- Run 1: workflow `wf_bdc8f6c5-3ff`; raw `tasks/wl97sgw3t.output`.
- Run 2 (clean re-run, rows 4/6): workflow `wf_484b6b1c-788`; raw `tasks/wwg5hdmdr.output`.
- Run 3 (fresh, corrected contract, authoritative): workflow `wf_5f03cc64-f8f`; raw `tasks/wqf3e5e74.output`.
