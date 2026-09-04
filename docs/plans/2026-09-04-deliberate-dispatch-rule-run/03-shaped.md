# Shape — four options for the dispatch-rule conflict

Rank-free comparison surface. Four options, developed by question rather than by option, so no option gets a finished narrative while its rivals stay slogans. No filtering, scoring, ranking, or lean. Field order preserved; the order was produced by the upstream Prune stage of this `deliberate` run, not supplied by the user.

## The field, exact wordings

1. **Ask JP which he meant.** Put both sentences to him in one question and make his answer the resolution, wherever he says it should live.
2. **Record the decision and change no instruction.** Add one entry to `docs/agents/contract-decisions.md` naming which sentence governs and why, and leave both texts exactly as written.
3. **Restate the skill's sentence as the global rule applied.** Say that five long dispatches make a cheaper capable model the right one, and that on Claude Code that model is Opus, instead of naming a model as an override.
4. **Let skills govern their own dispatches.** Add a clause: judgment stages inherit the session model unless a skill names its own model for its own stages.

### Collision check

I checked whether any two options succeed or fail for the same underlying reason. None do, and no collision is reported. The closest pair is 2 and 3: both leave `~/.claude/CLAUDE.md` untouched and both leave the operative behavior identical. Their decisive dependencies differ, so they can fail separately. Option 2 rests on the reading that a more specific instruction governs a general one. Option 3 rests on the different reading that the global rule's judgment bullet is a cost-matching default rather than a deliberate refusal to economize on judgment work. Either reading can be wrong without the other being wrong.

### How the options relate, as a fact about the field

Option 1's output space contains options 2, 3, and 4, plus resolutions nobody has named, because it makes JP's answer the resolution "wherever he says it should live." This is a structural fact about the option as worded, not an argument for or against it. It also means option 1 is the only option that would establish the precondition option 4's cheapest path needs (see Q4).

## The live questions

1. What changes, and where does a future agent meet it?
2. Does the contradiction still stand afterward?
3. Does it leave the Codex path working?
4. What does it cost to carry out, in this repo's own currency?
5. What must be true about JP's intent, and what if that is wrong?
6. Does it cover the other skill that already names its own dispatch model, and the next one?
7. What does it cost the reader, and what does it cost to undo?

## Facts at a glance

Factual attributes only; no column here is a score.

| Option | Surface changed | Gate or release triggered | Ledger entry owed | Text reaches `methodology-critique` |
| --- | --- | --- | --- | --- |
| 1. Ask JP | none until he answers | none until he answers | none until he answers | only if the question is widened past the two named sentences |
| 2. Record only | `docs/agents/contract-decisions.md` | none named by the charter for a collision adjudication; see Q4 | yes, that is the option | no, as worded it names one skill's sentence |
| 3. Restate the skill sentence | `plugins/decide/skills/deliberate/SKILL.md` line 29 | decide plugin release (constraint 2) | no; skill edits are build-and-prune | no, it rewrites one sentence in one skill |
| 4. Skills govern dispatches | `~/.claude/CLAUDE.md` judgment bullet | charter-gated always-loaded edit (constraint 1) | yes, charter line 68 | yes, by construction |

## Q1. What changes, and where does a future agent meet it?

**1. Ask JP.** Nothing changes until he answers, and the option does not say what surface the answer lands on. A future agent meets nothing new unless the answer is written somewhere a session loads. This is the one live question option 1 does not answer; it defers the mechanism rather than choosing one. That is a description of the option, not a defect claim: its whole content is that the mechanism is his to pick.

**2. Record only.** One entry in `docs/agents/contract-decisions.md`, a tracked file in this repo. No always-loaded surface and no skill text changes. A fresh Claude Code session still loads both bullets of the global rule, and a `deliberate` run still reads the skill's sentence at dispatch time. Neither reads the ledger. `AGENTS.md` points at the ledger, but `AGENTS.md` loads only in sessions working in `/Users/jp/.agents`, and its pointer routes an agent there before a gated charter event, not before a dispatch. So the record reaches an agent only when it is already doing charter work in this repo, which is not the moment the conflict bites.

