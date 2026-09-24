Here are the tradeoffs side by side. They come from what you've told me, not from your repo, so treat them as rough.

| | Permanent worktree per skill | Throwaway worktree per edit | Branches in the one checkout |
|---|---|---|---|
| Live skills stay safe while you edit | Yes, edits happen in another directory | Yes, same reason | No: switching branches changes the files the live skills read |
| Easy to find the skill you're working on | Yes, one fixed path per skill | No, a new path each time | Only by branch name |
| Cost per edit | None after first setup | Create and remove each time | One branch switch |
| Falling behind main | Yes: 100+ directories each need syncing | No: each starts fresh from main | One checkout to update |
| Several skills at once | Yes | Yes | No: one branch at a time, so commit or stash first |
| Leftover state | Uncommitted edits sit unnoticed in many directories | Forgotten cleanup leaves orphans; careless cleanup loses uncommitted work | Half-finished edits mix into the live files |
| Stable paths for editor and agent settings | Yes | No | Yes |
| Git rule | A branch can be open in only one worktree at a time | Same rule | None |

The safety row separates branches from the other two. The findability and falling-behind rows separate permanent from throwaway.

My read so far: you can't yet tell which want you have until you see what each option costs. The table doesn't pick for you, because the rows that matter depend on which want it is. Nothing here is settled.

Need from you: which of these is closest?
1. Safe editing is the main want.
2. A findable home per skill is the main want.
3. Both, or unsure. I'd then take these three options to `option-shaping` for a fuller comparison.
