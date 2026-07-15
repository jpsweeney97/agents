# Behavior Smoke Test — `deliberate` end-to-end (Claude/sonnet): v26 wording fix proven, Recommend `cut-basis` enum defect found and fixed (v27), first accepted Claude close capsule

- **Date:** 2026-07-15
- **Target:** the `deliberate` skill bundle (`skills/deliberate/`), exercised end to end on Claude Code as the outstanding cross-runtime proof left by the 2026-07-14/07-15 handoffs — the run the prior smoke (`2026-07-15_deliberate-prune-wording-fidelity.md`) failed at Prune.
- **Skill source at test:** branch `fix/deliberate-wording-canonicalization` (the live-served working tree). Helper SHA-256 `2bc357788c0644242c35123a277e1de7ebbf1ed956d8ca1c51338e35ad1ea6da`; 158/158 fixtures green; `contract-data-version` 5.
- **Harness:** blind stage agents running the real patched skill via a file-based, byte-exact relay. A fresh orchestrator runs the contract and pauses at each stage dispatch by writing the rendered brief to a relay dir; the operator (top-level session) runs one fresh, non-forked **sonnet** stage agent per stage and hands its verbatim envelope back. Exact 3,760-byte `$deliberate` prompt (SHA-256 `253f1bfe697124f685124f03adb539f5f55005284cb4f107de598b2272493a82`), recovered byte-identical from Codex rollout `…019f63d3…`. Harness note: both orchestrators self-reported `claude-opus-4-8[1m]` (the `model: sonnet` spawn override did not take on the background orchestrator); all five **stage** agents self-reported `claude-sonnet-5` in both runs — immaterial to the verdict, since the wording bug is triggered by stage-agent serialization, which was sonnet as in the prior smoke.
- **Headline:** the v26 wording-canonicalization fix is **proven on Claude** (Prune cleared byte-exact, twice), and the run surfaced a **second, unrelated defect** — the Recommend brief under-specified the `cut-basis` enum — which was fixed (v27). A fresh from-scratch re-smoke then reached an **accepted `deliberate-capsule/v1` close capsule**, independently re-validated. First Claude run past Prune; first accepted Claude capsule (a failure capsule in run 1, a success close capsule in run 2); first Contest execution on Claude.

---

## Run 1 — v26 proven at Prune; honest `stage failed: recommend` on an enum under-specification

- **Generate → Prune → Shape accepted.** Prune — the prior smoke's exact death point (`' '` vs `'\n'` order-preserving-subsequence rejection) — passed with the generated survivors accepted **byte-exact**. Independent offline checks confirmed the order-preserving subsequence and exact partition conservation. The v26 failure mode did not recur: the sonnet Generate agent emitted all wordings as single-line scalars (the patched brief's `>-`/single-line guidance), so no newline entered a canonical wording value.
- **`stage failed: recommend`.** The Recommend stage agent's disposition record carried `cut-basis: fact-established dominance end`. `validate-envelope --stage recommend --accept` correctly rejected it (`record key cut-basis must be one of ['constraint', 'equivalence', 'dominance', 'survivor budget', 'post-prune filter', 'post-prune dominance', 'post-prune collapse', 'only-serious-option rival']. Got: 'fact-established dominance end'`). No repair, no retry; Contest correctly never dispatched (global exit rule).
- **First `validate-capsule --accept` reached on Claude.** The honest terminal produced a `deliberate-capsule/v1` **failure capsule** (preserving the validated Generate/Prune/Shape artifacts, restart frontier at Recommend), accepted `exit 0`. (An API server error interrupted the orchestrator mid-failure-capsule-build; it was resumed and completed the terminal cleanly.)

### Root cause (a real, pre-existing defect, unrelated to v26)

The rendered Recommend brief **never surfaced the literal `recommend-bases` enum values.** The `record-list` shape note only said `cut-basis (from the stage's basis set)`, and the sole mention of the four cases was narrative prose in the Recommend brief-extra — "a filter on a recorded constraint consequence, **a fact-established dominance end**, a survivor collapse, or the rivals of an `only one serious option` close" — which the stage agent reasonably transcribed. By contrast, the Prune brief already surfaces its bases explicitly via `references/methods.md` (`Cut basis: <constraint | equivalence | dominance | survivor budget>`), which is why Prune agents emit valid values. This was previously unreachable on Claude because no run had ever passed Prune. The skill behaved correctly throughout (rejected the malformed envelope, honest terminal, no fabrication). The failure is probabilistic — an agent that happened to write `dominance` would have passed, since that string is in the combined eight-value enum.

