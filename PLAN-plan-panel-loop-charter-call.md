# PLAN: Discharge the `plan-panel-loop` charter classification

Rank: 4 of 5 — small, but it is the only OPEN charter item on the books. The throughline Frontier (Era-83 carry-forward) says: "OPEN — `plan-panel-loop` charter classification: within-turn subagent dispatch; its `ddf1e6b` containment spine leans build-and-prune but no ledger entry records the call. Confirm against the 'no human reads at call time' clause." This plan runs that confirmation and records the result durably.

## Goal

Determine whether `skills/plan-panel-loop` is build-and-prune or charter-gated under `docs/agents/charter.md`'s Reversibility Class, and record the determination with a one-line dated ledger entry so the open question stops carrying forward.

## Ground rules (repo invariants — do not skip)

- Branch first (`chore/plan-panel-loop-charter-call`); the hook blocks `main` edits. Never `rm`.
- The ledger is append-only. One line, at the end of the Decisions section, before `## Parks`.
- Expected outcome is a CLASSIFICATION note, not an admission: if (and only if) the determination comes out build-and-prune, no Admission test runs — build-and-prune skills do not take one. The entry exists because the throughline flagged the question as open and the ledger is the runtime-neutral durable record; precedent for inline classification reasoning is the Era-84 entry's own language ("`triage` model-invocable ≠ unattended"; "`resolve-conflicts` operates in mid-operation git state but resolves reversibly → ordinary case-(d) admit").
- Do NOT edit `skills/plan-panel-loop/` itself. If your analysis concludes the skill's TEXT needs hardening to stay ungated, stop and report that instead — text changes are a separate decision for JP.

## Exact files to touch

1. `docs/agents/contract-decisions.md` — one appended line. Nothing else.

Read-only inputs: `docs/agents/charter.md` (Reversibility Class, lines ~15–22), `skills/plan-panel-loop/SKILL.md`, `skills/plan-panel-loop/references/subagent-brief.md`, `git show ddf1e6b` (the containment commit).

## Steps, in order

### Step 1 — branch and read

`git status --short --branch`; `git checkout -b chore/plan-panel-loop-charter-call`; then read the four inputs above in full.

### Step 2 — answer the three classification questions, each against quoted text

The charter clause (charter.md ~line 22): a skill is gated despite its packaging if it "can fire unattended (a cron routine, a remote trigger, a subagent dispatch no human reads at call time)" or "wields irreversible-effect tools (send, merge, force-push, delete)". Third-party material is gated regardless.

**Q1 — Can it fire unattended?** The clause's "subagent dispatch no human reads at call time" describes the SKILL ITSELF running inside an unattended context — not a skill that dispatches subagents during an attended session. This distinction is the entire crux, and conflating the two is the likely error the open question exists to check. Evidence to weigh: the frontmatter description fires "only when the user explicitly wants an iterative adversarial panel" (SKILL.md line ~3); the Trigger Boundary repeats "only when the user wants all three parts" (~line 14); the containment section forbids reviewers from running `plan-panel-loop`, other panels, or any multi-agent workflow inside their review (~line 65), which blocks the recursive path by which the skill could end up firing where no human reads; the main agent alone consolidates, patches, and reports in the user-visible transcript (~line 55). There is no cron/remote-trigger surface, and `disable-model-invocation` is not set — but model-invocation in an attended session is still attended (the Era-84 `triage` precedent: "model-invocable ≠ unattended").

**Q2 — Does it wield irreversible-effect tools?** Evidence: reviewers are READ ONLY with an explicit no-edit/no-commit/no-push/no-external-state list (~lines 59–63); the main agent patches ONLY the named plan artifact (~line 79); for remote artifacts (issues, PR bodies) the default is a patch-shaped replacement in chat, not editing the remote surface (~line 24); file edits in a git worktree are reversible. No send/merge/force-push/delete.

**Q3 — Is it third-party material?** No — first-party Era-83 build (commits `4616498`, `ddf1e6b`).

