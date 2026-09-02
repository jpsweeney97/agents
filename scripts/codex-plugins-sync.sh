#!/usr/bin/env bash
# Reports Codex plugin source/cache equality for the unified plugin source.
#
# Canonical plugin sources live at plugins/<name>/ in this repo (Claude
# format: .claude-plugin/plugin.json). Codex discovers the personal
# marketplace implicitly at ~/.agents/plugins/marketplace.json and serves
# installed plugins from the versioned cache at
# ~/.codex/plugins/cache/turbo-mode/<name>/<version>/ — not directly from the
# source tree. For local-marketplace plugins, however, ChatGPT Desktop's
# embedded Codex app-server can synchronize a drifted source to this cache
# when it serves `plugin/list`, including pruning older version directories
# (confirmed 2026-07-17; see docs/agents/codex-plugin-list-cache-sync-2026-07-17.md).
# `--publish` is an explicit CLI refresh route, not the only cache-changing
# mechanism. `--check` reports source/cache equality only at invocation; it
# never establishes installation or activation, provenance or consent, or an
# applicable Gate B.
#
# External contracts (verified 2026-06-09 on Codex 0.137.0):
#   - ~/.agents/plugins/marketplace.json is discovered implicitly; its
#     marketplace root is $HOME, so plugin source paths must be RELATIVE
#     ("./.agents/plugins/<name>"). Absolute paths are silently skipped
#     and the plugin vanishes from `codex plugin list` while the stale
#     install cache keeps working — exactly the failure this canary exists
#     to catch.
#   - Codex reads .claude-plugin/plugin.json natively; no .codex-plugin/
#     manifest is needed. The interface block and "skills" field in it are
#     Codex-facing; Claude Code ignores unknown fields by documented design.
#   - `codex plugin add <name>@turbo-mode` re-copies the cache even when
#     the version is unchanged, so it doubles as the refresh lever.
#
# Usage:
#   codex-plugins-sync.sh [--check]        report source/cache inequality; exit 1 if any (default)
#   codex-plugins-sync.sh --publish NAME   explicitly run codex plugin add NAME@turbo-mode, then re-check
#
# Bootstrap / recovery (fresh machine or restored repo):
#   1. Clone the repo to ~/.agents; Codex finds the marketplace by itself.
#   2. codex plugin add handoff@turbo-mode
#      codex plugin add review-family@turbo-mode
#      codex plugin add git-cycle@turbo-mode
#      codex plugin add relay@turbo-mode
#      codex plugin add plan-cycle@turbo-mode
#      codex plugin add decide@turbo-mode
#   3. Enable state lives in ~/.codex/config.toml under
#      [plugins."<name>@turbo-mode"]; it survives republishing.
#   4. Claude Code delivery of the same sources is separate: see
#      scripts/claude-skills-sync.sh (skills-dir plugin symlinks).
#
# This script never deletes anything. Remove superseded cache version
# directories manually with `trash` if you want to reclaim space.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO/plugins"
MARKETPLACE="turbo-mode"
CACHE="$HOME/.codex/plugins/cache/$MARKETPLACE"

check() {
  local fail=0 dir name version cachedir
  for dir in "$SRC"/*/; do
    [ -d "$dir" ] || continue
    name="$(basename "$dir")"
    if ! version="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$dir/.claude-plugin/plugin.json" 2>/dev/null)"; then
      echo "NO-MANIFEST: $name (missing or invalid .claude-plugin/plugin.json with a version)"
      fail=1
      continue
    fi
    cachedir="$CACHE/$name/$version"
    if [ ! -d "$cachedir" ]; then
      echo "NOT-INSTALLED: $name@$version (run: $0 --publish $name)"
      fail=1
      continue
    fi
    if ! diff -r -q --exclude .DS_Store "${dir%/}" "$cachedir" >/dev/null 2>&1; then
      echo "DRIFT: $name source differs from installed cache $cachedir (run: $0 --publish $name)"
      fail=1
    fi
  done
  return "$fail"
}

publish() {
  local name="$1"
  if [ ! -d "$SRC/$name" ]; then
    echo "publish failed: no source dir for '$name'. Got: $SRC/$name" >&2
    exit 1
  fi
  codex plugin add "$name@$MARKETPLACE"
  echo "REMINDER: this publish pruned the previous version directory, but ChatGPT" >&2
  echo "Desktop's Codex keeps a version-pinned skill inventory in-process: sessions" >&2
  echo "started before it refreshes will link the pruned path and report the skill" >&2
  echo "file absent (recovery finds the installed copy). To close the window now," >&2
  echo "restart ChatGPT Desktop or open its plugin list. Observed 2026-08-23." >&2
  check
}

case "${1:---check}" in
  --check) check ;;
  --publish)
    [ $# -eq 2 ] || { echo "usage: $0 --publish <plugin-name>" >&2; exit 1; }
    publish "$2"
    ;;
  *) echo "usage: $0 [--check | --publish <plugin-name>]" >&2; exit 1 ;;
esac
