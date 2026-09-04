# Literal Language Sweep — JP-facing skill bodies

2026-09-04. Follow-on to `2026-08-08-register-sweep.md` (which measured the habit and produced the rule) and to commit `fabc8e9` (which first applied the rule to a skill body, `braindump`).

## The question this answers

The 23:51 handoff of 2026-09-03 left it open: should the Literal Language pass be applied to other JP-facing skill bodies as a deliberate sweep, or only as each skill is next touched? JP chose the sweep.

## What "JP-facing" turned out to mean

The rule is a **replies** rule. The register sweep measured only "the sentences I wrote directly to JP — no tool calls, no code, no subagent traffic," and the rule text was written for that. So a sweep of all 124 skill bodies (about 150,000 words) would extend the rule well past what it governs.

The empirical middle used here: the skills whose bodies **name JP directly** — nine, of which `braindump` was already done and `claude-home-audit` mentions him only in its routing description. That leaves seven, and they split on a line that matters:

- **Four whose text becomes, or shapes, the words JP reads.** `reality-check`, `reflect`, `email-writing`, `transcript-export`. `reality-check`'s output-shape bullets are echoed in the reply itself; its `examples/calibration.md` "Good response" blocks are literally Claude's modeled words to JP. This is the `braindump` case repeated, and the rule applies at full strength.
- **Three that tell an agent how to run a process.** `methodology-check`, `methodology-critique`, `gap-review`. Their text is machinery, not reply text, and their vocabulary has a committed record (below).

Only the first group was changed.

## Method

One Claude workflow, 14 agents: one sweep agent per skill applying the contract's own test sentence by sentence, then one adversarial checker per skill whose default was to refute, briefed on the repo's settled names and required to grep each quote before accepting it. Checkers also reported what the sweeps missed.

Totals: **166 proposed, 124 confirmed, 48 more found by the checkers.** The 25% refutation rate is low against the `gap-review` benchmark (50% reads as the instrument working), and 31 of the 42 refusals were "the flag is fair but the wording is worse" rather than "not a violation" — so the checkers were soft on whether something was a violation and strict only on the replacement. Every finding applied below was re-judged by hand against the live file; several were dropped, several were rewritten, and several consistency fixes were added that neither agent proposed.

## What was applied

| Skill | Commit | Files | Notable |
|---|---|---|---|
| `reality-check` | `774898f` | SKILL.md, agents/openai.yaml, examples/calibration.md | "read" as a noun removed from all six uses; calibration.md's modeled replies restated |
| `reflect` | `791c285` | SKILL.md | rising-into-view words ("surfacing"/"surfaced"/"emerged") removed from all six uses; two one-file-two-senses collisions closed |
| `email-writing` | `c1fe234` | SKILL.md | tone vocabulary restated, but "warm" kept |
| `transcript-export` | `51ea497` | SKILL.md | "artifact" removed — it also names a different Claude Code feature |

No obligation was added, removed, or lightened in any of the four. Each commit message carries its own preservation walk and evidence.

### Words kept on purpose

The contract's fourth bullet ("names of real things stay as names") and the `braindump` precedent for "empty his head" both carried weight:

- **`land` / `lands` / `landed`** in `reflect`, for writing and committing an entry. `land` is a real skill in this library; changing it in one skill alone would put that skill at odds with the rest.
- **`warm` / `warmth`** in `email-writing`. A temperature word, but it is JP's own framing in the description and the skill's core vocabulary. Replacing it would rewrite the skill rather than restate it.
- **The quoted user line** in `calibration.md` ("I buy the reframe"). The contract governs Claude's words, not JP's.

## What was held, and why

`methodology-check`, `methodology-critique`, and `gap-review` were swept but not changed. The sweep proposed 99 changes across them and the checkers confirmed 74 — a rewrite, not a restatement, of `methodology-critique` in particular (41 confirmed plus 14 more on a 1,766-word skill).

The reason to hold is not volume. It is that their vocabulary is **the settled terminology of a committed record**:

- `seam` appears in ten or more committed briefs under `docs/reviews/`.
- `landing train` appears in `docs/agents/contract-decisions.md`, an append-only ledger whose settled entries are never rewritten.
- The genre's own TLDR signature ("the Nth hold, with a shape none of the prior holds had") appears in ten or more briefs.

Rewording these inside the skills would make each skill disagree with the 35-brief record it produced and with a ledger entry that cannot be revised to match. The adversarial checkers caught only four of these; the rest surfaced from grepping `docs/` directly.

`## First Move` is a smaller instance of the same class: `transcript-export` and `plan-panel-loop` share the heading, and only the former was changed, so the two now differ.

## The held three: JP chose option 3, and it was applied

JP chose to restate only the sections describing what he receives and decides, leaving the run machinery in its own terms.

| Skill | Commit | Sections restated | Sections left alone |
|---|---|---|---|
| `gap-review` | `5407ff2` | Phase 3 (Report and Stop), Close Packet, Boundaries, plus the two report-label mentions in `references/review-prompts.md` | Phase 0, Phase 1, Phase 2, the rest of `review-prompts.md` |
| `methodology-check` | `f38bdd4` | frontmatter routing, Verdict and escalation, Aftermath, Routing | the altitude test, First move, Evidence, Findings |
| `methodology-critique` | `6971e12` | frontmatter routing, the opening framing, the Phase 0 dossier shown in chat, the Phase 2 brief floors, Phase 3 adjudication | Session Spanning, Phases 1 and 4–6, all of `references/evidence-recipe.md` |

### The rule that made option 3 work

A JP-facing section often uses a term the machinery defines. Renaming it in one place and not the other would split the file's vocabulary — the same defect this sweep exists to remove.

The resolution came from the contract's own fourth bullet: **names of real things stay as names, and get their plain meaning stated at first use.** So `the anchor`, `escalate-rider`, `the graded census`, `the treatment`, `a hold`, `an inversion`, and `the stop is a seam` all survive as names, each now followed by a short plain gloss where JP meets it. Nothing was renamed across a section boundary.

This also protected the committed record: `seam`, `landing train`, `hold`, `inversion`, `the rig`, and the house TLDR signature all still stand in `methodology-critique`, so the skill continues to agree with the 35 briefs under `docs/reviews/` and with the append-only ledger entry.

### Left unfixed on purpose

`methodology-critique`'s description is 115 words, over the ~90 ceiling in AGENTS.md. It was 111 before this sweep. That is a routing-precision problem, not a wording one, and fixing it is a separate task.

`## First Move` still differs between `transcript-export` (changed) and `plan-panel-loop` (not swept).

## Bounds

- Seven skills inspected; four changed. The other 117 skill bodies were not read.
- The four changes were validated structurally (`quick_validate.py`, YAML and frontmatter parses, referenced paths, `git diff --check`) and by a leftover-image grep per skill. No forward test was run: unlike `fabc8e9`, which had a two-arm preservation walk on `braindump`, these four were checked by reading the diff for moved obligations, not by running the skills.
- The confirmation rate above is evidence the checkers were soft, so the 124 figure should not be read as 124 real defects.
