# Conciseness Audit — SKILL.md Body Length Patterns

Date: 2026-07-13. Read-only diagnosis of what makes SKILL.md bodies long across the live inventory. No edits were made and no per-skill fix list is offered; harm judgments are left to the human.

## Scope and inventory shape

All 89 live SKILL.md bodies: `skills/` (65), `skills-claude/` (6), `plugins/*/skills/` (18). `skills-archive/` excluded. Body prose only; frontmatter treated as routing context.

Measured inventory: 105,919 total body words; median 1,083; p90 1,944; max 3,368 (`plugins/review-family/skills/implementation-review/SKILL.md`); min 161 (`skills/grill-me/SKILL.md`). Only 16 of 89 skills have a `references/` or `examples/` directory. Length is inventory-wide: the census below found a median of 10 distinct patterns per file, and no file — including the 161-word `grill-me` — had zero.

## Method

Two-pass multi-agent audit, all read-only:

1. **Discovery**: 12 parallel readers, each reading ~7–8 full bodies (all 89 covered), reported candidate patterns with verbatim evidence and root-cause guesses. Their reports converged strongly and independently — every reader surfaced some form of the neighbor-fence, per-rule-rationale, restatement, and inoculation families.
2. **Census**: candidates consolidated into a fixed 17-pattern taxonomy with per-file thresholds; 12 parallel classifiers re-read all 89 files against it. Every hit carries a verbatim quote and an impact band (minor <10%, moderate 10–25%, major >25% of body words — classifier judgment, not measurement). A random sample of 40 census quotes was mechanically verified against the source files: 40/40 verbatim.
3. Supporting evidence: mechanical greps for convergent boilerplate sentences, and 10 files read directly by the auditing session (the three longest, the shortest, and a spread of median-size trust and judgment skills across all three directories).

Frequency figures below are counts of files (out of 89) meeting the pattern's detection threshold in the census. "Top driver" counts how many files' classifiers named the pattern one of that file's 1–2 largest word consumers.

## Headline

**The length is obligation density, not flab.** All 12 discovery readers independently checked for and failed to find padding: sentences are clause-dense, nearly every clause binds a decision, and the few genuinely offloadable payloads are concentrated in ~10 files. What makes bodies long is the *number* of things each body chooses to do — defend its routing borders, justify each rule, restate its invariants at every landing point, preempt predicted agent misbehavior, and re-carry library-wide doctrine locally. Five root causes (final section) generate essentially all 17 surface patterns.

## Frequency-ranked patterns

### 1. frontmatter-echo — 77 of 89 files (25 moderate; top driver in 7)

A body passage — a `Trigger Boundaries` section, an identity preamble, or the opening paragraph under the H1 — that re-covers the use/non-use ground the YAML description already covers, usually in expanded form. The body maintains a second, longer copy of the routing contract on the same file's other surface.

- `plugins/review-family/skills/review-reviewer/SKILL.md`: "Non-trigger: ordinary critiques, first-pass reviews, implementation reviews, \"scrutinize this\", \"be adversarial\"…"
- `skills/orient-status/SKILL.md`: "Current state, recent activity, in-flight work, blockers, open decisions, deferred work, source conflicts, roadmap position, or live-vs-status-doc comparisons."
- `skills/steelman/SKILL.md` (opening paragraph): "Build the genuine strongest case *for* one position — usually one the user is inclined to dismiss — then stop without picking." — near-paraphrase of its description.

Root cause: the repo convention that the description is loader-facing routing text with a 25–60 word budget, combined with authors writing the body as a document that must stand alone once loaded. Scope gets written twice per skill, and the body copy — free of the budget — grows.

### 2. obligation-echo — 75 of 89 files (17 moderate; top driver in 4)

The same specific obligation or hard line stated in two or more separated body sections (excluding terminal recaps, counted separately): once as a headline rule, again inside the workflow step where it binds, again in an output or proof-boundary section. The highest-stakes rules get the most copies; `keep-green`'s no-commit/no-done-verdict invariant appears at least four times, and one file announces the habit outright.

