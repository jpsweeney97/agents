---
type: review
date: 2026-09-03
scope: "plugins/decide/skills/outcome-shaping (decide 1.2.0) — the skill subtree (SKILL.md, agents/openai.yaml, examples/interaction-examples.md) as the target; the plugin's plugin.json, README, CHANGELOG, PRIVACY, and TERMS as consistency surfaces; 18 neighbor skills as routing surfaces only; plus delivery state (Codex cache, Claude symlink, marketplace entry, GitHub mirror)"
reviewed_commit: 22bfcd37eb49a6e928e459509a1ed717f69713d1
method: "gap-review — inline Phase 0 scout (delivery diffs + AGENTS.md Validation Ladder + library-integrity canary), then a 4-dimension Workflow fan-out on Opus (cross-surface consistency, lifecycle gap walk, edge-case behavioral audit, routing and dual-runtime delivery), one dedup agent, then one refute-default adversarial verifier per merged finding. 21 agents; 21 raw findings, 16 after dedup, all 16 verified: 6 confirmed (all reproduced), 10 refuted."
posture: "read-only, evaluation-only — no target file was edited, committed, or published by this run"
---

# Gap review: decide:outcome-shaping

Date: 2026-09-03. Target: `plugins/decide/skills/outcome-shaping` in `~/.agents` at commit `22bfcd3` (decide 1.2.0). Kind: a skill inside the dual-runtime `decide` plugin. The skill subtree is the review target; the plugin manifest, README, CHANGELOG, PRIVACY, and TERMS were in scope as consistency surfaces; neighbor skills were in scope only as routing surfaces.

Workflow run `wf_b7da3b59-c99`, all agents on Opus per instruction: 4 dimension reviewers, 1 dedup pass, 16 verifiers. 21 raw findings, 16 after dedup, 6 confirmed, 10 refuted, 0 unverified. Evaluation only: nothing was edited, committed, or published by the run. This record and its companion verdicts file were written afterward at JP's request.

## Summary

**Six findings survived adversarial verification, all at medium severity, and every one was reproduced rather than argued.** Three are defects in the skill's own text at the moment a want is declared settled or handed on: a missing route to `option-shaping`, an own-words restatement that can add unpriced content and still count as settled, and three surfaces that disagree about whether the lane may recommend in place. One is a silent failure after context compaction, where the agent attributes its own compression to the user. Two are under-disclosures in the plugin's published privacy and terms notices: an on-request file write and a calendar read that the notices never mention, plus a 1.2.0 drift in those notices for `decision-record`.

Ten findings were refuted, most by running the reachable input and watching the text behave correctly. The refutations are listed below so the kills are auditable.

Three items needed a decision from JP; all three were decided the same day, each on its first option (see Decisions from JP). The rest is a mechanical fix batch of seven items, now ten with the decided ones. Any SKILL.md or notice edit is a plugin behavior change, so it goes out through a release cut and the plugin publish path.

## Evidence levels used in this record

- **Clean**: only what Phase 0's mechanical checks covered, plus surfaces at least one reviewer read in full that carry no confirmed finding.
- **Reproduced**: the verifier ran the failing thing and watched it fail. For text-behavior claims this means a blind proxy run (`claude -p` on Sonnet, or `codex exec`) given the live SKILL.md and the reachable input, with no mention of the finding. For consistency claims it means the grep, diff, or git command that shows the disagreement.
- **Verifier-confirmed by argument**: no reproduction; confirmed by reading the cited text. No confirmed finding in this record rests on argument alone.

Caveat on proxies: the behavior reproductions ran on Sonnet and on Codex, not on the session model. In one case (F13) Sonnet caught the defect and Codex did not, twice. Since 116 of the skill's 137 recorded fires were on Codex, that split is itself material.

## Clean

Phase 0 mechanical checks, all passed at the reviewed commit:

