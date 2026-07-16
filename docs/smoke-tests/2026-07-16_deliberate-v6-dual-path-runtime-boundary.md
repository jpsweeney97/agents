# v6 Smoke — dual-path runtime boundary (PASS); startup-latency delta flagged for JP

- **Date:** 2026-07-16
- **Target:** Task 6 of the [v6 shared-module extraction plan](../plans/2026-07-16-deliberate-v6-shared-module-extraction.md) — dual-path delivery evidence for the completed v6 cut (eight method surfaces, Gate-2 policy binding, runtime pre-import census, invocation-private external cache prefix), covering ADR-0001's "both delivery paths, interpreter recorded" obligation.
- **Repo state at test:** branch `feature/deliberate-v6-shared-module`, HEAD `ae911b644baa9fa4d51928e86d3b81830684fac6`, working tree clean. Claude symlink verified: `ls -la /Users/jp/.claude/skills/deliberate` → `lrwxr-xr-x@ 1 jp  staff  35 Jul 14 10:36 /Users/jp/.claude/skills/deliberate -> /Users/jp/.agents/skills/deliberate`.
- **Environment:** macOS 26.5.2 (`sw_vers -productVersion`), `uv 0.10.11 (006b56b12 2026-03-16)`. Effective interpreter observed: CPython 3.13.12 (section 3).
- **Headline:** **PASS on every gate.** Fixtures 159/159 with exit 0 through both delivery paths, identical identity-probe output and exit codes, Gate-2 agreement line verbatim-identical through both paths, one interpreter environment from both CWDs. Startup latency rose from a 0.14s baseline median to 0.25s — flagged for JP in section 4, not adjudicated here.

Every output below is the verbatim result of a command run this session on this machine; nothing is copied from expected values. `<A>` = `/Users/jp/.agents/skills/deliberate` (canonical in-place path); `<B>` = `/Users/jp/.claude/skills/deliberate` (Claude symlink path).

## 1. Both delivery paths, live tree — fixtures and identity

Fixtures, both paths: `uv run --script <path>/scripts/deliberate-validate.py fixtures --data <path>/references/contract-data.yaml`.

| Path | Tail line (verbatim) | Exit |
| --- | --- | --- |
| `<A>` | `159/159 fixtures behaved as required` | 0 |
| `<B>` | `159/159 fixtures behaved as required` | 0 |

Both runs printed the full PASS list (159 lines, every fixture `expected=… got=…` matching) preceded by two `proof inputs recorded: 003-proof-inputs.yaml` lines; the tail lines above are byte-identical across paths.

Derived-count correction: the plan's Task 6 text expects `158/158`, which is stale — v6's eighth method surface (`scripts/_deliberate_shared.py`) derives one additional embedded method-identity drift fixture (`method identity missing scripts/_deliberate_shared.py fails`, visible in both runs), so the true current count is 159/159, as adjudicated during Task 4.

Identity probe, both paths: `uv run --script <path>/scripts/deliberate-validate.py identity --data <path>/references/contract-data.yaml <path>/references/contract-data.yaml`.

Through `<A>`, exit 0:

```
identities:
- path: /Users/jp/.agents/skills/deliberate/references/contract-data.yaml
  id: 729691f17f353a47bbd23ca1f21f829f3f091db2d4dbdbe4e613b049f7f2dd52
total-bytes: 46986
```

Through `<B>`, exit 0:

```
identities:
- path: /Users/jp/.claude/skills/deliberate/references/contract-data.yaml
  id: 729691f17f353a47bbd23ca1f21f829f3f091db2d4dbdbe4e613b049f7f2dd52
total-bytes: 46986
```

Exit codes identical (0/0); content hash and byte count identical across paths; the `path:` echo differs only by the invocation spelling, as expected.

## 2. Gate-2 through both paths

`uv run --script <path>/tests/check_import_closure.py`, both paths. Verbatim output, identical for `<A>` and `<B>`, exit 0 both times:

```
import closure, on-disk production files, and method-surfaces agree: 2 Python surface(s)
```

## 3. Effective interpreter

Probe script written to the session scratchpad (not the repo), carrying the identical PEP 723 header the production entrypoint uses:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
import sys
print(sys.executable)
print(sys.version)
```

Run via `uv run --script` twice, exit 0 both times. With CWD `<A>` (first run; uv printed `Installed 1 package in 5ms` while creating the probe's environment):

```
/Users/jp/.cache/uv/environments-v2/interp-probe-519560b889592ae7/bin/python
3.13.12 (main, Mar 10 2026, 18:26:32) [Clang 21.1.4 ]
```

With CWD `<B>`:

```
/Users/jp/.cache/uv/environments-v2/interp-probe-519560b889592ae7/bin/python3
3.13.12 (main, Mar 10 2026, 18:26:32) [Clang 21.1.4 ]
```

Same uv environment (`interp-probe-519560b889592ae7`) and identical CPython 3.13.12 build from both CWDs; the `sys.executable` basename differs (`python` vs `python3`) within that one environment's `bin/`. No per-path interpreter-version variance observed in this run (contrast Gate-1's Finding 2, which saw 3.11 vs 3.13 across invocation forms).

## 4. Startup latency — before/after

Task 0 timing loop repeated verbatim from CWD `/Users/jp/.agents`:

```
for i in 1 2 3; do /usr/bin/time -p uv run --script skills/deliberate/scripts/deliberate-validate.py identity --data skills/deliberate/references/contract-data.yaml skills/deliberate/references/contract-data.yaml >/dev/null; done
```

Observed `real` values this run: `0.23`, `0.25`, `0.27`.

| Measurement | `real` values | Median |
| --- | --- | --- |
| Before (Task 0 baseline, this session, same machine, pre-v6) | 0.14, 0.14, 0.14 | 0.14 s |
| After (this run, v6 at `ae911b6`) | 0.23, 0.25, 0.27 | 0.25 s |

**FLAG for JP:** the after-median is materially above baseline (0.25 s vs 0.14 s, ≈1.8x). Causal note: the v6 entrypoint creates a fresh, invocation-private, never-reused external cache prefix per run (the ADR-0001 cache-neutralization mandate), so stdlib/pyyaml module bytecode is recompiled on every invocation by design. No pre-registered threshold exists; per the plan, this record flags the delta rather than judging it acceptable or unacceptable.

## 5. ADR obligation map

| ADR-0001 runtime obligation | Evidence |
| --- | --- |
| Seeded stale repo-local bytecode is ignored/refused | `test_seeded_pycache_directory_is_refused`, `test_seeded_sourceless_pyc_is_refused_without_executing` |
| Chosen prefix starts empty and outside the protected source root | `tempfile.mkdtemp` semantics + the external-success and unsafe-root branches of `test_cache_prefix_is_external_private_retired_and_unsafe_roots_refuse` |
| Second invocation cannot execute the first's cached code | `test_second_invocation_never_reuses_prior_bytecode` |
| No repo-local bytecode created or read | repo/bundle/`scripts/`/allowed-data/symlink/case-alias refusal branches of `test_cache_prefix_is_external_private_retired_and_unsafe_roots_refuse` + census `__pycache__` refusal |
| Seeded sourceless `.pyc` refused without executing | marker assertions in both `.pyc` tests |
| Both delivery paths, interpreter recorded | this smoke record, sections 1–3 |

All four named tests exist in `skills/deliberate/tests/test_runtime_boundary.py` (verified by definition grep this session).