- `skills/doc-drift-audit/SKILL.md`: "The cardinal honesty, stated once and repeated every run:"
- `plugins/git-cycle/skills/gh-address-comments/SKILL.md`: "never push, resolve a thread, or request re-review, regardless of how the threads classify" — re-stamped across intro, workflow, and output sections.
- `skills/making-recommendations/SKILL.md`: a "Core Behavior" invariant index that summarizes every following section ("These are the load-bearing invariants; the sections below add depth rather than restating them"), followed by a closing "Restraints" section that restates several anyway.

Root cause: defense-in-depth against partial reads — authors do not trust a skimming or mid-file-entering agent to carry a once-stated invariant to the point of action, so it is re-planted at every landing site. No within-file single-source discipline exists the way "by reference, never re-minting" exists across skills.

### 3. x-not-y-contrast — 70 of 89 files (68 minor)

Definition-by-negation as house voice: "X, not Y" / "a gate, not a criterion" / "display, never input" — the concept stated positively, then fenced against a foreseen misreading with a negated twin. Three-plus instances per file was the threshold; many files carry eight or more. Individually cheap, but the tic roughly doubles the length of every rule it touches, inventory-wide.

- `skills/dependency-upgrade/SKILL.md`: "Green is the **floor, not the proof**."
- `plugins/git-cycle/skills/closeout-check/SKILL.md`: "Use these as honest boundaries, not as ceremony."
- Six files share the section heading verbatim: "The moves — a rhythm, not a fill-in template" (`red-team`, `premortem`, `scope-cut`, `steelman`, `ideate`, `assumption-check`).

Root cause: a deliberate aphoristic register — the belief that agents comply better when the wrong reading is named and refused, not just the right one stated — hardened into the default sentence shape for new rules. This is stance prose: it may be earning its keep per instance; it is reported here because at 70 files it is one of the largest aggregate multipliers. No verdict rendered.

### 4. neighbor-fence — 63 of 89 files (5 major, 38 moderate; top driver in 34)

**The single largest identified word consumer.** Dedicated body prose differentiating this skill from named siblings at invocation time: `Fences` / `Boundaries with neighbors` / `Review-Family Routing` sections, "vs `skill`" bullets with a mini-essay per neighbor, and library-positioning preambles ("premortem is the library's one *prospective-failure* skill"). Some files carry the same neighbors in two sections (`red-team` has both "Boundaries with neighbors" and "When not to red-team"). Classifiers named it a top-two word consumer in 34 files — double any other pattern except contingency-ladder and per-rule-rationale.

- `skills/migration-safety/SKILL.md`: "Same word, opposite job. `migration-campaign` drives one mechanical *code* edit… across many call sites with a burndown"
- `skills/premortem/SKILL.md`: "`ideate` widens the *solution* space; premortem widens the *failure* space of one already-chosen solution."
- `skills/dependency-upgrade/SKILL.md`: "**vs `migration-campaign`** (the sharpest collision — its description already claims \"framework/API call-site bump\")."

Root cause: routing anxiety in an 89-lane library with genuinely overlapping territories, plus the description budget capping routing text at the loader surface — so the full neighborhood map overflows into every body. Each new sibling retro-adds fence bullets on *both* sides of the boundary, so the library-wide routing graph is paid for twice per edge and the ledgers grow monotonically with library size. Nothing prunes them.

### 5. handoff-choreography — 59 of 89 files (10 moderate; top driver in 7)

The routing family's second half: prose scripting where this skill's *outputs* go after it runs — "file each finding to `/triage` (or `$triage`), one per finding, and stop", "hand forward to `/characterization-tests`", named next-lane epilogues. Distinct from neighbor-fence (routing in); this is routing out. It is the only pattern present in the 161-word `grill-me` — even the leanest skill in the library pays this tax.

