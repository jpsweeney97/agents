---
name: fence-archaeology
description: "Use when about to remove, disable, or weaken something that looks useless or obsolete — code, a config value, a guard clause, a rule, a process step, a contract-template clause, a diligence or intake question, a checklist gate — and the reason it exists is not already known and current. Also fires when rationalizing a question set or process: every item kept or cut deserves a reconstructed reason. Digs the reason out of the record (git history, PR threads, ADRs, tests — or version history, prior template versions, the introducing author, the owning function's records) and renders a per-fence disposition — reason-dead / reason-alive / reason-unknown — before any removal. Do not use when the reason is already documented and current (just read it), to map consumers of an interface change (contract-change-propagation, where available), or to resolve which source of truth governs a claim (baseline, where available)."
---

# Fence Archaeology

Chesterton's fence, operationalized: don't take down a fence until you know why it was put up. The removal impulse ("this looks dead," "this blocks my change," "lint says unused") is the hypothesis under test, never the conclusion — "I can't see why this is here" is a fact about the observer, not the fence.

## The moves

1. **Pin the fence.** The exact thing about to be removed or weakened, and what prompted the impulse. One line each.
2. **Dig, cheapest instrument first — in whatever form this environment keeps its record.** Stop as soon as the reason surfaces.

   Versioned code:
   - `git log -S '<distinctive token>'` (add `--reverse` for the introducing commit; `git blame -C -M` and `--follow` survive renames and moves); read the introducing commit's full message.
   - The PR or issue thread the commit references, where reachable.
   - ADRs, CHANGELOG, docs, and nearby comments mentioning the token.
   - Tests that pin the behavior — a test that fails when the fence comes down is the reason, speaking.

   Documents and process:
   - Version history and tracked changes; prior versions of the template, checklist, or question set.
   - The thread, email, or meeting note that announced the change; the person or function that introduced it.
   - The owning program's framework docs. A control that exists because of a regulation, a security posture, or a counterparty requirement is alive no matter who remembers it — its reason lives with the control's owner (Legal, Privacy, Security, the program office), and one question to that owner beats an afternoon of digging.

   Timebox the dig. Exhausting the cheap instruments without an answer is a finding ("reason unknown"), not a mandate to spelunk.
3. **Reconstruct and date the original threat.** One sentence: what was true when the fence went up — the bug, the incident, the platform quirk, the requirement — with the evidence cited (sha, thread, test name).
4. **Test whether the reason still binds.** Is the original condition still present — the buggy dependency still in the lockfile, the platform still supported, the incident's cause still reachable? This, not the fence's age or looks, is the live/dead call.
5. **Render the disposition, one row per fence:**
   - **Reason found, dead** → remove; put the evidence the reason expired into the removing commit's message, so the next archaeologist inherits it.
   - **Reason found, alive** → keep; leave the reason more findable than you found it (a comment or doc pointer at the fence).
   - **Reason unknown** → never remove silently. Either keep-and-mark, or remove with a tripwire: name the observable that would fire if the fence turns out load-bearing, and make the removal maximally reversible (its own commit, trivial revert).

## The close

The disposition table is the deliverable; executing a removal belongs to the ordinary edit flow. Where the fence has an accountable owner — a control owner, a template owner, a program office — the disposition routes to them: reconstructing a fence's reason is evidence for the owner's removal decision, never authority to remove it. No certification — a fence whose reason you found may guard a second reason nobody wrote down; say what the dig did not cover.
