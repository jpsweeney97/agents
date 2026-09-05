---
name: incident-response
description: "Use when production is breaking right now — an unplanned live incident, harm growing, cause possibly unknown — and the job is to stabilize before you understand why: mitigate-first, advisory to a human operator, keeping a timestamped live timeline. Never deploys, shifts traffic, executes a rollback, or pages. Stops at stabilized; hands the unknown-cause hunt to `diagnose` and the retrospective to `postmortem`. Not for a planned risky ship (`deploy-plan`), a cause you must find before acting (`diagnose`), an incident already over (`postmortem`), or authoring a rollback procedure (`runbook-authoring`)."
---

# Incident Response

Production is breaking right now. The one imperative: **stabilize before you understand why.** Invocation: `/incident-response` or `$incident-response`.

Your trained reflex — and your operator's — is to find the cause first. That reflex is `diagnose`'s law and wrong here. Under fire, every minute spent understanding is a minute of harm you could have stopped — and you do not need the cause to stop the bleeding. The standing forcing question everything below answers: **what is the fastest reversible action that shrinks the harm right now?**

## Advisory-not-actor (read this before "act now")

An AI agent usually cannot read prod and must never act on it. You **advise the human operator**; you take no production action — no deploy, traffic shift, rollback execution, or paging. "Reduce harm now" is addressed to the operator *through you*: your speed is in compressing their decision loop, not in touching the system. The live timeline records only what you **observed** or were **told**, never invented telemetry; where blind, label `UNVERIFIED` and name the signal a human must read. This discipline is what keeps `postmortem`'s Beat-1 inputs clean.

## Move 1 — Mitigate first (severity folded in)

**Read severity as you mitigate — one breath, one line, then move:** how bad (blast radius and depth — degraded vs down vs data-loss/integrity), how fast (trend — growing, stable, or contained; trend is the load-bearing dimension, and a growing blast is the strongest pull to act now), and who must be woken now (you recommend; the operator pages). It is a judgment, not a lookup — no SEV ladder, no SEVn definitions (orgs differ). It is **provisional**: any new observed-or-told fact re-reads it as a fresh `DECISION` entry. It tunes exactly two things: how hard you mitigate and how loud comms gets. At the worst end the read and "mitigate now" collapse into one instant — fine; mitigate-first is the spine, severity only sets the intensity.

**The mitigate forcing question:** *what is the fastest action that shrinks the harm, even without knowing the cause?* A mitigation that works without a diagnosis is a success, not a shortcut. Common shapes — prompts to think, not a checklist: undo the most recent change (rollback — Move 2); turn off the failing path (kill the flag, disable the endpoint, drain the bad node); shed or redirect load (rate-limit, fail over, serve degraded); contain the blast radius (isolate the affected tenant, region, or dataset).

**Reversibility gate before advising any mitigation:** *if this is wrong, can it be cleanly undone?* A mitigation that can itself harm prod (a rollback past a point of no return, a failover that loses in-flight data) is a judgment, not a reflex — characterize its reversibility in `runbook-authoring`'s graded vocabulary (Move 2) before advising it.

**Default and exits.** Harm growing + a reversible mitigation exists → advise it now, hand the still-unknown cause to `diagnose` afterward. Hold-and-investigate is correct only when every candidate mitigation is itself irreversible and could deepen the blast, or the blast is already contained and not growing (then there may be no fire and you may be in the wrong skill). When no safe mitigation is obvious, probe **only enough to find a lever** — and the line is explicit: a mitigation-probe asks *"what can I turn off, drain, or contain?"*, never *"why is it failing?"* The moment your question turns to *why*, you have crossed into `diagnose` — stop and route there.

## Move 2 — Rollback vs forward (the sharpest call)

The most common mitigation is "undo the recent change," and the hard call is rollback or fix-forward. Make it as a judgment, in `runbook-authoring`'s **graded / multi-PONR vocabulary by reference**: is there a clean rollback? a lossy-but-available recovery, at what named cost? or are you past a point of no return where forward is the only path? Name each point of no return; never assume there is one. Cause-unknown — the common entry state — argues for rollback: rollback tolerates an unknown cause, fix-forward needs it.

Rollback is not automatically safe. You may be in this skill precisely because a planned rollback already harmed prod; when you arrived that way you are mid-decision — log the harmful rollback as a fresh blast-radius input and **re-run this call** (it is now discredited and likely past its safe PONR). The forks compose; there is no separate "we made it worse" branch. If a rollback runbook exists, **follow it advisory-to-the-operator, step by step — never re-author it under fire**. If none exists, do not stop to write one now; that absence is an input pushing toward forward-fix or escalation, and a `postmortem` action-item to note. Record the call as a `DECISION` entry carrying the PONR map and a one-line reason.

## Move 3 — The live timeline (kept as you go, subordinate)

You are the scribe while the operator firefights: if you do not log, no one does — so record **continuously**. But the record never outranks mitigation: **do not stop the bleeding to perfect it.** The timeline is a raw running jot, not a reconciled record; `postmortem` reconciles it. The format below is deliberately cheap, so "record continuously" and "don't stop to perfect it" stop contradicting each other.

## Move 4 — Comms cadence (thin, advisory)

Cadence **scales with the severity read** (its second consumer): the worse and faster-moving, the tighter the fixed interval, plus an update at every state change; a contained, non-growing incident gets status-channel updates only. Each update is coarse — current impact, what is being done, when the next update lands — and is **drawn from the live timeline**, so comms never broadcasts a fact the timeline does not hold and never states a cause that is `UNVERIFIED`. You draft; the operator sends. **Draft, do not wordsmith** — if you are perfecting the status post while harm grows, stop and mitigate.

