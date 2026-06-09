#!/usr/bin/env bash
# Guards the managed-skill invariant for the dual-runtime skill source.
#
# Every directory in skills/ (dual-runtime) and skills-claude/ (Claude-only)
# must exist in ~/.claude/skills as a symlink to its repo source. Anything
# else under ~/.claude/skills must be listed in EXEMPT. Codex needs no
# delivery: it scans $HOME/.agents/skills in place.
#
# Usage:
#   claude-skills-sync.sh [--check]   report violations; exit 1 if any (default)
#   claude-skills-sync.sh --link NAME create the symlink for a new skill
#   claude-skills-sync.sh --link-all  create every missing symlink (bootstrap)
#
# Bootstrap / recovery (fresh machine or restored repo):
#   1. Clone the repo to ~/.agents, then run:
#        scripts/claude-skills-sync.sh --link-all
#      Creates ~/.claude/skills if needed and links every skill. Existing
#      correct links are skipped; conflicting entries are reported, never
#      deleted.
#   2. Recreate the SessionStart canary in the repo's untracked
#      .claude/settings.local.json (untracked by design: .gitignore ignores
#      .claude/):
#        {"hooks": {"SessionStart": [{"hooks": [{"type": "command",
#          "command": "/Users/jp/.agents/scripts/claude-skills-sync.sh --check || true",
#          "timeout": 15, "statusMessage": "Checking managed-skill invariant"}]}]}}
#   3. The pre-migration backup of ~/.claude/skills (including the retired
#      exiting-worktrees eval artifacts, which exist nowhere else) lives at
#      ~/.claude/skills-backup-20260609.tar.gz.
#
# This script never deletes anything. Remove stale entries manually with
# `trash`. A branch without skills-claude/ reports MISSING/DANGLING until
# you return to a branch that has it; that is expected during branch work.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$HOME/.claude/skills"
SOURCES=("$REPO/skills" "$REPO/skills-claude")
EXEMPT=()

is_exempt() {
  local name="$1" e
  for e in "${EXEMPT[@]+"${EXEMPT[@]}"}"; do
    [ "$e" = "$name" ] && return 0
  done
  return 1
}

source_dir_for() {
  local name="$1" src hit=""
  for src in "${SOURCES[@]}"; do
    if [ -d "$src/$name" ]; then
      [ -n "$hit" ] && { echo "COLLISION: $name exists in both skills/ and skills-claude/" >&2; return 2; }
      hit="$src/$name"
    fi
  done
  [ -n "$hit" ] && { echo "$hit"; return 0; }
  return 1
}

check() {
  local fail=0 src dir name target actual expected entry

  for src in "${SOURCES[@]}"; do
    [ -d "$src" ] || { echo "MISSING-SOURCE-DIR: $src"; fail=1; continue; }
    for dir in "$src"/*/; do
      name="$(basename "$dir")"
      expected="${dir%/}"
      target="$DEST/$name"
      if [ ! -L "$target" ]; then
        if [ -e "$target" ]; then
          echo "NOT-A-SYMLINK: $target (hand-managed copy; expected link to $expected)"
        else
          echo "MISSING: $name (run: $0 --link $name)"
        fi
        fail=1
      else
        actual="$(readlink "$target")"
        if [ "$actual" != "$expected" ]; then
          echo "WRONG-TARGET: $name -> $actual (expected $expected)"
          fail=1
        fi
      fi
    done
  done

  if [ -d "$REPO/skills" ] && [ -d "$REPO/skills-claude" ]; then
    while IFS= read -r name; do
      [ -n "$name" ] && { echo "COLLISION: $name exists in both skills/ and skills-claude/"; fail=1; }
    done < <(comm -12 <(ls "$REPO/skills" | sort) <(ls "$REPO/skills-claude" | sort))
  fi

  for entry in "$DEST"/*; do
    [ -e "$entry" ] || [ -L "$entry" ] || continue
    name="$(basename "$entry")"
    [ "$name" = ".DS_Store" ] && continue
    if [ -L "$entry" ] && [ ! -e "$entry" ]; then
      echo "DANGLING: $entry -> $(readlink "$entry")"
      fail=1
      continue
    fi
    if ! source_dir_for "$name" >/dev/null && ! is_exempt "$name"; then
      echo "UNMANAGED: $entry (not in skills/ or skills-claude/; add to EXEMPT or remove with trash)"
      fail=1
    fi
  done

  return "$fail"
}

link_all() {
  local fail=0 src dir name expected target actual
  mkdir -p "$DEST"
  for src in "${SOURCES[@]}"; do
    [ -d "$src" ] || { echo "MISSING-SOURCE-DIR: $src"; fail=1; continue; }
    for dir in "$src"/*/; do
      name="$(basename "$dir")"
      expected="${dir%/}"
      target="$DEST/$name"
      if [ -L "$target" ]; then
        actual="$(readlink "$target")"
        if [ "$actual" != "$expected" ]; then
          echo "WRONG-TARGET: $name -> $actual (expected $expected)"
          fail=1
        fi
      elif [ -e "$target" ]; then
        echo "NOT-A-SYMLINK: $target (hand-managed copy; expected link to $expected)"
        fail=1
      else
        ln -s "$expected" "$target"
        echo "linked: $target -> $expected"
      fi
    done
  done
  return "$fail"
}

link_skill() {
  local name="$1" src
  src="$(source_dir_for "$name")" || {
    echo "link failed: no source dir for '$name' in skills/ or skills-claude/" >&2
    exit 1
  }
  if [ -e "$DEST/$name" ] || [ -L "$DEST/$name" ]; then
    echo "link failed: $DEST/$name already exists. Got: $(ls -ld "$DEST/$name" | awk '{print $1, $NF}')" >&2
    exit 1
  fi
  ln -s "$src" "$DEST/$name"
  echo "linked: $DEST/$name -> $src"
}

case "${1:---check}" in
  --check) check ;;
  --link)
    [ $# -eq 2 ] || { echo "usage: $0 --link <skill-name>" >&2; exit 1; }
    link_skill "$2"
    ;;
  --link-all) link_all ;;
  *) echo "usage: $0 [--check | --link <skill-name> | --link-all]" >&2; exit 1 ;;
esac
