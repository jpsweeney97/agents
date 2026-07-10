# PLAN: Build the `authorization-design` skill

Rank: #2 of 5. The Era-62 capability review's strongest unbuilt recommendation.

## Goal

Create `skills/authorization-design/` — a dual-runtime skill that designs the access-control model for ONE resource, endpoint, or feature before (or while) it is coded: enumerate the (subject, action, resource) decisions, choose the model (RBAC/ABAC/ownership), place enforcement, close the object-level (IDOR/BOLA) gap, guarantee tenant isolation, map privilege escalation — and prove the design with a must-allow/must-deny access matrix that is executed where a running surface exists and honestly marked authored-not-executed where none does.

Authority: the frozen Era-62 review (`docs/reviews/2026-07-01-skill-library-capability-growth-review.md`, Band B) calls this "the single strongest addition available" — the design-time application-security producer the whole library lacks (OWASP #1 territory), and its §9 next-moves list puts it second only to the already-built `assumption-check`. This is a build-and-prune skill build: it does not fire unattended and wields no irreversible-effect tools, so it is NOT a charter event and gets NO ledger entry (Era-85 `assumption-check` precedent: deliberately un-ledgered).

## Files to touch

- CREATE: `skills/authorization-design/SKILL.md` (single file; no `agents/openai.yaml`, no references/ — minimal bundle like `skills/assumption-check/`).
- RUN (not edit): `scripts/claude-skills-sync.sh`.
- READ ONLY: `skills/regex-craft/SKILL.md` (the domain-producer mold — mirror its shape), `skills/assumption-check/SKILL.md` (freshest minimal build), `skills/agent-facing-design/SKILL.md` and `skills/skill-ux-design/SKILL.md` (the authoring gates — consult before writing), `AGENTS.md` (Skill Editing + Validation Ladder sections).

## House rules (apply throughout)

- Branch first: `git checkout -b feature/authorization-design` before creating any file (a hook blocks edits on `main`).
- Never `rm`; use `trash`. Never push; no PRs; do not touch `plugins/`, the Codex cache, or the mirror — `skills/` is served in place.
- Markdown: one logical line per paragraph/bullet; no hard wrapping.
- Frontmatter description contains colons → it MUST be double-quoted.
- Name check (already done, verify anyway): `authorization-design` collides with no Codex-bundled (`openai-docs`, `skill-creator`, `skill-installer`, `plugin-creator`, `imagegen`, `pdf`, `doc`, `codex-primary-runtime`) or Claude-bundled (`code-review`, `debug`, `loop`, `claude-api`, `run`, `verify`, `security-review`) name.
- Dual-runtime text: name both invocation tokens (`/authorization-design` or `$authorization-design`); phrase any routing to Claude-only or plugin skills availability-conditionally ("when `review-family:scrutinize` is available" style).

## Implementation order

### Step 1 — Read the mold and the gates

Read `skills/regex-craft/SKILL.md` end to end — the new skill mirrors its skeleton: frontmatter → one-line summary + invocation → The owned job → Mixed skill (bar per part) → Shape (the forcing pass) → Modes and scope → Proof boundary → Fences → Done when → Build-and-prune note. Then read the two gate skills and the AGENTS.md Skill Editing rules.

### Step 2 — Write `skills/authorization-design/SKILL.md`

Use this description verbatim (63 words, within tolerance of the soft 25–60 budget; quoted):

```yaml
---
name: authorization-design
description: "Use when designing or vetting the access-control model for one resource, endpoint, or feature — who may do what to which objects: enumerate subject-action-resource decisions, choose RBAC/ABAC/ownership, place enforcement, close object-level (IDOR/BOLA) and tenant-isolation gaps, map privilege escalation, and prove it with a must-allow/must-deny access matrix. Not for login/session/token mechanics (authentication), attacker modeling (red-team), or a repo-wide vulnerability sweep."
---
```

Body requirements, section by section (author real prose in the house voice — study the mold; do not copy regex-craft sentences):

1. **Summary + invocation.** One paragraph: designs the authorization layer for one scoped surface, proves it with an access matrix, advisory-until-asked. Invocation: `/authorization-design` or `$authorization-design`.
2. **The owned job.** Why no neighbor owns it: `red-team` models attacker intent across a system and renders no verdict; `system-design-review` reviews trust surfaces at architecture altitude, not one endpoint's decision table; `implementation-review` needs a spec plus a diff; a repo-wide sweep is the parked security-audit's job (or the bundled `security-review` where that runtime ships it) — none designs one surface's access model with an executed proof. State the value: an authorization hole costs an account takeover or cross-tenant leak at run time; the human is spared composing the checklist and auditing that no class was skipped.
3. **Mixed skill — bar per part.** Firm (trust): the five-part hazard scan (model choice, enforcement placement, object-level, tenant isolation, escalation), the must-allow/must-deny matrix with both honest states (executed vs authored-not-executed), the fail-closed default, the scoped verdict vocabulary. Provoked (judgment): which model actually fits this domain's sharing semantics, where enforcement really belongs in this stack, which deny cases are the live bypasses here — forcing questions keyed to this surface, never a template filled to feel done.
4. **Shape — the forcing pass.** In order: (a) **Pin the surface and the subjects** — the one resource/endpoint/feature, every subject class that can reach it (including service accounts, background jobs, and admin tooling — the callers a happy-path list forgets). (b) **Enumerate subject-action-resource decisions** — the concrete triples, including partial access (read-own vs read-any, field-level visibility). (c) **Choose the model and say why** — RBAC (stable role set), ABAC (attribute/relationship rules), plain ownership, or a hybrid; the wrong-fit smell is roles multiplying to encode relationships. (d) **Place enforcement** — the layer where the check runs (route guard, service layer, query predicate, DB row-level security), fail-closed on missing/unknown, and the rule that object-level and tenant checks live in the data access path, not only the route. (e) **Close the object-level gap** — role checks alone still let any authenticated user read another user's record by ID (IDOR/BOLA); every by-ID access needs an ownership/membership predicate. (f) **Tenant isolation** — tenant scoping in every query predicate, not just the URL. (g) **Map escalation** — who assigns roles, who can grant grants, horizontal (peer-to-peer data) vs vertical (user-to-admin) paths.
5. **Prove it — the access matrix.** A table of concrete cases: each row subject × action × object-instance → MUST-ALLOW or MUST-DENY, with the deny rows carrying the interesting cases (cross-user object ID, cross-tenant ID, role without ownership, unauthenticated, deactivated user, the escalation attempt). Two honest states, stated per row set: **executed** (a running surface exists — run the checks as tests or real requests and report observed results) or **authored, not executed** (design-time — deliver the matrix with exact execution instructions for the implementer; never claim it ran). A matrix with no deny rows is a reassurance ritual, not a proof.
6. **Verdict vocabulary.** Exactly one of: **enforced-as-proven** (matrix executed, every row observed as specified — scoped to the rows run), **designed-not-yet-proven** (matrix authored, execution pending), **gap-found-because** (a must-deny case allows, or a class has no decision). Never "secure"; never a certificate beyond the rows in the table.
7. **Modes and scope.** Applied vs advisory follows the invocation (live code → edits plus executed matrix on a working branch; design/review → the advisory pack). One surface: pointed at a whole app, narrow to the named or riskiest surface and say so.
8. **Fences.** vs authentication: login flows, sessions, tokens, MFA, password policy are OUT — this skill starts after identity is established (say "authentication design is a neighboring job this skill does not own" — do NOT name `auth-session-design`, it does not exist). vs `red-team` (attacker modeling, no verdict — compose: red-team findings feed matrix deny rows). vs `system-design-review` (architecture altitude). vs the parked security-audit / repo sweeps. vs `contract-change-propagation` (changing an existing authz contract's consumers).
9. **Done when.** Checklist mirroring the shape: surface pinned; triples enumerated including non-human subjects; model chosen with rationale; enforcement placed fail-closed; object-level and tenant predicates specified; escalation mapped; matrix delivered with deny rows, each row set honestly marked executed or authored; one scoped verdict rendered; advisory-until-asked held.
10. **Build-and-prune note.** Thin in this authoring repo; value is portable to every repo with multi-user resources; judged by leverage + offload. First-to-prune on observed mis-fire. Failure shapes to watch: collapsing into a generic "add role checks" template (fold signal toward `implementation-review`), or accreting a per-framework authz-syntax encyclopedia.

### Step 3 — Validate structurally

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/authorization-design
git diff --check
python3 -c "import yaml,sys; d=yaml.safe_load(open('skills/authorization-design/SKILL.md').read().split('---')[1]); print(d['name'], len(d['description'].split()))"
```

quick_validate must pass. The ONLY acceptable complaint to waive is "unexpected key" for `argument-hint`/`disable-model-invocation` (not used here, so expect zero complaints); any other failure is real — fix it.

### Step 4 — Link and verify delivery

```bash
scripts/claude-skills-sync.sh --link authorization-design
scripts/claude-skills-sync.sh --check
```

Both must exit 0.

### Step 5 — Behavior smoke test (forward test)

Spawn ONE fresh subagent (or `claude -p` headless). Its prompt: the full text of the new `SKILL.md` framed as active guidance ("You have this skill loaded; follow it."), plus a realistic scenario written WITHOUT the skill's vocabulary — e.g.: "Our Express app has GET/PUT `/api/invoices/:id` and a new `/api/admin/users` page. Any logged-in user gets a JWT. Design how we should control who can see and edit what before we build more. Multi-company customers share the deployment." Grade the transcript against five pre-named behaviors: (1) enumerated subject-action-resource decisions including a non-human/admin caller; (2) named the object-level (by-ID cross-user) gap; (3) tenant isolation placed in the query path; (4) produced a matrix containing MUST-DENY rows; (5) marked the matrix authored-not-executed (no running surface) and rendered a scoped verdict, not "secure". Record pass/fail per behavior. 4/5 or better → proceed. Below that → tighten the SKILL.md wording that failed (once) and re-run. Still below → STOP at the committed branch and report honestly; do not land.

### Step 6 — Commit and land

```bash
git add skills/authorization-design
git commit -m "feat: add authorization-design skill (Era-62 review Band B, move #2)"
git checkout main && git merge --ff-only feature/authorization-design
git status --short --branch
```

Do NOT push. Do NOT add a ledger entry.

## Edge cases a weaker model would miss

- **Authored-vs-executed is the skill's honesty core.** At design time there is often nothing to run; the trap is writing a skill that either demands execution that can't happen or lets "executed" be claimed for an eyeballed table. Both states must be first-class and labeled per the proof-boundary discipline (see `regex-craft`'s "never assert a result you did not run").
- **Deny rows are the proof.** An access matrix of allow cases only always passes; the value is the must-DENY set (cross-user ID, cross-tenant, role-without-ownership). Make the skill text say a matrix without deny rows is a defect.
- **IDOR is object-level, not endpoint-level.** A weaker author writes "check the user's role on the route" — which passes while any authenticated user reads `/invoices/17` belonging to someone else. The ownership predicate on the object lookup is the named gap this skill exists to close.
- **Do not route to skills that don't exist.** No `auth-session-design`, no `injection-safe-inputs` reference unless it exists at execution time (it is plan #3 of this queue — check `ls skills/` and only name it if present).
- **The smoke-test scenario must not teach the test.** If your scenario contains "IDOR", "must-deny matrix", or "tenant isolation", the pass is fake. Describe the situation; let the skill supply the discipline.
- **`security-review` exists as a Claude-bundled skill** — the description's sweep boundary keeps misroutes away from it without claiming it exists on Codex (phrase availability-conditionally in the body).
- **quick_validate's schema lags Claude Code**: treat only the documented "unexpected key" complaint as waivable; never "fix" a validator complaint by deleting a documented-valid field.

## Acceptance criteria

1. `skills/authorization-design/SKILL.md` exists on `main`; frontmatter parses (`python3 -c "import yaml,..."` above prints the name); description is quoted and matches the Step-2 text.
2. `quick_validate.py skills/authorization-design` passes clean.
3. `scripts/claude-skills-sync.sh --check` exits 0 and `ls -la ~/.claude/skills/authorization-design` shows a symlink into this repo.
4. The body contains: an owned-job section fencing `red-team`, `system-design-review`, and repo sweeps; both matrix states (executed / authored-not-executed); a three-term verdict vocabulary excluding "secure"; a Done-when checklist; a build-and-prune note naming its fold signal.
5. Grep guards: `grep -c 'must-deny\|MUST-DENY' skills/authorization-design/SKILL.md` ≥ 2; `grep -i 'auth-session-design' skills/authorization-design/SKILL.md` returns nothing; `grep -n 'rm ' skills/authorization-design/SKILL.md` returns nothing.
6. Smoke test recorded in the final report: 5 behaviors, ≥4 passed, scenario text included, run on a fresh context.
7. Landed on `main` via `--ff-only`; working tree clean; nothing pushed; no ledger entry added.

## Out of scope

Authentication/session/token design; building `injection-safe-inputs` (separate plan); editing any existing skill; benchmarking; publishing.
