# Evidence packet (verbatim excerpts, gathered 2026-09-04)

## E1. Global rule: `~/.claude/CLAUDE.md`, lines 18-24 (always-loaded in every Claude Code session; file is not git-tracked)

```
## Multi-Agent Dispatch

When dispatching subagents (Workflow `agent()` calls, the Agent tool), match cost to the job. This overrides the harness's inherit-by-default and cost-is-no-constraint guidance, including under `ultracode`:

- Mechanical stages (search, extraction, formatting, mechanical edits): cheapest capable model, low effort.
- Judgment stages (verify, judge, synthesize, design): inherit the session model.
- When unsure which kind a stage is, treat it as judgment.
```

Origin: not recorded in docs/agents/contract-decisions.md. The 2026-09-01 memory `workflow-size-restraint` says "his global CLAUDE.md already says to match dispatch cost to the job", so the rule predates 2026-09-01 and is treated as JP's. Its stated purpose is cost-matching; its letter, for a judgment stage, is "inherit the session model" regardless of what that model costs.

## E2. Skill rule: `plugins/decide/skills/deliberate/SKILL.md` (decide 2.2.1; the model sentence landed in 2.1.0)

Line 17 (steering):
```
Plain-language steering the run honors: "don't add options" skips Generate and starts at Prune; "keep six" changes the survivor count; "you may research" allows web lookups in every stage; a model name ("use Sonnet for the stages") sets the stage model.
```

Line 23 (setup list includes "the model the stages will run on").

Line 29 (dispatch paragraph):
```
Each stage runs as a fresh agent with its own context, dispatched with a brief the orchestrator composes from `00-setup.md` and the previous stage's output file. On Claude Code, pass `model: opus` on every stage dispatch unless the user names a model; on another runtime, use its subagent model setting. Opus is the default because a run is five long dispatches. The fresh context is what keeps the user's lean, and each stage's reasoning, out of the stages that must not see them. Where the runtime cannot dispatch a fresh agent, run the stages in this context in order, still writing every file, and say in the close that the stages were not isolated.
```

The skill is 89 lines. JP reads every skill he invokes (memory `skills-jp-can-read`).

## E3. `plugins/decide/CHANGELOG.md`, 2.1.0 section

```
## 2.1.0 - 2026-09-03

### Added

- `deliberate` honors a model name as plain-language steering ("use Sonnet for the stages" sets the stage model), and the setup shown before the first dispatch names the model the stages will run on.

### Changed

- On Claude Code, `deliberate` dispatches every stage agent with `model: opus` unless the user names a model; on another runtime it uses that runtime's subagent model setting. Before, stages inherited the session model, so a run from a Fable session put five long dispatches on Fable. Minor, not patch: a steering phrase the run did not honor before, and a changed default the user sees in the setup and can override.
```

## E4. How 2.1.0 came about (handoff 2026-09-03 16:19, verbatim)

"After it, JP asked how to put deliberate's subagents on Opus instead of Fable. The docs (Claude Code 2.1.259) give the resolution order: per-call Agent `model` parameter, then the subagent definition's `model`, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the session model. JP chose the skill-text route."

"The global CLAUDE.md dispatch rule still says judgment stages inherit the session model; the skill's sentence is the more specific instruction and was not mirrored into CLAUDE.md (an always-loaded contract edit JP did not ask for)."

Validation of 2.1.0 included "a headless `claude -p --model opus` probe that passed `opus`, quoted the deciding sentence, and switched to `sonnet` for 'use Sonnet for the stages'."

## E5. Cost facts

- First deliberate 2.0 run (2026-09-03, before 2.1.0), in a Fable session with stages inheriting Fable: 44 minutes 34 seconds wall clock; $20.57 at list price across orchestrator and stage agents; all of it stage thinking, one shell call. (docs/smoke-tests/2026-09-03_deliberate-2.0-first-smoke.md)
- Billing: `claude -p` without `--bare` meters through the subscription login; Fable can bill usage credits past a plan limit; only `/usage` shows whether it did. (Era 149 record.)
- Fable 5.1 is the session model in this session and sits in a tier above Opus. The Agent tool in this session accepts `model` in {sonnet, opus, haiku, fable}. Claude Code's "fast mode" uses Opus.
- Model resolution order for a subagent (Claude Code 2.1.259 docs, per E4): per-call Agent `model` parameter → subagent definition's `model` → `CLAUDE_CODE_SUBAGENT_MODEL` env var → session model.

## E6. The charter on always-loaded edits (`docs/agents/charter.md`)

Line 3: "Skills and commands are build-and-prune and are **not** charter events — build them whenever they seem worth trying, prune them freely when they do not (see Reversibility Class). Consult this only before the events that stay gated: authoring or retiring an always-loaded contract (a rule, an AGENTS.md line, a hook, any ambient instruction), authoring a skill that can fire unattended or wields irreversible-effect tools (see Reversibility Class), installing anything that ships contract text, or deciding the fate of third-party contract material."

