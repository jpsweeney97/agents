# Prune: how to resolve the two dispatch-model instructions

Survivors: 4, in field order. Cuts: 18, one record each, below.

Every hard constraint in this run is inferred from the repo record and none was confirmed by the user this session. Where a cut rests on one, the record says so and is labelled a judgment call.

---

## Survivors

**Ask JP which he meant.**
Put both sentences to him in one question and make his answer the resolution, wherever he says it should live.

**Record the decision and change no instruction.**
Add one entry to `docs/agents/contract-decisions.md` naming which sentence governs and why, and leave both texts exactly as written.

**Restate the skill's sentence as the global rule applied.**
Say that five long dispatches make a cheaper capable model the right one, and that on Claude Code that model is Opus, instead of naming a model as an override.

**Let skills govern their own dispatches.**
Add a clause: judgment stages inherit the session model unless a skill names its own model for its own stages.

---

## Cut records

```text
Option:         **Measure the two models on one stage.**
                Run the same stage brief twice, once on Fable and once on Opus, compare the two outputs, and let that comparison decide which text changes.
Cut:            same reason, judgment call
Reason:         This and "Ask JP which he meant" make the same bet, which the field's own group name states: the resolution should wait on an input nobody has gathered. They fail together if the conflict can be settled from what is already known. Keeping the question to JP as the pair's representative. Every constraint and value in this run is marked inferred, and the input that would settle them is JP's intent, which one question reaches. The input this option gathers is model quality, which does not by itself say which of the two texts changes or where the resolution lives, and which costs a substantial run to get: the first deliberate 2.0 run took 44 minutes 34 seconds and $20.57 across its stages, and a two-arm comparison returns one sample per arm judged by whoever judges it.
Strongest case: It is the only option in the field that manufactures the observed evidence constraint 4 demands, and constraint 4 is exactly what blocks changing the global rule's substance on argument alone. Without it, every route that touches the global line is arguing rather than showing.
Revive if:      JP answers that the global rule's letter is what he meant, or the resolution turns on whether Opus stages are worth their cost. Either makes the measurement the deciding input rather than a detour.
```

```text
Option:         **Pin the model in a subagent definition.**
                Define a stage agent whose definition sets Opus, and have `deliberate` dispatch by agent type without passing a model parameter.
Cut:            constraint, judgment call
Reason:         Constraint 4, which is inferred. The 2026-09-03 handoff records JP being shown the full resolution order for a subagent model, per-call parameter then subagent definition then CLAUDE_CODE_SUBAGENT_MODEL then session model, and choosing the skill-text route. Re-routing to the subagent definition reverses that choice, and no observed evidence has appeared since. Judgment call on two counts: constraint 4 is inferred, and reading "JP chose the skill-text route" as a stated position about the other three routes is one reading of that sentence rather than the only one. Two further costs, not decisive on their own: a subagent definition lives in `~/.claude/agents/`, outside this repo and untracked like the global file, so the model choice leaves version control; and it is a Claude Code surface, so the skill still needs its Codex branch and the definition adds a place Codex never reads.
Strongest case: A model choice resolved by the runtime's own precedence order cannot be contradicted by an instruction, which is the cleanest available form of one source for a rule. It is also the only family that would let both texts stop naming a model at all.
Revive if:      JP says the configuration route is what he wanted, or a third and fourth skill need their own dispatch model and per-skill agent definitions become the cheaper pattern to maintain.
```

```text
Option:         **Set the model in the environment.**
                Set `CLAUDE_CODE_SUBAGENT_MODEL` so every subagent runs on the named model regardless of the session model.
Cut:            same reason, judgment call
Reason:         Same reason as "Pin the model in a subagent definition": both move the model choice out of instruction text into runtime configuration, and both stand or fall on whether configuration settles a disagreement that lives in two sentences. Keeping the subagent definition as the pair's representative, because it is scoped to the dispatches in dispute. The environment variable applies to every subagent dispatch on the machine, so every dispatch that names no model would run on the named model, including the mechanical stages the same global rule sends to the cheapest capable model. That widens the disagreement rather than settling it.
Strongest case: One environment variable, no new file to maintain, nothing added to any repo, and it sits above the session model in the resolution order for every skill at once.
Revive if:      The pair's representative is revived and per-agent definitions prove too many to maintain, or JP wants every unnamed subagent dispatch on one model as a deliberate machine-wide default.
```

