# Implementation Plan: `skill-squad` — orchestrated discovery for skill design

**Status:** ready to execute · **Date:** 2026-06-23 · **Source:** locked design
`docs/specs/2026-06-23-skill-squad.md` (commit `300a4dc`), itself the product of this session's
`outcome-interviewer` → `making-recommendations` → `design-exploration` chain. **Class:** local
`skills-claude/` skill — build-and-prune, **not** a charter event, **not** plugin-distributed (so **no**
version bump / Codex republish / mirror). Executor authority is **not** granted by this plan; hand to
`execute-plan` for a run.

## What this builds

One Claude-only skill, `skill-squad`, at `skills-claude/skill-squad/SKILL.md`. It is a **prose
discovery protocol** (Approach A) — it provokes the invoking agent to author a fresh multi-agent
**Workflow** per design; it does **not** embed a Workflow script. Single `SKILL.md`, no reference files
(add one only if the body outgrows itself during the gate step). The skill produces an approved skill
*design* and stops; it does not author the designed skill's `SKILL.md`.

## File structure

| Path | Created/modified | Single responsibility |
| --- | --- | --- |
| `skills-claude/skill-squad/SKILL.md` | created | the entire skill contract: routing description + the discovery protocol |
| `~/.claude/skills/skill-squad` | created (symlink, outside the repo) | Claude delivery; points to the repo source via `claude-skills-sync.sh --link` |
| `docs/plans/2026-06-23-skill-squad.md` | this file | the plan |

No other files change. The skill references no `references/`, `examples/`, or scripts, so there is no
path-resolution surface to wire.

## Conventions the executor needs (zero-context primer)

- **Branch / hook:** A user-level `require-gitflow` hook **blocks all edits on `main`**. Execute on a
  non-protected feature branch. This work continues on **`feature/skill-squad-spec`**, which already
  carries the spec commit `300a4dc`; the build commits stack on top and land together in one
  fast-forward merge. Protected branches (never commit on them): `main`, plus `master`/`develop`/
  `release/*`.
- **Delivery:** `skills-claude/` is Claude-only (Codex never scans it). A skill goes live for Claude via
  a symlink in `~/.claude/skills` created by `scripts/claude-skills-sync.sh --link <name>`; the source
  edit itself is the live skill for future invocations.
- **Validation ladder:** structural validator is
  `python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>`. Its
  schema lacks some valid Claude fields (`argument-hint`, `disable-model-invocation`) and emits an
  "unexpected key" complaint for them — that specific complaint is **accepted**, never fixed by deleting
  the field. `skill-squad` uses neither field, so it should not even surface. Treat any **other** failure
  as real.
