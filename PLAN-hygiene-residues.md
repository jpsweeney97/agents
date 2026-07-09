# PLAN: Clear the small flagged residues

Rank: 5 of 5 — lowest individual stakes, but each item is a standing bit of noise or record-staleness that costs attention every time it's re-noticed. All were found and verified during the 2026-07-09 repo sweep. Each item is independent; do them in the order given (cheapest and least-reversible-risk first), skip any whose precondition no longer holds, and report per-item.

## Goal

Close the three synthetic GitHub issues, trash dead local cruft, resolve the `teach` orphan companion file, add the missing `review-family` LICENSE, and append the ledger's final Era-84 closing update.

## Ground rules (repo invariants — do not skip)

- Branch first (`chore/hygiene-residues`) for the file-changing items; the hook blocks `main` edits. Never `rm`; delete only with `trash <path>`.
- The ledger is append-only. Markdown one logical line per bullet.
- Item E touches plugin SOURCE, which is mirrored to a version-keyed Codex cache checked by a SessionStart canary — follow its republish step exactly or every future session opens with DRIFT noise.
- Do not push anything: no `git push`, no mirror push. Closing GitHub issues (item A) is a tracker mutation JP has authorized by handing you this plan; it is the only remote mutation in scope.

## Exact files/surfaces to touch

1. GitHub issues #17, #18, #19 on `jpsweeney97/agents` (close + comment + label).
2. `scripts/err.txt` (trash).
3. `skills/.DS_Store`, `skills/simplify-code/scripts/__pycache__/`, `skills/simplify-code/tests/__pycache__/` (trash).
4. `skills/teach/GLOSSARY-FORMAT.md` and possibly `skills/teach/SKILL.md` (link or trash).
5. `plugins/review-family/LICENSE` (new file) + Codex cache republish.
6. `docs/agents/contract-decisions.md` (one appended Mining-Queue update line).

## Steps, in order

### Step A — close the three synthetic issues

Verify first, then act. The three open issues are synthetic test artifacts: each body ends "Source: tech-debt backlog, item N of 3", and they describe an auth module, retry-helper copies, and logging config across "4 services" — none of which exists in this repo (it is a skills workshop; confirm with a quick grep: `grep -ril 'auth module' skills/ docs/ scripts/ | head` and equivalents return nothing relevant). They were created 2026-06-21, consistent with a `to-issues`/`triage` skill evaluation. The repo's stated backlog policy makes the tracker a non-home anyway ("Backlog lives in the frozen capability review + handoffs + throughline — never the GitHub tracker").

```bash
gh label list --repo jpsweeney97/agents | grep wontfix   # the triage vocabulary (docs/agents/triage-labels.md) says wontfix exists; if missing, create it: gh label create wontfix --repo jpsweeney97/agents --description "Will not be actioned"
for n in 17 18 19; do
  gh issue edit  $n --repo jpsweeney97/agents --add-label wontfix --remove-label needs-triage
  gh issue close $n --repo jpsweeney97/agents --reason "not planned" \
    --comment "Closing as a synthetic test artifact: this issue describes code (auth module / retry helpers / multi-service logging) that does not exist in this repo — it was seeded during a skill evaluation (body: 'Source: tech-debt backlog, item N of 3'). No real work is tracked here; per repo policy the backlog lives outside the tracker."
done
gh issue list --repo jpsweeney97/agents --state open   # expect empty
```

Close ONLY #17/#18/#19. If any of the three has gained real content or references since (check `gh issue view N --comments` first), skip it and report.

### Step B — trash dead cruft

```bash
git status --short --branch   # confirm err.txt still untracked
wc -c scripts/err.txt          # expected 0 bytes; if NON-empty, read it and report instead of trashing
trash scripts/err.txt
trash skills/.DS_Store
trash skills/simplify-code/scripts/__pycache__
trash skills/simplify-code/tests/__pycache__
```

All four are untracked/gitignored (verify with `git check-ignore -v` if unsure) — no commit results from this step. `__pycache__` regenerating later is normal and fine.

### Step C — resolve the `teach` orphan companion

`skills/teach/GLOSSARY-FORMAT.md` exists on disk but `skills/teach/SKILL.md` never references it by name, while its three siblings (`MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`) are each linked. Read both files, then apply this decision rule:

- If SKILL.md instructs producing/maintaining a glossary artifact (its prose mentions a glossary around line 15) and GLOSSARY-FORMAT.md plausibly governs that artifact's shape → add a reference link in SKILL.md at the analogous place and in the same style as the three sibling links. This is the expected outcome.
- If the glossary prose was removed or GLOSSARY-FORMAT.md contradicts current SKILL.md behavior → `trash skills/teach/GLOSSARY-FORMAT.md` (build-and-prune material; no ledger entry, no archive required).

Either way, run `scripts/check-library-integrity.sh` afterward — its orphan-support-file check is the thing this step satisfies.

### Step D — add the missing `review-family` LICENSE

`plugins/review-family/.claude-plugin/plugin.json` declares `"license": "MIT"` but ships no LICENSE file; sibling plugins `handoff` and `git-cycle` both ship one. Copy the sibling's shape:

```bash
cp plugins/handoff/LICENSE plugins/review-family/LICENSE
head -5 plugins/review-family/LICENSE   # check the copyright line; if it names the handoff plugin specifically, edit to match review-family / keep the plain holder line as the siblings have it
```

Now the critical follow-through: plugin source is byte-diffed against the Codex cache by the SessionStart canary (`codex-plugins-sync.sh --check`). Adding a file to source creates DRIFT until republished. A LICENSE is not a behavior change, so per the repo convention ("bump the manifest version on behavior changes") no version bump is taken — republish in place at the current version:

```bash
scripts/codex-plugins-sync.sh --publish review-family
scripts/codex-plugins-sync.sh --check   # must exit 0 with no output
```

Do NOT touch the release mirror (`/Users/jp/Projects/active/codex-tool-dev/`): mirror sync is a push-authority operation reserved for release trains on JP's explicit go. The mirror lacking LICENSE until the next review-family release is a known, acceptable, canary-invisible gap — note it in your report so the next release-cut sweeps it.

### Step E — append the ledger's Era-84 closing update

The Mining Queue section of `docs/agents/contract-decisions.md` currently ends by saying the two Class-B publish trains are "outstanding" — but they ran later that same night (git-cycle `1.4.0` and handoff `3.2.1` published to the Codex cache and the mirror, mirror commit `aca0aef8`, per the 2026-07-09 00:50 handoff). Append one sentence to the END of the existing Reopened-(2026-07-08) paragraph, after its last "Update (2026-07-09, later): …" sentence (same append-in-place style, never altering existing words):

> Update (2026-07-09, closing): both Class-B publish trains ran the same night — git-cycle `1.3.0→1.4.0` and handoff `3.2.0→3.2.1` cut on-branch, ff-merged, republished to the Codex cache (`--check` green) and synced to the mirror (`aca0aef8`) — so nothing Era-84 remains outstanding in any channel; the program returns to closed-pending-triggers (parks stand, `wayfinder` per its entry).

### Step F — commit the file-changing work

```bash
git diff --check
git status --short          # expect: teach SKILL.md (maybe), review-family LICENSE, contract-decisions.md
git add <exactly the intended files>
git commit -m "chore: hygiene residues — teach glossary link, review-family LICENSE, Era-84 ledger closing update"
```

Items A and B leave no repo diff; report them as actions taken. Do not merge or push unless JP asks.

## Edge cases found during exploration (a weaker model would miss these)

- Closed issues #2–#16 are REAL history (they record actual skill fixes) — nothing in this plan touches closed issues. The synthetic trio is exactly #17/#18/#19.
- `gh issue close --reason` accepts `"not planned"` or `"completed"`; synthetic artifacts are "not planned". Using "completed" would falsely imply the described work was done.
- The Codex cache is version-keyed (`~/.codex/plugins/cache/turbo-mode/review-family/0.8.0/`). Publishing without a bump overwrites the same version dir — correct here precisely because nothing behavioral changed; if you find yourself changing ANY SKILL.md in the plugin, stop — that becomes a release-cut, out of this plan's scope.
- `--check` prints nothing on success (exit 0 is the signal); don't mistake silence for failure.
- The review-family plugin also ships `PRIVACY.md`/`TERMS.md`/`README.md` — do not "harmonize" those or copy anything else from siblings; the finding is LICENSE only.
- `throughline` and other handoff-plugin skills reference `.agents/handoffs/` paths that don't exist inside the plugin — those are runtime output paths in consuming projects, not broken references; don't "fix" them.
- Two skill descriptions exceed the 90-word budget guidance (`methodology-critique` ~100, `spec-drift-reconcile` ~91). Deliberately NOT in scope: `AGENTS.md` says description length is a routing-clarity input, never a conformance score, and both skills are boundary-heavy by design. Leave them.
- Similarly out of scope: the four git-cycle skills lacking `agents/openai.yaml` (companion metadata is optional by convention) and gitignored `.DS_Store` files elsewhere on the machine. Resist completing the pattern.

## Acceptance criteria (verify each; do not claim done without output)

1. `gh issue list --repo jpsweeney97/agents --state open` returns empty; each of #17/#18/#19 shows closed as "not planned" with the explanatory comment and `wontfix` label.
2. `scripts/err.txt`, `skills/.DS_Store`, and both `__pycache__` dirs are gone (`ls` errors), via `trash` only.
3. `scripts/check-library-integrity.sh` passes with no orphan-support-file complaint about `teach`.
4. `plugins/review-family/LICENSE` exists with an MIT text matching the siblings' shape; `codex-plugins-sync.sh --check` exits 0 AFTER the publish; the mirror is untouched (`git -C /Users/jp/Projects/active/codex-tool-dev status --short` shows no change from this session).
5. The ledger diff is a single appended sentence inside the Mining Queue paragraph; `git diff --check` clean.
6. One commit on `chore/hygiene-residues` containing exactly the intended files; items with no diff reported as actions.
