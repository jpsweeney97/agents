---
name: substitution-ledger
description: "Use the moment you are about to downgrade your own deliverable mid-task — writing `mock`, `stub`, `placeholder`, `simplified`, `for now`, `skipping`, or `TODO` about it, or delivering something that differs from the literal ask because of an obstacle. Logs each downgrade as a ledger row when it happens, then at delivery walks every row: upgrade it or carry it verbatim into the final message. Do not use for user-sanctioned descoping under a constraint (`scope-cut`), to drive review findings to stated outcomes (`apply-findings`), or for test doubles that were always part of the design."
---

# Substitution Ledger

Mid-task, the deliverable degrades quietly: a mock where the ask implied the real API, a hardcoded sample where live data was the point, an edge case "skipped for now" — and the final summary reports the original ask as done. The failure is temporal: at the moment of downgrade you always know you are downgrading, and by summary time that knowledge has evaporated. This skill relocates the recording to the moment of knowledge, so the gap between asked-for and delivered arrives as a decision for the user instead of a surprise in production.

Invocation: `/substitution-ledger` or `$substitution-ledger`; also fires unprompted at its tripwire — you are about to write a downgrade marker about your own deliverable (`instead`, `for now`, `mock`, `stub`, `simulate`, `placeholder`, `simplified`, `skipping`, `TODO`) in code, comments, or your own narration, or to deliver something that differs from the literal ask because of an obstacle. The finite hedge vocabulary is the tripwire precisely so no materiality judgment is needed to fire: if the word is about to leave your hands about your own work, the row gets written.

## 1. Log at the moment of downgrade

Before proceeding, append one row to a session ledger — in the session scratchpad where one exists, otherwise a working note that is not part of the deliverable:

```text
asked-for | delivering instead | reason | what would unblock the real thing
```

Then keep working. The row is a transaction record, not a request for permission — do not stop the task to ask, and do not let the logging talk you out of a downgrade that is genuinely the right call under the obstacle. One row per substitution, written when it happens. Noticing at delivery that a row was never written is late but not optional: write it then — the walk below cannot cover a row that does not exist.

## 2. Walk the ledger at delivery — mandatory

At delivery, walk every row and end each one in exactly one of two states:

- **Upgraded** — try the real thing first: blockers expire (the credential arrived, the endpoint came back, the time pressure passed, the right approach became cheap once the rest was built). A row that upgrades is done for real; note it as upgraded so the user sees the ask was ultimately met.
- **Carried** — still blocked, or still the right trade: the row goes into the final message verbatim, in the table below.

The final message must contain either the table of carried rows or the literal line:

```text
No substitutions: delivered matches asked-for.
```

The line is literal, not paraphrased, and it is a claim — writable only when the walk ran and left no carried rows. A run that wrote rows and does not surface them in the final message has reproduced the exact silent-downgrade failure this skill exists to kill.

```text
Substitutions (asked-for → delivered):
  live FX service call   → hardcoded 1.08 rate  — FX_TOKEN not set            — unblocks: credentials from platform team
  full 10k-row backfill  → first 500 rows       — runtime exceeds the sandbox — unblocks: run as a background job
```

## Boundaries

- Unsanctioned drift only: descoping the user drives, under a named constraint and with re-entry conditions, is `scope-cut`. A downgrade the user directed or approved mid-session is the ask changing, not a substitution — the ledger measures distance from the ask as the user last set it.
- A test double that was always part of the design — a mock in a unit test, a fixture in a harness — is not a substitution; a mock standing where the ask implied the real integration is.
- Disclosure, not verification: the ledger guarantees the delivered thing is honestly described, never that it is correct — proving the work is the job of the verification lanes (`verify`, `closeout-check`, where available). Driving discrete review findings to stated outcomes is `apply-findings`.
