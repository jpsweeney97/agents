# Skill lifecycle notes

Maintainer-facing prune-and-watch context for individual skills, moved here from their `SKILL.md` bodies (2026-07-12) so the fire-time skill surface carries only what changes behavior mid-invocation. Each entry preserves the skill's former build-and-prune note essentially verbatim: how the skill earns its keep, what to watch, and what would count as prune evidence. This is advisory context for keep/prune deliberations under the build-and-prune model (`docs/agents/charter.md`, Reversibility Class; `AGENTS.md` "What The Skills Are For") — not a contract, not a status board, no scores, no statuses, no required shape; edit entries freely as judgment changes. Where a note contained a fire-time behavioral fence, that fence stayed in the skill body and is not duplicated here.

## assumption-check

Artifact-first by design — the register is the deliverable and the human's tracking surface. "What am I assuming?" fires at planning time in any repo, so this is not first-to-prune — but watch it earn its guarantees over a bare assumption list: the honest differential is the implicit-assumption hunt, the reasoned ordering, and the confirm-or-kill probe per item, not a new capability. If in practice it only restyles a risk list, drifts into a verdict, or its probes stop naming kill evidence, fold or prune it.

## authorization-design

Thin in this authoring repo — no multi-user resources live here — and that silence is not evidence against it. The value is portable to every repo that gates objects by identity (broken access control sits atop the OWASP list for a reason), judged by that leverage and its cognitive-offload: the careful, deny-side-proven design pass summoned with one token. First-to-prune on observed mis-fire. Watch two failure shapes: the **fold signal** — if the pass collapses into a generic "add role checks" template and the matrix stops changing outcomes, it has thinned into a review lens that belongs in `implementation-review` (when available); and the **encyclopedia drift** — the moment it accretes a per-framework authorization-syntax reference (every middleware, every policy DSL), it has stopped being a forcing pass. Either is prune evidence to collect, not a reason to withhold the build.

## characterization-tests

Thin in this authoring repo — little legacy product code lives here — and that silence is not evidence against it. The value is portable to every repo with working, untested code in front of a change, judged by that leverage and its cognitive-offload: the full weave-tame-capture-prove procedure summoned with one token. First-to-prune on observed mis-fire. Watch three failure shapes: **pinning internals**, where the net becomes the obstacle to the refactor it was built to enable; **golden bloat**, where snapshots grow past what anyone reviews and the net decays into a rubber stamp; and the **skipped mutation proof**, where the net is handed over green-only — indistinguishable from the assertion-free tests it would otherwise resemble. Each is drift from net to decoration: prune evidence to collect, not a reason to withhold the build.

## deliberate

Built from the sixteen-round spec at `docs/specs/2026-07-13-deliberate.md`; build-and-prune class (user-invoked, read-only), no ledger entry owed. Its cognitive-offload case is the whole pipeline summoned by one token: generation, decisive contestable pruning, comparable shaping, an honest close, and a contested exclusion ledger, with a re-run capsule so disagreeing is cheap. Lifecycle facts to hold outside the fire-time body: (1) the skill-usage ledger **undercounts constituent fires** inside stages — Generate/Shape/Recommend read `ideate`, `option-shaping`, and `making-recommendations` as files, not Skill invocations, so those constituents' ledger silence during deliberate runs is expected; (2) `disable-model-invocation: true` removes the description from model context entirely — natural-language requests never surface it, `/deliberate` (or `$deliberate`) is the whole contract, **and model-side routing surfaces (`work-router`, any skill list the model consults) cannot see it either**, so routing docs that should reach it must name `deliberate` explicitly (`work-router` carries that explicit route as of the review-15/v16 repair); (3) after the v17 trim, an exact Claude Code 2.1.209 / Fable 5 system-prompt-file delta measures the spine at 4,749 tokens, 251 tokens (5.0%) inside the documented 5,000-token reattachment window; the independent `/context all` display corroborates the result at rounded grain. Verify-first items still owed live: whether Codex spawns ad hoc stage agents context-isolated from a skill-driven session (Claude-side isolation is documented: non-fork subagents start with a fresh context window); whether Codex supplies an ambient session-scoped temporary root for the run-state store locator (Claude Code's scratchpad is ambient system-prompt context) — until confirmed, Codex runs may exit `store unavailable` honestly; and the end-to-end smoke test on both runtimes. The decisive empirical check — shallow-prune results against a full-shaping control, hunting excluded eventual winners — runs only after its protocol is pre-registered through `methodology-check` or the contract-evaluation methodology; until then its result is a plan, not evidence. Prune-watch: if runs routinely end in `stage failed`/store friction rather than closes, or users stop pasting capsules back, the machinery is overhead, not offload — that is prune evidence to collect.

