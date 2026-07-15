# Deliberate Validator Monolith Tech Debt Scan

Status: complete
Date: 2026-07-15
Target: `skills/deliberate/scripts/deliberate-validate.py` at `61583d5`
Depth: medium
Finding Cap: 12
Artifact Path: `docs/audits/2026-07-15-deliberate-validator-debt-scan.md`

## Result Brief

### Top Debt Calls

- A naive file split is unsafe: `contract-data.yaml` defines an exact file-level method-surface inventory, method pins reject manifests, the orchestrator platform-hashes the entry script, and capsule validation requires the current exact inventory. Moving behavior into ordinary imported modules without redesigning that authentication boundary would weaken bootstrap proof; adding those modules to the inventory would make prior capsules fail current validation unless compatibility is handled explicitly.
- The executable contains its own dominant test corpus: 4,600 of 10,667 lines belong to fixture support and `cmd_fixtures`, with the command alone spanning 4,116 lines and 135 nested functions. The healthy 158-case suite is therefore both the main safety net and a major source-navigation/review burden, while no independent black-box characterization layer protects the CLI during structural movement.
- Production responsibilities are concentrated enough to compound review cost: one 411 KB file owns twelve CLI commands, parsing and read authorization, canonical contract validation, the run-state store, envelope acceptance, brief rendering, capsule validation, capsule import, rendering generation, and fixtures. Static analysis found 22 functions above Ruff's default C901 complexity threshold, and the file accumulated 12,891 changed lines across 12 commits in two days.

### Do First

- Add an independent black-box characterization suite around the unchanged `deliberate-validate.py` entrypoint. Pin the twelve-command CLI surface, exit-code mapping, stdout/stderr shapes, representative store files, accepted/rejected envelope and capsule behavior, and the current 158-fixture summary before moving production code. This work is un-gated and starts immediately: the harness is test-only and outside the runtime method-surface inventory. Keep the existing fixture command intact as the control; the harness's pass criterion is that it demonstrates detection of representative public-seam mutations (mutate, observe the net fail, restore, rerun green), never a claim of full behavioral coverage.

### Why It Matters

- This file is not ordinary utility code; it is trust machinery used identically by both runtimes, and failure removes resumable recovery. The current shape makes every correction compete with a large review surface, while an incautious modularization can silently weaken method authentication or reject saved capsules. The mandatory fixture preflight also costs about 52 seconds per tested session today.

### Audit Path

- `docs/audits/2026-07-15-deliberate-validator-debt-scan.md`

### Coverage Limits

- This is a medium, capped subsystem audit and ranked repair backlog, not an execution sequence. It did not edit the validator, inventory saved capsules, prototype an authenticated multi-file loader, run cross-runtime end-to-end smoke, measure coverage, or perform security-vulnerability analysis. Dependency-aware sequencing remains premature until the method-identity and prior-capsule compatibility choice is settled.

## Scan Snapshot

- Scope: subsystem - the validator script plus its direct skill/spec contracts, fixture files, smoke evidence, repository integrity checks, and git history; constituent skills and unrelated repository code are outside the target.
- Archetype: single-author project plus heavily integrated trust surface.
- Stakes: high - the helper controls acceptance, recovery, store mutation, drift detection, and capsule import across both runtimes.
- Output Mode: artifact.
- Security Boundary: dependency maintenance only; vulnerability work routes to a security-scan skill, not this audit.
- Repo Instructions Checked: `AGENTS.md` and the supplied global instructions for `/Users/jp/.agents`.

## Focus & Coverage

