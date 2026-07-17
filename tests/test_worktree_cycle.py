"""Guard, state-mapping, collision, and refusal coverage for worktree_cycle.py.

Every test runs the helper as a subprocess against a hermetic temp repo
(see conftest.Harness) unless noted (the merge-target pin test runs the
module in-process to spy on the git calls); nothing here touches the real
.agents repo or its satellites.
"""

from __future__ import annotations

import importlib.util
import json
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


# ---------------------------------------------------------------- inspect


def test_inspect_primary_overview(harness: Harness) -> None:
    harness.add_satellite("skill-a")
    code, out = harness.run("inspect", str(harness.primary), "--base", "main")
    assert code == 0 and "STATE: PRIMARY" in out


def test_inspect_parked(harness: Harness) -> None:
    sat = harness.add_satellite("skill-a")
    code, out = harness.run("inspect", str(sat), "--base", "main")
    assert code == 0 and "STATE: PARKED" in out


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
