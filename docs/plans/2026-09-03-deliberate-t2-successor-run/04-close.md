# T2: Recommend stage close

Stage: Recommend (`making-recommendations`), 2026-09-03, inside a `deliberate` 2.0 run. Input: `03-shaped.md` (six candidates at comparable resolution). Evidence read to verify cells: the prereg's frontmatter, Question, Arms, Winner-set extraction, Divergence/adjudication, Replication, Leakage, Case set, Pass/fail, Cost, and Results; the design panel report; the shape assessment; deliberate 2.0's SKILL.md; AGENTS.md lines 57-59. Nothing else.

**Outcome in two sentences.** The call is `check first`: spend about 30 to 60 minutes finding out whether one "known-answer" decision case can be written, and let that result choose between "Known-answer cases, Prune only" (candidate 5) and the user's own candidate 3. The user's lean rests on a premise ("unanswerable at acceptable cost") that this check tests directly, and the user's stated value (knowing matters more than closing tidily) says the premise should be tested rather than assumed.

## Field readiness

All six candidates answer the same five questions (what the result says and about which version; where the ground truth comes from; cost and timing; blind-rule overhead; what must exist) to the same depth, each with a bet paragraph and named gaps. Candidate 3, the user's, is developed as fully as the rest. Readiness passes; no handoff to `option-shaping`.

## Leans registered before comparing

- **My first-read lean: candidate 5**, "Known-answer cases, Prune only". What drove it: it is the only candidate that yields a count about version 2.0's Prune within a few hours, needs no judge, no blinding, and no T2 artifact.
- **The user's visible lean: candidate 3**, "Close T2 as unanswerable at acceptable cost and rely on watching real runs of the rebuilt skill instead." Stated by JP as his lean.

The comparison below attacks both. Where it ends: the structured pass moved me off "take 5" to "check whether 5 can be built, then take 5 or 3." Two things moved me: gap G7 (nobody has yet written a case with the property candidate 5 needs) and a fact from 2.0's skill text noted under the table (Prune never sees the evidence files), which makes the case design a real fork rather than a detail.

## Structure: filters, dominance, trades

**Null option.** "Do nothing at all" (no status edit, no watching) is not added. It could not win under the user's stated value, and the only fact it reveals is small: the prereg's status line already records "RUN CLOSED ... INCONCLUSIVE", so candidate 3's status edit is one added line, near-free. That fact is carried into the cells.

**Filter, constraint 1 (well under 15 operator-hours).** One candidate is set aside: "Seeded-dominator run" (candidate 6). Its own wording spans one to about a dozen seeded cases. What sets it apart is a sensitivity rate, and a rate needs several cases; at the surface's band that is about 1 to 2 hours per case plus setup that T2 never priced (an ARM C for whichever pipeline is tested, since 2.0 has no full-field shaping mode; confinement tooling; a judge route; a stem-freeze ledger; allowlist scripts). The user confirmed this constraint at a price that names "any successor at T2's scale", and this candidate is, in its own words, the successor the Results section sketched. At one case it fits the hours but is a re-run of T2's positive control and no longer does what sets it apart. This is a judgment call, because the hours are a band estimate; the record is at the end of this file with its strongest case and a revive condition.

**Filter, constraint 2 (blind-evaluation rule).** No candidate fails it. Candidates 1 and 6 carry its full overhead; candidate 4 as written is not an evaluation; candidates 2, 3, and 5 have no judge.

**Filter, constraint 3 (no web research).** No candidate needs it.

