# Plugin bundle candidates — 2026-09-02

Read-only assessment of which skills in `skills/` and `skills-claude/` form natural plugin bundles, what each bundle would cost, and what edits packaging needs. Nothing here has been built. Evidence: every SKILL.md description, the cross-reference graph between skill bodies, the skill-usage ledger (`~/.claude/logs/skill-usage-ledger.jsonl`, 6,854 records across both runtimes), git churn since 2026-06-01, the three existing plugins, and the prior extraction plan (`docs/plans/2026-06-17-git-cycle-plugin.md`).

## Summary

Three bundles are ready now: **decide** (shape and choose), **plan-cycle** (spec to execution), and **relay** (hand-carry between sessions). Four more are coherent but built from skills that have barely fired yet: **pressure-test**, **ops-cycle**, **test-cycle**, **threat-model**. One fold into an existing plugin is clear: `land` belongs in `git-cycle`. The skill-authoring family should stay unpackaged.

## How candidates were judged

The three existing plugins set the bar. `git-cycle` is "one arc" (dirty tree to merged-and-shared) whose skills hand off to each other. `review-family` is one job (evidence-first review) with a shared inline core guarded by a drift check. `handoff` is one storage contract. A candidate qualifies when its skills route to each other in their own text and a user would install them together.

Constraints applied to every candidate:

- Plugins are dual-runtime by contract (`AGENTS.md`, Plugin Layout And Delivery). Claude-only skills in `skills-claude/` stay out.
- Every behavior change to a plugin skill pays a release tax: version bump, CHANGELOG section, Codex republish, and an ask-gated mirror sync. High-churn skills pay it often.
- Usage is input, not verdict (`AGENTS.md`, What The Skills Are For). Skills admitted in August and September are silent because they are new, not because they lack merit.

Ledger caveat: records without a `runtime` field are Claude fires (3,666); `codex` records are 3,188. After packaging, Claude-side fires appear only under the namespaced token (bare `merge-branch` and `closeout-check` fires stop on 2026-06-17, the day `git-cycle` 1.0.0 landed).

## Tier 1 — bundle now

### 1. `decide` — shape a want, widen the field, choose, record

| Skill | Fires | Repos | Commits since June | First commit |
|---|---|---|---|---|
| making-recommendations | 299 | 17 | 18 | pre-June |
| outcome-shaping | 137 | 9 | 2 | pre-June |
| design-exploration | 36 | 8 | 8 | pre-June |
| decision-record | 19 | 3 | 4 | pre-June |
| deliberate | 14 | 3 | 29 | pre-June |
| ideate | 9 | 4 | 6 | pre-June |
| option-shaping | 5 | 4 | 2 | pre-June |
| scope-cut | 0 | 0 | 4 | 2026-06-30 |
| decision-owner-map | 0 | 0 | 3 | 2026-08-06 |

Why it is a family: the five core skills (outcome-shaping, ideate, option-shaping, making-recommendations, design-exploration) reference each other almost pairwise, and their descriptions already form one routing chain ("once the want is clear: shaping a design is design-exploration, choosing among named options is making-recommendations"). `deliberate` runs that chain autonomously. `scope-cut` cuts a shaped scope. `decision-record` and `decision-owner-map` capture and route the result. Total fires: 519, the highest of any unpackaged family.

Borderline: `next-steps` (27 fires, explicit-invoke only) turns findings into a sequenced action plan; it fits here or in plan-cycle. Default: leave it standalone until one bundle clearly owns it.

Cost to know: `deliberate` and `making-recommendations` are among the most-edited skills in the library (29 and 18 commits since June). Each future edit becomes a release. Mitigation is batching edits into releases, which `review-family` already does (0.17.0 in twelve weeks).

Bundle-specific edits:

- `deliberate` ships `scripts/` and `tests/`; both move with it. Its validator's embedded tests use `skills/<name>/SKILL.md` fixture paths (lines 5989 to 6869 of `deliberate-validate.py`); run `uv run pytest skills/deliberate/tests` after the move and update the fixtures if they are asserted against the tree.
- New re-run capsules will record source paths under `plugins/decide/skills/`; old capsules stay valid because they pin content ids.

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