```text
Option:         **One statement of the policy, plus a drift check.**
                Name the dispatch-model policy in exactly one file, have the other point at it, and add a script that fails when the two disagree.
Cut:            dominated, judgment call
Reason:         Dominated by "Let skills govern their own dispatches", which reaches this option's goal, one statement of the policy, with nothing copied and no script to maintain: the always-loaded line grants the authority and the skill states its own model, and those are complementary sentences rather than two copies of one rule. This option also does not say which file holds the policy, and every direction costs something. The skill pointing at `~/.claude/CLAUDE.md` leaves a Codex run of deliberate pointed at a file that runtime never loads, which is constraint 3, inferred. The global file pointing at the skill is the gated always-loaded edit, constraint 1, inferred, and makes an always-loaded rule depend on a plugin that may not be installed. A third file in this repo does not load when deliberate runs in another repo. The house drift-check pattern also assumes one agreed policy written twice, and these two sentences disagree, so the policy must be decided before a check has anything to check.
Strongest case: It is the repo's own sanctioned pattern for a copy that cannot be avoided, mechanically enforced, and it is the only option that would catch the two texts diverging again later instead of trusting that they will not.
Revive if:      The resolution turns out to need the same sentence in both files, or `~/.claude/CLAUDE.md` comes under version control so a check over it is maintainable.
```

```text
Option:         **Check each dispatch as it happens.**
                Add a hook that inspects subagent dispatches and reports when a judgment dispatch runs on a model other than the session model with no skill naming one.
Cut:            same reason, judgment call
Reason:         Same reason as "Say at run time which rule chose the model": both keep the two texts exactly as written and add runtime machinery that reports the model choice instead of settling it, and both stand or fall on whether catching a wrong model at dispatch time substitutes for a resolution. Keeping the run-time statement as the pair's representative, because it costs one sentence in a file JP already reads. This option is a new hook, which the charter names as an always-loaded contract in the class it gates hardest, firing on every dispatch in every repo to watch one skill's sentence, and it lands a second behavior-shaping governor while the first is still unreadable in live fire.
Strongest case: The disagreement only causes harm at the instant a model is picked, and this is the only option that would catch a wrong model in a skill nobody thought to check, including skills written after this decision is settled.
Revive if:      The representative is revived and per-run disclosure proves easy to miss, or wrong dispatch models show up in real work across several skills.
```

```text
Option:         **Write the precedence into the charter.**
                State in `docs/agents/charter.md` that a skill's own dispatch-model sentence governs its own dispatches and the global rule governs every other dispatch.
Cut:            same reason, judgment call
Reason:         Same reason as "Let skills govern their own dispatches": both install the same rule, that a skill's own model sentence governs its own dispatches and the global rule governs the rest, and they differ only in which document carries it. Keeping the global-file version. The charter is consulted before gated events, not at dispatch time, so a precedence rule written there is never read at the moment a model is chosen and would not change what any agent does. The charter's One Owner Per Job clause also says collisions are resolved by curation, one contract keeps the job and the other is narrowed, absorbed, or removed, and never by precedence rules, so this option must overturn that clause to install what the other reaches by amending the line that actually loads.
Strongest case: The reading that settles this is a rule about rules, and the charter is where this repo's rules about rules live. A resolution there governs every future collision of this shape, not only this one, and the charter is maintained by direct editing so amending it takes no admission of its own.
Revive if:      Skill-versus-global collisions appear in a third and fourth skill and a general resolution rule earns its charter amendment, or the no-precedence-rules clause is revisited for reasons of its own.
```

```text
Option:         **Lower the charter's cost for narrowing an existing always-loaded line.**
                Amend the charter so that adding an exception which reduces an existing line's reach costs less than admitting a new contract.
Cut:            dominated, judgment call
Reason:         Dominated by "Let skills govern their own dispatches". This option is not a resolution; it lowers the price of one, and the price it targets is already lower than it assumes. The charter's Decision Record covers folds as well as admissions, and the standing decision in the record is that an ambient line joins an existing owner as a fold whenever one exists. The Multi-Agent Dispatch section is an existing owner, so a clause narrowing it goes through the fold path today. The narrowing is therefore available now at fold cost, and this option adds a governance amendment that buys nothing this decision needs. Judgment call: whether an exception clause counts as a fold rather than an admission is a reading of the charter, not a settled fact.
Strongest case: If narrowings really are priced as admissions, this is the option that unblocks the most direct repair, and it makes every future narrowing cheaper rather than paying the same toll again each time.
Revive if:      An attempt to land a narrowing clause is actually charged Admission's full discipline, which would show the fold path does not cover it.
```

