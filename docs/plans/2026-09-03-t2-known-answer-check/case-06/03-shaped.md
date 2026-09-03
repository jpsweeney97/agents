# 03-shaped — comparison surface for the four survivors

Shape stage of the `deliberate` run on Brightline's doubled support queue. Field order preserved as Prune carried it. No ranking, scoring, filtering, or recommendation is performed here; several answers below are unkind to particular options, and that is development against evidence, not a verdict.

## The four options, as supplied

1. **Add a chatbot to the help center** (user's) — "Put an AI assistant on the help site to answer common questions before customers open a ticket."
2. **Expand the help documentation** — Write articles for the questions that come up most.
3. **Build canned macros for the most common replies** — Write templated answers so each common ticket takes a minute.
4. **Show a known-issues banner in the app** — Display a notice inside the product listing current known problems and workarounds.

## Shared findings, established before the per-option questions

**The surge has one identifiable cause, and the evidence names it.** Prune carried this question forward, and the supplied evidence settles it. Tickets tagged `export-dates` went from 0 in April to 482 in August (E1). Total tickets rose by 420 over the same period, so this one category is larger than the entire increase — every other category held flat or fell (how-to 140 to 118, billing 90 to 96, other 180 to 134). Non-`export-dates` volume actually declined in absolute terms, from 410 to 348, while accounts grew from 780 to 900 (E6). Customer growth therefore does not explain the surge; it runs the wrong direction.

The mechanism is documented. Release 5.12 on May 6 upgraded a CSV library, which unintentionally changed the export date column from the documented ISO 8601 form to `08/01/2026 00:00`, breaking customers' downstream imports (E1, E2). Bug tracker issue #2291 is open, priority medium, estimated two days including tests.

One evidence inconsistency, recorded rather than smoothed: E6 characterizes the non-`export-dates` rate as flat at about 0.4 tickets per account per month, but the tabulated figures give 0.53 in April and 0.39 in August. The direction of the finding is unaffected — non-export volume did not rise — but the "flat" characterization is not exactly what the tables show.

**Constraint 2 binds none of the four options.** The ninety-day notice promise governs changes to the format of data customers receive. None of these four options changes an export or API response format, so the constraint is inert across the whole field. It is stated once here rather than repeated per option. Separately, E3 records that restoring the documented format would count as a correction rather than a change and would need no notice — that fact does not act on any option in this field, and is noted because it removes a constraint someone might otherwise assume applies.

**Constraint 1 (budget freeze, no vendors) and constraint 3 (one engineer for one week) do discriminate**, and appear per option under question 2.

## Live comparison questions

Six questions survived the liveness test: each one has answers that differ across the options, or exposes an assumption that could reverse a later choice. Generic criteria that do not separate these four are omitted.

### Q1. Which slice of the August queue does it act on, and how large is that slice?

**Chatbot.** How-to questions, 118 a month and falling from 140 in April (E1). E5 prices the reachable share directly: a vendor pilot on comparable content deflected 20 to 30% of how-to tickets, which against 118 is at most about 35 tickets a month. The chatbot answers from the help documentation, so it cannot answer the `export-dates` question, whose true answer is that the product is emitting the wrong format.

**Expand documentation.** The same how-to slice, 118 a month. E5 reports documentation already covers about 85% of how-to questions, so new articles address the uncovered remainder, roughly 18 tickets a month if the uncovered share and the ticketing share match. That inference is not safe, and question 5 takes it up.

**Canned macros.** Acts on handling time rather than volume, so its slice is measured differently. E4 shows the largest opportunity is already taken: the `export-dates` macro was applied to 470 of the 482 tickets, at a six-minute median. Remaining reach is whatever common replies in billing (96) and other (134) lack a macro today, which the evidence does not enumerate.

**Known-issues banner.** The `export-dates` slice, 482 a month, is the largest reachable slice of any option in this field. Reach depends on customers seeing the banner before they file. Scheduled exports are used by 610 of 900 accounts (E7), which bounds the audience, but the breakage surfaces in the customer's own spreadsheet or importing system (E1), not inside Brightline's product. No evidence supplied says how often an `export-dates` ticket-opener visits the app first.

### Q2. What does it cost against the two constraints that discriminate?

**Chatbot.** Both routes are pinched by a confirmed constraint. A vendor subscription runs into constraint 1, which puts support vendors out under the budget freeze; E5's own evidence is a chatbot vendor's pilot, so the vendor route is the evidenced one. The option's wording does not require a vendor, but a self-built assistant is a new subsystem, which constraint 3 explicitly rules out at one engineer for one week. This is recorded as a constraint consequence, not applied as a filter; the candidate stays in the field and the decision belongs downstream. The unresolved fact is whether a chatbot subscription counts as a support vendor under the freeze, and at what price.

**Expand documentation.** No spend and no engineer time. The cost is writing hours drawn from a two-person team whose first-response time has already slipped from four hours to nineteen, which puts it in direct tension with the stated value of the support team's sustainability. The evidence supplies no estimate of hours per article.

**Canned macros.** The cheapest against both constraints. No spend, no engineer, and E4 confirms the capability already exists and is in daily use, so this is extending an established practice rather than building anything.

**Known-issues banner.** Needs product work, so it draws on constraint 3's single engineer-week. Whether a banner fits inside that week is unevidenced; no estimate for banner work appears in the file, unlike the two-day figure on record for the underlying bug fix (E2). It also touches the stated value of keeping the product simple, since it adds a permanent surface to the interface.

### Q3. Does it end the stream of tickets, or make each one cheaper?

E4 is the decisive fact for the whole field: each `export-dates` ticket generates a median of 2.3 follow-ups, because the scheduled export re-runs weekly and the customer has to re-apply their fix every week. Nothing that leaves the export output unchanged stops that weekly regeneration.

**Chatbot.** For how-to questions, answering generally does end that instance. For `export-dates` it ends nothing, since the customer's export breaks again the following week.

**Expand documentation.** Same as above. A documented weekly workaround converts a support ticket into a recurring customer chore rather than removing it.

**Canned macros.** Explicitly the make-each-one-cheaper option; it does not reduce the count. E4 lets the current load be estimated: about 482 originating tickets plus roughly 2.3 follow-ups each is near 1,590 touches a month, and at the six-minute median that is roughly 160 hours, approaching one full-time person-month out of a two-person team. That estimate assumes follow-ups cost about what an initial macro reply costs, which the evidence does not state.

**Known-issues banner.** Can suppress ticket creation but not the underlying weekly breakage. A customer who reads the banner still has a broken import each week, so the option converts tickets into silent customer effort.

### Q4. Does its value survive the export defect being corrected, or does it depend on the defect persisting?

This question separates the field structurally.

**Chatbot.** Independent of the defect. Its how-to value is unchanged either way.

**Expand documentation.** Independent of the defect, with one exception: any article written to document the export workaround becomes obsolete on correction.

**Canned macros.** Largely dependent. Its measured value today is concentrated in a macro that exists to answer a recurring complaint about a known bug; if the format were corrected, the macro's 470-ticket application would fall away and remaining reach would be the unenumerated billing and other categories.

**Known-issues banner.** Dependent by construction. The option is defined as listing current known problems and workarounds, so its content is the defect. Corrected, it has nothing to display for this surge.

### Q5. What does each assume about why customers contact support instead of self-serving?

This exposes an assumption that could reverse a later choice, and it cuts in more than one direction.

The evidence contains a tension worth naming: 118 how-to tickets arrive each month despite documentation that already covers about 85% of how-to questions (E5). Either those tickets fall in the uncovered 15%, or customers are not finding and using documentation that already answers them. The supplied evidence does not distinguish these.

**Chatbot.** Assumes findability is the binding problem, since it surfaces existing content rather than creating it. If the tension resolves toward customers not finding covered answers, that assumption is favourable to this option, and E5's 20 to 30% pilot figure would be the honest ceiling on the benefit.

**Expand documentation.** Assumes coverage is the binding problem. If the tension resolves toward findability, new articles address a small residue and the roughly 18-tickets-a-month figure in Q1 becomes an overestimate.

**Canned macros.** Assumes nothing about self-service; it accepts the contact and shortens it.

**Known-issues banner.** Assumes customers do not know the cause and would stop before filing if told. E9 supplies weak adjacent evidence against easy optimism: a status page has been live since 2024, and 482 tickets were filed anyway. That evidence is weak because the status page is not in-app, and E9 records no outage in the period, so the export defect may never have been posted there.

### Q6. What does it deliver against the stated value that customers getting what they need outranks deflection?

**Chatbot.** Deflection-shaped by construction; the option wording is to answer questions "before customers open a ticket," and E5 measures it in tickets deflected. For a genuine how-to question, a fast correct answer is what the customer needs, so deflection and service coincide. For `export-dates` they do not, because the need is a working export.

**Expand documentation.** Serves how-to needs directly and durably. Applied to the export problem it would document a manual weekly workaround, which serves the customer poorly against this value.

**Canned macros.** Serves the support team's throughput and the sustainability value. The customer receives a faster reply and still re-applies a fix every week, so it improves response time without improving outcome.

**Known-issues banner.** Serves customers by telling them the truth before they spend time diagnosing, particularly the 74% of `export-dates` tickets coming from the two highest-paying plans (E7). It informs without repairing.

## Collision recorded, not resolved

The chatbot and expanded documentation share a target and a dependency: both act on the same 118 how-to tickets, and the chatbot answers from the documentation, so documentation coverage sets the chatbot's ceiling. They remain distinct bets — one writes content, one serves existing content — and Q5 shows they rest on opposite assumptions about why customers ticket, so their identity is not blocked. Under this run's composition authority the collision is recorded and development continued; nothing was merged or dropped. Whether to treat them as one belongs downstream.

## Field-level note for the Recommend and Contest stages

Recorded as a property of the frozen field, without adding to, filtering, or reordering it. The evidence identifies a single cause for 482 of August's 830 tickets, and no option in this field acts on that cause; all four act on the residue, on handling time, or on notification. The largest reachable slice belongs to the banner, and its mechanism is notification rather than repair. This is stated so downstream stages read the surface accurately rather than inferring that the four options span the problem. Adding a candidate is not this stage's authority.

## Bias pass

The chatbot is the user's own candidate, which creates risk in both directions. Checked and corrected: the chatbot receives the charitable reading of its wording in Q2 (a non-vendor route is conceivable before constraint 3 is applied to it) and the assumption in Q5 that favours it is stated as plainly as the ones that do not. The three non-user options are held to the same standard: the macros option is not allowed to look free, since Q1 records that its largest opportunity is already captured and Q4 records its dependence on the defect persisting; the banner's reach figure is paired with an unevidenced mechanism assumption and an unpriced engineering cost; the documentation option's reachable slice is stated numerically rather than left as general usefulness. Effort is uneven by option complexity, not by favour. No claim is made that the result is neutral.

## What can now be compared, and what remains open

The four options are separable on six axes: which slice each reaches and how big it is, which confirmed constraints bite, whether it ends a stream or shortens a touch, whether its value survives the defect being fixed, what it assumes about why customers contact support, and what it delivers against the customer-need-over-deflection value.

Open assumptions and evidence gaps, each with the smallest check that would resolve it:

- Whether a chatbot subscription falls inside or outside the budget freeze, and its price. Check: one question to whoever owns the freeze, plus a vendor quote. This could change the option's basic viability.
- Whether the 118 how-to tickets come from uncovered topics or from covered-but-unfound ones. Check: sample twenty recent how-to tickets against the documentation. This shifts the reachable share for two options in opposite directions.
- What fraction of `export-dates` ticket-openers visit the app before filing. Check: cross-reference session logs against ticket timestamps for a sample. This sets the banner's real reach.
- An engineering estimate for the in-app banner, against the one available engineer-week. Check: ask the engineer.
- Which billing and other replies lack a macro today. Check: the support lead's macro inventory.
- Whether follow-ups cost about as long as an initial macro reply, which the roughly 160-hour figure in Q3 assumes.

No ranking, scoring, or recommendation was performed, and this surface does not claim the option space or the evidence base is complete. If the choice is wanted next, that is `making-recommendations`.
