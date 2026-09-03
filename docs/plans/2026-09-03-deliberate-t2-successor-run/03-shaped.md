# T2: six candidates shaped to comparable resolution

Stage: Shape (`option-shaping`), 2026-09-03, inside a `deliberate` 2.0 run. This file is a comparison surface (the skill's name for a rank-free side-by-side). It contains no ranking, lean, filter, or recommendation.

**Field provenance.** The six candidates and their order were produced by the upstream workflow's Generate and Prune stages, not by the user. JP invoked `deliberate` and delegated candidate selection to the run. Under option-shaping's rules for an authorized composition workflow, I worked on exactly these six, in this order, and did not add, merge, split, rename, drop, or filter any. Candidate 3 is the user's own and is quoted as given.

**Decision question.** What should be done with T2, the shallow-prune safety experiment, now that the `deliberate` skill has been rebuilt light as version 2.0 and still contains a shallow Prune stage?

**Terms** (from the brief, repeated so this file stands alone). ARM P: T2's shipped-pipeline arm (Generate, Prune, Shape, Recommend), which was the version-1 pipeline. ARM C: T2's control arm, which shaped the whole field with no Prune and then recommended. k: repeat Recommend runs per case. Crosswalk: the table mapping each candidate wording to a stable ID, made at stem-freeze (when the shared field is frozen). Survivor count: how many options Prune keeps (about four by default in 2.0). Seeded case: a case built with one candidate designed to be strongest yet fall to the survivor count. Divergence: a control-arm close that crowns a candidate the pipeline arm cut. S2: the one T2 case that produced a divergence. Close: a Recommend stage's final written recommendation. Rate gate: T2's name for its main pass/fail count. Hardened adjudication: T2's sealed procedure for testing a divergence (re-shape both candidates under one neutral condition, then blind judges). Version 1: the skill as it was when T2 ran.

## The six candidates, quoted exactly

1. **Adjudicate the one divergence** — Take the S2 candidate that ARM C crowned once in seven repeats and ARM P cut in both its repeats, re-shape it and ARM P's winner under one identical neutral single-pass condition, and put the pair to two agent judges whose read scope is confined to that packet.
Sets it apart: bets the single existing catch is a real one, on the panel control seat's reading that a rare crowning which survives clean adjudication counts; one packet, not the adjudication layer as sized.

2. **Same fields, 2.0 Prune** — Run version 2.0's Prune method on the seven frozen T2 fields and compare its exclusion sets with the stored ARM P sets (which agreed with themselves at 0.52 to 1.00 intersection over union).
Sets it apart: does not test safety; tests whether T2's data describes the rebuilt Prune at all, which decides whether any use of T2's artifacts is about 2.0.

3. **User's candidate (theirs, quoted exactly):** "Close T2 as unanswerable at acceptable cost and rely on watching real runs of the rebuilt skill instead."
Sets it apart: the detectors are the cut ledger, the Contest line, and the re-run offer already in 2.0; JP's reading of them is the judge; no apparatus beyond the skill.

4. **Develop one cut per run** — After every real close, a fresh agent shapes the survivor-count cut with the strongest recorded case and reports whether it beats the close.
Sets it apart: bets a missed winner would be the cut whose own record argued hardest for it (the one T2 divergence was exactly that); accrues one observation per run without JP's attention.

5. **Known-answer cases, Prune only** — Author decision cases where the best option is fixed by the evidence in the case but not obvious at sketch depth; run only 2.0's Prune and count how often the known winner is cut.
Sets it apart: no control arm, no judge, no blinding, because the ground truth is written into the case; rests on such cases being writable without the winner showing.

6. **Seeded-dominator run** — The successor the Results section sketched: from one to about a dozen seeded cases, the seeded candidate's crosswalk ID recorded at stem-freeze, k of 3 to 4 on the measured 0.71 committal rate, agent judges with confined read scope, allowlist-only inspection scripts from the first dispatch.
Sets it apart: measures the instrument's sensitivity directly instead of waiting for a roughly 2% spontaneous rate; a positive result gives T2's existing 48-of-49 non-divergence a meaning it does not have now.

## The live comparison questions

Derived from the outcome (know whether 2.0's Prune excludes winners), the two binding constraints (well under 15 operator hours; the repo's blind-evaluation rule), the stated values, and the six candidates. Each is live because plausible answers separate the candidates or could reverse the eventual choice.

- Q1. What can the candidate's result say about whether Prune excludes winners, and is that statement about 2.0's Prune or about version 1's?
- Q2. Where does the candidate's "this really was the winner" judgment come from, and what could make it wrong?
- Q3. What does it cost in operator time, when is that cost paid, and when does the observation arrive?
- Q4. What does the blind-evaluation rule require of it, and what does that add?
- Q5. What must exist, or happen, for it to produce any observation at all?

Omitted as not distinguishing: token cost (T2's binding constraint was operator attention, not tokens; prereg Cost section, line 91) and web research (constraint 3; no candidate needs it).

Evidence read: the prereg's frontmatter, Question, Arms, Winner-set extraction, Divergence/adjudication, Replication, Leakage, Case set, Attrition, Pass/fail, Descriptive measures, Cost, Parameters-fixed-at-seal, Amendments 1 and 6, and Results; the design panel report whole; the shape assessment whole; deliberate 2.0's SKILL.md whole; AGENTS.md lines 57-59. Nothing outside these.

## Q1. What the result can say, and about which version

**1. Adjudicate the one divergence.** Grounded: ARM P was the version-1 pipeline "exactly as shipped" (prereg line 29), so the S2 cut is a version-1 cut; the result says nothing about 2.0 unless 2.0 would make the same cut, which is candidate 2's question. Grounded: the S2 crowning appeared in 1 of 7 ARM C reps, the candidate was excluded in both ARM P reps (Results line 298-299), and it was counted under the primary gate, which by the sealed tiering rule admits only clear-call crownings (inference from prereg line 38 and the Results table). Three outcomes. (a) Both judges find the re-shaped cut stronger than ARM P's winner: one adjudication-surviving divergence at 1-of-7 reproduction. Under T2's own sealed rules that is at most an existence finding, which required a human cold judge to concur (prereg line 45); this candidate substitutes two agent judges, so the finding is weaker than T2's definition. The gates seat's objection also stands unanswered: a head-to-head measures strength in isolation, which is a different question from what full shaping crowns (panel line 84). (b) The cut loses or ties: T2's only catch was noise, and T2's 49 closes then hold zero surviving divergences; with the positive control still undetermined, "safe" and "instrument blind" stay indistinguishable (prereg line 83). (c) The judges split 1-1: non-convergent, no result. In every branch the claim is n = 1 and about version 1.

**2. Same fields, 2.0 Prune.** Grounded: says nothing about safety, as the candidate states. It yields, per case, the overlap between 2.0's exclusion set and the stored version-1 sets (10-15 candidates excluded in both reps per case; version-1 self-agreement 0.52-1.00 intersection over union; Results line 311). Reading that overlap needs a within-2.0 baseline: two 2.0 reps per case give 2.0's own self-agreement, a number 2.0 has never had; without it, a cross-version overlap of 0.6 cannot be told apart from ordinary run-to-run variation. If the cross-version overlap sits inside the within-version range, T2's descriptive facts (48 of 49 closes non-divergent; the S2 cut's own record carrying a revive-if and a strongest case; Contest not naming it) describe 2.0's cuts too, still unadjudicated. If the overlap is low, T2's artifacts do not describe 2.0, and candidate 1 (and candidate 6 if it reuses T2 fields) become statements about version 1 only. Assumption: the 2.0 Prune text is a trimmed carry-forward of version 1's (assessment lines 89 and 99), so similarity is plausible but unmeasured. Version 1's default survivor count is not in the evidence read (gap G4).

**3. User's candidate.** Grounded: licenses no rate and no safety claim; the question stays open by design. It yields this: on any real 2.0 run JP reads the cut ledger (option, cut, revive-if), the Contest line, and the re-run offer; if he asks for a revival, he learns for that one decision whether the revived option changes the close. T2 evidence for the detectors, n = 1 each: the one divergent candidate's own Prune record anticipated the challenge (a survivor-budget cut marked `contestable sketch-depth judgment`, with revive-if and strongest-case present; Results line 315), and Contest did not name it (line 316). So the ledger has one supporting instance and Contest has one miss. This is about 2.0 directly. It cannot yield a count: no run records whether a cut was a winner unless JP funds the revival and judges the result himself.

**4. Develop one cut per run.** Grounded: about 2.0 directly. It yields one observation per real run, "the developed survivor-count cut with the strongest recorded case beats the close: yes or no", accruing into a count over runs. It cannot yield a base rate of missed winners (only one cut per run is developed, so a missed winner among the other cuts is invisible) or a sensitivity figure (no case has a known answer). T2 support, n = 1: the S2 divergent candidate was a survivor-budget cut carrying a strongest case, the kind this rule selects; whether it was the strongest-argued among S2's 10-15 cuts is not recorded in the Results (gap G6). Whether the yes/no is trustworthy depends on Q2 and Q4.

**5. Known-answer cases, Prune only.** Grounded: about 2.0 directly. It yields "on n authored cases whose winner is fixed by in-case evidence and hidden at sketch depth, 2.0's Prune cut the winner in x", and the count can be split by cut type (constraint, same reason, dominated, survivor count; SKILL.md lines 49-55), since the failure mode T2 named is the survivor-count cut. This is a cut rate on fields built to hide the winner: a stress measurement, not a base rate on real fields (T2 could not give a base rate either, at about 2%). No instrument-blindness question arises, because the only instrument is Prune and the event (cut or kept) is read off `02-prune.md`. It cannot say whether the author's winner really is best (Q2), and says nothing about Shape, Recommend, or Contest.

**6. Seeded-dominator run.** Grounded (Results lines 375-382): it yields two rates. First, P(Prune cuts the seed), from the ARM P arm, which is the same count candidate 5 produces. Second, P(control arm plus judges crown the seed, given Prune cut it), the instrument's sensitivity. If sensitivity is shown high and the instrument is T2's instrument (version-1 ARM C, same model family), T2's 48-of-49 non-divergence becomes evidence bounding spontaneous damage near the observed 2% rate, which is the meaning the candidate names. If the instrument is rebuilt for 2.0 (2.0 has no full-field shaping mode; the T2 apparatus was moved to the archive, assessment line 99), the sensitivity claim is about the new instrument while T2's 48-of-49 was measured by the old one, so the transfer rests on an equivalence assumption. If sensitivity is low, T2 was instrument-blind and its null means nothing. Which pipeline plays ARM P (version 1 from the archive, or 2.0) is unspecified in the candidate; that choice decides whether the result is about 2.0. No human cold judge is included; T2's existence channel required one (prereg line 45), so this design's findings are agent-judged only.

## Q2. Where the ground truth comes from, and what could make it wrong

**1.** Two agent judges over the two candidates re-shaped under one neutral single-pass condition, in a packet regenerated by a fresh arm-blind rewriter and probed for leaks (prereg lines 43 and 58). What could make it wrong: the re-shape procedure is called a "sealed procedure" at line 43 but its text is not in the sections read and it never ran (gap G2); two judges where T2 sized five with a cross-family-inclusive majority, so a 1-1 split is non-convergent and two same-family judges carry the same-family bound (prereg line 27); if ARM P's S2 winner-set was plural, T2's rule requires the cut to beat every branch head, and whether it was plural is in the run workspace (gap G1); and the gates seat's point that isolation strength differs from what shaping crowns.

**2.** No ground truth is claimed; the measurement is set overlap resolved to crosswalk IDs. In T2 that resolution was fully mechanical with zero failures (Results line 368) because version-1 Prune quoted exact wordings. 2.0 also requires exact wordings (SKILL.md line 31), so resolution should stay mechanical; a 2.0 Prune agent that paraphrases breaks the match, and that case is then unresolvable rather than guessable.

**3.** JP's own reading, at sketch depth, with his lean known to him. This is not an evaluation: no independent judgment is recorded, and the depth is the same depth Prune judged at unless JP funds a re-run.

**4.** One fresh agent's judgment, made after shaping the cut. As written ("reports whether it beats the close") the agent reads the close, so it knows which option the pipeline crowned. That is the identity asymmetry T2's panel regenerated packets to remove (panel item 4), and the depth form of the same problem is what 2.0's Contest text warns about ("depth asymmetry is not evidence", SKILL.md line 73). The shaping removes depth asymmetry; identity asymmetry remains unless the candidate is reworked (Q4). If the same agent reads the close before shaping, the shaping itself may be steered by the close.

**5.** The author's assertion, written into the case. What could make it wrong: the winner is visible at sketch depth, so Prune keeps it and nothing was tested; the winner is not actually best, so a cut is scored as a miss wrongly; the author, knowing the hypothesis, builds fields that force a survivor-count cut, which is intended but makes x a rate on adversarial fields. No judge checks the author. A cheap validity check per case: a fresh agent asked to name the best option from the field wordings alone; if it names the winner, the case fails the "hidden at sketch depth" property. T2 evidence that such a case can be built blind: the positive-control builder produced one (Results line 324); its dominance was never validated.

**6.** Two layers: the seed's dominance by construction (the author), then the instrument's catch (control-arm crowning surviving adjudication by confined agent judges). The adjudication doubles as a check on the author: if the judges crown the seed head-to-head but the control arm did not, the control arm was blind (T2's named attention-dilution failure, prereg line 32); if the judges do not crown it, the seed was not dominant. What could make it wrong: the same judge-count and same-family issues as candidate 1, and the unrun re-shape procedure (G2).

## Q3. Cost, when it is paid, and when the observation arrives

Price basis, grounded. T2 spent about 14.9 operator-hours on 322 dispatches, about 2.8 minutes per dispatch averaged over the whole run including recovery (Results line 292; Amendment 1 clause 4). The mini-pilot priced about 24 dispatches and 35-40 attended minutes per case run in parallel pairs, about 1.5-1.7 minutes per dispatch (prereg line 91). Observed dispatches ran about 1.5 times the priced count (322 committed against about 216 priced for nine cases, of which eight ran; Amendment 2 clause 5). Band used below: 1.5-2.8 operator-minutes per dispatch, with a 1.5x overhead allowance for kills and redos. The band was measured on T2's heavier harness (validator, envelopes); 2.0 dispatches are lighter, which may lower it, but that is not assumed. Setup work (locating artifacts, restoring scripts, writing briefs) is outside the band and is where each estimate is least certain.

**1.** About 7-8 dispatches: two re-shapes, two packet rewrites, one leak probe (plus a rebuild if the probe recovers field width), two judges. Band with overhead: 15-35 minutes of dispatch attention. Setup, unpriced and probably larger than the dispatches: locate S2's stores and ARM P's winner, restore the re-shape brief, the role profiles and the sandbox wrapper, and write an allowlist-only script to read the S2 stores (the rule T2 adopted after six disclosures, Results line 359). Paid once; the observation arrives in one session.

**2.** 7 dispatches for one 2.0 rep, 14 for two (the within-2.0 baseline needs two), plus mechanical crosswalk resolution by the existing script. Band with overhead: 15-60 minutes, plus rendering seven T2 case setups into 2.0's Prune brief form (field with seeds marked; question; constraints at their price; values; survivor count). Paid once; the observation arrives in one session.

**3.** No apparatus. One status edit closing T2 in the prereg. Per real run, JP's reading time on the ledger and the Contest line. Observations arrive only when JP funds a revival; there is no bound on when.

**4.** Per real run: 1-2 dispatches as written (shape the cut; compare), or 4-5 if blinded per Q4 (add two rewrites and a probe). Operator time near zero per run if the step is written into 2.0's close. Setup: a skill edit (build-and-prune under JP's global rules) or a hook (a charter-gated event under those rules). Observations accrue at the real-run rate; none until runs happen.

**5.** Per case: one author dispatch (or JP writing it), one or two 2.0 Prune dispatches, one optional sketch-depth validity check. Matching is mechanical because the winner's wording is authored. For n = 10: about 30-40 dispatches, band with overhead roughly 1-3 hours, plus reading each case once. Paid once.

**6.** Per seeded case: T2's priced 24 dispatches at k = 7 becomes about 20 at k = 3-4, plus adjudication (two re-shapes, two rewrites, one probe, judges; the candidate does not fix the judge count and T2 sized five), about 26-29 priced. Band with overhead: about 1-2 hours per case. One case: 1-2 hours. A dozen: about 8-24 hours. Setup, unpriced: an ARM C for the pipeline under test (rebuild for 2.0, or restore version 1 from the archive), the confinement tooling, a ledger that records the seed's crosswalk ID at stem-freeze, and allowlist scripts before dispatch 1. Paid once per case; results arrive in one bounded campaign.

## Q4. What the blind-evaluation rule requires, and what that adds

The rule (AGENTS.md lines 57-59): never reveal apparatus state (reviewer or model outputs, intermediate scores, predictions, arm identities) in any channel a current or potential ground-truth judge can see, until their independent judgment is recorded; lost blinding is unrecoverable; re-administer to a fresh judge.

**1.** The two agent judges are ground-truth judges. Required: confined dispatch (T2's headless `claude -p --safe-mode` deny profiles, or the codex `sandbox-exec` wrapper; prereg line 57), regenerated packets with an executed leak probe, pinned prompts, A/B position randomization. JP is not a judge here, so the S2 blindness-compromise note (Results line 357: something about S2 reached JP-visible channels) does not touch this design; it only forecloses JP as a cold judge on S2, which this candidate does not ask for. Adds: the packet apparatus, and the operator must not become the matcher, so a script assembles the packet (Amendment 6 clause 4 is the pattern).

**2.** No judge; the rule requires nothing. Side effect to record: reading seven cases' fields and exclusion sets into JP-visible channels forecloses JP as a cold judge on any T2 case later (four of eight were already foreclosed, Results line 357).

**3.** No evaluation; the rule requires nothing; nothing is measured.

**4.** A fork the candidate does not settle. Read as an evaluation: the fresh agent is a ground-truth judge, and the close (a model output naming the pipeline's winner) is apparatus state it must not see; the comparison must then run over regenerated packets plus a probe, about three extra dispatches per run, all inside the skill and each able to fail. Read as a detector reporting a flag to JP: no blinding is required, and the yes/no is a flag rather than a recorded independent judgment. The candidate's text ("reports whether it beats the close") describes the second form.

**5.** No judge; the rule requires nothing. A separate validity choice: whether to confine the Prune agent so it cannot read repo documents naming the hypothesis. 2.0 dispatches Prune as an in-session fresh agent, and T2 recorded that the in-session Agent tool is not confinement-capable (prereg line 57). Confining Prune means dispatching it headless, a step away from 2.0's own dispatch shape. Not required by the rule; it changes what the count measures if the agent could learn it is being tested.

**6.** The full apparatus of candidate 1, per seeded case, plus: the seed's identity kept from packet composers and from both arms (the arms see it only as a field candidate), and allowlist-only inspection scripts before dispatch 1 (the candidate includes this; Results line 359 attributes five of six disclosures to improvised inspection). JP is not a judge, so JP-side sequestration is not required by the rule. This is the most per-case overhead of the six; T2's Results say this layer is where its hours went.

## Q5. What must exist, or happen, for any observation

**1.** Intact at `~/.t2-run/` (mode 700, durable since Amendment 1 clause 6): S2's frozen field, crosswalk, ARM P close and prune records, the divergent ARM C close and its agreed winner-set. Also: the neutral re-shape brief, the packet template, the rewriter and probe prompts, the role profiles and sandbox wrapper. Every item is a gap (G1, G2, G3).

**2.** Intact at `~/.t2-run/`: all seven fields, crosswalks, both ARM P exclusion sets per case, case setups; the exclusion-wording resolver script. Also version 1's default survivor count, to set 2.0's count equal (G4). Gaps G1, G4.

**3.** Real runs of 2.0 on JP's decisions, and JP reading their ledgers. Evidence: zero organic runs of version 1 in seven weeks and one misfire (assessment line 51); 2.0 is built to change that (model-invocable, 10-20 minutes) and this is untested. Inferred from this run's directory name (`scratchpad/smoke`): this run may be 2.0's first real-decision run. Marked inferred.

**4.** Everything in 3, plus a skill edit or hook, plus a selection rule for "the survivor-count cut with the strongest recorded case": either a judgment (someone reads all records and picks) or a mechanical stand-in (for example, first survivor-count cut in field order), which weakens the bet.

**5.** Cases with the property. One existence proof of blind construction (T2's builder), zero of validated dominance. An author (agent or JP). No T2 artifact is needed.

**6.** Everything in 5, plus an ARM C for the pipeline under test, the confinement tooling (G3), the extraction codebook (Appendix A, inside the prereg, intact), a stem-freeze ledger for the seed's ID, and a working judge dispatch route (cross-family demonstrated 2026-07-22 under the wrapper; whether it still works is untested, G3).

## Each candidate's bet, in one paragraph

**1.** Bet: the one spontaneous catch is real, and a rare crowning that survives clean adjudication counts as a revealed winner (the control seat's reading, panel addendum lines 76-84). Mechanism: one hardened-adjudication packet on existing data. Depends on: T2 artifacts, an unrun re-shape procedure, the confinement tooling, and the assumption that a version-1 cut says something about 2.0. Gaps: G1, G2, G3.

**2.** Bet: whether T2 describes 2.0 must be answered before any T2 artifact is reused, and it can be answered mechanically. Mechanism: set overlap on frozen inputs. Depends on: artifacts, exact-wording discipline, a within-2.0 baseline. Gaps: G1, G4.

**3.** Bet: 2.0's own disclosures (ledger, Contest line, re-run offer) plus JP's reading are enough detection for a rare event, and a rate is not worth apparatus. Mechanism: none beyond the skill. Depends on: real runs, and JP acting on records. Gap: G5.

**4.** Bet: a missed winner would be the cut whose own record argued hardest for it, and developing exactly that cut each run catches it without JP's attention. Mechanism: one shaped comparison per run. Depends on: real runs, a selection rule, and the blinding fork in Q4. Gaps: G5, G6.

**5.** Bet: a case can be written whose winner is fixed by evidence but hidden at sketch depth, and the author's word is enough ground truth. Mechanism: Prune alone on authored fields, cut or kept read off the file. Depends on: authoring, the validity check. Gap: G7.

**6.** Bet: sensitivity is the missing number, and measuring it gives T2's null a meaning. Mechanism: seeded cases through both arms plus adjudication, with the bookkeeping fix that lost T2. Depends on: an ARM C for the pipeline under test, the confinement tooling, case construction, adjudication. Gaps: G2, G3, G7, and the unspecified ARM P identity (which pipeline).

## Collisions and constraint consequences, recorded and not acted on

- Candidates 3 and 4 share one viability dependency: real 2.0 runs. If no runs happen, both yield nothing. Their bets differ (JP's reading versus a developed cut per run), so identity holds. Not merged.
- Candidates 5 and 6 share case construction, and 6's ARM P arm yields 5's count as a byproduct. Their bets differ (author fiat versus instrument-confirmed catch). Not merged.
- Candidates 1 and 2 share the `~/.t2-run/` dependency and are both about version 1; 2's result conditions what 1's result means for 2.0. Different bets. Not merged.
- Constraint 1 (well under 15 operator hours): candidate 6's own size range runs from about 1-2 hours to 8-24 hours by the band; its upper end reaches and passes T2's ceiling. Recorded; candidate preserved. Candidate 1's setup is unpriced and could exceed its dispatch estimate. Recorded.
- Constraint 2 (blind-evaluation rule): candidate 4 as written is not a blind evaluation; both readings are recorded in Q4. Candidates 1 and 6 carry the rule's full overhead. Candidates 2, 3, and 5 have no judge.
- Constraint 3 (no web research): no candidate needs it.
- No collision blocks option identity, so no terminal was returned.

## Evidence gaps and the smallest check for each

- G1. Whether `~/.t2-run/` still holds the seven fields, crosswalks, exclusion sets, closes, and S2's agreed winner-set, and whether S2's ARM P winner-set was plural. Check: an agent lists the workspace and verifies store hashes against `~/.t2-run/logs/run-facts.md`. Matters for 1, 2, and 6 if it reuses fields.
- G2. Whether the neutral single-pass re-shape procedure (prereg line 43, "sealed procedure") exists as written text. Check: search the seal commit's tree for the re-shape brief. Matters for 1 and 6.
- G3. Whether the role profiles, sandbox wrapper, packet template, rewriter and probe prompts, and allowlist scripts survive and still run. Check: search the seal commit and `~/.t2-run/` for them, then re-run the 2026-07-22 wrapper probe. Matters for 1 and 6.
- G4. Version 1's default survivor count. Check: read version 1's SKILL.md or contract-data at the seal commit. Matters for 2 (set 2.0's count equal) and for whether S2's cut would recur.
- G5. The rate of real 2.0 runs. Check: none available now; only time. Matters for 3 and 4.
- G6. Whether the S2 divergent candidate was the strongest-argued cut among S2's cuts. Check: read S2's prune records in `~/.t2-run/`. Matters for candidate 4's n = 1 support.
- G7. Whether cases with a hidden, evidence-fixed winner can be written. Check: write one and run the sketch-depth validity read from Q2. Matters for 5 and 6.
- Also unresolved: whether the "unblind" step was formally performed after the human arm closed. The Results verify the sealed map's hash (line 361) but do not say unblind was declared, so JP's custody rule over `~/.t2-run/` (Amendment 1 clause 6) may or may not still bind him. Matters for who may run G1's listing; an agent can run it either way.

## Bias pass

- Candidate 5 read as the cleanest on first pass. I added its ground-truth weakness (author fiat, adversarial-field rate, no check on the author) and the confinement choice, to the same depth as the judged designs.
- Candidate 6 has the most words because it has the most parts, not because it is favored; its cost uses the same band and the same component counting as candidate 1.
- Candidate 3 (the user's) got the same n = 1 evidence for its detectors as candidate 4 and the same run-rate dependency. I did not soften its "no count" limit, and I did not inflate the ledger's one hit.
- Candidate 1's attraction (cheap, uses an existing catch) is balanced by stating the 1-of-7 reproduction, the version-1 scope, the two-judge convergence issue, and the unpriced setup.
- Candidate 2's bookkeeping appearance is balanced by naming the new number it yields (2.0's own prune reproducibility).
- Candidate 4's blinding fork is stated both ways without choosing.

These are the asymmetries I found and corrected. The result is not certified neutral.

## Close

What can now be compared, for each candidate: what its result would say and about which version of Prune; where its ground truth comes from and what could break it; its priced dispatch cost, its unpriced setup, and when its observation arrives; what the blind-evaluation rule adds; and what must exist or happen for it to run at all. Assumptions still open: that the per-dispatch band from T2's harness applies to 2.0's lighter dispatches; that 2.0's Prune resembles version 1's; that real 2.0 runs will occur. Gaps G1 through G7 remain, each with its smallest check named. No ranking, lean, filter, or recommendation was performed. The field order is the upstream workflow's, not the user's.
