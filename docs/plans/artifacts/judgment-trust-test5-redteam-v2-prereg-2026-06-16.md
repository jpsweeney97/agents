---
type: pre-registration
experiment: judgment-trust test 5 v2 — adversarial red-team, BOTH ARMS (leniency FN + over-cut FP) under one seal
project: agents
status: "NOT SEALED — superseded by the pre-seal pilots. The 8-lens panel (wf_60516e04-80c) gated the seal on an unsealed base-rate pilot; the pilot + sharpening pilot (judgment-trust-test5-v2-pilot-results-2026-06-16.md) showed the FN leniency channel is empty (0/6 levers) and the FP over-cut channel is empty on neutral material. No sealed run is warranted → test 5 CLOSED as characterized, apparatus UNCHANGED. This draft is retained for provenance only."
sealed_at: "(set by the sealing commit — committed BEFORE any specimen is constructed or any reviewer runs)"
bar_on_ref: main @ <seal-commit> (the judgment-vs-trust LENS — `## Two Kinds of Skill` in agent-facing-design + the step-3/severity rules in scrutinize-skill)
bar_off_ref: 8b9cfc1 (= 3eb0e74^ — pre-lens baseline reviewer; single variable; same baseline as tests 1, 3, 5v1)
constructor_models: ["gpt-5.5 / Codex (white-box, cross-model adversary)", "claude-opus-4-8 (white-box, same-model adversary — the prereg-§7 complement v1 never ran)"]
ground_truth: HUMAN is the sole authority on every scored specimen (FN and FP); cross-family model pre-cert (Codex + Claude, >=3 blind reps) is a non-gating filter only
reviewer_model: claude-opus-4-8 (bar-ON and bar-OFF arms; reviewer-side same-model circularity NOT escaped — only ground truth + the Codex adversary are off-model)
disposition_judge: claude-opus-4-8 (blind, arm-relabelled) + human audit subset
depends_on: test 1 (CALIBRATED, 0f70235); test 2 (human PASS, 665fe5c); test 3 (LOAD-BEARING, f048687); test 4 (cut-then-use AT-LEAST-AS-GOOD, 386e5ff); test 5 v1 (INCONCLUSIVE/W2 + zero ground-truth leniency, 51ab24e)
supersedes: judgment-trust-test5-redteam-prereg-2026-06-16.md (v1 — INCONCLUSIVE by W2; v2 fixes the three documented failure modes)
---

# Pre-Registration — test 5 v2, adversarial red-team (BOTH ARMS, one seal)

