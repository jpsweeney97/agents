# claude-home-audit — approved design spec

Approved by JP 2026-07-14 at the end of a `design-exploration` cycle. The design took one `scrutinize-skill` pressure round (six independent skeptic lenses plus direct verification; verdict Major revision) and all 10 required changes were accepted and are folded into this v2. Recon evidence and review transcripts were session-local (dated 2026-07-14); every number below is an observation from that date — re-verify against live state, don't trust counts.

## Settled context (user decisions — binding on hand-authoring)

- The want: a recurring maintenance audit of `~/.claude/` returning legibility — a map plus a cleanup plan the user adjudicates; the audit never deletes on its own initiative; each run reports deltas against the previous run. The relief is reading the situation and making calls cheaply, not automation making them.
- Scope: three strata — authored surface (skills, hooks, plugins, settings, CLAUDE.md, references); root clutter (stray one-offs at top level); machine-generated runtime bulk.
- Adjudication grain: category-level yes/no for runtime bulk; item-level judgment for skills, hooks, root strays.
- Fork answers (2026-07-14): same-run gated execution under a build-and-prune charter stance; reports and state live in `~/.claude/audits/`; transcripts keep the platform's 30-day default sweep; name = `claude-home-audit`.

## Design-shaping discovery (recon, 2026-07-14)

The runtime-bulk stratum is already governed by the platform: the `cleanupPeriodDays` sweep (default 30, unset in settings.json) expires the documented swept paths at startup — every swept dir's oldest entry sat at exactly ~30 days. So the audit does not implement expiry; it verifies sweep health, surfaces the retention knob as adjudicable policy, and hunts what the sweep does not cover (observed then: `security/agent-sdk-venv` 272MB stale since May; legacy `handoffs/` 12.5MB; `.codex-events.jsonl`; assorted caches). One live hazard: the skill-usage ledger lives in `~/.claude/logs/`, a legacy dir whose contents the sweep removes — it survives only because actively fed; `gitflow-hook.log` and the miner launchd log share that kill zone.

## Identity

