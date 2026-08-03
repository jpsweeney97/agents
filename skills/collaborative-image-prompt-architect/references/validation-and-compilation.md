# Validation and Compiler Handoff

Validate the scene architecture, then give a compact handoff to the current target-model owner. Do not convert the complete scene specification directly into model-neutral prose.

## Contents

- [Set the proof boundary](#set-the-proof-boundary)
- [Validate the scene architecture](#validate-the-scene-architecture)
- [Validate the salience budget](#validate-the-salience-budget)
- [Resolve the compiler target](#resolve-the-compiler-target)
- [Build the compiler handoff](#build-the-compiler-handoff)
- [Review the target-compiled prompt](#review-the-target-compiled-prompt)
- [Evaluate generated results](#evaluate-generated-results)

## Set the proof boundary

Scene validation can show that the intended image is coherent and that the compiler handoff preserves it. It cannot prove that a target model will follow the prompt or that a generated image will match the user's mental image.

Target compilation can show that current target guidance was applied. It cannot prove visual quality without generation and comparison.

When no target-model skill or current official guidance is available, deliver a portable scene brief and label the adaptation boundary. Do not call a model-neutral brief verified or model-ready.

## Validate the scene architecture

Use these as lenses, not a checklist to expose ceremonially.

### Identity and visual thesis

- Does the contract identify the subject, viewpoint, frozen moment, intended use, and goal?
- Does the visual thesis join aesthetic, emotional read, and compositional character in one decisive image?
- Do semantic anchors have observable support?
- Could the same architecture accidentally read as a different genre or generic substitute?

### Camera, geometry, and composition

- Can the camera see every major element without passing through an object or person?
- Are framing, distance, crop, and subject scale compatible?
- Do foreground and depth support the viewpoint without obscuring the action?
- Could a person sketch the requested layout without inventing a conventional replacement?
- Are measurements only as precise as the decision requires?

### Frozen time and interaction

- Does every visible element belong to the same instant?
- Do posture, gaze, expression, fabric, hair, and moving objects reflect the same causal phase?
- Are invisible causes supported by visible consequences?
- Is camera awareness intentional?

### Rendering, lighting, and physics

- Do medium and style support the visual thesis rather than merely list effects?
- Do light sources explain illumination, shadow, reflection, and exposure compromise when realism matters?
- Are pose, balance, contacts, fabric, and material response plausible at the requested realism level?
- Are deliberate imperfections caused by capture behavior or scene physics rather than scattered randomly?

### References and creative latitude

- Has every relied-upon reference been inspected and assigned a role?
- Are controlled traits preserved while unrelated traits remain free?
- Are additions allowed by the chosen creative latitude?
- Do reference instructions, user locks, and proposed art direction conflict?

Resolve results as `pass`, `partial`, or `blocking` only when recording state helps. Fix blocking issues. Leave a partial issue open, choose a low-risk default, or disclose it according to creative latitude; do not manufacture detail to make every lens pass.

## Validate the salience budget

Choose three or four priorities, not a compressed inventory. Apply this counterfactual:

> If the target follows only these instructions, will an ordinary viewer still recognize the intended image?

The priorities should collectively protect the visual thesis, central subject or frozen action, decisive composition or viewpoint, and the most important style, reference, text, or preservation boundary.

Demote details that merely explain the reasoning. Keep a measurement only when the target would otherwise substitute a materially different composition. Keep a negative only when it prevents a likely or observed failure that positive direction cannot economically displace.

## Resolve the compiler target

Use this order:

1. the user's named model or target-model skill;
2. the active image tool and its current skill;
3. current official target guidance;
4. otherwise, a portable scene brief with an explicit unverified-compilation boundary.

For the active OpenAI image tool, defer to the current `imagegen` skill when it is available. Do not duplicate its model syntax, execution parameters, prompt schema, or generation workflow here; those can change independently.

## Build the compiler handoff

Give the target owner the smallest complete packet:

```yaml
target: <model, tool, or target skill>
intended_use: <where the image will be used>
output_type: <photo, illustration, product image, edit, etc.>
creative_latitude: <strict_preservation | tasteful_completion | exploratory_authorship>
visual_thesis: <one sentence>
salience_budget:
  - <priority 1>
  - <priority 2>
  - <priority 3>
locked_invariants: []
reference_roles: []
supporting_scene_facts: []
known_failure_to_prevent: <optional, one narrow failure>
```

This is a conceptual packet, not a mandatory output schema. Use prose when that is lighter. Omit empty fields and internal decision history.

The target compiler owns final ordering, supported syntax, prompt length, parameter guidance, and compression. It may add target-facing semantic phrasing within creative latitude, but it may not change locks or import unrelated visual ideas.

## Review the target-compiled prompt

Read the result independently of the design history.

- Is the target named and was current target guidance used?
- Does the opening establish the medium or image class, subject, action, and visual thesis quickly?
- Are the salience priorities easy to find and mutually compatible?
- Are semantic anchors paired with observable evidence where both help?
- Did internal measurements, adjacent moments, provenance, or rationale leak into the prompt without a generation-critical reason?
- Did the target compiler introduce a visually material fact outside accepted creative latitude?
- Does lower-priority detail compete with the intended image?
- Are failure-prevention instructions narrow and target-supported?

When the prompt is crowded, remove duplicated statements, design rationale, low-priority props, noncritical measurements, generic quality language, and redundant negatives before touching a salience priority.

## Evaluate generated results

If the user requests generation, let the target image skill generate and inspect the output. Compare the image with the scene architecture, not merely with the wording of the prompt.

For controlled prompt evaluation, keep the scene request, target, and judging criteria constant. Blind the judge to arm identity. Compare at least intent fidelity and visual strength, and separate prompt quality from generation variance by using multiple outputs when the claim depends on consistency.
