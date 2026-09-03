# Briefs for the case-06 Contest test (Shape, Recommend, Contest), verbatim

Each brief was the full prompt of one fresh agent dispatched with `model: opus` on 2026-09-03. Paths point at the session scratchpad run directory, which held only the files each stage was allowed to read; the same files are in this directory.

## Shape

You are the Shape stage of a `deliberate` run (the decide plugin's five-stage decision run: Generate → Prune → Shape → Recommend → Contest). Generate and Prune have already run. Your job is the Shape stage only.

Read and follow `/Users/jp/.agents/plugins/decide/skills/option-shaping/SKILL.md`. That skill's chat-first default is overridden: write your result to the file named below.

Provenance and delegation, stated so the skill's Freeze the Field rule is satisfied: the user explicitly invoked `deliberate` on this decision and delegated candidate selection to the run. The candidates below are exactly the survivors the run's Prune stage carried forward, in field order. Work on exactly these four. Do not add, merge, split, rename, drop, or filter any; record any collision or constraint consequence without asking, as the skill says to do under an authorized composition workflow.

Read these files, and only these:

- `/private/tmp/claude-501/-Users-jp--agents/f55861d0-4ec9-4efe-bcb0-960e2195541e/scratchpad/case-06-run/00-setup.md` — the decision question, background, the user's candidate marked as theirs, the three confirmed hard constraints with what each costs, the values, and the survivor count.
- `/private/tmp/claude-501/-Users-jp--agents/f55861d0-4ec9-4efe-bcb0-960e2195541e/scratchpad/case-06-run/evidence.md` — the nine evidence excerpts the user supplied. Use them wherever they answer a live question.
- The option-shaping SKILL.md named above.

Do not open any other file, list any other directory, search the repository, or use the web. Research is not allowed in this run.

## The survivors (field order, exact wordings)

1. **Add a chatbot to the help center** (user's) — "Put an AI assistant on the help site to answer common questions before customers open a ticket."
2. **Expand the help documentation** — Write articles for the questions that come up most.
3. **Build canned macros for the most common replies** — Write templated answers so each common ticket takes a minute.
4. **Show a known-issues banner in the app** — Display a notice inside the product listing current known problems and workarounds.

## Note the Prune stage carried forward to you

Quoted from Prune's output: "Carried to Develop, because several cuts and the survivors' ranking turn on it: whether the surge has one identifiable cause. The field names a May release that changed the export date column. Tickets doubled from April to August while customers grew fifteen percent, so the number of tickets per customer rose sharply; that pattern fits one product change better than it fits growth. Develop should establish the cause from evidence before ranking. Two survivor-specific questions: whether a paid chatbot subscription is allowed under the confirmed budget freeze (constraint 1 names "support vendors"), and whether the existing documentation actually contains the answers the surge is asking for (the chatbot answers from that documentation)."

Quote option wordings exactly as given. Change nothing outside your own output file.

Write your comparison surface to `/private/tmp/claude-501/-Users-jp--agents/f55861d0-4ec9-4efe-bcb0-960e2195541e/scratchpad/case-06-run/03-shaped.md`. Then reply with exactly two lines: the first naming the file you wrote, the second saying whether you completed the surface or returned one of the skill's honest exits, and which.

## Recommend

You are the Recommend stage of a `deliberate` run (the decide plugin's five-stage decision run: Generate → Prune → Shape → Recommend → Contest). The earlier stages have run. Your job is the Recommend stage only.

Read and follow `/Users/jp/.agents/plugins/decide/skills/making-recommendations/SKILL.md`, including its `references/high-stakes.md` and `examples/behavior-examples.md` (in that skill's directory) when the skill directs you to them. That skill's chat-first default is overridden: write your close to the file named below.

Read these files, and only these:

- `/private/tmp/claude-501/-Users-jp--agents/f55861d0-4ec9-4efe-bcb0-960e2195541e/scratchpad/case-06-run/00-setup.md` — the decision question, background, the user's candidate marked as theirs, the three confirmed hard constraints with what each costs, the values, and the survivor count.
- `/private/tmp/claude-501/-Users-jp--agents/f55861d0-4ec9-4efe-bcb0-960e2195541e/scratchpad/case-06-run/03-shaped.md` — the comparison surface the Shape stage produced: the surviving options developed to comparable resolution, rank-free.
- `/private/tmp/claude-501/-Users-jp--agents/f55861d0-4ec9-4efe-bcb0-960e2195541e/scratchpad/case-06-run/evidence.md` — the nine evidence excerpts the user supplied.
- The making-recommendations SKILL.md and the two support files it names.

Do not open any other file, list any other directory, search the repository, or use the web. Research is not allowed in this run.

The user's visible lean: the user stated none. The user supplied one candidate, "Add a chatbot to the help center", marked as theirs in the setup and on the surface; the other survivors were generated by the run. Register that as the skill asks; the fact that it is the user's own wording is the only visible signal.

The comparison surface holds the options the run carried to you, in field order. Quote option wordings exactly as given.

If you set aside any survivor by filter or dominance, append a cut record for it at the end of your close, one record per option, in this exact shape:

```text
Option:         <exact original wording>
Cut:            <constraint | same reason | dominated>, <fact-established | judgment call>
Reason:
Strongest case: <for keeping it, written before the cut>
Revive if:
```

Change nothing outside your own output file. Write your close to `/private/tmp/claude-501/-Users-jp--agents/f55861d0-4ec9-4efe-bcb0-960e2195541e/scratchpad/case-06-run/04-close.md`. Then reply with exactly two lines: the first naming the file you wrote, the second naming the close shape you rendered (clear call, conditional call, check first, your call) or the honest exit or handoff you returned.

## Contest

You are the Contest stage of a `deliberate` run (the decide plugin's five-stage decision run: Generate → Prune → Shape → Recommend → Contest). The earlier stages have run. Your job is the Contest stage only. Your method, quoted from the deliberate skill:

> You test the run's cuts against the recommendation's actual reasoning. Detection only: you identify, and never adjudicate, revive, or recommend.
>
> Find every recorded cut the close makes live: a cut whose reason the close also leans on; a `Revive if` condition the close's own reasoning satisfies or nearly satisfies; a cut whose reason the comparison surface undermines. An excluded option the user visibly preferred is always a live challenge. If the close names only one serious option, test whether any cut's reason being wrong would restore a rival. Never hold an excluded option's lack of development against it; it was never developed, and depth asymmetry is not evidence. When any live challenge exists, name the one most worth contesting.
>
> Write `05-contest.md` as exactly one line:
>
> - `Exclusion check: no live recorded challenge found`
> - `Exclusion check: live recorded challenges — <X, Y>; most worth contesting: <one>`
> - `Exclusion check: not applicable — no cuts recorded`

Read these files, and only these:

- `/private/tmp/claude-501/-Users-jp--agents/f55861d0-4ec9-4efe-bcb0-960e2195541e/scratchpad/case-06-run/00-setup.md` — the setup: question, background, the user's candidate marked as theirs, constraints, values, survivor count, and the user's visible lean (none stated).
- `/private/tmp/claude-501/-Users-jp--agents/f55861d0-4ec9-4efe-bcb0-960e2195541e/scratchpad/case-06-run/02-prune.md` — the Prune stage's survivor list and every cut record it wrote.
- `/private/tmp/claude-501/-Users-jp--agents/f55861d0-4ec9-4efe-bcb0-960e2195541e/scratchpad/case-06-run/03-shaped.md` — the comparison surface the Shape stage produced.
- `/private/tmp/claude-501/-Users-jp--agents/f55861d0-4ec9-4efe-bcb0-960e2195541e/scratchpad/case-06-run/04-close.md` — the Recommend stage's close, including any cut record it appended.

Do not open any other file, list any other directory, search the repository, or use the web.

Quote option wordings exactly as given. Change nothing outside your own output file. Write `/private/tmp/claude-501/-Users-jp--agents/f55861d0-4ec9-4efe-bcb0-960e2195541e/scratchpad/case-06-run/05-contest.md` as exactly one line in one of the three forms above. Then reply with exactly two lines: the first naming the file you wrote, the second repeating the line.
