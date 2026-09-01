#!/usr/bin/env bash
# check-library-integrity.sh — read-only STRUCTURAL integrity sweep for this
# dual-runtime skill repo. It owns the structural-wiring slice that the five
# delivery/cache/text-drift canaries do NOT touch, and DELEGATES that covered
# slice by invoking them (it never re-implements their logic). On-demand only.
#
# OWNED structural checks (the genuinely-uncovered slice):
#   1. name == directory     — frontmatter `name:` matches the skill's dir name
#   2. cited paths resolve   — every references/ scripts/ examples/ path a
#                              SKILL.md cites exists, resolved relative to that
#                              SKILL.md's own dir and honoring ../ prefixes
#                              (plugin-shared references/ live two levels up),
#                              falling back to the repo root so a cited root
#                              path (e.g. scripts/check-library-integrity.sh)
#                              is not a false dangle; glob patterns cited as
#                              prose (e.g. scripts/check-*.sh) are not path
#                              citations and are skipped
#   3. orphan support files  — every git-tracked file under a skill's
#                              references/ scripts/ examples/ is mentioned
#                              somewhere else in that skill's bundle
#   4. frontmatter sweep     — every delivered SKILL.md passes quick_validate.py,
#                              filtering the AGENTS.md-accepted argument-hint /
#                              disable-model-invocation "unexpected key" complaint
#   5. version lockstep      — each plugin's .claude-plugin/plugin.json version
#                              equals the newest CHANGELOG.md section, because a
#                              landed bump is the publish signal on both runtimes,
#                              so a disagreeing pair publishes a release whose own
#                              record contradicts it
#
# DELEGATED (covered elsewhere — invoked, never duplicated):
#   check-protected-set.sh, check-handoff-paths.sh, check-review-family.sh
#   (shared-text drift); claude-skills-sync.sh --check (Claude symlink delivery,
#   incl. the dangling-link case that caught the jp-writing-style retirement);
#   codex-plugins-sync.sh --check (Codex cache delivery).
#
# DELIBERATE NON-GOALS (per the 2026-06-22 scope — do not "restore" these):
#   - Read-only. Reports a defect list and exits non-zero; never edits/fixes.
#   - git-tracked floor: every file walk uses `git ls-files`, so untracked
#     working-tree artifacts (.DS_Store, __pycache__, and empty dirs git cannot
#     represent) are out of scope by construction — they belong to git-hygiene.
#     This is why there is no empty-support-dir check: under the git floor an
#     empty dir is indistinguishable from a non-existent one.
#   - NOT a SessionStart canary. Wiring it ambient would make it an always-loaded
#     hook = a GATED contract (docs/agents/charter.md, "Reversibility Class");
#     promote it only if a real orphan/parse-drift miss the five canaries cannot
#     catch is ever observed.
#   - "Cross-skill name references" and "handoffs naming archived skills" are
#     intentionally NOT checked: both are ~100% false-positive on this corpus
#     (no hard skills/<name>/ paths exist; archived names appear only as correct
#     dated history). See the scope for the evidence.
#
# Usage: check-library-integrity.sh [--check]      (default: --check)
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QV="${QUICK_VALIDATE:-/Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py}"

# Keys quick_validate.py rejects but AGENTS.md (Validation Ladder step 6) accepts
# as documented-valid Claude Code fields — never a real failure.
ACCEPTED_KEYS="argument-hint disable-model-invocation"

case "${1:---check}" in
  --check) ;;
  -h|--help) echo "usage: $0 [--check]   read-only structural integrity sweep"; exit 0 ;;
  *) echo "usage: $0 [--check]" >&2; exit 2 ;;
esac

fail=0
pass() { printf '  [PASS] %s\n' "$1"; }
skip() { printf '  [SKIP] %s\n' "$1"; }
bad()  { printf '  [FAIL] %s\n' "$1"; fail=1; }

# Every delivered skill dir (anything with a SKILL.md): skills/, skills-claude/,
# and each plugin's skills/. Plugin dirs are linked as a unit by
# claude-skills-sync; their individual skills live one level deeper.
skill_dirs() {
  local d
  for d in "$REPO"/skills/*/ "$REPO"/skills-claude/*/ "$REPO"/plugins/*/skills/*/; do
    [ -f "${d}SKILL.md" ] && printf '%s\n' "${d%/}"
  done
}

