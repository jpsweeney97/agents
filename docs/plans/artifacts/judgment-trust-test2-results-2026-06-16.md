---
type: results
experiment: judgment-trust test 2 — human cold-judge (blind to the bar)
project: agents
design: judgment-trust-test2-human-coldjudge-design-2026-06-16.md @ 9f34f69 (protocol + scoring + sealed limits)
sealed_key: test2-corpus/sealed-key.md (opened only AFTER all 14 answers were transcribed)
packet: .agents/scratch/test2-run/blind-packet-shuffled-2026-06-16.md (5197 bytes; md5 fd633222056762bc602eca373b2f850a; byte-identical to the phone copy)
answer_source: /Users/jp/scratch-workspace/skill-stuff/blind-packet-answered-2026-06-16.md
judge: software/design professional (experienced engineer/designer, not an AI-skill-design specialist); identity not separately recorded; administered WHOLE-PACKET (all 14 Elements visible at once), NOT one-at-a-time — see § Integrity and § Sealed limits
scoring: 3 independent Claude scorers (diverse lenses) + 1 transcription/map verifier + 3 adversarial refuters (wf_9e36986c-30f)
verdict: PASS — a bar-naive human expert agrees with bar-ON on 12/14 (contested 6–7/9); the finding-cap resolves toward DEFEND; calibration holds under the design's pre-registered reasoning-over-label rule; every disagreement is over-cut, never lenient
---

# Results — test 2, human cold-judge (blind to the bar)

A human, blind to the bar and its judgment/trust vocabulary, gave a 3-way call (keep-as-is / change-it
/ remove-it) + one sentence of reasoning on each of 14 anonymized skill-design choices. The element
key and bar-ON calls were sealed in `test2-corpus/sealed-key.md` and opened **only after every answer
was transcribed**. This is the **correctness anchor** of the 5-test menu: the one test escaping **both**
the authorship confound and same-model circularity (the C1 limit tests 1 & 3 cannot escape).

## Verdict: **PASS — the bar tracks blind expert judgment, and where it errs it errs strict**

- **The cap (item 1) — the headline — resolves toward DEFEND.** The human keeps the system-design-review
  finding-cap (lenses + report top-N, not exhaustive) as-is. Per the sealed key, human KEEP = test-1's
  anonymized DEFEND (2/3) was right and **test-3's home-named CUT (3/3) was the over-cut.** The standing
  frontier question — *does the bar over-cut the finding-cap?* — answers **no; the cap is legitimate.**
- **Calibration holds** under the design's pre-registered *reasoning-over-label* rule: all **5/5**
  control items agree with the bar by their reasons (unanimous across 3 independent scorers).
- **Direction is one-signed: over-cut only, zero leniency.** The human never removed anything the bar
  kept. Every human↔bar disagreement is the human **keeping** a structure the bar **cut**.
- **Overall agreement 12/14** (contested 6–7/9 depending on the change-mapping; controls 5/5).

Two honest caveats carried throughout (both surfaced by the adversarial pass and neither overturns the
verdict): the human cast **zero "remove" votes**, so *label-strict* calibration is weak and the result
rests on the design's "reasoning matters more than the label" rule; and **n = 1** — this is a
tie-breaker and a direction signal, not a population estimate.

## Integrity — what was verified before the key was opened

- **Packet binding: PASS.** All 14 element bodies in the answered file are **byte-identical**
  (whitespace-normalized) to the administered packet (`blind-packet-shuffled-2026-06-16.md`, 5197 bytes,
  md5 `fd633222…`, itself byte-identical to the phone copy). The unblinding map is therefore valid for
  what the human answered.
- **The "choice-not-skill" clarifier WAS added.** The administered preamble adds one framing-neutral
  sentence — *"Your call is about this choice, not the whole skill."* — the line flagged as an open
  question in the resume handoff. It reveals nothing about the bar, the categories, or which element is
  special; scoring is against the as-administered packet.
- **Transcription: PASS.** An independent verifier confirmed every Element→item mapping, every call, and
  every reason against the source files (only curly-vs-straight quote typography differs).
- **Calibration-set discrepancy: RESOLVED against the sealed key.** The key's partition is
  **CTRL-CUT = {4, 9} (expect remove), CTRL-KEEP = {3, 10, 12} (expect keep); contested = {1,2,5,6,7,8,11,13,14}.**
  This **vindicates the resume-handoff summary, not the design doc's "items 10–14" prose** (two scorers
  flagged this independently). Cause: item order was de-clustered after the Codex blinding leak-check; the
  design doc's Scoring § was written against the pre-de-clustering numbering and never updated. The key is
  authority.
