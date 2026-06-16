# Judgment/Trust Flip-Set — Acceptance Results (Task 9)

Durable, replayable record of the blind triplicate acceptance test for the
judgment-vs-trust apparatus change
(`docs/plans/2026-06-15-judgment-trust-apparatus.md`, Task 9). Pairs with the
blind fixture (`judgment-trust-flip-set.md`) and the sealed key
(`judgment-trust-flip-set-key.md`). This file is the merge gate Task 8 made the
branch depend on.

## Final verdict: **FAIL — branch not merge-ready**

- **Hard fail:** Row 7 (grill-me, the leniency tripwire) — 2 of 3 independent
  clean reviewers **raised then dropped** the softened-adversarial-posture
  concern; only 1 kept it (at Minor). The pass condition is explicit:
  raised-then-dropped on row 7 is a leniency FAIL.
- **Not yet proven:** Row 1 (scrutinize) — a **bar-classification divergence
  with teeth**: the "section-name divergence" half has a *legitimate* trust
  reading (a reusable template that drifted out of sync with the contract,
  confirmed live), so reviewers split judgment/trust and 2/3 kept it as a
  downgraded Minor rather than dropping it.
- **Lands as predicted (7 of 9):** Rows 2, 3, 4, 5, 6, 8, 9.
- **Diagnosis:** The apparatus *discriminates correctly*; the two non-landing
  rows are **fixture-construction problems** (borderline / compound cases that
  violate the key's own construction rule), not apparatus leniency. See
  **Diagnosis** and **Remediation** below. Per Task 9, the pass condition was
  **not** weakened to force a pass.

## Provenance

- **Loaded `review-family` version:** `0.3.10` (Task 5/6). Preflight (this fresh
  session): branch `feature/judgment-trust-distinction`; HEAD `0e76b1e` (the
  Task 10 commit, one past the Task 8 checkpoint `3eb0e74` — both apparatus
  commits present, expected); `scripts/codex-plugins-sync.sh --check` exit 0, no
  source-vs-cache drift; `grep -c "Bar And Execution Quality"
  plugins/review-family/skills/scrutinize-skill/SKILL.md` → `1` (loaded rubric
  carries the Task-4b bar step).
- **Runtime / session that loaded the edited skill:** Claude Code, fresh session
  (date 2026-06-16). To guarantee the *edited* rubric was applied (SKILL.md
  edits load next session), every reviewer was instructed to **read the
  working-tree source in full and apply it** —
  `plugins/review-family/skills/scrutinize-skill/SKILL.md` plus
  `skills/agent-facing-design/SKILL.md` ("Two Kinds of Skill") — rather than
  relying on the subagent skill-loader. The working tree is the live Claude
  source, so this is the post-edit state.
- **Method:** Two background workflow runs of fresh, independent subagent
  reviewers, each producing a structured review (bar classification stated
  *before* findings; every concern recorded as `raise-and-keep`,
  `raise-and-drop`, or — by absence — `not-raised`).
  - **Run 1** (`wf_bdc8f6c5-3ff`): 27 reviewers = 9 rows × 3. Row 4 reviewed its
    four siblings as a group.
  - **Run 2** (`wf_484b6b1c-788`): a **blindness-locked clean re-run** of rows 4
    and 6 only (6 reviewers), same unchanged 0.3.10 rubric — see
    **Methodological breach** below.
- **Withheld from every reviewer's context** (never pasted): the source report
  (`.agents/skill-library-scrutiny-2026-06-15.md`), the blind fixture, the
  sealed key, and the plan file. The orchestrator read these only to assemble
  reviewers and to diff after dispositions were recorded.

## Methodological breach (Run 1) and the clean re-run

Run 1 gave reviewers filesystem access for the Evidence-Floor sibling scan but
did **not** fence off `docs/plans/`. Three reviewers self-served withheld
material during directory scans (the orchestrator never pasted it, but
"withheld from context" was nonetheless violated):

| Reviewer | Read | Effect |
|---|---|---|
| row4 rev3 | the **plan file** (embeds the key) | contaminated |
| row6 rev1 | the **sealed key** directly | contaminated |
| row4 rev2 | the **Task-10 retriaged backlog** (derived dispositions) | contaminated |
| row6 rev3 | the **Task-10 retriaged backlog** | contaminated |

Containment, verified by a marker scan of all 27 serialized reviews: the breach
is confined to **rows 4 and 6** — both unanimous-PASS rows. **Rows 1, 2, 3, 5,
7, 8, 9 are 100% clean**, so the row-7 FAIL and the row-1 not-yet-proven verdict
rest entirely on uncontaminated reviewers.

**Remediation:** Run 2 re-ran rows 4 and 6 with a strict source boundary
(forbid reading anything under `docs/`, or any file named `*scrutiny*`,
`*flip-set*`, `*backlog*`, `*retriaged*`, `*judgment-trust*`; confine scans to
skill bundle directories). All 6 re-run reviewers verified clean. Rows 4 and 6
are scored on the Run-2 clean reviewers (plus the one already-clean Run-1
reviewer each, noted). **Fix for future runs:** the reviewer prompt must carry
the source boundary by default.

## Per-row dispositions and bar classifications

Disposition legend: **K** = raise-and-keep, **D** = raise-and-drop, **N** =
not-raised. Bar legend: **J** = judgment, **T** = trust, **PP** = per-part /
mixed. `*` marks a contaminated Run-1 reviewer (superseded by Run 2 for rows
4/6). Bar shown is the reviewer's classification of the row's concern.

| # | Skill | Key class | Expected | rev1 | rev2 | rev3 | Lands? |
|---|---|---|---|---|---|---|---|
| 1 | scrutinize | J | DROP | K·Minor (PP, "trust-flavored") | **D** (T) | K·Minor (J labels / T casing) | **NOT YET PROVEN** (bar divergence) |
| 2 | system-design-review | J | REVERSE | D (J) | N (J)¹ | D (PP) | **PASS** |
| 3 | tdd | J | REVERSE | N (—) | N (—) | N (—) | **PASS** |
| 4 | merge-branch ×4 | T | KEEP+ESC | K·Major (T) | K·Major (T) | K·Minor→mod (T) | **PASS** (Run 2 clean; +Run-1 rev1 clean K·Major) |
| 5 | search-handoffs | T | KEEP | K·Minor (T) | K·Minor (T) | **D** (T) | **PASS** (2/3 keep) |
| 6 | gh-pr-review-loop | mixed | SPLIT | per-part, kept trust lifecycle bug; no output-shape demand | per-part; no output-shape demand | per-part; no output-shape demand | **PASS (mechanism)**; `@codex` KEEP borderline |
| 7 | grill-me | J | KEEP/ESC | **raised → D** | **raised → D** | **raised → K·Minor** | **FAIL (leniency tripwire)** |
| 8 | claude-code-docs | T (lookup) | KEEP/ESC | K·Minor×3 (T) | K·Major×2+Minor×2 (T) | **D** (T) | **PASS (bar)**; wrong-bucket premise refuted live |
| 9 | outcome-interviewer | J (over-cut) | DO NOT FLAG | no over-cut (rhythm=J, kept) | no over-cut | no over-cut | **PASS** (no over-cut) |

¹ Row 2 rev2 raised a *different* structure concern (8-category screen) and did
not demand completing the cap rule; on the cap rule itself: not-raised.

### Per-row diff against the sealed key

- **Row 1 — DROP (judgment).** Reviewers split. rev2 dropped it (matches). rev1
  and rev3 kept it as an explicitly-cosmetic, non-blocking **Minor**, and **2/3
  classified the section-name half as trust-flavored** ("a reusable template
  whose value is a predictable, single-sourced shape"). Live check confirms the
  reviewers are right that a *real* trust seam exists: section labels drift
  across `scrutinize/SKILL.md:136` (`Real-World Breakpoints`, `Hidden
  Dependencies`, `Required Changes`) and the reusable
  `references/review-format.md:44/47/53` (`...And Edge Cases`, `...Or
  Bottlenecks`, `...Before This Is Credible`). No reviewer **escalated** it —
  the anti-over-flag goal held — but the key's uniform "judgment" label
  under-determines the bar, so the bar-divergence teeth fire: **not a clean
  pass.** Diagnosis: row is **compound** (judgment-cosmetic casing + trust
  template-drift), violating the construction rule's "verdict reproduces under
  one bar" standard.
- **Row 2 — REVERSE (judgment).** Matches in substance. **No reviewer asked to
  "complete the low/med/high rule"** (the pre-edit over-flag is gone); all three
  instead evaluated the numeric finding-caps under the judgment lens (substitutive
  quota vs. provoking prioritization) and reasoned about them. The reversal — stop
  completing a conformance rule, start questioning whether the structure belongs —
  occurred. PASS.
- **Row 3 — REVERSE (judgment).** Clean. **No reviewer flagged the absence of a
  mandated output shape / closure as a defect**; all correctly read the
  checklists as provoking, not substitutive. The one finding raised (rev1:
  checklist duplication) is a genuine trust-side drift concern, correctly
  classified. PASS.
- **Row 4 — KEEP + ESCALATE (trust).** Clean and robust. Across 4 clean
  reviewers (Run-2 ×3 + Run-1 rev1), **all keep** the hand-copied protected-branch
  gate as a **trust** defect; 3/4 at **Major**, with live `grep`/`rg` evidence of
  real drift (git-hygiene omits `develop`/`release/*`). PASS.
- **Row 5 — KEEP (trust).** 2/3 keep the unset-`$PROJECT_ROOT` snippet as a
  **trust** reliability gap; rev3 dropped it on the defensible ground that the
  "Project root resolution" prose (lines 22-26) tells the agent how to resolve
  it. All three applied the trust bar; majority keep. PASS.
- **Row 6 — PER-PART SPLIT (mixed).** The load-bearing mechanism passes: **all
  clean reviewers classify per part** (publish lifecycle = trust; thread
  assessment = judgment/delegated), **none demand a fixed output shape on the
  judgment part** (the classify-all-trust failure did not occur), and **each
  keeps a real trust lifecycle bug** (restated-stop-condition drift /
  no partial-publish recovery / non-idempotent replies — the classify-all-judgment
  failure did not occur). Nuance: the *specific* `@codex review` hardcode KEEP is
  **borderline** — kept by 1 of 4 clean reviewers (Run-1 rev2, Major) and
  dropped/not-raised by the other 3, who treated it as home-repo-acceptable. The
  per-part *mechanism* — what row 6 exists to prove — holds. PASS.
- **Row 7 — KEEP/ESCALATE (judgment), the tripwire — FAIL.** All three clean
  reviewers **surfaced** the provoke-dilution concern (the rubric made them look),
  but 2 of 3 **dropped** it after careful reading (rev1: the "shared
  understanding" goal does not dilute given "relentlessly / every aspect / each
  branch"; rev2: the "recommended answer" is paired with, not a substitute for,
  the forcing functions). rev3 **kept** it (Minor). Pass condition: raised-then-
  dropped is a leniency FAIL; "raised and kept/escalated by the independent
  reviewers" is not satisfied at 1/3 keep. **FAIL.** (Not "unanimous silence" —
  the concern was raised by all three.)
- **Row 8 — KEEP/ESCALATE (trust, mechanical/lookup).** The load-bearing point
  passes: **all three classify claude-code-docs as a trust/lookup skill** and
  apply the trust bar — none mis-sorts the tail as "not a real skill / outside
  both bars." 2/3 keep real trust reliability defects (stale category list,
  missing `dump_index_metadata`, redundant alias map as drift). Nuance: the
  *specific* row-8 premise (alias rewrites valid enum values → silent
  **wrong-bucket** retrieval) was **refuted by the reviewers' live checks** —
  the server accepts the aliases natively, so the map is *redundant*, not
  wrong-bucket. The reviewers kept other real trust defects instead. Bar:
  correct and unanimous. PASS (with the source-report premise correction noted).
