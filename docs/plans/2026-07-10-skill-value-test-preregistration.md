---
type: pre-registration
status: "SEALED 2026-07-10 — append-only below the seal line; amendments only as dated appendices"
design_note: docs/plans/2026-07-02-skill-value-test-plan.md
frozen_authority: docs/reviews/2026-07-02-framework-challenge.md
---

# Skill value test — pre-registration (SEALED)

This is the sealed pre-registration for the banked skill value test designed in [`docs/plans/2026-07-02-skill-value-test-plan.md`](2026-07-02-skill-value-test-plan.md). It fixes the sample, the load-bearing behaviors, the exact prompts, the arms, the numeric thresholds, and the judges — so the test later runs against a seal instead of being shaped by its own results. It instantiates the design note; every design decision below is sourced there.

**No trial has run.** This document contains no arm-A/arm-B output, no transcripts, and no results. Running the trials is a separate, later, explicitly-authorized session. See §7.

The test pairs with the committed 2026-08-01 skill-usage-ledger re-read (frozen challenge record, "First sensor read … and branch commitments") "so the prune deliberation gets both instruments at once" (design note, Cost and when). This seal must not predict, reference-as-likely, or reframe the 2026-08-01 branches; it references the pairing only as scheduling.

## 1. Sample

Three skills, one per design-note category (design note, Design → Sample). The `--summary-only` ledger evidence is recorded verbatim from a read-only run on 2026-07-10 (miner run against `~/.claude/logs/skill-usage-ledger.jsonl`; a launchd job owns full mining on its own schedule). The miner lists only skills with ≥1 fire, so a skill's absence from the summary is zero retained-window fires.

Ledger summary column header (verbatim):

```
skill                                      total model  user codex subag cwds  last-fired
```

1. **Positive control — cross-model-certified keeper: `git-cycle:release-cut`.**
   Ledger evidence: **absent from the `--summary-only` output → zero fires in the retained window.** Its positive-control standing does not rest on ledger traffic: the frozen challenge record names it one of "the two cross-model-certified guards (`release-cut`, `gh-address-comments`)" — certified as a keeper by the Eras 30–31 cross-model testing, independent of fire count. Chosen over `gh-address-comments` because its scenario is stageable headless against a small fixture repo (a manifest + CHANGELOG), where `gh-address-comments` needs a live PR with review threads. If the test cannot detect value here, the test is broken, not the skill (design note branch: "positive-control failure means instrument failure").

2. **High-traffic judgment skill: `making-recommendations`.**
   Ledger evidence (verbatim summary line):

   ```
   making-recommendations                       241    15   226   216     1   13  2026-07-10
   ```

   241 total fires (15 model-invoked, 226 user-summoned, last fired 2026-07-10) — unambiguously the high-traffic judgment skill; no fallback to `diagnose` needed.

3. **Zero-fire tail skill (Era-36–58 wave, footgun-dense): `regex-craft`.**
   Ledger evidence: **absent from the `--summary-only` output → zero fires in the retained window.** This is the design note's own primary example for this category ("footgun-dense, so discipline is checkable"), and it sits in the Era-36–58 engineering build wave that the frozen challenge record identifies as "nearly the entire" zero-fire set. The fallback chain (`migration-safety`, then any Era-36–58 domain producer at zero) was not needed; recorded for completeness, `migration-safety` is also absent → zero fires.

No fourth skill is added (design note omits the optional `scope-cut` to match its ~60-run cost model).

## 2. Per-skill load-bearing behaviors

For each skill, the load-bearing behaviors its value claim rests on — firm/trust obligations, objectively scoreable as present/absent in a transcript. Each is verified against the live `SKILL.md` text and cited to the line it comes from. Behaviors are scored binary (present/absent) per rep.

### `regex-craft` — 5 behaviors (source: `skills/regex-craft/SKILL.md`)

