#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Gate-2 authoring check: import closure vs `method-surfaces` vs on-disk files.

Derives three independent sets and requires exact pairwise equality
(ADR-0001, Rollout Boundary, gate 2):

1. the root-inclusive transitive first-party import closure of the
   deliberate validator entrypoint, derived by AST parsing alone;
2. the Python subset of the canonical ``validation.method-surfaces``
   inventory;
3. every production ``.py`` file physically present under ``scripts/``.

Alongside the set comparison, the same run enforces the complete ADR-0001
``scripts/`` layout, fail-closed:

- Production Python is the entrypoint plus flat
  ``scripts/_deliberate_<domain>.py`` regular files only; nested files,
  dotted first-party imports, and names that could shadow a stdlib or
  third-party import are rejected.
- A recursive census rejects every unexpected importable artifact anywhere
  under ``scripts/``: symlinks (file or directory, including symlinked
  packages), ``__pycache__`` entries, bytecode and extension-module files
  (any loader suffix other than flat source), zip-format archives
  (``.zip``/``.egg``/``.whl``, loadable through zipimport), and directories
  outside the declared data allowlist. Files with no loadable suffix are
  import-inert and permitted.
- A statically imported name with any local presence in ``scripts/`` other
  than its inventoried flat ``.py`` source is rejected rather than
  classified as third-party, so an import can never resolve to sourceless
  bytecode, a package directory, or a symlink.
- Dynamic-import and code-execution machinery is rejected by a positional
  identifier ban: a banned name used as an identifier (``ast.Name``) or as
  an imported module or symbol (``import`` / ``from ... import``) fails the
  check. The ban does not scan attribute names or string literals, so
  ordinary ``re.compile`` or the word "eval" in a docstring is not a false
  positive. Reaching import or exec machinery still requires naming a banned
  identifier or a reflection gadget; the gadget/computed-string residual is
  statically undetectable by design and is backstopped by the census
  guarantee that no loadable artifact sits uninventoried under ``scripts/``.
  Native-code loaders (for example ``ctypes`` loading a shared library) load
  outside the Python-module import graph and outside this gate's boundary.

Non-executing by design: importing the entrypoint or any production module
would execute code before the comparison and cross the authentication
boundary this check guards. Only ``ast.parse`` touches production sources.

Test tooling, deliberately outside `method-surfaces` (ADR-0001 consequence:
test-only harnesses never become authenticated production inputs).

Usage: ``uv run --script check_import_closure.py [skill-root]``; the root
defaults to this file's parent skill directory. Exit 0 on exact agreement,
exit 1 with the failure otherwise.
"""

from __future__ import annotations

import ast
import importlib.machinery
import re
import sys
from pathlib import Path

import yaml

ENTRYPOINT_NAME = "deliberate-validate.py"
MODULE_NAME = re.compile(r"^_deliberate_[a-z][a-z0-9_]*\.py$")
ALLOWED_DATA_DIRS = frozenset({"fixtures"})
BANNED_IDENTIFIERS = frozenset(
    {
        "__import__",
        "__builtins__",
        "builtins",
        "importlib",
        "zipimport",
        "runpy",
        "exec",
        "eval",
        "compile",
    }
)
# Every suffix the running interpreter's FileFinder can load, plus the
# cross-platform forms this platform does not register (.pyw/.pyc/.pyo/.pyd),
# so a census run on macOS still rejects artifacts another platform loads.
LOADER_SUFFIXES = frozenset(importlib.machinery.all_suffixes()) | {
    ".pyc",
    ".pyo",
    ".pyd",
    ".pyw",
    ".so",
}
ARTIFACT_SUFFIXES = tuple(sorted(s.lower() for s in LOADER_SUFFIXES if s != ".py"))
# Zip-format archives carry no FileFinder loader suffix but are loadable as
# code through zipimport / path hooks, so the census rejects them too — no
# importable artifact may sit beside the modules while the gate is green.
ARCHIVE_SUFFIXES = (".egg", ".whl", ".zip")
CENSUS_FORBIDDEN_SUFFIXES = tuple(
    sorted(set(ARTIFACT_SUFFIXES) | set(ARCHIVE_SUFFIXES))
)


def _reject_if_banned(name: str, node: ast.AST, source_path: Path) -> None:
    """Fail when any dotted segment of ``name`` is banned import/exec machinery."""
    for segment in name.split("."):
        if segment in BANNED_IDENTIFIERS:
            line = getattr(node, "lineno", "?")
            raise SystemExit(
                "import-closure check failed: dynamic import machinery is "
                "forbidden in production sources (ADR-0001), because the "
                f"static closure must be authoritative. Got: {segment!r} "
                f"(line {line}) in {source_path}"
            )


def reject_banned_identifiers(tree: ast.AST, source_path: Path) -> None:
    """Fail on named dynamic-import or code-execution machinery.

    The ban is positional, not textual: it fires on a banned name used as an
    identifier (``ast.Name``, any context) or as an imported module or symbol
    (``import`` / ``from ... import``). It deliberately does not scan attribute
    names or string literals, so ordinary ``re.compile`` or the word "eval" in
    a docstring is not a false positive. Reaching import or exec machinery
    still requires naming a banned identifier — ``__import__``, ``builtins``,
    ``__builtins__``, ``importlib``, ``zipimport``, ``runpy``, ``exec``,
    ``eval``, ``compile`` — or a reflection gadget; the gadget/computed-string
    residual is statically undetectable by design and is backstopped by the
    census guarantee that no loadable artifact sits uninventoried under
    ``scripts/``.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id in BANNED_IDENTIFIERS:
                raise SystemExit(
                    "import-closure check failed: dynamic import machinery is "
                    "forbidden in production sources (ADR-0001), because the "
                    f"static closure must be authoritative. Got: {node.id!r} "
                    f"(line {node.lineno}) in {source_path}"
                )
        elif isinstance(node, ast.Import):
            for alias in node.names:
                _reject_if_banned(alias.name, node, source_path)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                _reject_if_banned(node.module, node, source_path)
            for alias in node.names:
                _reject_if_banned(alias.name, node, source_path)


