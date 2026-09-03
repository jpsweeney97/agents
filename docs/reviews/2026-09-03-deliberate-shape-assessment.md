---
type: review
date: 2026-09-03
scope: "plugins/decide/skills/deliberate — a fresh-eyes assessment of whether the skill has the right shape for JP to use, plus the general question of how an orchestration skill should be designed"
source: "JP's /braindump of 2026-09-03: 'is this the right architecture? the right shape? if not, what is? if it is, how do we make it a useful tool and not an intimidating system?'"
posture: read-only; no skill edits; reads the live bundle, its spec and lineage, the July methodology critique, the T2 experiment record, and the skill-usage ledger
reviewed_commit: 22bfcd3
---

# Deliberate: is this the right shape?

## Verdict

**The pipeline is the right idea. The way it is built is the wrong shape for its only user, and the evidence says so plainly.** The five-stage sequence (generate, prune, shape, recommend, contest) and the two methods deliberate owns (Prune and Contest) are sound and worth keeping. Everything wrapped around them, the validator, the run-state store, the schemas, the pins, the capsule, the terminal taxonomy, was built to make the pipeline fail honestly. It succeeded at that and, in doing so, produced a skill that JP cannot read, cannot invoke without composing an eight-field specification, and has never once run on a real decision. My recommendation is a rebuild at roughly one-tenth the size, keeping the judgment and dropping the mechanism. Details and the reasoning follow.

Terms used below, defined once. **Constituent skills** are the three decide-plugin skills deliberate runs as stages: ideate, option-shaping, making-recommendations. **Machinery** means the scripts, schemas, validation rules, and state files, as opposed to instructions about how to think. **Organic fire** means a run on a real decision, as opposed to a test run on a prepared prompt.

## What JP asked for, and what got built

The spec records the want in JP's words: one invocation, no mid-run questions, decisive pruning with a reason and a revival condition for every cut, and the principle that the run must "complete every judgment it can honestly own, never manufacture a winner." That is a clear, small want.

What exists today, by size:

| Part | Size |
| --- | --- |
| SKILL.md | 97 lines, 2,232 words, tuned to 4,749 tokens |
| Five reference files | about 14,000 words |
| contract-data.yaml (canonical schemas and templates) | 710 lines |
| deliberate-validate.py (validator) | 10,868 lines of Python |
| Shared module, fixtures, tests | about 2,000 more lines |
| Design spec | 446 lines, 23,176 words, version 30 |

The two methods deliberate actually owns, Prune and Contest, are about 950 words in methods.md. **Less than six percent of the skill's text is about how to think; the rest is about how to move data between stages without error.** Compare making-recommendations: 2,370 words, nearly all of them judgment, fired 299 times in the ledger.

## Where the heaviness came from

JP's own guess in the braindump was that the agents ran away with it. The lineage section of the spec confirms this in detail, version by version.

