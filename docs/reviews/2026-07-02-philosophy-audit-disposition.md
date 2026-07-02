---
type: disposition
date: 2026-07-02
adjudicates: >-
  docs/reviews/2026-07-02-agent-facing-design-philosophy-audit.md
  (reviewed_commit 09d2b9c; 53-item ledger; 328-agent multi-agent audit)
status: >-
  Closed. The audit is adjudicated history: nothing in it carries a standing
  mandate beyond what this disposition explicitly accepts. Future sessions
  treat its unaccepted recommendations as parked or rejected, never as an
  outstanding to-do list.
---

# Philosophy Audit Disposition (2026-07-02)

JP approved the same-day recommendation from the critical read of the audit: adopt its few independently verified findings as small diffs, decline its program, and pivot the repo's next effort from text-grading to behavioral evidence.

## Basis

- The critical read (same session): the audit's verdict apparatus contained no deletion outcome (0 cuts in 53 items; the verdict legend lacks CUT entirely), 30 of 53 rewrites share one template (append blast-radius scaling plus a carve-out), the rewrites systematically trade bright-line robustness for self-scored conditionals the corpus's own reasoning distrusts (M2/M22/M30), its two critics and honesty appendix name a circularity the synthesis never acts on, and the synthesis carries craftsmanship defects (leaked tool-call XML in M37/M48; 9-vs-10 KEEP and 27-vs-30 REWRITE count inconsistencies). The evidence base is text-only: roughly 15–20 of ~76 skills read, no behavioral incident cited, and the one corpus claim checked during the audit itself (M43) was found overstated.
- Spot-verified before acting: the auto-commit contradiction is real (`grill-with-docs` SKILL.md:94 and `improve-codebase-architecture` SKILL.md:85 vs the global CLAUDE.md auto-commit rule); the charter's third-party rationale is deliberate, not accidental (`charter.md` Reversibility Class — "authorship coherence (Thesis), not reversibility"); the verdict partition is live practiced law (red-team's explicit no-verdict contract; outcome-check/closeout-check/deploy-plan each render exactly one).

## Accepted — landed with this disposition

- **M4 capability carve-out** (the audit's one finding grounded in verified environment capability rather than text-on-text): the build-and-prune exemption reads on capability, not packaging. A skill that can fire unattended (cron, remote trigger, subagent dispatch no human reads at call time) or wields irreversible-effect tools (send, merge, force-push, delete) fails the Reversibility Class lens's own premises — visible fire, clean prune — and is charter-gated. Landed: `docs/agents/charter.md` (intro enumeration + Reversibility Class), synced to `AGENTS.md` (Repo Docs bullet) and global `~/.claude/CLAUDE.md` (Behavior Contracts), since the charter requires every routing surface to name the gated events.
- **Auto-commit reconciliation**: a governing skill's explicit instruction about its own writes overrides the Markdown auto-commit default. Landed: global `~/.claude/CLAUDE.md` (Working).
- **M31 merge**: Admission's house-standards bullet now also asks "does it say plainly what an agent who encounters it must do?". Landed: `docs/agents/charter.md` (Admission).
- **Library conventions written down** (from the audit's espoused-vs-in-use findings, recorded as practiced — without M47/M49's proposed machinery: no mandatory residual-risk field, no co-sign tiers): the verdict partition and the close packet, each with its exemptions. Landed: `skills/agent-facing-design/SKILL.md` (Library Conventions).
- **Idempotency on resume** (from `principlesToAdd`, in lighter non-machinery form): one sentence each in `skills/execute-plan/SKILL.md` (Pace And Stops) and `skills/migration-campaign/SKILL.md` (§5).

## Rejected

- **M6/M7 third-party rewrite** (re-derive third-party gating from the reversibility axis; waive gating for scope-local third-party material "not swept in merely by origin"): rejected as a downgrade. Provenance/authorship is the correct axis for third-party contract risk — a third-party skill is trusted instruction text wherever it fires; trashing its directory undoes neither the sessions it steered nor the actions it persuaded an agent into, and the M4 capability test does not cover persuasion. The charter's third-party clause stands as written. Any future reopen moves toward tighter provenance gating, not looser.
- **The two structural rebuilds** (`agent-facing-design`, `writing-principles`): single-pass, same-frame, text-only evidence does not justify rebuilding the two core gate skills. Corrections land incrementally when evidenced; revisit a rebuild only if accumulated accepted edits leave either skill reading quilted.

## Parked — reopen triggers

- The remaining REWRITE/GROUND M-items: reopen per-item when a transcript shows the specific misfire that item predicts; adopt singly, never as a batch restyling of the corpus.
- The ten `principlesToAdd` machinery items (single-sourcing scans, nearest-neighbor collision detectors, scheduled bloat audits, falsification channels, circularity-escape gates, independent-verification admission, interface contracts, baseline-comparison rule, and kin): each reopens only as its own charter admission on observed friction matching it. The idempotency and auto-commit items from that list were accepted above in lighter, non-machinery form.

## Posture — recorded intent, deliberately not contract text

- Ambient and meta instruction surfaces stay net-zero-or-shrinking absent a transcript-cited incident; writing this posture into an always-loaded surface would itself be the accretion it guards against, so it lives here as recorded intent only.
- No further corpus-scale text-vs-text self-audits until the behavioral loop yields data worth auditing; large token spends go to transcripts, the skill-usage ledger, and `skill-benchmark` runs.
- The prune tranche is already governed by the 2026-07-02 skill-usage ledger entry (first read: 36/76 skills ever fired; re-read committed for 2026-08-01 before any tranche). This disposition adds nothing to and changes nothing about that commitment.
