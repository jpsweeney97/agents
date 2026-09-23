# Repo Hygiene Audit — `~/.agents`

Status: complete
Date: 2026-09-23
Target: `/Users/jp/.agents` at `deefb04` (`main`, level with `origin/main`), plus the places this repo delivers into or reads from: `~/.claude/skills`, `~/.claude/settings.json`, `~/.codex`, and the satellite worktrees under `/Users/jp/.agents-worktrees`
Mode: read-only. Nothing was changed. Every action below is a recommendation.
Artifact path: `docs/audits/2026-09-23-repo-hygiene-audit.md`
Follow-up: fixes were applied the same day, after the audit; see Follow-up at the end.

## Result

**The repo is structurally healthy, but its two automatic checks fail on every run for reasons that are not real defects, so a real new failure would not stand out.** Separately, 33 of the repo's skills reach Claude with no description, because the skill listing is over its size limit, and one skill (`athenahealth-brand-system`) tells agents to use nine files that do not exist.

The audit found 38 distinct problems after merging duplicates: 4 high, 7 medium, 20 low, and 7 informational. A separate verifier agent re-checked every finding. It refuted none and corrected the severity or scope of 11. The main session re-checked the four high findings and the ledger findings a third time.

"Hygiene" here means things that are stale, orphaned, duplicated, inconsistent with each other, misplaced, undocumented, broken, or leftover clutter. This audit does not judge whether any skill's method is good. Per `AGENTS.md`, it never treats a skill's silence in this repo as a reason to remove it.

Severity scale:

- **High:** breaks delivery, routing, validation, or a check right now, or leads an agent into a wrong action.
- **Medium:** drift or inconsistency likely to cause a wrong action or confusion later.
- **Low:** clutter or a cosmetic inconsistency with little effect.
- **Info:** worth recording; no action needed, or already known and deliberately held.

## Fix First

1. **Stop the false failures in both checks (H1, H2).** Two small script edits: exempt `synced` in `scripts/claude-skills-sync.sh`, and make the orphan check in `scripts/check-library-integrity.sh` recognize Python imports. After that, both checks pass, and any future failure means something.
2. **Decide how to make room in the skill listing (H3).** Until then, 33 skills can be invoked by name but are unlikely to be chosen on their own.
3. **Fix the `athenahealth-brand-system` asset paths (H4).** Rename two template references and either add or stop citing the fonts and logo.
4. **Make one decision about claude.ai skill sync (M1, M2, M3).** The three findings share one cause and one decision.
5. **Land or discard the stranded ledger entry (M4) before deleting any branches (L5).** Deleting that branch first would destroy the only copy.

## Findings at a Glance