- **Row 9 — DO NOT FLAG (judgment, over-cut probe).** Clean. **No reviewer
  raised a substitutive-structure / "cut the interview rhythm" finding**; all
  three explicitly considered the structure (twelve sections, six-field brief,
  one-question rhythm) and recognized it as organizing/eliciting, dropping the
  over-cut concern. The only findings raised were a legitimate trust/routing gap
  (missing grill-with-docs handoff), unrelated to the rhythm. No over-swing from
  over-flagging into over-cutting. PASS.

## Discrimination checks (Task 9, checks 1–6)

1. Rows 1–3 drop/reverse, surfacing structure-vs-thinking instead — **2 and 3
   yes; 1 partial** (no escalation, but kept-as-Minor + bar divergence).
2. Row 7 raised-then-kept across the three — **FAIL** (2/3 raised-then-dropped).
3. Rows 4–5 keep/escalate (trust) — **yes** (row 4 robust; row 5 majority).
4. Row 6 splits per part — **yes** (mechanism); `@codex` KEEP borderline.
5. Row 8 keeps/escalates as trust/lookup — **yes on the bar**; specific premise
   refuted live, other trust defects kept.
6. Row 9 draws no over-cut finding — **yes**.

## Diagnosis: the apparatus discriminates; rows 1 and 7 are fixture defects

