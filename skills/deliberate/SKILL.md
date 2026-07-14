---
name: deliberate
description: "Run one complete autonomous deliberation: generate options, prune on a contestable ledger, shape survivors, recommend honestly, contest the exclusions. Returns a close plus a re-run capsule. To develop one approved design collaboratively, use `design-exploration` instead; when serious, comparable options already exist and you only want the choice, use `making-recommendations` directly. Give the decision frame; optionally candidates with field mode, constraints at price, values, evidence with its authorization, and a survivor budget — or paste a prior capsule with directives."
disable-model-invocation: true
argument-hint: "[decision frame; candidates + field mode?; constraints at price?; values?; evidence + authorization?; survivor budget?; or: pasted capsule + re-run directives]"
---

# Deliberate

One explicit invocation (`/deliberate` or `$deliberate`) runs a complete autonomous decision pipeline — **Generate → Prune → Shape → Recommend → Contest** — in packet-isolated stages, and returns a close plus a control-state recovery capsule that makes disagreement and re-running cheap. The workflow never asks the user a mid-run decision question and judges alone when work is ready to cross each lane boundary; host permission prompts are runtime behavior outside this promise. The governing principle: **complete every judgment the run can honestly own, never manufacture a winner.** All four `making-recommendations` close shapes (`clear call`, `conditional call`, `check first`, `your call`) are successful completions.

## Bundle map and reload rule

The behavior-bearing contract exceeds what post-compaction reattachment preserves, so this spine points at purpose-named references with explicit reload points. Re-read the governing reference at every stage boundary and at capsule construction; rebuild byte-exact artifacts from the run-state store — references recover the rules, the store recovers the exact state, and neither packet composition, validation, nor capsule assembly ever runs from post-compaction memory.

- `references/stage-packets.md` — packet matrix, per-stage checklists, brief rendering, output envelope, validation, run-state store, validator boundary. Reload at every stage boundary.
- `references/methods.md` — the Prune and Contest methods (the only two methods this skill owns). Reload at those two boundaries.
- `references/capsule.md` — close order, capsule inventory, receipts, branch table, re-run transitions. Reload at every terminal, capsule construction, and re-run preflight.
- `references/schemas.md` — schemas, record key set, declared bounds, content identity.
- `references/contract-data.yaml` — the single canonical machine-readable source (matrix, stage-brief template, schemas, record keys); it wins over every authored rendering of it.
- `scripts/deliberate-validate.py` — the bundled helper both runtimes invoke via Bash for every brief render, validation, store write, and content identity. There is no reasoned fallback: orchestrator judgment never stands in for the validator.

## Invocation contract and echo

The invocation carries:

- **Decision frame** — mandatory; indiscernible → ask once before the run starts (pre-run, not mid-run).
- **Field mode** — `seed-and-widen` (default: supplied candidates seed Generate, which widens around them) or `closed-to-widening` (supplied field skips Generate and goes to Prune; required or echoed whenever candidates are supplied; echo states plainly: *closed to widening; the delegated Prune move may still narrow this field*).
- **Confirmed constraints**, each at its price. Unconfirmed constraints demote to soft preferences that never gate alone.
- **Stated values** (optional) — pre-answered exchange rates. Absent ones route the close toward `conditional call` / `your call`.
- **Soft preferences** (optional, labeled) — context, never gates.
- **Stakes context** (optional) — reversibility, stakes, blast radius; echoed with provenance; when absent, the echo says so and Recommend applies its own door-reading — the orchestrator never invents stakes.
- **Evidence inputs** (supplied facts, named paths, attachments, a conversation-context capsule) kept separate from **evidence authorization**. Default: *supplied evidence inputs and named paths may be inspected by default; no additional sources, web research, or probes are authorized unless echoed.* Authorization extends only to read-only inspection, web research, or explicitly non-mutating probes; experiments and side-effecting checks stay outside the run and return as `check first`.
- **Survivor budget** — default 4; a provisional capacity budget, explicitly not a claim about correct comparison width.
- **Inline-degradation permission** (optional) — covers isolation only, never mechanical validation.
- **Re-run payload** (optional): a pasted prior capsule plus directives — directive-free only when the capsule records an unfinished run.

