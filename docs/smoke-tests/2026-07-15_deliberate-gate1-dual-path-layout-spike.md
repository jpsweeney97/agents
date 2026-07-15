# Gate-1 Smoke — dual-path exact-layout spike (PASS); bytecode-cache hazard confirmed and mitigated

- **Date:** 2026-07-15
- **Target:** Gate 1 of [ADR-0001's Rollout Boundary](../adr/0001-authenticate-deliberate-modules-as-direct-method-surfaces.md) — the exact-layout dual-path import spike — plus the bytecode-cache claim tested as a hypothesis with its proposed mitigation, per JP's adjudicated protocol.
- **Repo state at test:** branch `chore/deliberate-gate1-layout-spike` off `321c024`; working tree clean before and after. Helper baseline SHA-256 `2bc357788c0644242c35123a277e1de7ebbf1ed956d8ca1c51338e35ad1ea6da` (matches the v27 hash recorded in the 2026-07-15 enum-fix smoke). All spike mutations were temporary and restored; this document is the only durable artifact.
- **Environment:** macOS (darwin 25.5.0), `uv 0.10.11`. Interpreters observed: CPython 3.11 (forms A/B/C) and CPython 3.13 (form D) — see Finding 2. Claude symlink verified: `readlink /Users/jp/.claude/skills/deliberate` → `/Users/jp/.agents/skills/deliberate`.
- **Headline:** **Gate 1 PASSES.** Sibling-module import through the PEP 723 entrypoint, including module-to-module import, resolves the canonical module identically through the in-place path and the Claude symlink path, with byte-identical exit/stdout/stderr on the gate-named forms. The bytecode-cache hypothesis is **confirmed** (a header-matching stale `.pyc` executed instead of edited source, silently) and the session-temp `sys.pycache_prefix` mitigation is **proven** (identical behavior, zero repo-local bytecode created or read).

## Selected smoke command and invocation forms

Selected smoke command: `identity --data <DATA> /Users/jp/.agents/skills/deliberate/SKILL.md` (single-file read, no cwd-relative resolution beyond `--data`, deterministic stdout). All runs used `uv run -q --script` with `LANG=C LC_ALL=C NO_COLOR=1 UV_NO_PROGRESS=1`.

| Form | cwd | Script argument | `--data` argument |
| --- | --- | --- | --- |
| A (gate-named: canonical in-place) | `/Users/jp/.agents/skills/deliberate` | `scripts/deliberate-validate.py` | `references/contract-data.yaml` |
| B (gate-named: Claude symlink) | `/Users/jp/.claude/skills/deliberate` | `scripts/deliberate-validate.py` | `references/contract-data.yaml` |
| C (extra: absolute canonical, TD-1 form) | `/Users/jp/.agents` | `/Users/jp/.agents/skills/deliberate/scripts/deliberate-validate.py` | absolute canonical |
| D (extra: absolute through symlink) | `/Users/jp/.agents` | `/Users/jp/.claude/skills/deliberate/scripts/deliberate-validate.py` | absolute symlink |

Runner: each form's exit status, stdout, and stderr were captured to files and compared with `cmp`; stream identities below are SHA-256 prefixes of the captured files. The exact runner script is reproduced at the end of this document.

## Temporary mutations (asserted before trusting any result)

Spike modules (untracked, trashed at cleanup): `scripts/_layout_spike.py` (`MARK = "AAAA"`, imports `_layout_spike_dep`, re-exports `DEP_MARK`/`DEP_FILE`) and `scripts/_layout_spike_dep.py` (`DEP_MARK = "DEPA"`). Mutation 1 inserted after the entrypoint's `import yaml` (asserted: `git diff --stat` = 12 insertions, marker grep = 1, `git status` showed the modified validator plus two untracked spike files):

```python
import _layout_spike

print(
    "layout-spike:"
    + " module=" + os.path.realpath(_layout_spike.__file__)
    + " dep=" + os.path.realpath(_layout_spike.DEP_FILE)
    + " mark=" + _layout_spike.MARK + _layout_spike.DEP_MARK
    + " python=%d.%d" % (sys.version_info.major, sys.version_info.minor)
    + " pycache_prefix=" + repr(sys.pycache_prefix),
    file=sys.stderr,
)
```

Mutation 2 (Pass 2 only; asserted: `git diff --stat` = 14 insertions, grep = 1) inserted immediately before `import _layout_spike`:

```python
sys.pycache_prefix = "<session-scratchpad>/gate1/pyc-prefix"
```

The mutated validator was live in the served tree for a few minutes; no deliberate run was in flight during the window.

## Pass 0 — baseline (unmutated validator)

All four forms: exit 0, stdout SHA `074fb8ca0a45` (the `identities:` YAML for SKILL.md, `total-bytes: 16288`), stderr empty (`e3b0c44298fc` = SHA-256 of empty). Cache snapshot found 4 pre-existing `.pyc` files — see Finding 3.

## Pass 1 — unmitigated exact-layout probe

| Form | Exit | stdout SHA | stderr SHA |
| --- | --- | --- | --- |
| A | 0 | `074fb8ca0a45` | `c9f483a4109c` |
| B | 0 | `074fb8ca0a45` | `c9f483a4109c` |
| C | 0 | `074fb8ca0a45` | `c9f483a4109c` |
| D | 0 | `074fb8ca0a45` | `a0e05ed77abf` (differs; see Finding 2) |

Form A/B/C stderr, verbatim: `layout-spike: module=/Users/jp/.agents/skills/deliberate/scripts/_layout_spike.py dep=/Users/jp/.agents/skills/deliberate/scripts/_layout_spike_dep.py mark=AAAADEPA python=3.11 pycache_prefix=None`. Form D printed the identical line except `python=3.13` (stderr SHA `a0e05ed77abf`).

**Finding 1 — Gate 1 criteria met.** Both gate-named forms (A, B) resolved the intended canonical module and dependency and returned byte-identical exit status, stdout, and stderr. Module-to-module import (`_layout_spike` → `_layout_spike_dep`) resolved canonically. The extra absolute forms (C, D) also resolved canonically.

**Finding 2 — interpreter selection varies by invocation form.** uv selected CPython 3.11 for forms A/B/C and CPython 3.13 for form D (absolute path through the symlink), producing bytecode cache entries for both versions in one pass. Not a gate failure (resolution and semantics were identical), but a v6 design input: the PEP 723 header pins only `>=3.11`, so per-path interpreter variance is possible and multi-version cache accumulation is real.

**Finding 3 — cache behavior.** Pass 1 wrote exactly four new files: `scripts/__pycache__/_layout_spike.cpython-{311,313}.pyc` and `_layout_spike_dep.cpython-{311,313}.pyc`. These are invisible to `git status` because `.gitignore:5` (`__pycache__/`) already ignores them — muting the untracked-dirt and git-visible-containment concerns from the scrutiny addendum, but leaving the read hazard live. Separately, `scripts/__pycache__/` **already contained** compiled bytecode of the production validator itself (`deliberate-validate.cpython-{311,313,314}.pyc`, mtimes 2026-07-14 18:40:54, 2026-07-15 18:11:19, 2026-07-15 12:11:31), plus a pytest cache under `tests/__pycache__/`. Origin probe: after trashing the cpython-313 entrypoint pyc, a fresh form-D run (python=3.13) did **not** regenerate it — `uv run --script` does not byte-compile the entrypoint; only *imported modules* are compiled by ordinary runs. The entrypoint bytecode came from some external tool (origin undetermined) and was removed at cleanup as a stale derived artifact of exactly the hazard class Finding 4 confirms.

## Pass 1b — bytecode-cache hypothesis test

Protocol: record the spike module's pyc and source identities, rewrite the source in place with a same-length change (`AAAA` → `BBBB`), restore `st_mtime_ns` exactly via `os.utime`, rerun form A.

- Source SHA-256 (16-hex prefix): `25f67b484a93b27c` → `f7fa263cc36d4f35`; size 360 bytes both; `st_mtime_ns` 1784158637965123515 preserved (asserted).
- Pyc SHA-256 unchanged before/after the run: `5b15f6c57221e4a3…`.
- Run result: exit 0, stderr printed **`mark=AAAADEPA`** while the source on disk contained `MARK = "BBBB"` (grep asserted = 1).

**Finding 4 — CONFIRMED.** CPython executed the stale, header-matching bytecode instead of the edited source, silently. Consequence for v6: platform-hashing `.py` sources does not authenticate the code Python actually executes when a repo-local `__pycache__` entry with a matching (mtime, size) header exists. Note: write-suppression (`PYTHONDONTWRITEBYTECODE`) does not prevent *reading* an existing cache per documented CPython semantics; that flag was not separately tested here.

## Pass 2 — session-temp `sys.pycache_prefix` mitigation

Repo-local `scripts/__pycache__/` was trashed first (clean slate, asserted absent). With Mutation 2 setting `sys.pycache_prefix` to a session-temp directory before the first first-party import:

| Form | Exit | stdout SHA | stderr SHA |
| --- | --- | --- | --- |
| A | 0 | `074fb8ca0a45` | `5dd79633019a` |
| B | 0 | `074fb8ca0a45` | `5dd79633019a` |
| C | 0 | `074fb8ca0a45` | `5dd79633019a` |
| D | 0 | `074fb8ca0a45` | `ff2f1ac9f755` (identical content except `python=3.13`) |

- Repo-local bytecode after the pass: **zero** files under `scripts/` (`find` count 0).
- Prefix populated with the four spike pycs, mirroring the **canonical** source path (`<prefix>/Users/jp/.agents/skills/deliberate/scripts/…`) for every form — including the symlink-path invocations. The loader therefore resolves the script path to canonical before import (uv canonicalizes; no duplicate cache identity per path).

**Finding 5 — mitigation PROVEN.** Behavior identical across paths (module resolution, marks, exit, stdout), no repo-local bytecode created, and nothing repo-local to read. `sys.pycache_prefix` set before the first first-party import is a workable v6 cache-neutralization mechanism; the production cut should derive the prefix from the runtime's session-temp root rather than this spike's hardcoded scratchpad path.

## Cleanup and restoration (all asserted)

`git restore skills/deliberate/scripts/deliberate-validate.py`; `trash` of `_layout_spike.py`, `_layout_spike_dep.py`, `scripts/__pycache__/` (including the pre-existing stale entrypoint bytecode, rationale in Finding 3), and the session pyc-prefix directory. Post-restore: helper SHA-256 back to baseline `2bc35778…` exactly; `git status` clean with zero diff; a full four-form rerun reproduced the Pass-0 baseline byte-exactly (stdout `074fb8ca0a45`, stderr empty, exit 0 on all forms); `find` reports zero cache files under `scripts/`. The pytest cache under `tests/__pycache__/` predates the spike and was left in place.

## Verdict and v6 carry-forward inputs

**Gate 1: PASS.** The direct-per-file layout is portable across both delivery paths as specified; the ADR-0001 hard-stop clause is not triggered and no root-cause investigation is needed.

Carry into the v6 cut as design inputs (deliberately *not* resolved here, per scope): (1) adopt cache neutralization in the v6 entrypoint — session-temp `sys.pycache_prefix` before any first-party import, per Finding 5 — so imported-module bytecode can neither pollute nor impersonate the authenticated sources; (2) decide whether v6 pins or records the interpreter minor version, given per-path selection variance (Finding 2); (3) module identity is single-homed at the canonical path even under symlink invocation (Pass 2), which the pinning design can rely on. Gate 2 (the non-executing import-closure check), the first coherent module choice, and frontier assignments remain separate v6-cut inputs.

## Reproduction

Runner script (paths session-specific only in the output directory):

```bash
#!/bin/zsh
set -euo pipefail
LABEL="$1"; BASE="<session-scratchpad>/gate1/$LABEL"
REPO="/Users/jp/.agents/skills/deliberate"
LINK="/Users/jp/.claude/skills/deliberate"
TARGET="/Users/jp/.agents/skills/deliberate/SKILL.md"
mkdir -p "$BASE"
export LANG=C LC_ALL=C NO_COLOR=1 UV_NO_PROGRESS=1
run_form() {
  local form="$1" dir="$2" script="$3" data="$4"; local rc=0
  ( cd "$dir" && uv run -q --script "$script" identity --data "$data" "$TARGET" ) \
    >"$BASE/$form.out" 2>"$BASE/$form.err" || rc=$?
  echo "$rc" >"$BASE/$form.exit"
}
run_form A "$REPO" "scripts/deliberate-validate.py" "references/contract-data.yaml"
run_form B "$LINK" "scripts/deliberate-validate.py" "references/contract-data.yaml"
run_form C "/Users/jp/.agents" "$REPO/scripts/deliberate-validate.py" "$REPO/references/contract-data.yaml"
run_form D "/Users/jp/.agents" "$LINK/scripts/deliberate-validate.py" "$LINK/references/contract-data.yaml"
for f in B C D; do cmp "$BASE/A.out" "$BASE/$f.out"; cmp "$BASE/A.err" "$BASE/$f.err" || true; done
```

Pass 1b mtime-preserving edit: read `st_mtime_ns`/`st_atime_ns` via `os.stat`, rewrite the same-length source bytes, then `os.utime(path, ns=(atime_ns, mtime_ns))`, asserting size and `st_mtime_ns` unchanged. Stream capture files were session-temporary; their SHA-256 prefixes are recorded in the tables above.