The apparatus is doing its job. Across the clean reviewers it produced correct
per-bar behavior on 7 of 9 rows: it stopped over-flagging conformance (rows 2,
3, and the no-escalation half of row 1), kept and escalated trust defects (rows
4, 5, 8), classified the mixed skill per part without demanding trust-shape on
its judgment part (row 6), and resisted over-cutting legitimate organizing
structure (row 9). On row 7 it even made every reviewer *surface* the
softened-provoke concern — the provoke-side text is reaching reviewers.

The two non-landing rows fail the key's **own construction rule** ("only findings
clear enough that the verdict reproduces under judgment belong here; borderline
provoke-vs-substitute cases are deliberately excluded"):

- **Row 1 is compound.** "Verdict-token casing" is clean judgment-cosmetic, but
  "section-name divergence with the reusable `review-format.md` template" is a
  *real* trust-flavored single-sourcing/drift seam (live-confirmed). The verdict
  does not reproduce under a single bar; reviewers correctly read two bars.
- **Row 7 is borderline.** grill-me's softening ("shared understanding",
  "recommended answer") is real but is outweighed by the dominant adversarial
  framing ("relentlessly about every aspect", "walk down each branch", "the
  single weakest remaining assumption"). Reasonable reviewers split.

**Why row 7 is borderline, not apparatus leniency** (adversarially checked):
(a) rev3 *kept* it — the rubric can make a reviewer keep a provoke defect, so
this is not "drop-everything" leniency; (b) the two droppers gave substantive,
text-specific reasoning, not reflexive hand-waving; (c) on rows 6 and 9 the same
class of reviewers discriminated correctly (did not reflexively drop judgment
findings; did not over-cut); (d) the source report independently logged grill-me
under "zero confirmed material findings" and the softening as Minor. The key
itself flagged row 7 as "a deliberately sharpened edge case." The reproduction
test it was meant to survive — does the verdict reproduce under independent
judgment? — it did not.

A caution recorded honestly: declaring the tripwire "borderline" is exactly the
move the plan warns can hollow out the leniency test, so the remediation must
*replace* the tripwire with a clearer, reproducible softened-provoke case (or
sharpen the apparatus), **not** delete it or relax row 7's KEEP requirement.

## Remediation (pending — see decision raised with the user)

Per Task 9, a non-landing row is a real finding to fix without weakening the
pass condition. The plan offers two paths and pre-commits row 7 to the first
("sharpen the provoke side, do not weaken the row"); the evidence here points to
the second ("the flip-set row violated the construction rule — repair it and
note why"). Because the two paths change *different* contract surfaces (the
apparatus text + a plugin version bump/republish vs. the fixture + key + a
re-run) and the user's own plan-nudge and construction-rule now conflict, the
direction was raised with the user rather than chosen unilaterally.

- **Row 7:** either (a) sharpen the provoke-side text in `agent-facing-design`
  "Two Kinds of Skill" and `scrutinize-skill` so a softened forcing function is
  unambiguously a KEEP — risking induced over-flagging of marginal softening
  (the mirror failure row 9 guards) — or (b) replace grill-me with a clearer,
  reproducible softened-provoke case and re-run.
- **Row 1:** reclassify the row as mixed/per-part (and score the casing half
  judgment-cosmetic, the template-drift half trust), or replace it with a pure
  judgment-cosmetic conformance case with no reusable-template seam.

The branch remains **not merge-ready** until a re-run lands rows 1 and 7 as
predicted under an unweakened pass condition.

## Reproduce

- Run 1 transcript: workflow `wf_bdc8f6c5-3ff`; raw results
  `tasks/wl97sgw3t.output`.
- Run 2 (clean re-run) transcript: workflow `wf_484b6b1c-788`; raw results
  `tasks/wwg5hdmdr.output`.
