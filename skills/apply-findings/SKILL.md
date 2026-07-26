---
name: apply-findings
description: "Use when a review, critique, or adjudication with discrete findings is in context or pasted and the user says to apply them — `apply the patch`, `apply 1-4`, `do #8 and #12`, `apply all three fixes`, `execute the repairs`. Drives every named finding to an explicit stated outcome with proof, so nothing is silently dropped. Do not use to produce the review itself, to file findings as tracked issues (`triage`), or to commit, merge, push, or land the result (`land`)."
argument-hint: "[which findings: all | 1-4 | #8 #12]"
---

# Apply Findings

A review comes back with N findings and the user says "apply the patch." The failure this skill exists to make impossible is silent attrition: N go in, N−2 fixes come out, and nobody says which two died. Every finding leaves this run with a stated outcome and the evidence behind it.

Invocation: `/apply-findings` or `$apply-findings`, or a plain instruction to apply, patch, or execute a set of findings already in context or pasted.

## Ledger first

Before touching a file, enumerate **every** finding in the source review into a ledger — including the ones the user did not name. "Apply 1–4" over a six-item review produces six rows: four in scope, two marked out of scope. Named and declined beats vanished.

Read the scope, state your reading, and proceed — do not stop to ask. "Apply the fixes" over an adjudicated review means every finding the adjudication upheld; over a raw review it means every finding. Put the reading in the ledger header so the user can correct one line instead of re-deriving your scope.

## Apply

- Work in dependency order, not list order, when fixes touch the same code.
- A finding that does not survive contact with the code is not force-applied. Record what the code actually showed and keep going: disagreement with the review is a ledger outcome, never a reason to stop the run or to ask permission to continue.
- Stay inside the findings. The adjacent cleanup you can see from here goes in a note under the ledger, not in the diff — a review-application turn that quietly becomes a refactor is unreviewable.
- A finding that should become tracked work rather than a fix now is a `skipped` row naming `triage` (where available), not an issue filed mid-run.

## Prove

Each applied fix gets the cheapest check that would catch it being wrong: the targeted test, the linter, the type checker, a re-read of the rendered or parsed output. Fresh evidence, not "should work now." One suite run covering several fixes is fine when they share a blast radius — name which rows it covers. Where no check exists, the evidence cell says so; an unproven fix is reported as unproven, never as done.

## Report

Close with the full ledger, one row per finding:

| # | Finding | Outcome | Evidence |

- **applied** — the change is in the diff, with its proof.
- **no-change-needed** — the required end state already held, or the finding did not survive the code. Evidence says which.
- **skipped** — deliberately not done: outside the stated scope, excluded by the user, or handed to another lane.
- **blocked** — should be done, could not be. Name what would unblock it: the missing access, the ambiguous fix, the decision the user owns.

Every row filled; no finding omitted for being uninteresting. When the host's own review flow supplies a reporting tool or outcome vocabulary — Claude Code's `/code-review` apply pass does — report through it and hold the same discipline: every finding, an explicit outcome, evidence attached.

Under the table, a tally line and anything the applying surfaced that the review missed:

```text
6 findings: 4 applied · 1 no-change-needed · 1 skipped · 0 blocked → next: /land
```

## Stop at the gate

Publication is not this skill's to perform: no merge, no push, no PR, no release, no landing ritual. Report the ledger and name `/land` (where available) as the next move.

The local commit is the one step this skill does not decide. Where the repo's own instructions make a local commit the default after verified work, that contract governs and this skill does not override it; where they do not, leave the tree so the user can read the ledger against it.
