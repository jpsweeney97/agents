# PLAN: Build the `resilience-policy` skill

Rank: #1 of 5. Opens the Era-62 review's Opening-C producer factory at its highest-footgun-density point (distributed-systems correctness), and is the first item in that review's own footgun-ordered build queue.

## Goal

Create `skills/resilience-policy/` — a dual-runtime skill that designs how ONE caller survives an unreliable dependency (an outbound service/API call, queue consumer, or scheduled job): inventory the transport's existing behavior first, enumerate the failure modes, set explicit timeout budgets, choose a retry policy only after establishing the operation is safe to retry, place circuit breaking, design visible (never silent) fallback and dead-letter behavior — and prove the design with a failure-mode × response table that is executed where a running surface exists and honestly marked authored-not-executed where none does.

Authority: the frozen Era-62 review (`docs/reviews/2026-07-01-skill-library-capability-growth-review.md`, Opening C, §9 move 5) — the domain-producer factory is "the biggest raw cognitive-offload volume", `resilience-policy` heads its build queue, and the `regex-craft`/`migration-safety` mold is the proven shape. This is a build-and-prune skill build: it does not fire unattended and wields no irreversible-effect tools, so it is NOT a charter event and gets NO ledger entry (Era-85/86 precedent: all five queue-built skills deliberately un-ledgered).

## Files to touch

- CREATE: `skills/resilience-policy/SKILL.md` (single file; no `agents/openai.yaml`, no `references/` — minimal bundle like `skills/injection-safe-inputs/`).
- RUN (not edit): `scripts/claude-skills-sync.sh`.
- READ ONLY: `skills/regex-craft/SKILL.md` (the producer mold — mirror its skeleton), `skills/injection-safe-inputs/SKILL.md` (the freshest sibling build, same skeleton), `skills/agent-facing-design/SKILL.md` and `skills/skill-ux-design/SKILL.md` (the authoring gates — consult before writing), `AGENTS.md` (Skill Editing + Validation Ladder sections).

## House rules (apply throughout)

- Branch first: `git checkout -b feature/resilience-policy` before creating any file (a hook blocks edits on `main`).
- Never `rm`; use `trash`. Never push; no PRs; do not touch `plugins/`, the Codex cache, or the mirror — `skills/` is served in place.
- Markdown: one logical line per paragraph/bullet; no hard wrapping.
- Frontmatter description contains colons → it MUST be double-quoted.
- Name check (already done, verify anyway): `resilience-policy` collides with no Codex-bundled (`openai-docs`, `skill-creator`, `skill-installer`, `plugin-creator`, `imagegen`, `pdf`, `doc`, `codex-primary-runtime`) or Claude-bundled (`code-review`, `debug`, `loop`, `claude-api`, `run`, `verify`, `security-review`) name.
- Dual-runtime text: name both invocation tokens (`/resilience-policy` or `$resilience-policy`); phrase routing to runtime-specific skills availability-conditionally.

## Implementation order

### Step 1 — Read the mold and the gates

Read `skills/regex-craft/SKILL.md` and `skills/injection-safe-inputs/SKILL.md` end to end — the new skill mirrors their shared skeleton: frontmatter → one-line summary + invocation → The owned job → Mixed skill (bar per part) → Shape (the forcing pass) → Prove it → Modes and scope → Proof boundary → Fences → Done when → Build-and-prune note. Then read the two gate skills and the AGENTS.md Skill Editing rules.

### Step 2 — Write `skills/resilience-policy/SKILL.md`

Use this description verbatim (quoted):

```yaml
---
name: resilience-policy
description: "Use when designing or vetting how one caller survives an unreliable dependency — an outbound service or API call, queue consumer, or scheduled job that can hang, fail, or flap: set explicit timeout budgets, choose the retry policy (backoff, jitter, caps, and whether the operation is safe to retry at all), place circuit breaking, design visible fallback and dead-letter behavior, and prove it with a failure-mode × response table. Caller-side only. Not for making the receiving side safe to process the same request twice (a separate design job), a live outage (`incident-response`), or an unknown-cause bug (`diagnose`)."
---
```

Body requirements, section by section (author real prose in the house voice — study the mold; do not copy regex-craft or injection-safe-inputs sentences):

