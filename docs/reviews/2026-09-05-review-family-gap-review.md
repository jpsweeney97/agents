<!-- Durable copy of the gap-review report produced 2026-09-05 in a temporary run directory (scratchpad gap-review-review-family.C34u; reviewer/verifier JSON, finding files, and 41 headless-trial transcripts lived there). Fixes were applied in review-family 0.18.0; see CHANGELOG.md. -->

# Gap Review — `review-family` plugin (0.17.0)

- Target: `/Users/jp/.agents/plugins/review-family` — dual-runtime plugin, five skills (`implementation-review`, `review-reviewer`, `scrutinize`, `scrutinize-skill`, `system-design-review`).
- Source revision: repo HEAD `ec626b19476e6df04d15cb40f6f35d4c08919931` (clean, `main...origin/main`); plugin last touched `35ffba1 2026-09-01 chore(review-family): cut 0.17.0`.
- Run: 2026-09-05. Coordinator: this session (Claude Fable 5.1). Agents: 4 reviewers + 23 verifiers, all fresh-context Opus subagents (user request "using Opus agents"). Headless proxy trials inside verifiers ran `claude -p --model sonnet`.
- Boundary: report only. Nothing under `/Users/jp/.agents`, `~/.claude/skills`, or `~/.codex` was edited; the tree is clean at the same HEAD after the run.
- Working files: this directory (`scope.md`, `review-0N.json`, `finding-NN.json`, `verify-NN.json`, `repro-NN/`, `verdicts-so-far.md`). Temporary; durable saving is a separate request.
- Completion: complete. 4 reviewer results and 23 verifier results all parsed and validated; every candidate has a verdict.

## Chat summary

~~~text
Target: plugins/review-family — dual-runtime plugin, 5 skills, 0.17.0
Completion: complete — 4 reviewers, 23 verifiers, every candidate adjudicated
Checked, nothing found: all 19 target surfaces read in full by ≥1 reviewer (17 by ≥3); structural validation, canary, YAML/JSON parse, referenced paths, Claude symlink, Codex cache, mirror, marketplace, routed-skill existence all pass
Findings: confirmed 7 (high 1, medium 3, low 3), 6 of them reproduced; refuted 16; unverified 0
Fix batch: 7 items (details in §5)
Decisions needed: D1 scrutinize-skill bounded verdict repair shape; D2 review-reviewer label co-occurrence rule; D3 self-authorship disclosure scope; D4 lens-parity assertion in the repo canary; D5 which refutation residues ride along; D6 release shape
How to apply (on approval): apply-findings through the repository's working-branch or worktree procedure; plugin changes follow its release and publication rules
Report: /private/tmp/claude-501/-Users-jp--agents/e5d9b1ed-4196-48f4-b42c-55db04ef27c6/scratchpad/gap-review-review-family.C34u/report.md (temporary; durable saving is a separate request)
~~~

## 1. Checked with nothing found

Bounded coverage: these checks ran and these files were read in full by at least one reviewer without a surviving finding. This is not a claim that the whole target is correct.

Mechanical checks (Phase 0, all passing; commands and outputs in `scope.md`):

