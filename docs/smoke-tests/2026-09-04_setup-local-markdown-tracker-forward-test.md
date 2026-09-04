# 2026-09-04 — `setup-matt-pocock-skills`: Local Markdown tracker protocol forward test

Behavior evidence for the completed Local Markdown tracker seed (`skills-claude/setup-matt-pocock-skills/issue-tracker-local.md`) and the category-role rows added to its `triage-labels.md` seed. The defect (Plan Cycle gap review F14, setup-skill half; D7 in the 2026-09-04 repair commission): the seed defined only paths, one `Status:` line, create, read, and comment append, while the Plan Cycle README requires a configured tracker to support create, read with comments, comment, apply and remove role labels (one category role plus one state role), close, list by role, and a blocker-closed test. Athena KB (`/Users/jp/athena-kb-local/docs/agents/issue-tracker.md`, 57 issues) had already evolved `Category:` lines, a `closed` lifecycle state, and relative links in live use; the new seed codifies that observed shape.

Method: three headless runs, `claude -p --model sonnet --allowed-tools "Read,Edit,Write,Glob,Grep,Bash(grep:*),Bash(ls:*),Bash(cat:*)" --output-format text`, prompt piped on stdin, each run in its own fixture repo under the session scratchpad so no repo instructions load, one fresh session per run. The fixture: a `.scratch/demo/` tracker with a PRD at `needs-triage` and five issues: 01 `closed`; 02 `ready-for-agent`, created 2026-09-01, blocked by 01; 03 `ready-for-agent`, created 2026-08-30, blocked by 04; 04 `wontfix`; 05 with no `Status:` line. The arms differ only in the seed text placed at `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`: `old` is the text on `main` at `63dfd45`; `new` is the first draft; `new2` is the landed text, which adds three definitions the `new` run reported as undefined (PRDs included in listing, the `<who>` field of a comment heading, path as the final ordering tie-break). The prompt, verbatim below, asked for the next ready issue with a blocker check, the unlabeled issues, and a quick state override (apply `bug` and `needs-info` to issue 05, post a triage comment, read the item back), and told the proxy to report anything the two files left undefined instead of inventing a rule.

## Result

| Arm | Text | Oldest-first rule | 03's `wontfix` blocker | Pick | Unlabeled | Category applied to 05 | State applied to 05 | Comment shape | Undefined items reported |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| old | `main` at `63dfd45` | none defined; flagged | "not `closed`"; semantics flagged | 02 | 05 | no: "no category role concept defined" | yes | copied from neighbouring files; flagged | 6 |
| new | first draft | `Created:` line | contradiction, per the text | 02 | 05 | yes | yes | dated heading, disclaimer first | 3 |
| new2 | landed | `Created:` line | contradiction, per the text | 02 | 05 | yes | yes | dated heading, disclaimer first | 3, none tracker-owned |

Observed behavior: the old arm reproduced F14. It declined to apply a category role because the old text defines none, and it named ordering, blocker semantics, `closed`, "unlabeled", the `Category:` field, and the comment sub-format as undefined. Both new arms performed all three tasks from the text alone and produced byte-identical edits to issue 05: two header lines added in the specified order, one dated comment appended with the disclaimer as its first line, read-back confirming one category and one state. The three items `new2` still reported as undefined are not the tracker's to define: fall-through selection when a ready issue is blocked (`implement-issue` owns it: pick the oldest unblocked), whether triage backfills the issue template on a bare bug report (`triage` owns it), and which `<who>` value a maintainer-instructed comment takes (the run chose `triage`, matching the text).

Why: a local Markdown tracker has no CLI to define its operations, so the contract text is the whole protocol. The old seed left the operations Plan Cycle names to inference, and a proxy told not to invent conventions stopped at exactly those points. The landed text defines each operation as a file operation, so the same proxy under the same instruction completed them.

## Structural checks

`quick_validate.py` on the skill directory (only the accepted `disable-model-invocation` complaint); YAML parse of `agents/openai.yaml`; frontmatter parse of `SKILL.md`; `git diff --check`; all five seed paths referenced from `SKILL.md` exist. Verified on the tip of `fix/setup-local-markdown-tracker`, the commit that carries this record.

## Proof boundary

One run per arm on one model family (Sonnet) and one fixture: each rule was followed once, not measured for reliability. The fixture's `wontfix` blocker led every arm to pick issue 02, so the pick alone does not separate the arms; the category role, the ordering rule, and the undefined-items count do. No run exercised `to-prd` or `to-issues` publishing into the local tracker, the resumed-run duplicate check, or the reporter-activity rule. The setup skill's new Section A follow-up (commit `.scratch/` or git-ignore it) was not exercised; it is a user-facing question inside a `disable-model-invocation` skill.

## Durable artifact

This record. The fixture is reproducible from the description above and the prompt below; the scratchpad copies are not preserved.

## Prompt, verbatim

```text
You are acting as the tracker layer for the `implement-issue` and `triage` skills in this repository. The issue tracker and triage label vocabulary are configured in `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`; read both first and follow them exactly. Do not guess conventions that those files do not state; where they leave something undefined, say so explicitly instead of inventing a rule.

Perform these three tasks and report each result under its own heading:

1. NEXT READY ISSUE. List every issue carrying the agent-ready triage role, oldest first as the tracker defines "oldest". For each, state whether all of its blockers are closed, citing the blocker's recorded state. Then name which one you would pick as "the next ready issue", or say why none is pickable.

2. UNLABELED. Name every issue that has never been triaged, as the tracker defines that.

3. QUICK STATE OVERRIDE. The maintainer says: "move issue 05 to needs-info, it's a bug". Apply the category role and the state role to issue 05 exactly as the tracker defines applying a label, then post a triage comment on it whose body is: "Needs the CI job name and a failing run link." This comment is generated during triage. Then read the item back and confirm it carries exactly one category role and one state role. Report the exact file edits you made.

End with a section "UNDEFINED" listing anything the two config files did not define that you needed.
```
