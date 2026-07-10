# PLAN: Build the `idempotency-design` skill

Rank: #2 of 5. The other half of the Era-62 factory's opening pair: `resilience-policy` decides whether a caller may retry; this skill makes the receiver survive the duplicates those retries (and at-least-once delivery) create. Execute AFTER plan #1 — this skill's description names `resilience-policy`.

## Goal

Create `skills/idempotency-design/` — a dual-runtime skill that designs how ONE receiving operation stays correct under duplicate delivery (a payment/order endpoint, webhook handler, queue consumer, or job runner): state the honest baseline (exactly-once delivery does not exist; exactly-once *processing* is what you build), classify natural idempotency first, choose the idempotency key and its scope, make the dedup reservation atomic with the state change, replay the original response to duplicates, fence downstream side effects, handle the concurrent-duplicate race — and prove it with a duplicate/concurrent-replay table, executed where a runnable surface exists and honestly marked authored-not-executed where none does.

Authority: the frozen Era-62 review (`docs/reviews/2026-07-01-skill-library-capability-growth-review.md`, Opening C, §9 move 5) lists `resilience-policy`/`idempotency-design` jointly at the head of the factory queue and flags their seam as one to settle at build time. This plan settles it: **caller-side failure discipline = `resilience-policy`; receiver-side duplicate-delivery safety = this skill**; the bridge sentence ("retry is safe only when the receiver is idempotent") appears on both sides as a fence, never as duplicated machinery. Build-and-prune: NOT a charter event, NO ledger entry.

## Files to touch