def classify_first_party(scripts_dir: Path, top: str, source_path: Path) -> bool:
    """True when ``top`` is a flat first-party module; fail on other local forms.

    Script-directory resolution tries every loader form, not just
    ``<top>.py`` — a sourceless ``.pyc``, an extension module, a package
    directory, or a symlink would each execute code the static closure never
    saw. Any such presence is rejected rather than classified.
    """
    flat = scripts_dir / f"{top}.py"
    other_forms = [scripts_dir / top] + [
        scripts_dir / f"{top}{suffix}" for suffix in ARTIFACT_SUFFIXES
    ]
    present = [p for p in other_forms if p.is_symlink() or p.exists()]
    if present:
        raise SystemExit(
            "import-closure check failed: a first-party import must resolve "
            "to a flat production source file, never bytecode, a package, or "
            f"a symlink (ADR-0001). Got: {top!r} in {source_path} also "
            f"resolvable to {[str(p) for p in present]}"
        )
    if flat.is_symlink():
        raise SystemExit(
            "import-closure check failed: a production module must be a "
            f"regular file, not a symlink (ADR-0001). Got: {flat}"
        )
    return flat.is_file()


def first_party_import_names(source_path: Path, scripts_dir: Path) -> set[str]:
    """Return every first-party module name imported anywhere in the file.

    Walks the full AST so conditional and function-scoped imports count:
    any import statement can execute, so any import is closure-relevant.
    Rejects relative imports, dotted first-party imports, dynamic-import
    machinery, and imports resolvable to non-flat-source local artifacts —
    each would let executed code escape the static closure.
    """
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    reject_banned_identifiers(tree, source_path)
    dotted_names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            dotted_names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                raise SystemExit(
                    "import-closure check failed: relative import is "
                    "unsupported in the script-directory layout. Got: "
                    f"level={node.level} in {source_path}"
                )
            if node.module:
                dotted_names.append(node.module)
    names: set[str] = set()
    for dotted in dotted_names:
        top = dotted.split(".")[0]
        if classify_first_party(scripts_dir, top, source_path):
            if "." in dotted:
                raise SystemExit(
                    "import-closure check failed: dotted import of a "
                    "first-party module is unsupported — production modules "
                    f"are flat files (ADR-0001). Got: {dotted!r} in "
                    f"{source_path}"
                )
            names.add(top)
    return names


def import_closure(entrypoint: Path) -> set[Path]:
    """Root-inclusive transitive first-party import closure, source-derived."""
    scripts_dir = entrypoint.parent
    closure: set[Path] = set()
    pending = [entrypoint.resolve()]
    while pending:
        current = pending.pop()
        if current in closure:
            continue
        closure.add(current)
        for name in sorted(first_party_import_names(current, scripts_dir)):
            resolved = (scripts_dir / f"{name}.py").resolve()
            if resolved not in closure:
                pending.append(resolved)
    return closure


