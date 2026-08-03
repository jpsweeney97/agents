---
name: collaborative-image-prompt-architect
description: "Use when the user wants to design, refine, adapt, or diagnose an image prompt; collaboratively resolve a vague or complex image idea; preserve scene intent across references or revisions; reason about photorealistic geometry, behavior, or frozen time; or hand one scene to a named image model or active image tool. Do not use when the user simply asks to generate or edit an image without asking for prompt design."
---

# Collaborative Image Prompt Architect

Invocation: `/collaborative-image-prompt-architect` or `$collaborative-image-prompt-architect`.

Treat the user's intended image as the work product. Own the model-neutral scene architecture: the visible idea, accepted decisions, reference contracts, frozen moment, visual thesis, and priorities that must survive generation. Hand that architecture to the current target-model skill for final model-facing wording whenever one is available.

Do not mistake a complete scene inventory for a strong prompt. Optimize for a decisive visual result: preserve intent, make the dominant image legible, and remove detail that competes with it.

## Choose collaboration depth and creative latitude

Match the process to the request.

- **Direct:** Reconstruct the image, make defensible defaults, resolve obvious conflicts, and move to target compilation without forcing an interview. Default to `tasteful completion` unless the user requests exact preservation or explicitly invites bolder authorship.
- **Guided:** Evolve a vague, complex, or explicitly collaborative idea over multiple turns. Recommend a direction before asking for a decision.
- **Diagnostic:** Compare a generated image with the intended scene, identify the earliest supported failure domain, revise the scene architecture, and recompile through the same target.

Choose one creative-latitude mode when it affects the result:

- **Strict preservation:** Add no visually material content beyond the user's decisions and neutral connective defaults.
- **Tasteful completion:** Fill low-risk gaps with coherent art direction that strengthens the user's idea without changing its subject, event, genre, or reference-controlled traits.
- **Exploratory authorship:** Make bolder visual proposals and alternatives; keep them visibly proposed until the user accepts them.

Do not turn latitude into a form the user must fill out. Infer it from the request, state it only when useful, and disclose any material direct-mode choice after the result.

## Reconstruct the image before designing the prompt

Begin with two to five sentences that state:

- what is visibly happening;
- who or what controls the viewpoint;
- the single frozen instant;
- the **visual thesis**: one sentence defining the dominant aesthetic, emotional read, and compositional character;
- any material conflict or assumption already visible.

Use semantic anchors and observable evidence together. Write `candid and unposed, shown through an off-center crop, averted gaze, and interrupted movement`, not merely `candid` and not an evidence list with no global visual meaning.

Do not open with a questionnaire. If the request is already sufficient, proceed. Otherwise resolve the decision whose answer would most change the visual thesis or the instructions most likely to survive model competition.

## Maintain scene state sparsely

Keep decisions separate from prompt wording. Track only facts that preserve intent, expose a conflict, support a recommendation, or change the compiler handoff.

Distinguish explicit user decisions, reference observations, assistant recommendations, derived consequences, low-impact defaults, and unresolved questions. Never present an inference from a reference as user intent. Lock only an explicit user choice or an accepted recommendation, and never change a lock implicitly.

Use a minimal scene specification for simple requests, a standard one when relationships affect the result, and an extended one only for references, complex physics, multiple subjects, or multiple targets. Read [scene-specification.md](references/scene-specification.md) and use [scene-specification-template.yaml](references/scene-specification-template.yaml) when structured state will improve continuity.

## Run the adaptive design loop

For each meaningful user update:

1. Update the scene architecture and preserve locks.
2. Test whether the visual thesis still describes one decisive image.
3. Identify contradictions, missing causal links, or a likely generic substitution.
4. Rank unresolved issues by their effect on image identity, visual thesis, salience, viewpoint, action, reference fidelity, or intended use.
5. Recommend the strongest defensible choice for the top issue, with its visible benefit and material tradeoff.
6. Ask the smallest coherent question set needed for that decision, then continue, hand off, or stop at the depth the user requested.

Do not revisit settled modules to perform the process. Do not make the user supervise low-impact art direction that fits the chosen latitude. Read [dialogue-workflow.md](references/dialogue-workflow.md) for guided work, references, and diagnosis.

## Design only the modules the image needs

Choose from these modules rather than filling all of them:

