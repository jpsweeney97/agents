# Implementation Plan: deliberate v6 — `_deliberate_shared.py` extraction under a single-sourced import-boundary policy

**Date:** 2026-07-16 · **Branch:** `feature/deliberate-v6-shared-module` (created at planning time; the ADR/portfolio decision folds and this plan are its first commits) · **Executor:** `execute-plan` or a follow-up session working task-by-task.

## Governing sources (read before executing)

- `docs/adr/0001-authenticate-deliberate-modules-as-direct-method-surfaces.md` — the authentication model, both rollout gates, the five runtime obligations, and the 2026-07-16 amendment (policy placement in pinned `contract-data.yaml`; embedded-values runtime mechanism; single v6 cut).
- `docs/hardening/2026-07-16-deliberate-import-boundary/proposals/import-execution-boundary.md` — Option 2 (chosen), its validation plan and work packages, decided open questions.
- `docs/audits/2026-07-15-deliberate-validator-debt-scan.md` — drift-class rules (line ~327) and the cross-runtime smoke bar ("Re-run an exact Codex and Claude smoke after any physical topology change").
- `skills/deliberate/tests/check_import_closure.py` — the Gate-2 authoring checker whose census semantics the runtime preflight mirrors.

## Current state (verified 2026-07-16 at `43065ca`)

- `main` holds the landed Gate-2 arc; this branch adds the decision folds, this plan, and one Gate-2 repair (`43065ca`, below). Worktree clean; full suite 39 passed in ~62s; Gate-2 checker exit 0 with "agree: 1 Python surface(s)"; fixtures 158/158.
- `skills/deliberate/scripts/deliberate-validate.py` is the single production Python surface (10,667 lines); `contract-data-version: 5`; `validation.method-surfaces` has seven entries.
- The entrypoint has no first-party imports; `yaml` is used only inside the block this plan extracts (verified: zero `yaml.` references outside lines 59–233).

### Prerequisite landed on this branch (`43065ca`) — prefixed-ZIP Gate-2 repair

The 2026-07-16 execution-readiness scrutiny of this plan reproduced a live Gate-2 bypass: a structurally valid zip carrying an arbitrary prefix (a shell/self-extracting stub whose first four bytes are not `PK`) passed the checker green while zipimport still loaded a module from it, because the census sniffed only `handle.read(4)`. The fix replaced the four-byte magic sniff with `zipfile.is_zipfile`, which locates the trailing end-of-central-directory record the way zipimport does. A `test_prefixed_zip_archive_is_rejected` regression (mutation-proven: reverting to the sniff fails it) and a real-zip rewrite of `test_disguised_zip_archive_is_rejected` landed with it. **This plan's runtime preflight must carry the same structural detector, not the four-byte sniff** — reflected in Task 3 below, and the `zip-magics` policy value the earlier draft embedded is dropped everywhere (there is no magic list to compare; detection is structural).

## What this plan builds

One `contract-data-version` bump to 6 delivering, together: (a) a declarative `import-boundary` policy section in the pinned `references/contract-data.yaml`; (b) the Gate-2 authoring checker consuming that section directly; (c) a two-pass, stdlib-only pre-import census (layout rules first, then a `zipfile.is_zipfile` content check on the collected inert files once shadows are provably cleared) plus a fresh invocation-private `sys.pycache_prefix` that is mechanically kept outside the repository (or outside the served skill root when standalone), with unsafe ambient temp roots refused fail-closed, a release-time test asserting the embedded policy equals the contract section, and a per-invocation `_require_boundary_match` as defense-in-depth; (d) the first physical extraction, `scripts/_deliberate_shared.py` (error/refusal constructors, read authorization, safe-YAML foundation), entering `method-surfaces` at the default (Generate) frontier; (e) the companion doc, test, smoke, and spec updates.

Non-goals: no further module splits (CH-1 stays gated on this landing), no launcher/staged-root (Option 3), no broadening of the external `sys.path` residual (portfolio open question 4 stays open), no plugin publish, no push, no merge to `main` — landing is JP's call.

## File map

| Path | Change | Responsibility |
| --- | --- | --- |
| `skills/deliberate/references/contract-data.yaml` | modify | version 5→6; new top-level `import-boundary` section; `method-surfaces` gains `scripts/_deliberate_shared.py` |
| `skills/deliberate/scripts/deliberate-validate.py` | modify | embedded boundary policy + module-level pre-import census + fresh cache prefix verified outside the repository/standalone skill root; unsafe temp roots refuse; accepts/validates `import-boundary`; version gate 6; embedded-vs-contract comparison at every load; shared foundation removed, `from _deliberate_shared import …` added |
| `skills/deliberate/scripts/_deliberate_shared.py` | create | the extracted foundation: exceptions, `fail`/`refuse`, `ReadSet`, `_decode_utf8`, `safe_parse`, `_UniqueKeyLoader`, `_NoAliasDumper`, `dump_yaml`, `SAFE_TAGS` |
| `skills/deliberate/tests/check_import_closure.py` | modify | census/ban values loaded from the target root's `contract-data.yaml` `import-boundary` section (structural zip detection via `zipfile.is_zipfile` already landed in `43065ca`) |
| `skills/deliberate/tests/test_import_closure.py` | modify | `make_layout` writes the policy section; live-tree test expects 2 surfaces; policy-floor, policy-binding, and embedded-vs-contract-equality tests (prefixed-ZIP regression already landed in `43065ca`) |
| `skills/deliberate/tests/test_runtime_boundary.py` | create | out-of-process battery: contract tamper, seeded-artifact refusals (incl. prefixed-ZIP), benign passes, external prefix lifecycle + unsafe repo/bundle/scripts/allowed-data/symlink/case-alias temp-root refusals, bytecode-freshness probe, module-name grammar (predicate-vs-regex agreement) |
| `skills/deliberate/SKILL.md` | modify | bootstrap verification hashes both production files; orchestrator hashing bullet names imported modules |
| `skills/deliberate/references/capsule.md` | modify | method-identity prose includes the shared module |
| `docs/specs/2026-07-13-deliberate.md` | modify | Status v27→v28; v28 lineage entry |
| `docs/smoke-tests/2026-07-XX_deliberate-v6-dual-path-runtime-boundary.md` | create | dual-path evidence, effective interpreter, startup latency, obligation checklist |
| `docs/smoke-tests/fixtures/2026-07-14-deliberate-exact-prompt.txt` | exists (`43065ca`) | byte-exact 3,760-byte `$deliberate` smoke prompt, SHA-256 `253f1bfe…`; the durable, hash-pinned Task 7 input (README beside it records provenance) |

`skills/deliberate/tests/test_validator_cli_characterization.py` should need no edits: it derives method pins from the live contract at run time, pins `--help` output (no commands change), and pins the fixture summary (`158/158`, unchanged). If it fails at any task boundary, that is a regression to fix, not a test to update — with one exception noted in Task 1.

## Design invariants (do not violate while executing)

- The Gate-2 checker stays non-executing: `ast.parse` only, never importing production code.
- The runtime census enforces layout rules only. Closure/inventory equality stays an authoring-gate concern: a flat, conforming, uninventoried module is inert at runtime because production code contains no dynamic-import machinery and the orchestrator hashes every method surface. Do not add a YAML read or inventory comparison before first-party import.
- **Import ordering before first-party code (revised after the 2026-07-16 scrutiny).** Only `os` and `sys` are imported before the *layout* census (both initialized during CPython startup, so they cannot be shadowed from `scripts/`). The layout census enforces every structural rule using `os`/`sys` alone and *collects* the inert-suffix files for a content check. Once that pass returns without refusing, no `.py`/`.pyc`/`.so`/package/symlink shadow exists under `scripts/`, so only the narrow deferred stdlib set needed to create and retire a verified-external cache prefix and perform the structural archive check (`atexit`, `shutil`, `tempfile`, `zipfile`, and their stdlib dependencies) may import; first-party code and every other import wait until the zip-content pass has refused nothing. The zip-content check runs `zipfile.is_zipfile` on the collected inert files, matching the Gate-2 checker's detector exactly. This is what makes the seeded-`scripts/argparse.py` test pass and what carries the prefixed-ZIP repair (`43065ca`) into runtime.
- **Zip detection is structural in both consumers.** Neither the checker nor the runtime compares magic bytes; both call `zipfile.is_zipfile`, so a prefixed/self-extracting zip is caught and the two consumers cannot drift on zip detection. There is no `zip-magics` policy value.
- **The cache prefix is fresh *and* external.** ADR-0001 requires the prefix outside the repository, not merely outside `scripts/`. After pass 1, the entrypoint resolves the served source path through symlinks, scans every ancestor and selects the outermost containing Git root so an inner `.git` marker cannot narrow the protected tree (falling back to the served skill root when standalone), resolves the process temp root, and refuses before prefix creation if that temp root is inside the protected root. Containment walks resolved ancestors and compares filesystem identity with `os.path.samefile`, not path-string casing, so case aliases on the default macOS filesystem cannot bypass the check; an identity-check error is treated as unsafe. It creates the prefix beneath the approved resolved temp root, resolves and checks the created path again to close a temp-root symlink swap between selection and creation, and only then assigns `sys.pycache_prefix`. A repo-, bundle-, `scripts/`-, allowed-data-, symlink-resolved-, or case-aliased internal `TMPDIR` is an invocation refusal, not a supported placement; an ordinary external `TMPDIR` remains supported and the prefix is retired at exit.
- **The embedded-vs-contract match is authenticated at release time, not pre-import at runtime (ordering decision, 2026-07-16 scrutiny).** A truly pre-import *runtime* equality check is architecturally impossible under this cut: the comparison needs the contract parsed, contract-loading uses `safe_parse`/`ReadSet`, and those are exactly the first-party code being extracted into `_deliberate_shared` — so matching before first-party import would be circular, and a weaker pre-import `yaml.safe_load` of the pinned surface was already rejected (ADR-0001 amendment). Instead, (a) the census's policy values are authenticated by the entrypoint's own method-surface hash — they live in the hashed entrypoint source, so trusting the entrypoint is trusting its embedded census; (b) a non-executing release-time test asserts the embedded `_BOUNDARY_POLICY` equals the contract's `import-boundary` section (minus `banned-identifiers`), so a desynced pair cannot ship green; and (c) `_require_boundary_match` in `load_contract` is per-invocation defense-in-depth (it catches a contract swapped via `--data` at runtime) and necessarily runs post-import. Do not "fix" this by adding a pre-import contract parse.
- Moved code is cut-and-pasted, never retyped: the characterization suite pins exact CLI messages, and any transcription drift fails it.
- Production sources never name a banned identifier (`__import__`, `__builtins__`, `builtins`, `importlib`, `zipimport`, `runpy`, `exec`, `eval`, `compile`) as an identifier or import — string literals are fine (the ban is positional). `zipfile` is *not* banned (it reads archives; `zipimport` loads them), so the runtime preflight may import it. Tests are outside that boundary and may use `py_compile`, `importlib`, etc.
- Every task ends with the full suite green and a commit; no task leaves the tree red.

