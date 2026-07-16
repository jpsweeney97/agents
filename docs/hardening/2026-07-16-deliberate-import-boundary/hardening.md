# Security Hardening Review: deliberate import-execution boundary

## Evidence Basis

This review uses an ordinary evidence collection rather than a Codex Security scan. The collection is anchored to branch `fix/deliberate-gate2-import-authority` at `288e4ca` and the composite evidence digest recorded in [context.md](context.md). The principal evidence is the user-supplied closure summary (`E001`, User-supplied closure summary), the branch handoff (`E002`, Branch handoff for zipimport closure), ADR-0001 (`E003`, ADR-0001 module authentication boundary), the current Gate-2 checker (`E004`, Gate-2 import-closure checker), the checker regression tests (`E005`, Gate-2 regression tests), the Gate-1 smoke (`E006`, Gate-1 dual-path layout smoke), and the current method-surface inventory (`E007`, Current method-surface inventory).

I inspected the live ADR, checker, tests, smoke record, and contract data on the current branch. I did not rerun the full proof ladder in this hardening pass, so the proposal treats the reported verification as evidence to preserve and design around, not as a newly reproduced result.

## Constraints

We should preserve the current direct per-file method-surface model from ADR-0001, keep the first v6 extraction small enough to review, avoid treating test harness code as authenticated production input, and maintain both delivery paths: the canonical in-place skill path and the Claude symlink path. No measured latency, memory, or operator budget was supplied, so this analysis uses a balanced profile and flags unmeasured resource effects as source-derived, analogous, or hypothetical rather than measured.

The source branch is local-only. Any implementation should refresh branch, `main`, and `origin/main` before coding, and it should preserve the tactical Gate-2 protections already landed until a selected structural option is implemented and revalidated.

## Opportunity Portfolio

| Opportunity | Evidence | Options | Recommendation | Proposal |
| --- | --- | --- | --- | --- |
| Own the import-execution boundary as one explicit control | Zipimport and disguised-zip bypass evidence (`E001`, `E002`), ADR-0001 boundary requirements (`E003`), checker and regression source (`E004`, `E005`), bytecode/cache evidence (`E006`) | Option 1: Finish the duplicated gate/runtime pair; Option 2: Single-source the boundary policy contract; Option 3: Run from a launcher-prepared clean module root | I recommend Option 2 under the current constraints: keep the first v6 cut reviewable while reducing policy drift between the authoring checker and the future runtime preflight. Option 1 is acceptable for a very small landing slice; Option 3 becomes attractive if future bypasses show Python's ambient import machinery is still too hard to bound in place. | [proposals/import-execution-boundary.md](proposals/import-execution-boundary.md) |

## Recommendation Summary

The repaired checker is valuable, and we should not dilute that with a speculative rewrite. The structural issue is narrower and more practical: the project is about to rely on the same import-execution invariant in several places that do not currently share an owner. ADR-0001 states the policy, the test-only checker enforces it before the cut, the future entrypoint must mirror it before first-party import, the orchestrator must hash method surfaces, and the cache-prefix rule has to stay aligned with both delivery paths.

That split is exactly where the recent failures came from. A zip suffix list was not enough; a disguised zip mattered because the narrowed identifier ban depends on the census being complete. A fresh `sys.pycache_prefix` was necessary but not sufficient because sourceless bytecode can be read directly beside the modules. The safe design move is to make the boundary policy a first-class contract with generated or mechanically checked consumers, rather than letting ADR prose, checker code, and future runtime code evolve by memory.

I recommend Option 2: single-source the boundary policy contract while keeping enforcement local in the authoring gate and runtime preflight. The policy source must itself stay inside the authenticated method identity, or the runtime must consume only policy values embedded in a pinned surface with a release-time mismatch check. That authentication choice is part of the security design, not a file-layout preference. If delivery urgency dominates, Option 1 can land the v6 cut with duplicated code and strong tests. If we keep finding ambient import mechanisms that escape the in-place model, Option 3 is the stronger containment design.

## Next Decisions

- Decide whether this hardening opportunity should be handled before or during the first v6 physical extraction.
- Choose between Option 1 and Option 2 for the immediate v6 cut. If Option 2 wins, choose the authenticated policy placement before implementation planning: existing pinned `contract-data.yaml`, a new pinned surface, or embedded values generated from an unpinned editing reference.
- If Option 2 is selected, the next artifact should be an implementation plan, not source edits in this proposal pass.