Confirm each answer yourself against the live files — do not trust this plan's line numbers if the file has changed (`git log --oneline -3 -- skills/plan-panel-loop/` to check for drift since `ddf1e6b`; if the skill changed materially since, re-read before answering).

### Step 3 — branch on the outcome

**Expected outcome (all three answers as above): build-and-prune.** Append this entry to the ledger (adjust date; one logical line):

> - 2026-07-NN — plan-panel-loop charter classification (Era-83 open question, discharged): **build-and-prune, not gated**. The Reversibility-Class read (charter.md ~:22) on the live skill text: it cannot fire unattended — invocation requires the user explicitly wanting panel+patch+re-review (SKILL.md description and Trigger Boundary), reviewers are forbidden from running it or any nested panel (Subagent Containment), and its within-turn subagent dispatch happens inside an attended session whose consolidated findings and closeout land in the user-read transcript — dispatching subagents ≠ being a "subagent dispatch no human reads at call time" (same seam as Era-84's "triage model-invocable ≠ unattended"); it wields no irreversible-effect tools — reviewers are read-only by brief, the main agent patches only the named plan artifact, and remote targets default to chat-shaped replacements; and it is first-party (Era-83 build, containment spine `ddf1e6b`). Classification note only — no Admission test runs for build-and-prune; recorded because the throughline carried the question as open. Evidence: `skills/plan-panel-loop/SKILL.md` + `references/subagent-brief.md` at this commit, `ddf1e6b`.

**Divergent outcome (any answer differs — e.g. you find live text permitting unattended fire or an irreversible tool):** do NOT write a build-and-prune entry, do NOT run an Admission test on your own authority, and do NOT edit the skill. Report the specific quoted text that flips the answer and stop. That finding changes what JP must decide (gate it, or harden the text), and pre-empting it would be exactly the kind of unattended gating decision the charter reserves.

### Step 4 — validate and commit (expected-outcome path only)

```bash
git diff --check
git add docs/agents/contract-decisions.md
git diff --cached --stat   # exactly one file
git commit -m "docs(charter): discharge plan-panel-loop classification — build-and-prune, not gated (Era-83 open question)"
```

Do not merge or push unless JP asks.

## Edge cases found during exploration (a weaker model would miss these)

- The tempting misread: "the skill dispatches subagents, subagents are mentioned in the gating clause, therefore gated." The clause gates skills that FIRE where no human reads; plan-panel-loop's dispatches happen inside a session the human is driving, and its outputs must surface in the transcript (Closeout packet is mandatory). Quote the clause and the skill text side by side in your reasoning; do not paraphrase either.
- `disable-model-invocation` being absent is not evidence of unattended fire. Two already-adjudicated skills (`triage`, model-invocable, tracker-writing) establish that model-invocable-in-attended-session stays ungated when effects are reversible and approval-gated.
- Build-and-prune churn "takes no ledger entry" (charter Decision Record) — but this entry is not churn (nothing is being built or pruned); it is the recorded discharge of a flagged classification question. Keep it one line precisely so it does not become the ceremony the charter warns against. Do not also create a park, an admission, or any companion doc.
- The skill's `agents/openai.yaml` exists (it is dual-runtime, in `skills/`). Classification does not depend on runtime reach; do not go down that path.
- If you find the SKILL.md has materially changed since commit `ddf1e6b` (new tool grants, changed containment), the analysis above may be stale — re-derive from live text, and say in the entry that you did.

## Acceptance criteria (verify each; do not claim done without output)

1. All three classification questions answered in the session with direct quotes from the live charter and skill text (not from this plan).
2. Exactly one line appended to `docs/agents/contract-decisions.md`; every pre-existing line byte-identical (`git diff` shows a single added line).
3. No changes under `skills/plan-panel-loop/`.
4. `git diff --check` clean; one commit on `chore/plan-panel-loop-charter-call`.
5. If the divergent path fired: no ledger entry, no commit, and a report quoting the flipping text — that outcome also satisfies this plan.
