#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal


SCRIPT_DIR = Path(__file__).resolve().parent
SCANNER = SCRIPT_DIR / "scoped_safety_scan.py"
DEFAULT_RETENTION = "keep until simplification review is complete"

GitState = Literal["git", "non-git"]


@dataclass(frozen=True)
class ScopedFile:
    input_path: Path
    absolute_path: Path
    relative_path: Path
    scanner_status: str
    scanner_categories: dict[str, str]


@dataclass(frozen=True)
class BackupRecord:
    relative_path: Path
    scanner_status: str
    backup_action: Literal["copied", "excluded"]
    reason: str
    sha256: str | None = None
    restore_limit: str | None = None
    copied_to: Path | None = None


def command_failed(operation: str, reason: str, got: object) -> RuntimeError:
    return RuntimeError(f"{operation} failed: {reason}. Got: {got!r:.100}")


def run_command(
    cmd: list[str],
    *,
    cwd: Path,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or result.returncode
        raise command_failed("command", str(detail), cmd)
    return result


def slugify(value: str, *, default: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._")
    return (slug or default)[:80]


def resolve_existing_root(raw_root: Path) -> Path:
    root = raw_root.expanduser().resolve()
    if not root.is_dir():
        raise command_failed("resolve root", "root is not a directory", str(raw_root))
    return root


def discover_git_root(cwd: Path) -> Path | None:
    result = run_command(["git", "rev-parse", "--show-toplevel"], cwd=cwd, check=False)
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


def common_path_root(paths: list[Path], cwd: Path) -> Path:
    absolute_paths = [
        (cwd / path).resolve() if not path.is_absolute() else path.resolve()
        for path in paths
    ]
    parents = [path if path.is_dir() else path.parent for path in absolute_paths]
    common = Path(os.path.commonpath([str(parent) for parent in parents])).resolve()
    return common if common.is_dir() else common.parent


def root_for_args(args: argparse.Namespace, cwd: Path) -> tuple[Path, GitState]:
    if args.root is not None:
        root = resolve_existing_root(args.root)
        git_root = discover_git_root(root)
        if git_root is not None:
            return git_root, "git"
        return root, "non-git"

    git_root = discover_git_root(cwd)
    if git_root is not None:
        return git_root, "git"

    return common_path_root(args.paths, cwd), "non-git"


def ensure_inside_root(path: Path, root: Path) -> Path:
    try:
        return path.resolve().relative_to(root)
    except ValueError as exc:
        raise command_failed("resolve path", "path is outside root", str(path)) from exc


def git_output(args: list[str], root: Path, *, check: bool = True) -> str:
    return run_command(["git", *args], cwd=root, check=check).stdout


def current_branch(root: Path, state: GitState) -> str | None:
    if state == "non-git":
        return None
    result = run_command(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root, check=False
    )
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip() or "unknown"


def current_head(root: Path, state: GitState) -> str | None:
    if state == "non-git":
        return None
    result = run_command(["git", "rev-parse", "HEAD"], cwd=root, check=False)
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def ensure_backup_root(root: Path, state: GitState, backup_root: Path | None) -> Path:
    target = backup_root.expanduser().resolve() if backup_root is not None else None
    if target is None and state == "git":
        target = root / ".backup"
    if target is None:
        target = Path.home() / "backup" / slugify(root.name, default="non-git-root")

    try:
        target.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise command_failed("create backup root", str(exc), str(target)) from exc

    if not target.is_dir():
        raise command_failed("create backup root", "not a directory", str(target))
    return target


def unique_artifact_path(
    backup_root: Path, *, branch: str | None, scope_slug: str
) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    branch_slug = slugify(branch or "no-branch", default="no-branch")
    scope = slugify(scope_slug, default="scope")
    base = backup_root / f"{timestamp}-{branch_slug}-{scope}-simplify-code"
    candidate = base
    counter = 2
    while candidate.exists():
        candidate = backup_root / f"{base.name}-{counter}"
        counter += 1
    candidate.mkdir(parents=False)
    return candidate


def add_git_exclude(root: Path, backup_root: Path) -> None:
    if backup_root != root / ".backup":
        return
    exclude_path_text = git_output(
        ["rev-parse", "--git-path", "info/exclude"], root
    ).strip()
    exclude_path = (
        (root / exclude_path_text).resolve()
        if not Path(exclude_path_text).is_absolute()
        else Path(exclude_path_text)
    )
    exclude_path.parent.mkdir(parents=True, exist_ok=True)
    existing = exclude_path.read_text(encoding="utf-8") if exclude_path.exists() else ""
    if ".backup/" in existing.splitlines():
        return
    separator = "" if existing.endswith("\n") or not existing else "\n"
    exclude_path.write_text(f"{existing}{separator}.backup/\n", encoding="utf-8")


def run_scanner(paths: list[Path], root: Path) -> dict[str, object]:
    cmd = [sys.executable, str(SCANNER), *(str(path) for path in paths)]
    result = run_command(cmd, cwd=root, check=False)
    if not result.stdout.strip():
        detail = result.stderr.strip() or result.returncode
        raise command_failed("scoped safety scan", "no JSON output", detail)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise command_failed(
            "scoped safety scan", "invalid JSON output", result.stdout[:200]
        ) from exc
    if result.returncode not in {0, 1}:
        raise command_failed(
            "scoped safety scan", "scanner error", result.stderr.strip()
        )
    return payload


def scanner_file_map(payload: dict[str, object]) -> dict[str, dict[str, object]]:
    files = payload.get("files")
    if not isinstance(files, list):
        raise command_failed("parse scanner output", "files is not a list", payload)
    mapped: dict[str, dict[str, object]] = {}
    for file_payload in files:
        if not isinstance(file_payload, dict):
            raise command_failed(
                "parse scanner output", "file entry is not an object", file_payload
            )
        path = file_payload.get("path")
        if not isinstance(path, str):
            raise command_failed(
                "parse scanner output", "file path is missing", file_payload
            )
        mapped[str(Path(path).resolve())] = file_payload
    return mapped


def scoped_files(
    paths: list[Path], root: Path, scanner_payload: dict[str, object], cwd: Path
) -> list[ScopedFile]:
    by_path = scanner_file_map(scanner_payload)
    files: list[ScopedFile] = []
    for input_path in paths:
        absolute_path = (
            (cwd / input_path).resolve()
            if not input_path.is_absolute()
            else input_path.resolve()
        )
        file_payload = by_path.get(str(absolute_path))
        if file_payload is None:
            raise command_failed(
                "parse scanner output", "scanned file missing", str(absolute_path)
            )
        categories = file_payload.get("categories")
        status = file_payload.get("status")
        if not isinstance(categories, dict) or not isinstance(status, str):
            raise command_failed(
                "parse scanner output", "file status is invalid", file_payload
            )
        files.append(
            ScopedFile(
                input_path=input_path,
                absolute_path=absolute_path,
                relative_path=ensure_inside_root(absolute_path, root),
                scanner_status=status,
                scanner_categories={
                    str(key): str(value) for key, value in categories.items()
                },
            )
        )
    return files


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def copy_or_exclude(scoped: ScopedFile, artifact: Path) -> BackupRecord:
    if (
        scoped.scanner_status == "clean"
        and scoped.absolute_path.is_file()
        and not scoped.absolute_path.is_symlink()
    ):
        target = artifact / "files" / scoped.relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(scoped.absolute_path, target)
        return BackupRecord(
            relative_path=scoped.relative_path,
            scanner_status=scoped.scanner_status,
            backup_action="copied",
            reason="scanner clean text file",
            sha256=sha256_file(scoped.absolute_path),
            restore_limit=f"restorable from files/{scoped.relative_path.as_posix()}",
            copied_to=target.relative_to(artifact),
        )

    categories = ", ".join(
        f"{name}={status}"
        for name, status in sorted(scoped.scanner_categories.items())
        if status != "clean"
    )
    reason = categories or f"scanner_status={scoped.scanner_status}"
    return BackupRecord(
        relative_path=scoped.relative_path,
        scanner_status=scoped.scanner_status,
        backup_action="excluded",
        reason=reason,
        restore_limit="not restorable from this artifact",
    )


def write_git_evidence(
    artifact: Path, root: Path, scoped: list[ScopedFile], state: GitState
) -> None:
    if state == "non-git":
        return
    relpaths = [file.relative_path.as_posix() for file in scoped]
    (artifact / "status.txt").write_text(
        git_output(["status", "--short", "--branch"], root), encoding="utf-8"
    )
    (artifact / "diff.patch").write_text(
        git_output(["diff", "--", *relpaths], root), encoding="utf-8"
    )
    (artifact / "cached.diff.patch").write_text(
        git_output(["diff", "--cached", "--", *relpaths], root), encoding="utf-8"
    )
    (artifact / "untracked.txt").write_text(
        git_output(
            ["ls-files", "--others", "--exclude-standard", "--", *relpaths], root
        ),
        encoding="utf-8",
    )


def manifest_text(
    *,
    root: Path,
    state: GitState,
    branch: str | None,
    head: str | None,
    artifact: Path,
    scope_slug: str,
    planned_verification: str,
    retention: str,
    scanner_payload: dict[str, object],
    records: list[BackupRecord],
    allow_exclusions: bool,
) -> str:
    lines = [
        "simplify-code backup manifest",
        f"root: {root}",
        f"repo_state: {state}",
        f"branch: {branch or 'no-git'}",
        f"head: {head or 'none'}",
        f"artifact_path: {artifact}",
        f"scope: {scope_slug}",
        f"planned_verification: {planned_verification}",
        f"retention: {retention}",
        f"scanner_overall_status: {scanner_payload.get('overall_status', 'unknown')}",
        f"exclusions_allowed: {str(allow_exclusions).lower()}",
        "files:",
    ]
    for record in records:
        lines.extend(
            [
                f"- path: {record.relative_path.as_posix()}",
                f"  scanner_status: {record.scanner_status}",
                f"  backup_action: {record.backup_action}",
                f"  reason: {record.reason}",
            ]
        )
        if record.sha256 is not None:
            lines.append(f"  sha256: {record.sha256}")
        if record.copied_to is not None:
            lines.append(f"  copied_to: {record.copied_to.as_posix()}")
        if record.restore_limit is not None:
            lines.append(f"  restore_limit: {record.restore_limit}")
    return "\n".join(lines) + "\n"


def payload_for(
    *,
    ok: bool,
    root: Path,
    state: GitState,
    branch: str | None,
    head: str | None,
    artifact: Path,
    scanner_payload: dict[str, object],
    records: list[BackupRecord],
    allow_exclusions: bool,
) -> dict[str, object]:
    return {
        "ok": ok,
        "root": str(root),
        "git": state == "git",
        "branch": branch,
        "head": head,
        "artifact_path": str(artifact),
        "scanner_overall_status": scanner_payload.get("overall_status"),
        "exclusions_require_approval": any(
            record.backup_action == "excluded" for record in records
        )
        and not allow_exclusions,
        "files": [
            {
                "path": record.relative_path.as_posix(),
                "scanner_status": record.scanner_status,
                "backup_action": record.backup_action,
                "reason": record.reason,
                "sha256": record.sha256,
                "copied_to": record.copied_to.as_posix() if record.copied_to else None,
                "restore_limit": record.restore_limit,
            }
            for record in records
        ],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a secret-safe simplify-code pre-edit backup artifact."
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Explicit project root. In git repos, the repository root is still used for backup evidence.",
    )
    parser.add_argument(
        "--backup-root",
        type=Path,
        help="Explicit directory where the backup artifact is created.",
    )
    parser.add_argument(
        "--scope-slug", required=True, help="Short slug for the simplification scope."
    )
    parser.add_argument(
        "--planned-verification",
        required=True,
        help="Planned verification strength, such as 'strong plan' or 'moderate plan'.",
    )
    parser.add_argument(
        "--retention", default=DEFAULT_RETENTION, help="Retention/cleanup expectation."
    )
    parser.add_argument(
        "--allow-exclusions",
        action="store_true",
        help="Return success even when scoped files are excluded from restorable backup.",
    )
    parser.add_argument(
        "paths", nargs="+", type=Path, help="Explicit editable files to back up."
    )
    return parser.parse_args(argv)


def create_backup(args: argparse.Namespace, cwd: Path) -> tuple[int, dict[str, object]]:
    root, state = root_for_args(args, cwd)
    branch = current_branch(root, state)
    head = current_head(root, state)
    backup_root = ensure_backup_root(root, state, args.backup_root)
    if state == "git":
        add_git_exclude(root, backup_root)

    absolute_paths = [
        (cwd / path).resolve() if not path.is_absolute() else path.resolve()
        for path in args.paths
    ]
    scanner_payload = run_scanner(absolute_paths, root)
    scoped = scoped_files(args.paths, root, scanner_payload, cwd)
    artifact = unique_artifact_path(
        backup_root, branch=branch, scope_slug=args.scope_slug
    )
    records = [copy_or_exclude(file, artifact) for file in scoped]

    write_git_evidence(artifact, root, scoped, state)
    (artifact / "scanner.json").write_text(
        json.dumps(scanner_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (artifact / "manifest.txt").write_text(
        manifest_text(
            root=root,
            state=state,
            branch=branch,
            head=head,
            artifact=artifact,
            scope_slug=args.scope_slug,
            planned_verification=args.planned_verification,
            retention=args.retention,
            scanner_payload=scanner_payload,
            records=records,
            allow_exclusions=args.allow_exclusions,
        ),
        encoding="utf-8",
    )

    ok = args.allow_exclusions or all(
        record.backup_action == "copied" for record in records
    )
    return 0 if ok else 1, payload_for(
        ok=ok,
        root=root,
        state=state,
        branch=branch,
        head=head,
        artifact=artifact,
        scanner_payload=scanner_payload,
        records=records,
        allow_exclusions=args.allow_exclusions,
    )


def main(argv: list[str] | None = None) -> int:
    args_list = sys.argv[1:] if argv is None else argv
    args = parse_args(args_list)
    try:
        code, payload = create_backup(args, Path.cwd())
    except Exception as exc:
        sys.stderr.write(
            f"create simplify backup failed: {exc}. Got: {args_list!r:.100}\n"
        )
        return 2
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
