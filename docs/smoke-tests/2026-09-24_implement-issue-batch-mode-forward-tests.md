# implement-issue batch mode: forward tests (2026-09-24)

Two blind `claude -p` proxies (Opus, `--permission-mode default --allowed-tools ""`, run from the session scratchpad) were given only the new `SKILL.md` and `references/batch-mode.md` text plus a planning scenario, and told to write their plan without running any command. This records what each was asked and what each produced, verbatim. The skill text tested is the one landed by the commit that adds this file.

## What was checked

- Batch path: a plural ask, four `ready-for-agent` issues (one blocked by another in the set), subagent tooling with worktree isolation available, local `main` one commit ahead of `origin/main`. Expected: a batch of three, the blocked one reported as a label contradiction; an independence test naming files per issue; a brief that instructs the implementer to run the skill on one reference, cuts the branch from the recorded tip commit, states the scan conclusion, gives the trailer as a shape, the stop rule, and the status-word report; landing commands with the strictly-ahead count after the rebase; one closeout question marking the pre-batch commit in the push list and showing closing comments in full. Result: all present.
- Fallback path: the same plural ask with no subagent tooling. Expected: the oldest unblocked issue worked alone, the rest named as fresh single-issue invocations, no question about parallelizing, no chaining. Result: all present.

## Batch scenario

# Scenario (planning dry run — do not run any git or gh command; write your plan only)

You are the agent in an attended top-level Claude Code session in repository `/work/acme`, checked out on `main`, clean. `main` is one commit ahead of `origin/main` (that commit is `a1b2c3d docs: annotate issues #12-#14 with triage briefs`). The proving command in AGENTS.md is `uv run python tools/check.py`. The repo's commit trailer convention is `Co-Authored-By: <model name> <noreply@anthropic.com>`. Branch convention is `fix/issue-<n>-<slug>`. The tracker is GitHub Issues with labels `ready-for-agent`, `ready-for-human`, `needs-info`.

You have the Agent tool with `isolation: "worktree"` available. The user says: **"work the ready issues"**.

`gh issue list --label ready-for-agent` returns:
- #12 "CLI: --version prints build date" — body names `src/acme/cli.py` (the `_build_version_string` function) and `tests/test_cli.py`. No blockers. Acceptance: `acme --version` output ends with the ISO date; a test covers it.
- #13 "Driver: reject empty note with typed error" — body names `src/acme/driver.py` (`_read_note`) and `tests/test_driver.py`, section "note handling". No blockers. Acceptance: empty stdin note exits 1 with `NoteError`; test added.
- #14 "Driver: strip BOM from note" — body names `src/acme/driver.py` (`_read_note`) and `tests/test_driver.py`, section "note handling". `Blocked by #13` in the body; #13 is open. Acceptance: BOM removed; test added.
- #15 "Docs: rename 'session' to 'run' in README" — body names `README.md` only. No blockers.

