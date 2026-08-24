# Review Prompts

Drafts to re-derive from when writing the Workflow script, not text to paste unexamined. The finding taxonomy and the non-goal rule travel verbatim; file lists, established facts, and non-goal lists are filled per target. Provenance: distilled from the handoff 3.3.0 gap review, 2026-08-23 (`plugins/handoff/CHANGELOG.md`, commit `4e7b5f9`) — 11 findings raw, 11 confirmed after refute-default verification, several by empirical reproduction.

## Reviewer context block

Prepend to every dimension prompt:

```text
You are reviewing <target> at <absolute path> — <one line on what it is>. Read the actual
files; do not work from this summary alone.

FILES (read all that your dimension needs): <every file, absolute paths>

ESTABLISHED FACTS (already verified, do not re-check, do not report as findings):
<validation results, delivery equality, canary status, live artifact numbers>

JUDGING FRAME (from the repo's AGENTS.md — apply it):
- Trust skills are judged on reliable execution and single-sourced machinery; judgment
  skills on whether structure protects thinking rather than doing it for the agent
  (see agent-facing-design, Two Kinds of Skill). Apply the bar per part for mixed targets.
- The target's documented non-goals are: <list them from its Boundaries sections AND its
  frontmatter description exclusions — the Do-not-use clauses; some surfaces carry only
  the latter>. A finding that merely re-proposes a documented non-goal is INVALID —
  unless you argue with evidence that the boundary itself is wrong.
- Classify every finding: (a) gap — behavior a future session needs and no surface
  provides; (b) contract-defect — surfaces disagree, or an algorithm as written
  misbehaves on a reachable input; (c) boundary-challenge — a deliberate boundary you
  believe is mis-drawn, argued from evidence.
- Report only findings you would defend under adversarial scrutiny. No filler; an empty
  list is an acceptable answer.
- In files_read, list every file you actually read in full — it is the coverage record
  the final report's "clean" claims rest on; never list a file you only skimmed.
```

## Verifier prompt

One per deduped finding:

```text
You are an adversarial verifier for one review finding against <target>. Your job is to
REFUTE it. Read the actual files it cites (and any surface it depends on) before judging.
Default to isReal=false when the finding: re-proposes a documented non-goal without
arguing the boundary is wrong (the non-goals are: <list>); describes an unreachable or
fabricated input; misreads the text (quote the text that refutes it); or is a taste-level
nitpick with no behavioral consequence. Reproduce the failure empirically when practical,
and set reproduced=true only when you actually ran the failing thing and watched it fail.
Confirm isReal=true only when the defect or gap is real, reachable, and would matter to a
future session or maintainer. Re-grade severity honestly (high = wrong behavior or lost
data in realistic use; medium = a session wastes real time or a maintainer is misled;
low = polish). Put any partial correction to the finding's mechanism in the correction
field, even when confirming; leave it empty when there is none.

FINDING [dimension] [class] [claimed severity]: <title / file / detail / evidence /
proposed fix>

Context facts you may rely on without re-checking: <established facts>.
```

## Schemas

Findings (per reviewer, via the Workflow `schema` option). `files_read` is the coverage record behind the report's "clean" claims:

```json
{"files_read": ["..."],
 "findings": [{"title": "...", "severity": "high|medium|low",
  "class": "gap|contract-defect|boundary-challenge",
  "file": "...", "detail": "...", "evidence": "...", "proposed_fix": "..."}]}
```

Verdict (per verifier). `reproduced` feeds the report's evidence labels; `correction` records a mechanism repair, empty when none:

```json
{"isReal": true, "reason": "...", "adjusted_severity": "high|medium|low|n/a",
 "reproduced": false, "correction": ""}
```

## Workflow shape notes

- Dedup across dimensions is the one justified barrier; verification fans out per finding after it.
- Scale to the target: the pilot (a four-skill plugin, nine surfaces) took 4 reviewers + 11 verifiers. A single-skill target warrants fewer dimensions and a smaller fleet.
- Reviewers and verifiers are judgment stages: inherit the session model per the global dispatch rule.
