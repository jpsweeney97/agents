---
name: postmortem
description: "Use when an incident is over and you need a durable, dated, blameless retrospective — any incident, including non-code ones (outage, data loss, security or process breach) — saved at `docs/postmortems/` with owned, dated action items filed one-per-finding to `/triage` (or `$triage`). Build an agreed, timestamped factual record before any cause or fix. Not for active firefighting, nor the unknown-cause hunt `diagnose` owns first, nor architecture or tech-debt review of a healthy system."
---

# Postmortem

Nail an agreed, timestamped factual record — what happened, when, and what it cost — before any cause, fix, or judgment is written, so every later claim must trace back to a recorded fact and blame has nowhere to hide. Blamelessness is not a banner recited up top; it is what the fact-before-cause wall produces.

This skill provokes the thinking a good retrospective needs; it is not a fill-in template. Every move below is done only when its forcing question is genuinely answered — a heading filled to look complete with its question unanswered is a failed postmortem. Invocation: `/postmortem` or `$postmortem`.

## The lens

Three plain distinctions the whole skill turns on:

- **Fact** — something a log or camera could show ("14:03 UTC the migration ran without the `--safe` flag").
- **Cause** — an interpretation of why ("the flag was easy to omit — the runbook didn't mention it").
- **Blame** — a cause that terminates at a person's character or intent ("Jane was careless"). Always out.

Beat 1 admits only facts; Beat 2 admits causes that cite facts; blame never enters. This is what makes the doc blameless by construction.

## Opening frame

Two gates before you start:

- **Is the incident over and stabilized?** If it is still burning, this is the wrong moment — that is firefighting, or `/diagnose` for an unknown cause. Return after.
- **What kind of incident** — code, ops outage, data, security, process, or mixed? Set vocabulary from that; do not assume code (do not presume logs, commits, tests, or a repo). The blameless test throughout: given the information available at the time, were the actions taken reasonable?

## Beat 1 — Build the record (facts only)

- **Timeline** in absolute timestamps with timezone: detection, key state changes, escalation, mitigations, resolution.
- **Impact**, quantified — duration, scope, count, money or data where known; for a breach, the exposure window. Measured, not adjectival.
- **Smuggling check:** re-read each line. If it contains "because / forgot / should have / failed to," you have smuggled in a cause or blame — move it to Beat 2 or strike it.
- **Disputed / Unknown list**, required. Naming what you cannot yet establish is the work; a record with zero unknowns is a red flag, not a gold star.
- **Reconcile before analysis.** Write no analysis until the record is reconciled: with people in the loop, would everyone present agree this is what happened?; solo or agent-run, reconcile against every available source and resolve each contradiction or move it to Disputed/Unknown. The rule is directional, not a phase prison — if Beat 2 surfaces a new fact, return it to the record and re-reconcile.

Bad looks like: the cause already woven into the timeline; impact as a vibe ("major outage") instead of measured ("checkout down 43 min, ~2,100 orders affected").

## Beat 2 — Analysis (only now; every claim cites a recorded fact)

- **Necessary cause(s) vs amplifiers.** Name the cause(s) without which there is no incident — there may be more than one independent necessary cause; do not force a single root onto a multi-cause incident — held apart from what merely deepened or lengthened it. Each must cite a timestamp from the record; a cause you cannot trace to a recorded fact is a story — strike it. Then push under it: separate what fired (proximate) from the latent condition that made the system fireable.
  Bad looks like: a person as the cause; "the root cause was human error"; an amplifier promoted to a cause.
- **Designed-vs-lucky save audit.** For each thing that kept this from being worse, ask: designed, or lucky? The test — would this save have fired with the responsible humans on vacation, the dashboard unwatched, and the timing hostile? A save that depended on someone happening to look, or on benign timing, is luck wearing the disguise of safety. Name the specific luck ("traffic was at a trough"), not "we got lucky"; a near-miss is a fact about how close the boundary ran — record it. If the saves were genuinely by design, say so and cite the facts that show it: a hardened incident with no meaningful luck is a real, good outcome.
  Bad looks like: "nothing, we were careful" with no reason given; a hollow "lucky the team responded fast" that names no latent risk.
- **Action items.** Owned and dated. Each kills a necessary cause or amplifier, or hardens a lucky save; an item that traces to nothing is decoration. Owner and due date are mandatory parts of the thought — unowned or undated is not finished thinking. When no individuals are in scope (a solo or agent-run retrospective), name the responsible role rather than a person — a role plus a real date is the honest maximum. Tag each as prevention / detection / mitigation. Every finding gets either an action or an explicit "accepted risk, no action, because…".
  Bad looks like: "improve monitoring" (unowned, undated, untraceable); a named cause with neither an action nor an accepted-risk note.

## Beat 3 — Land and route

- Save to `docs/postmortems/YYYY-MM-DD-<slug>.md`, dated by the incident date so the corpus reads chronologically (authoring date only if the incident date is unknown). Create the parent dir if missing; defer to a postmortem location set in the project's `AGENTS.md` or `CLAUDE.md` if one exists.
- Before writing, if the project is a git repository, run `git status`; if the path or its parent carries unrelated dirty state, surface that instead of writing over it. Leave the artifact uncommitted for the user to review — do not stage or commit it as part of the retrospective.
- When an action item is an operational procedure someone will re-run — a rollback, restart, failover, alert response — hand authoring it to `/runbook-authoring` (or `$runbook-authoring`) rather than leaving the procedure inline in the doc.
- File the owned, dated action items to `/triage` (or `$triage`), one issue per finding, and stop. The doc stays the durable record; triage makes the actions trackable.
- Report the artifact path, the filed issues, and the proof boundary: a written postmortem proves the record and analysis exist, not that any fix has shipped.

## Defaults

- Scope is any incident — outage, data loss, security event, or non-code process breach. Use incident-neutral vocabulary (guardrail, save, blast radius, near-miss, exposure window).
- Blameless by construction: facts name actions and systems, not intent; if a person must appear, name the role and the observable action ("the on-call ran X"), never the failing or the character.
- One incident per file; multiple incidents → one file each, or ask.
- Do not fabricate the narrative. Missing facts are flagged as gaps, not invented — a postmortem with holes beats a tidy fiction.
- No status machine, no finding caps, no scoring — composed in one pass.
- Emptiness is suspect in the Disputed/Unknown list and the save audit, but "the saves were by design, here are the facts" is a legitimate non-empty completion.

## When the trust parts fail

- No tracker or triage lane reachable → keep owner and date inline in the doc as the explicitly weaker fallback (docs rot, trackers do not), and say so in the report.
- `docs/` or the postmortems directory absent → create it before writing.
- Cause still unknown → record what is known and list the rest as Unknown; a postmortem may run with an unknown cause, but it never becomes a cause-hunt (that is `diagnose`).

## Fence

- **From `diagnose` (load-bearing):** `diagnose` Phase 6 is titled "Cleanup + post-mortem," but its post-mortem is a commit/PR line stating the winning hypothesis plus an optional `improve-codebase-architecture` handoff, scoped to one code bug. This skill is the durable, dated, blameless retrospective for any incident — same word, different deliverable. For a code bug whose cause is unknown, run `/diagnose` first, then `/postmortem`; a non-code incident needs no diagnose and postmortem stands alone.
- vs `system-design-review` and `tech-debt-scan`: both disclaim incident work — they review a healthy system, not an incident that happened.