> ## PANEL VERDICT — SUPERSEDED, DO NOT SEAL THIS VERSION  An 8-lens adversarial design panel (`wf_60516e04-80c`, 58 raw findings) returned **SEAL-AFTER-FIXES** with a decisive correction: **the §0 failure-mode-A fix misattributes test 4.** The whole-section cut in test 4 was made by **bar-ON (the lens, via cold blind discovery)**, NOT by the bar-OFF baseline — so there is **no evidence the baseline cuts whole sections.** Since the lens is uniformly ≥ baseline strictness (v1), the FN divergence cell (bar-OFF cuts ∧ bar-ON defends) may be **forbidden by construction** — the v1 wall re-imported. Accepted fixes (applied in the pilot-gated final v2.1):  1. **Re-key FN onto the change-keyed yardstick, decisive** (DEFEND-as-is vs CUT+RESHAPE); CUT-keyed is sensitivity-only. (BLOCKER) 2. **Gate the seal on an UNSEALED section-grain base-rate pilot** (bar-OFF, and bar-ON for contrast); an arm is sealed as a gated falsification channel only if the pilot shows its divergence cell can fire, else it drops to characterization-only. (BLOCKER) ← **this doc's immediate next step** 3. **Build a section-grain ground-truth instrument** (the v1 certifier asks about one embedded focal choice; a whole section has none): "for the section titled X — keep / trim-revise / remove entirely, and why?", asked uniformly on every candidate incl. filler/floors. (BLOCKER) 4. **Split §9 by power; forbid laundering an empty FN arm into "conclusive by accumulation"; pre-commit a non-vindicating DOUBLE-INCONCLUSIVE; reorder the rubric so gates are checked before the INCONCLUSIVE route.** (BLOCKER) 5. **Strip the false FP premise** (test 1 found the lens NET-PROTECTIVE, zero genuine over-cut; the test-3 home-cut did not replicate anonymized → FP is the FIRST real power on over-cut, not a confirmation); add a bar-OFF KEEP-AFFIRMED attribution ruling; key GATE-FP on CUT; **downgrade OVER-CUT-CONFIRMED from auto-mandate to a human-adjudicated, off-model-corroborated finding.** (MAJOR) 6. **Decouple FN admission from the Claude pre-certifier** (certify FN badness with Codex + human; carry a pre-cert-cleared-but-human-bad shared-blind-spot quota). (MAJOR) 7. **Operationalize in-remit + lens-attribution as pre-specimen, blind, capped, counted rulings** (not post-hoc escape hatches). (MAJOR) 8. **Build + hash the human packet BEFORE any reviewer runs**; non-orchestrator authors section/focal descriptions; separate blind tilt-check. (MAJOR) 9. **Re-derive corpus size from the AND-conjunction survival rate** (~20% joint → ~30 candidates/side for ≥6 certified, or loosen cert to non-veto); tighten cert beyond bare modal call. (MAJOR) 10. MINOR bundle: §8 FN route-1 wording bug ("cut by NEITHER arm"); pin filler size/list in the seal; re-scope to the judgment-part lens (or restore trust-side defects); add a unified cross-arm baseline-disposition table to §6; reword §9 independence honestly (one repeated Claude reviewer + one n=1 human, not three independent probes).  **The text below is the pre-panel draft, retained for provenance.** The pilot results and v2.1 final supersede it. Full panel reasoning: workflow `wf_60516e04-80c`.

**Sealed by its commit; written and committed BEFORE any specimen is built or any reviewer runs.** The results doc (`judgment-trust-test5-redteam-v2-results-<date>.md`) cites this SHA as proof predictions and gates preceded the data. This is the **re-run** of test 5 of the 5-test menu after v1 graded INCONCLUSIVE. Scoreboard at draft time: **1 ✓ · 2 ✓ · 3 ✓ · 4 ✓ · 5 ◐.**

## 0. Why v2 exists — the three documented failure modes v1 hit, and the fix for each

v1 (`7869892`) ran fully and graded **INCONCLUSIVE (route W2): the white-box Codex adversary built no specimen the bar-OFF baseline CUTS**, so the leniency channel (bar-OFF CUTS ∧ bar-ON DEFENDS) was structurally empty and GATE-FN was un-evaluable. The reviewer-side re-key (T1), an independent re-code, a 4-way refutation, and a fresh blind human (T2) all agreed on the *direction*: **zero lens leniency, the lens is if anything stricter, and on the one adjudicable specimen (FN6) the lens corrected the baseline toward the human.** But the falsification gate never got power. Three named causes, each with a v2 fix:

| # | v1 failure mode | v2 fix |
|---|-----------------|--------|
| **A** | **Leniency keyed on CUT**, a disposition opus reviewers almost never emit for an **embedded** focal choice (bar-OFF CUT 0/27). The channel was structurally empty. | **Move the badness into a WHOLE REMOVABLE SECTION/MECHANIC.** Test 4 proved opus reviewers DO cut whole superfluous sections cleanly (the `next-steps` recap checklist). So bar-OFF can actually CUT, and the divergence becomes constructible. Disposition keyed primarily on **CUT-vs-KEEP** (now achievable) **and** re-keyed on **any-change-vs-DEFEND-as-is** (the fair yardstick from T1) for robustness. |
| **B** | **56% construction-miss** — the adversary's own family agreed only 5/9 specimens were actually bad. Reviewer runs were spent on material that was not genuinely bad, so the gate's denominator collapsed. | **Over-generate, then cross-family certify badness BEFORE any reviewer run.** Keep only specimens where a cross-family model pre-cert (Codex + Claude, blind, >=3 reps each) **agrees with the intended ground truth**. The HUMAN remains the sole gating authority, but it scores a corpus already filtered to high agreed-badness/goodness. |
| **C** | **Single-family adversary** (Codex only); its hole-model may not transfer to the Claude-applied lens (the prereg-§7 RESILIENT ceiling). | **Two adversary families** build the pool: Codex (gpt-5.5, cross-model) **and** Claude (opus, same-model — the white-box probe v1 named but never ran). Same-model construction is *good* for finding the lens's real holes; cross-model gives diversity. |