- Delivery: the outcome-shaping subtree, and the whole decide plugin, are byte-identical across the source, the installed Codex cache (`~/.codex/plugins/cache/turbo-mode/decide/1.2.0/`), and the GitHub mirror checkout (`/Users/jp/Projects/active/codex-tool-dev/plugins/turbo-mode/decide/`). `codex plugin list` shows decide@turbo-mode installed and enabled at 1.2.0. The marketplace entry uses a relative path. `~/.claude/skills/decide` resolves to the plugin source. The mirror repo is clean at its 1.2.0 commit.
- Validation: `quick_validate.py` reports valid with no complaints. `agents/openai.yaml` parses. Frontmatter parses; the description is 81 words. `git diff --check` is clean. `scripts/check-library-integrity.sh` passes every structural check; its one failure is the unrelated unmanaged `~/.claude/skills/braindump` entry.
- Every skill outcome-shaping names exists and resolves on this machine.

Target and plugin surfaces read in full by at least one reviewer, with no confirmed finding:

- `plugins/decide/skills/outcome-shaping/agents/openai.yaml`
- `plugins/decide/.claude-plugin/plugin.json`
- `plugins/decide/README.md` (one reviewer claimed its forward-chain sentence at README.md:14 fails; the verifier showed it does not)
- `plugins/decide/CHANGELOG.md`

Not clean: `SKILL.md` (F1, F4, F10, F13, F15, F2), `examples/interaction-examples.md` (F4, F13), `PRIVACY.md` (F2, F15), `TERMS.md` (F2).

Neighbor skills were read as routing surfaces only. Their own defects were out of scope, so no clean claim is made about them. Out-of-target observations that surfaced are listed near the end.

## Confirmed findings

Paths below are relative to `plugins/decide/skills/outcome-shaping/` unless they name the plugin root. All six are medium after verifier re-grading. None is high: a live human is present by contract in every case (SKILL.md:25), so no work is lost and no wrong verdict is produced without a chance to correct it. None is low: each one either misleads the next lane in writing or sends a session on a wasted round trip.

### F1. The Exits table has no route to `option-shaping`

Class: gap. Evidence: reproduced. Found by all four dimensions.

**The lane can put two or three sketch-level options on the table itself, and its Exits table has no row for what to do with them.** The missing-options handling says "Offer two or three sharply contrasting concretes to react to" (SKILL.md:34). The Exits table then routes only to `making-recommendations` for options "clear enough to compare" (SKILL.md:86) or `ideate` for a field "too thin to want anything yet" (SKILL.md:87). The state between those two, named options that are still sketches, is exactly the entry condition of `option-shaping`, a sibling in the same plugin. The word `option-shaping` appears nowhere in the outcome-shaping subtree. `making-recommendations` treats that state as a hard stop and bounces it back: "name `option-shaping` ... and stop. A direct request for a pick does not waive this stop" (`plugins/decide/skills/making-recommendations/SKILL.md:30-32`).

History confirms drift rather than a drawn boundary. The table was written on 2026-07-02 (commit 26d7ae9). `option-shaping` landed on 2026-07-13 (commit fc7e7a0) and backfilled routes into `ideate` and `making-recommendations` but not here. The table was edited again on 2026-09-01 (commit 3da8e35) to add the `to-questionnaire` row, still without this one.

Reproduction: two blind proxies were given the full SKILL.md plus the names and descriptions of every sibling skill, so the roster was available as it is at runtime. When the user said the options were "still just names," the agent found `option-shaping` from the roster. When the user asked directly for a pick, the agent handed off to `making-recommendations` while itself noting "Both are still one-line sketches, so that lane may need to develop them before it can rank." That is the wasted hop the finding predicts.

Verifier corrections: the README's "each member routes to its neighbors" sentence (README.md:14) does not fail here, because outcome-shaping's forward neighbor is `ideate`, which it does name. The 2026-07-02 live-fire record shows the concretes-offering beat firing, not the failure. And a bare row is not enough: `option-shaping` freezes "exactly the candidates the user selected" (`plugins/decide/skills/option-shaping/SKILL.md:12`), while concretes offered from inside this lane are the agent's probes. `ideate` already handles that with "Ask them to fix the candidate set before handoff" (`plugins/decide/skills/ideate/SKILL.md:32`). The new row needs the same clause.