| # | Severity | Finding | Where | Who fixes it |
| --- | --- | --- | --- | --- |
| H1 | high | Sync check calls Claude Code's own claude.ai sync folder a stray and says to trash it | `scripts/claude-skills-sync.sh:60` | Direct script edit |
| H2 | high | Orphan check flags three live `cross-model-review` modules as unused | `scripts/check-library-integrity.sh:162-183` | Direct script edit |
| H3 | high | 33 repo skills reach Claude with no description (listing over its size limit) | `~/.claude/settings.json:12`; skill descriptions | JP decision; `update-config` for settings |
| H4 | high | `athenahealth-brand-system` cites nine asset files that do not exist | `skills/athenahealth-brand-system/` | Satellite edit via `worktree-task-cycle` |
| M1 | medium | 11 out-of-date claude.ai copies of live skills, plus one deleted skill, load in Claude Code | `~/.claude/skills/synced/` | JP decision on claude.ai |
| M2 | medium | Three repo documents say custom skills do not sync; they now do | `AGENTS.md:26`; `exports/README.md:7`; `skills/skill-export/SKILL.md:9` | Direct edit after M1 decision |
| M3 | medium | Synced `anthropic-skills:skill-creator` contradicts "no Claude-side constructor skill" | `AGENTS.md:75` | JP decision, with M1 |
| M4 | medium | A ledger entry exists only on an unmerged branch whose worktree folder is gone | branch `chore/codex-handoff-auto-commit-exception` | Branch flow, then `git worktree prune` |
| M5 | medium | `teach` and `to-questionnaire` are explicit-only on Claude but not on Codex | `skills/{teach,to-questionnaire}/agents/openai.yaml` | Satellite edit |
| M6 | medium | Ledger holds 32 decision entries under the "Mining Queue" heading | `docs/agents/contract-decisions.md:103-192` | Direct doc edit |
| M7 | medium | Ledger evidence pointers that no longer resolve | `docs/agents/contract-decisions.md:25,64,66,70` | Direct doc edit |
| L1 | low | `work-skills/` is not described in `AGENTS.md`; 6 of its 18 sources changed | `work-skills/`; `AGENTS.md:21-31` | Direct doc edit |
| L2 | low | Four live skills have no satellite worktree | `/Users/jp/.agents-worktrees/` | `satellite-fleet.py create-missing` |
| L3 | low | Charter's Decision Record section leaves out gated skills | `docs/agents/charter.md:68` | Charter edit (its own procedure) |
| L4 | low | The only open GitHub issue (#20) is already fixed | GitHub `jpsweeney97/agents#20` | Close the issue |
| L5 | low | 23 merged local branches, one merged remote branch, one leftover config section | `refs/heads/*`; `.git/config` | `git-hygiene` |
| L6 | low | Ignored `.agents/scratch` is cited by 12 tracked files | `.agents/scratch/` | JP decision; do not trash as stale |
| L7 | low | `.skill-lock.json` is undocumented and partly stale | `.skill-lock.json` | Direct edit |
| L8 | low | `skills-archive/README.md` describes 7 of 11 archived skills | `skills-archive/README.md` | Direct doc edit |
| L9 | low | `the-gang-explains` uses a Claude-only placeholder and hard-wrapped prose | `skills/the-gang-explains/` | Satellite edit |
| L10 | low | `AGENTS.md` list of Codex-bundled names is out of date | `AGENTS.md:29` | Direct doc edit |
| L11 | low | `skill-lifecycle-notes.md` describes the old `deliberate` | `docs/agents/skill-lifecycle-notes.md:15,73` | Direct doc edit |
| L12 | low | ADR 0001 has no Status line; its subject is archived | `docs/adr/0001-*.md` | Direct doc edit |
| L13 | low | `AGENTS.md` omits two `docs/agents` files, the test suite, and `.out-of-scope/` | `AGENTS.md:48-55` | Direct doc edit |
| L14 | low | 12 plans and specs still show an open status | `docs/plans/`; `docs/specs/` | Direct doc edit |
| L15 | low | Empty leftover directories and ignored cache folders inside skill folders | several | `git-hygiene`; hook edit is JP's choice |
| L16 | low | 12 of 53 allow rules in the repo-local Claude settings name missing paths | `.claude/settings.local.json` | `update-config` |
| L17 | low | `.git` still holds state files from the removed security-guidance plugin | `.git/sg-*` | Trash after approval |
| L18 | low | Two `openai.yaml` short descriptions exceed 64 characters | `plugins/decide/skills/{deliberate,outcome-shaping}/agents/openai.yaml` | Next `decide` release |
| L19 | low | Whitespace errors in four tracked files; `.gitignore` has no final newline | `docs/…`; `.gitignore` | Direct edit (optional) |
| L20 | low | A skill script has a shebang but no executable bit, unlike its sibling | `skills/simplify-code/scripts/create_simplify_backup.py` | Satellite edit |
| I1 | info | Satellite fleet check exits 2 on every run while the parked draft stays | `scripts/satellite-fleet.py` | None |
| I2 | info | `decision-record` still routes to archived `postmortem` (known, held) | `plugins/decide/skills/decision-record/SKILL.md:3,68` | Held for next `decide` bump |
| I3 | info | 11 descriptions exceed ~90 words (allowed by policy) | various | Input to H3 |
| I4 | info | The `steelman` export shows STALE only because `openai.yaml` was added | `exports/steelman/SKILL.md` | None |
| I5 | info | ruff 0.16.0 reports 93 style findings; the repo has no lint gate | `scripts/`; `tests/` | None |
| I6 | info | Night-porter Desktop task prompt is prepared but not registered | `scripts/night-porter-task-prompt.md` | None |
| I7 | info | 1,500 loose git objects and three Codex checkpoint refs | `.git/objects`; `refs/codex/` | None |

## High

### H1. The sync check calls Claude Code's own claude.ai sync folder a stray and says to trash it

- **What is wrong:** `scripts/claude-skills-sync.sh --check` reports `UNMANAGED: /Users/jp/.claude/skills/synced ... add to EXEMPT or remove with trash`. The folder is where Claude Code downloads the skills enabled on JP's claude.ai account. `EXEMPT` on line 60 lists only `synapsis`.
- **Evidence:** The Claude Code docs (skills, "Skills synced from claude.ai") say: "Claude Code downloads your account's skills into `~/.claude/skills/synced/` in the background, then checks claude.ai for changes about every 10 minutes." The folder holds two account buckets, each with a `manifest.json`. This check runs at every session start and printed the UNMANAGED line at the start of this session.
- **Why it matters:** The check now fails on every run, so a real delivery break would look the same as today's noise. The message also offers "remove with trash", which would not work: Claude Code downloads the folder again at the next sync.
- **Recommended action:** Add `synced` to `EXEMPT`, with a comment that Claude Code owns it (cite the docs section above). Update the recovery copy in the script header if it lists exemptions. If the M1 decision is to stop syncing, the setting `syncClaudeAiSkills: false` also removes the folder.
- **Who fixes it:** Direct edit to `scripts/claude-skills-sync.sh`. `scripts/` is not a skill surface, so a working branch in the primary checkout is enough.

### H2. The orphan check flags three live `cross-model-review` modules as unused

- **What is wrong:** `scripts/check-library-integrity.sh` reports `[FAIL] orphan support file` for `skills-claude/cross-model-review/scripts/cmr_archive.py`, `cmr_engine.py`, and `cmr_protocol.py`. All three are live code.
- **Evidence:** `review.py:17` has `import cmr_engine as engine`. `review.py:18` has `from cmr_archive import Archive, ReviewError`. `cmr_engine.py:10-11` imports `cmr_archive` and `cmr_protocol`. `SKILL.md:18` names `review.py` as the helper. The orphan check (lines 162-183) searches the bundle only for the file name with its `.py` extension, and a Python import names a module without the extension. The skill's own test suite passes (61 tests), which also shows the modules are in use.
- **Why it matters:** The repo's main structural check is red on every run. Its message suggests deleting live code.
- **Recommended action:** In the orphan check, for a `.py` file also accept a mention of the module name without the extension (the stem). Alternatively, have `SKILL.md` name the three modules, but fixing the check covers future multi-module skills too.
- **Who fixes it:** Direct edit to `scripts/check-library-integrity.sh`.

### H3. 33 repo skills reach Claude with no description, because the skill listing is over its size limit

- **What is wrong:** Claude Code shows Claude a list of skill names and descriptions, capped at a character budget. When the list is over budget, it keeps every name but drops the descriptions of the least-used skills. `~/.claude/settings.json:12` sets `SLASH_COMMAND_TOOL_CHAR_BUDGET` to `"50000"`. The repo's 114 model-invocable skills alone need 53,913 characters of name plus description (recounted by the main session). That is more than the whole budget before any plugin, bundled, or synced skill is added. The 35 synced claude.ai skills add about 17,000 more.
- **Evidence:** This session's own skill listing, and the listings seen by two audit agents, show the same 33 repo skills with a name only. Examples: `outside-view`, `steelman`, `source-fidelity`, `runbook-authoring`, `simplify-code`, `reality-check`, `decide:outcome-shaping`, `decide:scope-cut`, `plan-cycle:spec-drift-reconcile`, `plan-cycle:to-prd`, `relay:courier`, `git-cycle:resolve-conflicts`. None of the 33 has `disable-model-invocation: true` and none has an empty description, so the budget is the only cause. The docs confirm the mechanism (skills, "Skill descriptions are cut short"; settings, `skillListingBudgetFraction`).
- **Why it matters:** Claude can still run these skills when named, but is unlikely to choose them on its own for a matching request. That undercuts their value as global skills. Which skills lose their descriptions also shifts over time as usage changes.
- **Recommended action:** JP chooses one or a combination. (a) Raise the budget: set `SLASH_COMMAND_TOOL_CHAR_BUDGET` higher than 50000, or remove it and set `skillListingBudgetFraction` instead. (b) Turn off unused synced claude.ai skills (see M1), which frees about 17,000 characters. (c) Set low-priority skills to `"name-only"` in `skillOverrides`. (d) Trim the 11 descriptions over 90 words (I3), which also frees space. Option (b) alone is not enough, because the repo's own descriptions already exceed 50,000 characters, so (a) is needed in any case. After a change, `/doctor` and the `/context` Skills row show the listing's real size.
- **Who fixes it:** JP decides. Settings changes go through `update-config`. Description trims go through each skill's satellite.
- **Not checked:** Codex has its own listing budget. It was not inspected, because that needs a Codex runtime inspection this read-only audit did not run.

### H4. `athenahealth-brand-system` cites nine asset files that do not exist

- **What is wrong:** The skill tells agents to use bundled fonts, a logo, and two templates that are not in the bundle.
- **Evidence:** `SKILL.md:19` says to use the font files in `assets/fonts/`. `references/assets-and-sources.md` names six font files (`PTSerif-Bold.ttf`, `PTSerif-BoldItalic.ttf`, `PTSerif-Italic.ttf`, `PTSerif-Regular.ttf`, `SourceSans3-Italic-VF`, `SourceSans3-VF`) and `assets/logos/athenahealth-logo.png`. `assets/fonts/` and `assets/logos/` are empty, untracked directories, and git history shows they never held files. `SKILL.md:28` names `assets/templates/powerpoint/athenahealth_2025_brand_template.pptx` and `SKILL.md:43` names `assets/templates/excel/athenahealth_excel_template.xlsx`. The tracked files are `pptx-template.pptx` and `excel-template.xlsx`. A sweep of every support path cited in every live skill bundle found no other missing path.
- **Why the checks missed it:** `check-library-integrity.sh` resolves only `references/`, `scripts/`, and `examples/` paths cited in a `SKILL.md`. It does not check `assets/` paths or paths cited inside `references/*.md`.
- **Why it matters:** The skill's own rule is "use approved assets only". An agent that cannot find the named file must guess, which invites off-brand output.
- **Recommended action:** Rename the two template references (or the files) so the names match. Either add the fonts, their licence text, and the logo, or remove the claims. Consider extending the integrity check to cover `assets/` paths and paths cited inside `references/*.md`.
- **Who fixes it:** The `athenahealth-brand-system` satellite, through `worktree-task-cycle`. The optional check extension is a direct script edit.

## Medium

M1, M2, and M3 share one cause: Claude Code now downloads JP's claude.ai skills into every terminal session on this machine. **One decision covers all three:** keep the sync and turn off the unwanted skills on claude.ai, or stop the sync on this machine with `syncClaudeAiSkills: false`.

### M1. 11 out-of-date claude.ai copies of live skills, plus one deleted skill, load in Claude Code

- **What is wrong:** The synced bucket `93260d95-…` holds 12 skills that JP uploaded by hand to claude.ai (`source=custom` in `manifest.json`). They appear in Claude Code as `anthropic-skills:<name>`: `agent-facing-design`, `design-exploration`, `diagnose`, `ideate`, `making-recommendations`, `methodology-check`, `outcome-shaping`, `scrutinize`, `scrutinize-skill`, `the-gang-explains`, `writing-principles`, and `jp-writing-style`.
- **Evidence:** All 11 copies that have a repo source differ from it. For example, synced `diagnose` is 101 lines against the source's 161, and its description is a claude.ai re-targeting ("household, hardware, appliances…"). None of the 12 matches any version in git history, and none carries an export provenance line. `jp-writing-style` was deleted from the repo on 2026-06-15 (`7d76940`). Only `exports/steelman` has an export record.
- **Why it matters:** Two versions of the same skill with different behavior sit in one listing. A bare `/scrutinize` still runs the repo skill, because a synced skill loses a name clash. But the model can choose an `anthropic-skills:` copy by name.
- **Mitigating evidence:** The skill-usage ledger (18,360 rows) records zero uses of any of these custom copies, and the copies currently appear without descriptions (see H3). No wrong choice has been observed, which is why this is medium, not high.
- **Recommended action:** On claude.ai, turn off the custom uploads that are not needed there. If some are needed on claude.ai, re-export them from the current source through `skill-export` so each has provenance. Or set `syncClaudeAiSkills: false` in user settings.
- **Who fixes it:** JP, on claude.ai or in settings.

### M2. Three repo documents say custom skills do not sync across surfaces, and they now do

- **What is wrong:** `AGENTS.md:26` says exports are "a third delivery path with no delivery mechanism, since custom Skills do not sync across surfaces". `exports/README.md:7` and `skills/skill-export/SKILL.md:9` say the same.
- **Evidence:** See M1 and H1. The half that says nothing delivers repo changes *to* claude.ai is still true. The half that implies a claude.ai upload stays on claude.ai is now false.
- **Why it matters:** An agent reading `AGENTS.md` will assume an upload cannot reach Claude Code sessions, and will not check for the duplicates in M1.
- **Recommended action:** After the M1 decision, rewrite the sentence in all three places. Suggested wording: "nothing delivers repo changes to claude.ai; skills enabled on claude.ai are downloaded into Claude Code sessions as `anthropic-skills:<name>` unless `syncClaudeAiSkills` is false."
- **Who fixes it:** Direct edit for `AGENTS.md` and `exports/README.md`. The `skill-export` satellite for its `SKILL.md`.

### M3. Synced `anthropic-skills:skill-creator` contradicts "no Claude-side constructor skill, by design"

- **What is wrong:** `AGENTS.md:75` routes new-skill work on Claude to hand-authoring against `agent-facing-design` and `skill-ux-design`, and says "There is no Claude-side constructor skill, by design." Both synced buckets contain Anthropic's `skill-creator` (`anthropic-example`, updated 2026-09-14). It appears in Claude Code's listing as `anthropic-skills:skill-creator`, with a description that covers creating, editing, and benchmarking skills.
- **Why it matters:** A Claude session asked to create or benchmark a skill in this repo can now pick a skill that builds bundles by Anthropic's conventions, not this repo's. Its benchmarking also overlaps `skill-benchmark`.
- **Recommended action:** As part of the M1 decision, turn off `skill-creator` on claude.ai, or amend `AGENTS.md:75` to name `anthropic-skills:skill-creator` as not for this repo's skills.
- **Who fixes it:** JP decides. The `AGENTS.md` wording is a direct edit.

### M4. A ledger entry exists only on an unmerged branch whose worktree folder is gone

- **What is wrong:** Branch `chore/codex-handoff-auto-commit-exception` holds one commit, `9dc5b1b` (2026-09-06, "docs: record Codex handoff auto-commit exception"). That commit adds two lines to `docs/agents/contract-decisions.md`. Its worktree, `/private/tmp/codex-handoff-rule-20260906`, no longer exists, so `git worktree list` marks it prunable.
- **Evidence:** `git branch --no-merged main` lists only this branch. `git cherry main chore/codex-handoff-auto-commit-exception` shows `+ 9dc5b1b…`, meaning the change is not on `main` in any form. The added entry records a 2026-09-06 FOLD of a handoff auto-commit exception into `~/.codex/AGENTS.md`, with an observed failure and a pointer to cross-model commit `ef53fac`. The exception is live in `~/.codex/AGENTS.md` (line 15). The 2026-09-08 ledger entry on `main` only says the handoff exceptions are "unchanged".
- **Why it matters:** The charter requires one ledger entry per gated decision. This decision's only record is on a branch that a routine cleanup with `git branch -D` would delete.
- **Recommended action:** Decide whether the entry belongs in the ledger. If yes, cherry-pick `9dc5b1b` onto a working branch and fast-forward `main`. Then run `git worktree prune` and delete the branch. Do this before the branch cleanup in L5.
- **Who fixes it:** The repo's branch-and-fast-forward flow (`docs/agents/` is not a skill surface).

### M5. `teach` and `to-questionnaire` are explicit-only on Claude but not on Codex

- **What is wrong:** Both `SKILL.md` files set `disable-model-invocation: true`, so Claude runs them only when asked by name. Their `agents/openai.yaml` files do not set `policy.allow_implicit_invocation: false`, so Codex may choose them on its own.
- **Evidence:** The other six skills with `disable-model-invocation: true` all set `allow_implicit_invocation: false`. The gap was recorded on 2026-09-03 and was still open when commit `991bae2` added these files.
- **Why it matters:** The same skill behaves differently on the two runtimes. On Codex, it can fire on a request that was never meant for it.
- **Recommended action:** Add `policy: { allow_implicit_invocation: false }` to both `openai.yaml` files, matching the other six.
- **Who fixes it:** Each skill's satellite.

### M6. The decision ledger holds 32 decision entries under the "Mining Queue" heading

- **What is wrong:** `docs/agents/contract-decisions.md` has three sections: `## Decisions` (line 5), `## Parks` (line 80), and `## Mining Queue` (line 103). The Decisions section holds 48 dated entries from 2026-06-12 to 2026-09-22. The Mining Queue section holds 32 more dated decision entries, from 2026-07-26 to 2026-09-08. The two newest entries (2026-09-22) sit at the end of the Decisions section, after entries dated earlier.
- **Why it matters:** A reader or an appending agent that trusts the headings misses the July-to-September decisions. The charter treats this file as the durable record.
- **Recommended action:** Move the 32 entries into the Decisions section, in date order, without rewording them, and leave the Mining Queue section holding only queue items. `AGENTS.md` calls the ledger append-only. Moving entries without changing their text keeps each settled entry as written. If JP reads append-only as ruling out moves, add a dated note under the Mining Queue heading that says the entries below it are decisions instead.
- **Who fixes it:** Direct doc edit.

### M7. Ledger evidence pointers that no longer resolve

- **What is wrong:** Line 25 cites commits `241dc91` and `d981fde` on `feature/skill-squad-spec`. `git cat-file` reports neither is a valid object, and the branch no longer exists. Line 70 cites session transcripts `7f28dac0`, `38aa5101`, and `b0acf39b`, and none exists under `~/.claude`, `~/.codex`, or `~/.agents/.agents`. Lines 64 and 66 rest on "the 2026-07-17 Claude session transcript". No Claude transcript older than 2026-08-01 remains.
- **Evidence:** The finder checked 100 unique commit hashes cited in the ledger. 65 resolve in this repo, 21 resolve in the external repos they name, 6 belong to upstream clones that were trashed by design, and 2 are the dead ones above. The finder's tally leaves 6 hashes unaccounted for; they were not re-checked. Two other named transcripts (`b6a6327c`, `93b9e21c`) do exist.
- **Why it matters:** `docs/agents/charter.md:68` requires "a commit, a tracked file, or a named, persistent artifact reachable outside the session". These pointers can no longer be followed.
- **Recommended action:** For each dead pointer, add a dated annotation that names a surviving pointer, such as the commit that landed the change, a tracked file, or a handoff that quotes the evidence. If nothing survives, say so. Annotate; do not rewrite the settled entries.
- **Who fixes it:** Direct doc edit.

## Low

### L1. `work-skills/` is not described in `AGENTS.md`, and 6 of its 18 sources have changed

`work-skills/` holds 18 tracked `SKILL.md` variants plus a README, all added in one commit (`be00495`, 2026-07-28). Its README says it is a "public-safe source" set for manual transfer and "intentionally not a live skill-discovery location". `AGENTS.md` "Skill Layout And Delivery" lists `skills/`, `skills-claude/`, `skills-archive/`, and `exports/`, but not `work-skills/`. Since the copies were made, the source `SKILL.md` has changed for `design-exploration`, `email-writing`, `outcome-shaping`, `premortem`, `runbook-authoring`, and `scrutinize` (compared by file content, not commit count). **Action:** add one `AGENTS.md` line saying what `work-skills/` is, that it is derived and not delivered, and when to refresh it. Then decide whether the six changed variants need a refresh.

### L2. Four live skills have no satellite worktree

`uv run --script scripts/satellite-fleet.py check` reports `MISSING` for `plain-language` (added 2026-09-08), `claim-check`, `decision-walkthrough`, and `source-fidelity` (all added 2026-09-22 in `d4d990c`). The route guard says a new skill gains its satellite "after landing (attended create-missing)". `AGENTS.md` never names `satellite-fleet.py` or `create-missing`; they appear only in dated plans, specs, and tests. Editing is not blocked, because the route guard allows "any satellite activated for a task". **Action:** run `satellite-fleet.py create-missing` (attended). Add that step next to the `claude-skills-sync.sh --link` step in `AGENTS.md`.

### L3. The charter's Decision Record section leaves out gated skills

`docs/agents/charter.md:68` says a ledger entry is required for "an admission, fold, rejection, park, or retirement of an ambient contract or third-party material". It does not name skills that are gated because they run unattended or use irreversible tools, although `charter.md:22` makes those gated. The ledger itself recorded this gap on 2026-07-26 (`contract-decisions.md:114`, "closing that gap is a direct edit to the charter left undone here"). **Action:** add gated skills to the list at `charter.md:68` and to the ledger header at `contract-decisions.md:3`, following the charter's own procedure for editing it.

### L4. The only open GitHub issue is already fixed

Issue #20 (labels `bug`, `ready-for-human`, 2026-07-12) says `~/.codex/AGENTS.md` lacks the capability carve-out clause. `~/.codex/AGENTS.md:19` now has it, and ledger lines 169 and 182 record the 2026-09-08 fold. **Action:** close #20 as completed, with a comment that points to those ledger lines.

### L5. 23 merged local branches, one merged remote branch, and a leftover config section

`git for-each-ref refs/heads --merged main` lists 23 branches besides `main`, dated from 2026-07-25 to 2026-09-21. The remote branch `origin/chore/simplify-code-methodology-critique` is merged into `main` and still exists on GitHub. `.git/config` keeps a `[branch "codex/admit-athena-kb-operating-contract"]` section for a merged branch. Exception: `chore/execute-plan-contained-review` is checked out in the parked `execute-plan` satellite and cannot be deleted now. **Action:** after M4 is settled, clean up with `git-hygiene`. Deleting the remote branch is a push, so it needs JP's go-ahead.

### L6. The ignored `.agents/scratch` folder is cited by 12 tracked files

`.agents/scratch` holds 665 files (18 MB, 2026-05-28 to 2026-07-12) and is git-ignored. Twelve tracked files cite it, including `docs/agents/contract-evaluation-methodology.md:68`, a playbook listed in `AGENTS.md`, which says the reusable harness templates live in the ignored `.agents/scratch/test{4,5,5v2-pilot}-run/` folders. The playbook states this on purpose, so it is not a hidden defect. But by age and location the folder looks like disposable scratch. `.agents/foreign-skills` (18 files) has no tracked reference. **Action:** do not trash `.agents/scratch` as stale. If the templates should outlive this machine, move them into a tracked `docs/` location and update the pointers.

### L7. `.skill-lock.json` is undocumented and partly stale

This lock file comes from a third-party skills installer and was last pruned on 2026-06-09 (`3ef749b`). Its `write-a-skill` entry names a skill archived on 2026-06-12. Entries for `to-issues`, `to-prd`, and `triage` name skills that have since moved into `plugins/plan-cycle`. Nothing reads the file except two review docs that use it as a record of where skills came from. The installer command is not installed on this machine. **Action:** remove the `write-a-skill` entry as `3ef749b` did for other removed skills, or add a short note on the file's role.

### L8. `skills-archive/README.md` describes 7 of 11 archived skills

The README says nothing about `deliberate-v1` (archived in `cebf8e9`), `design-review-team` and `tech-debt-audit` (both `9d2ef7a`), or `write-a-skill` (`a880b78`). Its lines 3-9 are also hard-wrapped, against the repo's one-line-per-paragraph convention. **Action:** add an entry for each of the four, with the reason and commit, and unwrap lines 3-9.

### L9. `the-gang-explains` uses a Claude-only placeholder and hard-wrapped prose

`the-gang-explains` is in `skills/`, so both runtimes load it. It points to its companion files only through `${CLAUDE_SKILL_DIR}` (`SKILL.md:25,78,338`), which only Claude Code fills in. `skills/document-to-markdown/SKILL.md:63` shows the house pattern for naming the skill directory on both runtimes. Its three Markdown files also wrap prose at about 80 columns (124, 69, and 13 wrapped lines). It is the only live bundle that does. **Action:** at the next edit, name the files relative to the skill directory, following `document-to-markdown:63`, and unwrap the prose.

### L10. The `AGENTS.md` list of Codex-bundled skill names is out of date

`AGENTS.md:29` lists `doc`, which is not installed (`~/.codex/skills/doc` and `~/.codex/skills/.system/doc` do not exist). It omits `review-agent`, which is installed in `~/.codex/skills/.system/`. No live skill collides with either name today. **Action:** add `review-agent`, drop `doc`, and point to `ls ~/.codex/skills ~/.codex/skills/.system` as the live source.

### L11. `skill-lifecycle-notes.md` describes the old `deliberate`

`docs/agents/skill-lifecycle-notes.md:73` says `deliberate` carries `disable-model-invocation: true` and is hidden from routing. That field was removed on 2026-09-03 (`2a75e2c`, "model-invocable again"). Line 15 says "four" `review-family` skills send findings to `/triage`, and there are three. A 2026-09-08 review (`docs/reviews/2026-09-08-work-router-gap-review.md:119`) already reported the stale sentence. **Action:** rewrite point (2) of the `deliberate` entry for the current skill, and change "four" to "three" on line 15.

### L12. ADR 0001 has no Status line, and its subject is archived

`docs/adr/0001-authenticate-deliberate-modules-as-direct-method-surfaces.md` has no Status line, which under the house convention reads as in force. It governs the `deliberate` v1 validator, which was archived in `cebf8e9` (2026-09-03). The ADR only applies "when the validator is decomposed", so an agent is unlikely to act on it wrongly. **Action:** add `Status: deprecated` with the archiving commit.

### L13. `AGENTS.md` omits two `docs/agents` files, the test suite, and `.out-of-scope/`

The "Repo Docs" list leaves out `docs/agents/skill-lifecycle-notes.md` (cited from `skills/agent-facing-design/SKILL.md:80`) and `docs/agents/codex-plugin-list-cache-sync-2026-07-17.md` (cited from `scripts/codex-plugins-sync.sh:12`). `AGENTS.md` does not mention `tests/` or how to run it, and the repo has no `pyproject.toml` or `pytest.ini`. `.out-of-scope/` comes from the `plan-cycle` triage skill's convention and is not mentioned either. **Action:** add the two files to "Repo Docs". Add a Working Defaults line with the test command: `uv run --no-project --with pytest python -m pytest -p no:cacheprovider -q tests`. It ran 240 tests, all passing, in this audit. Add a line to `docs/agents/issue-tracker.md` saying the triage skill records rejected requests in `.out-of-scope/`.

### L14. 12 plans and specs still show an open status

Each of these has an open status line and a last commit more than 30 days ago. For most, the repo shows the work was finished, parked, or dropped.

| Document | Status line says | Repo state |
| --- | --- | --- |
| `docs/plans/2026-06-17-git-cycle-plugin.md` | ready to execute | `plugins/git-cycle` exists at 1.7.0 |
| `docs/plans/2026-06-23-skill-squad.md` | ready to execute | built, then archived |
| `docs/specs/2026-06-23-skill-squad.md` | ready for implementation-planning | built, then archived |
| `docs/specs/2026-06-27-advisory-lane-carve.md` | settled — unbuilt | `premortem` and `red-team` exist |
| `docs/specs/2026-06-27-operate-arc-carve.md` | builds in progress | `deploy-plan` and `outcome-check` exist; `incident-response` archived |
| `docs/plans/artifacts/judgment-trust-test2-human-coldjudge-design-2026-06-16.md` | PREPARED (not yet run) | results file exists |
| `docs/plans/artifacts/judgment-trust-test5-redteam-prereg-2026-06-16.md` | DRAFT … ready to seal | test 5 results say COMPLETE |
| `docs/plans/2026-07-08-mattpocock-skills-extraction-roadmap.md` | nothing landed | inventory says landed and ledgered |
| `docs/plans/2026-07-12-skill-use-contract-implementation-plan.md` | authored, executor `execute-plan` | ledger line 50: parked |
| `docs/specs/2026-07-13-deliberate.md` | v30 | subject archived 2026-09-03 |
| `docs/plans/2026-07-16-deliberate-v6-shared-module-extraction.md` | (no status) | subject archived 2026-09-03 |

The verifier spot-checked six of the twelve. **Action:** optional. These are dated history, so a one-line "Superseded / done / parked — see X" note at the top is enough.

### L15. Empty leftover directories and ignored cache folders inside skill folders

- Empty directories that nothing refers to: the root `references/` (emptied in `1be1bbd`, 2026-06-09, although `AGENTS.md:3` says the repo holds "references"), `skills/tech-debt-scan/examples/`, and `.agents/skills/` (holds only `.DS_Store`). `.agents/treatments/` is empty on purpose; `methodology-critique` expects it.
- Ignored cache folders inside skill folders that both runtimes read: `skills-claude/cross-model-review/{scripts,tests}/__pycache__`, `skills/document-to-markdown/.ruff_cache`, and `skills/document-to-markdown/scripts/__pycache__`. Also `.DS_Store` files in 11 skill folders.
- One cause: the user-level hook `~/.claude/hooks/ruff-format.py:31-37` runs `ruff format <path>` without `--no-cache`, from the session's working directory. During this audit, writing a scratch file outside the repo made that hook add an entry to `/Users/jp/.agents/.ruff_cache`.
- **Action:** trash the empty directories and cache folders during a `git-hygiene` pass. Whether to add `--no-cache` to the hook is JP's choice, because the hook lives outside this repo.

### L16. 12 of 53 allow rules in the repo-local Claude settings name missing paths

`.claude/settings.local.json` (git-ignored) holds 53 allow rules. Twelve name paths that no longer exist, all from one-time migrations. Examples: `rsync … /Users/jp/.codex/plugins/handoff/ plugins/handoff/`, `trash /Users/jp/.claude/skills/claudeonly`, and several `shasum` rules for `/Users/jp/.claude/skills/deliberate/…`. **Action:** remove the stale rules. Keep the SessionStart check entry, which matches the recovery copy in the `claude-skills-sync.sh` header.

### L17. `.git` still holds state files from the removed security-guidance plugin

`.git/sg-hook-once-toolu_013r8Ke9K1JEeV5FEuCeRu34`, `.git/sg-hook-once-toolu_01Ev9PrRhEeGTFyarTUodrN4`, and `.git/sg-reviewed-shas` date from 2026-06-13. That is the day the security-guidance plugin was removed (ledger line 18). **Action:** trash the three files after approval.

### L18. Two `openai.yaml` short descriptions exceed 64 characters

`plugins/decide/skills/deliberate/agents/openai.yaml` (90 characters) and `plugins/decide/skills/outcome-shaping/agents/openai.yaml` (83 characters) exceed the 25-64 character range in Codex's `skill-creator` reference. All 94 `openai.yaml` files parse. **Action:** shorten both at the next `decide` release.

### L19. Whitespace errors in four tracked files; `.gitignore` has no final newline

`git diff --check` against the empty tree reports trailing whitespace in `docs/plans/2026-07-11-skill-use-contract-census.txt` (12 lines) and `docs/reviews/2026-09-21-never-used-skill-census.txt` (3 lines), both captured command output. It also reports a Markdown line break (two trailing spaces) at `docs/reviews/2026-07-02-agent-facing-design-philosophy-audit.md:24`, and a blank line at the end of `docs/plans/artifacts/judgment-trust-test5-v2-pilot-results-2026-06-16.md`. `.gitignore` has no final newline and lists both `.DS_Store` and `**/.DS_Store`; the second adds nothing. No file uses CRLF line endings. **Action:** optional. Add the `.gitignore` newline and remove the extra blank line; leave the captured output and the intentional line break alone.

### L20. A skill script has a shebang but no executable bit

`skills/simplify-code/scripts/create_simplify_backup.py` starts with `#!/usr/bin/env -S uv run --script` but is mode 100644. Its sibling `scoped_safety_scan.py` is 100755. The playbook calls it with `python …`, so nothing breaks today. Three other shebang files without the bit are a template that gets copied before use, an archived test, and a one-off docs script, and they can stay. **Action:** set the executable bit on `create_simplify_backup.py`.

## Info

- **I1. The satellite fleet check exits 2 on every run.** The only cause is the known, parked `execute-plan` draft (lease `LEASE-ORPHANED`). While it stays, exit code 2 cannot signal new drift. The four missing satellites in L2 would produce exit 3 on their own.
- **I2. `decision-record` still routes incident retrospectives to the archived `postmortem`.** This is known and deliberately held for the next `decide` version bump. `decide` has not been bumped since (last bump `946da91`, 2.4.0), so the hold has not been missed.
- **I3. 11 live descriptions exceed ~90 words.** `AGENTS.md` allows this when it prevents a specific misroute. It matters only as an input to H3.
- **I4. The only export, `exports/steelman`, shows STALE.** The one newer source commit added `agents/openai.yaml`, which is not part of the exported text. No copy of `steelman` is in either synced bucket.
- **I5. ruff 0.16.0 reports 93 findings in `scripts/` and `tests/`.** 76 are quoted-annotation style rules (UP037), and most of the rest are other style rules. They come from ruff's own defaults; the repo has no ruff config and no lint gate. The ledger's "ruff clean" note was true under ruff 0.15.
- **I6. `scripts/night-porter-task-prompt.md` is a prepared Desktop scheduled-task prompt that was never registered.** Both LaunchAgents (`com.jp.night-porter`, `com.jp.skill-usage-miner`) are installed, identical to their repo copies, loaded, and last exited 0.
- **I7. The repo has 1,500 loose objects (16 MB) next to a 3.3 MB pack, and three Codex checkpoint refs under `refs/codex/`.** `git fsck --connectivity-only` is clean. No action needed.

## Checked and Clean

- Delegated drift checks: `check-protected-set.sh` (7 surfaces), `check-handoff-paths.sh`, `check-review-family.sh` (5 skills), and `codex-plugins-sync.sh --check` all pass.
- Structural checks: skill name matches directory name (122 skills), cited `references/`/`scripts/`/`examples/` paths resolve, frontmatter is valid (122 skills), plugin manifest and CHANGELOG versions agree (6 plugins), and the `ADR-FORMAT.md` symlink resolves.
- A wider sweep of every support path cited in any Markdown or YAML file of a live skill bundle found no missing path except H4. All 31 top-level support files in skill bundles are referenced.
- Delivery: 88 `~/.claude/skills` symlinks, equal to 74 + 8 + 6 source directories. None points into `skills-archive/`, `exports/`, or `work-skills/`. No duplicate skill names across `skills/`, `skills-claude/`, and `plugins/*/skills/`. No clash with a bundled name except the intentional `skills-claude/openai-docs`.
- Plugins: `plugins/marketplace.json` has 6 entries for 6 directories, all with relative paths that resolve. The release mirror (`/Users/jp/Projects/active/codex-tool-dev/plugins/turbo-mode`) and the Codex plugin cache both match all six plugin versions, with zero file differences, and the cache holds one version per plugin.
- Git: no stashes. No tracked file that `.gitignore` would ignore. No CRLF. The only tracked symlink is the expected one. `git fsck` is clean. `main` is level with `origin/main`. `.claude/worktrees` is empty. 117 satellites are parked and clean. Satellite directories match their registrations exactly.
- Scripts and tests: `bash -n` passes on all shell scripts. All 37 tracked Python files parse. shellcheck reports 0 warnings and 0 errors. The repo test suite passes (240 tests), and the `cross-model-review` suite passes (61 tests). Every script path cited from `AGENTS.md`, `docs/agents`, skills, plists, and tests exists, and every hook command that points into this repo or `~/.claude/hooks` exists.
- Docs: links and backticked paths in 22 current-state docs (`AGENTS.md`, `docs/agents/*`, `docs/adr/*`, and the README files) resolve. `AGENTS.md` and `docs/agents/*` have no hard-wrapped prose. `CLAUDE.md` is a correct `@AGENTS.md` shim. There are no nested instruction files and no active `.git/hooks`.
- `openai.yaml`: all 94 parse, and no `default_prompt` names a skill that does not exist.

## Coverage Limits

- **Codex runtime state was not inspected.** This covers Codex's own skill-listing budget, whether bare `$<skill>` tokens in plugin `default_prompt` fields resolve on Codex (which lists plugin skills as `<plugin>:<skill>`), and whether Codex hook trust hashes are still valid. Each needs an app-server inspection or a `codex exec` probe, which this read-only audit did not run.
- Whether the 33 skills in H3 are exactly the least-used ones was not mapped against the usage ledger. The docs state that the least-used lose their descriptions first.
- Whether Claude actually picks the synced copies in M1 over the repo skills was not tested live. Only the usage ledger was checked (zero uses).
- The 276 handoff files in `.agents/handoffs` were not reviewed for stale or misfiled entries.
- Six upstream-clone commit hashes in the ledger cannot be checked, because those clones were trashed by design.
- The archived `deliberate-v1` tests were not run.
- The hard-wrap check is a heuristic (3+ consecutive prose lines of 60-100 characters). It can miss shorter wraps and wrapped list continuations.

## Method

1. The main session ran `scripts/check-library-integrity.sh --check` from the primary checkout on `main` at `deefb04`, and inspected `~/.claude/skills/synced` and `git worktree list`.
2. A four-agent workflow ran three finders in parallel: git and filesystem; skill library and delivery; and docs, scripts, tests, and instruction files. One verifier-and-completeness agent then re-ran the evidence for every finding, tried to refute each one, merged duplicates, and ran the checks nobody had covered. It added three findings: M3, L3, and L4.
3. The main session re-checked the four high findings, the ledger structure (M6), the stranded branch (M4), the `openai.yaml` gap (M5), and issue #20. It also recounted the description characters for H3 and confirmed the H1 and H3 mechanisms in the Claude Code docs.
4. Read-only proof: after the workflow, `git status` in the primary checkout was clean, and every satellite was unchanged except the known, parked `execute-plan` draft. The one side effect was the ruff-format hook's `.ruff_cache` entry described in L15. That folder is git-ignored and outside version control.

## Follow-up

Applied on 2026-09-23 after the audit, on JP's four answers: turn off claude.ai skill sync with `syncClaudeAiSkills: false`, raise the skill listing budget, land the stranded ledger entry, and start the fixes that needed no decision. A read-only review of the fixes then found three errors in the new text; the commit that adds this section corrects them.

**Both automatic checks now pass, and every fix JP approved is on `main`; the findings still open are listed at the end of this section.**

Fixed or decided:

- **H1:** fixed in `0672d5a`. `scripts/claude-skills-sync.sh` exempts `synced`.
- **H2:** fixed in `0672d5a`. The orphan check counts an `import` or `from` line in another `.py` file of the bundle as a mention. A planted orphan in a throwaway copy of the repo still fails the check.
- **H3:** JP chose to raise the budget. `SLASH_COMMAND_TOOL_CHAR_BUDGET` in `~/.claude/settings.json` went from `50000` to `90000`. The file is outside the repo, and the change takes effect at the next Claude Code start. The review measured about 57,700 characters of listing text for next start, leaving roughly 24,000 characters of room after an estimated 7,000 to 8,000 for Claude Code's bundled skills.
- **M1 and M3:** JP chose `"syncClaudeAiSkills": false` in `~/.claude/settings.json`. At the next start, Claude Code stops loading the 27 synced skills and moves them to `~/.claude/skills/.trash/`. They stay available on claude.ai. Because 14 of the 27 are Anthropic-authored, the decision is recorded in the ledger as a third-party removal, with a reopen trigger for the `docx`, `pdf`, `pptx`, and `xlsx` skills.
- **M2:** fixed in `0ff9f9b` (`AGENTS.md`), `90e9d11` (`exports/README.md`), and `ad0a675` (`skills/skill-export/SKILL.md`).
- **M4:** fixed in `9def9ea`, a cherry-pick of `9dc5b1b` onto `main`. The branch itself still exists; see L5.
- **M5:** fixed in `ad0a675`.
- **M6:** fixed in `0c67ddc`. 33 entries moved, text unchanged: the 32 the audit counted plus the 2026-09-06 entry from M4, which first landed in the same place.
- **M7:** annotated in `9e40aa8`. Correction to this report: M7's statement that no Claude transcript older than 2026-08-01 remains is false. The audit judged transcript age by file modification time. The 2026-07-17 transcript survives, and a correction ledger entry quotes JP's grant and ruling from it.
- **L1, L10:** fixed in `0ff9f9b`.
- **L3:** fixed in `9e40aa8` (charter and ledger header) and `0ff9f9b` (`AGENTS.md` Repo Docs line).
- **L8, L12:** fixed in `90e9d11`.
- **L11:** line 15 fixed in `90e9d11`. Correction to this report: point (2) was not a defect, because the paragraph that follows it in `skill-lifecycle-notes.md` already marks the v1 `deliberate` text as history.
- **L13:** fixed in `0ff9f9b` (two Repo Docs files and the test command) and `90e9d11` (`.out-of-scope/` in `docs/agents/issue-tracker.md`).
- **L2, in part:** `0ff9f9b` added the satellite step to `AGENTS.md`, but it named `satellite-fleet.py create-missing`, which refuses while `check` reports drift in any satellite, as it does for the parked `execute-plan` draft. The commit that adds this section changes the step to `satellite-fleet.py create <name>`. The four satellites are not created yet.

Not done, each needing JP's decision or go-ahead:

- **H4:** the `athenahealth-brand-system` fonts and logo, plus the two template renames.
- **L2:** creating the four missing satellites (`claim-check`, `decision-walkthrough`, `plain-language`, `source-fidelity`) with `satellite-fleet.py create <name>`.
- **L4:** closing issue #20.
- **L5:** branch cleanup. `chore/codex-handoff-auto-commit-exception` now needs `git branch -D`, because its commit reached `main` as a cherry-pick with a different id. Deleting the remote branch is a push.
- **L6, L7, L9, L14, L15, L16, L17, L19, L20:** untouched. L18 waits for the next `decide` release.
- Not covered by the audit: claude.ai plugin sync is a separate setting (`syncClaudeAiPlugins`, unset), and it still delivers `cowork-plugin-management` into `~/.claude/plugins/synced/`.