**Plus JP's design choice: run BOTH arms under one seal.** v1 made the FP/over-cut side characterization-only. v2 **gates both**: the FN (leniency) arm AND the FP (over-cut) arm. Rationale: the leniency channel has come up empty twice; the **over-cut channel is where every prior test found live signal** (test 3 home-cut the system-design-review cap; test-5v1 GOOD1; the arc's recurring "the lens's only error mode is over-cutting"). Gating FP means **v2 yields a real, consequential result even if the FN arm is empty a third time.** See §9 for what a 2nd empty FN channel means — decided up front.

## 1. The one question, reframed as a classifier with two error directions

The lens introduces a **classifier** into the reviewer: on a judgment part, structure is either **provoking** (organizes/elicits thinking → KEEP) or **substitutive** (mandated shape / exhaustive rule list / fixed fill-in section that makes the judgment for the agent → CUT). v2 measures **both error directions of that classifier against human ground truth, relative to the no-lens baseline**:

- **bar-specific FN (ΔFN) — leniency, the original falsification target.** A whole section/mechanic that is **genuinely BAD** (human says remove/change) but **the lens DEFENDS** (bar-ON KEEP >=2/3) while the **baseline CUTS** it (bar-OFF CUT >=2/3). Mechanism: the section is bloat/substitutive **camouflaged as a forcing function**, so the lens's "provoking structure earns its place" clause talks the reviewer out of a cut the baseline makes. *The lens hands the reviewer a vocabulary to rationalize keeping bad structure.*
- **bar-specific FP (ΔFP) — over-cut, now gated.** A whole section/mechanic that is **genuinely GOOD** (human says keep) but **the lens CUTS** (bar-ON CUT >=2/3) while the **baseline KEEPS** it (bar-OFF KEEP >=2/3). Mechanism: a genuine forcing function **camouflaged as substitutive bloat**, so the lens's "cut substitutive structure" clause over-fires. *The lens's category boundary is drawn too aggressively.*
- **shared FN / shared FP** (both arms agree wrong) = generic-reviewer behavior, **never scored vs the lens**. Absolute bar-ON errors are not attributable to the lens (test 1: the baseline cuts seeded substitutives too). The unit is the **bar-ON − bar-OFF divergence**, ground-truthed by a human.

Both arms probe the **same decision boundary** (provoking vs substitutive) from opposite sides. The prediction the whole arc points to: **ΔFP > ΔFN** (the lens over-cuts more than it under-defends). v2 tests that with engineered divergence and human ground truth.

## 2. Roles

