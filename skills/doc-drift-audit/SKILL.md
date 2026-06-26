---
name: doc-drift-audit
description: "Use when the user wants to audit whether a documentation set (README, API/reference docs, CLI or config docs) still matches the code it describes — checking that the symbols, paths, signatures, endpoints, config keys, and flags named in prose still resolve against the current code tree, surfacing only high-confidence stale references and routing fixes to `/triage`. Read-only; detects, never edits or fixes. Not for resolving which source-of-truth governs a claim (`baseline`), driving the fix when intent changed (`spec-drift-reconcile`), a scored debt audit (`tech-debt-scan`), or checking runtime behavior (`verify`/`behavior-smoke-test`)."
---

# Doc Drift Audit

Audit a documentation set against the code it describes: extract the checkable references prose makes — symbols, paths, signatures, endpoints, config keys, CLI flags — verify each resolves against the current tree at a pinned commit, and report only high-confidence misses. Read-only; it detects drift and routes the fix, never makes it. Invocation: `/doc-drift-audit` or `$doc-drift-audit`.

The cardinal honesty, stated once and repeated every run: **CLEAN means the references resolve, not that the docs are accurate.** This audit verifies that a doc's *nouns exist*, never that its *verbs are true* — a doc can name every symbol correctly and still lie about what the code does. That blind spot is the price of being deterministic and low-false-positive; the mandatory disclaimer below is how it stays honest about it.

## Core contract

Every run takes a bounded doc set and a code referent, resolves each checkable reference to a **high-confidence miss** or a **could-not-verify**, and produces one read-only audit. False negatives are acceptable; **false positives are the cardinal sin** — a mechanical audit that cries drift on a resolved-but-indirect reference destroys the trust that is its whole product. When in doubt, it lists the reference under coverage, never as a finding. It edits nothing, commits nothing, and routes actionable drift to `/triage`.

## Drift from what — the referent

Drift is measured against the **deterministic source-of-truth that governs each token's class**, at a recorded `HEAD` SHA. Most tokens reduce to "does this resolve in the code/manifest at this commit?":

- **Symbols, signatures, import/module paths** → the code tree (prefer a language server or AST query; `rg` is the deterministic floor).
- **File and directory paths** → the filesystem at the commit.
- **API endpoints** (method + route literal) → route definitions in the code.
- **Config keys, env vars** → the code plus config/manifest schema.
- **CLI commands, subcommands, flags** → the arg parser / generated help.
- **Version pins** → the manifest (`package.json`, `pyproject.toml`, …), never source.
- **Release-state claims** → `CHANGELOG`. **Ownership claims** → `CODEOWNERS`.

A reference has **drifted** when its literal token no longer resolves against that source *and* a strong multi-probe search has ruled out the benign explanations. The audit sees **disagreement, not direction**: a finding says the doc and the code disagree with high confidence — never that the code is right and the doc is wrong.

## Scope: what is checkable

**In** — assertions that reduce to "does this literal token exist / match at this commit?": symbols, paths, signatures (lower-confidence tier — only when the definition is found *and* the mismatch is unambiguous), endpoints, config/env keys, CLI flags, import paths, and the named symbols *inside* code examples (verify they exist; never execute the example).

**Out** — and surfaced-and-routed, never silently dropped: behavioral/semantic claims ("returns sorted", "retries 3×"), rationale and intent prose, conceptual narrative, and soft counts/versions/dates. These go to verification (`verify`, `behavior-smoke-test`) or intent reconciliation (`spec-drift-reconcile`), not here.

## Verifying a reference

Never call drift on a single `rg`. For a reference that does not resolve directly, probe in order and stop at the first hit (→ resolved, not reported):

1. Exact / word-boundary search (`rg -w`, `rg -F`).
2. Definition-site search (`def name` / `function name` / `class name` / `const name`, language-appropriate).
3. Alias / re-export search (exported under another module, re-exported, aliased).
4. **Import / external resolution** — if the token resolves to an imported, vendored, or third-party symbol (a `DataFrame`, an HTTP-client call), it is out-of-tree → **resolved, never drift**. This gate is load-bearing: without it, ubiquitous library tokens fall through to a false miss.
5. Generated / vendored exclusion (`generated/`, `vendor/`, `node_modules/`, `dist/`, `build/`, an uncovered monorepo package) → **could-not-verify**, never drift.
6. String-key / case-variant search (config keys and flags often appear only as string literals).

A reference is reported **only if every reasonable probe fails.** Apply a **distinctive-token gate**: never report drift on a common word (`run`, `data`, `config`, `get`) — ambiguity is could-not-verify. Record the exact command(s) per finding so the verdict is reproducible.

## Output

**Artifact** — default `docs/audits/YYYY-MM-DD-<target-slug>-doc-drift-audit.md` (co-tenant with `tech-debt-scan`, distinct suffix; no collision). If `AGENTS.md`/`CLAUDE.md` names a different audit home, follow it. Run `git status` before writing; never overwrite unrelated dirty state; if the path cannot be written, fall back to a chat-only report and label the missing artifact a proof limit. **Leave it uncommitted** — this is point-in-time evidence, not durable authority.

Sections:

- **Header** — doc set; code referent + `HEAD` SHA; date; reference classes in scope; the cardinal-honesty sentence; `Status` (`draft` while sweeping → `complete` after coverage passes).
- **Findings** — ranked by **reader-harm** (a wrong copy-pasteable flag, command, or endpoint outranks a stale internal-symbol mention), then grouped by doc file. Each: doc `path:line` + the quoted reference; class; the probes run (exact commands); the code reality ("not found"; or "renamed to X" / "moved to Y" when a near-match is evident); and a one-line **suggested correction, not applied**.
- **Coverage** — doc files swept vs skipped; classes covered; the **could-not-verify** list with reasons; and the **routed-out worklist** of behavioral/intent claims worth a human or a verification lane, with where-to-check pointers.
- **Reproduce** — `HEAD` SHA + commands, so a future run is identical.

This artifact uses its **own binary finding shape** — it does **not** import `tech-debt-scan`'s severity/leverage/effort rubric, because drift findings are facts, not scored debt.

**Mandatory disclaimer, every run** (artifact header and chat): *"CLEAN means references resolve, not that the docs are accurate; behavioral and intent claims were not verified here."* Without it, a clean verdict is actively misleading. Report counts as **"K of M anchorable claims drifted,"** never "docs accurate" — a claim with no distinctive token is silently never checked, so the count is over the *anchorable* claims, and coverage names what was and was not swept.

**Chat summary** (executive only): the top reader-harm misses, total drift count, coverage limits (files swept, classes covered, could-not-verify count), the artifact path, and the `/triage` pointer.

## Workflow

`Frame → Inventory → Extract → Verify → Rank → Deliver → Route`

1. **Frame** — name the doc set, the code referent and its `HEAD` SHA, the classes in scope, the FP boundary, the artifact path, and the read-only stance, in a one-line opener. Ask only if the doc set or the code root is genuinely ambiguous.
2. **Inventory** — enumerate docs in scope; if "the docs" is vague, default to `README` + `docs/` and name what was excluded.
3. **Extract** — pull checkable references by class, keeping `path:line` for every one.
4. **Verify** — run the probe ladder; high-confidence miss or could-not-verify; record commands.
5. **Rank** — collect confident misses, order by reader-harm, group by file; route behavioral/intent claims to the worklist; uncertain references to coverage.
6. **Deliver** — write the artifact (uncommitted) + chat summary, carrying the mandatory disclaimer.
7. **Route** — send actionable drift to `/triage` (or `$triage`) — one issue per doc-file cluster — and stop. The skill never opens issues itself.

## Boundaries — read-only, detect-only

- Never edit docs or code; never stage, commit, or push; leave the artifact uncommitted. Defer any branch or landing concern to the repo's protected-branch floor and `git-cycle`; do not re-inline that apparatus.
- **No adjudication of correctness.** A finding asserts disagreement, not which side is wrong. The doc may faithfully document a live bug — in that case the fix is a code/config issue; route it as one, do not edit the doc to match.
- **No remediation.** Fixing is a separate, user-requested step. "Intent moved, the whole chain is stale" → `spec-drift-reconcile`. "Which authority even governs this contested claim?" → `baseline` first.

## Done when

- Every extracted checkable reference is a high-confidence miss or is listed under coverage as could-not-verify.
- Findings are ranked by reader-harm; the artifact carries the header (with `HEAD` SHA), findings, coverage, the mandatory disclaimer, and reproduce.
- Behavioral/intent claims are surfaced-and-routed, not silently dropped.
- Actionable drift is routed to `/triage`; nothing was edited, staged, or committed.

## Fence

- vs `baseline`: `baseline` **resolves** which source-of-truth governs a claim and explicitly declines the systematic sweep; `doc-drift-audit` **presupposes** the referent (code is the projection source) and runs the sweep `baseline` refuses. Unsure code is even the right authority (maybe the doc *is* the spec) → `baseline` first; any contested authority surfaced here routes to it, never adjudicated.
- vs `spec-drift-reconcile`: it is intent-anchored and **fixes** (drive the downstream change); this is code-anchored and **detects** (existing docs vs current code) and stops at `/triage`.
- vs `tech-debt-scan`: scored, prioritized debt with a severity rubric; this emits binary reference misses ranked only by reader-harm. "Where's our worst debt?" → `tech-debt-scan`. "Which doc references are factually stale against code?" → here.
- vs `contract-change-propagation`: it is change-anchored (a proposed interface delta → which consumers break, in what order); this is standing-state (no change supplied, existing docs vs current code).
- vs `verify` / `behavior-smoke-test`: they execute to check behavior; this never executes — it checks that named references *resolve*, not that the code *behaves* as documented.
- In **this** repo: the five SessionStart canaries + `scripts/check-library-integrity.sh` own the structural skill-wiring slice (name==dir, self-referenced paths, orphans, parse); `doc-drift-audit` defers that and audits only content claims (prose vs code).

## Build-and-prune note

Locally **first-to-prune**: a skill-library's prose carries few hard code symbols, and the canaries plus `check-library-integrity.sh` already own the structural slice, so content-claim drift is thin here. The real value is **portable** — code-heavy repos with READMEs, API/reference docs, and CLI/config docs that rot against a moving codebase. Build it because it is cheap to try and clean to remove; judge it by whether it fires usefully when pointed at a code-heavy repo, and prune without ceremony if it does not.