- `quick_validate.py` on all five skills (review-reviewer's `disable-model-invocation` complaint is the accepted class per AGENTS.md Validation Ladder item 6).
- Ruby YAML parse of all five `agents/openai.yaml`; JSON parse of `plugin.json` (0.17.0, `skills: ./skills/`); `git diff --check` clean.
- `scripts/check-review-family.sh` exit 0 (read-only core ×5, bounded core ×3, expiry gloss ×2, 10 template headings); wired as SessionStart hook in `.claude/settings.json:92` and `.codex/hooks.json:32`.
- Description word counts 44/48/57/53/44 (within the 25–60 soft budget).
- Every in-bundle referenced path exists. Every external skill the plugin routes to exists in the live library; none of the four skills archived on 2026-09-05 is named anywhere in the plugin.
- Delivery: Claude symlink correct and `claude-skills-sync.sh --check` exit 0; marketplace entry relative-pathed and AVAILABLE; `codex plugin list` shows review-family@turbo-mode installed, enabled 0.17.0; Codex cache `0.17.0` and the GitHub mirror checkout are byte-identical to source; CHANGELOG top = plugin.json = cache = mirror.

Files read in full by reviewers (count of the four reviewers who read each):

| File | Read by | Surviving confirmed finding? |
|---|---|---|
| `.claude-plugin/plugin.json` | 3 | none |
| `CHANGELOG.md` | 2 | none |
| `PRIVACY.md`, `TERMS.md` | 3 | none |
| `README.md` | 4 | none (F12, F23 refuted) |
| `implementation-review/SKILL.md` | 4 | F09 (high), F01 (medium); F14, F15, F19 refuted |
| `implementation-review/agents/openai.yaml` | 4 | none |
| `implementation-review/examples/review-findings.md` | 3 | none (F05 refuted) |
| `implementation-review/references/review-lenses.md` | 3 | none (F01 is a defect of the index, not the reference) |
| `review-reviewer/SKILL.md` | 4 | F18 |
| `review-reviewer/agents/openai.yaml` | 4 | none |
| `scrutinize/SKILL.md` | 4 | F17; F07 (disclosure) |
| `scrutinize/agents/openai.yaml` | 4 | none |
| `scrutinize/references/review-format.md` | 3 | F10 |
| `scrutinize-skill/SKILL.md` | 4 | F02; F07 (disclosure) |
| `scrutinize-skill/agents/openai.yaml` | 4 | none |
| `system-design-review/SKILL.md` | 4 | none (F06, F20 refuted; F07 names it only for the review snapshot) |
| `system-design-review/agents/openai.yaml` | 4 | none |
| `system-design-review/references/system-design-dimensions.md` | 3 | none |
| `LICENSE` | coordinator, head only | not reviewed |

Also read: `AGENTS.md` (2 reviewers), `plugins/marketplace.json` (1), `scripts/check-review-family.sh` (1).

Dimensions run: cross-file consistency and reference reachability; lifecycle omissions; reachable behavioral edge cases in the contract algorithms; routing and delivery (dual-runtime). 28 raw findings → 23 deduplicated candidates → 23 fresh verifiers.

## 2. Confirmed findings

Each is labeled **reproduced** (a headless execution demonstrated the claimed consequence) or **confirmed by reasoning** (source text establishes it; consequence not observed). Severity is the verifier-adjusted grade. Verifier corrections to the reviewer's mechanism are carried inline; the fix items in §5 already incorporate them. Findings that share a root cause are grouped.

### Root cause A — bounded-mode discipline was not carried uniformly across the three bounded-mode skills

**F09 — a caller-narrowed scope lets `implementation-review` return `Ship` on requirements the change implements but nobody inspected.** **High** (reviewer claim: medium; raised by the verifier). Reproduced (3 trials; the third is the decisive one). Bounded Review Mode's only trigger is size (`implementation-review/SKILL.md:140`), so a request like "review only the auth files against this plan" never enters it and its guard at `:144` is never read. The `not-applicable` definition at `:88` ("the requirement is real but outside the declared scope") combined with scope authority 1 (`:34`, the caller's boundary *is* the declared scope) licenses marking every excluded requirement `not-applicable`; `Ship` (`:172`) is barred only by `violated` or `unverified`. All three trials chose `not-applicable` citing the caller's boundary and explicitly declined bounded mode. Trial 3: a six-file PR whose three billing files implement plan requirements R4–R6 (a refund cap, a webhook signature check), with the user restricting the pass to the auth files — the reviewer marked R4–R6 `not-applicable` ("Implemented in `src/billing/invoice.py`, excluded from this pass by your explicit request"), omitted the billing files from the changed-area ledger, and closed with `Ship`. `scrutinize/SKILL.md:73` already carries the rule that closes this ("A review whose scope was narrowed externally … is also a bounded review: state the subset, scope the verdict to it, and leave full-clearance tokens unissued"). Verifier corrections: the text is not an even fork, it leans to the unsafe reading; the defect lives only where the change *does* implement the excluded requirements (the reviewer's own fixture wording described the benign case, where a scoped `Ship` is honest); "the family has already decided" overstates it — `scrutinize-skill:101` also lacks the rider, which entered as a scrutinize-only repair (commit 3d6594d, 2026-07-03) that touched no sibling. Mitigation: all three trials disclosed the boundary in prose, so the harm needs the `Ship` token to travel without the prose — the panel-seat and aggregated-verdict shapes.

