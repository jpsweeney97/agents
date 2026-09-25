Handing off to `implementation-planning` with one item still open: the design uses a fixed window, not the sliding window I called it earlier.

**Handoff note** (chat only, no doc written)

- **Approved design:**
  - A new `RateLimit` middleware in `api/middleware.py`, registered right after `auth`. It limits per `user_id`, with all endpoints counted together.
  - The Redis key is `rl:{user_id}:{window_start}`, where window start is the epoch time floored to 60 s. Each request runs `INCR`, and the TTL is set when the result is 1.
  - The limit is 600 requests per 60 s. Over the limit, the response is 429 with `Retry-After` computed from the key's remaining TTL.
  - On a Redis error or timeout, the response is 503 with `retry-after: 5` and a warning log. No request passes.
  - Tests cover under, at, and over the limit, and that the TTL is set only once. An integration test runs against a real Redis in CI.
- **Binding constraints:** ADR-0007 (all cross-request state lives in Redis). Follow the existing `INCR` patterns in `infra/redis.py`.
- **Deferred:** Token bucket (approach B). It only wins if you want short bursts above the steady rate, and nothing asked for that.
- **How settled each decision is:**
  - Per user across all endpoints, and 429 with `Retry-After`: your own words.
  - Fail closed with 503: contested and corrected. You overrode my fail-open.
  - Approach A, 60 s window, 600 limit: accepted as offered.
  - TTL of 60 s: my own change during self-review, which I disclosed. Accepted as offered.
  - Fixed vs sliding window: **open**, see below.
- **Approved by:** your own words ("Approved").
- **Pressure test:** none ran. I should have offered `grill-me` before asking for approval, and I didn't. These premises come from my own reading of the code and are untested until planning or the first real run:
  - The 2 ms Redis round trip.
  - `auth.identify()` always yielding a stable `user_id`.
  - A crash between `INCR` and the TTL set leaves a key with no TTL. That leaks a key but doesn't lock anyone out, since the key name changes each window.

**The open item:** the key includes the floored window start, so the counter resets at each 60 s boundary. A user can send 600 requests at the end of one window and 600 at the start of the next, up to 1200 in a short span. You approved this under the name "sliding-window counter", which was inaccurate.

Need from you:
1. Keep the fixed window and accept the boundary burst (simplest, as designed).
2. Switch to a true sliding window (more Redis work per request).
3. Run `grill-me` on the design before planning starts.

If you pick none, planning starts with the fixed-window question marked open.
