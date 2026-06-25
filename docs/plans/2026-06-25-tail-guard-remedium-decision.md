---
title: "Tail-Guard Re-Medium-to-Code — Decision (both certified guards stay PROSE) + cross-model arc closeout"
date: 2026-06-25
type: decision
project: agents
method: "29-agent blind adjudication workflow wf_df3cd1f1-b79 (2 analyze + 6 design-arms + 18 adversarial-verify + 2 synthesize + 1 decision-critic), every load-bearing claim re-verified against sources"
status: COMPLETE
---

# Tail-Guard Re-Medium-to-Code — Decision

Evidence at a point in time, not authority. This resolves the one item the cross-model results doc (`2026-06-24-cross-model-tail-guard-results.md`, line 102) left explicitly open and "the user's to make": for the two guards that certified LOAD-BEARING, should the skill be **re-mediumed to deterministic code**, or **left as prose**? With this settled, the cross-model tail-guard arc (Eras 30–34) is closed end to end — both on keep/delete dispositions and on medium.

## Bottom line

- **Both certified tail-guards stay PROSE. Re-medium-to-code is declined for `release-cut` and `gh-address-comments`.** A 29-agent blind adjudication (three design arms per skill — full-orchestration / minimal-core / skeptic-null — each stress-tested on three lenses, then a verifying decision critic) returned the same shape as the cognitive-offload eval: **only the skeptic-null arm survives clean for either skill.** Every build arm took at least one verified FATAL.
- **The keystone is structural, not preferential.** Each guard's certified hazard is a *negative* constraint — "do not fire the outward act" — over a surface a bundled script cannot reach: the agent's own unsandboxed shell (`release-cut`: `git tag → push → npm publish`) or its own MCP/`gh` tool interface (`gh-address-comments`: push / reply / resolve / re-review). A plugin script is not a hook, a sandbox, or a permissions-deny; the agent runs it and then sits in the *identical* post-stage position, governed by the *same* internalized followership that scored 0/10. "Enforce the gate in code" therefore has **no referent** — it can only mean "the script omits the outward command and exits," which constrains the script, not the agent. Re-medium adds zero guarantee on the only axis the experiment certified; this is the security-theater tell, and it is decisive.
- **No skill behavior changed; no version bump; no charter event.** `release-cut` and `gh-address-comments` bodies stay byte-identical to the text that scored gap 1.00 (verified unchanged on disk), so leaving them alone is the strongest possible consistency with the certification and incurs no re-certification debt. git-cycle stays `1.2.2`.

## The evaluation

Method: for each certified skill, three genuinely-different design arms (each developing its best honest version and stating its own failure modes), each refuted on three lenses — **guarantee** (does code add real enforcement/correctness, or merely relocate a followed-instruction?), **summon-no-regression** (does one invocation still yield the whole guardrailed run, and does the gap-1.00 behavior survive?), **over-engineering** (machinery for its own sake / script-vs-prose drift; inverted for the null arm: is real value being abandoned?). Verifiers defaulted to the skeptical verdict. Then a decision critic re-verified every load-bearing claim against the live sources.

Verdict matrix (FATAL = a kill the arm did not survive):

| Skill | arm | guarantee | summon | over-eng | result |
|---|---|---|---|---|---|
| `release-cut` | full-orchestration | FATAL | FIXABLE | FATAL | dead |
| `release-cut` | minimal-core | FATAL | SURVIVES | FATAL | dead |
| `release-cut` | **skeptic-null** | SURVIVES | SURVIVES | SURVIVES | **KEEP PROSE** |
| `gh-address-comments` | full-orchestration | FATAL | SURVIVES | FATAL | dead |
| `gh-address-comments` | minimal-core | FIXABLE | FIXABLE | FATAL | dead |
| `gh-address-comments` | **skeptic-null** | SURVIVES | SURVIVES | SURVIVES | **KEEP PROSE** |

The build arms did not merely fail to add value — they added *new harm*, verified against the sources:

- **`release-cut` (both build arms): a manifest-corruption surface + a protected-branch hook bypass.** The only correctness any arm could add (lockstep-by-construction) requires the script to *write* the manifest — and git-cycle's one existing script (`release-cut-facts.sh`) is read-only and self-disclaims its TOML parse as "best effort; the agent confirms." A read-only reporter cannot corrupt the manifest that SKILL.md calls "the release signal the runtime cache and any distribution mirror read"; a mutating writer can, one step before the irreversible publish train. Worse: the user-level `require-gitflow.py` main-guard self-guards with `EDIT_TOOLS = {"Edit","Write","MultiEdit"}` and exits 0 for any other tool (verified, hook lines 59 / 680–681) — so moving the manifest write out of the agent's Edit/Write tools into a bash script **bypasses the harness-enforced protected-branch floor**. minimal-core's shared `release-cut-lib.sh` seam additionally reintroduces the coupling git-cycle 1.0.0 deliberately rejected ("safety conventions stay inline… drift-guarded").
- **`gh-address-comments` (both build arms): no enforceable target + house-style rupture.** full-orchestration concedes its verb-less script "does not raise the prose's 0/10 ceiling" and would be the plugin's first script to network *and* write *and* commit, plus a 5-disposition enum duplicated into a validator that drifts. minimal-core wisely leaves the gate as prose and aims code only at the thread-fetch — but rests on the untested premise that ad-hoc fetch "fails often and silently" (its own honest verdict: "leave as prose absent a differential"), targets a non-damage-class reversible input step, and breaks the plugin's bright "no writes, no network" line.

## Provenance correction (load-bearing)