1. **Constructors — two families, white-box.** (a) Codex/gpt-5.5 and (b) Claude/opus. Each reads the full bar and builds specimens designed to make the lens mis-classify a WHOLE SECTION. Each logs (sealed, hidden from roles 3–5) the focal section, intended ground-truth disposition, attack vector, and the **exact lens clause weaponized**. *Residual: the Claude constructor and the Claude reviewer share a family (white-box same-model); this is a feature for hole-finding, a circularity for generality — see §8. The Codex constructor co-authored the bar's calibration (test-1), so its hole-theory may not transfer — the RESILIENT ceiling.*
2. **Cross-family badness pre-cert (non-gating filter).** Before any reviewer run, every candidate specimen is scored blind (focal section described neutrally, keep/change/remove, >=3 reps) by **both** Codex and Claude pre-certifiers. A specimen **advances to the reviewer corpus only if both families' modal call agrees with the constructor's intended ground truth** (FN: agree it is bad → change/remove; FP: agree it is good → keep). Disagreement → either escalate to the human pre-cert or drop (logged). **This filter cannot clear or trip any verdict gate** — it only raises the agreed-badness/goodness rate of what the human then authoritatively scores. (Fixes failure mode B.)
3. **Reviewer — two arms, same specimens:** Claude applying **bar-ON** (`main` @ seal) and **bar-OFF** (`8b9cfc1`), hermetic, blind, **3 reps each (5 on any 2-1 split)**, neutral arm names. Reuses the v1 `review-workflow.js` harness + `extract-configs.sh` single-variable lock (the bar contracts are the two frozen bar surfaces concatenated; the ONLY difference is the lens).
4. **Ground truth — HUMAN, sole authority on every scored specimen** (FN and FP). Reads the full coherent skill and calls **keep / change / remove** on the focal section with one sentence — the **neutral test-2 question** (the `certifier-prompt.txt` wording), never the lens's vocabulary. Administered under the **blinding guard** (`AGENTS.md` `## Blind Evaluations`): a fresh judge who has not seen apparatus state. A blind **Codex ground-truth check (>=3 reps)** runs as a *secondary, non-gating* corroborator (the cross-model ground-truth complement), reported but never decisive.
5. **Disposition judge** — Claude (blind, arm-relabelled) extracts **CUT / RESHAPE / KEEP(DEFEND) / SILENT** on each focal section, **+ human audit subset**. SILENT (review never engaged the section) on a confirmed-scored specimen is a **salience miss, not a divergence** (specimens are built so the focal section is the dominant design decision). Keying: see §5.

## 3. "The bar" = the lens (one object); in-remit + attribution rules

A specimen counts toward a gate only if its (human-confirmed) badness/goodness is something the **lens itself classifies** (sealed, decidable):

- **FN in-remit:** the bad section is, in truth, **substitutive** (a mandated shape, an exhaustive rule list, or a fixed fill-in section that makes the judgment for the agent) **or pure recap/bloat** that adds nothing over the bare agent — i.e. genuinely cuttable structure dressed as provoking.
- **FP in-remit:** the good section is, in truth, a **genuine forcing function** (an interrogation rhythm, a forced comparison, a required counterexample, an adversarial posture) that organizes/elicits thinking — i.e. genuinely keep-worthy structure dressed as substitutive.
- **Excluded:** out-of-lens defects (wrong facts, bad domain advice, UX/routing/validation problems), and any badness/goodness not visible in the contract text (needs runtime evidence the static reviewer lacks).

Two **blind, decidable, logged** rulings guard each scored cell, each made by a party who does **not** see the bar-ON verdict on that specimen:

- **in-remit ruling** — is the human-confirmed badness/goodness in the lens's classifier remit (above)? Logged with reason.
- **lens-attribution ruling** — is the divergence-creating disposition (the bar-OFF CUT for FN; the bar-ON CUT for FP) driven by a step whose bar-ON analogue is the judgment/trust **lens** (not a UX/routing/ validation step)? If not, the divergence is a generic-step difference, reported descriptively, **not** a scored FN/FP. Disputes go to the human audit.

## 4. Specimen ledger (sealed) and run tiers

**Over-generate, then certify down.** Target construction (pooled across the two adversary families):

- **~12 ΔFN candidates** — bad-section-as-forcing-function, spanning **>=2 distinct vectors** (substitutive section dressed as forced-comparison/interrogation; pure-recap/bloat section dressed as a "pre-flight forcing checklist" — the test-4-proven cuttable shape).
- **~12 ΔFP candidates** — good-forcing-function-as-substitutive, spanning **>=2 distinct vectors** (genuine forced-comparison dressed as a mandated fill-in shape; genuine required-counterexample mechanic dressed as an exhaustive rule list).
- **Positive controls (2):** **FN-PC** = a clearly-bad whole section the baseline should plainly CUT (proves the FN channel can fire — the W1 check test-4 evidence says will now succeed); **FP-PC** = a clearly-good forcing function the baseline should plainly KEEP (proves the FP channel can fire).
- **Floor controls (4):** 2 clear-GOOD + 2 clear-BAD, undisguised — prove the reviewer is awake.
- **Filler:** a sealed library slice chosen by a non-constructor (neutral, real skills) to dilute the adversarial tell; size set at run time per tier.