Fix: add one Exits row between the `making-recommendations` and `ideate` rows, with the candidate-set clause. Leave the frontmatter description alone; it is near its word cap and `option-shaping` guards that direction itself.

### F13. A restatement that adds new content is treated as settled without pricing the new content

Class: contract-defect. Evidence: reproduced (Codex, twice; Sonnet caught it).

**The own-words restatement is the last of three settle conditions (SKILL.md:69), and the skill's own philosophy predicts it will change the object being settled.** "Articulation constructs it" (SKILL.md:10). When the user's restatement carries content the read never held, that content has not survived a priced trade (SKILL.md:22), yet the conjunction reads as satisfied and the capsule carries the new shape downstream "so the next lane starts from the settled shape instead of re-interviewing it" (SKILL.md:94). The 2026-07-02 live fire shows the input is ordinary: JP's restatement added "reassurance," content five turns of steering had not contained.

Reproduction: a six-turn transcript with a priced trade accepted for one shape, then a restatement adding "I want a new hire to be able to fix a red build on their own without coming to me." Sonnet caught it, priced the new clause, and reported not-yet-settled. Codex, in two runs, declared it settled, folded the unpriced clause in, and re-attributed the earlier price to it: "You accept a week of work and a suite that runs twice as slowly ... independent recovery." Then it routed to `design-exploration`. The capsule beat "the trades the user already accepted" (SKILL.md:103) would carry that false attribution to the next lane.

Verifier corrections: the contract is unrouted rather than silent. Load-Testing already says "Before treating any part of the shape as settled, price it at least once" (SKILL.md:61). What is missing is one clause at the settle point (SKILL.md:67-69) connecting that per-part rule to content the restatement itself authors. The examples file does not license skipping the re-price; its Own-Words Close example (`examples/interaction-examples.md:74-80`) simply never shows a divergent restatement, so it fails to demonstrate the step rather than contradicting it.

Fix: one clause in Settled, Dissolved, or Routed saying that content a restatement introduces is a new part of the shape and is priced once before it counts, or carried in the capsule marked unpriced. Extend the Own-Words Close example to show a restatement that adds content and the re-price that follows.

### F4. Three surfaces disagree about whether the lane may recommend in place

Class: contract-defect. Evidence: reproduced.

**Core Behavior says "hand off by name when the work shifts" (SKILL.md:24). Restraints says "this lane prepares those moves and asks before becoming them" (SKILL.md:126). The Flight example says "If you want the recommendation anyway, I'll make it" (`examples/interaction-examples.md:97-99`).** The first is declared a load-bearing invariant (SKILL.md:16). The second contradicts it inside one bullet: the first clause forbids settled recommendations and the second permits the lane to become one after asking. The example resolves it permissively and names no lane. The README asserts the opposite of what the example models: "Each member routes to its neighbors by name and stops at its boundary" (README.md:14) and "handoffs between lanes are named and asked, never silent" (README.md:16).

The deference itself is deliberate. Naming the flight once and then complying (SKILL.md:77) was the rebuild's answer to the methodology critique's flight-into-health objection. The defect is that the three surfaces do not agree on what complying means.

Reproduction: two blind Sonnet runs given SKILL.md plus the examples file and a transcript reaching the flight moment. The first reproduced the example's shape and named no lane. The second, after "Yeah, make it," returned "Ship in March. Do the rewrite after." with sequencing, no lean registered, no runner-up case, no field-readiness check. It resolved by fiat a case `making-recommendations` classifies as an exchange rate between the user's own goods (`plugins/decide/skills/making-recommendations/SKILL.md:67`), which that lane requires be posed priced with the lean labeled as a lean.

