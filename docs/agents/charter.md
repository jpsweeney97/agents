# Behavior Contracts Charter

What earns a place in this environment, and on what terms. Consult this before
authoring a new contract — skill, command, or rule — installing anything that
ships contract text, retiring a contract, or deciding the fate of third-party
contract material.

## Scope

A behavior contract is text an agent must follow: skills, prompts, commands,
rules, and agent instructions. The environment is every contract surface this
charter can curate: this repo's skills, plugins, and instruction docs
(`AGENTS.md`, `docs/agents/`), plus anything installed or hand-authored at the
user level in either runtime, including instruction text delivered by hooks.

Runtime-bundled contracts — the skills and commands each runtime ships with —
load alongside the environment but cannot be curated. Treat them as fixed
terrain: they count as owners under One Owner Per Job and as the closest
existing contract in Admission, the authorship thesis does not apply to them,
and a collision with one is always resolved on the local side.

Capability tooling — MCP servers, hook executables, scripts that do work rather
than instruct — is out of scope. Tools are tools. Contracts that ship alongside
a tool (a plugin's skills or commands) are in scope like any other contract.

## Thesis

Every behavior contract that runs in this environment is first-party —
authored and stewarded by the user, whether in this repo, in another
first-party source, or hand-authored at the user level — or deliberately
adopted and re-authored here. Third-party contract material is source
material, not infrastructure: mine it on merit, tailor what survives, discard
the rest. Nothing third-party runs as-is.

## One Owner Per Job

No two contracts loaded by the same runtime may claim the same work; contracts
that never co-load do not collide, so a Claude-only lane may share a job with
a Codex-bundled skill. Collisions are resolved by curation — one contract
keeps the job; the other is narrowed, absorbed, or removed — never by
precedence rules or runtime routing adjudication. An installed third-party
contract that overlaps a local one is a defect to resolve, not a coexistence
to manage.

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
as admitting one: name the friction you looked for — misroutes, repeated
corrections, work handled badly ad hoc — and where in observed work you looked
without finding it. Rejections are cheap and admissions are paid for; do not
let that asymmetry stand in for the merit call.

A rejection may instead be a park: no slot now, with a named reopen trigger —
an observed failure or demonstrated friction that would reopen the call.
Parked candidates are settled until their trigger fires; do not silently
re-litigate them.

Slots are paid for. Codex truncates the skill list silently over its budget,
and every contract adds routing surface in each runtime that loads it — a
Claude-only lane in `skills-claude/` pays no Codex budget. A contract that
cannot name the work it owns does not get a slot.

## Extraction

When mining third-party contract material:

1. Read it as source material. Separate the discipline, structure, or move
   worth keeping from its packaging.
2. For whatever passes Admission, author a local contract to house standards
   that owns that work, or fold the idea into the existing contract that
   already owns it.
3. Remove the original from the environment whether or not anything survived —
   a zero-fold pass still ends in removal. Update or remove every contract
   that routes to the removed surface. Leaving it installed for reference
   recreates the collision this charter exists to prevent.

Installed third-party contracts are subject to this rule retroactively:
curation passes mine them and remove them on the same terms.

## Retirement

A repo contract that loses its job — absorbed, superseded, or no longer worth
its slot — moves to `skills-archive/`; an installed contract that loses its
job is removed under Extraction's terms. "No longer worth its slot" takes the
same evidence discipline as rejecting a candidate: name the observed-work
evidence, never route-absence alone. Update or remove every contract that
routes to it.

## Decision Record

Every admission, fold, rejection, park, and retirement gets a one-line entry
in `contract-decisions.md` (this directory): date, surface, outcome, evidence
pointer, and — for parks — the reopen trigger. That ledger is the
runtime-neutral record; session memory and handoffs may point at it, never
replace it.
