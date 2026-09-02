# Plugin bundle candidates — 2026-09-02

Read-only assessment of which skills in `skills/` and `skills-claude/` form natural plugin bundles, what each bundle would cost, and what edits packaging needs. Nothing here has been built. Evidence: every SKILL.md description, the cross-reference graph between skill bodies, the skill-usage ledger (`~/.claude/logs/skill-usage-ledger.jsonl`, 6,854 records across both runtimes), git churn since 2026-06-01, the three existing plugins, and the prior extraction plan (`docs/plans/2026-06-17-git-cycle-plugin.md`). Revised 2026-09-02 to the cross-model deliberation certificate; see Settled by deliberation at the end.

## Summary

Three bundles are ready now, to be built in this order: **relay** (hand-carry between sessions), then **plan-cycle** (spec to execution), then **decide** (shape and choose, seven skills). Four more are coherent but built from skills that have barely fired yet: **pressure-test**, **ops-cycle**, **test-cycle**, **threat-model**. One fold into an existing plugin is clear: `land` belongs in `git-cycle`. The skill-authoring family should stay unpackaged.

## How candidates were judged

The three existing plugins set the bar. `git-cycle` is "one arc" (dirty tree to merged-and-shared) whose skills hand off to each other. `review-family` is one job (evidence-first review) with a shared inline core guarded by a drift check. `handoff` is one storage contract. A candidate qualifies when its skills route to each other in their own text and a user would install them together.

Constraints applied to every candidate:

- Plugins are dual-runtime by contract (`AGENTS.md`, Plugin Layout And Delivery). Claude-only skills in `skills-claude/` stay out.
- Every behavior change to a plugin skill pays a release tax: version bump, CHANGELOG section, Codex republish, and an ask-gated mirror sync. High-churn skills pay it often.
- Usage is input, not verdict (`AGENTS.md`, What The Skills Are For). Skills admitted in August and September are silent because they are new, not because they lack merit.

Ledger caveat: records without a `runtime` field are Claude fires (3,666); `codex` records are 3,188. After packaging, Claude-side fires appear only under the namespaced token (bare `merge-branch` and `closeout-check` fires stop on 2026-06-17, the day `git-cycle` 1.0.0 landed).

## Tier 1 — bundle now

### 1. `decide` — shape a want, widen the field, choose

| Skill | Fires | Repos | Commits since June | First commit |
|---|---|---|---|---|
| making-recommendations | 299 | 17 | 18 | pre-June |
| outcome-shaping | 137 | 9 | 2 | pre-June |
| design-exploration | 36 | 8 | 8 | pre-June |
| deliberate | 14 | 3 | 29 | pre-June |
| ideate | 9 | 4 | 6 | pre-June |
| option-shaping | 5 | 4 | 2 | pre-June |
| scope-cut | 0 | 0 | 4 | 2026-06-30 |

Why it is a family: the five core skills (outcome-shaping, ideate, option-shaping, making-recommendations, design-exploration) reference each other almost pairwise, and their descriptions already form one routing chain ("once the want is clear: shaping a design is design-exploration, choosing among named options is making-recommendations"). `deliberate` runs that chain autonomously. `scope-cut` cuts a shaped scope. Total fires: 500, the highest of any unpackaged family.

Left standalone, per the deliberation (both were in the original nine): `decision-record` binds `../grill-with-docs/ADR-FORMAT.md` as its single format source and forbids forking it, so it cannot sit in a plugin apart from `grill-with-docs`; `decision-owner-map` routes a decision to an owner rather than making one, and no core decide skill routes to it.

Borderline: `next-steps` (27 fires, explicit-invoke only) turns findings into a sequenced action plan; it fits here or in plan-cycle. Default: leave it standalone until one bundle clearly owns it.

Cost to know: `deliberate` and `making-recommendations` are among the most-edited skills in the library (29 and 18 commits since June). Unique commits since 2026-06-01 across the seven: 57 (49 files). Each future edit becomes a release. Mitigation is batching edits into releases, which `review-family` already does (0.17.0 in twelve weeks).

Bundle-specific edits:

- `deliberate` ships `scripts/` and `tests/`; both move with it.
- deliberate re-run capsules: a re-run re-resolves constituent and method pins as whole path-plus-id entries (`_pin_change_frontiers` in `skills/deliberate/scripts/deliberate-validate.py`), so moving the decide skills changes the recorded locators and invalidates existing capsules from the affected stage, Generate once ideate or deliberate's own method paths move. The migration must run the full deliberate suite and a focused old-capsule/new-pins re-run test proving that invalidation. The embedded `skills/...` paths and `skills/deliberate/tests/fixtures/valid-capsule.yaml` are synthetic validation fixtures; update them only if the tests are intentionally changed to model the post-move layout, not as a prerequisite of the move. Do not claim old capsules continue unchanged.