- `~/.agents/skills-claude/claude-home-audit/` (Claude-only: targets Claude's home dir, uses Workflow and claude-code-docs), delivered via `claude-skills-sync.sh --link`. Bundle: `SKILL.md` + `scripts/inventory.py`.
- Build-and-prune class, internally consistent: manual invocation; adjudicated, trash-only mutation; platform-permanent mechanisms are route-only (never executed by the skill). Fire-time line in the body: never run unattended or scheduled — scheduling it is a charter event. Maintainer merit/prune-watch go to `docs/agents/skill-lifecycle-notes.md`, not the body.
- Frontmatter description finalized at hand-authoring against the misroute forecast below. Working draft: "Use when JP wants the recurring maintenance audit of ~/.claude (the user-level Claude home directory, not a project's .claude/): map what's live vs stale, verify the platform cleanup sweep is healthy, and adjudicate a cleanup plan executed with trash after approval. Symptoms: ~/.claude disk bloat, root clutter, stray files, unknown dirs, 'did cleanup run'. Do not use for a single settings edit (update-config), read-only status questions (orient-status), skill-merit judgments, or ~/.codex."
- Misroute forecast the description must defeat: wrongly-in — project-level `.claude/` cleanup, one-liner retention questions (cleanupPeriodDays guidance), read-only inventory questions, skill-merit/usage judgments, `~/.codex`; wrongly-out — disk-pressure phrasing ("Claude Code is eating my disk"), sweep-health doubts ("did cleanup run"), sensitive-stray reports.

## Run shape — six moves

1. **Preflight.** Mandated opening line: mode (first-run / delta / resume), sweep health, scale estimate (items to judge, expected sittings). Mode detection: any artifact under `~/.claude/audits/` ⇒ not first run; snapshot newer than last report close ⇒ offer resume with pending items; partial artifacts ⇒ say "state partially missing — recovery, not first run." Acquire `audits/.lock` (session id + timestamp); refuse to run over a fresh lock. Sweep health asserts the outcome, not inputs: zero swept-path entries older than cutoff+grace (script computes this), plus `.last-cleanup` freshness, settings parseability, effective `cleanupPeriodDays`. Version pins: run `claude --version`, read the docs-index freshness; on delta from the registry's stamped pair, re-verify registry entries against live docs before trusting classifications. Mutates nothing outside `~/.claude/audits/` before adjudication.
2. **Measure.** `scripts/inventory.py snapshot` — read-only, prints JSON: sizes/counts/ages/listings (the parts `find`/`du` get right by construction), settings-scope reference extraction (all scopes, including nested `~/.claude/.claude/settings.local.json`), symlink health, registry classification of documented platform paths, derived-floor computation. It does NOT do the ledger join or any semantic call. Registry entries are per-sub-path where docs demand it (`projects/<p>/memory/` = kept-forever, purge-destroyed; transcripts = swept). The registry is stamped with the docs-snapshot date + binary version it was authored against; unknown entries → `unclassified`.
3. **Judge** (agent, session model; Workflow fan-out only when item volume warrants — run #1's authored-surface pass). Forcing functions, not buckets:
   - A stray/unknown candidate enters the plan only with its writer and reader named, or an explicit "none found where I looked: <where>". Default for `unclassified + undocumented` is protected-pending-evidence — unknown ≠ stray.
   - An authored-surface candidate requires ≥1 non-ledger evidence item (broken wiring, supersession, observed mis-fire, user-stated doubt). Any silence citation states expected fire cadence vs. observation window. The ledger join is an agent move with a stated normalization contract: match both `name` and `plugin:name` keys, resolve aliases, verify against symlink targets; zero-fire on an existing skill ⇒ verify the key before believing. (Observed 2026-07-14: 144 distinct ledger names vs 77 installed entries; a naive join reads the most-fired skills as silent.)
   - An overlap claim must quote both skills' non-use boundaries and say why they fail to separate; otherwise it is not a candidate.
   - Proposed dirs are checked against contract-claimed surfaces (e.g., `handoffs/` is the handoff plugin's legacy read fallback for home-rooted sessions) — owned surfaces get an ownership flag and route out.
   - Prior decisions (`decisions.jsonl`) and the prior snapshot are read as context: deltas are computed judgmentally (plain diff over raw snapshots is fine); prior rejections are carried forward with judgment and re-surfaced cheaply with their dates in the Settled section — no mechanical suppression.
   - The empty run is legitimate: "clean — nothing to adjudicate," empty sections omitted, close immediately.
4. **Map + plan.** Write `~/.claude/audits/YYYY-MM-DD-HHMM.md`: delta-first map per stratum, then the plan in three sections matching the settled strata, with per-item flags instead of extra tiers:
   - **Runtime & policy** (category-level): sweep-health items, policy confirmations, purge candidates, non-swept bulk categories.
   - **Root strays** (item-level).
   - **Authored surface** (item-level, advisory): mostly `route:<lane>` (repo prune lanes, claude-skills-sync, update-config, repo-script edits); executed here only when the surface is `~/.claude` itself.
   - Flags: `charter-gate` (always-loaded contract — routed to the charter with evidence, never executed here even if approved in chat), `route:<lane>`, `PERMANENT` (platform mechanism — handed to the user, never run by the skill; `--yes` forbidden; dry-run offered; purge items state "deletes this project's auto memory and config entry"), `sensitive` (credential-looking strays, prioritized), and a reversibility class on every item (`trash-recoverable` / `PERMANENT` / `route`).
   - Every item: path, size, age, class, evidence (writer/reader or provenance), proposed action, flags. Settled section: prior decisions with dates, old rejections re-surfaced as one-liners.
5. **Adjudicate.** Chat carries a compact one-line-per-item digest per section; the report file carries full evidence, linked once. Category-level calls via structured asks (they fit 4×4). Item-level: numbered digest, ranged replies ("approve 1,3,5-9; reject 12: reason"), agent echoes back the parsed decisions for confirmation before recording. Item-level asks capped per sitting (~15 suggested; hand-authoring finalizes); overflow defaults to defer-and-carry at zero cost; unreached items recorded as deferred, never dropped. Each confirmed batch is appended to `audits/decisions.jsonl` immediately (resume-safe): ts, run id, path, class, decision (approve/reject/defer/policy), reason, flags.
6. **Execute + close.** Only approved, executable items (trash-recoverable, non-routed). Execute-time gate: `scripts/inventory.py check <paths>` re-stats each path, re-applies the full floor (including the derived floor and the 7-day rule) at execution time, verifies size/entry-count against the plan within tolerance; mismatches skip-and-report. Per-path preview always — never summarized ("887 files" is not a preview). `trash` only; no `rm` fallback ever — if trash fails, the item fails. Never follow symlinks out of `~/.claude`. Stop on failure; report succeeded / failed / unattempted. Unexecuted approvals expire at run close (revert to proposed, recorded as deferred). Receipt appended to the report; execution outcomes appended to `decisions.jsonl`; lock released. Close packet in chat: run date, mode, sweep health, freed, deferred, routed, failures, suggested re-run date.

## State model (v1 — deliberately thin)

`~/.claude/audits/` contains: `snapshots/<timestamp>.json` (raw inventory, schema-versioned, fail-fast with message on unknown schema), `decisions.jsonl` (append-only decision + execution-outcome records), dated reports, `.lock` during a run. No mechanical delta engine, no size-bucket identity, no key-matched suppression, no standing-policy store, no report index — the raw snapshots and decision records are the delta memory; run #2's judge diffs and carries decisions with judgment. If a mechanical differ is ever added later, it ships with a named synthetic test (fixture, two runs, one mutation) — never before.

## Hard protected floor

Two layers, enforced mechanically at measure time and again at execute time (check mode):

- **Static:** `settings.json`, nested `.claude/` (live project-scope settings + sessions for home-rooted sessions), `.claude.json`, `.mcp.json`, `plugins/`, `skills/` (symlink children; a non-symlink child like `synapsis` is item-level judgeable by explicit carve-out, never by default), `CLAUDE.md`, `keybindings.json`, `references/`, `agents/`, `commands/`, `hooks/`, `rules/`, `output-styles/` (when present), `audits/` itself.
- **Derived:** every path referenced from any settings scope (hook commands, statusline, env files) is protected wherever it lives.
- **Defaults:** `unclassified + undocumented` = protected-pending-evidence. Anything modified within 7 days is unproposable (re-checked at execution time). Never propose deleting contents of swept paths — the platform owns those; retention policy items are route-only.

## What it deliberately does not do

No verdicts on skill merit; never edits `~/.agents` sources (repo-side items route out — including the run-#1 ledger-relocation item, which is a repo-script edit to `scripts/skill-usage-hook.py` with multi-writer sequencing, not an update-config change); never executes charter-gated retirements; never executes PERMANENT platform mechanisms; never runs unattended; never re-implements the platform sweep; not a content-level security audit.

## Run-#1 queue (corrected by review)

- `security/agent-sdk-venv` (272MB observed): probe-first — creator unknown, bootstrap marker live; "unknown — probe before trash."
- `handoffs/` (12.5MB observed): handoff-plugin-owned surface — ownership flag, route/ask with the owner named; not a plain bulk-trash item.
- Ledger relocation out of legacy-swept `logs/`: route to the repo-script lane; also flag `gitflow-hook.log` and the miner launchd log living in the same kill zone.
- Root strays observed 2026-07-14: three March transcript exports, `claude-api.txt` (sensitive), `CLAUDE.md.bak-*`, three `security_warnings_state_*.json`, `skills-backup-20260609.tar.gz`.

## Proof plan

- Structural: `quick_validate.py`; YAML parse of any metadata.
- Script: snapshot mode run read-only against live `~/.claude`; check mode against a fixture (protected path, mutated path, clean path — expect block/skip/pass).
- Behavior: run #1 is the forward test for first-run mode; `behavior-smoke-test` after authoring for the reasoned predictions (adjudication ergonomics, judge forcing functions honored, empty-run legitimacy). Run #2 (real, ~a month later) is the first true delta-mode test — by design, since the mechanical delta engine was cut.
- Lifecycle-notes entry (`docs/agents/skill-lifecycle-notes.md`): merit = cognitive-offload (the careful recurring procedure summoned by one token); prune-watch = runs stop ending in adjudicated plans, seasonal non-invocation in the usage ledger, script rot vs platform changes.

## Deliberately deferred

Codex twin for `~/.codex`; archive-then-expire transcript lane; any mechanical delta/suppression engine (revisit only with two real snapshots and the synthetic test in hand); report template visual shape (settled by run #1); final adjudication cap number.

## Handoff capsule for the hand-authoring lane

- **Next lane:** hand-author `SKILL.md` + `scripts/inventory.py` against `agent-facing-design`, with the `skill-ux-design` authoring-time consult JP already scheduled; validate per the repo's Validation Ladder; link via `claude-skills-sync.sh --link claude-home-audit` and verify with `--check`; add the lifecycle-notes entry. No implementation plan needed at this size.
- **Settledness:** contested-and-corrected during the cycle — the runtime-bulk premise (platform sweep already governs it), the protected floor (rewritten from live wiring after review), the delta engine (cut from v1 by review), five-tiers→three-sections, and the run-#1 queue demotions. Accepted-as-offered — script-spine over Workflow-chassis, `~/.claude/audits/` home, the name, the 30-day policy, `skills-claude/` placement. User-settled via forks — execution model, report home, transcript policy, name.
- **Binding constraints:** trash-only literal with no `rm` fallback; PERMANENT items route-only with `--yes` forbidden; charter-gate items never executed; no unattended runs; floor enforced at measure and execute time; echo-back confirmation before any decision is recorded; per-path previews never summarized.
- **Known drift surface:** the script's registry is a stamped snapshot of the claude-code docs (authored against 2.1.210 / docs index 2026-07-13); preflight re-verifies on version or index delta.
