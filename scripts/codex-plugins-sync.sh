#!/usr/bin/env bash
# Guards the Codex plugin delivery invariant for the unified plugin source.
#
# Canonical plugin sources live at plugins/<name>/ in this repo (Claude
# format: .claude-plugin/plugin.json). Codex discovers the personal
# marketplace implicitly at ~/.agents/plugins/marketplace.json and serves
# installed plugins from the versioned cache at
# ~/.codex/plugins/cache/turbo-mode/<name>/<version>/ — not from the
# source tree. Source edits are invisible to Codex until republished;
# --check reports that drift, --publish repairs it.
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
#   codex-plugins-sync.sh [--check]        report drift; exit 1 if any (default)
#   codex-plugins-sync.sh --publish NAME   codex plugin add NAME@turbo-mode, then re-check
#
# Bootstrap / recovery (fresh machine or restored repo):
#   1. Clone the repo to ~/.agents; Codex finds the marketplace by itself.
#   2. codex plugin add handoff@turbo-mode
#      codex plugin add review-family@turbo-mode
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
