"""Guard, state-mapping, collision, and refusal coverage for worktree_cycle.py.

Every test runs the helper as a subprocess against a hermetic temp repo
(see conftest.Harness) unless noted (the merge-target pin test runs the
module in-process to spy on the git calls); nothing here touches the real
.agents repo or its satellites.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

from conftest import HELPER, SESSION, Harness, sh

FIXTURES = Path(__file__).parent / "fixtures" / "worktree-cycle"


def acquire(h: Harness, sat: Path, branch: str = "feature/t1") -> None:
    code, out = h.run(
        "lease-acquire", str(sat), "--branch", branch, "--purpose", "test"
    )
    assert code == 0, out


def acquire_fleet(
    h: Harness,
    identity: str,
    expected: Path,
    purpose: str = "fleet:repair",
) -> None:
    code, out = h.run(
        "fleet-lease-acquire",
        str(h.primary),
        "--identity",
        identity,
        "--path",
        str(expected),
        "--purpose",
        purpose,
    )
    assert code == 0, out


def activate(h: Harness, sat: Path, branch: str = "feature/t1") -> None:
    acquire(h, sat, branch)
    code, out = h.run("activate", str(sat), "--base", "main", "--branch", branch)
    assert code == 0, out


def work_and_record(h: Harness, sat: Path, filename: str = "work.txt") -> str:
    (sat / filename).write_text("work\n")
    tip = h.commit("task work", cwd=sat)
    code, out = h.run("record-validation", str(sat), "--ladder", "test-ladder")
    assert code == 0, out
    return tip


def load_helper(tmp_path: Path):
    sys.pycache_prefix = str(tmp_path / "pycache")
    spec = importlib.util.spec_from_file_location("worktree_cycle", HELPER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["worktree_cycle"] = module
    spec.loader.exec_module(module)
    return module


def plant_lease(h: Harness, name: str, owner: dict) -> Path:
    lease = h.leases() / name
    lease.mkdir()
    (lease / "owner.json").write_text(json.dumps(owner))
    return lease


def snapshot_bytes(root: Path) -> "dict[str, bytes]":
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


# ---------------------------------------------------------------- inspect


def test_inspect_primary_overview(harness: Harness) -> None:
    harness.add_satellite("skill-a")
    code, out = harness.run("inspect", str(harness.primary), "--base", "main")
    assert code == 0 and "STATE: PRIMARY" in out


def test_inspect_parked(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: PARKED" in out


def test_inspect_emits_canonical_lock_token(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0, out
    assert "FACT: lock=canonical" in out


def test_inspect_emits_absent_lock_token(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a", locked=False)
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0, out
    assert "FACT: lock=absent" in out


def test_inspect_emits_noncanonical_lock_token(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a", reason="initializing")
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0, out
    assert "FACT: lock=noncanonical" in out


def test_inspect_emits_absent_lease_tokens(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0, out
    assert "FACT: lease=absent" in out
    assert "FACT: lease-purpose=none" in out


def test_inspect_emits_self_task_lease_tokens(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat)
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0, out
    assert "FACT: lease=self" in out
    assert "FACT: lease-purpose=task" in out


def test_inspect_emits_self_fleet_lease_tokens(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    plant_lease(
        harness,
        "wt-skill-a.lease",
        {
            "session_id": SESSION,
            "runtime": "claude-code",
            "worktree": "skill-a",
            "branch": None,
            "purpose": "fleet:repair",
        },
    )
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0, out
    assert "FACT: lease=self" in out
    assert "FACT: lease-purpose=fleet" in out


def test_inspect_emits_foreign_lease_token(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    plant_lease(
        harness,
        "wt-skill-a.lease",
        {
            "session_id": "other-session",
            "runtime": "claude-code",
            "worktree": "skill-a",
            "branch": "feature/t1",
            "purpose": "test",
        },
    )
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0, out
    assert "FACT: lease=foreign" in out
    assert "FACT: lease-purpose=task" in out


def test_inspect_emits_unreadable_lease_token(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    lease = harness.leases() / "wt-skill-a.lease"
    lease.mkdir()
    (lease / "owner.json").write_text("not-json")
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0, out
    assert "FACT: lease=unreadable" in out
    assert "FACT: lease-purpose=unknown" in out


def test_inspect_emits_scope_mismatch_lease_token(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    plant_lease(
        harness,
        "wt-skill-a.lease",
        {
            "session_id": SESSION,
            "runtime": "claude-code",
            "worktree": "different-skill",
            "branch": "feature/t1",
            "purpose": "test",
        },
    )
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0, out
    assert "FACT: lease=scope-mismatch" in out
    assert "FACT: lease-purpose=task" in out


@pytest.mark.parametrize(
    ("locked", "reason", "lock_token"),
    [
        (True, "parked skill workspace (permanent)", "canonical"),
        (True, "initializing", "noncanonical"),
        (False, "parked skill workspace (permanent)", "absent"),
    ],
)
@pytest.mark.parametrize(
    ("lease_token", "owner"),
    [
        ("absent", None),
        (
            "self",
            {
                "session_id": SESSION,
                "runtime": "claude-code",
                "worktree": "skill-a",
                "branch": "feature/t1",
                "purpose": "test",
            },
        ),
        (
            "foreign",
            {
                "session_id": "other-session",
                "runtime": "claude-code",
                "worktree": "skill-a",
                "branch": "feature/t1",
                "purpose": "test",
            },
        ),
        ("unreadable", "not-json"),
        (
            "scope-mismatch",
            {
                "session_id": SESSION,
                "runtime": "claude-code",
                "worktree": "different-skill",
                "branch": "feature/t1",
                "purpose": "test",
            },
        ),
    ],
)
def test_inspect_lock_by_lease_machine_token_matrix(
    harness: Harness,
    locked: bool,
    reason: str,
    lock_token: str,
    lease_token: str,
    owner: "dict | str | None",
) -> None:
    sat = harness.add_satellite("skill-a", locked=locked, reason=reason)
    if owner is not None:
        lease = harness.leases() / "wt-skill-a.lease"
        lease.mkdir()
        (lease / "owner.json").write_text(
            json.dumps(owner) if isinstance(owner, dict) else owner
        )
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0, out
    assert f"FACT: lock={lock_token}" in out
    assert f"FACT: lease={lease_token}" in out


def test_inspect_freshly_activated_is_contained_unparked(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: CONTAINED-UNPARKED" in out
    assert "provenance unproven" in out


def test_inspect_dirty_tree_is_in_flight(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "wip.txt").write_text("uncommitted\n")
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: IN-FLIGHT" in out


def test_inspect_ready_and_committed_unlanded(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: READY" in out
    lease = harness.leases() / "wt-skill-a.lease"
    lease.rename(harness.root / "lease-removed")
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: COMMITTED-UNLANDED" in out


def test_inspect_ready_invalid_when_tip_moves_past_record(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    (sat / "more.txt").write_text("more\n")
    harness.commit("more work", cwd=sat)
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: READY-INVALID" in out


def test_inspect_detached_dirty_is_unmappable(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    (sat / "stray.txt").write_text("stray\n")
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 2 and "STATE: UNMAPPABLE" in out


def test_inspect_parked_orphan(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    (sat / "orphan.txt").write_text("orphan\n")
    harness.commit("orphan commit", cwd=sat)
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: PARKED-ORPHAN" in out


def test_inspect_ds_store_stays_parked(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    (sat / ".DS_Store").write_text("\x00")
    (harness.primary / ".git" / "info" / "exclude").write_text(".DS_Store\n")
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: PARKED" in out


def test_inspect_parked_undeleted(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 0, out
    code, out = harness.run("park", str(sat), "--base", "main")
    assert code == 0, out
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: PARKED-UNDELETED" in out
    assert "feature/t1" in out


def test_inspect_foreign_lease_on_parked_is_lease_orphaned(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    plant_lease(
        harness,
        "wt-skill-a.lease",
        {
            "session_id": "someone-else",
            "runtime": "claude-code",
            "worktree": "skill-a",
            "branch": "feature/x",
            "purpose": "p",
        },
    )
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: LEASE-ORPHANED" in out


def test_inspect_identityless_lease_on_parked_is_lease_orphaned(
    harness: Harness,
) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat)
    code, out = harness.run(
        "inspect", str(sat), "--base", "main", env=harness.helper_env(session=None)
    )
    assert code == 0 and "STATE: LEASE-ORPHANED" in out
    assert "owner unknown" in out or "not verified SELF" in out


def test_inspect_refuses_unpinned_base(harness: Harness) -> None:
    # the review counterexample: 'other' EXISTS but is not the primary's branch,
    # and the satellite tip is not contained in it — 1.5.0 classified this
    # PARKED-ORPHAN at exit 0 instead of refusing the unpinned base
    sh("git", "branch", "other", cwd=harness.primary, env=harness.git_env())
    (harness.primary / "advance.txt").write_text("x\n")
    harness.commit("advance main")
    sat = harness.add_satellite("skill-a")
    code, out = harness.run("inspect", str(sat), "--base", "other")
    assert code == 2 and "does not match the primary checkout's branch" in out
    assert "STATE:" not in out, "no lifecycle state may be asserted from a wrong base"


def test_inspect_active_branch_foreign_lease_is_lease_orphaned(
    harness: Harness,
) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    owner_file = harness.leases() / "wt-skill-a.lease" / "owner.json"
    owner = json.loads(owner_file.read_text())
    owner["session_id"] = "someone-else"
    owner_file.write_text(json.dumps(owner))
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: LEASE-ORPHANED" in out
    assert "COMMITTED-UNLANDED" not in out


def test_inspect_landed_unparked_foreign_lease_is_lease_orphaned(
    harness: Harness,
) -> None:
    # crash between land and park, recovered by a different session: the
    # foreign lease outranks the contained-healthy classification
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 0, out
    code, out = harness.run(
        "inspect", str(sat), "--base", "main", env=harness.helper_env(session="rescuer")
    )
    assert code == 0 and "STATE: LEASE-ORPHANED" in out
    assert "LANDED-UNPARKED" not in out


def test_inspect_landed_unparked_under_self_lease(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 0, out
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: LANDED-UNPARKED" in out


# ---------------------------------------------------------------- identity


def test_no_identity_refuses_lease_verbs(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    env = harness.helper_env(session=None)
    code, out = harness.run(
        "lease-acquire", str(sat), "--branch", "feature/t1", "--purpose", "p", env=env
    )
    assert code == 2 and "no session identity" in out


def test_both_identities_refuse_with_escape_hatch(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    env = harness.helper_env(session="s1", codex="c1")
    code, out = harness.run(
        "lease-acquire", str(sat), "--branch", "feature/t1", "--purpose", "p", env=env
    )
    assert code == 2 and "ambiguous session identity" in out and "env -u" in out


def test_inspect_runs_without_identity(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    code, out = harness.run(
        "inspect", str(sat), "--base", "main", env=harness.helper_env(session=None)
    )
    assert code == 0 and "STATE: PARKED" in out


def test_inspect_with_optional_locks_disabled_is_byte_read_only(
    harness: Harness,
) -> None:
    sat = harness.add_satellite("skill-a")
    admin = harness.primary / ".git" / "worktrees"
    before = snapshot_bytes(admin)
    env = harness.helper_env()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    code, out = harness.run("inspect", str(sat), "--base", "main", env=env)
    assert code == 0, out
    assert snapshot_bytes(admin) == before


# ---------------------------------------------------------------- leases


def test_lease_reacquire_same_scope_reenters(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat)
    code, out = harness.run(
        "lease-acquire", str(sat), "--branch", "feature/t1", "--purpose", "test"
    )
    assert code == 0 and "re-entering" in out


def test_lease_reacquire_different_scope_refuses(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat)
    code, out = harness.run(
        "lease-acquire", str(sat), "--branch", "feature/OTHER", "--purpose", "test"
    )
    assert code == 2 and "DIFFERENT scope" in out


def test_foreign_lease_refuses(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat)
    env = harness.helper_env(session="another-session")
    code, out = harness.run(
        "lease-acquire",
        str(sat),
        "--branch",
        "feature/t1",
        "--purpose",
        "test",
        env=env,
    )
    assert code == 2 and "FOREIGN" in out


def test_unreadable_lease_fails_closed(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat)
    (harness.leases() / "wt-skill-a.lease" / "owner.json").write_text("not json")
    code, out = harness.run(
        "lease-acquire", str(sat), "--branch", "feature/t1", "--purpose", "test"
    )
    assert code == 2 and "unreadable" in out and "user-authorized" in out


def test_lease_release_mid_task_refused(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    code, out = harness.run("lease-release", str(sat), "--base", "main")
    assert code == 2 and "mid-task" in out


def test_lease_release_when_parked(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat)
    code, out = harness.run("lease-release", str(sat), "--base", "main")
    assert code == 0 and "released" in out
    assert not (harness.leases() / "wt-skill-a.lease").exists()


def test_fleet_lease_acquire_protects_absent_identity(harness: Harness) -> None:
    expected = harness.root / "repo-worktrees" / "skill-new"
    code, out = harness.run(
        "fleet-lease-acquire",
        str(harness.primary),
        "--identity",
        "skill-new",
        "--path",
        str(expected),
        "--purpose",
        "fleet:create",
    )
    assert code == 0, out
    lease = harness.leases() / "wt-skill-new.lease"
    owner = json.loads((lease / "owner.json").read_text())
    assert owner["worktree"] == "skill-new"
    assert owner["branch"] is None
    assert owner["purpose"] == "fleet:create"
    assert owner["expected_path"] == str(expected)
    assert owner["fingerprint"]["path_kind"] == "absent"
    assert owner["fingerprint"]["registered_paths"] == []


def test_fleet_lease_reentry_refuses_different_expected_path(
    harness: Harness,
) -> None:
    expected = harness.root / "repo-worktrees" / "skill-new"
    other = harness.root / "elsewhere" / "skill-new"
    code, out = harness.run(
        "fleet-lease-acquire",
        str(harness.primary),
        "--identity",
        "skill-new",
        "--path",
        str(expected),
        "--purpose",
        "fleet:create",
    )
    assert code == 0, out
    code, out = harness.run(
        "fleet-lease-acquire",
        str(harness.primary),
        "--identity",
        "skill-new",
        "--path",
        str(other),
        "--purpose",
        "fleet:create",
    )
    assert code == 2, out
    assert "expected-path" in out and "DIFFERENT scope" in out


@pytest.mark.parametrize(
    ("locked", "reason", "expected_lock"),
    [
        (False, "", False),
        (True, "initializing", True),
    ],
)
def test_fleet_lease_acquire_fingerprints_damaged_registered_identity(
    harness: Harness,
    locked: bool,
    reason: str,
    expected_lock: bool,
) -> None:
    sat = harness.add_satellite(
        "skill-a",
        locked=locked,
        reason=reason or "parked skill workspace (permanent)",
    )
    acquire_fleet(harness, "skill-a", sat)
    owner = json.loads(
        (harness.leases() / "wt-skill-a.lease" / "owner.json").read_text()
    )
    assert owner["fingerprint"]["path_kind"] == "directory"
    assert owner["fingerprint"]["registered_paths"] == [str(sat.resolve())]
    assert owner["fingerprint"]["lock"][0]["locked"] is expected_lock


def test_fleet_lease_acquire_fingerprints_stale_admin(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    sat.rename(harness.root / "moved-aside")
    acquire_fleet(harness, "skill-a", sat)
    owner = json.loads(
        (harness.leases() / "wt-skill-a.lease" / "owner.json").read_text()
    )
    assert owner["fingerprint"]["path_kind"] == "absent"
    assert owner["fingerprint"]["registered_paths"] == [str(sat.resolve())]


def test_fleet_lease_acquire_fingerprints_symlink_without_following(
    harness: Harness,
) -> None:
    expected = harness.root / "repo-worktrees" / "skill-a"
    expected.parent.mkdir()
    outside = harness.root / "outside"
    outside.mkdir()
    expected.symlink_to(outside, target_is_directory=True)
    acquire_fleet(harness, "skill-a", expected)
    owner = json.loads(
        (harness.leases() / "wt-skill-a.lease" / "owner.json").read_text()
    )
    assert owner["expected_path"] == str(expected)
    assert owner["fingerprint"]["path_kind"] == "symlink"
    assert owner["fingerprint"]["registered_paths"] == []


def test_fleet_lease_acquire_refuses_unsafe_identity(harness: Harness) -> None:
    expected = harness.root / "repo-worktrees" / "skill-a"
    code, out = harness.run(
        "fleet-lease-acquire",
        str(harness.primary),
        "--identity",
        "../escape",
        "--path",
        str(expected),
        "--purpose",
        "fleet:repair",
    )
    assert code == 2, out
    assert "one safe path segment" in out
    assert not any(harness.leases().iterdir())


def test_fleet_lease_release_accepts_bare_terminal_shape(harness: Harness) -> None:
    expected = harness.root / "repo-worktrees" / "skill-new"
    code, out = harness.run(
        "fleet-lease-acquire",
        str(harness.primary),
        "--identity",
        "skill-new",
        "--path",
        str(expected),
        "--purpose",
        "fleet:create",
    )
    assert code == 0, out
    code, out = harness.run(
        "fleet-lease-release",
        str(harness.primary),
        "--identity",
        "skill-new",
        "--path",
        str(expected),
    )
    assert code == 0, out
    assert "terminal=bare" in out
    assert not (harness.leases() / "wt-skill-new.lease").exists()


def test_fleet_lease_release_accepts_healthy_terminal_shape(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    code, out = harness.run(
        "fleet-lease-acquire",
        str(harness.primary),
        "--identity",
        "skill-a",
        "--path",
        str(sat),
        "--purpose",
        "fleet:repair",
    )
    assert code == 0, out
    code, out = harness.run(
        "fleet-lease-release",
        str(harness.primary),
        "--identity",
        "skill-a",
        "--path",
        str(sat),
    )
    assert code == 0, out
    assert "terminal=healthy" in out
    assert not (harness.leases() / "wt-skill-a.lease").exists()


def test_fleet_lease_release_accepts_decommissioned_terminal_shape(
    harness: Harness,
) -> None:
    sat = harness.add_satellite("skill-a")
    code, out = harness.run(
        "fleet-lease-acquire",
        str(harness.primary),
        "--identity",
        "skill-a",
        "--path",
        str(sat),
        "--purpose",
        "fleet:retire",
    )
    assert code == 0, out
    sh(
        "git",
        "worktree",
        "unlock",
        str(sat),
        cwd=harness.primary,
        env=harness.git_env(),
    )
    sh(
        "git",
        "worktree",
        "remove",
        str(sat),
        cwd=harness.primary,
        env=harness.git_env(),
    )
    code, out = harness.run(
        "fleet-lease-release",
        str(harness.primary),
        "--identity",
        "skill-a",
        "--path",
        str(sat),
    )
    assert code == 0, out
    assert "terminal=decommissioned" in out
    assert not (harness.leases() / "wt-skill-a.lease").exists()


def test_fleet_lease_release_retains_lease_on_ambiguous_state(
    harness: Harness,
) -> None:
    sat = harness.add_satellite("skill-a")
    code, out = harness.run(
        "fleet-lease-acquire",
        str(harness.primary),
        "--identity",
        "skill-a",
        "--path",
        str(sat),
        "--purpose",
        "fleet:retire",
    )
    assert code == 0, out
    sh(
        "git",
        "worktree",
        "unlock",
        str(sat),
        cwd=harness.primary,
        env=harness.git_env(),
    )
    code, out = harness.run(
        "fleet-lease-release",
        str(harness.primary),
        "--identity",
        "skill-a",
        "--path",
        str(sat),
    )
    assert code == 2, out
    assert "STATE: FLEET-OP" in out
    assert "lease retained for recovery" in out
    assert (harness.leases() / "wt-skill-a.lease").is_dir()


def test_fleet_lease_release_requires_exact_parked_state(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire_fleet(harness, "skill-a", sat, purpose="fleet:repair")
    gitdir = Path(sh("git", "rev-parse", "--git-dir", cwd=sat, env=harness.git_env()))
    if not gitdir.is_absolute():
        gitdir = (sat / gitdir).resolve()
    (gitdir / "rebase-merge").mkdir()

    code, out = harness.run(
        "fleet-lease-release",
        str(harness.primary),
        "--identity",
        "skill-a",
        "--path",
        str(sat),
    )

    assert code == 2, out
    assert "STATE: FLEET-OP" in out
    assert "helper state ACTIVE-CONFLICT is not PARKED" in out
    assert "lease retained for recovery" in out
    assert (harness.leases() / "wt-skill-a.lease").is_dir()


def test_task_lease_release_refuses_fleet_purpose(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    code, out = harness.run(
        "fleet-lease-acquire",
        str(harness.primary),
        "--identity",
        "skill-a",
        "--path",
        str(sat),
        "--purpose",
        "fleet:repair",
    )
    assert code == 0, out
    code, out = harness.run("lease-release", str(sat), "--base", "main")
    assert code == 2, out
    assert "fleet-purposed" in out
    assert (harness.leases() / "wt-skill-a.lease").is_dir()


def test_task_activation_refuses_fleet_purpose(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire_fleet(harness, "skill-a", sat)
    code, out = harness.run(
        "activate", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2, out
    assert "fleet-purposed" in out
    assert (harness.leases() / "wt-skill-a.lease").is_dir()


def test_fleet_lease_release_refuses_absent_lease(harness: Harness) -> None:
    expected = harness.root / "repo-worktrees" / "skill-new"
    code, out = harness.run(
        "fleet-lease-release",
        str(harness.primary),
        "--identity",
        "skill-new",
        "--path",
        str(expected),
    )
    assert code == 2, out
    assert "nothing to release" in out


def test_fleet_lease_release_refuses_foreign_owner(harness: Harness) -> None:
    expected = harness.root / "repo-worktrees" / "skill-new"
    acquire_fleet(harness, "skill-new", expected)
    code, out = harness.run(
        "fleet-lease-release",
        str(harness.primary),
        "--identity",
        "skill-new",
        "--path",
        str(expected),
        env=harness.helper_env(session="other-session"),
    )
    assert code == 2, out
    assert "FOREIGN" in out
    assert (harness.leases() / "wt-skill-new.lease").is_dir()


def test_fleet_lease_release_refuses_unreadable_owner(harness: Harness) -> None:
    expected = harness.root / "repo-worktrees" / "skill-new"
    acquire_fleet(harness, "skill-new", expected)
    owner = harness.leases() / "wt-skill-new.lease" / "owner.json"
    owner.write_text("not-json")
    code, out = harness.run(
        "fleet-lease-release",
        str(harness.primary),
        "--identity",
        "skill-new",
        "--path",
        str(expected),
    )
    assert code == 2, out
    assert "unreadable ownership" in out
    assert owner.read_text() == "not-json"


def test_fleet_lease_release_refuses_task_purpose(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat)
    code, out = harness.run(
        "fleet-lease-release",
        str(harness.primary),
        "--identity",
        "skill-a",
        "--path",
        str(sat),
    )
    assert code == 2, out
    assert "not fleet-purposed" in out
    assert (harness.leases() / "wt-skill-a.lease").is_dir()


def test_fleet_lease_release_refuses_scope_mismatch(harness: Harness) -> None:
    expected = harness.root / "repo-worktrees" / "skill-new"
    acquire_fleet(harness, "skill-new", expected)
    owner_file = harness.leases() / "wt-skill-new.lease" / "owner.json"
    owner = json.loads(owner_file.read_text())
    owner["branch"] = "feature/not-null"
    owner_file.write_text(json.dumps(owner))
    code, out = harness.run(
        "fleet-lease-release",
        str(harness.primary),
        "--identity",
        "skill-new",
        "--path",
        str(expected),
    )
    assert code == 2, out
    assert "scope mismatch" in out
    assert owner_file.is_file()


def test_fleet_lease_release_refuses_expected_path_mismatch(
    harness: Harness,
) -> None:
    expected = harness.root / "repo-worktrees" / "skill-new"
    other = harness.root / "elsewhere" / "skill-new"
    acquire_fleet(harness, "skill-new", expected)
    code, out = harness.run(
        "fleet-lease-release",
        str(harness.primary),
        "--identity",
        "skill-new",
        "--path",
        str(other),
    )
    assert code == 2, out
    assert "expected-path mismatch" in out
    assert (harness.leases() / "wt-skill-new.lease").is_dir()


def test_fleet_lease_release_retains_lease_when_parked_proof_fails(
    harness: Harness,
) -> None:
    sat = harness.add_satellite("skill-a")
    acquire_fleet(harness, "skill-a", sat)
    (sat / "dirty.txt").write_text("dirty\n")
    code, out = harness.run(
        "fleet-lease-release",
        str(harness.primary),
        "--identity",
        "skill-a",
        "--path",
        str(sat),
    )
    assert code == 2, out
    assert "FACT: tree: dirty" in out
    assert "helper state UNMAPPABLE is not PARKED" in out
    assert (harness.leases() / "wt-skill-a.lease").is_dir()


# ---------------------------------------------------------------- activate


def test_activate_requires_lease(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    code, out = harness.run(
        "activate", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "no worktree lease" in out


def test_activate_happy_path(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "branch 'feature/t1'" in out


def test_activate_refuses_foreign_wt_lease(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat)
    env = harness.helper_env(session="another-session")
    code, out = harness.run(
        "activate", str(sat), "--base", "main", "--branch", "feature/t1", env=env
    )
    assert code == 2 and "FOREIGN" in out


def test_activate_refuses_taken_branch_name(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    sat2 = harness.add_satellite("skill-b")
    activate(harness, sat, "feature/t1")
    acquire(harness, sat2, "feature/t1")
    code, out = harness.run(
        "activate", str(sat2), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "already exists" in out


def test_activate_refuses_wrong_base(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat)
    code, out = harness.run(
        "activate", str(sat), "--base", "develop", "--branch", "feature/t1"
    )
    assert code == 2 and "does not match the primary checkout's branch" in out


def test_activate_refuses_op_marker(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat)
    marker = harness.primary / ".git" / "worktrees" / "skill-a" / "MERGE_HEAD"
    marker.write_text("0" * 40 + "\n")
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: ACTIVE-CONFLICT" in out
    code, out = harness.run(
        "activate", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "operation in progress" in out


def test_mutating_verbs_refuse_primary_target(harness: Harness) -> None:
    harness.add_satellite("skill-a")
    code, out = harness.run(
        "lease-acquire", str(harness.primary), "--branch", "b", "--purpose", "p"
    )
    assert code == 2 and "primary checkout" in out


def test_mutating_verbs_refuse_unlocked_worktree(harness: Harness) -> None:
    sat = harness.add_satellite("loose", locked=False)
    code, out = harness.run(
        "lease-acquire", str(sat), "--branch", "b", "--purpose", "p"
    )
    assert code == 2 and "not locked" in out


def test_mutating_verbs_refuse_noncanonical_lock_reason(harness: Harness) -> None:
    sat = harness.add_satellite("odd", reason="some other reason")
    code, out = harness.run(
        "lease-acquire", str(sat), "--branch", "b", "--purpose", "p"
    )
    assert code == 2 and "non-canonical" in out


def test_worktree_identity_cross_check(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    code, out = harness.run(
        "lease-acquire",
        str(sat),
        "--branch",
        "b",
        "--purpose",
        "p",
        "--worktree",
        "wrong-name",
    )
    assert code == 2 and "identity mismatch" in out


def test_unknown_ignored_path_hard_stops_activation(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    (sat / "junk").mkdir()
    (sat / "junk" / "x.bin").write_text("x")
    acquire(harness, sat)
    code, out = harness.run(
        "activate", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "unknown ignored path" in out


# ---------------------------------------------------------------- record-validation


def test_record_validation_detached_refused(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat)
    code, out = harness.run("record-validation", str(sat), "--ladder", "x")
    assert code == 2 and "detached" in out


def test_record_validation_collision_refused(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "w.txt").write_text("w\n")
    harness.commit("w", cwd=sat)
    (harness.validations() / "feature--t1.json").write_text(
        json.dumps(
            {
                "branch": "feature--t1",
                "validated_tip": "a" * 40,
                "ladder": "x",
                "ignored_state": "none present",
                "timestamp": "2026-01-01T00:00:00Z",
            }
        )
    )
    code, out = harness.run("record-validation", str(sat), "--ladder", "x")
    assert code == 2 and "filename collision" in out


def test_record_validation_reports_ignored_residue_class(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "w.txt").write_text("w\n")
    harness.commit("w", cwd=sat)
    (sat / "__pycache__").mkdir()
    (sat / "__pycache__" / "x.pyc").write_text("x")
    code, out = harness.run("record-validation", str(sat), "--ladder", "x")
    assert code == 0, out
    record = json.loads((harness.validations() / "feature--t1.json").read_text())
    assert record["ignored_state"].startswith("report-and-record:")
    assert "__pycache__/x.pyc" in record["ignored_state"]


def test_record_validation_unreadable_record_fails_closed(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "w.txt").write_text("w\n")
    harness.commit("w", cwd=sat)
    record = harness.validations() / "feature--t1.json"
    record.write_text("not json")
    code, out = harness.run("record-validation", str(sat), "--ladder", "x")
    assert code == 2 and "unreadable" in out
    assert record.read_text() == "not json", "evidence bytes must be preserved"


def test_record_validation_dangling_symlink_fails_closed(harness: Harness) -> None:
    # 1.5.1 fail-open: Path.exists() classified a dangling symlink as absent,
    # then write_text() followed it and created the outside target
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "w.txt").write_text("w\n")
    harness.commit("w", cwd=sat)
    outside = harness.root / "outside-target.json"
    record = harness.validations() / "feature--t1.json"
    record.symlink_to(outside)
    code, out = harness.run("record-validation", str(sat), "--ladder", "x")
    assert code == 2 and "is a symlink" in out and "never written through a link" in out
    assert record.is_symlink(), "the planted symlink must be preserved as evidence"
    assert os.readlink(record) == str(outside)
    assert not outside.exists(), "the outside target must not be created"


def test_record_validation_live_symlink_fails_closed(harness: Harness) -> None:
    # a live symlink to a valid same-branch record: 1.5.1 read it as ok and
    # superseded through the link, rewriting the aliased outside target
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "w.txt").write_text("w\n")
    harness.commit("w", cwd=sat)
    outside = harness.root / "outside-live.json"
    original = json.dumps(
        {
            "branch": "feature/t1",
            "validated_tip": "a" * 40,
            "ladder": "x",
            "ignored_state": "none present",
            "timestamp": "2026-01-01T00:00:00Z",
        }
    )
    outside.write_text(original)
    record = harness.validations() / "feature--t1.json"
    record.symlink_to(outside)
    code, out = harness.run("record-validation", str(sat), "--ladder", "x")
    assert code == 2 and "is a symlink" in out and "never written through a link" in out
    assert record.is_symlink()
    assert outside.read_text() == original, "aliased target bytes must be unchanged"


def test_record_validation_hardlinked_record_fails_closed(harness: Harness) -> None:
    # a hardlink is invisible to both the symlink checks and O_NOFOLLOW; the
    # O_TRUNC supersede would rewrite the shared inode's bytes outside the store
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "w.txt").write_text("w\n")
    harness.commit("w", cwd=sat)
    outside = harness.root / "outside-hard.json"
    original = json.dumps(
        {
            "branch": "feature/t1",
            "validated_tip": "a" * 40,
            "ladder": "x",
            "ignored_state": "none present",
            "timestamp": "2026-01-01T00:00:00Z",
        }
    )
    outside.write_text(original)
    record = harness.validations() / "feature--t1.json"
    os.link(outside, record)
    code, out = harness.run("record-validation", str(sat), "--ladder", "x")
    assert code == 2 and "hardlink" in out
    assert outside.read_text() == original, "shared-inode bytes must be unchanged"
    assert record.exists() and record.stat().st_nlink == 2


def test_load_record_nonregular_file_is_unreadable(tmp_path: Path) -> None:
    # a FIFO (or any non-regular file) at a record path must classify
    # unreadable instead of blocking at open; consumers then fail closed
    module = load_helper(tmp_path)
    fifo = tmp_path / "record.json"
    os.mkfifo(fifo)
    status, data = module.load_record(fifo)
    assert status == "unreadable" and data is None


def test_write_record_refuses_symlink_at_write_time(tmp_path: Path) -> None:
    # in-process pin for the O_NOFOLLOW write guard: even with every upstream
    # symlink check bypassed, the write itself must refuse a link
    module = load_helper(tmp_path)
    outside = tmp_path / "outside.json"
    link = tmp_path / "record.json"
    link.symlink_to(outside)
    with pytest.raises(SystemExit) as exc:
        module.write_record(link, "{}\n")
    assert exc.value.code == 2
    assert link.is_symlink()
    assert not outside.exists(), "O_NOFOLLOW must not create the link target"


def test_record_validation_write_goes_through_symlink_guarded_writer(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # wiring pin: the record write must go through write_record (the
    # O_NOFOLLOW guard), never a raw write that follows links
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "w.txt").write_text("w\n")
    harness.commit("w", cwd=sat)
    module = load_helper(tmp_path)
    calls: "list[Path]" = []
    real_write = module.write_record

    def spy(path: Path, payload: str) -> None:
        calls.append(path)
        real_write(path, payload)

    monkeypatch.setattr(module, "write_record", spy)
    for key, value in harness.helper_env().items():
        monkeypatch.setenv(key, value)
    monkeypatch.delenv("CODEX_THREAD_ID", raising=False)
    rc = module.main(["record-validation", str(sat), "--ladder", "x"])
    assert rc == 0
    assert [p.name for p in calls] == ["feature--t1.json"], (
        "the validation-record write must run through the guarded writer"
    )


def test_record_validation_create_and_supersede_still_succeed(
    harness: Harness,
) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    tip1 = work_and_record(harness, sat)
    record = harness.validations() / "feature--t1.json"
    assert not record.is_symlink()
    assert json.loads(record.read_text())["validated_tip"] == tip1
    (sat / "more.txt").write_text("more\n")
    tip2 = harness.commit("more work", cwd=sat)
    code, out = harness.run("record-validation", str(sat), "--ladder", "x")
    assert code == 0 and "superseding prior record" in out
    assert json.loads(record.read_text())["validated_tip"] == tip2


# ---------------------------------------------------------------- land


def test_land_happy_path_and_integration_lease_released(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    tip = work_and_record(harness, sat)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 0, out
    assert tip in out
    assert "integration lease released" in out
    assert not (harness.leases() / "integration.lease").exists()
    assert out.rstrip().endswith("RESULT: ok")
    main_tip = sh(
        "git", "rev-parse", "main", cwd=harness.primary, env=harness.git_env()
    )
    assert main_tip == tip


def test_land_refusal_releases_lease_before_result_line(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    (sat / "late.txt").write_text("late\n")
    harness.commit("late commit", cwd=sat)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "validation binding failed" in out
    assert not (harness.leases() / "integration.lease").exists()
    assert out.rstrip().endswith("RESULT: refused")
    assert out.index("integration lease released") < out.index("REFUSE:")


def test_land_refuses_absent_record(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "w.txt").write_text("w\n")
    harness.commit("w", cwd=sat)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "READY-INVALID" in out


def test_land_stale_base_labeled(harness: Harness) -> None:
    sat_a = harness.add_satellite("skill-a")
    sat_b = harness.add_satellite("skill-b")
    activate(harness, sat_a, "feature/a")
    activate(harness, sat_b, "feature/b")
    work_and_record(harness, sat_a, "a.txt")
    tip_b = work_and_record(harness, sat_b, "b.txt")
    code, out = harness.run(
        "land", str(sat_a), "--base", "main", "--branch", "feature/a"
    )
    assert code == 0, out
    code, out = harness.run(
        "land", str(sat_b), "--base", "main", "--branch", "feature/b"
    )
    assert code == 2 and "STATE: STALE-BASE" in out
    assert (
        sh(
            "git",
            "rev-parse",
            "refs/heads/feature/b",
            cwd=harness.primary,
            env=harness.git_env(),
        )
        == tip_b
    )


def test_land_record_branch_cross_check_fails_closed(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    record = harness.validations() / "feature--t1.json"
    data = json.loads(record.read_text())
    data["branch"] = "feature/OTHER"
    record.write_text(json.dumps(data))
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "cross-check failed" in out


def test_land_refuses_lease_scope_mismatch(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    owner_file = harness.leases() / "wt-skill-a.lease" / "owner.json"
    owner = json.loads(owner_file.read_text())
    owner["branch"] = "feature/OTHER"
    owner_file.write_text(json.dumps(owner))
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "scope mismatch" in out


def test_land_refuses_dirty_primary(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    (harness.primary / "dirty.txt").write_text("d\n")
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "primary tree is not clean" in out


def test_land_refuses_primary_op_marker(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    marker = harness.primary / ".git" / "MERGE_HEAD"
    marker.write_text("0" * 40 + "\n")
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "operation in progress in primary" in out


def test_land_refuses_behind_origin(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    bare = harness.add_origin()
    clone = harness.root / "clone"
    sh("git", "clone", str(bare), str(clone), cwd=harness.root, env=harness.git_env())
    (clone / "remote.txt").write_text("r\n")
    harness.commit("remote work", cwd=clone)
    sh("git", "push", cwd=clone, env=harness.git_env())
    sh("git", "fetch", "origin", cwd=harness.primary, env=harness.git_env())
    activate(harness, sat)
    work_and_record(harness, sat)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "behind origin" in out


def test_land_reports_ahead_only(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    harness.add_origin()
    (harness.primary / "local.txt").write_text("l\n")
    harness.commit("local main work")
    activate(harness, sat)
    work_and_record(harness, sat)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 0, out
    assert "ahead 1, behind 0" in out


def test_land_merges_validated_sha_not_ref(
    harness: Harness, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    tip = work_and_record(harness, sat)
    module = load_helper(tmp_path)
    merges: "list[tuple[str, ...]]" = []
    real_run_git = module.run_git

    def spy(*args: str, cwd: Path):
        if args and args[0] == "merge":
            merges.append(args)
        return real_run_git(*args, cwd=cwd)

    monkeypatch.setattr(module, "run_git", spy)
    for key, value in harness.helper_env().items():
        monkeypatch.setenv(key, value)
    monkeypatch.delenv("CODEX_THREAD_ID", raising=False)
    rc = module.main(["land", str(sat), "--base", "main", "--branch", "feature/t1"])
    assert rc == 0
    assert merges == [("merge", "--ff-only", tip)], (
        "the ff-only merge must target the record's validated_tip SHA, never the ref name"
    )


def test_land_cleanup_failure_is_nonzero_and_never_ok(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    tip = work_and_record(harness, sat)
    fake_trash = harness.bindir / "trash"
    fake_trash.write_text(
        "#!/bin/sh\n"
        'for p in "$@"; do\n'
        '  case "$p" in *integration.lease*) echo "simulated integration trash failure" >&2; exit 1;; esac\n'
        f'  mv "$p" "{harness.trashed}/$(basename "$p").$$" || exit 1\n'
        "done\n"
    )
    fake_trash.chmod(0o755)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code != 0, out
    assert "RESULT: ok" not in out
    assert (harness.leases() / "integration.lease").exists()
    main_tip = sh(
        "git", "rev-parse", "main", cwd=harness.primary, env=harness.git_env()
    )
    assert main_tip == tip, "the merge itself completed before the cleanup failure"


def test_land_integration_reentry_requires_purpose_match(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    base_before = sh(
        "git", "rev-parse", "main", cwd=harness.primary, env=harness.git_env()
    )
    plant_lease(
        harness,
        "integration.lease",
        {
            "session_id": SESSION,
            "runtime": "claude-code",
            "worktree": "skill-a",
            "branch": "feature/t1",
            "purpose": "WRONG-PURPOSE",
        },
    )
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "DIFFERENT scope" in out
    main_tip = sh(
        "git", "rev-parse", "main", cwd=harness.primary, env=harness.git_env()
    )
    assert main_tip == base_before, "the merge must not run under a wrong-purpose lease"


def test_land_refuses_symlink_record(harness: Harness) -> None:
    # a symlinked record must never authorize an integration: 1.5.1 followed
    # the link, read a valid record, and ran the merge
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "w.txt").write_text("w\n")
    tip = harness.commit("w", cwd=sat)
    base_before = sh(
        "git", "rev-parse", "main", cwd=harness.primary, env=harness.git_env()
    )
    outside = harness.root / "outside-rec.json"
    outside.write_text(
        json.dumps(
            {
                "branch": "feature/t1",
                "validated_tip": tip,
                "ladder": "x",
                "ignored_state": "none present",
                "timestamp": "2026-01-01T00:00:00Z",
            }
        )
    )
    (harness.validations() / "feature--t1.json").symlink_to(outside)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "is symlink; READY-INVALID" in out
    main_tip = sh(
        "git", "rev-parse", "main", cwd=harness.primary, env=harness.git_env()
    )
    assert main_tip == base_before, "no merge may run off a symlinked record"


# ---------------------------------------------------------------- park / delete


def test_park_refuses_unlanded_commits(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    code, out = harness.run("park", str(sat), "--base", "main")
    assert code == 2 and "containment proof failed" in out


def test_park_refuses_wrong_base(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    code, out = harness.run("park", str(sat), "--base", "feature/t1")
    assert code == 2 and "does not match the primary checkout's branch" in out


def test_park_detached_does_not_hide_unlanded_branch(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    sh("git", "switch", "--detach", "main", cwd=sat, env=harness.git_env())
    code, out = harness.run(
        "park", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "does not hide" in out
    assert (harness.leases() / "wt-skill-a.lease").exists()


def test_full_cycle_land_park_delete(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 0, out
    code, out = harness.run("park", str(sat), "--base", "main")
    assert code == 0, out
    assert "released (proven re-park)" in out
    assert not (harness.leases() / "wt-skill-a.lease").exists()
    code, out = harness.run(
        "delete-branch", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 0, out
    assert "safe-deleted" in out
    assert not (harness.validations() / "feature--t1.json").exists()
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: PARKED" in out


def test_park_already_detached_completes_reparked_proofs(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    acquire(harness, sat, "feature/t1")
    code, out = harness.run(
        "park", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 0 and "already detached" in out
    assert not (harness.leases() / "wt-skill-a.lease").exists()


def test_delete_branch_refuses_checked_out_branch(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    harness.run("land", str(sat), "--base", "main", "--branch", "feature/t1")
    code, out = harness.run(
        "delete-branch", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "checked out in worktree" in out


def test_delete_branch_refuses_unlanded(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    sh("git", "switch", "--detach", "main", cwd=sat, env=harness.git_env())
    code, out = harness.run(
        "delete-branch", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "not contained" in out and "-D" in out


def test_delete_branch_keeps_mismatched_record(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 0, out
    code, out = harness.run("park", str(sat), "--base", "main")
    assert code == 0, out
    record = harness.validations() / "feature--t1.json"
    data = json.loads(record.read_text())
    data["branch"] = "feature/OTHER"
    record.write_text(json.dumps(data))
    code, out = harness.run(
        "delete-branch", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 0 and "safe-deleted" in out
    assert "filename collision" in out
    assert record.exists()


def test_delete_branch_orphan_record_contained_is_cleaned(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    harness.run("land", str(sat), "--base", "main", "--branch", "feature/t1")
    harness.run("park", str(sat), "--base", "main")
    sh("git", "branch", "-d", "feature/t1", cwd=harness.primary, env=harness.git_env())
    assert (harness.validations() / "feature--t1.json").exists()
    code, out = harness.run(
        "delete-branch", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 0 and "prior completion" in out, out
    assert not (harness.validations() / "feature--t1.json").exists()


def test_delete_branch_orphan_record_uncontained_refuses(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    sh("git", "switch", "-c", "feature/ghost", "main", cwd=sat, env=harness.git_env())
    (sat / "ghost.txt").write_text("ghost\n")
    ghost_tip = harness.commit("ghost work", cwd=sat)
    sh("git", "switch", "--detach", "main", cwd=sat, env=harness.git_env())
    sh(
        "git",
        "branch",
        "-D",
        "feature/ghost",
        cwd=harness.primary,
        env=harness.git_env(),
    )
    (harness.validations() / "feature--ghost.json").write_text(
        json.dumps(
            {
                "branch": "feature/ghost",
                "validated_tip": ghost_tip,
                "ladder": "x",
                "ignored_state": "none present",
                "timestamp": "2026-01-01T00:00:00Z",
            }
        )
    )
    code, out = harness.run(
        "delete-branch", str(sat), "--base", "main", "--branch", "feature/ghost"
    )
    assert code == 2 and ("never trash" in out or "adjudication" in out)
    assert (harness.validations() / "feature--ghost.json").exists()


def test_delete_branch_nothing_to_do(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    code, out = harness.run(
        "delete-branch", str(sat), "--base", "main", "--branch", "feature/none"
    )
    assert code == 2 and "nothing to do" in out


def test_delete_branch_refuses_symlink_record(harness: Harness) -> None:
    # a symlink at the record path must refuse BEFORE the branch mutation:
    # an adjudication note on a RESULT: ok is the weakest signal in the
    # output contract, so nothing may mutate until the link is adjudicated
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    work_and_record(harness, sat)
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 0, out
    code, out = harness.run("park", str(sat), "--base", "main")
    assert code == 0, out
    record = harness.validations() / "feature--t1.json"
    outside = harness.root / "outside-del.json"
    outside.write_text(record.read_text())
    record.unlink()
    record.symlink_to(outside)
    original = outside.read_text()
    code, out = harness.run(
        "delete-branch", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "is a symlink" in out and "before deletion" in out
    survived = sh(
        "git",
        "rev-parse",
        "--verify",
        "refs/heads/feature/t1",
        cwd=harness.primary,
        env=harness.git_env(),
    )
    assert survived, "the branch must survive the refusal"
    assert record.is_symlink(), "a symlinked record is never trashed"
    assert outside.read_text() == original


# ---------------------------------------------------------------- store layout & misc


def test_missing_store_layout_fails_closed(harness: Harness, tmp_path: Path) -> None:
    bare = tmp_path / "other"
    bare.mkdir()
    sh("git", "init", "-b", "main", ".", cwd=bare, env=harness.git_env())
    (bare / "f.txt").write_text("f\n")
    sh("git", "add", "-A", cwd=bare, env=harness.git_env())
    sh("git", "commit", "-m", "i", cwd=bare, env=harness.git_env())
    code, out = harness.run("inspect", str(bare), "--base", "main")
    assert code == 2 and "no skill-worktree store" in out


def test_symlinked_validation_root_fails_closed(harness: Harness) -> None:
    # the same escape one level up: validations/ itself aliased outside the store
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "w.txt").write_text("w\n")
    harness.commit("w", cwd=sat)
    outside_dir = harness.root / "outside-validations"
    outside_dir.mkdir()
    real = harness.validations()
    real.rmdir()
    real.symlink_to(outside_dir)
    code, out = harness.run("record-validation", str(sat), "--ladder", "x")
    # gate phrases, not a bare "symlink" substring: this test's 30-char tmp_path
    # basename contains "symlink" and the refusal embeds the store path, so the
    # bare substring assert was self-satisfying via the path echo
    assert code == 2 and "store integrity failed" in out and "is a symlink" in out
    assert list(outside_dir.iterdir()) == [], "outside directory must stay unchanged"


def test_symlinked_store_parent_fails_closed(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "w.txt").write_text("w\n")
    harness.commit("w", cwd=sat)
    store = harness.primary / ".git" / "skill-worktree"
    outside_store = harness.root / "outside-store"
    store.rename(outside_store)
    store.symlink_to(outside_store)
    code, out = harness.run("record-validation", str(sat), "--ladder", "x")
    # same live path-echo hazard as the symlinked-validations-root test
    assert code == 2 and "store integrity failed" in out and "is a symlink" in out
    assert list((outside_store / "validations").iterdir()) == [], (
        "no record may be written through the aliased store"
    )


def test_symlinked_lease_root_fails_closed(harness: Harness) -> None:
    # 1.5.2 fail-open: discover() proved store and validations non-symlink but
    # not leases; a live symlinked lease root let lease-acquire create the
    # lease dir and owner.json outside the store while printing RESULT: ok
    sat = harness.add_satellite("skill-a")
    outside_dir = harness.root / "outside-leases"
    outside_dir.mkdir()
    real = harness.leases()
    real.rmdir()
    real.symlink_to(outside_dir)
    code, out = harness.run(
        "lease-acquire", str(sat), "--branch", "feature/t1", "--purpose", "test"
    )
    # pin on message phrases a tmp_path echo cannot satisfy: this test's own
    # name (embedded in the store path pytest prints) contains "symlink"
    assert code == 2 and "store integrity failed" in out and "is a symlink" in out
    assert real.is_symlink(), "the planted symlink must be preserved as evidence"
    assert list(outside_dir.iterdir()) == [], "outside directory must stay unchanged"


def test_dangling_symlinked_lease_root_fails_closed(harness: Harness) -> None:
    # dangling variant: 1.5.2 read leases.is_dir() False and refused with the
    # untruthful "no skill-worktree store" classification; the symlink gate
    # must name the real condition and leave the absent target uncreated
    sat = harness.add_satellite("skill-a")
    target = harness.root / "absent-leases"
    real = harness.leases()
    real.rmdir()
    real.symlink_to(target)
    code, out = harness.run(
        "lease-acquire", str(sat), "--branch", "feature/t1", "--purpose", "test"
    )
    # same path-echo hazard as the live pin: assert the gate's own phrases
    assert code == 2 and "store integrity failed" in out and "is a symlink" in out
    assert real.is_symlink()
    assert not target.exists(), "the dangling target must never be created"


def test_malformed_record_treated_unreadable(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    activate(harness, sat)
    (sat / "w.txt").write_text("w\n")
    harness.commit("w", cwd=sat)
    (harness.validations() / "feature--t1.json").write_text(
        json.dumps(
            {
                "branch": "feature/t1",
                "validated_tip": "main",
                "ladder": "x",
                "ignored_state": "none present",
                "timestamp": "2026-01-01T00:00:00Z",
            }
        )
    )
    code, out = harness.run(
        "land", str(sat), "--base", "main", "--branch", "feature/t1"
    )
    assert code == 2 and "unreadable" in out and "READY-INVALID" in out


def test_pilot_fixture_shapes() -> None:
    fixtures = sorted(FIXTURES.glob("*.json"))
    assert len(fixtures) == 4
    for path in fixtures:
        data = json.loads(path.read_text())
        assert {
            "branch",
            "validated_tip",
            "ladder",
            "ignored_state",
            "timestamp",
        } <= set(data)
        assert path.name == data["branch"].replace("/", "--") + ".json"
        assert len(data["validated_tip"]) == 40


def test_minimum_python_version_fails_closed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    module = load_helper(tmp_path)
    monkeypatch.setattr(sys, "version_info", (3, 8, 0))
    assert module.main(["inspect", ".", "--base", "main"]) == 2


def test_session_constant_matches_conftest() -> None:
    assert SESSION.startswith("test-session")
