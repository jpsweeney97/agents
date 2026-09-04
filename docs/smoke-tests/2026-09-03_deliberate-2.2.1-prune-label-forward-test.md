# 2026-09-03 — `decide:deliberate` 2.2.1: Prune label forward test (issue #21)

Behavior evidence for the one sentence decide 2.2.1 adds to the Prune method of `plugins/decide/skills/deliberate/SKILL.md`, which defines the second label on a cut record. The defect (GitHub issue jpsweeney97/agents#21): in the T2 known-answer check, case 06's Prune record for "Restore the previous export date format" carried `Cut: constraint, fact-established` while its own Reason said the deciding question was "a legal reading I cannot make here"; the evidence later established the opposite reading and the cut option was the run's winner (`docs/plans/2026-09-03-t2-known-answer-check/case-06/02-prune.md`). The label matters because the close delivers the cut ledger as a table of option, cut, and revive-if, so the label is the only evidence-status signal that reaches the user.

Method: five headless runs, `claude -p --model opus --allowed-tools ""`, prompt piped on stdin, run from the session scratchpad so no repo instructions load, one fresh session per run. Each prompt is the same fixed preamble ("You are the Prune stage of a `deliberate` run ... print the full contents of `02-prune.md` as your entire reply"), then the Prune section of `SKILL.md` verbatim for that arm, then case 06's `case.md` (setup and field; no evidence file, no lean), which is the recorded run's Prune view. The arms differ only in the one sentence on the line that introduces the cut record. The recorded run of 2026-09-03 on the 2.2.0 text is a sixth data point.

The sentence was written twice. The first form did not change the label in two runs; the landed form keys on the record's own `Revive if` line, which is where both first-form runs had disclosed the reading.

First form (not landed):

> Label a cut `fact-established` only when its stated reason settles it without interpretation; a cut that rests on a reading you made, or on one you say you cannot make, is `judgment call`.

Landed form (2.2.1):

> Label a cut `fact-established` only when its stated reason settles it without interpretation and only a changed constraint or a new fact could revive it; when your `Revive if` names a different reading of the same facts, including one you say you cannot make, the cut is `judgment call`.

## Result

| Run | Prune text | Label on the export-format cut | Where the record discloses a reading of constraint 2 | Label consistent with the rule under test |
| --- | --- | --- | --- | --- |
| recorded run (`case-06/02-prune.md`) | 2.2.0 | constraint, fact-established | Reason: "a legal reading I cannot make here"; Revive if (1): counsel reads reverting as honoring the promised format | no rule in 2.2.0; the defect |
| old-1 | 2.2.0 text (main) | constraint, fact-established | Revive if: "the ninety days' notice is sent now, so the revert lands at the start of next quarter; or counsel reads a return to the format customers were on before as not a new change requiring notice; or the affected customers ask for the old format back and waive the notice." | no rule in 2.2.0 |
| v1-1 | first sentence (not landed) | constraint, fact-established | Revive if: "Legal reads a return to the pre-May format as restoring the contracted format rather than changing it; or the company gives notice now, accepts the revert landing next quarter, and picks something else to carry this quarter." | no: the reading is disclosed and the label is still fact-established |
| v1-2 | first sentence (not landed) | constraint, fact-established | Revive if: "Counsel confirms that returning to a format customers previously received is not a "change" under the terms; or the ninety-day notice is issued now, accepting that relief arrives next quarter; or the surge is traced to this field, in which case the interim answer is a documented workaround, which the surviving banner, documentation and macros can all carry." | no: the reading is disclosed and the label is still fact-established |
| v2-1 | landed sentence (2.2.1) | constraint, fact-established | Revive if: "the ninety-day notice is sent now, which makes the restore a next-quarter action worth scheduling alongside something for this quarter; or the ticket text is measured and the export date format is confirmed as the dominant driver, which changes what the company is willing to pay to start the notice today." | yes: no reading is disclosed anywhere in the record, so fact-established matches what the record says |
| v2-2 | landed sentence (2.2.1) | constraint, judgment call | Revive if: "The clause is read as governing only changes away from the format customers were promised, so that restoring the pre-May format is not a change it covers; or notice is issued now and the change is scheduled ninety days out; or the ticket data shows the extra volume is about the date format, which would make the notice period worth starting today." | yes: the reading is in Revive if and the label is judgment call |

Every run kept the same four survivors as the recorded run (the chatbot, expanded documentation, canned macros, the known-issues banner) and cut the export-format option on constraint 2; the sentence changes the label, not the cut. In every run the outsourcing cut stayed `constraint, fact-established` with a Revive if naming a changed constraint (the budget freeze lifts), which is the discrimination the rule is for.

## The export-format record in each run

### old-1 (2.2.0 text (main))

```text
Option:         Restore the previous export date format — Change the date column in customers'
                scheduled exports back to the format it had before the May release.
Cut:            constraint, fact-established
Reason:         Constraint 2 is a terms-of-service promise of ninety days' notice before any change
                to the format of the data customers receive, and its confirmed cost is that format
                changes to exports and API responses are out this quarter. Changing the date column
                in scheduled exports back is a change to the format of the data customers receive,
                so it carries the same ninety-day notice as any other. It cannot land inside the
                quarter this decision covers.
Strongest case: The timing fits the problem better than anything else in the field. Tickets went
                from about 410 a month in April to about 830 in August while customers grew only 15
                percent, and the format changed in the May release. If that one field is the cause,
                this is the only option that removes the cause rather than handling what the cause
                produces. It touches one field in one feature, needs almost no engineering time,
                changes nothing about how support works, and keeps the product simple.
Revive if:      the ninety days' notice is sent now, so the revert lands at the start of next
                quarter; or counsel reads a return to the format customers were on before as not a
                new change requiring notice; or the affected customers ask for the old format back
                and waive the notice.
```

### v1-1 (first sentence (not landed))

```text
Option:         Restore the previous export date format — Change the date column in customers'
                scheduled exports back to the format it had before the May release.
Cut:            constraint, fact-established
Reason:         Constraint 2 puts format changes to exports out this quarter without ninety days'
                notice. This option is a change to the date column in customers' scheduled exports,
                which is exactly what the constraint's stated cost names.
Strongest case: Tickets nearly doubled while the customer count grew fifteen percent, so the extra
                volume is coming from existing accounts, and a format change in the May release is
                the one named candidate cause in the whole case. Removing a cause beats answering its
                symptoms, and this is a one-field change that keeps the product simple and costs the
                support team nothing.
Revive if:      Legal reads a return to the pre-May format as restoring the contracted format rather
                than changing it; or the company gives notice now, accepts the revert landing next
                quarter, and picks something else to carry this quarter.
```

### v1-2 (first sentence (not landed))

```text
Option:         Restore the previous export date format — Change the date column in customers' scheduled exports back to the format it had before the May release.
Cut:            constraint, fact-established
Reason:         Constraint 2. The terms promise ninety days' notice before any change to the format of the data customers receive, and the user's own cost line puts format changes to exports and API responses out this quarter. Customers currently receive the post-May format; restoring the earlier one changes the format they receive, with no notice given. Barred this quarter regardless of merit.
Strongest case: It is the only option in the field that names a possible cause of the surge rather than a way to absorb it — a May release changed this field, and tickets roughly doubled from April to August. If the date column is what customers are writing in about, one field fixes the volume at its source, and nothing else here does that.
Revive if:      Counsel confirms that returning to a format customers previously received is not a "change" under the terms; or the ninety-day notice is issued now, accepting that relief arrives next quarter; or the surge is traced to this field, in which case the interim answer is a documented workaround, which the surviving banner, documentation and macros can all carry.
```

### v2-1 (landed sentence (2.2.1))

```text
Option:         Restore the previous export date format — Change the date column in
                customers' scheduled exports back to the format it had before the May
                release.
Cut:            constraint, fact-established
Reason:         Constraint 2 requires ninety days' notice before any change to the format of
                data customers receive, and the confirmed cost of that constraint is stated
                directly: format changes to exports and API responses are out this quarter.
                The date column in scheduled exports is data customers receive, and changing
                it back is a change to its format. This disposes of the option for this
                quarter without reading the ticket data or weighing the values.
Strongest case: This is the only option in the field that would remove a cause instead of
                absorbing its effects, and the timing points straight at it: the May release
                changed this field, tickets went from about 410 in April to about 830 in
                August, and the customer count grew only fifteen percent. If the surge is the
                date format, every other option is a way of answering the same question
                faster.
Revive if:      the ninety-day notice is sent now, which makes the restore a next-quarter
                action worth scheduling alongside something for this quarter; or the ticket
                text is measured and the export date format is confirmed as the dominant
                driver, which changes what the company is willing to pay to start the notice
                today.
```

### v2-2 (landed sentence (2.2.1))

```text
Option:         Restore the previous export date format — Change the date column in customers' scheduled exports
                back to the format it had before the May release.
Cut:            constraint, judgment call
Reason:         Constraint 2. The terms of service require ninety days' notice before any change to the format of
                the data customers receive, and the user confirmed the cost as format changes to exports and API
                responses being out this quarter. Changing the date column back is a change to the format of a
                scheduled export, so it cannot ship this quarter under the constraint as confirmed.
Strongest case: This is the only candidate that would remove a cause rather than handle the effects, and the
                timing fits it. The format changed in the May release; tickets went from about 410 in April to
                about 830 in August while the customer count grew only fifteen percent, so the rise is per account,
                not from new customers. If a large share of those tickets are people asking why their date column
                changed, every other option in this field answers those people instead of fixing what they are
                asking about. It is also the smallest change in the field — one column in one feature — and it
                fits inside the engineer-week.
Revive if:      The clause is read as governing only changes away from the format customers were promised, so that
                restoring the pre-May format is not a change it covers; or notice is issued now and the change is
                scheduled ninety days out; or the ticket data shows the extra volume is about the date format,
                which would make the notice period worth starting today.
```

## Reading

The landed sentence fixes the defect the issue names: a record that discloses a reading of the constraint no longer carries `fact-established`. It does not make Prune see a reading it does not see: run v2-1 read constraint 2's cost line as settling the cut and disclosed no alternative reading, so its `fact-established` is honest to its own record and still wrong on evidence Prune never receives. That residue is the T2 question (whether a sketch-depth Prune cuts winners), not the label question, and is out of scope here.

## Limits

One case, one model (Opus), two runs per landed arm; no variance beyond that is measured. The runs printed `02-prune.md` to stdout instead of writing a file, and were not dispatched by an orchestrator, so they test the Prune method text, not the dispatch. The prompts and full outputs lived in the session scratchpad and are not kept; the records above are copied verbatim from them.
