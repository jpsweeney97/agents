# Per-Engine Behavior Map

Lookup map for placing a named engine: its class, anchor spellings, character-class defaults, and mitigation support. These are static hints, not proof — confirm support and semantics on the exact engine and version pinned in the target codebase before recommending a construct.

## Engine class — backtracking vs linear

- Backtracking engines, where catastrophic backtracking is the dominant hazard: PCRE/PCRE2, Perl, Python `re`, Java, JavaScript V8, .NET default, Ruby.
- Linear/automaton engines, where catastrophic backtracking is impossible by construction: RE2, Go `regexp`, Rust `regex`, the `re2` bindings. These instead reject backreferences and lookaround at compile time, so a "switch to RE2" fix can fail to compile the pattern.

## Absolute-anchor spellings

- Prefer `\A...\z` where supported; Python spells absolute-end `\Z`.
- JavaScript is the exception — it has no `\A`/`\z` (they match the literal letters), but its no-flag `$` is already absolute-end, so anchor JS with plain `^...$`.
- Python `re.match` anchors only the start; only `fullmatch` or explicit anchors bind both ends.

## Character-class defaults

- `\d` matches non-ASCII digits by default in Python 3, .NET, and Perl, while PCRE and Java default to ASCII unless a Unicode-property flag is set.

## Mitigation support

- Atomic groups `(?>...)` / possessive quantifiers `a++`: supported on PCRE, Perl, Java, Ruby, and .NET (atomic groups), and on Python `re` 3.11+ or the `regex` module — *not* on stock JavaScript or Python `re` before 3.11.
- Native per-match timeouts: .NET, Ruby 3.2+, the Python `regex` module, or PCRE2 step-limits; everywhere else needs an external watchdog.
