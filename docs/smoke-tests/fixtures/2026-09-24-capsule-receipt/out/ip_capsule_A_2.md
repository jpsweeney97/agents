I haven't written the plan yet. I can plan most of the capsule now, but five items aren't settled enough to build tasks on, and I'll leave the tasks that depend on them out until you answer.

**Building on now:**
- The `notifications` app and the `Notification` model with kinds urgent, important and other.
- Routing: urgent gets a push, important goes to the daily digest, and other gets nothing, not even a badge.
- "Urgent" means it blocks someone's work today.
- No new external services, running on the existing Celery beat (Celery's scheduler for recurring background jobs).

**Not building on yet:**
- **9am and seven-day expiry.** The earlier design step compressed these and you haven't confirmed them. Both change what users see.
- **Whose "local" time.** The capsule doesn't say. I'll check whether the user model stores a time zone.
- **The same-day delay.** An important item that matters today waits up to a day for the digest. Nobody has priced that.
- **The push channel.** The capsule names none and forbids new services. I'll look for an existing one (email, websockets, a push provider already in use). I won't write that task until it's known. If the repo has none or several, I'll ask you.
- **Badges for urgent and important.** The capsule says "other" gets no badge "either", but never says the other two do. I'll look for an existing badge.

**What I'll read first:**
- Settings: `INSTALLED_APPS`, the Celery settings, `TIME_ZONE`/`USE_TZ`, and the email backend.
- The Celery app, existing `tasks.py` files, and the beat schedule.
- The user model.
- One or two existing apps, for layout of models, tests, factories and migrations.
- The test and lint commands.
- Whether `docs/plans/` exists.
- Any `Acceptance map:` link on the source. If the capsule has no source file, I'll cite it as pasted in chat.

**Then I'll:**
- Map the files and write numbered, test-first tasks with exact paths, full code and commands.
- Self-check the plan against the capsule.
- Compare it with past changes in this repo that added an app or a Celery job. That is a check for work such changes usually need but the capsule didn't name. If the repo has no such history, I'll use general knowledge and say so in the plan.
- Save it to `docs/plans/2026-09-24-notification-system.md`, with a "Planner decisions" list of the small calls the capsule left open. One I expect: expiry stamps a timestamp on the row instead of deleting it.
- Commit only that file, if the repo is a git worktree, under your Markdown rule.

I won't start implementing. `execute-plan` runs the plan afterward.

Need from you:
1. Digest time and expiry: (a) 9am and seven days as written, or (b) different values.
2. What "9am local" means: (a) one site time zone from Celery's setting (my pick, since per-user settings are deferred), or (b) each user's own time zone (only if the user model already stores one).
3. The same-day delay: (a) accept it and record it in the plan as an accepted risk (my pick), (b) add a task to promote an item to urgent (new scope), or (c) go back to design-exploration.