- `plugins/review-family/skills/scrutinize/SKILL.md`: "name `/triage` or `$triage` as the lane to file them — one issue per finding, classified there — and stop"
- `skills/test-trust-audit/SKILL.md`: "hand forward to `/characterization-tests` (or `$characterization-tests`) to author the net that work needs first"
- `skills/grill-me/SKILL.md`: "handing off to implementation-planning to turn the hardened plan into tasks, or to scrutinize for a formal written stress test"

Root cause: the library is designed as an interlocking lattice of single-purpose lanes, but a firing agent sees one SKILL.md at a time, so each skill locally encodes its slice of the workflow graph. Composition doctrine ("name the lane and stop") makes the epilogue a de facto mandatory section.

### 6. proof-boundary-liturgy — 59 of 89 files (28 moderate; top driver in 12)

Per-skill re-instantiation of the house epistemology: what this run proved and did not, proof-class and freshness label vocabularies, never-certify refrains, "structural validation is not behavior proof", "written is not working". Each skill re-derives the doctrine in its own claim vocabulary rather than citing a shared statement.

- `skills/postmortem/SKILL.md`: "a written postmortem proves the record and analysis exist, not that any fix has shipped."
- `skills/triage/SKILL.md`: "Triage mutation proves only the tracker actions performed; it does not prove the bug exists, the feature is implemented…"
- `skills/premortem/SKILL.md`: "**Never certify coverage:** no \"all failure modes captured,\" no likelihood×impact matrix presented as complete or precise."

Root cause: the proof-discipline culture (AGENTS.md, global CLAUDE.md) is judged not guaranteed to be in context at fire time in foreign repos, so every skill carries its own specialized copy. Discovery readers flagged this as plainly deliberate and often load-bearing — the claim types genuinely differ per skill — but it is a systematic length tax on every trust skill, and the shape converges enough across files to read as liturgy. Stance prose; no verdict rendered.

### 7. shared-doctrine-copy — 59 of 89 files (58 minor)

Library-wide contract text hand-copied into individual bodies: the protected-branch floor verbatim in 5 files ("if the repo defines none, treat `main`, `master`, `develop`, and `release/*` as protected"), the live-source proof-boundary sentence near-verbatim in 4 ("when the edited file is itself the live source, those checks are its proof…"), "never a green stamp over a signal/metric merely reached for" in 3, git-status-before-writing paragraphs, and the dual-runtime token pair (`/x` or `$x`) in 44 files / 71 occurrences plus `AGENTS.md` or `CLAUDE.md` in 14. Each copy is individually small — hence 58 minor ratings — but this is the pattern that exists in the most places while being invisible in any one of them.

Root cause: skills deploy globally with no include mechanism, so cross-cutting floors are deliberately re-inlined per skill — AGENTS.md itself ratifies one case ("the `git-cycle` skills carry their own inline copy"). Sibling-as-template authoring then propagates the sentences to skills where no policy requires them. Partly policy, partly drift; the two are not distinguished at the copy site.

### 8. per-rule-rationale — 58 of 89 files (4 major, 28 moderate; top driver in 21)

Individual imperatives shipping with their own justification welded on: an em-dash, colon, or because-clause narrating the concrete failure the rule prevents. The threshold was three-plus justified rules per file; in the heaviest files most rules carry one, and riders are frequently longer than the rule they justify. Third-highest top-driver count (21).

- `plugins/git-cycle/skills/merge-branch/SKILL.md`: "a `git merge --ff-only` here prints \"Already up to date\" and exits 0, which would otherwise read as a successful landing"
- `plugins/handoff/skills/save-handoff/SKILL.md`: "…so a secret written here can leak."
- `plugins/handoff/skills/throughline/SKILL.md`: "`-` and `_` sort differently at the precision boundary, so lexicographic comparison misorders mixed-precision names"

