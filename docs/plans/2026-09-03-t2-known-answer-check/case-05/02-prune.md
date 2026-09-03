# Prune: the slow hiring process

Survivor count asked for: about four. Survivors: four. Cuts: eleven.

## Survivors (field order, exact wordings)

1. **Engage a recruiting agency** (user's) — "Use an external agency to source and screen candidates so the team only sees finalists."
2. **Batch the loop into a single onsite day** — Run all four stages back to back on one day per candidate instead of spread over weeks.
3. **Automate interview scheduling** — Use a scheduling tool so candidates pick slots from interviewers' live calendars.
4. **Put the hiring decision meeting on a standing daily slot** — Reserve a short slot every day for hiring decisions and require interviewers to attend or submit a written vote before it.

## Cut records (field order)

```text
Option:         Introduce a referral bonus — Pay employees for referrals who are hired.
Cut:            survivor count, judgment call
Reason:         Low-confidence cut to reach the count. I could not resolve its seriousness at sketch depth. The field's mechanism ("referred candidates tend to move through faster") depends on referred candidates moving faster through a loop that constraint 3 fixes at the same four stages for everyone, so it is unclear what a referral would speed up inside the measured span. It does not fail a confirmed constraint: the bonus goes to an employee, not to the offer. Mild tension with "fairness and consistency across candidates", since referral-heavy pipelines favour existing networks.
Strongest case: The cheapest sourcing change in the field. Referred candidates are better informed about the company and less likely to withdraw, and five withdrawals last quarter is the stated loss.
Revive if:      A later stage finds withdrawals concentrate among cold-sourced candidates, or finds that referred candidates do reach the loop with less pre-loop delay.
```

```text
Option:         Add a part-time sourcer — Bring in a contractor to find and approach candidates directly.
Cut:            dominated, judgment call
Reason:         Dominated by "Engage a recruiting agency" at the depth I can see. The agency both finds candidates and screens them so fewer people enter the four-stage loop; the sourcer only finds candidates and, by its own description, "changes nothing after first contact". Under constraint 2 (manager hours capped at four a week), more candidates entering an unchanged loop tends to lengthen the queue, not shorten the 71 days. The one dimension I could not see is cost: a contractor's rate against a per-hire fee.
Strongest case: If the real shortage is at the top of the funnel and the loop itself is fine, a sourcer fixes that without paying an agency fee per hire, and keeps screening in-house.
Revive if:      The agency is cut or rejected at a later stage and the top of the funnel proves to be the shortage, or the cost comparison strongly favours a contractor.
```

```text
Option:         Rewrite the job posts — Rework the postings for clarity and appeal.
Cut:            survivor count, judgment call
Reason:         Low-confidence cut to reach the count. I could not resolve its seriousness at sketch depth. The option acts before first contact, and the decision question measures first contact to accepted offer, so I cannot see whether it changes the 71-day span at all. The field's own note says it "helps only if the posts are what slows or deters candidates", and nothing in the case says they are.
Strongest case: It costs a few hours and nothing else. If the posts deter strong candidates or set wrong expectations that later cause withdrawals, it is the cheapest fix in the field.
Revive if:      A later stage finds low application rates or candidate feedback that points at the postings.
```

```text
Option:         Shorten the take-home exercise — Cut the take-home from its current length to about an hour.
Cut:            survivor count, judgment call
Reason:         Low-confidence cut to reach the count. I could not resolve its seriousness at sketch depth. Two things are unknown: how many of the 71 days are candidates holding the take-home, and whether a one-hour version keeps the signal the loop relies on. The user puts candidate quality above speed, so a version that loses signal would work against the stated values, but whether it loses signal is a fact I cannot see here. It does not fail constraint 3: the stage stays, only its content changes.
Strongest case: Long take-homes are exactly what candidates with competing offers skip. Shortening it may retain the strongest candidates and improve the candidate's experience of the process, both stated values.
Revive if:      A later stage finds candidate drop-off or the largest calendar gap sits at the take-home stage.
```

```text
Option:         Train interviewers to submit feedback faster — Set a same-day feedback rule and coach interviewers on writing it quickly.
Cut:            survivor count, judgment call
Reason:         Low-confidence cut to reach the count. I could not resolve its seriousness at sketch depth: how much of the 71 days is the gap between an interview and its write-up is unknown. If the surviving "Batch the loop into a single onsite day" is adopted with a same-day debrief, most of that gap disappears anyway, so this option's value depends on that survivor failing. It does not fail a confirmed constraint.
Strongest case: Nearly free, adds no manager hours, is fairness-neutral, and could land within a week. If stages are booked only after the previous stage's feedback arrives, this lag compounds four times per candidate.
Revive if:      Batching is rejected and feedback lag shows up as a large share of the days.
```

```text
Option:         Add an early technical screen call — Insert a short technical call before the loop to filter earlier.
Cut:            same reason, judgment call
Reason:         Same reason as "Engage a recruiting agency", the user's candidate, so the user's wording is kept and this one is cut. Both work by filtering candidates before the four-stage loop so fewer people consume the capped manager hours, and both fail for the same reason: if the 71 days come from calendar gaps inside the loop rather than from its load, filtering earlier shortens nothing. On my reading it does not fail constraint 3, since it adds a step before the loop and removes none of the four stages; but it does add a step to every successful candidate's path, which lengthens their span.
Strongest case: It keeps screening in the company's own hands with consistent criteria, which serves both "candidate quality" and "fairness and consistency", and it costs no fee per hire. An agency's screening quality is unknown; this one is not.
Revive if:      The agency is cut or rejected later, or a later stage finds loop load rather than loop gaps is the bottleneck and in-house screening is preferred for quality or fairness.
```

```text
Option:         Pre-approve offer packages before the final stage — Have finance sign off the offer range for each candidate before the final interview rather than after.
Cut:            survivor count, judgment call
Reason:         Low-confidence cut to reach the count. I could not resolve its seriousness at sketch depth: how long finance sign-off takes now is unknown, and the option saves at most that many days at the very end of the process. It does not fail a confirmed constraint and it costs nothing.
Strongest case: Free, removes a serial step, and lets the final-stage conversation end in an offer rather than a wait. Candidates who are weighing other offers are lost in exactly that wait.
Revive if:      A later stage finds offer approval takes more than a few days, or the recommendation wants same-day offers after the final stage.
```

```text
Option:         Send offers with a 48-hour expiry — Give candidates two days to accept.
Cut:            dominated, judgment call
Reason:         Dominated by "Pre-approve offer packages before the final stage" at the depth I can see. Both act on the tail of the process. Pre-approval shortens the company's own delay before an offer goes out with no cost to the candidate; the expiry shortens the candidate's deliberation by pressuring them, which the field itself says "risks the candidate experience", and which works against two stated values (candidate experience, and quality over speed). The case's loss mode is candidates taking other offers; a two-day deadline on someone comparing offers tends to push them to the other one, so it also risks quality. The one dimension I could not see is calendar days saved, and I judge it unlikely to favour the expiry for the reason just given.
Strongest case: If candidates are sitting on offers for weeks while the company waits, a firm deadline is the only option in the field that shortens that specific wait, and it is free.
Revive if:      A later stage finds candidate deliberation after the offer is a large share of the 71 days and the user is willing to trade candidate experience for it.
```

```text
Option:         Add a sign-on bonus — Offer a one-time bonus on acceptance.
Cut:            constraint, fact-established
Reason:         Fails constraint 1. The user stated what that constraint costs: "paying more per offer is out". A one-time bonus on acceptance is paying more per offer.
Strongest case: A one-time bonus does not move the compensation bands, and it may be the smallest lever that converts a candidate who is comparing offers.
Revive if:      Constraint 1 is relaxed to allow one-time payments outside the bands.
```

```text
Option:         Adopt an applicant-tracking system — Move the pipeline into a dedicated system with stage tracking and reminders.
Cut:            survivor count, judgment call
Reason:         Low-confidence cut to reach the count. I could not resolve its seriousness at sketch depth. Two things are unknown: whether the 71 days come from candidates going untracked between stages (what an ATS fixes) rather than from the lags the surviving scheduling, batching, and decision-slot options fix directly; and whether one part-time coordinator can run a setup project inside three months while also running six hires. It does not fail a confirmed constraint; a subscription is not headcount budget.
Strongest case: With one part-time coordinator and six hiring managers, nobody can see where each candidate is. Stage tracking and reminders might be the change that makes every other fix stick, and many such systems include the scheduling automation that survived.
Revive if:      A later stage finds candidates go untracked between stages, or the scheduling tool chosen is an ATS module anyway.
```

```text
Option:         Hire a full-time in-house recruiter — Replace the part-time coordinator with a dedicated recruiter who owns the process end to end.
Cut:            constraint, judgment call
Reason:         Fails constraint 1 on the plain reading. A full-time role is new headcount cost this cycle; the constraint bars increasing the headcount budget, and prices anything funded from it as fewer engineering hires. The option does not offer to give up a hire, and replacing a part-time coordinator offsets only part of a full-time salary. Judgment call rather than fact-established because the funding source and whether the cap covers non-engineering roles are not settled in the case. Supporting point: hiring the recruiter goes through the same process, median 71 days, inside a roughly 90-day window, so they would arrive with a few weeks left in the cycle.
Strongest case: The process has no owner: one part-time coordinator across six hiring managers. An owner is the one change that attacks every lag at once, and a recruiter may be findable faster than an engineer.
Revive if:      The user confirms funding outside the headcount budget, or accepts five hires instead of six, and the horizon extends past this cycle.
```

## Carried forward, not cuts

- The agency's per-hire fee and whether constraint 1's "headcount budget" covers recruiting spend are unresolved at this stage. No cut was made on it; the Develop stage should settle it.
- "Batch the loop into a single onsite day" does not add manager hours, but it concentrates them. The Develop stage should check one candidate-day against the four-hour weekly cap per manager.
