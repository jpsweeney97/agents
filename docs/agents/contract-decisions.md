# Contract Decisions

Ledger required by the charter's Decision Record section (`charter.md`): one
entry per admission, fold, rejection, park, or retirement — date, surface,
outcome, evidence pointer, and the reopen trigger for parks. Append new
entries; do not rewrite settled ones.

## Decisions

- 2026-06-12 — superpowers (pass 1): folded into `tdd` (+`mocking.md`),
  `diagnose`, `behavior-smoke-test`, and a global evidence-before-claims rule;
  admitted `design-exploration`, `implementation-planning`, `execute-plan`;
  requesting-review meta-skill rejected (collides with review lanes;
  checkpoint habit folded into `closeout-check`). Plugin removed. Evidence:
  commits `360fc77`, `966f903`, `d7351ec`.
- 2026-06-12 — commit-commands (pass 2): folded `[gone]` deletion-candidate
  discipline and a squash-merge proof path into `git-hygiene`;
  `commit`/`commit-push-pr` rejected (one-message/no-review mandates weaker
  than house discipline). Plugin removed. Evidence: commit `3b4cbc1`.
- 2026-06-12 — pr-review-toolkit + code-simplifier rider (pass 3): folded
  error-suppression and test-inadequacy lenses into `implementation-review`
  (review-family 0.3.2) and a clarity-over-brevity guardrail into
  `simplify-code`; six agent lanes rejected (numeric confidence/criticality
  scoring is rejected machinery; foreign CLAUDE.md leakage). Both plugins
  removed. Evidence: commit `5f64a54`.
- 2026-06-12 — feature-dev (pass 4): folded exploration grounding into
  `design-exploration` (read subagent-named key files first-hand before
  designing); command and three agents rejected (lane decomposition owns the
  workflow; settled no-numeric-confidence precedent). Plugin removed.
  Evidence: commit `2dc1b95`.
- 2026-06-12 — hookify (pass 5): zero folds — engine adjudicated capability
  tooling (charter-exempt as a category) but removed as unused; all six
  contract surfaces rejected (runtime-bundled `update-config` owns hook-backed
  automation). Plugin removed. Evidence: handoff
  `2026-06-12_18-35-34_feature-dev-hookify-mined-charter-amended-audit-reopens.md`.
- 2026-06-12 — discard audit (after the route-absence amendment, `6f7833d`):
  reopened two prior rejections — comment-accuracy lens folded into
  `implementation-review` (review-family 0.3.3, commit `1d0091a`);
  `friction-to-guards` admitted Claude-only in `skills-claude/` (commit
  `a5e6642`). All other prior discards held.
- 2026-06-12 — gh-address-comments: admitted (owns PR-comment addressing
  without publish authority); authoring deferred, tracked as
  jpsweeney97/agents#2.
- 2026-06-12 — frontend-design (pass 6): zero folds — the sole contract
  surface (a 41-line web-frontend aesthetics SKILL.md) parked rather than
  admitted. No local lane owns web-frontend aesthetic guidance, but the job
  has no observed work: installed since 2025-12-17 with zero invocations
  across all session transcripts (search pattern control-verified against
  known-invoked skills), no web-frontend stack in any project directory
  (lyrics-software is native SwiftUI), and zero inbound routes from curated
  contracts. Plugin removed; source recoverable in the claude-plugins-official
  marketplace catalog.
- 2026-06-12 — claude-code-setup (pass 7): zero folds — the sole skill
  (`claude-automation-recommender` + five reference files) rejected. The job
  decomposes entirely into owned lanes: feature/setup questions →
  runtime-bundled `claude-code-guide` + local `claude-code-docs`; hook and
  settings implementation → runtime-bundled `update-config` (settled pass 5);
  permission allowlists → runtime-bundled `fewer-permission-prompts`;
  automation-worthiness → the charter's admission test + `friction-to-guards`;
  skill authoring → `skill-creator`. Its speculative codebase-signal
  recommendation method contradicts the observed-friction admission standard,
  and its tables recommend reinstalling plugins this ledger already removed
  (frontend-design, hookify, commit-commands, feature-dev, pr-review-toolkit,
  code-simplifier) — running it as-is recreates resolved collisions. Friction
  looked for and not found: zero invocations since 2026-01-21 install
  (control-verified transcript search), no setup-recommendation requests in
  memory or handoffs; static Claude Code facts it carries are owned live by
  `claude-code-docs`. Plugin removed; source recoverable in the
  claude-plugins-official marketplace catalog.
