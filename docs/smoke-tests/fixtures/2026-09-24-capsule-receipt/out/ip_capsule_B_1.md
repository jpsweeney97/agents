I haven't written the plan yet. Several parts of the capsule are unconfirmed, and "push" conflicts with the no-new-external-services rule. I won't write tasks that depend on those parts until you answer.

**What I'll read first**
- The design capsule as a file (not just the pasted text), and its acceptance map if one exists. I need the repo path, because the current directory is not the app and is not a git repo.
- `settings.py`: `INSTALLED_APPS`, `TIME_ZONE`, `USE_TZ`, and the mail settings.
- The Celery app file and the Celery beat schedule. Celery beat is the scheduler that runs periodic jobs.
- The user model, to see whether it has a timezone field.
- One existing app, for file layout and test style.
- The test command and the dependency file.
- Git history for comparable changes: a new app with a model and scheduled jobs.

**What I'll do after your answers**
- Write `docs/plans/2026-09-24-notification-system.md`.
- Map the files, then write numbered tasks in build order. Each task has a failing test, the code, the passing run, and exact commands.
- Run Self-Review, then check the plan against how comparable past changes went in this repo.
- List every small choice I make under `Planner decisions`.

**What I won't build on yet**
- **"Push" for urgent.** Real push (phone or browser) needs an external service, which the binding rules out.
- **"9am local time."** It doesn't say whose local time.
- **Seven-day expiry.** It's unconfirmed, and "expire" isn't defined.
- **Same-day delay for important items.** It's unpriced, so I won't add any escalation or "send now" path.
- **"Urgent" meaning and "other gets no badge."** These were accepted, not confirmed, and they change what users see. Until you confirm, I'll assume the caller sets `kind` and nothing classifies it automatically.
- **Per-user digest time.** It's deferred, so I won't plan it. The digest hour will live in one constant.

**Need from you:**
1. What is "push"?
   1. Email through the mail setup the repo already has (my recommendation if one exists).
   2. In-app only, shown on the user's next page load.
   3. A channel the repo already uses. Tell me which.
2. Whose 9am?
   1. The project `TIME_ZONE` setting, one fixed time (my recommendation, since per-user preferences are deferred).
   2. Each user's own timezone. This needs a timezone field and an hourly job.
3. What does expiry mean?
   1. Keep the row, hide it from the user, mark it expired.
   2. Delete the row.

   Also confirm seven days, counted from digest send, or give the right number.
4. Is a one-day delay acceptable when an important item matters the same day?
   1. Yes, digest only.
   2. No. That reopens the design, so we go back to `design-exploration`.
5. Do you confirm the two accepted items: `kind` is set by the calling code, and `other` items get no badge?
   1. Yes.
   2. No. Tell me what to change.
6. What is the repo path?