Root cause: the house conviction that agents skip or relitigate unmotivated rules, so persuasion is attached per rule at authoring time — reinforced by friction-driven editing in which each observed violation earns its rule an inline defense. No discipline distinguishes rules whose rationale changes execution from rules where the imperative alone would bind; once written, a justification is never pruned because deleting it feels like weakening the rule. Discovery noted `system-design-review` as a nearly rider-free counterexample — among the shortest review-family bodies — showing the style is a choice, not a necessity.

### 9. failure-mode-inoculation — 46 of 89 files (9 moderate; top driver in 9)

Prose addressed to the agent's predicted psychology rather than to a step: naming the temptation, drift, or rationalization the firing agent is expected to produce and forbidding it in advance — sycophancy, completion theater, verdict creep, template-filling, the structured shrug. Includes the "tell" register that teaches the agent to recognize its own error moment from the inside.

- `skills/premortem/SKILL.md`: "If you catch yourself concluding \"so this isn't ready,\" you have left premortem for `scrutinize`."
- `skills/making-recommendations/SKILL.md`: "you are fluent, you are agreeable, and the user usually arrives leaning."
- `skills-claude/skill-squad/SKILL.md`: "If you find yourself building a rubric or a scoreboard, you have turned a discovery engine into the bureaucracy it exists to replace."

Root cause: deliberate judgment-skill doctrine (protect and provoke thinking) executed as one standing counter-spell per feared temptation, with each observed or imagined lapse memorialized. The inventory of feared temptations only grows; nothing retires an inoculation when the underlying model behavior improves. This is the clearest case of stance prose that may be earning its length — several discovery readers judged instances load-bearing — and no verdict is rendered on it. Its cost profile is noted: dedicated hazard paragraphs, roughly half the body in some judgment skills per the discovery pass.

### 10. contingency-ladder — 39 of 89 files (27 moderate; top driver in 21)

Enumerated if-this-then-that coverage of degraded states: source-authority resolution orders ("if scope is missing, use the first available authority: 1…5"), edge-case tables, per-failure fallback branches each ending in a scripted report string or degraded mode. Tied for second-highest top-driver count (21) — where it appears, it eats real space.

- `plugins/review-family/skills/implementation-review/SKILL.md`: "If scope is missing, use the first available authority in this order:" (five-rung ladder)
- `plugins/git-cycle/skills/exiting-worktrees/SKILL.md`: a nine-row Edge Cases table plus per-check fallback prose ("Without one, `@{upstream}` is undefined and `git log @{upstream}..` errors out to *empty* — which looks identical to \"nothing unpushed\"")
- `skills/orient-status/SKILL.md`: "If they fail or are unavailable, label the affected claims `connector-unavailable` or `remote-unrefreshed`; do not substitute stale local refs"

Root cause: fail-fast/no-silent-fallback doctrine plus authoring for unattended, cross-runtime robustness — every environment failure observed once earns a permanent enumerated branch. Each branch is individually defensible; there is no cap and no shared degraded-mode reference to point at, so the happy path ships with its full failure protocol inline.

### 11. prohibition-inventory — 39 of 89 files (37 minor)

Negative authorization by enumeration: comma-lists of four to ten named forbidden actions where a category term could cover the class, plus "ghost prohibitions" naming machinery only a prior design would think to build.

- `plugins/git-cycle/skills/closeout-check/SKILL.md`: "does not authorize pushing, merging, opening or updating PRs, resolving review threads, deleting files or branches, syncing plugins or marketplace state…"
- `plugins/handoff/skills/save-handoff/SKILL.md`: "Do not create transaction state, active-write reservations, chain state, consumed markers, content hashes, recovery metadata, or `.session-state` files." — legible only as the inventory of a retired design.
- `skills/acceptance-map/SKILL.md`: "Do not push, open PRs, update issues, resolve comments, merge branches, delete files, or sync remote state."

