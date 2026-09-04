---
name: gap-review
description: "Use when JP asks to evaluate or audit a skill or plugin in this library (~/.agents) for gaps or defects — `/gap-review <name>` or `evaluate <name> for gaps`: dimension-fitted multi-agent review with adversarial verification, ending at a verified-findings decision report. Claude-only (needs the Workflow tool); the expensive multi-agent lane, reserved for explicit gap/audit framing. Do not use for a plain review-this-skill or scrutinize ask or single-surface contract critique (`scrutinize-skill`), methodology soundness (`methodology-check`), quantitative benchmarking (`skill-benchmark`), or repo-wide debt scans (`tech-debt-scan`)."
argument-hint: <plugin-or-skill-name>
---

# Gap Review

Evaluate one skill or plugin in this library for gaps and defects, and end at a report in which every finding has survived adversarial verification. This skill's boundary is the report: it never edits the target, commits, lands, or publishes. Applying approved fixes belongs to the skills named in the close packet, after JP chooses.

"Gap" means: contract text that misbehaves on reachable inputs, surfaces that disagree with each other, lifecycle states no surface covers, conventions the contracts consume but never document, and routing or delivery defects — judged against what the target's own boundaries declare, not against an imagined larger product.

Runs attended, in the main session transcript; not for cron, hooks, or unattended dispatch.

## Target

The argument names the target. Resolve it against the library's primary checkout, `~/.agents`, regardless of the session's working directory — the landed tree there is what gets reviewed; unlanded drafts in worktrees are out of scope.

- Search `~/.agents/plugins/` — including each plugin's internal skills, `plugins/*/skills/*` — plus `~/.agents/skills/` and `~/.agents/skills-claude/`. Classify the match: plugin, skill inside a plugin, dual-runtime skill, or Claude-only skill.
- Unambiguous: state the resolution in the first status line — `Target resolved: plugins/handoff — dual-runtime plugin, four skills; evaluation-only, run ends at the report` — and proceed without waiting.
- The name matches a skill inside a plugin, or more than one unit: ask first, numbered options (the skill alone, its containing plugin, each match).
- The name also plausibly names an artifact live in this conversation — a handoff, a plan, a review: treat that as ambiguous too and ask; the general review lanes own the artifact reading.
- No argument: offer a numbered menu. With more than ~20 units in the homes, list the plugins and the most recently modified skills and ask for a name fragment to narrow; otherwise list everything, grouped by kind.
- Several targets named: one unit per run — confirm order, then run sequentially, each with its own report.
- Found only in `skills-archive/` or `exports/`: say that plainly — retired or build artifact, not reviewable here — and stop.
- Not found in the library at all: decline and point to the general review lanes (`review-family:scrutinize` for artifacts, `review-family:scrutinize-skill` for skill contracts elsewhere).

Steering is plain language: "just consistency and lifecycle" narrows the dimensions, "quick" shrinks the fleet, "skip delivery checks" trims Phase 0. Honor the words; no private command vocabulary.

## Phase 0 — Scout Inline

No subagents. Read every file of the target: all `SKILL.md` files, references, companion `agents/openai.yaml`; for plugins also README, CHANGELOG, and `.claude-plugin/plugin.json`. For a skill inside a plugin, the skill's subtree is the review target and the containing plugin's manifest, README, and CHANGELOG stay in scope as consistency surfaces.

Gather delivery facts directly. Plugin: `diff -rq` the source against the installed Codex cache and the GitHub mirror checkout — both located per AGENTS.md Plugin Layout And Delivery — and check the marketplace entry and the `~/.claude/skills/<name>` symlink; for a skill inside a plugin, scope the diffs to its subtree. Plain skill: `~/.agents/scripts/claude-skills-sync.sh --check`.

Run the AGENTS.md Validation Ladder checks for the target's surfaces: `quick_validate` per skill (its accepted-complaint class stands per the Ladder), YAML-parse each `openai.yaml`, and run any canary script guarding the target (`ls ~/.agents/scripts/check-*.sh`).