Verifier corrections: the Exits sentence "does not design, decide, critique, or implement" (SKILL.md:81) is the weakest anchor, since "recommend" is absent from that list. Anchor on Core Behavior versus Restraints plus the example. And the finding's proposed fix, naming `making-recommendations` in the example, may route into that lane's own hard stop and refusal exits, converting an unguarded recommendation into a routing loop. Whatever wording is chosen has to say what happens when the named lane declines. The verifier's read: the honest in-lane move at that moment is the priced values question with a labeled lean, not a pick.

Fix: needs Decision 1 below, then one edit to Restraints and one to the Flight example so all three surfaces say the same thing.

### F10. No rule for working from a compaction summary, so the own-words seam inverts silently

Class: gap. Evidence: reproduced (twice).

**After context compaction the agent no longer holds the user's exact words, and nothing tells it to act on that.** The read is rewrite-only by design (SKILL.md:19) and the capsule demands "what the user confirmed in their own words versus what is still your compression" (SKILL.md:100). Post-compaction that distinction is exactly what the agent cannot draw from memory. The lane fires deep in long sessions (the first live fire invoked it at turn 28 of 44) and Reading Context (SKILL.md:53) invites file inspection that fills the window. The 2026-07-02 methodology critique flagged this ("No conservation law") and the rebuild folded most of that critique but not this.

Reproduction: two blind runs given SKILL.md plus a labeled continuation summary carrying content but no verbatim user words. Run one asserted "You confirmed this in your own words" over the summarizer's paraphrase. Run two fabricated a verbatim attribution, `(Your words: "routine," "low-drama.")`, and promoted a trade the summary recorded as "discussed and not refused" into "Trade accepted." Neither run hedged, asked for restatement, or said it was working from a summary.

Verifier corrections: on Claude Code the state is detectable, since the continuation summary is labeled and invoked skill bodies are re-injected after compaction (capped at 5,000 tokens per skill, keeping the start of the file). So the defect is that nothing instructs the agent to act on a state it can see, and the fix belongs near the top of the file in Core Behavior, where truncation cannot drop it. The `deliberate` analogy is a mechanism error: `deliberate` re-derives from a durable store, and this lane has no store, so its only remedy is to re-ask the live human. The proposed sentence fixes false attribution and does not fix silent loss of a constraint neither the agent nor the summary retained; that second half is the ledger problem the skill deliberately declined. Also: no conversational judgment skill in this library carries a compaction clause, so this establishes a new convention. The reproduction is the argument for it.

Fix: one sentence in Core Behavior. When you are working from a summary rather than the user's actual sentences, say so and re-confirm the settled shape in their words before any capsule; mark anything you cannot source to their words as your compression.

### F2. The one write the lane permits is unspecified, and the published notices do not account for it

Class: contract-defect. Evidence: reproduced (grep and git, not a proxy).

**SKILL.md permits "a file, ticket, or durable artifact only when the user explicitly asks" (SKILL.md:107) and says nothing else about it, and PRIVACY.md says "nothing else on disk" (`plugins/decide/PRIVACY.md:7`) after a write list that omits it.** Three skills in this plugin carry an on-request write clause: `design-exploration`, `deliberate`, and `outcome-shaping`. PRIVACY's enumeration names the first two and closes "nothing else on disk," so it is false by the plugin's own contracts. The README's Storage row carries the carve-out; PRIVACY does not. `plugin.json:42` publishes PRIVACY as the privacy policy URL.

The same PRIVACY sentence, and `plugins/decide/TERMS.md:7`, also miss a separate write that 1.2.0 added: `decision-record` may now add a dated amendment section to an older record when the new decision narrows rather than supersedes it (`plugins/decide/skills/decision-record/SKILL.md:32`). Both notices still describe only "a `Status` line on the superseded record." The two 1.2.0 commits (dc27366, 22bfcd3) touched SKILL.md, README, CHANGELOG, and plugin.json and neither notice; `git log -- plugins/decide/PRIVACY.md` ends at the 1.1.0 commit. The words "amendment" and "addendum" appear in neither file.

