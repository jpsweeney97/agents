---
type: pilot-report
project: agents
created: 2026-07-19
status: "PILOT — UNSEALED (pre-registration draft's own pilot step; pilot data never enters the sealed run's evidence; the pilot case is spent by disclosure and excluded from the sealed case set)"
source: "Pilot step of docs/plans/2026-07-19-deliberate-shallow-prune-control-preregistration.md (DRAFT — UNSEALED); executed on JP's 2026-07-19 authorization to run the T2 pilot"
---

# T2 pilot report: the deliberate shallow-prune control, pilot case 1

One case run end-to-end through both arms of the shallow-prune control, per the unsealed pre-registration's own pilot step. The pilot's job was to establish five things before the seal: whether ARM C produces a stable winner-set at all, whether the divergence channel is reachable, base rates for the thresholds, per-case cost, and the feasibility of the full-field shaping batch rule. All five are answered. Everything here is design input for the pre-seal panel and JP's adjudication — none of it is evidence under the gate.

## Headline findings

1. **The divergence channel is reachable; the FALSIFIED gate is falsifiable.** ARM C rep 2 closed **clear call** on the route-redesign candidate — a candidate ARM P's Prune had excluded as a contestable survivor-budget cut. That is a mechanical divergence event under the draft's winner-set mapping, produced on the first pilot case.
2. **ARM C's winner-set is not stable at one rep.** Three fresh recommenders on byte-identical briefs produced: check-first (survivor-drawn branch heads), clear-call (the excluded candidate), check-first (same diagnostic as rep 1, overlapping heads). Pairwise winner-set agreement 1 of 3. The instability has structure — a modal check-first attractor naming the same pivotal diagnostic twice, with one clear-call outlier — but under the draft's own stability-probe rule, a sealed-run case with this profile routes to INCONCLUSIVE handling. Rep count and an outlier rule are now the load-bearing open parameters.
3. **The divergence coincides with the instability.** The one divergence event came from the outlier rep. On this case, "ARM C crowned an excluded candidate" and "ARM C recommender variance" are the same observation — exactly the confound the draft's adjudication layer and stability probe were designed for, now demonstrated live. A divergence event cannot be read as prune damage without surviving a stability gate.
4. **The contestable ledger anticipated the challenge.** The excluded winner's own Prune record disclosed the cut as a contestable sketch-depth budget cut, its `strongest-case` names precisely the basis rep 2 chose it on (cheap logistics lever, if the donor pool is real), and its `revive-if` names the confirming check rep 2's own close concedes is missing. The prune was honest about what it did not know; the divergence lands squarely on the disclosed low-confidence band, not on a confident kill. Contest, however, did not surface the eventual control-winner among its live challenges (it named two others).
5. **Convergent-cut signal:** all three ARM C recommenders independently re-excluded ARM P's three fact-established constraint cuts (over-cap warehouse, and the two candidates whose mechanisms cannot raise the grant's distributed-pounds metric), rep 1 re-derived two of ARM P's budget cuts as dominance kills, and no rep crowned any of the three constraint-cut candidates. On this case the fact-established band of the prune reproduces perfectly under full shaping; all observed action is in the disclosed contestable band.
6. **Batching is feasible and priced.** Full-field shaping ran as five batches (4/4/4/4/3) spliced mechanically from one canonical helper render (non-survivor bytes proven identical), merged mechanically, and accepted by the shipped validator. One systematic defect surfaced and was fixed mechanically: two of five batch Shape agents labeled the envelope `stage` with the constituent name; a one-line schema note in the relay note eliminated the defect (zero recurrences in seven subsequent dispatches).

## Shipped-pipeline behavior observed (ARM P)

Prune returned 8 survivors against a budget of 4 under a disclosed overflow — the value-trade guard refused to cut to budget without pricing an unresolved value trade, and carried the un-cuttable survivors forward within the allowed 2× bound. 11 complete exclusion records, partition 19 = 8 + 11 helper-verified. Recommend closed **conditional call** (retail-rescue lead if a chain-coverage check confirms; mobile pantry trucks otherwise), declined the user's leaned candidate as primary with its basis stated, and kept it as a complement. Contest returned live challenges on the community-garden disposition and the purchasing co-op budget cut. Every helper call in the accepted run exited 0; every envelope was accepted mechanically on first validation.

## Winner-sets (mechanical mapping, as extracted)

- ARM P (conditional → branch heads): {retail-rescue agreements, mobile pantry trucks}.
- ARM C rep 1 (check first): {volunteer program, bulk-buy, retail-rescue, fractional cold-storage} — all ARM P survivors. No divergence.
- ARM C rep 2 (clear call): {route redesign} — **in ARM P's Prune-excluded set. Divergence event.**
- ARM C rep 3 (check first, extra-protocol probe): {volunteer program, retail-rescue} (+ fractional cold-storage under a liberal conditional-head reading) — all ARM P survivors. No divergence.

## Base rates (n = 1 case, 3 control reps — pilot grain only)

Divergence in 1 of 3 control reps; divergence source = the outlier rep; stability-probe disagreement 1 of 1 probes (and 2 of 3 pairwise). Fact-established prune cuts reproduced 3 of 3 reps. These numbers inform thresholds; they prove nothing about the prune (null honesty: bounded to this case, these models, this harness).

## Per-case cost

Wall-clock ≈ 72 minutes from case freeze to final acceptance, arms run in parallel, including one killed run (~9 min) and the extra rep-3 probe (~8 min). Dispatches: 16 sonnet stage-agent dispatches (13 accepted, 3 killed: 1 harness transport bug, 2 stage-label defects), plus 1 session-model case-writer. ARM P matches the certified v30 smoke's shipped-run shape (which priced at roughly 0.5–1M tokens) minus capsule assembly; ARM C added 9 sonnet dispatches (1 shared Generate ride-along, 5 batch shapers, 3 recommenders), the recommenders each on an ~85KB brief. Harness-side per-agent token counts were not instrumented this run; that instrumentation is a sealed-run requirement. The draft's 1.5–3M tokens/case estimate remains plausible at 2-rep replication; the binding practical costs observed were orchestration attention and stage-agent latency, not context limits.

## Design inputs for the pre-seal panel and JP (from pilot evidence)

