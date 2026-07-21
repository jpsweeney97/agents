---
type: preregistration
project: agents
created: 2026-07-19
revised: 2026-07-21
status: DRAFT v2 — UNSEALED (no data may be collected under this document; the seal is a later commit after the mini-pilot, the feasibility checks, and JP's final parameter fixing)
source: "T2 decision (JP, 2026-07-18, deliberate treatment close-out); gate: docs/specs/2026-07-13-deliberate.md:442; brief: docs/reviews/2026-07-18-deliberate-methodology-critique.md T2; method: docs/agents/contract-evaluation-methodology.md; pilot: docs/plans/2026-07-19-deliberate-t2-pilot-report.md; panel: docs/plans/2026-07-21-deliberate-t2-design-panel-report.md"
---

# Pre-registration (DRAFT v2): the deliberate shallow-prune control

The decisive empirical check the `deliberate` spec has owed since v1: shallow-prune results against a full-shaping control, hunting excluded eventual winners. The spec's gate: "The check runs only after its protocol is pre-registered through `methodology-check` or the repo's contract-evaluation methodology — same-field control, winner adjudication, leakage boundary, case set, pass/fail rule — and until then its result is a plan, not evidence." This document is that protocol. The move-7 design panel ran 2026-07-21 (five adversarial lenses; report cited in frontmatter) and its formal position was: not sealable as drafted, satisfied conditional on the repairs now folded in below.

## Provenance and revision record

The pre-pilot draft is frozen verbatim at commit `e6db816` — that SHA is the immutable record of what was predicted before any arm ran, and the seal will cite it. This v2 incorporates the one-case pilot and the design panel's 19 consensus repairs, plus JP's 2026-07-21 adjudication of the panel's seven contested calls (chat, this repo's session record; resolutions: A blind-extractor codebook with close-shape tiering, no declaration obligation; B the composite damage definition; C k=7 provisional pending mini-pilot; D both-reps exclusion qualification; E positive control adopted in the adapt form; F MDDR pre-registered with N=8 retained and disclosed; G mini-pilot before seal). Sections below are marked [unchanged] or [revised post-pilot/panel]. The seal, when it lands, certifies that predictions preceded the sealed run's data — never the pilot's; pilot data never enters the sealed run's evidence.

## Question [unchanged]

Does `deliberate`'s delegated shallow prune — decisive cuts at sketch depth, before shaping — systematically exclude candidates that full shaping would have revealed as winners? The premise under test is the spec's own honesty bound made load-bearing: every budget cut is disclosed as a low-confidence cut of a candidate "whose seriousness was unresolved at sketch depth"; the pipeline bets that this delegation is nonetheless trustworthy. Seventeen review rounds hardened the choreography; no instrument had ever tested this bet.

## Arms [revised post-pilot/panel]

- Frozen surfaces: the repo tree at one commit SHA (re-pinned at seal; the eight-surface method identity recorded by hash), one stage-agent model per role identical across arms, the packet-isolated fresh-agent harness shape of the committed smoke records. Both experiment arms are same-family by design (a cross-family arm would swap in a model confound); the same-family bound attaches to every verdict (see Pass/fail).
- Shared per-case stem: setup and Generate run once per case; the stored generated field is the same-field input to both arms, byte-exact. At stem-freeze, a crosswalk from each generated candidate's canonical wording to a stable candidate ID is produced; both arms and all extraction use these IDs. A winner matching no generated wording under the pre-declared rule routes that case-rep to INCONCLUSIVE — never to an operator match.
- **ARM P (shallow-prune, as shipped):** Prune (default survivor budget) → Shape survivors → Recommend, exactly the shipped pipeline.
- **ARM C (full-shaping control):** no prune; every field candidate shaped to comparable depth, then a Recommend-equivalent over the fully-shaped surface with the identical authority packet. ARM C is named and bounded as a **synthetic instrument**: the shipped product has no full-field shaping mode, so ARM C's construction is sealed as disclosed protocol — batch size, shaping model, per-shaper candidate visibility, the identity-Prune scaffolding, and a **flat markerless merge** (no batch/pass boundaries or vocabulary, style-homogenized across batch shapers; the non-survivor-bytes-identical merge check is sealed protocol, with its disclosed limit: it proves candidate wordings stable, not shaped-consequence semantics). A pre-registered **seam-leak scan** flags any ARM C rep whose close cites pass/batch structure; that rep is discarded and re-run. Every ARM C-derived claim is bounded to "under this synthetic full-field shaping procedure," never "full shaping" unqualified.
- Symmetric scaffolding is identical from dispatch 1 in both arms (relay-note file transport, schema note, batching rule where applicable); the Recommend-equivalent brief spec is frozen at seal and is not an operator degree of freedom.
- The named irreducible asymmetry stands: ARM C's recommender reads a much wider surface, so attention dilution is a live control-side failure mode in both directions — inflating spurious crownings and suppressing true ones. Divergence alone is never damage; a zero-divergence run is never proof of safety (see Pass/fail).