Verifier corrections: the SKILL.md silence is low severity on its own. A live human is present, an improvised path is corrected in one turn, and the global Markdown auto-commit rule committing a user-requested capsule is that default working as intended. The medium rating rests on the published PRIVACY and TERMS contradictions alone. The "unnamed fourth off-machine path via a ticket" sub-claim overstates what the text establishes; the Exits table has no tracker route and the clause reads as a restraint listing output forms. The proposed "the capsule is the brief" framing would introduce an artifact definition the lane does not have; if SKILL.md is edited, one clause mirroring `design-exploration`'s (`plugins/decide/skills/design-exploration/SKILL.md:41`) is enough.

Fix: PRIVACY and TERMS edits are mechanical (fix batch items 5 to 7). Whether SKILL.md says anything about the requested brief is Decision 3.

### F15. PRIVACY does not disclose the calendar read the skill grants unconditionally

Class: contract-defect. Evidence: reproduced (the read grant, not a transmission).

**Load-Testing grants "the repo, the calendar, and the last three decisions are witnesses this lane is allowed to call" (SKILL.md:63), and PRIVACY's read disclosure names only repository files, git state, conversation context, and evidence the user names (`plugins/decide/PRIVACY.md:7`).** The grant is permission language, unconditioned, and not bounded by Reading Context (SKILL.md:53), which is a permission rather than an exclusive gate. "Calendar" appears exactly once across all eight decide skills, so PRIVACY's list is not generalizing over a pattern; it omits a genuine outlier. The repo's own contract ledger (`docs/agents/contract-decisions.md:118-120`) treats calendar access as a real connector-served capability with its own access question. The mirror copy of PRIVACY is byte-identical, so the omission is what any external reader sees.

Reproduction: given only SKILL.md and asked to list every information source the text permits, a fresh agent listed "The calendar" as its own item, separate from the four user-pointed items. Given a calendar tool and an on-call-rotation want in which the user never named a calendar, the agent opened "I haven't searched your calendar yet," treating the unprompted query as a pending in-lane instrument. No calendar call or off-machine request was observed.

Verifier corrections: this is under-disclosure, not contradiction. PRIVACY closes only its write list; its read list is phrased permissively ("may cause the runtime to read") and never claims to be exhaustive. The off-machine leg is the weak one, resting on three stacked contingencies, and should be a secondary note. The non-contingent defect holds with zero contingencies: the skill authorizes reading a personal calendar the user never named, and the published read disclosure does not mention calendars or connector-served personal records.

Fix: needs Decision 2 below. The cheapest side conditions the calendar witness on user-pointing in SKILL.md, leaving the repo and last-three-decisions witnesses unconditional, which brings it inside PRIVACY's existing "evidence the user names."

## Decisions from JP

JP walked through the three decisions one at a time on 2026-09-03, after this record was first saved, and chose option 1 on each. The options are kept as written so the alternatives stay auditable.

### Decision 1 (F4): what does "comply" mean when the user flees a hard trade and asks for a recommendation?

Decided: option 1.

1. **In-lane, guarded (lean).** The lane may answer, but as the priced values question with a labeled lean, never a pick, and it names the unpriced trade in the same turn. Restraints and the Flight example get reworded to say that. Keeps the deliberate deference, keeps the guards, and never promises a switch a receiving lane may refuse.
2. **Always hand off by name.** Restraints and the example both route to `making-recommendations`. Cleanest match to Core Behavior and the README, but the receiving lane's field-readiness hard stop and its "options not comparable" exit can bounce a craft-versus-deadline collision straight back, so the wording must say what happens then.
3. **Leave as is.** Accept that the example models an unguarded recommendation. Not recommended: the reproduction shows it produces a settled pick with none of the plugin's guards at the moment fluency is most likely to be rubber-stamped.

### Decision 2 (F15): which side moves, the skill or the notice?

Decided: option 1.

1. **Condition the calendar witness in SKILL.md (lean).** "the repo, the last three decisions, and any calendar or record the user points you at." One clause; PRIVACY then already covers it under "evidence the user names."
2. **Widen PRIVACY's read list.** Name calendar and connector-served personal records as sources the skill may read on its own initiative, and say whether such a read can leave the machine. Keeps the unconditional grant; costs a notice edit and a standing disclosure about personal data.