| Category | Disposition | Evidence Checked | Notes |
| --- | --- | --- | --- |
| dependency | background | PEP 723 header, imports, repository manifests | One runtime dependency (`pyyaml`) and no package framework; no maintenance debt promoted. Preserve the one-command cross-runtime property unless evidence justifies added packaging. |
| code-health | primary | file/AST metrics, Ruff, section inventory, churn history, large-function inventory | Concentration, complexity, and review load are the main code-health costs. |
| test-debt | primary | `cmd_fixtures`, four external YAML fixtures, 158-case live run, repository checks | Strong behavioral breadth, weak separation and no independent public-boundary harness. |
| architecture-drift | primary | method-surface inventory, method-pin validation, capsule validation, static cross-section call graph | Authentication and capsule continuity make ordinary modularization a contract question. |
| operational | background | skill preflight obligation, live fixture duration, repository automation surfaces | Mandatory proof is healthy but slow and not part of a repository-wide automated check. |
| knowledge | secondary | module docstring, `SKILL.md`, spec topology section, smoke records | Runtime behavior is documented deeply; acceptable modular topology and compatibility policy are not settled. |

## Evidence Trail

### E-CH-1: One file owns every mechanical domain

- Anchor: `wc -l -c skills/deliberate/scripts/deliberate-validate.py` returned 10,667 lines and 411,406 bytes; the module contract enumerates parsing, rendering, validation, store writes, identity, rendering checks, and fixtures at `deliberate-validate.py:6-34`; the CLI registers twelve commands at `deliberate-validate.py:10434-10645`.
- Category: code-health.
- Observation: the script contains 150 top-level functions and eight classes across parsing/read authorization, contract loading, identity, state storage, envelope validation, rendering, store commands, capsule validation, capsule import, generated-rendering checks, fixtures, and CLI dispatch.
- Present Cost: a maintainer must search and review a 411 KB surface for changes to any one command, and the same file changes for contract, runtime, recovery, and test corrections.
- Corroboration: evidence_corroborated.
- Source Notes: file metrics, AST inventory, module docstring, CLI parser, and section headers agree on the concentration.
- Promoted Finding: CH-1.

### E-CH-2: Complexity is concentrated in contract-critical paths

- Anchor: `uv run ruff check --select C901 --output-format concise skills/deliberate/scripts/deliberate-validate.py` reported 22 over-threshold functions; AST measurement found 13 definitions at least 100 lines, six at least 200, and two at least 500 (counting top-level definitions only; the 135 functions nested inside `cmd_fixtures` are excluded).
- Category: code-health.
- Observation: the largest production functions are `import_capsule_into_store` (563 lines, 79 Ruff complexity), `validate_capsule_document` (382 lines, 61), `validate_contract_data` (318 lines, 49), `_render_packet_item` (203 lines, 39), and `_validate_capsule_terminal_state` (195 lines, 45). The full ordinary Ruff check still passes because complexity is not selected by the repository's default invocation.
- Present Cost: high-risk changes require reasoning across many conditional branches in a single frame, and a green default lint run does not expose that risk.
- Corroboration: evidence_corroborated.
- Source Notes: independent AST size/branch counts and Ruff C901 agree; complexity is not itself a bug, so the finding is about change cost in contract-critical orchestration.
- Promoted Finding: CH-2.

### E-TD-1: The fixture harness dominates the source file

- Anchor: the static section partition assigns `deliberate-validate.py:5830-10429` to fixtures (4,600 lines, 43.1% of the file, including separators); `cmd_fixtures` alone spans `:6311-10426` (4,116 lines) and contains 135 nested functions; only four fixture documents exist under `scripts/fixtures/`.
- Category: test-debt.
- Observation: 153 `_expect` call sites plus parameterized paths produce 158 cases inside one function, including unit-like parser checks, store integration checks, CLI subprocess checks, fault injection, capsule round trips, import recovery, and contract drift checks.
- Present Cost: production navigation and fixture review are inseparable, test failures route through one custom result accumulator, and moving any internal symbol lacks an independent public-boundary control.
- Corroboration: evidence_corroborated.
- Source Notes: source layout, nested-function inventory, fixture file inventory, and live fixture output support the finding.
- Promoted Finding: TD-1 and TD-2.

### E-TD-2: The suite is healthy but is the only behavioral safety net

