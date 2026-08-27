---
type: review
date: 2026-08-26
scope: "plugins/review-family 0.11.0 — all 20 surfaces: 5 SKILL.md, 5 agents/openai.yaml, 3 references/examples, plugin.json, README, CHANGELOG, PRIVACY, TERMS, LICENSE; plus delivery state (Codex cache, Claude symlink, marketplace entry, GitHub mirror)"
reviewed_commit: b5d3a1e2cd1828f012b1d7da4b449779fe4ca24f
method: "gap-review — inline Phase 0 scout (delivery diffs + AGENTS.md Validation Ladder), then a 5-dimension Workflow fan-out (cross-surface consistency, edge-case behavioral audit, lifecycle gap walk, routing/dual-runtime delivery, intra-family vocabulary coherence), dedup, then one refute-default adversarial verifier per finding. 33 agents; 29 raw findings, 28 after dedup, all 28 verified."
posture: "read-only, evaluation-only — no target file was edited, committed, or published by this run"
---

# Gap Review — `plugins/review-family` 0.11.0

Date: 2026-08-26. Target: `/Users/jp/.agents/plugins/review-family` — dual-runtime Claude Code / Codex plugin, five skills (`implementation-review`, `review-reviewer`, `scrutinize`, `scrutinize-skill`, `system-design-review`).

Evaluation only. Nothing in the target was edited, committed, or published by this run.

---

## What This Run Actually Checked

Five independent review dimensions read the plugin's twenty surfaces; every deduplicated finding then got one adversarial verifier whose instruction was to refute it.

Dimensions: cross-surface consistency and documentation accuracy; edge-case behavioral audit; lifecycle gap walk; routing and dual-runtime delivery contracts; intra-family vocabulary coherence.

Counts: 29 raw findings → 28 after dedup → 14 confirmed, 14 refuted. The 14 confirmed merge to 12 reported findings (one root cause was found by three dimensions at three different severities).

Refutation rate was exactly 50%. That is the run working as intended, not a weak review — the refutations below are argued from the text and several were settled by running the failing thing.

---

## Clean

Two things, and nothing beyond them.

**Phase 0 mechanical checks, all passing:**

- Source is byte-identical to the installed Codex cache at `~/.codex/plugins/cache/turbo-mode/review-family/0.11.0` (`diff -rq` empty; `scripts/codex-plugins-sync.sh --check` exits 0).
- `~/.claude/skills/review-family` symlinks to the source and resolves.
- `plugins/marketplace.json` carries a `review-family` entry with the required relative path `./.agents/plugins/review-family`; the file parses.
- `scripts/check-review-family.sh` is green — the read-only CANON core is consistent across all five skills, the bounded-review core across the three adversarial skills.
- `quick_validate.py` passes on four skills; on `review-reviewer` it emits only the `disable-model-invocation` unexpected-key complaint, which the repo's Validation Ladder declares an accepted class.
- All five `agents/openai.yaml` parse as YAML; `plugin.json` and `marketplace.json` parse as JSON.
- Every internal reference path named by a `SKILL.md` exists.
- Every externally-named skill resolves in the library (`methodology-check`, `behavior-smoke-test`, `triage`, `steelman`, `recheck-investment`, `acceptance-map`, `tech-debt-scan`, `agent-facing-design`, `skill-ux-design` are dual-runtime; `methodology-critique` and `skill-benchmark` are Claude-only).

**Surfaces at least one dimension read in full and reported nothing against:** `LICENSE`, `skills/system-design-review/references/system-design-dimensions.md`, `skills/implementation-review/examples/review-findings.md`, and the `agents/openai.yaml` files for `implementation-review`, `scrutinize`, `review-reviewer`, and `system-design-review`.

This run claims nothing about the plugin beyond those two lists. It did not run a live invocation of any of the five skills as a whole; three verifiers did run targeted live probes, and those are labelled below.

---

## Confirmed Findings

Twelve, ordered by verifier-adjusted severity. Each is labelled by its strongest evidence: **reproduced** means a verifier ran or traced the failing thing end to end and watched it fail; **argued** means the verifier confirmed it by reading and reasoning over the text.

