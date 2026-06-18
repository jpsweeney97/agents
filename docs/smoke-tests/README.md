# Behavior Smoke-Test Records

Durable records of behavior smoke tests run in this repo — forward tests that a
changed agent-facing contract (a skill, prompt, rule, workflow, or schema) is
*actually followed*, not merely loadable. They are produced by the
`behavior-smoke-test` skill (`/behavior-smoke-test` or `$behavior-smoke-test`).

These records exist because **structural validation is not behavior proof.**
`quick_validate`, frontmatter parsing, and drift checks show the files parse and
the canonical text is byte-consistent; only a realistic invocation by a fresh,
context-isolated proxy shows a future agent following the contract produces the
intended behavior. A record captures that evidence so the proof does not have to
be re-derived from memory.

## What lives here

- One Markdown record per smoke-test session, named
  `YYYY-MM-DD_<target>.md` (date-prefixed like the repo's handoffs and plan
  artifacts; `<target>` names the changed contract under test).
- Not every smoke test earns a record. Persist one when it verifies a landed
  contract change worth a durable evidence trail, documents a fragile boundary,
  or caught a failure. Throwaway dry runs stay throwaway.

## Record shape

Each record follows the `behavior-smoke-test` output fields, per claim:
`Behavior claim`, `Scenario`, `Harness`, `Result`, `Observed behavior`, `Why`,
plus a shared `Structural checks`, `Proof boundary`, and `Durable artifact`
note. Record the commit verified and the harness source (workflow script path,
run ID) so the run is reproducible.

## Status of these records

Evidence, not authority. A record proves behavior *at the commit and harness it
names*. Later contract edits can invalidate it — re-run the smoke test rather
than trusting a stale record. The live `SKILL.md`, drift checks, and a fresh
invocation outrank anything written here.