- Anchor: `/usr/bin/time -p uv run --script scripts/deliberate-validate.py fixtures --data references/contract-data.yaml` passed 158/158 in 51.54 real seconds; `check-renderings` passed; the repository has no `.github/` workflow and `scripts/check-library-integrity.sh` checks skill structure/delivery rather than executing the deliberate helper.
- Category: test-debt.
- Observation: the current suite has strong must-pass/must-block breadth, but there is no separate test runner, coverage signal, or black-box compatibility suite outside the executable under refactor.
- Present Cost: a structural edit can make implementation-coupled fixtures green while changing CLI text, exit mapping, store artifacts, or import behavior that external callers depend on; every deliberate session also pays the full fixture runtime when the helper is untested that session.
- Corroboration: evidence_corroborated.
- Source Notes: live commands, repository automation inventory, `SKILL.md:39`, and `deliberate-validate.py:10414-10425` corroborate the current proof shape.
- Promoted Finding: TD-1 and OP-1.

### E-AD-1: Method authentication binds the current single-file topology

- Anchor: `contract-data.yaml:47-54` fixes the exact method-surface inventory with only `scripts/deliberate-validate.py`; `_check_method_pin_inventory` calls `_check_pin_list(... allow_manifest=False)` and rejects missing or unexpected surfaces at `deliberate-validate.py:1286-1319`; capsule validation applies that exact check at `:4261`; `SKILL.md:39,87-90` requires platform hashing the script and running its fixtures.
- Category: architecture-drift.
- Observation: imported production modules would execute behavior that the current platform hash and method-identity capsule member do not authenticate. Adding module files to the canonical inventory changes the exact set old capsules carry, so current capsule validation would reject them before a re-run could classify ordinary method drift.
- Present Cost: the obvious monolith repair is not behavior-preserving under the live contract; planning must account for authentication and capsule continuity before moving code.
- Corroboration: evidence_corroborated.
- Source Notes: the old-capsule consequence is an inference from exact-set validation at `:1286-1319` and its unconditional capsule call at `:4261`; no saved-capsule inventory was performed.
- Promoted Finding: SY-1.

### E-AD-2: The current sections are real seams, but state and validation cross them heavily

- Anchor: AST section mapping found 134 calls from run-state code into shared errors/read authorization, 41 calls from capsule validation into envelope helpers, 33 from capsule validation into run-state helpers, 25 from rendering into envelope/state-derived helpers, and `Store.write` directly invokes envelope and capsule validation at `deliberate-validate.py:872-1014`.
- Category: architecture-drift.
- Observation: parsing, pure shape validation, state derivation, persistence, and command I/O are not cleanly layered; the store is both persistence adapter and workflow coordinator.
- Present Cost: moving a section wholesale is likely to create import cycles or copied helpers, while tests must construct broad state even for narrow validation behavior.
- Corroboration: evidence_corroborated.
- Source Notes: static call-graph counts and direct source inspection agree; dynamic runtime coupling was not instrumented.
- Promoted Finding: AD-1.

### E-OP-1: Proof latency is visible and contract-bound

- Anchor: the fresh full fixture run completed in 51.54 seconds; `SKILL.md:39` requires fixtures when the helper is untested in the session; the same script rereads and reparses store items through `Store.items()` and repeated `find`/`require` calls at `deliberate-validate.py:830-1014`.
- Category: operational.
- Observation: the proof suite is not merely CI cost; it is invocation preflight. Its breadth is load-bearing, so a fast/slow split would change the trust contract unless the fast layer proves the same required property.
- Present Cost: users and agents wait nearly a minute before a fresh deliberation can spend, and maintainers wait the same amount for every complete local proof run.
- Corroboration: evidence_corroborated.
- Source Notes: timing plus the live preflight obligation support the cost; this scan did not isolate which fixtures or store reads dominate.
- Promoted Finding: OP-1.

### E-DP-1: Single-script dependency shape is a constraint, not current debt

