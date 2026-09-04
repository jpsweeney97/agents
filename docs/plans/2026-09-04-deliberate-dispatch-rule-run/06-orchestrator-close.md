# Orchestrator close — deliberate run on the dispatch-rule conflict (2026-09-04)

First interactive run of deliberate 2.x (decide 2.2.1) on a real decision. Orchestrator: Fable 5.1. Every stage: a fresh agent on Opus. Run directory created 00:04; Contest finished 00:40; about 36 minutes wall clock. Stage times from file timestamps: Generate 5 min (22 options), Prune 12 min (4 survivors, 18 cuts), Shape 7 min, Recommend 6 min, Contest 3 min. Cost not measured; only `/usage` shows it.

## 1. The Recommend stage's close, as written (04-close.md)

# Close — the dispatch-rule conflict

## Decision

How to resolve the conflict between the always-loaded rule in `~/.claude/CLAUDE.md` ("Judgment stages (verify, judge, synthesize, design): inherit the session model") and `deliberate`'s own sentence ("On Claude Code, pass `model: opus` on every stage dispatch unless the user names a model"), and where the resolution should live.

## The Call

**Clear call.** Take option 2: **Record the decision and change no instruction.** Add one entry to `docs/agents/contract-decisions.md` naming which sentence governs and why, and leave both texts exactly as written.

Write that entry as a **park of the always-loaded amendment, with a reopen trigger**, not as a standalone precedence ruling. That is a drafting specification inside option 2, not a fifth option: same file, same cost, same operative result. It matters because it removes both of the frictions the comparison surface raised against option 2.

## Why

**The behavior is already correct, so nothing here is urgent.** The skill's sentence is followed in practice. The comparison surface records one instance from today: the agent that wrote it ran on Opus, dispatched from a Fable session. No instance of a wrong dispatch appears anywhere in the record. Whatever the two texts look like side by side, no work has gone wrong because of them.

**The cost that is actually being paid is different, and option 2 is the only option that ends it.** This question has been carried unchanged as open work in five handoffs on 2026-09-03 and again in the 2026-09-04 frontier note. That recurrence is the observed friction in this decision. It is bookkeeping friction, and a ledger entry is the instrument for exactly that. One commit ends it.

**Writing the entry as a park makes it a decision the charter already recognizes.** Charter line 68 lists the entries a gated decision gets: admission, fold, rejection, park, retirement. A bare precedence adjudication is none of the five, which is why the comparison surface flagged it as the first of its kind. A park is on the list, and parks carry a reopen trigger by the charter's own requirement. The ledger already holds park entries in this shape (lines 85 and 86, both dated 2026-07-02). So the entry records what was actually decided: the amendment to the always-loaded rule was considered and set aside for now, and until it is reopened `deliberate`'s own sentence governs `deliberate`'s dispatches.

**The park framing also answers the charter-line-30 objection.** Line 30 says collisions "are resolved by curation... never by precedence rules." Two things defuse it. First, line 32 says One Owner Per Job is "a design heuristic, not an up-front gate" for build-and-prune contracts, and resolved by "pruning the weaker" when competing fires appear in the transcript. `deliberate` is a skill, so it is build-and-prune, and no competing fire exists in the record. Second, a park entry records a decision about the gated contract itself, not a precedence rule between two contracts.

**A park does not foreclose the general fix.** Its whole purpose is to be reopened on its stated trigger. So choosing option 2 now costs nothing that option 4 could later deliver.

### How to write the entry

Three drafting points, each fixing something the comparison surface named.

1. **Scope it to this collision.** Do not state a general precedence rule for all skills. That would put an ambient rule on the one file no session loads, which is the worst placement available.
2. **Name `methodology-critique` as an observation, not a rule.** It carries the same shape (its forward-test proxies run on Sonnet, "never the session model"). Recording that the pattern has two instances is what makes the reopen trigger checkable later. Recording it as permission is what option 4 does, and option 4 is parked.
3. **State the basis honestly.** JP chose the skill-text route on 2026-09-03 and the mirror-into-`CLAUDE.md` edit was declined then. He was not shown the collision and asked to adjudicate it. The entry should say the run parked the amendment on that basis, not that he ruled on it. Evidence pointer: the decide 2.1.0 CHANGELOG entry and its commit, plus the ledger commit itself, following the 2026-07-02 precedent for untracked global-file decisions.

## The Case Against

