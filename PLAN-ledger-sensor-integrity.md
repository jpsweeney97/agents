# PLAN: Ledger & Sensor Integrity (do this one first)

Rank: 1 of 5 — highest leverage-per-effort and time-sensitive. The skill-usage ledger feeds a pre-registered keep/prune decision committed for **2026-08-01** (`docs/reviews/2026-07-02-framework-challenge.md:62`). Its summary output is currently distorted by alias fragmentation and non-skill contamination; if unfixed, the 08-01 read runs on garbage. Separately, the fresh-machine recovery sample in `scripts/claude-skills-sync.sh` regenerates a SessionStart canary missing 2 of its 5 checks.

## Goal

1. Make `scripts/skill-usage-miner.py`'s summary trustworthy: merge invocation-token aliases of the same skill, and separate current-roster skills from built-in commands and retired tokens, so per-skill fire counts are honest.
2. Fix the stale recovery header in `scripts/claude-skills-sync.sh` so a fresh-machine recovery regenerates all 5 canary checks, not 3.
3. Append a factual correction to the decision ledger about the usage ledger's real coverage span.

## Ground rules (repo invariants — do not skip)

- Work on a branch (`chore/ledger-sensor-integrity`); a user-level hook blocks edits on `main`. Start with `git status --short --branch`.
- Never run `rm`; delete only with `trash <path>`.
- Markdown prose: one logical line per paragraph and per bullet; never hard-wrap.
- Do NOT edit `docs/reviews/2026-07-02-framework-challenge.md` — it is a frozen, dated review; the repo rule is "a dated review is never hand-edited."
- Do NOT rewrite, sort, dedupe, or delete lines in `~/.claude/logs/skill-usage-ledger.jsonl`. It is an append-only raw record. All normalization happens at read/summary time inside the miner.
- Do NOT change the pre-registered 08-01 branch definitions anywhere (still-zero → tranche-prune; spread → partial vindication). This plan calibrates the instrument; it must not touch the decision rules.
- Do NOT edit `scripts/skill-usage-hook.py` or `scripts/com.jp.skill-usage-miner.plist`. The hook writes raw canonical names already; the plist just invokes the miner script, so a miner edit needs no launchd reinstall (verify the plist still only references the script path, nothing internal to it).
- These scripts are capability tooling, not behavior contracts — per `docs/agents/charter.md` ("Tools are tools"), editing them is NOT a charter event. No charter consult, no admission test. Don't over-trigger the charter.

## Exact files to touch

1. `scripts/skill-usage-miner.py` — the only functional code change.
2. `scripts/claude-skills-sync.sh` — header comment block only (the sample SessionStart JSON, currently around lines 25–41).
3. `docs/agents/contract-decisions.md` — append-only factual update to the existing skill-usage-ledger entry (the 2026-07-02 entry that describes the first ledger read; find it by grepping for `skill-usage`).

Read-only inputs: `~/.claude/logs/skill-usage-ledger.jsonl`, `.claude/settings.local.json` (untracked; holds the live canary), `.codex/hooks.json` (tracked; same 5 entries), `plugins/handoff/skills/*/SKILL.md` (to verify alias identities).

## Background facts (verified 2026-07-09; re-verify cheaply before relying on them)