## Winner-set extraction [revised post-pilot/panel — replaces the "mechanical" mapping]

The pilot proved the drafted mapping was operator judgment, and extraction discretion set the headline. Extraction is now: at least two blind, sandboxed extractor agents independently apply a pre-registered codebook to close text only; inter-rater agreement is measured and reported; disagreement routes that case-rep to INCONCLUSIVE. No winner-set declaration obligation is added to either arm's Recommend — the arms' behavior stays untouched.

Close-shape tiering: only a **clear-call crowning** feeds the primary rate gate. Check-first and conditional branch heads, and `your call` presented-option heads, feed a labeled secondary channel recorded descriptively — a check-first close is a refusal to crown, not a revealed winner. No-basis and honest exits map to the empty set (a null for the primary gate).

## Divergence, adjudication, and the damage definition [revised post-pilot/panel — JP call B]

- **Divergence event (mechanical):** an ARM C rep's extracted winner-set contains a candidate ARM P's Prune excluded. Exclusion qualification [JP call D]: the candidate must be excluded in **both** ARM P reps to qualify for the gate; the union of exclusion sets is recorded descriptively.
- **Hardened adjudication (every divergence, any rep):** before judging, both the excluded candidate and ARM P's winner are **re-shaped under one identical neutral, seam-free, single-pass condition** (sealed procedure); the blind head-to-head is judged over that surface — never over ARM C's wide batched shaping, which is the instrument under test and the only other shaped source for the excluded candidate. When ARM P's winner-set is plural, the excluded candidate must be adjudicated strictly stronger than **every** ARM P branch head to count — fixed here, not at adjudication time. Panel: at least three fresh same-family judges plus at least two cross-family judges, all sandboxed (see Leakage); the same-family/cross-family split and escalation rule is fixed at seal; ties are recorded descriptively, never as damage.
- **Rate-gate event:** an adjudicated excluded eventual winner whose crowning reproduced in ≥2 of k ARM C reps and survived the hardened adjudication with cross-family corroboration.
- **Existence channel:** an adjudication-surviving, cross-family-corroborated excluded winner in which the human cold judge concurs is reported as an existence finding at any reproduction rate — always carrying its ARM C reproduction rate and its n=1 grain explicitly, and never moving the rate verdict. The two channels answer different questions — systematic damage versus demonstrated-once damage — and the report says so.

## Replication and instability handling [revised post-pilot/panel — JP call C]

- ARM C: **k = 7 recommender reps per case** [provisional; final k fixed at seal from the mini-pilot — k=5 permitted if the mini-pilot demonstrates per-rep detection reliability sufficient for ≥2-of-k power at k=5]. Reps re-run only the recommender over the one shared shaped brief, so extra reps are cheap.
- ARM P: 2 reps; the second rep runs **prune-only** (its exclusion set is all the design needs from it).
- Instability is handled **per case, never whole-run** (the drafted two-probe whole-run kill starved the run with probability ≈ 89% at pilot-measured variance and is deleted): a case where extraction cannot establish agreed winner-sets, or where no winner-set commands a plurality at the chosen k, routes to per-case INCONCLUSIVE with a reserve-pool replacement.
- **ARM C health floor** [number fixed at seal from mini-pilot]: a minimum share of committal (non-check-first) ARM C closes across the run for the run to be readable; below it, the run is INCONCLUSIVE regardless of divergence count.

## Leakage boundary [revised post-pilot/panel]