## dependency-upgrade

Thin in this authoring repo — nothing to upgrade here regularly — and that silence is not evidence against it. The value is **portable** to every package-managed repo, judged by that leverage and its cognitive-offload: the careful upgrade run summoned with one token. First-to-prune on observed mis-fire. Watch two failure shapes: the **fold signal** — if the cross-range read and the supply-chain gate almost never fire and the work collapses to "campaign-or-execute-plan, then `keep-green`," it has thinned into a routing note and should fold; and the **encyclopedia drift** — the moment it stops being a tight ordered pass and accretes per-manager solver recipes, it has become the multi-manager command reference it was built not to be. Either is prune evidence to collect, not a reason to withhold the build now.

## deploy-plan

Thin and **first-to-prune** — risky ships are rare in this authoring repo; the value is **portable** to ops/product repos. Watch it fire on a real risky ship; prune without ceremony if it never earns more than "read your own gauge."

## doc-drift-audit

Locally **first-to-prune**: a skill-library's prose carries few hard code symbols, and the canaries plus `check-library-integrity.sh` already own the structural slice, so content-claim drift is thin here. The real value is **portable** — code-heavy repos with READMEs, API/reference docs, and CLI/config docs that rot against a moving codebase. Build it because it is cheap to try and clean to remove; judge it by whether it fires usefully when pointed at a code-heavy repo, and prune without ceremony if it does not.

## ideate

Divergent generation fires often and locally, so this is not first-to-prune — but watch it actually earn its four guarantees over a bare brainstorm: the named frame plus a frame-breaking option, both anti-modal options present, mechanism-level distinctness under the de-cluster, and the un-ranked leak-checked field with its untouched-fixed-points close. Fold or prune if in practice it only restyles a list a capable agent already produces. The honest differential is reliability plus modest cognitive-offload, not a new capability.

## incident-response

Live burning-prod moments are rare in this authoring repo, so this is **first-to-prune**; the value is **portable** to ops/product repos. Watch the redirect-and-record fire on a real incident; prune without ceremony if it does not earn its keep — and never let it accrete a generic incident-management framework (ICS, role charts) to justify itself.

## injection-safe-inputs

Thin in this authoring repo — little untrusted input crosses trust lines here — and that silence is not evidence against it. The value is portable to every repo where input crosses a trust line (injection has sat near the top of the OWASP list for two decades), judged by that leverage and its cognitive-offload: the careful, sink-censused design pass summoned with one token. First-to-prune on observed mis-fire. Watch two failure shapes: the **fold signal** — if the sink census stops changing outcomes and the pass collapses into a generic "escape your inputs" lens, it has thinned into a review lens that belongs in `implementation-review` (when available); and the **encyclopedia drift** — the moment it accretes a per-framework payload encyclopedia (every ORM's placeholder syntax, every template engine's escape rules), it has stopped being a forcing pass. Either is prune evidence to collect, not a reason to withhold the build.

## migration-safety

Thin in this authoring repo — there is no production database here; the value is **portable** to backend, service, and data-platform repos with a relational DB and a migrations directory, where these footguns recur and land their cost at run time. First-to-prune locally. Watch it fire on real migration work; prune without ceremony if it never earns more than "looks fine." Never let it accrete into a multi-engine DDL encyclopedia — the moment it stops being a tight, engine-confirmed forcing pass over one migration and becomes a reference of every lock rule for every database, it has become the thing it was built not to be.

## observability-instrumentation

Thin in this authoring repo; the value is **portable** to backend, service, distributed-system, and data-pipeline repos, where these footguns recur and land their cost months later. Watch it fire on real instrumentation work; prune without ceremony if it never earns more than "add some logging." Never let it accrete into a multi-backend best-practices encyclopedia — the moment it stops being a tight forcing pass over one target, it has become the reference it was built not to be.

## outcome-check

Thin and heavily proof-bounded — **first-to-prune**; the value is **portable** to product repos that ship to move metrics. Watch it fire on a real "did it work?" question; prune without ceremony if it never earns more than "re-read the acceptance map weeks later."