- **Version 1** already contained the two structural decisions that drove everything after: stages run in fresh, isolated agents (so the pruning agent cannot see JP's lean), and the run ends in a pasteable "capsule" for re-runs. Both were chosen in the design-exploration conversation over a single-context alternative.
- **Versions 2 through 18: seventeen adversarial design reviews, each folded.** Every review asked "how could this fail, be gamed, drift, or lie?" and every answer was another rule, schema, terminal, or check. The reviews were adjudicated by review-reviewer, which judges whether a review is reliable. Nothing in the loop judged whether a fix was proportionate to the failure it prevented.
- **Versions 19 through 27: nine live test failures, all in the machinery.** YAML quoting, envelope schema gaps, a flag mismatch, a path canonicalization bug, the validator wrapping its own stored text and then rejecting honest work for not matching the wrapped bytes. Each fix was another rule.
- **Version 28** extracted a module from the validator and then built a checker to authenticate the module split. That checker was reopened by review four more times.
- **Versions 29 and 30** folded the July methodology critique and one more live bug.

The July critique read all twenty build handoffs and found, in its words, "no doubt sentence, no 'is this worth it,' no cost-benefit hesitation." The build cost about two million tokens and 27 agents. The critique itself cost about 1.8 million tokens. The follow-on experiment (below) cost 322 agent dispatches and 15 operator hours.

**So the answer to "where did all of that come from" is: from a review loop with no size brake, run by agents, in which JP adjudicated whether reviews were reliable but was never asked whether the design was getting too big.** agent-facing-design's whole-surface question ("if it now feels larger than the work it protects, simplify before adding more") and the recheck-investment skill exist for exactly this. Neither was applied.

## Evidence: what fired, what broke

**Fires.** Every completed run in the skill's life used the same prepared 3,760-byte test prompt. The July critique counted 4 full runs, 2 honest-failure runs, and about 10 partial runs, all tests. Organic fires as of that date: zero. I checked the ledger and the transcripts for anything since. There is exactly one: on 2026-08-14, in the athena-kb-local repo, JP typed `/deliberate` with a draft file as the argument. The agent replied that the invocation "names the draft file but no decision frame, which the contract requires," started reading the file, and three minutes later JP interrupted with "No, I want you to get an adversarial review from Codex." The one real attempt was a misfire: JP reached for the token wanting a review, and the skill's contract met him with a missing-field complaint.

**What broke.** The critique's central finding, which I re-verified against the lineage: across the whole build, zero failures in the judgment layer and about fifteen defects, all in the machinery. Generate, Prune, Shape, Recommend, and Contest never once did their job badly. The validator, the store, and the schemas broke repeatedly, sometimes against themselves. The critique's own phrase: "the machinery is its own failure surface." **The part of the skill that works is the small part. The part that breaks is the large part.**

**The premise test.** The whole architecture rests on one claim, stated once in the spec: isolating stages from each other reduces bias. The spec itself said this was untested and named the test: shallow pruning against a full-shaping control, to see whether the prune step excludes eventual winners. That experiment (T2) was pre-registered, sealed on 2026-07-22, run across four sessions, and stopped on 2026-07-25 at its 15-hour ceiling. Verdict: inconclusive. The core bet remains untested.

**Runtime cost.** The two clean test runs took 42 minutes (Codex) and 1 hour 43 minutes (Claude). One orchestrator session made 866 shell calls. The native Claude shape, where the session that receives `/deliberate` dispatches the stage agents itself, had never run as of the critique, and I found no run since. Both accepted Claude runs came through hand-built relay arrangements labeled as test accommodations.

**The re-run half.** The capsule, import, revival, and drift-restart features are about half the contract by text. No capsule has ever been pasted back. The transaction they price has never occurred.

## Judging the architecture, layer by layer

I separate four layers and judge each on agent-facing-design's own test: does a wrong step here damage the work, and is lighter context insufficient?

**Layer 1: the pipeline.** Generate with ideate, prune, shape with option-shaping, recommend with making-recommendations, contest the exclusions. **Right.** This is the "use A, then B, then C" shape JP described, plus a narrowing step that is genuinely needed (you cannot shape fifteen options to comparable depth) and a check at the end. The ledger supports the need: making-recommendations fires constantly, but ideate (9) and option-shaping (5) almost never fire on their own. People do not run four skills in sequence by hand. An orchestrator is how the front half of the chain gets used at all.

**Layer 2: fresh agents per stage, with the lean withheld.** The concern is real: a model that knows which option the user favors tends to favor it. The remedy is right in kind and disproportionate in form. The right form is one instruction: dispatch Prune and Recommend to fresh subagents whose brief contains the field, the constraints, the values, and the budget, and omits the user's lean and every earlier stage's reasoning. The current form is a fifteen-row by five-column packet matrix, a brief renderer, a byte-exact store the renderer reads from, and a validator that refuses off-column items. **Keep the idea. Replace the matrix with a paragraph.**

**Layer 3: the store, validator, pins, and capsule.** Each piece answers a real question. Compaction might make the orchestrator misremember an option's wording, so store everything byte-exact. A stage agent might paraphrase, so compare bytes. A constituent skill might change mid-run, so pin its hash. JP might disagree with a cut, so give him a resumable capsule. But apply the damage test. A wrong step here produces a slightly different wording, or a summary that is off, in a read-only chat advisory that JP reads and can re-run by saying "revive X." The store lives in a temp directory and is trashed at close. Nothing is deleted, no credential is exposed, no user state is corrupted. **This layer protects against failures whose cost is a re-run, using machinery whose own failures consumed the entire build.** Lighter context is sufficient: write each stage's output to a plain Markdown file in the scratchpad, tell stage agents to quote wordings verbatim, and let JP read the files.

**Layer 4: terminals, receipts, containment checks, model provenance, helper-call discipline.** These exist to make layer 3 fail honestly. They are justified only if layer 3 exists. Remove layer 3 and they go with it.

## Why this is the wrong shape for JP

1. **The only trigger is JP typing `/deliberate`, and JP cannot read the skill.** The skill sets `disable-model-invocation: true`, which removes it from the model's view entirely. A natural-language request like "help me deliberate this" cannot reach it. So the skill fires only when its human types its name, and its human has said he does not understand what it says. The ledger result follows: zero organic runs in seven weeks, one misfire.
2. **The argument hint is a specification, not a prompt.** It reads: decision frame; candidates plus field mode; constraints at price; values; evidence plus authorization; survivor budget; or a pasted capsule plus re-run directives. making-recommendations, which JP fires constantly, needs "recommend between these."
3. **It front-loads the work JP wants help with.** Composing constraints at their price, stated values, and an evidence authorization is the shaping work outcome-shaping exists to do with JP. deliberate demands it as input.
4. **The offload claim has failed its own test.** AGENTS.md says offload is absent when the user "quietly stops summoning the skill." JP never started. Seven weeks is long enough to say that.
5. **A one-token, walk-away skill that takes one to two hours per run** and may exit `store unavailable` on Codex is not walk-away.
6. **Judgment never failed; machinery always did.** Fifteen defects, all machinery, zero judgment. The skill's value is in the six percent that never broke.
7. **The premise the machinery serves is untested after a 322-dispatch experiment.** Building a heavy protective structure around an unproven bet, and then failing to prove the bet, leaves only the structure.

## What the right shape is

A rebuild of the same five-stage pipeline as a single SKILL.md of roughly 120 to 180 lines, with at most one short reference file for the Prune and Contest methods, and no scripts, schemas, or tests. Outline:

1. **What to bring.** A decision question. Optionally: candidates you already have, constraints you are sure of, and your current lean. Everything else defaults. One paragraph.
2. **The five stages, one paragraph each.** Which constituent skill runs, what its fresh subagent's brief contains, and what it omits (the lean; earlier stages' reasoning). Prune keeps about four survivors by default.
3. **The Prune method,** trimmed to about 300 words from methods.md: cuts by confirmed constraints, by fact-established equivalence or dominance, and disclosed budget cuts; never scores or invented weights; every cut gets a reason and a revival condition.
4. **The Contest method,** about 150 words: test each exclusion against the recommendation's actual logic; a user preference for an excluded option is always a live challenge.
5. **Stage outputs as files.** Each stage writes one Markdown file to the scratchpad (01-field.md through 05-contest.md). This is the entire compaction defense and the entire re-run mechanism. JP can read them.
6. **The close.** making-recommendations' own close, in any of its four shapes, plus the exclusion ledger as a table, plus one line: "to re-run, tell me which cut to revive or which constraint to change."
7. **Stop rules.** A muddy question routes to outcome-shaping before the run starts. A constituent skill's honest exit ends the run as that exit. Where the runtime cannot spawn fresh subagents, run inline and say so.

