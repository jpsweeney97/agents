# Behavior Contracts Charter

What earns a place in this environment, and on what terms. Consult this before
authoring a new skill, installing anything that ships skills, prompts, or
commands, or deciding the fate of third-party contract material.

## Scope

A behavior contract is text an agent must follow: skills, prompts, commands,
rules, and agent instructions. The environment is every contract surface the
two runtimes load: this repo's skills and plugins, plus anything installed at
the user level in either runtime.

Capability tooling — MCP servers, hook executables, scripts that do work rather
than instruct — is out of scope. Tools are tools. Contracts that ship alongside
a tool (a plugin's skills or commands) are in scope like any other contract.

## Thesis

Every behavior contract that runs in this environment is authored here, or
deliberately adopted and re-authored here. Third-party contract material is
source material, not infrastructure: mine it on merit, tailor what survives,
discard the rest. Nothing third-party runs as-is.

## One Owner Per Job

No two contracts in this environment may claim the same work. Collisions are
resolved by curation — one contract survives; the other is changed, absorbed,
or removed — never by precedence rules or runtime routing adjudication. An
installed third-party contract that overlaps a local one is a defect to
resolve, not a coexistence to manage.

## Admission

Merit decides, authorship-blind: a better contract is a better contract,
wherever it was found. Before admitting a new contract — authored or extracted
— answer:

- What work does it own that no existing lane owns? Name the closest existing
  contract and why this work is not its job.
- What misroute or failure does it prevent that lighter context — an AGENTS.md
  line, a reference file in an existing skill — would not?
- Can it be authored to house standards — Use-when/Do-not-use boundaries,
  proof-class discipline, availability-conditioned routing, dual-runtime
  phrasing where it applies? The test applies to the contract as it will land
  here, not the source's current form.

Run the test on observed work, not the routing graph. A genuine gap and a
non-job both show zero inbound routes, so "nothing routes to that lane" never
decides a rejection. Rejecting a candidate takes the same evidence discipline
as admitting one: name the demonstrated friction you looked for and did not
find — misroutes, repeated corrections, work handled badly ad hoc. Rejections
are cheap and admissions are paid for; do not let that asymmetry stand in for
the merit call.

Slots are paid for. Codex truncates the skill list silently over its budget,
and every contract adds routing surface in both runtimes. A contract that
cannot name the work it owns does not get a slot.

## Extraction

When third-party contract material looks valuable:

1. Read it as source material. Separate the discipline, structure, or move
   worth keeping from its packaging.
2. Author a local contract to house standards that owns that work, or fold the
   idea into the existing contract that already owns it.
3. Remove the original from the environment. Do not leave it installed for
   reference — that recreates the collision this charter exists to prevent.

Installed third-party contracts are subject to this rule retroactively:
curation passes mine them and remove them on the same terms.

## Retirement

A contract that loses its job — absorbed, superseded, or no longer worth its
slot — moves to `skills-archive/`. Update or remove every contract that routes
to it.