### 1. HIGH — `scrutinize` orders a verdict token its own enum forbids, with no carve-out for a disqualifying finding

`skills/scrutinize/SKILL.md` · contract-defect · reproduced · found by all three of *edge-case*, *consistency*, *coherence*

`SKILL.md:32` closes the ordinary enum: "Normal scrutiny verdicts are exactly one of `Reject`, `Major revision`, `Minor revision`, or `Defensible`." `SKILL.md:80` then orders, unconditionally: "for bounded ordinary scrutiny, write `Verdict: Partial review only`." That token is not in the enum and is defined only inside the *readiness* enum at `:47`. A third surface, Guardrails `:73`, resolves bounded mode a third way — it bars only `Defensible` and `Ready to Execute`, leaving `Reject` live.

The harm is the missing carve-out, not the vocabulary. A bounded ordinary scrutiny that finds a Critical failure has two live instructions: `:73` permits `Reject`; `:80` orders `Partial review only`. Following `:80` replaces "the reviewed slice failed" with "the pass was incomplete." `:73` also classifies every externally-narrowed review — a caller-restricted scope, an assigned lens, a panel seat, sampled coverage — as bounded, so this fires on panel-seat reviews, which is exactly where a Critical find is the expected outcome.

**Evidence, and an honest divergence.** Three verifiers graded this high, medium, and low. The low grade came from the only verifier that ran live trials: 8/8 `claude -p` trials wrote `Partial review only`, including 4/4 with `references/review-format.md` loaded and its four-token fence in view. Those trials confirm agents follow `:80` reliably and unconditionally — which is what makes the missing carve-out matter, not what excuses it. They did not include a Critical-finding scenario, so the specific suppression is traced from the text, not observed. I report at the highest adjusted severity per the merge rule, and the high grade rests on the reasoned suppression path.

Git history shows the mechanism: `:80` shipped in `047c8ca` (2026-06-09); the closed-enum sentence at `:32` was added three weeks later in `3d6594d` (0.7.0) without reconciling it. `check-review-family.sh` deliberately excludes verdict vocabulary from its drift check, so nothing catches this.

The sibling skills show both possible intents. `implementation-review` puts `Partial review only` inside its enum *and* adds a precedence order. `scrutinize-skill` keeps the four-token enum and simply bars `Defensible` in bounded mode, adding no fifth token. `scrutinize` did neither.

**Verifier corrections carried forward:** the capitalization complaint is refuted and must not be acted on — `Partial review only` (sentence case) and `Partial Review Only` (Title Case) are two different verdicts in two differently-cased enums, each internally correct. Do not sweep casing family-wide.

### 2. MEDIUM — `implementation-review`'s bounded mode collides with its own verdict precedence, and the shipped example teaches the losing rule

`skills/implementation-review/SKILL.md` · contract-defect · reproduced · *edge-case*

`:140` orders bounded mode to "mark omitted areas `unverified`". `:159` defines `blocker` — unqualified — as including "leaves a material requirement unverified". So a bounded pass omitting a material requirement now holds a blocker. `:169` matches `Blocked` on "at least one `blocker`", and `:174` puts `Blocked` first in precedence. But `:193` enumerates only `Partial review only` and `Split required` for bounded mode.

The author's intent is visible: `:169`'s third clause is deliberately qualified "in a full review". `:159`'s unqualified clause routes around that qualification via `:169`'s first clause.

**Reproduced against the skill's own shipped example.** `examples/review-findings.md:33` renders "[blocker] Billing callback requirements remain unverified" and `:43-44` render "Blocker count: 1 / Verdict: Partial review only" — a state `:174` forbids. I confirmed both files independently.

**Verifier corrections carried forward:** the practical failure is verdict nondeterminism between sessions reading the same text, not a uniform `Blocked` (the collision needs the omitted requirement to be *material*). The seam-dropping sub-claim is partly wrong — `:142` keys seam-naming to the judgment, not the verdict token; only the Verdict-section rendering slot at `:189` is verdict-keyed. Severity graded down from high because neither branch grants false clearance: both withhold `Ship`.

