## Census, graded

| Surface | Reading | Grade |
|---|---|---|
| Body-marker grep (Claude + Codex) | 61 sessions, 30 genuine fires. The whole body loads on every fire, so these markers can't tell one instrument from another. | contextualizes: the skill runs, nothing more |
| Field fires (cwd outside repo) | 19 of the 30 | contextualizes; small base for an absence claim |
| Route-name probe: `design-exploration` | Named in 16 of 19 fires. The Exits table is in context every fire and assistants quote it, so a hit doesn't show it was chosen as a route. | inconclusive |
| Route-name probe: `ideate`, `prototype`, `grill-me` | 0, 0, 0 in assistant text across the 19 fires | inconclusive for "dead" |
| Marker vintage, corpus reach | Cleared. Absence claims hold only from 2026-07-02 onward. | confound cleared |
| Local proxy sessions (repo test fixtures) | `prototype` and `ideate` named 40+ times. These are fixtures, not fires, so they are excluded. | carries nothing about the field |

## Findings

**F1: No field evidence that mud re-types to `ideate` or `prototype`. Escalate-rider** (structure decided here; how often it fires correctly needs the transcripts).

*Decided here.* Since 2026-07-02, none of the 19 field fires named `ideate`, `prototype`, or `grill-me`. The one route seen, `design-exploration`, is the "want is clear" exit, which is not re-typing. Per the excerpt, the typing is silent, so the route name is the only trace the method leaves in output. A wrong type also has no correction path. The user is asked to correct the read of the want, not the type. A mistyped mud, such as missing information typed as missing words, keeps the interview going.

*Not a contract finding because:* it asks whether the method can know it has left interview territory. That is the central claim, and it is not a wording or output-shape defect.

*Not decided here.* Zero names fits three different situations:
1. The instrument fails to fire when it should.
2. All 19 fires had mud that interviewing solved, so there was no occasion to re-route.
3. The assistant re-routed in paraphrase without the tool name.

The census can't separate these. Doing so needs each fire's mud kind and whether the questions stalled.

**What the route-name row can carry:**
- The three names never appeared in assistant text in 19 field fires after 2026-07-02.
- `design-exploration` appeared, which shows presence only.

**What it cannot carry:**
- That the instrument is dead.
- That it is live.
- That any route was the right one.
- Anything from the 40+ fixture hits, which show the names can be emitted, not that field use triggers them.

**Need from you:** to settle whether it fires the right way, commission `methodology-critique` on the re-typing axis. Have it read the mud kind in the 19 field fires and check whether the assistant kept interviewing when it should have re-routed.
1. Commission it.
2. Leave it open.