The contract echo labels every material field `user-supplied`, `inferred`, `default`, or `absent`. Visible setup, correctable by live interruption where the session supports it, otherwise by re-run — no universal interrupt promise. Every re-run echo also surfaces each active record-cited retrieval with its source and retrieval time (excluded-fact freshness is user-owned by disclosure).

**Preflight** (pre-spend, before any stage launches) rejects, as `invalid invocation: <reason>` with echo only: `closed-to-widening` with an empty candidate set; a survivor budget that is not an integer of at least two; a re-run capsule that fails validation (an unsupported schema version resumes only through a shipped migration, never reinterpreted); a completed-run re-run payload carrying no directives — while an unfinished-run capsule (recorded terminal in the failure set, or stored exclusion check `exclusion check unavailable`) is itself the resume request and passes directive-free as an implicit resume directive; a directive normalization cannot classify; a field-mode change to `closed-to-widening` naming no candidate base; a declared-bound breach (bounds in `references/schemas.md`); a pasted emergency receipt. An invalid invocation never masquerades as a run outcome. Preflight also proves the helper runs and bootstrap-verifies — verify the validator's content identifier with the platform hasher (`shasum -a 256`), then run its fixtures if untested this session; a helper that cannot execute or verify is the capability-unavailable exit, pre-spend, never waived by degradation permission. Fresh isolated stage agents unavailable → capability-unavailable exit unless inline degradation was permitted (then the run proceeds inline, labeled, isolation never claimed). The run-state store is created only after every other pre-spend check has passed — a rejected invocation never creates a store; any failure before the store durably holds its first write is the pre-spend exit `store unavailable`, echo only.

**Unsupported invocation context:** invocation from a cron job, hook, scheduled task, or another skill exits pre-spend as `unsupported invocation context` where the context is detectable — enforcement neither runtime fully proves is never claimed.

**Setup decomposition** (pre-run): decompose the invocation into a **candidate-free decision frame**, the **candidate set** per field mode, **per-candidate authority notes** (visible lean, stated preference, valuing language — each labeled `user-supplied` or `inferred`, each citing the invocation or echo span that grounds it; language too ambiguous to ground a note resolves to `absent`, never to an inferred lean), and **stakes context** extracted span-backed, `absent` when no span grounds it. Candidate-attached preference language moves into that candidate's authority note; any candidate-neutral comparison criterion the same language carries is extracted span-backed into `soft-prefs` (or stated values when it prices an exchange rate), so Shape develops the criterion without learning whose case it strengthens. Criterion language inseparable from a candidate's identity stays whole in the authority note, and the proof boundary names the wording-borne lean residual. The raw invocation wording survives only in the capsule; no stage packet carries it. The decomposition is displayed with the contract echo, correctable the same way. Then resolve and pin, recording content identifiers in the store's pins item: the constituent source set (each constituent `SKILL.md` plus every reference it names), every named evidence path (directories expand to manifests), every in-packet input's stored bytes (`no comparable identity` when un-serializable), and the method identity (this `SKILL.md`, each reference, the data file, the validator).

## The authority model

> The invocation delegates stage transitions and field widening and narrowing under the echoed constraints and survivor budget. It does not authorize invented hard constraints, unstated value exchange rates — including a budget cut whose only defensible basis would price a trade the user never stated — evidence access beyond the echoed scope, side effects, or silent resolution of an option collision. Missing authority survives into an honest exit or close; it is never filled in.

Only explicitly supplied or directly evidenced confirmations become price-confirmed constraints; `inferred` constraints and values stay soft context and never authorize a hard cut. The ledger separates **permission to decide from authorship of the decision**: equivalence and dominance are agent determinations even when well grounded, and applying a confirmed constraint still contains an agent judgment about predicate satisfaction — the record's independent axes say so.

