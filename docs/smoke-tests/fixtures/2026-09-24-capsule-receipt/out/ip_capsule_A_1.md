**I won't write the plan yet. I need to read the repo first, and four points in the capsule need your answers before I build tasks on them.**

**What I'll read first** (I won't assume paths from "standard layout"):
- `settings.py`: `INSTALLED_APPS`, `TIME_ZONE`, `USE_TZ`, `EMAIL_BACKEND`, and the Celery settings, including the beat schedule. Celery beat is the scheduler that starts periodic jobs.
- The Celery app file and one existing app's `models.py`, `tasks.py`, `tests/` and `admin.py`, so I can copy its layout.
- The user model. I need to know whether it is custom and whether it has a timezone field.
- Any existing email, push or websocket code. This decides what "push for urgent" can mean under "no new external services".
- The test and lint commands (`pyproject.toml`, `Makefile`, CI file) and the `docs/plans/` naming convention.
- Past commits or PRs that added an app with periodic tasks. I'll use them for the final completeness check.

**What I won't build on yet:**
- **Digest at 9am local:** the previous lane never confirmed it, and "local" isn't defined. Per-user times are deferred, so I need to know whose clock.
- **Seven-day expiry:** it is unconfirmed, and "expire" isn't defined.
- **Same-day delay for important items:** it is unpriced. I'll plan only the approved approach, with no same-day escalation, and record this as an open cost at the top of the plan.
- **Push for urgent:** mobile or web push usually needs an external service, which the binding constraint forbids. I'll hold this task until I've seen what the repo already has.

I will build the two accepted points as written. "Urgent" means it blocks someone's work today, and `other` items do nothing and get no badge.

**After your answers:** I'll write the tasks in dependency order, each test-first, with exact paths, complete code and commands with expected output. Where the design is silent, I'll list my choices under "Planner decisions" at the top. Then I'll check the plan against the capsule and against what similar changes needed in this repo. If the repo has no comparable change, I'll say I used general knowledge instead. I expect to add migrations, tests that fix the clock, a digest that is safe to run twice, and daylight-saving handling.

Need from you (I'll start reading the repo next; I need these before I write the digest, expiry, badge and push tasks):
1. Digest time:
   - a) 9am in one project timezone (Django `TIME_ZONE`), run once a day. I recommend this.
   - b) 9am in each user's own timezone. This needs a new per-user timezone field and an hourly run, and it is close to the deferred per-user preference.
   - c) Something else.
2. Expiry:
   - a) 7 days, and expired items are marked and kept. This is my default.
   - b) A different number of days.
   - c) 7 days, and expired rows are deleted.
3. Same-day delay for important items:
   - a) Accept it, and I'll note it in the plan.
   - b) Not acceptable, so the approach goes back to `design-exploration`.
4. In-app badge:
   - a) Urgent and important items both get one.
   - b) Urgent only.

The capsule only says `other` gets none.