- 2026-06-12 — skill-creator (pass 8): keep-with-cleanup. Bundle construction
  stays owned on Codex by the bundled copy (`~/.codex/skills/.system/`, fixed
  terrain); its do-work scripts are charter-exempt and the `quick_validate.py`
  the Validation Ladder cites resolves there. The removable third-party Claude
  plugin install (`skill-creator@claude-plugins-official`) — an eval/benchmark
  build (`run_loop`/`run_eval`/`aggregate_benchmark`/`improve_description`/
  `generate_review`; ships its own `quick_validate.py` but no `init_skill.py`/
  `generate_openai_yaml.py`) — removed under Extraction. Its authoring doctrine
  overlaps and folds into `agent-facing-design`/`writing-principles`/
  `skill-ux-design`/`behavior-smoke-test`/`scrutinize-skill` and persists in the
  Codex bundle. Its eval/benchmark capability re-authored to house standards as
  `skill-benchmark` (admitted, Claude-only in `skills-claude/`): owns
  quantitative skill benchmarking and trigger/description optimization, a job no
  local lane held (`behavior-smoke-test` is single-shot qualitative; never
  co-loads with the Codex-bundled `skill-creator`). Four inbound routes
  (`AGENTS.md` routing lane; `writing-principles` ×2; `agent-facing-design`)
  re-pointed availability-conditionally: Codex construction → bundled
  `skill-creator`; Claude construction → hand-author against the folded doctrine
  plus the Codex-bundled `quick_validate.py` via Bash (no invocable Claude-side
  constructor remains, by design). Reconciles pass-7 above: "skill authoring"
  still decomposes into an owned/fixed surface. Friction looked for and not
  found: zero failed or misrouted constructions, and the install's eval
  machinery never exercised, across two 2026-06-12 main-thread invocations that
  produced four now-live skills by hand-authoring + manual construction. Plugin
  uninstalled (`claude plugin uninstall`); source recoverable in the
  claude-plugins-official marketplace catalog. Evidence: commits `a5e6642`,
  `966f903`.
- 2026-06-13 — code-review (pass 9): fold-then-remove. The removable third-party
  Claude plugin `code-review@claude-plugins-official` — one command
  (`commands/code-review.md`): a fixed GitHub-PR pipeline (5 Sonnet lenses + a
  Haiku 0-100 confidence scorer, `<80` filter, `gh pr comment` post-back) —
  removed under Extraction. Three genuinely-novel false-positive exclusions
  folded into `implementation-review` (review-family 0.3.4), framed as the
  symmetric evidence burden on findings: correct code that resembles a bug;
  linter/typechecker/compiler/CI-catchable issues; and repo-instruction
  violations explicitly silenced in code (verified absent from the lane — zero
  matches across its skill dir). The 0-100 rubric + `<80` gate **not** folded.
  Scoring ruling (JP): the no-numeric-confidence precedent **bites** this
  internal, never-exposed gate, **scoped** to confidence/criticality scoring used
  as a judgment substitute, not all internal numbers; reached on inspectability
  grounds (a hidden gate is worse than an exposed one — "Found 0 issues" cannot
  be told from suppressed), reinforced by a verified miscalibration (the rubric's
  own 75 "important real issue" anchor sits below the `<80` cut; the same defect
  rode in the pass-3/pass-4 rejected artifacts). Everything else owned or banned:
  gh-PR-comment channel by fixed-terrain bundled `/code-review`+`/review`; 5-lens
  substance already folded passes 3 and 0.3.3; CLAUDE.md-adherence lens rejected
  pass 3 (foreign-CLAUDE.md leakage). Friction basis corrected: the queue's "in
  active use" is **refuted** — zero genuine invocations of the plugin or bare
  `/code-review` in this repo (triangulated; the apparent hits are this pass's
  own grep echoes). Per Admission this cannot decide removal but forecloses a
  relied-upon retention defense; removal stands on the same-runtime collision with
  the two Claude builtins. Correction for future passes: `codex-review` is itself
  an installed third-party plugin (codex-collaboration cache), unmined source
  material subject to Extraction — not a curated owner to lean on. Plugin
  uninstalled (`claude plugin uninstall`); source recoverable in the
  claude-plugins-official marketplace catalog. Evidence: charter pass-9
  route-inventory + merit-adjudication workflows (this session).