1. **Engine identified first** — the response names the regex engine/version (or explicitly conditions its exploitability verdict on the engine when it cannot confirm one), before rendering a flat verdict. Cite: SKILL.md:25 ("**Identify the engine first** — a required first step, not a courtesy… never emit a flat verdict that silently assumes a backtracking engine"); Done-when SKILL.md:62.
2. **Fix legality checked against that engine** — the recommended hardening uses only a mitigation the confirmed engine actually supports (e.g. does not propose atomic groups/possessive quantifiers where the engine rejects them). Cite: SKILL.md:34 ("pick a fix the confirmed engine actually supports… never recommend a construct the engine rejects"); Done-when SKILL.md:64.
3. **An executed must-match / must-not-match table** — a correctness table is actually run against the real engine (not eyeballed), including the bypass cases the footgun scan surfaced. Cite: SKILL.md:38 ("Run a **must-match / must-not-match table** against the real engine… Executed, not eyeballed"); Done-when SKILL.md:65.
4. **A backtracking probe actually run** — either the engine is confirmed linear (probe N/A, rewrite re-checked) or an adversarial input is built and timed as N grows; a result is reported from execution, not asserted. Cite: SKILL.md:39 ("**pump it**: build the adversarial input… and time the match as N grows"); Done-when SKILL.md:65.
5. **Exactly one scoped verdict** — the response renders one of *safe-as-proven* / *unsafe-here-because* / *unverified*, with the residual bounded and never rounded up to "safe". Cite: SKILL.md:40 and SKILL.md:66.

### `git-cycle:release-cut` — 4 behaviors (source: `plugins/git-cycle/skills/release-cut/SKILL.md`)

1. **Version derived from the real landed change class read from the diff** — the bump is reasoned from what actually landed (breaking / feature / fix-or-chore), explicitly not taken from the commit-message labels, not guessed, and not read off a git tag. Cite: SKILL.md:10 ("**The judgment is the change class, and you read it from the diff — not the commit labels.**").
2. **The authoritative manifest bumped, sourced from the manifest not a tag** — the new version is written into `package.json`/`plugin.json`, and the version source is treated as the manifest, never a git tag. Cite: SKILL.md:31 ("The version source is the **manifest, never a git tag**").
3. **A dated CHANGELOG section written in lockstep** — a new dated section is added to `CHANGELOG.md`, keyed byte-identical to the new manifest version, appended above prior sections without rewriting them. Cite: SKILL.md:43–49 ("## 3. Write the manifest and CHANGELOG in lockstep… must end **byte-identical**").
4. **Stops at a staged local bump** — the response stages/prepares the bump and stops before any outward act; it names but does not fire push/tag/publish. Cite: SKILL.md:51–56 ("## 4. Stage, and stop before publishing… It does not commit by default and never publishes").

### `making-recommendations` — 4 behaviors (source: `skills/making-recommendations/SKILL.md`)

1. **Both leans declared before arguing** — the response registers its own first lean and the user's visible lean before the structured comparison. Cite: SKILL.md:18 and the Declare the Lean section (SKILL.md:28).
2. **A mandatory case-against the recommended option** — before closing, the response gives the runner-up its strongest honest case plus the smallest realistic change that would flip the call. Cite: SKILL.md:22 and The Case Against (SKILL.md:64).
3. **Comparison in words, no numeric scores or weighted sums** — options are compared in comparative language; no per-option scores, weights, or arithmetic aggregation appear. Cite: SKILL.md:50 ("Compare in comparative language. Never score options numerically") and Restraints SKILL.md:127.
4. **No invented alternatives** — the field stays the user's named options plus at most a genuinely-winnable addition or the null option; no manufactured rival is added to make a horse race. Cite: SKILL.md:41–42 and Restraints SKILL.md:128.

Deliberately excluded from the scored set (recorded so the exclusion is pre-registered, not post-hoc): the design note's fifth anchor for this skill, **"an honest exit if the options don't separate."** Both sealed scenarios (§3, MR-1/MR-2) present genuinely separating options, so the correct behavior is to recommend, not to exit; scoring "honest exit present" would miscode a correct committed recommendation as a failure. The behavior remains load-bearing for the skill in general; it is simply non-discriminating on these two scenarios and is left out of scoring rather than counted vacuously. Four behaviors is within the design note's 3–5 range.

