---
name: claude-home-audit
description: "Use when JP wants the recurring maintenance audit of ~/.claude — the user-level Claude home directory, not a project's .claude/: map what's live vs stale, verify the platform cleanup sweep is healthy, and adjudicate a cleanup plan executed with trash after approval. Symptoms: ~/.claude disk bloat, root clutter, stray or unknown files, 'did cleanup run'. Do not use for a single settings edit (update-config), read-only status questions (orient-status), skill-merit judgments, or ~/.codex."
---

# Claude Home Audit

Recurring maintenance audit of `~/.claude`. The product is legibility: a delta-aware map of the home directory plus a cleanup plan the user adjudicates item by item. The audit proposes, the user decides, execution is trash-only. Each run reports deltas against the previous run.

Invoked as `/claude-home-audit`. Never run unattended or on a schedule — scheduling this skill is a charter event, not a configuration choice.

`$SKILL_DIR` below means this skill's base directory (announced when the skill loads).

## Boundaries

- Mutate nothing outside `~/.claude/audits/` before adjudication. After adjudication, mutate only approved plan items, only with `trash <path>`. No `rm`, ever, and no fallback: if `trash` fails, the item fails.
- Never follow symlinks out of `~/.claude`. The check gate blocks any path that resolves outside the home directory.
- Platform-permanent mechanisms are route-only. `claude project purge` and retention-policy changes are handed to the user as commands to run themselves, never executed by the audit; `--yes` is forbidden in any handed command; offer `--dry-run` first. Purge items state plainly: "deletes this project's auto memory and its config entry."
- Charter-gated items — always-loaded contracts such as hooks, rules, or ambient instructions — are routed to the charter with evidence, never executed here, even if approved in chat.
- Never edit `~/.agents` sources. Repo-side findings (script edits, skill changes) route out to their owning lanes.
- No verdicts on skill merit. Not a content-level security audit. Never re-implement the platform sweep — verify its outcome and surface its knob as adjudicable policy.

## Run Shape

### 1. Preflight

Open with one line before anything else:

```text
Audit: <first-run | delta since <date> | resume of <date>>; sweep <healthy | N violation(s)>; ~<N> items to judge, ~<M> sitting(s) expected.
```

Mode detection: any artifact under `~/.claude/audits/` means this is not a first run. A snapshot newer than the last report close means an interrupted run — offer resume with its pending items. Partial artifacts (snapshot without report, decisions without snapshot) mean "state partially missing — recovery, not first run"; say so.

Acquire `~/.claude/audits/.lock` containing the session id and an ISO timestamp. Refuse to run over a fresh lock (modified within 24 hours); an older lock is stale — note it and replace it.

Sweep health comes from the snapshot (move 2) and asserts the outcome, not the inputs: zero swept-path entries older than the cutoff-plus-grace the script computes, `.last-cleanup` fresh, every settings scope parseable (an unparseable settings file pauses the platform sweep), and the effective `cleanupPeriodDays` named.

Version pins: run `claude --version` and, when the claude-code-docs server is available, read the docs-index freshness. The snapshot carries the registry's stamped pair (docs-index date + binary version it was authored against). On a delta from the stamped pair, re-verify the registry classifications against live docs before trusting them; say which entries were re-verified.

### 2. Measure

```bash
mkdir -p ~/.claude/audits/snapshots
uv run "$SKILL_DIR/scripts/inventory.py" snapshot > ~/.claude/audits/snapshots/<UTC-timestamp>.json
```

The script is read-only and prints JSON: per-entry sizes, counts, ages, and listings; registry classification of documented platform paths (per-sub-path where the docs demand it — `projects/<p>/memory/` is kept-forever while the surrounding transcripts are swept); settings-scope reference extraction across all scopes including the nested `~/.claude/.claude/settings.local.json`; symlink health under `skills/`; sweep-health computation; and the protected floor (static + derived). Unknown entries come back `unclassified`. The script makes no semantic calls and does not do the ledger join.

### 3. Judge

Judgment work, not classification. The forcing functions:

- A stray/unknown candidate enters the plan only with its writer and reader named, or an explicit "none found where I looked: <where>". The default for `unclassified + undocumented` is protected-pending-evidence — unknown ≠ stray.
- An authored-surface candidate requires at least one non-ledger evidence item: broken wiring, supersession, observed mis-fire, or user-stated doubt. Any silence citation states expected fire cadence vs. the observation window.
- The ledger join is an agent move with a stated normalization contract: match both `name` and `plugin:name` keys, resolve aliases, verify against symlink targets. Zero-fire on an existing skill means verify the key before believing it — a naive join reads the most-fired skills as silent.
- An overlap claim must quote both skills' non-use boundaries and say why they fail to separate; otherwise it is not a candidate.
- Proposed directories are checked against contract-claimed surfaces before entering the plan — `~/.claude/handoffs/` is the handoff plugin's legacy read fallback for home-rooted sessions, so it gets an ownership flag and routes out rather than being a plain bulk item. Owned surfaces get an ownership flag and route out.
- Prior decisions (`decisions.jsonl`) and the prior snapshot are context: compute deltas judgmentally (a plain diff over raw snapshots is fine), carry prior rejections forward with judgment, and re-surface them cheaply as dated one-liners in the Settled section — no mechanical suppression.
- The empty run is legitimate: "clean — nothing to adjudicate," empty sections omitted, close immediately.

