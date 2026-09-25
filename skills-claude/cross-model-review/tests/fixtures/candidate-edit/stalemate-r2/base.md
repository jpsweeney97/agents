# Design: Retire the Typed Stalemate Third and Record the Close

Date: September 23, 2026, America/New_York.

Status: proposed design, awaiting JP's approval. Not an ADR, not a plan, not authorization to build. The settled want it serves is in `docs/session-reports/2026-09-23-capability-outcome-shaping.md` (section 2, JP's own words).

Repository state at writing: branch `chore/stalemate-third-design` from `main` at `431f132`; no source changed since `ef69b63` (2026-07-14). Every path below is relative to the repository root unless it starts with `~`.

Approach chosen by JP on 2026-09-23: **C**, one no-certificate ending, recorded in the run store. The rivals (A: purely subtractive with a text-only close; B: subtractive with a recorded close but the typed cap-exhausted ending kept) were declined.

## 1. What changes, in one paragraph

A `/synapsis` run ends in exactly one of two ways: the host emits a `RESOLVED_CERT@v1`, or the host **closes** the run. The close is a host-owned lifecycle event recorded through the driver (`synapsis close`), carrying a close-out note verbatim. It replaces three things that today are separate: the typed stalemate certificate (six types, never emitted through the driver), the typed cap-exhausted ending (never recorded; no run has ever reached its cap), and the discipline-only bounded non-terminal close (used five times; recorded only in a file outside the run store). The cap clock stays exactly as it is: `CapReached` fires by itself at the pre-registered bound, the window limits moves after it, and proposals freeze. What a capped run can do inside the window narrows to what the resolved family already provides: retire, press, and accept the live proposal. When nothing honest remains, the host closes.

## 2. Facts the design rests on

- No run record on disk holds a stalemate event. Across all 42 runs under `~/.synapsis/runs/`, the 232 recorded moves are all resolved-family events (`ProposalRevision`, `AcceptanceDeclaration`, `InitialStanceMove`, `RetireMove`, `ReserveMove`, `ContraryCaseMove`, `CounterpartAttestationMove`, `DefeatingArgumentMove`, `PressMove`). There are 24 `emit_resolved` operations and zero `emit_stalemate`, `declare_cap_tiebreak_exhausted`, or `record_cap_exhausted` operations. Old runs therefore need no stalemate event decoding.
- Every old run record lists five artifact hashes under `metadata.cross_model.artifacts`, two of them for the stalemate schema and registry. `validate_run_doc` requires that set to equal `ARTIFACT_PATHS` exactly (`src/cross_model_runtime/run_store.py:933-938`), and `artifact_drift` reads `current["artifacts"][name]` for every recorded name (`run_store.py:707-710`). Without a loader change, every old run would refuse to load after the deletion.
- The cap-exhausted ending requires `lifecycle.live_crux_ref` (`src/cross_model_contracts/terminal_outcomes.py:786-793`), which only a `CruxRevision` sets (`terminal_outcomes.py:603-604`), and `CruxRevision` is a stalemate-family event. Deleting the stalemate family makes that ending unreachable; this is why the design had to decide its fate.
- The `cross-model-review` helper imports seven names from `cross_model_runtime.codex_transport` and `schema_violations` from `cross_model_contracts.schema_validation` (`~/.agents/skills-claude/cross-model-review/scripts/cmr_protocol.py:9-14`, `cmr_engine.py:475`). Neither module's kept surface changes.

## 3. The ending model after the change

| Ending | What records it | What the host writes by hand |
|---|---|---|
| Resolved certificate | `emit-resolved` op, certificate verbatim, terminal emission marker | `answer.md` (ADR-0038) |
| Close | `close` op, close-out note verbatim, `RunClosed` lifecycle event | `answer.md` (ADR-0038); the note itself |

There is no terminal-outcome union, because there is one certificate type. The spec's sentence "a terminal outcome is exactly one of resolved or stalemate" becomes "a run's terminal outcome is a resolved certificate; every other ending is a close."

The three cases the close covers, and what governs each:

1. **Probes keep refusing.** ADR-0029's recognition and ADR-0030's close-bounds trigger stand unchanged: after the second refused sealed probe of successive revisions, no further attempt until bounds are pre-registered in the timestamped note, final attempt named, result binding, no same-text re-probe, no emission over a refusal. The note's required content (bounds with timestamps, close declaration, per-arm reasoning, transport-failure history) is unchanged. What changes: the note is now carried by the `close` op, so the store knows the run is closed.
2. **The models disagree and neither side will move.** The host closes with a note that states both positions, why neither accepted the other's checked correction, and the decision handed to JP. No classification into types; the note says it in prose.
3. **The cap window is spent with no concession.** The host closes. The cap clock still guarantees boundedness; the close replaces `CapTiebreakExhausted` plus `record-cap-exhausted`.

A close may also record an ordinary abandonment (a run started and then stopped for a reason outside the deliberation), so a started run never has to stay indistinguishable from an in-flight one.

## 4. The close: structure

### 4.1 Lifecycle event

`RunClosed(owner="host", order: int, ref: str)`, a frozen dataclass in `terminal_outcomes.py`, joining `CapReached` and `TerminalEmissionMarker` in `_HOST_OWNED_LIFECYCLE_EVENTS`. Machine-minted like the cap events: `ref` is `CLOSE-1`, `order` is the lifecycle's next order.

Rules, all in `TerminalLifecycleState.validate`:

- Owner must be `host`.
- Rejected after a terminal emission ("close after terminal emission").
- Rejected as a duplicate once a close exists; after a close, no event of any kind may follow ("no event may postdate RunClosed").
- If the pre-cap bound is met and `CapReached` is missing, rejected (the existing rule for every event).
- Strictly postdates `CapReached` when the run is capped: a new edge `close_postdates_cap_reached` in `O007_EDGE_POLICIES`, policy `strict`, replacing `cap_tiebreak_exhausted_postdates_cap_reached`.
- Does not require the window budget to be spent. The host's honest judgment that nothing remains replaces ADR-0020's "forced classification step".
- Does not spend window budget.

`emission_violations` keeps Te-1 (a certificate already emitted) and Px-3 (`cap_hit` agreement) and replaces CE-2 with **Cl-1**: "a close is recorded; terminal emission is mutually exclusive with RunClosed".

### 4.2 Machine surface

`DeliberationRun.close() -> RunClosed`: mints the event and appends it to the lifecycle directly (lifecycle-only, like the cap events). Raises the lifecycle's `ValueError` unwrapped (C6). Takes no note: the machine holds structure; the note is store data.

`codex_exchange` and the driver's `sealed-ask` refuse when `lifecycle.closed is not None`, with the same "the run reached a terminal ending" message they use after an emission.

### 4.3 Run store

- New op: `{"op": "close", "order": <event order>, "note": "<close-out note text, verbatim>"}`, appended by `record_close(doc, event, *, note)`.
- `_check_op`: `close` requires an integer `order` and a non-empty string `note`.
- `_replay_op`: `_require_next_order` then `run.close()`; the note is not replayed (already shape-checked).
- The note text lives inside `run.json`, the way an emitted certificate does, so the record is self-contained. The host may also keep a copy in the evidence dir; the op is the authority.

### 4.4 Driver

`synapsis close --run <dir> --note <path or ->` plus the common flags. Terminal-tier: artifact drift hard-fails without `--accept-artifact-drift`; target drift requires `--acknowledge-target-drift`. Sequence: lock, load, refuse torn record, containment, drift gate (terminal), rehydrate, `run.close()`, `record_close`, `sync_session`, dump. Result: `{"closed": {"order": N}}`. A missing or empty note is a typed exit-1 rejection before any write.

`status` reports `lifecycle.terminal` as `null`, `{"kind": "resolved", "order": N}`, or `{"kind": "closed", "order": N}`.

Subcommands after the change: `start`, `exchange`, `sealed-ask`, `host-move`, `codex-move`, `emit-resolved`, `close`, `status`. Removed: `emit-stalemate`, `declare-exhausted`, `record-cap-exhausted`.

