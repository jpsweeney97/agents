# T2 known-answer check and run (2026-09-03)

The `check first` call from the deliberate 2.0 run on the T2 question (`docs/plans/2026-09-03-deliberate-t2-successor-run/04-close.md`), executed by a session on 2026-09-03 on JP's instruction, then the run it licensed: ten authored decision cases, each with a winner fixed by evidence that 2.0's Prune never sees, each put once through 2.0's Prune. This directory holds every case, its evidence, the sealed answer written before any dispatch, both validation reads, every rewrite attempt, the ten Prune ledgers, and the run ledger.

**Outcome in two lines.** The check passed on its first case in about twelve minutes, so "Known-answer cases, Prune only" was buildable. Across ten cases, 2.0's Prune kept the hidden winner seven times and cut it three times; all three cut records carried a `Revive if` condition naming the exact fact that would have saved the option.

## What T2 asked, and what this answers

T2 asked whether deliberate's Prune stage, which cuts options at sketch depth before any option is developed, systematically excludes options that full development would have shown to be winners. It closed INCONCLUSIVE on 2026-07-25. This run answers the question in its conditional form for version 2.0: given a field that contains a candidate whose winning case lives only in evidence Prune does not receive, how often does Prune cut it? The answer here is three times in ten, on authored fields, with every cut disclosed as such and every cut record naming the reviving fact. It is a count about 2.0's Prune, bounded as stated under Honest limits; it is not a rate on real decisions and says nothing about Shape, Recommend, or Contest.

## Design

**Kind B throughout.** The facts that fix each winner sit only in `evidence.md`, which Prune never receives. Prune's view is `case.md`: the question, background, one user candidate marked as theirs, three confirmed constraints with what each costs, three values, survivor count "about four", and a field of fifteen or sixteen candidates in `ideate` shape. This is the T2 question in conditional form and matches 2.0's stage table, which gives Generate, Shape, and Recommend the evidence and Prune none. Kind A (fixing facts in the constraints or values Prune sees) was not built: it measures whether Prune reads carefully, a different question, and its Reader A test is incoherent.

**Validation, per case.** A sealed answer was written before any dispatch, naming the winner, the fixing facts, and why every other candidate loses. Two fresh agents then read the case with no knowledge of its purpose. Reader A received Prune's view and had to *not* name the winner as best (otherwise the winner is visible at sketch depth). Reader B received Shape's view (case plus evidence) and had to name it (otherwise the evidence does not fix it). A case that failed was rewritten, up to three attempts. Reader A's runners-up were recorded as a visibility grade.

**Prune dispatch.** One fresh in-session agent per case, told it is the Prune stage of a `deliberate` run, carrying the Prune method text verbatim from `plugins/decide/skills/deliberate/SKILL.md`, reading only `case.md`, writing `02-prune.md`. Not told the case was authored or that a winner existed.

**Disguise variety.** Each case was built so the winner looks cuttable for a different reason at sketch depth: the modest member of a cluster (01), the narrowest-looking fix (02), a dependency bump that depends on a vendor (03), an unrelated-looking building chore (04), a calendar rule beside process changes (05), an apparent violation of a visible constraint (06), the user's own candidate looking labour-heavy (07), the same-reason twin of a constraint-killed option (08), an apparent purchase under a no-spend constraint (09), and an apparent weakening of oversight (10). Domains: a nightly export job, CI flakiness, a mobile crash spike, a print shop, hiring, support volume, a clinic, an online checkout, a food pantry, a permits office. All organisations are fictional.

## Results