## premortem

Prospective hindsight (the Klein effect) fires often and locally in any repo at planning time, so this is not first-to-prune — but watch it actually earn its guarantees over a bare risk-list: if in practice it only restyles "what could go wrong," or drifts into a verdict or a coverage matrix, fold or prune it. The honest differential is reliability plus the forced past-tense frame, not a new capability.

## recheck-investment

Born from the cross-model slim-control retirement (that repo's ADR-0034): a "slim" one-off control grew through thirteen locally-valid repair rounds into a provenance-sensitive evaluation system whose verification cost disproved its own premise — every finding was real, and no lane asked whether the bargain still authorized the next repair. The value is the pause nothing else owns: review lanes validate findings, `agent-facing-design` judges structure, and this skill alone routes "does this still earn another pass?" to a human. Watch three failure shapes: **over-firing** on ordinary second passes — the immediate-resume rule is the guard, and users seeing interruptions with no drift is prune evidence; **self-refutation** — if it accretes scores, schemas, ledgers, or audit machinery, it has become its own counterexample, so strip or prune it; and the **fold signal** — if in practice it only restyles the "are we overdoing it?" a capable agent already asks, fold the routing line into `agent-facing-design` and prune the rest.

## red-team

Attacker-intent-from-the-defender's-chair fires often in any repo where something is worth attacking (a notch less universal than `premortem` — not every plan has an enemy, but every plan can fail by accident). Watch the no-certificate tightrope in practice: if the ease×payoff order ever drifts into reading as a complete coverage matrix, or the skill slides into a secret/repo scan, fold or sharpen it. The honest differential is the forced adversary posture plus reliability, not a new capability.

## regex-craft

Thin in this authoring repo — little regex-hardening work happens here — and that silence is not evidence against it. The value is **portable** to every repo that runs user-facing regexes (request validation, log and data parsing, input sanitizers), judged by that leverage and its cognitive-offload: the careful, *executed* hardening pass summoned with one token. First-to-prune on observed mis-fire. Watch two failure shapes: the **fold signal** — if engine-identification and the executed proof almost never change the outcome and the work collapses to "spot `(a+)+`, add anchors," it has thinned into a lens that belongs in `implementation-review`; and the **encyclopedia drift** — the moment it stops being a tight engine-confirmed forcing pass and accretes a per-engine regex-syntax reference, it has become the thing it was built not to be. Either is prune evidence to collect, not a reason to withhold the build now.

## runbook-authoring

Operational procedures are rare in this repo, so this is **first-to-prune**: watch it fire on a real "turn this into a runbook" request and prune without ceremony if it does not earn its keep. The value is **portable** — operations-heavy repos where deploys, rotations, and failovers need a durable, honestly-validated procedure.

## scope-cut

Descoping under a deadline fires often and locally at planning time, so this is not first-to-prune — but watch it actually earn its guarantees over a bare "MVP this": the cut core is a must/should/cut/defer call a capable agent already improvises, so the honest differential is reliability plus the constraint-first forcing move and the deferred-not-dropped ledger, not a new capability. If in practice it only restyles a must/should/could list, or drifts into ranking, design critique, or a build verdict, fold or prune it.

## spec-drift-reconcile

Locally **first-to-prune**: this repo's spec→code chains are thin. The value is **portable** — product repos where a PRD/plan/issue/code chain rots when intent moves mid-stream. Watch it fire on a real intent change; prune without ceremony if it does not earn its keep.

## steelman

Chat-first; no artifact by default. Advocacy against a too-fast dismissal fires often and locally, so this is not first-to-prune — but watch it actually earn its honesty guarantees over a bare "make the case for X," and fold or prune if in practice it only restyles a case a capable agent already produces. The honest differential is reliability plus modest cognitive-offload, not a new capability.

## test-trust-audit

Thin in this authoring repo — its suites are small — and that silence is not evidence against it. The value is portable to every repo with a test suite, judged by that leverage and its cognitive-offload: the complete hollow-green checklist plus the evidence-per-finding discipline, summoned with one token. First-to-prune on observed mis-fire. Watch two failure shapes: drifting into a **scored health grade** — a number is `tech-debt-scan`'s register, and exactly the certificate this skill exists to refuse; and the **probe outgrowing its containment** — its scale fence lives in the skill body's probe section. Either is prune evidence to collect, not a reason to withhold the build.
