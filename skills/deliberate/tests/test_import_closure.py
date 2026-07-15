"""Gate-2 checker tests: synthetic layouts prove detection; the live tree must pass.

The checker is non-executing by contract, so these tests exercise it against
throwaway skill layouts on disk — never by importing production code.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from check_import_closure import check, import_closure

SKILL_ROOT = Path(__file__).resolve().parents[1]


def make_layout(
    root: Path,
    entry_body: str,
    modules: dict[str, str],
    surfaces: list[str],
) -> Path:
    """Write a minimal skill layout: entrypoint, modules, contract data."""
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "deliberate-validate.py").write_text(entry_body, encoding="utf-8")
    for name, body in modules.items():
        (scripts / name).write_text(body, encoding="utf-8")
    references = root / "references"
    references.mkdir()
    listed = "\n".join(f"    - {surface}" for surface in surfaces)
    (references / "contract-data.yaml").write_text(
        f"validation:\n  method-surfaces:\n{listed}\n", encoding="utf-8"
    )
    return root


def test_exact_closure_passes_and_ignores_external_imports(tmp_path: Path) -> None:
    """Sibling, transitive, and function-scoped imports count; stdlib does not."""
    root = make_layout(
        tmp_path,
        "import os\nimport yaml\nimport _deliberate_shared\n",
        {
            "_deliberate_shared.py": (
                "def load():\n    import _deliberate_util\n    return _deliberate_util\n"
            ),
            "_deliberate_util.py": "VALUE = 1\n",
        },
        [
            "SKILL.md",
            "scripts/deliberate-validate.py",
            "scripts/_deliberate_shared.py",
            "scripts/_deliberate_util.py",
        ],
    )
    message = check(root)
    assert message == "import closure matches method-surfaces: 3 Python surface(s)"


def test_omitted_module_is_detected(tmp_path: Path) -> None:
    """A module the entrypoint reaches but the inventory omits must fail."""
    root = make_layout(
        tmp_path,
        "import _deliberate_shared\n",
        {
            "_deliberate_shared.py": "import _deliberate_util\n",
            "_deliberate_util.py": "VALUE = 1\n",
        },
        ["scripts/deliberate-validate.py", "scripts/_deliberate_shared.py"],
    )
    with pytest.raises(
        SystemExit, match=r"Imported but not inventoried.*_deliberate_util"
    ):
        check(root)


def test_unimported_inventory_entry_is_detected(tmp_path: Path) -> None:
    """A pinned Python surface nothing imports must fail (dead inventory)."""
    root = make_layout(
        tmp_path,
        "import os\n",
        {"_deliberate_ghost.py": "VALUE = 1\n"},
        ["scripts/deliberate-validate.py", "scripts/_deliberate_ghost.py"],
    )
    with pytest.raises(
        SystemExit, match=r"inventoried but never imported.*_deliberate_ghost"
    ):
        check(root)


def test_dependency_shadowing_module_is_detected(tmp_path: Path) -> None:
    """A local file taking a dependency's name enters the closure and fails."""
    root = make_layout(
        tmp_path,
        "import yaml\n",
        {"yaml.py": "VALUE = 1\n"},
        ["scripts/deliberate-validate.py"],
    )
    with pytest.raises(
        SystemExit, match=r"Imported but not inventoried.*scripts/yaml\.py"
    ):
        check(root)


def test_relative_import_fails_fast(tmp_path: Path) -> None:
    """Relative imports have no meaning in the script-directory layout."""
    root = make_layout(
        tmp_path,
        "from . import anything\n",
        {},
        ["scripts/deliberate-validate.py"],
    )
    with pytest.raises(SystemExit, match=r"relative import is unsupported"):
        check(root)


def test_live_tree_passes_with_entrypoint_only_closure() -> None:
    """Pre-v6 reality: the closure is exactly the entrypoint, and the gate passes."""
    entrypoint = SKILL_ROOT / "scripts" / "deliberate-validate.py"
    assert import_closure(entrypoint) == {entrypoint.resolve()}
    message = check(SKILL_ROOT)
    assert message == "import closure matches method-surfaces: 1 Python surface(s)"
