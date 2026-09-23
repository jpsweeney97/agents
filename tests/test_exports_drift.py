"""Exercise export provenance reporting against disposable Git repositories."""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(
    os.environ.get(
        "SKILL_EXPORT_DRIFT_SCRIPT",
        str(Path(__file__).resolve().parents[1] / "scripts/exports-drift.sh"),
    )
)


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        [
            "git",
            "-c",
            "core.hooksPath=/dev/null",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "user.name=Export Test",
            "-c",
            "user.email=export-test@example.invalid",
            *args,
        ],
        cwd=repo,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def make_repo(tmp_path: Path, source: str = "skills/demo") -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "fixture")
    (repo / source).mkdir(parents=True)
    (repo / source / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Demo.\n---\nOriginal.\n"
    )
    (repo / "scripts").mkdir()
    shutil.copyfile(SCRIPT, repo / "scripts/exports-drift.sh")
    git(repo, "add", source, "scripts")
    git(repo, "commit", "-qm", "source")
    sha = git(repo, "rev-parse", "HEAD")
    export = repo / "exports/demo/SKILL.md"
    export.parent.mkdir(parents=True)
    export.write_text(
        f"---\nname: demo\ndescription: Demo.\n---\n<!-- export: {source}/ @ {sha} | 2026-09-23 | claude.ai -->\nOriginal.\n"
    )
    git(repo, "add", "exports")
    git(repo, "commit", "-qm", "export")
    return repo


def run_drift(
    repo: Path, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "scripts/exports-drift.sh"],
        cwd=repo,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def snapshot(repo: Path) -> dict[str, bytes]:
    return {
        str(p.relative_to(repo)): p.read_bytes()
        for p in repo.rglob("*")
        if p.is_file() and ".git" not in p.parts
    }


@pytest.mark.parametrize(
    "source", ["skills/demo", "skills-claude/demo", "plugins/example/skills/demo"]
)
def test_actual_source_directories_are_current(tmp_path: Path, source: str) -> None:
    repo = make_repo(tmp_path, source)
    before = snapshot(repo)
    result = run_drift(repo)
    assert result.returncode == 0, result.stderr
    assert "CURRENT: demo" in result.stdout
    assert source in result.stdout
    assert snapshot(repo) == before


def test_committed_change_is_stale_without_rewriting_export(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    (repo / "skills/demo/SKILL.md").write_text("Changed source.\n")
    git(repo, "add", "skills/demo")
    git(repo, "commit", "-qm", "change source")
    before = snapshot(repo)
    result = run_drift(repo)
    assert result.returncode == 0, result.stderr
    assert "STALE:" in result.stdout
    assert "CURRENT:" not in result.stdout
    assert snapshot(repo) == before


def test_unrelated_commit_does_not_make_export_stale(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    (repo / "other.txt").write_text("Unrelated.\n")
    git(repo, "add", "other.txt")
    git(repo, "commit", "-qm", "unrelated")
    result = run_drift(repo)
    assert result.returncode == 0, result.stderr
    assert "CURRENT:" in result.stdout


@pytest.mark.parametrize("kind", ["unstaged", "staged", "untracked", "deleted"])
def test_dirty_source_is_never_current(tmp_path: Path, kind: str) -> None:
    repo = make_repo(tmp_path)
    source = repo / "skills/demo/SKILL.md"
    if kind == "untracked":
        (source.parent / "new-reference.md").write_text("New reference.\n")
    elif kind == "deleted":
        source.rename(repo / "removed-source.md")
    else:
        source.write_text("Uncommitted source.\n")
        if kind == "staged":
            git(repo, "add", "skills/demo")
    before = snapshot(repo)
    result = run_drift(repo)
    assert result.returncode == 2
    assert "DIRTY:" in result.stdout
    assert "CURRENT:" not in result.stdout
    assert snapshot(repo) == before


@pytest.mark.parametrize("operation", ["log", "status"])
def test_failed_git_query_is_reported(tmp_path: Path, operation: str) -> None:
    repo = make_repo(tmp_path)
    bindir = tmp_path / "bin"
    bindir.mkdir()
    real_git = shutil.which("git")
    assert real_git
    wrapper = bindir / "git"
    wrapper.write_text(
        f'#!/bin/sh\nif [ "$1" = "{operation}" ]; then\n'
        '  echo "fixture query failure" >&2\n  exit 128\nfi\n'
        f'exec {shlex.quote(real_git)} "$@"\n'
    )
    wrapper.chmod(0o755)
    env = dict(os.environ, PATH=f"{bindir}:{os.environ['PATH']}")
    result = run_drift(repo, env)
    assert result.returncode == 2
    assert f"git {operation} failed" in result.stdout
    assert "CURRENT:" not in result.stdout
    assert "fixture query failure" in result.stderr


@pytest.mark.parametrize("problem", ["comment", "commit", "source"])
def test_invalid_provenance_is_not_current(tmp_path: Path, problem: str) -> None:
    repo = make_repo(tmp_path)
    export = repo / "exports/demo/SKILL.md"
    text = export.read_text()
    if problem == "comment":
        text = "No provenance.\n"
    elif problem == "commit":
        text = text.replace(git(repo, "rev-parse", "HEAD~1"), "deadbeef")
    else:
        text = text.replace("skills/demo/ @", "skills/absent/ @")
    export.write_text(text)
    result = run_drift(repo)
    assert result.returncode == 2
    assert "MALFORMED:" in result.stdout
    assert "CURRENT:" not in result.stdout