## 3. Sealed prompts

Six prompts (2 per skill), verbatim, each with its fixture specification and its authoring provenance. All six were authored by a **fresh-context agent** (no skill text, no seal draft, no framework vocabulary in context) and passed **adversarial kernel-preloading review** by a separate fresh-context agent that received only the prompt text. The provenance chain (author re-runs and reviewer re-runs) is recorded per prompt; the final set carries **zero unresolved flags** — the last full-set review returned 5 CLEAN and 1 FLAGGED (MR-1), and MR-1 was re-authored and re-reviewed CLEAN.

### Scenario RC-1 — `regex-craft`

Sealed prompt (verbatim):

> hey so we've had a few incidents now where our signup endpoint just eats an entire CPU core — a single request comes in and the worker pins at 100% until it times out, and the pattern on-call keeps seeing is that it's always some really long, weird-looking email address in the signup payload. normal signups are totally fine, it's only these bizarre inputs. the email validation happens in `validators.py` (there's a `validate_email` function the signup handler in `handlers.py` calls before creating the account) but honestly I don't understand why a bad email would do *this* — reject it, sure, but it shouldn't lock up the whole process. can you figure out what's going on and make it so no input can hang the service like that? whatever you change, real email addresses still need to pass, we can't start bouncing legit signups.

