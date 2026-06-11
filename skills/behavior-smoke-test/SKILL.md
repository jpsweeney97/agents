---
name: behavior-smoke-test
description: "Use when the user asks for a behavior smoke test, forward test, realistic dry run, future-agent proxy check, or proof that a changed skill, prompt, rule, workflow, or agent-facing contract is actually followed. Do not use for structural validation alone, broad review, CI/test triage, implementation, debugging, or final closeout."
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

This skill may prefer a non-mutating, context-isolated subagent proxy for agent
behavior claims, but it does not override the active subagent tool's
authorization rules.

Do not use it for structural validation alone, broad review, generic test execution,
CI triage, implementation, debugging, baseline resolution, acceptance mapping, or
final closeout. Name the owning workflow instead.

## Core Workflow

1. Identify a concrete behavior claim.
2. Inspect the controlling authority: changed contract, local instructions,
   source artifact, existing smoke artifact, or relevant files.
3. Discover the available harness and its permission constraints before choosing
   a proxy, direct test, dry run, or existing artifact.
4. Prefer an existing smoke artifact only when it actually exercises the claim;
   otherwise design the smallest temporary scenario that does.
5. For skill, prompt, rule, workflow, or agent-contract behavior claims, prefer
   an authorized context-isolated subagent proxy when current tool policy permits
   it and the harness can stay safe.
6. For non-agent behavior claims, use direct tests, fixture runs, or realistic
   dry runs when they actually exercise the changed behavior.
7. Compare observed behavior to the claim. The proxy or test subject does not
   grade itself.
8. Report the result, harness source, observed behavior, structural checks, proof
   boundary, and durable artifact status.

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

## Harness Discovery

Before declaring a proxy available or unavailable, inspect the harness options
for the current session and claim type.

- For subagent or proxy checks, inspect the active tool metadata. If `tool_search`
  is available and a subagent tool is not already exposed, use it to search for
  subagent or proxy tooling, then read the discovered tool's authorization, role,
  context, mutation, and waiting constraints.
- The active tool contract wins over this skill. This skill may prefer a proxy;
  it never authorizes a tool action that current tool policy or user permissions
  do not allow.
- Do not infer proxy availability from source files, prior sessions, memory, or
  marketplace/cache metadata alone.
- In the report's `Harness` field, name the harness source: active tool metadata,
  `tool_search` discovery, explicit user-provided harness, direct local
  test/dry run, existing smoke artifact, or unavailable/unverified.

## Subagent Proxy Harness

For skill behavior-contract changes, use a context-isolated subagent proxy by
default only when current tool policy permits it and the harness is safe. Use
`fork_context: false` when supported.

### Subagent Availability And Authorization

Explicit user invocation of this skill is not by itself authorization to spawn a
subagent. Spawn only when the current subagent tool's policy permits the action.
If authorization is unclear and a proxy is the right harness, ask one permission
question before spawning.

If the skill was selected implicitly and the user did not explicitly request a
subagent, proxy, or delegated agent, do not spawn silently. For skill, prompt,
rule, workflow, or agent-contract behavior claims, ask one permission question
when authorization is the only missing piece; otherwise report `not run`. For
non-agent behavior claims, a direct test, fixture run, existing smoke artifact,
or realistic dry run can still count when it actually exercises the changed
behavior.

When spawning, use `fork_context: false` when supported. Use a `behavior-proxy`
custom agent only when current tool metadata exposes that role. Otherwise use
the safest allowed default role. Do not make a proxy search for a custom role,
and do not use a worker or explorer agent for behavior proof unless the user
explicitly asks for that role and the role itself is part of the behavior being
tested.

If no authorized, safe subagent harness is available, or if the harness cannot
keep the proxy context isolated and non-mutating, report `not run` for agent
behavior claims. Do not emulate a clean-context proxy inside the parent thread.

Keep the proxy non-mutating unless the disposable harness or a separate explicit
user instruction authorizes mutation.

Give the proxy the relevant skill contract, local authority, and miniature
scenario. The controlling contract may contain the rule being tested; that is
allowed context. Do not tell the proxy the external grading claim, expected
answer, old-vs-new behavior label, or "the behavior should be X" conclusion. Ask
it to act, not explain. The parent run grades the observed behavior; the proxy
or test subject does not grade itself.

Default proxy prompt:

```text
Under the provided local instructions, skill contract, and scenario, act as you
normally would.

Do not edit files, stage changes, commit, push, delete, install dependencies,
publish, sync, call external services, read broad repository or session context,
or otherwise mutate files, runtime state, remote state, or user data. For
first-move checks, do not call tools; state only the next tool/action you would
request or take, if applicable.

Do not explain the contract, identify the test purpose, infer the expected
answer, or grade the scenario. Return only:
- the next user-facing response you would send
- the next tool/action you would request or take, if applicable
- the blocking reason, only if you cannot act from the supplied context

Local instructions and skill contract: <excerpt>
User request and scenario: <scenario>
```

Use the default proxy prompt only for first-move claims. It can prove the next
response or next action, but not a multi-step workflow, validation path, stop
condition, durable-artifact decision, or report shape.

For multi-step claims, build a staged non-mutating harness:

1. Define the decision points that must be observed.
2. Send the proxy one stage at a time with only the context it would naturally
   have at that point.
3. Record each proxy response and intended next action.
4. Apply the same safety envelope at every stage: no edits, staging, commits,
   pushes, deletes, dependency installs, publishing, sync, external service
   calls, broad context reads, or tool calls unless a disposable harness or
   explicit user authorization permits that specific action class.
5. Stop before any real mutation; replace tool calls or edits with stated
   intended actions unless a disposable harness explicitly allows them.
6. Grade the collected observations in the parent run against the original
   behavior claim.

If the staged harness only proves the first move, leaks the grading claim, or
depends on the proxy judging itself, classify it as `not strong enough`.

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
