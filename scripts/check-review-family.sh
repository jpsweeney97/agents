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

# Verdict scope-and-expiry gloss — shared by the two skills whose ordinary enum
# carries `Defensible`. Each names its own clearance tokens as a rider around it;
# the enums themselves stay per-skill by design and are not asserted.
# implementation-review's `Ship` is exempt: its target is snapshot-identified by
# construction (gap review 2026-08-26, refutation 11).
EXPIRY_CANON='a clearance verdict claims serious search was exhausted without a disqualifying find — it does not certify soundness, and it expires when the artifact changes'
EXPIRY_TARGETS=(
  "$SKILLS_DIR/scrutinize/SKILL.md"
  "$SKILLS_DIR/scrutinize-skill/SKILL.md"
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
check "$EXPIRY_CANON" "verdict scope-and-expiry core" "${EXPIRY_TARGETS[@]}"

# Within-skill heading agreement — every `### ` heading review-format.md's
# templates emit must be a section SKILL.md declares (backticked). This is the
# drift class the 0.11.1 heading repair fixed by hand.
SCRUTINIZE_SKILL_MD="$ROOT/$SKILLS_DIR/scrutinize/SKILL.md"
SCRUTINIZE_FMT="$ROOT/$SKILLS_DIR/scrutinize/references/review-format.md"
heading_count=0
while IFS= read -r h; do
  heading_count=$((heading_count + 1))
  if ! grep -Fq "\`$h\`" "$SCRUTINIZE_SKILL_MD"; then
    echo "HEADING DRIFT: review-format.md emits '### $h' but scrutinize SKILL.md never declares \`$h\`" >&2
    fail=1
  fi
done < <(sed -n 's/^### //p' "$SCRUTINIZE_FMT")
if [ "$heading_count" -eq 0 ]; then
  echo "HEADING CHECK BROKEN: no '### ' headings extracted from review-format.md" >&2
  fail=1
fi

# Index/reference lens parity — every lens `references/review-lenses.md`
# defines must appear in implementation-review SKILL.md's step-3 index, and
# vice versa. This is the drift class 0.17.0 produced (two lenses added to the
# reference, index untouched) and 0.18.0 repaired by hand.
IR_SKILL_MD="$ROOT/$SKILLS_DIR/implementation-review/SKILL.md"
IR_LENSES="$ROOT/$SKILLS_DIR/implementation-review/references/review-lenses.md"
index_lenses="$(awk '/^### 3\. Attack Changed Areas/{f=1;next} /^### 4\./{f=0} f' "$IR_SKILL_MD" | sed -n 's/^- `\([^`]*\)`: .*/\1/p' | sort)"
ref_lenses="$(sed -n 's/^- \([A-Za-z][^,:]*\)[,:].*/\1/p' "$IR_LENSES" | sort)"
index_count=$(printf '%s\n' "$index_lenses" | grep -c . || true)
ref_count=$(printf '%s\n' "$ref_lenses" | grep -c . || true)
if [ "$index_count" -eq 0 ] || [ "$ref_count" -eq 0 ]; then
  echo "LENS CHECK BROKEN: extracted $index_count index lenses and $ref_count reference lenses" >&2
  fail=1
else
  while IFS= read -r l; do
    echo "LENS DRIFT: review-lenses.md defines '$l' but implementation-review SKILL.md's step-3 index lacks it" >&2; fail=1
  done < <(comm -13 <(printf '%s\n' "$index_lenses") <(printf '%s\n' "$ref_lenses"))
  while IFS= read -r l; do
    echo "LENS DRIFT: implementation-review SKILL.md indexes '$l' but review-lenses.md defines no such lens" >&2; fail=1
  done < <(comm -23 <(printf '%s\n' "$index_lenses") <(printf '%s\n' "$ref_lenses"))
fi

if [ "$fail" -ne 0 ]; then
  {
    echo ""
    echo "Canonical cores (single textual source, in this script):"
    echo "  read-only: $READONLY_CANON"
    echo "  bounded:   $BOUNDED_CANON"
    echo "  expiry:    $EXPIRY_CANON"
    echo "Fix the drifted copy to match exactly, or change CANON here AND every target."
  } >&2
  exit 1
fi
echo "OK: read-only core consistent across ${#READONLY_TARGETS[@]} review skills; bounded-review core across ${#BOUNDED_TARGETS[@]}; expiry core across ${#EXPIRY_TARGETS[@]}; $heading_count template headings declared; $ref_count lenses in index/reference parity"
