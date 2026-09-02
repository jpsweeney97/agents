# 2026-09-02 — `decide:decision-record`: first real capture in a project repo

Behavior evidence for the packaging arc's last unrun proof. The 2026-09-02 join of `decision-record` into the `decide` plugin (decide 1.1.0, `fc4166e`/`90a3ad9`) was proven by fresh-session listings and load probes on both runtimes; those showed discovery and reference-following, not a capture. This record is the capture, plus a same-day second stage that exercises the genealogy edit on real supersessions.

Method: one context-isolated `claude -p` run (Claude Code 2.1.258, model `claude-fable-5-1`, `--permission-mode acceptEdits`, an allow-list of read tools plus `Write`/`Edit` and non-publishing `git` subcommands, `git push`/`WebFetch`/`WebSearch`/`Agent` disallowed, stdin from `/dev/null`), started in `/Users/jp/Projects/active/cross-model` on a fresh working branch `chore/record-answer-artifact-decision` (the repo's branch policy; the user-level `require-gitflow` hook blocks writes on `main`). The prompt was the plugin token `/decide:decision-record` followed by a plain request naming the subject and its source documents only — no number, no format hints, no supersession hints. The parent session graded every observation from the `stream-json` tool log and from `git` afterwards, never from the run's own report.

## The claim and the scenario

**Behavior claim.** Invoked in a real project repo with a real, settled, un-captured decision, the plugin-distributed skill reads the whole source, reuses the repo's existing ADR convention through the plugin's own `references/ADR-FORMAT.md`, writes the record at the next sequential number with the real rationale and the genuinely considered options, performs the supersession scan without flipping any still-valid record, commits only the ADR on the working branch with the contract's message shape, and reports what it scanned and changed without claiming a corpus-wide guarantee.

**Scenario.** Cross-model's 2026-08-26 UX-diagnosis session decided that every `/synapsis` run ending writes a human-readable `answer.md` into the run dir as a skill-side obligation, declining the driver-side form (option D of `docs/audits/2026-08-26-synapsis-ux-diagnosis.md`). The repo's own `docs/agents/domain.md` says a new host obligation needs an ADR home first, and no ADR, playbook, or spec named `answer.md` (grep-verified before the run). The corpus held 37 ADRs, all `Status: accepted`, with two same-subject neighbours (0036 and 0037, both carrying 2026-08-26 addenda) as the over-flip temptation.

## Result: passed

| Observation | Contract requirement | Verified how |
|---|---|---|
| Read the audit and both named handoffs in full before anything else (tool calls 1, 5, 6) | Read the whole source first | tool log |
| Read `ADR-FORMAT.md` through `~/.claude/skills/decide/references/` (call 4), i.e. the plugin's own reference, resolving to the canonical | Reuse the format, never fork it | tool log |
| Listed all 37 titles (call 3); read 0001, 0002, 0025, 0030, 0034, 0035, 0036, 0037 in full (calls 7, 8, 14, 15, 16, 20, 21, 22); checked `git log --all` for a pre-existing 0038 on any branch (call 35) | Scan for the next number and for supersession candidates | tool log; the report's list of records read matches the log exactly |
| `git status` before the first write (call 9) and again before staging (call 38) | Write safety | tool log |
| Wrote `docs/adr/0038-require-a-readable-answer-artifact-at-every-run-ending-after-the-synapsis-ux-diagnosis.md`: title-case H1, `Status: accepted`, `Context:` / `Decision:` / `Consequences:` / `Considered Options:` / `Revisit when:` labelled paragraphs, the corpus's closing idiom "builds on … and supersedes none", wrapped near 80 columns like 0037 | Match the existing convention | file read; `git diff --check` clean |
| No existing file touched: `git diff --name-status main..HEAD` shows one `A` line | Change a status only when the old decision no longer holds | git |
| Record dated to the decision (2026-08-26) with one light provenance sentence naming the write date and sources | Date by the source; one light `Source:` phrase allowed | file read |
| Rationale kept unflattering and contingent: the best-ever output had vanished from the record; the ADR home came after the obligation; option D's single stated reason and its reconsider condition preserved; options A–D recorded as the source states them, C marked held so its absence is not read as rejection | Capture faithfully; never retrofit a tidy justification | file read against the audit's Options section |
| Commit `8767ac3`, message `docs(adr): record 0038 <slug>`, only the ADR staged, tree clean after, nothing pushed | Default local commit on a working branch; never push | git |
| Report named the records scanned and the one written, stated no Status was changed, and said the scan is "a title scan plus a same-subject read, not a guarantee" | Report what you did, claim no more | run output |
| Report disclosed one paragraph as the agent's own inference (the "from this record on, changes land in an ADR" sentence) and asked the user to keep or strike it | Honest provenance | run output |

Factual claims inside the new ADR were spot-verified rather than trusted: the "eight run dirs since the decision all hold `answer.md`" claim (eight directories 2026-08-26 through 2026-09-02, every one with the file), the "written at 14:14, issues landed at 14:21" staleness example (from the 2026-08-26 14:25:02 handoff), and the one-line characterizations of ADR-0002, 0025, and 0030 (each consistent with that ADR's `Decision:` line).

Run size, for the record only: 44 turns, 43 tool calls, 6.3 minutes, about $4.74.

## Observations that are not failures

- The run read beyond the named sources — the live synapsis skill, the run-lifecycle playbook, the throughline, a later handoff, run dirs under `~/.synapsis/` — to ground the Consequences paragraph. The contract asks for the whole source; extra grounding is within it. Nothing from the parent session's own arc (the format-home deliberation whose `answer.md` it also opened) leaked into the record.
- One multi-command `ls` over `~/.synapsis/` was refused by the allow-list; the run recovered with `Glob`. Harness artifact, not skill behavior.
- The right-size prompt ("an ADR may be overkill") was not offered. It was not owed: the decision is a host obligation the repo's own rule says needs an ADR home.
- The record is long (about 1,650 words). The format allows a single paragraph; the corpus convention is long labelled paragraphs (0037 is about 2,600 words). Matching the convention is the contract's instruction.

## Stage 1 proof boundary

- The load-bearing genealogy edit (adding or changing a `Status: superseded by ADR-NNNN` line) was not exercised by this stage. No real reversal exists in cross-model's corpus — every supersession there is partial and named in prose — and no reversal was fabricated. The negative side was exercised and held: two same-subject neighbours, no flip. Stage 2 below exercises the edit on real supersessions from two repos.
- Not exercised: the confirm-before-change question, the placement question for a `CONTEXT-MAP.md` repo, the dirty-target and slug-collision paths, the protected-branch skip-the-commit path, and Codex-side `$decision-record` invocation.
- One sample, not a rate. A repeat is `skill-benchmark`'s job.
- The fire is invisible to the live skill-usage hook: a `-p` prompt beginning with a slash command is expanded by the harness, not invoked through the `Skill` tool, so no `PostToolUse` row was written. The transcript carries `<command-name>/decide:decision-record</command-name>`, which the miner's user-typed path records at its next run.
- The captured ADR was merged into cross-model `main` as `8767ac3` on JP's later instruction through `merge-branch`; the merge is no part of this proof.

## Stage 2 — the genealogy edit, on real supersessions from two repos (same day, on JP's direction)

Stage 1 left the load-bearing edit unexercised. The same harness ran three more captures in disposable clones under the session scratchpad, each clone checked out at the commit just before a real ADR landed, with `main` reset to that same commit, every later ref deleted, and reflogs expired and pruned, so no proxy could read the real later record through `git show main:…`. Clones had no remote. Sources were the real material of the day: for cross-model, the issue #53 thread fetched with `gh` plus the two #53 commit messages; for athena-kb-local, a verbatim excerpt of the 2026-08-27 01:31 handoff (its arc paragraph, Decisions list, and the record of the failed attempt) with the two post-hoc sentences naming the resulting ADR removed, leak-gated before launch. Two harness defects were caught and fixed before any graded run: a first launch left the modern `main` reachable in both clones (one proxy noticed `main` was far ahead and began reading its corpus), and a first excerpt kept one `ADR-0011` mention and lost the ruling's opening sentence. Both runs were killed, the clones rebuilt, the excerpt rewritten from explicit text, and the runs relaunched.

| Stage | Clone, checkout | Real record re-captured | Result | Observed |
|---|---|---|---|---|
| 2a | cross-model at `dcfa03d^` (before ADR-0023) | 0023, whose source thread calls it "a superseding ADR" while ADR-0022's three parts (single-shot argv, adapter boundary, host-move convention) all stay in force | **passed** — partial supersession, no flip | Wrote 0023 in the 0022-era unwrapped style; kept 0022 at `Status: accepted` with the reason stated ("marking it superseded would tell a reader those are no longer in force, which is false"); cited 0022's own precedent of discharging 0009 without a status change; named the relationship in prose; put the flip to the user as an option. One ADR committed; the untracked source left alone and named. |
| 2b | athena-kb-local at `656fc17^` (before ADR-0011) | 0011, which the maintainer's own commit recorded as `status: superseded by ADR-0011` on 0010 | **not strong enough** for the edit; a real finding | Detected 0010 as the same-subject record and read it in full, but judged the ruling as narrowing one bound ("no file") rather than replacing the record: kept 0010 at accepted, appended a dated "Scope amendment" section to 0010 (this repo's convention; ADR-0002 carries five), wrote 0011 as a narrow record, and asked whether to keep the amendment or revert to prose-only. Every factual claim it made checked out: the amendment convention, the tracked no-trailer rule in the issue-27 plan, links, whitespace. |
| 2c | same clone, session resumed | the same, under one scenario turn: "treat this as a full replacement of ADR 0010 … 0010 should point forward to it" | **passed** — the status edit | Set `status: superseded by ADR-0011` in the file's lowercase frontmatter; removed its own amendment so 0010's only difference from its original body is the status line (verified by diff); rewrote 0011 to carry forward the corpus decision that still holds, opening with "This supersedes ADR 0010"; renamed the slug to the wider scope with `git mv`; committed as `docs(adr): record 0011 as the consultation record, supersede 0010`; left the excerpt untracked as told; reported scanned and changed records with no corpus-wide claim. |

Run sizes: 2a 18 turns, 2.8 minutes, about $2.13; 2b 41 turns, 5.6 minutes, about $3.41; 2c 14 turns, 3.2 minutes, about $1.37; the two killed partial runs are uncounted.

**What stage 2 establishes.** The skill will not flip a status on the strength of a source's own "superseding" language when the old decisions still hold (2a), and it performs the full edit correctly, in the target repo's own frontmatter convention, once the replacement is explicit (2c). Its unprompted replace-versus-narrow judgment can differ from the maintainer's (2b): the human record treated a full restatement with one changed bound as a supersession; the proxy treated the same ruling as an amendment, because the contract's decision rule ("change a status only when the old decision no longer holds") reads as no-flip when most of the old record survives, while its detection sentence also lists "replaces". Both readings are self-consistent; the divergence is the finding.

**Two contract observations for the owning lane, not applied here.** First, the replace-versus-amend call: the contract could say that a new record which restates the old one and changes a bound replaces it (supersede), while a record that leaves the old one governing and narrows a bound is a prose cross-reference. Second, a repo whose convention appends dated amendment sections to old records collides with the contract's "a settled record's body is never rewritten; only its Status changes"; the 2b proxy chose the repo's convention and disclosed the choice. `decision-record` is plugin-distributed, so any edit follows the Plugin Layout publish path.

**Stage 2 proof boundary.** Headless runs cannot confirm before changing: 2b appended its amendment and asked afterwards; 2c acted on the scenario turn. The scenario turn in 2c was written by the grading session, not by JP. Both clones were pre-arranged states, not live work, and the athena source was an excerpt, not the whole handoff. One sample per stage. The real repositories were untouched throughout, re-verified after the runs.

## Structural checks

`quick_validate.py` on `plugins/decide/skills/decision-record`: valid. `plugins/decide/.claude-plugin/plugin.json` parses (decide 1.1.0). `../../references/ADR-FORMAT.md` resolves from the skill directory. `git diff --check -- plugins/decide` clean. Library integrity sweep at `90a3ad9`: 6 owned checks and 5 delegated canaries all pass, including check 6 on the `grill-with-docs` alias.

## Durable artifact

This record. The runs' `stream-json` logs and the stage-2 clones lived in the session scratchpad and are not kept; every claim above names the observation it rests on so a run can be re-derived from a fresh invocation rather than from a log.