Estimated run time drops from one to two hours to the time the five stages take to think, likely ten to twenty minutes. The skill becomes model-invocable again, so "help me think through this decision properly" can reach it.

## What to keep from the current bundle

The judgment survived every fire. Carry it forward: the Prune method text, the Contest method text, the principle that all four close shapes are successes and no winner is manufactured, the exclusion ledger with reasons and revival conditions, fresh subagents for Prune and Recommend with the lean withheld, and the rule that a constituent's exit is final. The rest of the bundle (validator, tests, contract-data.yaml, schemas.md, stage-packets.md, capsule.md, the T2 apparatus) moves to skills-archive as history. Git preserves it either way.

## The general answer: how to design an orchestration skill

JP asked whether an orchestrator should be "use A, then B, then C" or "a rigid pipeline." The answer is: rigid in order, loose in format, and small.

**An orchestrator owns exactly five things and nothing else:**

1. **The order** of the stages.
2. **The hand-off:** what each stage receives from the previous one, and what it must not receive.
3. **The gate policy:** where it proceeds on the original authorization and where it stops for the human.
4. **The stop rule:** a constituent's stop is the answer, never overruled or worked around.
5. **The close shape:** what the human gets at the end.

It does not restate, re-derive, or validate any constituent's rules. It does not check a constituent's output beyond "did it produce what the next stage needs." The house already has this pattern working: `land`, in the git-cycle plugin, is 111 lines, states "this skill contributes sequencing and authorization, nothing else," and has 28 ledger fires. It is the model.

