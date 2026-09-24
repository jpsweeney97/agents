Here are the tradeoffs for all three options. This comes from how git worktrees work, and I haven't looked at your setup.

One correction to my last message: a worktree holds the whole repo, not one skill. If all your skills live in one repo, a hundred worktrees means a hundred full copies of every skill, unless you use sparse checkout (checking out only chosen folders).

| | Permanent worktree per skill | Throwaway worktree | Branches in one checkout |
|---|---|---|---|
| 1. Live skills untouched while editing | Yes. They change only when you merge to main | Yes, same | No, if this checkout serves live skills. Every switch or edit changes what's live |
| 2. Two skills open at once | Yes (a branch can be in only one folder) | Yes, same | No. One branch at a time, so you stash or switch |
| 3. Two sessions or agents editing at once | Safe, separate folders | Safe | They clash, because they share one set of files |
| 4. Finding your work later | Best. One fixed path per skill | Weak. New path each time, found with `git worktree list` | The branch name only. You switch to see it |
| 5. Staying current with main | You update each one, so up to a hundred can fall behind | Always fresh, made from current main | One update covers everything |
| 6. Cost to start an edit | None after a one-time setup of about a hundred | Seconds, every time | Seconds (one switch) |
| 7. Disk and folder count | Highest | Low | Lowest |
| 8. Unfinished work | Safe for weeks, but easy to forget | Lost if you remove the folder with uncommitted changes. Forgotten ones quietly become permanent | Stays in place, mixed with your other in-progress edits |
| 9. Tools that scan folders for skills | May find duplicate copies of every skill (worth checking) | Same, while the folders exist | No risk |
| 10. Cleanup | `git worktree prune` after moving or deleting folders. Reset each branch after merge | Remove each folder after merge | Delete merged branches |

**Rows 1–3 speak to "safe editing," row 4 speaks to "a home I can find," and rows 5–10 are what each option costs to run.** This table is my draft, not settled. I haven't ranked anything, because the ranking depends on which want is real.

Still open from my last message: your answer on the weekly sync chore. It only matters for permanent worktrees.

Need from you:
1. Which want is closer?
   1. Safe editing.
   2. A findable home per skill.
   3. Both, and I can't split them.
2. Is the checkout that serves your live skills the same one you edit in today? It decides whether option 3 protects live skills at all.
   1. Yes.
   2. No.
   3. Not sure.
