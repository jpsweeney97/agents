# 06 — the orchestrator's close as delivered to the user

The final message of the deliberate 2.0 run, verbatim: Recommend's close, the cut ledger table, the exclusion-check line, the run directory, the re-run offer, and what the run did not do.

---

The run is complete. **The recommendation is `check first`, not your lean: spend 30 to 60 minutes trying to write one "known-answer" decision case, and let that result choose between a cheap Prune-only count and closing T2 as you proposed.** All five stages ran as isolated fresh agents. The full working, including the comparison table, is in `04-close.md` in the run directory below.

## The close (Recommend stage, as written)

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

## Cut ledger

Candidate numbers in the close refer to the six survivors: 1 Adjudicate the one divergence, 2 Same fields 2.0 Prune, 3 your candidate, 4 Develop one cut per run, 5 Known-answer cases Prune only, 6 Seeded-dominator run. Fourteen cuts are Prune's; the last is Recommend's.

| Option | Cut | Revive if |
| --- | --- | --- |
| JP reads S2 un-blinded | same reason, judgment call | Candidate 1 is cut or fails to adjudicate cleanly, and JP accepts giving up his blind-judge standing on S2 |
| Divergence without a judge | same reason, judgment call | A new collection is chosen and needs its outcome rule |
| Unattended full-scale re-run | constraint, fact-established | Constraint 1 restated as operator hours only, and a small unattended pilot shows hours well under 15 at full scale |
| Argue safety from the rules | same reason, judgment call | Your candidate is cut, or you want its reliance written as a refutable claim |
| Look for an outside answer | constraint, fact-established | The no-research constraint is lifted |
| Withdraw the owed check | dominated, judgment call | Your candidate is cut, or you want the obligation's origin recorded separately |
| Publish what T2 measured, with its limits | survivor count, judgment call | Candidate 2 shows 2.0's cuts match T2's stored cuts, or you want a stated finding on record before any new dispatch |
| Second pruner, same fields | survivor count, judgment call | A non-Claude pruner with independent bias is available, and a confined judge is designed within the blind rule |
| Test Contest, not Prune | survivor count, judgment call | Candidate 3 or 4 is chosen (both rely on Contest as a detector), or it folds into candidate 1's packet |
| Paired real runs | survivor count, judgment call | Real-run accrual is chosen and you accept doubled per-run cost, or candidate 4 proves too narrow |
| Past decisions as cases | survivor count, judgment call | You can name several decided cases with hidden winners and accept realised outcome as ground truth |
| Ask the pruner what it would miss | survivor count, judgment call | Candidate 5 or 6 is chosen and needs a list of candidate kinds to seed against |
| Make Prune cut less | survivor count, judgment call | Any measurement shows a miss rate, or you decide to remove the exposure rather than measure it |
| Price the question first | survivor count, judgment call | You want a stated cost of a missed winner before choosing |
| Seeded-dominator run | constraint, judgment call (Recommend) | You would fund a 2-3 case existence test, the archived tooling runs with under an hour of setup, and you settle which pipeline plays ARM P |

**Exclusion check: live recorded challenges — "Test Contest, not Prune", "Make Prune cut less", "Price the question first", "Paired real runs", "JP reads S2 un-blinded", "Publish what T2 measured, with its limits"; most worth contesting: Test Contest, not Prune.** In plain words: that option's revive condition is "candidate 3 or 4 is chosen", and the close's fail branch chooses candidate 3, so the close nearly satisfies the condition for reviving it.

Run directory: `/private/tmp/claude-501/-Users-jp--agents/3437dee8-3161-4206-8e99-3af80da3df71/scratchpad/smoke/deliberate-t2-2026-09-03/`

To re-run, tell me which cut to revive, which constraint to change, or which survivor to develop further, and I will restart from the stage that changes.

What the run did not do: it did not verify facts the stages marked as assumptions, chiefly the per-dispatch time band, whether the T2 workspace is still intact, and that 2.0's Prune resembles version 1's. It did not develop the fifteen excluded options. One setup choice of mine to flag: I let stages read the prereg's Results section beyond the frontmatter and Question you pointed to, because it holds the measured rates the options were built on.

**Need from you:** one decision.
1. Run the check as described (say whether an agent or you will author the case).
2. Skip the check and close T2 now as your candidate.
3. Revive "Test Contest, not Prune" and restart from Shape, since Contest flagged it as the cut most worth contesting.
