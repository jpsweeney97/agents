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
