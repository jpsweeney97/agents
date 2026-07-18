"""Hermetic classification and routing tests for skill-route-guard.py."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SOURCE_ROOT = Path(__file__).resolve().parent.parent
SOURCE_GUARD = SOURCE_ROOT / "scripts" / "skill-route-guard.py"
SOURCE_FLEET = SOURCE_ROOT / "scripts" / "satellite-fleet.py"

ROUTE_PHRASE = "skill-surface mutation in the primary checkout"
PARKED_PHRASE = "PARKED (detached HEAD)"
GENERIC_PHRASE = "No satellite maps to this path"
LIKELY_PHRASE = "Likely satellite (confirm with inspect)"
BYPASS_PHRASE = "skill-route-guard enforcement bypassed"
NONBLOCK_PHRASE = "skill-route-guard: non-blocking error"


def sh(*args: str, cwd: Path, env: "dict[str, str]") -> str:
    """Run a command, assert success, return stripped stdout."""
    proc = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    assert proc.returncode == 0, f"{args} failed: {proc.stderr}"
    return proc.stdout.strip()


class GuardHarness:
    """One throwaway primary repo, a derived fleet root, and a guard copy."""

    def __init__(self, tmp_path: Path) -> None:
        self.base = tmp_path.resolve()
        self.repo = self.base / "repo"
        self.fleet = self.base / "repo-worktrees"
        home = self.base / "home"
        for d in (self.repo, self.fleet, home):
            d.mkdir(parents=True, exist_ok=True)
        self.env = {
            "PATH": os.environ["PATH"],
            "HOME": str(home),
            "PYTHONDONTWRITEBYTECODE": "1",
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@t",
        }
        sh("git", "init", "-q", "-b", "main", cwd=self.repo, env=self.env)
        self._seed_tree()
        sh("git", "add", "-A", cwd=self.repo, env=self.env)
        sh("git", "commit", "-q", "-m", "seed", cwd=self.repo, env=self.env)
        self.guard = self.repo / "scripts" / "skill-route-guard.py"
        assert SOURCE_GUARD.exists(), f"guard missing: {SOURCE_GUARD}"
        shutil.copy2(SOURCE_GUARD, self.guard)

    def _seed_tree(self) -> None:
        files = {
            "skills/mk-rec/SKILL.md": "skill body\n",
            "skills/README.md": "not a skill surface\n",
            "skills-claude/only-claude/SKILL.md": "skill body\n",
            "plugins/handoff/skills/save-handoff/SKILL.md": "skill body\n",
            "plugins/handoff/references/handoff-format.md": "runtime-loaded contract\n",
            "plugins/handoff/.claude-plugin/plugin.json": '{"name": "handoff"}\n',
            "plugins/marketplace.json": '{"plugins": []}\n',
            "docs/notes.md": "ordinary repo file\n",
            "scripts/.keep": "",
        }
        for rel, content in files.items():
            path = self.repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)

    def add_satellite(self, name: str, *, parked: bool) -> Path:
        sat = self.fleet / name
        if parked:
            sh(
                "git",
                "worktree",
                "add",
                "--detach",
                str(sat),
                "main",
                cwd=self.repo,
                env=self.env,
            )
        else:
            sh(
                "git",
                "worktree",
                "add",
                "-b",
                f"task/{name}",
                str(sat),
                "main",
                cwd=self.repo,
                env=self.env,
            )
        return sat

    def run(
        self,
        payload: "dict | None" = None,
        *,
        raw: "str | None" = None,
        cwd: "Path | None" = None,
        env_extra: "dict[str, str] | None" = None,
    ) -> "subprocess.CompletedProcess[str]":
        env = dict(self.env)
        if env_extra:
            env.update(env_extra)
        return subprocess.run(
            [sys.executable, str(self.guard)],
            input=raw if raw is not None else json.dumps(payload),
            cwd=str(cwd or self.repo),
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def edit(
        self, path: "Path | str", *, tool: str = "Edit", cwd: "Path | None" = None
    ) -> dict:
        return {
            "session_id": "t",
            "cwd": str(cwd or self.repo),
            "hook_event_name": "PreToolUse",
            "tool_name": tool,
            "tool_input": {
                "file_path": str(path),
                "old_string": "a",
                "new_string": "b",
            },
        }

    def notebook(self, path: "Path | str") -> dict:
        return {
            "session_id": "t",
            "cwd": str(self.repo),
            "hook_event_name": "PreToolUse",
            "tool_name": "NotebookEdit",
            "tool_input": {"notebook_path": str(path), "new_source": "x"},
        }

    def multiedit(self, paths: "list[Path | str]") -> dict:
        return {
            "session_id": "t",
            "cwd": str(self.repo),
            "hook_event_name": "PreToolUse",
            "tool_name": "MultiEdit",
            "tool_input": {
                "edits": [
                    {"file_path": str(p), "old_string": "a", "new_string": "b"}
                    for p in paths
                ]
            },
        }

    def apply_patch(self, patch: str, *, cwd: "Path | None" = None) -> dict:
        return {
            "session_id": "t",
            "cwd": str(cwd or self.repo),
            "hook_event_name": "PreToolUse",
            "tool_name": "apply_patch",
            "tool_input": {"command": patch},
        }


@pytest.fixture()
def guard(tmp_path: Path) -> GuardHarness:
    return GuardHarness(tmp_path)


def assert_deny(proc: "subprocess.CompletedProcess[str]", *phrases: str) -> None:
    assert proc.returncode == 2, (
        f"expected deny, got {proc.returncode}: {proc.stderr!r}"
    )
    for phrase in phrases:
        assert phrase in proc.stderr, f"missing {phrase!r} in: {proc.stderr!r}"


def assert_allow(proc: "subprocess.CompletedProcess[str]") -> None:
    assert proc.returncode == 0, (
        f"expected allow, got {proc.returncode}: {proc.stderr!r}"
    )


# --- primary-checkout skill surfaces ---


def test_skills_root_deny(guard: GuardHarness) -> None:
    proc = guard.run(guard.edit(guard.repo / "skills/mk-rec/SKILL.md"))
    assert_deny(proc, ROUTE_PHRASE, "worktree-task-cycle")


def test_skills_claude_root_deny(guard: GuardHarness) -> None:
    proc = guard.run(guard.edit(guard.repo / "skills-claude/only-claude/SKILL.md"))
    assert_deny(proc, ROUTE_PHRASE)


def test_plugin_skill_deny(guard: GuardHarness) -> None:
    proc = guard.run(
        guard.edit(guard.repo / "plugins/handoff/skills/save-handoff/SKILL.md")
    )
    assert_deny(proc, ROUTE_PHRASE)


def test_plugin_reference_deny(guard: GuardHarness) -> None:
    proc = guard.run(
        guard.edit(guard.repo / "plugins/handoff/references/handoff-format.md")
    )
    assert_deny(proc, ROUTE_PHRASE)


def test_plugin_manifest_deny(guard: GuardHarness) -> None:
    proc = guard.run(
        guard.edit(guard.repo / "plugins/handoff/.claude-plugin/plugin.json")
    )
    assert_deny(proc, ROUTE_PHRASE)


def test_marketplace_json_allow(guard: GuardHarness) -> None:
    assert_allow(guard.run(guard.edit(guard.repo / "plugins/marketplace.json")))


def test_skills_readme_allow(guard: GuardHarness) -> None:
    assert_allow(guard.run(guard.edit(guard.repo / "skills/README.md")))


def test_primary_non_skill_allow(guard: GuardHarness) -> None:
    assert_allow(guard.run(guard.edit(guard.repo / "docs/notes.md")))


def test_new_skill_write_deny(guard: GuardHarness) -> None:
    payload = guard.edit(guard.repo / "skills/brand-new/SKILL.md", tool="Write")
    proc = guard.run(payload)
    assert_deny(proc, ROUTE_PHRASE, GENERIC_PHRASE)


# --- satellite states ---


def test_satellite_active_allow(guard: GuardHarness) -> None:
    sat = guard.add_satellite("active-skill", parked=False)
    assert_allow(guard.run(guard.edit(sat / "skills/mk-rec/SKILL.md")))


def test_satellite_parked_deny(guard: GuardHarness) -> None:
    sat = guard.add_satellite("mk-rec", parked=True)
    proc = guard.run(guard.edit(sat / "skills/mk-rec/SKILL.md"))
    assert_deny(proc, PARKED_PHRASE)


def test_fleet_root_non_worktree_deny(guard: GuardHarness) -> None:
    stray = guard.fleet / "not-a-worktree"
    stray.mkdir()
    proc = guard.run(guard.edit(stray / "file.md"))
    assert proc.returncode == 2, proc.stderr


def test_fleet_root_direct_file_deny(guard: GuardHarness) -> None:
    proc = guard.run(guard.edit(guard.fleet / "note.md"))
    assert proc.returncode == 2, proc.stderr


# --- outside both roots ---


def test_outside_allow_silent(guard: GuardHarness) -> None:
    target = guard.base / "elsewhere" / "f.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    proc = guard.run(guard.edit(target), cwd=target.parent)
    assert_allow(proc)
    assert proc.stdout == "" and proc.stderr == ""


# --- path authority ---


def test_relative_path_resolved_against_cwd(guard: GuardHarness) -> None:
    proc = guard.run(
        guard.apply_patch(
            "*** Begin Patch\n*** Update File: skills/mk-rec/SKILL.md\n*** End Patch"
        )
    )
    assert_deny(proc, ROUTE_PHRASE)


def test_traversal_into_root_deny(guard: GuardHarness) -> None:
    proc = guard.run(
        guard.edit(guard.repo / "docs" / ".." / "skills" / "mk-rec" / "SKILL.md")
    )
    assert_deny(proc, ROUTE_PHRASE)


def test_symlink_into_root_deny(guard: GuardHarness) -> None:
    farm = guard.base / "farm"
    farm.mkdir()
    (farm / "mk-rec").symlink_to(guard.repo / "skills" / "mk-rec")
    proc = guard.run(guard.edit(farm / "mk-rec" / "SKILL.md"), cwd=farm)
    assert_deny(proc, ROUTE_PHRASE)


def test_symlink_out_of_root_deny(guard: GuardHarness) -> None:
    outside = guard.base / "outside-target"
    outside.mkdir()
    (outside / "f.md").write_text("x\n")
    link = guard.repo / "skills" / "mk-rec" / "linkout"
    link.symlink_to(outside)
    proc = guard.run(guard.edit(link / "f.md"))
    assert_deny(proc, ROUTE_PHRASE)


def test_nonexistent_suffix_still_classified(guard: GuardHarness) -> None:
    proc = guard.run(
        guard.edit(
            guard.repo / "skills" / "mk-rec" / "deep" / "new" / "file.md", tool="Write"
        )
    )
    assert_deny(proc, ROUTE_PHRASE)


# --- unclassifiable input precedence ---


def test_missing_file_path_guarded_cwd_deny(guard: GuardHarness) -> None:
    payload = guard.edit(guard.repo / "skills/mk-rec/SKILL.md")
    del payload["tool_input"]["file_path"]
    proc = guard.run(payload)
    assert proc.returncode == 2, proc.stderr


def test_missing_file_path_unguarded_cwd_nonblocking(guard: GuardHarness) -> None:
    elsewhere = guard.base / "elsewhere2"
    elsewhere.mkdir()
    payload = guard.edit(guard.repo / "skills/mk-rec/SKILL.md", cwd=elsewhere)
    del payload["tool_input"]["file_path"]
    proc = guard.run(payload, cwd=elsewhere)
    assert proc.returncode == 1, proc.stderr
    assert NONBLOCK_PHRASE in proc.stderr


def test_unparseable_stdin_guarded_cwd_deny(guard: GuardHarness) -> None:
    proc = guard.run(raw="this is not json", cwd=guard.repo)
    assert proc.returncode == 2, proc.stderr


def test_unparseable_stdin_unguarded_cwd_nonblocking(guard: GuardHarness) -> None:
    elsewhere = guard.base / "elsewhere3"
    elsewhere.mkdir()
    proc = guard.run(raw="this is not json", cwd=elsewhere)
    assert proc.returncode == 1, proc.stderr
    assert NONBLOCK_PHRASE in proc.stderr


def test_unknown_tool_guarded_cwd_deny(guard: GuardHarness) -> None:
    payload = guard.edit(guard.repo / "docs/notes.md")
    payload["tool_name"] = "SomeFutureTool"
    proc = guard.run(payload)
    assert proc.returncode == 2, proc.stderr


def test_apply_patch_unparseable_envelope_guarded_cwd_deny(guard: GuardHarness) -> None:
    proc = guard.run(guard.apply_patch("no patch markers here"))
    assert proc.returncode == 2, proc.stderr


# --- multi-target tools ---


def test_multiedit_mixed_targets_deny(guard: GuardHarness) -> None:
    proc = guard.run(
        guard.multiedit(
            [guard.repo / "docs/notes.md", guard.repo / "skills/mk-rec/SKILL.md"]
        )
    )
    assert_deny(proc, ROUTE_PHRASE)


def test_notebookedit_deny(guard: GuardHarness) -> None:
    proc = guard.run(guard.notebook(guard.repo / "skills/mk-rec/analysis.ipynb"))
    assert_deny(proc, ROUTE_PHRASE)


def test_apply_patch_all_verbs_deny(guard: GuardHarness) -> None:
    for verb in ("Add", "Update", "Delete"):
        patch = (
            f"*** Begin Patch\n*** {verb} File: skills/mk-rec/SKILL.md\n*** End Patch"
        )
        assert_deny(guard.run(guard.apply_patch(patch)), ROUTE_PHRASE)


def test_apply_patch_move_target_deny(guard: GuardHarness) -> None:
    patch = "*** Begin Patch\n*** Update File: docs/notes.md\n*** Move to: skills/mk-rec/moved.md\n*** End Patch"
    assert_deny(guard.run(guard.apply_patch(patch)), ROUTE_PHRASE)


def test_apply_patch_outside_targets_allow(guard: GuardHarness) -> None:
    patch = "*** Begin Patch\n*** Update File: docs/notes.md\n*** Add File: docs/new.md\n*** End Patch"
    assert_allow(guard.run(guard.apply_patch(patch)))


# --- messages ---


def test_route_message_names_existing_satellite(guard: GuardHarness) -> None:
    guard.add_satellite("mk-rec", parked=True)
    proc = guard.run(guard.edit(guard.repo / "skills/mk-rec/SKILL.md"))
    assert_deny(proc, LIKELY_PHRASE, str(guard.fleet / "mk-rec"))


def test_route_message_generic_for_plugin_subtree(guard: GuardHarness) -> None:
    proc = guard.run(
        guard.edit(guard.repo / "plugins/handoff/references/handoff-format.md")
    )
    assert_deny(proc, GENERIC_PHRASE)
    assert LIKELY_PHRASE not in proc.stderr


def test_route_message_generic_when_no_satellite(guard: GuardHarness) -> None:
    proc = guard.run(guard.edit(guard.repo / "skills/mk-rec/SKILL.md"))
    assert_deny(proc, GENERIC_PHRASE)


# --- bypass ---


def test_bypass_env_allows_with_warning(guard: GuardHarness) -> None:
    proc = guard.run(
        guard.edit(guard.repo / "skills/mk-rec/SKILL.md"),
        env_extra={"SKILL_ROUTE_GUARD_BYPASS": "1"},
    )
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert BYPASS_PHRASE in out["systemMessage"]
    assert out["hookSpecificOutput"]["hookEventName"] == "PreToolUse"


# --- roots stay single-sourced with the fleet controller ---


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None, f"cannot load {path}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(name, None)
    return module


def test_roots_match_satellite_fleet() -> None:
    guard_mod = _load_module(SOURCE_GUARD, "skill_route_guard_under_test")
    fleet_mod = _load_module(SOURCE_FLEET, "satellite_fleet_under_test")
    assert guard_mod.REPO == fleet_mod.REPO
    assert guard_mod.FLEET_ROOT == fleet_mod.FLEET_ROOT