1. **Stability handling is the central open design problem.** Options the evidence suggests: raise ARM C reps to k ≥ 3 with a majority/modal winner-set rule; count a divergence only when reproduced in ≥ 2 of k reps; or treat any winner-set disagreement as INCONCLUSIVE for that case (the draft's current rule — which this case shows will trigger often enough to starve the gate).
2. **The winner-set mapping needs hardening before seal.** Two gaps found live: a check-first close can contain a values-fork inside one branch (rep 1) — "branch heads" does not fix an extraction; and secondary/conditional levers (rep 3) blur the head set. Strongest fix: require each Recommend envelope in the sealed run to declare its winner-set as a structured artifact (the close's own branch heads, machine-readable), so extraction is not operator judgment. The `your call` shape also remains unmapped in the draft (flagged pre-run).
3. **Batch seams are visible.** Rep 3's close cites "three independent shaping passes" — the merged surface leaks batch structure, and recommenders interpret it. The seal's batching rule should either normalize seams in the merge or accept and disclose the leak symmetrically.
4. **Case-shape input:** this case's field carried no per-option cost or volume figures (every close flagged it), which plausibly widens recommender variance by leaving the surface structurally underdetermined. The panel should decide whether the sealed case-writer requirements demand a minimum quantitative-fact density per field, or whether fact-sparse fields are precisely the population of interest.
5. **Contest's miss is a finding to carry:** the excluded eventual control-winner was not among Contest's named live challenges on this run. If the sealed run wants Contest-surfacing as a descriptive measure, record it per case as here.

## Case-2 decision

Closed at one case plus the rep-3 probe. All five pilot obligations are answered, and the marginal value of a second case under the current ARM C design is dominated by the design revisions the panel must now settle (stability rule, structured winner-set declaration, seam normalization, case-shape fact-density); a second pilot case is better spent after those revisions, if the panel wants one. The draft authorizes one to two cases; this is a one-case close with the reasoning stated.

## Harness as executed, and every deviation (disclosed)

Frozen surfaces: repo `main` at `e6db816` (clean; the eight v30 method-surface hashes verified equal to the committed v30 smoke pins; 162/162 fixtures and `check-renderings` green at preflight; macOS 26.5.2, uv 0.10.11, CPython 3.13.12). Stage agents: fresh, non-forked sonnet agents in both arms, one per dispatch, briefs delivered by hash-verified file, envelopes returned by file and helper-validated before acceptance; every brief rendered by the shipped helper with its render identifier recorded before dispatch. Shared stem: setup document authored once by the operator from the frozen invocation; the stored invocation wording byte-compared to the fixture in both stores (the v30 gate); the accepted Generate envelope re-validated and accepted byte-same into the control store; stem brief-ids identical across stores.

Deviations from the shipped contract / v30 smoke shape, all harness accommodations: operator-as-orchestrator (no background orchestrator agent; stage packet isolation preserved); named store roots under the session scratchpad (not the fixed live-run locator; multiple concurrent stores); ARM P capsule assembly skipped (winner-set, records, and Contest line come from accepted envelopes; close/capsule overhead priced from the v30 smoke); a relay-note file-transport rule replacing the chat fence (its absence killed run r1 — disclosed); a mechanical schema note added to relay notes after the batch stage-label defect (ARM P's Generate and Prune ran before it existed; all later dispatches in both arms carried it); ARM C's identity-Prune and merged-Shape envelopes are synthetic harness scaffolding accepted through the shipped validator (partition trivially conserved; no packet-isolation claim is made for ARM C); ARM C rep stores are pre-acceptance clones sharing one run identifier so each rep's envelope gets mechanical validation; rep 3 was an extra-protocol exploratory probe beyond the draft's one re-run.

Blinding: no ground-truth judge was spent — divergence detection is mechanical, no adjudication panel convened, and JP-as-cold-judge remains unspent. The operator saw everything (the draft concedes this). The pilot case is spent and excluded from any sealed case set.

## What this pilot does not establish

It does not measure the prune's damage rate (one case, no adjudication); it does not validate ARM C as ground truth (the draft is explicit that the control is an instrument, and this pilot demonstrated its variance); it does not test the adjudication layer, the blinding machinery under load, the case-writer pipeline at scale, or the sealed run's cost at full replication. Zero of those claims should be read into it.

## Evidence appendix (verbatim artifacts)

The session-scratchpad working artifacts (stores, relay dirs, batch envelopes) are ephemeral; this appendix is the durable record. Envelope hash ledger — stem Generate `fa8cfd53…`; ARM P: Prune `f35cf36e…`, Shape `41382b27…`, Recommend `dcc3406c…`, Contest `03ad36df…`; ARM C: rep 1 `dbc28baf…`, rep 2 `dd08d1b9…`, rep 3 `d733cb52…`. Brief-id ledger — Generate `19ab031a…` (identical both stores), Prune `58ce244e…` (identical both stores), ARM P Shape `7cdfc3be…`, ARM P Recommend `6a480246…`, ARM P Contest `5ac5a8a7…`, ARM C full-field Shape `d32d9f78…`, ARM C Recommend `d193c1fa…` (84,730 bytes, identical bytes to all three reps).

### A1. Case invocation (frozen fixture, SHA-256 ebc4847dcfdea14ddffb4114eccf3f06e1fa6a5b9253c208f87b3462b51416e9, 4,591 bytes)

```text
$deliberate

I need to choose how the Riverbend Regional Food Network will close a widening gap between food demand and supply over the next twelve months. I lead the operations team of fourteen full-time staff serving about 22,000 households across six counties. Demand has reached about 4.1 million pounds per year against our current throughput of 3.2 million, a gap near 900,000 pounds. A restricted grant funds one cycle of change; I must commit this quarter and show results before it ends.

Field mode: seed-and-widen.

Candidate seeds:
1. Sign daily retail-rescue agreements with regional grocery chains to collect near-expiry and cosmetically-imperfect food.
2. Form a shared purchasing co-op with three neighboring food banks to buy shelf-stable staples in bulk.
3. Buy and operate two mobile pantry trucks that distribute directly in the six rural counties.
4. Convert the main distribution site to a client-choice model where households select their own groceries.
5. Contract a logistics firm to deliver prepacked boxes to homebound and remote clients.
6. Build refrigerated warehouse space to accept large perishable donations we now decline.
7. Launch a structured volunteer recruitment and retention program to raise sorting and packing throughput.
8. Consolidate the nine neighborhood drop points into four larger hubs and redirect the logistics savings to food purchasing.

Confirmed constraints, each at its price:
- One-time capital is hard-capped at $480,000 from a non-transferable restricted grant. Price: the refrigerated warehouse is quoted at $610,000 and cannot be built this cycle without a separate capital campaign that forfeits the grant deadline.
- The grant claws back funds unless a documented rise in food distributed lands within twelve months. Price: any approach that cannot show gains in the window, including co-op deals that take six to nine months to settle, risks forfeiture.
- Recurring operating budget rises by only $220,000 per year, and each loaded new hire costs about $55,000. Price: at most three net new staff are affordable, so any labor-heavy option must strand core distribution or lean on volunteers.
- Cold-chain capacity is fixed at forty pallet positions until storage grows. Price: perishable sourcing and delivery are capped, so retail-rescue and home delivery can only scale on shelf-stable goods.
- Rural service across the six counties is a standing board mandate covering thirty percent of our clients. Price: any consolidation that closes a rural drop point is off the table regardless of the savings.

Stated values:
- Reaching more households matters more than lowering cost per pound; I will accept a higher cost per pound in exchange for closing more of the demand gap.
- Dignity of service matters more than line speed; I will accept slower distribution in exchange for letting clients choose their food.
- Reliability for current clients matters more than reach at the margin; I will accept up to a five percent dip in service to existing clients to fund expansion, but not one point more.
- Long-term resilience matters more than one-year optics; I will accept smaller first-year gains in exchange for capacity that compounds later.
- Staff wellbeing matters more than peak surge output; I will accept lower maximum throughput in exchange for not burning out the fourteen staff I have.

Soft preferences and visible lean:
- All else equal, I prefer approaches I can explain to our board and donors in a single meeting.
- My current lean is toward "Launch a structured volunteer recruitment and retention program to raise sorting and packing throughput." because it needs no capital and we already employ a volunteer coordinator, so it is the easiest thing to start now. This is a soft preference, not a constraint or an instruction to preserve that candidate.

Stakes context:
- Stakes are high and only partly reversible: capital purchases are hard to unwind, program launches can be stopped, and a wrong choice risks grant clawback plus a year of unmet demand across roughly 9,000 household visits.

Evidence inputs:
- Use only the facts supplied in this prompt as decision evidence.

Evidence authorization:
- No additional decision-evidence sources, web research, project or user files, or external probes are authorized.
- Mandatory skill, reference, constituent-contract, Git-state, and mechanical-validation reads required by the deliberate contract are authorized.
- No side-effecting checks are authorized.

Survivor budget: 4.

Inline-degradation permission: not granted.

Run the complete deliberation now.
```

### A2. ARM P Prune survivors (8, disclosed 2x-budget overflow)

```text
[generated] Buy or lease a fractional share of existing refrigerated storage with neighboring food banks or a commercial cold-storage operator, adding cold-chain capacity without the full capital outlay of owning a new warehouse.
[user-seed] Buy and operate two mobile pantry trucks that distribute directly in the six rural counties.
[user-seed] Convert the main distribution site to a client-choice model where households select their own groceries.
[user-seed] Contract a logistics firm to deliver prepacked boxes to homebound and remote clients.
[user-seed] Launch a structured volunteer recruitment and retention program to raise sorting and packing throughput.
[generated] Spend the added capital and operating dollars on the lowest cost-per-pound shelf-stable commodities such as rice, beans, and oil in bulk, dropping variety and choice in favor of maximizing raw pounds distributed per dollar.
[generated] Dedicate part of the grant to a community-garden, partner-farmland, or small-scale production pilot that grows food directly for distribution rather than acquiring it through donation, rescue, or purchase.
[user-seed] Sign daily retail-rescue agreements with regional grocery chains to collect near-expiry and cosmetically-imperfect food.
```

### A3. ARM P Prune exclusions (11 record options with bases)

```text
(constraint | fact-established at comparable resolution) Build refrigerated warehouse space to accept large perishable donations we now decline.
(constraint | fact-established at comparable resolution) Fund embedded benefits-enrollment specialists who connect client households to food-purchasing power outside the network, such as SNAP or WIC, shrinking the network's own measured demand rather than growing its supply.
(constraint | fact-established at comparable resolution) Hold total pounds distributed roughly flat and build a shared intake and prioritization system that directs existing supply toward the highest-need households first, serving fewer households more deeply rather than growing total throughput.
(survivor budget | contestable sketch-depth judgment) Consolidate the nine neighborhood drop points into four larger hubs and redirect the logistics savings to food purchasing.
(survivor budget | contestable sketch-depth judgment) Partner with a workforce-development or reentry program whose own funding pays wages for embedded sorting and packing crews, adding paid labor capacity without counting against the three-net-new-hire cap.
(survivor budget | contestable sketch-depth judgment) Add weekend and evening distribution shifts using existing food stock, existing staff on overtime or shift swaps, and existing infrastructure, with no new sourcing, storage, or hires.
(survivor budget | contestable sketch-depth judgment) Stop operating as the single direct-distribution site and instead become a sourcing, funding, and cold-chain aggregator that channels food and grant dollars through the six counties' existing smaller pantries and churches, who handle last-mile distribution themselves.
(survivor budget | contestable sketch-depth judgment) Form a shared purchasing co-op with three neighboring food banks to buy shelf-stable staples in bulk.
(survivor budget | contestable sketch-depth judgment) Partner with regional farms to run harvest crews that recover unharvested or surplus crops directly from fields, drawing on a donor pool and field logistics separate from grocery retail rescue.
(survivor budget | contestable sketch-depth judgment) Adopt or build a digital matching platform that pairs any regional donor — grocers, restaurants, caterers, farms — in real time with whichever partner agency or mobile unit is nearest, replacing one-to-one donor agreements with a many-to-many marketplace.
(survivor budget | contestable sketch-depth judgment) Redesign pickup logistics into a single efficient multi-stop collection route across many small donors who individually give too little today to justify a dedicated pickup, unlocking donors currently priced out by collection cost.
```

### A4. ARM P overflow disclosure

```text
disclosure: 'Independent cuts removed 3 of 19 candidates for conflicting, by their own stated design,
  with echoed price-confirmed constraints, leaving 16 for budget triage against a survivor budget of 4.
  Of those 16, 8 were cut as budget cuts, each disclosed as a distinct mechanism-level candidate whose
  seriousness was unresolved at sketch depth. The remaining 8 could not be cut further: cutting any of
  them would either require pricing at least one of the five stated value trades that no stated value
  resolves on its own terms, or would require overriding a value the packet already resolves in the candidate''s
  favor, or would require dishonestly labeling an established, comparably serious mechanism as one whose
  seriousness is unresolved. This lands exactly at the correctable overflow ceiling of twice the echoed
  budget (8 survivors against a budget of 4); the run should treat 8, not 4, as the true comparison width
  entering Shape.'
blocked-cuts:
- option: Buy or lease a fractional share of existing refrigerated storage with neighboring food banks
    or a commercial cold-storage operator, adding cold-chain capacity without the full capital outlay
    of owning a new warehouse.
  unpriced-trade: Cutting this in favor of another reach-serving survivor would require ranking which
    cold-chain-unlocking mechanism best serves reach (reaching more households matters more than cost
    per pound) without a stated tiebreaker between comparably plausible mechanisms.
  why-blocked: This reads as an established, comparably serious mechanism at sketch depth, the direct
    in-budget alternative to the warehouse option the constraints priced out, so the low-confidence unresolved-seriousness
    disclosure a budget cut requires does not honestly apply to it.
- option: Buy and operate two mobile pantry trucks that distribute directly in the six rural counties.
  unpriced-trade: Cutting this would weigh the rural-service board mandate's practical urgency against
    other reach-serving survivors without a stated value ranking rural-direct reach above or below them.
  why-blocked: This is a well-established mechanism directly serving the standing rural-service board
    mandate covering thirty percent of clients; sketch depth does not read its seriousness as unresolved,
    and no stated value discounts rural-facing reach relative to the other reach mechanisms.
- option: Convert the main distribution site to a client-choice model where households select their own
    groceries.
  unpriced-trade: Cutting this would price the dignity-of-service value (dignity matters more than line
    speed; slower distribution is acceptable so clients can choose their food) against reach or cost,
    a trade the value already resolves in the option's favor rather than leaves open.
  why-blocked: This is the field's clearest and only direct representative of the stated dignity and client-choice
    value; cutting it would leave that value unrepresented among the survivors rather than merely leave
    a trade unpriced.
- option: Contract a logistics firm to deliver prepacked boxes to homebound and remote clients.
  unpriced-trade: Cutting this would weigh reach to homebound and remote clients against other reach-serving
    survivors without a stated ranking between them.
  why-blocked: Contracted home delivery is an established, comparably serious mechanism at sketch depth,
    not a thin or unresolved one, and no stated value discounts it relative to the other reach-serving
    survivors.
- option: Launch a structured volunteer recruitment and retention program to raise sorting and packing
    throughput.
  unpriced-trade: Cutting this would price the staff-wellbeing value (staff wellbeing matters more than
    peak surge output) against reach or cost by removing the clearest survivor mechanism that adds capacity
    without loading the fourteen existing staff.
  why-blocked: This is the field's clearest representative of added throughput that draws on neither the
    three-net-new-hire cap nor existing-staff burden, directly answering both the operating-budget constraint's
    own suggested mitigation and the staff-wellbeing value; cutting it would leave that value's trade
    unrepresented.
- option: Spend the added capital and operating dollars on the lowest cost-per-pound shelf-stable commodities
    such as rice, beans, and oil in bulk, dropping variety and choice in favor of maximizing raw pounds
    distributed per dollar.
  unpriced-trade: Keeping or cutting this candidate directly implicates whether reach-per-dollar (reach
    matters more than cost) outweighs client choice and dignity (dignity matters more than line speed,
    framed around letting clients choose their food) in this specific case; neither stated value resolves
    the trade on its own terms, since reach is silent on variety and dignity is silent on cost-efficiency.
  why-blocked: Cutting this candidate would implicitly resolve that unstated trade in dignity's favor
    without authorization to do so.
- option: Dedicate part of the grant to a community-garden, partner-farmland, or small-scale production
    pilot that grows food directly for distribution rather than acquiring it through donation, rescue,
    or purchase.
  unpriced-trade: Cutting this for slow first-year payoff would price near-term optics against long-term
    resilience (resilience matters more than one-year optics; smaller first-year gains are acceptable
    for capacity that compounds later), a trade the stated value already resolves toward keeping this
    kind of option.
  why-blocked: The stated resilience value directly and specifically endorses exactly this candidate's
    profile of slow first-year yield and compounding capacity; cutting it on timeline grounds would override,
    not merely leave unpriced, that resolved value, and no other survivor carries the same long-horizon
    production-capacity trade.
- option: Sign daily retail-rescue agreements with regional grocery chains to collect near-expiry and
    cosmetically-imperfect food.
  unpriced-trade: Cutting this in favor of another reach-serving survivor would require ranking which
    supply-growing mechanism is strongest without a stated tiebreaker between comparably plausible, comparably
    established mechanisms.
  why-blocked: Retail rescue is one of the most established, lowest-risk mechanisms in the entire field
    at sketch depth; the unresolved-seriousness disclosure a budget cut requires does not honestly apply
    to it, and no stated value discounts it relative to the other reach-serving survivors.
```

### A5. The divergent excluded winner's complete Prune record (route redesign)

```text
option: Redesign pickup logistics into a single efficient multi-stop collection route across many small
  donors who individually give too little today to justify a dedicated pickup, unlocking donors currently
  priced out by collection cost.
status: active
delegation: Budget-cut authority under the survivor-budget packet item.
predicate-source: agent-derived proposition
cut-basis: survivor budget
epistemic-status: contestable sketch-depth judgment
reason: 'This is a distinct mechanism-level candidate whose seriousness was unresolved at sketch depth:
  it presumes a pool of small donors currently priced out by collection cost is both real and reachable
  by a redesigned route, a donor population the packet does not evidence, and the size of the resulting
  supply gain is unstated.'
load-bearing-premise: The option's benefit is conditioned on an unconfirmed population of currently-excluded
  small donors existing in reachable density along a feasible route.
strongest-case: A single efficient multi-stop route could unlock many small donors at low incremental
  capital cost, purely through smarter logistics rather than new capital or headcount, a cheap lever if
  the donor pool is as described.
revive-if: A donor survey or pilot route confirms a meaningful volume of currently-excluded small donors
  along a feasible collection path.
```

### A6. ARM P registered leans

```text
agent-first-lean: 'On first read, before the surface/consequences analysis, leaned toward option A --
  "Buy or lease a fractional share of existing refrigerated storage with neighboring food banks or a commercial
  cold-storage operator, adding cold-chain capacity without the full capital outlay of owning a new warehouse."
  Basis: agent-derived reading of the frame, the five constraints, the five values, and the survivor wordings
  alone (no authority note is attached to option A) -- A is the survivor built explicitly as the workaround
  to the single most specifically quantified constraint in the packet (the $480,000 cap against the $610,000
  full-warehouse price), and it showed no apparent first-read conflict against any of the five stated
  values, unlike F (dignity), G (implied clawback-timeline tension from its own growing-food mechanism),
  or E (throughput-vs-supply-gap framing tension). The structured comparison moved this lean to a conditional
  call favoring H or B as primary, with A recommended as a next-cycle structural move instead.'
user-visible-lean: 'Toward option E -- "Launch a structured volunteer recruitment and retention program
  to raise sorting and packing throughput." Basis: the authority note attached to option E in the authority-notes-survivor
  packet, direct user-supplied lean language, explicitly self-labeled as a soft preference and not an
  instruction to preserve the candidate ("it needs no capital and we already employ a volunteer coordinator,
  so it is the easiest thing to start now"). The final call does not make E primary; E is recommended
  as a zero-cost complement in every branch, and the divergence from this visible lean is stated plainly
  in the close''s Case Against section, since the evidence lines up against making it the primary lever
  within the twelve-month clawback window.'
```

### A7. ARM P close (verbatim; conditional call)

```text
Decision: which lever(s) the Riverbend Regional Food Network commits its one-time
$480,000 capital and $220,000/year recurring operating increase to, this quarter, to
close the roughly 900,000 lb/year demand-supply gap within the twelve-month grant
window, from the frozen eight-survivor field (labeled A-H on the comparison surface).

Field readiness: passed. All eight survivors received the same six-question treatment
(mechanism/timing, cost fit, cold-chain interaction, rural-mandate interaction,
dignity/staff-load, evidence-gap/reversibility) with gaps honestly flagged rather than
filled from generic knowledge, so the field was comparable enough to register leans and
compare, per the making-recommendations field-readiness bar.

Leans on entry (registered before reading the surface and consequences packet items):
my own first-read lean, from the frame, constraints, values, soft preferences, and
survivor wordings alone, leaned toward option A (fractional/shared cold storage) as the
survivor built explicitly as the workaround to the packet's single most specifically
quantified obstacle (the $480,000 cap against the $610,000 warehouse), with no apparent
first-read conflict against any of the five stated values. The user's own visible lean,
per the authority note attached to option E, was toward E (volunteer
recruitment/retention), stated explicitly as a soft preference, not an instruction to
preserve the candidate. The structured comparison below moved me off my own first lean;
it does not adopt the user's visible lean as the primary answer either, for the reasons
given below.

The Call: conditional call.

Primary branch fork: recommend H (daily retail-rescue agreements with regional grocery
chains) as the lead lever if a fast, cheap outreach check confirms the participating
chains have workable presence and rescue-agreement appetite across the six counties,
including the rural ones. If that check comes back weak or unconfirmed within a couple
of weeks, recommend B (two mobile pantry trucks serving the rural counties directly) as
the lead lever instead -- the field's most directly confirmed fit to the standing
rural-service mandate, at the cost of consuming most of the affordable hire ceiling and
committing capital that is harder to reverse.

In either branch: pair the lead lever with E (structured volunteer
recruitment/retention) as a zero-capital, staff-wellbeing-aligned complement -- it is
the decider's own stated lean, costs nothing, uses the existing volunteer coordinator,
and does not materially compete with either branch's resources. Also layer in C
(client-choice conversion at the main site) alongside either branch: it is the field's
clearest fit to the dignity/choice value and plausibly the most reversible option in the
field, and it does not draw meaningfully on the scarce capital or hire ceiling, even
though alone it would not close the pound gap.

Recommend A (fractional/shared cold storage) as a structural move for the next grant
cycle rather than this one: it does not itself produce a documented rise in pounds
distributed this cycle, and if structured as a multi-party co-op-style deal, its own
settlement timeline risks eating into this cycle's twelve-month clawback window. It
remains the field's clearest fix to the shared cold-chain bottleneck several other
options (B, D, H) operate under, and best matches the long-term-resilience value once
the current cycle's clawback risk is retired.

Decline to lead with F (lowest-cost-per-pound bulk shelf-stable commodities) or D
(contracted prepacked-box delivery) as the primary lever. Both are the field's most
legible cost/timeline fits, but both directly and self-evidently trade against the
client dignity/choice value the network has explicitly ranked above line speed -- F by
its own stated design ("dropping variety and choice"), D by format (prepacked boxes are
not client-chosen by definition). Nothing in the five stated values pulls specifically
toward F's cost-per-pound-minimization logic: the reach value explicitly tolerates a
higher cost per pound in exchange for reach, it does not ask the network to minimize
cost per pound. This is not an unresolved values trade the way the H-vs-B fork is; it is
a values conflict with no stated value pulling the other way.

Exclude G (community-garden/farmland/production pilot) from this cycle's comparison: it
fails the twelve-month documented-distribution-rise clawback constraint on its own
stated mechanism (see the disposition record). Revive it if the grant is renewed or
extended beyond this cycle, if unrestricted (non-clawback) capital becomes available to
cover its pre-yield period, or if a specific fast-cycle crop or an already-planted
partner-farmland arrangement with a confirmed within-window harvest can be named.

Why: the rural-service mandate and the twelve-month clawback are the two hard
constraints doing the most work. The clawback rules out G outright and creates real
timing exposure for A if co-op-structured. The rural mandate is most directly and
confirmedly served by B, though H can serve it too through the existing six-county
distribution backbone if collection-side chain coverage checks out -- that dependency,
not the mandate itself, is what makes the H-vs-B call conditional rather than clear. The
at-most-three-net-new-hires ceiling bounds how many labor-heavy options (B, C, H) can
run at full scale at once, favoring a lead-plus-light-complement sequencing over running
all three simultaneously. The dignity/choice value, stated above line speed, weighs
directly and without a stated counterweight against F and, to a lesser extent, D, which
is why neither leads despite their operational cleanliness.

The Case Against:
- For B, if the check favors H: B's case is that it needs no third party's cooperation,
  directly matches the board's own rural mandate, and puts the network fully in control
  of the mechanism end to end. Smallest realistic change to make B win outright: chain
  outreach confirms weak or no rural-county participation, or B's own truck cost and
  hire needs turn out to fit comfortably alongside E and C.
- For H, if the check favors B by default: H's case is that it is faster and cheaper to
  start, does not consume most of the scarce hire ceiling, and is more reversible than a
  truck purchase (cancellable agreements versus owned, hard-to-unwind assets, per the
  packet's own stakes note). Smallest realistic change to make H win outright: the
  chain-coverage check comes back positive.
- For E, the user's own visible lean, not made primary here: its case is zero capital,
  an existing coordinator, the clearest fit to the staff-wellbeing value, and the
  easiest thing to start this week. It is not made primary because its mechanism lifts
  internal processing throughput rather than growing or channeling new supply, and its
  throughput lift and ramp speed are unquantified in the packet, leaving real doubt that
  it alone could produce a documented pounds-distributed rise large enough to satisfy
  the clawback in twelve months. Smallest realistic change to elevate it to primary or
  co-primary: a credible internal throughput estimate, not present in this packet,
  showing volunteer-driven gains alone can plausibly close a meaningful share of the
  900,000-lb gap in the window.
- For F, the field's most legible cost/mechanism fit: its case is the lowest execution
  risk, no cold-chain or hire-ceiling exposure, and the fastest, cleanest path to a
  documented pounds rise of any of the eight. Smallest realistic change to make it win:
  if the board and donor base, and the decider's own judgment of clients' interests,
  would accept a time-boxed, explicitly communicated emergency shift to lowest-cost bulk
  staples solely to clear the clawback deadline, with variety and choice restored once
  the gap closes -- i.e., reading dignity/choice as flexible for one cycle under an
  explicit exception rather than an absolute.

What Would Flip It:
- The chain-coverage check (days, not months, via outreach calls to regional grocery
  chains' community-relations contacts) resolves the H-vs-B branch directly.
- None of A, B, F, or H has a quoted price or volume in the packet; any of these landing
  far outside expectation could shift which lever fits the $480,000 capital cap or the
  three-hire ceiling.
- A credible volunteer-throughput estimate for E, not present in this packet, could
  elevate it from complement to primary.
- Confirmed board/donor appetite for a temporary, explicitly time-boxed F-style measure
  could make F a serious clawback-deadline safety valve, though not a standing strategy.

Commitment Point: signing the primary-branch agreement (H) or issuing the truck
purchase order (B) this quarter, since the grant requires committing this quarter with
documented results before the grant ends.

Rollback / Blast Radius: H's agreements are the most cancellable of the field if
participation underperforms, with a narrow blast radius (mainly relationship and
reputational cost with the chains). B's truck purchase is the least reversible of the
group -- capital is sunk, resale is likely at a loss, and it also consumes hire-ceiling
headroom that cannot easily be reclaimed mid-cycle if the bet underperforms. E and C are
both stoppable programs with minimal blast radius if they underperform. A, if pursued
next cycle, is bounded by lease-term reversibility that the packet does not confirm but
that is plausibly more exitable than owning a warehouse outright. G is excluded this
cycle per the filter above; land or planted-crop commitments, if pursued anyway, would
sit closer to the hard-to-unwind end of the packet's own stakes note than most of the
rest of the field.

Evidence-gap note carried forward: none of the eight survivors carries a quoted hard
cost or volume figure in the packet; every branch and complement above rests partly on
each option's stated mechanism logic rather than confirmed numbers, consistent with the
shape stage's own close on this point.
```

### A8. ARM P Contest exclusion-check line

```text
Exclusion check: live recorded challenges — G (community-garden/partner-farmland production pilot, excluded by this close's own post-prune filter application rather than by an earlier stage), the three-neighboring-food-bank purchasing co-op (budget-cut survivor-budget record), most worth contesting: G
```

### A9. ARM C rep 1 close (verbatim; check first)

```text
Decision: which single-cycle intervention(s) to commit the $480,000 one-time capital cap and the $220,000/year operating rise to, in order to close (or make credible, documentable progress on) the roughly 900,000-lb annual demand-supply gap inside the twelve-month grant window, without violating the capital cap, the rural-service mandate, the fixed forty-pallet cold-chain cap, the three-net-new-hire ceiling, or the stated values.

The Call: check first. The unknowns here are load-bearing (they determine which entire branch of the option space can even work) and the check is cheap and internal, so per making-recommendations' high-stakes guidance the check is the recommendation itself, not a caveat on one.

Why — filters and dominance first: "Build refrigerated warehouse space to accept large perishable donations we now decline" is excluded outright (post-prune filter): it is quoted at $610,000 against a hard, non-transferable $480,000 cap, and the packet states it cannot be built this cycle without a separate capital campaign that itself forfeits the grant deadline. Two further options are excluded by dominance, each against a close rival that is at least as good on every criterion that matters and strictly better on one: "Add weekend and evening distribution shifts using existing food stock, existing staff on overtime or shift swaps..." is dominated by "Launch a structured volunteer recruitment and retention program..." (same reach ceiling, same grant-timing safety, same capital-lightness, but the shift option directly burdens the fourteen existing staff, which the volunteer program does not); "Partner with regional farms to run harvest crews..." is dominated by "Sign daily retail-rescue agreements with regional grocery chains..." (same cold-chain exposure, but the harvest-crew option additionally carries co-op-like partnership-formation timing risk against the twelve-month clawback and the field's worst staff-burnout exposure, with no offsetting strength found). Full reasoning and revival conditions for all three exclusions are in disposition-records.

Why — the central unresolved fact: across every batch of this comparison, the single most recurring, decision-controlling gap is whether the roughly 900,000-lb shortfall is primarily a SOURCING deficit (not enough donated or purchased food reaches the network at all) or a PROCESSING/THROUGHPUT deficit (enough food is offered or available, but the network cannot sort, pack, and distribute it fast enough with current hours and capacity). This single fact cleanly splits the surviving field into two structurally different, largely non-overlapping branches, and it is answerable quickly from data the network almost certainly already holds: current donor-offer volume versus what actually gets accepted and processed, any known backlog of unsorted donations, and any donors currently turned away or under-collected for capacity reasons rather than availability reasons. Committing this one-time, no-second-chance grant cycle to the wrong branch risks showing no documented rise at all and forfeiting the grant.

If throughput-bound (Branch A): the strongest bet is "Launch a structured volunteer recruitment and retention program to raise sorting and packing throughput" — safest on the clawback timeline of any survivor, capital-free, fits inside the hire ceiling via the network's existing volunteer coordinator, and the field's best fit to the staff-wellbeing value. Complement with "Buy and operate two mobile pantry trucks that distribute directly in the six rural counties" if the rural counties specifically need more direct reach and the (unpriced) truck cost and driver/loader staffing clear the operating ceiling — this is the field's strongest fit to the rural-service mandate, since it runs with that mandate rather than merely avoiding conflict with it. "Convert the main distribution site to a client-choice model where households select their own groceries" is a values-forward complement if the main site's throughput can absorb the change within the five-point reliability ceiling. Case against the runner-up in this branch: the case for the truck option over the volunteer program as the LEAD bet is that it adds owned, durable, rural-facing capacity that compounds — matching both the resilience value and the rural mandate directly — where the volunteer program only speeds processing of food already on hand and does nothing if the real ceiling is sourcing, not hours. It would win outright if the truck routes are confirmed to fit under $480,000 alongside any other capital draw this cycle, and if driver/loader labor is confirmed to fit the three-hire ceiling without straining the existing fourteen staff or the wellbeing value.

If sourcing-bound (Branch B): the field's own leaned candidate, the volunteer program, provides essentially no benefit here — it only speeds processing, and by hypothesis processing is not the constraint — so the branch turns on a genuine values trade, not a fact. "Spend the added capital and operating dollars on the lowest cost-per-pound shelf-stable commodities such as rice, beans, and oil in bulk, dropping variety and choice in favor of maximizing raw pounds distributed per dollar" is the fastest, safest, most direct fit to closing the gap, but its own wording states it costs the dignity/choice value the decider ranks above raw throughput — a real, self-declared cost, not merely a risk. "Sign daily retail-rescue agreements with regional grocery chains..." and "Buy or lease a fractional share of existing refrigerated storage with neighboring food banks or a commercial cold-storage operator..." both add real supply while preserving variety/choice, at the cost of being cold-chain-bounded (retail-rescue) or carrying unpriced capital and co-op-style timing exposure (the lease/co-op option). "Adopt or build a digital matching platform..." is the most structurally different, largest-theoretical- reach bet in the whole field, and also the least proven — its own wording forks between a fast, lower-cost "adopt" path and a slow, expensive "build" path that carries the same timing risk the grant's clawback price names; only the adopt path belongs in this branch's comparison. Case against the runner-up in this branch: the case for retail-rescue or the lease/co-op option over the bulk-buy option is that they buy reach without spending down a value the packet gives no price discount for. The bulk-buy option would win outright if the decider confirms that speed-to-documented-rise this cycle is judged to dominate the choice/variety cost this year — i.e., if clawback risk is treated as the single largest threat this cycle.

What would flip it further, beyond the check: these options remain live in the field but were not developed as branch leaders because each carries a severe, load-bearing conflict with a named constraint or value that the packet's own text leaves unresolved rather than confirms or clears. "Fund embedded benefits-enrollment specialists..." and "Hold total pounds distributed roughly flat and build a shared intake and prioritization system..." both shrink or flatten the network's own measured distributed pounds by design, in tension with both the grant's documented- rise requirement and the reach-over-cost value; either could re-enter contention only if the grant administrator confirms a reading of "food distributed" broad enough to credit demand reduction or reallocation. "Stop operating as the single direct-distribution site and instead become a sourcing, funding, and cold-chain aggregator..." stacks the most simultaneous risk in the field (unpriced capital that could exceed the cap, a core mechanism that collides with the forty-pallet cap, and an unresolved question of whether partner-routed pounds even count under the grant's metric) against the field's largest theoretical reach if it worked; it needs the metric question resolved before it is a serious contender this cycle. "Consolidate the nine neighborhood drop points into four larger hubs..." is very likely to close at least one rural drop point, which the rural mandate bars outright regardless of savings, and its entire savings thesis is undercut once every current rural point is preserved inside four hubs; it would need an explicit, geometry-confirmed plan showing zero rural closures before it re-enters either branch, and even then it is the field's least reversible bet if the choice proves wrong. "Form a shared purchasing co-op with three neighboring food banks..." and "Partner with a workforce- development or reentry program..." both carry the same co-op-like partnership-formation timing exposure the grant's own price text names (six to nine months), without a compensating strength strong enough to lead a branch outright. "Dedicate part of the grant to a community-garden, partner-farmland, or small-scale production pilot..." is the field's sharpest values-versus- constraint tension: its fit to the resilience value (smaller first-year gains for capacity that compounds later) is real, but the grant carries no carve-out for compounding investment and requires a documented rise inside twelve months regardless of rationale — seasonal production is unlikely to clear that bar this cycle and reads better as a candidate to shape for next cycle's grant rather than this one's.

Other material unknowns and their cheapest checks, beyond the sourcing-versus-processing question: for the truck option, a same-cycle vehicle-and-staffing quote against the $480,000 cap and the three-hire ceiling; for the lease/co-op cold-storage option, a term-sheet estimate of buy-in or lease cost and expected time-to-signed-agreement; for the digital-matching option, a firm adopt-versus-build cost quote, since the two paths carry very different risk profiles under one survivor wording; for the client-choice conversion, an estimate of any throughput dip at the main site against the five-point reliability ceiling.

Commitment Point: capital draws — truck purchases, a cold-storage lease or buy-in, any aggregator-style facility upgrade — become costly to reverse at the point of purchase or signature. Staffing and programmatic launches (the volunteer program, added shifts, a logistics contract) remain stoppable up to the point of hiring, onboarding, or contract execution. The sourcing-versus-processing check itself commits nothing and is fully reversible.

Rollback / Blast Radius: a wrong throughput-side bet (Branch A) costs mainly coordinator time and a modest operating draw, recoverable within the cycle if it does not pan out. A wrong supply-side capital bet (Branch B) is harder to unwind mid-cycle and risks stranding capital that cannot be redeployed before the twelve-month deadline — directly threatening the grant's clawback condition if the resulting rise does not land in time, on top of a year of roughly 9,000 household visits' worth of unmet demand if the bet is wrong.

On the decider's stated lean: the volunteer program was both this agent's own first-read lean and the decider's self-labeled soft preference. This close agrees with that lean only conditionally, in Branch A, and says plainly why: if the sourcing-versus-processing check comes back sourcing-bound, the volunteer program's own mechanism cannot close the gap at all — the lean does not survive that branch. The agreement is therefore checkable, not assumed: what would have to be true for the volunteer program to be the wrong pick is exactly the fact this close recommends checking first.
```

### A10. ARM C rep 2 close (verbatim; clear call on the Prune-excluded route redesign)

```text
Decision: Which single strategy the Riverbend Regional Food Network should commit
this grant cycle's capital and operating dollars to, in order to close the widening
gap between food demand (~4.1M lbs/yr) and current throughput (~3.2M lbs/yr) within
the twelve-month window the restricted grant allows.

The Call: Clear call — Option 19, "Redesign pickup logistics into a single efficient
multi-stop collection route across many small donors who individually give too
little today to justify a dedicated pickup, unlocking donors currently priced out
by collection cost."

Why: Of the nineteen supplied survivors, three fail the packet's own hard
constraints outright and are excluded below (build-warehouse on the $480,000
capital cap; benefits-enrollment specialists and hold-flat/reprioritize on the
twelve-month documented-rise clawback condition, since both are defined by
mechanisms that do not raise the network's own distributed-pounds metric). Hub
consolidation survives only in a materially narrower, rural-preserving form than
as stated, and is carried forward as a live but structurally wounded option rather
than excluded, since the evidence does not confirm it must close a rural point. No
dominance relationship holds across the remaining fifteen: every survivor is
missing the same class of packet-supplied fact (a cost figure, a projected-pounds
figure, or both), so none can be shown strictly better on everything.

Given that, the decision turns on structure, not a weighted score. Because the
grant is one-shot and non-transferable, any capital or operating dollars spent on
an option that then misses the twelve-month documented-rise condition are lost
along with whatever durable capacity they were meant to build — timeline risk
against that single hard constraint is therefore prior to, not merely one input
among, the other criteria. That reasoning demotes several genuinely values-aligned
options (the cold-storage lease/co-op, the workforce-development partnership, the
purchasing co-op, the production pilot, the regional-farm harvest crews) below
where a flat weighing would place them, because each carries a real, named
resemblance to the six-to-nine-month settlement pattern the grant's own constraint
text calls out as a forfeiture risk.

Among the survivors carrying little or no such timeline risk, Option 19 and Option
14 (the lowest-cost-per-pound bulk-buy) are the two genuinely strongest candidates.
Both are fast, low-capital, and structurally safe against the clawback. Option 14
has the more direct lever on the single highest-ranked stated value ("reaching more
households matters more than lowering cost per pound"), and is arguably the single
safest, fastest option in the entire field against the deadline, since spend
converts to purchased pounds almost immediately with no partner or adoption
dependency. But Option 14's own wording self-declares a trade against a second
stated value: "dropping variety and choice in favor of maximizing raw pounds
distributed per dollar," in direct tension with "dignity of service matters more
than line speed... letting clients choose their food." It is also, by its own
framing, a one-cycle spending pattern rather than durable capacity — in tension
with "long-term resilience matters more than one-year optics; smaller first-year
gains are acceptable in exchange for capacity that compounds later."

Option 19 does not carry either of those two collisions: nothing in its evidence
suggests a dignity/choice cost, and its mechanism — a durable route-and-relationship
structure that keeps unlocking donors as it operates — reads as capacity that
compounds rather than a one-year spike. It also grows genuinely new supply (donors
"currently priced out by collection cost") rather than reallocating existing
pounds, so it serves the top-ranked reach value on its own terms, not merely by
discounting a competing value. Because the user's own values packet already states
how they resolve a reach-versus-dignity, reach-versus-durability trade like this
one ("acceptable in exchange for" language on both counts), applying that stated
exchange rate — not inventing one — is what carries Option 19 over Option 14 here.

The Case Against: Option 14 is the field's most serious rival, and the case for it
is real, not a token concession. If the decider is willing to treat this cycle's
dignity/choice cost as a one-time, correctable trade rather than a standing
compromise, and treats maximum, fastest, most certain raw-pound impact against the
clawback deadline as the dominant concern this cycle, Option 14 plausibly closes
more of the 900,000-pound gap, faster, with less execution uncertainty than Option
19's still-unbuilt logistics redesign and donor recruitment. The smallest realistic
change that would flip the call: an explicit board or funder decision to suspend
the dignity/choice value for this grant cycle only, or evidence that Option 19's
donor-recruitment timeline or per-route tooling cost is nontrivial enough to erode
its safety advantage over Option 14 — neither is established in the supplied
evidence.

What Would Flip It:
- If the decider suspends the dignity/choice value for this cycle, take Option 14
  instead (priced above).
- If a quick internal check shows the 900,000-pound gap is predominantly a
  processing/labor bottleneck rather than a sourcing bottleneck — i.e., the network
  already has more donated food offered than it can currently sort and move — the
  case shifts toward Option 9 (volunteer program) or Option 10 (partner-funded
  crews), which raise throughput on food already on hand rather than growing
  supply; this is the single largest evidence gap shared across the whole field and
  the cheapest one to check internally before committing.
- If the network secures the roughly $130,000 warehouse shortfall from a source
  outside this restricted grant, Option 1 returns to the field as the strongest
  durable-capacity play this cycle.
- If the board confirms in advance that a redesigned four-hub layout can retain all
  nine currently served rural points, Option 8 becomes viable without violating the
  rural mandate, though likely with less of the originally claimed logistics
  saving.
- On the user's own stated lean: I disagree with it, and say so plainly rather than
  soften it. The authority note's lean toward Option 9 (volunteer program) is
  genuine and well-reasoned on staff-wellbeing grounds — Option 9 is the single
  safest, most wellbeing-protective option in the whole field, exactly as the user
  described. It does not win here because the supplied evidence does not establish
  that raising processing throughput, rather than growing supply, is what actually
  closes a gap this large; if that sourcing-versus-processing question resolves the
  other way (see above), Option 9 becomes the stronger pick, and it should be
  revisited first. My own first-read lean, formed independently and before reading
  the shaped comparison, was toward Option 16 (retail-rescue agreements) for
  similar low-capital, fast-start reasons; the structured pass moved me off that
  lean too, once Option 19's comparable safety plus stronger resilience/dignity fit
  and Option 16's hard cold-chain scale cap became clear side by side.

Commitment Point: The choice among survivors remains fully reversible through this
comparison; it becomes costly to reverse once grant capital or operating dollars
are formally committed and drawn down against a chosen strategy — for Option 19,
once donor-recruitment outreach and route/logistics tooling spend are underway and
the twelve-month clock is running without a checked fallback.

Rollback / Blast Radius: Option 19 itself is comparatively easy to unwind: it is a
logistics and donor-relationship redesign, not a facility purchase or a durable
staffing commitment, so a poor early read (donors do not respond, collected volume
stays low) can be paused or redirected mid-cycle without stranding capital,
consistent with the stakes note that "program launches can be stopped." The
harder-to-unwind risk sits one level up and attaches to every option in the field,
not to Option 19 specifically: if twelve months pass without a documented rise in
distributed pounds, the restricted grant is clawed back regardless of which
strategy was chosen. Name a mid-cycle checkpoint (for example, month three or four)
to compare actual donor-recruitment and pounds-collected trajectory against what a
documented rise requires, and decide then whether to layer in Option 14 or Option
16 as a faster-acting supplement, both being low-capital enough to add without
abandoning Option 19's sunk tooling or donor relationships.

Evidence gap carried forward, honestly: no option in the supplied field —
including the pick — carries a packet-supplied cost estimate or a
projected-pounds figure, so how much of the roughly 900,000-pound annual gap
Option 19 could plausibly close cannot be tested against the evidence in hand;
this is not a confirmed strength claim, only the strongest structurally-supported
bet available on the evidence supplied.
```

### A11. ARM C rep 3 close (verbatim; check first — extra-protocol probe)

```text
Decision: which lever the Riverbend Regional Food Network commits this quarter's
restricted-grant cycle to for closing the roughly 900,000-lb annual demand-supply gap,
chosen from the nineteen frozen survivors, under the five confirmed constraints and the
five stated values.

The Call: check first. Before committing the cycle to a specific option, run one cheap,
internally-answerable diagnostic: how much of the roughly 900,000-lb gap is a sourcing
shortfall (food the network cannot currently obtain at all) versus a processing/hours
shortfall (food arriving but not sorted, packed, or distributed fast enough at current
capacity)? This is derivable from the network's own existing intake, waste, and backlog
records, needs no new purchase, partnership, or capital commitment to learn, and is
answerable in days, not months — well inside the "commitment this quarter" deadline. It
is not a fact this packet supplies, and this stage's evidence authorization covers only
facts already in the prompt with no additional probes authorized; per that authorization,
an unresolved cheap-check question returns as a check-first recommendation rather than an
invented assumption.

Why: across three independent shaping passes over this field, the packet names this same
unresolved fact as the one most likely to change which class of option is worth the
cycle's commitment. A processing-constrained gap favors "Launch a structured volunteer
recruitment and retention program to raise sorting and packing throughput" as the primary
bet: of the sixteen surviving candidates it is the only one that needs no meaningful
capital, adds no hours to the existing fourteen staff (protecting the stated
staff-wellbeing value), can start immediately with no external partner-formation step
exposed to the twelve-month clawback clock, and matches the decider's own disclosed soft
preference. "Add weekend and evening distribution shifts using existing food stock..." is
the faster but riskier secondary lever in that branch, since its own wording does not
specify whether the added hours are staffed by volunteers or by the existing fourteen,
and the latter directly trades against the staff-wellbeing value. A sourcing-constrained
gap instead favors "Sign daily retail-rescue agreements with regional grocery chains..."
as the fastest new-supply lever (no capital, near-immediate start), with "Buy or lease a
fractional share of existing refrigerated storage with neighboring food banks or a
commercial cold-storage operator..." as a stronger but capital- and timeline-uncertain
second bet if it clears the $480,000 cap with margin, since it would add durable
cold-chain headroom rather than only filling the network's existing forty pallet
positions faster. In this branch, throughput-only options such as the volunteer program
or added shifts would raise processing capacity against a supply ceiling that isn't the
actual bottleneck, and would under-deliver on the reach value relative to a supply-side
bet.

Three candidates are excluded outright regardless of which branch the check resolves to,
because each fails one of the five confirmed hard constraints on its own stated
mechanism, independent of the sourcing-versus-processing question: "Build refrigerated
warehouse space to accept large perishable donations we now decline" (quoted at $610,000
against a hard $480,000 one-time capital cap, and, as specified, not buildable this cycle
without forfeiting the grant deadline); "Hold total pounds distributed roughly flat and
build a shared intake and prioritization system..." (by its own wording holds total
pounds distributed flat by design, which does not satisfy the grant's twelve-month
documented-rise condition); and "Fund embedded benefits-enrollment specialists...
shrinking the network's own measured demand rather than growing its supply" (by its own
wording does not raise the network's own distributed pounds, so it does not satisfy the
same documented-rise condition). Each carries a disposition record with its own revival
condition below; none is closed permanently.

The Case Against, for each branch's leading pick: against the volunteer program, the
packet cannot confirm volunteer supply will actually materialize at the scale needed, and
weekend/evening shifts would beat it on speed and certainty if staffed in a way that does
not draw on the existing fourteen. Against retail-rescue agreements, the fixed
forty-pallet cold-chain cap bounds its achievable scale regardless of grocery-partner
interest, and lease/co-op cold storage would beat it if it clears the capital cap with
real margin, since it adds capacity rather than only filling what already exists faster.

What Would Flip It: the diagnostic result is the primary flip — sourcing-constrained
points the cycle at supply-growing options, processing-constrained points it at
throughput-growing options, and a genuine mix of both would put the volunteer program and
retail-rescue agreements on the table together rather than as branch-exclusive picks,
subject to the $220,000/yr and three-net-new-hire ceiling covering both. Separately, if
the grant administrator confirms that partner-routed pounds or demand-reduction gains can
satisfy the "documented rise in food distributed" condition, two of the three excluded
candidates above (the benefits-enrollment specialists option, and — beyond this field's
filters — the aggregator-pivot option carried elsewhere in this packet as a preserved,
not-cut consequence) would need to be re-opened from a materially different starting
point than assumed here.

Commitment Point / Rollback: nothing in this recommendation commits capital or new
headcount yet. The diagnostic itself is low-cost and reversible — it is a records pull,
not a program launch — so running it does not consume meaningful runway against the
quarterly deadline; the actual capital- or hiring-bearing commitment should follow
promptly once the branch is known, since the twelve-month clawback clock does not pause
for the check.
```

### A12. Operator metering log (UTC)

```text
event	timestamp	detail
preflight-green	2026-07-19T15:14:00Z	fixtures 162/162, hashes = v30 pins
gen-dispatch	2026-07-19T15:21:00Z	brief 19ab031a, 10355 bytes, sonnet
r1-killed	2026-07-19T15:29:12Z	fenced envelope failed validate-envelope (harness relay-note bug); shipped fail-fast honored; fresh run r2
gen-accepted	2026-07-19T15:36:30Z	envelope fa8cfd53, 19-option field (8 seeds + 11 generated), model claude-sonnet-5; accepted into both stores
parallel-dispatch	2026-07-19T15:39:30Z	ARM P prune (brief 58ce244e, 18302 B) + ARM C shape b1-b5 (spliced from d32d9f78), 6 sonnet agents
b1-killed	2026-07-19T15:42:00Z	stage label option-shaping (canonical: shape); redispatch b1-r2 with schema note
b4-killed	2026-07-19T15:47:00Z	stage label option-shaping again (2 of 5 batches); redispatch b4-r2 with schema note
prune-accepted	2026-07-19T15:52:30Z	envelope f35cf36e; 8 survivors (2x-budget overflow disclosed), 11 records (3 constraint fact-established, 8 budget contestable); leaned candidate survived
shape-merged-accepted	2026-07-19T15:53:00Z	merged 5 batches, 25 consequences, surface ~59KB; recommend brief d193c1fa 84730 B; rep1+rep2 dispatched
p-shape-dispatch	2026-07-19T15:56:00Z	brief 7cdfc3be, 10486 B, 8 survivors
c-rep1-accepted	2026-07-19T16:04:00Z	envelope dbc28baf
c-rep2-accepted	2026-07-19T16:01:30Z	envelope dd08d1b9 (clone store)
p-recommend-accepted	2026-07-19T16:11:00Z	envelope dcc3406c; conditional call, 1 disposition record
p-contest-accepted	2026-07-19T16:15:30Z	envelope 03ad36df; live challenges G + purchasing co-op, most worth contesting G
rep3-dispatch	2026-07-19T16:20:00Z	exploratory extra-protocol stability probe, same brief d193c1fa
```
