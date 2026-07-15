# Behavior Smoke Test — `deliberate` end-to-end (Claude/sonnet): caught a Prune-stage wording-fidelity failure

- **Date:** 2026-07-15
- **Target:** the landed `deliberate` skill bundle (`skills/deliberate/`), exercised end to end on Claude Code as the outstanding cross-runtime proof left by the 2026-07-14/07-15 handoffs
- **Commit verified:** `eeecefc` (`main`, in sync with `origin/main`; clean worktree throughout)
- **Skill:** `deliberate` (runtime smoke), diagnosed with `diagnose`, fix design settled with `synapsis`
- **Harness:** one fresh sonnet orchestrator subagent given the exact 3,760-byte `$deliberate` prompt (SHA-256 `253f1bfe697124f685124f03adb539f5f55005284cb4f107de598b2272493a82`), running the contract itself and dispatching each stage as a fresh non-forked stage agent (also sonnet). Because nested async children do not auto-resume the orchestrator in this environment, each completed stage envelope was relayed back to the orchestrator verbatim — a byte-faithful pass-through on both legs, confirmed not to be the failure cause.
- **Headline:** the run **did not reach capsule acceptance**. It terminated at the honest mechanical terminal `stage failed: prune` — a genuine, model-serialization-dependent wording-fidelity bug that the separate Codex smoke did not trigger. No capsule was produced or fabricated; the store was trashed; the worktree stayed clean.

The exact prompt was recovered byte-identical from the Codex rollout that established it (`rollout-2026-07-14T23-31-02-…019f63d3…`), so this run used the same input the accepted Codex run used.

---

## A — behavior claim: `deliberate` completes five stages → proof → terminal → capsule acceptance → carrier → cleanup under Claude/sonnet → **FAILED (caught a real bug)**

- **Behavior claim:** a fresh Claude Code run of the exact prompt reaches the same five-stage, proof-input, terminal-state, capsule-acceptance, carrier, and cleanup boundary the accepted Codex run reached.
- **Scenario:** the exact 3,760-byte `$deliberate` invocation (six-week validation-strategy decision; eight candidate seeds; five price-confirmed constraints; stated values; a visible soft-lean toward the interview-only candidate; survivor budget 4; inline degradation not granted).
- **Result:** **FAILED** — terminated at `stage failed: prune`; `validate-envelope --accept` on the Prune envelope rejected with *"survivors are not an order-preserving subsequence of the input field — Prune cuts, never reorders."*
- **Observed behavior:** preflight green (helper SHA `74cd4b0e…`, 149/149 fixtures); session-scoped store root resolved under the subagent's own temp root; nested fresh-agent stage isolation worked (real Generate and Prune stage agents, not `capability unavailable`); Generate produced a genuine widened field of 15 (8 user-seeds preserved byte-exact + 7 mechanism-distinct generated) and was accepted; Prune did real method work (4 survivors + 11 exclusion records, correctly cutting the user's lean candidate on the interview-only price and flagging Wizard-of-Oz on truthful framing) but its envelope was rejected before Shape.
- **Why:** the two *generated* survivors failed the exact-equality subsequence check on ` ` vs `\n` at soft-wrap points; the two *user-seed* survivors (single-line) matched. The failure is genuine (relay-exonerated) and reproducible offline.

### What the smoke did establish (positives)

- Session-scoped store root resolves cleanly on Claude Code (`…/scratchpad/deliberate-run-live`) — one of the handoff's open questions, answered yes.
- Nested fresh, non-forked stage-agent isolation works via the Task/Agent tool.
- Preflight, setup, Generate acceptance, and Prune method work all execute correctly; the fail-fast discipline held (no `record-proof-inputs` / `record-terminal` / `validate-capsule` calls after the rejection).

---

## Diagnosis (byte-proven; deterministic offline repro)

Root cause: soft-wrap newlines from Generate's YAML literal block-scalar option wordings enter the canonical wording **value** and defeat Prune's byte-exact subsequence check.

1. The Generate stage (sonnet) emitted long option wordings as `|-` literal block scalars soft-wrapped at width 88. Literal block style turns each cosmetic wrap into a real `\n` inside the wording string (4–6 per long option). Confirmed in the Generate stage agent's raw transcript.
2. `validate-envelope --accept` stores those `\n`-bearing wordings as canonical with no normalization or rejection; the `write-item` (`dump_yaml`) → re-parse round-trip preserves the newlines.
3. `render-brief` re-serializes via `dump_yaml` (`yaml.dump`, `width=88`); the Prune stage reproduced the wording as continuous single-line prose (the Prune agent performed the newline→space rewrite).
4. `_is_order_preserving_subsequence` (`skills/deliberate/scripts/deliberate-validate.py:2786`) compares exact `==`, so `…wide use…` ≠ `…wide\nuse…` → not a subsequence → `stage failed: prune`.

