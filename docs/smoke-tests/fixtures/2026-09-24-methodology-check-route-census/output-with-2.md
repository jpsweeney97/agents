## Census, graded

Window: 2026-07-02 to 2026-09-24. Vintage and reach are cleared, so every claim below is bounded to this window. The counts are as reported to me; I read no transcripts.

| Surface | Reading | Grade | Carries / cannot carry |
|---|---|---|---|
| Body-marker grep (Claude + Codex) | 61 in context, 30 genuine fires | contextualizes | Carries: the skill is used. Cannot carry: which body step is dead. The whole body enters context at every fire, so per-step deadness is not cheaply probeable. |
| Field fires (cwd outside skill repo) | 19 of the 30 | contextualizes | Carries: use beyond the repo. Cannot carry: how any step behaved. |
| Output probe, Exits route names in field assistant text | `design-exploration` 16, `ideate` 0, `prototype` 0, `grill-me` 0 | inconclusive | Mention count only. See Finding 1. |
| Marker vintage and corpus reach | Cleared | bound | Absence claims cover 2026-07-02 onward only. |
| Local proxy sessions (repo test fixtures) | `prototype`/`ideate` named 40+ times | excluded | Fixtures are not fires. The count says nothing about the field. |

## Findings

**1. Is the re-typing step live in the field? Escalate-rider.** The re-typing step is the one that changes the mud's kind and sends it to `ideate` or `prototype`.

- **Decided here (structure):** the body types the mud silently, so a re-type leaves no record by design. The only trace is what the assistant does next. The route-name probe cannot see that trace.
- **Why this is not a contract finding:** the question is whether the method can know its own typing was right. It is not about wording or output shape. The text gives no check that a re-type was needed or happened.
- **Not decided here (behavior):** I did not decide whether the re-typing step ran or was correct.
  - The zeros for `ideate`, `prototype` and `grill-me` do not show the step is dead. Real re-typing can read "let's list more options" or "run a small test" without the table's names.
  - The 16 `design-exploration` hits are not confirmed exits. The table is in context at every fire, and assistants quote or paraphrase it.
  - One hint, not a verdict: the other three names are at 0, so the 16 are not whole-table quotes. A single passing mention would still produce them.
- **What the route-name row can carry:** how often the table's names appear in assistant text across 19 field fires since 2026-07-02.
- **What it cannot carry:** that a route is dead, that an exit happened, or that the direction was right. The 40+ fixture hits carry nothing either way.
- **Recommendation:** to settle whether it fires the right way, commission `methodology-critique` on this axis. It would read the 19 field fires for what the assistant did once questions stopped helping: widen options, run a small test, or force a trade.

Need from you: tell me whether to leave the recommendation as is, or that you will commission `methodology-critique` yourself from a Claude session.