### 3. MEDIUM — Current Claim Check's four action buckets are keyed on three different axes, so reachable claims land in no bucket

`skills/review-reviewer/SKILL.md` · contract-defect · reproduced · *edge-case*

The 0.3.7 repair states the invariant it was protecting at `:202`: key on the disposition "so a partially-valid-but-rejected claim is not left out of every bucket." Two leaks survive it, because `Act On Now` keys on classification + severity + disposition, `Do Not Act On` on disposition, `Needs Verification` on classification, and `Deferred` on scope.

- A `Partially valid` claim, `should-fix`, dispositioned `verify-first` fails all four predicates. `:67` explicitly sanctions reading all five dispositions against all four classifications, so the combination is reachable. `:177` forbids a fifth bucket.
- The verifier found a third leak the reviewer missed: `defer` is defined at `:110` as "outside the current review scope **or not urgent here**", while the `Deferred` bucket at `:210` admits only claims "intentionally outside current scope". An in-scope-but-not-urgent `defer` also lands nowhere.

I confirmed both against the live file.

**Verifier corrections carried forward:** the reviewer's second shape (`note` + `act`) does **not** hold and should be dropped — `note` is defined as "does not require immediate action", which contradicts `act`. The proposed fix (make all four buckets disposition-keyed) is not a pure re-key: dropping the severity conjunct from `Act On Now` newly admits `note`+`act` into it, a behavior change beyond closing the gap.

### 4. MEDIUM — `scrutinize` declares its verdicts expire and mandates no datum by which anyone can tell

`skills/scrutinize/SKILL.md` · gap · argued · *lifecycle*

`:32` says `Defensible` and `Ready to Execute` "expire when the artifact changes." But the mandatory `Target And Evidence` field list at `:22` is "exact target, inspected files or sources, skipped or unread material, proof class, and whether runtime or current-state evidence was checked" — no commit SHA, mtime, version, or date. `scrutinize-skill`'s `Target And Surface` at `:66` has the same shape. `implementation-review` is the exception: `:28` requires recording "repo root, base/ref, current branch, and `HEAD`". So the anchoring datum already exists in the family and propagating it is one clause.

Downstream, `review-reviewer` step 5 (`:33`) covers PR targets and "commit-pinned non-PR targets" and gives no rule for an *unpinned non-PR target* — precisely the shape `scrutinize` emits for a plan document. That is a hole in a boundary rule 0.11.0 tightened.

I independently confirmed the field lists and that `grep -i expire` across all five skills returns exactly two hits.

**Verifier corrections carried forward, and they matter:** the reviewer's forcing mechanism is wrong. The cited fallback at `:33` is PR-scoped; the rule that actually catches the case is `:103`, which is general, and yields `unverified` for historical truth — epistemically correct given no snapshot. `under-evidenced` is *not* reached, because target access succeeds. The title's "no reviewer records the target version" is false twice over (`implementation-review:28`; `review-reviewer:127`). And `review-reviewer:17` permits git inspection, which often recovers the boundary anyway. The reduced, defensible finding is: **`scrutinize` declares an expiry with no evaluable anchor, and `review-reviewer` step 5 has no rule for the unpinned non-PR target `scrutinize` produces.** The reviewer's third paragraph (in-family authorship provenance) does not hold and is dropped.

### 5. MEDIUM — `implementation-review` mandates re-reviews and governs none of them

`skills/implementation-review/SKILL.md` · gap · argued · *lifecycle*

`scrutinize:34` is the family's only cross-pass discipline: re-read live, verify fixes against the artifact and diff rather than the description, treat prior findings as hypotheses to re-earn, hunt new defects, credit what held. `implementation-review` creates the re-review arc itself — `:171` says "split along the named seams, then re-review" — and says nothing about how a later pass relates to an earlier one.

**Verifier corrections carried forward, and they narrow this substantially:** the reviewer's claim that "nothing objects" is false. Evidence Gate item 1 *does* object, because the Changed-Area Ledger is defined over the diff and pass 2's scope authority (branch-vs-base) includes the fix commits — so the refactored file gets its own row, falsification attempt, and linked requirements. The reviewer also had the scope-authority argument backwards: selecting branch-vs-base is the partial guard, not an aggravator.

