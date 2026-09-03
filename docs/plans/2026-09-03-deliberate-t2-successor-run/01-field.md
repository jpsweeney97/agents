# 01 — Field (Generate stage, `ideate`)

Question: What should be done with T2, the shallow-prune safety experiment, now that `deliberate` has been rebuilt light as version 2.0 and still contains a shallow Prune stage?

**Frame the prompt assumes:** T2's question ("does the shallow Prune systematically cut candidates that full shaping would have crowned?") is still the right question to ask of version 2.0; JP's operator hours are the scarce resource; an option is any course of action on that question costing well under 15 operator hours. The assumption most of the field shares without saying so: that the answer has to come from watching agents prune. Some options below do not share it.

Terms used in the options, defined once. **ARM P** is T2's shipped-pipeline arm (Generate, Prune, Shape, Recommend). **ARM C** is T2's control arm, which shaped the whole field with no Prune and then recommended. **k** is the number of repeat Recommend runs per case. **Crosswalk** is the table that maps each generated candidate wording to a stable ID; **stem-freeze** is the moment the shared field is frozen and that table is made. **Survivor count** is how many options Prune keeps (about four by default in 2.0). **Seeded case** is a decision case built with one candidate designed to be the strongest yet fall to the survivor count. **Divergence** is a control-arm close that crowns a candidate the pipeline arm cut. **Codebook extraction** is T2's mechanical reading of a close text into a winner set by blind agents.

Ordered by the source each option draws on: T2's existing artifacts, then real runs of 2.0, then new prepared cases, then no measurement of the prune at all. Within a group, alphabetical by handle. No order below is a quality order.

---

## From what T2 already produced

**Adjudicate the one divergence** — Take the S2 candidate that ARM C crowned once in seven repeats and ARM P cut in both its repeats, re-shape it and ARM P's winner under one identical neutral single-pass condition, and put the pair to two agent judges whose read scope is confined to that packet.
Sets it apart: bets the single existing catch is a real one, on the panel control seat's reading that a rare crowning which survives clean adjudication counts; one packet, not the adjudication layer as sized.

**JP reads S2 un-blinded** — JP reads ARM C's S2 close and ARM P's S2 winner himself, with no blinding, and records what he sees, labelled a non-blind read.
Sets it apart: no judge is being protected, so no blinding is spent; buys one informed human opinion on a single instance at the price of never being able to use JP as a blind judge for that case.

**Publish what T2 measured, with its limits** — Close T2 by stating its mechanical result as the answer at its evidence grade: one divergent close in 49, unadjudicated; the cut's own Prune record anticipated it; Contest did not name it. Further descriptive passes over the stored closes and exclusion sets need no new dispatches.
Sets it apart: bets that the existing measure, disclosed with its bounds, is the answer the question can afford; adds no case, no judge, no run.

**Same fields, 2.0 Prune** — Run version 2.0's Prune method on the seven frozen T2 fields and compare its exclusion sets with the stored ARM P sets (which agreed with themselves at 0.52 to 1.00 intersection over union).
Sets it apart: does not test safety; tests whether T2's data describes the rebuilt Prune at all, which decides whether any use of T2's artifacts is about 2.0.

**Second pruner, same fields** — Have a different pruner cut the seven frozen T2 fields, either a non-Claude model or JP himself before he sees any agent cut, and develop only the candidates the two pruners disagree on.
Sets it apart: uses disagreement between pruners as the locator of risky cuts in place of a full-shaping arm; says nothing about a candidate both pruners cut.

**Test Contest, not Prune** — Feed S2's cut records and close to version 2.0's Contest method and record whether it names the candidate that version 1's Contest missed.
Sets it apart: treats the safety property as Prune plus Contest plus the revive offer, and tests the component that did not fire on the one instance; a few dispatches, no arm, no judge.

## From real runs of version 2.0

**User's candidate (theirs, quoted exactly):** "Close T2 as unanswerable at acceptable cost and rely on watching real runs of the rebuilt skill instead."
Sets it apart: the detectors are the cut ledger, the Contest line, and the re-run offer already in 2.0; JP's reading of them is the judge; no apparatus beyond the skill.

