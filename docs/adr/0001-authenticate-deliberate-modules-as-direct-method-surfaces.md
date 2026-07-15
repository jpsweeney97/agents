# Authenticate deliberate modules as direct method surfaces

When the `deliberate` validator is decomposed, every behavior-bearing imported production module will be listed directly in `validation.method-surfaces` alongside the stable `scripts/deliberate-validate.py` entrypoint, and every such file will be platform-hashed before any helper invocation. This extends the existing exact per-file pin, read-authorization, capsule-validation, and restart-frontier mechanism without adding an aggregate-identity layer; the evidence and compatibility boundary are recorded in the [validator debt scan](../audits/2026-07-15-deliberate-validator-debt-scan.md).

## Considered Options

- **Direct per-file inclusion — chosen.** It preserves the current file-grain identity model, keeps drift attributable to a concrete locator, and reuses exact-set validation plus the existing stage-frontier machinery.
- **Aggregate module identity — rejected.** It would add manifest construction and verification machinery, make file-level drift indirect, and create a second authentication abstraction without an observed need.
- **Import modules without pinning them — rejected.** Behavior would execute outside the authenticated method identity and weaken the bootstrap and recovery boundary even if the test suites stayed green.

## Consequences

- The first physical module extraction is contract evolution under `contract-data-version` 6, not a behavior-preserving file move. The version gate, exact `method-surfaces` inventory, and every affected rendering, fixture, test, and runtime instruction must change together.
- Pre-topology capsules carrying the current seven-surface inventory are unsupported and receive no migration path. This hard cut is accepted because no user-valued legacy capsule population exists, including pasted capsules outside the workspace.
- Membership in `method-surfaces` is necessary but not sufficient for bootstrap authentication: the orchestrator must platform-hash the entrypoint and every imported production module before starting the helper, because Python imports execute before helper-owned validation can run.
- Source hashing authenticates executed code only when repo-local bytecode can neither be created nor read: a `__pycache__` entry whose header matches the source's size and mtime executes in place of the hashed source, silently (proven in the [2026-07-15 gate-1 spike](../smoke-tests/2026-07-15_deliberate-gate1-dual-path-layout-spike.md), Pass 1b). The v6 entrypoint must therefore set a session-temporary `sys.pycache_prefix` before importing any first-party module, and the v6 cut's verification must show that no repo-local bytecode is created or read.
- Each new module must be classified through the existing method-pin restart-frontier mechanism. The default remains Generate unless a narrower stage is justified and represented in the canonical frontier map.
- Test-only harnesses and fixtures remain outside `method-surfaces`; they prove behavior but do not become authenticated production inputs.

## Rollout Boundary

CH-2 may proceed before the topology gates only while every extraction remains inside `scripts/deliberate-validate.py` and `method-surfaces` stays unchanged.

Before the first physical module extraction, both of these gates must pass:

- An exact-layout dual-path spike must exercise the intended module location and import syntax through the existing PEP 723 entrypoint from the canonical in-place skill path and the Claude symlink path. Both invocations must resolve the intended canonical module and return the same exit status and stdout/stderr for the selected smoke command; a generic throwaway layout is not sufficient evidence.
- An external, non-executing check must derive the root-inclusive transitive first-party Python import closure from source and require exact equality with the Python subset of `method-surfaces`. The check must not import the entrypoint or any production module, because executing imports before the comparison would cross the authentication boundary it is meant to guard. This authoring gate detects accidental inventory omission; platform hashing remains the runtime authentication gate for inventoried files.

Failure or absence of either gate blocks the v6 physical extraction, but does not block in-file CH-2 simplification.

## Revisit When

Reconsider aggregate identity only if the direct inventory becomes operationally unmanageable, a transitive import can no longer be enumerated before execution, or a real legacy capsule population creates a migration requirement.
