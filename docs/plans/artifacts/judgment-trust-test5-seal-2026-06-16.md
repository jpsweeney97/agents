---
type: seal-record
experiment: judgment-trust test 5 — adversarial red-team
project: agents
seal_commit: "7869892 (the prereg commit — judgment-trust-test5-redteam-prereg-2026-06-16.md)"
bar_on_ref: "7869892 (lens PRESENT: ## Two Kinds of Skill in agent-facing-design + scrutinize-skill step-3/severity rules)"
bar_off_ref: "8b9cfc1 (= 3eb0e74^; pre-lens baseline; same single-variable baseline as tests 1 & 3)"
constructor_model: "gpt-5.5 / Codex (white-box adversary), model_reasoning_effort=medium"
ground_truth: "HUMAN (sole authority on every scored FN-arm specimen); Codex >=3 reps = non-gating pre-filter"
reviewer_model: "claude-opus-4-8 (bar-ON and bar-OFF arms, hermetic, blind, 3 reps; 5 on a 2-1 split)"
disposition_judge: "claude-opus-4-8 (different family from the Codex pre-filter) + human audit subset"
written_before: "any specimen constructed or any reviewer run — this file is committed BEFORE Phase B"
---

# Test 5 — SEAL RECORD (committed before any specimen is built)

This file discharges prereg §9 step 1: it records the seal SHA, the bar-ON/bar-OFF commits, the
**verbatim certifier and reviewer prompts**, and the **sealed filler-library slice**, in a hashed
committed file. The prereg
(`docs/plans/artifacts/judgment-trust-test5-redteam-prereg-2026-06-16.md`, commit `7869892`) is the
design authority; this is the operational lock. The prereg is **not edited** by this commit.

## 0. Single-variable lock (tamper-evident)

bar-ON = the seal commit `7869892`; bar-OFF = `8b9cfc1` (`3eb0e74^`). The **only** intended difference
is the judgment/trust LENS. Frozen bar-surface bytes, SHA-256 (verify before each run via
`.agents/scratch/test5-run/extract-configs.sh`, which pins bar-ON to `7869892` — NOT `HEAD`, so this
seal-record commit cannot drift it):

```
70037a32d07b22029e9439ebd92b692d7b22d11a45693a9032ead3a9d6a38d98  bar-ON  agent-facing-design@7869892
7545f4ca3021403f1023240f100e060ef9775c46ed23cc93e9a31faeea5e0274  bar-ON  scrutinize-skill@7869892
086e84b4a73916f98a5fed1d021f6c7552535bb952b576d83b9c2efacbe3a2ca  bar-OFF agent-facing-design@8b9cfc1
04e9f0ec462b3f728548a0573826f2286e0ed03a5e5085bbac14cc63831d3f7b  bar-OFF scrutinize-skill@8b9cfc1
```

Sanity (from the extractor): bar-ON `Two Kinds of Skill`=1, `judgment`=25; bar-OFF `Two Kinds`=0,
`judgment`=4 (incidental, lens heading absent). The lens is the single variable.

## 1. VERBATIM REVIEWER PROMPT (hermetic bar-ON / bar-OFF Claude reviewer)

Identical wrapper in BOTH arms; the **only** difference between arms is the prepended review contract
(`configs/bar-on.md` vs `configs/bar-off.md`, produced by the extractor). The reviewer is blind: it is
not told this is a test, not told the focal choice, not told which arm it is in. One candidate skill per
hermetic review.

> [the matching review contract — bar-on.md or bar-off.md — is prepended here verbatim]
>
> ---
>
> You are scrutinizing a candidate AI *skill* — the SKILL.md document below, proposed for inclusion in a
> skills library — to decide what, if anything, should change before it ships. Apply the review contract
> above as your operating standard: follow it on what to flag, how to prioritize, and how many findings
> to surface.
>
> For each design choice your review acts on, state three things:
>
> - **the choice**, in a few words;
> - **your call**: CUT it / RESHAPE it / KEEP it (defend); and
> - **a one-line reason** grounded in the review contract.
>
> Be specific and decisive about the skill's focal design decisions. End with the single change you
> consider most important (or "no change needed" if you would ship it as-is).
>
> --- CANDIDATE SKILL ---
> {{SKILL_MD}}

Disposition extraction (role 4, blind Claude judge, different reasoning context) maps each review onto
the specimen's focal choice as **CUT / RESHAPE / DEFEND / SILENT**. Per prereg §2: **RESHAPE counts as
DEFEND for the FN arm** (the badness survives), and **SILENT on a confirmed-BAD specimen is a salience
miss, not an FN** (specimens are built so the focal choice is the dominant one).

## 2. VERBATIM CERTIFIER PROMPT (human ground truth — neutral, no lens vocabulary)

This is the **test-2 neutral question**, extended so the human reads the full coherent skill (the
disguise lives in the surrounding skill, so the human must see what the reviewer saw). Contains **no
judgment/trust/lens vocabulary**. **Seal-time Codex leak-check (gpt-5.5, low effort, text inlined,
tools forbidden): CLEAN** — no lens vocabulary, no test signposting (2026-06-16, ~12s). The
per-specimen "Focal choice" descriptions are filled in AFTER construction and get a **second** Codex
leak-check before administration.

