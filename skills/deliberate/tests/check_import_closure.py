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

Structural rules enforced alongside the set comparison: production Python
is the entrypoint plus flat ``scripts/_deliberate_<domain>.py`` modules
only — no packages, no nested files, no name that could shadow a stdlib or
third-party import — and production sources may not use dynamic-import
machinery (``__import__``, ``importlib``), so the static closure stays
authoritative for what executes.

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
import re
import sys
from pathlib import Path

import yaml

ENTRYPOINT_NAME = "deliberate-validate.py"
MODULE_NAME = re.compile(r"^_deliberate_[a-z][a-z0-9_]*\.py$")
DYNAMIC_IMPORT_TOP_NAMES = frozenset({"importlib"})


def first_party_import_names(source_path: Path, scripts_dir: Path) -> set[str]:
    """Return every first-party module name imported anywhere in the file.

    Walks the full AST so conditional and function-scoped imports count:
    any import statement can execute, so any import is closure-relevant.
    Rejects relative imports, dotted first-party imports, and dynamic-import
    machinery — each would let executed code escape the static closure.
    """
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
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
        elif isinstance(node, ast.Name) and node.id == "__import__":
            raise SystemExit(
                "import-closure check failed: dynamic import machinery is "
                "forbidden in production sources (ADR-0001), because the "
                "static closure must be authoritative. Got: __import__ in "
                f"{source_path}"
            )
    names: set[str] = set()
    for dotted in dotted_names:
        top = dotted.split(".")[0]
        if top in DYNAMIC_IMPORT_TOP_NAMES:
            raise SystemExit(
                "import-closure check failed: dynamic import machinery is "
                "forbidden in production sources (ADR-0001), because the "
                f"static closure must be authoritative. Got: import of "
                f"{dotted!r} in {source_path}"
            )
        if (scripts_dir / f"{top}.py").is_file():
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


def production_python_files(scripts_dir: Path) -> set[Path]:
    """Every ``.py`` under scripts/, validated against the ADR-0001 layout.

    Fails on any nested or package layout and on any module name outside
    ``_deliberate_<domain>.py``; the required prefix structurally prevents a
    local module from shadowing a stdlib or third-party import.
    """
    files: set[Path] = set()
    for path in sorted(scripts_dir.rglob("*.py")):
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
        path.relative_to(root).as_posix()
        for path in production_python_files(scripts_dir)
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