- Arms never see each other's outputs; the per-case stem (field) is the only shared state. ARM C's shapers and recommender never see Prune records or survivor identity; ARM P runs unmodified.
- **Blind roles are sandboxed, not merely fresh:** case-writers, extractors, judges, packet composers, and the leak-probe agent run with read scope confined to a packet directory outside this repo tree, enforced at dispatch — the committed prereg, pilot report, and panel report name the hypothesis and must be unreachable.
- **Adjudication packets are regenerated, then probed:** candidate cases are rewritten by a fresh arm-blind rewriter to a fixed template from the frozen decision facts plus the candidate's substantive case — never passed through from any shaping stage. Packets never carry field-width, option counts, numeric-versus-alpha labeling, batch vocabulary, or apparatus vocabulary. Verification is executed, not asserted: a fresh blind probe agent is asked to recover field-width and process; if it succeeds, the packet is rebuilt.
- **Operator-to-judge channels sealed:** packet composition by fresh blind agents from pinned templates; byte-identical pinned dispatch prompts across judge dispatches; A/B position randomization keyed off the sealed map with a committed seed; follow-ups pre-scripted or forbidden, all logged.
- **Sealed-map custody:** arm keys, case keys, judge assignments, and the A/B seed live in a keying map whose SHA-256 is recorded in the seal commit; the map itself lives at a named location outside every dispatched agent's read scope and outside JP's normal read paths; at unblind the map is revealed and verified against the sealed hash.
- **The human arm is sequestered:** no sealed-run divergence outcome, panel score, or count is written to any repo doc or any channel JP observes until his cold-judge adjudications are recorded; JP's packets are delivered out-of-band, composed blind, and include decoy packets (divergences where ARM P's winner is stronger, and ties) so his discrimination is measurable; the trigger for which divergences reach him is mechanical and pre-registered. Results are composed into this document only after the human arm closes.
- **Cross-family channel precondition:** the blind cross-family judge path (packet delivery to a non-Claude model, judgment capture, blinding held) must be demonstrated end-to-end before seal; if it cannot fire, the run's ceiling is INCONCLUSIVE and the seal says so.

## Case set [revised post-pilot/panel — JP calls E, F]

- N = 8 fresh decision cases [unchanged; retained at JP call F with the MDDR disclosure below], plus a reserve pool; the exhausted 2026-07-14 fixture and the spent pilot case are excluded.
- Cases are authored by sandboxed case-writer agents given only the setup-shape requirements — never the hypothesis, never the words shallow, prune, or control. Admission is a **pre-registered mechanical checklist** (fixed candidate count, budget-to-field ratio, seed/generated mix, difficulty rubric as checkboxes) — the hypothesis-aware operator renders no shape judgment. Adapted-historical cases are rejected (content-recognition and known-outcome leaks).
- **Fact-density stratification:** a hypothesis-blind density metric (count of options carrying packet-supplied cost/volume figures; count of numerically priced constraints) is computed per case by a screener who never sees the hypothesis; the case set spans declared density bands under a fixed quota (4 specified, 4 sparse); divergence and INCONCLUSIVE rates are reported by stratum; a density–INCONCLUSIVE correlation is a measurement limitation, never folded into the prune verdict.
- **Positive-control case [JP call E, adapt form]:** one additional case (outside the N=8 rate-gate set, never counted in it) is blind-constructed to seed a candidate designed to dominate the field yet be forced out by the survivor budget. Its construction runs through a sandboxed builder agent outside the normal case-writer machinery; its identity lives in the sealed map. The instrument catching it — ARM C crowning the seeded candidate and the crowning surviving hardened adjudication — is a **precondition for CALIBRATED**: it is the only demonstration separating "prune is safe" from "instrument is blind."
- Case admission is final before that case's first arm run; after data, a case leaves the set only by the pre-registered attrition rules below.

## Attrition dispositions [revised post-pilot/panel]

Pre-registered, one per failure mode: ARM C batch or envelope failure → a declared cap of mechanical retries with fresh agents, then void-and-replace; store loss mid-case → non-resumable void-and-replace; ARM P honest exit before Prune → case void, replacement from the reserve pool; ARM P honest exit after Prune → a distinct "ARM P declined" cell recorded descriptively and never fed to the divergence gate (naming no winner is not excluding one); reserve-pool exhaustion → N caps at the achieved count, disclosed, never backfilled. **Timing firewall:** every void or retry decision is timestamp-logged before that arm's winner-set is extracted; a void decided after a winner-set is seen is forbidden and the case is retained.

## Pass/fail rule [revised post-pilot/panel — JP calls B, F]

