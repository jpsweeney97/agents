#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# ///
"""Reconcile and operate the permanent skill-satellite fleet.

The repository owns which satellites exist; the git-cycle
``worktree-task-cycle`` helper owns every per-satellite lifecycle verdict and
the shared lease record. This tool never parses or writes ``owner.json``.

Output uses labeled lines only: ``FACT:``, ``POLICY:``, ``REFUSE:``, and
``RESULT:``. Exit codes are 0 for healthy/informational state, 3 for ordinary
catch-up work, 2 for drift or a refused mutation, and 1 for an unexpected
internal failure.
"""

from __future__ import annotations

import argparse
import os
import re
import stat
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

BASE = "main"
CANONICAL_LOCK_REASON = "parked skill workspace (permanent)"
REPO = Path(__file__).resolve().parent.parent
FLEET_ROOT = REPO.parent / f"{REPO.name}-worktrees"
HELPER = (
    REPO
    / "plugins"
    / "git-cycle"
    / "skills"
    / "worktree-task-cycle"
    / "scripts"
    / "worktree_cycle.py"
)
NO_OPTIONAL_LOCKS = "0"

EXIT_OK = 0
EXIT_INTERNAL = 1
EXIT_DRIFT = 2
EXIT_CATCHUP = 3

NOMINAL_ACTIVE_STATES = frozenset(
    {"CONTAINED-UNPARKED", "IN-FLIGHT", "READY", "LANDED-UNPARKED"}
)
REPAIR_STATES = (
    "STALE-ADMIN",
    "LOCK-ABSENT",
    "LOCK-NONCANONICAL",
    "INIT-RESIDUE",
    "SYMLINK-PATH",
    "MOVED-WORKTREE",
)


def say(label: str, message: str) -> None:
    """Print one machine-oriented output line."""

    print(f"{label}: {message}")


def fact(message: str) -> None:
    """Print one observed fact."""

    say("FACT", message)


def policy(message: str) -> None:
    """Print one policy interpretation."""

    say("POLICY", message)


class FleetRefusal(RuntimeError):
    """An expected fail-closed mutation refusal."""


class FleetInternalError(RuntimeError):
    """A violated tool invariant or unreadable dependency contract."""


class FleetArgumentParser(argparse.ArgumentParser):
    """Argument parser that preserves the fleet's labeled refusal contract."""

    def error(self, message: str) -> None:
        """Convert argparse usage failures into normal fleet refusals."""

        raise FleetRefusal(f"argument parsing failed: {message}. Got: {message!r:.100}")


@dataclass(frozen=True)
class SkillSurface:
    """One live SKILL.md-bearing directory in the immutable census snapshot."""

    path: Path
    basename: str
    root_tag: str
    priority: "tuple[int, str]"

    @property
    def prefixed_identity(self) -> str:
        """Return this root's deterministic collision identity."""

        prefix = "skills" if self.root_tag == "skills" else self.root_tag
        return f"{prefix}--{self.basename}"


@dataclass(frozen=True)
class Inventory:
    """One census snapshot and its deterministic identity assignment."""

    surfaces: "tuple[SkillSurface, ...]"
    by_identity: "dict[str, SkillSurface]"
    collisions: "tuple[str, ...]"


@dataclass(frozen=True)
class Worktree:
    """One record from git worktree list --porcelain."""

    path: Path
    head: str
    branch: Optional[str]
    detached: bool
    locked: bool
    lock_reason: Optional[str]


@dataclass(frozen=True)
class Registry:
    """One immutable worktree-registry read for a reconciliation pass."""

    primary: Worktree
    satellites: "tuple[Worktree, ...]"
    common_dir: Path


@dataclass(frozen=True)
class HelperFacts:
    """Pinned tokens returned by worktree_cycle.py inspect."""

    state: str
    lock: str
    lease: str
    lease_purpose: str
    output: str
    exit_code: int


@dataclass(frozen=True)
class Finding:
    """One total fleet classification."""

    classification: str
    identity: str
    detail: str = ""

    @property
    def exit_code(self) -> int:
        """Map the classification to the fleet exit contract."""

        if self.classification in {
            "OK-PARKED",
            "ACTIVE",
            "FLEET-OP",
            "FOREIGN-WORKTREE",
        }:
            return EXIT_OK
        if self.classification in {"MISSING", "RETIRED-PENDING"}:
            return EXIT_CATCHUP
        return EXIT_DRIFT


@dataclass(frozen=True)
class Snapshot:
    """All read-only inputs used by one reconciliation pass."""

    inventory: Inventory
    registry: Registry
    root_entries: "dict[str, str]"
    root_kind: str
    primary_head: str
    primary_branch: Optional[str]
    primary_dirty: bool


def git_env() -> "dict[str, str]":
    """Return an environment that forbids optional Git index writes."""

    env = dict(os.environ)
    env["GIT_OPTIONAL_LOCKS"] = NO_OPTIONAL_LOCKS
    return env


