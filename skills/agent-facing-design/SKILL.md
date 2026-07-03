---
name: agent-facing-design
description: "Use when creating or materially changing agent-facing prompts, skills, rules, workflows, tools, command interfaces, schemas, validators, or persistent artifacts that agents must read, follow, populate, invoke, or maintain, especially before adding required fields, statuses, stages, classifiers, scoring, hard rules, or semantic decision logic. Do not use for ordinary product code, internal helper scripts, or user-facing docs unless they create agent obligations."
---

# Agent-Facing Design

Keep agent-facing systems useful in the moment. This skill leads two lives: as a design gate it is not a ritual but a pause before adding structure that future agents must obey; as the library's quality constitution it is the canonical home of the two-kinds-of-skill lens and the offload doctrine that other skills read and defer to.

## Core Move

Start with the user's work product: the artifact, behavior, recovery path, review, ticket, handoff, or decision someone will rely on.

If the target already exists, inspect the live target and nearby authority before deciding. Read only enough to name the current obligation, the work product at stake, and the surface that controls it: prompt text, skill body, metadata, referenced examples, schema, validator, hook, script, repo instruction, or workflow doc. If a needed surface is unavailable, say what is unverified.

If there is no existing target and no concrete proposed structure yet, do not run the gate as an abstract design exercise. Name the likely work product, then ask one question or hand off to the owning design, creation, interview, or writing workflow.

Check where you sit relative to the decision, too. This gate is a pause *before* structure hardens; when the thing under judgment is a draft you have already finished or a change you have already resolved to make — your own completed design, a reviewer's finding you have decided to accept — the pause has arrived after the fork, and asking the question there ratifies the choice instead of making it. Say plainly that the verdict is ratification, or reopen one genuine lighter alternative and weigh it for real before blessing the draft.

Then ask:

```text
Am I adding context that helps an agent think, or machinery that makes the
decision for it?
```

Context supports judgment: examples, boundaries, counterexamples, recoverable state, ownership, structured evidence, preconditions, and failure behavior.

Machinery removes or narrows judgment: required fields, status systems, fixed workflow stages, validators, routers, classifiers, scoring, confidence fields, semantic decision scripts, and hard rules.

The sharpest form of the cut is who makes the semantic decision, not the format: prose that pre-makes the call is machinery however gently it reads, and a deterministic mechanic that pre-makes nothing is a lighter design, not a threat — format only sets how hard the constraint is to override.

If the change is only context, keep it clear and proceed — but context is not free: it spends the same future-reader attention machinery does and accretes with no gate of its own, so on a surface that has already grown, prefer replacing prose to adding more.

If the change adds machinery, ask the smaller question:

```text
What real damage happens if this is wrong, and could lighter context produce the
same result?
```

Use machinery when a wrong value or wrong step can damage the work: deletion, credential exposure, corrupted state, broken recovery, stale authority, unsafe actions, security or permissions failures, or misleading the user about what actually happened. Damage is machinery's sharpest justification, not its only one — Two Kinds of Skill below admits machinery for reliable, repeatable execution, and Library Conventions for an output a downstream skill or tool must parse; name the value actually being claimed instead of stretching this list to cover it.

Otherwise, prefer the smaller clearer design: prose, examples, a boundary, recoverable state, or a deterministic mechanic that does not make the semantic decision.

If the user explicitly asked for a field, status, schema, validator, router, classifier, score, hard rule, or semantic script and the gate says it is not justified, do not silently substitute a lighter design. Say what you would not add, why the failure mode does not justify it, and what lighter path would preserve the work. Ask before applying the substitute unless the user already asked you to choose the smaller design.

A gate verdict is narrow, and citing it honestly means keeping it narrow. A pass answers one question — is *this* increment context or machinery — about this increment, at this moment. It does not certify the increment's content or correctness, the fitness of any routing or naming choice, the whole surface the increment joins, or a later revision of it; the same surface can pass this gate and still be wrong on every one of those. A verdict quoted downstream — in a commit message, a verification block, a review — should name the increment and the question it answered, never read as a blanket clearance the gate never gave.

The per-edit grain hides the one thing a single verdict cannot see: accumulation. Run finding by finding through a review loop and each increment can be locally justified while the surface ratchets past the work it protects — a run of consecutive "justified" verdicts on one growing surface is itself the borderline case. Before the next yes, step back from the increment to the whole surface; if it now feels larger than the work it protects, simplify before adding more. This is the whole-surface question — run it here, per edit, not only when a reference happens to be opened.

