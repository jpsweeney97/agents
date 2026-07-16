# Behavior Smoke Test — `deliberate` end-to-end (Claude/sonnet stage agents): first live fire on the v6 eight-surface topology, accepted close capsule

- **Date:** 2026-07-16
- **Target:** the `deliberate` skill bundle (`skills/deliberate/`) on the v6 module topology — the Claude half of Task 7 of `docs/plans/2026-07-16-deliberate-v6-shared-module-extraction.md` (the debt-scan bar: fixtures and black-box CLI checks cannot prove runtime loading in both hosts; only a live exact-prompt fire can).
- **Skill source at test:** branch `feature/deliberate-v6-shared-module`, HEAD `627180282c1d8ea029b5d68fb60ad8f1e387dd31`, clean tree before, during (per-stage), and after. `contract-data-version` 6. Entrypoint `deliberate-validate.py` SHA-256 `a7f5ba33140001004587155d76f695409790d933e2dca40cbd3bef3057135013`; shared module `_deliberate_shared.py` SHA-256 `a7da9a453b69bc66e9d645b4221c0675ed33cbb8d71b873579c4ca798d0f318d`. 159/159 fixtures green at orchestrator preflight.
- **Input identity:** the exact 3,760-byte `$deliberate` prompt at `docs/smoke-tests/fixtures/2026-07-14-deliberate-exact-prompt.txt`, SHA-256 `253f1bfe697124f685124f03adb539f5f55005284cb4f107de598b2272493a82`, verified independently by operator and orchestrator before the run.
- **Effective interpreter:** CPython 3.13.12 (`main, Mar 10 2026, Clang 21.1.4`) selected by `uv 0.10.11` for the helper's PEP 723 header (`requires-python = ">=3.11"`, `dependencies = ["pyyaml"]`), probed via `uv run --script` from the session scratchpad; macOS 26.5.2. Same bounded environment as the Task-6 dual-path record.
- **Harness:** same relay shape as `2026-07-15_deliberate-recommend-enum-fix-and-success-capsule.md`. A fresh background orchestrator ran the contract with the fixture verbatim as its invocation, using the served path `~/.claude/skills/deliberate` (the Claude delivery symlink) as skill root; at each stage dispatch it wrote the rendered brief bytes to a relay dir and paused; the operator (top-level session) ran one fresh, non-forked **sonnet** stage agent per stage on the exact brief bytes, with the envelope returned by file, byte-exact. All five stage agents were spawned with an explicit sonnet override and self-reported `claude-sonnet-5` in their envelope `model` fields. The orchestrator's own model self-report was ambiguous (its harness header named `claude-fable-5` while its environment block named `claude-opus-4-8[1m]`) and is recorded unresolved in the capsule — immaterial to the verdict, as stage-agent serialization is the sensitive surface and that was sonnet, as in the prior record.
- **Headline:** the first live end-to-end fire on the v6 eight-surface topology **passes on Claude Code**: all five stages accepted mechanically, close rendered, store-backed capsule validation accepted, and the capsule independently re-validated storelessly by the operator. The v6 runtime boundary executed live on every helper invocation through the served symlink path, and — unplanned — refused a real seeded `scripts/__pycache__` with exit 2 before any store existed.

---

## Run — all five stages accepted, close rendered

Every stage returned `envelope valid … status=completed … 0 concerns amendment(s)` from `validate-envelope --accept`; brief identifiers were recorded in the store before each dispatch, and the operator independently re-hashed all five relay brief files after the run — every SHA-256 matched its recorded brief-id.

- **Generate** (brief `df646ae6…`, store seq4): field of 15 options — the 8 user seeds preserved byte-exact plus 7 generated; no retrievals, no encounters; ideate constituent pin verified by the stage agent.
- **Prune** (brief `65540734…`, store seq6): 4 survivors + 11 exclusion records (8 fact-established constraint cuts, 3 budget-forced cuts disclosed as low-confidence sketch-depth); partition exactly conserved (4+11=15); survivors an order-preserving subsequence — the v26 wording-canonicalization discipline proven again, now on the v6 topology. The lean-blind Prune cut the user's leaned candidate (twelve interviews) on the observed-repeat-use constraint.
- **Shape** (brief `feba83d1…`, store seq8): rank-free comparison surface over 6 live questions for the 4 survivors; 4 recorded constraint-consequences, none cutting; two honest encounters (instruction-like evidence-boundary language; a withheld-class provenance span) both treated as data.
- **Recommend** (brief `c17854e9…`, store seq10): `check first` close; leans registered before the surface read (agent-first and user-visible both A, inferred from user-seed authorship, order treated as non-evaluative); 2 post-prune dominance disposition records with canonical `cut-basis` values — the v27 enum-legibility fix proven again. The survivor share carried an empty authority-note set: the user's visible lean rode out with the excluded candidate, so the judgment stage decided lean-blind.
- **Contest** (brief `72a50910…`, store seq12): detection-only against the close and 13 active records; the exclusion-check line names both live challenges — the user's excluded favorite ("Twelve structured interviews…", mandatory because a visible user preference rode an exclusion) and the manual-workaround instrumentation cut, named most worth contesting.