### The fix (v27)

`references/contract-data.yaml` recommend brief-extra now names each canonical value inline, mapped to its narrative case, with an explicit instruction to emit the canonical value, never the prose: `post-prune filter` / `post-prune dominance` / `post-prune collapse` / `only-serious-option rival`. No schema or `contract-data-version` change — the enum set is unchanged, only brief legibility. Validated: YAML parses, 158/158 fixtures, `check-renderings` clean, `ruff` clean, `git diff --check` clean. The re-rendered Recommend brief in run 2 confirmed all four canonical values now appear.

---

## Run 2 — fresh from-scratch re-smoke reaches an accepted success close capsule

A fresh from-scratch run of the exact prompt against the fixed working tree (new orchestrator, new sonnet stage agents), same relay harness.

- **All five stages accepted**, each `validate-envelope --accept` `exit 0`: Generate (17 options: 9 generated + 8 user-seed, byte-exact) → Prune (4 survivors + 13 exclusions, byte-exact subsequence, partition conserved — v26 proven a second time) → Shape (comparison surface + 6 constraint-consequences, `option` fields byte-exact) → **Recommend (disposition record now carries `cut-basis: post-prune filter`, a canonical value — the fix)** → Contest (exclusion-check-line catching both live challenges: the excluded "Twelve structured interviews…" candidate with its visible user lean, and the D/Wizard-of-Oz cut).
- **Success capsule accepted.** `record-proof-inputs` → `record-terminal` → `validate-capsule --store --accept` `exit 0`: `capsule valid: run=deliberate-270dab0f18d6 terminal='close rendered'`. Store retired via `trash`. The close is a substantive conditional recommendation (D cut on the truthful-framing constraint; then B if a budget/data-scope check clears, else A with C as honest runner-up).
- **Independently re-validated.** The operator extracted the 77 KB capsule from the run's `FINAL.txt` and re-ran `validate-capsule` storelessly against the fixed contract: `exit 0`, `terminal='close rendered'`; all 14 capsule records carry canonical `cut-basis` values; `capsule-complete` digest `8ea7a619…` verified. This acceptance does not rest on the orchestrator's report.
- **Containment held.** After the run, the repository worktree was clean except the intentional v27 edit — no unauthorized mutation by any stage agent or orchestrator. HEAD unchanged.

---

## Secondary observations (surfaced, not blocking)

- **A Prune-stage semantic inconsistency the mechanical validator cannot catch.** In run 1, Prune's accepted envelope contained an equivalence-cut record claiming a mechanism-equivalent user-seed survives under seed protection, while a sibling budget cut in the same envelope independently removed that seed. Partition was still exactly conserved (the validator checks membership/partition, not cross-record semantic consistency). This is exactly the class Contest exists to catch, and Contest never ran in run 1 (Recommend failed first). Left for Contest or the user; not a validator gap to close mechanically. In run 2 the field differed and the inconsistency did not recur.
- **Orchestrator containment discipline.** Neither orchestrator captured an explicit per-stage `git status` before/after pair; run 2's containment claim rests on an end-of-run clean check plus zero pin-mismatch envelopes across all five stages, disclosed verbatim in the accepted capsule's own `proof-boundary.containment` / `proof-boundary.not-proven`. A stage-agent process gap, not a skill defect.

---

## Proof boundary and status

- The v26 wording-canonicalization fix and the v27 Recommend enum-legibility fix are both proven on Claude at branch `fix/deliberate-wording-canonicalization` under live sonnet stage agents. Re-run rather than trust this record after any contract edit.
- End-to-end recovery is now proven on both runtimes: an accepted exact-prompt success capsule on Codex (2026-07-14) and on Claude (this record). The Claude success capsule was not live re-imported (importability stays fixture-covered); the honest-exit constituent branches (muddy-goal at Generate, `field not ready`, drift terminals) were not exercised by these runs.
- The failure-capsule path was exercised end to end on Claude for the first time (run 1: accepted failure capsule); the success-capsule path for the first time (run 2).

## Durable artifacts

- Prior failure record (Prune wording fidelity): `docs/smoke-tests/2026-07-15_deliberate-prune-wording-fidelity.md`.
- v26/v27 authority: `docs/specs/2026-07-13-deliberate.md` (v27 version-history entry).
- The relay dirs, both run transcripts (`FINAL.txt`), the preserved run-1 store, and the extracted capsule lived in a session scratchpad and are ephemeral; the durable proof is this record plus the committed fix.
