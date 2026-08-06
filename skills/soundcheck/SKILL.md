---
name: soundcheck
description: Use when the user invokes /soundcheck or says the always-loaded instructions are fading, not being followed, or not salient enough — "you're drifting", "reread your instructions", "the contract isn't landing". Re-reads every always-loaded instruction file fresh, audits recent replies against them with quoted receipts and a cause read, restates the at-risk rules as applied to the current work, and logs one ledger line per ring. When a violation traces to the rule text itself, drafts a self-contained patch note — recommendation only, never an edit. With an argument (/soundcheck reply-shape), amplifies only that named rule. Do not use to author new rules or land durable rewrites (friction-to-guards), and not for "too loud" (that is the reply-register restate the Reply Shape contract itself owns).
---

# Soundcheck

Always-loaded instructions sit at the oldest position in context; session mass buries them. This skill is the monitor fader: it re-injects the contract at the newest position and binds it to the work in progress. The user rings it; you re-tune.

Being rung means drift was *felt*. Do not open by disputing that. The audit may still come back clean — if so, say so plainly, log the clean ring, and name what else might explain the felt drift.

## Moves

No-arg default is all moves. With an argument (`/soundcheck <rule>`), run the same moves against only the named rule or contract.

1. **Fresh Read, not recall.** Read the live always-loaded instruction files with actual Read calls, now: `~/.claude/CLAUDE.md`, the project `CLAUDE.md`(s) in scope, and any file those declare as always-loaded (charters, rule docs — not conditional consult-when-X references). Never quote a rule from memory. This skill deliberately contains no rule text, so there is nothing here to restate from.
2. **Audit with receipts.** Check your last 3–5 replies against the rules the recent work actually exercised — not the whole rulebook. Name the worst violation first, with a short quote of your own offending words beside the rule it broke. Max three receipts. Nothing found → "clean", plus the rule you judge most at risk anyway.
3. **Cause read.** One added line per receipt: what the rule lost to. Two causes exist. *Attention* — momentum, session mass, register gravity; the default. *Text* — the rule is ambiguous, collides with a competing rule, or misses a case. The drafter is the offender and "the rule was ambiguous" is always the flattering diagnosis, so a textual cause must quote the specific competing or missing text. No quote, no textual cause.
4. **Restate applied.** Restate the one or two rules that matter most for the work in front of you, phrased as what you will do differently in this session's next replies — not abstract rule text.
5. **Patch note — textual causes only.** Draft a minimal edit as a self-contained block an adjudicator can act on cold: receipt quote, the competing or missing text quoted, before → after, and a declared cost ("adds one line", "deletes two"). Invariant: **no louder, only clearer** — a patch may split, clarify, reposition, or delete; it may never merely emphasize. A pure-emphasis fix is a volume problem in a content costume: refuse it and re-anchor instead. Soundcheck never edits instruction files. Route the note: always-loaded global files go through the charter gate (friction-to-guards or a charter session); playpen files are cheap edits.
6. **Ledger.** Append one line to `rings.md` beside this SKILL.md: `date | project | rule(cause), rule(cause), … | note`. Clean rings get logged too. The ledger is telemetry, not paperwork: it is what makes a future docs remaster evidence-driven, and what shows whether an instruction edit actually reduced rings afterward.

## Escalation ladder

- Ring 1 on a rule → re-anchor. The normal case.
- Ring 2 on the same rule in one session → content problem by definition. Patch note even without a clean quote; say what evidence is missing.
- Three attention-rings on the same rule across the ledger → chronic. Patch note recommending a salience restructure, naming the lever: shorten, reposition, or anchor the rule to a trigger. Still never "add more."
- Three rings across *different* rules in one session → the room, not the desk. Stop mixing; recommend a fresh session and route to the handoff lane.

## Closeout ring

Before delivering anything big, run moves 1–3 silently against the draft. If receipts turn up, report them and log the ring with note `closeout`. If clean, say nothing and skip the ledger — no self-audit theater. This is the one self-triggered use; everything else waits for the bell.

## Reply

Model the contract in the reply itself — an overwhelming re-anchor is a failed one. Shape:

```
Soundcheck: <files re-read>

Receipts:
- <rule> — "<offending words>" — lost to <attention | text: "competing text quoted">
  (or: clean; most at risk is <rule>)

Re-anchor: <rule(s) restated as applied to the current work>

[Patch note: receipt · competing text · before → after · cost · route — only when a cause was textual]

Fork: <ladder rung reached> | Ledger: logged
```

Then continue the session under the re-anchored rules. The ledger line is the only durable write; the bell can be rung again.