1. **Summary + invocation.** One paragraph: a forcing pass over one caller→dependency edge; designs the failure-handling layer and proves it with a failure-mode × response table; advisory-until-asked. Invocation: `/resilience-policy` or `$resilience-policy`.
2. **The owned job.** Why no neighbor owns it: `incident-response` stabilizes a live incident and never designs ahead; `diagnose` hunts an unknown cause; `observability-instrumentation` decides what to *see*, not how the caller *behaves* under failure; `dependency-upgrade` absorbs a version bump; `deploy-plan` gauges one ship. None designs one integration's timeout/retry/breaker/fallback policy with a proof table. Value framing: an unhandled dependency failure cascades — one slow downstream hangs every request thread and takes the whole service down with it; the human is spared composing the checklist and auditing that no failure mode was skipped.
3. **Mixed skill — bar per part.** Firm (trust): the transport-inventory gate, the failure-mode enumeration, the retry-safety-before-retry-policy ordering, the failure-mode × response table with both honest states, the scoped verdict vocabulary. Provoked (judgment): which failure modes are live for THIS dependency, what timeout budget the caller's own deadline permits, whether a fallback is genuinely acceptable to the business or just hides breakage — forcing questions keyed to this edge, never a filled-in template.
4. **Shape — the forcing pass**, in order: (a) **Pin the edge and inventory the transport FIRST** (the identify-the-engine analogue — a required first step): the one caller→dependency edge; then what the actual client library already does — its default timeout (many have NONE: Python `requests` has no default timeout; a bare `axios` call has none), its built-in retries (AWS SDKs, gRPC, urllib3 `Retry` and many HTTP clients retry on their own — an app-level retry stacked on a hidden SDK retry multiplies attempts), its breaker support. Verify defaults on the actual library and version; never assume. (b) **Enumerate the failure modes** — connect failure, slow response/timeout, 5xx, retryable-vs-not 4xx, partial/malformed response, dependency down hard, dependency degraded (slow but alive — the worst one). Each gets a designed response; a single global "retry 3 times" is the anti-pattern. (c) **Set the timeout budget** — every remote call gets an explicit timeout; connect and read timeouts distinct where the transport separates them; deadline propagation: an inner timeout × retries must fit inside the caller's own deadline or upstream request timeout, otherwise retries never get to run or work continues after the caller gave up. (d) **Choose the retry policy — retry-safety first.** Before any retry: is this operation safe to invoke twice? A retried non-idempotent call double-books/double-charges — establish safety (the receiver-side duplicate-safety design is a neighboring job this skill does not own) or do not retry that operation. Then: retry only retryable failures (timeouts, connect errors, 5xx, and 429 with its `Retry-After` honored — never other 4xx); exponential backoff WITH jitter (no jitter = synchronized retry storms); cap both attempts and total elapsed time (a retry budget); never retry while holding locks or an open transaction; account for retry amplification through layers (each of two layers retrying 3× = up to 9 attempts at the bottom). (e) **Place circuit breaking** — when repeated failures should stop calls entirely (fail fast), per-dependency scope, half-open probing to recover, and what the caller does while open (the same path as fallback). For a low-volume caller, a breaker may be honest overkill — saying so is a valid design outcome. (f) **Design the give-up path** — fallback (cached/stale value, default, queue-for-later, or an honest error) chosen deliberately and VISIBLE (logged/metric/flagged) — a silent fallback that masks failure is the exact silent-fallback anti-pattern the house forbids; for async consumers, a dead-letter destination WITH a consumer and an alert — a DLQ nobody reads is a black hole, not a safety net.
5. **Prove it — the failure-mode × response table.** Rows: each enumerated failure mode → the designed response (concrete timeout values, retry count/backoff/jitter, breaker state change, fallback behavior, DLQ routing) → how it is verified. Two honest states, stated per row set: **executed** (a running or testable surface exists — fault-inject or stub the dependency and report observed behavior per row) or **authored, not executed** (design time — deliver the table with exact execution instructions; never claim it ran). A table whose rows are all happy-path is a reassurance ritual.
6. **Verdict vocabulary.** Exactly one of: **degrades-as-proven** (table executed, every row observed as specified — scoped to the rows run), **designed-not-yet-proven** (table authored, execution pending), **gap-found-because** (a failure mode has no designed response, a retry lacks a safety answer, a fallback is silent). Never "resilient" or "bulletproof" unqualified; the verdict never outruns the table.
7. **Modes and scope.** Applied vs advisory follows the invocation (live code → edits plus executed table on a working branch; design/review → the advisory pack). One edge: pointed at a whole service, narrow to the named or riskiest dependency edge and say so.
8. **Proof boundary (the inherited floor).** The library-wide evidence-before-claims floor specialized to failure behavior: never assert an observed response you did not run; bound the residual (e.g., "table executed against a stubbed 500/timeout harness; residual: real network partitions and the provider's actual 429 shape unobserved"). Advisory-until-asked.
9. **Fences.** vs `incident-response` (live incident now — mitigate first; compose: an incident's postmortem action "add timeouts" is this skill's trigger); vs `diagnose` (unknown cause; here the hazard class is known); vs `observability-instrumentation` (what to see vs how to behave — compose: every breaker/fallback/DLQ decision here names a signal to emit there); vs receiver-side duplicate-delivery safety (this skill decides WHETHER an operation may be retried; making the receiver safe under duplicates is a separate design job — if `skills/idempotency-design/` exists at execution time, name it here; otherwise write "a neighboring design job this skill does not own"); vs `dependency-upgrade` (version bumps).
10. **Done when.** Checklist mirroring the shape: transport inventoried with defaults verified; failure modes enumerated; timeouts explicit with deadline propagation checked; retry policy has a per-operation safety answer, jitter, and both caps; breaker placed or honestly declined; fallback visible and DLQ consumed; table delivered with each row set honestly labeled; one scoped verdict; advisory-until-asked held.
11. **Build-and-prune note.** Thin in this authoring repo; portable to every repo that calls anything over a network; judged by leverage + offload. First-to-prune on observed mis-fire. Failure shapes to watch: collapsing into a generic "add retries and timeouts" template (fold signal toward a review lens), or accreting a per-library resilience-API encyclopedia (Polly/resilience4j/tenacity syntax reference — that is drift, not the job).