## Two Kinds of Skill

The core move runs per edit. Run it once more per skill, at the whole-contract grain: what does this skill's value depend on?

- **Judgment skills** earn their keep by making the agent think better than it would alone — a sharper critique, a better recommendation, a real diagnosis. Their value is uplift. Hold them to: *does this protect and provoke better thinking?* The practical test for any structure in a judgment skill: does it organize or elicit thinking, or make the judgment for the agent? Provoking structure earns its place (an interrogation rhythm, a forced comparison, a counterexample); substitutive structure is the cost (mandated output shapes, exhaustive rule lists, fixed sections the agent fills to feel done), and past a point it makes the agent perform the contract instead of doing the work. When a judgment skill underperforms, the usual fix is to cut substitutive structure. But the bar is *protect and provoke*, and the provoke side fails too: a skill that provokes nothing — no forcing function, no counter-pressure, just "think carefully" — adds nothing over the bare agent. So does one that provokes too weakly: a forcing function present but dulled, hedged, or softened until it no longer creates real counter-pressure (an adversarial posture reframed as collaborative) is the same defect by degree, not a pass. Its fix is a sharper forcing function (a harder question, a forced comparison, a required counterexample), not more scaffolding. The output bar a judgment skill should demand is tempered, not timid: the strongest defensible judgment without flattening the case — preserve the distinctions that change the call (evidence, authority, scope, risk, reversibility, disposition), name the uncertainty that limits the judgment, and never soften a conclusion merely because it is uncomfortable.
- **Trust skills** earn their keep by reliably carrying a task so the user stops supervising it — landing a branch, closing out work, executing a plan step by step — or by returning a correct, grounded, faithfully-transformed result the user can stop double-checking (a correct doc lookup, a lossless reformat). Their value is predictable, repeatable execution (damage-prevention is its sharpest case, not its only one; correct retrieval and faithful transformation are the lookup/transform tail of the same value). That value has two sources and a skill needs only one — the agent would otherwise *err* (reliability), or it acts correctly unprompted yet the user is still spared the careful procedure (cognitive-offload, defined in full for both kinds below); so judging a trust skill only by whether its body changes a strong agent's behavior measures the first and is blind to the second, and *a capable model does this anyway* never by itself proves the skill valueless. Here defined steps, safe defaults, and firm refusals are the value, not the cost. Hold them to: *is this reliable, and is the machinery single-sourced rather than copied?* But trust skills fail under bad rules too — just never as lost thinking. The failure takes two shapes: brittle, duplicated machinery (the same gate hand-copied into four skills, drifting out of sync), and crude-rule overreach (a rule so rigid it does the wrong thing in a case the author never foresaw — a protected-branch stop that dead-ends legitimate work).

**Cognitive-offload accrues to either kind.** The trust bullet names it as one of a trust skill's two value sources and defers its definition here, because it is not trust-only: any skill *summoned by a token* spares the user composing the careful procedure and delivers the same complete run every time — the prompt they never had to type — so a judgment skill carries it too. It is why a well-built skill is worth summoning, not a pass on being well-built: a judgment skill still earns its keep by provoking better thinking, a trust skill by reliable execution. Treat it as a lens on worth, never a score — `AGENTS.md` "What The Skills Are For" raises it to the merit altitude across both kinds; do not build an offload metric. Refusing a metric is not refusing falsification: offload is absent when the user still re-supervises or corrects the runs, or quietly stops summoning the skill — the usage ledger shows the last — and a skill matching those symptoms has lost the claim.

This refines the core move; it does not restate it. Judgment skills may carry plenty of structure — stages, rhythms, prompts — as long as it organizes thinking without making the judgment, exactly the deterministic mechanic the core move already prefers over a decision-making rule. Structure that makes or pre-empts the judgment is the substitutive kind, and the cost. Trust skills are the case where machinery that *does* decide and constrain is justified — by the need for reliable, repeatable execution.

Most real skills are mixed. Apply the bar per part, not per skill: hold the thinking parts to the judgment bar and the lifecycle or safety parts to the trust bar. Do not stamp one label on a two-natured skill.

