# Field: how to resolve the two dispatch-model instructions

**Frame the prompt assumes:** that the two sentences genuinely disagree, and that settling them means changing what one of two instruction texts says. Some options below accept both halves; some test one or the other.

**Un-ranked.** Options are grouped by where the resolution would live, and the groups run in alphabetical order by group name, which carries no quality reading. Order inside a group follows how much of the existing text each option leaves standing, which also carries no quality reading. Nothing here is a recommendation, a ranking, or a shortlist.

---

## An input nobody has gathered yet

**Measure the two models on one stage.**
Run the same stage brief twice, once on Fable and once on Opus, compare the two outputs, and let that comparison decide which text changes.
Bet: this is a testable question about work quality being argued as a question about wording, and the evidence that would settle it does not exist yet.

**Ask JP which he meant.**
Put both sentences to him in one question and make his answer the resolution, wherever he says it should live.
Bet: the global sentence's intent is inferred rather than known, and one question is a cheaper source of truth than any argument about what the text implies.

## Configuration and scripts

**Pin the model in a subagent definition.**
Define a stage agent whose definition sets Opus, and have `deliberate` dispatch by agent type without passing a model parameter.
Bet: a model choice belongs in configuration that the runtime resolves by its own precedence order, not in instruction text where another instruction can contradict it.

**Set the model in the environment.**
Set `CLAUDE_CODE_SUBAGENT_MODEL` so every subagent runs on the named model regardless of the session model.
Bet: a setting that sits above both texts in the runtime's resolution order removes the need for either text to name a model at all.

**One statement of the policy, plus a drift check.**
Name the dispatch-model policy in exactly one file, have the other point at it, and add a script that fails when the two disagree.
Bet: two copies of a rule are safe when a check catches them diverging, which is the pattern already used for the protected-branch sentence.

**Check each dispatch as it happens.**
Add a hook that inspects subagent dispatches and reports when a judgment dispatch runs on a model other than the session model with no skill naming one.
Bet: the disagreement only causes harm at the moment a model is picked, so catch it there instead of wording it away in advance.

## Governance record

**Write the precedence into the charter.**
State in `docs/agents/charter.md` that a skill's own dispatch-model sentence governs its own dispatches and the global rule governs every other dispatch.
Bet: the reading that settles this should be written where the repo's rules about rules live, accepting that the charter today says collisions are resolved by curation and never by precedence rules, so this option also changes that clause.

**Record the decision and change no instruction.**
Add one entry to `docs/agents/contract-decisions.md` naming which sentence governs and why, and leave both texts exactly as written.
Bet: what is missing is a durable record of a decision, not different instructions.

**Lower the charter's cost for narrowing an existing always-loaded line.**
Amend the charter so that adding an exception which reduces an existing line's reach costs less than admitting a new contract.
Bet: the charter's cost is set for adding contracts, and that cost is what currently blocks the most direct repair.

## Neither text: the reading alone

**Specific instruction beats general default (seed, from the record).**
"Leave both as written; treat the skill sentence as the more specific instruction and the global line as governing every other dispatch."
Bet: a specific instruction overriding a general default is ordinary reading and needs no writing down anywhere.

## The `deliberate` skill

**Restate the skill's sentence as the global rule applied.**
Say that five long dispatches make a cheaper capable model the right one, and that on Claude Code that model is Opus, instead of naming a model as an override.
Bet: the disagreement lives in the skill's wording, and the skill is the text that can change without the charter's Admission discipline.

**Say at run time which rule chose the model.**
Keep both texts, and have the setup line name the stage model and state that it departs from the session model.
Bet: a person reading the setup before the run starts catches a wrong model faster than any rule prevents one.

**Let the orchestrator choose per run and state why.**
No text names a model; the orchestrator picks the stage model from the session model, the run length, and cost, and says in the setup what it picked and on what grounds.
Bet: which model runs a judgment stage is a judgment to make per run, not a policy either file should fix in advance.

**Make the run cheap enough not to need a default.**
Shorten or reduce the five dispatches until the run cost that prompted the Opus sentence is gone, then drop the sentence.
Bet: the model default is a workaround for what a run costs, and removing the cost removes the reason the two texts disagree.

**Delete the skill's model sentence.**
Remove the Opus default so stages inherit the session model, leaving the plain-language steering ("use Sonnet for the stages") as the only way to change it.
Bet: one authority for dispatch models is worth more than the run cost the default was added to save.

## The global `~/.claude/CLAUDE.md` file

**Mirror the Opus default (seed, from the record).**
"Mirror the Opus default into the global CLAUDE.md."
Bet: the always-loaded file should carry the exception in the same words the skill uses.

**Let skills govern their own dispatches.**
Add a clause: judgment stages inherit the session model unless a skill names its own model for its own stages.
Bet: fixing the class rather than the instance means no future skill needs its own mirrored exception.

**Reword the judgment bullet as a cost test.**
Replace "inherit the session model" with a test under which a model cheaper than the session model is already compliant, such as the cheapest model that can carry the judgment, with the session model when unsure.
Bet: the section's own first line is about matching cost to the job, and the word "inherit" turned a fallback into a floor.

**Add the case the rule does not cover.**
Say that a judgment stage repeated many times within one run may take a cheaper capable model.
Bet: what the rule is missing is dispatch volume, not skill authority.

**Delete the judgment bullet.**
Remove "Judgment stages: inherit the session model", keeping the mechanical-stage bullet and the when-unsure fallback.
Bet: a general cost rule has no business naming a model class for judgment work, and the cost-matching intent survives without it.

**Move the whole section out of the always-loaded file.**
Delete "Multi-Agent Dispatch" from `~/.claude/CLAUDE.md` and put its content in a file an agent reads when it is about to dispatch.
Bet: dispatch guidance does not need to load in every session to do its work.

## The session or environment

**Run `deliberate` from an Opus session.**
Change the practice rather than any text, so the session model and the skill's default are the same model.
Bet: the two sentences only disagree when the session model sits above Opus, so aligning the session removes the disagreement without any edit.

---

**One assumption runs under nearly every option here:** that the right model for a deliberate stage can be settled once, ahead of any particular run. The per-run orchestrator choice is the option that violates it.

**Fixed points from the prompt the field leaves untouched:** constraint 2 and constraint 3 — every option that edits the skill accepts the version bump, CHANGELOG section, satellite worktree run, and Codex republish as the price of changing one sentence, and no option proposes anything that would change what Codex does.