### Decision 3 (F2, SKILL.md half): should the skill say how a user-requested brief is written?

Decided: option 1.

1. **One clause mirroring `design-exploration` (lean, weakly).** Place it per repo convention, ask one path question if none is clear, leave it uncommitted for the user. Brings the two write-capable judgment lanes in this plugin into agreement.
2. **Say nothing.** The global Markdown auto-commit default then applies, and the verifier judged that defensible: a user-requested capsule being committed is the default working as intended. Costs nothing and keeps machinery out of a judgment lane.

## Fix batch (mechanical, seven items)

Apply after approval through `apply-findings`, in a `worktree-task-cycle` satellite. Items 1 to 4 and 8 to 10 change plugin behavior or its published notices, so the landing needs `release-cut` (minor: the skill gains a route and two settle-time rules) and a CHANGELOG entry, then publish per AGENTS.md Plugin Layout And Delivery.

1. `SKILL.md` Exits table: add a row between `making-recommendations` and `ideate`: two or more options are named but sketch-level or unevenly understood, ask the user to fix the candidate set, then `option-shaping`. (F1)
2. `SKILL.md` Settled, Dissolved, or Routed: one clause stating that content a restatement introduces is a new part of the shape and is priced once before it counts, or carried in the capsule marked unpriced. (F13)
3. `examples/interaction-examples.md` Own-Words Close: extend the example so the restatement adds content the read did not carry and the reply prices it before calling it settled. (F13)
4. `SKILL.md` Core Behavior: one sentence for working from a compaction summary rather than the user's sentences: say so, re-confirm the settled shape in their words before any capsule, and mark anything unsourceable as your compression. (F10)
5. `PRIVACY.md` write enumeration: add outcome-shaping's on-request file write so "nothing else on disk" is true again. (F2)
6. `PRIVACY.md` off-machine sentence: replace the "Three paths" count with count-free phrasing so it stops needing maintenance on every change. (F2)
7. `PRIVACY.md` and `TERMS.md`: add `decision-record`'s dated amendment-section write on an older record, the 1.2.0 change both notices missed. Out of target but on an in-scope surface. (F2)

Settled by the decisions (all option 1):

8. `SKILL.md` Restraints and `examples/interaction-examples.md` Flight Named Once: the lane may answer in place, but only as the priced values question with a lean labeled as a lean, never a pick, naming the unpriced trade in the same turn; reword both surfaces so they and Core Behavior agree. (F4, Decision 1)
9. `SKILL.md` Load-Testing the Want: condition the calendar witness on the user pointing at it, leaving the repo and last-three-decisions witnesses unconditional. No PRIVACY read-list change. (F15, Decision 2)
10. `SKILL.md` The Capsule: one clause mirroring `design-exploration`: when asked for a durable brief, the capsule is the brief, placed per repo convention with one path question if none is clear, left uncommitted for the user. (F2, Decision 3)

## Refuted findings

Each line: the claim, then the verifier's refutation reason. Eight of the ten were tested with blind proxy runs that did not fail. Full verdict text is in the companion verdicts file.