def run_git(*args: str, cwd: Path = REPO) -> "tuple[int, str, str]":
    """Run one guarded Git command under the fleet environment."""

    if any(
        arg == "--force"
        or arg.startswith("--force=")
        or re.fullmatch(r"-f+", arg) is not None
        for arg in args
    ):
        raise FleetInternalError(
            "force flags are prohibited in every fleet git invocation"
        )
    proc = subprocess.run(
        ("git", *args),
        cwd=str(cwd),
        env=git_env(),
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def git_read(*args: str, cwd: Path = REPO, operation: str) -> str:
    """Run a required read-only Git command or raise a labeled internal error."""

    code, out, err = run_git(*args, cwd=cwd)
    if code != 0:
        raise FleetInternalError(
            f"{operation} failed: git {' '.join(args)} exited {code}. Got: {err!r:.100}"
        )
    return out


def lstat_kind(path: Path) -> str:
    """Classify one path without following its final component."""

    try:
        mode = os.lstat(path).st_mode
    except FileNotFoundError:
        return "absent"
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISDIR(mode):
        return "directory"
    return "other"


def root_tagged_surfaces() -> "list[SkillSurface]":
    """Read the canonical live-skill roots once into path-level surfaces."""

    roots: "list[tuple[Path, str, tuple[int, str]]]" = [
        (REPO / "skills", "skills", (0, "")),
        (REPO / "skills-claude", "claude", (1, "")),
    ]
    plugins = REPO / "plugins"
    if not plugins.is_dir():
        raise FleetInternalError(
            f"inventory scan failed: plugin root missing. Got: {str(plugins)!r:.100}"
        )
    for plugin in sorted(path for path in plugins.iterdir() if path.is_dir()):
        skill_root = plugin / "skills"
        if skill_root.is_dir():
            roots.append((skill_root, plugin.name, (2, plugin.name.casefold())))

    surfaces: "list[SkillSurface]" = []
    for root, tag, priority in roots:
        if not root.is_dir():
            raise FleetInternalError(
                f"inventory scan failed: expected skill root missing. Got: {str(root)!r:.100}"
            )
        for candidate in sorted(root.iterdir(), key=lambda path: path.name.casefold()):
            if candidate.is_dir() and (candidate / "SKILL.md").is_file():
                surfaces.append(SkillSurface(candidate, candidate.name, tag, priority))
    return surfaces


def assign_inventory(
    surfaces: "Sequence[SkillSurface]", existing_identities: "set[str]"
) -> Inventory:
    """Assign immutable or deterministic identities to one census snapshot."""

    groups: "dict[str, list[SkillSurface]]" = {}
    for surface in surfaces:
        groups.setdefault(surface.basename.casefold(), []).append(surface)

    by_identity: "dict[str, SkillSurface]" = {}
    collisions: "list[str]" = []
    used_casefold: "dict[str, str]" = {}
    existing_by_casefold: "dict[str, str]" = {}
    for identity in sorted(existing_identities):
        folded = identity.casefold()
        prior = existing_by_casefold.get(folded)
        if prior is not None and prior != identity:
            collisions.append(
                f"existing immutable identities {prior!r} and {identity!r} collide case-insensitively"
            )
            continue
        existing_by_casefold[folded] = identity

    def claim(identity: str, surface: SkillSurface) -> None:
        prior = by_identity.get(identity)
        if prior is not None and prior != surface:
            collisions.append(
                f"identity {identity!r} aliases both {str(prior.path)!r} and {str(surface.path)!r}"
            )
            return
        by_identity[identity] = surface

    for _, group in sorted(groups.items()):
        ordered = sorted(group, key=lambda item: (item.priority, item.path.as_posix()))
        remaining = list(ordered)

        bare_existing = existing_by_casefold.get(ordered[0].basename.casefold())
        if bare_existing is not None:
            claim(bare_existing, remaining.pop(0))

        for surface in tuple(remaining):
            existing = existing_by_casefold.get(surface.prefixed_identity.casefold())
            if existing is not None:
                claim(existing, surface)
                remaining.remove(surface)

        for surface in remaining:
            bare = surface.basename
            identity = (
                bare
                if bare.casefold() not in {name.casefold() for name in by_identity}
                else surface.prefixed_identity
            )
            claim(identity, surface)

    for identity in by_identity:
        folded = identity.casefold()
        prior = used_casefold.get(folded)
        if prior is not None and prior != identity:
            collisions.append(
                f"{prior!r} collides case-insensitively with {identity!r}"
            )
        else:
            used_casefold[folded] = identity
    return Inventory(tuple(surfaces), by_identity, tuple(collisions))


def parse_worktrees(output: str) -> "tuple[Worktree, ...]":
    """Parse git worktree list --porcelain without guessing branch state."""

    records: "list[Worktree]" = []
    for block in output.split("\n\n"):
        lines = [line for line in block.splitlines() if line]
        if not lines:
            continue
        values: "dict[str, str]" = {}
        flags: "set[str]" = set()
        lock_reason: Optional[str] = None
        for line in lines:
            key, _, value = line.partition(" ")
            if key == "locked":
                flags.add("locked")
                lock_reason = value or None
            elif value:
                values[key] = value
            else:
                flags.add(key)
        if "worktree" not in values or "HEAD" not in values:
            raise FleetInternalError(
                f"worktree registry parse failed: incomplete record. Got: {block!r:.100}"
            )
        branch = values.get("branch")
        if branch is not None:
            branch = branch.removeprefix("refs/heads/")
        records.append(
            Worktree(
                path=Path(values["worktree"]).resolve(),
                head=values["HEAD"],
                branch=branch,
                detached="detached" in flags,
                locked="locked" in flags,
                lock_reason=lock_reason,
            )
        )
    if not records:
        raise FleetInternalError("worktree registry parse failed: no records. Got: ''")
    return tuple(records)


def read_registry() -> Registry:
    """Read the common worktree registry and resolve its primary checkout."""

    worktrees = parse_worktrees(
        git_read("worktree", "list", "--porcelain", operation="worktree registry read")
    )
    repo_real = REPO.resolve()
    primary = next((item for item in worktrees if item.path == repo_real), None)
    if primary is None:
        raise FleetInternalError(
            f"primary checkout lookup failed: {str(repo_real)!r} is not registered. Got: {len(worktrees)!r}"
        )
    common_raw = git_read("rev-parse", "--git-common-dir", operation="common-dir read")
    common = Path(common_raw)
    if not common.is_absolute():
        common = (REPO / common).resolve()
    return Registry(
        primary,
        tuple(item for item in worktrees if item.path != primary.path),
        common,
    )


def read_root_entries() -> "tuple[str, dict[str, str]]":
    """Read direct fleet-root entries with lstat discipline."""

    kind = lstat_kind(FLEET_ROOT)
    if kind != "directory":
        return kind, {}
    return kind, {
        entry.name: lstat_kind(Path(entry.path)) for entry in os.scandir(FLEET_ROOT)
    }


def existing_fleet_identities(registry: Registry) -> "set[str]":
    """Return direct-root or canonically locked permanent identities."""

    root = FLEET_ROOT.resolve()
    return {
        item.path.name
        for item in registry.satellites
        if item.path.parent == root
        or (item.locked and item.lock_reason == CANONICAL_LOCK_REASON)
    }


def build_snapshot(inventory: Optional[Inventory] = None) -> Snapshot:
    """Read census, registry, root, and primary facts once for one command."""

    registry = read_registry()
    fixed_inventory = inventory or assign_inventory(
        root_tagged_surfaces(), existing_fleet_identities(registry)
    )
    root_kind, entries = read_root_entries()
    head = git_read("rev-parse", "HEAD", operation="primary HEAD read")
    branch_code, branch, _ = run_git("symbolic-ref", "-q", "--short", "HEAD")
    status = git_read("status", "--porcelain", operation="primary status read")
    return Snapshot(
        fixed_inventory,
        registry,
        entries,
        root_kind,
        head,
        branch if branch_code == 0 else None,
        bool(status),
    )


def run_helper_inspect(path: Path) -> HelperFacts:
    """Invoke the source-tree helper and parse only its pinned machine tokens."""

    if not HELPER.is_file():
        raise FleetInternalError(
            f"canonical helper resolution failed: file missing. Got: {str(HELPER)!r:.100}"
        )
    proc = subprocess.run(
        (sys.executable, str(HELPER), "inspect", str(path), "--base", BASE),
        cwd=str(REPO),
        env=git_env(),
        capture_output=True,
        text=True,
        check=False,
    )
    output = proc.stdout + proc.stderr

    def token(prefix: str) -> str:
        matches = [
            line[len(prefix) :]
            for line in output.splitlines()
            if line.startswith(prefix)
        ]
        if len(matches) != 1:
            raise FleetInternalError(
                f"helper output contract failed: expected one {prefix!r} token. Got: {output!r:.100}"
            )
        return matches[0]

    if proc.returncode not in {0, 2}:
        raise FleetInternalError(
            f"helper inspect failed: exit {proc.returncode}. Got: {output!r:.100}"
        )
    return HelperFacts(
        state=token("STATE: "),
        lock=token("FACT: lock="),
        lease=token("FACT: lease="),
        lease_purpose=token("FACT: lease-purpose="),
        output=output,
        exit_code=proc.returncode,
    )


def classify_helper(
    identity: str,
    helper: HelperFacts,
    worktree: Worktree,
    *,
    in_census: bool,
) -> Finding:
    """Compose pinned helper tokens into the total fleet taxonomy."""

    if helper.lease in {"foreign", "unreadable", "scope-mismatch"}:
        return Finding(
            "RECOVERY:LEASE-ORPHANED",
            identity,
            f"lease={helper.lease} helper-state={helper.state}",
        )
    if helper.lease == "self" and helper.lease_purpose == "fleet":
        return Finding("FLEET-OP", identity, f"helper-state={helper.state}")
    if helper.lock == "absent":
        return Finding("LOCK-ABSENT", identity, f"helper-state={helper.state}")
    if helper.lock == "noncanonical":
        classification = (
            "INIT-RESIDUE"
            if worktree.lock_reason == "initializing"
            else "LOCK-NONCANONICAL"
        )
        return Finding(
            classification,
            identity,
            f"reason={worktree.lock_reason!r} helper-state={helper.state}",
        )
    if (
        helper.state in NOMINAL_ACTIVE_STATES
        and helper.lease == "self"
        and helper.lease_purpose == "task"
    ):
        return Finding("ACTIVE", identity, f"helper-state={helper.state}")
    if helper.state == "PARKED" and helper.lease == "absent":
        return Finding("OK-PARKED" if in_census else "RETIRED-PENDING", identity)
    if helper.state != "PARKED":
        return Finding(f"RECOVERY:{helper.state}", identity)
    return Finding(
        "UNMAPPABLE",
        identity,
        f"helper-state={helper.state} lock={helper.lock} lease={helper.lease}/{helper.lease_purpose}",
    )


def registered_by_identity(registry: Registry) -> "dict[str, list[Worktree]]":
    """Group direct-child fleet registrations by directory identity."""

    root = FLEET_ROOT.resolve()
    grouped: "dict[str, list[Worktree]]" = {}
    for worktree in registry.satellites:
        if worktree.path.parent == root:
            grouped.setdefault(worktree.path.name, []).append(worktree)
    return grouped


def moved_correspondence(snapshot: Snapshot, path: Path) -> Optional[Worktree]:
    """Prove a moved checkout by matching both sides of its admin backpointer."""

    gitfile = path / ".git"
    try:
        mode = os.lstat(gitfile).st_mode
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(mode):
        return None
    try:
        line = gitfile.read_text().strip()
    except OSError:
        return None
    if not line.startswith("gitdir: "):
        return None
    admin = Path(line.removeprefix("gitdir: "))
    admin = (path / admin).resolve() if not admin.is_absolute() else admin.resolve()
    admin_root = (snapshot.registry.common_dir / "worktrees").resolve()
    try:
        admin.relative_to(admin_root)
    except ValueError:
        return None
    backpointer = admin / "gitdir"
    try:
        backpointer_mode = os.lstat(backpointer).st_mode
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(backpointer_mode):
        return None
    try:
        old_gitfile_raw = Path(backpointer.read_text().strip())
    except OSError:
        return None
    old_gitfile = (
        old_gitfile_raw.resolve()
        if old_gitfile_raw.is_absolute()
        else (admin / old_gitfile_raw).resolve()
    )
    old_path = old_gitfile.parent
    for worktree in snapshot.registry.satellites:
        if worktree.path == old_path and lstat_kind(old_path) == "absent":
            return worktree
    return None


def classify_identity_artifact(
    snapshot: Snapshot, identity: str
) -> "Optional[tuple[Finding, Optional[Path]]]":
    """Classify one identity without inspecting unrelated satellites."""

    if snapshot.root_kind != "directory":
        return None
    expected = identity in snapshot.inventory.by_identity
    grouped = registered_by_identity(snapshot.registry)
    registrations = grouped.get(identity, [])
    path = FLEET_ROOT / identity
    path_kind = snapshot.root_entries.get(identity, "absent")

    if len(registrations) > 1:
        return (
            Finding(
                "UNMAPPABLE",
                identity,
                "multiple registered fleet paths share one identity",
            ),
            None,
        )
    if path_kind == "symlink":
        return Finding("SYMLINK-PATH", identity, str(path)), None
    if registrations and path_kind == "absent":
        detail = (
            f"registered={registrations[0].path}"
            if expected
            else "census-absent registered path missing"
        )
        return Finding("STALE-ADMIN", identity, detail), None
    if not registrations and path_kind == "absent":
        misplaced = [
            item
            for item in snapshot.registry.satellites
            if item.path.parent != FLEET_ROOT.resolve()
            and item.path.name == identity
            and item.locked
            and item.lock_reason == CANONICAL_LOCK_REASON
        ]
        if misplaced:
            return (
                Finding(
                    "UNMAPPABLE",
                    identity,
                    f"canonical permanent satellite registered outside fleet root: {misplaced[0].path}",
                ),
                None,
            )
        return (Finding("MISSING", identity), None) if expected else None
    if not registrations:
        if path_kind == "other":
            return Finding("UNMAPPABLE", identity, f"path-kind={path_kind}"), None
        moved = moved_correspondence(snapshot, path)
        if moved is not None:
            return (
                Finding(
                    "MOVED-WORKTREE",
                    identity,
                    f"registered={moved.path} actual={path}",
                ),
                moved.path,
            )
        return Finding("UNEXPECTED-DIR", identity, f"kind={path_kind}"), None
    if path_kind != "directory":
        return Finding("UNMAPPABLE", identity, f"path-kind={path_kind}"), None

    worktree = registrations[0]
    if worktree.path != path.resolve():
        return (
            Finding(
                "UNMAPPABLE",
                identity,
                f"registered path {worktree.path} != expected {path.resolve()}",
            ),
            None,
        )
    return (
        classify_helper(
            identity,
            run_helper_inspect(path),
            worktree,
            in_census=expected,
        ),
        None,
    )


def reconcile(snapshot: Snapshot) -> "list[Finding]":
    """Return one total classification for every census or fleet artifact."""

    findings: "list[Finding]" = []
    if snapshot.root_kind != "directory":
        classification = (
            "SYMLINK-PATH" if snapshot.root_kind == "symlink" else "UNMAPPABLE"
        )
        return [
            Finding(
                classification,
                "<fleet-root>",
                f"path={FLEET_ROOT} kind={snapshot.root_kind}",
            )
        ]
    for message in snapshot.inventory.collisions:
        findings.append(Finding("CASE-COLLISION", "<inventory>", message))

    root = FLEET_ROOT.resolve()
    grouped = registered_by_identity(snapshot.registry)
    identities = (
        set(snapshot.inventory.by_identity) | set(grouped) | set(snapshot.root_entries)
    )
    moved_registry_paths: "set[Path]" = set()
    for identity in sorted(identities, key=str.casefold):
        classified = classify_identity_artifact(snapshot, identity)
        if classified is None:
            continue
        finding, moved_path = classified
        findings.append(finding)
        if moved_path is not None:
            moved_registry_paths.add(moved_path)

    for worktree in snapshot.registry.satellites:
        if worktree.path.parent != root and worktree.path not in moved_registry_paths:
            if (
                worktree.path.name in snapshot.inventory.by_identity
                and worktree.locked
                and worktree.lock_reason == CANONICAL_LOCK_REASON
            ):
                continue
            findings.append(
                Finding("FOREIGN-WORKTREE", worktree.path.name, str(worktree.path))
            )

    return findings


def aggregate_exit(findings: "Sequence[Finding]") -> int:
    """Return the highest-priority fleet exit class."""

    if any(item.exit_code == EXIT_DRIFT for item in findings):
        return EXIT_DRIFT
    if any(item.exit_code == EXIT_CATCHUP for item in findings):
        return EXIT_CATCHUP
    return EXIT_OK


def emit_snapshot_facts(snapshot: Snapshot) -> None:
    """Emit the immutable snapshot anchors required by the fleet contract."""

    fact(f"census={len(snapshot.inventory.surfaces)}")
    fact(
        f"primary-head={snapshot.primary_head} "
        f"dirty={'true' if snapshot.primary_dirty else 'false'}"
    )
    fact(
        f"primary-branch={snapshot.primary_branch!r} fleet-root={str(FLEET_ROOT)!r} "
        f"registered={len(snapshot.registry.satellites) + 1}"
    )


def emit_findings(findings: "Sequence[Finding]") -> None:
    """Emit deterministic per-artifact classifications."""

    for finding in sorted(
        findings, key=lambda item: (item.identity.casefold(), item.classification)
    ):
        suffix = f" detail={finding.detail}" if finding.detail else ""
        say("RESULT", f"{finding.classification} identity={finding.identity}{suffix}")


def cmd_check(_args: argparse.Namespace) -> int:
    """Run a read-only census, registry, root, and helper reconciliation."""

    snapshot = build_snapshot()
    findings = reconcile(snapshot)
    emit_snapshot_facts(snapshot)
    emit_findings(findings)
    code = aggregate_exit(findings)
    say("RESULT", f"check exit={code} findings={len(findings)}")
    return code


def primary_op_markers(snapshot: Snapshot) -> "list[str]":
    """Return operation markers that make fleet mutation unsafe."""

    names = (
        "rebase-merge",
        "rebase-apply",
        "MERGE_HEAD",
        "CHERRY_PICK_HEAD",
        "REVERT_HEAD",
        "BISECT_LOG",
    )
    return [name for name in names if (snapshot.registry.common_dir / name).exists()]


def require_mutation_preflight(snapshot: Snapshot) -> None:
    """Require the primary integration lane to be clean on main."""

    markers = primary_op_markers(snapshot)
    if (
        snapshot.root_kind != "directory"
        or snapshot.primary_branch != BASE
        or snapshot.primary_dirty
        or markers
    ):
        raise FleetRefusal(
            "primary preflight refused: expected real fleet root plus clean-on-main with no operation markers. "
            f"Got: branch={snapshot.primary_branch!r} dirty={snapshot.primary_dirty!r} "
            f"markers={markers!r} root-kind={snapshot.root_kind!r}"
        )


def identity_finding(snapshot: Snapshot, identity: str) -> Finding:
    """Return the one non-foreign finding for an expected fleet identity."""

    classified = classify_identity_artifact(snapshot, identity)
    if identity not in snapshot.inventory.by_identity or classified is None:
        raise FleetInternalError(
            f"identity classification failed: expected one census finding. Got: {identity!r:.100}"
        )
    return classified[0]


def git_mutate(*args: str, operation: str) -> str:
    """Run one allowed Git mutation and convert failure into a refusal."""

    code, out, err = run_git(*args)
    if code != 0:
        raise FleetRefusal(
            f"{operation} failed: git {' '.join(args)} exited {code}. Got: {(err or out)!r:.100}"
        )
    return out


def create_one(identity: str, inventory: Inventory) -> str:
    """Create or idempotently accept one census identity."""

    snapshot = build_snapshot(inventory)
    require_mutation_preflight(snapshot)
    if inventory.collisions:
        raise FleetRefusal(
            f"create refused: CASE-COLLISION in immutable census. Got: {inventory.collisions!r:.100}"
        )
    if identity not in inventory.by_identity:
        raise FleetRefusal(
            f"create refused: identity is not in the immutable census. Got: {identity!r:.100}"
        )
    before = identity_finding(snapshot, identity)
    if before.classification == "OK-PARKED":
        say("RESULT", f"ALREADY-OK identity={identity}")
        return "already-ok"
    if before.classification != "MISSING":
        raise FleetRefusal(
            f"create refused: {identity!r} is {before.classification}, not MISSING. "
            f"Got: {before.detail!r:.100}"
        )

    target = FLEET_ROOT / identity
    if lstat_kind(target) != "absent":
        raise FleetRefusal(
            f"create path precondition failed: target must be absent; no adoption. Got: {str(target)!r:.100}"
        )
    git_mutate(
        "worktree",
        "add",
        "--detach",
        "--lock",
        "--reason",
        CANONICAL_LOCK_REASON,
        str(target),
        BASE,
        operation=f"create {identity!r}",
    )
    after = identity_finding(build_snapshot(inventory), identity)
    if after.classification != "OK-PARKED":
        say(
            "RESULT",
            f"CREATED-BUT-NOT-PARKED identity={identity} class={after.classification}",
        )
        raise FleetRefusal(
            f"create postcondition failed: helper did not prove exact PARKED with canonical lock. Got: {after.classification!r:.100}"
        )
    say("RESULT", f"CREATED identity={identity}")
    return "created"


def cmd_create(args: argparse.Namespace) -> int:
    """Create one missing census identity with an atomic locked add."""

    snapshot = build_snapshot()
    emit_snapshot_facts(snapshot)
    create_one(args.identity, snapshot.inventory)
    return EXIT_OK


def cmd_create_missing(_args: argparse.Namespace) -> int:
    """Create every missing census identity, stopping on the first failure."""

    snapshot = build_snapshot()
    require_mutation_preflight(snapshot)
    findings = reconcile(snapshot)
    emit_snapshot_facts(snapshot)
    drift = [item for item in findings if item.exit_code == EXIT_DRIFT]
    if drift:
        emit_findings(drift)
        raise FleetRefusal(
            f"create-missing preflight found drift; repair before rollout. Got: {[item.classification for item in drift]!r:.100}"
        )
    unresolved = [
        item
        for item in findings
        if item.classification in {"FLEET-OP", "RETIRED-PENDING"}
    ]
    if unresolved:
        emit_findings(unresolved)
        raise FleetRefusal(
            "create-missing preflight found an unfinished fleet operation or retirement; "
            f"adjudicate it before rollout. Got: {[item.classification for item in unresolved]!r:.100}"
        )
    missing = sorted(
        (item.identity for item in findings if item.classification == "MISSING"),
        key=str.casefold,
    )
    completed: "list[str]" = []
    for index, identity in enumerate(missing):
        try:
            create_one(identity, snapshot.inventory)
        except FleetRefusal:
            untouched = missing[index + 1 :]
            say(
                "RESULT",
                "create-missing "
                f"completed={','.join(completed) or 'none'} refused={identity} "
                f"untouched={','.join(untouched) or 'none'}",
            )
            raise
        completed.append(identity)
    say(
        "RESULT",
        "create-missing "
        f"completed={','.join(completed) or 'none'} refused=none untouched=none",
    )
    return EXIT_OK


def invoke_helper(*args: str, operation: str) -> str:
    """Run one helper-owned mutation primitive or convert it to a refusal."""

    if not HELPER.is_file():
        raise FleetInternalError(
            f"canonical helper resolution failed: file missing. Got: {str(HELPER)!r:.100}"
        )
    proc = subprocess.run(
        (sys.executable, str(HELPER), *args),
        cwd=str(REPO),
        env=git_env(),
        capture_output=True,
        text=True,
        check=False,
    )
    output = proc.stdout + proc.stderr
    if proc.returncode != 0:
        raise FleetRefusal(
            f"{operation} failed: helper exited {proc.returncode}. Got: {output!r:.100}"
        )
    return output


def fleet_lease_path(snapshot: Snapshot, identity: str) -> Path:
    """Return the helper-owned identity lease path without inspecting its record."""

    return (
        snapshot.registry.common_dir
        / "skill-worktree"
        / "leases"
        / f"wt-{identity}.lease"
    )


def require_no_identity_lease(snapshot: Snapshot, identity: str, verb: str) -> None:
    """Refuse every existing identity lease without reading owner data."""

    lease = fleet_lease_path(snapshot, identity)
    if lstat_kind(lease) != "absent":
        raise FleetRefusal(
            f"{verb} refused: identity lease already exists; no owner inference. Got: {str(lease)!r:.100}"
        )


def acquire_fleet_lease(
    snapshot: Snapshot, identity: str, path: Path, verb: str
) -> None:
    """Acquire one helper-owned fleet lease after an absence-only precheck."""

    require_no_identity_lease(snapshot, identity, verb)
    invoke_helper(
        "fleet-lease-acquire",
        str(REPO),
        "--identity",
        identity,
        "--path",
        str(path),
        "--purpose",
        f"fleet:{verb}",
        operation=f"{verb} lease acquisition",
    )
    fact(f"fleet-lease acquired identity={identity} purpose=fleet:{verb}")


def release_fleet_lease(identity: str, path: Path, verb: str) -> str:
    """Release one helper-owned lease and return its stable terminal shape."""

    output = invoke_helper(
        "fleet-lease-release",
        str(REPO),
        "--identity",
        identity,
        "--path",
        str(path),
        operation=f"{verb} lease release",
    )
    match = re.search(r"terminal=(healthy|decommissioned|bare)", output)
    if match is None:
        raise FleetInternalError(
            f"fleet lease release output lacked a terminal token. Got: {output!r:.100}"
        )
    terminal = match.group(1)
    fact(f"fleet-lease released identity={identity} terminal={terminal}")
    return terminal


def release_after_failure(identity: str, path: Path, verb: str) -> None:
    """Attempt stable release after a failed operation, retaining ambiguous leases."""

    try:
        terminal = release_fleet_lease(identity, path, verb)
    except (FleetRefusal, FleetInternalError) as exc:
        policy(f"{verb} failed with ambiguous live state; fleet lease retained: {exc}")
    else:
        policy(
            f"{verb} failed before an ambiguous mutation; fleet lease released at {terminal}"
        )


def raw_identity_finding(snapshot: Snapshot, identity: str) -> Finding:
    """Return one non-foreign finding for any live or retired identity."""

    classified = classify_identity_artifact(snapshot, identity)
    if classified is None:
        raise FleetRefusal(
            f"identity does not map to one fleet artifact. Got: {identity!r:.100}"
        )
    return classified[0]


def exact_registration(snapshot: Snapshot, identity: str, path: Path) -> Worktree:
    """Require one registry record at the canonical identity path."""

    expected = path.resolve()
    matches = [item for item in snapshot.registry.satellites if item.path == expected]
    if len(matches) != 1 or matches[0].path.name != identity:
        raise FleetRefusal(
            f"registry recheck failed for {identity!r}. Got: {[str(item.path) for item in matches]!r:.100}"
        )
    return matches[0]


def require_helper_parked(path: Path, *, lock: str) -> HelperFacts:
    """Require the exact helper PARKED state under a fleet-purpose SELF lease."""

    helper = run_helper_inspect(path)
    if not (
        helper.state == "PARKED"
        and helper.lock == lock
        and helper.lease == "self"
        and helper.lease_purpose == "fleet"
    ):
        raise FleetRefusal(
            "PARKED boundary recheck failed: expected helper PARKED plus SELF fleet lease "
            f"and lock={lock!r}. Got: state={helper.state!r} lock={helper.lock!r} "
            f"lease={helper.lease!r}/{helper.lease_purpose!r}"
        )
    return helper


def verify_decommissioned(inventory: Inventory, identity: str, path: Path) -> None:
    """Require both registry and filesystem absence after decommission."""

    snapshot = build_snapshot(inventory)
    if lstat_kind(path) != "absent" or any(
        item.path == path.resolve() for item in snapshot.registry.satellites
    ):
        raise FleetRefusal(
            f"decommission verification failed for {identity!r}. Got: path-kind={lstat_kind(path)!r}"
        )


def decommission_parked(identity: str, path: Path, inventory: Inventory) -> None:
    """Unlock, recheck, and non-force remove one canonical parked satellite."""

    snapshot = build_snapshot(inventory)
    exact_registration(snapshot, identity, path)
    require_helper_parked(path, lock="canonical")
    git_mutate("worktree", "unlock", str(path), operation=f"unlock {identity!r}")
    after_unlock = build_snapshot(inventory)
    unlocked = exact_registration(after_unlock, identity, path)
    if unlocked.locked:
        raise FleetRefusal(
            f"unlock recheck failed: registry still reports locked. Got: {identity!r:.100}"
        )
    require_helper_parked(path, lock="absent")
    git_mutate("worktree", "remove", str(path), operation=f"remove {identity!r}")
    verify_decommissioned(inventory, identity, path)


def stale_admin_registration(snapshot: Snapshot, identity: str, path: Path) -> Worktree:
    """Require one locked missing-path registry entry for stale-admin repair."""

    expected = path.resolve()
    matches = [item for item in snapshot.registry.satellites if item.path == expected]
    if len(matches) != 1 or not matches[0].locked or lstat_kind(path) != "absent":
        raise FleetRefusal(
            f"STALE-ADMIN recheck failed for {identity!r}. Got: matches={len(matches)!r} "
            f"path-kind={lstat_kind(path)!r}"
        )
    return matches[0]


def repair_stale_admin(identity: str, path: Path, inventory: Inventory) -> None:
    """Unlock and identity-remove one proven stale admin record."""

    stale_admin_registration(build_snapshot(inventory), identity, path)
    git_mutate("worktree", "unlock", str(path), operation=f"unlock stale {identity!r}")
    after_unlock = build_snapshot(inventory)
    expected = path.resolve()
    matches = [
        item for item in after_unlock.registry.satellites if item.path == expected
    ]
    if len(matches) != 1 or matches[0].locked or lstat_kind(path) != "absent":
        raise FleetRefusal(
            f"STALE-ADMIN post-unlock recheck failed. Got: {matches!r:.100}"
        )
    git_mutate("worktree", "remove", str(path), operation=f"remove stale {identity!r}")
    verify_decommissioned(inventory, identity, path)


def trash_path(path: Path, *, operation: str) -> None:
    """Move one exact path to Trash without traversing it."""

    proc = subprocess.run(
        ("trash", str(path)),
        cwd=str(REPO),
        env=git_env(),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise FleetRefusal(
            f"{operation} failed: trash exited {proc.returncode}. Got: {proc.stderr!r:.100}"
        )


def cmd_repair(args: argparse.Namespace) -> int:
    """Run one closed-enum, state-matched attended repair route."""

    snapshot = build_snapshot()
    require_mutation_preflight(snapshot)
    require_no_identity_lease(snapshot, args.identity, "repair")
    live = raw_identity_finding(snapshot, args.identity)
    if live.classification != args.state:
        raise FleetRefusal(
            f"repair refused: named state {args.state} does not match live {live.classification}. "
            f"Got: {args.identity!r:.100}"
        )
    if args.state == "INIT-RESIDUE":
        raise FleetRefusal(
            "INIT-RESIDUE repair is report-only: no native interrupted-add fixture "
            f"proved a safe unlock/remove route. Got: {args.identity!r:.100}"
        )
    if args.state == "LOCK-NONCANONICAL":
        registrations = registered_by_identity(snapshot.registry).get(args.identity, [])
        reason = registrations[0].lock_reason if len(registrations) == 1 else None
        if args.confirm_reason != reason:
            raise FleetRefusal(
                f"confirmation reason mismatch: expected {reason!r}. Got: {args.confirm_reason!r:.100}"
            )
    if (
        args.state in {"SYMLINK-PATH", "MOVED-WORKTREE"}
        and args.confirm != args.identity
    ):
        raise FleetRefusal(
            f"repair confirmation mismatch: expected {args.identity!r}. Got: {args.confirm!r:.100}"
        )

    path = FLEET_ROOT / args.identity
    acquire_fleet_lease(snapshot, args.identity, path, "repair")
    try:
        if args.state == "STALE-ADMIN":
            repair_stale_admin(args.identity, path, snapshot.inventory)
        elif args.state == "LOCK-ABSENT":
            exact_registration(build_snapshot(snapshot.inventory), args.identity, path)
            require_helper_parked(path, lock="absent")
            git_mutate(
                "worktree",
                "lock",
                "--reason",
                CANONICAL_LOCK_REASON,
                str(path),
                operation=f"relock {args.identity!r}",
            )
            require_helper_parked(path, lock="canonical")
        elif args.state == "LOCK-NONCANONICAL":
            exact_registration(build_snapshot(snapshot.inventory), args.identity, path)
            require_helper_parked(path, lock="noncanonical")
            git_mutate(
                "worktree", "unlock", str(path), operation=f"unlock {args.identity!r}"
            )
            exact_registration(build_snapshot(snapshot.inventory), args.identity, path)
            require_helper_parked(path, lock="absent")
            git_mutate(
                "worktree",
                "lock",
                "--reason",
                CANONICAL_LOCK_REASON,
                str(path),
                operation=f"relock {args.identity!r}",
            )
            require_helper_parked(path, lock="canonical")
        elif args.state == "SYMLINK-PATH":
            if lstat_kind(path) != "symlink":
                raise FleetRefusal(
                    f"SYMLINK-PATH recheck failed before trash. Got: {lstat_kind(path)!r:.100}"
                )
            trash_path(path, operation=f"trash symlink {args.identity!r}")
            if lstat_kind(path) != "absent":
                raise FleetRefusal(
                    f"symlink trash verification failed. Got: {lstat_kind(path)!r:.100}"
                )
            remaining = [
                item
                for item in build_snapshot(snapshot.inventory).registry.satellites
                if item.path.name == args.identity
            ]
            if remaining:
                if (
                    len(remaining) == 1
                    and remaining[0].locked
                    and lstat_kind(remaining[0].path) == "absent"
                ):
                    repair_stale_admin(
                        args.identity, remaining[0].path, snapshot.inventory
                    )
                else:
                    raise FleetRefusal(
                        f"symlink removed but registered state is not STALE-ADMIN. Got: {remaining!r:.100}"
                    )
        elif args.state == "MOVED-WORKTREE":
            current = build_snapshot(snapshot.inventory)
            if moved_correspondence(current, path) is None:
                raise FleetRefusal(
                    f"MOVED-WORKTREE correspondence vanished before repair. Got: {str(path)!r:.100}"
                )
            git_mutate(
                "worktree",
                "repair",
                str(path),
                operation=f"repair moved {args.identity!r}",
            )
            exact_registration(build_snapshot(snapshot.inventory), args.identity, path)
            require_helper_parked(path, lock="canonical")
        else:
            raise FleetInternalError(
                f"closed repair dispatcher missed a state. Got: {args.state!r:.100}"
            )
        terminal = release_fleet_lease(args.identity, path, "repair")
    except (FleetRefusal, FleetInternalError):
        release_after_failure(args.identity, path, "repair")
        raise
    say(
        "RESULT",
        f"REPAIRED identity={args.identity} state={args.state} terminal={terminal}",
    )
    return EXIT_OK


def decommission_command(args: argparse.Namespace, *, unwind: bool) -> int:
    """Run retire or explicitly-confirmed eager-fleet unwind."""

    snapshot = build_snapshot()
    require_mutation_preflight(snapshot)
    identity = args.identity
    require_no_identity_lease(snapshot, identity, "unwind" if unwind else "retire")
    if unwind:
        if args.confirm != identity:
            raise FleetRefusal(
                f"unwind confirmation mismatch: expected {identity!r}. Got: {args.confirm!r:.100}"
            )
    elif identity in snapshot.inventory.by_identity:
        raise FleetRefusal(
            f"retire refused: identity is still present in the immutable census. Got: {identity!r:.100}"
        )
    live = raw_identity_finding(snapshot, identity)
    allowed = {"OK-PARKED", "RETIRED-PENDING"} if unwind else {"RETIRED-PENDING"}
    if live.classification not in allowed:
        raise FleetRefusal(
            f"{'unwind' if unwind else 'retire'} requires a healthy parked satellite. "
            f"Got: {live.classification!r:.100}"
        )
    verb = "unwind" if unwind else "retire"
    path = FLEET_ROOT / identity
    acquire_fleet_lease(snapshot, identity, path, verb)
    try:
        decommission_parked(identity, path, snapshot.inventory)
        terminal = release_fleet_lease(identity, path, verb)
    except (FleetRefusal, FleetInternalError):
        release_after_failure(identity, path, verb)
        raise
    say(
        "RESULT",
        f"{'UNWOUND' if unwind else 'RETIRED'} identity={identity} terminal={terminal}",
    )
    return EXIT_OK


def cmd_retire(args: argparse.Namespace) -> int:
    """Retire one census-absent healthy satellite."""

    return decommission_command(args, unwind=False)


def cmd_unwind(args: argparse.Namespace) -> int:
    """Explicitly unwind one healthy eager-fleet satellite."""

    return decommission_command(args, unwind=True)


def build_parser() -> argparse.ArgumentParser:
    """Build the public fleet CLI."""

    parser = FleetArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")
    check = sub.add_parser("check", help="read-only fleet reconciliation")
    check.set_defaults(func=cmd_check)
    create = sub.add_parser("create")
    create.add_argument("identity")
    create.set_defaults(func=cmd_create)
    repair = sub.add_parser("repair")
    repair.add_argument("identity")
    repair.add_argument("--state", required=True, choices=REPAIR_STATES)
    repair.add_argument("--confirm")
    repair.add_argument("--confirm-reason")
    repair.set_defaults(func=cmd_repair)
    retire = sub.add_parser("retire")
    retire.add_argument("identity")
    retire.set_defaults(func=cmd_retire)
    unwind = sub.add_parser("unwind")
    unwind.add_argument("identity")
    unwind.add_argument("--confirm", required=True)
    unwind.set_defaults(func=cmd_unwind)
    create_missing = sub.add_parser("create-missing")
    create_missing.set_defaults(func=cmd_create_missing)
    return parser


def main(argv: "Optional[Sequence[str]]" = None) -> int:
    """Run one fleet command and honor the labeled exit contract."""

    args_list = list(sys.argv[1:] if argv is None else argv)
    if not args_list:
        args_list = ["check"]
    try:
        parser = build_parser()
        args = parser.parse_args(args_list)
        if not hasattr(args, "func"):
            raise FleetRefusal("argument parsing failed: a command is required")
        return int(args.func(args))
    except FleetRefusal as exc:
        say("REFUSE", str(exc))
        say("RESULT", "refused")
        return EXIT_DRIFT
    except FleetInternalError as exc:
        say("REFUSE", f"internal error: {exc}")
        say("RESULT", "internal-error")
        return EXIT_INTERNAL
    except OSError as exc:
        say(
            "REFUSE", f"internal error: operating-system call failed. Got: {exc!r:.100}"
        )
        say("RESULT", "internal-error")
        return EXIT_INTERNAL


if __name__ == "__main__":
    raise SystemExit(main())
