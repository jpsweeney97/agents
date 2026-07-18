from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "scripts" / "create_simplify_backup.py"


def run(
    cmd: list[str],
    cwd: Path,
    *,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=check)


def run_backup(
    repo: Path,
    *paths: str,
    scope_slug: str = "orders",
) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    cmd = [
        sys.executable,
        str(BACKUP),
        "--scope-slug",
        scope_slug,
        "--planned-verification",
        "strong plan",
        "--retention",
        "keep until simplification review is complete",
        *paths,
    ]
    result = run(cmd, repo, check=False)
    assert result.stdout, result.stderr
    return result, json.loads(result.stdout)


def init_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    run(["git", "init", "-q"], repo)
    run(["git", "config", "user.email", "backup@example.test"], repo)
    run(["git", "config", "user.name", "Backup Test"], repo)
    return repo


def commit_all(repo: Path) -> str:
    run(["git", "add", "."], repo)
    run(["git", "commit", "-m", "baseline", "-q"], repo)
    return run(["git", "rev-parse", "HEAD"], repo).stdout.strip()


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def backup_files_text(artifact: Path) -> str:
    parts: list[str] = []
    for path in sorted(file for file in artifact.rglob("*") if file.is_file()):
        parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


def test_git_backup_copies_clean_file_and_records_evidence(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    source = write(repo / "pkg" / "orders.py", "def total() -> int:\n    return 42\n")
    head = commit_all(repo)

    result, payload = run_backup(repo, "pkg/orders.py")

    assert result.returncode == 0, result.stderr
    assert payload["ok"] is True
    assert payload["root"] == str(repo)
    assert payload["head"] == head
    artifact = Path(str(payload["artifact_path"]))
    assert artifact.is_dir()
    assert artifact.parent == repo / ".backup"
    assert (artifact / "files" / "pkg" / "orders.py").read_text(encoding="utf-8") == (
        source.read_text(encoding="utf-8")
    )
    assert (artifact / "status.txt").is_file()
    assert (artifact / "diff.patch").is_file()
    assert (artifact / "cached.diff.patch").is_file()
    assert (artifact / "untracked.txt").is_file()
    manifest = (artifact / "manifest.txt").read_text(encoding="utf-8")
    assert "scope: orders" in manifest
    assert "planned_verification: strong plan" in manifest
    assert "retention: keep until simplification review is complete" in manifest
    assert "pkg/orders.py" in manifest
    assert "backup_action: copied" in manifest
    assert "sha256:" in manifest
    assert ".backup/" in (repo / ".git" / "info" / "exclude").read_text(
        encoding="utf-8"
    )


def test_secret_file_is_excluded_by_default_and_marks_backup_inadequate(
    tmp_path: Path,
) -> None:
    repo = init_repo(tmp_path)
    secret_value = "sk-test-secret-value"
    write(repo / "pkg" / ".env", f'API_KEY="{secret_value}"\n')
    commit_all(repo)

    result, payload = run_backup(repo, "pkg/.env", scope_slug="secret")

    assert result.returncode == 1
    assert payload["ok"] is False
    artifact = Path(str(payload["artifact_path"]))
    assert artifact.is_dir()
    assert not (artifact / "files" / "pkg" / ".env").exists()
    manifest = (artifact / "manifest.txt").read_text(encoding="utf-8")
    assert "scope: secret" in manifest
    assert "pkg/.env" in manifest
    assert "backup_action: excluded" in manifest
    assert "restore_limit: not restorable from this artifact" in manifest
    assert secret_value not in backup_files_text(artifact)


def test_non_git_backup_uses_explicit_backup_root(tmp_path: Path) -> None:
    root = tmp_path / "plain"
    backup_root = tmp_path / "backups"
    source = write(root / "module.py", "VALUE = 1\n")

    cmd = [
        sys.executable,
        str(BACKUP),
        "--root",
        str(root),
        "--backup-root",
        str(backup_root),
        "--scope-slug",
        "plain",
        "--planned-verification",
        "moderate plan",
        str(source),
    ]
    result = run(cmd, root, check=False)
    assert result.stdout, result.stderr
    payload = json.loads(result.stdout)

    assert result.returncode == 0, result.stderr
    assert payload["ok"] is True
    assert payload["root"] == str(root)
    assert payload["head"] is None
    artifact = Path(str(payload["artifact_path"]))
    assert artifact.parent == backup_root
    assert (artifact / "files" / "module.py").read_text(
        encoding="utf-8"
    ) == "VALUE = 1\n"
    assert not (artifact / "status.txt").exists()


def test_failed_run_leaves_no_artifact_and_reports_real_args(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    write(repo / "pkg" / "orders.py", "VALUE = 3\n")
    commit_all(repo)
    outside = write(tmp_path / "outside.py", "VALUE = 4\n")

    cmd = [
        sys.executable,
        str(BACKUP),
        "--scope-slug",
        "outside",
        "--planned-verification",
        "strong plan",
        str(outside),
    ]
    result = run(cmd, repo, check=False)

    assert result.returncode == 2
    assert "path is outside root" in result.stderr
    assert "Got: None" not in result.stderr
    assert "--scope-slug" in result.stderr
    backup_root = repo / ".backup"
    assert not backup_root.exists() or not any(backup_root.iterdir())


def test_planned_verification_must_begin_with_strength_label(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    write(repo / "pkg" / "orders.py", "VALUE = 5\n")
    commit_all(repo)

    cmd = [
        sys.executable,
        str(BACKUP),
        "--scope-slug",
        "orders",
        "--planned-verification",
        "uv run pytest tests/test_orders.py -q",
        "pkg/orders.py",
    ]
    result = run(cmd, repo, check=False)

    assert result.returncode == 2
    assert "must begin with" in result.stderr
    assert "uv run pytest" in result.stderr
    backup_root = repo / ".backup"
    assert not backup_root.exists() or not any(backup_root.iterdir())


def test_planned_verification_accepts_label_with_detail(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    write(repo / "pkg" / "orders.py", "VALUE = 6\n")
    commit_all(repo)

    cmd = [
        sys.executable,
        str(BACKUP),
        "--scope-slug",
        "orders",
        "--planned-verification",
        "strong plan: focused tests then full suite",
        "pkg/orders.py",
    ]
    result = run(cmd, repo, check=False)
    assert result.stdout, result.stderr
    payload = json.loads(result.stdout)

    assert result.returncode == 0, result.stderr
    assert payload["ok"] is True
    artifact = Path(str(payload["artifact_path"]))
    manifest = (artifact / "manifest.txt").read_text(encoding="utf-8")
    assert (
        "planned_verification: strong plan: focused tests then full suite" in manifest
    )


def test_explicit_subdir_root_still_uses_git_root(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    source = write(repo / "app" / "module.py", "VALUE = 2\n")
    commit_all(repo)

    cmd = [
        sys.executable,
        str(BACKUP),
        "--root",
        str(repo / "app"),
        "--scope-slug",
        "module",
        "--planned-verification",
        "strong plan",
        str(source),
    ]
    result = run(cmd, repo, check=False)
    assert result.stdout, result.stderr
    payload = json.loads(result.stdout)

    assert result.returncode == 0, result.stderr
    assert payload["git"] is True
    assert payload["root"] == str(repo)
    artifact = Path(str(payload["artifact_path"]))
    assert artifact.parent == repo / ".backup"
    assert (artifact / "files" / "app" / "module.py").read_text(
        encoding="utf-8"
    ) == "VALUE = 2\n"
