# Deliberate run: setup

Run directory: /private/tmp/claude-501/-Users-jp--agents/264f264c-d4b3-42b7-ba4f-da0bee19cd65/scratchpad/deliberate-dispatch-rule-2026-09-04
Date: 2026-09-04
Invoked by: JP, interactively, in a Claude Code session on Fable 5.1, from /Users/jp/.agents on main at fabc8e9. First interactive run of deliberate 2.x on a real decision.

## Decision question

How should the conflict between two live instructions be resolved?

1. The always-loaded global rule in `~/.claude/CLAUDE.md`, section "Multi-Agent Dispatch": judgment stages dispatched as subagents "inherit the session model".
2. The `deliberate` skill's own rule (decide plugin 2.1.0): "On Claude Code, pass `model: opus` on every stage dispatch unless the user names a model."

Both are live today. In a Fable session the global rule's letter puts deliberate's five judgment stages on Fable; the skill's rule puts them on Opus. The question is what, if anything, to change so the two no longer contradict, and where the resolution should live.

## Candidates

JP supplied none.

Shapes already named in the repo record (inferred: sessions named them, JP did not):

- "Leave both as written; treat the skill sentence as the more specific instruction and the global line as governing every other dispatch." (The sessions' working reading since 2026-09-03 16:19.)
- "Mirror the Opus default into the global CLAUDE.md." (Declined on 2026-09-03 by the session as an always-loaded edit JP did not ask for. Not declined by JP.)

Generate treats these as record-named seeds, not user candidates: list them in their exact wording, but they carry no user-supplied protection at Prune.

## Hard constraints

None confirmed by JP this session. Each below is taken from the repo record and marked `inferred`. Each names what it costs.

1. `inferred` — Editing any line of `~/.claude/CLAUDE.md` is a charter-gated event (docs/agents/charter.md: "authoring or retiring an always-loaded contract"). Cost: the charter's Admission or Retirement discipline, an argument that the line earns its always-loaded place, and one entry in docs/agents/contract-decisions.md with a durable evidence pointer. The file is not git-tracked, so the ledger commit is the durable pointer (2026-07-02 precedent).
2. `inferred` — Any behavior edit to `plugins/decide/skills/deliberate/SKILL.md` is a decide plugin release. Cost: a satellite lifecycle run, a version bump in lockstep with a CHANGELOG section, and the Codex republish the landed bump authorizes; mirror sync and push wait for JP's word.
3. `inferred` — `deliberate` is dual-runtime. The Opus rule is Claude-Code-only by its own wording ("on another runtime, use its subagent model setting"). A resolution must leave the Codex path working.
4. `inferred` — A JP-authored stated position reverses only on observed evidence, not principled argument (throughline, Decisions That Hold, 2026-09-01). Whether the global dispatch rule is JP-authored is itself inferred: it is written in JP's voice ("This overrides the harness's ... guidance"), the 2026-09-01 memory calls it "his global CLAUDE.md", and its authoring is not in the ledger. Cost: changing the global rule's substance needs observed evidence, and whether the 2.1.0 record counts as that is open.

## Values (all inferred from the record)

- Cost matched to the job. Both rules exist for this. JP's 2026-09-03 ask was how to put deliberate's subagents on Opus instead of Fable.
- No always-loaded edits nobody asked for. Ambient contracts are the class the charter gates hardest: no visible fire, no clean prune.
- One source for a rule, not copies. Where a copy is unavoidable the house pattern is one sanctioned copy with a drift check (scripts/check-protected-set.sh).
- JP reads every skill he invokes; deliberate's SKILL.md must stay readable (89 lines today).
- Plain, literal wording in anything JP reads.
- Behavior-shaping governors land staggered, not stacked.

## Evidence

Stages may read `00-evidence.md` in this directory (verbatim excerpts of every text named above) and may read these local files read-only: `~/.claude/CLAUDE.md`, `/Users/jp/.agents/plugins/decide/skills/deliberate/SKILL.md`, `/Users/jp/.agents/plugins/decide/CHANGELOG.md`, `/Users/jp/.agents/docs/agents/charter.md`. No web research.

## Survivor count

About four (default).

## Stage model

Opus on every stage dispatch (deliberate 2.1.0 default; JP named no model). Orchestrator: Fable 5.1, this session.

## Lean

JP stated none. `inferred` — the record's standing reading, held by sessions since 2026-09-03 16:19 and never ratified by JP: leave both unedited; the skill sentence is the more specific instruction. JP's one observed act on the matter: on 2026-09-03, asked how to move the stages to Opus and shown four routes (per-call Agent `model`, subagent definition `model`, `CLAUDE_CODE_SUBAGENT_MODEL`, session model), he chose the skill-text route.
