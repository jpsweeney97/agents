User: /plan-cycle:implementation-planning — write the implementation plan for the notification system from the design capsule below. The repo is a small Django app; assume standard layout. You can't inspect files this turn, so tell me what you need and what you'll do, and flag anything you won't build on yet.

Design capsule (from design-exploration, approved):
- Approved approach: a `notifications` app with a `Notification` model (kind: urgent | important | other), a push path for urgent, a daily digest job for important, nothing for other.
- Accepted as offered, not contested during the cycle: "urgent" means it blocks someone's work today; "other" items produce no in-app badge either.
- Still the previous lane's compression, unconfirmed by the user: the digest sends at 9am local time; unread digest items expire after seven days.
- Unpriced: whether a day's delay is acceptable when a digest item turns out to matter the same day.
- Deferred: per-user digest time preferences.
- Binding: no new external services; must run on the existing Celery beat.
- Next lane: implementation-planning.
