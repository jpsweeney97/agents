---
name: behavior-smoke-test
description: "Design and run the smallest realistic scenario that exercises a changed behavior claim. Use when the user asks for a behavior smoke test, forward test, realistic dry run, future-agent proxy check, or proof that a skill, prompt, rule, workflow, or agent-facing contract will be followed. For skill behavior-contract changes, uses a context-isolated subagent proxy by default when available and safe. Do not use for structural validation alone, broad review, CI/test triage, implementation, or final closeout."
---

# Behavior Smoke Test
Test whether a changed behavior claim is actually exercised. This skill protects
claims that a future agent, prompt, rule, workflow, or agent-facing contract will
cause different behavior. Structural checks show loadability and shape; they do
not prove behavior.

## Trigger Boundaries

Use this skill for behavior smoke tests, forward tests, future-agent proxy checks,
realistic dry runs, or proof that a changed skill, prompt, rule, workflow, or
agent-facing contract will be followed.

Do not use it for structural validation alone, broad review, generic test execution,
CI triage, implementation, debugging, baseline resolution, acceptance mapping, or
final closeout. Name the owning workflow instead.

## Core Workflow

1. Identify a concrete behavior claim.
2. Inspect the controlling authority: changed contract, local instructions,
   source artifact, existing smoke artifact, or relevant files.
3. Prefer an existing smoke artifact only when it actually exercises the claim;
   otherwise design the smallest temporary scenario that does.
4. For skill behavior-contract changes, run a context-isolated subagent proxy by
   default when available and safe.
5. Compare observed behavior to the claim. The proxy or test subject does not
   grade itself.
6. Report the result, observed behavior, structural checks, proof boundary, and
   durable artifact status.

If the claim is too vague to test, narrow it first. If it cannot be narrowed,
report `not run` and name the missing claim.

## Scenarios

The scenario should be just large enough to make the agent choose between old
behavior and new behavior. It may be markdown-first when that is the honest
harness, but it must make the changed rule operational.

Generated scenarios are temporary by default. Persist a smoke-test artifact only
when it is likely to be reused, documents a fragile boundary, caught a failure,
or the user asks for a durable example.

A scenario that only rereads the contract, summarizes expected behavior, or
checks files is not behavior evidence. Classify that as `not strong enough`.

## Subagent Proxy Harness

For skill behavior-contract changes, use a context-isolated subagent proxy by
default when available and safe. Use `fork_context: false` when supported.

Give the proxy the relevant skill contract, local authority, and miniature
scenario. Do not tell it the expected behavior or behavior claim. Ask it to act,
not explain.

Default proxy prompt:

```text
Under the provided local instructions, skill contract, and scenario, act as you
normally would. Do not explain the contract or grade the scenario. Return only:
- the next user-facing response you would send
- any tool/action you would take next, if applicable

Local instructions and skill contract: <excerpt>
User request and scenario: <scenario>
```

Keep proxy tests non-mutating by default: the proxy may state the next action it
would take, but must not edit real files unless the harness is disposable or the
user explicitly authorizes mutation.

If a proxy is unavailable, unsafe, or cannot honestly exercise the claim, report
that explicitly. Do not call the smoke test passed from structural checks alone.

## Results

- `passed`: the scenario forced the changed behavior and observation matched.
- `failed`: the scenario forced the changed behavior and observation
  contradicted it, skipped it, or errored in a relevant way.
- `not run`: no behavior scenario was executed.
- `not strong enough`: something was attempted, but it did not actually force
  or observe the behavior claim.

If the proxy prompt reveals the expected behavior, the scenario does not force
the claim, or the proxy only explains the contract, the result is `not strong
enough`, not `passed`.

## Output

Default reports summarize the scenario and observed behavior. Do not include the
full proxy prompt by default. Include the exact prompt only when prompt leakage,
missing context, mutation limits, or ambiguous proxy instructions affect the
proof boundary.

Use this shape: `Behavior claim`, `Scenario`, `Harness`, `Result`, `Observed behavior`, `Why`, `Structural checks`, `Proof boundary`, and `Durable artifact`.
