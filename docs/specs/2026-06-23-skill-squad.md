# Design Spec: `skill-squad` — orchestrated discovery for skill design

**Status:** approved design, ready for `implementation-planning` · **Date:** 2026-06-23 · **Source:** this session's `outcome-interviewer` → `making-recommendations` → `design-exploration` chain (Approach A, confirmed by JP). No discovery run has been executed yet — this is the design, not a build plan. Build-and-prune class (a skill): **not a charter event**, no ledger entry owed.

## What this builds

`skill-squad` is a Claude-only skill that designs a new skill — or materially redesigns an existing one — by orchestrating a multi-agent **discovery** run. It provokes the invoking agent to author a fresh Workflow that: fans out genuinely-different approaches, beats them against a **blind, ensemble control** (the design a careful agent reaches *without* the machinery), adversarially verifies the survivors, and returns a chosen design plus an honest **discovery-vs-control differential**.

Its headline output is one of two things, both wins:

- **Beat:** "here is a design that genuinely beats what you'd reach alone — by this margin, on these axes."
- **Marginal (honest-null):** "your default holds — and here is the proof it survived a real attempt to beat it."

It **stops at an approved design** and hands off to hand-authoring. It does **not** write the `SKILL.md`.

## Why — the outcome it serves

The settled outcome (from the interview): **more rigorous skill designs than are reachable ad hoc.** Not a capture of an existing process — JP already runs real design workflows (release-cut got a 14-agent run). The win is a higher *ceiling*: designs that come out better than the best he'd reliably reach by hand.

"More rigorous" resolved to two levers, with a clear center of gravity:

- **Discovery is the heart** — surface an approach or a flaw JP wouldn't reach alone.
- **The adversarial pass is a backstop**, not the main event — it keeps a discovery from being merely *seductive*. "Harder to fool" resolved specifically to two capture modes: authors blind to their own approach's flaws, and a judge dazzled by elaboration over correctness (JP leans simple-right beats clever-wrong).

The sharp constraint this design answers: across Eras 14–18 the repo's big orchestration runs kept coming out **marginal** — landing where a careful agent + `AGENTS.md` would already reach (release-cut, migration-campaign, pr-description). For a *discovery* skill, the whole game is exceeding that baseline, which means the skill has to *know* what that baseline is. That is exactly what the blind control supplies, and why the differential — not the design alone — is the headline.

## The decision: Approach A (of three considered)

Chosen: **A — a prose "discovery protocol" skill that provokes the agent to author a fresh Workflow each run.**

- **A over B (a standalone skill that embeds a fixed Workflow script):** discovery is a *judgment* job, and the `agent-facing-design` gate says answer those with provoking prose + a tight trust-discipline, **not** a fixed pipeline. A fixed pipeline for a discovery core is the substitutive-structure trap — fake-diverse generators and a dazzle-prone fixed judge become baked in. There is also **no repo precedent** for embedding a Workflow script inside a skill (every existing skill describes orchestration in prose and lets the agent author it), and a fixed script fights JP's own word "dynamic."
- **A over C (fold the capability into `design-exploration` as an orchestrated mode):** `design-exploration` is conversational-by-contract ("check in after sections"); bolting an autonomous, expensive fleet onto it muddies its nature and cost profile. And `skill-squad`'s value is *skill-domain-specialized* (the two-kinds bar + repo doctrine ground both the discovery and the control's judgment), which doesn't belong in a general design lane.

## Name, placement, scope

- **Name:** `skill-squad`.
- **Placement:** `skills-claude/skill-squad/` — Codex-excluded, like `skill-benchmark`, because it drives the Claude **Workflow** tool. Codex's bundled `skill-creator` already owns the equivalent work there, so this creates no dual-runtime obligation.
- **Scope:** **skills-first, with a reusable engine.** The protocol is grounded in skill-design doctrine (the two-kinds bar; `AGENTS.md` skill conventions) so the discovery and the control's judgment have a real bar to reason against, and so the trigger stays tight against `design-exploration`. The discovery *engine* (spread → blind control → adversarial verify → differential) is written to be reusable for other agent-facing-artifact design later, but skills are case #1 and the only triggered scope now.
- **Bundle:** start minimal — one `SKILL.md`, no reference file unless the body outgrows itself during authoring.

## Trigger / description (loader-facing routing)

> Use when you want to design a new skill (or materially redesign one) by orchestrating a multi-agent discovery run — fan out genuinely different approaches, beat them against a blind built-ins-only control, adversarially verify, and return a chosen design with an honest discovery-vs-control differential. Claude-only; expensive by design. Do not use for conversational or general design (`design-exploration`), judging whether proposed structure is justified (`agent-facing-design`), measuring an already-built skill (`skill-benchmark`), adversarial critique of an existing skill (`scrutinize-skill`), or hand-authoring the `SKILL.md` itself.

(Final wording to be tuned during authoring against the description budget; the fences above are the load-bearing part.)

