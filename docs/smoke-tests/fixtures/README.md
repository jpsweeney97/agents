# Smoke-test fixtures

Durable, hash-pinned inputs for the `deliberate` cross-runtime smoke re-runs (the debt-scan bar: an exact Codex and Claude smoke after any physical topology change).

## `2026-07-14-deliberate-exact-prompt.txt`

The exact `$deliberate` / `/deliberate` invocation prompt used by the first accepted end-to-end runs on both runtimes (Codex 2026-07-14, Claude 2026-07-15).

- **Bytes:** 3760
- **SHA-256:** `253f1bfe697124f685124f03adb539f5f55005284cb4f107de598b2272493a82`
- **Provenance:** recovered byte-identical from Codex rollout `rollout-2026-07-14T23-31-02-019f63d3-f19e-7c11-b182-a1f756ed2ee7.jsonl` (`payload.content[0].text`), the same input the accepted Codex run and the 2026-07-15 Claude re-smokes used. Cross-referenced in `../2026-07-15_deliberate-prune-wording-fidelity.md` and `../2026-07-15_deliberate-recommend-enum-fix-and-success-capsule.md`, which record the same SHA-256.

The file is stored byte-exact (no added trailing newline, no header) so it re-hashes to the pinned value. Verify before use:

```bash
shasum -a 256 docs/smoke-tests/fixtures/2026-07-14-deliberate-exact-prompt.txt
# expect: 253f1bfe697124f685124f03adb539f5f55005284cb4f107de598b2272493a82
```

Feed the file verbatim as the invocation prompt; do not edit it. If a future smoke deliberately changes the prompt, add a new pinned fixture rather than mutating this one.