Commands below assume the repo root as CWD. The ambient env lacks pyyaml/pytest: always run the suite as `uv run --with pyyaml --with pytest pytest skills/deliberate/tests/ -q`.

---

## Task 0: Branch and baseline

1. `git status --short --branch` — expect a clean tree on `feature/deliberate-v6-shared-module` (created at planning time, carrying the ADR amendment, portfolio decision fold, and this plan). If the branch is absent, create it from `main` at `fc86e7b` or later: `git switch -c feature/deliberate-v6-shared-module`.
2. Baseline the suite and gates; expected outputs shown:

```bash
uv run --with pyyaml --with pytest pytest skills/deliberate/tests/ -q          # 39 passed
uv run --script skills/deliberate/tests/check_import_closure.py               # import closure, on-disk production files, and method-surfaces agree: 1 Python surface(s)
uv run --script skills/deliberate/scripts/deliberate-validate.py fixtures --data skills/deliberate/references/contract-data.yaml | tail -1   # 158/158 fixtures behaved as required
uv run --script skills/deliberate/scripts/deliberate-validate.py check-renderings --data skills/deliberate/references/contract-data.yaml     # exit 0
```

3. Capture the startup-latency baseline for the smoke record (the portfolio's validation plan requires a before/after read; no threshold exists, so record and compare):

```bash
for i in 1 2 3; do /usr/bin/time -p uv run --script skills/deliberate/scripts/deliberate-validate.py identity --data skills/deliberate/references/contract-data.yaml skills/deliberate/references/contract-data.yaml >/dev/null; done
```

Record the three `real` values in scratch notes for Task 6.

## Task 1: Policy contract in `contract-data.yaml`, version 6, validator acceptance, embedded comparison

### 1.1 Write the failing tests first

Create `skills/deliberate/tests/test_runtime_boundary.py` with this exact content (later tasks append to it):

```python
"""Runtime import-boundary tests (ADR-0001 + 2026-07-16 amendment).

Out-of-process by design: the boundary is module-level entrypoint behavior,
so every case drives the real CLI on an isolated copy of the live bundle.
Test code may use py_compile/importlib freely — the identifier ban governs
production sources only.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def make_bundle(tmp_path: Path) -> Path:
    """Copy the live bundle (scripts/ + references/) into an isolated root."""
    root = tmp_path / "bundle"
    root.mkdir(parents=True)
    shutil.copytree(SKILL_ROOT / "scripts", root / "scripts")
    shutil.copytree(SKILL_ROOT / "references", root / "references")
    return root


def run_cli(
    root: Path, *args: str, tmpdir: Path | None = None
) -> subprocess.CompletedProcess[str]:
    """Run the copied entrypoint in a deterministic subprocess."""
    env = dict(os.environ, LC_ALL="C.UTF-8", PYTHONHASHSEED="0")
    if tmpdir is not None:
        env["TMPDIR"] = str(tmpdir)
    return subprocess.run(
        [
            "uv",
            "run",
            "--script",
            str(root / "scripts" / "deliberate-validate.py"),
            *args,
        ],
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    )


def identity_args(root: Path) -> list[str]:
    """Cheapest full contract-loading command: hash the contract file itself."""
    data = root / "references" / "contract-data.yaml"
    return ["identity", "--data", str(data), str(data)]


def test_unmodified_bundle_copy_passes(tmp_path: Path) -> None:
    """Harness pilot: the copied bundle loads its contract and exits 0."""
    root = make_bundle(tmp_path)
    result = run_cli(root, *identity_args(root))
    assert result.returncode == 0, result.stderr
    assert "identities:" in result.stdout


def test_contract_missing_import_boundary_is_refused(tmp_path: Path) -> None:
    """A contract without the policy section fails the exact top-level key set."""
    root = make_bundle(tmp_path)
    data = root / "references" / "contract-data.yaml"
    text = data.read_text(encoding="utf-8")
    start = text.index("import-boundary:")
    end = text.index("\n# ", start)
    data.write_text(text[:start] + text[end + 1 :], encoding="utf-8")
    result = run_cli(root, *identity_args(root))
    assert result.returncode == 2
    assert "top-level keys must be exactly" in result.stderr


def test_contract_policy_tamper_is_refused_at_load(tmp_path: Path) -> None:
    """Embedded census policy vs contract section: any drift refuses (ADR-0001)."""
    root = make_bundle(tmp_path)
    data = root / "references" / "contract-data.yaml"
    text = data.read_text(encoding="utf-8")
    assert text.count("[.egg, .whl, .zip]") == 1
    data.write_text(
        text.replace("[.egg, .whl, .zip]", "[.egg, .whl]"), encoding="utf-8"
    )
    result = run_cli(root, *identity_args(root))
    assert result.returncode == 2
    assert "import-boundary" in result.stderr
    assert "archive-suffixes" in result.stderr


def test_prior_contract_data_version_is_refused(tmp_path: Path) -> None:
    root = make_bundle(tmp_path)
    data = root / "references" / "contract-data.yaml"
    text = data.read_text(encoding="utf-8")
    assert text.count("contract-data-version: 6") == 1
    data.write_text(
        text.replace("contract-data-version: 6", "contract-data-version: 5"),
        encoding="utf-8",
    )
    result = run_cli(root, *identity_args(root))
    assert result.returncode == 2
    assert "unsupported contract-data-version" in result.stderr
```

Run it and watch it fail (the section, comparison, and version gate do not exist yet):

```bash
uv run --with pyyaml --with pytest pytest skills/deliberate/tests/test_runtime_boundary.py -q   # expect: 1 passed (pilot may pass), 3 failed — the pilot passes only after 1.2; on first run expect 4 failures or errors
```

### 1.2 Edit `skills/deliberate/references/contract-data.yaml`

Change the version line:

```yaml
contract-data-version: 6
```

Insert this section between the `bounds:` block and the `obliged-artifacts:` comment banner (top-level key; the *validator* accepts any placement between top-level sections — key-set validation is exact-set, not ordered). Two Task 1.1 tests do couple to the format specified here, though, so keep it: `test_contract_missing_import_boundary_is_refused` slices the section out via `text.index("\n# ", start)` (relies on a comment banner immediately following the section) and `test_contract_policy_tamper_is_refused_at_load` asserts `text.count("[.egg, .whl, .zip]") == 1` (relies on the flow-style `archive-suffixes` list). Emit the section exactly as written below.

```yaml
# ---------------------------------------------------------------------------
# Import-boundary policy contract (ADR-0001, 2026-07-16 amendment; hardening
# portfolio Option 2). Single declarative source for the scripts/ execution
# boundary. Consumers: the Gate-2 authoring checker
# (tests/check_import_closure.py) loads these values directly; the entrypoint
# embeds the census subset; a release-time test asserts the embedded
# rendering equals this section (minus banned-identifiers), and
# `_require_boundary_match` re-checks it at every contract load as
# defense-in-depth. banned-identifiers is authoring-time (AST) enforcement
# only — the runtime census does not parse Python. Zip detection is
# structural (zipfile.is_zipfile in both consumers), so there is no
# zip-magics list. Editing any value is a method-identity change: classify
# under the method-pin drift rules before landing.
# ---------------------------------------------------------------------------
import-boundary:
  entrypoint: deliberate-validate.py
  module-name-pattern: "^_deliberate_[a-z][a-z0-9_]*\\.py$"
  allowed-data-dirs: [fixtures]
  forbidden-loader-suffixes: [.pyc, .pyo, .pyd, .pyw, .so]
  archive-suffixes: [.egg, .whl, .zip]
  banned-identifiers: [__import__, __builtins__, builtins, importlib, zipimport, runpy, exec, eval, compile]
```

### 1.3 Edit `skills/deliberate/scripts/deliberate-validate.py`

(a) Add the embedded policy after the `PINS_NOT_PRODUCED` constant (Task 3 relocates the dict above the import block; placing it here first keeps this task minimal):

```python
# Embedded rendering of contract-data.yaml's `import-boundary` census subset
# (ADR-0001, 2026-07-16 amendment). The pre-import census consumes ONLY these
# values, authenticated by this entrypoint's own method-surface hash. A
# release-time test asserts this copy equals the contract section (minus
# banned-identifiers), so a desynced pair cannot ship; `_require_boundary_match`
# re-checks it at every contract load as defense-in-depth against a contract
# swapped via --data at runtime. banned-identifiers is deliberately absent: it
# has no runtime consumer (authoring-time AST ban). No zip-magics: zip
# detection is structural (zipfile.is_zipfile), not a magic-byte compare.
_BOUNDARY_POLICY: dict = {
    "entrypoint": "deliberate-validate.py",
    "module-name-pattern": r"^_deliberate_[a-z][a-z0-9_]*\.py$",
    "allowed-data-dirs": ["fixtures"],
    "forbidden-loader-suffixes": [".pyc", ".pyo", ".pyd", ".pyw", ".so"],
    "archive-suffixes": [".egg", ".whl", ".zip"],
}
```

(b) In `validate_contract_data`, add `"import-boundary"` to the `top_keys` set, change the version gate to `if data["contract-data-version"] != 6:`, and append this shape validation at the end of the function body:

```python
    boundary = data["import-boundary"]
    boundary_keys = {
        "entrypoint",
        "module-name-pattern",
        "allowed-data-dirs",
        "forbidden-loader-suffixes",
        "archive-suffixes",
        "banned-identifiers",
    }
    if not isinstance(boundary, dict) or set(boundary) != boundary_keys:
        raise refuse(
            op,
            f"import-boundary keys must be exactly {sorted(boundary_keys)}",
            boundary,
        )
    for key in ("entrypoint", "module-name-pattern"):
        if not isinstance(boundary[key], str) or not boundary[key].strip():
            raise refuse(
                op, f"import-boundary {key} must be a non-empty string", boundary[key]
            )
    for key in sorted(boundary_keys - {"entrypoint", "module-name-pattern"}):
        _contract_string_list(op, boundary, key)
```

(c) Add the comparison next to `load_contract` and call it from `load_contract` after `validate_contract_data(parsed)`:

```python
def _require_boundary_match(data: dict) -> None:
    """Refuse when the contract's import-boundary differs from the embedded census policy.

    The runtime census (module top) consumes only the embedded values, so this
    comparison is what proves — at every invocation — that the embedded
    rendering matches the authenticated policy source (ADR-0001 amendment):
    the runtime never reads an unpinned policy reference as authority.
    """
    boundary = data["import-boundary"]
    for key, embedded in _BOUNDARY_POLICY.items():
        if boundary[key] != embedded:
            raise refuse(
                "contract data",
                f"import-boundary {key} differs from the entrypoint's embedded "
                "census policy (ADR-0001) — the embedded rendering must match "
                "the authenticated contract",
                boundary[key],
            )
```

```python
def load_contract(data_path: Path, readset: ReadSet) -> Contract:
    readset.allow(data_path)
    raw = readset.read_bytes(data_path)
    parsed = safe_parse(raw, byte_cap=4 * 1024 * 1024, depth_cap=48, op="contract data")
    validate_contract_data(parsed)
    _require_boundary_match(parsed)
    return Contract(parsed, Path(os.path.realpath(data_path)))
```

### 1.4 Verify

```bash
uv run --with pyyaml --with pytest pytest skills/deliberate/tests/test_runtime_boundary.py -q   # 4 passed
uv run --with pyyaml --with pytest pytest skills/deliberate/tests/ -q                            # 43 passed
uv run --script skills/deliberate/tests/check_import_closure.py                                  # agree: 1 Python surface(s)  (checker reads only method-surfaces until Task 2)
uv run --script skills/deliberate/scripts/deliberate-validate.py fixtures --data skills/deliberate/references/contract-data.yaml | tail -1   # 158/158 fixtures behaved as required
uv run --script skills/deliberate/scripts/deliberate-validate.py check-renderings --data skills/deliberate/references/contract-data.yaml     # exit 0
```

Exception flagged in the file map: if any characterization case pinned a message that now includes the enlarged `top_keys` list, the assertion text updates to the new sorted list — verified 2026-07-16 that no test pins those messages, so expect no such edit.

### 1.5 Commit

`git add` the three files, review `git diff --cached --stat` and the diff, commit: `feat(deliberate): add pinned import-boundary policy contract (contract-data v6)`.

## Task 2: Bind the Gate-2 checker to the policy section

### 2.1 Failing tests first — append to `skills/deliberate/tests/test_import_closure.py`

Add `import yaml` to the imports, and add after `SKILL_ROOT`:

```python
LIVE_POLICY: dict = yaml.safe_load(
    (SKILL_ROOT / "references" / "contract-data.yaml").read_text(encoding="utf-8")
)["import-boundary"]
```

Append these tests:

```python
def test_live_policy_floor_holds_known_hazard_classes() -> None:
    """Regression floor: single-sourcing must never silently weaken the policy."""
    assert LIVE_POLICY["entrypoint"] == "deliberate-validate.py"
    assert LIVE_POLICY["module-name-pattern"] == r"^_deliberate_[a-z][a-z0-9_]*\.py$"
    assert set(LIVE_POLICY["allowed-data-dirs"]) == {"fixtures"}
    for suffix in (".pyc", ".pyo", ".pyd", ".pyw", ".so"):
        assert suffix in LIVE_POLICY["forbidden-loader-suffixes"]
    assert set(LIVE_POLICY["archive-suffixes"]) == {".egg", ".whl", ".zip"}
    for name in (
        "__import__",
        "__builtins__",
        "builtins",
        "importlib",
        "zipimport",
        "runpy",
        "exec",
        "eval",
        "compile",
    ):
        assert name in LIVE_POLICY["banned-identifiers"]


def test_checker_consumes_the_contract_policy_not_constants(tmp_path: Path) -> None:
    """Weakening a synthetic layout's policy must change checker behavior: the
    contract is the authority, not hardcoded constants. (On the live tree the
    floor test above plus the release-time embedded-vs-contract equality test
    guard against weakening.)

    Weaken `allowed-data-dirs` — a value the checker cannot reconstruct from the
    interpreter (unlike loader suffixes, which the checker re-unions from
    `importlib.machinery.all_suffixes()`, or zips, which it detects
    structurally). With `vendor` allowed, a `scripts/vendor/` directory passes;
    under the live policy the same directory is rejected."""
    weakened = dict(LIVE_POLICY)
    weakened["allowed-data-dirs"] = ["fixtures", "vendor"]
    root = make_layout(
        tmp_path,
        "import os\n",
        {},
        ["scripts/deliberate-validate.py"],
        policy=weakened,
    )
    (root / "scripts" / "vendor").mkdir()
    assert check(root).endswith("1 Python surface(s)")


def test_embedded_runtime_policy_matches_contract_section() -> None:
    """Release-time authentication of the embedded census policy (ADR-0001,
    2026-07-16 amendment): the entrypoint's `_BOUNDARY_POLICY` must equal the
    contract's `import-boundary` section minus `banned-identifiers`. A desynced
    pair cannot ship green, which is what lets `_require_boundary_match` run
    post-import as defense-in-depth rather than as the authentication gate.
    Extraction is non-executing: the entrypoint runs its census on import, so
    the dict is read by AST/`literal_eval`, never by importing production code.
    """
    import ast

    entrypoint = SKILL_ROOT / "scripts" / "deliberate-validate.py"
    tree = ast.parse(entrypoint.read_text(encoding="utf-8"))
    embedded = None
    for node in ast.walk(tree):
        target = None
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target = node.target.id
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(
            node.targets[0], ast.Name
        ):
            target = node.targets[0].id
        if target == "_BOUNDARY_POLICY":
            embedded = ast.literal_eval(node.value)
            break
    assert embedded is not None, "_BOUNDARY_POLICY not found in the entrypoint"
    expected = {k: v for k, v in LIVE_POLICY.items() if k != "banned-identifiers"}
    assert embedded == expected
```

### 2.2 Update `make_layout` in the same file

Replace its `references` block so every synthetic contract carries a policy section (default: the live one), keeping the existing signature plus a `policy` keyword:

```python
def make_layout(
    root: Path,
    entry_body: str,
    modules: dict[str, str],
    surfaces: list[str],
    policy: dict | None = None,
) -> Path:
    """Write a minimal skill layout: entrypoint, modules, contract data.

    Module keys are scripts-relative paths; nested keys create the parent
    directories so package layouts can be expressed (to prove rejection).
    Every layout carries an import-boundary section (default: the live
    policy) because the checker consumes the contract as its policy source.
    """
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "deliberate-validate.py").write_text(entry_body, encoding="utf-8")
    for name, body in modules.items():
        target = scripts / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    references = root / "references"
    references.mkdir()
    document = {
        "validation": {"method-surfaces": surfaces},
        "import-boundary": policy if policy is not None else LIVE_POLICY,
    }
    (references / "contract-data.yaml").write_text(
        yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
    )
    return root
```

Run the file's suite; `test_checker_consumes_the_contract_policy_not_constants` fails (the checker still uses constants), while `test_live_policy_floor_holds_known_hazard_classes` and `test_embedded_runtime_policy_matches_contract_section` pass immediately (they depend only on Task 1's contract section and embedded policy), and existing tests still pass:

```bash
uv run --with pyyaml --with pytest pytest skills/deliberate/tests/test_import_closure.py -q
```

### 2.3 Rework `skills/deliberate/tests/check_import_closure.py`

Replace the module-level constants `ENTRYPOINT_NAME`, `MODULE_NAME`, `ALLOWED_DATA_DIRS`, `BANNED_IDENTIFIERS`, `LOADER_SUFFIXES`, `ARTIFACT_SUFFIXES`, `ARCHIVE_SUFFIXES`, `CENSUS_FORBIDDEN_SUFFIXES`, and `ZIP_MAGICS` with a policy object loaded from the target's contract, threaded through the existing functions:

```python
class BoundaryPolicy:
    """Census and ban values from the target's pinned contract-data.yaml.

    The static forbidden-suffix family from the contract is unioned with the
    running interpreter's ``importlib.machinery.all_suffixes()`` — a
    test-side-only extension (production code may not name importlib), so a
    census run on macOS still rejects artifacts another platform loads.
    """

    def __init__(self, raw: object, source: Path) -> None:
        if not isinstance(raw, dict):
            raise SystemExit(
                "import-closure check failed: import-boundary section missing "
                f"or not a mapping in {source}. Got: {raw!r:.100}"
            )
        required = {
            "entrypoint",
            "module-name-pattern",
            "allowed-data-dirs",
            "forbidden-loader-suffixes",
            "archive-suffixes",
            "banned-identifiers",
        }
        if set(raw) != required:
            raise SystemExit(
                "import-closure check failed: import-boundary keys must be "
                f"exactly {sorted(required)} in {source}. Got: {sorted(raw)}"
            )
        self.entrypoint_name: str = raw["entrypoint"]
        self.module_name = re.compile(raw["module-name-pattern"])
        self.allowed_data_dirs = frozenset(raw["allowed-data-dirs"])
        self.banned_identifiers = frozenset(raw["banned-identifiers"])
        static = frozenset(s.lower() for s in raw["forbidden-loader-suffixes"])
        loader_suffixes = frozenset(importlib.machinery.all_suffixes()) | static
        self.artifact_suffixes = tuple(
            sorted(s.lower() for s in loader_suffixes if s != ".py")
        )
        archive_suffixes = tuple(s.lower() for s in raw["archive-suffixes"])
        self.census_forbidden_suffixes = tuple(
            sorted(set(self.artifact_suffixes) | set(archive_suffixes))
        )
```