## The discovery protocol — the heart (a provoking rhythm, not a template)

The skill provokes the agent to author a **fresh** Workflow per design, scaled to the problem and budget. Five moves:

1. **Set the bar, blind.** An independent arm writes the design a careful agent reaches *without* the discovery machinery — the control. It never sees the discovery arm.
2. **Spread genuinely-incompatible approaches.** Fan out generators seeded with *mutually-exclusive governing commitments* (release-cut's minimal-mechanical / judgment-provoker / member / portable-deriver), not N restatements. **Forcing function:** each approach must be one another author would call *wrong*, not merely *different*.
3. **Kill seductive-but-wrong.** Survivors face independent skeptics (delegated to `scrutinize-skill`'s lens): authors never grade their own work (kills author-blindness); the judge is told to favor simple-right over elaborate-wrong (kills dazzle). **Forcing function:** a design advances only by surviving a real refutation attempt, not a rubber-stamp.
4. **Pick the strongest, then run the decisive comparison.** Pick the strongest single approach; a merge is allowed only as **one-spine-plus-justified-grafts that must beat the best parent** (see Hybrid handling). Then put the winner head-to-head against the blind control before an independent judge. The product is the **margin** — does it genuinely beat what a careful agent reaches alone, and on which axes?
5. **Report, honest-null included.** Either "genuinely better design + margin," or "marginal: the control holds — here's proof it survived a real beating." Both are wins.

## The blind-control discipline — the trust core (where machinery is justified)

This is the one place to spend real machinery: a corrupted control fakes a discovery (or fakes a marginal), and that is exactly the user-trust damage the gate says machinery may protect.

- **Blind:** the control arm sees only the original design problem, never the discovery arm's approaches.
- **Ensemble, always:** the control is a fixed **2–3 careful-default designs**, not one — a robust bar that isn't one lucky/unlucky draw. Discovery must beat the **strongest** member of the control ensemble, not the average. (Budget-scaling still governs discovery *breadth*; the control ensemble is fixed.)
- **"The baseline is not empty"** (borrowed from `skill-benchmark`): the control is *a careful agent + the repo's doctrine*, named honestly as "careful-default," never "no skill."
- **Validity check before trusting the margin:** confirm the control was genuinely independent *and* genuinely hard (a real attempt, not a soft strawman). If not → report "differential unreliable," not a margin.
- **Single-sourced, not copied:** the skill *names* `skill-benchmark`'s "baseline-is-not-empty + validity-gate" principle as shared doctrine and carries only the design-time specifics. It does **not** clone skill-benchmark's `claude -p` subprocess mechanics, which don't apply before a skill exists.

## Hybrid handling — one spine, not a blend

Hybrids are expected, not an edge case: **release-cut's own design was a hybrid** ("the resolution of that disagreement, not a vote — anchor on minimal-mechanical's structure, relocate into git-cycle, narrow the provoker's battery to one question"). The protocol welcomes hybrids without letting them become mush.

A hybrid is legitimate only as **one spine + justified grafts — never a blend of spines:**

- **Mush (the camel):** average several philosophies, graft everyone's good parts. Usually *more* elaborate than any single approach → the dazzle-by-elaboration failure. **Rejected**, not crowned.
- **Resolution (the real discovery):** one approach's philosophy wins the spine; rival elements are imported only as **subordinated, individually-justified grafts**. (Release-cut kept minimal-mechanical's spine and imported a *narrowed* sliver of the provoker — the hybrid *subtracted* complexity.)

Three rules enforce it:

1. **A hybrid is a candidate, not a default compromise.** It **re-enters the adversarial pass** like any approach — synthesis doesn't launder a merge past the skeptics.
2. **It must name one spine in a sentence.** If you can't say which philosophy governs and why each graft is a deliberate import, it's mush → killed.
3. **It must beat the best *parent*, not just the control.** This extends the differential: a non-hybrid winner only beats the strongest control; **a hybrid also has to beat the strongest single approach it was built from.** If it beats the control but ties or loses to the best parent, the **parent wins** and the hybrid is reported as considered-and-rejected.

This *strengthens* discovery: "beats the best parent" is a higher bar than "beats the control," so the hybrid path is the most anti-dazzle route in the skill. It stays on the judgment side of the gate — enforced by a **forcing question** ("one spine, or a committee average?") and a **forced comparison** (head-to-head vs the best parent), **not** a coherence score.

## The differential output — frame fixed, content free

Predictable verdict *shape* is part of the trust value, so the frame is fixed but the design itself is judgment:

- the chosen design (approach, shape, key decisions, open risks);
- the verdict — **beat** (margin + axes) or **marginal** (control holds + surviving-attack proof);
- what got killed and why (so the breadth is visibly real — including any rejected hybrid);
- a hard stop: it hands off, it does **not** write the `SKILL.md`.

## Adversarial backstop — delegate, don't reinvent

The "harder to fool" backstop is **delegated to `scrutinize-skill`** (the repo's owner of adversarial skill-contract review), not re-implemented inline — the trust-bar's "single-sourced rather than copied" move. A lighter inline refutation is acceptable only when a candidate design is too embryonic for a contract review; otherwise the skeptics run `scrutinize-skill`'s lens.

## Cost & authorization

Invoking `skill-squad` *is* a valid Workflow opt-in, but a run is expensive (release-cut: 14 agents /~770k tokens; the Era-12 review: 62 / ~3.2M). So **invoking ≠ authorized to spawn** (the `skill-benchmark` posture):

- state the intended scale before launching;
- scale the discovery fleet to the skill's complexity + available budget (the "dynamic" part);
- ask one cost question before launching unless already authorized (e.g. "ultracode" is on).

## Where it stops / handoff

Stops at an approved design → hands to hand-authoring against `agent-facing-design` + `skill-ux-design` (honoring the repo's deliberate "no Claude-side constructor"). `skill-squad` is the **front of the authoring pipeline**:

```
skill-squad (discover the design) → hand-author the SKILL.md → behavior-smoke-test / skill-benchmark
```

No collision with any stage: `skill-squad` generates and selects a *design*; the others judge structure, review a contract, or measure a built skill.

## What it deliberately does NOT add (gate compliance)

To keep the judgment core on the provoke side of `agent-facing-design`:

- no discovery **score**, no classifier deciding "is this a discovery";
- no required fill-in fields, no fixed agent count, no rigid stop-sequence;
- the differential is a **judgment the panel argues**, not a number it computes.

Machinery is concentrated only where it protects trust in the verdict: the blind-control discipline and the validity check.

## One-Owner positioning

| Neighbor | Owns | Why `skill-squad` doesn't collide |
| --- | --- | --- |
| `design-exploration` | conversational design shaping of any artifact | `skill-squad` is autonomous orchestrated fan-out, skill-specialized, expensive-by-design — a different method and grounding |
| `agent-facing-design` | the gate: is proposed structure justified? | `skill-squad` *generates* candidate designs; it passes through the gate, doesn't replace it |
| `skill-benchmark` | post-build numeric with/without-skill measurement | `skill-squad` is design-time, pre-build, qualitative; it borrows the differential-honesty *principle* only |
| `scrutinize-skill` | adversarial critique of an existing/proposed skill | `skill-squad` *delegates to* it for the backstop |

One-Owner is a heuristic for build-and-prune skills (collisions surface as competing fires → prune the weaker), not a hard gate. The novel job — orchestrated, control-anchored discovery of a *design* — is genuinely unowned.

## Settled decisions

- Approach **A** (prose protocol, standalone, agent authors the Workflow).
- Name **`skill-squad`**; placement **`skills-claude/`**; **skills-first** scope with a reusable engine.
- Control: **ensemble always** (2–3), beat the strongest member.
- Backstop: **delegate to `scrutinize-skill`**.
- Stops at a **design** (no constructor); hands to hand-authoring.

## Open for planning / authoring

- Exact **fleet-scaling thresholds** (how breadth/agent-count maps to budget and skill complexity).
- Whether the **reusable engine** is factored out now or only after a second use appears (default: keep it inline in `skill-squad` until a real second caller exists — build-and-prune).
- Final **description** wording against the budget; whether the body needs a `references/` file or stays a single `SKILL.md`.
- The precise **prose shape** of the protocol so it provokes without ossifying (the core `agent-facing-design` authoring risk).

## Honest limits / risks

- **The skill faces its own marginal-differential risk.** Whether orchestration beats a careful agent is the open empirical question across Eras 14–18 — and `skill-squad`'s honest-null verdict is precisely its answer: it is built to *report* when a run was marginal rather than launder it. First real fire is the proof, not this spec.
- **Lazy-control failure.** If the agent runs a soft strawman control, the differential is meaningless. The validity check is the guard, and it has to be a real forcing function — the highest-risk authoring detail.
- **Cost.** Expensive by design; the authorization posture and budget-scaling are load-bearing, not optional.
- **Not yet validated.** No behavior smoke test exists yet; the design's followability is unproven until authored and proxy-tested.

## Provenance & grounding

- Interview chain this session: `outcome-interviewer` (discovery is the heart; "harder to fool" = author-blindness + judge-dazzle) → `making-recommendations` (the blind-control / honest-null mechanism, chosen over three baseline strategies) → `design-exploration` (Approach A; hybrid handling).
- Live files read while grounding: `skills/agent-facing-design/SKILL.md` (the gate + two-kinds doctrine), `skills-claude/skill-benchmark/SKILL.md` (the differential precedent + "baseline is not empty"), `plugins/review-family/skills/scrutinize-skill/SKILL.md` (the delegated backstop). `deep-research` — the closest structural analog named in the skill list — was not found on disk, so its shape is unverified.
- Next lane: `implementation-planning` for an executable build plan.
