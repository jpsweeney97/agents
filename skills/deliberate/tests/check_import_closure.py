#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Gate-2 authoring check: first-party import closure vs `method-surfaces`.

Derives the root-inclusive transitive first-party import closure of the
deliberate validator entrypoint by AST parsing alone and requires exact
equality with the Python subset of the canonical
`validation.method-surfaces` inventory (ADR-0001, Rollout Boundary, gate 2).

Non-executing by design: importing the entrypoint or any production module
would execute code before the comparison and cross the authentication
boundary this check guards. Only ``ast.parse`` touches production sources.

Test tooling, deliberately outside `method-surfaces` (ADR-0001 consequence:
test-only harnesses never become authenticated production inputs).

Usage: ``uv run --script check_import_closure.py [skill-root]``; the root
defaults to this file's parent skill directory. Exit 0 on exact equality,
exit 1 with the delta otherwise.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import yaml


def top_level_import_names(source_path: Path) -> set[str]:
    """Return every top-level module name imported anywhere in the file.

    Walks the full AST so conditional and function-scoped imports count:
    any import statement can execute, so any import is closure-relevant.
    """
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                raise SystemExit(
                    "import-closure check failed: relative import is "
                    "unsupported in the script-directory layout. Got: "
                    f"level={node.level} in {source_path}"
                )
            if node.module:
                names.add(node.module.split(".")[0])
    return names


def resolve_first_party(name: str, scripts_dir: Path) -> Path | None:
    """Map an import name to a first-party file under scripts/, if present."""
    module = scripts_dir / f"{name}.py"
    if module.is_file():
        return module
    package_init = scripts_dir / name / "__init__.py"
    if package_init.is_file():
        return package_init
    return None


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
        for name in sorted(top_level_import_names(current)):
            resolved = resolve_first_party(name, scripts_dir)
            if resolved is not None and resolved.resolve() not in closure:
                pending.append(resolved.resolve())
    return closure


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
    """Require closure == inventory; return the pass message or exit 1."""
    root = skill_root.resolve()
    entrypoint = root / "scripts" / "deliberate-validate.py"
    contract_data = root / "references" / "contract-data.yaml"
    for required in (entrypoint, contract_data):
        if not required.is_file():
            raise SystemExit(
                f"import-closure check failed: required file missing. Got: {required}"
            )
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
    return f"import closure matches method-surfaces: {len(closure)} Python surface(s)"


if __name__ == "__main__":
    given_root = (
        Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    )
    print(check(given_root))
