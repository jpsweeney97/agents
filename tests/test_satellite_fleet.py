"""Hermetic fleet reconciliation and mutation tests for satellite-fleet.py."""

from __future__ import annotations

import os
import signal
import shutil
import subprocess
import sys
import importlib.util
import json
import time
from pathlib import Path

import pytest

SOURCE_ROOT = Path(__file__).resolve().parent.parent
SOURCE_FLEET = SOURCE_ROOT / "scripts" / "satellite-fleet.py"
SOURCE_HELPER = (
    SOURCE_ROOT
    / "plugins"
    / "git-cycle"
    / "skills"
    / "worktree-task-cycle"
    / "scripts"
    / "worktree_cycle.py"
)
CANONICAL_LOCK_REASON = "parked skill workspace (permanent)"
SESSION = "fleet-test-session"


def sh(*args: str, cwd: Path, env: "dict[str, str]") -> str:
    """Run one fixture command and return stdout."""

    proc = subprocess.run(
        args,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, f"{args} failed: {proc.stdout}{proc.stderr}"
    return proc.stdout.strip()


def snapshot_tree(root: Path) -> "dict[str, tuple[str, bytes | str]]":
    """Capture names, file bytes, and symlink targets without following links."""

    if not root.exists():
        return {}
    snapshot: "dict[str, tuple[str, bytes | str]]" = {}
    for path in sorted(root.rglob("*")):
        rel = str(path.relative_to(root))
        if path.is_symlink():
            snapshot[rel] = ("symlink", os.readlink(path))
        elif path.is_file():
            snapshot[rel] = ("file", path.read_bytes())
        elif path.is_dir():
            snapshot[rel] = ("dir", "")
    return snapshot


class FleetHarness:
    """One throwaway primary repo with its own fleet root and helper copy."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.primary = root / "repo"
        self.fleet_root = root / "repo-worktrees"
        self.bindir = root / "bin"
        self.trashed = root / ".trashed"
        self.primary.mkdir()
        self.fleet_root.mkdir()
        self.bindir.mkdir()
        self.trashed.mkdir()
        fake_trash = self.bindir / "trash"
        fake_trash.write_text(
            "#!/bin/sh\n"
            f'for p in "$@"; do mv "$p" "{self.trashed}/$(basename "$p").$$" || exit 1; done\n'
        )
        fake_trash.chmod(0o755)
        self.env = {
            "PATH": f"{self.bindir}:{os.environ['PATH']}",
            "HOME": os.environ.get("HOME", str(root)),
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@t",
            "PYTHONDONTWRITEBYTECODE": "1",
            "CLAUDE_CODE_SESSION_ID": SESSION,
        }
        sh("git", "init", "-b", "main", ".", cwd=self.primary, env=self.env)
        (self.primary / "seed.txt").write_text("seed\n")
        (self.primary / ".gitignore").write_text("__pycache__/\n.pytest_cache/\n")
        self.add_skill("skills", "alpha")
        self.add_skill("skills-claude", "beta")
        helper = (
            self.primary
            / "plugins"
            / "git-cycle"
            / "skills"
            / "worktree-task-cycle"
            / "scripts"
            / "worktree_cycle.py"
        )
        helper.parent.mkdir(parents=True)
        shutil.copy2(SOURCE_HELPER, helper)
        self.helper = helper
        fleet = self.primary / "scripts" / "satellite-fleet.py"
        fleet.parent.mkdir()
        shutil.copy2(SOURCE_FLEET, fleet)
        self.commit("fixture")
        store = self.primary / ".git" / "skill-worktree"
        (store / "leases").mkdir(parents=True)
        (store / "validations").mkdir()

    def add_skill(self, root: str, name: str) -> Path:
        """Add one live skill surface to the fixture working tree."""

        path = self.primary / root / name
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text(f"---\nname: {name}\n---\n")
        return path

    def commit(self, message: str) -> str:
        """Commit all fixture setup and return the new tip."""

        sh("git", "add", "-A", cwd=self.primary, env=self.env)
        sh("git", "commit", "-m", message, cwd=self.primary, env=self.env)
        return sh("git", "rev-parse", "HEAD", cwd=self.primary, env=self.env)

    def remove_skill(self, root: str, name: str) -> None:
        """Remove one fixture skill surface and commit the census change."""

        sh(
            "trash",
            str(self.primary / root / name),
            cwd=self.primary,
            env=self.env,
        )
        self.commit(f"remove {name}")

    def add_satellite(
        self,
        identity: str,
        *,
        locked: bool = True,
        reason: str = CANONICAL_LOCK_REASON,
        start: str = "main",
    ) -> Path:
        """Create one fixture satellite with a selected lock state."""

        path = self.fleet_root / identity
        args = ["git", "worktree", "add", "--detach"]
        if locked:
            args.extend(("--lock", "--reason", reason))
        args.extend((str(path), start))
        sh(*args, cwd=self.primary, env=self.env)
        return path

    def run(self, *args: str) -> "tuple[int, str]":
        """Run the copied fleet tool and return exit code plus combined output."""

        proc = subprocess.run(
            (
                sys.executable,
                str(self.primary / "scripts" / "satellite-fleet.py"),
                *args,
            ),
            cwd=str(self.primary),
            env=self.env,
            capture_output=True,
            text=True,
            check=False,
        )
        return proc.returncode, proc.stdout + proc.stderr

    def run_helper(self, *args: str) -> "tuple[int, str]":
        """Run the fixture's canonical helper copy."""

        proc = subprocess.run(
            (sys.executable, str(self.helper), *args),
            cwd=str(self.primary),
            env=self.env,
            capture_output=True,
            text=True,
            check=False,
        )
        return proc.returncode, proc.stdout + proc.stderr

    def plant_lease(self, identity: str, owner: dict) -> Path:
        """Plant one recovery fixture in the shared lease store."""

        lease = (
            self.primary / ".git" / "skill-worktree" / "leases" / f"wt-{identity}.lease"
        )
        lease.mkdir()
        (lease / "owner.json").write_text(json.dumps(owner))
        return lease

    def install_git_probe(
        self,
        *,
        fail_identity: "str | None" = None,
        fail_remove_identity: "str | None" = None,
        unlock_after_identity: "str | None" = None,
    ) -> Path:
        """Install a delegating git probe with optional worktree-add sabotage."""

        real_git = shutil.which("git", path=os.environ["PATH"])
        assert real_git
        log = self.root / "git-invocations.jsonl"
        wrapper = self.bindir / "git"
        wrapper.write_text(
            "#!/usr/bin/env python3\n"
            "import json, pathlib, subprocess, sys\n"
            f"real = {real_git!r}\n"
            f"log = pathlib.Path({str(log)!r})\n"
            f"fail_identity = {fail_identity!r}\n"
            f"fail_remove_identity = {fail_remove_identity!r}\n"
            f"unlock_after_identity = {unlock_after_identity!r}\n"
            "args = sys.argv[1:]\n"
            "with log.open('a') as fh: fh.write(json.dumps(args) + '\\n')\n"
            "is_add = args[:2] == ['worktree', 'add']\n"
            "is_remove = args[:2] == ['worktree', 'remove']\n"
            "target = pathlib.Path(args[-2] if is_add else args[-1]) if (is_add or is_remove) else None\n"
            "if is_add and fail_identity and target.name == fail_identity:\n"
            "    print('fixture refused worktree add', file=sys.stderr)\n"
            "    raise SystemExit(55)\n"
            "if is_remove and fail_remove_identity and target.name == fail_remove_identity:\n"
            "    print('fixture refused worktree remove', file=sys.stderr)\n"
            "    raise SystemExit(56)\n"
            "proc = subprocess.run([real, *args])\n"
            "if proc.returncode == 0 and is_add and unlock_after_identity and target.name == unlock_after_identity:\n"
            "    subprocess.run([real, 'worktree', 'unlock', str(target)], check=True)\n"
            "raise SystemExit(proc.returncode)\n"
        )
        wrapper.chmod(0o755)
        return log


@pytest.fixture()
def fleet(tmp_path: Path) -> FleetHarness:
    return FleetHarness(tmp_path)


def test_check_reports_healthy_and_missing_without_mutation(
    fleet: FleetHarness,
) -> None:
    fleet.add_satellite("alpha")
    worktree_admin = fleet.primary / ".git" / "worktrees"
    lease_store = fleet.primary / ".git" / "skill-worktree" / "leases"
    before = (
        snapshot_tree(worktree_admin),
        snapshot_tree(fleet.fleet_root),
        snapshot_tree(lease_store),
    )

    code, out = fleet.run("check")

    assert code == 3, out
    assert "FACT: census=2" in out
    assert "FACT: primary-head=" in out and "dirty=false" in out
    assert "RESULT: OK-PARKED identity=alpha" in out
    assert "RESULT: MISSING identity=beta" in out
    assert "RESULT: check exit=3" in out
    after = (
        snapshot_tree(worktree_admin),
        snapshot_tree(fleet.fleet_root),
        snapshot_tree(lease_store),
    )
    assert after == before


@pytest.mark.parametrize(
    ("locked", "reason", "classification"),
    [
        (False, CANONICAL_LOCK_REASON, "LOCK-ABSENT"),
        (True, "temporary operator lock", "LOCK-NONCANONICAL"),
        (True, "initializing", "INIT-RESIDUE"),
    ],
)
def test_check_classifies_lock_drift(
    fleet: FleetHarness,
    locked: bool,
    reason: str,
    classification: str,
) -> None:
    fleet.add_satellite("alpha", locked=locked, reason=reason)

    code, out = fleet.run("check")

    assert code == 2, out
    assert f"RESULT: {classification} identity=alpha" in out


def test_check_classifies_active_task_lane(fleet: FleetHarness) -> None:
    sat = fleet.add_satellite("alpha")
    branch = "feature/alpha--fixture"
    code, out = fleet.run_helper(
        "lease-acquire",
        str(sat),
        "--branch",
        branch,
        "--purpose",
        "test active lane",
    )
    assert code == 0, out
    code, out = fleet.run_helper(
        "activate", str(sat), "--base", "main", "--branch", branch
    )
    assert code == 0, out

    code, out = fleet.run("check")

    assert code == 3, out  # beta remains ordinary catch-up work
    assert "RESULT: ACTIVE identity=alpha detail=helper-state=CONTAINED-UNPARKED" in out


def test_check_classifies_self_fleet_operation(fleet: FleetHarness) -> None:
    sat = fleet.add_satellite("alpha")
    code, out = fleet.run_helper(
        "fleet-lease-acquire",
        str(fleet.primary),
        "--identity",
        "alpha",
        "--path",
        str(sat),
        "--purpose",
        "fleet:repair",
    )
    assert code == 0, out

    code, out = fleet.run("check")

    assert code == 3, out
    assert "RESULT: FLEET-OP identity=alpha" in out


def test_check_classifies_foreign_lease_as_recovery(fleet: FleetHarness) -> None:
    fleet.add_satellite("alpha")
    fleet.plant_lease(
        "alpha",
        {
            "session_id": "foreign-session",
            "runtime": "claude-code",
            "worktree": "alpha",
            "branch": None,
            "purpose": "fleet:repair",
        },
    )

    code, out = fleet.run("check")

    assert code == 2, out
    assert "RESULT: RECOVERY:LEASE-ORPHANED identity=alpha" in out


def test_check_surfaces_helper_recovery_state_verbatim(fleet: FleetHarness) -> None:
    sat = fleet.add_satellite("alpha")
    sh(
        "git",
        "switch",
        "-c",
        "feature/orphan",
        cwd=sat,
        env=fleet.env,
    )
    (sat / "orphan.txt").write_text("orphan\n")
    sh("git", "add", "orphan.txt", cwd=sat, env=fleet.env)
    sh("git", "commit", "-m", "orphan", cwd=sat, env=fleet.env)
    sh("git", "switch", "--detach", "HEAD", cwd=sat, env=fleet.env)

    code, out = fleet.run("check")

    assert code == 2, out
    assert "RESULT: RECOVERY:PARKED-ORPHAN identity=alpha" in out


def test_check_distinguishes_retired_pending_from_missing(fleet: FleetHarness) -> None:
    fleet.add_satellite("alpha")
    fleet.remove_skill("skills", "alpha")

    code, out = fleet.run("check")

    assert code == 3, out
    assert "RESULT: RETIRED-PENDING identity=alpha" in out
    assert "RESULT: MISSING identity=beta" in out


def test_check_classifies_stale_admin_without_calling_it_missing(
    fleet: FleetHarness,
) -> None:
    sat = fleet.add_satellite("alpha")
    sh("trash", str(sat), cwd=fleet.primary, env=fleet.env)

    code, out = fleet.run("check")

    assert code == 2, out
    assert "RESULT: STALE-ADMIN identity=alpha" in out
    assert "RESULT: MISSING identity=alpha" not in out


def test_check_classifies_unregistered_expected_directory(
    fleet: FleetHarness,
) -> None:
    (fleet.fleet_root / "alpha").mkdir()

    code, out = fleet.run("check")

    assert code == 2, out
    assert "RESULT: UNEXPECTED-DIR identity=alpha" in out


def test_check_classifies_symlink_at_expected_path_without_following(
    fleet: FleetHarness,
) -> None:
    outside = fleet.root / "outside"
    outside.mkdir()
    (fleet.fleet_root / "alpha").symlink_to(outside, target_is_directory=True)

    code, out = fleet.run("check")

    assert code == 2, out
    assert "RESULT: SYMLINK-PATH identity=alpha" in out
    assert not any(outside.iterdir())


def test_check_classifies_symlinked_fleet_root_as_drift(
    fleet: FleetHarness,
) -> None:
    sh("trash", str(fleet.fleet_root), cwd=fleet.primary, env=fleet.env)
    outside = fleet.root / "outside-root"
    outside.mkdir()
    fleet.fleet_root.symlink_to(outside, target_is_directory=True)

    code, out = fleet.run("check")

    assert code == 2, out
    assert "RESULT: SYMLINK-PATH identity=<fleet-root>" in out
    assert not any(outside.iterdir())


def test_check_classifies_non_directory_expected_path_as_unmappable(
    fleet: FleetHarness,
) -> None:
    (fleet.fleet_root / "alpha").write_text("not a checkout\n")

    code, out = fleet.run("check")

    assert code == 2, out
    assert "RESULT: UNMAPPABLE identity=alpha" in out


def test_check_treats_registered_runtime_worktree_as_foreign_information(
    fleet: FleetHarness,
) -> None:
    runtime = fleet.root / "runtime-worktrees" / "session-1"
    runtime.parent.mkdir()
    sh(
        "git",
        "worktree",
        "add",
        "--detach",
        str(runtime),
        "main",
        cwd=fleet.primary,
        env=fleet.env,
    )

    code, out = fleet.run("check")

    assert code == 3, out
    assert "RESULT: FOREIGN-WORKTREE identity=session-1" in out


def test_check_refuses_canonical_permanent_satellite_outside_fleet_root(
    fleet: FleetHarness,
) -> None:
    misplaced = fleet.root / "elsewhere" / "alpha"
    misplaced.parent.mkdir()
    sh(
        "git",
        "worktree",
        "add",
        "--detach",
        "--lock",
        "--reason",
        CANONICAL_LOCK_REASON,
        str(misplaced),
        "main",
        cwd=fleet.primary,
        env=fleet.env,
    )

    code, out = fleet.run("check")

    assert code == 2, out
    assert "RESULT: UNMAPPABLE identity=alpha" in out
    assert "RESULT: MISSING identity=alpha" not in out
    code, create = fleet.run("create", "alpha")
    assert code == 2, create
    assert "UNMAPPABLE" in create
    assert not (fleet.fleet_root / "alpha").exists()


def test_check_propagates_optional_locks_zero_to_helper(fleet: FleetHarness) -> None:
    fleet.add_satellite("alpha")
    real_helper = fleet.helper.with_name("worktree_cycle_real.py")
    shutil.copy2(fleet.helper, real_helper)
    marker = fleet.root / "helper-env.txt"
    fleet.helper.write_text(
        "#!/usr/bin/env python3\n"
        "import os, pathlib, sys\n"
        f"pathlib.Path({str(marker)!r}).write_text(os.environ.get('GIT_OPTIONAL_LOCKS', '<missing>'))\n"
        f"os.execv(sys.executable, [sys.executable, {str(real_helper)!r}, *sys.argv[1:]])\n"
    )

    code, out = fleet.run("check")

    assert code == 3, out
    assert marker.read_text() == "0"


def test_create_uses_atomic_locked_add_and_proves_parked(
    fleet: FleetHarness,
) -> None:
    log = fleet.install_git_probe()

    code, out = fleet.run("create", "alpha")

    assert code == 0, out
    assert "RESULT: CREATED identity=alpha" in out
    code, check = fleet.run("check")
    assert code == 3, check
    assert "RESULT: OK-PARKED identity=alpha" in check
    invocations = [json.loads(line) for line in log.read_text().splitlines()]
    adds = [args for args in invocations if args[:2] == ["worktree", "add"]]
    assert len(adds) == 1
    assert adds[0][:6] == [
        "worktree",
        "add",
        "--detach",
        "--lock",
        "--reason",
        CANONICAL_LOCK_REASON,
    ]
    assert adds[0][-1] == "main"
    assert not any(arg.startswith("--force") for args in invocations for arg in args)


def test_create_is_idempotent_over_healthy_existing_satellite(
    fleet: FleetHarness,
) -> None:
    fleet.add_satellite("alpha")
    (fleet.primary / "advance.txt").write_text("advance main\n")
    fleet.commit("advance main past parked satellite")
    before = snapshot_tree(fleet.primary / ".git" / "worktrees")

    code, out = fleet.run("create", "alpha")

    assert code == 0, out
    assert "RESULT: ALREADY-OK identity=alpha" in out
    assert snapshot_tree(fleet.primary / ".git" / "worktrees") == before


def test_create_refuses_path_adoption_and_non_census_identity(
    fleet: FleetHarness,
) -> None:
    planted = fleet.fleet_root / "alpha"
    planted.mkdir()

    code, out = fleet.run("create", "alpha")
    assert code == 2, out
    assert "UNEXPECTED-DIR" in out and "refused" in out
    assert planted.is_dir()

    code, out = fleet.run("create", "not-a-skill")
    assert code == 2, out
    assert "not in the immutable census" in out


@pytest.mark.parametrize("primary_state", ["dirty", "off-main"])
def test_create_requires_clean_primary_on_main(
    fleet: FleetHarness,
    primary_state: str,
) -> None:
    if primary_state == "dirty":
        (fleet.primary / "dirty.txt").write_text("dirty\n")
    else:
        sh("git", "switch", "-c", "feature/off-main", cwd=fleet.primary, env=fleet.env)

    code, out = fleet.run("create", "alpha")

    assert code == 2, out
    assert "primary preflight refused" in out
    assert not (fleet.fleet_root / "alpha").exists()


def test_create_reports_created_but_not_parked_and_stops(
    fleet: FleetHarness,
) -> None:
    fleet.install_git_probe(unlock_after_identity="alpha")

    code, out = fleet.run("create", "alpha")

    assert code == 2, out
    assert "CREATED-BUT-NOT-PARKED" in out
    assert (fleet.fleet_root / "alpha").is_dir()
    code, check = fleet.run("check")
    assert code == 2, check
    assert "RESULT: LOCK-ABSENT identity=alpha" in check


def test_create_missing_stops_at_first_failure_with_explicit_summary(
    fleet: FleetHarness,
) -> None:
    fleet.add_skill("skills", "gamma")
    fleet.commit("add gamma")
    fleet.install_git_probe(fail_identity="beta")

    code, out = fleet.run("create-missing")

    assert code == 2, out
    assert "RESULT: create-missing completed=alpha refused=beta untouched=gamma" in out
    assert (fleet.fleet_root / "alpha").is_dir()
    assert not (fleet.fleet_root / "beta").exists()
    assert not (fleet.fleet_root / "gamma").exists()


def test_create_missing_converges_all_missing_identities(fleet: FleetHarness) -> None:
    code, out = fleet.run("create-missing")

    assert code == 0, out
    assert (
        "RESULT: create-missing completed=alpha,beta refused=none untouched=none" in out
    )
    code, check = fleet.run("check")
    assert code == 0, check
    assert check.count("RESULT: OK-PARKED identity=") == 2


def test_create_missing_skips_current_and_aged_healthy_pilot_replicas(
    fleet: FleetHarness,
) -> None:
    aged = fleet.add_satellite("alpha")
    (fleet.primary / "advance.txt").write_text("advance\n")
    fleet.commit("advance main")
    current = fleet.add_satellite("beta")
    before = snapshot_tree(fleet.primary / ".git" / "worktrees")

    code, out = fleet.run("create-missing")

    assert code == 0, out
    assert "completed=none refused=none untouched=none" in out
    assert snapshot_tree(fleet.primary / ".git" / "worktrees") == before
    assert aged.is_dir() and current.is_dir()


def test_create_missing_refuses_unfinished_fleet_operation(
    fleet: FleetHarness,
) -> None:
    sat = fleet.add_satellite("alpha")
    code, out = fleet.run_helper(
        "fleet-lease-acquire",
        str(fleet.primary),
        "--identity",
        "alpha",
        "--path",
        str(sat),
        "--purpose",
        "fleet:repair",
    )
    assert code == 0, out

    code, out = fleet.run("create-missing")

    assert code == 2, out
    assert "unfinished fleet operation" in out
    assert not (fleet.fleet_root / "beta").exists()


def test_create_inspects_only_the_target_identity(fleet: FleetHarness) -> None:
    fleet.add_satellite("alpha")
    real_helper = fleet.helper.with_name("worktree_cycle_real.py")
    shutil.copy2(fleet.helper, real_helper)
    log = fleet.root / "helper-inspects.txt"
    fleet.helper.write_text(
        "#!/usr/bin/env python3\n"
        "import os, pathlib, sys\n"
        f"real = {str(real_helper)!r}\n"
        f"log = pathlib.Path({str(log)!r})\n"
        "if len(sys.argv) > 2 and sys.argv[1] == 'inspect':\n"
        "    with log.open('a') as fh: fh.write(pathlib.Path(sys.argv[2]).name + '\\n')\n"
        "os.execv(sys.executable, [sys.executable, real, *sys.argv[1:]])\n"
    )
    fleet.commit("install helper invocation probe")

    code, out = fleet.run("create", "beta")

    assert code == 0, out
    assert log.read_text().splitlines() == ["beta"]


def test_repair_refuses_named_state_mismatch_before_lease(fleet: FleetHarness) -> None:
    fleet.add_satellite("alpha", locked=False)

    code, out = fleet.run("repair", "alpha", "--state", "STALE-ADMIN")

    assert code == 2, out
    assert "named state STALE-ADMIN does not match live LOCK-ABSENT" in out
    assert not (
        fleet.primary / ".git" / "skill-worktree" / "leases" / "wt-alpha.lease"
    ).exists()


def test_repair_refuses_any_preexisting_identity_lease(fleet: FleetHarness) -> None:
    fleet.add_satellite("alpha", locked=False)
    lease = fleet.plant_lease(
        "alpha",
        {
            "session_id": SESSION,
            "runtime": "claude-code",
            "worktree": "alpha",
            "branch": None,
            "purpose": "fleet:prior",
        },
    )

    code, out = fleet.run("repair", "alpha", "--state", "LOCK-ABSENT")

    assert code == 2, out
    assert "identity lease already exists" in out
    assert lease.is_dir()


def test_repair_lock_absent_relocks_and_releases(fleet: FleetHarness) -> None:
    fleet.add_satellite("alpha", locked=False)

    code, out = fleet.run("repair", "alpha", "--state", "LOCK-ABSENT")

    assert code == 0, out
    assert "RESULT: REPAIRED identity=alpha state=LOCK-ABSENT terminal=healthy" in out
    code, check = fleet.run("check")
    assert code == 3, check
    assert "RESULT: OK-PARKED identity=alpha" in check


def test_repair_noncanonical_lock_requires_exact_reason_echo(
    fleet: FleetHarness,
) -> None:
    fleet.add_satellite("alpha", reason="operator hold")

    code, out = fleet.run(
        "repair",
        "alpha",
        "--state",
        "LOCK-NONCANONICAL",
        "--confirm-reason",
        "wrong",
    )
    assert code == 2, out
    assert "confirmation reason mismatch" in out

    code, out = fleet.run(
        "repair",
        "alpha",
        "--state",
        "LOCK-NONCANONICAL",
        "--confirm-reason",
        "operator hold",
    )
    assert code == 0, out
    assert "terminal=healthy" in out


def test_repair_initializing_residue_is_report_only_without_fixture_proof(
    fleet: FleetHarness,
) -> None:
    fleet.add_satellite("alpha", reason="initializing")

    code, out = fleet.run("repair", "alpha", "--state", "INIT-RESIDUE")

    assert code == 2, out
    assert "report-only" in out and "native interrupted-add fixture" in out
    assert not (
        fleet.primary / ".git" / "skill-worktree" / "leases" / "wt-alpha.lease"
    ).exists()


def test_native_interrupted_add_does_not_prove_initializing_route(
    fleet: FleetHarness,
) -> None:
    marker = fleet.root / "smudge-started"
    release = fleet.root / "smudge-release"
    slow_filter = fleet.root / "slow_filter.py"
    slow_filter.write_text(
        "import pathlib, sys, time\n"
        "payload = sys.stdin.buffer.read()\n"
        f"pathlib.Path({str(marker)!r}).write_text('started')\n"
        f"release = pathlib.Path({str(release)!r})\n"
        "while not release.exists(): time.sleep(0.01)\n"
        "sys.stdout.buffer.write(payload)\n"
    )
    sh(
        "git",
        "config",
        "filter.slow.smudge",
        f"{sys.executable} {slow_filter}",
        cwd=fleet.primary,
        env=fleet.env,
    )
    (fleet.primary / ".gitattributes").write_text("slow.txt filter=slow\n")
    (fleet.primary / "slow.txt").write_text("slow\n")
    fleet.commit("add slow checkout fixture")
    target = fleet.fleet_root / "alpha"
    proc = subprocess.Popen(
        (
            "git",
            "worktree",
            "add",
            "--detach",
            "--lock",
            str(target),
            "main",
        ),
        cwd=str(fleet.primary),
        env=fleet.env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    deadline = time.monotonic() + 5
    while not marker.exists() and proc.poll() is None and time.monotonic() < deadline:
        time.sleep(0.01)
    assert marker.exists(), proc.communicate(timeout=1)
    os.killpg(proc.pid, signal.SIGKILL)
    proc.wait(timeout=5)

    registry = sh(
        "git", "worktree", "list", "--porcelain", cwd=fleet.primary, env=fleet.env
    )
    assert str(target) in registry
    assert "locked added with --lock" in registry
    assert "locked initializing" not in registry
    code, out = fleet.run("check")
    assert code == 2, out
    assert "RESULT: LOCK-NONCANONICAL identity=alpha" in out


def test_repair_stale_admin_decommissions_without_force_or_prune(
    fleet: FleetHarness,
) -> None:
    sat = fleet.add_satellite("alpha")
    sh("trash", str(sat), cwd=fleet.primary, env=fleet.env)
    log = fleet.install_git_probe()

    code, out = fleet.run("repair", "alpha", "--state", "STALE-ADMIN")

    assert code == 0, out
    assert "terminal=decommissioned" in out
    assert "alpha" not in sh(
        "git", "worktree", "list", "--porcelain", cwd=fleet.primary, env=fleet.env
    )
    invocations = [json.loads(line) for line in log.read_text().splitlines()]
    assert ["worktree", "remove", str(sat.resolve())] in invocations
    assert not any("prune" in args for args in invocations)
    assert not any(arg.startswith("--force") for args in invocations for arg in args)


def test_repair_symlink_trashes_link_itself_and_leaves_target_untouched(
    fleet: FleetHarness,
) -> None:
    outside = fleet.root / "outside"
    outside.mkdir()
    marker = outside / "marker.txt"
    marker.write_text("keep\n")
    link = fleet.fleet_root / "alpha"
    link.symlink_to(outside, target_is_directory=True)

    code, out = fleet.run(
        "repair",
        "alpha",
        "--state",
        "SYMLINK-PATH",
        "--confirm",
        "alpha",
    )

    assert code == 0, out
    assert "terminal=decommissioned" in out
    assert not link.exists() and not link.is_symlink()
    assert marker.read_text() == "keep\n"


def test_check_and_repair_moved_worktree_from_proven_backpointer(
    fleet: FleetHarness,
) -> None:
    old_root = fleet.root / "old-fleet"
    old_root.mkdir()
    old = old_root / "alpha"
    sh(
        "git",
        "worktree",
        "add",
        "--detach",
        "--lock",
        "--reason",
        CANONICAL_LOCK_REASON,
        str(old),
        "main",
        cwd=fleet.primary,
        env=fleet.env,
    )
    old.rename(fleet.fleet_root / "alpha")

    code, check = fleet.run("check")
    assert code == 2, check
    assert "RESULT: MOVED-WORKTREE identity=alpha" in check

    code, out = fleet.run(
        "repair",
        "alpha",
        "--state",
        "MOVED-WORKTREE",
        "--confirm",
        "alpha",
    )
    assert code == 0, out
    assert "terminal=healthy" in out
    code, check = fleet.run("check")
    assert code == 3, check
    assert "RESULT: OK-PARKED identity=alpha" in check


def test_moved_worktree_repair_also_handles_census_absent_identity(
    fleet: FleetHarness,
) -> None:
    old_root = fleet.root / "old-fleet"
    old_root.mkdir()
    old = old_root / "alpha"
    sh(
        "git",
        "worktree",
        "add",
        "--detach",
        "--lock",
        "--reason",
        CANONICAL_LOCK_REASON,
        str(old),
        "main",
        cwd=fleet.primary,
        env=fleet.env,
    )
    fleet.remove_skill("skills", "alpha")
    old.rename(fleet.fleet_root / "alpha")

    code, check = fleet.run("check")
    assert code == 2, check
    assert "RESULT: MOVED-WORKTREE identity=alpha" in check
    code, out = fleet.run(
        "repair",
        "alpha",
        "--state",
        "MOVED-WORKTREE",
        "--confirm",
        "alpha",
    )
    assert code == 0, out
    code, check = fleet.run("check")
    assert code == 3, check
    assert "RESULT: RETIRED-PENDING identity=alpha" in check


def test_retire_requires_census_absence(fleet: FleetHarness) -> None:
    fleet.add_satellite("alpha")

    code, out = fleet.run("retire", "alpha")

    assert code == 2, out
    assert "still present in the immutable census" in out
    assert (fleet.fleet_root / "alpha").is_dir()


def test_retire_decommissions_census_absent_parked_satellite(
    fleet: FleetHarness,
) -> None:
    sat = fleet.add_satellite("alpha", start="HEAD~0")
    fleet.remove_skill("skills", "alpha")

    code, out = fleet.run("retire", "alpha")

    assert code == 0, out
    assert "RESULT: RETIRED identity=alpha terminal=decommissioned" in out
    assert not sat.exists()


def test_unwind_requires_exact_confirmation_then_decommissions_live_identity(
    fleet: FleetHarness,
) -> None:
    sat = fleet.add_satellite("alpha")

    code, out = fleet.run("unwind", "alpha", "--confirm", "wrong")
    assert code == 2, out
    assert "confirmation mismatch" in out
    assert sat.is_dir()

    code, out = fleet.run("unwind", "alpha", "--confirm", "alpha")
    assert code == 0, out
    assert "RESULT: UNWOUND identity=alpha terminal=decommissioned" in out
    assert not sat.exists()


def test_failed_remove_retains_fleet_lease_as_recovery_signal(
    fleet: FleetHarness,
) -> None:
    fleet.add_satellite("alpha")
    fleet.remove_skill("skills", "alpha")
    fleet.install_git_probe(fail_remove_identity="alpha")

    code, out = fleet.run("retire", "alpha")

    assert code == 2, out
    assert "lease retained" in out
    lease = fleet.primary / ".git" / "skill-worktree" / "leases" / "wt-alpha.lease"
    assert lease.is_dir()


def load_fleet_module(tmp_path: Path):
    """Load the production fleet module for pure identity tests."""

    sys.pycache_prefix = str(tmp_path / "pycache")
    spec = importlib.util.spec_from_file_location("satellite_fleet", SOURCE_FLEET)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["satellite_fleet"] = module
    spec.loader.exec_module(module)
    return module


def test_identity_assignment_detects_casefold_collision_after_prefixing(
    tmp_path: Path,
) -> None:
    module = load_fleet_module(tmp_path)
    surfaces = [
        module.SkillSurface(tmp_path / "skills" / "X", "X", "skills", (0, "")),
        module.SkillSurface(tmp_path / "Plug" / "x", "x", "Plug", (2, "plug")),
        module.SkillSurface(tmp_path / "plug" / "X", "X", "plug", (2, "plug")),
    ]

    inventory = module.assign_inventory(surfaces, set())

    assert inventory.collisions
    assert "Plug--x" in inventory.by_identity
    assert "plug--X" in inventory.by_identity
    assert module.Finding("CASE-COLLISION", "x").exit_code == 2


def test_identity_assignment_preserves_existing_prefixed_identity(
    tmp_path: Path,
) -> None:
    module = load_fleet_module(tmp_path)
    claude = module.SkillSurface(
        tmp_path / "skills-claude" / "same", "same", "claude", (1, "")
    )

    inventory = module.assign_inventory([claude], {"claude--same"})

    assert inventory.by_identity == {"claude--same": claude}


def test_identity_assignment_rejects_casefold_collision_in_existing_fleet(
    tmp_path: Path,
) -> None:
    module = load_fleet_module(tmp_path)
    surface = module.SkillSurface(
        tmp_path / "skills" / "alpha", "alpha", "skills", (0, "")
    )

    inventory = module.assign_inventory([surface], {"alpha", "ALPHA"})

    assert any("existing immutable identities" in item for item in inventory.collisions)


def test_identity_assignment_detects_literal_vs_prefixed_alias(
    tmp_path: Path,
) -> None:
    module = load_fleet_module(tmp_path)
    literal = module.SkillSurface(
        tmp_path / "skills" / "claude--same",
        "claude--same",
        "skills",
        (0, ""),
    )
    senior = module.SkillSurface(
        tmp_path / "skills" / "same", "same", "skills", (0, "")
    )
    junior = module.SkillSurface(
        tmp_path / "skills-claude" / "same", "same", "claude", (1, "")
    )

    inventory = module.assign_inventory([literal, senior, junior], set())

    assert any("aliases both" in item for item in inventory.collisions)


@pytest.mark.parametrize(
    ("classification", "exit_code"),
    [
        ("OK-PARKED", 0),
        ("ACTIVE", 0),
        ("FLEET-OP", 0),
        ("FOREIGN-WORKTREE", 0),
        ("MISSING", 3),
        ("RETIRED-PENDING", 3),
        ("LOCK-ABSENT", 2),
        ("RECOVERY:PARKED-ORPHAN", 2),
        ("UNMAPPABLE", 2),
    ],
)
def test_classification_exit_contract(
    tmp_path: Path, classification: str, exit_code: int
) -> None:
    module = load_fleet_module(tmp_path)
    assert module.Finding(classification, "x").exit_code == exit_code


def test_missing_helper_is_labeled_internal_error(fleet: FleetHarness) -> None:
    fleet.add_satellite("alpha")
    fleet.helper.rename(fleet.helper.with_suffix(".missing"))

    code, out = fleet.run("check")

    assert code == 1, out
    assert "RESULT: internal-error" in out


def test_force_flag_guard_refuses_before_git_invocation(tmp_path: Path) -> None:
    module = load_fleet_module(tmp_path)
    for force in ("--force", "-f", "-ff"):
        with pytest.raises(
            module.FleetInternalError, match="force flags are prohibited"
        ):
            module.run_git("worktree", "remove", force, "/tmp/never")


def test_argument_errors_keep_labeled_refusal_contract(fleet: FleetHarness) -> None:
    code, out = fleet.run("repair", "alpha", "--state", "NOT-A-STATE")
    assert code == 2, out
    assert "REFUSE: argument parsing failed" in out
    assert "RESULT: refused" in out
