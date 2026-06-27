---
name: steelman
description: "Use when the user wants the strongest one-sided case FOR a position — 'argue the other side', 'make the best case for X', 'the strongest case against my choice'. Builds a committed advocate's brief with its load-bearing assumptions made visible and an honest surviving-counter close; it picks no winner. Do not use to rank options and pick a winner (`making-recommendations`), attack an artifact for flaws (`scrutinize`), ask one question at a time (`grill-me`), or generate many options (`ideate`)."
---

# Steelman

Build the genuine strongest case *for* one position — usually one the user is inclined to dismiss — then stop without picking. Invocation: `/steelman` or `$steelman`.

steelman is the library's one *advocacy* skill. Everything around it refuses a side: `making-recommendations` weighs options evenly and picks a winner, `scrutinize` attacks an artifact, `grill-me` interrogates, `ideate` widens, `design-exploration` shapes a design. steelman runs the other direction — handed a position, it builds the strongest case for it the way its smartest believer would, with the load-bearing joints made visible, then stops without picking. Its value is the one thing a capable both-sidesing agent never volunteers: a committed case for a view the user is about to dismiss, honest enough that they can actually weigh it.

## The owned job (why it is a distinct skill)

A capable agent told "make the case for X" already argues, so steelman earns its place two ways: it *guarantees* the honesty behaviors a bare advocacy prompt drops under the pull to either hedge or flatter (below), and it is the one owner whose **product is a committed one-sided case**. It is defined by inverting its nearest neighbors:

- `making-recommendations` is even-handed and ends in a **pick**; steelman develops **one** position and picks **no winner**. The behavioral tell: if you catch yourself comparing the position to a rival to decide which is better, you have left steelman.
- `scrutinize` / `scrutinize-skill` **attack** an artifact to surface flaws; steelman **builds** a position up. Even "the strongest case *against* my choice" is constructive — it is the best case *for* the alternative, not a flaw-hunt.
- `grill-me` / `grill-with-docs` **ask** one question at a time; steelman **argues** and delivers a brief.
- `ideate` widens to many un-ranked options; steelman deepens **one**.
- `design-exploration` shapes and approves a design; steelman neither designs nor decides.

steelman is the constructive-advocacy member of the advisory lane; where they exist, route adversarial attack to `red-team` and prospective failure to `premortem` (neither is built yet — name them only if available).

## Mixed skill — apply the bar per part

- **Provoked (judgment).** Which position, its strongest honest form, which arguments are genuinely strongest, what the case truly rests on, the real surviving counter, and whether the position should be advanced at all. The skill poses these; it never fills them in.
- **Firm (trust).** The mandatory bounded honest close, the one-sided / no-winner contract, the harm gate, and the no-artifact default. Their value is a predictable, honest shape; a missing one is a defect, not a style choice.

## The moves — a rhythm, not a fill-in template

