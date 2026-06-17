# Implementation Plan: the `git-cycle` plugin (lean Approach A)

**Status:** ready to execute · **Date:** 2026-06-17 · **Source:** locked design from this
session's outcome-interview → design-exploration → adversarial-panel scrutiny (run
`wf_9986b895-452`, 11 confirmed findings folded in). Reference file **dropped**. Patched 2026-06-17
after a `review-reviewer` adjudication (R1 protected-resolution blocker; R2 Codex-test relabel; R3
charter note; R4 Codex bootstrap; R5 six-skill validation; R6 Markdown fences).

## What this builds

The six git skills become one coherent dual-runtime plugin, `git-cycle` (the packaging/coherence
home for the arc "local change → merged-and-shared, safely"). There is **no shared-reference file**:
the adversarial panel showed it was the wrong vehicle for safety machinery, which silently degrades
if a conditionally-loaded pointer is missed. All safety machinery stays **inline and always-loaded**.
Anti-drift comes from (a) a textual consistency check over the inline copies and (b) an always-loaded
`AGENTS.md` floor — both honestly **drift-detection**, not single-sourcing.

Members (6): `git-hygiene`, `closeout-check`, `merge-branch`, `exiting-worktrees`,
`gh-address-comments`, `gh-pr-review-loop`. `acceptance-map` stays **out** of the plugin (it defines
"done" before building — a different job) but its protected-set copy **is** covered by the drift
check. No skills are merged; each keeps its modes and distinct protected-branch response.

## How to use this plan — three independent workstreams

| WS | What | Lands on | Gates | Closes |
|----|------|----------|-------|--------|
| **1** | git-hygiene #9/#10 fixes + protected-set canonicalization + drift check + `AGENTS.md` floor | in place on `skills/` (immediate dual-runtime) | nothing | #9, #10 |
| **2** | `exiting-worktrees` dual-runtime port + Codex *mechanism* proof | in place on `skills-claude/` | a passing **Codex** command/mechanism smoke test | — |
| **3** | `git-cycle` packaging migration (copy-first) | new `plugins/git-cycle/` | WS1 **and** WS2 landed | the coherence goal |

**WS1 and WS2 are independently executable and landable now.** WS3 absorbs the already-fixed skills;
it depends on WS1+WS2 being landed but must not block them. Run each workstream on its own working
branch and fast-forward onto `main` when its verification passes.

## Repo conventions every task obeys

- **Branching:** do file-changing work on a `chore/`/`fix/`/`feature/` branch and fast-forward onto
  `main`. A user-level hook blocks edits made directly on `main`.
- **Deletion:** `trash <path>`, never `rm`.
- **No publish:** do not push, add remotes, open PRs, or publish the mirror unless the user asks.
  Codex cache republish (WS3) is local and expected; the GitHub release mirror is **out of scope**.
- **Validation ladder:** parse edited `SKILL.md` frontmatter and `plugin.json`; confirm every
  referenced path exists; run focused checks on changed scripts; add a live invocation / forward test
  / realistic dry run for behavior changes. `quick_validate.py` is structural-only — accept its
  "unexpected key" complaint on `argument-hint`/`disable-model-invocation`; never delete those fields.
- **The canonical protected-set sentence** (used verbatim throughout this plan):

  > Treat repo-defined protected branches first; if the repo defines none, treat `main`, `master`, `develop`, and `release/*` as protected.

  `closeout-check` and `acceptance-map` already carry it verbatim. `merge-branch` carries a reworded
  variant (fixed in WS1). `git-hygiene` carries no literal list today (added in WS1). `AGENTS.md`
  gains it as the floor (WS1).

---

# Workstream 1 — git-hygiene #9/#10 + protected-set consistency

Lands in place on `skills/`; closes issues #9 and #10. Start it on a branch:

```bash
git switch -c fix/git-hygiene-protected-set main
```

