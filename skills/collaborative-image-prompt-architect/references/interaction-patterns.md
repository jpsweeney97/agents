# Interaction Patterns

Use these as adaptable response shapes. Omit empty sections and do not expose internal state when a sentence will do.

## Reconstruction and next move

```markdown
You are aiming for <two-to-five-sentence reconstruction of the visible image and frozen instant>.

Visual thesis: <dominant aesthetic, emotional read, and compositional character>.

The highest-leverage open decision is <decision>, because <visible downstream consequence>.

I recommend <choice>. It preserves <benefit>. The tradeoff is <tradeoff>.

<One focused question.>
```

Do not show a separate thesis line when it reads more naturally inside the reconstruction.

## Compact continuity update

```markdown
Locked: <accepted decisions that matter now>.

Proposed: <current recommendation>.

Still unresolved: <one material uncertainty>.

Next decision: <highest-leverage choice and why it matters>.
```

Use this only when the user benefits from continuity.

## Creative-latitude disclosure

```markdown
Creative latitude: <strict preservation | tasteful completion | exploratory authorship>. <One sentence explaining what may be added or must remain untouched.>
```

State this when the mode is not obvious or another plausible mode would materially change the image. Do not make it a routine form field.

## Coupled framing decision

```markdown
I recommend <aspect ratio> with <crop>. Together they preserve <visual benefit>.

The alternative, <other pairing>, preserves <competing benefit> but costs <tradeoff>.

Should I lock the recommendation, or is <specific competing need> more important?
```

## Reference contract

```markdown
I will use the references this way:

- **Reference 1 — identity:** preserve <traits>; do not copy <pose/background/lighting>.
- **Reference 2 — environment:** preserve <layout/materials>; allow <incidental details> to vary.

I cannot infer <unseen or ambiguous property>. <Focused question if material.>
```

## Compiler handoff

Use this compactly and usually keep it internal:

```markdown
Target: <model, active image tool, or target skill>
Intended use: <use>
Visual thesis: <one sentence>
Must survive:
- <salience priority>
- <salience priority>
- <salience priority>
Locked: <invariants and reference controls>
Creative latitude: <mode>
Supporting facts: <only what the compiler needs>
```

Do not hand the target compiler the complete scene specification by default.

## Final delivery after target compilation

```markdown
## Production prompt — <target>

<target-compiled prompt>

Assumption: <one material direct-mode assumption, if any>.
```

Add settings, a negative prompt, reference map, compact variant, or scene specification only when the target supports it and the user will benefit.

## Portable scene brief when no target is resolved

```markdown
## Portable scene brief

<visual thesis, salience priorities, invariants, and minimum supporting scene facts>

Compiler boundary: No current target model or target-specific guidance was resolved, so this is a portable brief rather than a verified model-ready prompt.
```

## Diagnostic response

```markdown
The earliest supported failure is **<domain>**: <visible evidence>.

That may explain <downstream symptoms>. I would revise <source scene facts>, preserve <unaffected locks>, and return those changes to <target compiler>.

Next controlled change: <one targeted revision>.
```

For a single stochastic sample, say `supported hypothesis` rather than claiming proven prompt causality.
