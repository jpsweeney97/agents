Design approved; handing off to `implementation-planning`. One correction to my own wording: I called approach A a "sliding-window counter," but the design you approved is a fixed-window counter. The key holds the clock-aligned minute, so the count resets at every minute boundary. A user could send 600 requests just before a boundary and 600 just after, so up to 1,200 in a few seconds. You haven't seen that trade-off priced, so the capsule marks it unconfirmed.

**Handoff capsule**
- **Approved approach:** One `RateLimit` middleware placed right after `auth` in `api/middleware.py`.
  - It keeps a Redis counter per user across all endpoints, with key `rl:{user_id}:{window_start}`, a 60 s window and a limit of 600.
  - The TTL is 60 s, set when INCR returns 1.
  - Over the limit, it returns 429 with `Retry-After` computed from the remaining TTL.
  - On a Redis error or timeout, it returns 503 with `retry-after: 5` and a warning log. No request passes.
- **Binding constraints:** ADR-0007 (all cross-request state lives in Redis). `user_id` comes from `auth.identify()`. The limit is per user across all endpoints, and the response is 429 with Retry-After.
- **How settled each decision is:**
  - You stated: the per-user scope and the 429 with Retry-After.
  - You corrected: fail-closed 503. I had offered fail-open.
  - Accepted as offered: approach A over token bucket, the 60 s window, and the 600 limit. I checked no traffic data for the 600.
  - Changed by me in self-review: TTL 60 s instead of 120 s. You approved it with the whole design but did not examine it separately.
  - Unconfirmed: the fixed-window boundary burst above.
- **Deferred or open:**
  - Token bucket (B) stays available if you later want bursts above the steady rate.
  - INCR and EXPIRE are two separate calls. A crash between them leaves a key with no TTL, which is a leak only, because the key is window-scoped. The planner decides whether to make it atomic.
- **Where the design lives:** In chat only, with no doc written. `implementation-planning` should read the full design message above in full. This capsule only orients it.

Need from you:
1. Is the fixed-window edge burst acceptable?
   1. Yes, keep it.
   2. No, switch to a true sliding window. That changes the key scheme and adds Redis work per request.
2. Save the design to a doc before planning?
   1. No, chat is enough.
   2. Yes, give me the path.
