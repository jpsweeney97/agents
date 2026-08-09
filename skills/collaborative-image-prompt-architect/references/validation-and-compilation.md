# Validation and Compiler Handoff

Validate Intent and Prompt continuity, then compile without execution. `execution_permission` permits `compile_only`, `generate_image`, or `edit_image`; default to `compile_only`, and select a pixel state only for an explicit request for the image itself before routing execution to the active image tool. A prompt request never generates or edits pixels.

## Proof boundary

Intent validation can establish a coherent requested image and a faithful handoff. Compilation can establish that a named target's available guidance was used. Neither proves a result, target acceptance, visual quality, optimization, or model readiness without the relevant target execution and result evaluation.

If no target or current target guidance is resolved, provide portable wording and state that it is unverified, untested, unoptimized, and not model-ready.

## Validate Intent

Use these as reasoning lenses, not a ceremonial checklist:

- Does the thesis join visible aesthetic, emotional or narrative read, and composition?
- Do the subject/event, camera origin, crop, depth, and occlusion permit a sketchable image rather than a generic substitute?
- Does every subject, gaze, balance, material response, light source, and moving object belong to the same frozen instant?
- Do three or four salience priorities retain image identity if lower-detail wording drops away?
- Was every available visual reference inspected before observed controls were derived, and does every material reference state its role, controls, allowed variation, and non-inferable facts? For inaccessible input, retain only user-declared role and unverified visual traits; request reattachment only when material.
- Does the selected latitude permit every addition, while locks remain intact?

## Compile

Resolve authority in this order: user-named target-model skill or current target guidance; active image tool's current skill or guidance; current official guidance only when genuinely needed. Hand the compiler only target, intended use, output type, visual thesis, salience, locks, reference contracts, permitted latitude, and the minimum supporting facts. It owns syntax, order, compression, and target-facing phrasing only after current authority is resolved. It may not alter locks, add rejected concepts, or execute without explicit permission. If a named target lacks a current owner or guidance, return portable explicitly unverified wording; never improvise target-specific claims.

Read compiled wording independently: it should establish image class, subject/event, thesis, and salient controls without leaking internal provenance, measurements, adjacent time states, or drafting rationale. Remove lower-priority competition before weakening a salience priority.

## Route other work correctly

Skeptical text evaluation belongs to `$scrutinize-image-prompt` `REVIEW`. Generated-output comparison, divergence claims, and repair diagnosis belong to reviewer `DIAGNOSE`. Explicit pixel generation or editing belongs to the active image tool only when explicitly requested. This skill may implement an authorized reviewer repair brief as strict-preservation `EDIT`, but does not evaluate the result that motivated it.