**F02 — `scrutinize-skill` has no legal verdict for a clean bounded pass.** Medium (reviewer claims: high, medium). Reproduced (2/2 trials). `scrutinize-skill/SKILL.md:72` fixes four tokens (`Reject`, `Major revision`, `Minor revision`, `Defensible`); `:101` forbids `Defensible` in bounded mode with no replacement. It is the only one of the three skills named in the canary's `BOUNDED_TARGETS` with no bounded-verdict token; 0.12.0 gave `scrutinize` the token and precedence for exactly this hole and touched `scrutinize-skill` only for the expiry gloss. Two headless trials with a clean bounded slice both emitted `Defensible` with a scoping gloss, the token `:101` forbids. Verifier corrections: bounded mode is reachable for large bundles but not routine (`:53` prescribes a bounded-avoiding overlap procedure); the reviewer's "suppression path" claim runs backwards — with no `Partial review only` label there is nothing to hide behind, and adding the token alone would *introduce* that path, so the fix is safe only paired with the precedence order; the trials self-mitigated with a scoping gloss, which is why severity is medium not high.

**F17 — `scrutinize`'s readiness precedence scopes one above-Partial token and not the other.** Low (reviewer claim: medium). Confirmed by reasoning; two trials never reached the `Patch Before Implementation` branch. `scrutinize/SKILL.md:49` says "a disqualifying blocker found in a bounded pass renders `Not Executable Yet`, scoped to the reviewed subset" and says nothing for `Patch Before Implementation`, while both sibling bounded lines (`scrutinize:80`, `implementation-review:201`) name every above-Partial token. Verifier corrections: the ordering itself is correct and must not change (a single mid-tier token spanning major and minor cannot sit below `Partial Review Only` without reopening the 0.12.0 suppression path); `Partial Review Only` is not unreachable — it is the token for a clean bounded slice; the incompleteness survives in the mandatory `Bounded Review Scope` section, so only the verdict token can lose it. The reviewer's proposed fix (extend the clause, keep the order) is the right repair; the title and sibling-inconsistency argument are not.

### Root cause B — the 0.17.0 release added lenses to the reference without updating the always-loaded index

**F01 — `implementation-review`'s step-3 lens index omits two lenses the reference defines.** Medium (reviewer claims: medium, medium). Reproduced (single-variable differential, 2 trials). `SKILL.md:98–106` lists 9 lenses and presents itself as "the lenses and their trigger surfaces"; `references/review-lenses.md` defines 11 (adds Retry-safety/idempotency at `:12`, Orphaned code at `:15`); `SKILL.md:115` names "the orphaned-code lens" which the always-loaded body never lists. CHANGELOG 0.17.0 shows the release edited `:115` without touching the index; CHANGELOG 0.9.1 records the one-line-per-lens index invariant. Trial with SKILL.md alone: the agent's lens census was exactly the nine indexed lenses on a diff built on both missing surfaces (a retried per-call key and a stranded legacy route), and it read the reference load as conditional on a lens firing. Same prompt with the reference pasted in: both missing lenses fired. Verifier corrections: `:115` does not literally say "above" for the orphan lens, so "names it as if indexed" overstates — the defect is that the body invokes a lens it never lists; the fixture does not automatically trigger none of the nine (trial 1 found two), so the full silent-skip path is reachable but model-dependent and was not executed. The canary does not assert index/reference parity.

### Root cause C — `review-reviewer`'s Review Judgment labels have no co-occurrence rule

**F18 — two of the five labels can both fit with nothing selecting between them.** Medium (reviewer claim: medium). Reproduced (2 trials, byte-identical input, two different headline labels). `review-reviewer/SKILL.md:161` mandates exactly one label and `:169` says "the label follows the findings", but on a review that inflates severity on three claims and misses a confirmed blocker, trial 1 returned `partially reliable` (reading the "at most" cap as selecting that label) and trial 2 returned `underpowered` (reading the cap as only excluding `reliable`). Verifier corrections: the reviewer's second input (`under-evidenced` vs the cap) is a misread — they are jointly satisfiable; the "every other enum has a precedence order" claim is false (three do; `scrutinize-skill` has none); and the reviewer's proposed precedence order should be **rejected** — these five labels mix two quality grades with three failure-kind diagnoses that carry no severity relation, so ranking `overreaching` above `underpowered` would mechanically label a review that missed a security blocker `overreaching`. The repair that fits the judgment bar defines co-occurrence without ranking (see D2).

