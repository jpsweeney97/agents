# PLAN: Build the `time-handling` skill

Rank: #3 of 5. Third item in the Era-62 factory queue and the widest-reach correctness domain on it — every codebase touches time, and the worst footgun ("just store everything in UTC") masquerades as best practice.

## Goal

Create `skills/time-handling/` — a dual-runtime skill that designs or vets how code represents and computes dates and times: identify the stack's time model first, choose the correct representation per value (UTC instant vs local-time-plus-IANA-zone vs plain date — the three are not interchangeable), scan the known hazards (DST gaps/overlaps, offset-vs-zone confusion, naive/aware mixing, epoch-unit mixups, wall-vs-monotonic clocks, serialization drift), and prove the result with an executed boundary-case table where a runtime exists, honestly marked authored-not-executed where none does.

Authority: the frozen Era-62 review (`docs/reviews/2026-07-01-skill-library-capability-growth-review.md`, Opening C, §9 move 5) — `time-handling` is the factory queue's third item ("TZ/DST/serialization, executed table"). Build-and-prune: NOT a charter event, NO ledger entry (Era-85/86 precedent).

## Files to touch

- CREATE: `skills/time-handling/SKILL.md` (single file; no `agents/openai.yaml`, no `references/`).
- RUN (not edit): `scripts/claude-skills-sync.sh`.
- READ ONLY: `skills/regex-craft/SKILL.md` (the mold — its identify-the-engine-first gate is the direct template for this skill's identify-the-time-model gate), `skills/injection-safe-inputs/SKILL.md` (freshest sibling), `skills/agent-facing-design/SKILL.md`, `skills/skill-ux-design/SKILL.md`, `AGENTS.md` (Skill Editing + Validation Ladder).

## House rules (apply throughout)

- Branch first: `git checkout -b feature/time-handling` (a hook blocks edits on `main`).
- Never `rm`; use `trash`. Never push; no PRs; do not touch `plugins/`, the Codex cache, or the mirror.
- Markdown: one logical line per paragraph/bullet. Description has colons → double-quote it.
- Name check: `time-handling` collides with no Codex-bundled (`openai-docs`, `skill-creator`, `skill-installer`, `plugin-creator`, `imagegen`, `pdf`, `doc`, `codex-primary-runtime`) or Claude-bundled (`code-review`, `debug`, `loop`, `claude-api`, `run`, `verify`, `security-review`) name.
- Dual-runtime tokens: `/time-handling` or `$time-handling`.

## Implementation order

### Step 1 — Read the mold and the gates

Read `skills/regex-craft/SKILL.md` and `skills/injection-safe-inputs/SKILL.md` end to end; then the two gates and AGENTS.md Skill Editing rules. Mirror the shared skeleton: summary+invocation → owned job → mixed-skill bars → shape → prove it → modes and scope → proof boundary → fences → done when → build-and-prune note.

### Step 2 — Write `skills/time-handling/SKILL.md`

Use this description verbatim (quoted):

```yaml
---
name: time-handling
description: "Use when designing or vetting how code represents and computes dates and times — timezones, DST transitions, storage and serialization, recurring or future events, date arithmetic, or clock choice: pick the correct representation per value (UTC instant vs local-time-plus-IANA-zone vs plain date), scan the known hazards (DST gaps and overlaps, offset-vs-zone confusion, naive/aware mixing, epoch-unit mixups, wall-vs-monotonic clocks), and prove it with an executed boundary-case table. Not for calendar-product feature design, scheduling-infrastructure choice, or code that merely calls a date API with no correctness question."
---
```

Body requirements, section by section (real prose in the house voice; do not copy sibling sentences):

1. **Summary + invocation.** A forcing pass over one codebase area's time handling; picks the right representation per value and proves the choices at the boundaries; advisory-until-asked. `/time-handling` or `$time-handling`.
2. **The owned job.** No neighbor owns it: `diagnose` hunts an unknown cause (here the hazard class is known); `migration-safety` runs schema changes, not representation choices; `regex-craft` would only meet time at a date-parsing pattern (compose: hand a validation regex there); `characterization-tests` pins existing behavior and already treats `now()` as volatility to isolate — it does not design the representation. Value framing: time bugs ship silently and fire twice a year (DST) or once a quarter (a user west of Greenwich gets yesterday's date) — the human is spared holding the zone/offset/DST rules in mind and auditing that the boundary cases were actually exercised.
3. **Mixed skill — bar per part.** Firm (trust): the identify-the-time-model gate, the three-representation classification (instant / zoned wall-clock / plain date), the hazard scan, the executed boundary table with both honest states, the scoped verdict vocabulary. Provoked (judgment): which representation each value in THIS domain actually is (an appointment is not a log timestamp), what this stack's libraries really do at a DST gap, which boundaries (DB, JSON, queue) this data actually crosses — forcing questions, never a filled template.
4. **Shape — the forcing pass**, in order: (a) **Identify the stack's time model FIRST** (the identify-the-engine analogue — required): the language and library semantics in play (Python naive-vs-aware `datetime` and what `datetime.now()` returns; JavaScript `Date` as a UTC-epoch instant that only *renders* locally; Java's `Instant`/`ZonedDateTime`/`LocalDate` split; the database's column types — in Postgres `timestamptz` stores a UTC instant and does NOT store the zone, `timestamp` stores a zoneless wall-clock; JSON has no date type at all). The same design question flips answers on the stack — state it and verify semantics on the actual versions, never from memory. (b) **Classify every value into one of three representations — the core forcing move:** an **instant** (a moment in physical time: log event, payment capture, `created_at` → store UTC / epoch, render per-viewer later); a **zoned wall-clock future event** (the 9:00 AM Monday meeting in Boston → store local time + IANA zone identifier and derive the instant at use time — converting to UTC at write time silently freezes today's DST rules and breaks when the zone's rules change or the clocks shift; this is the case where "just store UTC" is WRONG, and it is the single most-missed rule in the domain); a **plain date** (birthday, due date, expiry → a calendar date with no time and no zone; storing it as midnight-anything shifts it a day for part of the world). (c) **Scan the DST hazards** for any local-time math: nonexistent local times (the spring-forward gap — 02:30 does not occur that day; what does this library do: raise, shift, or silently pick?), ambiguous local times (the fall-back overlap — 01:30 occurs twice; which one, and is the choice explicit?), calendar-day vs 24-hour arithmetic (add-one-day ≠ add-24-hours across a transition), and recurring local-time events drifting against UTC seasonally by construction. (d) **Offset is not zone.** `+05:30` is a fact about one instant; `Asia/Kolkata` is a ruleset over history and future. Storing an offset for anything future-dated freezes DST decisions; three-letter abbreviations (`CST`, `IST`) are ambiguous across continents — IANA names only. (e) **Serialization and interchange:** ISO-8601 with explicit offset or `Z` for instants; the local-datetime-with-no-zone string is the drift bug; epoch seconds vs milliseconds mixups (a 1000× error that renders as 1970 or 55978); the JSON contract (string vs number) stated per field; round-trips must preserve the instant, not just the wall-clock digits. (f) **Clock choice:** wall clock (`now()`) for timestamps; monotonic clock for durations and timeouts — wall-clock deltas go negative or jump under NTP steps; and `now()` read more than once per logical operation is a consistency bug (read once, pass it down). (g) **Testability:** time is injected/frozen at the seam, never called ambiently where behavior depends on it — the proof table below needs a controllable clock to run at all.
5. **Prove it — the executed boundary-case table.** Rows keyed to the real stack, run where a runtime exists: the spring-forward nonexistent time (what the library actually does, observed); the fall-back ambiguous time; add-1-day vs add-24h across a transition; a round-trip through each serialization boundary preserving the instant; a plain date staying the same date for a UTC−10 and a UTC+12 viewer; the epoch-unit check at the interchange boundary. Two honest states per row set: **executed** (run in the repo's language against its actual libraries — a scratch script is enough; report observed results) or **authored, not executed** (exact run instructions; never claim it ran).
6. **Verdict vocabulary.** Exactly one of: **boundaries-hold-as-proven** (scoped to the rows run), **designed-not-yet-proven**, **gap-found-because** (a value mis-classified, a DST case unhandled, a boundary that mangles the instant). Never "timezone-safe" unqualified; the verdict never outruns the table.
7. **Modes and scope.** Applied vs advisory follows the invocation. One area: pointed at a whole codebase, narrow to the named or riskiest surface (the scheduling module, the billing timestamps) and say so.
8. **Proof boundary (the inherited floor).** Never assert what a library does at a DST edge without running it — training-data memory of library DST behavior is exactly the kind of claim that must be executed, not recalled; bound the residual (e.g., "boundary table executed on Python 3.12/zoneinfo; residual: the JS client's rendering unverified").
9. **Fences.** vs `diagnose` (unknown-cause bug vs known hazard class); vs `characterization-tests` (when available: it pins existing behavior including treating `now()` as volatility — compose: pin first, then redesign here); vs `regex-craft` (a date-format validation pattern is handed there); vs calendar-product features (recurrence UIs, availability search — product design, not representation correctness); vs `migration-safety` (executing a column-type migration this skill recommends).
10. **Done when.** Checklist mirroring the shape: stack time model identified with semantics verified; every value in scope classified into the three representations with rationale; DST gap/overlap/arithmetic cases dispositioned; zones stored as IANA names where zones are stored; each serialization boundary contracted; clock choice per use stated; time injectable at the seam; table delivered with honest per-row-set labels; one scoped verdict; advisory-until-asked held.
11. **Build-and-prune note.** Thin in this authoring repo; portable to effectively every repo. First-to-prune on observed mis-fire. Failure shapes: collapsing into a "store everything in UTC" one-liner (the exact over-simplification the skill exists to prevent — fold signal), or accreting a per-language datetime-API encyclopedia (drift, not the job).

### Step 3 — Validate structurally

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/time-handling
git diff --check
python3 -c "import yaml; d=yaml.safe_load(open('skills/time-handling/SKILL.md').read().split('---')[1]); print(d['name'], len(d['description'].split()))"
```

Then prove the description character-exact against this plan's yaml block (same comparison snippet as plan #1, paths substituted). Only the documented "unexpected key" complaint is waivable; expect zero complaints.

### Step 4 — Link and verify delivery

```bash
scripts/claude-skills-sync.sh --link time-handling
scripts/claude-skills-sync.sh --check
```

Both must exit 0.

### Step 5 — Behavior smoke test (forward test)

ONE fresh subagent; prompt = the full new `SKILL.md` as active guidance plus this scenario verbatim (no skill vocabulary): "We're building a coaching platform in Python with Postgres. Customers book a recurring Monday 9:00 AM check-in call with their coach; customers and coaches are often in different cities. After March, several customers complained their calls now happen an hour off. We also store when each booking was created, and customer birthdays for a birthday-discount feature. Work out how we should store and compute all of these before we refactor the scheduler." Grade against five pre-named behaviors: (1) the recurring 9:00 AM booking is stored as local time + IANA zone (with the instant derived at use time) and NOT as a UTC instant, with the DST reasoning stated; (2) the March complaint is correctly attributed to a DST offset shift, and the nonexistent/ambiguous local-time cases are handled explicitly; (3) the three value kinds are separated: `created_at` as a UTC instant, the recurrence as zoned wall-clock, the birthday as a plain date (not midnight-anything); (4) Postgres column reasoning is correct — `timestamptz` stores an instant, not the zone, so the zone lives in its own column; IANA names, not offsets or abbreviations; (5) a boundary-case table is delivered and — since Python is available to the subagent — at least one DST boundary row is actually executed (or every row is honestly labeled authored-not-executed with exact run instructions), and the verdict is scoped, not "timezone-safe now". Record pass/fail per behavior. 4/5 → proceed; below → tighten wording once and re-run; still below → STOP at the committed branch and report honestly.

### Step 6 — Commit and land

```bash
git add skills/time-handling
git commit -m "feat: add time-handling skill (Era-62 review Opening C, factory move #2)"
git checkout main && git merge --ff-only feature/time-handling
git branch -d feature/time-handling
git status --short --branch
```

Do NOT push. Do NOT add a ledger entry.

## Edge cases a weaker model would miss

- **"Store everything in UTC" is the domain's most dangerous half-truth.** It is correct for instants and WRONG for zoned future events: a 9:00 AM Boston meeting stored as UTC breaks when DST shifts or when the IANA rules change between write and use. The skill must state this inversion explicitly — it is the whole reason the skill out-earns a one-line rule.
- **Postgres `timestamptz` does not store a timezone.** It normalizes to UTC and renders per session; the zone must be its own column when the zone is data. A weaker author reads the type name and assumes otherwise.
- **A birthday is not a datetime.** Plain dates stored as midnight-UTC (or midnight-local) shift a day across the date line; the plain-date representation must be first-class, not a truncated instant.
- **Offset ≠ zone** (`+05:30` vs `Asia/Kolkata`), and `CST`/`IST` are ambiguous abbreviations. Future-dated anything stored with a fixed offset has silently frozen DST policy.
- **Library DST behavior must be executed, not recalled.** What Python `zoneinfo`, `pytz` (its `localize` trap), or a JS lib does at a nonexistent 02:30 differs; the proof boundary must forbid answering from memory — this is the skill's sharpest evidence-before-claims specialization.
- **Monotonic vs wall clocks:** durations measured with `now()` deltas go negative under NTP; a weaker author never mentions clock choice at all.
- **Add-1-day vs add-24-hours diverge across DST** — calendar arithmetic and duration arithmetic are different operations; naming this pair is what makes the recurrence design correct.
- **The smoke scenario must not teach the test** — it never says "DST", "IANA", "UTC", "offset", or "timezone-aware". Use it verbatim.
- **quick_validate:** only the documented "unexpected key" complaint is waivable; never delete a documented-valid field to satisfy it.

## Acceptance criteria

1. `skills/time-handling/SKILL.md` exists on `main`; frontmatter parses; description double-quoted and character-exact to this plan's yaml block.
2. `quick_validate.py skills/time-handling` passes clean; `git diff --check` clean.
3. `scripts/claude-skills-sync.sh --check` exits 0; `ls -la ~/.claude/skills/time-handling` shows a symlink into this repo.
4. The body contains: an identify-the-time-model-first gate naming that semantics are verified on the actual stack; the three-representation classification with the zoned-future-event inversion of "store UTC"; DST gap/overlap/arithmetic hazards; offset-vs-zone with IANA names; serialization round-trip and epoch-unit checks; wall-vs-monotonic clock choice; both table states; a three-term verdict vocabulary; Done-when; Build-and-prune with fold signal + encyclopedia drift.
5. Grep guards: `grep -c 'IANA' skills/time-handling/SKILL.md` ≥ 2; `grep -ci 'DST' skills/time-handling/SKILL.md` ≥ 4; `grep -ci 'monotonic' skills/time-handling/SKILL.md` ≥ 2; `grep -ci 'plain date' skills/time-handling/SKILL.md` ≥ 2; `grep -n 'rm ' skills/time-handling/SKILL.md` returns nothing.
6. Smoke test recorded: 5 behaviors, ≥4 passed, scenario plan-verbatim, fresh context.
7. Landed via `--ff-only`; branch deleted; tree clean; nothing pushed; no ledger entry.

## Out of scope

Building `money-decimal` (plan #4); calendar/recurrence product features (RRULE UIs, availability search); NTP/clock-sync infrastructure; leap-second policy beyond a passing mention if natural; editing existing skills; benchmarking; publishing.