Mechanical threading (keep every check, message, and traversal order as-is; only the value source changes):

- `_reject_if_banned(name, node, source_path, policy)` and `reject_banned_identifiers(tree, source_path, policy)` use `policy.banned_identifiers`.
- `classify_first_party(scripts_dir, top, source_path, policy)` uses `policy.artifact_suffixes`.
- `first_party_import_names(source_path, scripts_dir, policy)` threads `policy` down.
- `import_closure(entrypoint, policy)` threads `policy` down.
- `_is_zip_archive(path)` stays policy-free — it calls `zipfile.is_zipfile` (structural detection, already landed in `43065ca`); no magic list to thread.
- `census_scripts_layout(scripts_dir, policy)` uses `policy.allowed_data_dirs`, `policy.entrypoint_name`, `policy.module_name`, `policy.census_forbidden_suffixes`, and `_is_zip_archive(path)`.
- `check(skill_root)` loads the contract once, builds both the policy and the inventory from that one parse, and threads the policy:

```python
def check(skill_root: Path) -> str:
    """Require closure == inventory == on-disk; return the pass message or exit 1."""
    root = skill_root.resolve()
    scripts_dir = root / "scripts"
    contract_data = root / "references" / "contract-data.yaml"
    if not contract_data.is_file():
        raise SystemExit(
            f"import-closure check failed: required file missing. Got: {contract_data}"
        )
    loaded = yaml.safe_load(contract_data.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise SystemExit(
            f"import-closure check failed: contract data is not a mapping. Got: {contract_data}"
        )
    policy = BoundaryPolicy(loaded.get("import-boundary"), contract_data)
    entrypoint = scripts_dir / policy.entrypoint_name
    if not entrypoint.is_file():
        raise SystemExit(
            f"import-closure check failed: required file missing. Got: {entrypoint}"
        )
    on_disk = {
        path.relative_to(root).as_posix()
        for path in census_scripts_layout(scripts_dir, policy)
    }
    closure = {
        path.relative_to(root).as_posix()
        for path in import_closure(entrypoint, policy)
    }
    inventory = inventory_python_surfaces(loaded, contract_data)
    if closure != inventory:
        missing = sorted(closure - inventory)
        unlisted = sorted(inventory - closure)
        raise SystemExit(
            "import-closure check failed: source closure and method-surfaces "
            f"Python subset differ. Imported but not inventoried: {missing}; "
            f"inventoried but never imported: {unlisted}"
        )
    if on_disk != inventory:
        present = sorted(on_disk - inventory)
        absent = sorted(inventory - on_disk)
        raise SystemExit(
            "import-closure check failed: on-disk production Python and "
            f"method-surfaces Python subset differ. On disk but not "
            f"inventoried: {present}; inventoried but absent from scripts/: "
            f"{absent}"
        )
    return (
        "import closure, on-disk production files, and method-surfaces "
        f"agree: {len(closure)} Python surface(s)"
    )
```

`inventory_python_surfaces` changes signature to take the already-parsed mapping instead of re-reading the file; its validation and message text stay byte-identical:

```python
def inventory_python_surfaces(loaded: object, contract_data: Path) -> set[str]:
    """Python entries of validation.method-surfaces, as skill-relative paths."""
    try:
        surfaces = loaded["validation"]["method-surfaces"]
    except (TypeError, KeyError) as error:
        raise SystemExit(
            "import-closure check failed: validation.method-surfaces absent "
            f"from {contract_data}. Got: {error!r}"
        ) from error
    if not isinstance(surfaces, list) or not surfaces:
        raise SystemExit(
            "import-closure check failed: validation.method-surfaces must be "
            f"a non-empty list. Got: {surfaces!r:.100}"
        )
    return {str(surface) for surface in surfaces if str(surface).endswith(".py")}
```

Update **every** direct `import_closure(...)` caller in `test_import_closure.py` — the signature is now `import_closure(entrypoint, policy)`, so a one-arg call raises `TypeError` that `pytest.raises(SystemExit, …)` will not catch. There are three:

- `test_import_resolving_to_sourceless_bytecode_is_rejected` and `test_import_resolving_to_directory_is_rejected` each call `import_closure(<entrypoint path>)`; build the policy first and pass it, e.g.

```python
    from check_import_closure import BoundaryPolicy

    policy = BoundaryPolicy(LIVE_POLICY, root / "references" / "contract-data.yaml")
    with pytest.raises(SystemExit, match=r"never bytecode, a package, or a symlink"):
        import_closure(root / "scripts" / "deliberate-validate.py", policy)
```

  (These layouts are built by `make_layout`, which now writes the live policy section, so `LIVE_POLICY` is the right value.)

- The live-tree test builds the policy explicitly —

```python
def test_live_tree_passes_with_entrypoint_only_closure() -> None:
    """Pre-extraction reality: the closure is exactly the entrypoint, and the gate passes."""
    from check_import_closure import BoundaryPolicy

    entrypoint = SKILL_ROOT / "scripts" / "deliberate-validate.py"
    policy = BoundaryPolicy(
        LIVE_POLICY, SKILL_ROOT / "references" / "contract-data.yaml"
    )
    assert import_closure(entrypoint, policy) == {entrypoint.resolve()}
    message = check(SKILL_ROOT)
    assert message == (
        "import closure, on-disk production files, and method-surfaces "
        "agree: 1 Python surface(s)"
    )
```

(Task 4 rewrites this test for two surfaces.)

### 2.4 Verify and commit

```bash
uv run --with pyyaml --with pytest pytest skills/deliberate/tests/ -q            # 46 passed
uv run --script skills/deliberate/tests/check_import_closure.py                  # agree: 1 Python surface(s)
```

Commit: `feat(deliberate): bind gate-2 checker to the pinned import-boundary policy`.

## Task 3: Runtime pre-import census and fresh cache prefix

### 3.1 Failing tests first — append to `skills/deliberate/tests/test_runtime_boundary.py`

Add `import py_compile` to the imports, then append:

```python
def seed_marker_pyc(root: Path, tmp_path: Path, name: str) -> Path:
    """Compile a marker-writing source into a sourceless .pyc under scripts/."""
    marker = tmp_path / "executed.marker"
    src = tmp_path / "seed_src.py"
    src.write_text(f"open({str(marker)!r}, 'w').write('ran')\n", encoding="utf-8")
    py_compile.compile(str(src), cfile=str(root / "scripts" / name))
    return marker


def test_seeded_sourceless_pyc_is_refused_without_executing(tmp_path: Path) -> None:
    root = make_bundle(tmp_path)
    marker = seed_marker_pyc(root, tmp_path, "_deliberate_hidden.pyc")
    result = run_cli(root, *identity_args(root))
    assert result.returncode == 2
    assert "import boundary refused" in result.stderr
    assert "_deliberate_hidden.pyc" in result.stderr
    assert not marker.exists()


def test_seeded_pycache_directory_is_refused(tmp_path: Path) -> None:
    root = make_bundle(tmp_path)
    cache = root / "scripts" / "__pycache__"
    cache.mkdir()
    (cache / "stale.cpython-313.pyc").write_bytes(b"\x00stale")
    result = run_cli(root, *identity_args(root))
    assert result.returncode == 2
    assert "__pycache__" in result.stderr


def test_symlinked_module_and_symlinked_package_are_refused(tmp_path: Path) -> None:
    outside_file = tmp_path / "outside.py"
    outside_file.write_text("VALUE = 1\n", encoding="utf-8")
    outside_pkg = tmp_path / "outside_pkg"
    outside_pkg.mkdir()
    (outside_pkg / "__init__.py").write_text("VALUE = 1\n", encoding="utf-8")
    for label, target, link_name in (
        ("file", outside_file, "_deliberate_link.py"),
        ("package", outside_pkg, "_deliberate_linkpkg"),
    ):
        root = make_bundle(tmp_path / label)
        (root / "scripts" / link_name).symlink_to(target)
        result = run_cli(root, *identity_args(root))
        assert result.returncode == 2, label
        assert "symlink" in result.stderr, label


def test_package_directory_is_refused(tmp_path: Path) -> None:
    root = make_bundle(tmp_path)
    pkg = root / "scripts" / "_deliberate_pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("VALUE = 1\n", encoding="utf-8")
    result = run_cli(root, *identity_args(root))
    assert result.returncode == 2
    assert "_deliberate_pkg" in result.stderr


def _zip_bytes(arcname: str = "evilmod.py", body: str = "VALUE = 1\n") -> bytes:
    """A real, structurally valid zip archive (has an end-of-central-directory)."""
    import io
    import zipfile

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr(arcname, body)
    return buffer.getvalue()


def test_zip_archives_and_disguised_zip_are_refused(tmp_path: Path) -> None:
    """.zip/.egg/.whl fall to the suffix rule; a real (even prefixed) zip with an
    inert suffix falls to pass 2's structural `is_zipfile` check. The `.dat`
    cases use genuine archives: a four-byte fragment would not be importable and
    must not be relied on. `prefixed.dat` is the 2026-07-16 scrutiny case — a
    valid zip behind a shell stub whose first bytes are not `PK`."""
    cases = {
        "payload.zip": b"PK\x03\x04fragment",  # suffix rule; content irrelevant
        "payload.egg": b"PK\x03\x04fragment",
        "payload.whl": b"PK\x03\x04fragment",
        "payload.dat": _zip_bytes(),  # inert suffix: real zip → structural check
        "prefixed.dat": b"#!/bin/sh\n# self-extracting stub\n" + _zip_bytes(),
    }
    for name, content in cases.items():
        root = make_bundle(tmp_path / name.replace(".", "_"))
        (root / "scripts" / name).write_bytes(content)
        result = run_cli(root, *identity_args(root))
        assert result.returncode == 2, name
        assert name in result.stderr, name


def test_nested_python_file_is_refused(tmp_path: Path) -> None:
    root = make_bundle(tmp_path)
    (root / "scripts" / "fixtures" / "evil.py").write_text(
        "VALUE = 1\n", encoding="utf-8"
    )
    result = run_cli(root, *identity_args(root))
    assert result.returncode == 2
    assert "evil.py" in result.stderr


def test_stdlib_shadow_is_refused_before_it_can_import(tmp_path: Path) -> None:
    """A scripts/argparse.py would shadow stdlib argparse via sys.path[0]; the
    census must refuse it before the entrypoint's own deferred imports run —
    the marker proves nothing executed."""
    root = make_bundle(tmp_path)
    marker = tmp_path / "shadow.marker"
    (root / "scripts" / "argparse.py").write_text(
        f"open({str(marker)!r}, 'w').write('ran')\n", encoding="utf-8"
    )
    result = run_cli(root, *identity_args(root))
    assert result.returncode == 2
    assert "argparse.py" in result.stderr
    assert not marker.exists()


def test_inert_file_passes_and_conforming_extra_module_is_runtime_inert(
    tmp_path: Path,
) -> None:
    """Layer boundary: the runtime census is layout-only. An inert data file
    passes; a flat conforming-but-uninventoried module also passes at runtime
    (it is unreachable without dynamic import) while the authoring gate
    rejects the same layout via inventory equality."""
    import pytest
    from check_import_closure import check

    root = make_bundle(tmp_path)
    (root / "scripts" / "notes.txt").write_text("plain text\n", encoding="utf-8")
    (root / "scripts" / "_deliberate_extra.py").write_text(
        "VALUE = 1\n", encoding="utf-8"
    )
    result = run_cli(root, *identity_args(root))
    assert result.returncode == 0, result.stderr
    with pytest.raises(SystemExit, match="on-disk production Python"):
        check(root)


def test_module_name_grammar_matches_declared_pattern(tmp_path: Path) -> None:
    """The census's re-free name check must agree with module-name-pattern."""
    accepted = ["_deliberate_shared.py", "_deliberate_a9_x.py"]
    refused = [
        "_deliberate_.py",
        "_deliberate_9x.py",
        "_Deliberate_x.py",
        "_deliberate_X.py",
        "deliberate_x.py",
        "_deliberate_x.mod.py",
    ]
    for index, name in enumerate(accepted):
        root = make_bundle(tmp_path / f"ok{index}")
        (root / "scripts" / name).write_text("VALUE = 1\n", encoding="utf-8")
        assert run_cli(root, *identity_args(root)).returncode == 0, name
    for index, name in enumerate(refused):
        root = make_bundle(tmp_path / f"bad{index}")
        (root / "scripts" / name).write_text("VALUE = 1\n", encoding="utf-8")
        result = run_cli(root, *identity_args(root))
        assert result.returncode == 2, name
        assert name in result.stderr


def test_cache_prefix_is_external_private_retired_and_unsafe_roots_refuse(
    tmp_path: Path,
) -> None:
    """An external temp root works; any protected-tree placement refuses.

    ADR-0001 requires the prefix outside the repository, not merely outside
    scripts/. The runtime finds the outermost containing Git root (so an inner
    marker cannot narrow the boundary), falls back to the served bundle when
    standalone, resolves symlinks, and refuses before any first-party import.
    The optional shared-module marker becomes active after Task 4 without
    changing this Task-3 checkpoint.
    """
    root = make_bundle(tmp_path / "external")
    scoped = tmp_path / "scoped-tmp"
    scoped.mkdir()
    result = run_cli(root, *identity_args(root), tmpdir=scoped)
    assert result.returncode == 0, result.stderr
    assert list(scoped.glob("deliberate-pycache-*")) == []  # prefix retired at exit
    assert list(root.rglob("deliberate-pycache-*")) == []
    assert list((root / "scripts").rglob("__pycache__")) == []
    assert list((root / "scripts").rglob("*.pyc")) == []

    cases: list[tuple[str, Path, Path]] = []
    for label, relative in (
        ("bundle", "tmp"),
        ("scripts", "scripts"),
        ("allowed-data", "scripts/fixtures"),
    ):
        case_root = make_bundle(tmp_path / label)
        unsafe = case_root / relative
        unsafe.mkdir(parents=True, exist_ok=True)
        cases.append((label, case_root, unsafe))

    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)
    repo_root = make_bundle(repo / "skills" / "deliberate")
    (repo_root / ".git").mkdir()  # inner marker must not narrow the outer root
    repo_tmp = repo / "tmp"  # inside Git root, outside the served bundle
    repo_tmp.mkdir()
    cases.append(("repo", repo_root, repo_tmp))
    case_alias = repo.parent / repo.name.swapcase() / "tmp"
    if case_alias.exists() and os.path.samefile(case_alias, repo_tmp):
        cases.append(("case-alias", repo_root, case_alias))

    link_root = make_bundle(tmp_path / "symlink")
    link_target = link_root / "tmp"
    link_target.mkdir()
    unsafe_link = tmp_path / "symlink" / "tmp-link"
    unsafe_link.symlink_to(link_target, target_is_directory=True)
    cases.append(("symlink", link_root, unsafe_link))

    for label, case_root, unsafe in cases:
        marker = tmp_path / f"{label}.marker"
        shared = case_root / "scripts" / "_deliberate_shared.py"
        if shared.exists():
            text = shared.read_text(encoding="utf-8")
            needle = "from __future__ import annotations\n"
            assert text.count(needle) == 1
            shared.write_text(
                text.replace(
                    needle,
                    needle + f"\nopen({str(marker)!r}, 'w').write('ran')\n",
                    1,
                ),
                encoding="utf-8",
            )
        result = run_cli(case_root, *identity_args(case_root), tmpdir=unsafe)
        assert result.returncode == 2, label
        assert "cache temp root must resolve outside" in result.stderr, label
        assert not marker.exists(), label
        assert list(tmp_path.rglob("deliberate-pycache-*")) == [], label
        assert list(tmp_path.rglob("*.pyc")) == [], label
        assert list((case_root / "scripts").rglob("__pycache__")) == [], label
        assert list((case_root / "scripts").rglob("*.pyc")) == [], label
```

Also append to `skills/deliberate/tests/test_import_closure.py` a non-executing test proving the runtime name predicate agrees with the contract regex over a *generated* corpus, not a handful of examples (2026-07-16 scrutiny finding 5 / assumption audit: examples are not algorithmic equivalence). It extracts the dependency-free `_boundary_module_name_conforms` by source segment and compiles it in isolation — never importing the entrypoint (which runs its census on import):

```python
def test_runtime_name_predicate_matches_contract_regex() -> None:
    """The entrypoint's re-free `_boundary_module_name_conforms` must agree with
    the contract's `module-name-pattern` over a generated corpus of realistic
    (newline-free) filenames. Non-executing: the function is dependency-free,
    extracted by source segment and exec'd in isolation, never by importing
    production code. Scope note: `re`'s `$` matches before a trailing newline
    while the predicate requires `.endswith('.py')`, so a name like
    `"_deliberate_x.py\\n"` would disagree — but that class is unreachable
    because both the runtime census and the Gate-2 checker gate on
    `lower.endswith('.py')` before applying the name rule (fail-closed either
    way), so the corpus is deliberately newline-free."""
    import ast
    import itertools
    import re as _re

    source = (SKILL_ROOT / "scripts" / "deliberate-validate.py").read_text(
        encoding="utf-8"
    )
    tree = ast.parse(source)
    func_node = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and node.name == "_boundary_module_name_conforms"
    )
    namespace: dict = {}
    exec(ast.get_source_segment(source, func_node), namespace)
    predicate = namespace["_boundary_module_name_conforms"]
    regex = _re.compile(LIVE_POLICY["module-name-pattern"])
    corpus = [
        "_deliberate_" + "".join(combo) + ".py"
        for length in range(0, 4)
        for combo in itertools.product("az9_.AZ-", repeat=length)
    ]
    corpus += [
        "_deliberate_shared.py", "_deliberate_a9_x.py", "_deliberate_.py",
        "_deliberate_9x.py", "_Deliberate_x.py", "_deliberate_X.py",
        "deliberate_x.py", "_deliberate_x.mod.py", "_deliberate_shared.txt",
        "deliberate-validate.py", "evil.py", "",
    ]
    for name in corpus:
        assert predicate(name) == bool(regex.match(name)), name
```

Run and watch them fail: `uv run --with pyyaml --with pytest pytest skills/deliberate/tests/test_runtime_boundary.py skills/deliberate/tests/test_import_closure.py -q`. Every seeded runtime case currently exits 0 because no census exists; the agreement test fails because `_boundary_module_name_conforms` does not exist yet.

### 3.2 Restructure the entrypoint header

In `skills/deliberate/scripts/deliberate-validate.py`, replace the import block (currently `import argparse` through `import yaml`) with the following, and move the `_BOUNDARY_POLICY` dict from Task 1 up into this block (delete it from its Task-1 position). The PEP 723 header, docstring, and `from __future__ import annotations` stay first and unchanged (the docstring gains one bullet, below):