**Runner-up: option 1, "Ask JP which he meant."** The strongest case for it is the strongest argument in this whole field. Every constraint and every value this run compared against is marked inferred, and none was confirmed by him this session. That includes the value doing the most work in my recommendation. He is the only person who can say whether he wants his always-loaded rule to carve out skills, and the question is cheap in the format he prefers: one decision, batched, numbered options. My recommendation infers his answer from one adjacent act.

The smallest realistic change that would make it win is concrete and checkable at drafting time: **if the entry cannot be written without asserting that JP adjudicated the collision, ask him instead.** Point 3 above is the test. If the honest entry turns out to need his voice, option 2 has failed and option 1 is the call.

**Option 3, "Restate the skill's sentence as the global rule applied."** Its case: it is the only option that reaches the person who reads every skill he invokes, in a paragraph he meets on every run, and it costs a plugin release he is already practiced at.

It loses on two specific findings. First, its distinctive content is a claim that is false in some sessions. Saying Opus is "a cheaper capable model" is true from Fable and false from a Sonnet or Haiku session, where the same rule moves stages up in cost. The current sentence names a model and is never wrong. Second, strip that claim out and almost nothing is left to release: line 29 already says "Opus is the default because a run is five long dispatches," which is the reason option 3 wants stated, and the skill never claims to override anything. The word does not appear. Option 3 fixes an appearance the skill text does not itself create, at the price of a fourth release in one day and a claim that can be false.

The smallest realistic change that would make it win: a draft that removes the apparent override without generalizing away from a named model, plus evidence that a reader actually stumbles on the current paragraph.

## What Would Flip It

- **An observed wrong dispatch.** A `deliberate` or `methodology-critique` run whose stages went to the session model against the skill's own sentence. That is the reopen trigger to write into the park, and it flips this toward option 4. The cheapest check that would size the exposure is the skill-usage ledger at `~/.claude/logs/skill-usage-ledger.jsonl`, counting fires of both skills since 2026-09-03. It was outside the previous stage's evidence scope and is not needed before writing the entry.
- **JP asking for the general carve-out.** One sentence from him lifts the only thing stopping option 4. My recommendation agrees with the reading the record already carried, so this is where the agreement is made checkable: option 4 wins the moment he says he wants his ambient rule to carry the exception, and nothing else in the comparison stops it.
- **A third skill naming its own dispatch model.** Two instances are a pattern worth noting. Three, arriving without anyone deciding a general rule, is evidence that the instances should stop being written one at a time.
- **The drafting test failing.** See The Case Against, first item.

## Commitment point and reversibility

The recommended option is a two-way door. The ledger is append-only, so the entry is undone by one later entry, and not silently. The one-way door in this field is option 4: `~/.claude/CLAUDE.md` is tracked by no git repository on this machine, so that edit gets no branch, no diff review, and no revert. That asymmetry is the reason it is set aside rather than weighed.

## Lean, disclosed

My first-read lean was option 2, and the record's visible working reading was also that both texts should stay unedited. I did not move off it. The case, not the comparison, is what carries it: no observed failure, the recurring carry is the real cost, and the ledger is the instrument for that cost. The comparison did change two things. It moved me from option 2 as worded to option 2 written as a park, and it showed that option 2 does not foreclose option 1 or option 4, which is what makes recommending it now honest rather than premature.

No option was added. Doing nothing at all was considered and is not recorded as an option: it leaves the recurring carry in place, and option 2 removes it for one commit.

---

Option:         **Let skills govern their own dispatches.** Add a clause: judgment stages inherit the session model unless a skill names its own model for its own stages.
Cut:            constraint, judgment call
Reason:         This run has no authority to edit `~/.claude/CLAUDE.md` on JP's behalf. The stated value "no always-loaded edits nobody asked for" is the one value in the setup backed by a dated observed act: on 2026-09-03 the closely adjacent edit, mirroring the Opus default into that file, was declined as an always-loaded edit he did not ask for. Constraint 4 compounds it — a JP-authored stated position reverses only on observed evidence, and there is no observed instance of the contradiction causing a wrong dispatch. I tested the constraint before letting it cut: it is not overstated, and it is not permanent, because option 1 lifts it in one question. Two further costs stand independent of authority. The file is tracked by no git repository, so the edit has no diff and no revert. And the clause creates a boundary it does not settle: "for its own stages" does not say whether a skill may name an expensive model for a mechanical stage, which inverts the section's own headline for the case it exists to prevent.
Strongest case: It is the only option that actually removes the contradiction rather than explaining it, and the only one that covers `methodology-critique` and every future skill that names its own dispatch model. It amends an existing ambient rule rather than adding one, so the standing decision that an ambient line joins an existing owner as a fold could apply. Writing the same permission one skill at a time is how a general rule gets built by accident, unread, across files nobody compares. If the pattern is real, the rule is the right place for it.
Revive if:      JP says he wants the carve-out in his always-loaded rule; or an observed instance appears of a judgment stage dispatched on the session model against a skill's own named model; or a third skill names its own dispatch model. The recommended ledger entry parks this option with those triggers, so it stays live by construction.