**Cross-family certification gate (§2.2) runs on all candidates BEFORE the reviewer corpus is fixed.** Only candidates whose intended ground truth is **cross-family-agreed** enter the reviewer run. **Equal construction effort per side**, reported in *checkable* units (candidates built, realism-rejected, retained per side/family), never a self-attested budget. **Denominators:** GATE-FN over the **certified ΔFN specimens** (plus escalated construction-misses); GATE-FP over the **certified ΔFP specimens**; PCs, floor controls, and filler are reported separately, never in a gate denominator.

**Realism gate** (blind to label/direction, not the constructor; sealed hard conditions, per-specimen logged): the focal section would plausibly ship (name a real analogue); the surrounding skill is a coherent real job; the disguise is not signposted; a reader told only "candidate skill" would not flag it as a test. Any condition fails ⇒ excluded or rebuilt subtler (same vector, outcome-blind).

**Run tiers (pick at run time; the dual core is mandatory):**

- **DUAL-CORE (mandatory):** certified ΔFN + certified ΔFP + 2 PC + 4 floor + a small fixed filler slice, × {bar-ON, bar-OFF} × 3 reps. With ~6 certified per side this is ~(6+6+2+4+filler) ≈ 20 candidates × 2 × 3 ≈ **~120 hermetic reviews**; human certifies the ~12–16 scored specimens + PCs + escalations (on the order of test-2/v1 human load).
- **SCALE-UP (optional):** widen each side to its full ~12 + a larger filler corpus if the core completes and the budget allows. Characterization either way.

## 5. Disposition keying and the gates (human-authoritative, baseline-relative, rate-based)

Dispositions at **>=2/3-reps consensus** per arm. **Primary keying** (whole-section specimens make CUT achievable — failure-mode-A fix):

- **CUT** = remove the section. **KEEP/DEFEND** = leave it essentially as-is. **RESHAPE** = materially change it. **SILENT** = never engaged.

**Two keyings, both pre-registered, both reported (the T1 robustness discipline):**

- **Primary (CUT-keyed):** FN divergence = bar-OFF CUT>=2/3 ∧ bar-ON KEEP>=2/3. FP divergence = bar-ON CUT>=2/3 ∧ bar-OFF KEEP>=2/3.
- **Robustness (change-keyed, the fair yardstick):** CAUGHT = CUT+RESHAPE>=2/3; LENIENT = KEEP/DEFEND>=2/3. FN = bar-ON LENIENT ∧ bar-OFF CAUGHT; FP = bar-OFF would-keep but framed as the over-cut side — for FP the change-keyed read is bar-ON CAUGHT (cut/reshape) ∧ bar-OFF KEEP. **The verdict cites both; they must agree in direction or the disagreement is itself a reported finding.**

**Power floors.** An arm is **POWERED** only if **>=3** specimens reach (human-confirmed intended ground truth ∧ the baseline behaves as the divergence requires: FN needs >=3 baseline-CUT-confirmed; FP needs
> =3 baseline-KEEP-confirmed). **<3 ⇒ that arm is UNDERPOWERED → INCONCLUSIVE on that arm.**

**Construction-miss → human, never a silent drop.** A constructor-intended specimen the cross-family pre-cert splits on is **escalated to the human**; a human-confirmed bad-section the lens DEFENDS (or human-confirmed good-section the lens CUTS) is a **scored divergence** even if the pre-cert missed it (the shared-blind-spot case — the most diagnostic). Drop count is a named output; **per-side drops >50% ⇒ that side certifier-confounded, INCONCLUSIVE on that side.**

- **GATE-FN (leniency falsification).** **>=2** bar-specific FN across **>=2 distinct vectors** ⇒ the lens creates leniency a no-lens reviewer would not → **FALSIFIED-LENIENT**.
- **GATE-FP (over-cut, NEW — gated this time).** **>=2** bar-specific FP across **>=2 distinct vectors** ⇒ the lens over-cuts legitimate forcing functions a no-lens reviewer keeps → **OVER-CUT-CONFIRMED**.
- **Per-rep metrics** (consensus can hide partial effects): over confirmed divergence-eligible specimens, the fraction of individual bar-ON reps that DEFEND where bar-OFF cut (FN) / that CUT where bar-OFF kept (FP). **>20% on either is itself a reported finding** even if no specimen reaches >=2/3.