```python
import os
import sys

# ---------------------------------------------------------------------------
# Pre-import boundary (ADR-0001 + 2026-07-16 amendment), two passes before any
# first-party import. Pass 1 (the LAYOUT census) uses only `os`/`sys` — modules
# already initialized at interpreter startup, so they cannot be shadowed from
# scripts/ (which is sys.path[0]) — enforces every structural rule, and COLLECTS
# the inert-suffix files. Once pass 1 returns without refusing, no
# .py/.pyc/.so/package/symlink shadow exists under scripts/, so only the narrow
# deferred stdlib imports below may run: atexit/shutil/tempfile create and
# retire a cache prefix mechanically verified outside the repository (or the
# served skill root when standalone), and zipfile performs pass 2's structural
# archive check. Unsafe ambient temp roots refuse before prefix creation; the
# created prefix is resolved and checked again before assignment. Pass 2 runs
# `zipfile.is_zipfile` on the collected inert files — the same detector the
# Gate-2 checker uses (43065ca), so a prefixed/self-extracting zip is caught and
# the two consumers cannot drift on zip detection. Every first-party and other
# import waits until pass 2 returns. The census consumes only the embedded
# policy, authenticated by this entrypoint's own method-surface hash; a
# release-time test asserts that embedding equals the pinned contract section,
# and `_require_boundary_match` re-checks it per invocation as defense-in-depth.
# No pre-import contract parse (a weaker first parse of a pinned surface was
# rejected — ADR-0001 amendment).
# ---------------------------------------------------------------------------
_BOUNDARY_POLICY: dict = {
    "entrypoint": "deliberate-validate.py",
    "module-name-pattern": r"^_deliberate_[a-z][a-z0-9_]*\.py$",
    "allowed-data-dirs": ["fixtures"],
    "forbidden-loader-suffixes": [".pyc", ".pyo", ".pyd", ".pyw", ".so"],
    "archive-suffixes": [".egg", ".whl", ".zip"],
}
_BOUNDARY_FORBIDDEN_SUFFIXES = tuple(
    sorted(
        set(_BOUNDARY_POLICY["forbidden-loader-suffixes"])
        | set(_BOUNDARY_POLICY["archive-suffixes"])
    )
)


def _boundary_refuse(reason: str, got: str) -> None:
    sys.stderr.write(f"import boundary refused: {reason}. Got: {got}\n")
    sys.exit(2)


def _boundary_module_name_conforms(name: str) -> bool:
    """`re`-free rendering of module-name-pattern; agreement is test-pinned."""
    if not name.startswith("_deliberate_") or not name.endswith(".py"):
        return False
    stem = name[len("_deliberate_") : -len(".py")]
    if not stem or stem[0] not in "abcdefghijklmnopqrstuvwxyz":
        return False
    return all(c in "abcdefghijklmnopqrstuvwxyz0123456789_" for c in stem)


def _boundary_layout_census(scripts_dir: str) -> list[str]:
    """ADR-0001 runtime layout census (pass 1): os/sys only, fail-closed.

    Enforces every structural rule and RETURNS the inert-suffix files (no .py,
    no forbidden loader/archive suffix) for the pass-2 content check. Mirrors
    the Gate-2 authoring census (tests/check_import_closure.py) minus
    closure/inventory equality, which stays an authoring-gate concern: a flat
    conforming uninventoried module is inert here because production code
    contains no dynamic-import machinery and the orchestrator platform-hashes
    every method surface before trusting results.
    """
    if os.path.islink(scripts_dir):
        _boundary_refuse(
            "scripts/ itself must be a real directory, not a symlink (ADR-0001)",
            scripts_dir,
        )
    allowed_dirs = set(_BOUNDARY_POLICY["allowed-data-dirs"])
    inert: list[str] = []
    for dirpath, dirnames, filenames in os.walk(scripts_dir, followlinks=False):
        for name in sorted(dirnames):
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                _boundary_refuse(
                    "symlinks are forbidden anywhere under scripts/ (ADR-0001)", path
                )
            if name == "__pycache__":
                _boundary_refuse(
                    "__pycache__ is forbidden under scripts/ (ADR-0001)", path
                )
            top = os.path.relpath(path, scripts_dir).split(os.sep)[0]
            if top not in allowed_dirs:
                _boundary_refuse(
                    "directories under scripts/ are forbidden outside the "
                    f"declared data allowlist {sorted(allowed_dirs)} (ADR-0001)",
                    path,
                )
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                _boundary_refuse(
                    "symlinks are forbidden anywhere under scripts/ (ADR-0001)", path
                )
            if name == "__pycache__":
                _boundary_refuse(
                    "__pycache__ is forbidden under scripts/ (ADR-0001)", path
                )
            if not os.path.isfile(path):
                _boundary_refuse("unsupported filesystem object under scripts/", path)
            lower = name.lower()
            if lower.endswith(".py"):
                if dirpath != scripts_dir:
                    _boundary_refuse(
                        "production Python must be flat in scripts/ (ADR-0001)", path
                    )
                if name != _BOUNDARY_POLICY[
                    "entrypoint"
                ] and not _boundary_module_name_conforms(name):
                    _boundary_refuse(
                        "production module name must match _deliberate_<domain>.py "
                        "(ADR-0001 naming rule)",
                        path,
                    )
                continue
            if any(lower.endswith(suffix) for suffix in _BOUNDARY_FORBIDDEN_SUFFIXES):
                _boundary_refuse(
                    "importable non-source artifact is forbidden under scripts/ "
                    "(ADR-0001)",
                    path,
                )
            inert.append(path)
    return inert


_boundary_scripts_dir = os.path.dirname(os.path.abspath(__file__))
_boundary_inert_files = _boundary_layout_census(_boundary_scripts_dir)

import atexit  # noqa: E402 — deferred by design: imports wait for pass 1
import shutil  # noqa: E402
import tempfile  # noqa: E402


def _boundary_protected_root(scripts_dir: str) -> str:
    """Outermost Git root containing the skill, or skill root if standalone."""
    skill_root = os.path.realpath(os.path.dirname(scripts_dir))
    protected_root = skill_root
    cursor = skill_root
    while True:
        if os.path.exists(os.path.join(cursor, ".git")):
            protected_root = cursor
        parent = os.path.dirname(cursor)
        if parent == cursor:
            return protected_root
        cursor = parent


def _boundary_path_is_within(path: str, root: str) -> bool:
    """Containment by filesystem identity; comparison errors are unsafe."""
    real_root = os.path.realpath(root)
    cursor = os.path.realpath(path)
    while True:
        try:
            if os.path.samefile(cursor, real_root):
                return True
        except OSError:
            return True
        parent = os.path.dirname(cursor)
        if parent == cursor:
            return False
        cursor = parent


# Fresh, initially empty (mkdtemp), invocation-private (0o700), under the
# process temp root but mechanically outside the repository (or outside the
# served skill root when no Git root is present), retired at exit, never reused
# across invocations (ADR-0001). A temp root inside the protected source tree —
# directly, through a symlink, or through a case alias — refuses BEFORE prefix
# creation. Containment compares filesystem identity, not path-string casing;
# errors are unsafe. The created prefix is resolved and checked again before
# assignment, closing a symlink swap between selection and creation.
# Redirecting alone is insufficient — pass 1 above is what stops directly-read
# sourceless bytecode.
_boundary_source_root = _boundary_protected_root(_boundary_scripts_dir)
_boundary_temp_root = os.path.realpath(tempfile.gettempdir())
if _boundary_path_is_within(_boundary_temp_root, _boundary_source_root):
    _boundary_refuse(
        "cache temp root must resolve outside the repository or served skill "
        "root (ADR-0001)",
        _boundary_temp_root,
    )
_boundary_cache_prefix = os.path.realpath(
    tempfile.mkdtemp(prefix="deliberate-pycache-", dir=_boundary_temp_root)
)
if _boundary_path_is_within(_boundary_cache_prefix, _boundary_source_root):
    shutil.rmtree(_boundary_cache_prefix, ignore_errors=True)
    _boundary_refuse(
        "created cache prefix must resolve outside the repository or served "
        "skill root (ADR-0001)",
        _boundary_cache_prefix,
    )
sys.pycache_prefix = _boundary_cache_prefix
atexit.register(shutil.rmtree, sys.pycache_prefix, ignore_errors=True)

# Pass 2: pass 1 refused every importable shadow, so importing zipfile (which
# reads archives; zipimport, banned, loads them) cannot resolve to a scripts/
# file. is_zipfile locates the trailing end-of-central-directory record the way
# zipimport does, catching a prefixed/self-extracting zip a magic sniff misses.
import zipfile  # noqa: E402 — safe only after pass 1 cleared every importable shadow

for _inert_path in _boundary_inert_files:
    if zipfile.is_zipfile(_inert_path):
        _boundary_refuse(
            "file is a valid zip archive despite an inert suffix (ADR-0001) — a "
            "disguised or prefixed archive on sys.path imports as code through "
            "zipimport",
            _inert_path,
        )

import argparse  # noqa: E402
import copy  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import re  # noqa: E402
import stat  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import Any  # noqa: E402

import yaml  # noqa: E402
```

Add one bullet to the docstring's "Validator boundary" list:

```
- Pre-import boundary: before any first-party import, a two-pass stdlib-only
  census of scripts/ refuses unexpected artifacts fail-closed (ADR-0001) —
  layout rules run on os/sys before any shadowable import, then the narrow
  deferred stdlib set performs a structural zip check (zipfile.is_zipfile,
  after direct shadows are cleared) that catches prefixed archives; bytecode is
  redirected to a fresh invocation-private cache prefix mechanically verified
  outside the repository (or served skill root when standalone) and retired at
  exit, with repo-, bundle-, scripts-, allowed-data-, symlink-resolved-, and
  case-aliased internal temp roots refused before first-party import; the
  embedded census policy is authenticated by this file's own method-surface
  hash and asserted equal to contract-data.yaml's import-boundary section by a
  release-time test, with _require_boundary_match re-checking it at every load.
```