Why it is a family: PRD to issues to plan to execution is one arc, and every member routes to its neighbors by name. `triage` and `implement-issue` are the tracker side of the same arc. `acceptance-map` sits between spec and implementation. `spec-drift-reconcile` is what runs when intent changes mid-arc. Total fires: 180. Churn is lower than `decide`, so this is the cheaper first bundle to build.

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

Why it is a family: all three exist to move a packet between a session here and a session elsewhere, and each names the other two as its neighbor. `context-checkpoint` belongs to the same job but is Claude-only and stays in `skills-claude/`.

Alternative: fold these into `handoff` as 4.0.0. Against that: `handoff` is defined by one storage contract (`<project_root>/.agents/handoffs/`, guarded by `scripts/check-handoff-paths.sh`), and these three write elsewhere (`~/scratch-workspace/relay/`, `~/prompts`). A separate plugin keeps the handoff contract clean. Recommendation: separate plugin.

Borderline: `to-questionnaire` (0 fires, 2026-09-01) produces a Markdown packet for a named person and names `courier` and `stage-prompt` as neighbors; `transcript-export` (0 fires) exports a session. Either could join later.

## Tier 2 — coherent, bundle when you want them as a unit

These families are real by cross-reference, but most members were admitted between late June and early August and have fired zero or one time. Bundling them now buys a README that maps the family and a versioned unit, at the release tax. Silence is not evidence against them; it is a reason the bundle has no observed payoff yet.

### 4. `pressure-test` — before committing to a settled plan

Members: grill-me (57 fires, none since 2026-06-09), grill-with-docs (30), assumption-check (0), premortem (1), steelman (0), decision-flip (0), outside-view (0), incentive-map (0). Total 88.

Why separate from `decide`: six of eight are zero-or-one-fire. Mixing them into the highest-use release unit means their edits tax `decide`'s releases. Merge the two later if one arc is preferred.

Edits: `grill-with-docs` ships `ADR-FORMAT.md` and `CONTEXT-FORMAT.md`. `steelman` is exported to claude.ai (`exports/steelman`); its export header records `skills/steelman/ @ <sha>`, so `scripts/exports-drift.sh` needs the new path.

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
6. Run `codex plugin add <name>@turbo-mode`, enable it in `~/.codex/config.toml`, and add the plugin to the bootstrap lists in both sync-script headers.
7. Repoint path-bound surfaces: `check-protected-set.sh` (acceptance-map, land), `exports-drift.sh` headers for any exported skill, `AGENTS.md` path references.
8. Invocation tokens change on Claude to `/<plugin>:<skill>`; on Codex `$<skill>` keeps working. Cross-references from other skills use bare tokens today and model routing keeps working (git-cycle precedent); prefixing them is optional.
9. Validate: `quick_validate.py` per moved skill, YAML parse of each `agents/openai.yaml`, `git diff --check`, `scripts/check-library-integrity.sh`, and one live invocation per runtime.
10. Mirror sync and push stay ask-gated.

Packaging is not a charter event: skills are build-and-prune, and the ledger's 2026-07-26 entries settle that reversibility class reads on capability, not packaging. A new drift-check script is capability tooling and charter-exempt; its SessionStart wiring lives in the untracked `.claude/settings.local.json`.

## Naming constraints

The plugin name is the Claude namespace. Avoid installed plugin names (codex, github, impeccable, obsidian, pyright-lsp, swift-lsp, typescript-lsp), Claude bundled skill names (code-review, debug, loop, run, verify, security-review, simplify), and Codex bundled names. Proposed names: `decide`, `plan-cycle`, `relay`, `pressure-test`, `ops-cycle`, `test-cycle`, `threat-model`.

## Open decisions

1. Build order. Recommended: `plan-cycle` first (lowest churn, cheapest proof of the process), then `decide`, then `relay`.
2. `pressure-test`: separate plugin (recommended) or folded into `decide`.
3. `relay`: separate plugin (recommended) or `handoff` 4.0.0.
4. `land` into `git-cycle` 1.7.0: yes or no.
5. Placement of `next-steps` and `to-questionnaire`: standalone (recommended for now), `decide`/`plan-cycle`, or `relay`.