Root cause: loophole anxiety toward a literal-minded reader — fear that any unnamed act escapes the rule — so categories are spelled out member by member, and lists grow monotonically because deleting a named prohibition feels like licensing it. The ghost subtype is prune-by-prohibition: removed machinery memorialized as standing bans instead of trusted absence.

### 12. label-taxonomy — 37 of 89 files (4 major, 16 moderate; top driver in 14)

Closed controlled vocabularies defined inline — verdict sets, severities, statuses, modes, freshness and evidence classes — each label with its own definition, misuse guard, and often a tie-break rule. One taxonomy costs 100–300 words; review and trust skills carry several apiece (`baseline` carries three: 6 statuses, 7 trust-gap types, 9 precedence rungs).

- `plugins/review-family/skills/implementation-review/SKILL.md`: four-status requirement vocabulary, three-severity set, and a four-verdict taxonomy with an ordering rule.
- `skills/orient-status/SKILL.md`: six freshness labels, each glossed.
- `plugins/git-cycle/skills/gh-address-comments/SKILL.md`: "`needs-user-decision`: the thread is ambiguous, conflicts with another requirement, needs product judgment…"

Root cause: the trust-skill doctrine — fix stop conditions and output shape; predictable shape is their value — generalized so that every judgment axis gets its own named enum. Deliberate machinery under the library's own rules; its length cost concentrates in the review family and git-cycle.

### 13. both-directions-fence — 34 of 89 files (33 minor)

A rule fenced in the same passage against both its over-application and its under-application — two poles, one sentence.

- `plugins/review-family/skills/scrutinize-skill/SKILL.md`: "Stopping over-flagging conformance is the goal; going lenient on judgment is the opposite failure, not success."
- `skills/writing-principles/SKILL.md`: "Deleting on sight and keeping out of superstition are the same failure in opposite directions."
- `plugins/git-cycle/skills/gh-address-comments/SKILL.md`: "stalling in analysis fails the request, and implementing unverified fails this discipline"

Root cause: the misfire-evidence feedback loop — a skill observed over-applied gets a correction, later observed under-applied gets the opposite correction, and both land in the same sentence. Mature, frequently-fired skills accrete two-sided fences; the pattern is a visible fossil of the build-and-prune history. Stance prose in most instances; no verdict rendered.

### 14. qualification-stack — 33 of 89 files (20 moderate; top driver in 6)

Sentences carrying three-plus qualifying clauses — parentheticals, em-dash chains, nested exceptions — that read as accreted patches on an older, simpler sentence. The extreme cases run 60–100 words with two or more em-dash asides and a parenthetical protocol inside.

- `plugins/review-family/skills/implementation-review/SKILL.md`: "(authorship is read off the request, the commit or PR author, or the governing handoff already recorded in scope; if unknown, run the cheap check anyway and state the assumption)"
- `skills/agent-facing-design/SKILL.md`: "a forcing function present but dulled, hedged, or softened until it no longer creates real counter-pressure (an adversarial posture reframed as collaborative) is the same defect by degree, not a pass"
- `plugins/git-cycle/skills/merge-branch/SKILL.md`: "(no upstream configured, the remote-tracking ref is absent, or the target is a purely local branch)"

Root cause: edit-by-accretion — each review finding or friction event appends a clause to the governing sentence rather than restructuring it — amplified by the one-logical-line-per-paragraph convention, under which a sentence's growth is invisible in diffs and never triggers a split. The same mechanism that produces both-directions-fence at the rule grain produces this at the sentence grain.

### 15. terminal-recap-gate — 30 of 89 files (14 moderate; top driver in 5)

A closing checklist section — `Done when`, `Evidence Gate`, `Quality bar`, `Red Flags` (18 files carry such a heading by grep; the census adds unlabeled closers) — whose items substantially re-enumerate obligations already imposed by the body. Every obligation is paid for twice: once as instruction, once as gate item.