### 3.3 Verify and commit

```bash
uv run --with pyyaml --with pytest pytest skills/deliberate/tests/ -q            # 57 passed
uv run --script skills/deliberate/tests/check_import_closure.py                  # agree: 1 Python surface(s)
uv run --script skills/deliberate/scripts/deliberate-validate.py fixtures --data skills/deliberate/references/contract-data.yaml | tail -1   # 158/158 fixtures behaved as required
uvx ruff check skills/deliberate/scripts/deliberate-validate.py                  # All checks passed!
```

Commit: `feat(deliberate): runtime pre-import census and invocation-private cache prefix`.

## Task 4: Extract `scripts/_deliberate_shared.py`

### 4.1 Failing tests first

Rewrite `test_live_tree_passes_with_entrypoint_only_closure` in `skills/deliberate/tests/test_import_closure.py` as:

```python
def test_live_tree_passes_with_shared_module_closure() -> None:
    """v6 reality: the closure is the entrypoint plus _deliberate_shared."""
    from check_import_closure import BoundaryPolicy

    entrypoint = SKILL_ROOT / "scripts" / "deliberate-validate.py"
    shared = SKILL_ROOT / "scripts" / "_deliberate_shared.py"
    policy = BoundaryPolicy(
        LIVE_POLICY, SKILL_ROOT / "references" / "contract-data.yaml"
    )
    assert import_closure(entrypoint, policy) == {
        entrypoint.resolve(),
        shared.resolve(),
    }
    message = check(SKILL_ROOT)
    assert message == (
        "import closure, on-disk production files, and method-surfaces "
        "agree: 2 Python surface(s)"
    )
```

Append to `skills/deliberate/tests/test_runtime_boundary.py`:

```python
def test_sourceless_shadow_of_shared_module_is_refused(tmp_path: Path) -> None:
    """A sourceless _deliberate_shared.pyc beside the real module is exactly
    the directly-read-bytecode hazard: refused before any import."""
    root = make_bundle(tmp_path)
    marker = seed_marker_pyc(root, tmp_path, "_deliberate_shared.pyc")
    result = run_cli(root, *identity_args(root))
    assert result.returncode == 2
    assert "_deliberate_shared.pyc" in result.stderr
    assert not marker.exists()


def test_second_invocation_never_reuses_prior_bytecode(tmp_path: Path) -> None:
    """Gate-1 follow-up hazard as a tripwire: after a same-size, mtime-restored
    edit to _deliberate_shared.py, the second invocation must execute the
    edited code — a reused cache entry (size+mtime match) would show the old
    string. The observable channel is safe_parse's anchor refusal, which lives
    in the shared module."""
    root = make_bundle(tmp_path)
    scoped = tmp_path / "scoped-tmp"
    scoped.mkdir()
    bad_contract = tmp_path / "anchored.yaml"
    bad_contract.write_text("a: &x 1\nb: *x\n", encoding="utf-8")
    probe_args = ["identity", "--data", str(bad_contract), str(bad_contract)]
    first = run_cli(root, *probe_args, tmpdir=scoped)
    assert first.returncode == 2
    assert "YAML anchors are rejected" in first.stderr
    shared = root / "scripts" / "_deliberate_shared.py"
    before = shared.stat()
    text = shared.read_text(encoding="utf-8")
    assert text.count("YAML anchors are rejected") == 1
    edited = text.replace("YAML anchors are rejected", "YAML anchorZ are rejected")
    assert len(edited.encode("utf-8")) == len(text.encode("utf-8"))
    shared.write_text(edited, encoding="utf-8")
    os.utime(shared, ns=(before.st_atime_ns, before.st_mtime_ns))
    second = run_cli(root, *probe_args, tmpdir=scoped)
    assert second.returncode == 2
    assert "YAML anchorZ are rejected" in second.stderr
```

Run both files; the closure test and the two new runtime tests fail (module absent).

### 4.2 Create `skills/deliberate/scripts/_deliberate_shared.py`

Start the file with exactly:

```python
"""deliberate — shared foundation: errors, read authorization, safe YAML.

Extracted from scripts/deliberate-validate.py under ADR-0001 (contract-data
version 6): the base of the internal dependency graph — everything calls into
it; it calls into no other first-party code. A direct method surface: listed
in validation.method-surfaces and platform-hashed by the orchestrator before
any helper invocation. No PEP 723 header: an imported module, never an
entrypoint — the entrypoint's script environment supplies `yaml`.
"""

from __future__ import annotations

import io
import os
from pathlib import Path
from typing import Any

import yaml
```

Then cut (not copy) the following block from `deliberate-validate.py` and paste it verbatim below that header — cut-and-paste in the editor, never retype. The block starts at the line `SAFE_TAGS = {` and ends at the closing `    )` of `dump_yaml` (the line before the `# Canonical data` section banner). It comprises, in order: `SAFE_TAGS`; the `Refusal`, `ValidationFailure`, `StoreReadLoss` classes; `fail`; `refuse`; the `# Read-set enforcement` banner and `ReadSet`; the `# Safe YAML` banner, `_decode_utf8`, `safe_parse`, `_UniqueKeyLoader`, `_construct_unique_mapping`, the `add_constructor` call, `_NoAliasDumper`, and `dump_yaml`.

### 4.3 Wire the entrypoint

In `deliberate-validate.py`, at the point where the cut block was removed (just after the deferred `import yaml`), add:

```python
from _deliberate_shared import (  # noqa: E402
    ReadSet,
    Refusal,
    StoreReadLoss,
    ValidationFailure,
    _decode_utf8,
    dump_yaml,
    fail,
    refuse,
    safe_parse,
)
```

Then prune now-unused entrypoint imports: run `uvx ruff check skills/deliberate/scripts/deliberate-validate.py` and delete exactly the imports it reports as F401 (expected: `io` and `yaml` — verified 2026-07-16 as the only imports with zero uses outside the moved block; `tempfile`, `re`, `stat`, `subprocess`, `copy`, `hashlib` all have live uses elsewhere in the file). Do NOT remove `pyyaml` from the PEP 723 `dependencies` — the shared module needs it from the entrypoint's script environment.

### 4.4 Inventory, prose, and bootstrap updates

(a) `skills/deliberate/references/contract-data.yaml` — in `validation.method-surfaces`, insert `scripts/_deliberate_shared.py` before `scripts/deliberate-validate.py`:

```yaml
  method-surfaces:
    - SKILL.md
    - references/capsule.md
    - references/contract-data.yaml
    - references/methods.md
    - references/schemas.md
    - references/stage-packets.md
    - scripts/_deliberate_shared.py
    - scripts/deliberate-validate.py
```

(b) `skills/deliberate/references/capsule.md` — in the method-identity sentence, replace this exact fragment:

```text
and the bundled validator script, recorded at setup beside the constituent pins
```

with:

```text
and the bundled validator script with its imported production module (`scripts/_deliberate_shared.py`), recorded at setup beside the constituent pins
```

(c) `skills/deliberate/SKILL.md` — two edits:

- In the preflight paragraph, change `Before spending, verify the helper with \`shasum -a 256\`` to `Before spending, verify the helper — the entrypoint and every imported production module — with \`shasum -a 256\``.
- In the Helper section code block, change the first two lines to:

```bash
V=scripts/deliberate-validate.py; M=scripts/_deliberate_shared.py; D=references/contract-data.yaml   # paths relative to this skill directory
shasum -a 256 $V $M
```

- In the orchestrator obligations bullet, change `verify the validator with the platform hasher. A drifted validator takes the emergency-receipt branch.` to `verify the validator and its imported production modules with the platform hasher. A drifted validator or module takes the emergency-receipt branch.`

### 4.5 Verify and commit

```bash
uv run --script skills/deliberate/tests/check_import_closure.py                  # agree: 2 Python surface(s)
uv run --with pyyaml --with pytest pytest skills/deliberate/tests/ -q            # 59 passed
uv run --script skills/deliberate/scripts/deliberate-validate.py fixtures --data skills/deliberate/references/contract-data.yaml | tail -1   # 158/158 fixtures behaved as required
uv run --script skills/deliberate/scripts/deliberate-validate.py check-renderings --data skills/deliberate/references/contract-data.yaml     # exit 0
uvx ruff check skills/deliberate/scripts/                                        # All checks passed!
git diff --word-diff=plain -- skills/deliberate/scripts/deliberate-validate.py | head -80   # the moved region must show as pure deletion
```

Commit: `feat(deliberate): extract scripts/_deliberate_shared.py as the eighth method surface`.

## Task 5: Spec lineage

In `docs/specs/2026-07-13-deliberate.md`:

- Status line: change `**Status:** v27 —` to `**Status:** v28 —`, and change `· **Date:** 2026-07-13 (v26–v27: 2026-07-15)` to `· **Date:** 2026-07-13 (v26–v27: 2026-07-15; v28: <execution date>)`.
- In the Design lineage list, append after the v27 entry:

```markdown
- **v28** (contract evolution — v6 module topology and the import-execution boundary): the first physical extraction under ADR-0001 — `scripts/_deliberate_shared.py` (error/refusal constructors, read authorization, safe-YAML foundation) leaves the entrypoint; `validation.method-surfaces` grows to eight entries and `contract-data-version` bumps to 6, hard-cutting pre-topology capsules (no migration path; no legacy population). The import-execution boundary becomes one explicit control (hardening portfolio Option 2; placement decided by JP 2026-07-16): a declarative `import-boundary` policy section in the pinned `contract-data.yaml` feeds the Gate-2 authoring checker directly, and the entrypoint embeds the census subset (authenticated by its own method-surface hash), runs a two-pass stdlib-only pre-first-party-import census of `scripts/` (layout hazards — symlinks, `__pycache__`, bytecode and extension artifacts, archive suffixes, out-of-allowlist directories, nested or non-conforming `.py` — refused on `os`/`sys` before any shadowable import; zip structure checked by the narrow deferred stdlib set after direct shadows are cleared so a prefixed/self-extracting archive is caught), and sets a fresh invocation-private `sys.pycache_prefix` mechanically verified outside the repository (or served skill root when standalone) and retired at exit, refusing repo-, bundle-, `scripts/`-, allowed-data-, symlink-resolved-, and case-aliased internal temp roots before first-party import. The embedded policy is asserted equal to the contract section by a release-time test; `_require_boundary_match` re-checks it per invocation as defense-in-depth (post-import, because a pre-import runtime match is circular under this cut — the contract-loading machinery is the extracted module — and a weaker pre-import parse was rejected). **To be verified by** the runtime-boundary battery (seeded sourceless `.pyc`, stdlib shadow, real and prefixed disguised zips, policy tamper, embedded-vs-contract equality, bytecode-freshness probe, external-prefix lifecycle and unsafe-temp-root refusals including symlink and case aliases, predicate-vs-regex agreement), Gate-2 at two Python surfaces, dual-path smokes with the effective interpreter recorded, and exact-prompt end-to-end re-smokes on both runtimes per the debt-scan bar; the observed-proof sentence is added only after Tasks 6–7 pass (Task 7).
```

The verification clause is deliberately prospective ("To be verified by") because Tasks 6–7 have not run at this point and Task 7 may pause for JP or fail; Task 7 replaces it with an observed statement once both smoke tasks succeed.

Commit: `docs(deliberate): record v28 contract evolution in the spec lineage (proof pending)`.

## Task 6: Dual-path smoke and evidence record

Create `docs/smoke-tests/<execution date>_deliberate-v6-dual-path-runtime-boundary.md` recording, with commands and verbatim output:

1. Both delivery paths, live tree: `uv run --script <path>/scripts/deliberate-validate.py fixtures --data <path>/references/contract-data.yaml` and the `identity` probe, where `<path>` is (a) `/Users/jp/.agents/skills/deliberate` and (b) `~/.claude/skills/deliberate` (the symlink). Expect identical exit codes and `158/158`.
2. Gate-2 through both paths: `uv run --script <path>/tests/check_import_closure.py` → `agree: 2 Python surface(s)` twice.
3. Effective interpreter, recorded the way the Gate-1 spike did: run a throwaway probe script carrying the identical PEP 723 header (`requires-python = ">=3.11"`, `dependencies = ["pyyaml"]`) that prints `sys.executable` and `sys.version`, executed via `uv run --script` from both paths; put the script in the scratchpad, not the repo.
4. Startup latency: repeat the Task 0 timing loop; record before/after medians side by side. No pre-registered threshold exists; flag anything materially above baseline for JP rather than deciding alone.
5. The ADR obligation map — one line each stating where the evidence lives:

| ADR-0001 runtime obligation | Evidence |
| --- | --- |
| Seeded stale repo-local bytecode is ignored/refused | `test_seeded_pycache_directory_is_refused`, `test_seeded_sourceless_pyc_is_refused_without_executing` |
| Chosen prefix starts empty and outside the protected source root | `tempfile.mkdtemp` semantics + the external-success and unsafe-root branches of `test_cache_prefix_is_external_private_retired_and_unsafe_roots_refuse` |
| Second invocation cannot execute the first's cached code | `test_second_invocation_never_reuses_prior_bytecode` |
| No repo-local bytecode created or read | repo/bundle/`scripts/`/allowed-data/symlink/case-alias refusal branches of `test_cache_prefix_is_external_private_retired_and_unsafe_roots_refuse` + census `__pycache__` refusal |
| Seeded sourceless `.pyc` refused without executing | marker assertions in both `.pyc` tests |
| Both delivery paths, interpreter recorded | this smoke record, sections 1–3 |

Commit: `docs(deliberate): v6 dual-path runtime-boundary smoke record`.

## Task 7: Cross-runtime end-to-end re-smokes (the debt-scan bar)

The debt scan is explicit: "Re-run an exact Codex and Claude smoke after any physical topology change; fixtures and black-box CLI checks cannot prove runtime loading in both hosts." This task needs JP to fire live runs — flag it rather than skipping silently.

The exact prompt is durable and hash-pinned — do not re-derive it from a session store. It lives at `docs/smoke-tests/fixtures/2026-07-14-deliberate-exact-prompt.txt` (3,760 bytes, SHA-256 `253f1bfe697124f685124f03adb539f5f55005284cb4f107de598b2272493a82`; provenance in the sibling `README.md`). There is no 2026-07-14 deliberate smoke *record* in the repo — the accepted Codex run of 2026-07-14 is a session rollout, and the 07-15 records preserve only this SHA, not the bytes; this fixture closes that gap.

1. Verify the fixture before use: `shasum -a 256 docs/smoke-tests/fixtures/2026-07-14-deliberate-exact-prompt.txt` must print `253f1bfe…`. If it does not, stop — the input is corrupt.
2. Claude Code: feed the fixture verbatim as the invocation prompt; run all five stages to a validated close capsule.
3. Codex: feed the same fixture verbatim; run likewise.
4. Record both under `docs/smoke-tests/` following the existing records' shape, including the effective interpreter, the fixture SHA-256 as the input identity, and the eight-surface method identity in the capsule. **Commit the evidence** (`docs(deliberate): v6 cross-runtime end-to-end re-smoke records`) — every task commits (this one was previously implicit and is now explicit).
5. Only after both smokes pass, update the v28 spec lineage entry: replace **"To be verified by"** with **"Verified by"** and drop the trailing "the observed-proof sentence is added only after Tasks 6–7 pass (Task 7)." clause. Commit: `docs(deliberate): record observed v28 cross-runtime verification`.

A failure here is a v6 defect: diagnose before landing; do not weaken the boundary to pass, and do not perform step 5.

## Task 8: Closeout

1. Validation ladder: `git diff --check` on the branch range; re-run the full suite, fixtures, check-renderings, and Gate-2 one final time; `python3 -m json.tool docs/hardening/2026-07-16-deliberate-import-boundary/hardening.json > /dev/null`.
2. Review the whole branch diff (`git diff main...HEAD --stat`, then per-file, word-diff for prose).
3. Landing (`merge-branch` lane), pushing, and branch retirement (`fix/deliberate-gate2-*` are already retirement candidates) are JP's decisions — stop and report.

## Rollback

Every task commits a green tree, so rollback is `git revert` (or branch abandonment before landing) in reverse task order. Reverting Task 1 or 4 restores the prior `contract-data.yaml` hash and the seven-surface identity — that is a method-identity change like any other; the tactical Gate-2 protections (checker + tests) survive every rollback point because Task 2 only rebinds their value source.

## Self-review notes (already applied)

- Coverage check against ADR-0001's five runtime obligations, the portfolio's validation plan (mismatch test, runtime negative tests for every E005 class, external cache-prefix placement with unsafe repo/bundle/`scripts/`/allowed-data/symlink/case-alias temp-root refusals, dual-path, interpreter recording, latency baseline), and the decided open questions: each maps to a task above; the sole deliberate deviation is that cache-prefix *obligations* are not declared as policy data — they are behavior, proven by tests, with no mechanical consumer; the ADR amendment records this.
- Consistency: `_BOUNDARY_POLICY` keys equal the contract section minus `banned-identifiers` (no `zip-magics` — zip detection is structural); the checker requires the full key set; `_require_boundary_match` iterates only embedded keys, so the ban list never falsely mismatches; `test_embedded_runtime_policy_matches_contract_section` pins the embedding to the contract at release time.
- Ordering decision (2026-07-16 scrutiny, Blocker 2): the embedded census is authenticated by the entrypoint's own method-surface hash and by a release-time equality test; `_require_boundary_match` runs post-import as defense-in-depth because a pre-import *runtime* match is circular (the contract-loading machinery is the extracted first-party module) and a weaker pre-import parse was rejected. This is the deliberately-accepted weaker-than-"strong-form" boundary; ADR-0001 and the proposal are amended to say so.
- The characterization suite is the transcription-drift net for the moved block; expected test counts at each boundary: 39 → 43 → 46 → 57 → 59 (predictions until run; recompute if a test is added or split).

## Outside view

Reference class: this repo's own contract-evolution cuts on `deliberate` (v26, v27, the Gate-2 arc) — schema-plus-runtime changes under a hash-authenticated method identity. What that class reliably required beyond the obvious diff, and where this plan carries it: renderings regeneration and fixture reruns after any `contract-data.yaml` edit (Tasks 1.4, 4.5); companion prose surfaces that silently encode the old topology — `capsule.md`, `SKILL.md` bootstrap — found and edited explicitly (Task 4.4); live cross-runtime fires exposing what fixtures cannot (Task 7, the bar the debt scan pre-registered after v26/v27 each caught a defect only in live fire); interpreter variance recorded rather than pinned (Task 6.3, per the Gate-1 decision); and startup-latency evidence because the portfolio asked for a baseline before accepting runtime preflight cost (Tasks 0.3, 6.4). The class also warns that adversarial re-review finds what the author's own review missed — twice proven in Era 94, then a third time by the 2026-07-16 execution-readiness scrutiny of *this* plan: a valid prefixed/self-extracting zip imported through zipimport while the earlier "content-sniff the four-byte magic" repair passed it green, and the runtime equality check was placed after first-party import in contradiction of the proposal's ordering language. The first was fixed in the live Gate-2 census (`43065ca`, structural `zipfile.is_zipfile`) before this plan proceeds and is carried into the runtime pass 2; the second was resolved as an explicit, documented ordering decision (release-time authentication + post-import defense-in-depth) with ADR-0001 and the proposal amended. So the tactical Gate-2 tests are the floor plus one proven repair, and the plan adds tripwires rather than replacing anything. This is a debias against under-scoping, not a completeness certificate: the residuals named in ADR-0001 (reflection gadgets, native loaders, external `sys.path`) remain open by design, and platform evidence stays bounded to macOS + CPython 3.13 via `uv --script`.