### Root cause D — self-authorship disclosure exists in one skill only

**F07 — reviewing your own work is uncovered outside `review-reviewer`.** Low (reviewer claim: medium). Reproduced for the disclosure half (2 trials); the leniency half refuted. The rule lives only at `review-reviewer/SKILL.md:74` with a plan-scoped half at `implementation-review/SKILL.md:238`. With authorship buried in a realistic session history, a `scrutinize-skill` self-review disclosed it nowhere; with authorship made salient it disclosed spontaneously. Both trials nonetheless returned `Major revision` with two Critical Failures against their own artifact — no leniency, no `Defensible`. Verifier corrections: the causal claim ("therefore renders `Defensible`") is contradicted; `system-design-review` renders no clearance verdict so does not belong in the verdict claim (its exposure is the review snapshot only); the fix's re-derivation clause duplicates `scrutinize-skill:40/:66/:95` and `scrutinize` step 1. The minimal repair is a disclosure sentence plus declared extra skepticism on absence claims, and widening `implementation-review:238` to cover the implementation.

### Root cause E — an always-applicable output rule is homed only in a conditionally-loaded reference

**F10 — the only shorter-answer rule sits behind a load trigger a short answer never fires.** Low (reviewer claim: medium). Reproduced (single-variable differential, 1 trial per arm). `review-format.md:61` ("keep the same section order and compress the content rather than dropping sections") is the bundle's only output-length rule; `scrutinize/SKILL.md:84` gates the reference on complex targets and full structured reviews. Without the sentence, a "keep it short" scrutiny dropped `Patterns And Root Causes` and hoisted `Verdict` to the top; with it, all nine sections appeared in order. Verifier corrections: the claimed loss of `Premise Check` / `Hidden Dependencies` did not happen — both are backed by always-loaded workflow steps and survived; "complex target, keep it brief" does fire the load trigger, so the unread state is confined to simple targets; AGENTS.md's placement rule is satisfied on its face. Worth doing as a small completeness improvement.

## 3. Refuted findings

Each refuted by a fresh verifier; reason abbreviated (full text in `verify-NN.json`).

