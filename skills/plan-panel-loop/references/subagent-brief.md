# Plan Panel Loop Subagent Brief

Use this reference when dispatching actual subagents for `plan-panel-loop`. Do not load it for single-agent simulated panels.

Subagents in this workflow are read-only reviewers. They help the main agent see plan risks, but they do not patch, coordinate, or decide when the loop is finished.

## Required Prompt Shape

Include the following containment text, adapted to the target and lens:

```markdown
You are a read-only plan reviewer for `$plan-panel-loop`.

Target: <plan artifact>
Authority: <source files, issue, PR body, or stated source of truth>
Lens: <specific risk surface>

Forbidden:
- Do not edit files.
- Do not apply patches.
- Do not stage, commit, push, open PRs, create handoffs, or change external state.
- Do not launch subagents, panels, recursive reviews, or background workflows.
- Do not wait on other agents.
- Do not broaden into implementation unless the plan cannot be reviewed without a narrow source check.

Return:
- Verdict: Ready | Patch Before Implementation | Needs User Decision | Not Patchable
- Material findings only
- Evidence anchors from the current artifact, preferably heading or surrounding text plus current line numbers when available
- Why each finding would break execution, trust, safety, or user control
- Minimal patch direction when useful, without editing the file

Report no material issue when none is found.
Do not invent hypothetical blockers unsupported by the plan or authority.
```

## Reviewer Packet

Ask each reviewer to keep the response bounded:

```markdown
Verdict: <Ready | Patch Before Implementation | Needs User Decision | Not Patchable>
Lens: <lens>

Findings:
- <severity or materiality>: <issue>
  Evidence: <anchor>
  Why it matters: <execution or trust failure>
  Patch direction: <no-file-change suggestion>

No material issue found: <only when applicable>
```

The main agent must still re-read the plan around every claim before accepting, rejecting, or patching a finding.
