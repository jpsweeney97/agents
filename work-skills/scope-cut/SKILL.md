---
name: scope-cut
description: "Use when an already-shaped scope is too large for a binding deadline, risk ceiling, capacity limit, or complexity bound and needs a defensible minimal slice. It partitions one chosen scope into keep, defer, and cut, preserving every removed item with a re-entry condition. Not for choosing among alternatives, expanding an idea, or turning an agreed plan into tracked work."
---

# Scope Cut

Cut an already-shaped scope to a defensible minimal slice: retain what the goal cannot survive without and defer or cut the rest without losing it. Invocation: `/scope-cut` or `$scope-cut`.

Work from the active workspace's live `AGENTS.md` or `CLAUDE.md` and applicable policy before handling workspace content or creating any durable artifact. When classification, permission, or the allowed destination is unclear, take the more protective path and stop for clarification. This skill is chat-first. Do not browse, access a connector, install anything, create or update a tracker item, write a file, send, publish, or make any other external change unless the user separately requests it and the active workspace permits it. Never stage, commit, stash, or push work content.

scope-cut partitions one chosen scope against a real constraint. It does not rank rival options, critique a design, widen an idea, or make a commitment decision.

## The moves

1. **Pin the binding constraint first, explicitly, before any cutting.** Name the deadline, risk ceiling, capacity limit, complexity bound, or other real budget that forces a smaller scope. If nothing forces the scope down, stop: it may not need cutting. If the scope is not yet an enumerable set, shape it before cutting. If the goal is too unclear to say what “defensible” means, ask for that clarity first. The constraint is the yardstick for every later call.
2. **Enumerate discrete items.** List the features, requirements, components, or other separable units. If items cannot separate cleanly, name the coupling rather than pretending a clean cut exists.
3. **Classify each item against the goal and constraint.** A must is **keep**: the slice would be incoherent or worthless without it. A should has value but the goal survives without it, so keep it only if the budget admits it after the musts. Every removed item is **defer** when it has a concrete re-entry condition, or **cut** when it has no planned return. Resist making everything a must. Distinguish user-stated facts and constraints from the skill's judgment: keep a concise source pointer for claims affecting decisions, owners, numbers, or deadlines, and mark an agent-inferred rationale or re-entry condition `unverified`. If an honest pass leaves an irreducible scope that still cannot fit, do not manufacture a cut; return the constraint decision to the user.
4. **Check that the kept slice is coherent and fits.** It must stand on its own: usable, testable where applicable, and not silently dependent on a removed item. If a kept item needs a deferred item, correct the partition. Measure the coherent slice against the original constraint; if it still exceeds the budget, say that no defensible slice fits and return the decision to relax the constraint, shrink the goal, or change the timing.
5. **Return the authoritative inline defer/cut ledger.** Include every removed item in the chat response. Each entry states its disposition, why it is absent, an observable re-entry condition, and either the supporting source pointer or `unverified` when the rationale or condition is agent inference. A deferment names a concrete trigger such as a freed constraint, completed dependency, or agreed date; a cut says at least that it returns only if the constraint materially lifts. Nothing is silently dropped.

## Close

Return the kept slice and inline ledger in chat. Do not create a tracker item, invoke a connector, write a file, or issue a build/no-build verdict. End with one honest line naming the capability or guarantee the original goal will lack because of the cut. The user decides whether to accept the tradeoff.

If the user explicitly asks for a durable record, first check the active workspace's instructions and permitted destination. Only then write the agreed content there; do not use Git retention as a substitute for workspace authorization.

## When not to use scope-cut

- No binding constraint exists: the scope may not need cutting.
- The scope is an unshaped idea rather than enumerable work: shape it first.
- The need is to choose among alternatives, examine whether a draft is overbuilt, or sequence an already-agreed plan: use the method appropriate to that question.
