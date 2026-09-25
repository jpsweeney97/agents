Approved. Before I hand off, I found two flaws in the design text I showed you, both mine. The first affects behavior you approved, so the handoff waits on your answer.

**1. The counter is fixed-window, not sliding-window.** I named approach A a "sliding-window counter." The design keys each counter on the 60-second window start, so counts reset at each boundary. A user could send 600 requests at the end of one window and 600 at the start of the next, which is 1200 in a few seconds. My lean is to keep fixed-window: it is the simple design you approved, and nothing in the outcome asks for a strict rate. The alternative is a true sliding window or approach B, which costs more design work.

**2. Retry-After should not come from the key's TTL.** The TTL starts at the first request in the window, so it can outlast the window and overstate the wait. It should be `window_start + 60 − now`. Nothing else changes.

**Handoff capsule for `implementation-planning`**
- **Approach:** `RateLimit` middleware right after `auth` in `api/middleware.py`. It runs `INCR` on `rl:{user_id}:{window_start}` and sets a 60 s TTL when the result is 1. Over 600 returns 429 with `Retry-After`. A Redis error or timeout returns 503 with `retry-after: 5` and a warning log.
- **Your own words:** limit is per user across all endpoints; 429 with Retry-After.
- **Corrected by you:** fail closed with a 503 when Redis is unreachable.
- **Accepted as offered:** 60 s window and a limit of 600. TTL is 60 s, a change I made in self-review that you then approved.
- **Unconfirmed:** items 1 and 2 above.
- **Binding constraints:**
  - ADR-0007: all cross-request state lives in Redis.
  - Follow the existing `INCR` patterns in `infra/redis.py`.
  - Tests: unit tests for under-limit, at-limit, over-limit and TTL set once, plus an integration test against real Redis in CI.
- **Left open for planning:** `INCR` and `EXPIRE` are two calls, not one atomic step. A crash between them leaves a dead key, not a lockout. Planning can choose a pipeline or a Lua script.
- **Not built:** token bucket (B) and per-endpoint limits.
- **Design doc:** none written. The full design is the section text earlier in this chat, and the planner reads it in full.

**Need from you:**
1. Fixed-window: (a) keep it, and the plan states the boundary burst plainly; (b) switch to a true sliding window.
2. Retry-After computed from the window end: yes or no?

Once you answer, I hand off to `implementation-planning`.
