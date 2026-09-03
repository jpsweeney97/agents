# Evidence the user supplied for the support-queue decision

Nine excerpts.

## E1. Ticket taxonomy (support lead's tagging)

| Tag | April (410 tickets) | August (830 tickets) |
| --- | --- | --- |
| `export-dates`: the customer's downstream spreadsheet or import broke because the scheduled export's date column changed | 0 | 482 |
| How-to questions | 140 | 118 |
| Billing | 90 | 96 |
| Other, including product bugs | 180 | 134 |

The `export-dates` tickets report that the export's date column changed from the form `2026-08-01` to `08/01/2026 00:00`, which their importing systems reject or misread.

## E2. Bug tracker, issue #2291 (opened 2026-05-09)

"Export date format changed unintentionally by the CSV library upgrade in release 5.12 (May 6). The documented format in the API and export schema is ISO 8601 (`YYYY-MM-DD`). Fix: pin the formatter to the documented format; add a per-account toggle for any customer who has since adapted to the accidental format. Estimate: two days including tests." Status: backlog, priority medium.

## E3. Legal note (July)

"The May format change was made without the ninety days' notice the terms of service require, so the company is currently out of compliance with its own terms. Restoring the documented format is a correction to the promised format, not a change to it, and needs no notice. The three customers who have told us they adapted to the new format should be informed; a per-account toggle covers them."

## E4. Support handling statistics (August)

The `export-dates` macro was applied to 470 tickets. Median handling time with the macro: six minutes. Each such ticket generates a median of 2.3 follow-ups, because the scheduled export re-runs weekly and the customer's fix has to be re-applied each week.

## E5. Help-center analytics and chatbot pilot

Documentation covers about 85% of how-to questions. A chatbot vendor's pilot on comparable content deflected 20 to 30% of how-to tickets; applied to Brightline's 118 how-to tickets that is at most about 35 tickets a month.

## E6. Customer growth

780 accounts in April, 900 in August. The rate of non-`export-dates` tickets per account is flat at about 0.4 a month.

## E7. Product analytics

Scheduled exports are used by 610 of 900 accounts. 74% of `export-dates` tickets come from accounts on the two highest-paying plans.

## E8. Other estimates on file

- Community forum: four to six months to become self-sustaining, per the vendor's own guidance.
- Office hours: twelve attendees per session over the last four sessions.
- Auto-close: in a June trial, 61% of auto-closed threads were reopened by the customer within a week.
- Outsourced first-line vendor: $6,000 a month; the vendor's scope excludes product changes.

## E9. Status

No outage in the period. The status page has been live since 2024.
