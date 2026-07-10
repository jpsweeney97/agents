# PLAN: Build the `injection-safe-inputs` skill

Rank: #3 of 5. The design-time sibling of `authorization-design` (Era-62 review, Band B).

## Goal

Create `skills/injection-safe-inputs/` — a dual-runtime skill that designs untrusted-input handling for ONE trust boundary: identify every sink the input reaches (SQL, shell/process, path, HTML/JS, template, LDAP), apply the sink-correct defense (never generic "sanitization"), cover mass assignment and unsafe deserialization, set size/type limits, and prove the design with a must-block / must-pass payload table — executed where a running surface exists, honestly marked authored-not-executed where none does.

Authority: the frozen Era-62 review (`docs/reviews/2026-07-01-skill-library-capability-growth-review.md`, Band B) names this the sibling of its strongest addition (OWASP #3 territory), §9 move #2. Build-and-prune: not unattended, no irreversible-effect tools → NOT a charter event, NO ledger entry.

## Files to touch

- CREATE: `skills/injection-safe-inputs/SKILL.md` (single file, minimal bundle).
- RUN: `scripts/claude-skills-sync.sh`.
- READ ONLY: `skills/regex-craft/SKILL.md` (mold), `skills/authorization-design/SKILL.md` IF plan #2 already landed (sibling consistency), `skills/agent-facing-design/SKILL.md`, `skills/skill-ux-design/SKILL.md`, `AGENTS.md` (Skill Editing + Validation Ladder).

## House rules (apply throughout)

- Branch first: `git checkout -b feature/injection-safe-inputs` before creating any file (a hook blocks edits on `main`).
- Never `rm`; use `trash`. Never push; no PRs; do not touch `plugins/`, the Codex cache, or the mirror.
- Markdown: one logical line per paragraph/bullet.
- Quoted frontmatter description (it contains colons).
- Dual-runtime: name both tokens (`/injection-safe-inputs` or `$injection-safe-inputs`); availability-conditional phrasing for single-runtime neighbors.
- Name collides with no bundled skill (verify against the lists in AGENTS.md Skill Layout).

## Implementation order

### Step 1 — Read the mold and gates

Same as the sibling plan: `regex-craft` for the skeleton (owned job → mixed bars → forcing pass → proof → fences → done-when → build-and-prune note), the two gate skills, AGENTS.md Skill Editing.

### Step 2 — Write `skills/injection-safe-inputs/SKILL.md`

Description, verbatim (quoted):

```yaml
---
name: injection-safe-inputs
description: "Use when designing or vetting how one trust boundary handles untrusted input — a request body, upload, webhook, query param, or file path: identify every sink the input reaches (SQL, shell, path, HTML/JS, template, LDAP), apply the sink-correct defense, cover mass assignment, deserialization, and size/type limits, and prove it with a must-block/must-pass payload table. Not for hardening one regex (regex-craft), LLM prompt injection, or a repo-wide vulnerability sweep."
---
```

Body requirements (real prose in house voice, mirroring the mold's rhythm):

1. **Summary + invocation.** One trust boundary, sink-first, proven by an executed payload table; advisory-until-asked.
2. **The owned job.** No neighbor designs one boundary's input handling: `regex-craft` hardens one pattern (compose: a validation regex this skill specifies is handed there); `implementation-review` needs spec+diff; `red-team` models intent, no verdict; repo-wide sweeps are the parked security-audit / `tech-debt-scan` backlog. Value: an injection that ships is an RCE or data exfiltration at run time; the human is spared composing the sink checklist and auditing that no sink was missed.
3. **Mixed skill — bar per part.** Firm (trust): the sink census gate (defenses are chosen per sink, so an unidentified sink is an unguarded one), the sink-correct defense table, the mass-assignment/deserialization/limits scan, the executed must-block AND must-pass table, the two honest proof states, the scoped verdict. Provoked (judgment): which sinks this input actually reaches (including second-order ones — stored now, rendered later), whether a defense belongs at this boundary or the sink side, what the realistic bypass classes are for this stack.
4. **Shape — the forcing pass.** (a) **Pin the boundary** — the one entry point and the data's full downstream path; trace where it is stored, logged, rendered, executed, or passed on (second-order/stored injection is found here, not at the entry). (b) **Census the sinks** — for each downstream use, name the sink class: SQL/NoSQL query, shell or process invocation, filesystem path, HTML/JS render context, template engine, LDAP/directory query. An input that reaches no sink needs limits only. (c) **Sink-correct defense, named per sink** — SQL: parameterized queries/prepared statements, never string-building, never escaping-as-primary; shell: argument arrays with shell=false, never string interpolation into a command line; path: canonicalize FIRST then enforce an allowlisted base-directory prefix (decode/normalize before the check, or `%2e%2e%2f` and symlinks walk past it); HTML/JS: context-aware output encoding at render time (the sink side), plus framework auto-escaping left ON; template: user input as data only, never concatenated into template source (SSTI); LDAP: the engine's escaping API. The rule to state plainly: **validation supplements, defenses replace** — an allowlist check is a good filter, but parameterization is what removes the vulnerability class. (d) **The boundary trio** — mass assignment (bind allowlisted fields only, never object-splat request bodies into models), unsafe deserialization (never `pickle`/`ObjectInputStream`/`yaml.load` on untrusted bytes; safe loaders or plain data formats), size/type/encoding limits declared at the boundary (length caps, content-type checks, reject-don't-truncate).
5. **Prove it — the payload table.** Concrete cases in two mandatory halves: **must-block** — per identified sink, the classic payload plus one bypass-class variant (`' OR 1=1--`, `; rm x`-shaped argument, `../../etc/passwd` AND its URL-encoded form, `<img onerror=...>`, `{{7*7}}`, a splatted `role=admin` field, an oversized body); **must-pass** — realistic benign inputs that overzealous filtering breaks (`O'Brien`, a path containing spaces, prose containing `<` or `{{`). Over-blocking is a correctness regression, not safety. Two honest states per row set: executed (run against the real surface, observed results reported) or authored-not-executed (design-time; exact execution instructions delivered). Keep the table sampled-and-said: it proves the rows run, never "injection-proof".
6. **Verdict vocabulary.** Exactly one of: **defended-as-proven** (table executed, scoped to its rows), **designed-not-yet-proven**, **gap-found-because** (a must-block passed, a must-pass blocked, or a sink has no named defense). Never "sanitized", never "injection-proof".
7. **Modes and scope.** Applied vs advisory follows the invocation; one boundary — pointed at a whole app, narrow to the named or riskiest boundary and say so.
8. **Fences.** vs `regex-craft` (one pattern, engine-first, executed regex proof — this skill may specify a validation pattern and hand its hardening there); vs `red-team`; vs repo sweeps (parked security-audit; the bundled `security-review` where that runtime ships it); LLM prompt injection is a deliberately unowned neighbor — do NOT claim it or route it to a named skill (none exists; the Era-62 review contains that AI sub-cluster: do not populate it).
9. **Done when.** Boundary pinned with the full downstream path; every sink censused and given its named sink-correct defense; the trio (mass assignment, deserialization, limits) dispositioned; payload table delivered with both halves, each row set marked executed or authored; one scoped verdict; advisory-until-asked held.
10. **Build-and-prune note.** Thin here, portable everywhere inputs cross trust lines; first-to-prune on mis-fire. Failure shapes: collapsing into a generic "escape your inputs" lens (fold signal), or accreting a per-framework payload encyclopedia (the mold's named drift).

### Step 3 — Validate structurally

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/injection-safe-inputs
git diff --check
```

Pass required; only the documented "unexpected key" complaint is waivable (expect none).

### Step 4 — Link and verify delivery

```bash
scripts/claude-skills-sync.sh --link injection-safe-inputs
scripts/claude-skills-sync.sh --check
```

Both exit 0.

### Step 5 — Behavior smoke test

One fresh subagent (or `claude -p`), the new SKILL.md as active guidance, scenario WITHOUT skill vocabulary — e.g.: "We're adding a report-builder endpoint: users POST a JSON body with a title, some filter values, and an optional filename to save as; the server queries Postgres with those filters, writes a CSV to a reports directory under that filename, and later shows the title on a shared dashboard page. What should we do to handle this input safely before we ship it?" Grade five behaviors: (1) traced the downstream path and identified ≥3 sinks (SQL, path, HTML render) including the stored/rendered-later one; (2) named parameterized queries (not escaping) for SQL; (3) canonicalize-then-allowlist for the filename, catching the encoded traversal variant; (4) produced a payload table with BOTH must-block and must-pass halves; (5) marked the table authored-not-executed and rendered a scoped verdict (no "injection-proof"). 4/5 → proceed; one tighten-and-rerun allowed; otherwise stop at branch and report.

### Step 6 — Commit and land

```bash
git add skills/injection-safe-inputs
git commit -m "feat: add injection-safe-inputs skill (Era-62 review Band B, move #2 sibling)"
git checkout main && git merge --ff-only feature/injection-safe-inputs
git status --short --branch
```

No push. No ledger entry.

## Edge cases a weaker model would miss

- **Encode at the sink, not the entry.** The classic wrong design is HTML-encoding at input time — it corrupts data for every non-HTML sink and still misses contexts. Output encoding is sink-side; the skill text must place it there explicitly.
- **Escaping is not the SQL defense.** A weaker author writes "escape quotes"; the skill must rank parameterization as the class-removing defense and escaping as legacy fallback at best.
- **Canonicalize before the path check.** Checking for `../` before decoding/normalizing is a bypass (`%2e%2e%2f`, double-encoding, symlinks). Order is the content.
- **Must-pass rows are half the proof.** A table of only attack payloads rewards over-blocking; `O'Brien` breaking is a real regression. Both halves mandatory.
- **Second-order injection.** Input that is stored now and rendered/queried later still reaches the sink; the boundary trace must follow the data, not stop at the request handler.
- **Do not absorb LLM prompt injection.** The Era-62 review explicitly contains the AI sub-cluster ("resist adding more until a concrete unowned job surfaces"). One boundary line in the description, no routing target named.
- **Sibling consistency without dependency.** If `authorization-design` landed first, align verdict-vocabulary style (three terms, scoped, two proof states) — but this skill must stand alone if it lands first; never reference the sibling as a prerequisite.
- **Smoke scenario hygiene**: no "injection", "sink", "parameterized", or "traversal" in the scenario text — symptoms and situation only.

## Acceptance criteria

1. `skills/injection-safe-inputs/SKILL.md` on `main`; frontmatter parses; description quoted and matches Step 2.
2. `quick_validate.py` passes clean; `git diff --check` clean.
3. `claude-skills-sync.sh --check` exits 0; `~/.claude/skills/injection-safe-inputs` is a symlink into the repo.
4. Body contains: sink census as a gate; per-sink named defenses including canonicalize-then-check ordering; the mass-assignment/deserialization/limits trio; a two-half payload table with two honest states; three-term verdict vocabulary; fences for `regex-craft`, `red-team`, sweeps, and the unclaimed LLM boundary; a build-and-prune note naming both failure shapes.
5. Grep guards: `grep -ci 'must-pass' skills/injection-safe-inputs/SKILL.md` ≥ 2; `grep -i 'prompt-injection-defense' skills/injection-safe-inputs/SKILL.md` returns nothing (the boundary is named as unowned, not routed to a nonexistent skill); `grep -in 'injection-proof' skills/injection-safe-inputs/SKILL.md` hits only in the never-say-this context.
6. Smoke test: 5 behaviors, ≥4 passed, fresh context, scenario recorded.
7. Landed via `--ff-only`; tree clean; nothing pushed; no ledger entry.

## Out of scope

Regex hardening (route to `regex-craft`); authorization (sibling skill); LLM prompt injection; editing existing skills; sweeps; publishing.