### 2. `plan-cycle` — from settled spec to executed work

| Skill | Fires | Repos | Commits since June | First commit |
|---|---|---|---|---|
| implementation-planning | 70 | 9 | 6 | pre-June |
| triage | 54 | 6 | 9 | pre-June |
| execute-plan | 48 | 9 | 4 | pre-June |
| to-issues | 5 | 2 | 10 | pre-June |
| spec-drift-reconcile | 2 | 1 | 4 | pre-June |
| acceptance-map | 1 | 1 | 6 | pre-June |
| to-prd | 0 | 0 | 8 | 2026-06-05 |
| plan-queue | 0 | 0 | 1 | 2026-07-26 |
| implement-issue | 0 | 0 | 1 | 2026-09-01 |

Why it is a family: PRD to issues to plan to execution is one arc, and every member routes to its neighbors by name. `triage` and `implement-issue` are the tracker side of the same arc. `acceptance-map` sits between spec and implementation. `spec-drift-reconcile` is what runs when intent changes mid-arc. Total fires: 180. Unique commits since 2026-06-01 across the nine: 25 (12 files). Build it second, after `relay`.

Bundle-specific edits:

- `acceptance-map` carries the protected-branch sentence and is a target in `scripts/check-protected-set.sh`; repoint that entry.
- `to-prd`, `to-issues`, and `triage` name `setup-matt-pocock-skills` (Claude-only, stays in `skills-claude/`); the phrasing is already availability-conditional, so no text change is needed.
- `triage` ships `AGENT-BRIEF.md` and `OUT-OF-SCOPE.md`; they move with it.
- `plan-queue` performs fast-forward merges and was admitted under the irreversible-effect carve-out. Packaging does not change its class: the ledger's 2026-07-26 `land` entry states reversibility reads on capability, not packaging.

### 3. `relay` — carry work between sessions and models by hand

| Skill | Fires | Repos | First commit |
|---|---|---|---|
| relay-by-reference | 56 | 4 | 2026-07-26 |
| stage-prompt | 28 | 7 | pre-June |
| courier | 3 | 1 | 2026-07-26 |

Unique commits since 2026-06-01 across the three: 5 (3 files). Build it first: it is the smallest, lowest-churn migration on which to prove the packaging and dual-runtime load procedure.

Why it is a family: all three exist to move a packet between a session here and a session elsewhere, and each names the other two as its neighbor. `context-checkpoint` belongs to the same job but is Claude-only and stays in `skills-claude/`.

Alternative: fold these into `handoff` as 4.0.0. Against that: `handoff` is defined by one storage contract (`<project_root>/.agents/handoffs/`, guarded by `scripts/check-handoff-paths.sh`), and these three write elsewhere (`~/scratch-workspace/relay/`, `~/prompts`). A separate plugin keeps the handoff contract clean. Recommendation: separate plugin.

Borderline: `to-questionnaire` (0 fires, 2026-09-01) produces a Markdown packet for a named person and names `courier` and `stage-prompt` as neighbors; `transcript-export` (0 fires) exports a session. Either could join later.

## Tier 2 — coherent, bundle when you want them as a unit

These families are real by cross-reference, but most members were admitted between late June and early August and have fired zero or one time. Bundling them now buys a README that maps the family and a versioned unit, at the release tax. Silence is not evidence against them; it is a reason the bundle has no observed payoff yet.

### 4. `pressure-test` — before committing to a settled plan

Members: grill-me (57 fires, none since 2026-06-09), grill-with-docs (30), assumption-check (0), premortem (1), steelman (0), decision-flip (0), outside-view (0), incentive-map (0). Total 88.

Why separate from `decide`: its skills challenge a settled or proposed position rather than forming or choosing one. The fire counts above (six of eight at zero or one) were not re-derived in the deliberation and do not determine this; keeping the two release units apart also stops their edits taxing `decide`'s releases. Merge the two later if one arc is preferred.

Edits: `grill-with-docs` ships `ADR-FORMAT.md` and `CONTEXT-FORMAT.md`; `decision-record` (standalone) and `improve-codebase-architecture` link those files by relative path, so moving `grill-with-docs` means updating their references per the maintenance note in `grill-with-docs/SKILL.md`. `steelman` is exported to claude.ai (`exports/steelman`); its export header records `skills/steelman/ @ <sha>`, so `scripts/exports-drift.sh` needs the new path.

