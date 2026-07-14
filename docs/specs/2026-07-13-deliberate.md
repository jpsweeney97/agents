# Design Spec: `deliberate` — one-invocation autonomous deliberation pipeline

**Status:** v8 approval candidate — seven review rounds folded; hand-authoring starts on JP's explicit approval · **Date:** 2026-07-13 · **Source:** this session's `outcome-shaping` → `making-recommendations` → `design-exploration` chain, with three external design reviews adjudicated via `review-reviewer` (all judged `reliable`; every confirmed correction incorporated), a fourth in-repo `scrutinize-skill` review folded as v5, and a fifth in-repo `scrutinize-skill` review adjudicated `reliable` via `review-reviewer` and folded as v6 — both confirmed P1 packet-contract defects plus the adjudication's two adjacent packet gaps, a sixth design review adjudicated `reliable` via `review-reviewer` and folded as v7 — its three confirmed P1 contract gaps plus the three adjacent findings its adjudication added, and a seventh design review adjudicated `reliable` via `review-reviewer` and folded as v8 — its four confirmed blockers and three execution risks, plus its adjudication's three missed-issue findings. Build-and-prune class (a user-invoked, read-only skill): **not a charter event**, no ledger entry owed.

## What this builds

`deliberate` is a dual-runtime skill that turns one explicit invocation into a complete autonomous decision run: generate a wide option field, narrow it transparently under delegated authority, develop the survivors to comparable depth, recommend honestly, and contest the exclusions against the recommendation's actual logic. It returns a self-contained recovery capsule that makes disagreement and re-running cheap.

The governing principle, in JP's words: **the workflow must complete every judgment it can honestly own, not manufacture a winner.** All four `making-recommendations` close shapes (`clear call`, `conditional call`, `check first`, `your call`) are successful completions — forcing a pick would delegate JP's values, not the process.

The pipeline: **Generate → Prune → Shape → Recommend → Contest**, orchestrated by a main context that is trust machinery plus exactly one named judgment surface — setup decomposition, constrained under Invocation contract and echo. Generate, Shape, and Recommend read and execute the live constituent contracts (`ideate`, `option-shaping`, `making-recommendations`); Prune and Contest are the only methods this skill owns, and the only deliberate-owned deviations from constituent behavior are the named composition seams (see Composition seams).

## The settled want (from the shaping arc)

- One invocation, no mid-run intervention; the workflow judges when work is ready to cross each lane boundary.
- Decisive autonomous pruning at the `ideate` → `option-shaping` boundary, in the labeled-lean form: cuts by confirmed filters, fact-established judgments, and disclosed judgment cuts — never scores or invented weights.
- Every exclusion gets an explicit, contestable reason plus a revival condition. The ledger is operational: revival conditions are re-run triggers, and re-run cost is the accepted safety price.
- JP's authorship relocates rather than disappears: front-loaded into the invocation contract, post-hoc into the ledger.
- Two-way door under the repo's build-and-prune model; the decisive dial is calibrated from run evidence.

## Design lineage

- **v1:** staged seam-authority architecture chosen over single-context and orchestrated-mode-clause alternatives; chat-first paste-able ledger chosen over a durable file.
- **v2** (review 1 folded): real invocation controls in both runtimes; packet-isolated (not "blind") stages; self-contained prune method; cardinality branches; refined kill records; Contest as a named fifth move; single recovery capsule; one narrow `option-shaping` edit.
- **v3** (review 2 folded): bounded authority grant with independent exclusion axes; `closed-to-widening` mode naming; honest survivor terminals; neutral authority capsule for Recommend; expanded `option-shaping` edit; detection-only Contest; conservative re-run invalidation; totalized branch table; single-sourced proof boundary; labeled exclusion records.
- **v4** (review 3 folded): value-trade guard with overflow-before-terminal; both stage packets completed by merge; three-case Shape constraint-consequence split; field storage separated from generation provenance; dominance gated to fact-established; full capsule inventory; provisional-seed and re-run totalization; Contest pinned isolated; operational-failure terminals; `option-shaping:51` ordering seam; honest budget-cut wording.
- **v5** (review 4 — in-repo `scrutinize-skill` — folded): seeds collapse-exempt through Generate with seed-preserving equivalence cuts; Recommend constituent-exit branch row plus a constituent-exit catch-all; fixed per-stage input-packet checklists keying the isolation claim; Contest's highlight made conditional-mandatory; two forward tests added.
- **v6** (review 5 — in-repo `scrutinize-skill`, adjudicated `reliable` via `review-reviewer` — folded): setup decomposition of the invocation replaces "original decision wording" in Recommend's packet (candidate-free frame; per-candidate authority notes with provenance; raw wording capsule-only); per-stage checklists made exhaustive two-sided lists, with the budget-overflow disclosure routed to Recommend as a named withhold exception; Contest totalized — eligibility keyed to validated exclusion records, ledger-only packet shape on surface-less terminals, excluded-visible-favorite always a live challenge; named composition-seam section with a precedence rule; constituent source set pinned at setup with a `constituent drift` terminal and capsule version evidence; favorite-excluded and zero/one-survivor forward tests upgraded to packet-level assertions; the empirical pruning check gated behind a pre-registered protocol.
- **v7** (review 6 — adjudicated `reliable` via `review-reviewer` — folded): canonical packet vocabulary and a five-stage include/withhold matrix, with Prune pinned lean-blind, an explicit read-isolation class for evidence-content leakage, and the wording-borne lean residual named; every post-Prune Recommend exclusion (filter, dominance end, collapse, `only one serious option` rivals) owes a ledger disposition record with its authority note routed to Contest; live evidence authority — capsule evidence identity, drift-restart at the earliest consuming stage, an `evidence unavailable` exit, retrieval-time provenance for web facts; orchestrator reclassified trust-plus-one-judgment-surface with span-backed, ambiguous-to-absent setup decomposition; pre-spend preflight with an `invalid invocation` terminal; containment-violation dirty-state receipt; pre-stage re-run refusals exempted from Contest eligibility; constituent pinning widened to the full referenced source set; the isolation proof phrase corrected to stages-that-ran; four forward tests added and one upgraded.
- **v8** (review 7 — adjudicated `reliable` via `review-reviewer` — folded): re-run transitions derived from the stage packet matrix with stated-reason exceptions — values changes regenerate, constraint changes keep re-prune under `ideate`'s relaxation-target reason, accepted seeds split by field mode; the capsule closed over restart (comparison surface, constraint consequences, close, terminal claim, exclusion check line stored, `not produced` markers) and made the carrier on failure terminals as the failure capsule; soft preferences candidate-free by construction, removed from Prune and routed to Shape, with the lean-blind claim narrowed to packet-lean-blind; stakes given a named owner — an optional invocation field extracted span-backed in setup decomposition — with Shape-level invalidation; run-time evidence pinning with an `evidence drift` terminal and the stage-local web-retrieval rule; the Recommend add-alternative seam completed; nine forward tests added.