- **Judge & administration (confirmed by the user; the file records neither).** The judge is a
  **software/design professional** (experienced engineer/designer, not an AI-skill-design specialist) — a
  strong signal on the API/release/dependency items, a moderate one on the skill-design-specific framing.
  The packet was **read as a whole (all 14 Elements visible at once), NOT administered one-at-a-time** — so
  the design's **primary blinding defense (one-item-at-a-time + shuffle) was not in force**, and the
  de-clustering (no-adjacent-same-Job) constraint is moot. This is a real protocol deviation; its impact is
  bounded and analysed in § NEW finding (the relocated over-cut) and § Sealed limits — it weights down **one** finding
  (item 7) and leaves the cap and calibration robust.

## The mapped result (human blind to every column but "Human call + reason")

| Item | El | Skill (anonymized) | Category | bar-ON | Human call | Score |
|---|---|---|---|---|---|---|
| **1** | C | **system-design-review finding-cap** | **CONTESTED — cap** | **DEFEND 2/3** | **keep-as-is** | **AGREE → DEFEND** |
| 2 | H | qa-4 (stop once report actionable) | contested | DEFEND | keep-as-is | agree |
| 3 | D | design-interface-2 (parallel options) | CTRL-KEEP | DEFEND | change-it | agree (keep-aligned) |
| 4 | I | release-readiness (checklist = verdict) | CTRL-CUT | CUT 3/3 | change-it | agree (cut-aligned) |
| 5 | E | mcp-builder (~10 eval Qs) | contested | leaned keep | change-it | agree (keep-aligned)* |
| 6 | A | frontend-design-2 (color/type quotas) | contested | DEFEND | change-it | agree (keep-aligned) |
| **7** | N | **design-interface-1 (pre-design question list)** | contested | **CUT 2/3** | **keep-as-is** | **DISAGREE — over-cut** |
| 8 | K | teach-3 (lesson = numbered file) | contested | CUT 2/3 | change-it | agree (cut-aligned)* |
| 9 | M | evaluate-dependency (score band = verdict) | CTRL-CUT | CUT 3/3 | change-it | agree (cut-aligned) |
| 10 | F | qa-1 (structured bug report) | CTRL-KEEP | DEFEND 3/3 | keep-as-is | agree |
| 11 | B | request-refactor-plan ("in depth") | contested | CUT 2/3 | change-it | agree (cut-aligned) |
| 12 | L | frontend-design-1 (plan→self-critique) | CTRL-KEEP | DEFEND 3/3 | change-it | agree (keep-aligned) |
| **13** | J | **teach-5 (equal-length quiz answers)** | contested | **CUT 3/3** | **keep-as-is** | **DISAGREE — over-cut** |
| 14 | G | design-interface-3 (common write-up structure) | contested | DEFEND | keep-as-is | agree |

\* Mapping-sensitive items (see § The "change it" phenomenon). Across 3 independent scorers, items 4, 9,
11 were unanimously **cut-aligned**; 3, 6, 12 unanimously **keep-aligned**; item 8 was cut-aligned by 2/3
(one scorer flagged a keep-leaning read); item 5 was keep-aligned by 2/3 (one scorer marked it ambiguous).

## Calibration check — controls (key partition: CUT {4,9}, KEEP {3,10,12})

**Verdict: HOLDS (5/5) — unanimous across all 3 scorers, under the design's reasoning-over-label rule.**

- **CTRL-CUT, items 4 & 9 (the two seeded substitutives):** the human said **change-it**, not "remove" —
  but the *reason* independently reproduces the bar's exact substitutive objection. Item 4: *"a readiness
  checklist should **inform** the ship decision, **not equal it**."* Item 9: *"weighted scoring helps… but
  adoption needs **non-compensable gates**."* Both attack precisely the *completion/score-total = the
  verdict* defect the bar cut. **Cut-aligned → agree.**
- **CTRL-KEEP, items 3, 10, 12:** item 10 is a clean keep; items 3 and 12 are change-it calls that
  explicitly endorse the core structure ("valuable", "good") and only add a refining qualifier
  (simplest-baseline option; distinguish clichés from useful conventions). **Keep-aligned → agree.**