- Ledger: ~3,627 records, 0 malformed, 136 distinct skill tokens, span 2026-01-07 → 2026-07-09. The file is NOT time-sorted (append order is Claude-projects-then-Codex).
- Fragmentation: the same handoff skills appear under both their typed command token and their canonical skill name — `load` (~328) vs `load-handoff` (~337), `save` (~171) vs `save-handoff` (~280). Typed tokens come from `<command-name>` capture; canonical names from Skill-tool fires.
- Contamination: the `<command-name>` regex also captures Claude Code built-in commands that are not roster skills — `effort` (~233, ranks #5 overall), `copy` (~120, #10), `model`, `clear`, `compact`, `config`, `cd`, `init`, `review` — and retired-era tokens like `summary` (~135), `save-summary` (~32), `quicksave` (~5).
- The live SessionStart canary (both `.claude/settings.local.json` and `.codex/hooks.json`) has 5 entries: `claude-skills-sync.sh --check`, `codex-plugins-sync.sh --check`, `check-protected-set.sh`, `check-handoff-paths.sh`, `check-review-family.sh`. The recovery sample in the sync-script header lists only the first 3. That header is the designated recovery path for the untracked settings file (`docs/plans/2026-06-17-git-cycle-plugin.md:304`), so a fresh-machine recovery would silently drop two drift guards.
- The ledger entry in `contract-decisions.md` describes the first read as covering "~6 weeks of Claude-side transcripts"; the actual mined span is ~6 months because Codex sessions reach back to January.

## Steps, in order

### Step 1 — baseline

```bash
cd /Users/jp/.agents && git status --short --branch
git checkout -b chore/ledger-sensor-integrity
python3 scripts/skill-usage-miner.py --summary-only > /tmp/miner-baseline.txt 2>&1 || true
```

Record from the baseline: total fires, distinct-token count, and the per-token counts for `load`, `load-handoff`, `save`, `save-handoff`, `search`, `search-handoffs`. You need these for the acceptance check.

### Step 2 — verify alias identities before merging anything

An alias merge is only safe when (a) the alias token is a documented invocation token of the target skill and (b) the alias token is not itself a skill anywhere in the repo. For each proposed pair, verify both:

- `load` → `load-handoff`: `plugins/handoff/skills/load-handoff/SKILL.md` description names `/load` (or `$load`) as its token; no dir named `load` exists under `skills/`, `skills-claude/`, or `plugins/*/skills/`.
- `save` → `save-handoff`: same check against `plugins/handoff/skills/save-handoff/SKILL.md`.
- `search` → `search-handoffs`: same check against `plugins/handoff/skills/search-handoffs/SKILL.md`.

Do NOT alias-merge `summary`, `save-summary`, or `quicksave` into anything. Those are retired-era tokens whose identity mapping is uncertain; the roster classification in Step 3 will separate them instead. Merging on guesswork corrupts exactly the signal this plan protects.

### Step 3 — edit `summarize()` in the miner

Design constraints: normalization happens only at summary time (raw records stay raw); the roster is derived live from the repo, not hardcoded; the script keeps its stdlib-only, no-dependency shape; full type hints; fail fast with the house error format (`"{operation} failed: {reason}. Got: {input!r:.100}"`).

Implementation sketch (adapt to the existing code style, which you must read first):

```python
REPO = Path(__file__).resolve().parent.parent

ALIASES = {
    # typed command token -> canonical skill name (verified: token documented
    # in the target SKILL.md; no roster dir of the alias name exists)
    "load": "load-handoff",
    "save": "save-handoff",
    "search": "search-handoffs",
}


def roster_names() -> set[str]:
    """Current skill names: dirs in skills/, skills-claude/, plugins/*/skills/."""
    roots = [REPO / "skills", REPO / "skills-claude", *sorted((REPO / "plugins").glob("*/skills"))]
    names: set[str] = set()
    for root in roots:
        if not root.is_dir():
            raise SystemExit(f"roster scan failed: expected skill root missing. Got: {str(root)!r:.100}")
        names.update(p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))
    return names


def archived_names() -> set[str]:
    root = REPO / "skills-archive"
    return {p.name for p in root.iterdir() if p.is_dir()} if root.is_dir() else set()
```

In `summarize()`: apply `ALIASES.get(skill, skill)` to each record's skill token before accumulating, then print three sections instead of one flat table — current-roster skills first (sorted by total, descending), then archived skills, then everything else under a heading like `non-roster tokens (built-in commands, plugin-qualified externals, retired/unknown)`. Keep the existing column format for each section. Keep the final `N distinct skills, M fires total` line, but make it report the three section counts too.

Also update the module docstring: note that summaries alias-merge typed command tokens into canonical skill names, that the ledger file is append-ordered (not time-sorted — consumers must never assume chronology), and that raw records are never rewritten.

Edge cases a naive implementation gets wrong:

- Tokens with plugin/namespace prefixes exist in the ledger (e.g. `github:github`, `gmail:gmail`, `handoff:load-handoff`-style forms may appear depending on runtime). Match roster membership on the segment after the last `:` as a fallback when the full token is not in the roster, and say so in the section heading logic — but never alias-merge on the fallback.
- `review`, `init`, `verify`, `run`, `loop`, `code-review` are Claude-bundled skills/commands, NOT repo roster skills. They must land in the non-roster section, not be dropped. No record is ever discarded — every fire appears in exactly one section.
- The alias merge must not create collisions: assert (fail fast) that no alias key is present in `roster_names()`.
- `skills-archive/` may contain non-skill files; only count directories.

### Step 4 — validate the miner change

```bash
python3 -m py_compile scripts/skill-usage-miner.py
ruff check scripts/skill-usage-miner.py   # if ruff is available; note the result either way
python3 scripts/skill-usage-miner.py --summary-only > /tmp/miner-after.txt 2>&1
```

Check against the Step-1 baseline: total fire count is IDENTICAL (normalization must not lose records); `load`/`save`/`search` no longer appear as separate rows; `load-handoff`'s count is the sum of the old `load` + `load-handoff` (same for save/search pairs); `effort`, `copy`, `clear` etc. appear only in the non-roster section; distinct-token count dropped by exactly the number of merged alias keys that had fires.

Then run the full miner once (`python3 scripts/skill-usage-miner.py`) to confirm mining mode still works end-to-end and appends nothing malformed (it may legitimately add new fires from recent sessions; that is fine).

### Step 5 — fix the recovery header in `scripts/claude-skills-sync.sh`

In the header comment block's sample SessionStart JSON (currently ~lines 32–41), add two entries after the `check-protected-set.sh` entry, matching the existing format exactly:

```
#          {"type": "command",
#           "command": "/Users/jp/.agents/scripts/check-handoff-paths.sh || true",
#           "timeout": 15, "statusMessage": "Checking handoff path-set drift"},
#          {"type": "command",
#           "command": "/Users/jp/.agents/scripts/check-review-family.sh || true",
#           "timeout": 15, "statusMessage": "Checking review-family core drift"}
```

Mind the JSON comma placement (the previously-last entry gains a trailing comma). Then verify: `bash -n scripts/claude-skills-sync.sh`, and diff the 5 commands in the header sample against the 5 in `.codex/hooks.json` — the command paths must match exactly. This is a comment-only edit; the script's behavior must be unchanged (`bash scripts/claude-skills-sync.sh --check` still exits 0).

### Step 6 — append the ledger correction

In `docs/agents/contract-decisions.md`, find the entry recording the skill-usage ledger's first read (grep `6 weeks` or `skill-usage`). Entries are one logical line each; append to the END of that same line (never alter its existing words):

> Update (2026-07-09): the mined span actually reaches back to 2026-01 (Codex sessions back-mine to January), ~6 months of coverage, not ~6 weeks; the ledger file is append-ordered, not time-sorted, so consumers must not assume chronology; summary-time alias normalization (typed handoff command tokens merged into canonical skill names) and roster/non-roster classification were added to the miner so the 2026-08-01 re-read runs on merged, uncontaminated counts — raw records and the pre-registered decision branches are untouched.

This follows the ledger's existing "Update (date): …" append precedent. The ledger is append-only: never rewrite settled entry text.

### Step 7 — commit

```bash
git diff --check
git add scripts/skill-usage-miner.py scripts/claude-skills-sync.sh docs/agents/contract-decisions.md
git diff --cached --stat   # confirm exactly these three files
git commit -m "fix(sensors): miner alias-merge + roster classification; complete canary recovery sample; ledger coverage correction"
```

Do not merge to `main` or push unless JP asks. Report the branch name and the before/after summary numbers.

## Edge cases found during exploration (a weaker model would miss these)

- The ledger file's first LINE is dated 2026-06 but the earliest TIMESTAMP is 2026-01 — anyone "checking the date range" by reading the first/last lines gets it wrong. Compute ranges from the `ts` field.
- The launchd job (`com.jp.skill-usage-miner`) runs the miner every ~5 days and logs its stdout. Changing the summary format is safe (log-only consumer), but breaking the script breaks silent background mining — hence the mandatory full-run check in Step 4.
- The installed plist at `~/Library/LaunchAgents/com.jp.skill-usage-miner.plist` is byte-identical to the repo copy and must stay that way; this plan gives no reason to touch either.
- `synapsis` appears in `~/.claude/skills/` but is NOT this repo's skill (external, exempted in the sync script at the `EXEMPT=(synapsis)` line). If it shows up in ledger data, it belongs in the non-roster section; do not add it to any roster.
- Fires from subagents are tagged `sidechain`; the summary already tracks them separately. Do not filter them out — the 08-01 read wants total visibility.
- Do not "fix" the non-chronological ledger by sorting and rewriting the file. Dedup keys and the append-only contract depend on the file as-is.

## Acceptance criteria (verify each; do not claim done without output)

1. `python3 -m py_compile scripts/skill-usage-miner.py` exits 0.
2. `--summary-only` output: three sections; total fires equal to baseline; `load`+`load-handoff` merged (sum matches baseline arithmetic); `effort`/`copy` in non-roster section only.
3. A full miner run completes without error and the ledger line count only grows (never shrinks).
4. `bash -n scripts/claude-skills-sync.sh` exits 0; `--check` exits 0; the header sample now names all 5 canary commands with paths byte-identical to `.codex/hooks.json`.
5. `docs/agents/contract-decisions.md` diff shows only an appended "Update (2026-07-09): …" sentence on one existing line; `git diff --check` clean.
6. `docs/reviews/2026-07-02-framework-challenge.md`, `scripts/skill-usage-hook.py`, the plist, and the raw ledger JSONL are all untouched (`git status` confirms; ledger untracked but never opened for write).
7. One commit on `chore/ledger-sensor-integrity` containing exactly the three intended files.
