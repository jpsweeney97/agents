---
type: test-design
experiment: judgment-trust test 2 — human cold-judge, blind to the bar
project: agents
status: PREPARED (not yet run; runs in a fresh session with a human judge)
depends_on:
  - test 3 (home differential) — PASSED, f048687
  - test 1 (foreign differential) — PASSED, 0f70235
escapes: BOTH the authorship confound AND same-model circularity (the C1 limit tests 1 & 3 cannot escape)
---

# Test 2 — human cold-judge (blind to the bar)

## Why this test exists

Tests 1 and 3 both proved the bar is **load-bearing and non-over-cutting**, but both share one fatal limit (sealed C1 in each): **the reviewer is Claude — the same model that, with its author, produced the bar.** So they can show the bar *changes* reviews and *doesn't over-cut*, but **never that its calls are correct.** Correctness needs a judge outside both the authorship and the model.

Test 2 is that judge: **a human, blind to the bar's existence and its judgment-vs-trust framing, independently decides whether specific skill-structure choices help or hurt.** Their calls are the correctness anchor. We then compare: does the bar agree with a bar-naive human?

The trigger is concrete: **on the finding-cap, the bar's own two runs now disagree** — test 3 (home, named) cut it as substitutive 3/3; test 1 (anonymized) defended it 2/3. An apparatus that contradicts itself across runs cannot adjudicate itself. A human breaks the tie.

## The single variable

The human is **never shown** the bar, the words judgment/trust/substitutive/forcing-function/ provoke, the prior verdicts, or which items are contested vs controls. They see anonymized skills and a uniform neutral question. That blindness is the whole experiment — protect it.

## Protocol (for the administering session)

1. **Present the blind packet** (`test2-corpus/blind-judge-packet.md`) to the human **one item at a time, in randomized order** (shuffle per session). One-at-a-time + shuffle is the primary defense against cross-item theory-reversal: it denies the judge the contrast set they'd otherwise scan to infer "mechanical structure = suspect." Present all items, or a subset if time-limited (item 1, the cap, is the priority; the controls calibrate). Do **not** show or paraphrase the sealed key, the bar, the categories, or this design doc's framing.
2. **Collect, per item:** a 3-way call — **keep as-is / change it / remove it** — plus one sentence of reasoning. Reasoning matters more than the label.
3. **Only after all answers are in,** open `test2-corpus/sealed-key.md` and compare.
4. **Score** (below). Write `judgment-trust-test2-results-<date>.md`. Apparatus stays unchanged unless the result demands it (that is a separate, gated decision).

## Scoring

- **Calibration check (items 10–14, clear cases).** The human should mostly **remove** the two substitution probes (10, 11) and **keep** the three genuine structures (12–14). If they don't, the human isn't judging carefully (or our "clear" cases aren't) — note it; the contested results are only trustworthy if calibration holds.
- **Adjudication (items 1–9, contested).** For each, does the human's call match **bar-ON**? Record agreement/disagreement and the human's reason. The aggregate human↔bar-ON agreement rate on the contested set is the headline.
- **The cap (item 1) is decided outright** by the human's call — it resolves the test-3/test-1 self-disagreement and the standing frontier question.
- **Direction of any disagreement matters:** human "keep" where bar-ON "cut" = the bar over-cuts (mis-calibrated strict); human "remove" where bar-ON "kept" = the bar is lenient.

## Sealed limits (state in the results)

- **n = 1 human** (or few). A single judge carries their own taste; this is a tie-breaker and a direction-check, not a population estimate. More judges strengthen it.
- **Packet framing can still steer — and blinding has a faithfulness floor (IMPORTANT).** The packet was leak-checked **3× by a different model (Codex/gpt-5.5)**. The first pass caught real, fixable framing leaks — asymmetric loaded language, verdict-telegraphing slogans ("is the recommendation", "checking the boxes is what ready means"), and good/bad checklist adjacency — all removed. The residual the checker still flags is **faithfulness-bound**: the calibration controls read as clear cases *because they are* clear cases (that is their job), and the contested items describe their genuinely-contested features (a numeric quota, a score→band, an "in-depth" interview step). Removing that readability would mean **misrepresenting the elements** — testing different choices than the bar actually reviewed, which corrupts the experiment more than the readability hurts it. So blinding is **good, not perfect**. Mitigations: (a) one-item-at-a-time + randomized order (defeats cross-item theory-reversal — the main risk); (b) controls are a minority (5 of 14) interleaved among 9 contested items; (c) even a judge who infers "mechanical structure is suspect" must still make a real call on each contested item, since that heuristic does not resolve them. A stronger-blinding option, if desired later: have a human (not the apparatus author) rewrite the packet, or use a judge from a domain unaware of skill-design debates.
- **"Better thinking" is unmeasurable** for pure-judgment skills (the skill-benchmark caveat). The human judges the **structure decision** (does this element help or hurt the skill), not a measured uplift in thinking quality.
- **The human's expertise is a variable.** A judge who knows the domains (skill review, design, teaching, MCP) gives a stronger signal than a lay judge; record who judged.

## What's prepared (in this repo, for the fresh session)

- `test2-corpus/blind-judge-packet.md` — the human-facing items (neutral; show this).
- `test2-corpus/sealed-key.md` — bar calls + function labels per item (open only AFTER answers).
- This design doc — protocol + scoring + limits.
- A handoff in `.agents/handoffs/` resumes the fresh session straight into running it.

## Provenance

Items drawn from the test-1 sealed element key (`judgment-trust-test1-foreign-prereg-2026-06-16.md` @ d6cf84e) and results (`...test1-foreign-results...` @ 0f70235): the 8 cross-model-contested ambiguous elements + the home-replication cap + 5 calibration controls (2 substitution probes the bar cut, 3 genuine structures the bar kept). Blind packet leak-checked by Codex/gpt-5.5 (a different model) **3×**: fixable framing leaks removed; residual is faithfulness-bound (see the blinding limit above).
