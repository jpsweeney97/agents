# Implementation Plan: Teach the Skill Apparatus the Judgment-vs-Trust Distinction

Date: 2026-06-15
Branch: `feature/judgment-trust-distinction`
Source design: approved in session (design-exploration), grounded in
`.agents/skill-library-scrutiny-2026-06-15.md`.

## Goal

Make the skill-authoring/review apparatus hold two kinds of skill to two
different bars:

- **Judgment skills** (value = better thinking): *does this protect and provoke
  better thinking?*
- **Trust skills** (value = reliable execution): *is this reliable, and is the
  machinery single-sourced rather than copied?*

Today there is one bar — conformance — wrong for the judgment half. The change
lands the distinction on three surfaces (a single concept, single-sourced and
pointed-to), proves it with a flip-set acceptance test, then applies it to the
present backlog.

## Scope and split

This plan covers the **apparatus change**: Surfaces 1–3, the flip-set artifact,
and the acceptance test (Tasks 1–9). It also includes the **re-triage** of the
existing report backlog (Task 10), which is bounded and produces an artifact.

It does **not** fully specify the **re-review-and-cut** of existing judgment
skills — that content cannot exist until the new reviewer runs and produces
findings. After Task 9 proves the apparatus, slice that follow-on via
`to-issues` (one issue per judgment skill to re-review). This is named in
"Follow-on work" below, not tasked here.

## Conventions (verified against the repo)

- Edits run on branch `feature/judgment-trust-distinction` (already created; the
  user-level hook blocks edits on `main`).
- `agent-facing-design` is a local `skills/` skill: SKILL.md edits are live next
  session; proof is structural (`quick_validate.py`) plus a forward test. No
  installed-runtime proof layer.
- `scrutinize-skill` is plugin-distributed (`plugins/review-family/`): its edit
  follows the Plugin Layout publish path — version bump + Codex republish. The
  **GitHub mirror** (`/Users/jp/Projects/active/codex-tool-dev`) is **out of
  scope**: AGENTS.md Working Defaults forbids publishing mirror/marketplace
  state unless the user asks. Do not touch the mirror in this plan.
- `AGENTS.md` is standalone instruction Markdown: proof is `git diff --check`.
- Validator: `python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>`.
  Its `disable-model-invocation` "unexpected key" complaint is accepted policy;
  no skill in this plan adds or removes that field, so expect a clean parse.
- Commit locally per repo convention after each surface validates; **do not
  push, open PRs, sync caches to remote, or update the mirror.**

## File structure (what changes, and each file's single responsibility)

| File | Action | Responsibility after change |
|---|---|---|
| `skills/agent-facing-design/SKILL.md` | modify | Single source of the judgment-vs-trust concept (new `## Two Kinds of Skill` section) |
| `AGENTS.md` | modify (3 spots) | Anchor pointing at the concept; bar-aware body-shape rule; length-as-budget reframe |
| `plugins/review-family/skills/scrutinize-skill/SKILL.md` | modify (3 spots) | Reviewer applies the bar: new failure modes, bar-classification step, severity-by-bar |
| `plugins/review-family/.claude-plugin/plugin.json` | modify (version) | `0.3.9` → `0.3.10` so the Codex cache re-keys |
| `plugins/review-family/CHANGELOG.md` | modify | New `0.3.10` entry recording the judgment-vs-trust bar additions (release traceability) |
| `docs/plans/artifacts/judgment-trust-flip-set.md` | create | Acceptance artifact — **blind fixture**: 9 rows (id + skill + report concern), no expected verdicts; safe to reference while assembling reviewers |
| `docs/plans/artifacts/judgment-trust-flip-set-key.md` | create | Acceptance artifact — **sealed answer key**: per-row class + expected flip + load-bearing rationale + anti-leniency check; opened only after Task 9 dispositions are recorded, never loaded into a reviewer |
| `docs/plans/artifacts/judgment-trust-flip-set-results.md` | create (Task 9) | Acceptance artifact — **results record**: loaded version, reviewer/pass ids, all dispositions + bar classifications, key diff, pass/fail; the durable merge-gate proof that replaces the chat-only record |
| `skills/agent-facing-design/agents/openai.yaml` | inspect; modify only if stale | Companion metadata kept aligned with the new section (Task 2) |
| `plugins/review-family/skills/scrutinize-skill/agents/openai.yaml` | inspect; modify only if stale | Companion metadata kept aligned with the bar edits (Task 4) |
| `.agents/skill-library-scrutiny-2026-06-15.md` | (read only in Task 10) | Source of the backlog to re-triage; not edited |

---

## Task 1 — Confirm clean starting state

1. Run:
   ```bash
   git status --short --branch
   ```
   Expected: `## feature/judgment-trust-distinction`, the untracked plan file
   `?? docs/plans/2026-06-15-judgment-trust-apparatus.md` (expected and
   related — Task 8 stages it), and no *other* dirty files. If dirty files
   unrelated to this plan exist, stop and resolve before proceeding (staging
   would be ambiguous).

---

## Task 2 — Surface 1: add `## Two Kinds of Skill` to `agent-facing-design`

This section is the single source of the concept; later surfaces point to it, so
it must exist first.

**File:** `skills/agent-facing-design/SKILL.md`

Insert a new section between the end of `## Core Move` and the start of
`## When Machinery Survives`.

**Find this exact text:**
```
If the user explicitly asked for a field, status, schema, validator, router,
classifier, score, hard rule, or semantic script and the gate says it is not
justified, do not silently substitute a lighter design. Say what you would not
add, why the failure mode does not justify it, and what lighter path would
preserve the work. Ask before applying the substitute unless the user already
asked you to choose the smaller design.

## When Machinery Survives
```

**Replace with:**
```
If the user explicitly asked for a field, status, schema, validator, router,
classifier, score, hard rule, or semantic script and the gate says it is not
justified, do not silently substitute a lighter design. Say what you would not
add, why the failure mode does not justify it, and what lighter path would
preserve the work. Ask before applying the substitute unless the user already
asked you to choose the smaller design.

## Two Kinds of Skill

The core move runs per edit. Run it once more per skill, at the whole-contract
grain: what does this skill's value depend on?

- **Judgment skills** earn their keep by making the agent think better than it
  would alone — a sharper critique, a better recommendation, a real diagnosis.
  Their value is uplift. Hold them to: *does this protect and provoke better
  thinking?* The practical test for any structure in a judgment skill: does it
  organize or elicit thinking, or make the judgment for the agent? Provoking
  structure earns its place (an interrogation rhythm, a forced comparison, a
  counterexample); substitutive structure is the cost (mandated output shapes,
  exhaustive rule lists, fixed sections the agent fills to feel done), and past
  a point it makes the agent perform the contract instead of doing the work.
  When a judgment skill underperforms, the usual fix is to cut substitutive
  structure. But the bar is *protect and provoke*, and the provoke side fails
  too: a skill that provokes nothing — no forcing function, no counter-pressure,
  just "think carefully" — adds nothing over the bare agent. So does one that
  provokes too weakly: a forcing function present but dulled, hedged, or softened
  until it no longer creates real counter-pressure (an adversarial posture
  reframed as collaborative) is the same defect by degree, not a pass. Its fix is
  a sharper forcing function (a harder question, a forced comparison, a required
  counterexample), not more scaffolding.
- **Trust skills** earn their keep by reliably carrying a task so the user stops
  supervising it — landing a branch, closing out work, executing a plan step by
  step — or by returning a correct, grounded, faithfully-transformed result the
  user can stop double-checking (a correct doc lookup, a lossless reformat).
  Their value is predictable, repeatable execution (damage-prevention is
  its sharpest case, not its only one; correct retrieval and faithful
  transformation are the lookup/transform tail of the same value). Here defined steps, safe defaults, and
  firm refusals are the value, not the cost. Hold them to: *is this reliable,
  and is the machinery single-sourced rather than copied?* But trust skills fail
  under bad rules too — just never as lost thinking. The failure takes two
  shapes: brittle, duplicated machinery (the same gate hand-copied into four
  skills, drifting out of sync), and crude-rule overreach (a rule so rigid it
  does the wrong thing in a case the author never foresaw — a protected-branch
  stop that dead-ends legitimate work).

This refines the core move; it does not restate it. Judgment skills may carry
plenty of structure — stages, rhythms, prompts — as long as it organizes
thinking without making the judgment, exactly the deterministic mechanic the
core move already prefers over a decision-making rule. Structure that makes or
pre-empts the judgment is the substitutive kind, and the cost. Trust skills are
the case where machinery that *does* decide and constrain is justified — by the
need for reliable, repeatable execution.

Most real skills are mixed. Apply the bar per part, not per skill: hold the
thinking parts to the judgment bar and the lifecycle or safety parts to the
trust bar. Do not stamp one label on a two-natured skill.

This is a lens, not a label. There is no skill class to declare, score, or
validate — infer the bar from what the skill does, apply it in the moment, move
on. If applying it ever produces a fixed checklist every judgment skill "must
satisfy," it has ossified into the machinery it exists to prevent — and that
failure mode applies to this section too. The lens governs *quality* only;
delivery hygiene (invocation tokens, naming, Codex budget, parseability) stays
uniform across both kinds.

This section and `scrutinize-skill` are themselves judgment skills: hold any edit
to them to the bar above — add a lens, not a score or required section.

## When Machinery Survives
```