**Close:** `check first` — run a same-day budget-feasibility estimate against the $8,000 / six-engineer-week cap; if it clears, run A (five-team design-partner cohort, the user's own seed), else run C; B and D are dominance-excluded against C, each with a revive-if condition.

**Capsule:** `validate-capsule --store --accept` exit 0 — `capsule valid: run=smoke-v6-20260716 terminal='close rendered'`; `capsule-complete` digest `cdcb5505a6ecc28c1702b2fcb8b2328e5aa7cac55b4b9b8426a6f51bb9d99956`. Store (16 items, seq 0–15) retired to the local Trash after the carrier rendered; the fixed locator was confirmed empty afterward.

## Independent re-validation (operator; acceptance does not rest on the orchestrator's report)

- The operator extracted the fenced capsule from the run's `FINAL.txt` (66,876 bytes) and re-ran `validate-capsule` storelessly against the pinned contract through the repo path: `capsule valid: run=smoke-v6-20260716 terminal='close rendered'`, exit 0.
- Method identity in the capsule is exactly the eight v6 surfaces, resolved through the served path, and both script hashes equal the operator's own `shasum -a 256` of the served files.
- All 13 record `cut-basis` values are canonical enum members (8 `constraint`, 3 `survivor budget`, 2 `post-prune dominance`).
- Containment: `git status` porcelain empty and HEAD unchanged at every orchestrator per-stage check and at the operator's end-of-run check; no bytecode under `scripts/` at close.

## v6 runtime-boundary observations

- Every helper invocation of the run — preflight fixtures, `init-setup`, pin writes, `render-brief` ×5, `validate-envelope --accept` ×5, `record-proof-inputs`, `record-terminal`, `validate-capsule --store --accept`, plus the operator's storeless re-validation — executed the v6 two-pass pre-import census and external cache prefix live, through the served symlink path. This record is the Claude half of the live proof the v28 spec clause requires.
- Unplanned live negative probe: the orchestrator's out-of-band setup pre-check imported the shared module under plain `uv run` and wrote `scripts/__pycache__` into the repo tree; the census refused the first `init-setup` with exit 2 (`__pycache__` forbidden under `scripts/`) before any store existed. The orchestrator trashed the artifact, re-ran `init-setup` cleanly, and ran all later pre-checks under `PYTHONDONTWRITEBYTECODE=1`. This was a genuine (gitignored) write inside the repo working tree by the harness — a disclosed, remediated containment deviation by the orchestrator's own pre-check, and incidentally the first refusal of a real, non-test-seeded census hazard.

## Anomalies and residuals (disclosed, non-blocking)

- The orchestrator authored the setup document, proof-boundary body, and capsule by building dicts in Python with the helper's own dumper and pre-validating in-process (read-only imports of the validator's functions) before each single-shot CLI call; the authoritative gate remained the CLI, and every store-mutating helper call returned exit 0 on its single real attempt. The only nonzero helper exit of the run was the census refusal above, pre-spend.
- The shape stage agent left an identical draft copy of its envelope beside the relay file (harness debris outside the repo; no impact).
- The `uv run --script` launcher's inert `uv-*.lock` TMPDIR metadata remains outside the boundary claim per the plan; nothing anomalous was observed.

## Proof boundary and status

- This is the **Claude half of Task 7 only**. The Codex twin re-smoke on the same fixture is still owed; the v28 spec-lineage clause stays "To be verified by" until both smokes pass (Task 7 step 5 deliberately not performed).
- Evidence is bounded to macOS 26.5.2 + CPython 3.13.12 + uv 0.10.11 via `uv run --script`, sonnet stage agents, and this run's field; honest-exit constituent branches, drift terminals, and live capsule re-import remain unexercised on Claude.
- Re-run rather than trust this record after any contract edit or method-surface change.

## Durable artifacts

- The relay dir (briefs and envelopes), `FINAL.txt`, the extracted capsule, and the orchestrator's scratch build scripts live in a session scratchpad and are ephemeral; the durable proof is this record.
- Prior-topology proof lineage: `2026-07-15_deliberate-recommend-enum-fix-and-success-capsule.md` (v27, Claude), the 2026-07-14 Codex session rollout (v25), and the Task-6 structural record `2026-07-16_deliberate-v6-dual-path-runtime-boundary.md`.