- **Minimum detectable damage rate, pre-registered:** at N=8 and threshold 2, the rate gate detects case-level damage at roughly a 25% rate or above; a prune with a true 10% per-case damage rate is exonerated ~81% of the time (binomial). Reproduction gating further lowers per-case detection power (≈0.74 at k=7 against pilot-measured 1/3 reliability; the mini-pilot re-measures this). Every verdict carries this floor explicitly. The low-rate regime belongs to the existence channel.
- **FALSIFIED** (the delegated shallow prune is not trustworthy as shipped, within the stated bounds): rate-gate events in ≥ 2 of N cases. Mandates a separately scrutinized repair decision, not an automatic redesign.
- **CALIBRATED / no-excluded-winner-found** [renamed; "net-protective" dropped — this experiment measures do-no-harm only, never benefit]: zero rate-gate events, AND the sealed run itself demonstrated a non-empty channel (≥1 divergence adjudicated, even to a tie), AND the positive-control case was caught, AND the ARM C health floor was met. The pilot-liveness clause is struck: pilot data never satisfies any sealed-run condition. The verdict reads in full: "no excluded winner found at ≥ the stated MDDR, by a same-family synthetic full-field shaping control, on these N cases, these models, this harness" — never "the prune is worth trusting" unqualified.
- **INCONCLUSIVE (W2):** zero sealed-run divergences, a failed positive control, a failed health floor, non-convergent adjudication, or an unfired cross-family channel — no substantive verdict, and not a pass. Per-case INCONCLUSIVE routing is defined under Replication; the whole-run stability kill is deleted.
- **Existence finding** (distinct from the rate gate, per the composite): reported as defined in the damage-definition section, at n=1 grain with its reproduction rate, without moving the rate verdict.
- Null honesty: zero divergences is never "the prune never cuts winners"; every claim is bounded to N cases × reps, these models, this synthetic control procedure, this harness, this environment; a zero-divergence result is consistent with both "safe" and "instrument-blind," which is why the positive control preconditions CALIBRATED.

## Descriptive measures [revised post-pilot/panel — firewall added]

Survivor overlap across P-reps; exclusion-set union versus intersection; whether a divergent excluded candidate's own Prune record anticipated the challenge; whether Contest surfaced the eventual winner; close-shape distribution per arm and per ARM C rep; ARM C reproduction rates; inter-extractor agreement; cost per case per arm. **Firewall:** no descriptive measure may reclassify, mitigate, or discount any rate-gate count or the verdict it produces; the verdict is computed from adjudicated counts alone and recorded before any descriptive measure is consulted; descriptives live in this section and no gate reads them.

## Cost, instrumentation, and ceiling [revised post-pilot/panel]

The binding constraint the pilot actually hit was operator attention, not tokens (~15–17 dispatches per case; ≈120+ at N=8; ~19% dispatch kill rate observed). The budget ceiling is set in **dispatch-count and operator-hours** [numbers fixed at seal], not tokens. Per-dispatch instrumentation records stage, arm, rep, brief and envelope bytes, wall-clock, and model; runtime token counts only if the harness exposes them, else the byte-proxy flagged as estimate. The pilot's 1.5–3M tokens/case figure was never measured and is carried as an unvalidated estimate only.

## Sequencing to seal [revised post-pilot/panel — JP call G]

1. This v2 revision lands (done at this commit).
2. Feasibility checks: enforceable read-scope sandboxing for blind dispatches; a live end-to-end blind cross-family judge dispatch; harness token-count exposure. Each is demonstrated or its absence is folded into the seal honestly.
3. **Mini-pilot** (2–3 cases, separately JP-authorized, spent cases excluded from the sealed set): measures per-rep detection reliability under the revised instruments (codebook extraction, flat merge, seam scan), prices a case at the revised k, and supplies the numbers for final k, the health floor, and the MDDR statement. Mini-pilot data never enters sealed-run evidence.
4. JP fixes the remaining open parameters; the finalized document is committed as **the seal** — citing `e6db816` (pre-pilot record), the pilot report, the panel report, and this v2 as its provenance chain.
5. The sealed run executes only on JP's separate, explicit authorization. Results are composed into this document only after the human arm closes, per the sequestration rule.

## Open parameters for JP at seal [revised post-pilot/panel]

Final k (7 provisional; 5 if the mini-pilot licenses it); the ARM C health-floor number; the extractor codebook text; the mechanical admission checklist text; the positive-control construction; the same/cross-family judge split and escalation rule; the mechanical trigger for which divergences reach the human arm; the dispatch-count and operator-hours ceiling; the sealed-map location. The FALSIFIED threshold stays 2 of N=8 with the MDDR disclosure unless the mini-pilot's reliability measurement forces a re-derivation, which would be marked revised-post-mini-pilot in the seal.
