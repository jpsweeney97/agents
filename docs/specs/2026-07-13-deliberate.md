# Design Spec: `deliberate` — one-invocation autonomous deliberation pipeline

**Status:** v5 approval candidate — four review rounds folded; hand-authoring starts on JP's explicit approval · **Date:** 2026-07-13 · **Source:** this session's `outcome-shaping` → `making-recommendations` → `design-exploration` chain, with three external design reviews adjudicated via `review-reviewer` (all judged `reliable`; every confirmed correction incorporated) and a fourth in-repo `scrutinize-skill` review folded as v5. Build-and-prune class (a user-invoked, read-only skill): **not a charter event**, no ledger entry owed.

## What this builds

`deliberate` is a dual-runtime skill that turns one explicit invocation into a complete autonomous decision run: generate a wide option field, narrow it transparently under delegated authority, develop the survivors to comparable depth, recommend honestly, and contest the exclusions against the recommendation's actual logic. It returns a self-contained recovery capsule that makes disagreement and re-running cheap.

The governing principle, in JP's words: **the workflow must complete every judgment it can honestly own, not manufacture a winner.** All four `making-recommendations` close shapes (`clear call`, `conditional call`, `check first`, `your call`) are successful completions — forcing a pick would delegate JP's values, not the process.

The pipeline: **Generate → Prune → Shape → Recommend → Contest**, orchestrated by a main context that does trust work only. Generate, Shape, and Recommend read and execute the live constituent contracts (`ideate`, `option-shaping`, `making-recommendations`); Prune and Contest are the only methods this skill owns.

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
- **Evidence inputs** — supplied facts, named paths, attached material, a compact capsule of relevant conversation context — kept separate from **evidence authorization**. Default: *supplied evidence inputs and named paths may be inspected by default; no additional sources, web research, or probes are authorized unless echoed.* Authorization may extend only to read-only inspection, web research, or explicitly non-mutating probes; experiments, prototypes, and side-effecting checks stay outside the run, and Recommend returns them as `check first`.
- **Survivor budget** — default 4; a provisional capacity budget, explicitly not a claim about correct comparison width.
- **Inline-degradation permission** (optional).
- **Re-run payload** (optional): a pasted prior capsule plus directives.

The contract echo labels every material field `user-supplied`, `inferred`, `default`, or `absent`. Visible setup, correctable by live interruption where the session supports it, otherwise by re-run — no universal interrupt promise.

## Run shape