The framing that motivated this thread — "the charter routes damage-class guards to deterministic machinery; a reliability defense living as a prose skill is the defect" — is **not a charter clause.** Verified: zero hits in `docs/agents/charter.md`; exactly one hit repo-wide, at `2026-06-24-cross-model-tail-guard-results.md` line 50, which self-attributes it to "the prior arc's reasoning." So **no standing rule required re-medium** — the merits decide, and they decide against. (Earlier session prose, including this run's own briefing, repeated the loose "the charter routes…" phrasing; it is corrected here.) The charter's actual relevant content cuts the other way: it classifies scripts that *do work* rather than instruct as out-of-scope tooling and states no preference for code on safety gates.

## Why `release-cut` in particular collapses to null

The offload caveat ("a re-medium must either (a) have code orchestrate the full run, or (b) keep the skill as the front end to the code") is what forces the result. Option (a) is **impossible** here: the skill's core is irreducible judgment — the change class read "from the diff, not the commit labels," and a CHANGELOG body "assembled from real landed changes, never invented." A script cannot make those calls without either stranding them (caveat fail) or encoding the commit-label shortcut the skill was *built to kill* (a behavior regression that reopens the gap). So re-medium collapses to option (b) — skill-as-front-end-to-a-write-script — whose script does only the mechanical write, i.e. exactly the corruption + hook-bypass surface above. The irony is precise: **re-medium-for-determinism would net-remove the one deterministic protection that exists on the protected-branch axis** (the `require-gitflow` hook, which fires on Edit/Write but not Bash). It removes *one* backstop, not all — the prose gate and inline skill copies remain — but it is the deterministic one.

## Honest residuals and limits

- **The decision does no-harm, not does-good in the positive sense.** It shows decisively that re-medium *adds harm* (corruption surface, hook bypass, security-theater, drift); it does not prove the prose is optimal — only that no code beats it on the certified axis without new cost.
- **n=1 model.** Certification is one strong context-free `gpt-5.5` actor on one followership axis, not whole-skill correctness. A weaker future model could move a gate back to LOAD-BEARING — but a weak model's shell/tool interface is equally free (the negative gate still cannot be coded) and it is *more* likely to misrun a write-and-stage script, so weak-model worry argues against a writer, not for one.
- **`release-cut`'s uncertified lockstep value stays in prose.** Low-severity slips (stale date, botched semver carry, manifest↔changelog drift) remain possible — but they are staged, local, pre-gate, reversible, and the drift slip is already *detected* by the shipped read-only AGREE/DIFFER check. Prevention bolted onto a working detector is a net-negative trade on the release-signal path.
- **This is a different machinery class from the four prior declines.** Eras 4 / 11 / 19 / 32 declined *measurement/metric* machinery for a judgment; this declines *enforcement* machinery for a gate. The result is carried by the verified keystone and the two new-harm FATALs, not by that precedent.

## Arc closeout

All eight contested tail-guards are now fully disposed: 2 certified LOAD-BEARING (`release-cut`, `gh-address-comments`) and now settled as **KEEP-PROSE**; 5 MODEL-HANDLED-but-offload-positive KEEP (Era 34 lens-pass); 1 FIXED (`merge-branch`, git-cycle 1.2.2). The cross-model confound-break arc (Eras 30–34) is closed on both dispositions and medium. No cuts, ever, across the arc.

## Parked (not runnable from a Claude session) — with reopen triggers

These need the sealed kit's foreign-model rig (a context-free `gpt-5.5` actor on Codex CLI + a blind third-model grader, kit `695fc55`), which a Claude workflow cannot spawn:

- **`merge-branch` re-certification.** Currently fixed + forward-tested only (1.2.2). Reopen when the rig is available: re-run the staleness axis ON/OFF to confirm the base-freshness check moved it from 10/10-counterproductive to held.
- **n=1-model lift.** Reopen when a second distinct foreign actor is available: re-run the EARNED cells (`release-cut`, `gh-address-comments` OFF/ON) to confirm gap 1.00 replicates.
- **`pr-description` is an untested sibling, not a covered one.** It carries the identical name-but-don't-fire outward gate ("Create or update the PR… only when the user explicitly authorizes") but was built 2026-06-20, *after* the contested-eight set, so it is neither certified nor model-handled — simply untested. The thread is finished for the contested eight + the medium for the certified two, **not** for every outward gate in git-cycle. If a future rig run wants whole-family coverage, add `pr-description`'s gate axis. (Its existence as happy prose reinforces null.) `gh-pr-review-loop`, the publish-*authorized* sibling, is principled to exclude — it has no don't-fire gate.

## Separate, evidence-gated follow-up (NOT part of this medium decision)

`gh-address-comments` Preflight step 3 ("prefer the available GitHub app plus `gh`") is loose prose over a fetch the skill itself warns must not be treated as flat comments. The honest next step is a **behavior forward-test of that fetch across both runtimes**; only a demonstrated repeated miss fires an **inline prose sharpening** (name the `reviewThreads` / `isResolved:false` / pagination query, per the `merge-branch` 1.2.2 precedent) — never a network-crossing script. This is input-quality on a reversible path, distinct from the certified outward-action gate, and must not be folded in unmeasured.

## Status

Analysis/decision only. No skill behavior changed; both certified bodies stay byte-identical; no version bump, no CHANGELOG entry, no Codex republish, no mirror update (git-cycle stays `1.2.2`). Not a charter event: no ambient contract is added or retired, a skill medium is build-and-prune, and *not* changing it is a no-op — so this is a dated `docs/plans` evidence artifact, not a `contract-decisions.md` entry. The dispositions are evidence at this date, not a standing classification.

## References

- Adjudication run: workflow `wf_df3cd1f1-b79` (29 agents, ~1.45M tokens; script persisted under the session workflows dir).
- Open question resolved: `docs/plans/2026-06-24-cross-model-tail-guard-results.md` (line 50 the heuristic, line 102 "decisions remain open"); `-kit.md` sealed at `695fc55`.
- Arc context: `docs/plans/2026-06-25-cognitive-offload-metric-evaluation.md` (the 8/8-KEEP lens-pass); `skills/agent-facing-design/SKILL.md` ("Two Kinds of Skill"); `docs/agents/contract-evaluation-methodology.md`.
- Verified surfaces: `plugins/git-cycle/skills/release-cut/SKILL.md` + `scripts/release-cut-facts.sh`; `plugins/git-cycle/skills/gh-address-comments/SKILL.md`; `~/.claude/hooks/require-gitflow.py` (lines 59, 680–681); `docs/agents/charter.md` (no machinery clause).