**Develop one cut per run** — After every real close, a fresh agent shapes the survivor-count cut with the strongest recorded case and reports whether it beats the close.
Sets it apart: bets a missed winner would be the cut whose own record argued hardest for it (the one T2 divergence was exactly that); accrues one observation per run without JP's attention.

**Paired real runs** — Run each real decision twice, once at the default survivor count and once at about double it, and compare the two closes mechanically for a winner the narrower run cut.
Sets it apart: gives every real decision its own wider control arm; needs no judge, because the comparison is between two closes of the same decision.

## From new prepared cases

**Divergence without a judge** — For any new collection, define the outcome as codebook-extracted divergence (which reached 96.4% dual-extractor agreement in T2) and drop adjudication.
Sets it apart: removes the layer where T2's verdict was to be made and the blinding burden with it; accepts that divergence and damage become the same word.

**Known-answer cases, Prune only** — Author decision cases where the best option is fixed by the evidence in the case but not obvious at sketch depth; run only 2.0's Prune and count how often the known winner is cut.
Sets it apart: no control arm, no judge, no blinding, because the ground truth is written into the case; rests on such cases being writable without the winner showing.

**Past decisions as cases** — Take decisions JP already made whose outcome is known, run Generate and Prune with the outcome kept out of the agent's read scope, and check whether the option that in fact worked survives the cut.
Sets it apart: ground truth is history rather than construction; depends on a stock of decided cases and on the outcome staying out of the agent's reach.

**Seeded-dominator run** — The successor the Results section sketched: from one to about a dozen seeded cases, the seeded candidate's crosswalk ID recorded at stem-freeze, k of 3 to 4 on the measured 0.71 committal rate, agent judges with confined read scope, allowlist-only inspection scripts from the first dispatch.
Sets it apart: measures the instrument's sensitivity directly instead of waiting for a roughly 2% spontaneous rate; a positive result gives T2's existing 48-of-49 non-divergence a meaning it does not have now.

**Unattended full-scale re-run** — Re-run the sealed design at its original scale with an orchestrating agent as the operator and every inspection routed through allowlist-only scripts; JP reads only the verdict.
Sets it apart: bets the binding cost was operator attention rather than dispatches and that it can be engineered to near zero; treats the hours ceiling as a design target, not a limit.

## Without measuring the prune

**Argue safety from the rules** — Write the argument that the shallow prune cannot lose a winner silently: every survivor-count cut carries a reason, a strongest case, and a revival condition; Contest reads them against the close; a preferred exclusion is always a live challenge; a re-run revives on request.
Sets it apart: an answer in the form of an argument that can be refuted by reading; costs a document.

**Ask the pruner what it would miss** — Dispatch fresh agents with the Prune method text and ask them to name the kinds of candidates it would systematically cut wrongly; use the answer as the finding, or as the target list a seeded run would need.
Sets it apart: self-report in place of measurement; output is a list of candidate kinds, not a rate.

**Look for an outside answer** — Look outside the repo for what is known about early-elimination error in staged selection (screening funnels, tournaments, beam search) and map it onto Prune.
Sets it apart: bets the question is not specific to this skill; relaxes the no-research constraint.

**Make Prune cut less** — Change Prune so fewer decisive sketch-depth cuts happen: carry survivor-count cuts into Recommend at sketch depth, or raise the default survivor count, or give the cut side a short shaping pass before a cut lands.
Sets it apart: removes the exposure instead of measuring it; trades the question for run cost and for depth asymmetry inside Recommend.

**Price the question first** — Before spending anything, decide what a missed winner costs across the decisions deliberate will actually run on, and set the test budget from that number, possibly at zero.
Sets it apart: decides whether to decide; its output is a budget, not evidence.

**Withdraw the owed check** — Record that the check was owed by version 1's spec, that 2.0's close already says it did not develop the excluded options, and that no document now claims the prune is safe; remove the obligation.
Sets it apart: changes what is claimed rather than what is known.

---

Untouched fixed point: constraint 2. No option proposes a blind evaluation that breaks the blind-evaluation rule or proposes changing that rule; every option that uses a judge keeps it, and the rest avoid it by using no judge or by being openly non-blind.