Five moves, **all five packet-isolated** in fresh, non-forked stage agents — Contest included, pinned rather than optional, so the proof boundary has one story. Stages receive ambient instructions and can read the filesystem; they do not receive earlier stage reasoning unless the seam packet carries it — "blind" is not claimed. Fresh agents unavailable → capability-unavailable honest exit unless the invocation permits inline degradation (a named, deliberate divergence from `plan-panel-loop`'s degrade-and-label idiom, because here isolation is load-bearing bias mitigation). The isolation rule throughout: **hide previous-stage judgments, never decision-controlling user authority.**

**Single-sourcing:** Generate reads and executes the current `ideate` contract; Shape reads and executes the current `option-shaping` contract plus its authorized-composition seam; Recommend reads and executes the current `making-recommendations` contract. Prune and Contest are the only methods `deliberate` owns. Methods are read live from the constituent files, never copied into this skill.

**Global exit rule:** any constituent honest exit not explicitly transformed by this contract terminates the run as that exit. The orchestrator names the next lane; it never asks a mid-run permission question and never silently enters that lane.

**Stage rules, in every brief:** never ask the user a question — return assumptions, gaps, or an honest exit inside the bounded packet; behavioral containment (read-only, no nested agents or workflows, one bounded packet) is always included and is distinguished from **runtime-enforced containment**, which is claimed only when tool restrictions, sandboxing, or depth limits actually enforce it. In a git worktree, the orchestrator snapshots worktree state before and after each stage (the `plan-panel-loop` precedent); unauthorized mutation is reported and stops the run — while the proof boundary stays narrower, since snapshots do not prove absence of external side effects. Stage agents request or preserve the session model where the runtime supports that guarantee; the proof boundary reports the effective model when observable and marks it unknown or overridden otherwise. Each stage's input packet is composed from a fixed per-stage checklist authored in the skill — an explicit include list and withhold list, never recomposed from memory at run time — because output-packet validation cannot catch an isolation leak the orchestrator itself introduced on the way in.

**Progress visibility:** inherit host behavior; report stage transitions and counts without revealing hidden judgments — "Generated 9 options; pruning now," "Shaping 4 survivors."

**Operational failure rule** (small and global): the orchestrator validates each stage packet before accepting it; a failed, timed-out, or malformed stage → `stage failed: <stage>`; unauthorized mutation → `containment violation`; only validated partial artifacts are preserved, and any later resume restarts at the earliest stage whose artifact is absent or invalid. If Contest alone fails after a valid close, the run reports `exclusion check unavailable` and never claims anything about exclusion stability.

The moves:

1. **Generate** — receives the frame, constraints (kept visible: ideate uses them as relaxation and inversion targets), seeds if any, and the generation-controlling supplied context: relevant evidence inputs and stated values — never candidate-specific prior judgments. Returns the un-ranked field plus the untouched-fixed-points line. **User-supplied seeds are collapse-exempt:** `ideate`'s de-cluster never merges, drops, or renames a seed in private scratch — a seed sharing a mechanism with another option survives to the field, and the shared mechanism passes to Prune as a recordable equivalence or collision judgment. A seed dies only on Prune's ledger; anything else is the silent option-collision resolution the authority grant forbids.
2. **Prune** — receives field, full effective contract, and the prune method below. Returns survivors plus labeled exclusion records, plus any disclosed budget overflow.
3. **Shape** — receives the frozen survivors, frame, constraints, stated values, evidence inputs, evidence authorization. Hidden: the wider field, the kills, Prune's reasoning. Constraint-consequence ownership, split explicitly: a consequence of an **echoed, price-confirmed constraint** → record it, preserve the candidate, Recommend owns the filter; an **unconfirmed or newly inferred constraint** → no cut ever, and an authority-gap exit only if honest comparison cannot proceed; a **collision requiring merge, drop, or changed identity** → `field collision unresolved`, while recordable collisions are recorded and development continues.
4. **Recommend** — receives the comparison surface plus the complete authority packet: the **effective decision frame**; the **echoed price-confirmed constraints**; **stated values**; **labeled soft preferences** (context, never gates); the original decision wording; the survivors' original wording and relative ordering **with an order-provenance field** — `user-supplied order — may evidence lean` or `Generate-produced order — non-evaluative; never evidence of user lean`; any explicit or visible user preference among the survivors; reversibility, stakes, and blast-radius context; evidence inputs, evidence gaps, and evidence authorization. Still withheld: excluded identities and every Generate/Prune judgment — if the user's visible favorite was excluded, Contest owns that challenge. Owns filters on recorded constraint consequences and collapsed survivors, and all honest exits; a discovered unshaped alternative that could win → field-not-ready exit, recorded as a provisional rerun seed.
5. **Contest** — packet-isolated; receives the effective contract, comparison surface, close, and full ledger. Detection only: identifies every recorded exclusion premise or revival condition the final logic makes live, names the one most worth contesting whenever any live challenge exists, never compares unshaped exclusions to shaped survivors, never substitutes a recommendation.

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
Cut basis:             <constraint | equivalence | dominance | survivor budget>
Epistemic status:      <fact-established at comparable resolution | contestable sketch-depth judgment>
Reason:
Load-bearing premise:
Strongest case:        <written before the kill>
Revive if:
Evidence warning:
```

## Branch table

Totalized, with every branch emitting only artifacts that exist (`not produced` / `not applicable` otherwise):

| Branch | Terminal | Artifacts that exist |
| --- | --- | --- |
| Muddy goal at Generate | exit naming `outcome-shaping` | echo only |
| One right answer at Generate | that honest terminal | echo, partial field if any |
| Zero survivors | `no candidate survives the confirmed cuts` | echo, field, exclusion records, capsule |
| One survivor | `one candidate survives the authorized cuts; no comparative recommendation was performed` — survivor, rivals' exclusion basis, smallest next lane | echo, field, records, capsule |
| Budget unmeetable without a value trade (past overflow bound) | `survivor budget cannot be met without an unstated value trade` | echo, field, records incl. blocked cuts, capsule |
| Two or more survivors | full path | all |
| Field collision unresolved in Shape | that terminal | echo, field, records, partial surface, capsule |
| Authority gap in Shape | that exit | same as above |
| Field-not-ready from Recommend | that exit, seed recorded | all but close/Contest |
| Recommend constituent exit (`options not comparable` / `no basis yet`) | that exit; its basis-restoring question is carried in the close as the suggested re-run directive, never asked mid-run | echo, field, records, comparison surface, capsule |
| Capability unavailable | that exit, pre-spend | echo only |
| Stage failure / malformed packet | `stage failed: <stage>` | echo plus validated partials only |
| Unauthorized mutation | `containment violation` | echo plus validated partials only |
| Contest fails after valid close | `exclusion check unavailable` — no stability claim | all but exclusion check |
| Revived option violating an active constraint | `authority conflict` | capsule, records |

Any constituent honest exit without its own row terminates under the global exit rule and emits the echo, every artifact validated before the exiting stage, and — whenever a field exists — the capsule.

A user-revived option joins on user authority, may exceed the budget, and evicts nothing.

## Close and recovery capsule

Close order:

1. **Exclusion check** — `Exclusion check: no live recorded challenge found` or `Exclusion check: live recorded challenges — X, Y`, naming the kill most worth contesting whenever any live challenge exists (omitted otherwise). Detection language only; works under every close shape.
2. The recommendation or honest exit — any of the four `making-recommendations` close shapes is a successful completion.
3. **The recovery capsule**, one self-contained paste-able block (chat-first; written to a file only on request).

The capsule stores the **complete effective contract**: frame; field mode; priced constraints; stated values; soft preferences; evidence inputs and authorization; survivor budget; inline-degradation permission; the full Recommend authority packet (original wording, ordering with provenance, visible preference, stakes/reversibility). Then the field, stored separately from its provenance:

```text
Original field:       <complete generated or user-supplied field — always present>
Generation boundary:  <untouched-fixed-points line | Generate not run: closed-to-widening>
```

Then prior survivors, any disclosed budget overflow, every exclusion record, any provisional rerun seed (marked unaccepted), revival instructions, and, as its final field, **the single proof boundary** — packet isolation achieved or not (claimed only when every stage ran fresh on a checklist-composed input packet), effective models when observable, evidence scope actually used, containment class (behavioral vs runtime-enforced), and what none of it proves. Nothing outside the capsule re-renders the proof boundary; a close that displays it displays the capsule's field verbatim. `not generated` never means `field unavailable`.

## Re-runs

One principle: **restart at the earliest stage whose input or required artifact became invalid.**

- Only a revival directive changed, and no accepted provisional seed is active → skip Generate and Prune; the revived option joins the survivors on user authority.
- A change that only alters downstream admissibility (values, evidence scope, budget, degradation permission where execution-only) → re-prune the stored field; degradation-permission-only changes preserve the field and re-echo execution mode.
- A change that could alter what counts as a candidate or a mechanism-distinct field — the frame, the field mode, or a constraint change of that character → regenerate in `seed-and-widen`.
- A revived option is pinned against delegated budget, equivalence, and dominance cuts after any re-prune, provided it satisfies every still-active confirmed constraint; if it violates one, the run returns `authority conflict` rather than silently reviving or re-killing it. Reviving a constraint-failing option therefore requires withdrawing or repricing that constraint — a contract change, which re-prunes.
- A provisional seed stays provisional until the user explicitly accepts it or changes field mode — relaunching with an unrelated directive is not acceptance, and a seed never auto-widens a `closed-to-widening` field. An accepted seed must carry Generate's minimum option shape (handle, core idea, distinct bet) to join re-prune directly; otherwise it passes through Generate, collapse-exempt like any seed.

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
- Zero- and one-survivor fields exercising the honest terminals.
- A muddy-goal Generate exit.
- A `closed-to-widening` run (no manufactured field-boundary artifacts; capsule retains every candidate).
- Absent values → `conditional call` or `your call`.
- A visibly-user-leaning invocation whose favorite gets excluded (Contest, not Recommend, must surface it).
- A rich field where meeting the budget would require pricing an unstated value trade (overflow first, terminal past the bound).
- A field already within budget where only contestable dominance exists (no cut may fire).
- Generated ordering must not be read as a user lean.
- A closed-field capsule pasted into a fresh session must retain every candidate.
- A provisional seed under `closed-to-widening` (no silent widening).
- A `seed-and-widen` run where a supplied seed shares a mechanism with a generated option: the seed must reach Prune intact and may die only on the ledger, with the generated twin cut first under equivalence.
- A thin invocation driving Recommend's `no basis yet` exit: the run terminates with that row's artifact set and carries the basis-restoring question in the close as the re-run directive.
- A constraint change that must regenerate rather than re-prune.
- A malformed stage packet, a stage timeout, and a containment violation.
- Contest failure after a valid recommendation (no stability claim).
- A revived-option re-run and a constraint-repricing re-run; the revived option must survive delegated cuts.
- A packet-isolated run and the capability-unavailable exit.
- The standalone `option-shaping` regression: ask-the-user moves *and* ordering behavior unchanged for user-provenance fields.

Then a `scrutinize-skill` pass, then the decisive empirical check: shallow-prune results against a full-shaping control, hunting excluded eventual winners. Contract correctness makes v1 executable; only that control can tell whether the delegated pruning is worth trusting.

## Handoff

On JP's approval, the next lane is hand-authoring the bundle against `agent-facing-design` and `skill-ux-design` (Claude-side route), including the expanded `option-shaping` patch, then the forward tests above.
