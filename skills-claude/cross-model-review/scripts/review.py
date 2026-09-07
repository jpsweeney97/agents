#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["cross-model-contracts"]
# [tool.uv.sources]
# cross-model-contracts = { path = "/Users/jp/Projects/active/cross-model", editable = true }
# ///
"""Operate one local cross-model draft review; only `review` calls Codex."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cmr_engine as engine
from cmr_archive import Archive, ReviewError
from cross_model_runtime.codex_transport import (
    DEFAULT_TIMEOUT_SECONDS,
    CodexTransportError,
)


def main() -> int:
    """Dispatch an explicitly requested operation and print its saved result."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("init")
    create.add_argument("--repo", required=True, type=Path)
    create.add_argument("--source", required=True, type=Path)
    create.add_argument("--rounds", type=int, default=3)
    commands.add_parser("begin")
    commands.add_parser("status")
    commands.add_parser("resume")
    continuation = commands.add_parser("continue")
    continuation.add_argument("--authorization", required=True, type=Path)
    query = commands.add_parser("review")
    query.add_argument("--candidate", required=True, type=Path)
    query.add_argument("--request", required=True, type=Path)
    query.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    finish = commands.add_parser("finish")
    finish.add_argument(
        "--outcome",
        required=True,
        choices=("complete", "decision", "exhausted", "failed"),
    )
    finish.add_argument("--note", required=True, type=Path)
    extend = commands.add_parser("extend")
    extend.add_argument("--extra", required=True, type=int)
    extend.add_argument("--authorization", required=True, type=Path)
    args = parser.parse_args()
    archive = Archive(args.review)
    try:
        if args.command == "init":
            result = Archive.create(
                args.review, args.repo, args.source, args.rounds
            ).load()
        elif args.command == "begin":
            result = engine.begin(archive)
        elif args.command == "status":
            result = archive.load()
        elif args.command == "resume":
            result = engine.resume(archive)
        elif args.command == "continue":
            result = engine.continue_after_failure(archive, args.authorization)
        elif args.command == "review":
            result = engine.query(
                archive, args.candidate, args.request, timeout=args.timeout
            )
        elif args.command == "finish":
            result = engine.finish(archive, args.outcome, args.note)
        else:
            result = engine.extend(archive, args.extra, args.authorization)
    except (ReviewError, CodexTransportError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        print(
            f"{args.command} failed: invalid input or saved record: {exc}. "
            f"Got: {str(args.review)!r:.100}",
            file=sys.stderr,
        )
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