```text
Option:         **Specific instruction beats general default (seed, from the record).**
                "Leave both as written; treat the skill sentence as the more specific instruction and the global line as governing every other dispatch."
Cut:            dominated, judgment call
Reason:         Dominated by "Record the decision and change no instruction". Both rest on the same reading and neither changes a text, but they do not fail together, so this is not a same-reason pair and the seed-keeping rule does not apply: the unrecorded version has one failure mode the recorded version does not. This option is the live state today. The 2026-09-03 handoff says the skill sentence is the more specific instruction and was not mirrored, and the throughline has carried the pair as unreconciled through five handoffs since. The reading alone has already been tried and has not closed the question; the ledger entry is what closes it. The seed's only edge is costing nothing at all, against one ledger entry and one commit.
Strongest case: Specific instruction beating a general default is ordinary reading and needs no writing down anywhere. Every option that writes something down spends a gate or a release to record what a careful reader already does, and the record it writes is one more surface to keep true.
Revive if:      The ledger is the wrong home for this. The charter's Decision Record covers gated decisions, admission, fold, rejection, park, retirement, and "change nothing" may be none of them. On that reading the entry cannot be written and the reading with nothing written down is what remains.
```

```text
Option:         **Say at run time which rule chose the model.**
                Keep both texts, and have the setup line name the stage model and state that it departs from the session model.
Cut:            dominated, judgment call
Reason:         Dominated by "Record the decision and change no instruction". Both leave the two texts standing and state which rule governs. The record does it once, durably, in a runtime-neutral file, with no release. This option pays a decide release, satellite run, version bump, CHANGELOG section, Codex republish, to restate it at every run while the durable record stays silent, so the question keeps reopening in the handoffs. Its increment is also smaller than it reads: the setup shown before the first dispatch already names the model the stages will run on, so what is added is the sentence saying that model departs from the session model.
Strongest case: A person reading the setup catches a wrong model before the run spends anything, and a ledger entry is a file nobody opens mid-run. The disclosure lands where the cost is about to be incurred.
Revive if:      A recorded resolution proves invisible where it matters and a wrong stage model actually ships, or a skill edit is happening anyway and this line rides along at no extra release.
```

```text
Option:         **Let the orchestrator choose per run and state why.**
                No text names a model; the orchestrator picks the stage model from the session model, the run length, and cost, and says in the setup what it picked and on what grounds.
Cut:            dominated, judgment call
Reason:         Dominated by "Restate the skill's sentence as the global rule applied". Both change only the skill and pay the same release. The restatement writes the reason down once, in the file JP reads before he invokes it, and keeps the choice reviewable before the run starts. This option removes the written default and leaves the departure unwritten: the global bullet still says a judgment stage inherits the session model, so an orchestrator picking otherwise contradicts it with no sentence authorizing the departure. The contradiction stops being visible without stopping. It also makes the model differ between runs of the same skill, against the house bar for trust machinery, which is that it be reliable and single-sourced.
Strongest case: Which model runs a judgment stage may genuinely be a per-run judgment. A session already on a cheap model, or a short run, does not need the same answer as five long dispatches from a Fable session, and no fixed default can see the run in front of it.
Revive if:      The fixed default proves wrong across a range of sessions, or the per-run statement in the setup is shown to give the user the same control that a written default gives.
```

```text
Option:         **Make the run cheap enough not to need a default.**
                Shorten or reduce the five dispatches until the run cost that prompted the Opus sentence is gone, then drop the sentence.
Cut:            same reason, judgment call
Reason:         Same reason as "Delete the skill's model sentence": both end with the skill naming no model, so stages inherit the session model and the global rule is the only authority left, and both stand or fall on whether one authority for dispatch models is worth the run cost that follows. Keeping the deletion as the pair's representative, because it reaches the same endpoint by removing one sentence. This option rebuilds the five-stage run to get there, and the five stages are the skill's invocation contract, which is a major version change under the house versioning rule, spent to settle a disagreement about a sentence. It also assumes the shortening reduces cost enough to make the default unnecessary, which nothing in the record establishes.
Strongest case: The model default is a workaround for what a run costs. Removing the cost removes the reason for the default rather than arguing about which text owns it, and a shorter run is worth having on its own terms.
Revive if:      The five-stage run turns out to be too long or too expensive on its own merits, which would make the shortening worth doing whatever happens to the model sentence.
```

