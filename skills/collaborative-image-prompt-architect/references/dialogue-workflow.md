# Dialogue Workflow

Use this workflow for guided collaboration, reference-conditioned design, or diagnosis after a generation misses. It is an adaptive loop, not a questionnaire or mandatory sequence.

## Contents

- [Choose the operating mode](#choose-the-operating-mode)
- [Open with reconstruction and a visual thesis](#open-with-reconstruction-and-a-visual-thesis)
- [Rank leverage](#rank-leverage)
- [Recommend before asking](#recommend-before-asking)
- [Use creative latitude](#use-creative-latitude)
- [Lock and revise](#lock-and-revise)
- [Use references](#use-references)
- [Diagnose a failed generation](#diagnose-a-failed-generation)
- [Know when to hand off](#know-when-to-hand-off)

## Choose the operating mode

Infer the lightest mode that satisfies the user.

### Direct

Use when the user asks for a finished prompt, quick revision, or target-model adaptation. Default to `tasteful completion`: make coherent low-risk visual choices, then disclose only material assumptions. Use `strict preservation` when the user asks for exactness, and `exploratory authorship` only when the user invites bold invention.

Pause only for a missing decision that would change image identity, violate a reference lock, or make the request contradictory. Resolve the target compiler before calling the result model-ready.

### Guided

Use when the user asks to collaborate, arrives with a vague or complex image, values fidelity over speed, or keeps refining decisions. Maintain continuity and take one high-leverage decision at a time.

### Diagnostic

Use when the user provides an output and says it is wrong, artificial, inconsistent, or unlike a reference. Inspect the output, compare it with the scene architecture, revise the earliest supported failure domain, and return the change to the same target compiler.

The mode can change. A guided session may switch to direct handoff when the user says, “Write it now.”

## Open with reconstruction and a visual thesis

Reconstruct before interrogating. A useful opening contains:

1. the visible image as currently understood;
2. the frozen instant and non-negotiable facts;
3. a proposed visual thesis;
4. the decision with the greatest effect on that thesis or the eventual salience budget.

Example:

> You are aiming for a candid phone snapshot from an employee's position behind a restaurant counter, caught just after a customer has been startled. My visual thesis is an ordinary, slightly chaotic slice of life whose off-center framing and asymmetric motion make the reaction feel accidental rather than performed. The highest-leverage choice is whether the reaction is still escalating or already resolving, because that changes the gaze, balance, arms, and emotional read together. I recommend the first half-second after the trigger has left frame.

The thesis keeps the semantic anchors—`candid`, `ordinary`, `slightly chaotic`—and grounds them in visible evidence. Do not list every unknown. Low-impact details may remain free or receive a default allowed by the chosen latitude.

## Rank leverage

Rank uncertainty by the consequence of getting it wrong:

- **Critical:** changes image identity, target use, central event, or a reference-controlled subject.
- **High:** changes the visual thesis, one of the likely salience priorities, composition, frozen action, interaction, or preservation boundary.
- **Medium:** visibly changes the result without changing its core read.
- **Low:** affects incidental detail or harmless variation.

Prefer a decision that constrains several downstream choices. Camera origin may constrain crop, foreground, distance, and occlusion. A visual thesis may constrain palette, lighting, subject scale, and negative space. Frozen time may constrain pose, gaze, fabric, hair, and motion softness.

Do not pretend the ranking is quantitative. State the visible consequence.

## Recommend before asking

Make a real choice. Include only what helps the user decide:

- the recommended option;
- the visible benefit;
- the material tradeoff;
- confidence only when uncertainty changes the recommendation.

Example:

> I recommend keeping the bee out of frame. The reaction remains the focus, the image stays mundane rather than horrific, and the target has fewer competing subjects. The tradeoff is that gaze and recoil must carry the cause.

Do not ask the user to choose among visually equivalent options. Do not present a weak recommendation as a neutral menu.

## Use creative latitude

Treat latitude as permission, not a checklist.

- Under `strict preservation`, ask before adding a material palette, setting, subject trait, prop, or narrative beat.
- Under `tasteful completion`, choose low-risk art direction that makes the accepted idea coherent. Do not ask about every minor color, texture, or background detail.
- Under `exploratory authorship`, propose a strong visual direction and one genuinely different alternative when that contrast helps; do not silently lock either.

When a direct-mode choice is material, append one short assumption after the target-compiled prompt. Do not narrate routine completion choices.

## Lock and revise

Lock a decision when the user states it explicitly or accepts a recommendation. A lock protects meaning, not exact wording.

When revising, update the canonical fact, identify dependent modules, revalidate only affected relationships, preserve unrelated locks, and reconsider the salience budget if the changed fact was one of its priorities.

If the user intentionally contradicts a lock, treat the newer request as a proposed revision. State the visible consequence and confirm only when material intent remains ambiguous.

## Use references

For each reference, identify what is directly observable, its role, what it controls, what may vary, and what cannot be inferred.

```yaml
- id: REF-01
  role: environment
  controls:
    - storefront materials
    - counter layout
    - window proportions
  may_vary:
    - people
    - exact props
    - lighting time
  unknown:
    - space behind the photographer
```

When references conflict, do not average them silently. Resolve the property by explicit user intent, accepted invariant, declared role, or one focused question.

## Diagnose a failed generation

Inspect the generated image before proposing changes. Separate these domains:

1. image identity or visual thesis;
2. reference use or identity preservation;
3. camera and geometry;
4. frozen time, interaction, or biomechanics;
5. lighting and material physics;
6. rendering or typography;
7. salience competition;
8. target-compiler mismatch;
9. generation variance.

Find the earliest domain visibly supported by the output. Revise the scene architecture there, then let the target compiler re-express the affected priorities. Do not append a negative list for every symptom.

A single sample supports a next hypothesis, not a confident causal diagnosis. Compare multiple controlled outputs before calling a failure systematic.

## Know when to hand off

Hand off when:

- image identity, visual thesis, and intended use are stable;
- the subject and frozen action are coherent;
- three or four salience priorities are clear;
- high-leverage geometry and reference roles are resolved;
- creative latitude is understood;
- no critical conflict remains;
- a target model, active image tool, or current target guidance source is resolved.

If no target is available, deliver a portable scene brief. If the user wants to continue exploring, state the current next move instead of compiling prematurely.