- **F03** review-reviewer Boundaries vs Routing on the namespaced form — the Boundaries line's second sentence scopes the rule to the implicit route, not token spelling; Routing:22 rules the namespaced form in; the two are additive. Under the finding's reading the skill would be unreachable on Claude (no `commands/` directory, model invocation disabled). 2/2 trials saw no conflict.
- **F04** explicit-only gate cites a Codex-only field — six surfaces state explicit-only unconditionally and agree; AGENTS.md:30 governs tokens, instruction-file names, and single-runtime routing, not enforcement metadata; the pairing rule is deliberately single-sourced in `agent-facing-design:78` and belongs outside fire-time bodies. 2/2 trials: agents were not misled and named the Claude gate unprompted.
- **F05** example Verdict blocks omit fields — the examples file is an excerpt collection by construction (every block omits most of the eight sections); the "extra" lines are mandated by `SKILL.md:140` and `:197`; the with-examples proxy arm emitted all five Verdict fields.
- **F06** two evidence-absence tokens — they label different fields in different sections; the reference defining `not enough evidence` loads at step 4, after the step-3 stop-rule count; nothing parses either token. 2/2 trials kept the vocabularies separate.
- **F08** no re-review discipline in scrutinize-skill — re-proposes a fix the 2026-08-26 gap review's decision D4 declined and CHANGELOG 0.15.0 landed as a scoping decision; the skill has no cross-pass artifact for the implementation-review analogy to transfer to; system-design-review re-screens every run. 2/2 trials produced every behavior the sentence would add, without it (caveat: `claude -p` loads the user-level CLAUDE.md, whose no-unverified-claims rule one trial cited).
- **F11** no apply-findings lane — the claimed improvised fix pass did not reproduce (2/2 trials routed to apply-findings on its description alone); the omission is booked as a known open edge in `docs/agents/skill-lifecycle-notes.md:15` with a stated release-shaped reason; the analogy to the five volunteered-judgment pointers does not hold since the user has already named the action.
- **F12** README:5 divergence claim — the sentence has a compound subject and the "runtime artifacts … runtime-proof lane" half is true of Claude (a running session's loaded skill is stale until restart); the claimed harm inverts the sentence's force; 0.11.1's direction supports the current neutral wording.
- **F13** methodology-critique route unconditioned — the route target is `methodology-check` (dual-runtime); methodology-critique appears only in a relative clause describing what methodology-check escalates to, which is true on Codex by recommendation; "where available" at `:99` hedges tokens, not runtime availability; the genuine version of this defect was fixed in 0.8.0.
- **F14** working-tree anchor — the Re-Review rule re-earns every carried row regardless, so no pass needs to know which rows moved; the content record lives in the mandated ledgers; the sibling records dirty state as a flag, not a hash. 1 trial: HEAD unchanged, uncommitted rewrite, reviewer flipped two rows to `violated` correctly.
- **F15** Evidence Gate cannot pass in bounded mode — gate item 1 says "accounted for", which an `unverified` Changed-Area row satisfies; `examples/review-findings.md:40` already writes a falsification cell as "none this pass" under `Partial review only`; line 219 assigns bounded verdicts to "the bounded-mode discipline". 2/2 trials walked the gate item by item, marked every item PASS, and issued `Partial review only` (omission-only) or `Blocked` scoped to the slice (in-slice violation). Residue: the gate states the subset scoping nowhere in `SKILL.md` itself.
- **F16** Current Claim Check bucket orphans — `verify-first` is by definition the `Unverified` state (`:63`, `:111`, routed that way at `:45` and `:75`); `note` with `act`/`narrow` is self-contradictory (`:119` vs `:107`); enumeration shows every coherent combination lands in a bucket. 2/2 trials built to induce orphans produced none. The proposed fix would defeat severity triage.
- **F19** undefined "zero-findings gate" — lowercase prose naming is the file's convention (`:55`, `:169`); the referent is forced (two gates, the second's trigger contains "zero-findings"); the block self-triggers on `Ship`. 2/2 trials resolved it instantly and kept the obligation.
- **F20** reduced-depth cap vs finding targets — the reference itself separates targets from hard caps; a cap composes with caps and the stricter binds; `SKILL.md:56` authorizes zero findings so no floor pressure exists. 2/2 trials: depth label chosen first, count followed.
- **F21** scrutinize skill-bundle guardrail — the wins-clause idiom is identical in siblings (family wins, bullets pick the member); "generic" is glossed at `:23` and in `scrutinize-skill:12`; the guardrail has a live branch under step 2's own exception. 2/2 trials handed the skill target off; deleting `:70` would strip discipline from the branch step 2 opens.
- **F22** sibling redirects to review-reviewer — the trailing "Otherwise-wrong lane … if invocation rules bar switching, ask one routing question" is the compressed survivor (d61afc2) of a bullet that governed every redirect, review-reviewer's included; the 0.11.1 review considered and left the redirects unmarked. Trials showed the agent absorbing the pasted review inline, which review-reviewer's own `:25` permits.
- **F23** README baseline cells — "PR" and "known intended behavior" are legitimate spec sources per `SKILL.md:24` ("PR description", "user-provided text"); only the word "diff" in README:27 sits on the wrong side, and README:50 corrects it in place.

## 4. Unchecked or unfinished

None of the items below prevents completion of the requested scope; they bound what the results prove.