### Files touched
- `skills/git-hygiene/SKILL.md` — converge protected resolution (#9); add `revert` to the
  always-loaded preflight clause (#10).
- `skills/git-hygiene/references/git-hygiene-reference.md` — add `revert` to the marker clause (#10).
- `skills/merge-branch/SKILL.md` — reword its protected-set sentence to the canonical wording.
- `AGENTS.md` — add the protected-set floor to "Git And Cleanup".
- `scripts/check-protected-set.sh` — **new** drift-detection script.
- `.claude/settings.local.json` — wire the check into the SessionStart canary (real caller).

`skills/closeout-check/SKILL.md` and `skills/acceptance-map/SKILL.md` are **read-only here** — verified
already-canonical in Task 1.4, not edited.

---

### Task 1.1 — Converge git-hygiene's protected resolution (#9)

`skills/git-hygiene/SKILL.md` Core Rules currently resolve protection via the default branch + a
`branchProtection` glob, with **no** literal fallback — the divergence #9 reports. Replace the rule so
it carries the canonical fallback **only when the repo defines no `branchProtection` policy**, keeping
the default branch always-protected as a separate condition (this is the panel's finding #4: an
unconditional union would force-branch legitimate work on `develop`/`release/*` in a `trunk`-default
repo).

Replace this exact block (lines 16–20):

```text
- Never commit onto the default or a protected branch. Before any `commit-shaping`
  or `commit-only` commit, create a working branch (`chore/`, `fix/`, or
  `feature/`) when the checked-out branch is the default branch or matches a
  `branchProtection` glob; reuse the branch and default branch already captured in
  preflight.
```

with:

```text
- Never commit onto the default branch or a protected branch. The default branch
  is always protected; resolve the *protected* set repo-defined first, where
  "repo-defined" means the configured `branchProtection` policy — not the mere
  existence of a default branch. Treat repo-defined protected branches first; if
  the repo defines none, treat `main`, `master`, `develop`, and `release/*` as
  protected. Before any `commit-shaping` or `commit-only` commit, create a working
  branch (`chore/`, `fix/`, or `feature/`) when the checked-out branch is the
  default branch or is protected under that resolution; reuse the branch and
  default branch already captured in preflight.
```

This embeds the canonical sentence verbatim, keeps the default branch as a separate always-protected
condition (matching `closeout-check` and `acceptance-map`, which gate on "protected or the repo's
default branch"), defines "repo-defined protection" as the configured `branchProtection` policy — not
the mere existence of a default branch — and applies the fallback set only when no `branchProtection`
policy is defined. **Known limit to record in the commit body (do not paper over):** perfect cross-skill
consistency is not achievable — the four skills read "repo-defined protection" from different sources
(git default detection, `AGENTS.md`/`CLAUDE.md` policy, `.git-hygiene.json` `branchProtection`), which
is the settled "cannot single-home core behavior across independently-loaded skills" rule. #9 fixes the
common **no-config** case (all four now protect the same fallback set) and aligns the wording; exotic
partial-config divergence remains and is expected.

Verify the canonical sentence is present verbatim (modulo line-wrap):

```bash
tr '\n' ' ' < skills/git-hygiene/SKILL.md | tr -s ' \t' | \
  grep -Fq 'Treat repo-defined protected branches first; if the repo defines none, treat `main`, `master`, `develop`, and `release/*` as protected.' \
  && echo "git-hygiene: canonical present"
```
Expected output: `git-hygiene: canonical present`

---

### Task 1.2 — Add `revert` to git-hygiene's always-loaded preflight clause (#10)

`skills/git-hygiene/SKILL.md:40` (the always-loaded Preflight prose) lists in-progress operations but
omits revert — the exact #10 gap. Because it is always-loaded, this is where the fix must land (panel
finding #6).

In `skills/git-hygiene/SKILL.md`, find:

```text
abort on rebase, merge, cherry-pick, or bisect;
```

replace with:

```text
abort on any in-progress git operation (rebase, merge, cherry-pick, revert, or bisect);
```

Verify:

```bash
grep -n 'rebase, merge, cherry-pick, revert, or bisect' skills/git-hygiene/SKILL.md \
  && echo "preflight names revert"
```
Expected: a line 40 match and `preflight names revert`.

---

### Task 1.3 — Add `revert` to the git-hygiene reference marker clause (#10, second site)

`skills/git-hygiene/references/git-hygiene-reference.md:20` repeats the operation list and also omits
revert. Fix it so the conditionally-loaded surface agrees with the always-loaded one.

Find:

```text
Use the git directory from `git rev-parse --git-dir` to inspect rebase, merge, cherry-pick, and bisect markers.
```

replace with:

```text
Use the git directory from `git rev-parse --git-dir` to inspect rebase, merge, cherry-pick, revert, and bisect markers.
```

Verify:

```bash
grep -n 'rebase, merge, cherry-pick, revert, and bisect markers' skills/git-hygiene/references/git-hygiene-reference.md \
  && echo "reference names revert"
```
Expected: a line 20 match and `reference names revert`.

---

### Task 1.4 — Canonicalize merge-branch; confirm closeout-check and acceptance-map already match

In `skills/merge-branch/SKILL.md`, replace this exact block (lines 61–63):

```text
Treat protected branches as repo-defined protected branches first. If the repo
does not define them, treat `main`, `master`, `develop`, and `release/*` as
protected for this workflow.
```

with:

```text
Treat repo-defined protected branches first; if the repo defines none, treat
`main`, `master`, `develop`, and `release/*` as protected.
```

(merge-branch keeps its own response — the Preflight stop conditions on lines 65–71 are unchanged.)

Then confirm — **do not edit** — that the other two already carry the canonical sentence verbatim:

```bash
for f in skills/merge-branch/SKILL.md skills/closeout-check/SKILL.md skills/acceptance-map/SKILL.md; do
  tr '\n' ' ' < "$f" | tr -s ' \t' | \
    grep -Fq 'Treat repo-defined protected branches first; if the repo defines none, treat `main`, `master`, `develop`, and `release/*` as protected.' \
    && echo "OK: $f" || echo "MISSING: $f"
done
```
Expected: `OK:` for all three.

---

### Task 1.5 — Add the protected-set floor to `AGENTS.md`

Promote the protected-set obligation to the always-loaded repo instructions (panel finding #8 — the
always-loaded backstop the library review credited does not currently carry the set). State the floor's
scope honestly.

In `AGENTS.md`, under `## Git And Cleanup`, after the existing first bullet that ends
`enforces this by blocking edits on `main`.`, insert this new bullet:

```text
- Protected-branch floor (this repo): never commit on the default branch or a
  protected branch. Treat repo-defined protected branches first; if the repo
  defines none, treat `main`, `master`, `develop`, and `release/*` as protected.
  This always-loaded floor governs work in this repo only; it does not travel to
  other repositories, where the `git-cycle` skills carry their own inline copy.
```

Verify:

```bash
tr '\n' ' ' < AGENTS.md | tr -s ' \t' | \
  grep -Fq 'Treat repo-defined protected branches first; if the repo defines none, treat `main`, `master`, `develop`, and `release/*` as protected.' \
  && echo "AGENTS.md: floor present"
```
Expected: `AGENTS.md: floor present`

---

### Task 1.6 — Create the drift-detection script

Create `scripts/check-protected-set.sh` with **exactly** this content:

```bash
#!/usr/bin/env bash
# check-protected-set.sh — drift DETECTION (not single-sourcing) for the canonical
# protected-branch fallback sentence. The git-cycle git-lifecycle skills each inline
# this sentence in their always-loaded body for portable, always-loaded safety; this
# check asserts every copy is byte-identical (modulo line-wrap) so the deliberate
# duplication cannot silently drift — the failure that produced issue #9. CANON below
# is the single textual source: to change the wording, edit it here and update every
# target. Exit non-zero on any mismatch.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

CANON='Treat repo-defined protected branches first; if the repo defines none, treat `main`, `master`, `develop`, and `release/*` as protected.'

# Every always-loaded surface that must carry the sentence verbatim.
# WS3 repoints the four skill paths under plugins/git-cycle/skills/ (acceptance-map
# and AGENTS.md stay put) — update this list in that migration step.
TARGETS=(
  "AGENTS.md"
  "skills/git-hygiene/SKILL.md"
  "skills/merge-branch/SKILL.md"
  "skills/closeout-check/SKILL.md"
  "skills/acceptance-map/SKILL.md"
)

fail=0
for t in "${TARGETS[@]}"; do
  path="$ROOT/$t"
  if [ ! -f "$path" ]; then
    echo "MISSING FILE: $t" >&2; fail=1; continue
  fi
  if ! tr '\n' ' ' < "$path" | tr -s ' \t' | grep -Fq "$CANON"; then
    echo "DRIFT: $t lacks the canonical protected-set sentence verbatim" >&2; fail=1
  fi
done

if [ "$fail" -ne 0 ]; then
  {
    echo ""
    echo "Canonical sentence (single textual source, in this script):"
    echo "  $CANON"
    echo "Fix the drifted copy to match exactly, or change CANON here AND every target."
  } >&2
  exit 1
fi
echo "OK: protected-set sentence consistent across ${#TARGETS[@]} surfaces"
```

Make it executable and run the focused checks:

```bash
chmod +x scripts/check-protected-set.sh
bash -n scripts/check-protected-set.sh && echo "syntax OK"
scripts/check-protected-set.sh
```
Expected: `syntax OK`, then `OK: protected-set sentence consistent across 5 surfaces`.
If it reports DRIFT, fix the named file to match the canonical sentence before continuing.

---

### Task 1.7 — Wire the check into the SessionStart canary (a real caller)

The validation ladder (Task 1.8) is the script's primary caller. To also catch drift every session —
and because the panel showed the canary does **not** currently call any in-plugin script — add a third
SessionStart hook entry in `.claude/settings.local.json` (untracked/local; this edit does not ship).

In `.claude/settings.local.json`, the `SessionStart` hooks array already contains two command entries
(`claude-skills-sync.sh --check` and `codex-plugins-sync.sh --check`). Add a third sibling entry with
the same shape:

```json
{
  "type": "command",
  "command": "/Users/jp/.agents/scripts/check-protected-set.sh || true"
}
```

Add the matching permission to the `permissions.allow` array so it runs without a prompt:

```json
"Bash(scripts/check-protected-set.sh)"
```

Verify the file still parses and the canary entry is present:

```bash
python3 -c "import json,sys; json.load(open('.claude/settings.local.json')); print('settings.local.json parses')"
grep -n 'check-protected-set.sh' .claude/settings.local.json
```
Expected: `settings.local.json parses` and two matches (hook command + permission).

> Note: `codex-plugins-sync.sh --check` only diffs trees and runs no plugin script, and `--publish`
> repairs drift without running checks. Do **not** claim either as a caller of this script. Cache-side
> drift is already caught because `--check` is a content diff, not version-gated.

---

### Task 1.8 — WS1 verification, commit, and land

Run the full local validation for the edited surfaces:

```bash
# Frontmatter still parses on the edited skills
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/git-hygiene
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/merge-branch
# Whitespace hygiene on every edited surface
git diff --check
# The drift check passes (5 surfaces)
scripts/check-protected-set.sh
```
Expected: validators pass (the documented `argument-hint`/`disable-model-invocation` "unexpected key"
note, if any, is accepted), `git diff --check` is silent, drift check prints `OK: ... 5 surfaces`.

Behavior forward-test (panel finding #5 — prove the always-loaded floor holds without any reference):
read `skills/git-hygiene/SKILL.md` Core Rules + Preflight **only** and confirm that, with no other
file loaded, an agent on a `develop` branch in a no-config repo would (a) treat `develop` as protected
and branch first, and (b) abort on an in-progress `revert`. Record the two answers in the commit body.

Commit (close both issues) and fast-forward onto `main`:

```bash
git add skills/git-hygiene/SKILL.md skills/git-hygiene/references/git-hygiene-reference.md \
        skills/merge-branch/SKILL.md AGENTS.md scripts/check-protected-set.sh
git commit  # message below; .claude/settings.local.json is untracked/local — do not stage
git switch main && git merge --ff-only fix/git-hygiene-protected-set
```

Commit message:

```text
fix(git-hygiene): converge protected resolution + add revert marker (closes #9, #10)

Resolve "protected" repo-defined-first, else the canonical fallback set, matching
merge-branch/closeout-check/acceptance-map in the no-config case (#9); add revert to
the always-loaded preflight clause and the reference marker list (#10). Canonicalize
merge-branch's wording, add an always-loaded protected-set floor to AGENTS.md, and add
scripts/check-protected-set.sh to detect drift across all five inline copies.

Known limit: perfect cross-skill consistency is not achievable (the four skills read
"repo-defined protection" from different sources — the settled cannot-single-home rule);
#9 fixes the common no-config case and aligns wording. Exotic partial-config divergence
is expected.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

Then close the tracker issues with a one-line evidence comment each (the merge commit hash):

```bash
gh issue close 9 --repo jpsweeney97/agents --comment "Fixed in <hash>: git-hygiene resolves protected repo-defined-first else the canonical fallback; wording canonicalized across 4 bodies; drift guarded by scripts/check-protected-set.sh; AGENTS.md floor added. Cross-skill perfect consistency is a documented known limit."
gh issue close 10 --repo jpsweeney97/agents --comment "Fixed in <hash>: revert added to git-hygiene SKILL.md:40 (always-loaded) and references marker list."
```

**WS1 landed.** It does not depend on WS2 or WS3.

---

# Workstream 2 — `exiting-worktrees` dual-runtime port

Lands in place; **gated on a passing Codex command/mechanism smoke test**. The skill stays in `skills-claude/`
(Claude-only) until that test passes — only then does WS3 move it into the plugin as dual-runtime.
Start on a branch:

```bash
git switch -c fix/exiting-worktrees-dual-runtime main
```

### Files touched
- `skills-claude/exiting-worktrees/SKILL.md` — make the native `git -C <main>` path the baseline;
  demote `ExitWorktree` to an availability-conditional optimization.

### Task 2.1 — Reframe the removal section: native baseline first

The skill currently presents `ExitWorktree` (a Claude-only built-in) as the primary mechanism and the
native path as a fallback (panel BLOCKER finding #1: a Codex agent has no `ExitWorktree`, so it always
takes the path the skill labels "fallback"). Invert that.

Replace the entire section that begins `## The ExitWorktree Tool` (line 10) and ends just before
`## Why This Skill Exists` (line 39) with this content:

````text
## Removing a Worktree

The baseline removal path is native `git worktree`, which works in every runtime. The Claude Code
`ExitWorktree` built-in is an **optimization layered on top** — prefer it when it is available, but the
native path below is the contract and must carry every guard.

### Native baseline (all runtimes)

Run removal from the **main repo directory**, never from inside the worktree — running `git worktree
remove` from inside the worktree invalidates the shell CWD and every later command fails with "Path
does not exist."

```bash
# 0. Resolve <main-repo-path>. From inside a worktree, `git rev-parse --show-toplevel`
#    returns the WORKTREE path, not main; the first `worktree` entry of the porcelain
#    list is always the main checkout:
git worktree list --porcelain | awk '/^worktree /{print $2; exit}'
# 1. Remove the worktree from the main repo (the -C flag never changes your shell CWD):
git -C <main-repo-path> worktree remove <worktree-path>
# 2. Delete the branch from the main repo:
git -C <main-repo-path> branch -d <branch-name>
```

Reuse the `<main-repo-path>` resolved in step 0 for every `git -C` command. The `-C` flag is what makes
this CWD-safe — it never enters the worktree. This native path is the only acceptable removal mechanism
when `ExitWorktree` is unavailable or was a no-op.

### ExitWorktree optimization (Claude Code only)

When the Claude Code `ExitWorktree` built-in is available (deferred — fetch its schema via `ToolSearch`
before first use), prefer it: it removes the worktree and restores the session to the original working
directory (the directory before `EnterWorktree`) in a single atomic operation, so you are never
stranded in a deleted path.

- `action` (required): `"remove"` (delete worktree + branch) or `"keep"` (leave both intact).
- `discard_changes` (optional, default false): with `action: "remove"`, forces removal even with
  uncommitted files or unmerged commits. The tool refuses without this flag if the worktree has
  unsaved state.

**Scope:** `ExitWorktree` only operates on a worktree that `EnterWorktree` created in the *current*
session. For a worktree created manually (`git worktree add`), in a previous session, or via
`claude --worktree`, it is a guaranteed **no-op** ("no worktree session is active") — calling it is
harmless, but then fall back to the native baseline above, run from the main repo directory.

**Branch cleanup:** `ExitWorktree` may not delete the branch (notably with `discard_changes: true`).
After it returns, verify with `git branch --list '<branch-pattern>'`; if the branch survives, delete it
with `git branch -d <branch-name>`.
````

(The not-yet-landed inline-merge path in Pre-Exit Checklist step 4, lines 101–120, already uses
`git -C <main-repo-path>` and stays unchanged — it is already runtime-neutral.)

---

### Task 2.2 — Update the frontmatter description

In `skills-claude/exiting-worktrees/SKILL.md` frontmatter, replace:

```text
Requires Claude Code worktree cleanup tooling, landed-work verification, and user confirmation before removal.
```

with:

```text
Uses native `git worktree` removal (with Claude Code's ExitWorktree as an optimization when available), landed-work verification, and user confirmation before removal.
```

---

### Task 2.3 — Make the Exit Procedure removal step availability-conditional

Replace the Exit Procedure block (lines 161–169) that begins `**2. Call ExitWorktree:**` and ends at
the `discard_changes: true` caveat with:

````text
**2. Remove the worktree:**

If the Claude Code `ExitWorktree` tool is available, prefer it:

```
ExitWorktree(action: "remove")
```

If it reports uncommitted files or unmerged commits, go back to the checklist — do NOT retry with
`discard_changes: true` unless the user explicitly says to discard, or the worktree directory is
already gone (broken state from a prior attempt).

If `ExitWorktree` is unavailable (any non-Claude-Code runtime) or returns the no-op "no worktree
session is active", use the native baseline from "Removing a Worktree": resolve `<main-repo-path>`
porcelain-first, then `git -C <main-repo-path> worktree remove <worktree-path>` and
`git -C <main-repo-path> branch -d <branch-name>`. Never `cd` into the worktree to remove it.
````

---

### Task 2.4 — Fix the Prohibited Actions table

The table's first row forbids `git worktree remove` outright and points only to `ExitWorktree`, which
contradicts the native baseline. In the `## Prohibited Actions` table, replace the first row:

```text
| `git worktree remove` | Breaks when run from inside worktree; CWD becomes invalid | `ExitWorktree` tool |
```

with:

```text
| `git worktree remove` run **from inside the worktree** | Invalidates the shell CWD; later commands fail | `git -C <main-repo-path> worktree remove` from the main repo (or `ExitWorktree`) |
```

Verify frontmatter still parses and no path references broke:

```bash
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills-claude/exiting-worktrees
git diff --check
```
Expected: validator passes; `git diff --check` silent.

---

### Task 2.5 — Codex command/mechanism smoke test (the gate; run in a Codex session)

This is the panel's single most important fix and **cannot** be satisfied by prose. It must run in a
**Codex** session (where `ExitWorktree` does not exist) to prove the native baseline is CWD-safe and
its guards hold. **Scope:** this proves the native command *mechanism* is CWD-safe in Codex's shell —
it does **not** prove Codex discovers, routes to, or obeys the skill (it cannot: `skills-claude/` is
Claude-only per `AGENTS.md`). Codex skill *discovery* is verified separately by the both-runtime load
check in Task 3.8 (discovery, not obedience). Run against a throwaway repo, not `.agents`.

```bash
# Setup a throwaway repo with a worktree holding a landed commit
TMP="$(mktemp -d)"; cd "$TMP"
git init -q repo && cd repo
git commit -q --allow-empty -m "base"
git worktree add -q ../wt -b feature
cd ../wt
git commit -q --allow-empty -m "work on feature"
# Land it into main from the main repo (the not-yet-landed checklist path)
MAIN="$(git worktree list --porcelain | awk '/^worktree /{print $2; exit}')"
git -C "$MAIN" rev-parse --abbrev-ref HEAD            # expect: master or main
git -C "$MAIN" merge --ff-only feature
# Remove the worktree from INSIDE it, via the native baseline (the CWD-safety test)
git -C "$MAIN" worktree remove "$PWD"
# CRITICAL ASSERTION: a command must still succeed even though CWD was the removed worktree
git -C "$MAIN" worktree list
git -C "$MAIN" branch -d feature
git -C "$MAIN" worktree list
```

**Pass criteria (all must hold):**
1. `git -C "$MAIN" worktree list` after removal succeeds and no longer lists the `wt` path — i.e. the
   `git -C` form did not depend on the now-deleted CWD.
2. `git -C "$MAIN" branch -d feature` succeeds (the landed branch deletes cleanly).
3. The final `worktree list` shows only the main checkout.

If any step fails, **do not land WS2** and do not let WS3 move the skill into the plugin — the skill
stays Claude-only. Capture the transcript. (Clean up: `cd / && trash "$TMP"`.)

---

### Task 2.6 — WS2 commit and land (only after Task 2.5 passes on Codex)

```bash
git add skills-claude/exiting-worktrees/SKILL.md
git commit   # message below
git switch main && git merge --ff-only fix/exiting-worktrees-dual-runtime
```

Commit message:

```text
fix(exiting-worktrees): native git worktree removal as the dual-runtime baseline

Make `git -C <main-repo-path> worktree remove` (run from the main repo, never inside the
worktree) the baseline path that carries every CWD-safety and data-loss guard; demote the
Claude-only ExitWorktree built-in to an availability-conditional optimization. Proven on
Codex by a command/mechanism smoke test (worktree removed from inside it via `git -C`,
CWD-safe, guards intact); this proves the native mechanism, not Codex skill routing or
obedience. Skill stays in skills-claude/ until packaged by the git-cycle migration.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

**WS2 landed.** The skill is now runtime-neutral in content but still delivered Claude-only until WS3.

---

# Workstream 3 — `git-cycle` packaging migration (copy-first)

**Prerequisite:** WS1 and WS2 are landed on `main`. This workstream only packages already-fixed skills;
it introduces no behavior change beyond delivery. Copy-first: the originals remain the rollback point
until the new plugin is proven live in both runtimes (panel finding #7).

**Charter check (consulted; no ledger entry).** This packages six **already-admitted, first-party**
skills into a delivery plugin — same jobs, none merged, none archived, none losing its job (each
contract persists at the new path). Per the charter's four triggers (`docs/agents/charter.md`) this is
**neither an admission, fold, rejection, park, nor retirement**, so it takes **no
`docs/agents/contract-decisions.md` entry** — consistent with the prior `handoff`/`review-family`
packaging, which were never themselves ledgered. One Owner Per Job is unaffected: no new owner, no
collision, and `acceptance-map` stays out.

Start on a branch:

```bash
git switch -c feature/git-cycle-plugin main
```

### Files created / moved
- `plugins/git-cycle/.claude-plugin/plugin.json`, `README.md`, `LICENSE`, `PRIVACY.md`, `TERMS.md`,
  `CHANGELOG.md` — **new**.
- `plugins/git-cycle/skills/{git-hygiene,closeout-check,merge-branch,exiting-worktrees,gh-address-comments,gh-pr-review-loop}/`
  — copied from `skills/` and `skills-claude/`.
- `plugins/marketplace.json` — add the `git-cycle` entry.
- `scripts/check-protected-set.sh` — repoint four target paths.
- `scripts/codex-plugins-sync.sh` — add `git-cycle` to the bootstrap/recovery block (Task 3.7).
- Old `skills/{...}` and `skills-claude/exiting-worktrees` — trashed **last** (Task 3.9).

### Task 3.1 — Scaffold the plugin manifest

Create `plugins/git-cycle/.claude-plugin/plugin.json` with exactly:

```json
{
  "name": "git-cycle",
  "version": "1.0.0",
  "description": "Coherent local-to-shared git lifecycle: hygiene, closeout, landing, worktree exit, and PR review response",
  "author": {
    "name": "JP"
  },
  "license": "MIT",
  "keywords": [
    "git",
    "github",
    "lifecycle",
    "merge",
    "worktree",
    "pull-request"
  ],
  "skills": "./skills/",
  "interface": {
    "displayName": "Git Cycle",
    "shortDescription": "Get local work safely from a dirty tree to merged-and-shared",
    "longDescription": "A coherent git/VCS lifecycle family: clean and shape local state, confirm work is done and commit it, land a branch locally, address and publish PR review, and exit a worktree safely. Shared safety conventions (protected branches, in-progress-operation markers, fast-forward landing) are kept inline in each skill and guarded against drift.",
    "developerName": "JP",
    "category": "Productivity",
    "capabilities": [
      "Interactive",
      "Read",
      "Write"
    ],
    "defaultPrompt": [
      "Audit and clean up this repo's local git state",
      "Is this work done? Close it out with a final commit",
      "Land this branch into main locally",
      "Address the review comments on this PR",
      "Exit this worktree now that the work has landed"
    ],
    "websiteURL": "https://github.com/jpsweeney97/codex-tool-dev/tree/main/plugins/turbo-mode/git-cycle",
    "privacyPolicyURL": "https://github.com/jpsweeney97/codex-tool-dev/blob/main/plugins/turbo-mode/git-cycle/PRIVACY.md",
    "termsOfServiceURL": "https://github.com/jpsweeney97/codex-tool-dev/blob/main/plugins/turbo-mode/git-cycle/TERMS.md",
    "brandColor": "#059669",
    "screenshots": []
  }
}
```

Version 1.0.0 is honest: this packages six in-production skills (panel finding #11 — 0.1.0 would signal
"never shipped"). Justify it in the CHANGELOG (Task 3.3).

Verify it parses:

```bash
python3 -c "import json; json.load(open('plugins/git-cycle/.claude-plugin/plugin.json')); print('plugin.json parses')"
```
Expected: `plugin.json parses`.

### Task 3.2 — Copy supporting docs from an existing plugin

Reuse the existing plugins' legal/readme shape so polish matches:

```bash
mkdir -p plugins/git-cycle
cp plugins/handoff/LICENSE plugins/git-cycle/LICENSE        # review-family has no LICENSE; handoff does
cp plugins/review-family/PRIVACY.md plugins/git-cycle/PRIVACY.md
cp plugins/review-family/TERMS.md plugins/git-cycle/TERMS.md
```

Open `plugins/git-cycle/PRIVACY.md` and `plugins/git-cycle/TERMS.md`; if either names "review-family"
or "Review Family" in its body, replace those with "git-cycle" / "Git Cycle". Verify:

```bash
grep -in 'review.family' plugins/git-cycle/PRIVACY.md plugins/git-cycle/TERMS.md || echo "no stale plugin name"
```
Expected: `no stale plugin name`.

### Task 3.3 — Write the README and CHANGELOG

Create `plugins/git-cycle/README.md`:

```markdown
# Git Cycle

Get local work safely from a dirty working tree to merged-and-shared. Six skills covering one arc:

- `git-hygiene` — audit and clean local git state; shape commits by concern; prune branches.
- `closeout-check` — decide whether work is truly done and create the final local commit.
- `merge-branch` — fast-forward-land a completed branch into a verified target, locally.
- `exiting-worktrees` — verify work landed, then remove the worktree safely (native `git worktree`,
  with Claude Code's `ExitWorktree` as an optimization).
- `gh-address-comments` — verify, classify, and fix PR review threads locally; stop at one commit.
- `gh-pr-review-loop` — the full publish lifecycle on top of `gh-address-comments` (explicit-invoke).

Shared safety conventions (the protected-branch set, in-progress-operation markers, fast-forward
landing discipline) are kept inline in each skill — never behind a conditionally-loaded pointer — and
the protected-branch sentence is guarded against drift by `scripts/check-protected-set.sh`.
```

Create `plugins/git-cycle/CHANGELOG.md`:

```markdown
# Changelog

All notable changes to the Git Cycle plugin are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 1.0.0 - 2026-06-17

### Added

- Initial packaging of six in-production git-lifecycle skills (`git-hygiene`, `closeout-check`,
  `merge-branch`, `exiting-worktrees`, `gh-address-comments`, `gh-pr-review-loop`) as one coherent
  dual-runtime plugin. Version 1.0.0 reflects established skills, not new ones; the only behavior
  changes shipped separately ahead of packaging were the git-hygiene protected-resolution convergence
  and revert marker (issues #9/#10) and the `exiting-worktrees` native-git dual-runtime port. No shared
  reference file: safety conventions stay inline in each skill, drift-guarded by
  `scripts/check-protected-set.sh`.
```

### Task 3.4 — Copy the six skills into the plugin

Copy-first — originals stay until Task 3.9:

```bash
mkdir -p plugins/git-cycle/skills
for s in git-hygiene closeout-check merge-branch gh-address-comments gh-pr-review-loop; do
  cp -R "skills/$s" "plugins/git-cycle/skills/$s"
done
cp -R skills-claude/exiting-worktrees plugins/git-cycle/skills/exiting-worktrees
ls plugins/git-cycle/skills
```
Expected: the six skill directories listed. Confirm git-hygiene's reference travelled:

```bash
test -f plugins/git-cycle/skills/git-hygiene/references/git-hygiene-reference.md && echo "reference copied"
```
Expected: `reference copied`.

### Task 3.5 — Repoint the drift check at the new locations

In `scripts/check-protected-set.sh`, replace the `TARGETS` array so the three relocated skills point
into the plugin (`closeout-check` and `merge-branch` move; `git-hygiene` moves; `acceptance-map` and
`AGENTS.md` stay):

```bash
TARGETS=(
  "AGENTS.md"
  "plugins/git-cycle/skills/git-hygiene/SKILL.md"
  "plugins/git-cycle/skills/merge-branch/SKILL.md"
  "plugins/git-cycle/skills/closeout-check/SKILL.md"
  "skills/acceptance-map/SKILL.md"
)
```

Run it against the copies (originals still present, but the check now reads the plugin copies):

```bash
scripts/check-protected-set.sh
```
Expected: `OK: protected-set sentence consistent across 5 surfaces`.

### Task 3.6 — Add the marketplace entry and verify resolution

In `plugins/marketplace.json`, add a third object to the `plugins` array (after `review-family`),
matching the existing shape exactly:

```json
{
  "name": "git-cycle",
  "source": {
    "source": "local",
    "path": "./.agents/plugins/git-cycle"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

Verify the JSON parses and the path resolves (a relative path — absolute paths are silently skipped):

```bash
python3 -c "import json; d=json.load(open('plugins/marketplace.json')); print([p['name'] for p in d['plugins']])"
test -d plugins/git-cycle && echo "git-cycle source dir exists"
codex plugin list
```
Expected: the name list includes `git-cycle`; `git-cycle source dir exists`; `codex plugin list` runs
without error (it need not yet show git-cycle as installed — that is Task 3.7).

### Task 3.7 — Link (Claude) and publish (Codex)

```bash
scripts/claude-skills-sync.sh --link git-cycle
scripts/codex-plugins-sync.sh --publish git-cycle
scripts/claude-skills-sync.sh --check
scripts/codex-plugins-sync.sh --check
```
Expected: the link command creates the `~/.claude/skills/git-cycle` entry; `--publish` runs
`codex plugin add git-cycle@turbo-mode` and re-checks clean; both `--check` runs report no drift /
no missing links for git-cycle.

Then update the **bootstrap/recovery** block in `scripts/codex-plugins-sync.sh` (the stated recovery
home) so a fresh machine restores all three plugins — after WS3 the six skills live only in
`git-cycle`. In the header's `# Bootstrap / recovery` block, add a third install line under step 2,
beside `handoff` and `review-family`:

```text
#      codex plugin add git-cycle@turbo-mode
```

Verify:

```bash
grep -n 'codex plugin add git-cycle@turbo-mode' scripts/codex-plugins-sync.sh && echo 'bootstrap updated'
```
Expected: a match and `bootstrap updated`.

### Task 3.8 — Live load test in both runtimes (the gate before deletion)

Do not proceed to deletion until all six skills load in **both** runtimes from the plugin.

- **Claude Code:** confirm the symlink resolves and the six skills are discoverable:

  ```bash
  ls -l ~/.claude/skills/git-cycle
  readlink ~/.claude/skills/git-cycle
  ```
  Expected: a symlink pointing at `/Users/jp/.agents/plugins/git-cycle`.

- **Codex:** in a Codex session, confirm `git-cycle` is installed and its skills are listed:

  ```bash
  codex plugin list
  ```
  Expected: `git-cycle` present/installed. Spot-check that `merge-branch` and `exiting-worktrees`
  appear in the Codex skill list.

If any skill fails to load, fix the manifest/paths before Task 3.9. The originals are still the live
source, so nothing is lost.

### Task 3.9 — Remove the originals (only after Task 3.8 passes)

Now that the plugin is proven live in both runtimes, retire the old sources and stale symlinks:

```bash
# Stale ~/.claude/skills entries for the five that were standalone (exiting-worktrees was Claude-only,
# also linked). Remove each symlink with trash:
for s in git-hygiene closeout-check merge-branch exiting-worktrees gh-address-comments gh-pr-review-loop; do
  [ -L ~/.claude/skills/$s ] && trash ~/.claude/skills/$s
done
# Old source dirs:
for s in git-hygiene closeout-check merge-branch gh-address-comments gh-pr-review-loop; do
  trash skills/$s
done
trash skills-claude/exiting-worktrees
# Confirm no dangling links and the canary scripts are clean:
scripts/claude-skills-sync.sh --check
scripts/codex-plugins-sync.sh --check
```
Expected: both `--check` runs clean (no MISSING, no DANGLING, no DRIFT). If `--check` reports a
dangling link for any of the six, remove it with `trash`.

### Task 3.10 — WS3 verification, commit, and land

```bash
python3 -c "import json; json.load(open('plugins/git-cycle/.claude-plugin/plugin.json'))" && echo "manifest ok"
# Structurally validate all six copied skills (cp -R of already-validated sources; catches a partial
# copy and re-parses each frontmatter at its new path):
for s in git-hygiene closeout-check merge-branch exiting-worktrees gh-address-comments gh-pr-review-loop; do
  python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py "plugins/git-cycle/skills/$s"
done
# Parse every copied openai.yaml companion (exiting-worktrees has none):
for s in git-hygiene closeout-check merge-branch gh-address-comments gh-pr-review-loop; do
  ruby -ryaml -e 'YAML.load_file(ARGV[0])' "plugins/git-cycle/skills/$s/agents/openai.yaml" && echo "openai.yaml ok: $s"
done
scripts/check-protected-set.sh
git diff --check
git status --short
```
Expected: `manifest ok`; the validator passes for all six (the documented
`argument-hint`/`disable-model-invocation` "unexpected key" note is accepted); each `openai.yaml`
parses; drift check `OK: ... 5 surfaces`; `git diff --check` silent;
`git status` shows the additions under `plugins/git-cycle/`, the marketplace edit, the script repoint,
and the deletions of the old skill dirs.

Commit and fast-forward onto `main`:

```bash
git add -A
git commit   # message below
git switch main && git merge --ff-only feature/git-cycle-plugin
```

Commit message:

```text
feat(git-cycle): package the six git-lifecycle skills as one dual-runtime plugin

Move git-hygiene, closeout-check, merge-branch, exiting-worktrees, gh-address-comments,
and gh-pr-review-loop into plugins/git-cycle/ (no shared reference — safety conventions
stay inline, drift-guarded by scripts/check-protected-set.sh, now repointed). exiting-
worktrees gains Codex delivery (its native path proved on Codex in the prior workstream).
Copy-first migration: plugin proven live in both runtimes before the originals were
trashed. Marketplace entry added; Codex cache republished. Mirror not published.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

> Codex cache republish (Task 3.7) is local and expected. The GitHub release **mirror** is out of
> scope — publish it only when the user explicitly asks.

**WS3 landed.** `git-cycle` is the coherence/packaging home for all six skills.

---

## Self-review

- **Coverage:** every locked-design element maps to a task — #9 convergence (1.1), #10 both sites
  (1.2/1.3), canonicalization (1.4), `AGENTS.md` floor (1.5), drift check + real caller (1.6/1.7),
  worktree port + Codex *mechanism* proof (2.1–2.5), copy-first packaging with load gate (3.1–3.9). The dropped
  reference appears nowhere. acceptance-map's copy is covered by the check (1.6 target list) though it
  stays out of the plugin.
- **Independence:** WS1 and WS2 each land on their own branch with their own verification and never
  reference plugin paths; WS3 explicitly lists WS1+WS2 landed as a prerequisite and only moves files.
- **Placeholders:** the one intentional `<...>` token is `<main-repo-path>` / `<worktree-path>` /
  `<branch-name>` inside skill prose and the behavior-test (resolved at runtime by the executor), and
  `<hash>` in the issue-close comments (the merge commit hash). No "TBD"/"similar to Task N".
- **Known limits carried forward (not gaps):** perfect cross-skill protected-resolution consistency is
  not achievable (recorded in 1.1 and the commit body); the `AGENTS.md` floor is `.agents`-local and
  does not travel (stated in 1.5); the drift check's only ship-relevant caller is the validation ladder
  plus the local SessionStart canary (1.7) — the Codex publish path is not a caller and is not claimed.