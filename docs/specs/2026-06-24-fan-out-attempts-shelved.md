# Design Record: `fan-out-attempts` — best-of-N task execution (SHELVED)

**Status:** approved-but-thin design, **SHELVED — not built** · **Date:** 2026-06-24 · **Source:** a `skill-squad` discovery run (`wf_599a2ab1-5c1`, 17 agents, ~760K tokens) followed by a dedicated 3-skeptic kill pass. Build-and-prune class (a skill): **not a charter event**, no ledger entry owed.

## Decision: shelved, with a revive trigger

This design is captured but **deliberately not built**. The discovery run produced a modest *relative* win (the squad design beat the careful-default control 2–0 in a blind head-to-head), but a dedicated adversarial kill pass — run precisely to close the gap that the head-to-head never re-scrutinized the crowned hybrid on its own merits — came back **2 KILLED + 1 SURVIVES-WITH-SURGERY**, converging from two independent lenses on the same honest verdict: this is a **narrow-trigger, marginal-differential skill** — buildable under build-and-prune, but a fast prune candidate, and thinner than `explain-codebase` was.

The deciding consideration was not a flaw in the design. It was the library state: there is already a **growing stack of shipped marginal-differential skills with zero real-world fire** (`explain-codebase`, `release-cut`, the four Era-13 builds). `fan-out-attempts` would be the thinnest of them. Minting a third-tier prune candidate before the existing ones have earned their keep is the questionable move, more than anything wrong with the design.

**Revive trigger:** revisit this design if either (a) you hit a real best-of-N task in the wild where you genuinely wished you had this lane, or (b) `explain-codebase`/`release-cut` demonstrate real-world value, validating that marginal-differential builds earn their slots here. If revived, the design below is build-ready — hand-author it against `agent-facing-design` + `skill-ux-design`, carrying the validity surgery already folded in.

## The job it would own

A reusable agent capability that dispatches N *independent parallel attempts at ONE task*, then selects the single best result by an *objective fan-in signal* — "best-of-N" / parallel solution exploration (~N× token cost for a quality lift on hard, gradeable tasks). Originally proposed in the 2026-06-19 capability-growth review (since superseded by `docs/reviews/2026-06-26-skill-library-capability-growth-review.md`): "Claude-only v1, PICK-ONE, gate hard on 'objectively gradeable,' cap concurrency, state the ~N× cost before dispatch." No skill owns it: `execute-plan` runs one subagent per *distinct* plan task in sequence (a different shape); `prototype` is one throwaway exploration.

## The crowned design (validity surgery applied)

This is **Approach A (the gate)** as the governing spine, with three subordinated grafts, plus skeptic 2's validity surgery from the dedicated kill folded into step 1. The result is *simpler* than its parents — no selector taxonomy, no economics layer, no variance-engineering layer.

**Spine (one sentence):** `fan-out-attempts` is an objective-fan-in gate — it refuses the ~N× best-of-N spend unless the task carries a pre-committed, runnable signal **with a fixed pass threshold and a stated blind spot**, and only once that signal is sealed does it dispatch N independent attempts and PICK-ONE winner by it.

**Shape:** a one-screen prose decision-gate-plus-thin-dispatch — not a framework, not a wrapper, not a fresh-Workflow-per-task generator. Mostly a *trust* skill (predictable shape: same gate, same cost line, same PICK-ONE output) with one *judgment* moment (is this task actually gradeable by a valid signal?).

**What the agent does, start to finish:**