**Then inspect the companion metadata.** This is a behavior change to
`agent-facing-design`, so AGENTS.md Working Defaults requires inspecting its
companion metadata and updating it if the change made it stale. Read
`skills/agent-facing-design/agents/openai.yaml` and check `display_name`,
`short_description`, and `default_prompt` against the new section. Likely
outcome: no change — the `default_prompt` already frames the skill as keeping
changes "judgment-supporting," which this section sharpens rather than
contradicts. If you edit it, keep it aligned, re-parse
(`ruby -ryaml -e 'YAML.load_file(ARGV[0])' skills/agent-facing-design/agents/openai.yaml`),
and add it to Task 8 staging; if not, record a one-line no-change rationale.

**Verify:**
```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/agent-facing-design
git diff --check -- skills/agent-facing-design/SKILL.md
```
Expected: `quick_validate.py` reports a clean/passing structural result (frontmatter
parses, referenced `references/calibration.md` exists); `git diff --check` prints
nothing (no whitespace errors).

---

## Task 3 — Surface 3: three `AGENTS.md` edits

`AGENTS.md` points at the concept Task 2 created and fixes the one universal rule
that over-imposes trust-shape on judgment skills.

**File:** `AGENTS.md`

### 3a — Anchor the distinction in the routing entry

**Find this exact text:**
```
- `agent-facing-design` — before adding or materially expanding agent-facing
  obligations, proof standards, authority rules, lifecycle behavior, mutation
  boundaries, persistence, routing, or machinery. The canonical gate is
  `skills/agent-facing-design/SKILL.md`; do not duplicate it here.
```

**Replace with:**
```
- `agent-facing-design` — before adding or materially expanding agent-facing
  obligations, proof standards, authority rules, lifecycle behavior, mutation
  boundaries, persistence, routing, or machinery. It also owns the
  judgment-vs-trust distinction: a skill whose value is better thinking is held
  to "does this protect and provoke better thinking?", a skill whose value is
  reliable execution to "is this reliable, and is the machinery single-sourced
  rather than copied?"; apply the bar per part for mixed skills. The canonical
  gate is `skills/agent-facing-design/SKILL.md`; do not duplicate it here.
```

### 3b — Make the body-shape rule bar-aware

**Find this exact text:**
```
- In the body, state expected behavior, defaults, stop conditions, and output
  shape.
```

**Replace with:**
```
- In the body, state expected behavior and defaults. For trust skills, also fix
  stop conditions and output shape — predictable shape is their value. For
  judgment skills, structure is fine when it organizes or provokes thinking (a
  rhythm, a forced comparison, a findings format) and a defect when it makes the
  judgment for the agent (fill-in sections completed to feel done, a rigid stop
  sequence that pre-empts thinking). See `agent-facing-design`, Two Kinds of
  Skill.
```

### 3c — Reframe description length as budget, not quality

**Find this exact text:**
```
- Soft 25-60 word description budget; go past ~90 words only to prevent a
  specific likely misroute.
```

**Replace with:**
```
- Soft 25-60 word description budget; go past ~90 words only to prevent a
  specific likely misroute. Description length is a Codex-budget input, not a
  skill-quality score: a judgment skill is not lower-quality for sitting near
  the cap. Trim for budget pressure, not for conformance.
```

**Verify:**
```bash
git diff --check -- AGENTS.md
grep -n "judgment-vs-trust distinction" AGENTS.md
grep -n "Two Kinds of Skill" AGENTS.md
```
Expected: `git diff --check` prints nothing; both `grep`s return one line each
(anchor present, body-shape pointer present).

---

## Task 4 — Surface 2: three `scrutinize-skill` edits

**File:** `plugins/review-family/skills/scrutinize-skill/SKILL.md`

### 4a — Add the two new failure modes

**Find this exact text:**
```
- the skill silently becomes another workflow instead of handing off
- overlapping skills make routing unclear, duplicate, or fragmented
- validation claims prove structure while implying behavior
```

**Replace with:**
```
- the skill silently becomes another workflow instead of handing off
- overlapping skills make routing unclear, duplicate, or fragmented
- validation claims prove structure while implying behavior
- a judgment skill is so over-ruled — fixed output shapes, exhaustive rules,
  sections filled to feel done — that the agent performs the contract instead
  of thinking
- a judgment skill provokes nothing — no forcing function, no counter-pressure —
  so it adds nothing over the bare agent, or provokes too weakly — a forcing
  function present but dulled, hedged, or softened (an adversarial posture
  reframed as collaborative) so it no longer creates real counter-pressure (the
  *provoke* half of the bar, failed by absence or by dilution rather than by
  over-ruling)
- a trust skill is so rigidly ruled it does the wrong thing in an unforeseen
  case (a crude gate dead-ending legitimate work), or reimplements machinery
  copied from siblings instead of sharing it
```

### 4b — Rewrite workflow step 3 as bar-aware

**Find this exact text:**
```
3. **Execution Quality** - Review first move, context reading, defaults, stop
   conditions, handoffs, output shape, and failure handling.
```

**Replace with:**
```
3. **Bar And Execution Quality** - First classify the target's bar. A part is
   judgment if its value is the agent thinking better than it would alone (a
   sharper critique, recommendation, or diagnosis); trust if its value is
   reliably carrying a task so the user stops supervising it (landing a branch,
   closing out, executing a plan step by step) or returning a correct, grounded,
   faithfully-transformed result the user can stop double-checking (a correct doc
   lookup, a lossless reformat). When in doubt, ask what breaks if
   the part is removed — lost thinking (judgment) or lost reliability (trust). For
   mixed skills, classify each part the same way (see `agent-facing-design`, Two
   Kinds of Skill, for the fuller treatment). Review each part against its bar.
   Trust parts: first move, context reading, defaults, stop conditions, handoffs,
   output shape, failure handling, and whether machinery is single-sourced rather
   than copied. Judgment parts: whether structure protects and provokes thinking —
   treat a mandated output shape, exhaustive rule list, or fixed-section
   conformance as a defect, not a requirement. Do not raise trust-shape
   expectations against judgment parts as findings. Equally, do not go toothless:
   a judgment part that provokes nothing (no forcing function, no counter-pressure),
   provokes too weakly (a forcing function present but dulled, hedged, or softened
   — an adversarial posture reframed as collaborative — so it no longer creates
   real counter-pressure), or whose structure strangles thinking is a real finding
   to raise. Stopping over-flagging conformance is the goal; going lenient on
   judgment is the opposite failure, not success.
```