**The surviving hole is narrow:** a *Requirements* Ledger row marked `satisfied` in pass 1 can be carried forward with a stale line pointer, and no gate item can detect it, because that ledger is spec-derived and therefore looks complete. The strongest version of the finding is that the most common re-review arc — `Blocked` → fix → second pass — is the one the skill never names at all.

The scrutinize-skill half of the reviewer's proposed fix pushes against a deliberate, changelogged decision (0.9.0 routes the post-fix claim to `behavior-smoke-test` *instead of* a re-review) with no concrete failure shown. Discount it. Including `system-design-review` in the absence is overreach — it issues no verdict and mandates no fix cycle.

### 6. LOW — `scrutinize-skill` reuses `Defensible` verbatim with none of the expiry gloss that defines it

`skills/scrutinize-skill/SKILL.md:72` · gap · argued · *lifecycle*

`scrutinize:32` defines `Defensible` as claiming "serious search was exhausted without a disqualifying find — they do not certify soundness, and they expire when the artifact changes." `scrutinize-skill:72` uses the identical four-token enum and scopes the verdict only by *altitude* ("grades the behavior contract as written"), never by time. `check-review-family.sh`'s own header states these skills load independently, so an agent running `scrutinize-skill` never sees the definition.

**Report this one with the divergence stated.** A second dimension raised the same theme against `implementation-review`'s `Ship` and its verifier **refuted** it, on grounds the first verifier substantially conceded: `Ship`'s target is snapshot-identified by construction (`:28`, scope authorities 3–5, and a mandatory `Review Scope` section all record `HEAD`), and two of `Ship`'s five clauses are already facts about the search rather than the artifact. Both verifiers also agree the "three of four siblings carry the doctrine" premise is really two of four. So the `Ship` half is dead; only the `scrutinize-skill` half survives, and it survives at low.

### 7. LOW — README's Trigger cell for `review-reviewer` states a condition that is necessary but not sufficient

`README.md:38` · contract-defect · reproduced · *consistency*

Under a column literally headed "Trigger", README gives `review-reviewer`'s firing condition as "Supplied review, critique, audit, reviewer output, or pasted claims that need checking" — with no mention of the explicit-only gate. Every other surface states it: `SKILL.md:4` (`disable-model-invocation: true`), `:13`, `:15`, `:25`; `agents/openai.yaml` (`allow_implicit_invocation: false`); both of `plugin.json`'s `review-reviewer` starter prompts carry `$review-reviewer`; README's own Usage Patterns at `:84` and `:90` carry the token.

**Verifier corrections carried forward:** there is **no routing consequence** — the loader strips the skill from the model-invocable set, verified against this session's own inventory, so no README text can cause a mis-fire. The residual harm is one human's wrong expectation. README `:29` is **not** a defect and should be left alone: it sits under a column headed *Description*, makes no firing claim, and the reviewer's proposed fix wrongly applied a trigger remedy to it. The secondary "stale" wording complaint does not hold. **One cell, not two rows.**

### 8. LOW — `PRIVACY.md` and `TERMS.md` describe a Codex-only plugin

`PRIVACY.md`, `TERMS.md` · contract-defect · reproduced · *consistency*