**3. Restate the skill sentence.** One sentence, or two, inside line 29 of `plugins/decide/skills/deliberate/SKILL.md`. The mechanism is that it removes the word-level appearance of an override by re-deriving Opus from the global rule's own headline principle, so an agent holding both texts sees an application rather than an exception. A future agent meets it whenever it invokes `deliberate` and reads the paragraph, which is every run. What it does not touch: the global bullet still says judgment stages inherit the session model, and `deliberate`'s five stages are judgment stages by the rule's own list.

**4. Skills govern dispatches.** One clause added to the judgment bullet in `~/.claude/CLAUDE.md`. That file loads in every Claude Code session on this machine, in every repo, whether or not the session dispatches anything. So the change is met constantly and by every agent, not at a trigger. The two skills that name their own model need no edit, and the conflict stops existing in the text rather than being explained away.

## Q2. Does the contradiction still stand afterward?

**1. Ask JP.** Unknown until he answers. His answer could leave both texts standing, change one of them, or remove the Opus default entirely, which is a state nobody in this field has proposed. The honest answer to this question is that the option's range of outcomes includes "yes, still standing."

**2. Record only.** Yes, in the texts. Both sentences stay exactly as written and continue to say different things about the same dispatch. What changes is that an agent who notices the conflict and finds the ledger has an adjudication instead of having to reason one out. An agent who notices it mid-run and does not find the ledger still reasons it out, and the likely reasoning is the specific-over-general reading, which is what the ledger would have said. So the practical outcome converges whether or not the record is consulted.

**3. Restate the skill sentence.** Partly. A reader of the skill alone sees no conflict, because nothing there claims to override anything. A reader holding both sentences still sees "inherit the session model" against "on Claude Code that model is Opus" and must resolve it by treating the bullet as a default the section's headline overrides. The conflict moves from explicit to interpretive rather than disappearing. One introduced defect is specific and worth stating: the restatement asserts that Opus is the cheaper capable model, which is true from a Fable session and false from a Sonnet or Haiku session, where the same rule moves stages up in cost. The current wording names a model and is never wrong on its face; the restatement carries a cost claim that is wrong in exactly those sessions.

**4. Skills govern dispatches.** No, on its face. The bullet is amended so that a skill naming its own model is the sanctioned path, and both existing skill rules become applications of the amended rule. The residual is a new boundary question the clause creates rather than answers: "for its own stages" does not say whether a skill may name an expensive model for a mechanical stage. The section headline would still argue against it; the clause would not.

## Q3. Does it leave the Codex path working?

Constraint 3: `deliberate` is dual-runtime and its Opus rule is Claude-Code-only by its own wording. The global rule in `~/.claude/CLAUDE.md` is a Claude Code surface, so the contradiction exists only on Claude Code.

**1. Ask JP.** Unknown; whatever he chooses must keep the sentence "on another runtime, use its subagent model setting" intact.

**2. Record only.** Yes, by construction. No text changes at all, so nothing Codex reads is touched.

**3. Restate the skill sentence.** It can, but this is the option most exposed. The rewrite sits immediately beside the Codex sentence in the same paragraph and must not consume it. There is also a subtler wrinkle: a justification derived from the global Claude rule lands in a file Codex reads, so a Codex agent would read a rationale referencing a rule its runtime never loads. That is a readability cost specific to this option, not a functional break.

**4. Skills govern dispatches.** Yes. The clause never reaches Codex, so it creates no Codex obligation and changes no dual-runtime file. It fixes the contradiction on the only runtime where the contradiction exists.

## Q4. What does it cost to carry out?

**1. Ask JP.** One question, which his stated preference format makes cheap: batched, one decision, numbered options. No gate, no release, no worktree, no ledger entry until his answer names one, at which point that answer's own price applies on top. The distinctive cost is the thing this run cannot supply from the record: his attention, spent on a decision he did not ask to make. Within this library's own terms the move is a recognized completion rather than an evasion, since "your call" is one of the four `making-recommendations` close shapes the `deliberate` skill names as successes.