## Run shape

Five moves, all five packet-isolated in fresh, non-forked stage agents — Contest included, mandatory on every Contest-eligible branch. Stages receive ambient instructions and can read the filesystem; "blind" is not claimed. The isolation rule throughout: **hide previous-stage judgments, never decision-controlling user authority.**

1. **Generate** — reads and executes the live `ideate` contract. Returns the un-ranked field plus the untouched-fixed-points line. User-supplied seeds are collapse-exempt; a seed dies only on Prune's ledger.
2. **Prune** — the deliberate-owned method (`references/methods.md`): decisive cuts by confirmed filters, fact-established judgments, and disclosed judgment cuts — never scores or invented weights. Candidate-attached-lean-blind and value-aware. Returns survivors (an order-preserving subsequence of the field) plus labeled exclusion records, plus any disclosed budget overflow with its blocked-cut disclosures.
3. **Shape** — reads and executes the live `option-shaping` contract under its authorized-composition seam, on the frozen survivors. Constraint-consequence split: echoed price-confirmed constraint → record, preserve, Recommend owns the filter; unconfirmed or newly inferred → never a cut; identity-blocking collision → `field collision unresolved`.
4. **Recommend** — reads and executes the live `making-recommendations` contract on the comparison surface plus the complete authority packet (survivor authority notes carry the user lean; the raw invocation never enters). Owns filters on recorded consequences, all honest exits, and a disposition record for every exclusion it creates; the orchestrator routes each newly excluded candidate's authority note into Contest's packet.
5. **Contest** — the deliberate-owned detection-only method: tests recorded exclusions against the close's actual logic (or the `terminal-claim` on close-less eligible terminals); an excluded candidate carrying a visible user preference is always a live challenge.

**Orchestrator obligations, every stage:**

- Render every brief with the helper (`render-brief`) from the store per the stage's matrix column — never hand-assembled; the render identifier is recorded before dispatch; dispatch the rendered bytes unaltered (a named behavioral residual). An off-column refusal is corrected against the matrix, never overridden.
- Validate every returned envelope with the helper (`validate-envelope --accept`) before acceptance; a failed, timed-out, or malformed stage is `stage failed: <stage>`.
- Verify pins before every stage: the stage's constituent files (mismatch → `constituent drift`), the evidence identity (mismatch → `evidence drift`), and the method identity before every own-reference reread and helper invocation, the validator's identifier checked with the platform hasher (mismatch → `method drift`; a drifted validator → emergency receipt).
- In a git worktree, snapshot net Git-visible state before and after each stage; unauthorized mutation is `containment violation` — dirty-state receipt, stop for user direction, never silently restore or adopt. The snapshot pair detects net Git-visible change only; read-only execution is never claimed as proven.
- Stage agents request or preserve the session model where the runtime supports it; report effective models, `unknown` otherwise.
- Report stage transitions and counts without revealing hidden judgments ("Generated 9 options; pruning now").

**Global exit rule:** any constituent honest exit not explicitly transformed by this contract terminates the run as that exit; the orchestrator names the next lane, never asks a mid-run permission question, never silently enters that lane. Muddy goal at Generate → exit naming `outcome-shaping`, echo only.

**Operational failure rule:** failed/timed-out/malformed stage → `stage failed: <stage>`; only validated artifacts are preserved, carried in a **failure capsule** (the standard capsule shape, `not produced` marking unvalidated artifacts, terminal recorded) — resume restarts at the earliest stage whose artifact is absent or invalid. When the failed component is the validation helper or the store's read path, close instead with the **emergency receipt** (`references/capsule.md`) — recovery never depends on the component that just failed. If Contest alone fails on an eligible branch, report `exclusion check unavailable` and claim nothing about exclusion stability. Store failures are named for what failed, never charged to a stage: `store unavailable` pre-spend, `store failed: write` (failure capsule from previously stored state), `store failed: read` (emergency receipt).

## Composition seams