- 2026-06-13 — security-guidance (pass 10): fold-then-remove. The installed +
  enabled third-party plugin `security-guidance@claude-plugins-official`
  (v2.0.6) — a hooks bundle with no invocation token that auto-fires on
  UserPromptSubmit/PostToolUse/Stop, injecting 25 regex pattern warnings on
  edits, a single-shot LLM diff review on Stop, and an agentic cross-file
  investigate→self-refute reviewer on commit/push — removed under Extraction.
  Scope ruling (JP-ratified): the hooks engine is charter-exempt capability
  tooling (ll.22-24), but the injected instruction text is in-scope contract
  (l.24; l.14 names "instruction text delivered by hooks"), and the fused engine
  departs with the contract as packaging. Removal is value-independent
  (Extraction ll.87-90) — the engine was demonstrably used (80 review fires over
  16 days; one fully-closed fire-and-mattered loop where a commit-review finding
  changed committed `settings.json`), so pass 5's "removed as unused" is a
  distinguishable, not controlling, prior. One-Owner: the Stop/commit/push
  LLM-review jobs claim the same work as the fixed-terrain bundled
  `/security-review` (ll.16-20, 37); the collision resolves on the local side —
  delivery-mode differences (auto-fire vs invoke; recall vs precision; turn/commit
  vs branch) do not save job identity (pass-9 precedent). Two genuinely-novel
  disciplines folded into `implementation-review` (review-family 0.3.5), both
  verified zero-match in the lane: (1) resource-cap-defeat DoS — report
  exhaustion only when a change defeats an existing cap, not volumetric load
  (sits in the gap `/security-review` explicitly excludes); (2) attacker/victim +
  privilege-boundary + off-diff adversarial-refute discipline, including the
  agent-capability-gate carve-out (the model is the attacker, the user is the
  victim). Confidence-precedent (pass 9) does NOT trip — scoped to
  confidence-as-judgment-substitute: the plugin gates on an ordinal severity enum
  + qualitative cited-evidence self-refutation; its numeric `confidence` field is
  schema-optional and no code path filters on it (the exposed, inspectable kind
  the precedent prefers). Jobs rejected: inline 25-pattern edit warnings
  (lighter-alternative beats a paid slot, ll.53-55); Stop/commit/push LLM review
  (collision). Two lower-confidence folds (additive-only embedded-guidance
  guardrail; over-broad-grant sharpening) declined by JP. No inbound curated
  routes to repair (`tech-debt-scan`'s hand-off targets a hypothetical Codex
  `codex-security:security-scan`, availability-conditioned with a clean
  fallback). Plugin uninstalled (`claude plugin uninstall`); source recoverable
  in the claude-plugins-official marketplace catalog. Evidence: charter pass-10
  route-inventory + merit-adjudication workflows (this session).