- `plugins/review-family/skills/implementation-review/SKILL.md`: an 11-item Evidence Gate plus a 4-item Ship gate, nearly all items mapping to earlier sections.
- `skills/characterization-tests/SKILL.md`: "Every nondeterminism source is dispositioned — injected or normalized — before the first capture." (Done-when item mirroring a body rule.)
- `skills/observability-instrumentation/SKILL.md`: "Every footgun is explicitly checked: cardinality bounded, correlation/trace IDs threaded, no PII/secrets in logs…"

Root cause: template gravity from the stop-conditions convention — a verifiable exit checklist is a valued trust-skill shape, and authors populate it by walking back through the procedure. Nothing forces gate items to reference rather than restate.

### 16. output-packet-spec — 28 of 89 files (8 major — the most major ratings of any pattern; top driver in 18)

Fenced output templates plus prose governing them: field-by-field packet specs with mandated empty-state literals ("None found"), compression rules, and meta-rules policing which template applies when — including forbidden-template rules. Grep anchor: 19 files carry fenced ```markdown/```text output blocks (40 blocks total). Highest per-file weight of any structural pattern: 8 major ratings and a top-driver count of 18.

- `skills/skill-ux-design/SKILL.md`: two full closeout templates plus ~200 further words policing the boundary between them ("the closeout must include one sentence beginning `Safe UX because...`" / "can never carry the receipt").
- `skills/orient-status/SKILL.md`: a 4-field invariant brief plus a 9-field full packet with per-field empty-state rules.
- `skills/next-steps/SKILL.md`: "`Decision Gates`: use `None - all tasks have a single forward path.` when applicable."

Root cause: the same trust-skill shape doctrine as label-taxonomy, plus receipt anti-misuse: once a template exists, observed or anticipated misuse of it accretes guard prose around it, so each receipt grows its own meta-contract. Deliberate machinery under library rules; the census shows the spec-plus-policing form now extends well beyond trust skills.

### 17. inline-reference-payload — 10 of 89 files (4 major; top driver in 9)

The rare-but-outsized pattern: reference-grade lookup material carried whole in the body — per-engine behavior matrices, per-sink defense catalogs, diagnostic tables, alias maps, full command protocols with per-runtime variants. Only 10 files, but a top-two word consumer in 9 of them; the affected files include several of the longest in the inventory.

- `skills/migration-safety/SKILL.md`: "a `NOT NULL`-with-default add rewrites the table on PostgreSQL < 11 but not on 11+; MySQL routes large changes through `INSTANT` / `INPLACE` / `COPY` algorithms" — roughly half the skill is engine matrix.
- `plugins/git-cycle/skills/exiting-worktrees/SKILL.md`: the full native-vs-ExitWorktree removal protocol, prohibited-actions table, and edge-case table inline (2,274 words, no `references/`).
- `plugins/review-family/skills/implementation-review/SKILL.md`: nine surface lenses (≈80 words on average, the longest over 200) forming an inline review rubric (3,368 words — the longest body in the inventory).

Root cause: the AGENTS.md caution — "do not move behavior-critical instructions into a reference unless SKILL.md clearly says when to load it" — resolved by classifying nearly everything as behavior-critical, so the single-file default wins. The library's own counterexamples (`git-hygiene` offloads exactly this class to `references/git-hygiene-reference.md` and stays under 700 words; `system-design-review` externalized its taxonomy) show the discipline exists but is unevenly applied.

## Rarer observations with outsized or structural significance