**Machinery is justified in an orchestrator in two cases only:** a stage's output is consumed by a machine that needs a fixed format, or a wrong value would cause damage the human reading the output would not catch. In deliberate, every consumer is a reader (the next stage's agent, then JP) and the output is advice. Neither case holds.

**Intermediate state goes in plain files a human can read** when a run is long enough that context might compact. Not a store with a validator. A folder.

**Fresh subagents are for withholding, not for purity.** Use one when a stage must not see something specific, and say in one sentence what its brief omits.

**Put a size brake in the design before the first review round.** State a line budget in the spec. Require each review fold to remove as much as it adds, or refuse the fold. Read the argument hint aloud and ask whether the intended user would type it. The lesson of deliberate is not that adversarial review is bad; it is that adversarial review only ever asks "how could this fail?", and a loop with only that question grows without bound.

## Where I disagree with the July critique

The July methodology critique held deliberate and wrote: "Nothing in the evidence licenses tearing down machinery whose observed failures were all repaired and whose premise is unproven rather than disproven — that would be the overcorrection." I respect the reasoning and disagree with applying it now, for three reasons. First, that critique's question was whether the method is sound; JP's question is whether the skill is usable by him, and a skill its user cannot invoke has failed the offload test regardless of method soundness. Second, it was written four days after founding and said "four days is nothing"; it is now seven weeks with zero organic runs and one misfire. Third, the critique's own findings are the case for the rebuild: judgment never failed, machinery always did, the premise is untested, the re-run half has never been used. A rebuild that keeps the judgment and drops the machinery is not tearing down what works. It is keeping exactly what the fires proved.

## Recommendation and next step

**Rebuild deliberate in place as the light version described above, release it as decide 2.0.0, and archive the current bundle.** The version bump is major because the invocation contract changes: no capsule, no field modes, no survivor budget as a field, model-invocable again. The work is one skill file, one optional reference, a README paragraph, a CHANGELOG entry, and the archive move. It routes through agent-facing-design for the design and skill-ux-design for the invocation surface, and it should be smoke-tested on one real decision of JP's, not a fixture, before the version lands.

Two cheaper alternatives, and why I rank them lower. Fixing only the human-facing surfaces (description, argument hint, README) leaves the one-to-two-hour runtime, the never-run native dispatch shape, and eleven thousand lines of validator to maintain. Building a second, light skill beside the current one gives one job two skills and leaves the intimidating one in the plugin JP opens.

## Correction, 2026-09-03, after the first run of the rebuilt skill

The estimate above, "likely ten to twenty minutes," was wrong. The first end-to-end run of the rebuilt skill took 44 minutes 34 seconds and cost $20.57 at list price (`docs/smoke-tests/2026-09-03_deliberate-2.0-first-smoke.md`). The time is stage thinking on a 20-option field, not choreography: the run made one shell call where a v1 run made 866. The comparison to v1's 42 minutes and 1 hour 43 minutes stands; the claim that the rebuild is much faster does not, and the question of whether a 45-minute run is one JP will invoke is now a prune-watch item in the lifecycle note.

## Evidence boundary

Read whole: SKILL.md, agents/openai.yaml, the plugin manifest and README, the spec's settled-want and lineage sections, the full July methodology critique, ADR 0001, the T2 pre-registration's status and question, the lifecycle note, and the transcript of the 2026-08-14 invocation. Read at heading and structure grain: the five references, the validator's subcommand list, contract-data.yaml's head, the T2 pilot and panel reports. Not read: the validator's body, the test suites, the smoke-test records beyond what the critique and lifecycle note quote. Fire counts come from the skill-usage ledger, which the critique showed undercounts Claude-side `/deliberate` fires (the hook only sees Skill-tool calls); I therefore also grepped the athena-kb-local transcript directly, which is how the one 2026-08-14 attempt was found. Run-time figures and the build's token cost are the critique's numbers, not re-measured here.
