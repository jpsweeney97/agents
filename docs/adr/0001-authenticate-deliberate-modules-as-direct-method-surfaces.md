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
- Each new module must be classified through the existing method-pin restart-frontier mechanism. The default remains Generate unless a narrower stage is justified and represented in the canonical frontier map.
- Test-only harnesses and fixtures remain outside `method-surfaces`; they prove behavior but do not become authenticated production inputs.

## Revisit When

Reconsider aggregate identity only if the direct inventory becomes operationally unmanageable, a transitive import can no longer be enumerated before execution, or a real legacy capsule population creates a migration requirement.
