# Behavior Smoke Test — `deliberate` end to end (Codex stage agents): v6 eight-surface topology, accepted close capsule

- **Date:** 2026-07-16
- **Target:** the `deliberate` skill bundle (`skills/deliberate/`) on the v6 shared-module topology — the Codex half of Task 7 of `docs/plans/2026-07-16-deliberate-v6-shared-module-extraction.md`.
- **Skill source at test:** branch `feature/deliberate-v6-shared-module`, HEAD `dfa0a8438ad4ac2406e801f38c192916be683ff5`, clean tree before, between, and after every stage. `contract-data-version` 6. Entrypoint `deliberate-validate.py` SHA-256 `a7f5ba33140001004587155d76f695409790d933e2dca40cbd3bef3057135013`; shared module `_deliberate_shared.py` SHA-256 `a7da9a453b69bc66e9d645b4221c0675ed33cbb8d71b873579c4ca798d0f318d`. Preflight fixtures: 159/159 green.
- **Input identity:** the exact 3,760-byte fixture at `docs/smoke-tests/fixtures/2026-07-14-deliberate-exact-prompt.txt`, SHA-256 `253f1bfe697124f685124f03adb539f5f55005284cb4f107de598b2272493a82`. The setup parser's stored `invocation-wording-initial` was byte-compared with the fixture before the run.
- **Effective interpreter:** CPython 3.13.12 (`main, Mar 10 2026, Clang 21.1.4`) selected through uv 0.10.11 on macOS 26.5.2 (build 25F84).
- **Harness:** the live Codex source path was executed in place. The orchestrator rendered each complete stage brief through the pinned helper, recorded its content identifier before dispatch, wrote the exact bytes to a relay file, verified the relay hash, and launched one fresh non-forked Codex stage agent. Each returned envelope was accepted once through `validate-envelope --accept`; Git state and all 16 live pins were checked at the stage boundaries.
- **Headline:** the Task 7 Codex twin **passes**. Generate, Prune, Shape, Recommend, and Contest all completed and were mechanically accepted; the proof inputs and `close rendered` terminal were recorded; the 77,386-byte `deliberate-capsule/v1` carrier was accepted store-backed and independently revalidated storelessly; the live store was retired only after the carrier existed.

## Accepted run

- **Run:** `smoke-v6-codex-20260716-r2`.
- **Stages:** 5/5 completed and 5/5 accepted, with zero concerns amendments at every acceptance.
- **Field:** Generate returned 18 canonical options. Prune conserved the partition as 8 survivors plus 10 active exclusion records. Shape produced the complete comparison surface and constraint consequences. Recommend returned a `check first` close with no provisional seed. Contest returned a live-challenge line and named the truthful refundable-commitment cohort as most worth contesting.
- **Retrievals:** none. Decision evidence stayed inside the exact supplied fixture; no web research, project evidence, user files, or external probes were used.
- **Models:** Generate `unknown`; Prune `unknown`; Shape `GPT-5`; Recommend `unknown`; Contest `unknown`. Unknown means the stage runtime exposed no trustworthy effective-model identifier.
- **Capsule:** terminal `close rendered`; `capsule-complete` SHA-256 `97048af4bce2244835a1fb65bb726dd48d5fa902243f083c404716540121ea69`.
- **Validation:** the authoritative accepting call returned `capsule valid: run=smoke-v6-codex-20260716-r2 terminal='close rendered'`; a separate storeless call returned the same result.
- **Containment:** the branch remained at `dfa0a8438ad4ac2406e801f38c192916be683ff5` with empty porcelain throughout the runtime run. This proves net Git-visible containment only, not absence of side effects outside the worktree.

## Eight-surface method identity

| Surface | SHA-256 |
| --- | --- |
| `skills/deliberate/SKILL.md` | `aef975142846f166a13a19257ee54e2c92da039e515602162784d42acd3740f1` |
| `skills/deliberate/references/capsule.md` | `ae6948a5b17ea31d8583ce2ee925d3b191b51f01f70a648996cdbc5fdec83244` |
| `skills/deliberate/references/contract-data.yaml` | `729691f17f353a47bbd23ca1f21f829f3f091db2d4dbdbe4e613b049f7f2dd52` |
| `skills/deliberate/references/methods.md` | `7f0b25dd3d6fc774d387dab274cb0461f3e933e5987b415286c0ce3f16da79be` |
| `skills/deliberate/references/schemas.md` | `554aca6f6d20a5e494c489294dbe63774add6890150ef6edf2d5ba15a2b513dc` |
| `skills/deliberate/references/stage-packets.md` | `eef5c8f8bfbc0cfba00b627d727fdddf1b55b0d86ae18400d3137df2e19d352b` |
| `skills/deliberate/scripts/_deliberate_shared.py` | `a7da9a453b69bc66e9d645b4221c0675ed33cbb8d71b873579c4ca798d0f318d` |
| `skills/deliberate/scripts/deliberate-validate.py` | `a7f5ba33140001004587155d76f695409790d933e2dca40cbd3bef3057135013` |

## Harness anomaly and recovery

The interrupted first attempt had already accepted Generate through Recommend when its Contest brief exceeded the tool's initial output display budget. The operator incorrectly called `render-brief --stage contest` a second time to recover the bytes. The helper correctly refused the duplicate with exit 2 (`brief-render already recorded for stage contest`). The pinned fail-fast rule was honored: no later helper command ran in that attempt, a terminated non-resumable emergency receipt was rendered, and its store was retired. No result from that attempt was reused.

The accepted run started from a new store and fresh agents at Generate. It captured every relay with a sufficient output budget on the first render. This anomaly is a harness mistake and a positive observation of the singleton brief-render guard, not evidence against the v6 topology.

## Proof boundary and Task status

- Together with `2026-07-16_deliberate-v6-claude-end-to-end-re-smoke.md`, this supplies both exact-prompt live-runtime halves required by Task 7.
- The capsule proves typed store consistency, exact method and constituent identities, canonical option identity, partition conservation, recorded packet identifiers, and the declared terminal/artifact relationship. It does not prove semantic correctness, complete option coverage, undeclared-reliance absence, prompt-injection prevention, or side effects outside net Git-visible state.
- This commit records only the Codex smoke. The v28 lineage clause was not edited and Task 8 was not begun in this run-record commit.
- Re-run this smoke after any behavior-surface or physical-topology change.