**Dominance.** No survivor is at least as good as another on everything that matters and better on something. Candidate 2 comes closest to being dominated: alone it says nothing about safety, and its unique output (whether T2's artifacts describe 2.0) has a use only if candidate 1 or 6 runs. I did not cut it; it stays in the comparison as the necessary first step of the artifact-reuse path (2 then 1), and is compared on that footing.

**Trades.** Five survivors: 1 (with 2 as its preliminary), 2, 3, 4, 5. They are better at different things, so the rest of the method applies.

## Comparison in words

Criteria are the surface's five questions. Cells are comparative facts, not scores. Assumptions are marked.

| Candidate | What it says about 2.0's Prune safety | Ground truth and its weak point | Operator cost; when the observation arrives | Blind-rule cost | Must exist first |
| --- | --- | --- | --- | --- | --- |
| 1. "Adjudicate the one divergence" | One judged observation about a **version-1** cut (ARM P was the shipped version-1 pipeline, prereg line 29). At best an existence finding weaker than T2's own definition: T2 sealed five judges with a cross-family majority plus a human cold judge for the existence channel (prereg lines 43, 45); this uses two agent judges. If the cut loses, "safe" and "instrument-blind" still cannot be told apart. | Two agent judges over re-shaped packets. Wrong if the judges split 1-1 (no result), if the "sealed" re-shape text does not exist (G2), or because head-to-head strength is a different question from what shaping crowns (panel line 84, unanswered). | 15-35 minutes of dispatches plus unpriced setup that is probably larger (locate stores, restore brief, profiles, wrapper, allowlist script). One session. | Full packet apparatus: confined judges, regenerated packets, an executed leak probe, pinned prompts. | G1, G2, G3 all open. |
| 2. "Same fields, 2.0 Prune" | Nothing directly. Tells whether T2's stored cuts describe 2.0 at all, which decides whether candidate 1's result is about 2.0. Also yields 2.0's own run-to-run prune agreement, a number 2.0 has never had. | None claimed; mechanical set overlap on exact wordings (zero resolution failures in T2, Results line 368). Wrong only if a 2.0 Prune agent paraphrases, which makes the case unresolvable rather than misread. | 15-60 minutes of dispatches plus rendering seven T2 setups into 2.0's brief form. One session. | None. Side effect: reading seven fields into JP-visible channels forecloses JP as a cold judge on all seven T2 cases (four of eight already foreclosed). | G1, G4 open. |
| 3. User's: "Close T2 as unanswerable at acceptable cost and rely on watching real runs of the rebuilt skill instead." | Nothing, by design. Per real run JP can read the cut ledger and the Contest line; a count never accrues unless JP funds a revival and judges it himself. T2 support for the detectors, n = 1 each: the divergent candidate's own record anticipated the challenge (Results line 315); Contest did not name it (line 316). | JP's own reading at sketch depth with his lean known to him. Not a recorded independent judgment. | Near zero: one added status line (the prereg already records the close). Observations arrive only if real runs happen and JP revives a cut; no bound on when. | None. | Real 2.0 runs (G5). Track record: zero organic runs of version 1 in seven weeks and one misfire (assessment line 51); 2.0 is built to change that and is untested. |
| 4. "Develop one cut per run" | About 2.0 directly, on real fields: one yes/no per real run, accruing into a count. No base rate (only one cut per run is developed) and no sensitivity figure. | One fresh agent that has seen the close, so it knows which option won (identity asymmetry, the thing T2's panel regenerated packets to remove). If read as an evaluation it needs blinding; if read as a flag to JP it does not, and the candidate's wording is the flag form. | A skill edit once (build-and-prune under JP's global rules; a hook instead would be a charter-gated event). Per run 1-2 dispatches, or 4-5 if blinded. Observations only as runs happen. | None in the flag form; full packet apparatus per run in the evaluation form. The fork is unsettled. | Real 2.0 runs (G5); a selection rule for "strongest recorded case" (G6); the skill edit. |
| 5. "Known-answer cases, Prune only" | About 2.0 directly. A cut rate on about ten authored cases whose winner is fixed by facts but not visible in the wording, split by cut type (constraint, same reason, dominated, survivor count). A rate on built fields, not a base rate on real ones; says nothing about Shape, Recommend, or Contest. | The author's assertion, written into the case. Wrong two ways: the winner is visible at sketch depth (Prune keeps it, nothing tested), or the winner is so hidden that a cut is near-certain (nothing learned about Prune's reading). The surface's validity read catches only the first. See the note below the table. | About 1-3 hours of dispatches for n of about 10, plus reading each case once (assumption: an agent authors; JP reads). One or two sessions. | None required. Prune is not confined: 2.0 dispatches it as an in-session fresh agent, and the in-session Agent tool is not confinement-capable (prereg line 57). | G7 open: nobody has yet written a case with the property and shown it has it. No T2 artifact needed. |

**A fact the surface did not record, and it changes candidate 5's design.** In 2.0's stage table (SKILL.md lines 35-38), Generate, Shape, and Recommend each receive "evidence"; Prune receives "the field with the user's candidates marked; question, constraints at their price, values, survivor count" and no evidence. So there are two different cases candidate 5 could build, and they answer different sub-questions:

- Fixing facts placed where Prune can see them (in the constraints, values, or question) but not decisive from the candidate wording alone. The count then measures whether Prune reads carefully enough to keep a winner whose case is available to it.
- Fixing facts placed only in evidence Prune never sees. The count then measures how often Prune's sketch-level judgment keeps a winner it has no way to recognize. This is the T2 question in its conditional form ("given such a candidate exists, how often is it cut"), and a high rate is the expected outcome. It is still informative: a rate near the survivor-count cut rate for unresolvable candidates would mean 2.0's safety on such fields rests entirely on the cut record, the revive-if, Contest, and the re-run offer, not on Prune's judgment.

Both are worth having. They must not be mixed in one count, and the check below must fix which one is being built.

**Assumptions carried.** The per-dispatch band (1.5-2.8 minutes, times 1.5 for kills and redos) was measured on T2's heavier harness; 2.0's dispatches are lighter, so the band is probably an overestimate. An unconfined Prune agent could in principle read repo documents that name the hypothesis; the likely effect is more careful keeping, which biases toward the reassuring result, not away from it. Ten cases read a rate only coarsely: enough to tell "mostly cut" from "mostly kept", not enough to fix a percentage.

## Whose call it is

The outcome is stable across any reasonable weighing of the trades. The choice between 5 and 3 turns on a fact (can a calibrated case be written), not on an exchange rate between the user's goods. The choice between 5 and 4 turns on a dependency with no track record (real runs) and an unsettled validity fork; 5 runs now and is bounded. The choice between 5 and the artifact path (2 then 1) turns on three open gaps and on the result being about version 1. The one place a value enters: candidate 5 costs about 2 to 4 hours of operator time against candidate 3's near zero. I read the user's stated value (knowing whether Prune is safe matters more than closing tidily; no more week) as covering a few hours for a bounded count about 2.0. That is a reading of the user's words, marked as such; if it is wrong, see What Would Flip It.

## The Close

### Decision

What to do with T2 now that `deliberate` 2.0 keeps a shallow Prune stage: which of six candidates to act on, under the constraints of well under 15 operator-hours, the repo's blind-evaluation rule, and no web research.

### The Call

**`check first`.** Before choosing between candidate 5 and candidate 3, run one cheap check: try to write one known-answer decision case and confirm it has the property candidate 5 needs. About 30 to 60 minutes. The check's result chooses the candidate.

**The check.**

1. An agent (or JP) writes one decision case: a question, constraints at their price, values, a field of roughly the size a real Generate produces (about fifteen candidates), and, in a separate note, which candidate is the winner and which facts fix it. The author states where the fixing facts sit: in the constraints or values Prune sees, or only in evidence Prune does not see. Pick one kind and stay with it for the whole run.
2. Two fresh agents, each dispatched with a brief containing only the case. Agent A gets exactly Prune's view (field, question, constraints, values) and is asked to name the best candidate. If it names the winner, the winner is visible at sketch depth; rewrite. Agent B gets Shape's view (the same plus the evidence) and is asked the same. If it does not name the winner, the case does not fix its winner; rewrite.
3. Up to three attempts. Three to nine dispatches; 30 to 60 minutes including JP's reading.

**If a case passes both reads within three attempts:** candidate 5 is buildable. Run it as written, "Known-answer cases, Prune only", at about ten cases of the same kind, one or two 2.0 Prune dispatches each, counting cut or kept by cut type. About 1 to 3 more hours. Close T2's prereg with one added status line that points at the new test. One addition beyond the candidate's wording, optional and free because the file already exists: for each cut winner, read its `Revive if` line in `02-prune.md` and note whether it names the fixing fact. That is the T2 descriptive finding (the record anticipated the challenge) re-measured on 2.0, and it is the mechanism candidate 3 relies on.

What each result of that run implies:

- Most hidden winners cut: 2.0's Prune does not protect against this failure on such fields; safety rests on the ledger, revive-if, Contest, and re-run net. The response is a design change (a larger survivor count, giving Prune the evidence, or a stronger Contest), which is a separate decision.
- Most hidden winners kept: Prune's sketch-depth reading keeps evidence-backed winners more often than chance on built fields. Reassuring, bounded to authored fields, the author's word, one model family, about ten cases.
- Either way, a count about 2.0 exists where none does now, and which sub-question it answers is on record.

**If no case passes in three attempts:** the premise of the user's candidate ("unanswerable at acceptable cost") has been tested rather than assumed. Take candidate 3 as written: "Close T2 as unanswerable at acceptable cost and rely on watching real runs of the rebuilt skill instead." The status line can record that a successor test was attempted and found unbuildable at this cost.

### Why

- **The user's value and the user's lean pull apart, and a cheap check resolves the pull.** The lean closes the question; the value says knowing matters more than closing. The lean's premise is a factual claim about cost. Candidate 5 is the one candidate that could falsify that claim within a few hours, and its only open gap (G7) is exactly what the check settles. Accepting the premise untested is the one move the user's own value argues against.
- **Candidate 5 is the only survivor that yields a count about 2.0 now, without a judge, without T2's artifacts, and without the blind-evaluation overhead.** Candidates 1 and 2 are about version 1 unless 2 shows overlap, and both depend on artifacts and tooling whose state is unknown (G1-G4). Candidate 4 depends on real runs that have no track record and on a validity fork it does not settle. Candidate 3 yields no count at all.
- **The result would change what JP does.** A high cut rate points at a specific design change; a low one licenses leaving Prune alone. A result that would not change anything is not worth hours; this one would.
- **The check is cheap and two-sided.** It costs less than an hour, it catches both ways a case can be invalid (too visible, or not actually fixed), and it also forces the design choice (facts in Prune's view or not) that decides what the count means.

Assumption: the Prune agent is dispatched the way 2.0 dispatches it (in-session, fresh, unconfined). If JP wants the count free of any chance the agent read the hypothesis, dispatch Prune headless with the deny profile T2 used (prereg line 57). That adds setup and moves the measurement away from 2.0's own dispatch shape; I would not do it for the first ten cases.

### The Case Against

The runner-up is candidate 3 taken now, without the check. Its strongest honest case:

The count candidate 5 produces has the author's word as its only ground truth, no judge checks it, and it is a rate on fields built to hide the winner. JP may reasonably trust it no more than he trusts T2's unadjudicated 2% hint, and a number he would not act on is worth zero hours, not a few. Candidate 5 also does not test the part of 2.0 that actually carries safety: the cut record with its revive-if, the Contest line, and the re-run offer. T2's one data point favors that net (the record anticipated the challenge). Only real runs test the net on real fields, and candidate 3 is the only candidate that waits for them at no cost. Finally, the shape assessment found zero judgment failures across the whole build and about fifteen machinery failures; spending hours to test Prune's judgment repeats the pattern the rebuild was meant to end, protecting against a failure never observed.

Smallest realistic change that makes candidate 3 win outright: JP says a few hours is more than an author-asserted count is worth to him. Then skip the check and close now.

Candidate 4's best case, briefly: it is the only candidate that measures real fields at near-zero operator cost per run. It wins on the candidate-3 branch if real 2.0 runs start arriving at a steady rate and JP accepts the flag form (a detector reporting to him, not a recorded evaluation). The blinding fork must be chosen before the skill edit, not after.

The artifact path (2 then 1), briefly: it is the only path that puts a judged verdict on a real spontaneous catch rather than an authored one. It wins if G1, G2, and G3 all resolve cheaply and JP wants that verdict even though it is about version 1 at 1-of-7 reproduction with two judges.

### What Would Flip It

- The check fails three times: candidate 3, as stated above.
- JP reads his own value as "knowing matters, but not at a few hours": candidate 3 now, no check.
- Real 2.0 runs begin at a steady rate: on the candidate-3 branch, candidate 4 becomes worth its skill edit as a flag; choose the fork first.
- An agent lists `~/.t2-run/` and verifies the store hashes (G1), the re-shape brief is found at the seal commit (G2), and the 2026-07-22 wrapper probe still passes (G3), and JP wants a judged read of the S2 catch: run 2 first, then 1, in the same few hours. Run 2 first because its overlap result decides whether 1 says anything about 2.0.
- JP would fund two to three seeded cases and G3 passes with under about an hour of setup: revive candidate 6 (record below).
- 2.0's Prune brief is changed to include evidence: candidate 5's second kind of case (facts only in evidence) stops being meaningful and only the first kind should be built.

### Door

This is a two-way door, so there is no Commitment Point or Rollback section. The check and the run cost a few hours at most, touch no T2 artifact (JP's standing as a cold judge on T2 cases is unchanged), involve no ground-truth judge (no blinding can be lost), change nothing under the working tree, and the status edit is one line of text.

**Need from you:** one decision. (1) Run the check as described, or (2) skip it and close T2 now as candidate 3. If you choose (1), also say whether an agent or you will author the case.

## Cut records

```text
Option:         Seeded-dominator run — The successor the Results section sketched: from one to about a dozen seeded cases, the seeded candidate's crosswalk ID recorded at stem-freeze, k of 3 to 4 on the measured 0.71 committal rate, agent judges with confined read scope, allowlist-only inspection scripts from the first dispatch.
Cut:            constraint, judgment call
Reason:         Constraint 1 (well under 15 operator-hours), which the user confirmed at a price that names "any successor at T2's scale". What sets this candidate apart is a sensitivity rate, and a rate needs several cases. At the surface's band each case is about 1 to 2 hours of dispatches, and its setup is unpriced and heavy: an ARM C for the pipeline under test (2.0 has no full-field shaping mode, so this is a rebuild, or a restore of version 1 from the archive, which then makes the result about version 1), confinement tooling and a judge route whose survival is unknown (G3), a stem-freeze ledger, allowlist scripts before dispatch 1, and the unrun re-shape procedure (G2). T2's own Results say the adjudication layer is where its hours were mis-sized. At its lower end (one case) it fits the hours, but it is then a re-run of T2's positive control and no longer measures a rate. Judgment call because every hour figure is a band estimate, not a measurement.
Strongest case: It is the only candidate that measures the instrument's sensitivity, which is the one number that could give T2's existing 48-of-49 non-divergence a meaning; every other candidate leaves that null meaningless. It carries the bookkeeping fix (crosswalk ID at stem-freeze) that would have saved T2, and its ARM P arm yields candidate 5's count as a byproduct, so it strictly contains candidate 5's information. Under the user's stated value (knowing matters more than closing tidily) it is the candidate that value favors most.
Revive if:      JP would fund a two-to-three case run as an existence test rather than a rate; and an agent confirms (G3) that the archived role profiles, wrapper, packet template, and prompts still run with under about an hour of setup; and JP settles which pipeline plays ARM P, accepting that version 1 gives a result about version 1 and 2.0 requires a rebuilt control arm.
```