Both shipped legal surfaces read as if Codex were the only runtime, while README `:3` says "for Claude Code and Codex" and every `SKILL.md` is runtime-neutral by contract. `git log` shows only `047c8ca` and a whitespace reflow touched them, so the 0.2.0 dual-runtime unification and every later de-Codexing pass (0.3.8 fixed exactly this class in `scrutinize-skill`'s companion) skipped them.

**The verifier found the decisive evidence and the correct target wording:** `plugins/git-cycle/PRIVACY.md` is the *same template written neutrally* — "may cause the runtime to inspect"; "Codex, Claude, account handling, model requests, telemetry" — and was authored eight days *after* review-family's unification. So the neutral wording is the repo's own later convention and these files are pre-unification residue.

**Verifier correction that changes the fix:** only **4 of 6** Codex mentions are defective. `PRIVACY.md` para 1 and `TERMS.md` para 1 (about an installed cache going stale) are **accurate as written** and are preserved verbatim in the neutral sibling, because only Codex has a versioned install cache — Claude Code reads source in place through its symlink. Replacing those two would introduce a false claim.

Severity dropped to low: the manifest URLs that advertise these files sit in the Codex-facing `interface` block and point at the 0.8.0 mirror, so the live exposure is README's pointer alone.

### 9. LOW — "pragmatic review" reaches no skill in the family

`README.md:65` · gap · reproduced · *lifecycle*

Four skills were retired with replacement routes documented only in README — a surface neither runtime reads at skill-selection time. Three of the four are covered incidentally or by design. `pragmatic-review` is the genuine gap: its replacement is `scrutinize`'s execution-readiness mode, and "pragmatic" appears in no frontmatter description or `openai.yaml` anywhere in the plugin.

**Reproduced by a single-variable forward test.** Same plan file, same config, one word changed: "Run a pragmatic review of this plan" fired **no Skill tool at all** (2/2 replicates); the control "Run an execution-readiness review of this plan" fired `review-family:scrutinize`.

**Verifier corrections carried forward:** the un-routed run still produced a substantive review that caught the plan's real defects — what is lost is `scrutinize`'s verdict vocabulary, its reject-until-proven stance, bounded-review scoping, and the confidence boundary. The user gets a review without the contract, not a bad review. The skill-usage ledger shows ~30 `pragmatic-review` fires, all explicit-token, all before the retirement, and none after; a miss writes no ledger row, so the ledger neither confirms nor refutes that the prose path has actually been hit.

**The verifier flagged a real risk in the obvious fix:** "pragmatic" reads to a general user as *practical and proportionate* — close to the opposite of `scrutinize`'s stance, and adjacent to "balanced feedback", which its description explicitly lists as a non-use. Bind the phrase rather than adding it bare. The reviewer's second half (no surface says when a retirement note may be dropped) does **not** hold and is dropped.

### 10. LOW — `review-format.md`'s Full Template emits three heading names `SKILL.md`'s section list does not use

`skills/scrutinize/references/review-format.md` · contract-defect · reproduced · *consistency*

`SKILL.md:80` declares nine default sections; the template at `:28-56` emits nine headings in the same order, six matching byte-for-byte and three differing: `Real-World Breakpoints` vs `Real-World Breakpoints And Edge Cases`, `Hidden Dependencies` vs `Hidden Dependencies Or Bottlenecks`, `Required Changes` vs `Required Changes Before This Is Credible`. `implementation-review` is the counter-example whose required sections match its examples exactly.

**Verifier corrections carried forward:** the reviewer's "downstream rules key on the short names" is **wrong** — nothing performs string matching on these headings; no script, hook, or parser reads them, and `check-review-family.sh` does not touch heading text. The `scrutinize-skill` citation is not a coupling at all: `scrutinize/SKILL.md:84` is the only reference to `review-format.md` anywhere in the plugin. The real cost is dual-maintenance staleness, and the justification should rest on single-sourcing hygiene, not a broken routing rule.

### 11. LOW — `scrutinize-skill`'s Codex starter prompt is the only one in the repo missing its invocation token

`skills/scrutinize-skill/agents/openai.yaml:4` · contract-defect · reproduced · *routing*

Four of five family starters open with the Codex token; `scrutinize-skill`'s opens with the bare name. The verifier enumerated **all 34** `default_prompt` values across `plugins/` and `skills/`: every one using the "Use \<name\> to …" form carries `$<name>` except this one, making it the sole outlier repo-wide. Git history shows the string was edited three times after creation without the token ever being added.

**Verifier corrections that change the fix:** the `plugin.json` half is **backwards** and its proposed fix must be dropped. Four of six manifest `defaultPrompt` entries are bare; the only two carrying a token are both `review-reviewer` — which tracks the documented design fact that `review-reviewer` is explicit-only and *cannot* be reached by natural language. Prefixing only the `scrutinize-skill` entry would create a new inconsistency. The CHANGELOG citation also does not support the finding (it governs `SKILL.md` prose, which already complies). **Scope the fix to `agents/openai.yaml:4`, plus `README:78` and `README:50`.**

### 12. LOW — `system-design-review`'s "unless requested" licenses a verdict the skill never defines

`skills/system-design-review/SKILL.md:56` · contract-defect · argued · *coherence*

`:56` reads "End with 2-4 sharp questions, not a verdict, unless requested." An exhaustive grep of the skill's only three files for verdict/clearance/pass-fail vocabulary returns the word "verdict" **exactly once in the whole skill** — in the sentence that licenses it. There is no enum, no severity scale, no clearance condition, no scope statement, and no verdict slot in *either* of the skill's two output contracts (`SKILL.md:26` and the reference's Output sections). Every sibling that issues a verdict fences it to a closed enum. `git log -S` shows the phrase entered at the original commit and survived the 0.9.1 compression pass unrevised.

**The verifier found a sharper mechanism than the reviewer did:** the conflict is with the skill's *own routing block* — `:14` already sends "execution-readiness review before implementation" to `scrutinize`, so `:56` lets the skill answer in chat what `:14` sends elsewhere. And the worst reachable case is the `reduced-depth` path: under sparse evidence the skill caps findings at 4 but bars nothing about clearance, while the three adversarial siblings all carry the bounded-review CANON forbidding "a full-clearance verdict for the full target" — and `check-review-family.sh` deliberately excludes `system-design-review` from that assertion.

**Verifier correction that changes the fix:** the reviewer's claim that a requested pass/fail is "usually" an implementation-readiness audit is **not established**. `:30`'s in-scope list leads with "decision quality", so "does this design hold up?" is squarely in scope; only "is this ready to build from?" routes away. A routing-only fix as drafted would misroute in-scope soundness questions.

---

## Refuted Findings

Fourteen findings were killed by their verifiers. Listed so the kills are auditable.

| # | Finding | Why it was refuted |
|---|---|---|
| 1 | `review-reviewer`'s explicit-only rule is conditional on a Codex-only metadata value | Misreads the AGENTS.md rule it cites ("name instruction files jointly" names two files, not `openai.yaml`). Five unconditional statements survive the hypothesised edit. Observed: the loader, not the text, enforces the gate. |
| 2 | The label-follows-findings cap discards `overreaching`/`underpowered` | "At most" is a ceiling, not an assignment; the skill uses "must be" elsewhere for mandates. Blind proxies: 2/2 chose `overreaching` under the cap; control with the clause deleted showed the identical spread. |
| 3 | Evidence Gate item 1 has no bounded-mode exit, so a bounded review can never issue a verdict | Misread. `unverified` *is* a status, and `:140` names exactly the categories claimed impossible. Traced on a 200-requirement spec: the gate passes. `:169`'s "in a full review" qualifier would be dead text otherwise. |
| 4 | `reduced-depth` caps findings at 4 while the reference targets 8–12 | Both are ceilings and compose by taking the tighter. "Targets" are never stated as a floor. The exemplar routes to a STOP before reaching the conflict. |
| 5 | Publish posture exists only as four CHANGELOG entries, three now false | Every concrete consequence is empirically false: the mirror names no reference file (grep exits 1), LICENSE postdates 0.8.0, the URLs resolve to byte-identical content. The "contradiction" dissolves once the dated release headers are read. |
| 6 | `scrutinize` grants explicit invocation a precedence step 2 revokes | Turns on reading "generic invocation" as "non-explicit". The pre-compression wording ("*That* generic invocation") is anaphoric to the explicit namespaced form; the family's word for non-explicit is "natural-language", used ten words later. |
| 7 | Claude-only `methodology-critique` is routed to with no availability hedge | The *route* is `methodology-check`, which is dual-runtime; `methodology-critique` appears only in a subordinate clause. `methodology-check` itself handles the runtime question explicitly: on Codex the recommendation is the deliverable. |
| 8 | `scrutinize`'s description gates on "explicitly asks", so plain readiness phrasing never loads it | Empirically false. "Is this handoff ready to build from?" routed to `scrutinize` 5/5; "review my plan before I build" 4/5. Treats a model-read description as a literal-string matcher. |
| 9 | `scrutinize-skill` mandates severity behavior but names no severity scale | It mandates no severity *field* at all — the siblings fence a ladder precisely because they do. The calculus is executable: both outputs (section placement, verdict enum) are defined. The proposed ladder collides with `:91`'s explicit refusal of a bar-keyed score. |
| 10 | `Bounded Review Scope` carries two opposite clearance contracts | It is not a section heading anywhere — it is an output label meaning the same thing in all four skills. The labels grade different objects. Skills load independently, so no agent holds both texts. |
| 11 | `Ship` is the only clearance verdict without a scope-and-expiry clause | The pattern is two of four siblings, not three. Two of `Ship`'s five clauses are already facts about the search. `implementation-review` is the one family member whose target is snapshot-identified by construction. (See confirmed finding 6 for the half that survived.) |
| 12 | `review-reviewer`'s severity scale cannot express its siblings' labels | The forced comparison never occurs: `challenged` lives in a packet that assigns no severity label to supplied claims. |
| 13 | README carries a sixth, uncanaried copy of the read-only CANON list | The canary's non-coverage of README is documented design. No agent ingests README as contract text. The list carries no exhaustiveness marker and its omissions are covered by surrounding prose. |
| 14 | `scrutinize`'s architecture handoff lacks a readiness carve-out, so readiness routes in a circle | The bullet's trigger is the requested *lens*, not the artifact type. Both entry points traced end to end: one handoff, terminating in both directions. |

---

## Decisions Only You Can Make

Six. Each is a design or boundary choice, not a mechanical repair.

**D1. How should `scrutinize` resolve its bounded ordinary verdict?** (finding 1)
1. *(my lean)* Mirror `implementation-review`: add `Partial review only` to the `:32` enum with its definition, plus a precedence line in the same paragraph — `Reject` and `Major revision` outrank it, which outranks `Minor revision` and `Defensible`. Also add the same precedence line to the readiness enum, which lacks one too.
2. Mirror `scrutinize-skill` instead: delete `:80`'s mandate, and let bounded ordinary scrutiny use the four existing tokens scoped to the slice, barring `Defensible`.
3. Leave it; accept a self-contradicting always-loaded contract that 8/8 live trials navigate correctly.

I lean 1 because it is the only option that closes the suppression path, and because it copies a solution already proven in the same plugin.

**D2. Which rule wins in `implementation-review`'s bounded mode?** (finding 2)
1. *(my lean)* Qualify `:159` the way `:169`'s third clause already is — an omitted requirement in bounded mode carries `unverified` status, not a `blocker` finding — then add a precedence carve-out naming what a bounded pass does with a genuine in-slice blocker. Requires updating `examples/review-findings.md:43-44`.
2. Keep `:159` and change `:193` to admit `Blocked` in bounded mode. Keeps the example valid; makes `Partial review only` rarer.

Either way the shipped example must move, because it currently teaches the losing rule.

**D3. Add a target-version field to `scrutinize`'s `Target And Evidence`?** (finding 4) This adds an obligation to a judgment skill, so it is an `agent-facing-design` call, not a typo fix. My lean: yes for the one-clause field (the datum already exists in `implementation-review`), and yes to extending `review-reviewer` step 5 to name the unpinned non-PR case.

**D4. Add a re-review rider to `implementation-review`?** (finding 5) The surviving hole is narrow — carried-forward `satisfied` rows with stale evidence pointers. My lean: yes, but scoped to that, and framed around the arc the skill never names (`Blocked` → fix → second pass). Do not add the `scrutinize-skill` half.

**D5. Put "pragmatic review" into `scrutinize`'s description?** (finding 9) My lean: yes, bound as "pragmatic or execution-readiness review" so the phrase inherits the intended sense rather than pulling in requests wanting proportionate feedback. Description is at 54 words against a 25–60 soft budget, so it fits.

**D6. How to close `system-design-review`'s "unless requested"?** (finding 12)
1. *(my lean)* Condition the routing: a requested *readiness or pass/fail* answer goes to `scrutinize`; a requested judgment on design soundness is answered here in the decision states the skill already defines.
2. Give the skill a fenced verdict enum with a scope clause, like its siblings.
3. Delete the two words, making the no-verdict rule absolute.

Option 1 preserves the no-verdict design and fixes the verifier's objection to the reviewer's blunter routing draft.

---

## Fix Batch

Five mechanical items, no judgment required. All are in the report; none were applied.

1. **`README.md:38`** — lead the `review-reviewer` Trigger cell with the invocation requirement: "Explicit `/review-reviewer` or `$review-reviewer` only — supplied review, critique, audit, reviewer output, or pasted claims". Leave `:29` alone.
2. **`PRIVACY.md` and `TERMS.md`** — de-Codex exactly four mentions (`PRIVACY` paras 2, 3, 4; `TERMS` para 2), using `plugins/git-cycle/PRIVACY.md` as the wording model. Leave `PRIVACY` para 1 and `TERMS` para 1 untouched — they are accurate, because only Codex has a versioned install cache.
3. **`skills/scrutinize/references/review-format.md`** — shorten the three template headings to match `SKILL.md:80`'s declared section names, moving any extra scope to a bracketed line under the heading.
4. **`skills/scrutinize-skill/agents/openai.yaml:4`** — add the `$` token; likewise `README:78` and `README:50`. Do **not** touch `plugin.json`'s starter list.
5. **Stray `.DS_Store` files** — four exist in the source tree (plugin root, `skills/`, `skills/scrutinize/`, `skills/system-design-review/`) and have been copied into the Codex install cache. Remove with `trash`. *(Phase 0 observation, not a reviewed finding.)*
   **Do this one last, and know its consequence.** These files are gitignored and untracked (`git ls-files | grep -c DS_Store` returns 0), so removing them is a local filesystem cleanup with nothing to commit. But `codex plugin add` copied them into the cache, and source and cache are currently byte-identical — so deleting them from source makes `codex-plugins-sync.sh --check` report DRIFT until the next republish. If items 1–4 are landing with a version bump and republish anyway, sequence this before that republish and the drift closes itself. If not, expect `--check` to be non-zero and know why.

### Executing this batch

Every file in items 1–4 lives under `plugins/review-family/`, which `scripts/skill-route-guard.py` guards (`SKILL_SURFACE_RE` matches `^plugins/[^/]+/.+` — the whole plugin, README and legal files included, not just `skills/`). Edit/Write on those paths is denied in the primary checkout and in any parked satellite. **The batch must run through `git-cycle:worktree-task-cycle`** — inspect → lease-acquire → activate → edit in the satellite → validate → record-validation → land → park.

All five review-family satellites exist under `~/.agents-worktrees/` (`scrutinize`, `scrutinize-skill`, `system-design-review`, `review-reviewer`, `implementation-review`) and are currently parked at detached HEAD. Items 1, 2, and 4-partial touch plugin-root files (`README.md`, `PRIVACY.md`, `TERMS.md`) that map to no single skill identity, so the guard's generic rule applies: work them in any satellite activated for the task.

Items 1–4 are documentation and metadata only and change no skill behavior. Whether they need a version bump is a release call: they touch shipped plugin files, so under the repo's lockstep rule they do — and per AGENTS.md a landed bump goes live on both runtimes without further consent, so land it only when local liveness is intended, then complete it promptly with `codex-plugins-sync.sh --publish review-family`. Mirror sync and push stay ask-gated.

---

## Evidence Boundary

- No skill was invoked end to end as itself. Three verifiers ran targeted live probes (`claude -p` forward tests for findings 1 and 9, a blind proxy differential for refutation 2, a loader harness for refutation 8); everything else labelled *argued* rests on reading and tracing the text.
- The first pass capped verification at 16 findings; that cap was lifted and the run resumed, so all 28 deduplicated findings were verified. Nothing was silently dropped.
- Keep-or-prune merit for these five skills is out of scope here — that is charter and usage-ledger territory, not a gap question.