## Identity and invocation

Dual-runtime skill at `skills/deliberate/`.

- Claude: `disable-model-invocation: true` in frontmatter. Consequence to document: the skill's description leaves the model's context entirely — natural-language requests never surface it; `/deliberate` is the whole contract, and the description is written for the human `/`-menu, not model routing.
- Codex: `agents/openai.yaml` with `policy: allow_implicit_invocation: false` (matches the `review-reviewer` precedent); `$deliberate` is the token.
- The Claude `argument-hint` and Codex `default_prompt` are authored together and kept aligned.
- Invocation from a cron job, hook, scheduled task, or another skill is an **unsupported invocation context**: Claude documents enforcement for manual-only skills; Codex documents only implicit-versus-explicit invocation, so where the context is detectable the run exits honestly rather than claiming enforcement neither runtime fully proves.

## The authority model

The bounded grant, with the value-trade guard stated inside it:

> The invocation delegates stage transitions and field widening and narrowing under the echoed constraints and survivor budget. It does not authorize invented hard constraints, unstated value exchange rates — including a budget cut whose only defensible basis would price a trade the user never stated — evidence access beyond the echoed scope, side effects, or silent resolution of an option collision. Missing authority survives into an honest exit or close; it is never filled in.

Only explicitly supplied or directly evidenced confirmations become price-confirmed constraints; `inferred` constraints and values stay soft context and never authorize a hard cut.

The ledger separates **permission to decide from authorship of the decision** via the exclusion record's independent axes. Equivalence and dominance are agent determinations even when well grounded, and applying a confirmed constraint to a specific option still contains an agent judgment about predicate satisfaction.

## Invocation contract and echo

The invocation carries:

- **The decision frame** — mandatory; indiscernible → ask once before the run starts (pre-run, not mid-run).
- **Field mode** — `seed-and-widen` (default: supplied candidates seed Generate, which widens around them) or `closed-to-widening` (supplied field skips Generate and goes to Prune; required or echoed whenever candidates are supplied; echo states plainly: *closed to widening; the delegated Prune move may still narrow this field*).
- **Confirmed constraints**, each at its price. Unconfirmed constraints demote to soft preferences that never gate alone.
- **Stated values** (optional) — pre-answered exchange rates. Absent ones route the close toward `conditional call` / `your call`.
- **Soft preferences** (optional, labeled as such) — context, never gates.
- **Stakes context** (optional) — reversibility, stakes, blast radius. Echoed with provenance like every field; when absent, the echo says so and Recommend applies its own door-reading to the decision frame — the orchestrator never invents stakes.
- **Evidence inputs** — supplied facts, named paths, attached material, a compact capsule of relevant conversation context — kept separate from **evidence authorization**. Default: *supplied evidence inputs and named paths may be inspected by default; no additional sources, web research, or probes are authorized unless echoed.* Authorization may extend only to read-only inspection, web research, or explicitly non-mutating probes; experiments, prototypes, and side-effecting checks stay outside the run, and Recommend returns them as `check first`.
- **Survivor budget** — default 4; a provisional capacity budget, explicitly not a claim about correct comparison width.
- **Inline-degradation permission** (optional).
- **Re-run payload** (optional): a pasted prior capsule plus directives.

The contract echo labels every material field `user-supplied`, `inferred`, `default`, or `absent`. Visible setup, correctable by live interruption where the session supports it, otherwise by re-run — no universal interrupt promise.

**Preflight** (pre-spend, before any stage launches): the run rejects an invocation whose fields cannot produce a valid run — `closed-to-widening` with an empty candidate set, a survivor budget that is not an integer of at least two (the floor of two makes smaller budgets unsatisfiable by delegated cuts), a re-run payload whose capsule fails validation — as the terminal `invalid invocation: <reason>`, echo only, no stage spend. An invalid invocation never masquerades as a zero-survivor or any other run outcome.

