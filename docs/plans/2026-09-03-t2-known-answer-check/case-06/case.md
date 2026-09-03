# Decision case: the doubled support queue

## Decision question

How should Brightline, a twelve-person software company, reduce its support ticket volume, which has doubled in four months while its customer count grew fifteen percent, before its two-person support team burns out?

## Background, as the user stated it

A business-to-business software product with about 900 customer accounts. Tickets rose from about 410 a month in April to about 830 in August. Two people handle support. First-response time has slipped from four hours to nineteen. One engineer can be spared for a short time.

## User's candidates (marked as theirs, quoted exactly)

- **Add a chatbot to the help center** — "Put an AI assistant on the help site to answer common questions before customers open a ticket." (user's)

## Hard constraints the user confirmed, with what each costs

1. No new hires and no outsourced staff this quarter; there is a budget freeze. What it costs: a third support person, contractors, and support vendors are out.
2. The terms of service promise customers ninety days' notice before any change to the format of the data they receive; the company cannot make a format change without that notice. What it costs: format changes to exports and API responses are out this quarter.
3. Engineering can spare one engineer for one week. What it costs: product rebuilds and new subsystems are out.

## Values the user stated

- Customers getting what they need matters more than deflecting tickets.
- The support team's sustainability.
- Keep the product simple.

## Survivor count

About four.

---

# Field

Grouped by what each option changes: what customers can find for themselves, how support handles tickets, the product, and who gets to ask. Order within a group is not a quality order.

## Help customers help themselves

**Add a chatbot to the help center** (user's) — "Put an AI assistant on the help site to answer common questions before customers open a ticket."
Sets it apart: answers around the clock without a person; a vendor product on top of the existing docs.

**Expand the help documentation** — Write articles for the questions that come up most.
Sets it apart: the cheapest self-serve change; helps only where a question has a written answer.

**Add in-app guided tours** — Build walkthroughs inside the product for its main workflows.
Sets it apart: meets users where the confusion happens; a product change rather than a docs change.

**Add a self-serve status page** — Publish a live page showing the product's operational state.
Sets it apart: answers "is it down?" without a ticket; irrelevant if the tickets are not about outages.

**Run weekly office-hours webinars** — Hold a live session each week where customers bring questions.
Sets it apart: a human answer without a ticket; scales to whoever shows up.

**Start a community forum** — Open a forum where customers answer one another.
Sets it apart: support that grows with the customer base; slow to take hold.

## Change how support works

**Build canned macros for the most common replies** — Write templated answers so each common ticket takes a minute.
Sets it apart: cuts handling time per ticket, not the number of tickets.

**Introduce tiered support with response targets by plan** — Give paying tiers defined response times and answer the rest as capacity allows.
Sets it apart: rations attention by value; changes who waits, not how many ask.

**Auto-close tickets after three days without a customer reply** — Close stale threads automatically.
Sets it apart: shrinks the open queue mechanically; the underlying question may remain.

**Show a known-issues banner in the app** — Display a notice inside the product listing current known problems and workarounds.
Sets it apart: reaches every customer at the moment they would ask; one message for everyone.

## Change the product

**Restore the previous export date format** — Change the date column in customers' scheduled exports back to the format it had before the May release.
Sets it apart: a one-field change to one feature; touches nothing about how support works.

## Change who gets to ask

**Require a documentation search before a ticket can be submitted** — Make the ticket form show matching articles and ask the customer to confirm none answers the question.
Sets it apart: a gate in front of the queue; adds friction for every customer.

**Rate-limit ticket submissions per account** — Cap how many tickets an account can open in a week.
Sets it apart: bounds the load from the noisiest accounts; a customer with a real problem hits the cap too.

**Raise prices to shed low-value accounts** — Increase prices on the lowest tier so the accounts that cost most to support leave.
Sets it apart: shrinks the customer base to fit the team; revenue may fall.

**Outsource first-line support to a vendor** — Contract a support company to handle first responses.
Sets it apart: adds people without hiring; the vendor knows less about the product than the team does.