- **Family-template skeletons.** The advisory family shares a verbatim skeleton: "The moves — a rhythm, not a fill-in template" appears word-for-word in the same 6 files (`red-team`, `premortem`, `scope-cut`, `steelman`, `ideate`, `assumption-check`), and "…is defined by inverting its nearest neighbors" verbatim in 5 of them plus a near-variant in `ideate` ("inverting its two nearest neighbors"), with matching section suites (identity preamble → boundaries → moves → no-certificate close → when-not-to). Sections exist because the family shape has them; each new family member reproduces the full skeleton. The same convergence appears in the ops trio (`deploy-plan`, `outcome-check`, `dependency-upgrade` share "never a green stamp over a …merely reached for").
- **Sibling-contract mirroring.** When a body names another skill it often inlines a summary of that skill's internals ("bounded anti-thrash stop conditions (retry cap, same-failure and oscillation detection, and escalation of cause-unknown failures to `diagnose`)" — `closeout-check` describing `keep-green`), duplicating text the sibling owns and creating drift surface. A small number of files pin seam claims to sibling line numbers (`diagnose:51`, `system-design-review:30-32,42` in `incident-response` and `red-team`), which adds a maintenance surface prose must service.
- **Incident-scar accretion.** In the git-cycle trust skills, each historically-hit tooling edge case lives inline forever — first as a guard paragraph at the point of failure, then again as a summary-table row (`exiting-worktrees` states the no-upstream, squash-merge, and no-op-tool cases twice each). The content is behavior-critical; the twice-stated inline form is the length driver.

## Patterns checked for and not found

These were tested by all 12 discovery readers and reported absent, batch by batch:

- **Superfluity** (prose addressed to no decision the firing agent makes): essentially absent. Readers repeatedly noted that recent commits stripping maintainer-facing philosophy from 20 bodies did their job — what survives is trace residue entangled with live instructions (a provenance clause here, a library-placement aside there), not a length driver. One residual instance: `skills/decision-record/SKILL.md`'s maintainer registration chore ("Because there is now a third consumer, register it: extend the maintenance note in `grill-with-docs/SKILL.md`").
- **Verbose sentence-level prose** (padding around one load-bearing clause): not found anywhere. The unanimous observation was the opposite — sentences are dense to the point of compression; length comes from clause count and obligation count, not filler. The per-word information density of this library is high; that is precisely why total length is an attention question rather than an editing-out-fluff question.
- **Inline examples that could be pointers**: largely absent. The inline templates and micro-examples that exist are load-bearing output contracts the agent must reproduce, or clause-length calibration specimens inseparable from their sentences. Exceptions were noted (two ASCII directory trees in `grill-with-docs`, a worked-invocation gallery in `openai-docs` and `transcript-export`) but are file-local, not a habit.
- **Poor progressive disclosure as a general habit**: not found as such. Where `references/`/`examples/` exist (16 skills) they are used well, with explicit load triggers. The failure shape that does exist is narrower and inverted: 73 skills have no disclosure structure at all, and in ~10 of them (pattern 17) genuinely reference-grade payloads sit inline. The habit is not "dumping into the body what references should hold" so much as "never creating references in the first place."

## Root causes, consolidated

The 17 surface patterns reduce to five producing mechanisms. Where several patterns share a cause, fixing (or accepting) the cause is the leverage point, not the individual pattern.