**2. Record only.** One tracked-file edit and one commit, through the repo's branch flow because a user-level hook blocks edits on `main`. The charter requires date, surface, outcome, and a durable evidence pointer; the 2026-07-02 precedent makes the ledger commit itself the pointer when the subject file is untracked. There is a real friction in the charter's own text worth naming. Charter line 30 says collisions between contracts "are resolved by curation — one contract keeps the job; the other is narrowed, absorbed, or removed — never by precedence rules or runtime routing adjudication." Option 2 resolves this collision by naming which sentence governs and changing neither, which is the precedence move that sentence excludes. The counter-reading is that One Owner Per Job governs two contracts claiming the same *job*, and the global rule is a dispatch-policy contract while the skill's sentence is a clause inside a skill whose job is deliberation. Whether the charter clause bites therefore turns on a reading nobody has settled. Second cost, smaller: charter line 68 lists the gated decisions that get an entry as admission, fold, rejection, park, and retirement, and a collision adjudication is none of the five, so the entry would be the first of its kind.

**3. Restate the skill sentence.** A decide plugin release: satellite lifecycle run, version bump in lockstep with a CHANGELOG section, and the Codex republish that the landed bump authorizes; mirror sync and push stay ask-gated. The version class is not settled by the option as worded and depends on the drafting. If the restatement keeps the same operative default, the standing rule that a doc-only cut is a patch makes it 2.2.2. If the restatement genuinely changes the rule from "always Opus" to "the cheaper capable model," it changes behavior in a Sonnet session, which makes it a minor. There is a fourth release in one day to weigh against 2.1.0, 2.2.0, and 2.2.1, all dated 2026-09-03. The local proof bar is visible in 2.2.1's own record: a changed sentence was forward-tested with two Opus runs on the patched text before landing.

**4. Skills govern dispatches.** The charter-gated path, and its price is lower than it first looks in one respect and higher in another. Lower: this amends an existing ambient rule rather than adding a new one, and the standing decision says an ambient line joins an existing owner as a fold whenever one exists, which would reduce the argument owed from "this line earns an always-loaded slot" to "this clause folds into the rule that already owns dispatch policy." Higher: that standing decision's own precondition is "when JP has already decided *whether*," and here nobody has decided whether the global rule should carve out skills at all. So the cheap fold path is not obviously available, and the expensive reading is the Admission argument in full. On top of either: the ledger entry with the commit as its pointer, and the practical fact that `~/.claude/CLAUDE.md` sits outside this repo and outside the satellite fleet, tracked by no git repo on this machine. The edit gets no branch, no diff review, and no revert. That is an asymmetry the other three options do not carry.

## Q5. What must be true about JP's intent, and what if that is wrong?

Every constraint and value in this run's setup is marked inferred; none was confirmed by him this session. That raises the stakes on this question for every option except the first.

**1. Ask JP.** Nothing must be true. It is the only option in the field that does not infer his intent. Its bet is that he has a view and that the question is worth his attention. If that is wrong he answers "you decide," and the run has spent its output on a question. The record cannot distinguish the readings: the throughline has carried this open question unchanged across five handoffs on 2026-09-03, which is consistent with him never being asked, with him not caring, and with it never reaching the top of a session.

**2. Record only.** That the specific-instruction reading is what he meant on 2026-09-03. This is the shortest inferential distance in the field. The handoff records that he asked how to put `deliberate`'s subagents on Opus and chose the skill-text route, and the Abandoned Paths entry records that mirroring the Opus default into the global file was declined as an edit he did not ask for. What option 2 adds beyond the record is only the ledger's statement of why.

