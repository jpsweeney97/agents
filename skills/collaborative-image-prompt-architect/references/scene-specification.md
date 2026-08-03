# Scene Specification

Use the scene specification to preserve visual intent across collaboration and handoff. It is internal architecture, not a prompt template. Keep it sparse: include a field only when it carries a decision, exposes uncertainty, prevents drift, or changes what the target compiler should prioritize.

## Contents

- [Choose a depth](#choose-a-depth)
- [Use the canonical shape lightly](#use-the-canonical-shape-lightly)
- [Write the visual thesis](#write-the-visual-thesis)
- [Set creative latitude](#set-creative-latitude)
- [Set the salience budget](#set-the-salience-budget)
- [Track decisions and provenance](#track-decisions-and-provenance)
- [Represent geometry and time](#represent-geometry-and-time)
- [Separate architecture from compiler handoff](#separate-architecture-from-compiler-handoff)
- [Expose state selectively](#expose-state-selectively)

## Choose a depth

### Minimal

Use for a simple scene or direct request:

- contract and visual thesis;
- three or four salience priorities;
- image identity, subject, and frozen action;
- viewpoint or composition;
- creative latitude;
- target compiler and material assumptions.

### Standard

Add when relationships affect the result:

- invariants;
- environment and lighting;
- explicit spatial geometry;
- interaction and awareness;
- rendering behavior;
- accepted decisions and unresolved high-leverage questions.

### Extended

Add only when required:

- per-reference control assignments;
- multiple subjects and awareness relationships;
- causal physics chains;
- conflicts and acceptable degradation;
- reversible decision history;
- multiple compiler targets.

The specification may grow or shrink as the request changes. Do not preserve empty modules for completeness.

## Use the canonical shape lightly

Keep canonical facts model-neutral. Store target ownership and handoff notes under `compiler`; do not store target prompt syntax or final wording in the scene.

```yaml
ssl_version: "1.1"
project:
  creative_latitude: tasteful_completion
contract: {}
visual_thesis: ""
salience_budget: []
invariants: []
scene:
  identity: {}
  camera: {}
  environment: {}
  geometry: {}
  subjects: []
  time: {}
  interaction: {}
  composition: {}
  rendering: {}
  physics: {}
  narrative_read: {}
references: []
controls:
  failure_prevention: []
  escape_hatches: []
state:
  metadata: {}
  assumptions: []
  questions: []
  conflicts: []
  decisions: []
compiler:
  target: active_image_tool
  owner: target_model_skill
  handoff_notes: []
```

Start from [scene-specification-template.yaml](scene-specification-template.yaml), then remove unused keys rather than populating them with invented detail.

## Write the visual thesis

The visual thesis is one sentence that holds together three things:

- dominant aesthetic;
- intended emotional or narrative read;
- compositional character.

It should be specific enough to reject a generic substitute without becoming a full prompt.

```text
An intimate, rain-muted editorial illustration that makes the lone commuter feel small inside a broad field of reflective city color.
```

Keep the semantic anchors—`intimate`, `rain-muted`, `editorial illustration`—and support them with visible consequences—`lone commuter`, `small`, `broad field`, `reflective city color`.

## Set creative latitude

Record creative latitude only when it changes how gaps may be filled:

- `strict_preservation`: no visually material additions;
- `tasteful_completion`: coherent low-risk additions may strengthen the accepted image;
- `exploratory_authorship`: bolder proposals are allowed but remain proposed until accepted.

The value governs scene design and target compilation. It does not override locks or reference-controlled traits.

## Set the salience budget

Keep three or four priorities. Ask: if the target model follows only these instructions, does the image retain its identity?

Good priorities name visible outcomes:

```yaml
salience_budget:
  - candid employee viewpoint from behind the counter
  - customer caught in one asymmetric recoil after the bee has left frame
  - ordinary consumer-phone rendering rather than staged portraiture
  - supplied storefront structure preserved without copying its camera angle
```

Do not put every invariant into the budget. Measurements, secondary props, adjacent moments, and diagnostic negatives stay internal unless their omission would change the image.

## Track decisions and provenance

Use states only when they change future behavior:

- `unresolved`;
- `proposed`;
- `accepted`;
- `locked`;
- `conflicted`;
- `superseded`.

Use the narrowest accurate source: `user_explicit`, `reference_observed`, `assistant_recommendation`, `derived`, `default`, or `target_constraint`.

Do not wrap every scalar in metadata. Put exceptional state under `state.metadata` using dotted paths. Never convert a reference inference into explicit user intent.

## Represent geometry and time

Use the camera as origin when spatial layout matters. Record only the position, orientation, depth planes, crop, frame share, overlaps, and contact relationships needed to prevent a conventional substitute or impossible composition.

Prefer useful approximation over fake measurement. Keep exact-seeming distances internal unless the target needs them. The test is whether a person could sketch the layout without replacing it with a generic composition.

Store the trigger, immediately-before context, frozen instant, and likely immediately-after state only when they help reason about momentum or causality. Compile only the visible frozen instant. Reject a state that combines incompatible phases of motion.

## Separate architecture from compiler handoff

The scene specification owns meaning. The target compiler owns final generation wording, ordering, supported syntax, and target-appropriate compression.

Before handoff, resolve:

- target model or active image tool;
- target compiler owner or current guidance source;
- intended use and output type;
- visual thesis and salience budget;
- locked invariants and reference roles;
- creative latitude;
- the minimum supporting scene facts the compiler needs.

If no current target owner or guidance exists, label the output `portable_scene_brief`. Do not store a model-neutral prose prompt in the canonical scene as though it were target-ready.

## Expose state selectively

Keep the full structure internal unless the user asks for it or needs to verify continuity. In ordinary turns, surface only accepted facts, the current proposal, material uncertainty, and the next decision. At final delivery, provide the specification only when it will be reused or is needed to explain a tradeoff.