1. **The routing tax: every body re-carries its slice of the library map.** Produces neighbor-fence (63), handoff-choreography (59), frontmatter-echo (77), and much of shared-doctrine-copy's token doubling. Mechanism: 89 overlapping lanes, a deliberately tight frontmatter budget, misroute-anxiety after observed misfires, and reciprocal fence-adding whenever a sibling lands. This cluster is the largest aggregate consumer, it scales with library size rather than skill complexity, and it is paid on both sides of every boundary.
2. **Writing for a distrusted reader.** Produces obligation-echo (75), per-rule-rationale (58), x-not-y-contrast (70), failure-mode-inoculation (46), prohibition-inventory (39), terminal-recap-gate (30). Mechanism: the author models the firing agent as skimming, skeptical, literal-minded, and completion-biased — so every rule is restated at each landing point, self-justifying, twinned with its forbidden misreading, enumerated against loopholes, and recapped at the exit. Each device is individually rational; together they are the second-largest consumer and the dominant *per-rule* multiplier. Much of this cluster is deliberate stance prose whose value judgment belongs to the human.
3. **Patch-accretion editing.** Produces qualification-stack (33), both-directions-fence (34), incident-scar accretion, ghost prohibitions, and the growth trajectory of clusters 1 and 2. Mechanism: build-and-prune in practice mostly builds — each misfire, review finding, or incident appends a clause to the exact sentence that failed, and the one-logical-line convention hides sentence growth in diffs. Nothing in the lifecycle triggers a rewrite-in-place or retires a scar when the underlying behavior improves.
4. **Template gravity from the trust-skill doctrine.** Produces label-taxonomy (37), output-packet-spec (28), terminal-recap-gate (30), contingency-ladder (39), and the family skeletons. Mechanism: "fix stop conditions and output shape — predictable shape is their value" plus sibling-as-template authoring converge every skill onto a house section suite (identity → boundaries → modes → workflow → proof boundary → packet → done-when), whether or not each section earns its place in that skill. The doctrine is the library's own; the census shows its section suite now ships nearly universally, including in judgment skills.
5. **Self-containment with no include mechanism.** Produces shared-doctrine-copy (59), proof-boundary-liturgy (59), the inlined git-lifecycle protocol, and dual-runtime token doubling. Mechanism: skills fire in foreign repos where AGENTS.md floors may be absent, and there is no way for a dual-runtime SKILL.md to import shared contract text — so floors are re-inlined per skill, sometimes as explicit policy (git-cycle), sometimes as copy-drift. The cost is a fixed per-skill tax times 89, plus a synchronization surface every floor edit must sweep.

A sixth observation cuts across all five: the house voice itself — aphoristic, contrast-heavy, epigrammatic — is a deliberate register that trades words for memorability on nearly every rule. Discovery readers consistently classified it as stance rather than bloat, and consistently identified it as the largest sentence-level multiplier. It may be exactly what makes these skills work; that judgment is outside this audit's scope.

## Census tally (reference)

| # | Pattern | Files /89 | Major | Moderate | Top-driver |
|---|---------|-----------|-------|----------|------------|
| 1 | frontmatter-echo | 77 | 0 | 25 | 7 |
| 2 | obligation-echo | 75 | 0 | 17 | 4 |
| 3 | x-not-y-contrast | 70 | 0 | 2 | 1 |
| 4 | neighbor-fence | 63 | 5 | 38 | 34 |
| 5 | handoff-choreography | 59 | 0 | 10 | 7 |
| 6 | proof-boundary-liturgy | 59 | 0 | 28 | 12 |
| 7 | shared-doctrine-copy | 59 | 0 | 1 | 1 |
| 8 | per-rule-rationale | 58 | 4 | 28 | 21 |
| 9 | failure-mode-inoculation | 46 | 0 | 9 | 9 |
| 10 | contingency-ladder | 39 | 0 | 27 | 21 |
| 11 | prohibition-inventory | 39 | 0 | 2 | 1 |
| 12 | label-taxonomy | 37 | 4 | 16 | 14 |
| 13 | both-directions-fence | 34 | 0 | 1 | 0 |
| 14 | qualification-stack | 33 | 0 | 20 | 6 |
| 15 | terminal-recap-gate | 30 | 0 | 14 | 5 |
| 16 | output-packet-spec | 28 | 8 | 12 | 18 |
| 17 | inline-reference-payload | 10 | 4 | 4 | 9 |

Impact bands: minor <10%, moderate 10–25%, major >25% of body words (classifier judgment). "Top-driver": files whose classifier named the pattern one of that file's 1–2 largest word consumers. Working artifacts (per-batch discovery reports, census hits with per-file quotes, aggregation JSON) were session-scratchpad files; the verbatim quotes reproduced above were verified against source at audit time. Limitation: those scratchpad artifacts were ephemeral and are no longer recoverable, so the per-file counts in this table are spot-checkable but not re-derivable; future census runs should persist the per-file census JSON under `docs/audits/`.