### 5. `ops-cycle` — ship, watch, respond, learn

Members: deploy-plan, incident-response, postmortem, runbook-authoring, observability-instrumentation, migration-safety, outcome-check. All admitted 2026-06-25 to 2026-06-27; 1 fire total. Dense cross-references; every member is advisory-only and names what it never executes. That shared convention is phrased differently per skill, so a drift check would be new design, not a repoint.

Left out on purpose: `dependency-upgrade` and `migration-campaign` apply changes rather than plan operations.

### 6. `test-cycle` — from failing behavior to trusted green

Members: tdd (27 fires), diagnose (8), bug-epidemiology (0), characterization-tests (0), test-trust-audit (0), keep-green (0). Total 35. `diagnose` ships `scripts/`; `tdd` ships five reference docs.

### 7. `threat-model` — attacker modeling and boundary defense

Members: red-team (1 fire), authorization-design (0), injection-safe-inputs (0), regex-craft (0). Three of them already share two verbatim sentences ("Default to the mode the context implies; ask once when genuinely ambiguous." and "Delivered in the mode the invocation implies, advisory-until-asked, nothing published unless asked."). That is the same situation `review-family` solved with `scripts/check-review-family.sh`; this bundle would need its own drift check. The name must avoid Claude's bundled `security-review`.

## One fold into an existing plugin

`land` (26 fires, 9 repos) references seven of the ten `git-cycle` skills, is already a target in `check-protected-set.sh`, and completes the arc `git-cycle` describes ("to merged-and-shared"). Moving it in is a feature, so `git-cycle` goes to 1.7.0. Repoint the drift-check entry.

## Not bundling, and why

- **Skill-authoring family** (agent-facing-design, writing-principles, skill-ux-design, behavior-smoke-test, methodology-check, skill-export, work-router, plus the Claude-only skill-benchmark, skill-squad, gap-review, methodology-critique, friction-to-guards). Half is Claude-only. The dual-runtime half is the most-edited in the library (28, 21, and 13 commits since June for the first three), so the release tax would land on the skills you touch most. `AGENTS.md` hardcodes `skills/agent-facing-design/SKILL.md` as the canonical gate. `scrutinize-skill` already lives in `review-family`, so the family would span two plugins either way.
- **Image-prompt pair** (collaborative-image-prompt-architect, scrutinize-image-prompt). Tightly paired, 8 fires total. A plugin's fixed overhead (manifest, five support files, marketplace entry, mirror) exceeds the benefit of packaging two skills.
- **Markdown toolbox** (markdown-reformat, markdown-synthesis, research-capture, document-to-markdown). Each is invoked alone; they do not hand off to one another.
- **Codebase-map cluster** (explain-codebase, zoom-out, orient-status, add-an-x-by-example, co-change-radar, contract-change-propagation, fence-archaeology, doc-drift-audit, shelf-life, baseline). Two loose sub-clusters, 25 fires total, no shared contract.
- **Code-quality toolbox** (simplify-code, improve-codebase-architecture, tech-debt-scan, perf-optimize, migration-campaign, dependency-upgrade). Standalone invocations with high churn (19 and 15 commits for tech-debt-scan and simplify-code).
- **Standalone disciplines and personal skills** (hold-or-fold, recheck-investment, substitution-ledger, working-slice-review, soundcheck, reflect, reality-check, email-writing, caveman, the-gang-explains, teach, athenahealth-brand-system, claude-code-docs). No arc to join.
- **decision-record and decision-owner-map** (removed from `decide` by the deliberation). decision-record cannot leave `grill-with-docs`'s format file under its current text; decision-owner-map is a routing packet, not a decision, with no reciprocal reference from the core.
- **apply-findings** must not go into `review-family`: that plugin's contract is review-only, guarded by the read-only core in `check-review-family.sh`, and `apply-findings` edits files.

## What packaging costs

Claude reads plugin source in place; a SKILL.md edit is live next session. Codex serves a versioned cache, so every behavior change needs a manifest bump, a CHANGELOG section (`release-cut`), a `codex plugin add` republish, and, when you choose to publish, a mirror sync. Per `AGENTS.md`, a landed bump is publish intent. The route guard (`scripts/skill-route-guard.py`) already covers `plugins/` paths, so the satellite editing workflow does not change.

## Edits every bundle needs

