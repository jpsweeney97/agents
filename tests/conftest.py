"""Shared fixtures for the worktree_cycle helper tests.

Everything is hermetic: throwaway temp repos, a fake `trash` executable on
PATH (moves targets into a `.trashed/` dir instead of the real Trash), and
explicit session-identity env. Bytecode is neutralized so no __pycache__
ever lands in the plugin tree.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.pycache_prefix = os.path.join(tempfile.gettempdir(), "worktree-cycle-test-pycache")

REPO_ROOT = Path(__file__).resolve().parent.parent
HELPER = (
    REPO_ROOT
    / "plugins"
    / "git-cycle"
    / "skills"
    / "worktree-task-cycle"
    / "scripts"
    / "worktree_cycle.py"
)
CANONICAL_LOCK_REASON = "parked skill workspace (permanent)"
SESSION = "test-session-0001"


def sh(*args: str, cwd: Path, env: "dict[str, str] | None" = None) -> str:
    proc = subprocess.run(
        args, cwd=str(cwd), capture_output=True, text=True, env=env, check=False
    )
    assert proc.returncode == 0, f"{args} failed: {proc.stderr}"
    return proc.stdout.strip()


class Harness:
    """One temp primary repo plus N locked satellites and a helper runner."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.primary = root / "repo"
        self.trashed = root / ".trashed"
        self.bindir = root / "bin"
        self.primary.mkdir(parents=True)
        self.trashed.mkdir()
        self.bindir.mkdir()
        fake_trash = self.bindir / "trash"
        fake_trash.write_text(
            "#!/bin/sh\n"
            f'for p in "$@"; do mv "$p" "{self.trashed}/$(basename "$p").$$" || exit 1; done\n'
        )
        fake_trash.chmod(0o755)
        self.env_base = {
            "PATH": f"{self.bindir}:{os.environ['PATH']}",
            "HOME": os.environ.get("HOME", str(root)),
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@t",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        sh("git", "init", "-b", "main", ".", cwd=self.primary, env=self.git_env())
        (self.primary / "seed.txt").write_text("seed\n")
        (self.primary / ".gitignore").write_text("junk/\n*.tmp\n__pycache__/\n")
        self.commit("initial")
        store = self.primary / ".git" / "skill-worktree"
        (store / "leases").mkdir(parents=True)
        (store / "validations").mkdir()

    def git_env(self) -> "dict[str, str]":
        return dict(self.env_base)

    def helper_env(
        self, *, session: "str | None" = SESSION, codex: "str | None" = None
    ) -> "dict[str, str]":
        env = dict(self.env_base)
        if session is not None:
            env["CLAUDE_CODE_SESSION_ID"] = session
        if codex is not None:
            env["CODEX_THREAD_ID"] = codex
        return env

    def commit(self, message: str, cwd: "Path | None" = None) -> str:
        where = cwd or self.primary
        sh("git", "add", "-A", cwd=where, env=self.git_env())
        sh("git", "commit", "-m", message, cwd=where, env=self.git_env())
        return sh("git", "rev-parse", "HEAD", cwd=where, env=self.git_env())

    def add_satellite(
        self, name: str, *, locked: bool = True, reason: str = CANONICAL_LOCK_REASON
    ) -> Path:
        path = self.root / "repo-worktrees" / name
        path.parent.mkdir(exist_ok=True)
        sh(
            "git",
            "worktree",
            "add",
            "--detach",
            str(path),
            "main",
            cwd=self.primary,
            env=self.git_env(),
        )
        if locked:
            sh(
                "git",
                "worktree",
                "lock",
                "--reason",
                reason,
                str(path),
                cwd=self.primary,
                env=self.git_env(),
            )
        return path

    def run(self, *args: str, env: "dict[str, str] | None" = None) -> "tuple[int, str]":
        proc = subprocess.run(
            (sys.executable, str(HELPER), *args),
            capture_output=True,
            text=True,
            env=env if env is not None else self.helper_env(),
            check=False,
        )
        return proc.returncode, proc.stdout + proc.stderr

    def add_origin(self) -> Path:
        bare = self.root / "origin.git"
        sh(
            "git",
            "init",
            "--bare",
            "-b",
            "main",
            str(bare),
            cwd=self.root,
            env=self.git_env(),
        )
        sh(
            "git",
            "remote",
            "add",
            "origin",
            str(bare),
            cwd=self.primary,
            env=self.git_env(),
        )
        sh("git", "push", "-u", "origin", "main", cwd=self.primary, env=self.git_env())
        return bare

    def leases(self) -> Path:
        return self.primary / ".git" / "skill-worktree" / "leases"

    def validations(self) -> Path:
        return self.primary / ".git" / "skill-worktree" / "validations"


@pytest.fixture()
def harness(tmp_path: Path) -> Harness:
    return Harness(tmp_path)