1. **Pin the position; gate on harm.** State the position in one sentence in its strongest, most charitable form — strip the dismissive caricature the user arrived with, since de-strawmanning is the first act of advocacy. Read the position from context and *state* it ("I take the position to be X"); ask at most one scoping question, and only when the readings genuinely diverge — never an interview. In the same move, the floor: if advancing this would require real harm (safety, legality, deception, irreversible damage) or can only be argued by fabricating, name that and decline or heavily caveat instead of producing a slick brief. It fires rarely — most "bad ideas" can be honestly steelmanned, which is the whole point.
2. **Build the genuine affirmative case — 2 to 4 strongest arguments, on the position's *own* terms.** The best *real* arguments, developed and committed, from premises that could actually be true; ordered strongest-first; each distinct; never padded to a count, because a pile of weak arguments weakens a steelman. Include arguments fully *orthogonal* to whatever the user holds against the position — the strongest case routinely concedes their objections entirely and wins on a consideration they never raised ("your concerns hold, and it still wins on X"). Never cap the case to the user's frame. **Frame, don't fabricate:** the best framing of genuine grounds is advocacy; inventing facts, data, or citations is sophistry and out of bounds.
3. **Surface what the case rests on — visible, and aimed.** Name the load-bearing assumptions ("what would have to be true for this to be right"), but *aim* them at the user rather than tabulating them: show how much of the case a skeptic already grants, isolate the one genuinely contested crux, and argue why that crux is more defensible than it looks. This is visible structure the user can go verify, kept in the advocate's voice — never a plausibility-scored fragility map, which is `scrutinize`'s job pointed the other way.
4. **(Conditional) engage the user's stated reasons — after the case, never as the case.** If the user gave specific reasons for leaning against the position, address them once the affirmative case stands: concede the valid-but-non-dispositive ones, show which the case overcomes, and say plainly where it wins orthogonally. Skip this move entirely when the user stated no reasons. It never becomes the spine — the product is the case for the position, not a rebuttal of the user.
5. **The honest close — mandatory, the primary guard.** Declare plainly: *this is one-sided advocacy, not my recommendation.* Name the **single strongest surviving counter** — the sharpest objection this case does *not* defeat — and leave it standing, un-rebutted; if you cannot find one, the case is overclaiming, so dig until you find the one you cannot knock down. Carry a **committed read of how strong the best case really is**, plus the advance / don't-advance flag if it was not already triggered. One bounded counter, never the opposing brief — so the close cannot drift into balanced analysis.

## The honesty mechanism — what keeps a committed advocate from becoming a sophist

Honesty is structural and carried by the close, not assumed as a free byproduct of arguing hard:

- **The bounded honest close is the primary guard.** A sophist's case answers everything; a real steelman ends by handing over the live weakness it cannot beat and labels itself advocacy.
- **Effort is lopsided; candor is level.** Put all the effort into the best case and none into ranking it against rivals — but never overstate how strong that case turned out to be. That single asymmetry is what lets a one-sided skill stay honest.
- **Anchor the case and the counter to something external.** On a position with real informed holders, target the version its smartest proponent would endorse. On a counterfactual about the user's *own* choice — the common "argue against my decision," where there is no outside proponent to anchor on — name an anchor outside your own "what I find convincing": a real precedent, an established principle or decision-rule, or the actual reasoning-class of people who choose this way. Without an external anchor the surviving counter is graded by the same judgment that built the case — the agent marking its own homework, exactly the self-certification `ideate` forbids.
- **"Stays weak" is a successful run.** Concluding that the best honest case is genuinely weak gives a dismissed position its fair hearing and confirms, with reasons, that the dismissal was warranted. A skill that can reach that verdict has no incentive to inflate.

## Output

A reasoned brief in the response — the pinned position, the affirmative case, the visible load-bearing structure, the honest close. No ranking, no winner, no even-handed comparison. Nothing is persisted: a one-sided brief left in the repo is a confirmation-bias hazard in reverse — found later without its close, it reads as a balanced verdict it never was. If the user wants it kept, hand to a capture lane (`research-capture` / `markdown-synthesis`) rather than grow a persistence part here.

The committed strength read is one judgment, not a scoreboard — name calibration bands like "stands up / holds if / stays weak" only when they sharpen the read, never as required fields completed to feel done.

## When not to advocate

- The options are already on the table and the user wants a pick → `making-recommendations`.
- The user wants the artifact torn down, not a case built → `scrutinize`.
- The position needs no defense, or no honest case can be built → say so and stop; do not manufacture advocacy. Knowing when *not* to advocate is part of the skill.

## Build-and-prune note

Chat-first; no artifact by default. Advocacy against a too-fast dismissal fires often and locally, so this is not first-to-prune — but watch it actually earn its honesty guarantees over a bare "make the case for X," and fold or prune if in practice it only restyles a case a capable agent already produces. The honest differential is reliability plus modest cognitive-offload, not a new capability.