# Frontmatter `name:` value (the first one inside the opening --- fence).
frontmatter_name() {
  awk '
    /^---[[:space:]]*$/ { fence++; next }
    fence==1 && /^name:/ {
      v=$0; sub(/^name:[[:space:]]*/,"",v); gsub(/["\047]/,"",v); sub(/[[:space:]].*$/,"",v)
      print v; exit
    }
  ' "$1"
}

echo "== Delegated checks (covered by the five canaries) =="
DELEGATED=(
  "check-protected-set.sh"
  "check-handoff-paths.sh"
  "check-review-family.sh"
  "claude-skills-sync.sh --check"
  "codex-plugins-sync.sh --check"
)
for entry in "${DELEGATED[@]}"; do
  # shellcheck disable=SC2086  # intentional word-split of "script --flag"
  set -- $entry
  scr="$REPO/scripts/$1"; shift
  [ -f "$scr" ] || { bad "$(basename "$scr") (missing)"; continue; }
  if out=$(bash "$scr" "$@" 2>&1); then
    pass "$(basename "$scr")${*:+ $*}"
  else
    bad "$(basename "$scr")${*:+ $*}"
    printf '%s\n' "$out" | sed 's/^/         /'
  fi
done

echo "== Structural integrity (owned here) =="

# --- 1: name == directory ---
nmismatch=0 ncount=0
while IFS= read -r d; do
  ncount=$((ncount + 1))
  nm="$(frontmatter_name "$d/SKILL.md")"
  base="$(basename "$d")"
  if [ "$nm" != "$base" ]; then
    bad "name != dir: $d/SKILL.md declares name '$nm'"
    nmismatch=$((nmismatch + 1))
  fi
done < <(skill_dirs)
[ "$nmismatch" -eq 0 ] && pass "name == directory ($ncount skills)"

# --- 2: cited paths resolve (../-aware; bundle-relative, else repo-root) ---
dangling=0 tokens=0
while IFS= read -r d; do
  while IFS= read -r tok; do
    [ -n "$tok" ] || continue
    tokens=$((tokens + 1))
    # Resolve bundle-relative first; fall back to repo-root so a SKILL.md citing
    # a root path (e.g. scripts/check-library-integrity.sh) is not a false dangle.
    if [ ! -e "$d/$tok" ] && [ ! -e "$REPO/$tok" ]; then
      bad "dangling ref: $d/SKILL.md -> $tok"
      dangling=$((dangling + 1))
    fi
  # `*` is in the char class so a glob like scripts/check-*.sh is captured whole
  # instead of truncating to scripts/check-; after stripping a trailing bold
  # marker (**), any token still holding a `*` is a glob cited as prose, not a
  # path citation — skip it.
  done < <(grep -ohE '(\.\./)*(references|scripts|examples)/[A-Za-z0-9][A-Za-z0-9._/*-]*' "$d/SKILL.md" 2>/dev/null \
             | sed -E 's/[.,:;]+$//; s/\*\*+$//' | grep -v '\*' | sort -u)
done < <(skill_dirs)
[ "$dangling" -eq 0 ] && pass "self-referenced paths resolve ($tokens tokens)"

# --- 3: orphan support files (git-tracked, mentioned-anywhere-in-bundle) ---
orphans=0 supportfiles=0
while IFS= read -r d; do
  rel="${d#"$REPO"/}"
  bundle=()
  while IFS= read -r line; do bundle+=("$line"); done < <(git -C "$REPO" ls-files "$rel")
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    supportfiles=$((supportfiles + 1))
    b="$(basename "$f")"
    referenced=0
    for g in "${bundle[@]+"${bundle[@]}"}"; do
      [ "$g" = "$f" ] && continue
      if grep -qF "$b" "$REPO/$g" 2>/dev/null; then referenced=1; break; fi
    done
    if [ "$referenced" -eq 0 ]; then
      bad "orphan support file: $f (unmentioned in its skill bundle)"
      orphans=$((orphans + 1))
    fi
  done < <(git -C "$REPO" ls-files "$rel/references" "$rel/scripts" "$rel/examples")
done < <(skill_dirs)
[ "$orphans" -eq 0 ] && pass "no orphan support files ($supportfiles checked)"

# --- 4: frontmatter sweep (wraps quick_validate.py; filters accepted complaint) ---
if command -v python3 >/dev/null 2>&1 && [ -f "$QV" ]; then
  fmbad=0 fmcount=0
  while IFS= read -r d; do
    fmcount=$((fmcount + 1))
    msg=$(python3 "$QV" "$d" 2>&1) && rc=0 || rc=$?
    [ "$rc" -eq 0 ] && continue
    case "$msg" in
      "Unexpected key(s) in SKILL.md frontmatter:"*)
        keys="${msg#*frontmatter: }"; keys="${keys%%. Allowed*}"
        accepted=1
        IFS=', ' read -ra arr <<< "$keys"
        for k in "${arr[@]+"${arr[@]}"}"; do
          [ -n "$k" ] || continue
          ok=0
          for a in $ACCEPTED_KEYS; do [ "$k" = "$a" ] && ok=1; done
          [ "$ok" -eq 1 ] || accepted=0
        done
        [ "$accepted" -eq 1 ] && continue
        ;;
    esac
    bad "frontmatter: $d/SKILL.md -> $msg"
    fmbad=$((fmbad + 1))
  done < <(skill_dirs)
  [ "$fmbad" -eq 0 ] && pass "frontmatter valid ($fmcount skills; accepted-key complaint filtered)"
else
  skip "frontmatter sweep (python3 or quick_validate.py unavailable: $QV)"
fi

# --- 5: plugin manifest-to-CHANGELOG version lockstep ---
lockbad=0 plugincount=0
for pj in "$REPO"/plugins/*/.claude-plugin/plugin.json; do
  [ -f "$pj" ] || continue
  plugincount=$((plugincount + 1))
  pdir="$(dirname "$(dirname "$pj")")"
  pname="$(basename "$pdir")"
  mver="$(sed -nE 's/.*"version"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/p' "$pj" | head -1)"
  cl="$pdir/CHANGELOG.md"
  if [ ! -f "$cl" ]; then
    bad "version lockstep: plugins/$pname has no CHANGELOG.md (manifest '$mver')"
    lockbad=$((lockbad + 1)); continue
  fi
  cver="$(grep -m1 -oE '^## [0-9]+\.[0-9]+\.[0-9]+' "$cl" | awk '{print $2}')"
  if [ -z "$mver" ] || [ -z "$cver" ] || [ "$mver" != "$cver" ]; then
    bad "version lockstep: plugins/$pname manifest '$mver' != newest CHANGELOG section '$cver'"
    lockbad=$((lockbad + 1))
  fi
done
[ "$lockbad" -eq 0 ] && pass "plugin manifest/CHANGELOG version lockstep ($plugincount plugins)"

echo
if [ "$fail" -ne 0 ]; then
  echo "FAIL: library integrity found defects (see [FAIL] lines above)" >&2
  exit 1
fi
echo "OK: library integrity clean (5 structural checks + 5 delegated canaries)"