### 4.5 What stays the host's by hand (ADR-0009)

Whether the close was honest, whether the note's per-arm reasoning is true, whether the bounds were really pre-registered before the final attempt. The code checks that a note exists and that the close sits legally in the log. Nothing classifies, grades, or derives from a close.

## 5. Contracts layer

### 5.1 Deleted

- `src/cross_model_contracts/stalemate_events.py`, `stalemate_emit.py`, `stalemate_blocking_presses.py`, `stalemate_constraint_preference_gate.py`, `stalemate_cross_arm_routing.py`, `stalemate_gate_common.py`, `stalemate_irreducible_gate.py`, `stalemate_scope_evidence_gate.py` (eight files, 2,631 lines).
- `src/cross_model_runtime/stalemate_tracer.py` (471 lines; the frozen #51 proof script, imported only by its own test).
- `schemas/synapsis/stalemate-cert-v1.schema.json`, `schemas/synapsis/terminal-outcome-v1.schema.json`, `schemas/synapsis/cap-exhausted-run-ending-v1.schema.json`.
- `registries/synapsis/stalemate-cert-registry-v1.json`.
- In `registry.py`: `stalemate_registry_violations` and the row helpers only stalemate rows use (`_distinct_field_values_violations`, `_participant_coverage_violations`); `load_registry` and the resolved row functions stay.
- In `projections.py`: `STALEMATE_DERIVER_VERSION`, `render_next_action`, `build_stalemate_decision_record`, `CAP_EXHAUSTED_DISPOSITION`, `render_cap_exhausted_ending`. The four resolved projections stay (ADR-0002; outside this design).
- In `schema_validation.py`: `validator_with_referenced_schemas` (its only purpose was the union; ADR-0021 is reversed). `load_schema`, `schema_violations`, `validate_with_draft_2020_12` stay.

### 5.2 `terminal_outcomes.py` after

Imports only `resolved_events`. Keeps `RunCapConfig`, `CapReached`, `TerminalEmissionMarker` (the `arm` field dropped; one arm exists), `EmissionRejected`, `TerminalLifecycleState`, `double_feed_resolved_event` (name kept), `append_terminal_emission_marker(lifecycle, emission_order, rejection)` (arm parameter dropped). Adds `RunClosed`. Removes `TERMINAL_ARMS`, `CapTiebreakExhausted`, `record_cap_exhausted_run_ending`, `double_feed_stalemate_event`, `live_press_refs`, the `_live_crux_ref` tracking, and the post-cap `crux_ref` targeting check. `_LEGAL_WINDOW_MOVE_TYPES` becomes `(RetireMove, PressMove, AcceptanceDeclaration)`; the post-cap acceptance-must-target-the-frozen-proposal check stays. `domain_view_disagreements` keeps its signature (one family is passed).

`resolved_emit.py`: the marker call drops its arm argument; three docstring mentions of the stalemate boundary are reworded. `resolved_events.py:265` comment and `tracer.py:54` comment are reworded.

## 6. Runtime

### 6.1 `deliberation_run.py`

Constructor drops `stalemate_schema`, `stalemate_registry`, `cap_exhausted_schema`. Removes `_stalemate_log`, `stalemate_log`, `emit_stalemate`, `declare_cap_tiebreak_exhausted`, `record_cap_exhausted`. `_append_move` accepts only `RESOLVED_DOMAIN_EVENTS`; anything else is the existing "not a domain event" `DeliberationRunError`. Adds `close()`. Module docstring loses the "both domain event logs" wording.

### 6.2 `run_store.py`

- `ARTIFACT_PATHS` keeps `resolved_schema` and `resolved_registry` only.
- `_EVENT_TYPES` is built from `RESOLVED_DOMAIN_EVENTS` only.
- `record_emit(doc, cert, *, order)` writes `emit_resolved`; the arm parameter goes. `record_declare_exhausted` and `record_cap_exhausted_op` go; `record_close` is added.
- `_check_op` accepts `host_move`, `codex_move`, `emit_resolved`, `close`; every other op, including the three retired ones, is "unknown op" (none exists in any record on disk).
- `validate_run_doc`: the artifact check becomes `set(ARTIFACT_PATHS) <= set(artifacts)` (a record may list artifacts the checkout no longer has; it must list every artifact the checkout does have).
- `artifact_drift`: a recorded artifact whose name is absent from the current snapshot reports `"artifact {name} removed from the checkout ({path})"`; present ones compare hashes as today. `snapshot_cross_model` hashes the current `ARTIFACT_PATHS` only.
- `FORMAT_VERSION` stays `SYNAPSIS_RUN@v1`. New records list two artifacts; old records list five; both load.
- `rehydrate_run` drops the three parameters.

### 6.3 `synapsis_driver.py`

`_load_artifacts` returns two entries; `_rehydrated` and `_cmd_start` pass two. `_cmd_emit` loses its arm parameter. `_cmd_declare_exhausted` and `_cmd_record_cap_exhausted` go; `_cmd_close` is added (section 4.4). The parser and `_dispatch` match. `_cmd_status` reports the `kind`-shaped terminal.

### 6.4 Old runs

All 42 load unchanged under the tolerant artifact rule. `status` on any of them already reports cross-model commit drift (the checkout moved on); after this change it also reports the two removed artifacts as drift. Nothing gates on `status`. The two historical bounded closes (`2026-08-26-athena-os-second-brain-fitness`, `2026-09-03-contest-recovered-cut`) are **not** closed retroactively: their records are append-only history and their close-out records in `~/.synapsis/evidence/` remain their authority.

## 7. Tests and fixtures

Deleted test files (14): `test_stalemate_cert_projections.py`, `test_stalemate_cert_registry.py`, `test_stalemate_cross_arm_routing.py`, `test_stalemate_runtime_tracer.py`, `test_stalemate_constraint_preference_gate.py`, `test_stalemate_emission_composition.py`, `test_stalemate_scope_evidence_gate.py`, `test_stalemate_emit_gate.py`, `test_stalemate_cert_schema.py`, `test_stalemate_irreducible_gate.py`, `stalemate_cert_fixtures.py`, `stalemate_emit_gate_fixtures.py`, `terminal_union_support.py`, `test_terminal_union_production_validation.py`.

Deleted fixture directories (66 files): `tests/fixtures/synapsis/stalemate-cert-v1/` (46), `terminal-outcome-v1/` (6), `cap-exhausted-run-ending-v1/` (14). `resolved-cert-v1/` (9) stays.

Modified test files:

- `test_terminal_outcome_lifecycle.py` (46 tests): stalemate-family window-move cases become resolved-family cases; `CapTiebreakExhausted` cases become `RunClosed` cases; the two-arm exclusivity cases become one-certificate cases; the module-roster test names `resolved_events` and `terminal_outcomes` only; the CE-3 rendering test goes.
- `test_double_feed_seam.py` (8): resolved-family cases only.
- `test_deliberation_run.py` (25): constructor calls drop three arguments; `test_emit_stalemate_passes_the_real_scope_ambiguity_gates` is replaced by close tests.
- `test_run_store.py` (49): drops the stalemate schema loads and the two-family roster; adds close-op and tolerant-artifact cases.
- `test_synapsis_driver.py` (46): the `emit-stalemate` argv case becomes `close`; adds close-command cases.
- `test_resolved_emission_composition.py` (24): the one window-budget case at lines 515-526 uses resolved-family moves.
- `test_residual_boundary_drift.py` (12): drops the stalemate fixture directories from its scan roots; the resolved anti-laundering set stays.
- `test_pin_comment_drift.py` (2): drops the eliminated-stalemate-type pin.
- `test_resolved_emit_gate.py`: one comment.

Added coverage (about 20 tests):

- Lifecycle: `RunClosed` legal with zero events; legal inside the window with budget left; rejected same-step after `CapReached`; rejected after emission; every event rejected after it; emission rejected after it (Cl-1); window budget unchanged by it; duplicate rejected; non-host owner rejected.
- Machine: `close()` mints order and ref; `codex_exchange` refused after close.
- Store: `record_close` shape; validation rejects a missing, non-string, or empty note; replay asserts order; the three retired ops are unknown; a five-artifact record loads; a record missing a current artifact is rejected; `artifact_drift` names a removed artifact.
- Driver: `close` happy path; refused after `emit-resolved`; refused twice; terminal drift gate; unreadable note path; `status` shows `closed`; `exchange` and `sealed-ask` refused after close.

Expected suite size: about 310 (from 523).

## 8. Documents

### 8.1 ADR-0039 (new; written through the decision-record lane after approval)

Records: the typed stalemate arm and its six types are retired; the terminal-outcome union is retired (one certificate type); the cap-exhausted ending is retired; the close is the one no-certificate ending and is recorded in the run store; the cap clock stands; ADR-0029's recognition and ADR-0030's close-bounds trigger and note content stand and now flow through the close. Names the evidence: zero stalemate events and zero cap-reached events in 42 runs; the host never offered the route; 14 of 15 real certificates by concession.

Status changes, per the repository's practice:

- Superseded by 0039 (wholly about the retired surface): ADR-0006, 0007, 0012, 0015, 0016, 0018, 0019, 0021.
- Narrowed by an addendum naming 0039: ADR-0003 (a wall vote that cannot name what moved now closes), 0009 (the stalemate residual-routing rows are void; the moderation model stands), 0011 (materiality no longer includes moving between resolved and stalemate or selecting a stalemate type), 0020 (cap clock stands; window moves are retire, press, accept; `CapTiebreakExhausted` and `CAP_EXHAUSTED_RUN_ENDING@v1` retired), 0028 (the unplaybooked-arm trigger is void), 0029 (the counterparty-declined-the-stalemate-route case no longer exists; the close is now recorded), 0030 (the no-store-marker ruling is reversed by the close; everything else stands), 0038 (the ending list is certificate or close).

### 8.2 Spec: `docs/specs/synapsis-terminal-outcomes-v1.md`, edited in place

- Status line gains "revised under ADR-0039 on 2026-09-23".
- Intro: "a resolved answer with `RESOLVED_CERT@v1`; every other ending is a recorded close."
- Terminal Outcomes: rewritten to the two-ending model; the cap paragraph names the close.
- Contrary-Case Probe: "until that objection is retired or the run closes."
- Deliberation Trace: the stalemate paragraph goes; the cap paragraph cites ADR-0020 as narrowed by ADR-0039.
- Sections STALEMATE_CERT@v1 and Terminal Outcome Union are removed.
- Validity Invariants: every stalemate and union invariant is removed; the resolved invariants stay.
- Cert Projections and Decision Record Trigger are untouched.

### 8.3 `CONTEXT.md`

Removed entries: Stalemate, Scope ambiguity, Evidence missing, Evidence conflict, Branch declaration, Crux revision, Branch/item reference, Decisiveness press, Constraint conflict, Value tradeoff, Irreducible stalemate, Final-position declaration, Unmoved-by declaration, Elimination-reason revision, Irreducible press, Stalemate next action, Stalemate certificate, Item declaration, Routing press, Single-waiver claim, Cap-exhausted ending.

Edited entries: the opening sentence; Cross-model; Terminal outcome ("the emitted certificate result of a run: a resolved certificate", avoid: close, envelope, status); Cap tiebreak ("the bounded post-cap window in which the run either resolves through a concession or is closed").

Added entries:

- **Close**: the recorded no-certificate ending of a `/synapsis` run. The host closes the run with a close-out note that says why no certificate was earned and what the user must decide. Avoid: stalemate, failure, timeout, cap-exhausted, fallback.
- **Close-out note**: the host-written prose the close carries verbatim: the reason, the pre-registered bounds and per-arm reasoning where probes refused, the transport-failure history, and the decision owed. Avoid: certificate, classification, verdict, run ending record.

### 8.4 Playbooks

- `docs/choreography/scope-ambiguity.md` and `docs/choreography/cap-exhausted.md` are deleted. The cap-clock content worth keeping (the cap fires by itself; the window; legal window moves) moves into `run-lifecycle.md`.
- `run-lifecycle.md`: the subcommand list; the live-proof paragraph drops the sentence about the three retired commands and says `close` has not yet run live; "Ending a run" is rewritten around the two endings, with the bounded-close paragraph becoming the close's probe-refusal case, ADR-0030's bounds discipline verbatim, and the `close` command shown.
- `concession.md` lines 13 and 59: "emit nothing or classify the stalemate honestly" becomes "close the run"; the capped case names the close.
- `uncontested.md` lines 20 and 62: a probe stance cannot ground a party position; the refused-successors ending is the close under ADR-0030's bounds.

### 8.5 Other text

- `AGENTS.md` line 48: "or the host honestly closes the run without a certificate."
- `~/.claude/skills/synapsis/SKILL.md` lines 8, 22, 72, 78, and 101: the three-way ending becomes certificate or close; "honest typed stalemate" is removed; the presentation rule for a close: no certificate, the decision handed back under "Need from you". This file is unversioned; the implementer records its pre-edit sha256 in the landing record.
- `docs/agents/domain.md` needs no change.

## 9. Error handling

- `close` with no note, an empty note, or an unreadable note path: typed exit 1 before any write.
- `close` on an emitted or already-closed run: the lifecycle's `ValueError`, exit 1, nothing written.
- `close` under artifact drift without the override, or target drift without the acknowledgment: `RunStoreError`, exit 1.
- `exchange`, `sealed-ask`, `host-move`, `codex-move`, `emit-resolved` after a close: refused with the run's terminal state named.
- A hand-edited record with a retired op, a non-string note, or a missing current artifact: `RunStoreError` at load.

## 10. Risks and checks

- The library helper is unaffected in code; its 61 tests are run from `~/.agents` after the change as proof (`uv run --no-project --with pytest --with-editable /Users/jp/Projects/active/cross-model python -m pytest skills-claude/cross-model-review/tests`).
- `test_residual_boundary_drift.py` scans source for banned derived terms; new wording must not introduce one.
- `close` makes no Codex call, so it needs no transport live proof. A scripted smoke against a scratch run dir (start with a fake runner, one move, close, `status`) is the proof. The first organic close is recorded in the run-lifecycle playbook when it happens; ADR-0034 forbids manufacturing one.
- The synapsis skill file has no version control. A separate decision (outside this design) is whether to move it into `~/.agents`.

## 11. Suggested build order

1. ADR-0039, the eight status lines, the eight addenda, the spec, `CONTEXT.md` (authority first; `docs/agents/domain.md` requires an ADR home before a new host obligation).
2. Contracts: delete the eight modules and the tracer; simplify `terminal_outcomes.py`; trim `registry.py`, `projections.py`, `schema_validation.py`; delete the 14 test files and 66 fixtures; repair the mixed tests. Suite green.
3. Runtime: `deliberation_run.py`, `run_store.py` (close op, tolerant artifacts), `synapsis_driver.py`. New tests. Suite green.
4. Playbooks, `AGENTS.md`, the skill text.
5. `uv run python tools/check.py`; the library tests from `~/.agents`; the scripted close smoke.

One commit per step on this branch; landing under the repository's usual review and receipts.

## 12. Decisions JP may still correct

1. The close-out note is stored verbatim inside `run.json` (section 4.3), not as a path plus hash.
2. A close is legal at any point before a certificate: with zero moves, and inside the cap window with budget left (section 4.1).
3. The two historical bounded-closed runs are left as they are (section 6.4).
4. ADR bookkeeping: eight superseded outright, eight narrowed by addendum (section 8.1).
5. `scope-ambiguity.md` and `cap-exhausted.md` are deleted; the close lives in `run-lifecycle.md`, not in a new arm playbook (section 8.4).
