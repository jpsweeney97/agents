# 00-setup — deliberate run on the doubled support queue

Run 2026-09-03. Runtime: Claude Code; each stage dispatched as a fresh agent via the Agent tool with `model: opus`.

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

## Evidence stages may read

- `evidence.md` in this run directory: nine excerpts the user supplied (ticket taxonomy, bug tracker, legal note, support handling statistics, help-center analytics and chatbot pilot, customer growth, product analytics, other estimates on file, status).

Research: not allowed (the default; the user did not authorize it).

## Survivor count

About four.

## Model

Opus: `model: opus` on every stage dispatch, the decide 2.1.0 default. The user named no model.

## User's visible lean

None stated. The user supplied one candidate (the chatbot) and stated no preference among options. The candidate is marked as theirs to every stage; no stage receives a lean.