```text
Option:         **Delete the skill's model sentence.**
                Remove the Opus default so stages inherit the session model, leaving the plain-language steering ("use Sonnet for the stages") as the only way to change it.
Cut:            constraint, judgment call
Reason:         Constraint 4, which is inferred. On 2026-09-03 JP asked how to put deliberate's subagents on Opus instead of Fable, and 2.1.0 landed exactly that. Deleting the sentence reverses the behavior he asked for, and no observed evidence has appeared since that the Opus default is wrong; the comparison that would produce it is itself an ungathered option in this field. The cost it re-imposes is measured: the one deliberate 2.0 run made before 2.1.0, from a Fable session with stages inheriting Fable, took 44 minutes 34 seconds and $20.57. Judgment call on two counts. Constraint 4 is inferred. And as the prompt states it, constraint 4 guards the global rule, so applying it to JP's ask about the skill extends it; if both sentences are JP's, constraint 4 does not adjudicate between them, which is the question the surviving first option puts to him.
Strongest case: One authority for dispatch models is worth real money, and this is the only option that leaves exactly one sentence in the whole environment naming a model for a judgment stage. It also needs no gate, no charter argument, and no question to anyone.
Revive if:      JP says the global rule's letter is what he meant, or a Fable-versus-Opus comparison shows the stages do not need Opus.
```

```text
Option:         **Mirror the Opus default (seed, from the record).**
                "Mirror the Opus default into the global CLAUDE.md."
Cut:            dominated, judgment call
Reason:         Dominated by "Let skills govern their own dispatches". Both add text to the always-loaded file so it stops contradicting the skill, and both pay the same gate, but they do not fail together, so this is not a same-reason pair and the seed-keeping rule does not apply: the mirror has a failure mode the class rule does not. It writes deliberate's specific model into the always-loaded file, which is a second copy of one rule. The house pattern for a sanctioned copy requires a drift check, and a second copy without one is repair-or-prune evidence. It also has to be edited again, in a gated file, every time the skill's model changes. The class rule names no model, so there is nothing to drift. The record also declined this once already, as an always-loaded edit JP did not ask for.
Strongest case: The always-loaded file should say plainly what actually happens, in the same words the skill uses, rather than granting an authority whose instances a reader has to go and find. It is the most literal of the global-file options and the easiest to check by eye.
Revive if:      JP asks for the exception in literal words, or the class grant proves too broad and a named, drift-checked exception is preferred to it.
```

```text
Option:         **Reword the judgment bullet as a cost test.**
                Replace "inherit the session model" with a test under which a model cheaper than the session model is already compliant, such as the cheapest model that can carry the judgment, with the session model when unsure.
Cut:            constraint, judgment call
Reason:         Constraint 4, which is inferred. This replaces the bullet's rule rather than carving an exception from it: "inherit the session model" becomes "the cheapest model that can carry the judgment", so the default itself reverses. Constraint 4 says a JP-authored stated position reverses only on observed evidence, and no such evidence exists; the comparison that would produce it is an ungathered option in this field. The surviving global-file option leaves the default standing and adds one exception, which is the smaller claim and the one the record's fold path is for. There is also a concrete cost: "cheapest that can carry the judgment" makes Haiku compliant for a judgment stage whenever an agent judges it capable, removing the floor the current wording provides, and the when-unsure fallback only catches the cases an agent knows it is unsure about. Judgment call on three counts: constraint 4 is inferred, whether the global rule is JP-authored is inferred, and whether the 2.1.0 record already counts as observed evidence is open on the prompt's own statement.
Strongest case: The section's own first line is about matching cost to the job, and this is the only option that makes the bullet say what the section says it means. It fixes a word that turned a fallback into a floor, for every skill at once, and it makes both skills that currently contradict the bullet compliant without granting skills any new authority.
Revive if:      A Fable-versus-Opus comparison shows a cheaper model carries the judgment, or JP says the bullet's "inherit" was never meant as a floor.
```

