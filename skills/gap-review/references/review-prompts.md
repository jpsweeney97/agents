# Review Prompts

Compose each brief from these instructions and the actual target. The finding taxonomy and documented-non-goal rule travel verbatim; the paths, facts, scope, and assigned result file are filled from the current run. These prompts work with native subagents on either runtime.

Provenance: the original method came from the handoff 3.3.0 gap review of 2026-08-23, recorded in plugins/handoff/CHANGELOG.md at commit 4e7b5f9. Its historical outcomes are not evidence about the current target.

## Reviewer brief

Give each reviewer the resolved target and absolute file paths; its assigned dimension; checked facts with commands and observed results; unchecked items; the judging rules below; and an absolute path for its review-NN.json file.

Tell it to read the files its dimension needs, make no target edits, spawn no agents, write only its assigned result file, and return that path. Do not provide another reviewer's conclusions.

Carry this judging block verbatim, filling only the target's documented non-goals:

~~~text
Trust skills are judged on reliable execution and single-sourced machinery; judgment skills on whether structure protects thinking rather than doing it for the agent. Apply the bar per part for mixed targets.

The target's documented non-goals are: <list them from its Boundaries sections AND its frontmatter description exclusions — the Do-not-use clauses; some surfaces carry only the latter>. A finding that merely re-proposes a documented non-goal is INVALID — unless you argue with evidence that the boundary itself is wrong.

Classify every finding: (a) gap — behavior a future session needs and no surface provides; (b) contract-defect — surfaces disagree, or an algorithm as written misbehaves on a reachable input; (c) boundary-challenge — a deliberate boundary you believe is mis-drawn, argued from evidence.

Report only findings you would defend under adversarial scrutiny. No filler; an empty list is an acceptable answer.

In files_read, list every file you actually read in full. Never list a file you only skimmed. Established facts cover only their stated checks, not conclusions that those checks cannot establish.
~~~

## Verifier brief

Give each verifier one deduplicated candidate, its cited source paths and necessary dependencies, the target's non-goals, relevant checked facts, its absolute verify-NN.json output path, and a separate temporary reproduction directory. Require a fresh context, no delegation, no target edits, and no access to other verifiers' conclusions.

Carry the same non-goal rule and taxonomy as in the reviewer judging block, then state:

~~~text
Your job is to REFUTE this finding. Read the actual files it cites and any file it depends on before judging.

Refute when the finding re-proposes a documented non-goal without evidence that the boundary is wrong, describes an unreachable or fabricated input, misreads the text, or is a taste preference with no behavioral consequence. Quote the source that refutes it.

Confirm only when the defect or gap is real, reachable, and matters to a future session or maintainer. Re-grade severity honestly: high means wrong behavior or lost data in realistic use; medium means a session wastes real time or a maintainer is misled; low means polish.

Reproduce empirically when practical. Use read-only commands or a temporary copy, preserve the reviewed source, and record the command and observed failure in reason. Set reproduced=true only when that execution demonstrates this finding's claimed consequence. A related check does not suffice: executing a program's valid rejection does not demonstrate a routing failure, and inspecting an omission does not execute its claimed effect on a future agent. If source reasoning confirms the finding without observing that consequence, use reproduced=false and state what remains untested.

Put any correction to the finding's mechanism in correction even when confirming it; use an empty string only when there is none. Missing access or inconclusive evidence is unfinished verification: report the obstacle rather than inventing a boolean verdict.

Write the judgment to the assigned JSON result file without a Markdown fence, and return its absolute path. Any reproduction files stay in your assigned temporary reproduction directory; change nothing else.
~~~

## Reviewer JSON

The result is an object with files_read, an array of absolute path strings, and findings, an array of finding objects. A successful empty review has findings equal to an empty array.

Each finding has string fields title, severity, class, file, detail, evidence, and proposed_fix. Severity is high, medium, or low. Class is gap, contract-defect, or boundary-challenge. File names the relevant absolute path. Evidence names the observed source text or executed check, not just the conclusion.

~~~json
{
  "files_read": ["/absolute/source/SKILL.md"],
  "findings": [
    {
      "title": "Short finding title",
      "severity": "medium",
      "class": "contract-defect",
      "file": "/absolute/source/SKILL.md",
      "detail": "The reachable input and resulting wrong behavior.",
      "evidence": "The source text or command and observed result.",
      "proposed_fix": "The smallest proposed correction."
    }
  ]
}
~~~

## Verifier JSON

The result is an object with boolean isReal and reproduced fields and string reason, adjusted_severity, and correction fields. A confirmed finding uses high, medium, or low for adjusted_severity. A refuted finding uses n/a and reproduced=false. A confirmation by reasoning uses reproduced=false.

~~~json
{
  "isReal": true,
  "reason": "Source evidence, plus command and observed failure when reproduced.",
  "adjusted_severity": "medium",
  "reproduced": false,
  "correction": ""
}
~~~

These are ordinary JSON contracts, not a dependency on a provider's schema option. The coordinator parses the files and checks required keys, types, allowed values, and the conditional rules above. Every selected reviewer result must pass before deduplication or verifier dispatch; a check performed only before the final report is too late. Extra fields cannot replace required evidence. A string such as "false" is not a boolean; an absent findings field is not an empty array; a missing verification file is neither a confirmation nor a refutation.

The coordinator may ask the originating agent to repair malformed output but must not manufacture evidence, complete a judgment, or change a verdict to make it parse. Unresolved results follow the incomplete-report instructions in SKILL.md.