**The label-strict floor (stated honestly).** The human cast **zero removes** across all 14 items, so by
the *pre-registered binary* keep/remove rubric the human produced no exact "remove" token on either
CTRL-CUT item — at the label level only **1 of 5** controls (item 10) is a clean match. Calibration is
therefore "confirmed under reasoning," not "confirmed under labels." This is licensed because the design
doc itself pre-registered **"reasoning matters more than the label"** (design § Protocol, line 44), and
because the human **discriminated**: he kept other rigid/mechanical structures (items 1, 10, 13, 14) and
flagged only the *verdict=structure* substitutives (4, 9) — so the change-it calls track the substitutive
property specifically, not mere mechanicalness. That discrimination is the real calibration signal.

## The cap (item 1) — decided outright

The blind human **keeps** the finding-cap, reasoning *"a lens-based review that reports the top findings
is exactly how to make architecture feedback usable, **provided the omitted scope is clear**."* Per the
sealed key, human-keep here means **test-1's anonymized DEFEND (2/3) was correct and test-3's home-named
CUT (3/3) was the over-cut.** The apparatus's own two runs disagreed and so could not adjudicate
themselves; the cold human breaks the tie **toward DEFEND.** The cap is a genuine focusing structure, not
substitutive.

Two facts strengthen this against the obvious objections: (a) the human independently names the cap's
*legitimacy condition* (scope disclosure), which is the correct guardrail, not a hedge that flips the
call; and (b) any residual blinding leak would bias a naive judge toward **cutting** a mechanical-looking
cap — so the keep cuts **against** the leak, not with it.

**Scope (per the adversarial pass):** call this a **weighted-down, conditional, directional tie-breaker
favoring DEFEND**, not a strong "resolution." The key itself (line 39) calls n=1 a tie-breaker; the keep
is conditional on scope transparency; and under a label-strict reading of the controls one would weight
contested results (the cap included) down. The **direction** is robust; the **strength** is one judge.

## Contested aggregate & direction

- **Agreement 6–7/9** on the contested set. Robust agrees: items 1, 2, 6, 14 (+ 11 cut-aligned). Swing:
  item 5 (keep-aligned by 2/3; ambiguous by 1) and item 8 (cut-aligned by 2/3). Under the harshest
  defensible mapping the floor is ~5/9; under the most charitable, 7/9. **No reading produces a lenient
  disagreement.**
- **Direction = over-cut only (unanimous).** Every clean disagreement is the human **keeping** a structure
  the bar **cut** (items 7, 13). There is **zero** "human-remove where bar-defended" — no leniency evidence
  anywhere.

## NEW finding — the over-cut is relocated, not absent

Test 1 (foreign material) found the bar **net-protective** and produced no genuine consensus over-cut.
Test 2 (the human anchor) finds the bar **did over-cut two specific contested structures** — and they are
**not** the cap:

- **Item 7 — design-interface-1, a short pre-design question list** (problem / caller / operations /
  constraints / hide-vs-expose). Bar CUT 2/3; the human keeps it outright: *"cheap, and prevents most
  wrong-shape designs."*
- **Item 13 — teach-5, equal-length quiz answer options.** Bar CUT 3/3 (its most confident contested cut);
  the human keeps it outright: *"a simple, low-cost guard against accidental test-taking cues."*