- Anchor: `deliberate-validate.py:1-5` declares Python 3.11+ and one PEP 723 dependency, `pyyaml`; ordinary Ruff, renderings, and fixtures all pass under `uv run --script`.
- Category: dependency.
- Observation: no unused dependency, skew, lock drift, or compatibility failure was found in the target.
- Present Cost: none promoted; adding package/build machinery solely to split files could create new delivery cost.
- Corroboration: evidence_corroborated.
- Source Notes: dependency sentinel only; security-vulnerability analysis was excluded.
- Promoted Finding: none.

### E-KN-1: Runtime rules are deep, but modular compatibility is unspecified

- Anchor: `docs/specs/2026-07-13-deliberate.md:176-180,331` specifies one shared helper, self-hash bootstrap, exact state authority, and bundle topology; the module docstring and section headers describe responsibilities, but no live artifact defines an acceptable authenticated multi-file topology or prior-capsule behavior after a method-surface expansion.
- Category: knowledge.
- Observation: the missing knowledge is not general documentation; it is the exact compatibility decision required by the requested refactor.
- Present Cost: an implementation plan cannot honestly claim behavior preservation until that choice is explicit.
- Corroboration: evidence_corroborated.
- Source Notes: merged into SY-1 rather than promoted separately.
- Promoted Finding: SY-1.

## Ranked Backlog

### SY-1: Settle authenticated modularity and capsule continuity before a file split

- Severity: P1.
- Category: systemic.
- Subcategory: trust boundary and compatibility.
- Anchor: `contract-data.yaml:47-54`; `deliberate-validate.py:1286-1319,4261`; `SKILL.md:39,87-90`.
- Problem: ordinary imports would move behavior outside the authenticated surface, while expanding the exact surface set makes existing capsules fail current validation.
- Impact: a nominal cleanup can weaken bootstrap proof or break the recovery product the skill promises.
- Recommendation: specify and prove one authenticated multi-file design that preserves the public entrypoint and explicitly defines prior-capsule behavior. If it changes the method-identity shape, contract-data version, capsule acceptance, or migration policy, classify that work as contract evolution rather than behavior-preserving simplification.
- Revision (2026-07-15): the compatibility branch is collapsed — pre-topology capsules are declared unsupported (no legacy population found; see Revisions). The open question is authentication topology only: direct per-file inclusion in `method-surfaces` versus an aggregate identity. P1 preserved until that choice is confirmed; its concrete delta then gets a `contract-change-propagation` pass before CH-1.
- Effort: medium.
- Leverage: high.
- Confidence: high.
- Corroboration: evidence_corroborated.
- Evidence Sources: canonical contract data, validator enforcement code, capsule validation path, skill contract, design spec.
- Cross Link: CH-1, TD-2.

### TD-1: Add an independent black-box characterization harness

- Severity: P1.
- Category: test-debt.
- Subcategory: refactor safety and external contract coverage.
- Anchor: `deliberate-validate.py:10434-10645`; live 158/158 fixture result; absence of a separate runner.
- Problem: the only behavioral suite lives inside the implementation being reorganized and primarily calls internal functions.
- Impact: structural movement lacks an independent detector for CLI, exit-code, stdout/stderr, file-layout, and cross-process behavior changes.
- Recommendation: add an out-of-process suite around the unchanged script, covering all command help surfaces and representative pass/refuse/fail/store-read paths, exact observable messages where contractual, store file names and sequence, capsule import/validation round trips, and the current fixture summary. Do not delete or relocate embedded fixtures in this slice.
- Revision (2026-07-15): un-gated — the harness is test-only and outside the runtime method-surface inventory, so it starts immediately, before SY-1, through `characterization-tests`. Include the mandatory deliberate-mutation proof: mutate production code, observe the net fail, restore, rerun green. The pass criterion is detection of representative public-seam mutations with the embedded 158-case suite as control, never a claim of full behavioral coverage.
- Effort: medium.
- Leverage: high.
- Confidence: high.
- Corroboration: evidence_corroborated.
- Evidence Sources: CLI parser, custom fixture harness, live fixture run, repository automation inventory.
- Cross Link: TD-2, SY-1, CH-1.

### CH-1: Decompose by behavioral domain while keeping one stable CLI entrypoint