Generalized from the git-cycle plan, Workstream 3.

1. Do the move in a satellite worktree through `worktree-task-cycle`; the route guard blocks skill-surface edits in the primary checkout. The fleet keys satellite identity on the bare directory name and censuses plugin skill roots, so a moved skill keeps its satellite; run `scripts/satellite-fleet.py check` after landing to confirm.
2. Scaffold `plugins/<name>/.claude-plugin/plugin.json` (the `name` becomes the Claude namespace; version 1.0.0 for established skills, per the git-cycle precedent), plus README, CHANGELOG, LICENSE, PRIVACY.md, TERMS.md copied from an existing plugin.
3. Copy each skill directory with its companions (`agents/openai.yaml`, `references/`, `examples/`, `scripts/`, `tests/`, loose reference files). Delete the originals only after a live-load test in both runtimes.
4. Add the `plugins/marketplace.json` entry with a relative path (`./.agents/plugins/<name>`); verify with `codex plugin list`.
5. Run `scripts/claude-skills-sync.sh --link <name>`, trash each moved skill's stale symlink in `~/.claude/skills`, then `--check`.
6. Run `codex plugin add <name>@turbo-mode`, enable it in `~/.codex/config.toml`, and add the plugin to the enumerated bootstrap list in the header of `scripts/codex-plugins-sync.sh` (`scripts/claude-skills-sync.sh` discovers every `plugins/` directory generically and needs no edit).
7. Repoint path-bound surfaces: `check-protected-set.sh` (acceptance-map, land), `exports-drift.sh` headers for any exported skill, `AGENTS.md` path references.
8. Invocation tokens change on Claude to `/<plugin>:<skill>`; on Codex `$<skill>` keeps working. Cross-references from other skills use bare tokens today and model routing keeps working (git-cycle precedent); prefixing them is optional.
9. Validate: `quick_validate.py` per moved skill, YAML parse of each `agents/openai.yaml`, `git diff --check`, `scripts/check-library-integrity.sh`, and one live invocation per runtime.
10. Mirror sync and push stay ask-gated.

Packaging is not a charter event: skills are build-and-prune, and the ledger's 2026-07-26 entries settle that reversibility class reads on capability, not packaging. A new drift-check script is capability tooling and charter-exempt; its SessionStart wiring lives in the untracked `.claude/settings.local.json`.

## Naming constraints

The plugin name is the Claude namespace. Avoid installed plugin names (codex, github, impeccable, obsidian, pyright-lsp, swift-lsp, typescript-lsp), Claude bundled skill names (code-review, debug, loop, run, verify, security-review, simplify), and Codex bundled names. Proposed names: `decide`, `plan-cycle`, `relay`, `pressure-test`, `ops-cycle`, `test-cycle`, `threat-model`.

## Settled by deliberation (2026-09-02)

A cross-model deliberation with Codex (run `~/.synapsis/runs/2026-09-02-plugin-bundle-candidates/`, readable `answer.md` beside the authoritative `run.json`) ended in a CONCESSION certificate: the host retired its pre-committed stance on two of the six decisions after verifying Codex's evidence at 5ee3a53. Settled: (1) `decide` at seven skills with `pressure-test` separate; (2) `plan-cycle` at nine; (3) `relay` as its own plugin, not a `handoff` fold; (4) `land` into `git-cycle` 1.7.0; (5) the skill-authoring family unpackaged; (6) build order `relay`, then `plan-cycle`, then `decide`. The certificate also corrected two packaging claims in the original text (deliberate capsule invalidation; the sync-script bootstrap list), both applied above. It does not assert that anything is built or published, that the tier-2 bundles were re-verified, that the usage counts are correct, or where `ADR-FORMAT.md` should live long-term.

## Open decisions

1. Go or no-go on building `relay` first.
2. Placement of `next-steps` and `to-questionnaire`: standalone (recommended for now), `decide`/`plan-cycle`, or `relay`.
3. Only if `decide` is built: whether to redesign the home of `ADR-FORMAT.md` so `decision-record` can join it.
   Resolved 2026-09-02: `decide` 1.1.0 takes `decision-record`; the format file moved to `plugins/decide/references/ADR-FORMAT.md` with a git-tracked symlink at the old `skills/grill-with-docs/` path. Design and certificate: `docs/plans/2026-09-02-adr-format-home.md`, `~/.synapsis/runs/2026-09-02-adr-format-home/`. The statements above that `decision-record` cannot leave `grill-with-docs` describe the tree at the time and are left as written.
