---
name: recheck-investment
description: "Use when work is entering a third or later hardening or scrutiny pass over the same work product and value bargain, has hit a declared review cap, or the next repair would add a new subsystem, trust boundary, schema, or persistent proof surface — or when asked directly whether continued hardening is still worth it: reconstruct the original value-for-cost bargain and gate further investment on it. Do not use for first-pass overbuild critique of technical drafts (`working-slice-review`), first-pass value questions (`making-recommendations`), correctness review, constraint-driven scope cutting (`scope-cut`), or post-launch outcome measurement (`outcome-check`)."
---

# Recheck Investment

Reprice work before another hardening pass: interrupt a correctness-hardening ratchet when the original value-for-cost bargain may have changed. A finding can be valid while another repair is no longer worth authorizing — the review lane that produced a finding owns whether it is real; this skill owns only whether changed circumstances require renewed human authorization to keep going. Invocation: `/recheck-investment` or `$recheck-investment`.

Open every run with one visible setup line: the target artifact, the cue that fired, where the original bargain is recorded, and that mutation stays paused while the check runs.

## Trigger Cues

Counts, caps, and size are prompts to run the check, never themselves evidence of drift. Cues:

- a third or later hardening or scrutiny pass over the same work product and value bargain, observable from the artifact's own revision history rather than session memory
- a declared review or iteration cap is reached while material findings remain
- the next repair would add a new subsystem, trust boundary, schema, fixture suite, persistent record, or platform-like execution surface
- findings now mainly police machinery earlier repairs added, rather than the original problem
- hypothetical reuse is carrying the value case
- a direct "is this still worth it?" question

Run only where a human reads the invocation. In a context where no human reads the invocation at call time — cron, remote triggers, unattended automated loops, subagent dispatches — surface the trigger and evidence to a human-visible caller rather than invoking this skill. A loop running in the human-visible main session may invoke it normally.

## Boundaries

- First-pass overbuild critique of a technical design, spec, plan, or architecture draft before a working slice exists is `working-slice-review`'s job, and first-pass value questions — should this be built at all? — belong to the deciding lanes (`making-recommendations`, or `outcome-shaping` where available). This skill starts from an already-struck bargain.
- Finding validity stays with the review lane that produced the finding; a pause here never invalidates a correct finding.
- `agent-facing-design` keeps per-edit context-vs-machinery and design-size judgment; when its whole-surface question surfaces a possibly-changed bargain, the continued-investment decision lands here.
- Constraint-driven partitioning of an agreed scope is `scope-cut`; post-launch goal measurement is `outcome-check`.
- Read-only: never cancel, retire, recharter, edit, commit, land, or publish anything, and never design the replacement system inside the check.
- Never score complexity numerically or enforce universal line, revision, test, or budget caps; thresholds prompt the check, judgment decides it. Never create a persistent investment ledger.

## Procedure

1. Recover the original bargain: promised outcome, consumer or decision owner, the decision it governs, one-off or recurring frequency, harm if wrong, expected assurance, expected cost, and the original done condition. Mark inferred premises as inferences.
2. Describe the changed reality: remaining implementation and verification work, recurring maintenance and cognitive cost, newly introduced artifacts and trust boundaries, new failure modes caused by earlier repairs, unresolved uncertainty, and opportunity cost. Separate sunk cost from future cost; sunk work is never evidence that continuing is valuable.
3. Test for material drift: has the work changed category; does expected value still earn the remaining cost; does the next repair reduce risk in the original outcome or mainly protect machinery earlier repairs added; does claimed reuse have a real owner and credible recurring use?
4. Shape the serious directions — continue, simplify assurance, check one missing fact first, recharter as separately-owned tooling, or retire preserving evidence — and compare them with `making-recommendations`' standards: comparative language, no numeric scoring, the strongest case against, and check-first as a first-class answer.
5. Gate. No material drift: say so in a sentence or two and return control immediately — no packet, no question. Material drift: emit the packet below, keep mutation paused, ask exactly one direction-setting question (for check-first, that question is authorization to run the named check), and stop for the human ruling.

## Rulings

This skill never persists, searches for, or infers a ruling. It may honor an explicit prior ruling only when that ruling is already present in its current reading context — an authorization note in the artifact it is reading qualifies; hunting through decision records or inferring intent from history does not. An in-scope prior ruling is quoted and control returns immediately; work past the ruling's named boundary gets a fresh check.

The human supplies the ruling. The caller may record it only through a mutation surface it already owns, and durable decision-record capture (`decision-record`, where available) is an explicit follow-up — never automatic.

## Output Packet

- **Original bargain:** promised outcome, consumer, frequency, stakes, assurance premise, expected cost.
- **What changed:** the material category, value, assurance, or ownership drift.
- **Remaining investment:** future and recurring costs only.
- **Recommendation:** one direction.
- **Strongest countercase:** the best argument against it, and the fact most likely to change the call.
- **Proposed boundary:** an observable line — a named pass, repair class, subsystem, or artifact state — that a later reader can compare without inventing intent.
- **Caller state:** `may resume` or `paused for human ruling`.

If paused, exactly one decision question follows the packet.

## Proof Boundary

The output is a qualitative recommendation from inspected evidence. It computes no return-on-investment number and certifies nothing as overbuilt; missing facts and estimates stay visible in the packet. If one cheap fact could change the recommendation, prefer check-first over deciding on the estimate.