**3. Restate the skill sentence.** That the purpose of his global rule is cost-matching and that Opus-for-`deliberate` is an instance of it. The section's first sentence says "match cost to the job," which supports the reading. The strongest contrary reading is structural and comes from the same text: the section economizes on mechanical stages and then says judgment stages inherit the session model, so the bullet may be a deliberate refusal to trade quality for cost on exactly the class of work `deliberate`'s stages fall into. Under that reading, restating Opus as the cost rule applied inverts the bullet's purpose for the class it exists to protect. There is also a question about constraint 4, which says a JP-authored stated position reverses only on observed evidence: this option changes none of his text but does re-describe what his rule means in another file, and whether that counts as touching his position is unsettled.

**4. Skills govern dispatches.** That he would accept a general carve-out in his own always-loaded file that he did not ask for. This is the longest inferential distance in the field, and the record contains a directly adjacent decline dated one day ago: mirroring the Opus default into the global file was declined as an always-loaded edit he did not ask for. A general clause is not the same edit as a mirrored default, so this is not automatically a reversal of that decline. It is the same class of edit on the same file, decided against yesterday. Constraint 4 also applies with full force here, and its own text leaves open whether the 2.1.0 record counts as the observed evidence that a reversal would require.

## Q6. Does it cover the other skill, and the next one?

A grep across every `SKILL.md` in the library found two skills that name a dispatch model. `methodology-critique` puts its forward-test proxies on Sonnet "by default, never the session model," which contradicts the global bullet more directly in words than `deliberate` does. Any option scoped to `deliberate` leaves that second instance standing.

**1. Ask JP.** As worded, the option puts "both sentences" to him, meaning the global bullet and `deliberate`'s. `methodology-critique` sits outside that question unless the question is widened, which nothing prevents but nothing in the option's wording does.

**2. Record only.** `deliberate` only, as worded: the entry names which sentence governs. A future agent meeting `methodology-critique`'s rule finds no entry. Writing the entry generally instead would state a precedence rule for all skills, which is a wider claim recorded on the weakest-reaching surface in the field.

**3. Restate the skill sentence.** `deliberate` only, by construction, since it re-derives Opus from this skill's five-dispatch shape. `methodology-critique`'s rule would in fact restate cleanly under the same logic, because Sonnet is the cheaper capable reading, but nothing in this option does that work, and its "never the session model" phrasing forbids the global bullet's default outright rather than departing from it once.

**4. Skills govern dispatches.** Covers both existing instances and every future skill that names its own model, because it changes the rule rather than the instances. The same fact is its cost: it grants the permission prospectively to skills nobody has written, bounded only by the phrase "for its own stages."

## Q7. What does it cost the reader, and what does it cost to undo?

**1. Ask JP.** Reader cost is one question in the format he prefers. Undo cost is unusual: there is nothing to revert, but his answer becomes a stated position, and constraint 4 then makes it reverse only on observed evidence. The option converts a live ambiguity into a settled position, which is both its point and its irreversibility.

**2. Record only.** Reader cost is zero. The skill stays at its current 91 lines, the always-loaded set is unchanged, and no session gets longer. Undo cost is one later entry, because the ledger is append-only and settled entries are never rewritten. Cheap, and not silent.

**3. Restate the skill sentence.** Reader cost lands on the person who reads every skill he invokes, in a paragraph he will read on every run. It could go either way on length: the restatement replaces the existing sentence "Opus is the default because a run is five long dispatches" rather than adding to it, so the net could be neutral or shorter, but no draft exists and the plain-literal-wording value applies to whatever is drafted. Undo cost is another plugin release at the same price as doing it.

**4. Skills govern dispatches.** Reader cost is one clause in every Claude Code session on this machine, in every repo, indefinitely, whether or not the session dispatches. That is the always-loaded budget the charter gates hardest, and its stated reason applies exactly here: an ambient contract has no visible fire, so you cannot watch it mis-fire, and it is entangled, so removal has non-local effects. Undo cost is retirement discipline requiring observed-work evidence rather than route-absence, performed on a file no git repo tracks, so there is no diff to revert to. The staggering value would also apply if another behavior-shaping governor is currently settling, and I have no record of what governors landed recently.