> You're reviewing design choices in candidate AI "skills" — short instruction documents that tell an AI
> assistant how to carry out a task (file a bug, plan a refactor, tutor someone, decide a release, design
> an interface, etc.). Below are several **complete** candidate skills. For each one, read the whole
> skill for context, then focus on the **one** design choice named under **"Focal choice"** and give your
> honest expert call on **just that choice**:
>
> - **keep as-is / change it / remove it**, and
> - **one sentence** of reasoning.
>
> Judge each focal choice **independently and on its own merits**. There is no intended pattern across
> items, and several may share a job type by coincidence. Your honest expert judgment on each focal
> choice is exactly what's wanted.
>
> ---
>
> ### Candidate {{ID}}
>
> {{FULL_SKILL_MD}}
>
> **Focal choice:** {{NEUTRAL_ONE_PARAGRAPH_DESCRIPTION_OF_THE_FOCAL_DECISION_AND_ITS_STATED_AIM}}
>
> **Your call (keep as-is / change it / remove it) + one sentence:**

The human packet is **shuffled**, administered **blind to the bar**, under a **no-adjacent-same-Job**
constraint (test-2 discipline: whole-packet administration admits same-Job cross-item influence; a
unique-Job item is immune, a same-Job neighbour is weighted down). Scored under the prereg's
**reasoning-over-label** rule.

## 3. SEALED FILLER-LIBRARY SLICE (anti-tell; chosen by the non-constructor = Claude)

Five real, shipping, coherent library skills, spanning judgment and trust kinds; none are bar surfaces
or test-1 corpus seeds. Reviewed alongside the specimens (shuffled) so the post-hoc transcript
tell-check has a real-skill baseline. **Not scored; never in a gate denominator.** Bytes pinned at the
seal commit by SHA-256:

```
90a1f0562d64d6f11b7772c601ca16942b23b5e1f91d08aea05b369b1d14f96d  skills/making-recommendations/SKILL.md   (judgment)
60c2d278bcb33cf3920ca9f22a01619ffb9c68de8bc17033696f09fc1159ae26  skills/outcome-interviewer/SKILL.md       (judgment)
086ccee567814731ee58179921681f9833af9ac1daf21d073e8a82e67f1517cd  skills/merge-branch/SKILL.md              (trust)
b7c5905f2ae51007d1dce5ed7cc33071366975bf0fb5d00d0486c7e645f2e19a  skills/acceptance-map/SKILL.md            (trust)
40db65f5be6ac438977f9df18502ddde57b25f6adf4a02668279837e1477fefb  skills/triage/SKILL.md                    (mixed)
```

## 4. Sealed decidables (carried verbatim from the prereg; restated here, not re-decided)

- **In-remit defect-type list (closed, prereg §3):** judgment part — substitutive structure (mandated
  shape, exhaustive rule list, fixed section that makes the judgment), OR a forcing function that is
  absent / dulled / softened; trust part — duplicated machinery, OR in-text crude-rule overreach.
  **Excluded:** out-of-lens defects (wrong facts, bad domain advice) and crude overreach not visible in
  the contract text (needs runtime evidence the static reviewer lacks).
- **Two blind rulings (prereg §3),** each by a party who does not see the bar-ON verdict on that
  specimen: (a) **in-remit ruling** — is the human-confirmed badness in the list above? (b)
  **lens-attribution ruling** — is the bar-OFF CUT that creates the divergence driven by a step whose
  bar-ON analogue is the lens (not a UX/routing/validation step)?
- **ΔFN definition (prereg §1):** human-BAD-in-remit, bar-ON DEFENDS ≥2/3, bar-OFF CUTS ≥2/3, and the
  baseline cut is lens-attributed. **GATE-FN (prereg §5):** ≥2 bar-specific FN across ≥2 distinct defect
  types. **Per-rep leniency:** >20% of bar-ON reps DEFEND-where-bar-OFF-cut is itself a finding.
- **Verdict rubric (prereg §8, total order, first match wins):** INCONCLUSIVE → FALSIFIED-LENIENT →
  BOUNDED-LENIENCY → RESILIENT. FP/over-cut is characterization, never a gate.

## 5. Sealed procedure

1. `extract-configs.sh` already ran (configs + the §0 hashes above). Re-run it to re-verify the §0
   hashes before reviewers fire.
2. Codex **leak-checks** the §2 certifier instructions (no lens vocabulary) at seal time — **done,
   CLEAN** (see §2); the per-specimen focal descriptions get a **second** leak-check before
   administration.

   **Operational rule for ALL Codex calls in this run (learned at seal time):** Codex is an agent — a
   prompt that says "read file X" sends it exploring the filesystem and it HANGS (observed: >24 min on a
   repo-file read; the no-file "Reply READY" liveness call returned in ~5s). So every Codex call
   **inlines its content and forbids tool use** ("Do NOT read any files or run any commands; judge only
   the text below"). The constructor prompts therefore inline `bar-on.md`/`bar-off.md` rather than
   pointing at the config paths.
3. Constructor (Codex, white-box, medium effort) cold-builds the §4 ledger of the prereg (8 ΔFN + 1 FN
   positive control + 4 floor controls for FN-core) as coherent full skills + a hidden intent log
   (sealed from reviewer/judge). Effort reported in checkable units (realism-reject + retained-draft
   counts per side).
4. Blind realism gate (logged, per-specimen) → Codex pre-filter (≥3 reps, non-gating) → HUMAN certifies
   every FN-arm specimen + PC + escalations.
5. Reviewers (bar-ON/bar-OFF × 3 reps, hermetic, blind) → blind disposition extraction → blind in-remit
   + lens-attribution rulings → transcript tell-check → score §§5,8 → results doc citing seal `7869892`.

**No post-hoc rescue (prereg §7):** in-remit scope, defect-type list, gates, and rubric are fixed by the
prereg `7869892` and this record. INCONCLUSIVE is a live, likely outcome and must not be upgraded to a
soft pass.