## The live-timeline format

Append-only, one line per event, newest at the bottom, written as events happen and never back-edited. This is the artifact `postmortem` consumes as Beat-1 raw facts.

```
## Incident <slug> — live timeline — opened HH:MM:SS TZ
Severity: <one-line read> (as of HH:MM:SS TZ)  |  State: BURNING | MITIGATING | STABILIZED  |  Operator: <role/name>

- HH:MM:SS TZ  TAG: text
```

Five tags — the proof-law made mechanical, collapsed to what is writable one-handed under fire:

- `OBSERVED` — you read it yourself, in-band: your own command/CI output, a log line pasted into the channel, a file you opened.
- `TOLD` — a human or source reported it. **This is the default** for all operator-relayed prod telemetry (dashboards, metrics, alerts you cannot read).
- `UNVERIFIED` — claimed-but-unconfirmed, or you are blind; name the exact signal a human must read.
- `DECISION` — a hard call (the severity read, mitigate-vs-investigate, rollback-vs-forward, declared-stabilized) with the inputs that drove it.
- `ADVISED` — what you recommended. **There is no action-taken tag** — the agent never acts, so the vocabulary cannot express it.

Firm rules (each is load-bearing and costs ~nothing under fire): one line per event, append-only, never back-edited; an absolute timestamp + timezone on every line; a provenance tag on every fact line by **one default rule, not per-line adjudication** — *write `TOLD` unless you literally read it yourself (then `OBSERVED`); a number you cannot read is `UNVERIFIED`*; **facts only, no causes** ("checkout returning 5xx" is a fact; "…because the migration ran" is a cause — causes are `postmortem` Beat-2). Attribution (who/where) is natural content of a `TOLD` line when you have it, not a gated token; stitching each `ADVISED` to its outcome is reconciliation `postmortem` owns, not bookkeeping you do while prod burns. The provoked part is *what is worth recording* — state changes, decisions, what you observed or were told; do not narrate keystrokes.

```
## Incident checkout-5xx — live timeline — opened 14:02:00 UTC
Severity: revenue path down, all-region, climbing — recommend waking system owner (as of 14:03:05 UTC)  |  State: MITIGATING  |  Operator: on-call-web

- 14:02:10 UTC  TOLD: checkout 5xx ~100% all regions (on-call, status dashboard — I can't read it)
- 14:03:05 UTC  DECISION: severity — down, all-region, climbing → mitigate now; recommend waking system owner
- 14:03:40 UTC  ADVISED: roll back deploy abc123 via docs/runbooks/web-rollback.md; PONR = schema-migrate step 3, not yet crossed
- 14:05:50 UTC  TOLD: rollback started (operator)
- 14:08:12 UTC  OBSERVED: 5xx log sample pasted in channel — rate 0.12 and falling
- 14:11:30 UTC  UNVERIFIED: suspect DB pool exhaustion — can't read prod; a human must check pool-saturation metrics
- 14:14:00 UTC  DECISION: declared STABILIZED — trend flat, 5xx <1% (told), holding; cause unknown → diagnose; timeline → postmortem Beat-1
```

## Stop at stabilized — the hard fence, guarded both directions

**Stabilized** = an observed-or-told signal that harm has stopped growing and the system sits in a state the operator accepts as holding — even if degraded, on a workaround, or running forward-only. Stabilized is **not** fixed and **not** cause-found. That is the exit, not a failure.

The diagnose-first pull attacks both ends:

- **Quit early** — the mitigation *looked* like it worked but the signal is still climbing. Re-read what you actually observed-or-were-told before you call it; a hoped-for recovery is not a confirmed one.
- **Overrun** — you are stabilized and you keep going (hunting cause, drafting the writeup, hardening the system). Stop. That work is real but it is not this skill's, and doing it here means doing it badly under adrenaline.

At stabilized the skill **stops**: it does not hunt cause, retrospect, or author a runbook, and at no point takes a production action or pages. Record "declared STABILIZED" as the final `DECISION` entry, then hand off.

## Hand-offs / seams

- **Entry.** Prod is burning. Sometimes arrives via `deploy-plan`'s abort path — a planned rollback that harmed prod; handle it by re-running the rollback-vs-forward call (Move 2), no special branch.
- **Cause still unknown at stabilized → `diagnose`.** Hand over the live timeline plus the mitigated-but-fragile state as the starting symptom; now that prod is not burning, cause-first is correct again.
- **The retrospective → `postmortem`.** The live timeline *is* postmortem's Beat-1 raw facts — already timestamped, observed-or-told, `UNVERIFIED`-labeled, and cause-free; it reconciles there, not during the fire. For a code bug with unknown cause, `diagnose` runs first, then `postmortem`; a non-code incident can go straight to `postmortem`.

## Fences

- Cause-first investigation → `diagnose`; this skill exits into it at stabilized.
- The retrospective, after the fire → `postmortem`; the live timeline is its Beat-1 input.
- Authoring a procedure → `runbook-authoring`; under fire, follow the existing runbook (Move 2), never re-author it.
- A planned ship's gauge and bake-read → `deploy-plan`; a planned abort that harms prod enters here.

## Done when

- Harm has stopped growing and the operator accepts the state as holding; "declared STABILIZED" is the final `DECISION` entry.
- A live timeline exists — timestamped, provenance-tagged by the default rule, causes excluded, advised-not-acted — ready to hand to `postmortem` as Beat-1.
- The unknown cause (if any) is routed to `diagnose`, and the retrospective to `postmortem`; no production action was taken and no cause was asserted over a signal you could not read.