- **Deletion:** use `trash <path>`, never `rm`.
- **Commits:** conventional-commit subjects (`type(scope): summary`), explanatory body, end with the
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` trailer. Commit completed
  focused work by default; review `git diff --cached --stat` before committing.
- **No publish:** do not push, open PRs, or sync anything unless the user explicitly asks. Landing
  (FF-merge) is the user-gated final step (Task 8).

---

## Task 1 — Confirm branch and clean tree

Verify the execution context before any edit (the hook will block edits if you are on `main`).

```bash
cd /Users/jp/.agents
git rev-parse --abbrev-ref HEAD     # expect: feature/skill-squad-spec
git status --short                  # expect: no output (clean tree)
ls -d skills-claude                 # expect: skills-claude
test ! -e skills-claude/skill-squad && echo "OK: skill-squad does not yet exist"
```

Expected: branch is `feature/skill-squad-spec`, tree clean, `skills-claude/` present, and
`skill-squad` not yet created. If the branch is `main`, create the build branch first:
`git switch -c feature/skill-squad` (then use that branch for the rest of the plan).

## Task 2 — Author `skills-claude/skill-squad/SKILL.md`

Create the directory and write the file with **exactly** the content below. This is the entire skill.

```bash
mkdir -p /Users/jp/.agents/skills-claude/skill-squad
```

Write `/Users/jp/.agents/skills-claude/skill-squad/SKILL.md` with this content verbatim:

````markdown
---
name: skill-squad
description: "Use when you want to design a new skill (or materially redesign one) by orchestrating a multi-agent discovery run — fan out genuinely different approaches, beat them against a blind built-ins-only control, adversarially verify, and return a chosen design with an honest discovery-vs-control differential. Claude-only; expensive by design. Do not use for conversational or general design (design-exploration), judging whether proposed structure is justified (agent-facing-design), measuring an already-built skill (skill-benchmark), adversarial critique of an existing skill (scrutinize-skill), or hand-authoring the SKILL.md itself."
---

# Skill Squad

Design a skill by sending a squad of agents to *discover* one — not to confirm the
design you already have. The value is discovery: surfacing an approach, or a flaw,
you would not reach alone. Everything else here serves that, including the one hard
rule that keeps a discovery honest — it has to beat a control that never saw it.

This skill runs an expensive, multi-agent **Workflow**, and is Claude-only. It stops
at an approved *design* and hands off to hand-authoring; it does **not** write the
`SKILL.md`.

## When To Reach For It

Reach for it when a skill is worth designing well and you suspect your first instinct
is not the ceiling — a genuinely open design space, a skill you have rewritten before,
or one where getting the shape wrong is costly. For a small or obvious skill,
hand-author against `agent-facing-design` and skip the squad; the run is not worth its
cost.

## Before You Spawn

Invoking this skill is not authorization to spawn the squad. A real run is many agents
and can cost hundreds of thousands of tokens (a comparable design run was 14 agents; a
library sweep, 62). So:

- State the intended scale and rough budget before launching.
- Scale the discovery fleet to the design's openness and the budget you have — more
  genuinely-different approaches for a wide-open skill, fewer for a narrow one. The
  control ensemble stays fixed (below).
- If multi-agent orchestration is not already authorized for this session, ask once
  before launching.

## The Run

Author a fresh Workflow for the design in front of you — do not reach for a fixed
pipeline. Five moves; the order matters, the agent counts do not.

**1 — Set the bar, blind.** Before anything else, an independent arm writes the design
a careful agent reaches *with no squad* — the control. Keep it blind: it sees only the
design problem, never the squad's approaches. Run the control as an ensemble of 2–3,
not one, so the bar is not a single lucky or unlucky draw; the bar to beat is the
*strongest* control, not the average. This baseline is not empty — it is a careful
agent plus this repo's doctrine; call it the "careful-default," never "no skill." (This
is the same honesty `skill-benchmark` keeps about its baseline — borrow the principle,
not its `claude -p` machinery, which needs a built skill this stage does not have.)

**2 — Spread genuinely-incompatible approaches.** Fan out generators, each seeded with
a governing commitment the others would call *wrong* — not a restatement in new words.
The forcing question for the spread: would the author of approach B say approach A is
the wrong shape, or merely a variation of theirs? If they are variations, the spread
failed — widen it.

**3 — Try to kill each survivor.** Hand the approaches to independent skeptics —
delegate to `scrutinize-skill` for the adversarial read; do not hand-roll a critique.
Two rules make it honest: an approach is never graded by its own author (kills the
blind spot the authors cannot see), and the skeptic favors the simple-and-right over
the elaborate-and-clever (kills the dazzle that lets the best-argued beat the best). A
design advances only by surviving a real refutation, never a rubber-stamp.

**4 — Pick the strongest, then run the decisive comparison.** Pick the strongest single
surviving approach. A *merge* is allowed only under the Hybrid rule below — never as a
default compromise. Then put the winner head-to-head against the blind control, judged
by an arm that saw neither side's authorship. The product of this move is not "the
design" — it is the margin: does the winner genuinely beat the careful-default, and on
which axes?

**5 — Report the margin, including the honest null.** Two outcomes, both wins:
- **Beat** — a design that genuinely beats the careful-default, with the margin and the
  axes it won on.
- **Marginal** — the careful-default holds. Say so plainly, and show the proof: the
  best thing the squad surfaced, and why it did not clear the bar. A run that honestly
  reports "your instinct was right, here is what survived trying to beat it" has done
  its job.

## Hybrids: One Spine, Not A Blend

The best design is often a hybrid — but only one kind is real, and the difference
decides whether you crown it or kill it:

- **A blend of spines is mush.** Averaging philosophies and grafting everyone's good
  parts produces something more elaborate than any single approach — exactly the dazzle
  move 3 exists to kill. Reject it.
- **One spine plus justified grafts is a resolution.** One approach's philosophy wins
  and governs; rival elements are imported only as subordinated, individually-justified
  grafts. A real resolution often *subtracts* — it is simpler than the approaches it
  drew from, not a superset of them.

Three rules keep a hybrid honest:

1. It is a candidate, not a compromise — it re-enters move 3 and faces the skeptics like
   any approach. Synthesis does not launder it past the kill step.
2. You must name its single spine in one sentence, and say why each graft is a
   deliberate import. If you cannot, it is mush.
3. It must beat the best *parent* it was built from, not only the control. A hybrid that
   beats the careful-default but ties or loses to the strongest single approach is
   needless elaboration — the parent wins, and the hybrid is reported as
   considered-and-rejected.

## What This Skill Will Not Do

The discovery and the margin are judgments the squad argues, not numbers it computes.
This skill does not score approaches, does not classify "is this a discovery," and does
not make you fill fixed fields to feel done. If you find yourself building a rubric or a
scoreboard, you have turned a discovery engine into the bureaucracy it exists to
replace. The only hard machinery is the control discipline — blind, ensemble,
validity-checked — because a corrupted control fakes a discovery, and that is the one
failure that destroys the run's whole point.

**Validity check before you trust the margin.** Confirm the control was genuinely
independent (it never saw the squad's work) and genuinely hard (a real careful attempt,
not a strawman the squad could trivially beat). If either is in doubt, report the
differential as unreliable rather than claiming a margin.

## Where It Stops

The deliverable is an approved *design*: the chosen approach and its shape, the key
decisions and open risks, the margin (or the honest null), and what got killed and why
— so the breadth is visibly real. It stops there.

It does not write the skill. Hand the design to hand-authoring against
`agent-facing-design` and `skill-ux-design` (this repo keeps no Claude-side constructor
by design). After the skill is authored, prove it with `behavior-smoke-test` and, if you
want numbers, `skill-benchmark`. Skill-squad is the front of that pipeline, not the
whole of it.
````

Verify the file landed:

```bash
test -f /Users/jp/.agents/skills-claude/skill-squad/SKILL.md && echo "OK: file written"
head -4 /Users/jp/.agents/skills-claude/skill-squad/SKILL.md   # expect frontmatter: ---, name:, description:, ---
```

## Task 3 — Gate the draft through `agent-facing-design`

The draft was written to pass the gate, but the spec flags prose-shape as the top risk, so verify it
explicitly — this is judgment work, not a command. Load `agent-facing-design` and apply its
**Two Kinds of Skill** lens to the file, per part:

- **Judgment core** (the protocol, the spread, the hybrid rules): confirm every piece *provokes*
  (forcing questions, the kill step, the forced head-to-head) rather than *substitutes* (no scoring, no
  classifier, no fill-in fields, no fixed agent count). The "What This Skill Will Not Do" section is the
  self-check; confirm it is true of the body.
- **Trust core** (the control discipline + validity check): confirm the machinery is narrow and
  justified by a real failure (a corrupted control fakes a discovery), and that it is **single-sourced,
  not copied** — the backstop delegates to `scrutinize-skill`, and the baseline-honesty borrows
  `skill-benchmark`'s principle without cloning its `claude -p` mechanics.

Tighten any wording where the draft makes the judgment *for* the agent or hedges a forcing function into
a suggestion. Tighten the `description` only for routing precision if it reads long against close
neighbors (`design-exploration`, `agent-facing-design`, `skill-benchmark`, `scrutinize-skill`); do not
pad it. Apply edits inline to the file. Expected outcome: the draft survives with at most wording
tightening; if the gate demands a structural change (a removed section, a de-scored mechanic), apply it
and note it in the commit body.

## Task 4 — Structural validation

Run the validation ladder against the edited file.

```bash
cd /Users/jp/.agents
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills-claude/skill-squad
echo "validator exit: $?"
```

Pass condition: exit `0`, reported valid. `skill-squad` uses only `name` + `description`, so the accepted
`argument-hint`/`disable-model-invocation` "unexpected key" complaint should not appear; any other
structural error (missing/!malformed frontmatter, name≠dir) is a real failure — fix it and re-run.

Confirm `name` matches the directory and the frontmatter parses as YAML:

```bash
python - <<'PY'
import pathlib, yaml
p = pathlib.Path("skills-claude/skill-squad/SKILL.md")
fm = p.read_text().split("---", 2)[1]
d = yaml.safe_load(fm)
assert d["name"] == "skill-squad", f'name mismatch: {d["name"]!r}'
assert isinstance(d["description"], str) and d["description"], "missing description"
print("OK: frontmatter parses; name == skill-squad; description present")
PY
```

Whitespace check (intent-to-add so the new file is visible to `git diff`):

```bash
git add -N skills-claude/skill-squad/SKILL.md
git diff --check; echo "diff --check exit: $?"   # expect: exit 0, no output
git reset -q skills-claude/skill-squad/SKILL.md
```

Referenced-path check: the skill references no `references/`, `examples/`, or scripts, so there is no
path surface to verify. State that explicitly rather than skipping silently.

## Task 5 — Link into `~/.claude/skills` and verify delivery

```bash
cd /Users/jp/.agents
scripts/claude-skills-sync.sh --link skill-squad
ls -la ~/.claude/skills/skill-squad     # expect: symlink -> /Users/jp/.agents/skills-claude/skill-squad
scripts/claude-skills-sync.sh --check; echo "check exit: $?"
```

Pass condition: `--link` creates `~/.claude/skills/skill-squad` as a symlink to the repo source; `ls`
shows the link resolving; `--check` exits `0` (managed-skill invariant holds). The script never deletes;
if `--check` reports a *pre-existing, unrelated* violation, resolve that separately and do not let it
block — the skill-squad-specific expectation is that its own link is present and correct.

## Task 6 — Behavior smoke test (forward proof)

Prove a future agent following this contract actually adopts the protocol — structural checks only show
the file loads. Use `behavior-smoke-test`'s context-isolated subagent proxy. **Authorization:** spawning
a subagent is a separate permission; if it is not already authorized for the session, ask one permission
question before spawning. Keep the proxy non-mutating.

- **Behavior claim (first-move):** Under the `skill-squad` contract, given a request to design a
  non-trivial new skill plus pressure to "just give me the design quickly," the agent's first move is to
  (a) flag the cost/authorization stop, (b) set up a blind careful-default control, and (c) frame the
  deliverable as a discovery-vs-control differential including an honest-null option — rather than
  directly proposing one design.
- **Scenario (pressured toward the old behavior):**
  > "I want a new skill that helps an agent decide when to split a big refactor into multiple PRs vs.
  > keep it as one. The design space is wide open. Just give me the design quickly — don't overthink it
  > or spin up a bunch of agents."
  The pressure ("quickly," "don't spin up agents") pushes toward skipping the squad; the design is
  genuinely open, so the squad is warranted.
- **Harness:** context-isolated subagent proxy, `fork_context: false` if supported. Give the proxy the
  `skill-squad` `SKILL.md` as its contract plus the scenario. Use `behavior-smoke-test`'s default
  first-move proxy prompt (act, state next action; do not explain, do not grade, do not mutate). Do not
  tell the proxy the grading claim or the expected answer.
- **Grade in the parent (the proxy does not grade itself):**
  - `passed` — the proxy's next move sets up / plans a blind control and frames a differential (incl. the
    honest-null), and surfaces the cost/authorization stop.
  - `failed` — the proxy just produces a single design with no control and no differential.
  - `not strong enough` — ambiguous, or the proxy only restates the contract.
- **Proof boundary:** this proves the first-move stance (control + differential + cost-stop), **not** that
  a full multi-agent run executes or yields a good design. Report in `behavior-smoke-test`'s shape
  (`Behavior claim`, `Scenario`, `Harness`, `Result`, `Observed behavior`, `Why`, `Structural checks`,
  `Proof boundary`, `Durable artifact`). The scenario is temporary; persist a `docs/smoke-tests/` artifact
  only if it caught a failure or the user asks.

If `passed`, proceed. If `failed` or `not strong enough`, fix the contract (usually a dulled forcing
function in Task 2's wording), re-gate (Task 3), and re-run.

## Task 7 — Commit

```bash
cd /Users/jp/.agents
git add skills-claude/skill-squad/SKILL.md
git diff --cached --stat        # expect: only skills-claude/skill-squad/SKILL.md
git commit -F - <<'EOF'
feat(skill-squad): add orchestrated skill-design discovery skill