| Case | Domain | Winner (sealed) | Attempt | Reader A: winner's rank | Prune | Cut type | Revive-if names the fact |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | nightly export | Tune the catalog fetch's request parameters | 1 | not listed | **cut** (5 survive) | survivor count, judgment | yes |
| 02 | CI flakiness | Isolate the integration shards' databases | 1 | 1st runner-up | kept (4) | | |
| 03 | mobile crash spike | Update the app's third-party libraries | 2 | 2nd runner-up | kept (4) | | |
| 04 | print-shop press | Service the shop's compressed-air system | 2 | not listed | **cut** (5) | survivor count, judgment | yes |
| 05 | hiring speed | Put the hiring decision meeting on a standing daily slot | 2 | 1st runner-up | kept (4) | | |
| 06 | support volume | Restore the previous export date format | 1 | seen, deterred by constraint; named in unknowns | **cut** (4) | constraint, fact-established | yes |
| 07 | clinic no-shows | Call patients the day before (user's candidate) | 1 | not listed | kept (4) | | |
| 08 | checkout abandonment | Switch the payment step to the provider's hosted checkout page | 1 | 1st runner-up | kept (5) | | |
| 09 | volunteer scheduling | Use the scheduling module of the pantry's donor-management system | 1 | 2nd runner-up | kept (5) | | |
| 10 | permit backlog | Change which applications get the supervisor sign-off | 3 | 2nd runner-up | kept (4) | | |

Reader B named the winner on every valid attempt, citing the fixing facts by number each time.

**The three cuts.**

- Case 01: cut to reach the survivor count; "the case gives no view of the current settings." Revive if "Develop finds the current request settings far below the API's documented limits": E4 against E2 exactly.
- Case 04: cut to reach the survivor count; "whether the stops are air-related ... the file does not say." Revive if "the stop log shows feeder, suction, or sheet-transport faults, or the air-supply contractor's inspection finds moisture": E1 and E2.
- Case 06: a constraint cut, marked fact-established on the constraint's wording ("this option changes the date column ... that is a format change to exports"), with Prune adding that whether reverting is treated differently under the terms "is a legal reading I cannot make here." Its `Strongest case` argued the option "may be the cause, not a treatment," and its first revive condition, "the May change was itself made without the ninety days' notice, and the user or their counsel reads reverting as honoring the promised format," is E3 almost verbatim. On the evidence the cut is wrong; on Prune's view it is the reading the constraint's cost line invites.

## Observations, recorded as observations

- **Prune's keep tracks a careful reader's sketch-depth ranking.** Every winner that Reader A listed as a runner-up was kept (02, 03, 05, 08, 09, 10); the two winners Reader A did not list at all were cut (01, 04); the one Reader A saw and rejected on the constraint was cut on the same constraint (06). The exception is 07, the user's candidate, which Reader A did not list and Prune kept. Reader A and Prune are both single sketch-depth reads by the same model family, so this is partly one judgment measured twice; it means the validation test also predicts the outcome, which is a limit on what the count can show.
- **The cut types.** No winner died by same-reason or dominance. The same-reason trap in case 08 did not fire because constraint 1 removed the twin first, leaving the winner standing alone. The two survivor-count cuts were disclosed as low-confidence exactly as the contract requires; the constraint cut was disclosed as fact-established when it was in fact a reading.
- **Survivor discipline.** Prune stopped at five in four cases rather than force a fourth cut, each time naming what blocked it (an unpriced value trade in 04 and 09; a fact it could not see in 01 and 08). It carried explicit checks forward in 06, 09, and 10 (whether the module is on the plan; whether the sign-off is required by ordinance; whether the surge has one cause), and in 06 and 10 those checks are the fixing facts.
- **The user's candidate.** In 07 it was the winner and survived; in the other nine it was a loser and survived in eight of them (01, 02, 03, 05, 06, 08, 09, 10), cut only in 04 (backup press, constraint 1). The contract's protection of the user's wording is visible in the ledgers.
- **Where cases leaked.** Five rewrites were needed, and each leak is a reusable authoring lesson: a cluster of similar options plus a constraint naming the same thing (03); an option wording that names a current fault (04); a background sentence that locates the loss (05); a timing coincidence between the question and an option (10, attempt 1); and elimination, where visible constraints leave one constraint-clean throughput option (10, attempt 2). All attempt files are kept.

## Honest limits

- Ten cases, one Prune dispatch each: no run-to-run variance measured. Ten reads a rate coarsely: "mostly kept" is supportable; a percentage is not.
- One author (this session), one model family for author, readers, and Prune. The cases share one shape: a hidden single cause with a cheap fix. Decisions of other shapes (genuine value trades, no hidden cause) were not built.
- Ground truth is the author's assertion, checked by one read each way. Cases were rewritten until Reader A did not name the winner; that selection pushes winners toward invisibility, and the observation above says invisibility to Reader A predicts a cut. The rewritten cases split three kept, one cut.
- In-session agents were unconfined; each was told to read only the named files and none of the outputs cites anything outside them.
- The Prune agents knew they were inside a `deliberate` run, as a real dispatch would; they were not told the field was authored.
- Sealed answers are in this directory only because every case's Prune has run. For any further case, keep its sealed answer outside the tree until its Prune dispatch is complete.

## The Contest test on case-06

Run on 2026-09-03, 16:28 to 16:40, on JP's instruction from the 16:08 handoff: case 06's four Prune survivors were carried through Shape, Recommend, and Contest, each a fresh agent dispatched with `model: opus`, the decide 2.1.0 default and its first live use. The question was whether the later stages catch Prune's wrong constraint cut of the winner, whose first `Revive if` condition is E3 nearly verbatim.

**What each stage received.** Shape: the setup (`00-setup.md`: question, background, the user's candidate marked as theirs, constraints at their price, values, survivor count, the model, no lean), the four survivors in field order with exact wordings, `evidence.md`, the delegation statement, and Prune's "Carried to Develop" paragraph, passed because it is addressed to the next stage and is not a cut record. Recommend: the setup, `03-shaped.md`, `evidence.md`, the statement that the user stated no lean and that the chatbot is the user's own wording, and the append-a-cut-record instruction. Contest: the method text, the setup, `02-prune.md`, `03-shaped.md`, `04-close.md`. The briefs are in `case-06/briefs.md` verbatim. Each agent worked from a session scratchpad directory holding only the files it was allowed to read: `case.md` (the full field) and `02-prune.md` were held outside it until Contest, and the sealed answer and this README were never in it. No output cites a file outside its brief.

**Shape** (`03-shaped.md`, 121 lines) completed the surface with no honest exit. From E1, E2, and E6 it established that the surge has one documented cause and that customer growth runs the wrong way to explain it. It recorded that constraint 2 binds none of the four survivors, and that E3 "removes a constraint someone might otherwise assume applies", without naming any option outside the field. Its field-level note to the later stages says that no option in the field acts on the cause of 482 of the 830 tickets and that "adding a candidate is not this stage's authority". It recorded the chatbot's constraint consequence without filtering and the chatbot/documentation collision without merging.

**Recommend** (`04-close.md`, 144 lines) rendered `clear call` for an option it added: "correct the export date format (bug tracker issue #2291)". It added it under `making-recommendations`' own field rule (add an alternative only when it could realistically win), said so openly, and passed it through all three constraints, clearing constraint 2 on E3. It cut the chatbot (constraint, judgment call) and the banner (dominated by the added fix, fact-established), each with a record in Prune's shape; it left documentation and macros uncut and unrecommended. The call goes against the user's candidate and says so. Under What Would Flip It it wrote that an earlier stage may have "considered the export fix and rejected it for a reason not visible on the shaped surface" and that Contest "can see the cuts this stage cannot, and this is the first thing it should check." Neither outcome the handoff predicted (`no basis yet`, or `check first` with all four survivors killed by the evidence) occurred; the close re-derived the cut winner from the evidence.

**Contest** (`05-contest.md`) wrote one line naming "Require a documentation search before a ticket can be submitted" as the only live challenge and the one most worth contesting. That cut's `Revive if` ("the chatbot is cut on constraint 1 ... and the user still wants documentation surfaced before filing") is satisfied by the close's chatbot cut, so the flag is correct by the method. It did not name "Restore the previous export date format", whose `Revive if` (1) the close's E3 reasoning satisfies in full and whose substance the close adopted. Asked afterward, in a prompted question sent after its line was recorded, the agent said the omission was deliberate: an exclusion check names what is still excluded from the close, and the close had adopted the option's substance as its recommendation, so naming it "would have told a reader that an option was wrongly kept out, when it is the option that won". It added that a strict literal reading of the three grounds would have listed the cut, and that "the one-line output form has no slot for a confirmation". The full reply is `case-06/05-contest-posthoc.md`, labeled post hoc.

**Reading.** The run's final recommendation is the sealed winner, reached with the fixing facts (E1, E2, E3, E4) and against the user's candidate. The route was not revival of the cut: Recommend never saw the cut record, and the option came back through `making-recommendations`' add-an-alternative rule on a full-evidence read, the same read that found the winner in every Reader B validation. The instrument built to catch this cut, Contest, did not name it. For the T2 question that means: on this case the pipeline recovered from Prune's wrong cut, and the recovery came from Recommend's contract, not from the cut ledger or the exclusion check. Shape's field-level note and Recommend's What-Would-Flip-It line are the two places the miss was visible to a reader before Contest ran.

**Limits of this test.** One case, one dispatch per stage; no variance measured. The winner here is obvious to any full-evidence reader (Reader B named it on the first attempt), so Recommend's add rule had an easy target; a cut winner that full evidence supports less plainly was not tested. The Recommend brief did not forbid adding options, matching a real run; a brief that froze the field would have produced a different close. Contest's one-line output form records no reasoning, so why it omitted the cut is known only from a post-hoc reply to a prompted question, which is weaker evidence than the line itself.

## What this run did not do

It did not run Shape, Recommend, or Contest on any case, so it does not show whether the later stages catch a cut winner whose revive condition names the fact; case 06 is the sharpest candidate for that test. That test ran later the same day; see "The Contest test on case-06" above. It did not re-dispatch Prune on any case. It did not edit the T2 pre-registration.

## Files

| Path | What it is |
| --- | --- |
| `run-ledger.md` | one row per case attempt, plus the tally |
| `case-NN/case.md` | Prune's view (the valid attempt) |
| `case-NN/evidence.md` | Shape's addition (the valid attempt) |
| `case-NN/read-A.md`, `read-B.md` | the two validation reads for the valid attempt |
| `case-NN/02-prune.md` | deliberate 2.0's Prune output |
| `case-06/00-setup.md`, `03-shaped.md`, `04-close.md`, `05-contest.md` | the Contest test: the setup written for the resumed run, Shape's surface, Recommend's close with its cut records, Contest's line |
| `case-06/05-contest-posthoc.md` | the Contest agent's prompted post-hoc reply, labeled as such |
| `case-06/briefs.md` | the three stage briefs of the Contest test, verbatim |
| `case-NN/attempt-N/` | failed attempts' case, evidence, and reads (03, 04, 05, 10) |
| `sealed/case-NN-ANSWER.md` | the sealed answer for the valid attempt; `.attempt-N.md` for failed ones |
| `case-01/` | the original check case, as before |

Timing: the check ran 15:09 to 15:21; the nine further cases ran 15:36 to 16:02, about 26 minutes wall clock for 30 reader dispatches and 9 Prune dispatches plus authoring.
