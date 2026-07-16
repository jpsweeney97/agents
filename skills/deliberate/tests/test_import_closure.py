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
    """Write a minimal skill layout: entrypoint, modules, contract data.

    Module keys are scripts-relative paths; nested keys create the parent
    directories so package layouts can be expressed (to prove rejection).
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
    assert message == (
        "import closure, on-disk production files, and method-surfaces "
        "agree: 3 Python surface(s)"
    )


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


def test_uninventoried_shadowing_module_is_detected(tmp_path: Path) -> None:
    """A local file taking a dependency's name violates the naming rule."""
    root = make_layout(
        tmp_path,
        "import yaml\n",
        {"yaml.py": "VALUE = 1\n"},
        ["scripts/deliberate-validate.py"],
    )
    with pytest.raises(
        SystemExit, match=r"must match _deliberate_<domain>\.py.*yaml\.py"
    ):
        check(root)


def test_inventoried_shadowing_module_is_detected(tmp_path: Path) -> None:
    """Inventorying the shadow file must not launder it past the naming rule."""
    root = make_layout(
        tmp_path,
        "import yaml\n",
        {"yaml.py": "VALUE = 1\n"},
        ["scripts/deliberate-validate.py", "scripts/yaml.py"],
    )
    with pytest.raises(
        SystemExit, match=r"must match _deliberate_<domain>\.py.*yaml\.py"
    ):
        check(root)


def test_dynamic_import_call_is_rejected(tmp_path: Path) -> None:
    """__import__ can execute first-party code the static closure never sees."""
    root = make_layout(
        tmp_path,
        '__import__("_deliberate_hidden")\n',
        {"_deliberate_hidden.py": "VALUE = 1\n"},
        ["scripts/deliberate-validate.py"],
    )
    with pytest.raises(
        SystemExit, match=r"dynamic import machinery is forbidden.*__import__"
    ):
        check(root)


def test_importlib_import_is_rejected(tmp_path: Path) -> None:
    """importlib is dynamic-import machinery regardless of how it is imported."""
    root = make_layout(
        tmp_path,
        "from importlib import import_module\n",
        {},
        ["scripts/deliberate-validate.py"],
    )
    with pytest.raises(
        SystemExit, match=r"dynamic import machinery is forbidden.*importlib"
    ):
        check(root)


def test_package_submodule_layout_is_rejected(tmp_path: Path) -> None:
    """A package under scripts/ executes files the flat closure cannot pin."""
    root = make_layout(
        tmp_path,
        "import _deliberate_pkg.sub\n",
        {
            "_deliberate_pkg/__init__.py": "",
            "_deliberate_pkg/sub.py": "VALUE = 1\n",
        },
        [
            "scripts/deliberate-validate.py",
            "scripts/_deliberate_pkg/__init__.py",
        ],
    )
    with pytest.raises(SystemExit, match=r"packages and nested files are forbidden"):
        check(root)


def test_dotted_first_party_import_is_rejected(tmp_path: Path) -> None:
    """A dotted first-party import has no meaning for flat production modules."""
    root = make_layout(
        tmp_path,
        "import _deliberate_shared.sub\n",
        {"_deliberate_shared.py": "VALUE = 1\n"},
        ["scripts/deliberate-validate.py", "scripts/_deliberate_shared.py"],
    )
    with pytest.raises(
        SystemExit, match=r"dotted import of a first-party module is unsupported"
    ):
        check(root)


def test_on_disk_orphan_module_is_detected(tmp_path: Path) -> None:
    """A conforming on-disk module outside closure and inventory must fail.

    This is the fail-closed backstop: any first-party file reachable only
    dynamically (or plain dead code) surfaces as an on-disk/inventory delta.
    """
    root = make_layout(
        tmp_path,
        "import os\n",
        {"_deliberate_orphan.py": "VALUE = 1\n"},
        ["scripts/deliberate-validate.py"],
    )
    with pytest.raises(
        SystemExit, match=r"On disk but not inventoried.*_deliberate_orphan"
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
    assert message == (
        "import closure, on-disk production files, and method-surfaces "
        "agree: 1 Python surface(s)"
    )