```text
Option:         **Add the case the rule does not cover.**
                Say that a judgment stage repeated many times within one run may take a cheaper capable model.
Cut:            survivor count, judgment call
Reason:         Cut to reach the survivor count. This is a low-confidence cut of an option whose seriousness I could not resolve at sketch depth, not a judgment that it is unserious. It and the surviving global-file option are both exceptions carved from the same bullet at the same gate price, and they differ in what the exception keys on: dispatch volume here, skill authority there. Volume grants less, which counts for something under a value that says no always-loaded edits nobody asked for. Skill authority covers more: the two skills in this library that name a dispatch model today are both covered by it, where a volume-keyed exception leaves methodology-critique's rule, Sonnet by default and never the session model, still contradicting the bullet on a single proxy dispatch. Which of those matters more is the trade I could not settle at this depth.
Strongest case: The narrowest gated edit that removes the conflict is the right one, and what the rule is actually missing is dispatch volume. Five long dispatches in one run is a different situation from one judgment call, and saying so needs no grant of authority to skills at all.
Revive if:      The class grant is judged too broad, or a count of what actually contradicts the bullet shows volume covers it.
```

```text
Option:         **Delete the judgment bullet.**
                Remove "Judgment stages: inherit the session model", keeping the mechanical-stage bullet and the when-unsure fallback.
Cut:            same reason, judgment call
Reason:         Same reason as "Move the whole section out of the always-loaded file": both remove the judgment guidance from the always-loaded surface, both are retirements under the charter's Retirement discipline, which takes the same observed-work evidence as an admission and never route-absence alone, and both stand or fall on whether the ambient dispatch guidance has stopped earning its slot. Keeping the relocation as the pair's representative, because it preserves the guidance instead of deleting it. This option also leaves the section internally broken: the fallback it keeps, when unsure which kind a stage is treat it as judgment, would point at a bullet that no longer exists.
Strongest case: A general cost rule has no business naming a model class for judgment work, and the cost-matching intent survives in the section's first line without the bullet. It is also the only option that makes the contradiction disappear by removing one of its two halves outright.
Revive if:      The relocation is revived and the guidance is judged worth keeping ambient, which leaves deleting the one bullet as the smaller change.
```

```text
Option:         **Move the whole section out of the always-loaded file.**
                Delete "Multi-Agent Dispatch" from `~/.claude/CLAUDE.md` and put its content in a file an agent reads when it is about to dispatch.
Cut:            dominated, judgment call
Reason:         Dominated by "Let skills govern their own dispatches". Both change the global file so it stops contradicting the skill. The class rule keeps the section always-loaded, which is what makes it work: the section says in its own words that it overrides the harness's inherit-by-default and cost-is-no-constraint guidance, and an override of a default only fires if it is loaded before the default takes effect. Moving it to a file an agent reads when it is about to dispatch defeats that stated purpose, because the harness default applies to exactly the agents that never think to read it. This is also the largest always-loaded change in the field, and retiring text from the always-loaded surface takes observed-work evidence that nobody has gathered.
Strongest case: Dispatch guidance genuinely does not need to load in every session to do its work, and moving it out removes the charter gate from every future edit to it, including this one. It buys back always-loaded context in every session for guidance that only matters at one moment.
Revive if:      The section is shown not to fire, meaning dispatches in real work ignore it, or the always-loaded context budget becomes the binding problem.
```

```text
Option:         **Run `deliberate` from an Opus session.**
                Change the practice rather than any text, so the session model and the skill's default are the same model.
Cut:            dominated, judgment call
Reason:         Dominated by "Record the decision and change no instruction". Both change no instruction text and leave both runtimes working. The record settles which sentence governs once and for everyone. This option avoids triggering the disagreement rather than resolving it, and only for as long as JP remembers to start the session on Opus. It also inverts the value both rules exist for: it pins the whole session, orchestrator and every unrelated dispatch included, in order to control five stage dispatches. And the conflict fires again the first time deliberate runs from a Fable session, which is the session this decision is being made in.
Strongest case: No edit, no gate, no release, nothing to maintain, and it is the only option where the two sentences point at the same model in fact rather than by argument.
Revive if:      JP works mainly from Opus sessions anyway, or the real resolution needs time and a stopgap is wanted while it waits.
```
