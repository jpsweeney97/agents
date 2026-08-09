# Intent Specification

Intent is the canonical model-neutral scene meaning, never target prompt text, workspace state, execution authority, or output evidence. Keep it sparse: include only facts that preserve identity, expose uncertainty, prevent drift, or constrain compilation.

## Minimal by default

Use [scene-specification-minimal-template.yaml](scene-specification-minimal-template.yaml) for an ordinary direct request. It holds the visible contract, visual thesis, three or four salience priorities, locks, reference contracts, and only the subject/event, viewpoint, and frozen moment needed to preserve the image.

Use [scene-specification-template.yaml](scene-specification-template.yaml) only when reference control, multiple subjects, material geometry, causal physics, complex time, or a conflict needs structured continuity. Omit empty modules; no persistence is mandatory.

## Intent rules

Write a visual thesis that joins dominant aesthetic, emotional or narrative read, and compositional character. Preserve semantic anchors with observable evidence. Keep three or four salience priorities; do not turn the budget into an inventory.

Record only camera origin, depth, crop, overlap, contact, and approximate measurement necessary to sketch the layout without a generic substitute. Reason with trigger, immediately-before state, frozen instant, and immediately-after state when causal coherence needs it, but compile only the visible frozen instant.

Inspect every available visual reference before recording observed controls. Reference entries use `identity_reference`, `environment_reference`, `wardrobe_reference`, `pose_reference`, `composition_reference`, `rendering_reference`, `inspiration`, `generated_evidence`, `edit_target`, or `unknown`. For material input, state controls, allowed variation, and non-inferable facts. If a reference is inaccessible, retain only a user-declared role and mark visual traits unverified; request reattachment only when those traits matter. Reference observations never become user intent and unseen content is never inferred.

Keep provenance light: `user_explicit`, `reference_observed`, `assistant_recommendation`, `derived`, `default`, or `target_constraint` only when it changes future handling. A lock is an explicit user decision or accepted recommendation; it is never silently rewritten.
