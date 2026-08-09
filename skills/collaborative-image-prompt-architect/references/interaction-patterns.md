# Interaction Patterns

Use these only when they make the response clearer. Keep internal state internal unless continuity or a material choice needs exposure.

## Guided recommendation

```markdown
You are aiming for <brief visible reconstruction and frozen instant>.

I recommend <strongest choice>. It preserves <visible benefit>; the tradeoff is <tradeoff>.

<One focused high-leverage question.>
```

## EXPLORE: premise diversity

```markdown
Here are <n> materially different directions:

- <direction>: <different premise, frozen moment, composition, relationship, spatial read, or emotional read>.
- <direction>: <materially different premise>.

These are candidates, not replacements for the active prompt. Which should I continue?
```

## EXPLORE: controlled variation

```markdown
Locks retained: <locks>.
Authorized variation: <only the allowed dimensions>.

- Candidate A: <variation>.
- Candidate B: <variation>.
```

Use only when every lock remains fixed.

## EDIT

```markdown
Active prompt: <version or source>.
Scope: <surgical | coherent_revision | broad_rewrite>.
Requested delta: <change>.
Preserved: <unrelated locks>.
Necessary continuity changes: <camera/light/focus/rendering only when forced>.

<Complete revised prompt, unless the user asked for a patch.>
```

## FINALIZE

For `prompt only`, emit the accepted active prompt exactly once with no title, rationale, changelog, or closing. Otherwise a compact label is allowed, but the prompt itself remains unchanged.

## Portable compiler handoff

```markdown
Target: <target or unresolved>
Execution permission: compile_only
Visual thesis: <one sentence>
Must survive: <three or four salience priorities>
Locks and references: <only material controls>
Supporting facts: <only generation-relevant facts>
```

The compiler may choose target syntax, order, compression, and phrasing. It cannot change locks, import rejected ideas, or execute. With no target, say the wording is portable and unverified, untested, unoptimized, and not model-ready.