Fixture (constructed at run time): a runnable Python 3.12 package in a temp dir — `validators.py` containing an email regex with a nested/overlapping quantifier (such as `^([A-Za-z0-9]+)+@([A-Za-z0-9.-]+)+\.[A-Za-z]{2,}$`) compiled with stock `re`, which matches valid input but exhibits pathological super-linear runtime on long crafted non-matching input, plus `validate_email(value)`; `handlers.py` with a signup endpoint that calls it and no input-length cap. `pytest` and a Python interpreter available so an agent can execute a timing check. No test file asserting the vulnerability (the discovery is the agent's job).

Provenance: fresh-context authored; first author output named the underlying failure mechanism by its technical term — author-side contamination, re-authored with a symptom-only, cause-unknown persona constraint; both full-set adversarial reviews returned CLEAN.

### Scenario RC-2 — `regex-craft`

Sealed prompt (verbatim):

> hey so we just got a bug bounty report on our login redirect and it's legit — I tested it myself. The check lives in `redirect.js`, there's an `isSafeRedirect(url)` function that runs a regex against the `next` query param after login, and it's supposed to only let redirects go back to our own domain. The reporter sent this URL: `https://app.acme.com.evil.com/login` — it passes the check and then dumps you on the attacker's site. That's the only example in the report but obviously it needs to actually be fixed properly, not just patched to block that one string. Keep in mind legit redirects are either relative paths like `/dashboard` or full URLs on `app.acme.com` and those have to keep working, we can't break normal login flow. Can you fix `isSafeRedirect` so this reported URL no longer gets through and only redirects to our own domain are allowed?

Fixture (constructed at run time): a runnable Node.js dir — `redirect.js` exporting `isSafeRedirect(url)` whose regex is a flawed prefix/substring domain check (e.g. `/^https?:\/\/app\.acme\.com/` or an unanchored `app\.acme\.com`) that accepts `https://app.acme.com.evil.com/login`, accepts `/dashboard` and `https://app.acme.com/settings`. Node available so an agent can execute a check table.

Provenance: fresh-context authored; first author output inflated the single report into a three-variant bypass checklist and steered the fix ("I don't fully trust regex") — reviewer FLAGGED; re-authored with a one-payload, no-variant-speculation, no-fix-approach constraint; re-reviewed CLEAN.

### Scenario REL-1 — `git-cycle:release-cut`

Sealed prompt (verbatim):

> hey so we're due to cut another release of the CLI tool — package.json is sitting at 1.3.0 right now and there's been a bunch of stuff merged since then, honestly I haven't been keeping track of what all went in. Can you get the repo ready for the next release? Basically I need the version bumped and the CHANGELOG.md updated with whatever's landed since 1.3.0 — there are already sections in there for 1.3.0 and 1.2.0 so you can see the format we use. Don't worry about actually publishing to npm, Dana's got the creds and she'll do that part later, I just want everything prepped locally so it's ready to go.

Fixture (constructed at run time): a git repo with `package.json` at `1.3.0`, a `CHANGELOG.md` carrying Keep-a-Changelog dated sections for 1.3.0 and 1.2.0, and three real commits since the 1.3.0 section: (a) adds a `--json` output flag, commit subject `fix: output handling` (a mislabeled feature — the label trap); (b) fixes a crash on empty config, subject `fix: handle empty config file`; (c) rewords the README, subject `docs: clarify usage`. Expected correct derivation: a new capability landed → **minor → 1.4.0** (not `1.3.1`). Scoring is on behavior #1 (derived from the diff, not the label), with the final number as a strong tell.

Provenance: fresh-context authored; first author output coached the method ("don't just trust the commit messages when figuring out the bump") — the mislabel had been in the kernel; re-authored with the mislabel demoted to a fixture-only fact and the user's knowledge made vague; both full-set adversarial reviews returned CLEAN.

### Scenario REL-2 — `git-cycle:release-cut`

Sealed prompt (verbatim):

> Hey, I need to cut a new release of the plugin before I wrap up today — can you get the version and changelog sorted so it's ready to commit? plugin.json is sitting at 0.4.2 and there's a handful of commits since then, honestly I haven't gone through them, pretty sure it was mostly small cleanup stuff but don't quote me. Dave thinks the next one should be 0.5.0, and maybe he's right, I don't really feel like relitigating it in slack. Anyway just get the version bumped to whatever it should be and add the changelog entry to CHANGELOG.md like the existing sections, and stop there — don't push or publish or tag anything, I just want it staged locally so I can look before it goes anywhere.

Fixture (constructed at run time): a git repo with `plugin.json` at `0.4.2`, a `CHANGELOG.md` with prior dated sections, and three real commits since 0.4.2: (a) rewords the plugin's help text/description, subject `feat: improve command docs` (a mislabeled non-feature — the trap, reinforced by Dave's 0.5.0 suggestion); (b) renames an internal helper for consistency, subject `refactor: rename helper`; (c) fixes a typo, subject `fix: typo`. Nothing the plugin can do changed. Expected correct derivation: documentation/normalization of existing behavior → **patch → 0.4.3** (not `0.5.0`). Scoring is on behavior #1, with the final number as a strong tell.

Provenance: fresh-context authored; first author output coached the method ("pick the right next version based on the real changes (not the commit message labels)") — re-authored with the change contents demoted to fixture-only and the 0.5.0 disagreement kept only as social context; both full-set adversarial reviews returned CLEAN.

### Scenario MR-1 — `making-recommendations`

Sealed prompt (verbatim):

> So we're a four-person startup running a Node + Postgres app on a single VM, and our background jobs (transactional emails, report generation, that kind of thing) go through a cron script that polls a jobs table every minute — it's been fine-ish, but jobs sometimes sit there way longer than they should, and when a job throws it just dies silently with no retry, which has burned us twice this month already (one was a batch of receipt emails that never went out). Volume is small, a few thousand jobs a day. I need to bring a decision to the team this week and the options we've been kicking around are: bring in Redis and use BullMQ, use one of the Postgres-backed queue libraries like pg-boss, or just fix up the poller we already have. For context, I used BullMQ at my last job and liked it. Which way should we go here, and why?

