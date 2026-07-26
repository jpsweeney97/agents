#!/usr/bin/env bash
# exports-drift.sh — report which claude.ai exports have a source that moved.
#
# Each export under exports/<name>/SKILL.md carries a provenance comment as the
# first line of its body:
#
#   <!-- export: skills/<name>/ @ <sha> | <YYYY-MM-DD> | claude.ai -->
#
# Drift is `git log <sha>..HEAD -- <source>` being non-empty. This script only
# reports; it never rewrites an export or advances a sha. Whether a stale export
# needs rebuilding is a judgment call about whether the source change reached the
# exported text — that belongs to the `skill-export` skill, not here.
#
# Exit: 0 when every export parsed (whether current or stale), 2 when any export
# is malformed or names a source or sha git cannot resolve. Staleness alone is
# expected and is never an error.
#
# Usage: scripts/exports-drift.sh [name ...]     (default: every export)

set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO" || exit 1

EXPORTS="$REPO/exports"
[ -d "$EXPORTS" ] || { echo "NONE: no exports/ directory"; exit 0; }

if [ "$#" -gt 0 ]; then
  targets=()
  for n in "$@"; do targets+=("$EXPORTS/$n"); done
else
  targets=()
  for d in "$EXPORTS"/*/; do [ -d "$d" ] && targets+=("${d%/}"); done
fi

[ "${#targets[@]}" -eq 0 ] && { echo "NONE: no exports built yet"; exit 0; }

bad=0 stale=0 current=0

for dir in "${targets[@]}"; do
  name="$(basename "$dir")"
  md="$dir/SKILL.md"

  if [ ! -f "$md" ]; then
    echo "MALFORMED: $name (no SKILL.md)"; bad=$((bad + 1)); continue
  fi

  line="$(grep -m1 -o '<!-- export: .* -->' "$md" || true)"
  if [ -z "$line" ]; then
    echo "MALFORMED: $name (no provenance comment)"; bad=$((bad + 1)); continue
  fi

  src="$(sed -E 's/^<!-- export: (.*) @ .*/\1/' <<<"$line")"
  sha="$(sed -E 's/^<!-- export: .* @ ([^ ]+) \|.*/\1/' <<<"$line")"

  if [ -z "$src" ] || [ -z "$sha" ] || [ "$src" = "$line" ] || [ "$sha" = "$line" ]; then
    echo "MALFORMED: $name (unparseable provenance: $line)"; bad=$((bad + 1)); continue
  fi

  if ! git cat-file -e "${sha}^{commit}" 2>/dev/null; then
    echo "MALFORMED: $name (source commit $sha not in this repo)"; bad=$((bad + 1)); continue
  fi

  if [ ! -e "$src" ]; then
    echo "MALFORMED: $name (source path '$src' does not exist)"; bad=$((bad + 1)); continue
  fi

  commits="$(git log --oneline "${sha}..HEAD" -- "$src" 2>/dev/null)"
  if [ -z "$commits" ]; then
    echo "CURRENT: $name ($src @ $sha)"; current=$((current + 1))
  else
    n="$(wc -l <<<"$commits" | tr -d ' ')"
    echo "STALE:   $name ($src @ $sha — $n commit(s) since)"
    sed 's/^/           /' <<<"$commits"
    stale=$((stale + 1))
  fi
done

echo "---"
echo "RESULT: $current current, $stale stale, $bad malformed"
[ "$bad" -gt 0 ] && exit 2
exit 0
