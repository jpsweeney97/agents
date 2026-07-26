---
name: context-checkpoint
description: "Use when the user asks how much context room is left, whether some piece of work still fits, or whether something should start in a fresh session — and, at an arc boundary in a session that has been running heavy, to measure and volunteer the stop-or-continue call once. Recommendation only: it measures occupancy from the live transcript, names the window it divided by, and routes into `handoff:save-handoff` on approval. Do not use to write the handoff itself, to load one (`load-handoff`), or for compaction mechanics."
---

# Context Checkpoint

When to stop an arc and hand off is usually decided by feel, and the misses are expensive: a session that runs past its room dies into auto-compaction mid-ritual, taking the handoff with it. This skill replaces the feel with a measurement and stops there. It advises. It never saves, exits, or compacts.

Invocation: `/context-checkpoint` or `$context-checkpoint`, a plain question about room or fresh-session timing, or — once per arc boundary, above the floor below — unprompted.

Claude Code only: the probe reads Claude Code's own transcript layout.

## Measure, never estimate

Occupancy is the last assistant turn's `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`. Read it:

```sh
/Users/jp/.agents/skills-claude/context-checkpoint/scripts/occupancy.py
```

It resolves this session's transcript from `$CLAUDE_CODE_SESSION_ID` and the working directory, then prints occupancy now, the session's peak, the model as the transcript recorded it, and the tokens added between recent typed user turns. Pass `--transcript <path>` for another session's transcript, or `--cwd <dir>` when the shell has moved out of the directory the session started in.

If the transcript cannot be resolved, the script fails loudly — say so and stop. A measured number is worth having because it was measured; a guessed one is worse than none, because it will be acted on.

Read two things out of the numbers before going further. A **negative turn delta** is a compaction that already happened, so deltas spanning it are not comparable arc costs. A **peak far above the current reading** says the same thing: this session has already been squeezed once.

## Name the window you divided by

Tokens are the fact. Percent is an interpretation, and it needs a denominator the transcript does not carry: the recorded model string omits the context-window variant, so a session running a 1M-token window records as plain `claude-opus-5`, indistinguishable there from the 200k variant. Never read the window off that field — a real transcript in this library peaked at 493,557 tokens under a model string that a 200k assumption would have called impossible.

Peak occupancy, which the probe also prints, is a hard floor under the window: a session that reached 493,557 tokens is not running a 200k window whatever its model string says. Use that floor to check the assumption, and to settle it outright whenever the peak already exceeds the smaller variant.

Otherwise take the window from what this session knows about its own model, state where the number came from, and give the percent as a division rather than a fact:

```text
158,010 tokens — 16% of the 1M window (from this session's model id, claude-opus-5[1m]).
```

When the window is genuinely unknown, say so and let the forecast carry the call alone. A percentage of an unnamed denominator is the vibe this skill exists to replace.

## Forecast the next arc

Size the proposed next arc from this session's own history rather than a general sense of cost: sum the turn deltas across a comparable past stretch and show the arithmetic — "the last review round cost about 35k; two more of those do not fit in what is left."

When nothing comparable has run yet, give an estimate, label it an estimate, and name what it is based on.

## Recommend

One verdict — **continue**, **checkpoint now**, or **split** — and always with the stop point named rather than the bare call: "checkpoint after round 1; round 2 gets a fresh session."

The forecast drives the verdict; occupancy only gates whether to volunteer it. Unprompted, speak at most once per arc boundary and only above roughly 35% occupancy — below that, or when the call was already given at this boundary, stay quiet. Asked directly, answer at any occupancy.

That floor is calibrated from checkpoints taken between 39% and 54% of a 200k window. On a much larger window the same percentage is a far larger stretch of work, so let the forecast carry more of the call there and the percentage less.

**Continue is a real verdict.** A high number is not by itself a reason to stop, and a session with room for the arc in front of it should be told so plainly. A checkpoint skill that only ever counsels stopping is a nag, and gets ignored exactly when it is right.

## On approval

Ask exactly one question — **which thread deserves emphasis in the handoff?** — then invoke `handoff:save-handoff`, carrying the answer as its brief.

One question, not an interview. Everything else a handoff needs is `save-handoff`'s to gather, and when the session is ending its own throughline suggestion does that job.

## Bounds

- Never save, exit, or compact on your own. The verdict is advice, and stays advice until the user takes it.
- Never change settings or install a hook to arrange a future automatic save. This skill measures and recommends inside the session it is running in; harness configuration is `update-config`'s.
- Report tokens before percent, always. The measurement is the contribution; the percentage is a convenience laid over an assumption.

## Output

```markdown
Occupancy: <tokens> — <percent> of the <window> window (<where the window came from>)
Next arc: <size, and the past stretch it was drawn from>
Verdict: continue | checkpoint now | split — <the named stop point>
```