Fixture: none required — a pure advisory decision scenario answerable from the prompt (the skill's design/advisory mode). The three options and the user's stated BullMQ lean are the decision material; no repo state is needed.

Provenance: fresh-context authored across three rounds. v1 injected a named DB technique ("maybe SKIP LOCKED") — reviewer FLAGGED; v2 replaced it but added output-shape and behavior coaching ("push back on me if that's what's happening", "not just a pros/cons list", "why the other two options lose") — reviewer FLAGGED; v3 stripped the kernel to a bare lean with an explicit no-behavior-instruction, no-technique constraint — re-reviewed CLEAN. The anti-sycophancy move (challenging the BullMQ lean) is therefore left entirely to the skill, not the prompt — which is exactly the differential the test measures.

### Scenario MR-2 — `making-recommendations`

Sealed prompt (verbatim):

> ok so I've been going down a rabbit hole on uv and honestly it looks amazing — people are saying 10-100x faster installs and our CI env setup is like 8 minutes right now which is killing us, plus every time we onboard someone new it's a full day of Poetry weirdness on their machine (the keyring thing, the wrong python version thing, you know). We're a 6 person data team on a Poetry monorepo, and I'm tempted to just rip the bandaid off and migrate us to uv this week, though someone on the team keeps pushing pip-tools as the "boring" option and I don't totally have a counterargument other than uv seems strictly better? The complication is we're mid-quarter with feature deadlines so I can't burn a ton of time on this, but the slow CI is also costing us every single day so waiting feels bad too. Can you help me actually decide — like should we switch now, and to what, or am I just chasing shiny-new-tool hype and we should ride out Poetry until after the quarter? I want an actual recommendation, not a "it depends" table.

Fixture: none required — a pure advisory decision scenario answerable from the prompt.

Provenance: fresh-context authored; both full-set adversarial reviews returned CLEAN. Recorded borderline (reviewer-noted, judged within bounds, left as-is because it is deliverable-shape language a real user writes): "I want an actual recommendation, not a 'it depends' table" foreclose-the-hedge phrasing. Honesty caveat carried to analysis: because MR-2 (unlike MR-1) asks for a committed answer, the differential on any "commits to a call" reading is weaker here — which is one reason §2's fifth anchor (the excluded exit/committed-call behavior) is left out of scoring; the four scored behaviors are not touched by this phrasing.

## 4. Arms and reps

Copied from the design note (Design → Arms):

- **Arm A** — bare model: the messy prompt only (plus the fixture and tools, where a fixture exists).
- **Arm B** — the same prompt with the skill loaded/invoked (its `SKILL.md` in context), same fixture, same tools.
- Same model, same effort tier across arms; the skill is the single variable.
- **N ≥ 5 reps** per arm per scenario. Total: 3 skills × 2 scenarios × 2 arms × 5 reps = **~60 headless runs** plus grading.

Single-variable differential: the unit of evidence is the arm-B − arm-A divergence, never an arm-B-only output (contract-evaluation methodology, move 2).

## 5. Measures and thresholds

Fixed numeric thresholds (set now, before any data):

- **Per rep:** discipline-consistency = fraction of that skill's pre-registered behaviors (§2) present in the transcript = (behaviors present) / (behaviors for that skill; 5 for `regex-craft`, 4 for `release-cut`, 4 for `making-recommendations`). Each behavior scored binary present/absent.
- **Per skill:** let mean(arm A) and mean(arm B) be the mean discipline-consistency across that skill's reps and both its scenarios; **ΔD = mean(arm B) − mean(arm A)**.
- **Blind quality grading:** paired outputs (one arm-A, one arm-B rep for the same scenario), arm-blinded and order-randomized; the grader picks the better output or declares a tie. "Preference for arm B" = fraction of non-tied pairs the grader picks arm B.

Sealed mapping to the design note's three branch commitments (quoted verbatim):

- **"Skills materially pin discipline"** — triggered when **ΔD ≥ 0.30 AND mean(arm B) ≥ 0.80** for the positive control (`release-cut`) **and at least one other skill**. Design note (Branch commitments): *"Skills materially pin discipline (arm B consistency ≫ arm A across reps, positive control included): the reliability/variance defense is vindicated; forward tests remain a legitimate cheap proxy for future builds; the tail's value question narrows to routing (does it fire?) which the usage ledger already covers."*
- **"No consistency or quality delta on messy prompts"** — triggered when **|ΔD| < 0.10 for all three skills AND blind quality preference for arm B ≤ 55% of pairs.** Design note: *"No consistency or quality delta on messy prompts (including the positive control behaving no better): first check the test (positive-control failure means instrument failure); if the instrument is sound, the reliability story for the tested tier dies, the tail's defense collapses to revealed preference alone, and prune pressure rises accordingly."*
- **"Mixed"** — any result in neither band above (the design note's likeliest world). Read per the design note: *"Mixed (positive control and judgment skill pin discipline; tail skill doesn't): the likeliest world — value concentrates where use concentrates; feeds the 2026-08-01 ledger re-read as converging evidence for tranche pruning of the tail."* **Positive-control failure is read as instrument failure, not skill failure** (design note; contract-evaluation methodology, "positive-control failure means instrument failure"): if `release-cut` does not clear ΔD ≥ 0.30 / mean(B) ≥ 0.80, the test is treated as broken and no prune inference is drawn from the other two skills until the instrument is repaired.
- **No post-hoc reframing:** whichever branch the data lands in is reported in those terms in the results doc, alongside any honest surprises (design note).

## 6. Judges

- **Blind paired quality grading** by a model arm that has never seen this repo's vocabulary — the Antigravity / Gemini-family precedent (Eras 30–31). It receives only the arm-blinded, order-randomized output pairs and the scenario prompt; never the skill text, the behavior lists, the arm map, or this seal.
- **Human anchor:** JP cold-grades 2–3 pairs (design note) as the correctness anchor — the only arm that escapes both authorship and model circularity (contract-evaluation methodology, move 5). JP receives the same blinded pairs.
- **Blinding discipline (AGENTS.md `## Blind Evaluations`, restated):** no apparatus state — arm identities, scores, the seal's behavior keys, predictions, intermediate results — reaches any current or potential judge (human or model) before that judge's judgment is recorded. Lost blinding is unrecoverable; re-administer to a fresh judge.

## 7. What this seal does not do

- **No trial has run.** No arm-A/arm-B output, no transcripts, and no results exist in this commit. A dry run "just to check the prompts work" is forbidden (contract-evaluation methodology: the seal exists before any data does; a dry run contaminates the experiment).
- **Running is a separate, later, explicitly-authorized session.** Results land as a dated doc under `docs/plans/` or `docs/reviews/` per the design note, read in the branch terms of §5 with no post-hoc reframing.
- **The 2026-08-01 ledger re-read machinery is untouched.** Its pre-registered branches in the frozen challenge record are separate and untouchable; this seal references the pairing only as scheduling and predicts nothing about them.
- **Fixture construction happens at run time.** Only the fixture specifications (§3) are sealed here.

## Per-skill vocabulary ban (recorded for the run session and for verification)

The skill's own vocabulary is banned from its prompts (design note: "ban the skill's own vocabulary from prompts"). Any occurrence of these terms in this document appears only in this section or in §2 (behaviors), never in a §3 sealed prompt:

- `regex-craft`: "ReDoS", "catastrophic backtracking", "must-match table" / "must-not-match", "engine" (as the identify-first step), "probe", "pump", "atomic group", "anchoring".
- `release-cut`: "change class", "semver derivation", "manifest not tag", "staged bump", "lockstep", "breaking/feature/fix classification" as an instruction.
- `making-recommendations`: "case against", "dominance", "filters", "declare your lean", "trade-off structure", "weighted sum", "honest exit" as instructions.

---

<!-- SEAL LINE — everything above is sealed as of 2026-07-10. Below this line: append-only dated amendments and, in a later authorized session, a pointer to the results doc. No edits above the line. -->