Offline reproduction against the live module: parsed Generate field wordings carried 4–6 embedded `\n` each; the storage round-trip preserved them; `_is_order_preserving_subsequence(survivors, stored_field)` returned `False`; the two generated survivors mismatched on `' '` vs `'\n'`; the two user-seed survivors matched.

The byte difference is pure YAML-serialization noise the contract injected into its own canonical data — the Prune agent did not paraphrase. Codex's earlier accepted run dodged it because that model emitted the wordings on single physical lines (no soft-wrap → no `\n`); sonnet soft-wraps inside block scalars, exposing the latent bug. This also stresses the skill's cross-runtime determinism claim (`schemas.md:9`): a spurious *formatting* drift was treated as real.

Key code references: `skills/deliberate/scripts/deliberate-validate.py` — `dump_yaml` `:220`, `_is_order_preserving_subsequence` `:2786`, Prune envelope validation `:2872-2944`, `render-brief` field dump `~:3105`; `skills/deliberate/references/stage-packets.md:252-258` (byte-identical records / value-preserving storage vs discarded document formatting); `references/contract-data.yaml:354-355`.

---

## Cross-model fix design (synapsis — RESOLVED / CONCESSION)

The fix design was settled by a cross-model deliberation between this session (host) and Codex.

- **Outcome:** RESOLVED / CONCESSION, `conceded_by: host`, strength **strong** (uncapped, no cap-tiebreak). Codex independently confirmed the root cause (its own in-memory fixture) and refuted the host's original over-reach: normalizing *before every comparison* would replace byte-identity with whitespace-equivalence downstream and weaken the contract's paraphrase/identity guarantee. The host retired that clause.
- **Run dir (durable certificate + full receipts):** `/Users/jp/.synapsis/runs/2026-07-15-122901-deliberate-wording-fidelity-fix/`
- **Retired position (host):** "The correct and sufficient fix requires applying the whitespace canonicalization both at ingress and before every wording comparison; comparison-time normalization is part of the correct and sufficient fix."

### The converged fix (certified answer)

- Canonicalize option-wording whitespace (collapse internal whitespace runs, including newlines, to a single space; trim) **exactly once, at identity establishment (ingress)** — normalize fresh generated Generate wordings before the field becomes canonical, and normalize initial setup candidates only under an explicitly documented `init-setup` rule (preserving non-generated seeds exactly unless that rule has canonicalized them).
- Run duplicate/collision detection **after** normalization, rejecting post-normalization collisions (e.g. `A B` vs `A\nB`).
- Keep **all downstream comparisons byte-exact** — Prune survivor subsequence and option-object preservation, record option byte-identity, retrieval concerns, directives, and every capsule/store wording authority. Comparison-time normalization is explicitly **rejected**.
- **Reject or explicitly migrate/version-gate** legacy v1 capsules containing non-canonical wordings; never silently reinterpret them (capsule completeness hashes raw bytes).
- Update the Generate/Prune briefs to require single-line or folded (`>-`) option-wording scalars.

### Proof obligations (regression fixtures to add)

- Literal-block soft-wrapping is canonicalized only at origin.
- Post-normalization collisions fail.
- A whitespace-altered downstream survivor or record still fails (paraphrase/identity guarantee intact).
- Prune partition conservation stays exact.
- Capsule round-trip / import preserves the canonical wording.

---

## Proof boundary and status

- The smoke proves behavior **at commit `eeecefc` under sonnet stage agents**: the Claude runtime reaches Prune but fails there on this wording-fidelity bug. Re-run rather than trust this record after any contract edit.
- The synapsis certificate settles the fix **design** only. It explicitly does not assert that comparison-time normalization is acceptable, the exact code lines / canonicalizer API, which legacy-capsule path (hard reject vs version-gated migration) is chosen, or that the fix is implemented / fixtures pass.
- **Not implemented.** Implementation should route the proof-semantics change through `agent-facing-design`, update `docs/specs/2026-07-13-deliberate.md`, validate all 149 fixtures plus the new regression fixtures, and re-run this exact Claude smoke.

## Durable artifacts

- Synapsis run dir (certificate + receipts): `/Users/jp/.synapsis/runs/2026-07-15-122901-deliberate-wording-fidelity-fix/`.
- The accepted-Codex exact-run rollout that established the prompt: `~/.codex/sessions/2026/07/14/rollout-2026-07-14T23-40-27-…019f63dc…jsonl`; the invalid `store unavailable` attempt (source of the byte-exact prompt): `…019f63d3…`.
- The smoke's raw helper-output evidence log and offline repro lived in a session scratchpad (`/private/tmp/…/scratchpad/`) and are ephemeral; the durable record is this file plus the run dir. The live `deliberate` store was trashed at close per contract.