- 2026-06-13 — explanatory-output-style (pass 11): reject (zero-fold removal).
  The installed-but-disabled third-party plugin
  `explanatory-output-style@claude-plugins-official` (v1.0.0) — a single
  SessionStart hook (`session-start.sh`, a heredoc `cat` of a static
  `additionalContext` blob: an always-on "explanatory output style" teaching
  register emitting `★ Insight` boxes before/after writing code,
  codebase-specific, "may exceed typical length constraints") — removed under
  Extraction; the contract IS the deliverable and the engine does no work, so the
  pass-10 packaging-departure + value-independent removal (ll.87-93) apply a
  fortiori (pass 10 had a real engine to exempt; here a trivial `cat`). One-Owner:
  doubly owned. (1) The fixed-terrain built-in "Explanatory" output style is
  live/un-deprecated (changelog "Un-deprecate output styles"; `outputStyle:
  "Explanatory"` documented; only the `/output-style` command was removed) and
  does the exact job; the plugin's "deprecated" self-label is factually stale;
  same-runtime (Claude-only — no Codex output-style/SessionStart-`additionalContext`
  analogue), co-loadable, resolves local-side (ll.16-20, 36-44). (2) Global
  `~/.claude/CLAUDE.md` Communication defaults own the chat register; the contract
  inverts them on three axes (always-on insights vs task-focus; "may exceed length
  constraints" vs brevity/outcome-first; `★`-box scaffold in chat vs "save formal
  structure for artifacts"). Zero folds: the lone substantive discipline
  (codebase-specific-not-generic insights) fails Extraction step-1 — inseparable
  from the always-on packaging and already owned by `scrutinize-skill`
  (SKILL.md:137,155), `writing-principles` (SKILL.md:172), the built-in's
  description, and CLAUDE.md. Rejection evidence (ll.60-66): usage was
  demonstrably PRESENT (715 fires, ~1380 obeyed codebase-specific boxes,
  2026-05-14 → eve of mining, concentrated in codex-collaboration), so
  usage-absence is barred as a rationale; the reject rests instead on a
  positive-control friction search (memory + handoffs + AGENTS.md + CLAUDE.md +
  ripgrep for teach/educational/insight/pedagog/verbose/output-style) that
  returned ZERO teaching-register friction while the same instrument fired on the
  opposite-vector brevity/compression family (caveman; pass-3 clarity-over-brevity
  guardrail) — that asymmetry is the finding. Lighter-alternative (ll.53-55):
  README concedes CLAUDE.md-equivalence and `outputStyle` is a one-line setting,
  both beating a paid slot. No park (the need is owned now by the live built-in,
  one `/config` flip away); keep-with-cleanup foreclosed (no Codex co-load,
  unlike pass 8). First-of-its-kind communication/output-style precedent — no
  prior chat-verbosity contract; this reject sets it. JP steer honored as
  reinforcing, not load-bearing: Ruling A (disable ruled "incidental") treated as
  neutral — the reject never rests on the toggle; Ruling B ("built-in is enough;
  no standing register") converges with the independently-reached verdict and
  forecloses any register-reinstating fold/park. Plugin uninstalled (`claude
  plugin uninstall`); source recoverable in the claude-plugins-official
  marketplace catalog. Evidence: charter pass-11 route-inventory +
  merit-adjudication workflows (this session).

## Parks

- type-design invariant lens — parked by JP's explicit choice (2026-06-12);
  reopen only on JP's ask.
- feature-dev approach-triad example — parked by JP's explicit choice
  (2026-06-12); reopen only on JP's ask.
- code-comprehension lane — parked (2026-06-12); reopen on an observed
  comprehension failure in real work.
- frontend-design web-aesthetics guidance — parked (2026-06-12); reopen on the
  first real web-frontend build task in observed work; on reopen, re-author to
  house standards from the marketplace catalog source, do not reinstall.
- security-guidance Codex-runtime security review — parked (2026-06-13, pass 10);
  reopen on the first observed Codex-side security-review need or a genuine
  `codex-security:security-scan` fire. On reopen, author to house standards; do
  not reinstall the plugin.
- security-guidance on-disk/at-rest secret detection — parked (2026-06-13,
  pass 10); reopen on the first observed at-rest-secret miss in real work (the
  gap bundled `/security-review` explicitly disclaims).
- security-guidance whole-repo / pre-existing-code security scanning — parked
  (2026-06-13, pass 10); reopen on the first observed pre-existing-code
  vulnerability that a diff-scoped review missed.

## Mining Queue

Unmined contract-shipping surfaces, on amended charter terms (rejection
evidence named per discard):

(empty — all ten queued surfaces mined through pass 11.)

Unassessed: the `github` plugin — verify whether it ships contract text beyond
MCP tooling before queueing or exempting it.
