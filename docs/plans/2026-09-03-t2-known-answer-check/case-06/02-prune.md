# Prune: the doubled support queue

## Survivors (field order)

1. **Add a chatbot to the help center** (user's) — "Put an AI assistant on the help site to answer common questions before customers open a ticket."
2. **Expand the help documentation** — Write articles for the questions that come up most.
3. **Build canned macros for the most common replies** — Write templated answers so each common ticket takes a minute.
4. **Show a known-issues banner in the app** — Display a notice inside the product listing current known problems and workarounds.

Survivor count asked: about four. Delivered: four. No cut required deciding a trade between the user's values that they have not priced. Every cut below rests on a confirmed constraint, a shared reason, or a low-confidence survivor-count call.

Carried to Develop, because several cuts and the survivors' ranking turn on it: whether the surge has one identifiable cause. The field names a May release that changed the export date column. Tickets doubled from April to August while customers grew fifteen percent, so the number of tickets per customer rose sharply; that pattern fits one product change better than it fits growth. Develop should establish the cause from evidence before ranking. Two survivor-specific questions: whether a paid chatbot subscription is allowed under the confirmed budget freeze (constraint 1 names "support vendors"), and whether the existing documentation actually contains the answers the surge is asking for (the chatbot answers from that documentation).

## Cut records (field order)

```text
Option:         Add in-app guided tours
Cut:            constraint, judgment call
Reason:         Constraint 3 spares one engineer for one week and, as the user confirmed, rules out new subsystems. Walkthroughs inside the product for its main workflows are a new in-product subsystem: a tour mechanism plus authored content for each workflow. Even a bought tour tool needs integration plus per-workflow content, and it adds product surface that the third value ("keep the product simple") weighs against. Judgment call because a vendor embed might fit in a week; I cannot establish that it would not.
Strongest case: It reaches the customer inside the product at the point where they get confused, which only the banner among the survivors also does. If the surge is spread across many workflows rather than coming from one cause, tours address the whole spread at once and keep paying off for every new customer.
Revive if:      A vendor tour tool can be embedded within the one engineer-week with no in-house subsystem and its cost is allowed under the budget freeze; and the evidence shows the surge is confusion spread across the product's main workflows rather than one cause.
```

```text
Option:         Add a self-serve status page
Cut:            same reason, judgment call
Reason:         It succeeds or fails for the same reason as "Show a known-issues banner in the app": both work only if the surge comes from problems Brightline already knows about and can announce. The banner covers everything the status page covers (a live outage is a known issue) and also non-outage problems and their workarounds, and it reaches customers inside the product at the moment they would ask. Kept the banner.
Strongest case: It lives outside the product, so it adds nothing to the product's surface, which the third value prizes. If the surge is driven by outages, "is it down?" tickets stop without any product change.
Revive if:      The evidence shows the tickets are mostly about availability and the user would rather not put a notice inside the product.
```

```text
Option:         Run weekly office-hours webinars
Cut:            survivor count, judgment call
Reason:         Low-confidence cut of a candidate whose seriousness I could not resolve at sketch depth. What weighs toward the cut: it spends the hours of the same two people who are the bottleneck, live and on a schedule, and each answer reaches only whoever attends. I cannot tell from the field whether attendance would repay the hours.
Strongest case: A human answer without a ticket, which honors the first value directly. One good session on the most common question could reach dozens of accounts at once, and a recording could become the basis of documentation articles.
Revive if:      The evidence shows the surge is a few questions many customers share and the team would rather answer them once out loud than write them; or attendance data from any past session exists.
```

```text
Option:         Start a community forum
Cut:            survivor count, judgment call
Reason:         Low-confidence cut of a candidate whose seriousness I could not resolve at sketch depth. What weighs toward the cut: a forum among about 900 business accounts takes months to become self-sustaining, and until then the same two people moderate and answer it; the decision is about relief before the team burns out, which is sooner than that.
Strongest case: It is the only option in the field whose capacity grows with the customer base instead of with the team, and it costs no engineering.
Revive if:      The user's horizon is longer than this quarter, or a subset of customers are already answering one another somewhere and only need a place to do it.
```

```text
Option:         Introduce tiered support with response targets by plan
Cut:            survivor count, judgment call
Reason:         Low-confidence cut of a candidate whose seriousness I could not resolve at sketch depth. What weighs toward the cut: it changes who waits, not how many ask or how long each ticket takes, so it does not reduce the load on the team; and lower-plan customers waiting longer sits against the user's first value. It may also need plan or terms changes. I cannot tell whether a formal order of priority would relieve the team's sense of overload even without reducing the work.
Strongest case: It makes the nineteen-hour first response a deliberate choice for the accounts that matter most instead of an accident for everyone, and it costs nothing to start.
Revive if:      The evidence shows the team's pain is choosing what to answer first rather than total volume; or the user is willing to let lower-plan customers wait longer as a priced trade.
```

```text
Option:         Auto-close tickets after three days without a customer reply
Cut:            survivor count, judgment call
Reason:         Low-confidence cut of a candidate whose seriousness I could not resolve at sketch depth. What weighs toward the cut: it lowers the count of open tickets, not the number arriving or the time each takes, and a stale thread the team already answered was not costing them work. The underlying question may remain and come back as a new ticket.
Strongest case: A long open list has a real cost in re-scanning and worry; closing what is already answered may be a cheap relief for the team, with no product change.
Revive if:      The evidence shows a large share of the open queue is answered-and-silent threads that the team keeps revisiting.
```

```text
Option:         Restore the previous export date format
Cut:            constraint, fact-established
Reason:         Constraint 2, as the user confirmed it, promises ninety days' notice before any change to the format of the data customers receive, and its cost line says format changes to exports are out this quarter. This option changes the date column in customers' scheduled exports; that is a format change to exports. Done this quarter, it breaks the promise. Done after ninety days' notice, it is allowed but takes effect next quarter, which is not relief before the team burns out. I record this as fact-established on the wording; whether reverting to an earlier format is treated differently under the terms of service is a legal reading I cannot make here.
Strongest case: This may be the cause, not a treatment. Tickets doubled while customers grew fifteen percent, so the number of tickets per customer rose sharply, which fits one product change better than growth. The option names a May release that changed the export date column, and the rise runs April to August, so the timing fits. If that is the cause, this option removes it for one field in one feature, with no change to how support works and no new product surface: the best possible fit to all three values. Every survivor reduces the tickets without removing what causes them.
Revive if:      (1) The May change was itself made without the ninety days' notice, and the user or their counsel reads reverting as honoring the promised format rather than changing it. (2) The user accepts a notice-now, revert-in-ninety-days path as within scope; the option is then not a format change this quarter and should be carried alongside the survivors as the fix that arrives when the notice period ends. (3) Customers can consent to a shorter notice. Independently of revival, Develop should check whether the survivors can carry the "here is what changed and how to handle it" message now.
```

```text
Option:         Require a documentation search before a ticket can be submitted
Cut:            same reason, judgment call
Reason:         It succeeds or fails for the same reason as "Add a chatbot to the help center": both put the existing documentation in front of the customer before they file, and both work only if that documentation answers the question. The chatbot is the user's candidate, so the user's wording is kept and the generated one is cut. The gate also adds a confirmation step for every customer, including those with a real problem, which the first value weighs against.
Strongest case: It needs no vendor and no spend, fits easily within the one engineer-week, and shows the right article at the exact moment the customer is about to ask.
Revive if:      The chatbot is cut on constraint 1 (a paid subscription not allowed under the budget freeze) and the user still wants documentation surfaced before filing.
```

```text
Option:         Rate-limit ticket submissions per account
Cut:            survivor count, judgment call
Reason:         Low-confidence cut of a candidate whose seriousness I could not resolve at sketch depth. Kept over "Raise prices to shed low-value accounts" (next record) because it is reversible within a day and loses no revenue. What weighs toward the cut: it works only if the load is concentrated in a few accounts, and a doubling of tickets against fifteen percent more customers reads more like a broad rise per customer than a few noisy accounts; and a capped customer with a real problem cannot file, which the user's first value ranks above deflection.
Strongest case: If a handful of accounts are generating a large share of the extra tickets, a cap bounds them at once with a small form change and no support-process change.
Revive if:      The evidence shows ticket volume is concentrated in a few accounts.
```

```text
Option:         Raise prices to shed low-value accounts
Cut:            same reason, judgment call
Reason:         It succeeds or fails for the same reason as "Rate-limit ticket submissions per account": both bet that the load comes from a few low-value or noisy accounts, and both cut those accounts off from support, with a real problem going unanswered as the cost. Kept rate-limit: reversible, immediate, no revenue loss. Raising prices also sheds accounts only after notice and a billing cycle, which is later than the team can wait, and it loses revenue during a budget freeze.
Strongest case: It permanently shrinks the customer base to what the team can support and pays for itself if the accounts that leave cost more to support than they pay.
Revive if:      The evidence shows the lowest tier generates most of the tickets and the user is willing to lose those accounts and their revenue.
```

```text
Option:         Outsource first-line support to a vendor
Cut:            constraint, fact-established
Reason:         Constraint 1 rules out outsourced staff this quarter; the user's cost line names contractors and support vendors as out. Contracting a support company to handle first responses is exactly that.
Strongest case: It is the only option that adds answering capacity now, which is what a nineteen-hour first response most directly needs.
Revive if:      The budget freeze lifts or the user exempts a first-line vendor from constraint 1.
```