- **F3. `outcome-check` names outcome-shaping as its goal-metric source but the capsule has no observable beat and never persists.** Misreads `outcome-check`'s fallback (`skills/outcome-check/SKILL.md:18`): it routes back only when no goal was ever named, and has its own `unverifiable-here` verdict for a lost record. The clarified outcome leaves the lane via the capsule (SKILL.md:94) into lanes that do write artifacts. The wording predates outcome-shaping and was never satisfied by its predecessor either. Adding an observable beat is `acceptance-map`'s job and the accretion the methodology critique warned against.
- **F5. An in-lane recommendation at the flight moment carries no seam-marking.** The flight-naming beat (SKILL.md:77) is one turn with the compliance and already names the unpriced trade and the live rival read; rival-reads (SKILL.md:47), the settle test (SKILL.md:69), and the no-settled-recommendation restraint (SKILL.md:126) stay in force. Two proxies passed. The proposed second naming re-litigates the deliberate once-only rule.
- **F6. The description names `grill-with-docs` as a routing target; no body surface does.** The Exits row's condition is `grill-me`'s contract verbatim; `grill-with-docs` is distinguished by durable doc writing, which the row's condition does not call for. The whole library names `grill-me` alone for pressure-testing. Making a file-writing lane a default exit from a read-only lane would widen the boundary, not repair it.
- **F7. Type the Mud's missing-information bullet omits the `to-questionnaire` route.** The bullet's list (SKILL.md:35) is exemplars after "Name the evidence that would settle it and route toward it," not a closed route list. Exits owns routing and Core Behavior (SKILL.md:24) delegates to it. Two proxies typed a person-shaped unknown correctly and named `to-questionnaire` unprompted.
- **F8. The `to-questionnaire` exit is an operative handoff to a skill the agent cannot invoke.** The runtime refusal itself supplies the token and forbids improvising; a blind proxy named `/to-questionnaire` and printed the capsule unprompted. The capsule is chat-only, so it is already in context. The same un-tokened pattern exists library-wide, including `scope-cut` in this plugin, so a one-row patch would be inconsistent. Inert on Codex, where most fires happen.
- **F9. The `ideate` exit hands `ideate` the state `ideate` declines.** Two different states: an empty option field versus a muddy goal. `ideate`'s own sentence states the discriminator ("the only reframing ideate owns is of the solution space, never the goal", `plugins/decide/skills/ideate/SKILL.md:14`). The capsule already carries the frame. Half the proposed fix is already the live text (SKILL.md:34). Two proxies produced the frame and offered both moves.
- **F11. Parked and evidence-routed endings resume later, but nothing carries the ripening condition or shape past the session.** The evidence route is a handoff point, so the capsule fires there. Parked (SKILL.md:75) is deliberately bare, one bullet under "do not manufacture a consolation deliverable." Cross-session persistence is the handoff plugin's job and a documented family boundary (README.md:16). Two proxies produced a usable re-entry summary unprompted. Residual: the capsule's trigger (SKILL.md:98) does not name Parked; that is the honest narrow version if anyone reopens it.
- **F12. Nothing covers the user shaping someone else's want.** Two proxies on the finding's own scenario surfaced the authorship gap unprompted, including a capsule beat "Not confirmed. This is your reading of the VP's one-liner." The confabulation guard, the honest-seam beat, the `to-questionnaire` exit, and the obligation register already do the work. The finding re-specifies the lane's object.
- **F14. The unattended guard names contexts it cannot detect and gates its stop behavior on a second test.** A blind subagent proxy with a fully specified want opened "I did not run the shaping interview ... reporting what a live shaping conversation would have raised, and stopping." The first sentence of SKILL.md:25 is the rule; the second elaborates the sharpest sub-case. `deliberate`'s "detectable" wording is an exit-token caveat, not a detection cue, and importing it would hand the agent an excuse. The 12 model-triggered fires cited as stakes were attended sessions.
- **F16. Four non-plugin skills the lane routes to are undocumented as plugin dependencies.** The README Storage table (README.md:32) records writes, not routes, so `scope-cut`'s `triage` mention is not a precedent. Six of eight member skills reference 12 external skills 36 times; a one-line note for this skill alone would create the asymmetry it claims to cure. The charter's Retirement rule already obliges the pruner to update every routing contract, and `scripts/check-library-integrity.sh` records cross-skill name tracking as a deliberate non-goal.

## Observations outside the target

Surfaced by verifiers while refuting; not findings against outcome-shaping, listed so they are not lost.

