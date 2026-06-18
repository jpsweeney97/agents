#!/usr/bin/env bash
# check-handoff-paths.sh — drift DETECTION (not single-sourcing) for the handoff
# plugin's storage path-set and project-root resolution. The handoff skills are a
# globally-distributed dual-runtime plugin run in arbitrary repos, so these blocks
# cannot be homed in AGENTS.md (absent in foreign repos) or a conditionally-loaded
# reference (can be missed on a given run); they are deliberately inlined in each
# skill. This check asserts every copy is byte-identical (modulo line-wrap) so the
# duplication cannot silently drift — the divergence that produced issue #12 (the
# `*.md`-glob disagreement). The two CANON blocks below are the single textual
# source: to change a block, edit it here and update every target. Exit non-zero
# on any mismatch.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# The three-path storage set, rendered as a code block by every skill that lists
# the full read scope. save-handoff renders only the primary path (it is the
# writer, never the legacy reader) and is intentionally excluded from this check.
PATHS_CANON='<project_root>/.agents/handoffs/ <project_root>/.claude/handoffs/ (legacy, read-only) <project_root>/.codex/handoffs/ (legacy, read-only)'
PATHS_TARGETS=(
  "plugins/handoff/skills/load-handoff/SKILL.md"
  "plugins/handoff/skills/search-handoffs/SKILL.md"
  "plugins/handoff/skills/throughline/SKILL.md"
)

# The project-root resolution two-step, inlined identically by all four skills.
ROOT_CANON='1. Use `git rev-parse --show-toplevel` when the current directory is inside a git repository. 2. Otherwise use the current working directory.'
ROOT_TARGETS=(
  "plugins/handoff/skills/load-handoff/SKILL.md"
  "plugins/handoff/skills/save-handoff/SKILL.md"
  "plugins/handoff/skills/search-handoffs/SKILL.md"
  "plugins/handoff/skills/throughline/SKILL.md"
)

fail=0
check() {
  local canon="$1" label="$2"; shift 2
  local t path
  for t in "$@"; do
    path="$ROOT/$t"
    if [ ! -f "$path" ]; then
      echo "MISSING FILE: $t" >&2; fail=1; continue
    fi
    if ! tr '\n' ' ' < "$path" | tr -s ' \t' | grep -Fq "$canon"; then
      echo "DRIFT: $t lacks the canonical $label verbatim" >&2; fail=1
    fi
  done
}

check "$PATHS_CANON" "handoff storage path-set" "${PATHS_TARGETS[@]}"
check "$ROOT_CANON" "project-root resolution" "${ROOT_TARGETS[@]}"

if [ "$fail" -ne 0 ]; then
  {
    echo ""
    echo "Canonical blocks (single textual source, in this script):"
    echo "  path-set: $PATHS_CANON"
    echo "  root:     $ROOT_CANON"
    echo "Fix the drifted copy to match exactly, or change CANON here AND every target."
  } >&2
  exit 1
fi
echo "OK: handoff path-set consistent across ${#PATHS_TARGETS[@]} surfaces; project-root across ${#ROOT_TARGETS[@]}"