- Severity: P1.
- Category: code-health.
- Subcategory: size, responsibility concentration, and review surface.
- Anchor: 10,667-line/411 KB file; section inventory; twelve command handlers; 12,891 lines of two-day churn.
- Problem: parsing, authority enforcement, state persistence, stage validation, rendering, capsule logic, resume logic, generated renderings, fixtures, and CLI registration change in one file.
- Impact: reviews are larger, ownership is unclear, and defects in one lane are harder to isolate from adjacent trust machinery.
- Recommendation: after SY-1 and TD-1, retain `scripts/deliberate-validate.py` as the stable command carrier and separate implementation around the existing domains: shared errors/read authorization/YAML, contract model, identity, run-state persistence, envelope validation, packet rendering, capsule validation, capsule import/restart, rendering generation, and fixtures. Move one coherent domain per change and preserve CLI/output/store behavior with black-box proof plus the full fixture suite.
- Effort: large.
- Leverage: high.
- Confidence: high.
- Corroboration: evidence_corroborated.
- Evidence Sources: file metrics, AST section inventory, module docstring, CLI parser, git churn.
- Cross Link: SY-1, TD-1, AD-1.

### CH-2: Split complex orchestrators into pure phase helpers before physical modules

- Severity: P1.
- Category: code-health.
- Subcategory: cyclomatic complexity and local reasoning cost.
- Anchor: Ruff C901 findings for 22 functions; largest production functions at `deliberate-validate.py:251,3117,3907,4159,5012`.
- Problem: contract validation, packet rendering, terminal-state validation, capsule validation, and capsule import each combine normalization, shape validation, cross-field policy, state derivation, and effects.
- Impact: small behavior changes touch dense branch sets and are difficult to verify at function grain.
- Recommendation: use the existing file as the first behavior-preserving simplification surface: extract table/registry-driven contract checks, per-packet renderers, capsule subvalidators, import normalization, restart-plan derivation, and atomic publication into named pure helpers without changing paths, CLI, schema, output, or method-surface identity. Require TD-1 plus 158/158 fixtures for each slice.
- Effort: medium.
- Leverage: high.
- Confidence: high.
- Corroboration: evidence_corroborated.
- Evidence Sources: Ruff complexity output, AST line/branch counts, source inspection, commit history.
- Cross Link: CH-1, AD-1.

### TD-2: Separate fixture organization from production navigation

- Severity: P1.
- Category: test-debt.
- Subcategory: test architecture and fixture ownership.
- Anchor: `deliberate-validate.py:5830-10429`; four external YAML fixtures; 153 `_expect` call sites and 158 live cases.
- Problem: parser checks, domain validations, integrated stores, fault injection, CLI alias tests, capsule round trips, and import state tests are nested inside one command function.
- Impact: the production file remains dominated by test code, failures lack domain-level test ownership, and fixture reuse requires reaching into a large local-function scope.
- Recommendation: once SY-1 defines how behavior-bearing fixture code is authenticated, organize the suite by contract domain and preserve the existing `fixtures` command, names, expected outcomes, aggregate summary, and nonzero behavior. Keep must-pass/must-block data external where declarative fixtures improve reviewability; keep fault-injection logic in focused test helpers.
- Effort: medium.
- Leverage: high.
- Confidence: high.
- Corroboration: evidence_corroborated.
- Evidence Sources: source layout, nested definition inventory, external fixture inventory, live fixture output.
- Cross Link: TD-1, SY-1, OP-1.

### OP-1: Reduce mandatory fixture latency without weakening the preflight claim