### Step 3 — Validate structurally

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/resilience-policy
git diff --check
python3 -c "import yaml; d=yaml.safe_load(open('skills/resilience-policy/SKILL.md').read().split('---')[1]); print(d['name'], len(d['description'].split()))"
```

quick_validate must pass ("Skill is valid!", exit 0). The ONLY waivable complaint is "unexpected key" for `argument-hint`/`disable-model-invocation` (not used here, so expect zero complaints); any other failure is real — fix it. Then prove the description character-exact against this plan's yaml block:

```bash
python3 - <<'EOF'
import yaml, re
plan = open('PLAN-resilience-policy.md').read()
want = yaml.safe_load(re.search(r'```yaml\n---\n(.*?)\n---\n```', plan, re.S).group(1))['description']
got = yaml.safe_load(open('skills/resilience-policy/SKILL.md').read().split('---')[1])['description']
assert got == want, "description drifted from the plan"
print("description character-exact:", len(got), "chars")
EOF
```

### Step 4 — Link and verify delivery

```bash
scripts/claude-skills-sync.sh --link resilience-policy
scripts/claude-skills-sync.sh --check
```

Both must exit 0.

### Step 5 — Behavior smoke test (forward test)

Spawn ONE fresh subagent. Its prompt: the full text of the new `SKILL.md` framed as active guidance ("You have this skill loaded; follow it."), plus this scenario verbatim (it deliberately contains none of the skill's vocabulary): "Our Node service calls a third-party shipping API twice during checkout: once to fetch rate quotes, and once to book the shipment after payment succeeds. Lately that API sometimes hangs for 30+ seconds or returns 500s — checkout pages spin, and sometimes the whole service gets slow for everyone. We use axios with default settings. Work out how our service should handle this dependency before we build more on top of it." Grade the transcript against five pre-named behaviors: (1) inventoried axios's actual default behavior (no default timeout) or explicitly demanded verifying it, rather than assuming; (2) retry policy included exponential backoff WITH jitter AND separated retryable failures (timeout/5xx/429) from non-retryable 4xx; (3) treated fetch-rates and book-shipment differently on retry-safety — booking is not blindly retried (double-booking named or its safety made a precondition); (4) fallback/breaker behavior is visible (logged/flagged/alerting), not a silent swallow, and the thread-exhaustion cascade is addressed (timeout budget/fail-fast); (5) delivered a failure-mode × response table marked authored-not-executed (no running surface in the scenario) and rendered a scoped verdict, not "resilient now". Record pass/fail per behavior. 4/5 or better → proceed. Below → tighten the SKILL.md wording that failed (once) and re-run. Still below → STOP at the committed branch and report honestly; do not land.

### Step 6 — Commit and land

```bash
git add skills/resilience-policy
git commit -m "feat: add resilience-policy skill (Era-62 review Opening C, factory move #1)"
git checkout main && git merge --ff-only feature/resilience-policy
git branch -d feature/resilience-policy
git status --short --branch
```

Do NOT push. Do NOT add a ledger entry.

## Edge cases a weaker model would miss

- **The transport inventory is the load-bearing gate**, mirroring regex-craft's identify-the-engine: Python `requests` has NO default timeout (hangs forever); many SDKs (AWS, gRPC, urllib3) retry internally, so an app-level retry silently multiplies attempts. The skill must demand the defaults be looked up on the actual library/version, never assumed.
- **Retry-safety precedes retry policy.** A weaker author writes "retry with backoff" as a universal good; retrying a non-idempotent booking/charge is the most expensive bug in this domain. The safety question must be a mandatory pre-step, not a bullet.
- **Jitter is load-bearing, not decoration** — synchronized backoff across many clients is a self-inflicted DDoS (retry storm / thundering herd).
- **429 is the retryable 4xx** (honor `Retry-After`); a naive "retry 5xx only / never 4xx" rule gets it wrong on both sides.
- **Deadline propagation:** per-try timeout × attempts must fit the caller's own deadline, or retries are theater. This interaction is the kind of thing a checklist without the multiplication misses.
- **A silent fallback violates this user's global fail-fast rule** (`~/.claude/CLAUDE.md`: no silent fallbacks). The skill text must make fallback visibility a firm requirement, which also keeps the skill consistent with the house rules it ships under.
- **Do not name skills that don't exist.** `idempotency-design` is plan #2 of this queue — run `ls skills/` at execution time and name it in the fence ONLY if present; the description already avoids naming it (by design — do not "fix" that).
- **The smoke scenario must not teach the test.** If your scenario says "timeout", "jitter", "circuit breaker", or "idempotent", the pass is fake. The scenario above is the tested wording — use it verbatim.
- **quick_validate's schema lags Claude Code:** only the documented "unexpected key" complaint is waivable; never resolve a validator complaint by deleting a documented-valid field.

## Acceptance criteria

1. `skills/resilience-policy/SKILL.md` exists on `main`; frontmatter parses; description is double-quoted and character-exact to this plan's yaml block (the Step-3 comparison passes).
2. `quick_validate.py skills/resilience-policy` passes clean; `git diff --check` clean.
3. `scripts/claude-skills-sync.sh --check` exits 0 and `ls -la ~/.claude/skills/resilience-policy` shows a symlink into this repo.
4. The body contains: a transport-inventory first step naming that defaults must be verified; a retry-safety-before-retry-policy ordering; both table states (executed / authored-not-executed); a three-term verdict vocabulary that excludes bare "resilient"; a Done-when checklist; a Build-and-prune note naming its fold signal and encyclopedia drift.
5. Grep guards: `grep -ci 'jitter' skills/resilience-policy/SKILL.md` ≥ 2; `grep -ci 'idempoten\|safe to retry\|safe to invoke twice' skills/resilience-policy/SKILL.md` ≥ 2; `grep -ci 'dead-letter' skills/resilience-policy/SKILL.md` ≥ 2; `grep -n 'rm ' skills/resilience-policy/SKILL.md` returns nothing.
6. Smoke test recorded in the final report: 5 behaviors, ≥4 passed, scenario text plan-verbatim, run on a fresh context.
7. Landed on `main` via `--ff-only`; feature branch deleted; working tree clean; nothing pushed; no ledger entry added.

## Out of scope

Building `idempotency-design` (plan #2); receiver-side duplicate-safety content beyond the one fence line; editing any existing skill; rate-limiting/backpressure design (a future factory item); benchmarking; publishing.
