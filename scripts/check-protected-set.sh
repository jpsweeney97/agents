#!/usr/bin/env bash
# check-protected-set.sh — drift DETECTION (not single-sourcing) for the canonical
# protected-branch fallback sentence. The git-cycle git-lifecycle skills each inline
# this sentence in their always-loaded body for portable, always-loaded safety; this
# check asserts every copy is byte-identical (modulo line-wrap) so the deliberate
# duplication cannot silently drift — the failure that produced issue #9. CANON below
# is the single textual source: to change the wording, edit it here and update every
# target. Exit non-zero on any mismatch.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

CANON='Treat repo-defined protected branches first; if the repo defines none, treat `main`, `master`, `develop`, and `release/*` as protected.'

# Every always-loaded surface that must carry the sentence verbatim.
# WS3 repoints the three SKILL.md that move under plugins/git-cycle/skills/ (git-hygiene,
# merge-branch, closeout-check); acceptance-map and AGENTS.md stay put — update this list
# in that migration step (Task 3.5).
TARGETS=(
  "AGENTS.md"
  "plugins/git-cycle/skills/git-hygiene/SKILL.md"
  "plugins/git-cycle/skills/merge-branch/SKILL.md"
  "plugins/git-cycle/skills/closeout-check/SKILL.md"
  "skills/acceptance-map/SKILL.md"
)

fail=0
for t in "${TARGETS[@]}"; do
  path="$ROOT/$t"
  if [ ! -f "$path" ]; then
    echo "MISSING FILE: $t" >&2; fail=1; continue
  fi
  if ! tr '\n' ' ' < "$path" | tr -s ' \t' | grep -Fq "$CANON"; then
    echo "DRIFT: $t lacks the canonical protected-set sentence verbatim" >&2; fail=1
  fi
done

if [ "$fail" -ne 0 ]; then
  {
    echo ""
    echo "Canonical sentence (single textual source, in this script):"
    echo "  $CANON"
    echo "Fix the drifted copy to match exactly, or change CANON here AND every target."
  } >&2
  exit 1
fi
echo "OK: protected-set sentence consistent across ${#TARGETS[@]} surfaces"