- CREATE: `skills/idempotency-design/SKILL.md` (single file; no `agents/openai.yaml`, no `references/`).
- RUN (not edit): `scripts/claude-skills-sync.sh`.
- READ ONLY: `skills/regex-craft/SKILL.md` and `skills/injection-safe-inputs/SKILL.md` (the mold + freshest sibling), `skills/resilience-policy/SKILL.md` (landed by plan #1 — mirror its fence wording from the other side), `skills/agent-facing-design/SKILL.md`, `skills/skill-ux-design/SKILL.md`, `AGENTS.md` (Skill Editing + Validation Ladder).

## House rules (apply throughout)

- Branch first: `git checkout -b feature/idempotency-design` (a hook blocks edits on `main`).
- Never `rm`; use `trash`. Never push; no PRs; do not touch `plugins/`, the Codex cache, or the mirror.
- Markdown: one logical line per paragraph/bullet. Description has colons → double-quote it.
- Name check: `idempotency-design` collides with no Codex-bundled (`openai-docs`, `skill-creator`, `skill-installer`, `plugin-creator`, `imagegen`, `pdf`, `doc`, `codex-primary-runtime`) or Claude-bundled (`code-review`, `debug`, `loop`, `claude-api`, `run`, `verify`, `security-review`) name.
- Dual-runtime tokens: `/idempotency-design` or `$idempotency-design`.
- Precondition check: `ls skills/resilience-policy/SKILL.md` must exist (plan #1 landed). If it does not, STOP and execute plan #1 first — do not reword this plan's description around its absence.

## Implementation order

### Step 1 — Read the mold, the sibling, and the gates

Read `skills/regex-craft/SKILL.md`, `skills/injection-safe-inputs/SKILL.md`, and the landed `skills/resilience-policy/SKILL.md` end to end; then the two gate skills and AGENTS.md Skill Editing rules. The new skill mirrors the shared skeleton: summary+invocation → owned job → mixed-skill bars → shape → prove it → modes and scope → proof boundary → fences → done when → build-and-prune note.

### Step 2 — Write `skills/idempotency-design/SKILL.md`

Use this description verbatim (quoted):

```yaml
---
name: idempotency-design
description: "Use when designing or vetting how one receiving operation stays correct under duplicate delivery — a payment or order endpoint, webhook handler, queue consumer, or job that client retries, at-least-once delivery, or double-clicks can invoke twice: choose the idempotency key and its scope, make the dedup check atomic with the state change, replay the original response, fence downstream side effects, and prove it with a duplicate/concurrent-replay table. Receiver-side only. Not for caller-side timeout/retry/circuit-breaker policy (`resilience-policy`) or debugging an unexplained double-charge already in production (`diagnose` finds the cause first)."
---
```

Body requirements, section by section (real prose in the house voice; do not copy sibling sentences):

1. **Summary + invocation.** A forcing pass over one receiving operation; designs exactly-once *processing* on top of at-least-once *delivery* and proves it with a duplicate/concurrent-replay table; advisory-until-asked.
2. **The owned job.** No neighbor owns it: `resilience-policy` is the caller's side — it decides whether to retry, and its retry-safety question routes HERE for the answer; `injection-safe-inputs` guards what the input contains, not how often it arrives; `diagnose` hunts an unknown cause after the double-charge already happened; `migration-safety`/`contract-change-propagation` are different axes entirely. Value framing: the duplicate-delivery bug class is maximally expensive precisely where it is most likely (payments, orders, notifications), and the window is invisible in happy-path testing — the human is spared composing the checklist and auditing that the race cases were actually covered.
3. **Mixed skill — bar per part.** Firm (trust): the exactly-once-delivery-is-a-myth baseline, the natural-idempotency classification gate, the atomic-reservation requirement (naming check-then-act as a defect), the response-replay rule, the proof table with both honest states, the scoped verdict vocabulary. Provoked (judgment): which key actually identifies "the same intent" for THIS operation, where the reservation can live so it shares a transaction with the state change in THIS stack, which side effects genuinely need fencing — forcing questions, never a template.
4. **Shape — the forcing pass**, in order: (a) **Pin the operation and its duplicate sources** — the one receiving operation; why duplicates arrive here (client/SDK retries, at-least-once queue redelivery, webhook provider redelivery, user double-click, replayed jobs); state the baseline plainly: exactly-once delivery does not exist between separate systems — the receiver owns exactly-once processing. (b) **Classify natural idempotency first — the honest cheap exit.** Full-state overwrites (SET, PUT-with-complete-resource, upsert-to-absolute-value) are naturally idempotent and may need no machinery — but the claim must survive scrutiny: an "upsert" that also increments a counter, appends a log entry, or sends an email is NOT naturally idempotent; the side effects decide, not the verb. Recognizing that no machinery is needed is a valid, stated outcome. (c) **Choose the key and its scope.** Client-generated idempotency key where the caller can send one (the caller is the only party that knows two requests are the same *intent* — a request hash conflates "same intent twice" with "same payload legitimately re-sent"); a natural business key where it cannot (the webhook provider's event id, the order id). Scope the key per operation, not globally (the same key on create-order and cancel-order must not collide). Set the retention window from how late duplicates can actually arrive (queue redrive policies, webhook retry schedules — days, not minutes), and say what happens when a duplicate arrives after expiry. (d) **Make the reservation atomic with the state change.** Check-then-act is the defect: two concurrent duplicates both pass the "seen?" check and both process. The reservation must be an atomic claim — a unique-constraint INSERT, a conditional put, `SETNX` — and the strongest form puts the reservation row in the SAME database transaction as the state change, so they commit or roll back together. A dedup store in one system (Redis) guarding state in another (Postgres) has a crash window between them — name it and either accept it explicitly or close it. (e) **Replay the response.** A duplicate of a completed operation returns the ORIGINAL response (store the result keyed by the idempotency key), not an error — a client that timed out cannot distinguish "already done" from "failed, retry again", and a 409 forces every caller to write a second lookup path. A duplicate of an IN-FLIGHT operation (first attempt still running) must wait or get a retry-later signal — never process concurrently. (f) **Fence downstream side effects.** The operation's own state change is now safe; its outbound effects (charge the card, send the email, call another service) each need their own idempotency answer — pass a derived idempotency key downstream where the provider supports one (payment APIs do), or record-and-skip on replay. A crash after the state change but before/mid side effects means the retry re-enters: design what re-execution does per effect. (g) **Name the ordering/staleness edge** where relevant: a late-arriving duplicate must not overwrite newer state (version checks / fencing tokens) — one paragraph, not a second skill.
5. **Prove it — the duplicate/concurrent-replay table.** Rows at minimum: sequential duplicate of a completed operation → original response replayed, zero repeated side effects; two CONCURRENT duplicates → exactly one processes, the other waits/replays; crash-mid-processing then retry → completes or cleanly re-runs with no double effect; different key → processes independently; post-expiry duplicate → the stated behavior. Two honest states per row set: **executed** (a runnable surface exists — drive duplicates in tests or against a dev surface and report observed results) or **authored, not executed** (exact execution instructions; never claim it ran).
6. **Verdict vocabulary.** Exactly one of: **duplicate-safe-as-proven** (scoped to the rows run), **designed-not-yet-proven**, **gap-found-because** (a check-then-act window, a missing replay path, an unfenced side effect). Never "exactly-once" as an unqualified system property; never a certificate beyond the table.
7. **Modes and scope.** Applied vs advisory follows the invocation; one operation — pointed at a whole API, narrow to the named or riskiest operation and say so.
8. **Proof boundary (the inherited floor).** Never assert an observed replay outcome you did not run; bound the residual (e.g., "concurrent-duplicate row executed with two parallel test workers; residual: the provider's real redelivery timing unobserved").
9. **Fences.** vs `resilience-policy` (the caller's side; the bridge stated from this side: a caller may safely retry exactly because this design exists — compose, never duplicate its timeout/backoff machinery); vs `injection-safe-inputs` (content vs arrival-count); vs `diagnose` (an unexplained production double-charge is cause-unknown first); vs `migration-safety` (running data changes). Where the target is a queue consumer, note the delivery-semantics claim of the broker is an input, not a guarantee to lean on.
10. **Done when.** Checklist mirroring the shape: duplicate sources named; natural-idempotency classification stated (including the no-machinery-needed exit when true); key + scope + retention chosen with rationale; reservation atomic with the state change (or the two-store gap explicitly accepted); response replay for completed AND in-flight duplicates; each downstream side effect fenced; table delivered with honest per-row-set labels; one scoped verdict; advisory-until-asked held.
11. **Build-and-prune note.** Thin here; portable to every repo that receives requests, webhooks, or queue messages. First-to-prune on observed mis-fire. Failure shapes: collapsing into "add a unique constraint" boilerplate (fold signal), or accreting a per-broker/per-provider semantics encyclopedia (Kafka/SQS/Stripe reference tables — drift, not the job).

### Step 3 — Validate structurally

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/idempotency-design
git diff --check
python3 -c "import yaml; d=yaml.safe_load(open('skills/idempotency-design/SKILL.md').read().split('---')[1]); print(d['name'], len(d['description'].split()))"
```

Then prove the description character-exact against this plan's yaml block (same comparison snippet as plan #1, with `PLAN-idempotency-design.md` and `skills/idempotency-design/SKILL.md` substituted). Only the documented "unexpected key" complaint is waivable; expect zero complaints.

### Step 4 — Link and verify delivery

```bash
scripts/claude-skills-sync.sh --link idempotency-design
scripts/claude-skills-sync.sh --check
```

Both must exit 0.

### Step 5 — Behavior smoke test (forward test)

ONE fresh subagent; prompt = the full new `SKILL.md` as active guidance plus this scenario verbatim (no skill vocabulary): "We're on Rails with Postgres and Sidekiq. Two problems keep happening: our payment provider's webhook sometimes gets delivered to us two or three times for the same event, and users sometimes double-click the Place Order button. Each order must charge the customer once and send exactly one confirmation email. Work out how the order-creation endpoint and the webhook handler should be built to handle this." Grade against five pre-named behaviors: (1) chose a per-operation key with stated scope for each surface — the provider's event id for the webhook, a client-generated key (or equivalent single-intent token) for order creation — with a retention window; (2) named the concurrent-duplicate race and made the reservation atomic (unique constraint / conditional insert), not a check-then-look pattern; (3) placed the reservation in the same Postgres transaction as the order write, or explicitly surfaced the two-store crash window if it proposed Redis; (4) duplicates of a completed request get the original response back (and in-flight duplicates wait or get retry-later), not an error that strands the client; (5) fenced the downstream effects — the charge gets an idempotency key passed to the provider, the email is recorded-and-skipped on replay — and delivered a replay table with a scoped verdict, marked authored-not-executed. Record pass/fail per behavior. 4/5 → proceed; below → tighten wording once and re-run; still below → STOP at the committed branch and report honestly.

### Step 6 — Commit and land

```bash
git add skills/idempotency-design
git commit -m "feat: add idempotency-design skill (Era-62 review Opening C, factory move #1 pair)"
git checkout main && git merge --ff-only feature/idempotency-design
git branch -d feature/idempotency-design
git status --short --branch
```

Do NOT push. Do NOT add a ledger entry. Do NOT edit `resilience-policy`'s description to add a reciprocal name — the Era-86 precedent ("name neighbors only when selection-critical; no edge without an observed misroute") holds; its generic receiver-side boundary phrasing is deliberate.

## Edge cases a weaker model would miss

- **Check-then-act is the central defect, not a style choice.** "Look up the key; if absent, process; then record it" fails under concurrency and under crash-between-steps. The skill text must name the atomic claim (unique constraint / conditional write) as the requirement and check-then-act as the anti-pattern by name.
- **The dedup record and the state change must share a transaction where possible.** A Redis-guarding-Postgres design has a crash window that either lets the duplicate through or permanently blocks the original; a weaker author proposes Redis reflexively because tutorials do.
- **Duplicates get the original response, not a 409.** The whole point of an idempotency key is that the timed-out caller can safely re-send and get its receipt; erroring on duplicates re-creates the ambiguity the key exists to remove.
- **In-flight concurrent duplicates are a distinct row** from sequential ones — "return the stored response" doesn't exist yet mid-flight; the design must say wait / lock / retry-later.
- **Side effects don't inherit the endpoint's idempotency.** Making the order row safe does nothing for the charge and the email; each outbound effect needs its own answer (downstream idempotency keys exist in real payment APIs — use that fact).
- **Natural idempotency is the honest cheap exit** — but verb-level reasoning ("it's an upsert") lies when side effects ride along. The classification gate must interrogate effects, not verbs.
- **"Exactly-once" claims:** brokers and buses market exactly-once *within their own boundary*; across systems it is at-least-once + dedup. The skill must state the myth plainly without turning into a broker-semantics encyclopedia.
- **The seam with `resilience-policy` is settled by this queue** (caller vs receiver) — do not re-open it, do not duplicate timeout/backoff content here, and do not add machinery for the caller's side.
- **The smoke scenario must not teach the test** — the scenario above never says "idempotency", "key", "atomic", "race", or "replay". Use it verbatim.

## Acceptance criteria

1. `skills/idempotency-design/SKILL.md` exists on `main`; frontmatter parses; description double-quoted and character-exact to this plan's yaml block.
2. `quick_validate.py skills/idempotency-design` passes clean; `git diff --check` clean.
3. `scripts/claude-skills-sync.sh --check` exits 0; `ls -la ~/.claude/skills/idempotency-design` shows a symlink into this repo.
4. The body contains: the exactly-once-processing-over-at-least-once-delivery baseline; a natural-idempotency classification gate with the no-machinery exit; an atomic-reservation requirement naming check-then-act as the defect; response replay covering completed and in-flight duplicates; downstream side-effect fencing; both table states; a three-term verdict vocabulary; Done-when; Build-and-prune with fold signal + encyclopedia drift.
5. Grep guards: `grep -ci 'check-then-act' skills/idempotency-design/SKILL.md` ≥ 1; `grep -ci 'replay' skills/idempotency-design/SKILL.md` ≥ 3; `grep -ci 'exactly-once' skills/idempotency-design/SKILL.md` ≥ 2; `grep -c 'resilience-policy' skills/idempotency-design/SKILL.md` ≥ 2 (description + fence); `grep -n 'rm ' skills/idempotency-design/SKILL.md` returns nothing.
6. Smoke test recorded: 5 behaviors, ≥4 passed, scenario plan-verbatim, fresh context.
7. Landed via `--ff-only`; branch deleted; tree clean; nothing pushed; no ledger entry; `resilience-policy` untouched.

## Out of scope

Editing `resilience-policy` (including adding it a reciprocal named edge); caller-side retry/timeout/breaker content beyond the fence; distributed-transaction/saga design; broker selection; benchmarking; publishing.