- Severity: P2 (downgraded from P1, 2026-07-15 revision: the latency is material but carries no trust or recovery consequence comparable to SY-1).
- Category: operational.
- Subcategory: local proof latency.
- Anchor: 51.54-second fresh fixture run; `SKILL.md:39`; repeated store parsing at `deliberate-validate.py:830-1014`.
- Problem: every untested session pays a full-suite delay, and the suite repeatedly exercises state reads through a persistence abstraction that reparses files on demand.
- Impact: nearly a minute of setup latency per fresh deliberate session and per complete maintainer check.
- Recommendation: profile the unmodified baseline, then optimize only proven hot paths such as per-process immutable store snapshots with explicit invalidation on writes or redundant fixture setup. Preserve all 158 names/outcomes and the full-suite preflight obligation unless a separately approved trust-contract change proves an equivalent cheaper gate.
- Effort: medium.
- Leverage: medium.
- Confidence: medium.
- Corroboration: evidence_corroborated.
- Evidence Sources: live timing, preflight contract, Store implementation, fixture architecture.
- Cross Link: TD-2, AD-1.
- Next Probe: capture per-test or per-call timing before choosing a performance repair.

### AD-1: Separate pure validation from persistence orchestration

- Severity: P2.
- Category: architecture-drift.
- Subcategory: coupling and test seams.
- Anchor: `Store.write` at `deliberate-validate.py:872-1014`; AST cross-section call graph; capsule/store cross-calls.
- Problem: persistence methods invoke domain validators, while renderers, validators, import logic, and fixtures reach back through mutable store queries.
- Impact: domain extraction risks cycles and narrow tests require broad store construction.
- Recommendation: introduce explicit pure inputs/results at the existing boundaries before module movement: parsed contract, immutable run-state snapshot, validated envelope/capsule result, and publication request. Keep filesystem effects in the store/command layer and preserve fail-fast order.
- Effort: medium.
- Leverage: high.
- Confidence: medium.
- Corroboration: evidence_corroborated.
- Evidence Sources: Store source, static cross-section calls, fixture setup patterns.
- Cross Link: CH-2, CH-1.

## Quick Wins

- None found. A small-fix pass considered moving `build_parser`, fixtures, or low-level helpers first, but each either leaves the real concentration untouched or creates an unauthenticated imported behavior surface. The smallest credible high-leverage action is TD-1, estimated medium rather than small.

## High-Leverage Fixes

- SY-1, TD-1, CH-1, CH-2, TD-2, and AD-1.

## Strategic Items

- CH-1 is the one large P1 item: the eventual domain decomposition.

## Watch List

- AD-1 remains P2 until a concrete extraction demonstrates that store/validation coupling blocks progress; avoid building a generalized repository abstraction without that evidence.
- Dependency shape is intentionally small and portable. Do not introduce packaging, generation, or a new runtime dependency merely to make the source tree look modular.
- The 214-line `build_parser` function is long but low-complexity declarative wiring; it is not an early target unless black-box CLI tests expose a maintenance cost.

## Tradeoff Map

- Refactor/ship: immediate file splitting improves navigation, but the current method-authentication boundary makes it unsafe until SY-1 is resolved.
- Coverage/speed: the 52-second suite is costly, but its complete must-pass/must-block result is the current trust gate; optimize execution before considering coverage reduction.
- Local/strategic repair: CH-2 can reduce complexity within the current authenticated file, while CH-1 yields the larger readability gain only after the topology decision.
- Simplicity/portability: a multi-file package may improve source ownership but can add import, packaging, or generation machinery to a deliberately portable PEP 723 command.

## Coverage Gaps / Next Probes

- Inventory whether any user-valued capsules minted under the current seven-surface method identity must remain importable; the answer materially changes SY-1.
- Compare authenticated topology options in a dedicated design pass: exact per-file method surfaces with explicit compatibility, a verified aggregate identity that transitively commits to modules, or a deliberately versioned capsule/migration boundary. This audit does not select one.
- Add TD-1 before measuring internal coverage; current fixtures may cover more public behavior than their in-file shape makes visible.
- Capture per-test/per-call timing before acting on OP-1; the 51.54-second total proves cost, not root cause.
- Re-run an exact Codex and Claude smoke after any physical topology change; fixtures and black-box CLI checks cannot prove runtime loading in both hosts.
- Security-vulnerability analysis, dependency CVEs, and exploitability were out of scope.

## Metrics