`git log --all --grep '#12'` (and likewise for #13, #14, #15) each return only `a1b2c3d`, the triage annotation commit.

Write, as your answer: (1) which issues form the batch and which are left out, with reasons; (2) the independence test result with the files per issue; (3) the full text of the brief you would give the implementer for #13; (4) the landing steps you will run after the implementers return, as an ordered list of the exact commands; (5) the closeout question you will ask the user, verbatim.

## Batch proxy output

**Plan:** #12, #13, and #15 run as a batch. Each gets its own worktree (a second checkout of the repo in another folder, on its own branch), cut from `a1b2c3d`. #14 is left out because its blocker, #13, is still open. This is a plan only: I ran no git or gh commands.

## 1. Batch and exclusions

| Issue | Batch? | Reason |
|---|---|---|
| #12 | Yes | No blockers. The only commit that mentions it is the triage annotation `a1b2c3d`. |
| #13 | Yes | Same as #12. |
| #15 | Yes | Same as #12. |
| #14 | No: blocked | It says `Blocked by #13`, and #13 is open. |

**#14 carries `ready-for-agent` while its blocker is open, and those two facts contradict each other, so I report the contradiction and do not start #14.** It would also have to wait even with no blocker. Its body depends on #13's change, and it edits the same function (`_read_note`) and the same test section. Once #13 is closed, run #14 on its own as `/implement-issue #14` in a fresh session.

None of the four is a pull request or `ready-for-human`.

The scenario doesn't state the results of these checks. I would run them before dispatch:
- AGENTS.md neither requires a particular worktree lifecycle nor sends landing through pull requests. If it does either, the plan changes.
- `git branch --list '*issue-12*' '*issue-13*' '*issue-15*'` prints nothing. The skill scans branch names as well as commit messages.
- `git show --stat a1b2c3d` shows only triage annotations. Its subject says "#12-#14", yet the scan also matched #15, so I'd read the full commit message.
- `gh issue view <n> --comments` for each issue, plus GitHub's own "blocked by" links, not only the body text.
- `git check-ignore .claude/worktrees` runs if the worktree tool puts worktrees inside the repo. If that folder isn't ignored, the primary checkout would stop reading as clean after dispatch, and I'd raise that with you first.

## 2. Independence test

- **#12:** `src/acme/cli.py` (`_build_version_string`) and `tests/test_cli.py`.
- **#13:** `src/acme/driver.py` (`_read_note`) and `tests/test_driver.py` ("note handling" section). Also the file that defines `NoteError`, if it already exists (`grep -rn "class NoteError" src/`). Also the file that turns errors into exit codes (`grep -rn "SystemExit\|sys.exit" src/acme/`).
- **#15:** `README.md`.
- **Files every change touches:** I expect none. I'd confirm AGENTS.md doesn't require a changelog entry. No issue adds a dependency, so `uv.lock` shouldn't change.

**No pair shares a file, and none depends on another, so all three are independent and no placements need pinning.** One case would change this: if #13's exit-code handling lives in `cli.py`, #13 shares that file with #12. If the two edits sit in separate regions, I pin both placements in both briefs. If I can't tell the regions apart, #13 waits for a later run.

## 3. Brief for #13

Before dispatch:
- Integration branch: `main`, the remote default.
- `git branch --show-current` prints `main`.
- `git status --porcelain` prints nothing.
- `git rev-list --count main..main@{u}` prints `0`. `main` is 1 commit ahead of `origin/main` and 0 behind.
- Recorded tip: `git rev-parse main` gives the full SHA of `a1b2c3d`.

**The worktree tool may start from `origin/main`, which lacks `a1b2c3d`, so the brief names the base commit explicitly.** I'd send three Agent calls in one message, each with `subagent_type: "general-purpose"`, `isolation: "worktree"`, and `name: "issue-12"`/`"issue-13"`/`"issue-15"`. The names let me continue an implementer with SendMessage. No `model` is set, so implementers use the session model.

```
You are implementing exactly one GitHub issue, #13, in the repository whose primary checkout is /work/acme. You start with no context; everything you need is here.

1. Skill. Run the `plan-cycle:implement-issue` skill (/implement-issue) on exactly issue #13. Its Verify, Implement, and Prove rules govern this work. Work #13 as a single issue: do not enter batch mode and do not pick up any other issue.

2. Issue and repo. Fetch the issue with `gh issue view 13 --comments` and read every comment; later comments amend the body. Read /work/acme/AGENTS.md before editing. The proving command is `uv run python tools/check.py`.

3. Branch. You are in an isolated worktree whose starting HEAD may be origin/main, which lacks a commit you need. Do not branch from that HEAD. Before any edit, run inside the worktree:
   git checkout -b fix/issue-13-reject-empty-note <FULL_SHA_OF_a1b2c3d>
   Then confirm `git log -1 --format=%h` prints a1b2c3d.

4. Prior work. The identifier scan is done: there is no prior work for #13. The only commit mentioning it is a1b2c3d ("docs: annotate issues #12-#14 with triage briefs"), a triage annotation, and no local branch name carries 13. Start fresh; do not ask about resuming.

5. Scope. The issue's scope section bounds the work: `_read_note` in src/acme/driver.py and the "note handling" section of tests/test_driver.py. Two sibling issues run at the same time in other worktrees: #12 edits src/acme/cli.py and tests/test_cli.py, and #15 edits README.md. Do not edit those files. Issue #14 (strip a BOM from the note) touches the same function and waits on you; implement no part of it. If making an empty note exit 1 requires editing src/acme/cli.py, stop and report NEEDS_CONTEXT before editing it. If neither the issue nor the code settles where NoteError is defined or how it becomes exit code 1, stop with NEEDS_CONTEXT; do not invent it. Build test-first.

6. Commit trailer. End the commit message with:
   Co-Authored-By: <your model name> <noreply@anthropic.com>
   filling in your own model name.

7. Outside resources. If the proving command needs anything outside this worktree (a fixed port, a local database, a container), do not run it. Stop and report NEEDS_CONTEXT naming the resource; I will answer.

8. Stop rule. When the work is done, make exactly one commit on fix/issue-13-reject-empty-note and leave nothing else modified or untracked (`git status --porcelain` prints nothing). If you stop early, make no commit and give the reason. Do not merge, rebase, push, open a pull request, or comment on, label, or close any issue. Report and stop.

9. Report, in this order:
   - Status: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, or BLOCKED.
   - Branch and commit SHA, and the branch name the worktree started on.
   - Worktree path (absolute).
   - For each acceptance criterion, the command you ran and its output, or "not verified" and why:
     a. An empty stdin note exits 1 with NoteError: run the real CLI with empty stdin and show its stderr and `echo $?`, in addition to the test.
     b. Test added: the test's name and the output of running it alone.
   - The last 20 lines of `uv run python tools/check.py` output, exactly as printed.
   - Each deviation from the issue body, with its reason, or "none".
   - Out-of-scope findings, one sentence each with a file path, or "none".
```

## 4. Landing commands

All commands run in `/work/acme`. Placeholders:
- `<tip>` is the full SHA of `a1b2c3d`.
- `<wt12>`, `<wt13>`, and `<wt15>` are the worktree paths from the reports.
- The branches are `fix/issue-12-version-build-date`, `fix/issue-13-reject-empty-note`, and `fix/issue-15-readme-session-to-run`.

**Step 1: check each branch.** Shown for #12; repeat for #13 and #15. A failed check leaves out only that branch.
```
git merge-base --is-ancestor <tip> fix/issue-12-version-build-date; echo $?   # expect 0
git -C <wt12> status --porcelain                                                # expect no output
git rev-list --count main..fix/issue-12-version-build-date                     # expect 1 (stop rule)
git log -1 --format=%B fix/issue-12-version-build-date                         # trailer present
git diff main...fix/issue-12-version-build-date
```
Then I check the report's claims, especially its deviations, against the diff and the live tree.

**Step 2: check the integration branch.** Any failure stops all landing.
```
git branch --show-current              # expect main
git status --porcelain                 # expect no output
git rev-list --count main..main@{u}    # expect 0
```

**Step 3: land in issue order, #12, then #13, then #15.** None touches a shared file. Shown for #12:
```
git rev-list --count main..fix/issue-12-version-build-date      # record as N
git -C <wt12> rebase main
git rev-list --count main..fix/issue-12-version-build-date      # expect >0 and >= N
git merge --ff-only fix/issue-12-version-build-date
git merge-base --is-ancestor fix/issue-12-version-build-date main; echo $?   # expect 0
```
If a rebase conflicts, I run `resolve-conflicts` with every command inside that branch's worktree.

**Step 4: run the proving command once on the combined result.**
```
uv run python tools/check.py
```
If it fails, I stop, reset nothing, and skip the closeout question. To find the commit that broke it, I rebuild fresh at `<tip>` and then at each landed commit in order:
```
d=$(mktemp -d) && git archive <sha> | tar -x -C "$d" && (cd "$d" && uv run python tools/check.py)
```
Then I report the failing output, the first failing commit, and `<tip>` as the point you could reset to.

## 5. Closeout question (verbatim)

Angle brackets mark values that exist only after the run.

```
All three issues landed on local main, and `uv run python tools/check.py` passed on the combined result (<last output line>). Nothing has been pushed, commented, closed, or removed yet. Please answer each item:

1. Push main to origin/main? It would send these 4 commits (`git log main@{u}..main`):
   - a1b2c3d docs: annotate issues #12-#14 with triage briefs  ← made BEFORE this batch
   - <sha12> <subject>  (#12)
   - <sha13> <subject>  (#13)
   - <sha15> <subject>  (#15)
   Any fix-now commits you approve in item 4 would go in the same push.
   Answer: push / don't push.

2. Close #12, #13, and #15 with these comments? Answer: all / list which / none.
   #12:
   > Implemented in <sha12> on main.
   > - `acme --version` output ends with the ISO date: `<command>` → `<output>`
   > - A test covers it: `<test name>` → `<result>`
   > Deviations: <each with its reason, or "none">.
   #13:
   > Implemented in <sha13> on main.
   > - An empty stdin note exits 1 with NoteError: `<command>` → `<stderr>`, exit 1
   > - Test added: `<test name>` → `<result>`
   > Deviations: <each with its reason, or "none">.
   #15:
   > Implemented in <sha15> on main.
   > - <each acceptance criterion>: `<command>` → `<output>`
   > Deviations: <each with its reason, or "none">.
   No parent issue will be changed.

3. Clean up? I would remove the three implementer worktrees with `git worktree remove <path>` (never --force; if one refuses, I keep it and list its files) and delete the branches the worktree tool created (<names>) with `git branch -d`. The fix/issue-12, -13, and -15 branches stay for your normal branch cleanup.
   Answer: yes / no.

4. Out-of-scope findings (<n>):
   a. <finding> — <path>
   For each one: file it through `triage`, or fix it now as its own commit, proven and landed the same way. Answer per letter.

5. Issues that left the batch: none.

I'll do only what you approve, in this order: fix-now findings, push, issue closures, cleanup.
```

Nothing needed from you. This was a dry run and nothing was executed.

## Fallback scenario

# Scenario (planning dry run — do not run any git or gh command; write your plan only)

You are the agent in an attended session in repository `/work/acme`, checked out on `main`, clean. You have NO subagent tool of any kind and cannot create worktrees for other agents. The proving command in AGENTS.md is `uv run python tools/check.py`. The tracker is GitHub Issues with labels `ready-for-agent`, `ready-for-human`, `needs-info`.

The user says: **"work the ready issues"**.

`gh issue list --label ready-for-agent` returns:
- #12 "CLI: --version prints build date" — names `src/acme/cli.py` and `tests/test_cli.py`. No blockers. Opened 2026-09-20.
- #13 "Driver: reject empty note with typed error" — names `src/acme/driver.py` and `tests/test_driver.py`. No blockers. Opened 2026-09-21.
- #15 "Docs: rename 'session' to 'run' in README" — names `README.md`. No blockers. Opened 2026-09-22.

`git log --all --grep` for each number returns only `a1b2c3d`, the triage annotation commit.

Write, as your answer: (1) what you do with this request — exactly which issue(s) you work in this session and in what order, and what you say about the others; (2) the first three concrete steps you would take.

## Fallback proxy output

**This session works one issue: #12, the oldest unblocked one. #13 and #15 are left for separate sessions.** Batch mode (several issues at once, one helper agent each) is not possible here: it needs subagent tooling that gives each implementer its own worktree, and this session has none. I don't ask whether to parallelize, because the skill says to fall back to a single issue in that case.

## (1) What I do with the request

- **Tracker setup:** GitHub Issues with `ready-for-agent`, `ready-for-human` and `needs-info` counts as configured, so no setup question is needed.
- **Candidates:** #12, #13 and #15 all carry `ready-for-agent`, none has blockers, and none is `ready-for-human`.
- **Pick:** #12, "CLI: --version prints build date". It was opened 2026-09-20, the oldest of the three.
- **Prior work:** the commit search found only `a1b2c3d`, the triage annotation, for every issue. That is not prior implementation work, so there is no resume-or-fresh question.
- **What I tell the user:**
  - "I'm working #12 only in this session. This session has no subagents, so the ready issues can't run as a batch."
  - "#13 (Driver: reject empty note with typed error) and #15 (Docs: rename 'session' to 'run' in README) are also ready and unblocked. Run each one separately in a fresh session: `implement #13`, then `implement #15`."
- **Order:** #12 only. When #12 is done, I stop. I don't start #13, even if #12 went quickly.

## (2) First three steps

1. **Read the contract and check blockers.**
   - Read AGENTS.md for the branch naming convention and the proving command, `uv run python tools/check.py`.
   - Run `gh issue view 12 --comments` to get the full body, the acceptance criteria, any agent brief, and comments that change the body.
   - Confirm blockers are closed in two places: native issue dependencies, and any `Blocked by` text.
   - If the scope is under-specified, I stop and suggest the `needs-info` label.
2. **Finish the prior-work check and create a working branch.**
   - The commit search covered commit messages only. The skill also asks about branch names, so I run `git branch --list '*12*'`.
   - If that finds nothing, I create a working branch from clean `main` using the repo's naming convention, for example `git checkout -b issue-12-version-build-date`. I never work directly on `main`.
3. **Write the failing test first.**
   - Following `/tdd`, add a test to `tests/test_cli.py` for each acceptance criterion about `--version` printing the build date.
   - Run `uv run python tools/check.py` and read the output to confirm the test fails for the expected reason.
   - Only after that, change `src/acme/cli.py`.

After the code is written, I check each acceptance criterion against real command output. The report lists the evidence per criterion, deviations from the issue, and any out-of-scope findings. Before posting, I show the user the closing comment I would put on #12 and wait for approval. I don't merge or push; landing is handled by a separate workflow.

Nothing needed from you.