## 6. Outputs (sealed shape)

For each arm: the bar-ON absolute 2×2 (descriptive); the **ΔFN and ΔFP matrices** with per-cell example specimens (focal section, attack vector, weaponized lens clause, bar-ON n/3, bar-OFF n/3, human reason, in-remit + lens-attribution rulings); per-family **construction-success, cross-family-cert agreement, and drop counts**; **certifier↔human agreement**; the **per-rep ΔFN/ΔFP rates**; both PC outcomes; realism- reject counts per side/vector/family; the **ΔFP vs ΔFN asymmetry** with bar-OFF base rates; the per-arm verdict and the combined apparatus disposition (§8); the secondary Codex ground-truth corroboration; the W1/W2 determination per arm.

## 7. Sealed caveats (must survive into the results)

- **Reviewer-side circularity NOT escaped (C1, as tests 1, 3, 5v1).** bar-ON disposition and disposition extraction are claude-opus-4-8. Only the **human ground truth** and the **Codex** arms (adversary + secondary ground-truth check) are off-model. v2 characterizes one model's application of the lens; a cross-model-*reviewer* arm (test-1 §9 style) is the portability complement, not run here.
- **Same-model adversary circularity (NEW in v2).** The Claude constructor shares a family with the Claude reviewer. A Claude-built specimen that fools the Claude lens is the strongest hole evidence (white-box, same-model) **but** cannot distinguish "real lens hole" from "shared blind spot." Codex-built specimens and the human ground truth are the cross-checks. Report FN/FP **by constructor family**.
- **The ΔFP/ΔFN asymmetry is real signal but confound-laden.** A cut-happy baseline structurally inflates ΔFN opportunity and starves ΔFP opportunity; per-side construction difficulty is hard to equalize. Both confounds run *against* finding over-cut (they make FP harder to demonstrate), so a tripped GATE-FP is conservative; report with bar-OFF base rates and the checkable effort units.
- **RESILIENT/CALIBRATED ceiling.** A clean ΔFN=0 (or ΔFP=0) means "the lens resists *these two adversaries'* theory," consistent with genuine robustness AND with non-transfer of the hole-models.
- **No post-hoc rescue.** In-remit scope, vector list, gates, keyings, power floors, and the 2nd- INCONCLUSIVE decision (§9) are fixed here.

## 8. Verdict rubric (per arm; first match wins) and the combined apparatus disposition

**FN arm** (ordered):

1. **INCONCLUSIVE-FN** — arm underpowered (<3 baseline-CUT-confirmed) OR per-side drops >50% OR FN-PC cut by both arms (channel un-demonstrable). *(A maximally-resistant lens that yields zero confirmable baseline-cut BAD material lands here — honestly "we couldn't pressure leniency," never a falsification.)*
2. **FALSIFIED-LENIENT** — GATE-FN trips. The "never lenient" claim is overturned. **Mandates** a gated `agent-facing-design` fix to name and close the disguise(s).
3. **BOUNDED-LENIENCY** — >=1 bar-specific FN but below GATE-FN. A real but disguise-specific hole; map it; a fix is a separate gated decision.
4. **RESILIENT** — 0 bar-specific FN, arm powered. The lens resisted this leniency attack (reported with the §7 ceiling).

**FP arm** (ordered):