skills-claude/skill-squad (Claude-only): a prose discovery protocol that
provokes the agent to author a fresh multi-agent Workflow to DESIGN a skill —
spread genuinely-incompatible approaches, beat them against a blind ensemble
careful-default control, adversarially verify (delegating to scrutinize-skill),
and report a discovery-vs-control differential. Headline is a genuinely-better
design + margin OR an honest null ("your default holds, here's what survived
trying to beat it") — both wins. Stops at a design; does NOT write the SKILL.md
(no Claude-side constructor by design).

Mixed skill per agent-facing-design: the discovery core stays on the provoke
side (no score, no classifier; the differential is argued, not computed);
machinery only in the blind-control discipline + validity check. Single-sourced,
not copied: backstop delegates to scrutinize-skill; baseline honesty borrows
skill-benchmark's "baseline is not empty" principle, not its claude -p mechanics.
Ensemble-always control (beat the strongest member); hybrids = one-spine-plus-
justified-grafts that must beat the best parent. Cost/authorization stop:
invoking != authorized to spawn.

Design: docs/specs/2026-06-23-skill-squad.md. Build-and-prune (a skill): not a
charter event, no ledger entry. Local skills-claude/ skill: no plugin train.

Verified: quick_validate clean; frontmatter parses, name==dir; diff --check
clean; claude-skills-sync --link + --check OK; behavior-smoke-test forward proxy
<RESULT> on the first-move control+differential claim.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
git log -1 --format='%h %s'
```

Replace `<RESULT>` with the actual Task 6 result before committing (`passed`, or the honest
classification). Do not write `passed` unless Task 6 returned it.

## Task 8 — Land (user-gated)

Landing and publishing are **not** authorized by this plan. When the user asks to land:

- Route through `closeout-check` (final verification) then `merge-branch` to fast-forward
  `feature/skill-squad-spec` (carrying both the spec `300a4dc` and the build commits) onto `main`.
- Pushing `main` is a **separate** explicit authorization — do not push otherwise.
- This is a local `skills-claude/` skill: there is **no** version bump, Codex republish, or mirror.
- Optional cleanup after landing: `git branch -d feature/skill-squad-spec` once merged.

---

## Self-review

- **Coverage** — every spec requirement maps to a task: the SKILL.md + prose-protocol shape and all
  settled content (5 moves, ensemble control, hybrid rule, differential output, delegated backstop, cost
  posture, stops-at-design) → Task 2; `agent-facing-design` gate → Task 3; structural ladder → Task 4;
  sync `--link`/`--check` → Task 5; `behavior-smoke-test` forward proof → Task 6; commit-by-default →
  Task 7; FF-merge/land (push gated) → Task 8; single-sourcing + local-skill/no-train → Task 2 content +
  Task 3 gate + preamble.
- **Placeholder scan** — no `TBD`/`similar to`/`add error handling`; the full SKILL.md content is inline;
  the one intentional fill-in (`<RESULT>` in the commit body) is gated on Task 6's real result, with an
  explicit "do not write passed unless returned" guard.
- **Consistency** — `skill-squad`, `skills-claude/skill-squad/SKILL.md`, the validator path, and the
  sync commands are identical across tasks; the SKILL.md's own internal references (`scrutinize-skill`,
  `skill-benchmark`, `agent-facing-design`, `skill-ux-design`, `behavior-smoke-test`) all name skills
  that exist in this repo.

## Handoff

Executor: `execute-plan` (in-session, task-by-task) — execution is a separate authorization not granted
here. The plan assumes the spec branch `feature/skill-squad-spec`; confirm Task 1 before editing.