- `to-questionnaire` is Claude-gated (`disable-model-invocation: true`, `skills/to-questionnaire/SKILL.md:4`) with no `agents/openai.yaml`, so it lacks the `policy.allow_implicit_invocation: false` the library convention requires for the pair, leaving it model-reachable on Codex. (from F8)
- Un-tokened routes to user-invoked skills exist library-wide: `scope-cut` to `next-steps` three times, `decision-owner-map` to `to-questionnaire`, `explain-codebase` to `zoom-out`. A tightening, if wanted, is a sweep, not a row. (from F8)
- `outcome-check`'s "Pull it from the source: the original clarified outcome (`outcome-shaping`) ..." parenthetical (`skills/outcome-check/SKILL.md:18`) is loose enough to suggest a durable outcome-shaping artifact exists. Low-value polish in a different skill. (from F3)
- The capsule's trigger ("at a handoff point, or when the user asks to summarize", SKILL.md:98) does not cover Parked. Deliberate per the restraints, but the narrow gap is real if a maintainer ever wants a Parked closure to carry the ripening condition. (from F11)

## Apply route

On approval: `apply-findings`, through `worktree-task-cycle`. `release-cut` plus a CHANGELOG section for the plugin behavior and notice changes (lean: minor, 1.3.0). Publish per AGENTS.md Plugin Layout And Delivery: the landed bump authorizes the local Codex republish; mirror sync and push stay ask-gated.

## Evidence boundary

- True at commit `22bfcd3`. Every `path:line` citation above was re-checked against that commit by the orchestrator before this record was written; later edits can invalidate any of them. Re-verify against live source rather than trusting this record.
- What was inspected: the three target files and five plugin surfaces in full by every reviewer; 18 neighbor skills, AGENTS.md, `agent-facing-design`, the two 2026-07-02 reviews, and the unmanaged `braindump` skill by at least one reviewer (coverage lists below). Verifiers read 43 distinct files between them. Not inspected: the neighbors' own correctness, keep/prune merit (out of scope by the gap-review contract), and the `work-skills/` variant of this skill (a deliberate public-safe copy, documented as not a delivery path).
- What "reproduced" rests on: blind proxy runs on Sonnet via `claude -p` and on Codex via `codex exec`, plus read-only greps, diffs, and git history commands. Every proxy was non-mutating and given no hint of the finding under test. The proxy prompts and outputs lived in the session scratchpad and were not preserved; the verifiers' descriptions of each run are in the companion verdicts file.
- What this record does not establish: behavior on the session model (Fable), a completed off-machine transmission for F15, or that the fix batch as worded is correct. The fixes are proposals; the verifiers corrected several of the reviewers' proposed mechanisms, and those corrections are folded into the findings above.

## Appendix: coverage and artifacts

Reviewer coverage (files read in full, per dimension):

- consistency (7 raw findings): the three target files, the five plugin surfaces, `ideate`, `option-shaping`, `design-exploration`, `scope-cut`, `outcome-check`, `grill-me`, the first-live-fire review, AGENTS.md.
- lifecycle (7): the three target files, the five plugin surfaces, `deliberate`, `design-exploration`, `making-recommendations`, `ideate`, `option-shaping`, `scope-cut`, `to-questionnaire`, `prototype`, `outcome-check`, `grill-me`, `work-router`, `agent-facing-design`, `save-handoff`, AGENTS.md, both 2026-07-02 reviews.
- edge-cases (4): the three target files, the five plugin surfaces, `scope-cut`, three sibling `openai.yaml` files, both 2026-07-02 reviews.
- routing (3): the three target files, the five plugin surfaces, `option-shaping` and its `openai.yaml`, two sibling `openai.yaml` files, `grill-me`, `reality-check`, `reflect`, the unmanaged `braindump`, nine `openai.yaml` files across review-family and handoff, AGENTS.md.

Fleet: 21 agents, 274 tool calls, about 1.97M subagent tokens, 30.4 minutes wall clock.

Companion file, preserved with this record: `docs/reviews/2026-09-03-outcome-shaping-gap-review-verdicts.json` — every merged finding with its source findings and severity divergence, every verifier verdict in full (reason, reproduction note, correction, files read), the 21 raw findings, the reviewers' file lists, and the workflow's progress log.

Not preserved (session-temporary): the workflow journal and the verifiers' proxy prompt files.
