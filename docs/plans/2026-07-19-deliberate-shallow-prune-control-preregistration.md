---
type: preregistration
project: agents
created: 2026-07-19
status: DRAFT — UNSEALED (no data may be collected under this document; the seal is a later commit after pilot, design panel, and JP adjudication)
source: "T2 decision (JP, 2026-07-18, deliberate treatment close-out); gate: docs/specs/2026-07-13-deliberate.md:442; brief: docs/reviews/2026-07-18-deliberate-methodology-critique.md T2; method: docs/agents/contract-evaluation-methodology.md"
---

# Pre-registration (DRAFT): the deliberate shallow-prune control

The decisive empirical check the `deliberate` spec has owed since v1: shallow-prune results against a full-shaping control, hunting excluded eventual winners. The spec's gate: "The check runs only after its protocol is pre-registered through `methodology-check` or the repo's contract-evaluation methodology — same-field control, winner adjudication, leakage boundary, case set, pass/fail rule — and until then its result is a plan, not evidence. Contract correctness makes v1 executable; only that control can tell whether the delegated pruning is worth trusting." This draft is that protocol, designed against the contract-evaluation methodology's eight moves; a `methodology-check`-style pass rides the pre-seal design panel (the gate names either route; JP may redirect at adjudication).

## Question

Does `deliberate`'s delegated shallow prune — decisive cuts at sketch depth, before shaping — systematically exclude candidates that full shaping would have revealed as winners? The premise under test is the spec's own honesty bound made load-bearing: every budget cut is disclosed as a low-confidence cut of a candidate "whose seriousness was unresolved at sketch depth" (spec, Prune honesty rules); the pipeline bets that this delegation is nonetheless trustworthy. Seventeen review rounds hardened the choreography; no instrument has ever tested this bet (the treatment's verdict: "premise unbought by its own admission").

## Arms (single-variable differential — move 2)

- Frozen surfaces: the repo tree at one commit SHA (re-pinned at seal; the eight-surface method identity recorded by hash), one stage-agent model per role identical across arms, the packet-isolated fresh-agent harness shape of the committed smoke records.
- Shared per-case stem: setup and Generate run once per case; the stored generated field is the same-field input to both arms, byte-exact. Generation variance is thereby excluded from the differential.
- **ARM P (shallow-prune, as shipped):** Prune (default survivor budget) → Shape survivors → Recommend, exactly the shipped pipeline. Products: winner-set, Prune's complete exclusion records, Contest's output.
- **ARM C (full-shaping control):** no prune; every field candidate shaped to comparable depth under the same `option-shaping` constituent and composition seam (batched to respect context bounds; the batching rule is fixed at seal and identical across cases), then a Recommend-equivalent over the fully-shaped surface with the identical authority packet. Product: winner-set.
- The only intended difference is the presence of the sketch-depth prune and its consequence, shaped-field width at Recommend. One asymmetry cannot be removed and is named now: ARM C's recommender reads a much wider surface, so attention dilution is a live control-side failure mode — divergence alone is therefore never damage; adjudication decides (below). The control is an instrument, not ground truth.

## Winner adjudication

- Winner-set mapping (mechanical, fixed now): a close maps to the set of candidates left as a primary recommendation under any branch of its own stated checks — clear call → that candidate; check-first / conditional → the branch heads; no-basis or honest exit → empty set, and that case-rep is a null for the primary gate. Candidate identity is by canonical stored wording.
- Divergence event (mechanical): ARM C's winner-set contains at least one candidate ARM P's Prune excluded. A different pick among common survivors is preference variance — recorded descriptively, never gate-relevant.
- Adjudication of each divergence (judged, blind): a neutral head-to-head packet — the decision frame, constraints at price, values, and the two candidates' full-shaping cases only; no arm identity, no run artifacts, no apparatus vocabulary — asking which candidate is the stronger recommendation or too close to call. Panel: at least three fresh same-family judges plus at least one cross-family judge (move 4), escalation on splits; JP as the human cold-judge anchor (move 5) spent only on decisive divergences, administered under the AGENTS.md blinding guard.
- An **adjudicated excluded eventual winner** is a divergence where the panel, with cross-family corroboration, finds the excluded candidate strictly stronger than ARM P's winner. A tie is not damage: cutting an equal under a declared budget is the pipeline's disclosed, priced behavior — ties are recorded descriptively.

## Case set

- Proposed N = 8 fresh decision cases (fixed at seal after the pilot prices a case); the exhausted 2026-07-14 fixture is excluded.
- Authorship leak control: cases are authored by case-writer agents given only the setup-shape requirements (decision frame, field mode with seeds, constraints at price, values, a stated lean, domain-diversity quota) — never the hypothesis, never the words shallow, prune, or control; the operator screens for shape validity only. Alternative source for the design panel to weigh: adapting real historical decisions from repo artifacts (richer, but leak-prone and less controllable).
- Case admission is final before that case's first arm run; after data, a case leaves the set only by the pre-registered validity rule (ARM P exits honestly before Prune → case void, replacement drawn from the reserve pool).

## Leakage boundary

- Arms never see each other's outputs; the per-case stem (field) is the only shared state.
- ARM C's shapers and recommender never see Prune records or survivor identity; ARM P runs unmodified.
- Judges receive leak-checked neutral packets — verified as produced, not merely as sourced (move 3); arm keys, case keys, and judge assignments live in sealed maps outside any shared or tmp path until unblinding.
- Nothing — outputs, scores, divergence counts, predictions — reaches JP-as-judge before his judgment is recorded (`AGENTS.md` Blind Evaluations; lost blinding is unrecoverable, re-administer to a fresh judge). The orchestrating operator session necessarily sees everything, so every judge is a fresh non-fork agent and JP's packet is composed under the guard.

## Replication (proposed; fixed at seal after pilot)

Two independent ARM P reps per case — prune stochasticity is part of the question, so an excluded-winner event is checked against both reps' exclusion sets. One ARM C rep per case plus a stability probe: on two designated cases, re-run ARM C's recommender once; disagreement between its winner-sets marks the control channel unstable and routes the run to the INCONCLUSIVE handling below.

## Pass/fail rule (gates pre-registered; thresholds proposed, fixed at seal)

- **FALSIFIED** (the delegated shallow prune is not trustworthy as shipped): adjudicated excluded eventual winners in ≥ 2 of N cases, any rep. Mandates a separately scrutinized repair decision, not an automatic redesign.
- **CALIBRATED / net-protective**: zero adjudicated excluded eventual winners with a demonstrably non-empty channel (divergences occurred and were adjudicated, or the pilot proved the channel can fire).
- **INCONCLUSIVE (W2)**: the control channel is unstable, empty for a measurement reason, or adjudication non-convergent — no substantive verdict, and not a pass.
- Existence finding (pre-registered as distinct from the rate gate): any single excluded eventual winner in which the human cold judge concurs is reported as a confirmed existence proof at n=1 grain — an existence claim needs one instance — without moving the rate verdict.
- Null honesty (move 8): zero divergences is never "the prune never cuts winners"; every claim is bounded to N cases × reps, these models, this harness, this environment.

## Descriptive measures (recorded, never gates)

Survivor overlap across P-reps; whether a divergent excluded candidate's own Prune record anticipated the challenge (`Strongest case`, `Revive if` — the contestable ledger working as designed vs surprised); whether Contest surfaced the eventual winner as a live challenge on divergent P-runs; close-shape distribution per arm; cost per case per arm (the offload-pricing input).

## Pilot (unsealed, before seal — move 6)

One to two cases end-to-end through both arms. It must establish: that ARM C produces a stable winner-set at all; that the divergence channel is reachable (the gate is falsifiable); base rates informing the thresholds; per-case token and wall-clock cost; and the feasibility of the full-field shaping batch rule. Pilot data never enters the sealed run's evidence. An empty pilot channel is itself a legitimate honest close of the question at characterization grade (the test-5 precedent).

## Design panel (before seal — move 7)

Independent adversarial review of this pre-registration attacking: pre-ordained verdicts, unreachable gates, divergence cells forbidden by construction, the control-arm-as-ground-truth fallacy, case-authorship leaks, winner-set mapping gameability, and the batching rule's fairness across arms. A `methodology-check`-style pass over the protocol rides this panel, satisfying the spec gate's either-route clause.

## Sealing and execution

After pilot, panel, and JP's adjudication of the open parameters, the finalized document is committed as the seal — the commit SHA is the proof that predictions preceded data. Execution runs only on JP's explicit authorization (the T2 decision authorized design-and-seal; the run is separately authorized). Results append to this document; no gate, threshold, or keying changes after the seal.

## Open parameters for JP at seal

N and the rep counts; the FALSIFIED threshold; case source (authored-blind vs adapted-historical); judge panel composition and whether the human arm is pre-committed or divergence-triggered; the batching rule for ARM C; the budget ceiling. Rough cost flag: the v30 smoke priced one shipped-pipeline run at roughly 0.5–1M tokens; ARM C's full-field shaping is the heavy step, so a plausible all-in estimate is 1.5–3M tokens per case before adjudication — the pilot prices this properly before anything seals.
