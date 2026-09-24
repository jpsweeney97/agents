I can write most of the plan, but not the tasks that depend on four unconfirmed points. I'll hold those until you answer.

**What I'll read first (read-only)**
- The full design doc behind this capsule, and any `Acceptance map:` link in it. I only have the capsule.
- `settings.py`: `INSTALLED_APPS`, `AUTH_USER_MODEL`, `TIME_ZONE`, `USE_TZ`, Celery config and any existing beat schedule. Celery beat is the scheduler that runs timed jobs.
- `celery.py` and any existing `tasks.py`, to copy how tasks are written and registered.
- One existing app's layout, tests and migrations.
- Email backend settings, Django Channels, or any push library already installed. This decides what "push" can mean under "no new external services".
- The test and lint commands.
- `git log` for past changes that added a model plus a Celery job. I'll compare against those to find work this kind of change usually needs that the design left out. If there are none, I'll use general knowledge and say so in the plan.

**What I'll write**
One plan, because push and digest both depend only on the model. It goes to `docs/plans/2026-09-24-notification-system.md`. I won't execute it, and I won't commit unless the repo's convention says to.

**What I'll build on now**
- The app skeleton, the `Notification` model with its migration, admin, and tests.
- "Other" stores a row and does nothing else: no push, no digest, no badge. I'll list this under `Planner decisions` as accepted-as-offered, not confirmed.
- The definition of "urgent" goes into a docstring only. Callers choose the kind, and the plan builds no classifier.

**What I won't build on yet**
- **9am local time.** "Local" could mean one project time zone or each user's own. Per-user needs a stored time zone per user, and per-user digest time is deferred.
- **Seven-day expiry of unread digest items.** It needs a read-state field, and "expire" is undefined.
- **Delay for important items.** This is unpriced. I won't add an early-send path, so the plan builds only the once-a-day digest.
- **What "push" means.** I'll propose one option after the repo read, based on what's already installed.

Need from you:
1. What does "9am local" mean?
   1. One project time zone (recommended, matches the deferral).
   2. Each user's own time zone.
2. What does expiry do to an unread digest item?
   1. Hide it from the digest and keep the row (recommended).
   2. Delete it.
   3. Drop the expiry rule.
3. Is a one-day delay acceptable for important items?
   1. Yes, build as designed.
   2. No. That reopens the design, so we'd go back to `design-exploration`.
4. Is there a fuller design doc or acceptance map? If so, send the path.
