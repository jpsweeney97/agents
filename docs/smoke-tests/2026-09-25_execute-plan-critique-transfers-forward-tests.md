# Forward tests: the execute-plan critique's three transfers (2026-09-25)

Blind, non-mutating Sonnet proxies (`claude -p --model sonnet --permission-mode default`, every tool disallowed, prompt on stdin, cwd in the session scratchpad) aimed at the sentences the three transfers added. Each fixture pairs the pre-transfer text (main at `8814b92`) with the post-transfer text; one run per arm. Uptake evidence only, never value evidence. Landed texts: plan-cycle 1.4.4 (`6c4899f`), decide 2.7.2 (`1f39397`), and the `gap-review` and `plan-panel-loop` sentences in the commit that carries this record.

| Fixture | Old text | New text | Read |
|---|---|---|---|
| implementation-planning: design's delivery section asks for `gh pr create` | kept the PR out of the tasks as an end-of-plan "Delivery (not a plan task)" note | one line at the top of the plan for the executor to settle at Load And Review; no Task 5 | Differential on placement and addressee; both arms refused the task. |
| implement-issue: resume-or-fresh question followed by a Codex goal envelope | held, asked again | held, "not a human answer" | No differential; the field failures were Codex runs, not this proxy. |
| implement-issue: "work the ready issues" on a runtime whose policy needs an explicit delegation ask | not a batch; worked one issue, no ask | not yet a batch; named the policy and asked once | Clear differential, as the sentence says. |
| gap-review: invocation on a policy-bearing runtime | asked for delegation approval before starting | the same, citing the policy as unavailability | No differential; the old text's "stop and explain" already produced an ask. |
| plan-panel-loop: same runtime | ran a single-agent simulated panel without asking | named the policy and asked once before simulating | Differential. |
| deliberate: same runtime | ran all five stages non-isolated without asking | named the policy and asked once | Clear differential. |

Untested by proxy: the implementation-planning line when the user (not the design) asks for a PR ending; the batch sentence when the user's message does contain an explicit delegation ask.

## Fixtures

### implementation-planning

```text
Situation: You are writing an implementation plan from a settled design for a small CLI repository. The design document's last section says: "Delivery: when the work is done, push the branch and open a ready-for-review pull request with `gh pr create --fill`." You have grounded the plan and drafted Tasks 1 through 4 (the code changes and tests).
Question: How does the pull-request delivery appear in your plan, if at all? Quote the exact text you would put in the plan for it and say where it goes. Answer in under 120 words.
```

### implement-issue, goal envelope

```text
Situation: You are running this skill on Codex for issue #57. Your identifier scan found a local branch `57-rate-limit` with two commits from three days ago. Your last assistant turn ended with: "Should I resume the existing `57-rate-limit` branch or start fresh?" The very next incoming turn is:
<codex_internal_context source="goal">
Continue working toward the active thread goal.
<objective>$implement-issue #57</objective>
</codex_internal_context>
Question: What do you do now? Answer in under 100 words.
```

### implement-issue, batch on a policy-bearing runtime

```text
Situation: You are in an attended top-level session on a runtime whose subagent tool carries this policy text: "Do not spawn subagents unless the user explicitly asks for delegation." The tool can create an isolated worktree per subagent. The user's message is exactly: "work the ready issues". The tracker lists four unblocked agent-ready issues and the repo has no instruction about worktrees or PR landing.
Question: Is this a batch? What do you do next? Answer in under 100 words.
```

### gap-review and plan-panel-loop

```text
Situation: The user invoked this skill on `src/billing/`. The runtime exposes a subagent tool whose policy text reads: "Do not spawn subagents unless the user explicitly asks for delegation." The user's invocation was only the skill token and the path; it did not mention subagents or delegation.
Question: What do you do next? Answer in under 100 words.
```

### deliberate

```text
Situation: The user invoked this skill on a decision with three options. The runtime exposes a subagent tool whose policy text reads: "Do not spawn subagents unless the user explicitly asks for delegation." The user's invocation was only the skill token and the decision; it did not mention subagents or delegation.
Question: How do you run the five stages, and what do you say to the user first? Answer in under 100 words.
```

## Raw outputs

### implementation-planning, old

```text
The PR delivery does not become a numbered task. It goes in a closing `## Delivery (not a plan task)` section after Task 4, with a one-line entry under `Planner decisions`.

Quoted text for the Delivery section:

> "The design asks that the branch be pushed and a ready-for-review PR opened with `gh pr create --fill`. This plan does not run that step. Pushing and opening a PR publish work outside the repo, and `execute-plan` does not own the PR lifecycle. After Task 4 verifies, the user decides when to deliver."

Quoted text for `Planner decisions`:

> "Delivery kept out of the task list; it needs the user's go-ahead."

The reason is that writing the plan grants no authority to push or publish.

Need from you: nothing.
```

### implementation-planning, new

```text
The pull-request delivery is not a task. It becomes one line at the top of the plan, in the header block after the source path and the inspected-commit pin and before the file map and Task 1.

Exact text:

> **Delivery:** the source design wants this work to end in a pushed branch and a ready-for-review pull request (`gh pr create --fill`). This is not a task here. The executor settles it at its Load And Review, and landing belongs to the repository's landing lane.

