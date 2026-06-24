# Behavior Contracts Charter

What earns a place in this environment, and on what terms. Skills and commands are build-and-prune and are **not** charter events — build them whenever they seem worth trying, prune them freely when they do not (see Reversibility Class). Consult this only before the events that stay gated: authoring or retiring an always-loaded contract (a rule, an AGENTS.md line, a hook, any ambient instruction), installing anything that ships contract text, or deciding the fate of third-party contract material. Every surface that routes here must name these gated events; a pointer that gates skill or command authoring over-triggers the charter.

## Scope

A behavior contract is text an agent must follow: skills, prompts, commands, rules, and agent instructions. The environment is every contract surface this charter can curate: this repo's skills, plugins, and instruction docs (`AGENTS.md`, `docs/agents/`), plus anything installed or hand-authored at the user level in either runtime, including instruction text delivered by hooks.

Runtime-bundled contracts — the skills and commands each runtime ships with — load alongside the environment but cannot be curated. Treat them as fixed terrain: they count as owners under One Owner Per Job and as the closest existing contract in Admission, the authorship thesis does not apply to them, and a collision with one is always resolved on the local side.

Capability tooling — MCP servers, hook executables, scripts that do work rather than instruct — is out of scope. Tools are tools. Contracts that ship alongside a tool (a plugin's skills or commands) are in scope like any other contract. When contract text is fused to an exempt engine rather than merely shipped beside it, the engine departs with the contract as packaging; a standalone tool that ships no contract stays. An engine is fused when delivering contract text is its only function — a hook whose sole output is injected instructions; it is a standalone tool when it does work beyond delivering any contract — an MCP server answering tool calls.

This charter and its decision ledger are the curation machinery itself; the other governance docs in `docs/agents/` support it. None is a contract admitted under the charter: they are maintained by direct editing and take no admission, retirement, or decision-ledger entry of their own.

## Reversibility Class

How much a contract is gated turns on one thing: whether a bad one is *caught cheaply and undone cleanly*.

- **Build-and-prune — skills and commands.** A skill fires *visibly*: both runtimes surface every invocation, including model-initiated ones, so a mis-fire or a stolen fire shows up in the transcript the moment it happens. And it is *modular* — a directory you trash. So build one whenever it seems worth trying, judge it by watching it fire on real work, and prune it freely when it does not earn its place. No observed-friction proof, no admission test, no park, no ledger entry, no archive step. Healthy churn is the design, not a failure — the library is meant to turn over.
- **Gated — rules, AGENTS.md lines, hooks, any always-loaded instruction.** An ambient contract has *no visible fire*: it shapes every response with no trigger in the transcript, so you cannot watch it mis-fire. And it is *entangled* — woven into surrounding guidance, so removing it has non-local effects you will not reliably notice. You can neither see it go wrong nor cleanly prune it, so it keeps the full Admission and Retirement discipline below.

Infer the class from whether the contract fires visibly and prunes cleanly; this is a lens, not a label to declare. Third-party material is gated regardless of class — its risk is authorship coherence (Thesis), not reversibility.

## Thesis

Every behavior contract that runs in this environment is first-party — authored and stewarded by the user, whether in this repo, in another first-party source, or hand-authored at the user level — or deliberately adopted and re-authored here. Third-party contract material is source material, not infrastructure: mine it on merit, tailor what survives, discard the rest. Nothing third-party runs as-is, except the runtime-bundled contracts Scope exempts as fixed terrain.

## One Owner Per Job

No two contracts loaded by the same runtime may claim the same work; contracts that never co-load do not collide, so a Claude-only lane may share a job with a Codex-bundled skill. Collisions are resolved by curation — one contract keeps the job; the other is narrowed, absorbed, or removed — never by precedence rules or runtime routing adjudication. An installed third-party contract that overlaps a local one is a defect to resolve, not a coexistence to manage. Whether two contracts claim the same work turns on the work itself — the question a contract answers and the work product it returns — not on how it is delivered. Two contracts do different jobs when those differ in kind, such as a qualitative pass/fail judgment versus a measured benchmark; they do the same job when one merely fires differently, goes deeper, or recalls more over the same work product. Differences in delivery mode (auto-fire versus invoke, recall versus precision, per-turn versus per-branch), and the coverage, timing, or unprompted action that follow from them, do not by themselves make it a different job.

For build-and-prune contracts this is a design heuristic, not an up-front gate: a collision surfaces as competing fires in the transcript and is resolved by pruning the weaker, so do not build an obvious duplicate, but do not litigate overlap before building either. For gated contracts it is a firm admission condition.

## Admission

This test governs **gated** contracts only — always-loaded instructions and third-party material. Skills and commands are build-and-prune (see Reversibility Class) and do not run it.

Merit decides, authorship-blind: a better contract is a better contract, wherever it was found. Before admitting a new contract — authored or extracted — answer:

- What work does it own that no existing lane owns? Name the closest existing contract and why this work is not its job.
- What misroute or failure does it prevent that lighter context — an AGENTS.md line, a reference file in an existing skill — would not?
- Can it be authored to house standards — Use-when/Do-not-use boundaries, proof-class discipline, availability-conditioned routing, dual-runtime phrasing where it applies? The test applies to the contract as it will land here, not the source's current form.

Run the test on observed work, not the routing graph. A genuine gap and a non-job both show zero inbound routes, so "nothing routes to that lane" never decides a rejection. Rejecting a candidate takes the same evidence discipline as admitting one: name the friction you looked for — misroutes, repeated corrections, work handled badly ad hoc — and where in observed work you looked without finding it. Rejections are cheap and admissions are paid for; do not let that asymmetry stand in for the merit call.

A rejection may instead be a park: no slot now, with a named reopen trigger — an observed failure or demonstrated friction that would reopen the call. Parked candidates are settled until their trigger fires; do not silently re-litigate them.

Every contract adds routing surface in each runtime that loads it. A contract that cannot name the work it owns does not get a slot.

## Extraction

When mining third-party contract material:

1. Read it as source material. Separate the discipline, structure, or move worth keeping from its packaging.
2. For whatever passes Admission, author a local contract to house standards that owns that work, or fold the idea into the existing contract that already owns it.
3. Remove the original from the environment whether or not anything survived — a zero-fold pass still ends in removal. When the original is a separable contract bundled in the same uninstall unit as a standalone exempt tool, removal still binds the contract but must spare the tool: quarantine the contract — fold its merit, then stop the bundled copy loading or routing — instead of uninstalling; if no quarantine is possible, resolve the One-Owner collision explicitly and record which side kept the job. Update or remove every contract that routes to the removed surface. Leaving it installed for reference recreates the collision this charter exists to prevent.

Installed third-party contracts are subject to this rule retroactively: curation passes mine them and remove them on the same terms.

## Retirement

A skill or command is build-and-prune: trash it the moment it stops earning its place — no evidence ceremony, and archiving to `skills-archive/` is optional, not required. A **gated** contract that loses its job — absorbed, superseded, or no longer worth its slot — retires under discipline: a rule or instruction line with no archive home is deleted from its surface; an installed third-party contract is removed under Extraction's terms. For these gated retirements, "no longer worth its slot" takes the same evidence discipline as admitting one: name the observed-work evidence, never route-absence alone. Update or remove every contract that routes to a removed surface, whichever class it was.

## Decision Record

Build-and-prune churn — creating or pruning skills and commands — takes no ledger entry. Every **gated** decision — an admission, fold, rejection, park, or retirement of an ambient contract or third-party material — gets one entry in `contract-decisions.md` (this directory): date, surface, outcome, evidence pointer, and — for parks — the reopen trigger. The evidence pointer must be durable and replayable — a commit, a tracked file, or a named, persistent artifact reachable outside the session — not a bare session reference; when recovery depends on an external source that can change, pin a version or snapshot. That ledger is the runtime-neutral record; session memory and handoffs may point at it, never replace it.