- No Codex-side proxy trial ran; every headless trial used `claude -p --model sonnet` (the verifiers' reproduction model, not Opus). Codex behavior on the confirmed findings is inferred from shared text, not observed.
- `claude -p` loads the user-level `~/.claude/CLAUDE.md`, so trials demonstrate the real Claude deployment environment rather than skill text in isolation (noted by verifier 8; one trial cited that file's no-unverified-claims rule).
- `--allowed-tools ""` did not fully bar filesystem reads in at least one trial (verifier 4 saw a subprocess quote `agents/openai.yaml` content not in its prompt). No writes occurred; the repo was verified clean after each such trial.
- Reproductions were capped at two trials (verifier 9 ran three, to isolate the change-implements-it case): demonstrations, not rates.
- Codex Desktop (ChatGPT app) plugin inventory and Codex-side SessionStart hook execution were not observed.
- `LICENSE` was read by head only (MIT boilerplate).
- The prior gap review (`docs/reviews/2026-08-26-review-family-gap-review.md`) was not fed to any agent; verifiers 8, 11, 14, and 22 consulted it or `docs/agents/skill-lifecycle-notes.md` on their own as cited dependencies.

## 5. Fix batch (mechanical, on approval)

All items edit plugin-distributed sources, so they follow the Plugin Layout publish path: version bump in lockstep, CHANGELOG entries, Codex republish, mirror sync ask-gated. Per the repo's hooks, skill-surface edits are blocked in the primary checkout and route through the `review-family` worktree-task-cycle satellite. Items are written with the verifier corrections already applied.

1. **F01 — `implementation-review/SKILL.md` step 3.** Add two index bullets in the reference's order: after `Concurrency`, "`Retry-safety and idempotency`: the change adds or alters a state-changing endpoint or a side effect behind a retry."; after `Supply-chain provenance`, "`Orphaned code`: the change replaces or removes a code path." (Optional guard, see D4.)
2. **F02 — `scrutinize-skill/SKILL.md:72` and `:101`.** Subject to D1. Recommended form: extend step 7 to "Use exactly one of `Reject`, `Major revision`, `Partial review only`, `Minor revision`, or `Defensible`; `Partial review only` means bounded review mode was used — the reviewed subset was judged, the full target was not. If more than one could apply, choose the first matching in this order: `Reject`, `Major revision`, `Partial review only`, `Minor revision`, `Defensible` — a disqualifying in-slice finding renders its own verdict, scoped to the slice, and is never hidden behind an incomplete-pass label." Align the `:101` parenthetical to "(do not use `Defensible`; use `Partial review only` unless a disqualifying in-slice finding renders `Reject` or `Major revision`)".
3. **F17 — `scrutinize/SKILL.md:49`.** Keep the order; extend the scoping clause: "— a disqualifying blocker found in a bounded pass renders `Not Executable Yet`, and a patchable in-slice gap renders `Patch Before Implementation`, each scoped to the reviewed subset with the uninspected readiness surface named."
4. **F18 — `review-reviewer/SKILL.md:169`.** Subject to D2. Recommended form: append "When two failure-kind labels (`overreaching`, `underpowered`) both fit, the label is `partially reliable` and the rationale names both kinds. 'At most `partially reliable`' excludes only `reliable`: a failure-kind label that fits still applies." Do not add a ranked precedence order.
5. **F07 — Guardrails of `scrutinize` and `scrutinize-skill`; `implementation-review:238`.** Subject to D3. Recommended form: one sentence in each Guardrails list — "If you authored the target, disclose it in `Target And Evidence` / `Target And Surface` and treat your own absence claims (`None found`, no material overlap, a clearance verdict) with declared extra skepticism." Widen `implementation-review:238` from "wrote the original plan" to "wrote the plan or the implementation". Leave `system-design-review` unchanged unless JP wants the snapshot line covered.
6. **F10 — `scrutinize/SKILL.md` Output section (`:80`).** Add the sentence "If the user asks for a shorter answer, keep the same section order and compress the content rather than dropping sections." next to the default-section list; keep or drop the copy at `review-format.md:61`.
7. **F09 — `implementation-review/SKILL.md` Bounded Review Mode (`:140`) and the `not-applicable` definition (`:70`, `:88`).** Two edits, both load-bearing. (a) Import `scrutinize:73`'s rider into Bounded Review Mode: "A review whose scope was narrowed externally — a caller-restricted file set, an assigned lens or panel seat, or sampled coverage — is also a bounded review: state the subset, scope the verdict to it, and leave `Ship` unissued." (b) Disambiguate the status: at `:70` and `:88`, "`not-applicable`: the requirement is real but the change under review does not reach it. A requirement the change implements or touches in files outside a caller-narrowed slice is `unverified`, not `not-applicable`." Verifier note: the repair must key on whether the change reaches the requirement, not only on whether the caller narrowed the scope. Consider the same rider for `scrutinize-skill:101` (D5).

Release class: minor (F09, F02, and F18 change verdict contracts, matching the 0.12.0–0.16.0 precedent), so `0.18.0`; F01, F10, F17, F07 ride as the same entry's smaller items. F09 should lead the CHANGELOG entry. Forward-test after landing per the plugin's own precedent (two fresh `claude -p` trials per changed behavior).

## 6. Decisions for JP

Each has options and a recommendation. Mechanical items above proceed on approval without further decision.

**D1 — How to close `scrutinize-skill`'s bounded-verdict hole (F02).**
1. Add `Partial review only` plus the precedence order, mirroring `scrutinize` (recommended — it is the family's already-tested shape, and the verifier showed the token is safe only with the order).
2. Keep the four-token enum and instead rewrite `:101` to permit `Defensible` with a mandatory scoping gloss (matches what both trials did; but it contradicts the family doctrine that bounded passes never issue clearance tokens).
3. Leave as is and record the asymmetry in `skill-lifecycle-notes.md` (the hole is real and the canary lists this skill as a bounded-mode skill; not recommended).

**D2 — How to make `review-reviewer`'s Review Judgment deterministic (F18).**
1. Define co-occurrence: two failure-kind labels → `partially reliable` with both named in the rationale; state that "at most `partially reliable`" only excludes `reliable` (recommended — fixes the indeterminacy without ranking diagnoses that have no severity relation).
2. The reviewer's precedence order `under-evidenced` > `overreaching` > `underpowered` > `partially reliable` > `reliable` (rejected by the verifier: it would label a review that missed a security blocker `overreaching`).
3. Clarify only the "at most" cap and leave label choice to judgment (removes the trial-1/trial-2 split on the cap but not the `overreaching`/`underpowered` tie).

**D3 — Scope of the self-authorship disclosure (F07).**
1. Minimal: disclosure sentence plus declared extra skepticism on absence claims in `scrutinize` and `scrutinize-skill`; widen `implementation-review:238` (recommended — the observed consequence was only the missing disclosure line).
2. The reviewer's full three-part clause in all three skills including `system-design-review` (duplicates existing target-first obligations; sdr has no clearance verdict).
3. Do nothing (low severity; but two trials showed the disclosure is omitted whenever authorship is not freshly salient).

**D4 — Add an index/reference lens-parity assertion to `scripts/check-review-family.sh` (F01 class guard).** The canary is an always-loaded SessionStart hook in both runtimes, so extending its assertion set is a change to an ambient contract. Options: (1) add the assertion in the same change, recorded as maintenance of the existing canary (recommended if JP reads it as maintenance rather than a new contract — it would have caught 0.17.0's omission); (2) do not extend the canary; rely on the fix alone. If (1), consult `docs/agents/charter.md` first per the always-loaded-contract rule.

**D5 — Which refutation residues ride along in the same release.** None is a finding; each is a one-word or one-clause polish the verifiers noted while refuting:
- `README.md:27` — delete the word "diff" from the "against" list (F23 residue). Recommended: yes, zero risk.
- `implementation-review/SKILL.md:16` and `system-design-review/SKILL.md:16` — d61afc2 dropped the word "explicit" from these two review-reviewer redirect lines, the only gate marker they carried (F22 residue). Recommended: yes, restore "explicit".
- `review-reviewer` frontmatter `:3` and `README.md:38` — add the namespaced `review-family:review-reviewer` form that Routing:22 already accepts (F03 residue). Recommended: no unless touching those lines anyway; the description does no model routing under `disable-model-invocation`.
- `review-reviewer/SKILL.md:13` — the trailing clause names only the Codex enforcement key and would go stale if that key were removed (F04 residue). Recommended: no; the pairing rule is single-sourced in `agent-facing-design:78`.
- `docs/reviews/2026-08-26-review-family-gap-review.md` refutation 11 overstates "snapshot-identified by construction" for scope authority 5 (F14 residue). Recommended: no edit to a settled record; note only.
- `docs/agents/skill-lifecycle-notes.md:15` still books the apply-findings pointer as a deferred own-release item (F11 residue). Recommended: leave as booked.
- `implementation-review/SKILL.md` Evidence Gate — states the bounded-mode subset scoping nowhere in its own words, leaning on the conditionally-loaded examples file (F15 residue). Recommended: optional one-clause note ("in bounded mode, read each item as scoped to the reviewed subset"); harmless, not a defect repair.
- `scrutinize-skill/SKILL.md:101` — also lacks the externally-narrowed-scope rider that `scrutinize:73` carries and that fix item 7 adds to `implementation-review` (F09 correction). Recommended: yes, add the same sentence so all three bounded-mode skills agree; it costs one sentence and the F09 verifier traced the omission to a scrutinize-only repair, not a decision.

**D6 — Release shape.** (1) One `0.18.0` carrying every approved item (recommended — one CHANGELOG entry per finding, one republish, one mirror decision); (2) split the two verdict-contract changes (F02, F18) from the rest; (3) hold everything for the next natural bump.

## 7. Method notes and limits

- Every reviewer result and every verifier result was parsed with `validate.py` (required keys, types, allowed values, the refuted→`n/a`/`reproduced=false` rule) before use; all 27 passed first time.
- Deduplication grouped 28 raw findings into 23 candidates by defect and evidence (`dedup.py`), keeping every source dimension and severity claim; three groups had two or three reporters (F01, F02, F04, F13).
- Verifiers refuted 16 of 23 candidates and confirmed 7; they raised one severity (F09 medium→high) and lowered four (F02 high→medium, F07 medium→low, F10 medium→low, F17 medium→low). Four refutations rested partly on decisions recorded in the prior gap review or the lifecycle notes, which the verifiers located as cited dependencies — those documents were not supplied to them.
- Verifier corrections rejected three reviewer-proposed fixes outright (F18's precedence order, F16's severity-filter removal, F21's guardrail deletion) and narrowed four more (F02 pairing, F07 minimal form, F17 keep-the-order, F09 key-on-reach). The fix batch above uses the corrected forms.
- 41 headless proxy trials ran inside verifiers (all `claude -p --model sonnet`), each from a copy of the skill text in the verifier's own `repro-NN/` directory; the reviewed source was never touched.
- Keep/prune merit was not assessed; the usage-ledger figures in `scope.md` are context only.

## 8. Application record (added on apply, 2026-09-05)

- Applied as review-family 0.18.0 in the `scrutinize` satellite with every recommended option: D1 opt 1, D2 opt 1, D3 opt 1, D4 canary extension, D5 "yes" residues only (README "diff", "explicit" ×2, scrutinize-skill rider), D6 one release. The 16 refuted findings and the D5 "no" residues were not applied.
- Forward tests: a 14-agent workflow ran one verify-applied agent and one forward-test agent per confirmed finding (two fresh `claude -p --model sonnet` trials each on the verifier's own fixture with the new text). 7/7 verify pass, 7/7 forward pass, 14/14 trials showed the expected behavior; the old defect recurred in none.
- Wording pass after the verify-applied agents, inside the findings: implementation-review's rider anchors on "a file set narrower than the change" and `:61`/`:240` name the caller-narrowed pass as a bounded-mode trigger; `:70`/`:88` say "the whole change, not only the reviewed slice"; scrutinize-skill `:42` now runs a request narrowed to one file as a bounded review of the skill so it agrees with the `:101` rider, and `:101` says "Workflow step 7"; review-reviewer `:169` names `overreaching`/`underpowered` and both `under-evidenced` triggers; scrutinize's shorter-answer sentence says "keep the section order". Three re-run trials (F09 ×2, F18 ×1) held: the decisive F09 fixture still renders `Partial review only` with no `Ship`, and the benign F09 fixture (change = the three auth files) keeps `not-applicable` and a scoped `Ship`, which the first applied text had withheld.
- Not applied from the wording notes: F17's naming location, F07's placement, F09's two-place statement, and the rider's three-obligation summary (inherited from scrutinize:74).