- **Contract:** subject, viewpoint, frozen moment, intended use, and goal.
- **Visual thesis:** dominant aesthetic, emotional read, and compositional character.
- **Invariants:** three to seven truths whose failure would change the image's identity.
- **Camera and geometry:** origin, framing, depth, placement, crop, overlaps, and occlusion when spatial substitution is dangerous.
- **Subjects and interaction:** stable identity, transient pose, expression, gaze, awareness, and movement.
- **Environment and light:** layout, functional context, materials, sources, palette, and atmosphere.
- **Rendering:** medium, style, texture, focus, exposure, color, motion, and depth behavior.
- **Physics and time:** one frozen instant, balance, contact, gravity, material response, and only the adjacent moments needed for internal causal reasoning.
- **References:** what each input controls, what may vary, and what must not leak into the result.
- **Controls:** salience budget, likely substitution to prevent, creative latitude, and acceptable degradation.

Make geometry concrete enough to sketch without pretending to know an exact measurement. Keep adjacent moments and most measurements internal unless they are among the few facts the target must obey.

## Set a salience budget

Before handoff, identify three or four instructions that must survive if the target model follows only part of the prompt. Each should protect image identity, not incidental completeness.

A useful salience budget usually covers:

- the visual thesis;
- the primary subject and frozen action;
- the decisive viewpoint or composition;
- one style, reference, text, or preservation constraint that cannot degrade.

Phrase priorities as visible outcomes, not internal metadata. Remove or demote measurements, causal backstory, minor props, and defensive negatives that compete with them. A detail belongs in final wording only when omitting it creates a materially different image or the target compiler needs it to prevent a known substitution.

## Work with references deliberately

Inspect every available reference before relying on it. Assign each a role—identity, environment, wardrobe, pose, palette, composition, or rendering—and state what it controls and what may vary.

Do not infer unseen geometry or inherit a reference's composition unless requested. Resolve material conflicts by explicit user intent, accepted invariants, and declared reference role. If a required reference is inaccessible, stop only that branch and ask the user to attach it again.

## Validate the scene architecture

Validate relationships before handoff: camera visibility, crop, balance, frozen time, light causality, reference boundaries, narrative evidence, visual thesis, and salience. Treat a critical contradiction as blocking; leave low-impact gaps open according to creative latitude.

Read [validation-and-compilation.md](references/validation-and-compilation.md) before handing off a complex, reference-conditioned, maximum-realism, or image-edit request. Its compilation guidance describes the handoff boundary, not a second model-neutral prompt language.

## Resolve the target and hand off final wording

Resolve a compiler target before calling a prompt `model-ready`.

- Use the user's named model or target-model skill when supplied.
- Otherwise default to the active image tool and its current skill or official prompt guidance.
- When `imagegen` is available and the active OpenAI image tool is the target, let `imagegen` own prompt structure, target syntax, and generation-facing wording.
- If no target or current target guidance is available, deliver a portable scene brief or compiler handoff and label it as such; do not imply verified model readiness.

Hand the target compiler only what it needs:

- target model or active image tool;
- intended use and output type;
- visual thesis;
- three or four salience priorities;
- locked invariants and reference roles;
- creative latitude and any accepted additions;
- only the scene facts needed to preserve the requested image.

The target compiler may compress, reorder, dual-code semantic anchors with evidence, and use supported target syntax. It must not change locks, import rejected ideas, or add visually material content outside the accepted creative latitude. Keep detailed geometry and causal reasoning in the scene architecture unless the target compiler determines that they are generation-critical.

## Present only useful state

During guided work, show only accepted decisions, the current proposal, material uncertainty, and the next high-leverage decision when continuity helps.

For final delivery after target compilation, provide the target-compiled production prompt first and name the target. Add a compact variant, negative prompt, settings, reference map, or scene specification only when the target supports it and the user will benefit. If compilation could not be handed to a current target owner, provide the portable scene brief first and state that boundary.

Use [interaction-patterns.md](references/interaction-patterns.md) for concise response shapes. Use [worked-example.md](references/worked-example.md) for cross-domain calibration and to see what should remain internal in different image classes.

## Diagnose with an evidence boundary

When a generated result misses, separate identity, reference use, camera, geometry, frozen time, biomechanics, lighting, rendering, typography, prompt competition, and generation variance. Revise the earliest domain supported by visible evidence, then hand the affected architecture back to the same target compiler.

Do not infer prompt causality confidently from one stochastic sample. A single result can justify a targeted next attempt; multiple controlled outputs are needed to distinguish a systematic prompt failure from generation variance.

## Completion boundary

The scene architecture is ready when it preserves image identity, states a visual thesis, has no blocking contradiction, resolves high-leverage geometry and action, declares reference roles, and identifies the three or four priorities that must survive.

The production prompt is ready only after a target is resolved and the target compiler has produced the final model-facing wording. A prompt is not evidence that an image was generated or that the result matched the scene architecture.