Local-run synthesis metadata, not durable proof and not audit evidence — the findings' warrant is the Evidence Trail, not these counts.

- Raw Findings: 9.
- Canonical Findings: 7.
- Merged Clusters: 2 - method-identity plus missing compatibility policy became SY-1; fixture concentration plus runner absence were separated into TD-1/TD-2 without double-counting the same impact.
- Corroborated Count: 7.
- Singleton Count: 0.
- Contradictions: 1 - source modularity conflicts with the current single-file authentication/portability design.
- Skipped Categories: 0; dependency and operational received background sentinel checks.
- Quick Wins: 0; small-fix pass found no safe high-leverage small move.
- Strategic Items: 1.
- Tradeoffs: 4.

## Fidelity Check

- Anchors match evidence trail: yes - file lines, commands, AST metrics, and git metrics were re-read against live `61583d5`.
- Recommendations preserve evidence qualifiers: yes - the old-capsule effect is labeled as an inference and the performance root cause remains unproven.
- Top calls are corroborated with present cost: yes - each uses at least two source classes and names current review, runtime, or recovery cost.
- Coverage limits are visible in Result Brief: yes - the artifact is explicitly an audit/backlog, not an execution sequence.
- Status updated to complete only after final checks: yes - the final artifact diff, whitespace check, metrics, source anchors, and recommendation qualifiers were reviewed before this status change.

## Revisions

### 2026-07-15: post-audit adjudication (repo head `59b4015`; audited validator byte-identical to `61583d5`)

An independent verification pass re-ran every quantitative anchor against the live tree; all reproduced. The following adjudicated changes were applied in place (marked `Revision (2026-07-15)` in the affected entries) and are recorded here with their evidence.

- Verification upgrade: the old-capsule consequence in E-AD-1/SY-1 is code-confirmed, no longer inferential. Every capsule-validating command loads the current contract (`load_contract(Path(args.data), ...)`), and `_check_method_pin_inventory` (`deliberate-validate.py:1286-1319`, called unconditionally at `:4261`) requires the capsule's method-identity to match the current canonical surface set exactly. Expanding `method-surfaces` therefore rejects every capsule carrying the current seven-surface inventory — factual.
- Scope correction: not every contract-data change orphans capsules. `contract-data-version == 5` (`deliberate-validate.py:269`) versions the contract-data document the helper accepts; capsules do not carry it as their compatibility discriminator, so a version bump alone neither rejects nor migrates old capsules. Changed method-pin identifiers are deliberate drift handling, converted into restart frontiers by `_pin_change_frontiers` (`deliberate-validate.py:4920`), and the v27 brief-only edit (`61583d5`) changed `contract-data.yaml` without a version or schema change. Set expansion, bounds, schema, and tightened-value changes do break capsules; identifier drift and value-neutral text edits do not.
- Compatibility branch collapsed: no `deliberate-run-live/` store exists in the current temporary roots or the repository, the smoke record carries no durable full capsule, and v26 (`docs/specs/2026-07-13-deliberate.md:55`) set the hard-rejection-without-migration precedent when no legacy population exists. Pre-topology capsules are declared unsupported for this refactor. Pasted capsules outside the visible workspace remain the one unreachable consumer class and are accepted as lost unless one surfaces.
- SY-1 narrows to its topology branch: how imported implementation files enter authentication. Working lean: direct per-file inclusion in `method-surfaces`, extending the mechanism already present rather than introducing aggregate-manifest machinery. P1 preserved until the choice is confirmed; the concrete delta then gets a `contract-change-propagation` pass before CH-1.
- TD-1 un-gated: starts immediately via `characterization-tests` with the mandatory deliberate-mutation proof; "proves equivalent coverage" replaced with the bounded detection claim in Do First and TD-1.
- OP-1 downgraded P1 → P2.
- Corrections applied in place: method-surface anchor is `contract-data.yaml:47-54` (was 45-54); the E-CH-2 complexity distribution now states it counts top-level definitions and excludes the 135 nested fixture functions.
