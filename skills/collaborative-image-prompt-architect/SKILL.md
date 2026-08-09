---
name: collaborative-image-prompt-architect
description: "Use when the user wants to explore an image concept, develop a scene, construct, revise, adapt, vary, or finalize image-prompt text. Do not use for skeptical prompt review, generated-output diagnosis or repair, or direct image generation or editing."
---

# Collaborative Image Prompt Architect

Invocation: `/collaborative-image-prompt-architect` or `$collaborative-image-prompt-architect`.

Own prompt work, not pixels: preserve a model-neutral Intent while making replaceable target-facing Prompt versions. The work product is a decisive intended image, not an exhaustive inventory. Keep the visual thesis, three-or-four-item salience budget, locks, reference contracts, sketchable geometry, frozen time, physical logic, and cross-domain core intact.

## Route before acting

Own only `EXPLORE`, `BUILD`, `EDIT`, and `FINALIZE`.

- A skeptical evaluation of prompt text routes to `$scrutinize-image-prompt` in `REVIEW`.
- Analysis or repair conditioned on a generated output routes to the reviewer in `DIAGNOSE`; this skill may consume that reviewer's authorized repair brief only through `EDIT` with `strict_preservation`.
- An explicit request to generate or edit pixels uses an active image tool only when the user explicitly asks for pixels; prompt requests never generate.
- Multiple concepts, directions, or variants route to `EXPLORE`.
- A requested modification or target adaptation routes to `EDIT`.
- A request to emit an accepted active prompt unchanged routes to `FINALIZE`.
- Otherwise route to `BUILD`. The existence of a prompt alone does not make the work `EDIT`.

## Choose interaction and latitude

Reconstruct the scene internally in every operation; show the reconstruction only when it helps the user. Set `interaction_depth` to `direct` or `guided`, and independently set `creative_latitude` to `strict_preservation`, `tasteful_completion`, or `exploratory_authorship`.

In `direct`, proceed with low-risk defaults and do not open a questionnaire. In `guided`, recommend the strongest choice with its visible benefit and tradeoff, then ask one focused, high-leverage question. Ask only when material uncertainty remains.

`strict_preservation` protects all locks; `tasteful_completion` fills low-risk gaps without changing identity; `exploratory_authorship` may propose bolder directions, which remain proposed until selected. Latitude never overrides a lock or reference control. Read [dialogue-workflow.md](references/dialogue-workflow.md) for the operation router and repair-brief boundary.

## Build scene meaning before wording

Keep the three layers distinct:

- **Intent** is the canonical, model-neutral scene specification only: accepted facts, thesis, salience, locks, geometry, time, physics, and reference contracts. Use [scene-specification.md](references/scene-specification.md); begin with [scene-specification-minimal-template.yaml](references/scene-specification-minimal-template.yaml) and use the extended template only when complexity warrants it.
- **Prompt workspace** holds target, mode, active prompt, candidates, versions, requested delta, assumptions, output contract, and execution permission. It is optional and sparse; use [prompt-workspace.md](references/prompt-workspace.md) when continuity needs it.
- **Evidence** records outputs, divergences, hypotheses, confidence, alternatives, tests, and the next change. It belongs to the reviewer for diagnosis, not this skill.

Inspect every available visual reference before deriving observed controls. Use reference roles precisely: `identity_reference`, `environment_reference`, `wardrobe_reference`, `pose_reference`, `composition_reference`, `rendering_reference`, `inspiration`, `generated_evidence`, `edit_target`, or `unknown`. When material, say what each controls, what may vary, and what cannot be inferred. For an inaccessible reference, retain only its user-declared role, mark visual traits unverified, and request reattachment only when those traits materially affect prompt work. Never infer unseen content or convert a reference observation into user intent.

Keep geometry drawable from the camera origin, specify one compatible frozen instant, and use cause-and-effect physical logic rather than decorative detail. The optional [jp-photographic-profile.md](references/jp-photographic-profile.md) applies only when explicitly requested, project-established, or compatible with otherwise-unspecified candid photography; it never overrides explicit style or incompatible media.

## Operate

In `EXPLORE`, use `premise_diversity` for materially different premises, frozen moments, compositions, relationships, spatial reads, or emotional reads. Use `controlled_variation` only when all locks stay fixed and only authorized dimensions vary. Candidates never replace the active prompt until selected or continued.

In `BUILD`, establish facts, thesis, subject/event, viewpoint, frozen moment, salience, and low-risk choices. Complete a prompt once the scene is coherent; keep schema, rationale, provenance, and most measurements internal.

In `EDIT`, pin the active prompt, requested delta, unavoidable dependencies, and preserved locks. Classify scope as `surgical` for “only” or “identical,” `coherent_revision` for ordinary revisions, and `broad_rewrite` only for an explicit overhaul. Create a new version while retaining the prior one. A surgical edit may adjust dependent camera, light, focus, or rendering continuity, but never redesign subject, event, setting, or mood. Adaptation changes formulation for a target, never identity.

In `FINALIZE`, require an accepted active prompt, make zero visual or semantic change, remove drafting residue and discussion, and emit it exactly once. “Prompt only” means no heading, rationale, changelog, or closing. A loose idea remains `BUILD`.

## Compile without executing

Use exactly three execution states: `compile_only`, `generate_image`, and `edit_image`. Default to `compile_only`; only an explicit request for the image itself may select `generate_image` or `edit_image`, and pixel execution then routes to the active image tool. Resolve target authority in order: the user's named target-model skill or current target guidance; the active image tool's current skill or guidance; then current official target guidance when genuinely needed. Compile target-specific wording only from resolved current authority. If a named target lacks current guidance or an owner, return portable, explicitly unverified wording rather than improvising target-specific claims. A compiler may choose syntax, order, compression, and target-facing phrasing, but cannot alter locks, import rejected ideas, or execute. Read [validation-and-compilation.md](references/validation-and-compilation.md) before complex handoff, and [interaction-patterns.md](references/interaction-patterns.md) for concise delivery shapes. [worked-example.md](references/worked-example.md) calibrates the same reasoning across domains.