1. **Pre-commit the signal — or stop.** Name the executable that emits an objective per-attempt verdict (a passing test suite / pass-rate, a typecheck, a benchmark number, compiles-and-runs, an exact-match oracle). Then — this is the validity surgery, and it is the load-bearing organ — pre-commit, before seeing any attempt: the **fixed pass threshold** the winner must clear, and one sentence stating **what a passing score would fail to catch**. A signal whose threshold the agent cannot state up front, or whose blind spot is "nothing," is rejected. This kills the gameable case the bare "is it a runnable command?" test admits (e.g. `ruff check --statistics` is runnable, deterministic, and authorship-blind, yet measures nothing about task success; a flaky pass-rate is non-reproducible). The gate tests signal *validity*, not just mechanical *objectivity*. If no signal survives this, STOP: output "this is not a fan-out-attempts task" and route out — **do not improvise a rubric-judge** (that is `skill-squad`'s lane).
2. **State cost + cap.** One line before dispatch: "N attempts at ~N× the single-attempt token/time cost; concurrency capped at C." Default N=3.
3. **Spread for independence.** Each attempt is a fresh, mutually-blind worker given the bare task and the sealed signal — no shared scratch, no sight of siblings; vary the lever where the task admits it (starting file, algorithm family, framing). Dispatch is **availability-conditional** (the repo idiom — `execute-plan`'s "subagent mode when available, else inline"; `improve-codebase-architecture`'s "exploration subagent when the runtime offers one… otherwise explore directly"): author a parallel best-of-N Workflow when the runtime offers parallel fan-out, else spawn N subagents via the Agent/Task tool, else run sequentially inline. **No hardcoded `parallel()`** — it is the Workflow-DSL hook the orchestrator uses, not a callable a fired skill can assume (verified: zero hits in any live skill body).
4. **Detect collapse.** When results return, check whether the attempts actually diverged or all failed the same way; a collapsed pool is N× spend for ~1× diversity — say so rather than crowning a winner from it.
5. **Fan in objectively, PICK-ONE.** Run the named command against every attempt; the command decides against the pre-committed threshold. Return the single highest-scoring **intact** attempt — never merge, splice, or take "the best parts of two" (a blend has been graded by nothing and re-imports the taste the gate excluded). If no attempt clears the threshold, report "none passed" — do not force a winner.
6. **Report the margin.** Winner's signal value, the runner-up's, and N actually spent. If the signal cannot separate them, say best-of-1 would have done — so the user sees whether the N× bought anything.

**Use when:** one concrete hard task with a pre-committable objective pass/fail or numeric signal (fixed threshold + stated blind spot), hard enough that one attempt often misses, and a best-of-N lift worth ~N×.

**Do not use — fences:** vs `skill-squad` (interchangeable attempts + a runnable signal here; genuinely-incompatible approaches + argued judgment against a blind control there — "if your selector is an argument, it's skill-squad; if it's a command that returns a number or a pass/fail, it's this"; when no valid signal exists, route *to* skill-squad, do not improvise a judge here); vs `execute-plan` (N attempts at *one* task, not one subagent per *distinct* task); vs `prototype` (a graded winner, not a throwaway learning); vs **bare subagent dispatch** (which will fan out an ungradeable task, hide the N× cost, let attempts contaminate each other, and let you blend winners).

**The one thing whose removal makes it not-this-skill:** the pre-committed runnable-signal gate (a signal + fixed threshold + stated blind spot, sealed before dispatch) and PICK-ONE selection by it. Remove it and you have either bare subagent dispatch (no skill) or a rubric-judged pick (skill-squad's shape).

## Discovery record — the `skill-squad` run (`wf_599a2ab1-5c1`)

Five genuinely-incompatible spines fanned out against a blind 3-agent careful-default control ensemble; each approach torn at by a `scrutinize-skill`-disciplined skeptic; strongest survivor picked; blind counterbalanced head-to-head vs the strongest control. Integrity gates passed: 3 controls produced, all 5 approaches reached a substantive quotable critique, `marginReliable: true`.

**The five approaches and what happened to each:**

- **A — gate** (objective-gradeability gate is the spine): SURVIVES-WITH-SURGERY. Became the governing spine of the crown.
- **B — selector** (build a trustworthy selector across a gradeability spectrum): **KILLED** — its rubric-judge tier is `skill-squad`'s blind-judge machinery re-implemented (One-Owner collision); its only clean slice (a hard automated oracle) collapses back into A.
- **C — economics** (the N× spend decision is the spine): SURVIVES-WITH-SURGERY but lost on spine honesty — its own removal-test showed the load-bearing organ is gradeability, not cost. Its cost-disclosure line survives as a graft onto A.
- **D — diversity** (engineering uncorrelated attempts is the spine): SURVIVES-WITH-SURGERY but its variance-engineering core is lifted from `skill-squad`'s move-2 spread test — double-ownership of the sibling's core. Its collapse-detection check survives as a graft.
- **E — minimal** (defer to the runtime `parallel()` primitive): **KILLED** — its spine rests on a callable primitive that does not exist for a fired skill (zero hits in live sources). Strip the phantom and it is bare subagent dispatch colliding with `execute-plan`.

**Head-to-head (the squad's own verdict):** the crowned hybrid beat the strongest control **2–0**, counterbalanced for position bias (judge-1 *clear*, judge-2 *marginal*). Both judges, with control/squad positions swapped, picked the squad design. The win was a *modest enrichment of a shared spine* — every approach and both controls converged on the same gate spine; the squad won on one execution detail (a concrete enforceability test the control left hand-waved) plus a factual correction (no callable `parallel()`).

**Honest caveat on that margin:** the workflow handed the judges the squad pick *with its adjudication scaffolding still attached* ("THE WINNER", "WHAT WAS KILLED", grafts), which both judges noticed — so the head-to-head was not perfectly provenance-blind. The discovery stands on its own merits regardless; the *margin* is softened.

## The dedicated kill — why this was shelved, not built

The crowned hybrid had only ever faced the two head-to-head judges, never a dedicated skeptic on its own merits (`skill-squad`'s Hybrid rule says a hybrid re-enters the kill step). Three independent `scrutinize-skill`-disciplined skeptics, distinct lenses:

- **Skeptic 1 (One-Owner) — KILLED:** "the boundary vs `skill-squad` is a relabel, not a mechanism… the gradeable-but-borderline middle evaporates." Recommended folding into `skill-squad`.
- **Skeptic 2 (enforceability) — SURVIVES-WITH-SURGERY:** the sharpest, most load-bearing finding — *"the gate's entire load-bearing test is self-administered and self-graded by the agent that wants the answer to be yes."* `ruff check --statistics` passes every literal clause of the original honesty test yet measures nothing. The gate tested mechanical objectivity, not validity. **Surgery: the pre-commitment (signal + fixed threshold + stated blind spot, fixed before any attempt) — folded into step 1 above.** This is the genuine improvement the kill produced.
- **Skeptic 3 (trigger-reality) — KILLED:** "a runnable authorship-blind ranker is, in practice, a test suite / benchmark / fuzzer… when you already have a green-bar oracle, dispatching a few attempts and keeping the passing one is what a careful agent does anyway." Value-add dismissed as ceremony.

**Adjudication (weighed against this repo's own doctrine):** two of the three kills lean partly on arguments this repo has explicitly voided. Skeptic 3's core ("changes nothing a careful agent wouldn't reach") is the **marginal-differential / prove-it-first** argument — the voided Era-19 anti-pattern; build-and-prune does not gate on outcome-proof. Skeptic 1's "fold into `skill-squad`" is a **category error**: `skill-squad` designs *skills* (judgment-selected); `fan-out-attempts` executes a *concrete task* (oracle-selected) — a shared *shape*, not the same *job*, and One-Owner keys on the job. What genuinely survives, stripped of the doctrine-invalid parts: (1) skeptic 2's real, fixable flaw and its surgery (carried), and (2) a confirmed honest expectation — narrow trigger, marginal differential, fast prune candidate. By the repo's rules the design **survives — but barely**, only with the validity surgery, as an acknowledged prune candidate. Combined with the stack of unproven marginal builds, that tipped to **shelve**.

## Methodological note (feedback for `skill-squad` itself, not yet applied)

This run is a clean data point that the **relative head-to-head can over-credit a design that shares the control's spine.** The bake-off asked "which is stronger" (squad won 2–0); the dedicated kill asked "does this earn a slot at all" (2 KILLED). The Hybrid-re-enters-the-kill rule is what caught it — worth treating as non-optional for crowned hybrids, not a nicety. Two concrete improvements `skill-squad` could adopt: (1) **strip adjudication scaffolding from the pick before the blind head-to-head** (this run leaked provenance because the pick carried its own "what I killed" narration); (2) **run the dedicated kill on the crown by default**, not only on request. These are notes for a future `skill-squad` edit, deliberately not made here.

## References

- `skill-squad` discovery run: `wf_599a2ab1-5c1` (task `wwjix8tf0`, 17 agents, ~760K tokens). Script persisted at `…/workflows/scripts/design-fan-out-attempts-wf_599a2ab1-5c1.js`; run outputs ephemeral.
- Dedicated kill: three `general-purpose` skeptics (agent ids `ac8adbcc22ec49305`, `a42bebba862791e8d`, `ae0d1900b4dfd7b1b`).
- Proposal source: the 2026-06-19 capability-growth review, rows 4 and 206 / build-order item 4 (superseded by `docs/reviews/2026-06-26-skill-library-capability-growth-review.md`).
- Neighbor contracts: `skills-claude/skill-squad/SKILL.md`, `skills/execute-plan/SKILL.md`, `skills/prototype/SKILL.md`, `skills/agent-facing-design/SKILL.md`.