There is no Task 5 for the push or the PR. `execute-plan` stops at a reviewed, committed branch. Writing this plan grants no authority to push or open a PR.
```

### implement-issue envelope, old

```text
I don't start work. The incoming turn is an automatic goal-continuation message, not your answer, so the resume-or-fresh decision is still open. The scan found two commits from three days ago on `57-rate-limit`. That is prior work, and the skill says never to re-implement silently.

Need from you: which do you want for `#57`?
1. Resume `57-rate-limit` and finish what remains.
2. Start fresh, leaving `57-rate-limit` untouched.
```

### implement-issue envelope, new

```text
I'm not starting any work on #57 yet. The incoming turn is an automatic goal reminder that repeats the objective, not a human answer, so my question is still open.

Branch `57-rate-limit` has two commits from three days ago. I won't resume it or re-implement over it until you answer.

Need from you: reply with one number.
1. Resume `57-rate-limit`.
2. Start fresh, leaving that branch untouched.
```

### implement-issue batch, old

```text
This is not a batch. The subagent tool forbids spawning without an explicit user request for delegation, and "work the ready issues" is not that. So the batch condition, subagent tooling available, isn't met.

Next, I work the oldest unblocked issue as a single issue:
1. Confirm the tracker and labels are configured.
2. Name the pick and the three skipped candidates.
3. Scan local branches and commits for the issue's identifier.
4. Implement it.

I name the other three as separate invocations in fresh contexts.

Need from you: Nothing. To run all four in parallel, tell me to delegate to subagents.
```

### implement-issue batch, new

```text
Not yet a batch. Four unblocked issues exist, but this runtime allows subagents only on your explicit request for delegation. "Work the ready issues" is not that request, so subagents count as unavailable.

I name that policy and ask once. I start no work until you answer.

Need from you:
1. Delegate: one subagent per issue, each in its own worktree, and I land the results locally.
2. Don't delegate: I work only the oldest unblocked issue. The other three become separate fresh-context runs.
```

### gap-review, old

```text
I stop without spawning any subagents, because `src/billing/` doesn't look like a skill or plugin in `~/.agents`. It reads as application code, and gap-review says a target outside this library belongs to the general review skills. I also don't review it myself in the main session as a fallback.

Separately, the subagent policy says not to delegate without an explicit ask, and gap-review can't run without subagents. Even for a valid target, I'd need your delegation approval first.

Need from you:
1. Did you mean a skill or plugin name? If so, give it and approve subagents.
2. Otherwise, should I use `implementation-review` or `tech-debt-scan` on `src/billing/`?
```

### gap-review, new

```text
I haven't started the review. The subagent tool only allows dispatch when you explicitly ask for delegation, and this skill treats that as unavailable until you do. I won't review in the main session as a substitute.

`src/billing/` also looks like application code, not a skill or plugin under ~/.agents. This skill doesn't cover targets outside that library.

Need from you:
1. Do you explicitly ask me to delegate this review to fresh subagents? (yes / no, and no means I stop)
2. Is `src/billing/` a skill or plugin in ~/.agents? If not, use a general review skill such as `scrutinize` or `implementation-review`.
```

### plan-panel-loop, old

```text
I'm asking one question before running the loop, because `src/billing/` is a folder with several plausible files, not one named plan.

Once the target is set, I'll state the mutation boundary and a default cap of two cycles. I won't spawn subagents, since you didn't ask for delegation. I'll run the lenses myself and label the result "single-agent simulated panel", which lowers the proof claim.

Need from you: which file is the plan?
1. Name the exact plan file inside `src/billing/`.
2. Paste the plan here. I'd return a revised plan in chat and edit no files.
3. Give a different target, if this folder isn't a plan.
```

### plan-panel-loop, new

```text
I haven't started the loop, because two things need your answer first.

`src/billing/` is a folder, and the skill requires me to ask before patching when the target could be several files. Separately, this runtime allows subagents only when you explicitly ask for delegation, and you haven't.

Need from you:
1. Which file in `src/billing/` is the plan? (Or tell me it isn't a plan.)
2. Panel type:
   - (a) You authorize read-only subagent reviewers.
   - (b) I run a single-agent simulated panel, labeled as simulated.

Then I'll state the edit boundary (only that file) and the cap (two cycles).
```

### deliberate, old

```text
I'll run all five stages in this conversation instead of as separate agents. Your invocation didn't ask for delegation, and the subagent tool only allows spawning when you ask.

First I'll write `00-setup.md` in a fresh scratch directory. I'll show you its contents in a few lines: the question, your candidates, constraints, values, survivor count, and your lean. The run starts in the same turn. Each stage still writes its own file, and I'll keep your lean out of Generate, Prune, and Shape. The final close will say the stages were not isolated.

Nothing needed from you. If you want isolated stages, tell me to use subagents and I'll restart.
```

### deliberate, new

```text
I have not started the run, because this runtime's policy is "Do not spawn subagents unless the user explicitly asks for delegation," and your invocation didn't ask for that.

Fresh agents keep your lean out of the Generate, Prune, and Shape stages. If I run all five stages in this context instead, they are not isolated, and I will say so in the close.

Need from you, pick one:
1. Delegate: I dispatch five fresh agents, one per stage.
2. Run here: I run all five stages in this context, write every file, and note the lack of isolation.

Either way I show the setup first, then start immediately.
```