ZIP_MAGICS = (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")


def _has_zip_magic(path: Path) -> bool:
    """True when the file begins with a zip local/central/spanned signature.

    Zip archives import as code through zipimport regardless of filename, so a
    disguised-suffix archive (``payload.dat``) added to ``sys.path`` would load
    without naming any banned identifier. Content-sniffing the four-byte magic
    closes that gap so the census guarantee — no loadable Python artifact sits
    uninventoried under ``scripts/`` — actually holds, which is what lets the
    identifier ban stay narrow (attribute names and string literals unscanned).
    """
    with path.open("rb") as handle:
        return handle.read(4) in ZIP_MAGICS


def census_scripts_layout(scripts_dir: Path) -> set[Path]:
    """Fail-closed census of everything under scripts/; returns production ``.py`` files.

    Rejects every unexpected importable artifact — symlinks, ``__pycache__``,
    bytecode and extension modules, zip-format archives (by suffix and by
    content signature), directories outside the declared data allowlist,
    nested or non-conforming ``.py`` — whether or not anything imports it.
    Files with no loadable suffix and no archive signature are import-inert
    and pass.
    """
    if scripts_dir.is_symlink():
        raise SystemExit(
            "import-closure check failed: scripts/ itself must be a real "
            f"directory, not a symlink (ADR-0001). Got: {scripts_dir}"
        )
    files: set[Path] = set()
    for path in sorted(scripts_dir.rglob("*")):
        if path.is_symlink():
            raise SystemExit(
                "import-closure check failed: symlinks are forbidden anywhere "
                "under scripts/ (ADR-0001) — a symlinked module or package "
                f"executes code outside the authenticated tree. Got: {path}"
            )
        if path.name == "__pycache__":
            raise SystemExit(
                "import-closure check failed: __pycache__ is forbidden under "
                "scripts/ (ADR-0001) — cached bytecode executes in place of "
                f"hashed source. Got: {path}"
            )
        if path.is_dir():
            top = path.relative_to(scripts_dir).parts[0]
            if top not in ALLOWED_DATA_DIRS:
                raise SystemExit(
                    "import-closure check failed: directories under scripts/ "
                    "are forbidden outside the declared data allowlist "
                    f"{sorted(ALLOWED_DATA_DIRS)} (ADR-0001) — a directory is "
                    f"an importable package. Got: {path}"
                )
            continue
        if not path.is_file():
            raise SystemExit(
                "import-closure check failed: unsupported filesystem object "
                f"under scripts/. Got: {path}"
            )
        lower_name = path.name.lower()
        if lower_name.endswith(".py"):
            if path.parent != scripts_dir:
                raise SystemExit(
                    "import-closure check failed: production Python must be flat "
                    "in scripts/ — packages and nested files are forbidden "
                    f"(ADR-0001). Got: {path}"
                )
            if path.name != ENTRYPOINT_NAME and not MODULE_NAME.match(path.name):
                raise SystemExit(
                    "import-closure check failed: production module name must "
                    "match _deliberate_<domain>.py (ADR-0001 naming rule). Got: "
                    f"{path}"
                )
            files.add(path.resolve())
            continue
        if any(lower_name.endswith(suffix) for suffix in CENSUS_FORBIDDEN_SUFFIXES):
            raise SystemExit(
                "import-closure check failed: importable non-source artifact "
                "is forbidden under scripts/ (ADR-0001) — bytecode, extension "
                "modules, and zip-format archives execute or import without "
                f"matching any hashed source. Got: {path}"
            )
        if _has_zip_magic(path):
            raise SystemExit(
                "import-closure check failed: file carries a zip archive "
                "signature despite an inert suffix (ADR-0001) — a disguised "
                "archive on sys.path imports as code through zipimport without "
                f"naming any banned identifier. Got: {path}"
            )
    return files


def inventory_python_surfaces(contract_data: Path) -> set[str]:
    """Python entries of validation.method-surfaces, as skill-relative paths."""
    loaded = yaml.safe_load(contract_data.read_text(encoding="utf-8"))
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


def check(skill_root: Path) -> str:
    """Require closure == inventory == on-disk; return the pass message or exit 1."""
    root = skill_root.resolve()
    scripts_dir = root / "scripts"
    entrypoint = scripts_dir / ENTRYPOINT_NAME
    contract_data = root / "references" / "contract-data.yaml"
    for required in (entrypoint, contract_data):
        if not required.is_file():
            raise SystemExit(
                f"import-closure check failed: required file missing. Got: {required}"
            )
    on_disk = {
        path.relative_to(root).as_posix() for path in census_scripts_layout(scripts_dir)
    }
    closure = {path.relative_to(root).as_posix() for path in import_closure(entrypoint)}
    inventory = inventory_python_surfaces(contract_data)
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


if __name__ == "__main__":
    given_root = (
        Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    )
    print(check(given_root))