This is a lens, not a label. There is no skill class to declare, score, or validate — infer the bar from what the skill does, apply it in the moment, move on. If applying it ever produces a fixed checklist every judgment skill "must satisfy," it has ossified into the machinery it exists to prevent — and that failure mode applies to this section too. The lens governs *quality* only; delivery hygiene (invocation tokens, naming, Codex budget, parseability) stays uniform across both kinds.

This section and `scrutinize-skill` are themselves judgment skills: hold any edit to them to the bar above — add a lens, not a score or required section. Self-application runs one level up as well: an edit to any part of this skill — a new obligatory branch, a size budget, a required column, a mandated section — is itself agent-facing structure, so run this skill's own Core Move question on it before it lands. The gate does not exempt its own body.

## Library Conventions

Two output conventions run through the skill library as practiced but previously unwritten law; they are stated here so a new or edited skill lands on the right side deliberately rather than by drift. Both are context for the designing agent, not a validator.

- **Verdict partition.** Exploratory and adversarial skills (`ideate`, `premortem`, `red-team`, `steelman`) render no verdict: their output is deliberately one-sided or divergent, and a bolted-on verdict gets mistaken for the calibrated call, short-circuiting the owner that should weigh the full picture. Decision-owning skills (`closeout-check`, `deploy-plan`, `outcome-check`) render exactly one. Place a new skill on one side on purpose; a skill that both explores and adjudicates is two skills.
- **Close packet.** A skill whose output gates a downstream action or chains into another skill closes with a compact labelled field:value shape (`closeout-check`'s verdict block, `deploy-plan`'s bake-read) so the next reader — human or skill — can branch without re-parsing prose. Read-only, exploratory, and dialogic skills keep their native close; forcing a packet on them is waste, not discipline.

## When Machinery Survives

Keep the surviving machinery narrow. Be able to say plainly:

- what user work it protects or improves
- why lighter context is insufficient
- what failure mode it prevents
- what future agents must understand, populate, follow, or maintain

Most of that reasoning belongs in chat or your own working notes. Write it into the artifact only when the choice is high-risk, becomes part of a durable contract, or would be hard for a future agent to reconstruct.

Passing the test justifies this guard, not a framework around it.

## Workflow Boundary

This skill is a design gate, not the owner of every agent-facing edit. Use it to decide whether the proposed structure is justified, then continue with the workflow that owns the requested work.

Examples:

- use `writing-principles` for instruction-doc writing or editing
- for skill construction, use the bundled `skill-creator` on Codex; on Claude, hand-author against this gate and `skill-ux-design` (no Claude-side constructor skill, by design)
- for quantitative skill benchmarking or trigger optimization, use `skill-benchmark` (Claude-only)
- use the relevant review-family skill for critique or review
- use the domain or implementation skill that owns the product change

Do not silently become a UX audit, design interview, review report, skill-writing workflow, or implementation workflow. If the user only asked for this gate's judgment, stop after the brief answer. If the user asked for an edit and the owning workflow is already clear, apply the smaller clearer design there.

## Calibration

Read [references/calibration.md](references/calibration.md) when the case is borderline, the surface has grown, you are shaping what a tool returns to a calling agent, or you are about to add schemas, workflow stages, validators, routers, classifiers, scoring, confidence fields, semantic decision scripts, or hard rules.

Use the examples for judgment, not checklist compliance.

## Output Shape

For implementation work, apply the smaller clearer design directly only when the owning edit path is already clear. After direct edits, validate through that owning workflow and state the proof boundary. Structural source checks prove parsing and shape, not that a realistic invocation followed the behavior. When the edited file is itself the live source, those checks are its proof; plugin caches, marketplace metadata, distributed copies, and other runtime surfaces need their own checks only when that surface is part of the claim.

For obvious gate decisions, a single crisp sentence is enough. For review or design discussion where the reasoning matters, answer briefly:

```markdown
My read: <context or machinery, and what work product is at stake>.
Evidence: <live target/context inspected, or what is unverified>.
The lighter path is <prose/example/recoverable state/deterministic mechanic>.
Machinery is justified only if <specific damage or failure mode>.
Next move: <apply directly | hand off to owning skill | ask one question>.
```

This template is one honest shape, not a required one. A gate answer owes the same three things in any form — the verdict (context or machinery, and the work product at stake), the damage reasoning behind it, and the next move — and none of that owes the labelled block: a single sentence, a few lines, or plain prose all pass as long as those three survive. Match the shape to the moment, not the moment to the shape.