Fan out via Workflow only when item volume warrants it (a first run's authored-surface pass); otherwise judge inline.

### 4. Map + Plan

Write `~/.claude/audits/YYYY-MM-DD-HHMM.md`: a delta-first map per stratum, then the plan in three sections:

- **Runtime & policy** (category-level): sweep-health items, policy confirmations, purge candidates, non-swept bulk categories.
- **Root strays** (item-level).
- **Authored surface** (item-level, advisory): mostly `route:<lane>` items — repo prune lanes, `claude-skills-sync`, `update-config`, repo-script edits; executed here only when the surface is `~/.claude` itself.

Every item carries: path, size, age, class, evidence (writer/reader or provenance), proposed action, and flags. Flags: `charter-gate`, `route:<lane>`, `PERMANENT` (platform mechanism, handed to the user), `sensitive` (credential-looking strays, prioritized first), and a reversibility class on every item — `trash-recoverable` / `PERMANENT` / `route`. Close the report with a Settled section: prior decisions with dates, old rejections as one-liners.

### 5. Adjudicate

Chat carries a compact one-line-per-item digest per section; the report file carries full evidence, linked once. Category-level calls go through structured asks. Item-level: numbered digest, ranged replies ("approve 1,3,5-9; reject 12: reason"), then echo back the parsed decisions for confirmation before recording anything. Cap item-level asks at 15 per sitting; overflow defaults to defer-and-carry at zero cost; unreached items are recorded as deferred, never dropped. Append each confirmed batch to `~/.claude/audits/decisions.jsonl` immediately (resume-safe): ts, run id, path, class, decision (approve/reject/defer/policy), reason, flags.

### 6. Execute + Close

Only approved, executable items: `trash-recoverable` and not routed. Gate every execution batch:

```bash
uv run "$SKILL_DIR/scripts/inventory.py" check <plan.json>
```

The check re-stats each path, re-applies the full floor (static, derived, registry, 7-day rule) at execution time, and verifies size/entry-count against the plan within tolerance. `block` and `skip` verdicts are skip-and-report — never argued past. Per-path preview always, before each trash: path, size, entry count ("887 files" as a summary is not a preview — show the paths). Stop on the first failure; report succeeded / failed / unattempted. Unexecuted approvals expire at run close: revert to proposed, recorded as deferred.

Append the receipt to the report and the execution outcomes to `decisions.jsonl`, release the lock, then close in chat:

```text
Run <date> (<mode>): sweep <verdict>; freed <size>; <N> deferred; <N> routed; <N> failures. Re-run suggested <date>.
```

## Protected Floor

Enforced mechanically by the script at measure time and again at execute time:

- **Static:** `settings.json`, nested `.claude/`, `.claude.json`, `.mcp.json`, `plugins/`, `skills/`, `CLAUDE.md`, `keybindings.json`, `references/`, `agents/`, `commands/`, `hooks/`, `rules/`, `output-styles/`, and `audits/` itself. `skills/` children are symlinks; a non-symlink child (e.g. `synapsis`) is item-level judgeable by explicit carve-out, never by default.
- **Derived:** every path referenced from any settings scope (hook commands, statusline, env files) is protected wherever it lives.
- **Defaults:** `unclassified + undocumented` is protected-pending-evidence. Anything modified within 7 days is unproposable (re-checked at execution time). Never propose deleting contents of swept paths — the platform owns those; retention policy is a route-only item.

## State

`~/.claude/audits/` holds: `snapshots/<timestamp>.json` (raw inventory, schema-versioned — a reader that meets an unknown schema version fails fast with a message), `decisions.jsonl` (append-only decision and execution-outcome records), dated reports, and `.lock` during a run. There is no mechanical delta engine, no suppression index, no report index: the raw snapshots and decision records are the delta memory, and the next run's judge diffs them with judgment.

## Steering

- "runtime only" / "skip authored surface" — limit the run to the named strata.
- "defer everything" — record all open items as deferred and close.
- "show item N" — full evidence for one digest item from the report.
- "abort" — release the lock, execute nothing, record nothing new.
- Ranged replies at adjudication: "approve 1,3,5-9; reject 12: reason; defer the rest."

## Known Hazards

- The skill-usage ledger lives in `~/.claude/logs/` — a legacy directory whose contents the platform sweep removes. It survives only because it is actively fed; `gitflow-hook.log` and the miner launchd log share that kill zone. Relocation is a repo-script edit (`route:repo`), not an audit execution and not an `update-config` change.
- `~/.claude/handoffs/` is contract-claimed by the handoff plugin (legacy read fallback); flag ownership, route out.
- Transcripts and history are plaintext; credential-looking strays get the `sensitive` flag and go first in the digest.