Where the target's contracts govern live artifacts on this machine, gather their numbers — e.g. for a handoff-related target: the `~/.agents` pile's handoff count, newest timestamp, archive presence, `THROUGHLINE.md` size and coverage.

Everything verified here becomes the reviewers' established-facts list: verified, do not re-check, do not report as findings.

## Phase 1 — Review Workflow

Use the Workflow tool; this skill's instruction is the orchestration opt-in. Pick 3–5 independent dimensions fitted to the target — which dimensions and how many is judgment. The proven four:

1. Cross-surface consistency and documentation accuracy — everything stated on more than one surface, checked for agreement at the level of meaning; external URLs and promised paths included.
2. Lifecycle gap walk — follow the target's artifact or workflow through months of real use; hunt states and transitions no surface covers.
3. Edge-case behavioral audit — execute every written algorithm mentally against hostile-but-reachable inputs; report where the text as written misbehaves.
4. Routing and triggers — all targets; plus dual-runtime delivery contracts for dual-runtime targets.

The reviewer contract is not judgment: every reviewer reads the actual files, records which files it read, receives the established-facts list and the judging frame, classifies each finding gap / contract-defect / boundary-challenge, and is told an empty list is acceptable. Read [references/review-prompts.md](references/review-prompts.md) before writing the workflow script and re-derive the prompts from it — the non-goal rule and taxonomy travel verbatim; the rest adapts to the target.

Give progress at phase boundaries only: scout facts summarized, workflow launched, verification counts. No per-file narration.

## Phase 2 — Adversarial Verification

Dedup findings across dimensions first, then one refute-default verifier per finding (prompt draft in the same reference). Verifiers read the cited files, reproduce failures empirically where practical — reproduction is the strongest confirmation; prefer running the failing thing over reasoning about it — re-grade severity honestly, and record partial corrections to a finding's mechanism even when confirming it.

## Phase 3 — Report and Stop

Merge findings that share one root cause, even when different dimensions found them at different severities: the merged finding reports once, at the highest verifier-adjusted severity, naming the divergence. Write the full report to the session scratchpad and send the file; the chat reply is the short summary.

The report's claims match its evidence, at three levels, named as such:

- Checked with nothing found: only Phase 0's mechanical checks, plus surfaces at least one dimension read without findings (from the reviewers' recorded file lists). Claim nothing beyond those two.
- Confirmed findings: each labeled by its strongest evidence — reproduced (the verifier's `reproduced` field), or verifier-confirmed by argument.
- Refuted findings: a section listing each refuted finding's title and the verifier's reason, one line each, so the refusals can be checked.

Separate two kinds of item: decisions only JP can make (design or boundary choices — numbered options, with the one you would choose) and the mechanical fix batch. The fix batch is in the report; the close packet gives its count. Then stop. The run is complete at the report; apply nothing, even when a fix looks obvious.

## Close Packet

```text
Target: <resolved unit and kind>
Checked, nothing found: <Phase 0 checks; surfaces read without findings>
Findings: <n confirmed (high/medium/low), m refuted — refutations listed in the report>
Fix batch: <n items, in the report>
Decisions needed: <numbered, or none>
How to apply (on approval): apply-findings, through worktree-task-cycle; release-cut + CHANGELOG for plugin behavior changes; publish per AGENTS.md Plugin Layout And Delivery
Report: <absolute path> (session-temporary; tell me to save it durably and I will)
```

## Boundaries

- Evaluation only. No target edits, no commits, no landing, no publishing, no mirror or push. The close packet names the owners.
- Keep/prune merit judgment is out of scope — that is a charter and usage-ledger question, not a gap question.
- The established-facts discipline applies in both directions: reviewers must not re-litigate what Phase 0 verified, and the report must not claim anything Phase 0, a reviewer's recorded reading, or a verifier did not actually check.
