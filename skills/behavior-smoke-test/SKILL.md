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

Invoking this skill authorizes use of a non-mutating, context-isolated subagent
proxy for the behavior smoke test when the harness is available and safe.

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

The user's invocation of this skill is authorization to use that proxy for the
smoke test. Keep the proxy non-mutating unless the disposable harness or a
separate explicit user instruction authorizes mutation.

Give the proxy the relevant skill contract, local authority, and miniature
scenario. The controlling contract may contain the rule being tested; that is
allowed context. Do not tell the proxy the external grading claim, expected
answer, old-vs-new behavior label, or "the behavior should be X" conclusion. Ask
it to act, not explain.

Default proxy prompt:

```text
Under the provided local instructions, skill contract, and scenario, act as you
normally would. Do not explain the contract or grade the scenario. Return only:
- the next user-facing response you would send
- any tool/action you would take next, if applicable

Local instructions and skill contract: <excerpt>
User request and scenario: <scenario>
```

Use the default proxy prompt only for first-move claims. It can prove the next
response or next action, but not a multi-step workflow, validation path, stop
condition, durable-artifact decision, or report shape. For those claims, build a
multi-step non-mutating harness that lets the proxy act through the relevant
decision points without editing real files.

If a proxy is unavailable, unsafe, or cannot honestly exercise the claim, report
that explicitly. Do not call the smoke test passed from structural checks alone.

## Structural Checks

Structural checks show whether the controlling files are loadable and coherent.
They do not prove that the changed behavior was followed.

For local skills, the minimum structural checks are:

- parse `SKILL.md` frontmatter
- parse `agents/openai.yaml` when present
- inspect referenced paths and confirm each exists
- run the available local skill validator when present
- run a diff whitespace check when files were edited or are under review

Report structural checks separately from behavior proof. If a structural check
was not applicable or was not run, say that directly in the `Structural checks`
field.

## Results

- `passed`: the scenario forced the changed behavior and observation matched.
- `failed`: the scenario forced the changed behavior and observation
  contradicted it, skipped it, or errored in a relevant way.
- `not run`: no behavior scenario was executed.
- `not strong enough`: something was attempted, but it did not actually force
  or observe the behavior claim.

If the proxy prompt reveals the external grading claim or expected answer, the
scenario does not force the claim, the harness is only a first-action check for
a multi-step claim, or the proxy only explains the contract, classify it as
`not strong enough`, not `passed`.

## Output

Default reports summarize the scenario and observed behavior. Do not include the
full proxy prompt by default. Include the exact prompt only when prompt leakage,
missing context, mutation limits, or ambiguous proxy instructions affect the
proof boundary.

Use this shape: `Behavior claim`, `Scenario`, `Harness`, `Result`, `Observed behavior`, `Why`, `Structural checks`, `Proof boundary`, and `Durable artifact`.