## Evidence gaps

- **No observed instance of the contradiction causing a wrong dispatch.** This is the largest gap in the field and it bears on all four options, because the charter's own admission and retirement discipline asks for observed-work friction rather than argument. The smallest check that would size it: the skill-usage ledger at `~/.claude/logs/skill-usage-ledger.jsonl` records skill invocations across all repos, so counting `deliberate` and `methodology-critique` fires since 2026-09-03 would bound how much exposure has actually occurred. I did not run it; reading it is outside the evidence scope this stage was given.
- **Whether the 2.1.0 validation probe had the global rule loaded is unrecorded.** The handoff records a headless probe that passed `opus` and quoted the deciding sentence, but not whether `~/.claude/CLAUDE.md` was in that context. If it was not, the probe is evidence that the skill sentence is followed, not evidence that agents resolve the conflict correctly. This weakens the practical-convergence answer given for options 2 and 3 in Q2.
- **Whether the global dispatch rule is JP-authored is itself inferred.** The setup marks it so. Constraint 4 applies only if it is, and constraint 4 bears hardest on option 4.
- **No record of which behavior-shaping governors are currently settling.** Bears only on option 4, through the staggering value.
- **No drafted wording exists for options 3 or 4.** Option 3's version class and its net effect on skill length both depend on the draft, and option 4's boundary problem depends on how "for its own stages" is phrased.

## One observation available from inside this run

The agent writing this stage runs on Opus, dispatched from a Fable session. That is one observed instance, today, of the skill's sentence being followed over the global bullet in real work rather than in a probe. Its limits are worth stating: it is a single instance, I can see only my own model identity and not the orchestrator's reasoning, and the orchestrator that dispatched me is the same session that composed my brief, so it is not an independent agent making the call cold.

## Bias pass

The skill requires checking whether one option received more charitable assumptions, implementation detail, or effort merely because it felt attractive. Developed word counts came out uneven: 437 for option 1, 589 for option 2, 754 for option 3, 660 for option 4. The unevenness is not favor. Option 3 carries the most words because it carries the most live defects and unsettled dependencies, and option 1 carries the fewest because it specifies no surface and so has less mechanism to describe. Each option has at least one adverse finding developed to the same depth as its strengths: option 1 leaves the resolution's location unspecified and converts an open question into a position that reverses only on observed evidence; option 2 uses the precedence move charter line 30 excludes and reaches the fewest agents; option 3 introduces a cost claim that is false in a Sonnet session and puts a Claude-only rationale in a dual-runtime file; option 4 is the same class of edit on the same file that was declined one day ago, on a file no repo tracks.

Two corrections were made during the pass. Option 3's shared dependency with option 2 was first written as a single decisive reading and corrected to two different readings that can fail separately, which removed a false collision. Option 2's reader-cost cell first cited the skill at 89 lines from the evidence packet; the live file measures 91, and the verified count is used.

This is a record of the pass, not a certification that the surface is neutral.

## What can now be compared, and what was not done

The four options are now distinguishable on the seven questions above. The sharpest live distinctions are these. Only option 4 changes an always-loaded surface, and only option 4 covers the second skill that already names its own dispatch model. Only option 1 avoids inferring JP's intent, and only option 1 leaves the resolution's location unspecified. Options 2 and 3 keep the operative behavior identical and differ in which surface carries the reconciliation and who reads it. Option 3 is the only option that introduces a claim that can be false in a session that is not this one. Option 2 is the only option whose method the charter's own collision text arguably excludes.

Certainty is not equal across these cells and does not need to be. The costs of options 3 and 4 are documented in the repo record; the cost of option 1 is a matter of his attention and cannot be read from any file; the standing of option 2 against charter line 30 is an unsettled reading rather than a fact.

No ranking, scoring, filtering, or lean was performed, no option was eliminated, and none of the four was developed into a finished design. Nothing outside this file was changed.