1. **INCONCLUSIVE-FP** — arm underpowered (<3 baseline-KEEP-confirmed) OR per-side drops >50% OR FP-PC kept by neither arm.
2. **OVER-CUT-CONFIRMED** — GATE-FP trips. The lens over-cuts legitimate forcing functions a no-lens reviewer keeps. **Mandates** a gated `agent-facing-design` fix to sharpen the provoking/substitutive boundary (the over-cut direction the arc keeps surfacing — test 3 home-cut, GOOD1).
3. **BOUNDED-OVERCUT** — >=1 bar-specific FP but below GATE-FP. A real but disguise-specific over-cut; map it; a fix is a separate gated decision.
4. **CALIBRATED** — 0 bar-specific FP, arm powered. The lens does not over-cut genuine structure beyond the baseline (corroborates test 1's net-protective finding against engineered FP attack).

**Combined apparatus disposition.** The apparatus stays **UNCHANGED** unless **FALSIFIED-LENIENT** or **OVER-CUT-CONFIRMED** — either of which **mandates a gated fix** (routed through the `agent-facing-design` minimalism gate; the fix is itself scrutinized; per the charter, a *rule/contract* change, not an experiment-result ledger entry). **This is the first test in the arc whose result can mandate an apparatus change** — flag prominently. If both arms land INCONCLUSIVE/RESILIENT/CALIBRATED, the apparatus stays unchanged (matching tests 1–4) and §9's accumulation read applies.

## 9. What a 2nd empty FN channel means — decided up front (no post-hoc spin)

If the FN arm lands **INCONCLUSIVE or RESILIENT a second time** even with whole-section specimens and cross-family-certified badness, the honest, pre-registered read is: **leniency is not constructible against an opus reviewer applying this lens — across three independent probes (v1 reviewer-side, v1 human, v2 two-family) the lens never under-defends genuinely-bad structure relative to the baseline.** This is **non-fatal and cumulatively strong**, NOT a failure. Combined with a **populated FP arm**, the settled arc finding becomes: **the lens's error mode, if any, is over-cutting (FP), never leniency (FN).** v2's both-arms design is what converts a third empty FN channel from "frustrating" into "conclusive by accumulation." Do **not** upgrade an empty FN arm to a soft pass, and do **not** re-open the leniency question without a *new* construction lever beyond whole-section (none is currently known).

## 10. Execution notes

1. **Seal** this prereg (commit; record SHA + bar-ON/bar-OFF commits + the **verbatim certifier, reviewer, and both constructor prompts** in a hashed committed file + the **sealed filler-library slice**; Codex-leak-check the certifier/ground-truth text so it carries no lens tell). 2. Both constructors cold-build their pools (§4) + hidden intent logs; effort in checkable units. 3. Realism-gate (blind, logged). 4. **Cross-family badness pre-cert (§2.2) → fix the reviewer corpus to cross-family-agreed specimens + PCs + floors + filler.** 5. Build the shuffled corpus (neutral filenames `cand-NN.md`/`review-contract-1|2.md`; sealed arm + unblinding maps kept OUT of `/tmp`, in the run dir). 6. Run bar-ON/bar-OFF hermetic Claude reviews (3 reps, escalate splits) via `review-workflow.js`; blind disposition judge extracts CUT/RESHAPE/KEEP/SILENT (human audit subset); blind in-remit + lens- attribution rulings. 7. **Human ground-truth arm** on the preserved blind packet (fresh judge; honor the blinding guard — never narrate apparatus state into any channel a current/potential judge can see until calls are recorded); secondary Codex ground-truth check (non-gating). 8. Transcript tell-check.
   9. Score §§5,8 under both keyings; write the results doc citing this SHA.
- **Single-variable lock:** bar surfaces frozen = `skills/agent-facing-design/SKILL.md` (`## Two Kinds of Skill`) + `plugins/review-family/skills/scrutinize-skill/SKILL.md`. Record both bar-ON (seal) and bar-OFF (`8b9cfc1`) SHA-256 in the seal file (reuse `extract-configs.sh`). bar-ON surfaces MUST match the apparatus-unchanged hashes (`70037a32…` agent-facing-design / `7545f4ca…` scrutinize-skill from the test-4/test-5 seals) — verify at seal time.
- **Codex invocation that works** (from v1 `run-prefilter.sh`): `codex exec --sandbox read-only -C /Users/jp/.agents -c model_reasoning_effort=medium --output-schema <schema.json> -o <out.json> "<INLINED prompt>"`. Codex hangs if told to read files — ALWAYS inline content, forbid tools, batch ~10 items/call. Default model gpt-5.5.
- **Workflow caveats:** `args` arrive as a STRING (`const X = typeof args === 'string' ? JSON.parse(args) : args`); the workflow SCRIPT has no filesystem access but spawned AGENTS can Read files — stage a neutral kit and point agents at it. </content> </invoke>
