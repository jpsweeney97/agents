I'm not giving the full tradeoff list yet, because the tradeoffs score differently depending on which want is the point. The full comparison is the job of `option-shaping`, a skill that fills out and compares options you've already named. Here is a short version by want for you to react to.

My read so far: you have three setups in mind, and the choice turns on whether you want safe editing or a findable home per skill. You haven't said which yet.

| Option | Safe editing (live checkout never touched) | Findable home per skill |
|---|---|---|
| Permanent worktree per skill | Strong | Strong, but many directories to keep in sync with main |
| Throwaway worktree | Strong while it exists | Weak: no fixed path, so you recreate it each time |
| Branches in the one checkout | Weak: switching branches changes what the live skills serve | Weak: the branch name is the only home |

The last row assumes the live skills are served from that same checkout. I haven't checked that.

Need from you:
1. Answer which want is nearer, safe editing or findable home, and I'll keep shaping.
2. Or hand off to `option-shaping` now with these three options as the fixed set, and the want question left open.