**Setup decomposition** (pre-run, before any stage launches): the orchestrator decomposes the invocation into a **candidate-free decision frame** — the decision restated so it names no candidate — the **candidate set** per field mode, and **per-candidate authority notes**: visible lean, stated preference, valuing language, each labeled `user-supplied` or `inferred` — plus the **stakes context** (reversibility, stakes, blast radius), extracted span-backed under the same rule, `absent` when no span grounds it. The raw invocation wording survives only in the capsule; no stage packet carries it. This decomposition is what keeps stage isolation satisfiable when the invocation itself names candidates: candidate identity and candidate-attached authority travel per candidate, so any packet can carry exactly its stage's share. The decomposition is judgment, not transport, and is constrained: every authority note cites the invocation or echo span that grounds it; language too ambiguous to ground a note resolves to `absent`, never to an inferred lean; and the decomposition is displayed with the contract echo, correctable the same way. Valuing language is extracted into authority notes; where it is inseparable from a candidate's identity, the candidate's wording travels intact and the proof boundary names the wording-borne lean residual. Soft preferences are split the same way: candidate-attached preference language moves into that candidate's authority note and out of the `soft-prefs` item, which is candidate-free by construction.

## Run shape

Five moves, **all five packet-isolated** in fresh, non-forked stage agents — Contest included, pinned isolated whenever it runs and mandatory on every Contest-eligible branch (the eligibility rule, under Close), so the proof boundary has one story. Stages receive ambient instructions and can read the filesystem; they do not receive earlier stage reasoning unless the seam packet carries it — "blind" is not claimed. Fresh agents unavailable → capability-unavailable honest exit unless the invocation permits inline degradation (a named, deliberate divergence from `plan-panel-loop`'s degrade-and-label idiom, because here isolation is load-bearing bias mitigation). The isolation rule throughout: **hide previous-stage judgments, never decision-controlling user authority.**

**Single-sourcing:** Generate reads and executes the current `ideate` contract; Shape reads and executes the current `option-shaping` contract plus its authorized-composition seam; Recommend reads and executes the current `making-recommendations` contract. Prune and Contest are the only methods `deliberate` owns. Methods are read live from the constituent files, never copied into this skill. Where this contract deliberately deviates from a constituent, the deviation is a named composition seam (see Composition seams); everywhere no seam is named, the stage obeys the live constituent.

**Global exit rule:** any constituent honest exit not explicitly transformed by this contract terminates the run as that exit. The orchestrator names the next lane; it never asks a mid-run permission question and never silently enters that lane.

**Stage rules, in every brief:** never ask the user a question — return assumptions, gaps, or an honest exit inside the bounded packet; behavioral containment (read-only, no nested agents or workflows, one bounded packet) is always included and is distinguished from **runtime-enforced containment**, which is claimed only when tool restrictions, sandboxing, or depth limits actually enforce it. In a git worktree, the orchestrator snapshots worktree state before and after each stage (the `plan-panel-loop` precedent); unauthorized mutation is reported and stops the run — while the proof boundary stays narrower, since snapshots do not prove absence of external side effects. Stage agents request or preserve the session model where the runtime supports that guarantee; the proof boundary reports the effective model when observable and marks it unknown or overridden otherwise. Each stage's input packet is composed from a fixed per-stage checklist authored in the skill — an explicit include list and withhold list, never recomposed from memory at run time — because output-packet validation cannot catch an isolation leak the orchestrator itself introduced on the way in. The checklists are exhaustive two-sided lists implementing the stage packet matrix below: an item on neither list is withheld by default, and admitting it is a skill edit, never run-time judgment. At setup the orchestrator resolves the constituent source set once — each constituent `SKILL.md` plus every reference and example file that `SKILL.md` names — and records a compact content identifier for each; every stage brief carries its constituent's resolved paths and identifiers, the stage verifies the match before executing (including any referenced file it actually loads), and a mismatch terminates the run as `constituent drift` — the checked-out tree is the live skill source, so a mid-run branch switch or rebase is a real hazard, not a hypothetical. The same pin covers evidence: setup records a content identifier for every named evidence path — the run's evidence identity — every stage brief carries it, the stage verifies each named path it actually loads before executing, and a mismatch terminates the run as `evidence drift`, the same mid-run hazard caught the same way. Web retrievals are stage-local by design: a stage's web facts enter shared run state only through its returned packet artifact, carrying source and retrieval time, and no stage inherits another stage's raw retrievals.

**Progress visibility:** inherit host behavior; report stage transitions and counts without revealing hidden judgments — "Generated 9 options; pruning now," "Shaping 4 survivors."

**Operational failure rule** (small and global): the orchestrator validates each stage packet before accepting it; a failed, timed-out, or malformed stage → `stage failed: <stage>`; unauthorized mutation → `containment violation`, closing with a dirty-state receipt — the changed paths, the pre- and post-stage snapshot identities, the stage charged, and the statement that side effects outside the worktree remain unverified — and stopping for user direction: the orchestrator never silently restores the worktree and never adopts the mutation; only validated partial artifacts are preserved — carried in a **failure capsule**, the standard capsule shape with `not produced` marking every artifact the run never validated and the terminal recorded, because the pasted capsule is the only defined resume input — and any later resume restarts at the earliest stage whose artifact is absent or invalid. If Contest alone fails on a Contest-eligible branch, the run reports `exclusion check unavailable` and never claims anything about exclusion stability.

The moves:

1. **Generate** — receives the frame, constraints (kept visible: ideate uses them as relaxation and inversion targets), seeds if any, and the generation-controlling supplied context per its matrix row: the evidence inputs whole and the stated values — never candidate-specific prior judgments, and never an orchestrator-side relevance filter over the evidence. Returns the un-ranked field plus the untouched-fixed-points line. **User-supplied seeds are collapse-exempt:** `ideate`'s de-cluster never merges, drops, or renames a seed in private scratch — a seed sharing a mechanism with another option survives to the field, and the shared mechanism passes to Prune as a recordable equivalence or collision judgment. A seed dies only on Prune's ledger; anything else is the silent option-collision resolution the authority grant forbids.
2. **Prune** — receives the field with per-candidate provenance flags, its matrix share of the effective contract, and the prune method below — never the authority notes or the soft preferences: Prune's packet carries no preference-class item, so it cuts **packet-lean-blind** (the evidence-content residual is the read-isolation class), and seed protection runs on provenance flags, which carry identity, not preference. Returns survivors plus labeled exclusion records, plus any disclosed budget overflow.
3. **Shape** — receives the frozen survivors, frame, constraints, stated values, candidate-free soft preferences — context for deriving live comparison questions, never gates — stakes context, evidence inputs, evidence authorization. Hidden: the wider field, the kills, Prune's reasoning. Constraint-consequence ownership, split explicitly: a consequence of an **echoed, price-confirmed constraint** → record it, preserve the candidate, Recommend owns the filter; an **unconfirmed or newly inferred constraint** → no cut ever, and an authority-gap exit only if honest comparison cannot proceed; a **collision requiring merge, drop, or changed identity** → `field collision unresolved`, while recordable collisions are recorded and development continues.
4. **Recommend** — receives the comparison surface plus the complete authority packet: the **candidate-free decision frame** from setup decomposition; the **echoed price-confirmed constraints**; **stated values**; **candidate-free soft preferences** (context, never gates); each survivor's original wording and the survivors' relative ordering **with an order-provenance field** — `user-supplied order — may evidence lean` or `Generate-produced order — non-evaluative; never evidence of user lean`; the survivors' **per-candidate authority notes** with provenance — this is where `making-recommendations`' register-the-lean move gets its user lean; **any disclosed budget overflow**, carried as the named exception to the Prune-judgment withhold so the unpriced trade is posed priced — the blocked trade's existence and identity cross, Prune's per-cut reasoning does not; reversibility, stakes, and blast-radius context; evidence inputs, evidence gaps, and evidence authorization. Withheld, exhaustively: the raw invocation wording, excluded identities, excluded candidates' authority notes (they route to Contest), and every other Generate/Prune judgment — if the user's visible favorite was excluded, Contest owns that challenge. Owns filters on recorded constraint consequences and collapsed survivors, and all honest exits; a discovered unshaped alternative that could win → field-not-ready exit, recorded as a provisional rerun seed in Generate's minimum option shape (handle, core idea, distinct bet). Every exclusion Recommend creates — a filter on a recorded constraint consequence, a fact-established dominance end, a survivor collapse, or the rivals set aside by an `only one serious option` close — appends a disposition record to the ledger in the labeled record shape before the close is valid; the orchestrator routes each newly excluded candidate's authority note into Contest's packet, and the close carries the record's revival condition.
5. **Contest** — packet-isolated; runs on every Contest-eligible branch (the eligibility rule, under Close). Receives its matrix share of the effective contract, the full ledger — Prune's exclusion records plus every Recommend disposition record — the **excluded candidates' authority notes** (Prune-excluded from setup decomposition, Recommend-excluded routed by the orchestrator after Recommend returns), and — when they exist — the comparison surface and close (`not produced` otherwise: on a surface-less terminal, Contest tests the exclusions against the terminal claim itself — on zero survivors, whether any recorded premise being wrong would revive a candidate; on one survivor, whether one would restore a rival). Detection only: identifies every recorded exclusion premise or revival condition the final logic — or terminal claim — makes live, names the one most worth contesting whenever any live challenge exists, never compares unshaped exclusions to shaped survivors, never substitutes a recommendation. **An excluded candidate carrying a visible user preference is always a live challenge**, whether or not its kill premise is load-bearing in the final logic.

## Stage packet matrix

The canonical packet-item vocabulary and the five-stage include/withhold matrix. The per-stage checklists in the skill implement this matrix literally; where the move prose above and this matrix disagree, the matrix wins. No stage receives the effective contract whole — that phrase names the capsule inventory, and each stage receives exactly its column.

| Packet item | Generate | Prune | Shape | Recommend | Contest |
| --- | --- | --- | --- | --- | --- |
| `frame` — candidate-free decision frame | ✓ | ✓ | ✓ | ✓ | ✓ |
| `field-mode` | — | ✓ | — | — | ✓ |
| `constraints` — echoed price-confirmed, each at its price | ✓ | ✓ | ✓ | ✓ | ✓ |
| `values` — stated values | ✓ | ✓ | ✓ | ✓ | ✓ |
| `soft-prefs` — labeled soft preferences, candidate-free by construction | — | — | ✓ | ✓ | ✓ |
| `evidence` — supplied inputs, known gaps, echoed authorization, pinned identifiers for named paths | ✓ | ✓ | ✓ | ✓ | ✓ |
| `budget` — survivor budget | — | ✓ | — | — | ✓ |
| `seeds` — user-supplied candidates, wording intact, provenance-flagged | ✓ | — (flags ride the field) | — | — | — |
| `field` — un-ranked field, untouched-fixed-points line, provenance flags | — | ✓ | — | — | — |
| `survivors` — frozen wording, order, order-provenance | — | — | ✓ | ✓ | — |
| `authority-notes`, survivor share | — | — | — | ✓ | — |
| `authority-notes`, excluded share (Prune- and Recommend-excluded) | — | — | — | — | ✓ |
| `records` — the ledger: Prune exclusion plus Recommend disposition records | — | — | — | — | ✓ |
| `overflow` — the blocked trade's existence and identity only | — | — | — | ✓ | ✓ |
| `consequences` — Shape-recorded constraint consequences | — | — | — | ✓ | — |
| `surface` — comparison surface | — | — | — | ✓ | ✓ when produced |
| `close` — Recommend's close | — | — | — | — | ✓ when produced |
| `stakes` — reversibility, stakes, blast radius, from the echo via setup decomposition | — | — | ✓ | ✓ | — |
| `method` — the deliberate-owned Prune or Contest method text | — | ✓ | — | — | ✓ |
| `pin` — the stage's constituent resolved paths and identifiers | ✓ | — | ✓ | ✓ | — |
| `raw-invocation` — capsule-only | — | — | — | — | — |
| `degradation` — inline-degradation permission, orchestrator-only | — | — | — | — | — |

A pasted capsule's prior artifacts enter a packet only where this matrix names them (the re-run rule). Prune's packet-lean-blindness is deliberate — no preference-class item, authority note or soft preference, appears in its column — so cuts must be defensible without knowing the user's preference, and the excluded-favorite challenge belongs to Contest, which holds the excluded share. The claim is packet-level only; evidence-content exposure is the read-isolation class below.

**Read isolation is packet-field only.** Stages read the filesystem, so withheld-class content — raw decision wording, excluded identities, lean language — can exist inside authorized evidence, and the packet boundary does not protect against that. The contract says so instead of pretending: a stage that encounters withheld-class material inside evidence must not treat it as user authority and must report the encounter in its returned packet, and the proof boundary carries a read-isolation line (`packet-field isolation only; evidence-content encounters: none reported | <listed>`) parallel to the containment class.

## Composition seams

The named deliberate-owned overrides to constituent behavior — the only ones. Precedence: inside a run these seams outrank the constituent text; everywhere no seam is named the stage obeys the live constituent, and a conflict no seam covers resolves as a constituent honest exit under the global exit rule, never by stage improvisation.

- **All stages:** constituent ask-the-user moves and permissioned handoffs are transformed — questions return inside the bounded packet as assumptions, gaps, or honest exits, and handoffs terminate the run naming the lane. The stage rules and global exit rule above carry this; it is a seam, not an accident.
- **`ideate` (Generate):** user-supplied seeds are collapse-exempt in de-cluster — a seed dies only on Prune's ledger; and ideate's "ask them to fix the candidate set before handoff" is replaced by the delegated Prune stage, because candidate-set fixing is exactly what the invocation authorized.
- **`option-shaping` (Shape):** the provenance seam ships as a source edit (see The constituent edit) because it changes what the skill accepts standalone; the constraint-consequence split and collision terminals in the Shape move are run-context packet rules layered on top.
- **`making-recommendations` (Recommend):** register-the-lean reads the extracted per-survivor authority notes, never raw invocation wording; unstable-fact verification and cheap-check recommendations are bounded by the echoed evidence authorization — an unauthorized check returns as `check first`, never performed; field-readiness failure exits as field-not-ready with a provisional rerun seed; the constituent's add-a-distinct-alternative and null-option move never adds a candidate to the comparison — an alternative that could realistically win is the field-not-ready exit, and one that merely reveals a constraint or would change the recommendation enters the close only as a named agent-derived consideration, never silently; and every post-Prune exclusion — filter, dominance end, collapse, or the rivals of an `only one serious option` close — owes a ledger disposition record in the labeled record shape, with the excluded candidate's authority note routed onward to Contest: the constituent may drop an option mid-comparison, but inside this run nothing disappears off-ledger.

Only `option-shaping` warrants a source edit: its user-provenance assumptions govern standalone behavior, while the `ideate` and `making-recommendations` overrides are pure run-context transformations that leave the standalone contracts untouched.

## Prune method

Independent cuts — permitted regardless of budget — are exactly:

- Applications of echoed price-confirmed constraints (predicate application recorded as agent judgment).
- **Fact-established** mechanism-equivalence: a nameable shared failure reason. When equivalence holds between a user-supplied seed and a generated option, the generated option is the one cut — the seed's original wording is what Recommend's authority packet preserves.
- **Fact-established** dominance at comparable resolution.

A contestable sketch-depth dominance impression never triggers a cut by itself — it may appear only as the disclosed rationale inside a budget-forced cut. There is no "retired non-serious" class: options that read as non-serious at sketch depth are exactly where anti-modal kills would launder, so they die only as fully recorded judgment cuts.

Budget cuts, when survivors still exceed the budget, carry two guards:

- **The value-trade guard:** each cut must be defensible without pricing an unresolved value trade. When the budget cannot be met without pricing one, the run does not invent the weight and does not immediately die: it **overflows the budget with disclosure** — carrying the un-cuttable survivors into Shape so Recommend can pose the trade priced — up to twice the echoed budget (a correctable default). Beyond that, the honest terminal `survivor budget cannot be met without an unstated value trade`. Value boundary outranks capacity preference; the budget was explicitly capacity, not epistemics.
- **Honest disclosure wording:** every budget cut is disclosed as a low-confidence cut of a **distinct mechanism-level candidate whose seriousness was unresolved at sketch depth** — never "a distinct serious bet," which claims what sketch depth cannot establish.

**Floor of two:** only a cut whose predicate source is a direct user rule *and* whose epistemic status is fact-established may reduce the field below two; budget cuts never may.

Every exclusion is a compact labeled record — prose inside each value, the warning omitted when inapplicable, no scores:

```text
Option:
Delegation:            <what the invocation authorized here>
Predicate source:      <direct user rule | agent-derived proposition>
Cut basis:             <constraint | equivalence | dominance | survivor budget | post-prune filter | post-prune dominance | post-prune collapse>
Epistemic status:      <fact-established at comparable resolution | contestable sketch-depth judgment>
Reason:
Load-bearing premise:
Strongest case:        <written before the kill>
Revive if:
Evidence warning:
```

Recommend's disposition records use the same template with the post-prune cut bases; `Delegation` still names what the invocation authorized there, and `Revive if` is still mandatory.

## Branch table

Totalized, with every branch emitting only artifacts that exist (`not produced` / `not applicable` otherwise):

| Branch | Terminal | Artifacts that exist |
| --- | --- | --- |
| Invalid invocation at preflight | `invalid invocation: <reason>` — pre-spend | echo only |
| Muddy goal at Generate | exit naming `outcome-shaping` | echo only |
| One right answer at Generate | that honest terminal | echo, partial field if any |
| Zero survivors | `no candidate survives the confirmed cuts` | echo, field, exclusion records, exclusion check, capsule |
| One survivor | `one candidate survives the authorized cuts; no comparative recommendation was performed` — survivor, rivals' exclusion basis, smallest next lane | echo, field, records, exclusion check, capsule |
| Budget unmeetable without a value trade (past overflow bound) | `survivor budget cannot be met without an unstated value trade` | echo, field, records incl. blocked cuts, exclusion check, capsule |
| Two or more survivors | full path | all |
| Field collision unresolved in Shape | that terminal | echo, field, records, partial surface, exclusion check, capsule |
| Authority gap in Shape | that exit | same as above |
| Field-not-ready from Recommend | that exit, seed recorded | all but close |
| Recommend constituent exit (`options not comparable` / `no basis yet` / `only one serious option`) | that exit; a basis-restoring question is carried in the close as the suggested re-run directive, never asked mid-run; `only one serious option` closes with the lone survivor and its rivals' disposition records | echo, field, records, comparison surface, exclusion check, capsule |
| Capability unavailable | that exit, pre-spend | echo only |
| Stage failure / malformed packet | `stage failed: <stage>` | echo, failure capsule (validated artifacts only) |
| Unauthorized mutation | `containment violation` | echo, dirty-state receipt, failure capsule (validated artifacts only) |
| Constituent drift mid-run | `constituent drift` | echo, failure capsule (validated artifacts only) |
| Evidence drift mid-run | `evidence drift` | echo, failure capsule (validated artifacts only) |
| Contest fails on an eligible branch | `exclusion check unavailable` — no stability claim | all but exclusion check |
| Revived option violating an active constraint | `authority conflict` — a pre-stage re-run refusal | capsule, records |
| Required evidence unresolvable at re-run | `evidence unavailable` — pre-spend on the re-run | echo, the pasted capsule as received |

Any constituent honest exit without its own row terminates under the global exit rule and emits the echo, every artifact validated before the exiting stage, and — whenever a field exists — the capsule, with the exclusion check whenever exclusion records exist.

A user-revived option joins on user authority, may exceed the budget, and evicts nothing.

## Close and recovery capsule

Close order:

1. **Exclusion check** — exactly one of: `Exclusion check: no live recorded challenge found`; `Exclusion check: live recorded challenges — X, Y`, naming the kill most worth contesting; `Exclusion check: not applicable — no exclusions recorded` (branches where Prune never cut); or `exclusion check unavailable` (Contest failed). **Eligibility:** Contest runs on every branch whose terminal or close carries at least one validated exclusion record, except the failure terminals (`stage failed`, `containment violation`, `constituent drift`, `evidence drift`), which stop the run immediately, and the pre-stage re-run refusals (`authority conflict`, `evidence unavailable`): no stage ran this run and the records they carry are the prior run's, so an exclusion check there would claim work this run never did. Detection language only; works under every close shape and every eligible terminal.
2. The recommendation or honest exit — any of the four `making-recommendations` close shapes is a successful completion.
3. **The recovery capsule**, one self-contained paste-able block (chat-first; written to a file only on request).

The capsule stores the **complete effective contract**: frame; field mode; priced constraints; stated values; soft preferences; evidence inputs and authorization; the **evidence identity** — a content identifier for every named path at run time, source and retrieval time for web research, `not re-resolvable` for attachments and conversation-capsule inputs (identifiers and provenance only; the capsule never embeds source contents); survivor budget; inline-degradation permission; the raw invocation wording (capsule-only — no stage packet carries it); the setup decomposition (candidate-free frame, per-candidate authority notes with provenance); the full Recommend authority packet (survivor wordings, ordering with provenance, per-survivor authority notes, any overflow disclosure, stakes/reversibility). Then the field, stored separately from its provenance:

```text
Original field:       <complete generated or user-supplied field — always present>
Generation boundary:  <untouched-fixed-points line | Generate not run: closed-to-widening>
```

Then prior survivors, any disclosed budget overflow, every exclusion and disposition record, and — verbatim when produced, `not produced` otherwise — Shape's comparison surface and recorded constraint consequences, Recommend's close and terminal claim, and the rendered exclusion check line: the capsule is closed over restart, so a resume can rebuild any stage's matrix packet, including a Recommend-only or Contest-only restart, from the capsule alone. Then any provisional rerun seed (marked unaccepted), revival instructions, and, as its final field, **the single proof boundary** — packet isolation achieved or not (claimed only when every stage that ran was fresh on a matrix-composed input packet, with intentionally skipped stages listed), the read-isolation line (`packet-field isolation only; evidence-content encounters: none reported | <listed>`), the pinned constituent source set (the full resolved set: paths and content identifiers), effective models when observable, evidence scope actually used, containment class (behavioral vs runtime-enforced), and what none of it proves. Nothing outside the capsule re-renders the proof boundary; a close that displays it displays the capsule's field verbatim. `not generated` never means `field unavailable`.

## Re-runs

One principle: **restart at the earliest stage whose input or required artifact became invalid.** The transitions below are derived from the stage packet matrix — a changed input invalidates the earliest stage whose column carries it, and any narrower transition states its testable reason inline. Where Generate never ran (`closed-to-widening`), a restart at Generate resolves to Prune.

Evidence authority is live, checked by identity: at re-run the orchestrator re-resolves every named evidence path and compares content identifiers against the capsule's evidence identity. Drift at an unchanged path invalidates every stored artifact built downstream of that evidence; the matrix routes the evidence item to every stage, so drift in run-supplied evidence restarts at the first stage that ran, and an input first added by a prior re-run directive restarts where it first entered. (Mid-run, the same mismatch is the terminal `evidence drift`; at re-run, drift is expected and routes here.) A required evidence input that no longer resolves — a missing path, an expired attachment marked `not re-resolvable` — exits as `evidence unavailable` rather than silently reusing the stored field. Web-research facts are not re-fetched wholesale: the capsule's retrieval-time provenance makes their age visible, and staleness routes through Recommend's unstable-fact rule under the echoed authorization.

- Only a revival directive changed, and no accepted provisional seed is active → skip Generate and Prune; the revived option joins the survivors on user authority and Shape reruns.
- Frame or field-mode change → regenerate.
- Constraint change → re-prune the stored field. The stated reason this stops short of Generate: `ideate` consumes constraints as relaxation and inversion targets, not gates, so the field's width does not depend on the constraint set — cuts are what a constraint change invalidates. The exception keeps its boundary: a constraint change that could alter what counts as a candidate or a mechanism-distinct field regenerates.
- Values change → regenerate: the matrix routes stated values to Generate as generation-controlling context, and no narrower reason survives that.
- Evidence content or authorization change → restart per the drift rule above; an expanded authorization is a Generate-consumed input (new sources can expose mechanism-distinct options), so it regenerates.
- Budget change → re-prune: Prune is the budget's earliest consumer.
- Soft-preference or stakes change → re-shape the stored survivors: Shape is their earliest consumer.
- Degradation-permission-only change (execution-only) → preserve every artifact and re-echo execution mode.
- A revived option is pinned against delegated budget, equivalence, and dominance cuts after any re-prune, provided it satisfies every still-active confirmed constraint; if it violates one, the run returns `authority conflict` at preflight, before any stage launches, rather than silently reviving or re-killing it. Reviving a constraint-failing option therefore requires withdrawing or repricing that constraint — a contract change, which re-prunes.
- **Accepted provisional seeds split by field mode.** Under `seed-and-widen`, an accepted seed is a new Generate input: Generate reruns and widens around it, collapse-exempt like any seed — the direct-to-Prune shortcut would freeze the field around an option Generate never saw. Under `closed-to-widening`, acceptance is the user adding a candidate to their closed field: the seed joins re-prune directly on user authority, carrying Generate's minimum option shape (handle, core idea, distinct bet), which provisional seeds record by construction.
- A provisional seed stays provisional until the user explicitly accepts it or changes field mode — relaunching with an unrelated directive is not acceptance, and a seed never auto-widens a `closed-to-widening` field.
- A re-run re-resolves and re-pins the live constituents; the capsule's recorded identifiers are evidence of what governed the prior run, never a freeze against constituent evolution — a method change between runs is visible, not blocking. The pasted capsule is orchestrator input: its prior judgments (records, close, proof boundary) enter a stage packet only where that stage's checklist names them.

## The constituent edit (`option-shaping`)

Patched across every provenance-dependent seam; `ideate` and `making-recommendations` stay untouched; `option-shaping/agents/openai.yaml` stays as is (verified to say "fixed options," which remains true).

- Accept candidates fixed by the user **or by an explicitly authorized upstream composition workflow** (the `:8` phrase and the `:12` "candidates the user selected" sentence both).
- The supplied field stays frozen inside Shape regardless of provenance.
- When shaping surfaces an option collision or a newly apparent constraint consequence: under user provenance, the existing ask-the-user behavior is unchanged; under an authorized composition workflow, report it without merging, dropping, or asking, and return the corresponding terminal (`field collision unresolved` for identity-blocking collisions) to the orchestrator.
- The `:51` ordering seam: "Preserve the user's option order" becomes preserve the *supplied field order*, carrying whether that order was user-supplied or produced by an upstream composition workflow, so downstream lean-reading stays honest.

The edit ships through the normal local-skill flow with the validation ladder, plus the standalone regression test below.

## v1 boundaries and build notes

Read-only throughout; no auto-revival loop; no persistence by default; chat-first; never fired from cron, hooks, or another skill (unsupported context, exits where detectable).

Lifecycle notes (outside the skill body, per house convention): the usage-ledger undercount of constituent fires inside stages (file reads, not Skill invocations); the description-invisibility consequence of `disable-model-invocation`.

Verify-first at authoring: whether Codex spawns ad hoc stage agents from a skill-driven session (docs indicate yes; shipped `.codex/agents/` TOML believed unnecessary — confirm live).

**Forward tests:**

- A rich field where an unconventional option deserves to survive.
- Zero- and one-survivor fields exercising the honest terminals — asserted at dispatch and packet level: Shape and Recommend never launch, Contest launches with the ledger-only packet shape (`not produced` for surface and close), and the terminal carries the exclusion check.
- A muddy-goal Generate exit.
- A `closed-to-widening` run (no manufactured field-boundary artifacts; capsule retains every candidate).
- Absent values → `conditional call` or `your call`.
- A visibly-user-leaning invocation whose favorite gets excluded — asserted at packet level: Recommend's literal input carries no excluded identity, no raw invocation wording, and no excluded-candidate authority note; Contest's input carries the favorite's authority note; the close surfaces that exclusion as a live challenge.
- The Recommend-side favorite kill: Shape records a confirmed-constraint consequence for the user's visible favorite and Recommend filters it — the ledger gains a complete disposition record, Contest receives the favorite's authority note, the close carries its revival condition, and the exclusion check names it live.
- An evidence file carrying a distinctive excluded-favorite marker: no delegation prompt carries the marker, any stage that meets it in evidence reports the encounter, and the proof boundary's read-isolation line reflects exactly that.
- A completed run against a named file, the file's content changed at the same path, capsule pasted into a fresh session: the re-run detects identifier drift and restarts at the earliest stage that consumed that evidence, not at the revival shortcut.
- A `closed-to-widening` invocation with no candidates, and separately a survivor budget below two: pre-spend `invalid invocation`, echo only, no stage launched.
- A rich field where meeting the budget would require pricing an unstated value trade (overflow first, terminal past the bound); on the overflow path, Recommend's packet carries the overflow disclosure and the close poses the trade priced.
- A field already within budget where only contestable dominance exists (no cut may fire).
- Generated ordering must not be read as a user lean.
- A closed-field capsule pasted into a fresh session must retain every candidate.
- A provisional seed under `closed-to-widening` (no silent widening).
- A `seed-and-widen` run where a supplied seed shares a mechanism with a generated option: the seed must reach Prune intact and may die only on the ledger, with the generated twin cut first under equivalence.
- A thin invocation driving Recommend's `no basis yet` exit: the run terminates with that row's artifact set and carries the basis-restoring question in the close as the re-run directive.
- A constraint change that must regenerate rather than re-prune.
- A malformed stage packet, a stage timeout, and a containment violation — the violation emitting the dirty-state receipt (changed paths, snapshot identities, the unverified-external-effects statement) and stopping for user direction.
- A constituent file mutated between stages: the next stage's identifier check fails, the run exits `constituent drift`, and the capsule records the pinned source set.
- Contest failure after a valid recommendation (no stability claim).
- A revived-option re-run and a constraint-repricing re-run; the revived option must survive delegated cuts.
- A packet-isolated run and the capability-unavailable exit.
- A `seed-and-widen` re-run with an accepted provisional seed: Generate reruns and widens around it, collapse-exempt; the same acceptance under `closed-to-widening` joins re-prune directly with no widening.
- An evidence-authorization expansion at re-run that could expose a mechanism-distinct option: the stored field is invalidated and Generate reruns rather than re-pruning.
- A values change at re-run: regenerates under `seed-and-widen`, re-prunes under `closed-to-widening`.
- A Recommend failure and a Contest failure, recovered separately from the pasted failure capsule alone: resume restarts exactly at the failed stage, rebuilding its matrix packet from the capsule with every earlier artifact reused.
- A named evidence file mutated between Generate and Shape: the pre-stage identifier check fails, the run exits `evidence drift` with the failure capsule, and no stage consumes the mutated version.
- A candidate-free soft preference that distinguishes the options: Shape's packet carries it and the surface develops it into a live question; Prune's packet omits it (packet-level assert) and no exclusion record cites it.
- A candidate-attached preference in the invocation: setup decomposition moves it into that candidate's authority note, `soft-prefs` stays candidate-free, and Prune's packet carries neither.
- A reversible and an irreversible decision: stakes enter the echo with provenance or as `absent`, Shape and Recommend receive them per the matrix, and close depth follows the constituent's door-reading — never an orchestrator invention.
- A Recommend run where the null option would change the recommendation without winning: the close names it as an agent-derived consideration and no unledgered candidate enters the comparison.
- The standalone `option-shaping` regression: ask-the-user moves *and* ordering behavior unchanged for user-provenance fields.

Then a `scrutinize-skill` pass, then the decisive empirical check: shallow-prune results against a full-shaping control, hunting excluded eventual winners. The check runs only after its protocol is pre-registered through `methodology-check` or the repo's contract-evaluation methodology — same-field control, winner adjudication, leakage boundary, case set, pass/fail rule — and until then its result is a plan, not evidence. Contract correctness makes v1 executable; only that control can tell whether the delegated pruning is worth trusting.

## Handoff

On JP's approval, the next lane is hand-authoring the bundle against `agent-facing-design` and `skill-ux-design` (Claude-side route), including the expanded `option-shaping` patch, then the forward tests above.