### 4c — Add severity-by-bar guidance

**Find this exact text:**
```
Lead findings with user-visible behavior: wrong amount of friction, unclear
first move, poor handoff, generic output, missing stop condition, false proof,
or ambiguous overlap.
```

**Replace with:**
```
Lead findings with user-visible behavior: wrong amount of friction, unclear
first move, poor handoff, generic output, missing stop condition, false proof,
or ambiguous overlap.

A finding's severity follows the bar. On a judgment part, internal-conformance
divergence drops or downgrades, but a thinking or provoke-side defect — structure
that strangles thinking, a part that provokes nothing (no forcing function, no
counter-pressure), or a forcing function dulled, hedged, or softened until it no
longer creates real counter-pressure — keeps or escalates, exactly as a trust
defect would. On a
trust part, duplication, drift, or overreach keeps or escalates. Delivery hygiene
(invocation tokens, naming, budget, parseability) is uniform — judged the same for
both. Dropping conformance noise is the goal; going toothless on a real judgment
defect is the opposite failure, not leniency rewarded as success.

These judgment failure modes are examples, not a checklist to complete. Do not add
a bar-keyed required step, fixed section, or score to this review — that is itself
the over-ruling the lens exists to prevent, and it applies to this rubric too.
```

**Then inspect the companion metadata.** This is a behavior change to
`scrutinize-skill` (new failure modes, a bar-classification step, severity-by-bar),
so inspect `plugins/review-family/skills/scrutinize-skill/agents/openai.yaml` and
check `display_name`, `short_description`, and `default_prompt` against the edits.
The `default_prompt` enumerates review dimensions ("UX, composability, overlap,
proof gaps") without the bar; minimal metadata is acceptable, so either add a
brief judgment-vs-trust-bar mention to keep it current or record a one-line
no-change rationale. If you edit it, keep it aligned, re-parse
(`ruby -ryaml -e 'YAML.load_file(ARGV[0])' plugins/review-family/skills/scrutinize-skill/agents/openai.yaml`),
and add it to Task 8 staging.

**Verify:**
```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/review-family/skills/scrutinize-skill
git diff --check -- plugins/review-family/skills/scrutinize-skill/SKILL.md
```
Expected: structural pass; `git diff --check` prints nothing.

---

## Task 5 — Bump the `review-family` version and record the changelog entry

The Codex cache is version-keyed; a behavior change needs a new version.

**File:** `plugins/review-family/.claude-plugin/plugin.json`

**Find this exact text:**
```
  "version": "0.3.9",
```

**Replace with:**
```
  "version": "0.3.10",
```

The CHANGELOG carries an entry for every prior version and the README points
users to it, so a behavior change needs a matching entry.

**File:** `plugins/review-family/CHANGELOG.md`

**Find this exact text:**
```
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 0.3.9 - 2026-06-14
```

**Replace with:**
```
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 0.3.10 - 2026-06-15

### Added

- `scrutinize-skill`: apply the judgment-vs-trust bar. Two new failure modes (a
  judgment skill over-ruled into performing the contract; a judgment skill that
  provokes nothing or only weakly — a dulled or softened forcing function), a
  bar-classification step in the review workflow (judgment vs trust, per part for
  mixed skills), and severity-by-bar guidance. The distinction is single-sourced
  in `agent-facing-design` (`## Two Kinds of Skill`) and anchored in `AGENTS.md`.
  No skill class field — a lens applied per part.

## 0.3.9 - 2026-06-14
```

**Verify:**
```bash
python -c "import json; print(json.load(open('plugins/review-family/.claude-plugin/plugin.json'))['version'])"
grep -n "## 0.3.10 - 2026-06-15" plugins/review-family/CHANGELOG.md
```
Expected output: `0.3.10`; the `grep` returns one line (the new changelog entry).

---

## Task 6 — Republish `review-family` to the local Codex cache

This makes the `scrutinize-skill` edit live on Codex. **Local cache only — not
the GitHub mirror.**

```bash
scripts/codex-plugins-sync.sh --publish review-family
scripts/codex-plugins-sync.sh --check
```
Expected: `--publish` writes version `0.3.10` into
`~/.codex/plugins/cache/turbo-mode/review-family/0.3.10`; `--check` exits 0 with
no source-vs-cache drift reported for `review-family`. If `--check` reports
drift, stop and resolve before continuing.

> Proof boundary: this publishes to the local Codex cache. It does **not** update
> the GitHub release mirror at `/Users/jp/Projects/active/codex-tool-dev`. Leave
> the mirror untouched unless the user explicitly asks to publish.

---

## Task 7 — Create the flip-set acceptance artifact (blind fixture + sealed key)

The acceptance artifact is split into two files so the answer key cannot leak into
a reviewer's context. **Reviewers get neither file** (Task 9 gives them only the
skill + the edited rubric); the fixture is the executor's mapping reference, and
the key is opened only after every disposition is recorded.

### 7a — Blind fixture

**File:** `docs/plans/artifacts/judgment-trust-flip-set.md` (create new)

**Exact content:**
```markdown
# Judgment/Trust Flip-Set — Blind Fixture

Input half of the acceptance test for the judgment-vs-trust apparatus change
(`docs/plans/2026-06-15-judgment-trust-apparatus.md`). This file carries **no
expected verdicts** — it is safe to reference while assembling reviewers. The
answer key (class + expected flip + rationale) lives in
`docs/plans/artifacts/judgment-trust-flip-set-key.md`; do **not** open it until every reviewer
disposition is recorded (Task 9), and never load either file into a reviewer's
context.

Rows 1–8 are each a finding from `.agents/skill-library-scrutiny-2026-06-15.md`;
row 9 is an over-cut probe with no report finding. To run the test, review each
named skill with the edited `scrutinize-skill` (blind, in triplicate — see Task
9). Each row names the skill and the source-report concern the reviewer is
expected to re-derive independently; the executor uses this table only to map
reviewer output onto rows.

| # | Skill | Report concern |
|---|---|---|
| 1 | scrutinize | verdict-token casing / section-name divergence with reference |
| 2 | system-design-review | "define low/med/high so the finding-cap rule is complete" |
| 3 | tdd | "no closure / done condition / output shape" flagged as a defect |
| 4 | merge-branch / closeout-check / acceptance-map / git-hygiene | protected-branch gate hand-copied into 4 skills |
| 5 | search-handoffs | `$PROJECT_ROOT` referenced in snippets, never assigned |
| 6 | gh-pr-review-loop | `@codex review` hardcode AND a "thread-assessment lacks fixed output shape" concern |
| 7 | grill-me | "'shared understanding' framing softens the adversarial posture" (report §4, grill-me row) |
| 8 | claude-code-docs | Alias section rewrites category filters that are themselves valid live enum values (`claude-md`→`memory`, `configuration`→`config`), risking silent wrong-bucket retrieval (report top-issue #10) |
| 9 | outcome-interviewer | the one-question-at-a-time interview rhythm (ask, wait, reflect, choose the next question) — an organizing structure present in the skill; no source-report finding (this row is the over-cut probe) |
```

**Verify:**
```bash
test -f docs/plans/artifacts/judgment-trust-flip-set.md && echo EXISTS
git diff --check -- docs/plans/artifacts/judgment-trust-flip-set.md
grep -c "Expected flip" docs/plans/artifacts/judgment-trust-flip-set.md
```
Expected: `EXISTS`; `git diff --check` prints nothing; `grep -c` prints `0` (the
fixture leaks no expected verdicts).

### 7b — Sealed answer key

**File:** `docs/plans/artifacts/judgment-trust-flip-set-key.md` (create new)

**Exact content:**
```markdown
# Judgment/Trust Flip-Set — Answer Key (SEALED)

> Do **not** load this file into any reviewer's context, and do **not** open it
> until every reviewer disposition from Task 9 is recorded. Pairs with the blind
> fixture `docs/plans/artifacts/judgment-trust-flip-set.md`.

Acceptance test for the judgment-vs-trust apparatus change
(`docs/plans/2026-06-15-judgment-trust-apparatus.md`). Rows 1–8 are each a finding
from `.agents/skill-library-scrutiny-2026-06-15.md`; row 9 is an over-cut probe
(no report finding — its pass is that the reviewer raises *none*). After the
apparatus edits land and `review-family` is republished, re-score each row by
reviewing the named skill with the edited `scrutinize-skill`. **Pass = the reviewer
applies the right bar to each finding — not one label to each skill.** Judgment
*conformance* findings drop/reverse; judgment *thinking* findings
(under-provocation — including a softened/dulled forcing function — and structure
that strangles thinking) keep/escalate; trust findings — including the
mechanical/lookup tail (row 8) — keep/escalate; the mixed row splits per part; the
over-cut probe (row 9) draws no substitutive-structure finding. The signal is
correct discrimination, not a uniform direction per class.

Construction rule: only findings clear enough that the verdict reproduces under
judgment belong here. Borderline provoke-vs-substitute cases are deliberately
excluded — they would make the signal non-reproducible. The one over-cut probe
(row 9) is admitted on the same standard from the other direction: the organizing
structure it protects must be *clearly* the eliciting kind, so that flagging it as
substitutive is reproducibly wrong.

| # | Skill | Class | Report finding | Expected flip |
|---|---|---|---|---|
| 1 | scrutinize | judgment | verdict-token casing / section-name divergence with reference | DROP — cosmetic; no effect on critique quality |
| 2 | system-design-review | judgment | "define low/med/high so the finding-cap rule is complete" | REVERSE — question whether numeric finding-caps belong on a thinking skill, do not complete the rule |
| 3 | tdd | judgment | "no closure / done condition / output shape" flagged as a defect | REVERSE — absence of a mandated output shape is often correct for a judgment skill, not a defect |
| 4 | merge-branch / closeout-check / acceptance-map / git-hygiene | trust | protected-branch gate hand-copied into 4 skills | KEEP + ESCALATE — shared machinery is the value; duplication is real brittleness |
| 5 | search-handoffs | trust | `$PROJECT_ROOT` referenced in snippets, never assigned | KEEP — silent no-op breaks reliability |
| 6 | gh-pr-review-loop | mixed | `@codex review` hardcode (trust part) AND a "thread-assessment lacks fixed output shape" concern (judgment part) | PER-PART SPLIT — KEEP/escalate the hardcode (trust part); DROP the output-shape concern (judgment part). Passes only if the reviewer classifies per part, not the whole skill |
| 7 | grill-me | judgment | "'shared understanding' framing softens the adversarial posture" (report §4, grill-me row) | KEEP/ESCALATE — grill-me's whole value is adversarial provocation; softening that posture is lost thinking, the judgment bar's *provoke* failure. A reviewer that drops this as "just a soft prose nit on a judgment skill" has gone lenient, not discriminating. This is the tripwire row |
| 8 | claude-code-docs | trust (mechanical/lookup) | Alias section rewrites category filters that are themselves valid live enum values (`claude-md`→`memory`, `configuration`→`config`), risking silent wrong-bucket retrieval (report top-issue #10) | KEEP/ESCALATE — claude-code-docs is a mechanical/lookup skill, and that tail sits on the *trust* side (reliable, correct retrieval is its value, not better thinking). A silent wrong-bucket bug is the exact reliability failure the trust bar exists to catch. A reviewer that treats lookup/transform skills as outside both bars, or waves this off as "not a real skill," has mis-sorted the tail |
| 9 | outcome-interviewer | judgment (over-cut probe) | The one-question-at-a-time interview rhythm (ask, wait, reflect, choose the next question) could be read as a mandated output shape / fixed-section conformance to cut | DO NOT FLAG — the rhythm *is* the forcing function that elicits one decision at a time; it organizes and provokes thinking rather than making the judgment for the agent. A reviewer that flags it as "substitutive structure, cut it" has over-swung from over-flagging conformance to over-cutting legitimate organizing structure. Expected: no substitutive-structure finding raised against the interview rhythm |

Why row 6 is load-bearing: whole-skill classification fails it both ways —
classify-all-trust wrongly demands output shape on the judgment part;
classify-all-judgment wrongly drops a real lifecycle bug. It is the only row that
exercises per-part classification, the mechanism that made "no class field" the
right design choice.

Why row 7 is load-bearing: rows 1–3 are all designed to drop, so a reviewer that
reflexively drops *every* judgment finding passes them — and, with rows 4–5
keeping, satisfies a naive "asymmetry by class" check while having stopped
reviewing judgment skills at all. Row 7 is the only judgment finding that must
KEEP. It separates "stopped over-flagging conformance" (the goal) from "went
lenient on judgment" (the new failure mode). Without it the test cannot fail on
leniency. Row 7's defect is a *softened* forcing function — grill-me's adversarial
posture diluted by "shared understanding," not a total absence of provocation — so
the loaded rubric (Tasks 2/4) must name the dulled/softened-provocation shape or a
blind reviewer cannot reach it; that naming is part of this plan. Caveat carried
knowingly: the source report logged this finding as Minor and listed grill-me under
"zero confirmed material findings," so row 7's KEEP is a deliberately sharpened
edge case — which is exactly why Task 9 scores silence across three independent
reviewers as leniency rather than trusting a single pass. Row 7 meets the
construction rule as a clear softened-provoke case on a skill whose value is
provocation, not a borderline provoke-vs-substitute call.

Why row 8 is load-bearing: it is the only row drawn from the mechanical/lookup
tail — knowledge-lookup and pure-transform skills (claude-code-docs, openai-docs,
markdown-reformat) that are neither "better thinking" nor a supervised task. The
binary is most likely to mis-sort exactly here. Row 8 pins the intended answer:
the tail is governed by the trust bar (reliable, correct execution is its value),
so a real reliability defect KEEPS. Without it the flip-set proves the distinction
only on the two families it was built around and stays silent where its soundness
is most in question.

Why row 9 is load-bearing: rows 1–3 and 7 test the over-flag axis (does the
reviewer stop docking conformance, yet still keep a real thinking defect?). None
tests the symmetric hazard the apparatus introduces — that a reviewer now told to
treat mandated shape, exhaustive rules, and fixed sections as defects over-swings
and CUTS organizing structure that should stay (Task 2: judgment skills "may carry
plenty of structure ... as long as it organizes thinking"). Row 9 is the only
over-cut probe: its pass is the reviewer NOT raising a substitutive-structure
finding against outcome-interviewer's eliciting rhythm. Unlike rows 1–8 it is not a
re-scored report finding but a no-finding-expected probe; if a future reviewer
genuinely cannot tell the organizing rhythm from substitutive scaffolding, that
inability is itself the finding. Without row 9 a reviewer that has swung to
"structure on a judgment skill is always a defect" passes the set clean.

Anti-leniency check: the pass condition is correct discrimination, not fewer
findings. Score row 7 by what the reviewer does with the provoke concern, not by
whether the word "keep" appears: if the reviewer raises the softened-adversarial-
posture concern and then KEEPS/ESCALATES it, that is the pass; if it raises the
concern and then drops or downgrades it, the apparatus has gone lenient on
judgment — FAIL, even if rows 1–6 all land exactly as predicted. The test runs
three independent reviewers (Task 9): if **all three** stay silent on the concern,
that is a leniency FAIL by default — a certified provoke defect no independent
reviewer surfaces means the apparatus is not making reviewers look, not that the
row is borderline. Marginality is earned only by a separate manual re-read
concluding the row is genuinely borderline (or by a raised/never-raised split among
the three), never assumed from silence.
```

**Verify:**
```bash
test -f docs/plans/artifacts/judgment-trust-flip-set-key.md && echo EXISTS
git diff --check -- docs/plans/artifacts/judgment-trust-flip-set-key.md
```
Expected: `EXISTS`; `git diff --check` prints nothing.

---

## Task 8 — Commit the apparatus change as a provisional checkpoint (local only)

This is a **checkpoint commit, not an acceptance-cleared one.** The behavioral
acceptance gate (Task 9) can only run in a fresh session, so it has not run yet:
the structural layer is verified (Tasks 2/4/7), the behavioral layer is not.
Commit so the editing work is not stranded uncommitted across the session
boundary, but treat the branch as **not merge-ready until Task 9 passes.**

> Live-before-proof (carry this): the apparatus is already live the moment these
> edits exist — `agent-facing-design` loads from the working tree for Claude next
> session, and Task 6 has already published `scrutinize-skill` to the Codex cache
> from the working tree (`codex-plugins-sync.sh` copies source, not a committed
> tree). So this commit does not gate exposure; the change is serving reviews on
> both runtimes before Task 9 proves it. If Task 9 FAILS, treat it as a live
> regression: fix per Task 9's loop and re-commit (amend or a follow-up `fix`
> commit) promptly — do not leave a failed apparatus serving, and do not merge to
> `main`.

```bash
# Add either companion yaml ONLY if Task 2/4 updated it (else omit that path).
git add skills/agent-facing-design/SKILL.md AGENTS.md \
  plugins/review-family/skills/scrutinize-skill/SKILL.md \
  plugins/review-family/.claude-plugin/plugin.json \
  plugins/review-family/CHANGELOG.md \
  docs/plans/artifacts/judgment-trust-flip-set.md docs/plans/artifacts/judgment-trust-flip-set-key.md \
  docs/plans/2026-06-15-judgment-trust-apparatus.md
git diff --cached --stat
git commit -m "feat(skills): teach apparatus the judgment-vs-trust distinction

Single-source the distinction in agent-facing-design; have scrutinize-skill and
AGENTS.md apply/anchor it. Add the flip-set acceptance artifact (blind fixture +
sealed key). No skill class field — a lens applied per part. review-family
0.3.9 -> 0.3.10.

Checkpoint commit: the acceptance test (Task 9) runs in a fresh session and has
not run yet; the branch is not merge-ready until it passes.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```
Expected: `git diff --cached --stat` lists the staged files — the core files
(including `plugins/review-family/CHANGELOG.md`), plus
`docs/plans/artifacts/judgment-trust-flip-set-key.md`, plus either companion yaml that
Task 2/4 updated; commit succeeds on `feature/judgment-trust-distinction`. **Do
not push; do not merge to `main` until Task 9 passes.**

---

## Task 9 — Acceptance test: re-score the flip-set (forward test)

> Proof boundary: the edited `scrutinize-skill` is live for Claude **next
> session** (SKILL.md edits load next session) and for Codex **after Task 6's
> republish**. Run this test against the *loaded edited* skill — a fresh
> session — not the version loaded before Task 4. State this when reporting.

**Task 9 preflight (run first, in this fresh session).** Confirm this session is
testing the post-edit state before dispatching any reviewer. The working tree is
the live Claude skill source and Codex serves the version-keyed cache, so a stale
branch or an un-republished cache would silently score the *pre-edit* rubric:

```bash
git status --short --branch
scripts/codex-plugins-sync.sh --check
grep -c "Bar And Execution Quality" plugins/review-family/skills/scrutinize-skill/SKILL.md
```
Expected: branch `feature/judgment-trust-distinction`, `HEAD` at the Task 8
checkpoint commit, and no unrelated dirty files; `--check` exits 0 with
`review-family` at `0.3.10` and no source-vs-cache drift; the `grep` prints a
non-zero count (the loaded `scrutinize-skill` carries the new Task-4b bar step).
If any check fails, stop and resolve — do not score the flip-set against an
unverified or pre-edit skill version.

Run the review **blind to the answer key,** and run it **independently in
triplicate.** For each skill named in the flip-set, dispatch **three independent
fresh reviewers** (separate subagents / fresh review passes), each reviewing the
named skill with the edited `scrutinize-skill` rubric. Reviewers apply
`scrutinize-skill`'s normal Evidence Floor — the skill bundle (`SKILL.md`,
companion `agents/*.yaml`), directly-referenced behavior files, a sibling/overlap
scan across the skill set, and any live check a finding needs (for row 8, the live
`search_docs` category enum that `claude-code-docs` rewrites) — exactly as in a
real review. The **only** materials withheld are the source report
(`.agents/skill-library-scrutiny-2026-06-15.md`), the blind fixture
(`docs/plans/artifacts/judgment-trust-flip-set.md`), the sealed answer key
(`docs/plans/artifacts/judgment-trust-flip-set-key.md`), and **this plan file**
(it embeds the key inline in Task 7b). Row 4 names four sibling skills
(`merge-branch`/`closeout-check`/`acceptance-map`/`git-hygiene`): review them as a
group so the cross-skill duplication is in scope — it is reachable only through the
sibling scan, not from any one skill alone.
Require each reviewer to record, for every finding, an explicit disposition —
raise-and-keep, raise-and-drop, or (only if it genuinely sees nothing) not-raised —
so that silence and a token mention are scored on the same leniency axis, not on
opposite branches. Before recording any disposition, have each reviewer first state,
in its own words, which bar (judgment or trust, or which parts are which) each
finding falls under and why. Then record the dispositions it actually produces.
Only after every disposition is recorded, open the answer key
(`docs/plans/artifacts/judgment-trust-flip-set-key.md`) and diff against its expected column.
None of the withheld materials above (source report, blind fixture, sealed key,
or this plan file) may be in any reviewer's context while reviews run.

Then check discrimination, not class-uniformity:

1. Rows 1–3 (judgment conformance): each **drops or reverses**, and the review
   instead surfaces (or at least does not flag) structure-vs-thinking concerns.
2. Row 7 (judgment thinking — the leniency tripwire): score by handling, not
   vocabulary, across the three reviewers. Raised-then-kept passes;
   raised-then-dropped is leniency (FAIL). **Unanimous never-raised across all
   three independent reviewers is a leniency FAIL** — a clear, certified provoke
   defect that no independent reviewer surfaces means the apparatus is not making
   reviewers look. "Row marginality" must be **earned**, not assumed from silence:
   it applies only if a separate manual re-read under the construction rule
   concludes the row is genuinely borderline (or the three split
   raised/never-raised — then score the raised passes by handling and flag the row
   for a marginality re-check).
3. Rows 4–5 (trust): each **keeps or escalates**.
4. Row 6 (mixed): the reviewer **splits per part** — keeps the `@codex review`
   hardcode, drops the output-shape concern.
5. Row 8 (mechanical/lookup, trust): **keeps or escalates** — the reviewer treats
   claude-code-docs as a trust skill and the wrong-bucket bug as a real
   reliability defect, not a non-skill to wave off.
6. Row 9 (over-cut probe): **no substitutive-structure finding is raised** against
   outcome-interviewer's interview rhythm — the reviewer recognizes organizing/
   eliciting structure and does not cut it. A raised "cut this structure" finding
   here is the over-cut failure (FAIL), the mirror of over-flagging.

**Pass condition:** rows 1–3 drop/reverse, rows 4–5 keep, row 6 splits per part,
row 8 keeps, row 9 draws no over-cut finding, and row 7 is **raised and
kept/escalated** by the independent reviewers. **If a reviewer raises row 7 and
then drops or downgrades it, FAIL — the apparatus has gone lenient on judgment, not
discriminating.** **If all three reviewers stay silent on row 7, FAIL by default**
— marginality is earned only by a separate manual re-read (per the construction
rule), never read off silence. Additionally, **a recorded bar-classification
divergence has teeth:** on any row where a reviewer's independent bar
classification diverges from the key — even when the disposition still matches —
that row is **not yet proven**; investigate whether the apparatus text
under-determines the bar (return to Task 2/4) or the row is borderline
(construction-rule replace), and do not score it as a clean pass.

Record the acceptance result durably, not only in chat — Task 8 makes the branch
merge gate depend on it, and a transcript is not replayable. Write
`docs/plans/artifacts/judgment-trust-flip-set-results.md` (tracked) containing: the
loaded `review-family` version (Task 5/6), the reviewer/pass identifiers and which
runtime/session loaded the edited skill, all nine dispositions across all three
reviewers, each reviewer's independent bar classification, the per-row diff against
the sealed key, any failures, and the final pass/fail. Summarize the same in chat.

**Verify:**
```bash
test -f docs/plans/artifacts/judgment-trust-flip-set-results.md && echo EXISTS
git diff --check -- docs/plans/artifacts/judgment-trust-flip-set-results.md
```
Expected: `EXISTS`; no whitespace errors. Commit locally on the branch as a
follow-up to the Task 8 checkpoint (this runs in the fresh Task 9 session); do not
push.

If any row does not land as predicted, treat it as a real finding: either the
apparatus text needs sharpening (return to Task 2/4 — for row 7, sharpen the
*provoke* side, do not weaken the row) or the flip-set row violated the
construction rule (remove it and note why). Do not weaken the pass condition to
make it pass.

---

## Task 10 — Re-triage the existing report backlog through the distinction

Bounded, artifact-producing. Closes the loop from "apparatus learned" toward
"pain relieved."

1. Read `.agents/skill-library-scrutiny-2026-06-15.md` §6 (Prioritized
   Remediation Backlog, P0–P2) for the item list — **and** read §4 (headlines)
   and §5 (Per-Skill Detailed Findings) for the evidence and rationale behind each
   item. §6 is a compressed action table; on its own it is too thin to re-judge a
   finding against the new bar or to tag `budget-driven` vs `conformance-driven`.
2. For each backlog item, classify and re-disposition. **When an item is both a
   budget-recovery trim and a conformance nit — an over-cap description on a
   judgment skill is both — the budget reading wins while the description is over
   the Codex cap: preserve it as budget, and drop the residual as conformance only
   once it is back under the cap.** Tag each item `budget-driven` or
   `conformance-driven` so the tie-break is recorded, not improvised.
   - **Delivery hygiene** (dual-runtime tokens, naming, budget, parseability) and
     the **delivery/charter P0s** (`jp-writing-style` dangling symlink + ledger
     desync) — **preserve unchanged**; these are uniform and survive re-triage.
   - **Conformance-quality nits on judgment skills** (e.g. P1/D2 description
     trims on `making-recommendations`, `outcome-interviewer`; the `scrutinize`
     casing nit; `system-design-review` cap-completion) — **drop or reverse** per
     the new bar — **except** where the trim is the cheapest budget recovery for an
     over-cap description, which stays preserved per the rule above until under the
     cap.
   - **Trust-skill findings** — **keep or escalate**.
3. Write the result to `docs/plans/artifacts/skill-library-backlog-retriaged-2026-06-15.md`:
   a table of each original item with `{original disposition, class, new
   disposition, one-line reason, evidence}`. For every item whose disposition
   **changes** under the new bar, the `evidence` cell cites the originating §5
   finding (skill + the report's evidence pointer) and, where the new bar flips the
   result, a live skill line — so each re-disposition is grounded, not improvised.

**Verify:**
```bash
test -f docs/plans/artifacts/skill-library-backlog-retriaged-2026-06-15.md && echo EXISTS
git diff --check -- docs/plans/artifacts/skill-library-backlog-retriaged-2026-06-15.md
```
Expected: `EXISTS`; no whitespace errors. Commit locally (do not push).

---

## Follow-on work (not tasked here — slice via `to-issues`)

After Task 9 proves the apparatus and Task 10 produces the filtered backlog:

- **Re-review each judgment skill** under the new reviewer and **cut substitutive
  structure** it flags. This content cannot be pre-specified (it depends on the
  reviewer's output), so slice it as one `to-issues` issue per judgment skill,
  each referencing this plan and the re-triaged backlog.
- **Signal A (longer-term):** once several judgment skills are trimmed, measure
  uplift with `skill-benchmark` (with/without-skill eval runs) on a sample. A is
  the lagging confirmation that the work got better; the flip-set (Task 9) is the
  leading proxy. A is not a gate on this plan.
- **Ossification re-test (standing):** after substantial future `scrutinize-skill`
  edits, re-run the flip-set (Task 9). Checklist-creep surfaces as judgment rows
  starting to mis-fire — once-dropped conformance rows beginning to keep, or the
  failure-mode list having grown a required step. This is the recurring check the
  inline self-guard (Task 4c) cannot enforce on its own. **Anti-accretion default:**
  when a future `scrutinize-skill` edit is proposed to fix a mis-fire, the default
  move is to **tighten or cut** existing bar text, not add a clause; any
  net-additive edit to the 4a/4b/4c bar-handling material must justify why a rewrite
  or deletion could not achieve the same. Treat the combined 4a/4b/4c bar material
  as carrying a soft word budget — growth is visible and must be argued, the way 3c
  makes description length a tracked input rather than a free dimension.
- **Charter — consulted, not a charter event (determination, not deferred work):**
  this change refines three already-admitted, first-party contracts
  (`agent-facing-design`, `scrutinize-skill`, `AGENTS.md`). It is not an admission,
  extraction, retirement, or third-party-material decision — the charter's four
  triggers (`docs/agents/charter.md`) — so it takes **no `contract-decisions.md`
  entry** (the ledger records only those five outcomes; a content refinement inside
  an existing owner is none of them). Admission/One-Owner stay class-blind, and the
  distinction lives inside `agent-facing-design`. The charter's existing "qualitative
  judgment vs measured benchmark" language is a latent cousin if formal alignment is
  ever wanted — genuinely optional, and the only part of this bullet that is future
  work.

## Self-review (done against the design)

- **Coverage:** Surfaces 1–3 (Tasks 2–4), plugin delivery (Tasks 5–6), flip-set
  with the per-part row, judgment-keep tripwire, and the over-cut probe (Task 7),
  acceptance test run in triplicate (Task 9), backlog re-triage
  (Task 10), and the named follow-on all trace to design components. The six
  session folds (rollout, signal A, trust failure modes, charter exclusion,
  self-application note, word-count reframe) are each present.
- **Placeholders:** none — every edit gives exact find/replace text and exact
  verify commands with expected output.
- **Consistency:** the full bar concept lives once in Task 2; Task 4b carries a
  compact operative restatement of the classification criterion (per MECH-1, so
  the reviewer can classify without the non-co-loaded sibling) and points to Task
  2 for depth. The flip-set quotes the bars; `AGENTS.md` 3a quotes the bar
  verbatim and 3b paraphrases the body-shape rule by pointer (it does not
  re-define the bar). The round-2 additions follow the same pattern: the
  softened/dulled-provocation shape and the lookup/transform trust tail are stated
  in Task 2 and restated operatively in scrutinize-skill (4a/4b/4c) because the
  loader never co-loads the sibling — the deliberate operative-restatement the load
  model requires, not unmanaged duplication.
- **Proof boundaries stated:** local-skill vs plugin-cache vs next-session-load,
  and mirror explicitly out of scope.

## Post-evaluation hardening (2026-06-15, panel verdict: execute-with-fixes)

An adversarial multi-lens panel evaluated this design pre-execution and returned
`execute-with-fixes`. The four must-fixes are applied above; two were ratified
forks (full scope; the mechanical/lookup tail governed by the trust bar):

- **MECH-1** (corroborated by 4 independent lenses): Task 4b now inlines the
  bar-classification criterion instead of offloading it to `agent-facing-design`,
  which the reviewer's loader never co-loads. The pointer stays as a deepening
  reference, not the carrier of the operative rule.
- **Row 7 / Task 9** (3 lenses): the leniency gate now scores row 7 by *handling* —
  raised-then-kept passes, raised-then-dropped FAILS, never-raised is row
  marginality (not an apparatus FAIL) — resolving the collapse the panel found.
- **SCOPE-2:** Task 10 step 2 now orders budget-preserve over conformance-drop for
  over-cap judgment descriptions, with a per-item budget/conformance tag.
- **DICHOTOMY-3:** flip-set row 8 (`claude-code-docs`, mechanical/lookup) tests the
  tail the binary is most likely to mis-sort; ratified intent = that tail is
  governed by the **trust** bar.
- **Independence break:** Task 9 now has the blind re-scorer state each finding's
  bar in its own words before the key is revealed, so divergence is recorded as
  signal.

Also folded in on request (the two should-addresses):

- **LENIENCY-1:** Task 4b and 4c now carry the KEEP-side instruction explicitly — a
  judgment part that provokes nothing or strangles thinking keeps/escalates, and
  going toothless on judgment is named as the opposite failure — so a reviewer who
  never runs the flip-set still carries it, not only the DROP-side.
- **OSSIFY-3:** Task 4c now states inline that the judgment failure modes are
  examples, not a checklist, and that adding a required step/section/score to the
  review is itself the over-ruling the lens prevents; Follow-on adds a standing
  flip-set re-test so checklist-creep resurfaces after future `scrutinize-skill`
  edits.

## Post-evaluation hardening — round 2 (independent panel verdict: execute-with-fixes, converged)

A second independent adversarial panel (15 lenses — 8 fresh design + 7 regression
on the round-1 fixes — plus a completeness critic and an xhigh adjudicator; run
`wf_ee58152b-885`, 109 agents) re-evaluated the hardened design. Verdict:
`execute-with-fixes`, and **converged** ("stop after this fix; do not commission a
round 3"). The regression panel cleared **5 of the 6** round-1 fixes outright; one
blocking finding survived, plus three should-address majors the user chose to fold
in (the fourth, ossification bloat, handled conservatively). All are applied above.

- **Blocking — the leniency tripwire was disarmed** (REG-TASK9-FALSEPASS-1,
  corroborated by MECH2-PROVOKE-SHAPE-1, TRIPWIRE-NEVERRAISED-1,
  ACCEPT-ROW7-MARGINAL, REG-TASK9-UNFALSIFIABLE-1). Two interacting defects, both
  introduced by the round-1 three-way scoring fix: (a) the loaded rubric named the
  provoke-defect only as *absence* ("provokes nothing"), but row 7's defect is a
  *softening* — a shape named only in the answer key the blind reviewer cannot see;
  and (b) `never-raised = row marginality` routed the most natural lenient behavior
  (silence) to a PASS. Fix, per the user's three fork calls: (1) **name the
  softened/dulled-provocation shape in the loaded rubric and the source concept** —
  Task 2 and scrutinize-skill 4a/4b/4c now cover "provokes too weakly: a forcing
  function present but dulled, hedged, or softened"; (2) **Task 9 runs three
  independent reviewers and FAILS on unanimous never-raised** — marginality must be
  earned by a separate manual re-read, never read off silence, and "raised" is
  operationalized as an explicit per-finding disposition so silence and
  token-mention sit on the same leniency axis. **Row 7 kept and sharpened** (not
  replaced): a "material" replacement does not exist — the report's ~0 kept judgment
  thinking-defects *is* the apparatus's motivating premise — so row 7's
  source-report Minor/immaterial logging is carried knowingly, bounded by the
  triplicate-silence rule, with `skill-benchmark` Signal A the lagging
  author-independent control.
- **Should-address (folded in) — trust definition reaches the lookup tail**
  (DICHOTOMY-R2-1). The shipped trust bar was task-supervision only, so it did not
  actually reach row 8's `claude-code-docs`; a grounded lookup could read as uplift.
  Task 2 and the 4b criterion now name "a correct, grounded, faithfully-transformed
  result the user can stop double-checking" as a trust value, so row 8 follows from
  the rule the blind reviewer applies, not the key.
- **Should-address (folded in) — over-cut probe added** (ACCEPT-OVERCUT-UNTESTED).
  The flip-set tested over-flagging→drop but never the symmetric hazard the
  apparatus introduces — over-CUTTING legitimate organizing structure. New **row 9**
  (`outcome-interviewer` interview rhythm; expected = no substitutive-structure
  finding raised) plus Task 9 check 6 close it; the construction rule admits it from
  the other direction.
- **Should-address (folded in) — independence check given teeth** (REG-INDEP-2).
  "Recorded as signal" was inert (every check keyed on disposition). Task 9's pass
  condition now makes a bar-classification divergence — even with a matching
  disposition — mark the row *not yet proven*, routing to Task 2/4 or a
  construction-rule replace.
- **Ossification bloat handled conservatively** (OSSIFY-R2-3 / REG-OSSIFY-BLOAT-2,
  user call). Rather than compress Task 4b step 3 — which risked re-opening the
  MECH-1 offload — Follow-on's Ossification re-test gains an **anti-accretion
  default**: the default fix for a future mis-fire is to tighten or cut bar text,
  net-additive edits must be argued, and the combined 4a/4b/4c bar material carries
  a soft word budget.

Preserved unchanged (panel-credited strengths): single-source discipline,
lens-not-label, the per-part grain (row 6), the delivery-hygiene firewall, the
raised-then-dropped FAIL branch, and the clean count migration. Round-2
relitigation explicitly rejected: the "0 value findings" premise attack (a framing
wart, not load-bearing), the lean-two-sentence alternative, the MECH-1 drift and
row-8 non-discrimination challenges, and the same-author-key objection (bounded by
Signal A). The flip-set is now **9 rows**; Task 9 runs in **triplicate**.

## Post-adjudication fixes (2026-06-15, `review-reviewer`: partially reliable)

A `review-reviewer` adjudication of this plan (read-only, against live `AGENTS.md`,
both companion `agents/openai.yaml`, and `scripts/codex-plugins-sync.sh`) returned
**partially reliable**: two findings real and acted on, one minor, one (the second
"High") challenged as resting on a misread of the Task 9 harness but adopted as
cheap defense-in-depth. The converged round-1/round-2 design is unchanged; these
are plan-text edits only.

- **R1 + M1 — commit-before-proof.** Task 8 reframed as a **provisional
  checkpoint**, not acceptance-cleared: the structural layer is verified but the
  behavioral gate (Task 9) cannot run until a fresh session, so the branch is
  **not merge-ready until Task 9 passes.** Added the live-before-proof note (M1):
  the apparatus serves reviews on both runtimes the moment the edits exist (Claude
  working-tree load; Codex Task-6 cache publish from source), so the commit does
  not gate exposure and a Task 9 failure is a live regression to fix and re-commit
  promptly.
- **R2 — flip-set split for blind hygiene.** Task 7 now creates a **blind
  fixture** (id + skill + report concern, no verdicts) and a **sealed answer key**
  (class + expected flip + rationale + anti-leniency check). Reviewers still get
  only the skill + rubric (neither file); the key is opened only after dispositions
  are recorded (Task 9 updated to match). The adjudication confirmed the original
  single file did not actually force a leak — reviewers were never handed flip-set
  findings; they re-derive concerns by reviewing the skill cold, which the
  triplicate-silence rule depends on — so this is defense-in-depth against an
  executing agent accidentally pasting the key into a reviewer prompt, not a
  correctness fix.
- **R3 — companion metadata.** Tasks 2 and 4 now inspect each skill's
  `agents/openai.yaml` against the behavior change, update if stale or record a
  one-line no-change rationale, and stage only if changed (per AGENTS.md Working
  Defaults); the file-structure table lists both as inspect targets.
- **R4 — Task 1 clean state.** Task 1 now names the untracked plan file as
  expected and related, so the executor does not mistake it for an unrelated dirty
  file.

## Post-adjudication fixes — second pass (2026-06-15, `review-reviewer` on a Codex review: partially reliable)

A second `review-reviewer` adjudication — this time of a supplied Codex
`scrutinize-skill`-style review of this plan, read against live `.gitignore`, the
charter, and git's ignore/stage behavior — returned **partially reliable**: one
confirmed blocker, one confirmed should-fix, one challenged-and-narrowed finding.
The converged round-1/round-2 design is unchanged; these are plan-text edits only.

- **CF1 — acceptance artifacts were under ignored `.agents/` (CONFIRMED blocker,
  empirically proven).** `git check-ignore -v` flagged all three created artifacts
  (`.gitignore:9` ignores `.agents/` wholesale; zero files are tracked there), and
  `git add` of an explicitly-named ignored path exits 1 — so Task 8's staging halted
  as written, no `-f` present. The prior pass's own R2 split compounded this by
  adding a second ignored artifact. Fix: the blind fixture, sealed key, and Task 10
  retriage artifact moved from `.agents/` to the **tracked** path
  `docs/plans/artifacts/`; every in-plan path reference, the file-structure table,
  and the Task 8 staging line updated (plain `git add` now works). The source report
  `.agents/skill-library-scrutiny-2026-06-15.md` stays put — read-only input, not
  created or committed here. Root cause the review only treated as a symptom: Task 7
  framed the fixture as the executor's scratch "mapping reference" while Task 8
  committed it as proof — resolved here in favor of committed proof on a tracked
  path.
- **R-UX / M2 — chat-only acceptance gate (CONFIRMED should-fix).** Task 9 gated the
  branch merge (Task 8) on a result recorded only in chat — not replayable. Task 9
  now writes a tracked `docs/plans/artifacts/judgment-trust-flip-set-results.md`
  (loaded version, reviewer/pass ids, all dispositions + bar classifications, key
  diff, failures, pass/fail) and commits it in the fresh Task 9 session. This closes
  the long-open M2.
- **CF2 — "charter alignment is optional" (CHALLENGED, narrowed to a wording fix).**
  The review pitched a co-equal blocker requiring an early charter-consult step and a
  possible `contract-decisions.md` entry. Adjudication against charter text: refining
  three already-admitted first-party contracts is none of the charter's four triggers
  and none of the ledger's five recorded outcomes, so **no entry is owed** and the
  severity was inflated. Kept only the real residue: the Follow-on "Charter alignment
  (optional, future)" bullet is reworded to **record the determination** (consulted;
  not a charter event; no ledger entry) rather than imply a deferred chore.

Not acted on (challenged parts of CF2): adding a charter-consult task or any
`contract-decisions.md` entry. The `/Users/jp/vault/` snapshot is no longer
maintained — it has served its purpose; this plan file is now the sole canonical
copy.

## Post-adjudication fixes — third pass (2026-06-15, `review-reviewer` of a second Codex-style review: partially reliable)

A third `review-reviewer` adjudication of this plan (read-only against live
`scrutinize-skill`'s Evidence Floor, `AGENTS.md`, the source report §4–§6, and the
`review-family` CHANGELOG/README) returned **partially reliable**: no false
positives, three confirmed should-fixes, two findings narrowed (one severity-
inflated, one re-raising settled `AGENTS.md` 3b ground), plus two missed issues the
adjudication added. The converged round-1/round-2 design is unchanged; these are
plan-text edits only. No commit; the plan stays untracked until Task 8.

- **R2 — fresh-session preflight (CONFIRMED should-fix).** Task 9 recorded the
  loaded version only *after* the run. Added a **Task 9 preflight** that runs first
  in the fresh session: branch/HEAD/dirty check, `codex-plugins-sync.sh --check`
  (review-family at `0.3.10`), and a grep proving the loaded `scrutinize-skill`
  carries the new Task-4b bar step — so the gate cannot score a stale or pre-edit
  rubric.
- **R1 + two missed issues — Task 9 evidence boundary (CHALLENGED → narrowed).**
  "Too loose to prove the apparatus" overstated: `scrutinize-skill`'s Evidence
  Floor already governs what reviewers inspect. But the wording "only the skill"
  was ambiguous for the cross-skill (row 4) and live-enum (row 8) rows. Rewrote the
  dispatch paragraph: reviewers apply the normal Evidence Floor (bundle, referenced
  files, sibling/overlap scan, needed live checks); the **only** withheld materials
  are the source report, fixture, key, **and this plan file** (which embeds the key
  inline in Task 7b — the missed leak vector); row 4's four siblings are reviewed as
  a group so the duplication is in scope.
- **R4 — Task 10 read-from-evidence (CONFIRMED should-fix).** Task 10 read only the
  compressed §6 action table. Now also reads §4 headlines + §5 detail, and the
  retriage table gains an `evidence` column citing the originating §5 finding for
  every changed disposition.
- **R5 — changelog entry (CONFIRMED, low).** The version bump had no CHANGELOG
  entry against a plugin that documents every release. Task 5 now also adds a
  `0.3.10 - 2026-06-15` entry; Task 8 stages `CHANGELOG.md`; the file-structure
  table lists it.
- **R3 — `AGENTS.md` single-source (CHALLENGED, not acted on).** The "parallel
  mini-contract" framing was inflated and largely re-raised the deliberately-settled
  3b-offload point. 3a's two one-line bar questions are the anchor's essence, not a
  second definition (the full concept stays single-sourced in `agent-facing-design`);
  cutting them would weaken the anchor for no real drift reduction. Left unchanged.