Line 20: "**Gated — rules, AGENTS.md lines, hooks, any always-loaded instruction.** An ambient contract has *no visible fire*: it shapes every response with no trigger in the transcript, so you cannot watch it mis-fire. And it is *entangled* — woven into surrounding guidance, so removing it has non-local effects you will not reliably notice. You can neither see it go wrong nor cleanly prune it, so it keeps the full Admission and Retirement discipline below."

Line 68: "Every **gated** decision — an admission, fold, rejection, park, or retirement of an ambient contract or third-party material — gets one entry in `contract-decisions.md` ... The evidence pointer must be durable and replayable — a commit, a tracked file, or a named, persistent artifact reachable outside the session — not a bare session reference."

Ledger precedent (2026-07-02 entry): amendments to global `~/.claude/CLAUDE.md` are ledgered with the ledger commit as the durable pointer, because the file is untracked.

## E7. Standing decisions in the throughline that bear on this (verbatim)

- "**Choosing a skill over an ambient rule is itself the cheap path.** A summoned skill is attended, reversible, ungated; prefer it unless the behavior must fire without invocation."
- "**An ambient line joins an existing owner as a fold whenever one exists.** When JP has already decided *whether*, the gate decides fold-versus-admission, placement, and minimum content, and the entry discloses the ratification posture."
- "**A JP-authored stated position reverses only on observed evidence, not principled argument (2026-09-01, C1).**"
- "**Behavior-shaping conversation governors land staggered, not stacked.** Stacking governors makes behavior changes unattributable, so each new one waits until the last is readable in live fire."
- "**A doc/metadata-only cut is a patch, not a minor; a capability change is a minor; an invocation-contract or output change is a major.**"
- "**`agent-facing-design` is the gate and constitution, not a template engine.** Judgment work must protect and provoke better thinking; trust machinery must be reliable and single-sourced; apply the bar per part."
- "**A landed manifest bump is publish intent (1-A, 2026-07-17).** ... Local Codex republish is authorized by the landed bump; mirror sync and push always remain ask-gated."
- Abandoned Paths, decide 2026-09-03 releases: "Mirroring the Opus default into the global CLAUDE.md was declined as an always-loaded edit JP did not ask for."
- House pattern for a sanctioned copy: the `land` skill carries one copy of the protected-set sentence, drift-detected by `scripts/check-protected-set.sh`; "a second copy of any constituent rule is repair-or-prune evidence."

## E8. The throughline's own statement of the open question (Frontier, 2026-09-04)

"The global CLAUDE.md dispatch rule (judgment stages inherit the session model) and deliberate 2.1.0's Opus default are unreconciled; the skill sentence is the more specific instruction and the always-loaded line is a gated edit nobody has asked for."

Carried unchanged in the 16:19, 21:21, and 22:39 handoffs of 2026-09-03 and the 23:10 and 23:51 handoffs.

## E9. Repo facts about skill and plugin editing (AGENTS.md)

- `skills/` is dual-runtime (Codex and Claude Code); plugin sources under `plugins/<name>/` are one source serving both runtimes; never per-runtime copies.
- "Bump the manifest `version` in lockstep with the behavior change it releases, and treat landing that bump as publish intent."
- `agent-facing-design` is consulted "before adding or materially expanding agent-facing obligations, proof standards, authority rules, lifecycle behavior, mutation boundaries, persistence, routing, or machinery."
- `writing-principles` owns "obligation-only prose edits inside an existing skill, support doc, AGENTS.md, CLAUDE.md".
- A Claude Code user-level hook blocks edits on `main`; skill-surface edits route through locked satellite worktrees (`worktree-task-cycle`).
- `~/.claude/CLAUDE.md` is outside this repo and outside the satellite fleet; it is not tracked by any git repo on this machine.

## E10. Which skills in this library name a dispatch model (grep over every SKILL.md, 2026-09-04)

Pattern: `model: opus|sonnet|haiku|fable`, `model=`, `"model"`, `model parameter`, `session model`, `inherit the session`. Full matching lines:

```
skills-claude/methodology-critique/SKILL.md:68:Validate every edited surface per the AGENTS.md ladder. Forward-test with blind, non-mutating subagent proxies aimed at whatever instruments changed, crewed under the rig's model rule — Sonnet by default, never the session model; a proxy pass is uptake evidence, never value evidence, and simulated assent is noise twice over. Grade whatever proxies cannot reach as untested, honestly, in the commit message.
plugins/decide/skills/deliberate/SKILL.md:29:Each stage runs as a fresh agent with its own context, dispatched with a brief the orchestrator composes from `00-setup.md` and the previous stage's output file. On Claude Code, pass `model: opus` on every stage dispatch unless the user names a model; on another runtime, use its subagent model setting. Opus is the default because a run is five long dispatches. The fresh context is what keeps the user's lean, and each stage's reasoning, out of the stages that must not see them. Where the runtime cannot dispatch a fresh agent, run the stages in this context in order, still writing every file, and say in the close that the stages were not isolated.
```

Read this as: which skills currently say anything about the model their dispatches run on. A skill absent from the list dispatches under the global rule alone. Two skills carry their own dispatch-model rule: `methodology-critique` (Claude-only) puts its forward-test proxies on Sonnet by default and says "never the session model"; `deliberate` puts its five judgment stages on Opus. Both sit beside the global rule today. No other skill names a model.