## 2. Cut ledger (19 cuts: 18 from Prune, 1 from Recommend; every one labelled judgment call, none fact-established)

| # | Option | Cut | Revive if |
| --- | --- | --- | --- |
| 1 | Measure the two models on one stage | same reason | JP says the global rule's letter is what he meant, or the resolution turns on whether Opus stages are worth their cost |
| 2 | Pin the model in a subagent definition | constraint 4 | JP says the configuration route is what he wanted, or a third and fourth skill need their own dispatch model |
| 3 | Set the model in the environment | same reason | the subagent-definition route is revived and per-agent definitions prove too many, or JP wants one machine-wide default |
| 4 | One statement of the policy, plus a drift check | dominated | the resolution needs the same sentence in both files, or `~/.claude/CLAUDE.md` comes under version control |
| 5 | Check each dispatch as it happens | same reason | the run-time statement is revived and per-run disclosure proves easy to miss, or wrong models show up across several skills |
| 6 | Write the precedence into the charter | same reason | skill-versus-global collisions appear in a third and fourth skill, or the no-precedence-rules clause is revisited |
| 7 | Lower the charter's cost for narrowing an existing always-loaded line | dominated | an attempt to land a narrowing clause is actually charged Admission's full discipline |
| 8 | Specific instruction beats general default (seed) | dominated | the ledger is the wrong home: "change nothing" is none of the five entry kinds |
| 9 | Say at run time which rule chose the model | dominated | a recorded resolution proves invisible and a wrong stage model ships, or a skill edit is happening anyway |
| 10 | Let the orchestrator choose per run and state why | dominated | the fixed default proves wrong across sessions, or the per-run statement gives the same control |
| 11 | Make the run cheap enough not to need a default | same reason | the five-stage run is too long or expensive on its own merits |
| 12 | Delete the skill's model sentence | constraint 4 | JP says the global rule's letter is what he meant, or a Fable-versus-Opus comparison shows the stages do not need Opus |
| 13 | Mirror the Opus default (seed) | dominated | JP asks for the exception in literal words, or the class grant proves too broad |
| 14 | Reword the judgment bullet as a cost test | constraint 4 | a comparison shows a cheaper model carries the judgment, or JP says "inherit" was never meant as a floor |
| 15 | Add the case the rule does not cover | survivor count | the class grant is judged too broad, or a count shows volume covers what contradicts the bullet |
| 16 | Delete the judgment bullet | same reason | the relocation is revived and the guidance is judged worth keeping ambient |
| 17 | Move the whole section out of the always-loaded file | dominated | the section is shown not to fire, or the always-loaded budget becomes the binding problem |
| 18 | Run `deliberate` from an Opus session | dominated | JP works mainly from Opus sessions, or a stopgap is wanted while the real resolution waits |
| 19 | Let skills govern their own dispatches (cut by Recommend) | constraint | JP says he wants the carve-out; an observed wrong dispatch; a third skill names its own dispatch model |

## 3. Exclusion check (05-contest.md)

Exclusion check: live recorded challenges — **Add the case the rule does not cover.**, **Write the precedence into the charter.**, **Specific instruction beats general default (seed, from the record).**; most worth contesting: **Add the case the rule does not cover.**

## 4. Run directory

/private/tmp/claude-501/-Users-jp--agents/264f264c-d4b3-42b7-ba4f-da0bee19cd65/scratchpad/deliberate-dispatch-rule-2026-09-04 (00-setup, 00-evidence, 01-field, 02-prune, 03-shaped, 04-close, 05-contest, this file). The scratchpad does not survive the session.

## 5. Re-run

To re-run, tell me which cut to revive, which constraint to change, or which survivor to develop further, and I will restart from the stage that changes.

## 6. What the run did not do

It did not verify facts the stages marked as assumptions: every constraint and value was inferred from the record, not confirmed by JP; whether the global rule is JP-authored is inferred; the 2.1.0 probe's context is unrecorded; the usage ledger was not read. It did not develop the 18 excluded options. Stages were isolated (fresh Opus agents), so the lean reached only Recommend and Contest.