These are deliberate **keeps** (not the human's modal "change"), they survived adversarial refutation, and
by the sealed key's own pre-registered interpretation a human-keep on a bar-cut item **is** direct over-cut
evidence. So the over-cut question is **not closed — it is moved off the cap and onto items 7 and 13**: the
bar, applied by a fresh reviewer, can over-cut cheap legitimate guards. Bounded by n=1 over two items.

**Whole-packet caveat — weight item 7 down, not item 13 or the cap.** Because the judge read all 14 at once
(§ Integrity), same-**Job** items were simultaneously visible. **Item 7** shares its Job ("design a
software interface/API") with items 3 and 14, **both of which the human kept** — so his keep on 7 may be
partly cross-item consistency rather than an independent over-cut signal; weight it down. **Item 13** is
more robust: the human **discriminated** within the teaching pair (kept 13, changed 8), which a blanket
same-domain heuristic would not do. And the **cap (item 1) has a unique Job** in the packet, so no same-Job
neighbour can have contaminated it. Net: the over-cut signal rests most safely on **item 13**; **item 7** is
corroborating-but-confounded; the **cap result is untouched** by the administration deviation.

## The "change it" phenomenon (a finding in its own right)

The human's **modal call was "keep or refine, never remove"**: 7 keeps, 7 changes, **0 removes** across 14
items. A bar-naive expert treated essentially **no** structural choice as outright removable. This
independently **vindicates the bar's protect/defend default** — and it also explains the bar's only error
mode: where the human says *"change/refine,"* the bar sometimes says *"cut,"* and on items 7 and 13 the
human won't even change — just keep. The bar's residual miscalibration, judged against the correctness
anchor, is a **mild strictness bias on contested structures**, never leniency.

## Adversarial verification — all three load-bearing claims survived (narrowed)

Three refuters each tried hard to break a headline claim (wf_9e36986c-30f, Verify phase). None was
decisively refuted; each was narrowed:

1. **Cap → DEFEND.** Survives as a *conditional, weighted-down, n=1 directional* signal (not a strong
   "resolution"). The KEEP is real and on-target, the key interpretation is applied correctly, and the keep
   cuts against (not with) any blinding leak.
2. **Over-cut on items 7 & 13.** Survives. The two keeps are deliberate positive endorsements (the human
   used "keep" only where he endorsed, and discriminated by changing the other bar-cut items 8, 11) — not a
   keep-everything reflex or a blinding artifact. Items 8, 11 correctly **excluded** from the over-cut count.
3. **Calibration holds + zero leniency.** Survives **under reasoning, not labels** — explicitly scoped: by
   the binary rubric the human emitted no "remove" token on the CTRL-CUT items, so this is a reason-level
   pass. The zero-removes / over-cut-only direction is robust; the leak confound is defused by the human
   keeping other mechanical structures.

## Sealed limits (carried into any downstream use)

- **n = 1** — a tie-breaker and direction signal, not a population estimate. More judges strengthen it.
- **Whole-packet administration (confirmed) — the primary blinding defense was bypassed.** The judge read
  all 14 Elements at once rather than one-at-a-time, so the contrast set the design tried to deny was
  available and the de-clustering constraint is moot. Two things bound the damage. (1) The *cross-item
  theory-reversal* failure mode this defense guards against **did not manifest**: the human kept mechanical
  structures (cap 1, bug-report 10, quiz-answers 13, write-up 14) and cut/changed only on the *substitutive
  verdict=structure* property — the opposite of a blanket "mechanical = suspect" heuristic — and he
  discriminated within same-domain pairs (kept 13, changed 8). (2) Same-**Job** influence remains possible
  for any item with a same-Job neighbour on the page; this **specifically bounds item 7** (§ NEW finding —
  the relocated over-cut), while the **cap (item 1) has a unique Job** and is unaffected. The judge being a
  **software/design professional** (not a skill-design specialist) makes the engineering-item calls (API,
  release, dependency) the strongest part of the signal and the skill-design framing the weakest.
- **Label/scale mismatch.** The human used a 3-way scale dominated by "change it" (9/14 counting both
  middle reads); the sealed key's interpretation column is binary (keep/remove). Every "change" required a
  reason-read; the result is reported under multiple mappings and is direction-robust, count-sensitive.
- **Blinding is good, not perfect** (faithfulness floor, per design): bar-ON vocabulary self-identifies and
  contested items read as their genuinely-contested feature; this residual was accepted at design time.

## Apparatus decision — UNCHANGED (gated)

Per protocol, the apparatus stays unchanged unless the result demands it (a separate, gated decision). It
does not, here:

- The cap result **confirms the live library**, which already keeps system-design-review's finding-cap; no
  edit follows. Test-3's home cut was a fresh-reviewer probe, never a library change.
- The over-cut on items 7 & 13 concerns the **bar's behavior on the test corpus**, not a needed edit to any
  shipped skill. It is logged as the **live open question** (relocated from the cap). A future refinement to
  the *provoke* side — "do not cut cheap, low-cost guards / pre-design question lists" — is a candidate, but
  it is **n=1** and explicitly **gated**: do not adjust the apparatus on this alone.

## What test 2 proves — and does not

**Proves (the menu's correctness anchor, first time):** the bar's calls **agree with a blind, bar-naive
human expert** at 12/14 with calibration holding; the **finding-cap should be kept** (resolving the
test-3/test-1 self-disagreement toward DEFEND); and the bar's only detectable error mode against the human
is **over-cutting, never leniency.** Combined with test 3 (LOAD-BEARING) and test 1 (CALIBRATED on foreign
material), the apparatus now has an external correctness check, not just internal/contrast ones.

**Does not prove:** a population-level agreement rate (n=1); that the over-cut on items 7 & 13 is a general
property vs. two single-judge data points; or anything about the bar applied by a *different model* (still
Claude-as-reviewer by design — test 1 §9's Codex-reviewer arm remains the portability check). The
correctness anchor is now planted; widening it (more judges; tests 4 "actually cut something then use it"
and 5 "red-team") is the remaining frontier.
