#!/usr/bin/env bash
# check-review-family.sh — drift DETECTION (not single-sourcing) for the shared
# contracts the five review-family skills each inline in their always-loaded
# SKILL.md. These skills load independently, so a binding rule cannot be homed in
# a conditionally-loaded reference (it can be absent on a given run, silently
# un-binding the skill); the rules are deliberately duplicated inline and this
# check asserts each shared CORE is byte-identical (modulo line-wrap) so the
# duplication cannot silently drift — the divergence that produced issue #11
# (five different read-only verb lists). Per-skill riders and verdict vocabulary
# stay explicit around each CORE. The CANON blocks below are the single textual
# source: to change a rule, edit it here and update every target. Exit non-zero
# on any mismatch.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

SKILLS_DIR="plugins/review-family/skills"

# Read-only / protected-action boundary — the shared core every review skill
# carries; each skill keeps its own opener and risk-specific riders around it.
READONLY_CANON='do not edit files, stage, commit, push, delete, sync, publish, or implement fixes unless the user explicitly asks for that separate action'
READONLY_TARGETS=(
  "$SKILLS_DIR/scrutinize/SKILL.md"
  "$SKILLS_DIR/scrutinize-skill/SKILL.md"
  "$SKILLS_DIR/implementation-review/SKILL.md"
  "$SKILLS_DIR/system-design-review/SKILL.md"
  "$SKILLS_DIR/review-reviewer/SKILL.md"
)

# Bounded-review contract core — shared by the three adversarial skills that run
# a true bounded-review mode. Each keeps its own verdict label as a rider
# (`Defensible`/`Ready to Execute`/`Ship`). system-design-review (reduced-depth)
# and review-reviewer (bounded adjudication scope) use deliberately different
# mechanisms and are not asserted here.
BOUNDED_CANON='state the reviewed subset before findings, review the highest-risk surface first, mark omitted areas `unverified`, give the next slice needed for a complete review, and do not issue a full-clearance verdict for the full target'
BOUNDED_TARGETS=(
  "$SKILLS_DIR/scrutinize/SKILL.md"
  "$SKILLS_DIR/scrutinize-skill/SKILL.md"
  "$SKILLS_DIR/implementation-review/SKILL.md"
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

check "$READONLY_CANON" "read-only boundary core" "${READONLY_TARGETS[@]}"
check "$BOUNDED_CANON" "bounded-review core" "${BOUNDED_TARGETS[@]}"

if [ "$fail" -ne 0 ]; then
  {
    echo ""
    echo "Canonical cores (single textual source, in this script):"
    echo "  read-only: $READONLY_CANON"
    echo "  bounded:   $BOUNDED_CANON"
    echo "Fix the drifted copy to match exactly, or change CANON here AND every target."
  } >&2
  exit 1
fi
echo "OK: read-only core consistent across ${#READONLY_TARGETS[@]} review skills; bounded-review core across ${#BOUNDED_TARGETS[@]}"