The named deliberate-owned overrides to constituent behavior — the only ones. Inside a run these seams outrank the constituent text; everywhere no seam is named the stage obeys the live constituent, and a conflict no seam covers resolves as a constituent honest exit under the global exit rule.

- **All stages:** constituent ask-the-user moves and permissioned handoffs are transformed — questions return inside the bounded packet as assumptions, gaps, or honest exits; handoffs terminate the run naming the lane.
- **`ideate` (Generate):** seeds are collapse-exempt in de-cluster; "ask them to fix the candidate set" is replaced by the delegated Prune stage.
- **`option-shaping` (Shape):** the provenance seam ships as a source edit in `option-shaping` itself (composition-workflow candidates accepted on evidenced invocation provenance); the constraint-consequence split and collision terminals are run-context packet rules layered on top.
- **`making-recommendations` (Recommend):** register-the-lean reads the extracted authority notes, never raw wording, and registers both leans **before reading the `surface` and `consequences` items** (envelope-recorded; the ordering inside one context is behavioral, and the proof boundary says so); unstable-fact checks are bounded by the echoed evidence authorization (unauthorized → `check first`, never performed); a could-win unshaped alternative → field-not-ready exit with a provisional rerun seed; the add-alternative/null-option move never adds a comparison candidate — a constraint-revealing or recommendation-changing alternative enters the close only as a named agent-derived consideration; every post-Prune exclusion owes a ledger disposition record — inside this run nothing disappears off-ledger.

## Close

Close order (full rules in `references/capsule.md`): **exclusion check** (eligibility: at least one validated `Status: active` exclusion record, excluding failure terminals and pre-stage re-run refusals) → **the recommendation or honest exit** → **the recovery capsule**, one paste-able fenced YAML document under `deliberate-capsule/v1`, ending in its completeness terminator, validated by the helper before display. The capsule's final content field is the single proof boundary; nothing outside the capsule re-renders it. Terminals and their artifact sets are totalized in the branch table (`references/capsule.md`); every branch emits only artifacts that exist. After the carrier finishes rendering — and only then — retire the store via `trash`, recording the path; `capsule bound exceeded` alone waits on user direction. A retirement failure is disclosed, never swallowed.

## Re-runs

One principle: **restart at the earliest stage whose input or required artifact became invalid** — matrix-derived, with named exceptions and the fixed directive-normalization order in `references/capsule.md`. Evidence authority is live, checked by content identity; constituent and method drift converts to invalidation via the source-drift map; revival is a full active-state transition followed by the standing cardinality branches; a pasted capsule's prior judgments enter a stage packet only where that stage's checklist names them.

## Helper crib

```bash
V=scripts/deliberate-validate.py; D=references/contract-data.yaml   # paths relative to this skill directory
shasum -a 256 $V                          # bootstrap: verify the validator with the platform hasher first
uv run --script $V fixtures --data $D     # must-block/must-pass set — run before trusting the helper
uv run --script $V identity --data $D [--as-evidence] <path>...
uv run --script $V init-store --data $D --store <root>/deliberate-run-live --run <id> --echo-body <echo.yaml>
uv run --script $V write-item --data $D --store <store> --kind <kind> [--stage <stage>] <body.yaml>
uv run --script $V render-brief --data $D --store <store> --stage <stage>
uv run --script $V validate-envelope --data $D --store <store> --stage <stage> --accept <envelope.yaml>
uv run --script $V validate-capsule --data $D <capsule.yaml>
```

Store root: the fixed name `deliberate-run-live/` directly under the runtime's ambient session-scoped temporary root (Claude Code: the session scratchpad directory named in ambient context). No detectable session-scoped root → `store unavailable`. Exit codes: 0 pass, 1 validation failure, 2 refusal, 4 store read loss.

## v1 boundaries

Read-only toward user-visible state throughout; no auto-revival loop; no persistence beyond the run by default (the store is retired to the user's local Trash at close — no live store survives the run, and byte destruction is never claimed); chat-first — the capsule is written to a file only on request; never fired from cron, hooks, or another skill.
