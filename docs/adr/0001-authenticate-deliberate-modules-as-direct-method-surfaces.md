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
- Source hashing authenticates executed code only when stale bytecode can neither be created nor read anywhere Python looks: a cache entry whose header matches the source's size and mtime executes in place of the hashed source, silently — proven for repo-local `__pycache__` in the [2026-07-15 gate-1 spike](../smoke-tests/2026-07-15_deliberate-gate1-dual-path-layout-spike.md) (Pass 1b), and proven again inside a reused `sys.pycache_prefix` by the 2026-07-15 follow-up probe (a same-size source edit with restored mtime executed the previous invocation's cached code). Redirecting the cache does not neutralize the hazard; freshness does. The v6 entrypoint must set `sys.pycache_prefix` to a freshly created, initially empty, invocation-private directory outside the repository before importing any first-party module; a prefix is never reused across invocations, and the entrypoint owns its retirement (create it under the process temp root, remove it at exit — an abandoned prefix is harmless only because nothing ever reuses one). The v6 cut's verification must show all four: seeded stale repo-local bytecode is ignored, the chosen prefix starts empty, a second invocation cannot execute the first invocation's cached code, and no repo-local bytecode is created or read.
- Each new module must be classified through the existing method-pin restart-frontier mechanism. The default remains Generate unless a narrower stage is justified and represented in the canonical frontier map.
- Test-only harnesses and fixtures remain outside `method-surfaces`; they prove behavior but do not become authenticated production inputs.

## Rollout Boundary

CH-2 may proceed before the topology gates only while every extraction remains inside `scripts/deliberate-validate.py` and `method-surfaces` stays unchanged.

Before the first physical module extraction, both of these gates must pass:

- An exact-layout dual-path spike must exercise the intended module location and import syntax through the existing PEP 723 entrypoint from the canonical in-place skill path and the Claude symlink path. Both invocations must resolve the intended canonical module and return the same exit status and stdout/stderr for the selected smoke command; a generic throwaway layout is not sufficient evidence.
- An external, non-executing check must compare three independently derived sets and require exact pairwise equality: the root-inclusive transitive first-party Python import closure derived from source, the Python subset of `method-surfaces`, and every production `.py` file physically present under `scripts/`. The same check enforces the module layout rules below (entrypoint plus flat `scripts/_deliberate_<domain>.py` files only; packages, nested files, and dotted first-party imports are rejected) and rejects dynamic-import machinery (`__import__`, `importlib`) in production sources, so the static closure stays authoritative and no dynamically reachable file can sit outside the authenticated identity while the gate is green. The check must not import the entrypoint or any production module, because executing imports before the comparison would cross the authentication boundary it is meant to guard. This authoring gate detects inventory omission, dead inventory, on-disk orphans, and layout violations; platform hashing remains the runtime authentication gate for inventoried files.

The first physical extraction is `scripts/_deliberate_shared.py`: the shared error/refusal constructors, read-authorization, and safe-YAML loading foundation — the smallest coherent domain, the base of the internal dependency graph (everything calls into it; it calls into no other first-party code), so the v6 machinery rides the smallest, lowest-semantic-risk payload. Its restart frontier is the existing `default` (Generate); v6 adds no frontier-map entry and therefore no frontier-shape change to the validator. Module naming rule: production modules are `scripts/_deliberate_<domain>.py`, and no module may take the top-level name of any stdlib or third-party import the bundle uses, because script-directory resolution makes a local module shadow the installed package. Production modules are flat files — no packages — and never use dynamic-import machinery (`__import__`, `importlib`). The import-closure check enforces the naming rule, the flat layout, and the dynamic-import prohibition directly, whether or not the offending file is inventoried.

Failure or absence of either gate blocks the v6 physical extraction, but does not block in-file CH-2 simplification.

## Revisit When

Reconsider aggregate identity only if the direct inventory becomes operationally unmanageable, a transitive import can no longer be enumerated before execution, or a real legacy capsule population creates a migration requirement.
