# Skill-Use Contract — Implementation Plan

Status: authored 2026-07-12 from the JP-approved governing design [`docs/plans/2026-07-11-skill-use-contract-design.md`](2026-07-11-skill-use-contract-design.md) (approved at `6b5365d`, branch `feature/skill-use-contract`). The design's Build Order steps 1–15 are the settled sequence; this plan expands them into executor-followable tasks. Executor: `execute-plan` or a session working task-by-task.

## Orientation for a zero-context executor

- This repo (`/Users/jp/.agents`) is the single source for skills served to both Claude Code and Codex. `skills/` is dual-runtime, `skills-claude/` Claude-only, `plugins/review-family/` a dual-runtime plugin. Editing a `skills/` file changes the live skill immediately (Claude serves it via `~/.claude/skills` symlinks; Codex scans the tree in place).
- All repo work happens on `feature/skill-use-contract`. Never commit on `main` (a hook blocks it). Delete only with `trash`, never `rm`. Do not push, publish, or sync caches/mirrors without JP's explicit ask.
- Markdown prose here is one logical line per paragraph and per bullet — never hard-wrapped.
- The two user-global instruction files — `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` — are plain files outside this repo and outside version control. **They are edited only in Task 10, and only after the Task 9 GO.**
- Blind-evaluation discipline (repo `AGENTS.md`, `## Blind Evaluations`) binds Tasks 4–8: never reveal arm identities, expected outcomes, or intermediate results to any context that will grade trials. Trial prompts are authored fresh-context on facts-only kernels (Task 5), never written in this plan or by an agent that has read this plan's expectations.

## Hard gates (JP decision points — stop and ask, do not proceed past these)

1. **Gate 1 (in Task 3):** if the live Codex runtime verification fails, stop; the contract narrowing reopens per the design's Premise fallback (runtime-divergent text, weaker canary). JP decides.
2. **Gate 2 (Task 9):** the Charter Admission consult plus JP's separate GO/NO-GO ratification for Decision A (runtime contract) and Decision B (repo convention). No global-file edit and no repo-`AGENTS.md` convention edit before the respective GO.
3. **Standing:** `scrutinize-skill`'s edit stays source-only; the Class-B publish train (version bump → Codex republish → mirror) runs only on JP's explicit ask. No push without JP's ask. Expected consequence, not a failure: from the Task-12 edit until that ask, `codex-plugins-sync.sh --check` — wired into SessionStart in both `.codex/hooks.json` and `.claude/settings.local.json` — reports `DRIFT: review-family` at every `.agents` session start. Leave it red; never "repair" it by publishing without JP's explicit ask.

## File map

Created by this plan:

- `docs/plans/2026-07-12-skill-use-contract-implementation-plan.md` — this plan.
- `.agents/scratch/skill-use-probes/` — the probe rig (git-ignored via the `.agents/` ignore rule; verified in `.gitignore`). Subdirs: `trees/` (two scratch `CLAUDE_CONFIG_DIR` trees + pristine tarballs), `fixture/` (frozen workspace fixture + manifest), `armmap/` (arm map + sealed keys; never readable by the scorer), `tasks/` (fresh-authored trial prompts), `out/` (captured trial streams + stripped scorer packets); plus `runner.py`, `schedule.json`, `pilot-schedule.json`, `schedule-extensions.json` (derived re-run/escalation rows only — the sealed `schedule.json` is never edited), and the exact-roster check inputs `expected-roster.json` and `sentinel-absent.json` at the rig root.
- `docs/plans/2026-07-NN-skill-use-probes-preregistration.md` — the sealed preregistration (Task 7; `NN` = authoring date).
- `scripts/check-skill-use-contract.sh` — the byte-identity drift canary (Task 10).
- `docs/smoke-tests/2026-07-NN-skill-use-data-layer-matrix.md` — the data-layer behavior-proof coverage table (Task 13).

Modified by this plan:

- `docs/plans/2026-07-11-skill-use-contract-design.md` — gains a `## Build Records` appendix (Tasks 2, 3, 8).
- `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md` — the `## Skill Use` block (Task 10, post-GO only).
- `.codex/hooks.json` (tracked), `.claude/settings.local.json` (untracked), `scripts/claude-skills-sync.sh` header recipe — canary wiring (Task 10).
- `AGENTS.md` — one convention line in Skill Editing (Task 11, post-GO only).
- Nine `SKILL.md` bodies + one description (Task 12): `skills/diagnose`, `skills/tdd`, `skills/test-trust-audit`, `skills/red-team`, `skills/postmortem`, `skills/observability-instrumentation`, `skills/deploy-plan`, `skills/behavior-smoke-test`, `plugins/review-family/skills/scrutinize-skill`, `skills/making-recommendations` (description only).
- `docs/agents/contract-decisions.md` — two ledger entries (Task 14).

## Task 1 — Branch and evidence-surface check

1. Run `git status --short --branch` and `git log -1 --oneline`. Required: branch `feature/skill-use-contract`, clean tree, HEAD at or past `6b5365d`.
2. Confirm the design doc is committed: `git log --oneline -1 -- docs/plans/2026-07-11-skill-use-contract-design.md` returns a commit. It is the durable evidence artifact every later ledger entry cites.
3. If anything mismatches, stop and reconcile before proceeding — no other task starts from a dirty or wrong-branch state.

## Task 2 — Finalize the contract wording (design Build Order step 2, first half)

The draft, verbatim from the design (§1) — this is the input, not yet the landed text:

```markdown
## Skill Use

- When a mid-task finding changes what the work needs, re-check whether an available skill owns the newly revealed work; when one plausibly fits, invoke it rather than improvising the same job unaided. The check is silent — don't narrate it.
- When an invoked skill completes and names a follow-on lane — an exit, handoff, or next-step pointer — take it only when the current request and governing skill authorize continuation; otherwise offer it explicitly. Don't drop the chain and improvise the next step.
- When a task or its findings span more than one skill's job, compose the skills rather than stretching one past its boundary. Composition may be sequential or concurrent, but it does not itself authorize subagent fan-out.
- A governing skill's explicit stop, containment, or sequencing instruction overrides these defaults, and delegated agents follow their brief.
```

1. Run the `agent-facing-design` skill on the draft as a material always-loaded obligation being added: does each bullet protect/provoke correctly, is any machinery smuggled in, is the no-subagent-authority boundary airtight? Carry the design's named flag: no wording may read as license for unrequested multi-agent fan-out (the draft already says "does not itself authorize subagent fan-out" — the gate confirms it survives edits).
2. Run the `writing-principles` skill on the surviving text for obligation-prose quality.
3. Constraints that survive both gates unchanged: the section heading is exactly `## Skill Use`; the text is byte-identical for both runtimes (no runtime-specific tokens; note the draft already contains none); the four-bullet structure and the precedence-clause final bullet stay unless a gate finds a defect.
4. Record the final wording, the word count (design priced 144 words including the heading — re-price if changed), and both gate outcomes in a new `## Build Records` section appended to `docs/plans/2026-07-11-skill-use-contract-design.md`. Commit: `git add docs/plans/2026-07-11-skill-use-contract-design.md && git commit -m "docs: record final skill-use contract wording through AFD and writing-principles gates"`.

The final wording from this task is THE canonical text used in Tasks 4 (ON tree), 7 (prereg hash), and 10 (landing + canary `CANON`). Every later task copies it byte-exactly from the Build Records section; no task re-edits it.

## Task 3 — Verify the Codex request-time terrain claim (step 2, second half; Gate 1)

The design's round-3 narrowing rests on an unverified claim: the current Codex runtime carries a request-time skill-matching instruction. Verify it against the live runtime before any Admission consult.

1. Record `codex --version` (live at plan authoring: `codex-cli 0.144.1`).
2. Probe first-hand: `codex exec --sandbox read-only "Quote verbatim every sentence in your system instructions that tells you when to use, match, or prefer available skills. If no such instruction exists, reply exactly: NONE."` Save the full output. If the CLI flags differ on the live version, adapt (`codex exec --help`) — the requirement is a fresh headless run of the real runtime, not memory or docs.
3. Corroborate via source when available: search the installed Codex CLI's prompt assets (e.g. `grep -ri "skill" "$(dirname "$(readlink -f "$(which codex)")")"/../` or the npm package dir) for the matching instruction — the npm entry point is a JS launcher over a vendored native binary, so use `grep -a` or `strings` on binary hits to extract the quotable text a bare `grep` only flags as "Binary file matches"; a source hit plus the probe is the strongest local evidence. Absence of a source hit with a positive probe is still a pass — record which evidence classes fired, and label a probe-only pass explicitly as the weaker class in the Build Records entry (a model can confabulate a plausible "verbatim quote"; the source hit is the corroborating class).
4. **Decision rule:** the probe (or source) shows a request-time instruction directing Codex to use an available matching skill → claim verified; record version, method, and quoted text in `## Build Records` and proceed. Nothing found → **STOP (Gate 1)**: report to JP that the Premise fallback is live (runtime-divergent text for the Codex copy, at the cost of the byte-identical canary) and await direction. Do not run Tasks 4–9 in the failed state without JP's reopened-narrowing decision.
5. Commit the Build Records update.

## Task 4 — Build the probe rig (step 3)

All rig state lives under `.agents/scratch/skill-use-probes/` (git-ignored); per-trial disposable copies — config trees and fixture copies — extract into unique `sup-*` temp dirs, created fresh each trial and never deleted by the runner (reclaim with `trash` when wanted; the trash-only rule holds with no carve-out). Nothing in this task edits tracked files — this is scratch infrastructure.

1. **Preflight.** Record `claude --version` (must be pinned for the whole run; live at authoring: `2.1.207`). Disable auto-update for trial invocations by setting `DISABLE_AUTOUPDATER=1` in the trial environment. Confirm Keychain auth reaches scratch trees with one throwaway run: `CLAUDE_CONFIG_DIR=$(mktemp -d) claude -p "reply with exactly: ok"` (the 2026-07-12 delivery probe showed auth survives; re-confirm on this machine today). Also export `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` for every trial (unconditional-input surface, per the design's Environment surfaces bullet).
2. **Instruction replica.** Author one replica file used by both trees: take the current `~/.claude/CLAUDE.md` content, change the first heading to `# Global Instructions — Replica`, and remove the entire `## Behavior Contracts` section (it points at this repo's charter and would confound trials; its removal also supplies the distinctive-absent host phrase). The distinctive host phrase for canary checks is: `consult ~/.agents/docs/agents/charter.md` — present in the host file (where the path is backtick-wrapped, so any literal-match check against the host must use the backtick form; the model-answered canary question below is unaffected), absent from the replica. The ON tree's replica additionally contains the Task-2 final `## Skill Use` block inserted after the `## Working` section; the OFF tree's replica lacks it; the two replicas are otherwise byte-identical (verify: `diff <(grep -v -F "$(sed -n '/## Skill Use/,/^## /p' ...)")` — practically, construct OFF first, then produce ON by one insertion, and diff to confirm the delta is exactly the block).
3. **Scratch trees.** Build `trees/tree-A/` and `trees/tree-B/` (neutral names). Each contains: `CLAUDE.md` (the arm's replica), `settings.json` with `{"disableClaudeAiConnectors": true}` and no hooks (the production skill-usage ledger hook is deliberately excluded — it writes to the `$HOME`-keyed live ledger the 2026-08-01 watch reads; takes come from each trial's own `tool_use` stream), and `skills/` containing **copies** (not symlinks) of the pinned fixture roster, all copied from this repo at one recorded commit SHA. Fixture roster (identical in both trees, all probes): `diagnose`, `tdd`, `keep-green`, `characterization-tests`, `test-trust-audit`, `simplify-code`, `authorization-design`, `injection-safe-inputs`, `red-team`, `making-recommendations`, `ideate`. Exception, per the design's single-variable rule: both trees' `diagnose` copy carries the planned body exit to `tdd` (draft the Task-12 diagnose edit early, apply it identically to both trees' copies only — the repo source stays unedited until Task 12). Tar each finished tree with the tree directory as the top-level entry (`tar -cf trees/tree-A.pristine.tar -C trees tree-A` — `runner.py` extracts each trial's copy into a fresh disposable dir and expects `tree-A/…` as the tar's top level) for per-trial resets; the tar, not the tree, is the artifact trials actually execute, so both tarballs are hashed and tar↔tree identity is verified mechanically (4.9). The trees contain **no plugins** (no plugin dirs, no plugin state in the tree's `.claude.json`): the design's "identical seeded settings, skills, and skills-directory plugins" is satisfied by identical absence, the pilot's `system/init` must show no plugin-sourced entries, and the exact-roster check below is what catches host plugin or skill leakage at trial time. Fixed trial permission surface (design: "fixed permissions/tools"): every trial runs with `--permission-mode bypassPermissions`, set in `runner.py` — headless `-p` runs cannot answer permission prompts, so default-mode denials would gut the positive probes' real work (edits, test runs) and keep the seam probe from ever reaching an in-session skill completion; bypass is acceptable because each trial is confined to a disposable fixture copy and a scratch tree, and the surface is identical across arms. The pilot confirms no permission denials appear in any stream; if the pinned CLI rejects the mode in headless runs, the pre-seal fallback is an explicit allowlist in the tree `settings.json`, recorded identically. The mode is recorded in the hash and environment records (4.9/4.10) and the prereg. Then write the two roster-check inputs at the rig root. `expected-roster.json`: the JSON array of the **full** expected init roster — the eleven fixture skills plus whatever built-in entries headless mode reports — as the runtime's `system/init` event spells them, pilot-confirmed against the first pilot trial's actual init event (adjust pre-seal if the field or spellings differ). `sentinel-absent.json`: a JSON array of host-only skill names outside the fixture roster (at minimum `skill-benchmark`, `synapsis`, `work-router`) that must appear in **no** trial's init roster. `runner.py` requires exact set equality with `expected-roster.json` and zero sentinel hits (design: "the exact expected target-skill roster") — a subset check would pass silently if the host's ~90-skill library loaded instead of the tree's, since every fixture name also exists on the host, and the sentinel list guards the pilot-confirmation itself: any sentinel name in the pilot init means delivery was broken while `expected-roster.json` was being confirmed, so fix delivery rather than accepting that roster.
4. **Arm map.** Write `armmap/arm-map.json` mapping `tree-A`/`tree-B` → `ON`/`OFF` (decide by one coin flip, record it). Only `runner.py` and the executor-as-arm-map-holder read this directory; the blind scorer never does. Sealed per-trial authorization keys and negative-control overfire keys also land here as `trial-keys.json` (Task 7) — the tally derivation input.
5. **Workspace fixture.** Author `fixture/` as one small frozen project that can host every probe: a small Python service (uv layout, runnable tests) containing (a) an untested legacy module that any refactor of it would first need characterization (mid-task probe: the trial task is a refactor elsewhere whose finding reveals this module); (b) one reproducible failing behavior whose cause is not stated anywhere in the fixture (seam probe: request-time terrain routes into `diagnose`; the scored moment is `diagnose` completing and naming `tdd`); (c) a feature surface whose findings span access-control design and untrusted-input handling (composition probe: both `authorization-design` and `injection-safe-inputs`); plus material for N1 (a mid-task finding that changes nothing about what the work needs), N2 (a completed skill naming a follow-on the prompt does not authorize), and N3 (a several-concept task still owned by one skill). Write `fixture/MANIFEST.txt` listing every file with its SHA-256 (`shasum -a 256`). The fixture contains no skill names, no arm vocabulary, and no discipline vocabulary — mechanized, not just asserted: a word-bounded case-insensitive grep over `fixture/` for every fixture-roster skill name and the discipline terms (`arm`, `probe`, `trial`, `overfire`, `contract`, `skill use`) must return zero hits; record the command and output in `pilot-notes.md` and re-run it at each 4.9 hash-record pass.
6. **Runner.** Write `runner.py` — the arm-map-holding script. Complete initial implementation below; pre-seal amendments from the pilot are expected and legitimate (only post-seal surfaces freeze). Before the first Task-4.9 hash record, verify `tally` against synthetic inputs: hand-built `grades.json`/`trial-keys.json`/`schedule.json` (plus `results-index.json`/`schedule-extensions.json` where a case needs them) sets covering a 2–1 positive split, a clean 3–0, a negative overfire-differ-by-one, an ungraded non-invalid-marked trial, an invalid-marked trial with no replacement row, an invalid-marked trial whose graded replacement row is present, and the fail-closed malformed-input cases — an unknown grade event string, a grade row missing its `skill` field, a grade keyed to an unscheduled trial id, a replacement row that changes probe/task/tree/`seam_skill`, a scheduled task with no sealed key, and a probe whose tasks mix positive and negative kinds — must yield exactly the sealed EXTEND flags, key-matched pass/overfire counts, no per-arm detail while an extension is pending, a hard block (the error line and nothing else) on both incomplete cases and on every malformed-input case, and full-n aggregation on the replacement case — the pilot never exercises escalation, so this synthetic check is the only pre-seal proof the mechanical rules work:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
# runner.py — arm-map-holding trial runner for the skill-use contract probes.
# Executes the seeded, arm-interleaved schedule; resets fixture + config tree
# per trial; captures stream-json; extracts init roster and Skill takes; emits
# stripped scorer packets; derives pass/overfire from raw scorer events via the
# sealed keys and applies the sealed escalation rule mechanically.
# The scorer NEVER runs this and never reads armmap/.
# This script never deletes anything: each trial extracts/copies into fresh
# unique sup-* temp dirs; leftovers are reclaimed manually with `trash` when
# wanted — the trash-only rule holds with no carve-out.
# Fail-closed seal: `record` writes the hash record over every runtime-
# consumed artifact (pristine tars included) after proving manifest↔fixture
# and tar↔tree identity; `run` refuses to spend trials while any check or
# the record mismatches; `verify` re-checks on demand (again after batches).
import json, shutil, subprocess, sys, tarfile, tempfile, hashlib
from pathlib import Path

RIG = Path(__file__).parent
SEED = 20260712  # recorded in the prereg; schedule is a pure function of it
MODEL = "RECORDED-IN-PREREG"  # exact --model id, fixed for every trial
PERMISSION_MODE = "bypassPermissions"  # fixed trial permission surface (4.3); in the prereg record
ENV = {"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "DISABLE_AUTOUPDATER": "1"}

def load_schedule(pilot: bool = False) -> list:
    if pilot:
        return json.loads((RIG / "pilot-schedule.json").read_text())
    sched = json.loads((RIG / "schedule.json").read_text())
    ext = RIG / "schedule-extensions.json"  # derived rows only (Task 4.7 rule)
    if ext.exists():
        sched += json.loads(ext.read_text())
    return sched

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def hash_inventory() -> dict:
    """Every runtime-consumed artifact, rig-relative: the pristine tarballs
    and all tree files, every fixture and task file, this script, the sealed
    schedule and roster inputs, the arm map, and (once sealed) the keys."""
    files = [RIG / "runner.py", RIG / "schedule.json",
             RIG / "expected-roster.json", RIG / "sentinel-absent.json",
             RIG / "armmap" / "arm-map.json"]
    if (RIG / "armmap" / "trial-keys.json").exists():
        files.append(RIG / "armmap" / "trial-keys.json")
    for sub in ("trees", "fixture", "tasks"):
        files += [p for p in sorted((RIG / sub).rglob("*")) if p.is_file()]
    return {str(p.relative_to(RIG)): sha256(p) for p in files}

def verify_fixture_manifest() -> None:
    """MANIFEST.txt must equal the live fixture exactly (`shasum -a 256`
    lines, paths relative to fixture/) — hashing the manifest alone would
    let a fixture file drift underneath it."""
    listed = {}
    for line in (RIG / "fixture" / "MANIFEST.txt").read_text().splitlines():
        if line.strip():
            digest, name = line.split(maxsplit=1)
            listed[name.strip().lstrip("./")] = digest
    live = {str(p.relative_to(RIG / "fixture")): sha256(p)
            for p in (RIG / "fixture").rglob("*")
            if p.is_file() and p.name != "MANIFEST.txt"}
    if listed != live:
        sys.exit("verify failed: fixture/MANIFEST.txt does not match live "
                 f"fixture. Got: {sorted(set(listed) ^ set(live)) or 'digest drift'}")

def verify_tars() -> None:
    """Each pristine tar must expand byte-identically to its source tree —
    the tar, not the tree, is what trials execute."""
    for name in ("tree-A", "tree-B"):
        tmp = Path(tempfile.mkdtemp(prefix="sup-tarcheck-"))
        with tarfile.open(RIG / "trees" / f"{name}.pristine.tar") as t:
            t.extractall(tmp, filter="data")
        src, out = RIG / "trees" / name, tmp / name
        want = {str(p.relative_to(src)): sha256(p)
                for p in src.rglob("*") if p.is_file()}
        got = {str(p.relative_to(out)): sha256(p)
               for p in out.rglob("*") if p.is_file()}
        if want != got:
            sys.exit(f"verify failed: {name}.pristine.tar does not match "
                     f"trees/{name}. Got: {sorted(set(want) ^ set(got)) or 'digest drift'}")

def runtime_identity() -> dict:
    v = subprocess.run(["claude", "--version"], capture_output=True, text=True)
    return {"claude_version": v.stdout.strip(), "model": MODEL,
            "permission_mode": PERMISSION_MODE, "env": ENV}

def record_hashes() -> None:
    verify_fixture_manifest()
    verify_tars()
    (RIG / "armmap" / "hash-record.json").write_text(json.dumps(
        {"hashes": hash_inventory(), "runtime": runtime_identity()}, indent=2))
    print("recorded: armmap/hash-record.json")

def verify_sealed_inputs() -> None:
    """Hard gate before any trial spends; re-run after each batch. A mismatch
    invalidates the run (not a contract failure): pre-seal, amend deliberately
    and re-record; post-seal, abort and report."""
    rec = json.loads((RIG / "armmap" / "hash-record.json").read_text())
    verify_fixture_manifest()
    verify_tars()
    live = hash_inventory()
    if rec["hashes"] != live:
        drift = sorted({k for k, _ in set(rec["hashes"].items()) ^ set(live.items())})
        sys.exit(f"verify failed: hash record mismatch. Got: {drift}")
    if rec["runtime"] != runtime_identity():
        sys.exit(f"verify failed: runtime identity changed. Got: {runtime_identity()}")

def reset_tree(tree_name: str) -> Path:
    """Fresh unique extraction per call — no pre-run deletion exists to need."""
    dest = Path(tempfile.mkdtemp(prefix=f"sup-tree-{tree_name}-"))
    with tarfile.open(RIG / "trees" / f"{tree_name}.pristine.tar") as t:
        t.extractall(dest, filter="data")
    return dest / tree_name

def reset_fixture() -> Path:
    work = Path(tempfile.mkdtemp(prefix="sup-fixture-"))
    shutil.copytree(RIG / "fixture", work / "fixture", dirs_exist_ok=True)
    return work / "fixture"

def run_trial(trial: dict) -> dict:
    tree = reset_tree(trial["tree"])
    cwd = reset_fixture()
    prompt = (RIG / "tasks" / f"{trial['task_id']}.txt").read_text()
    out_path = RIG / "out" / f"{trial['trial_id']}.jsonl"
    out_path.parent.mkdir(exist_ok=True)
    env = {**dict(__import__('os').environ), **ENV, "CLAUDE_CONFIG_DIR": str(tree)}
    with out_path.open("w") as out:
        r = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "stream-json",
             "--verbose", "--model", MODEL, "--permission-mode", PERMISSION_MODE],
            cwd=cwd, env=env, stdout=out, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        return {"trial": trial, "valid": False,
                "why": f"claude -p failed: {r.stderr[:300]}"}
    events = [json.loads(l) for l in out_path.read_text().splitlines() if l.strip()]
    init = next((e for e in events if e.get("type") == "system"
                 and e.get("subtype") == "init"), None)
    expected = set(json.loads((RIG / "expected-roster.json").read_text()))
    sentinels = set(json.loads((RIG / "sentinel-absent.json").read_text()))
    got = set()
    if init:
        got = {s for s in init.get("skills", init.get("tools", []))
               if isinstance(s, str)}
    # Exact equality plus host-only sentinel absence (design: "the exact
    # expected target-skill roster"): a subset check passes silently when the
    # host's ~90-skill library loads instead of the tree's, because every
    # fixture skill name also exists on the host.
    roster_ok = (init is not None and got == expected
                 and not (got & sentinels))
    skill_uses = [b for e in events if e.get("type") == "assistant"
                  for b in e.get("message", {}).get("content", [])
                  if isinstance(b, dict) and b.get("type") == "tool_use"
                  and b.get("name") == "Skill"]
    takes = [b.get("input", {}).get("skill") or b.get("input", {}).get("name")
             for b in skill_uses]
    # Seam-reach check (design rule, mechanized; seam probe AND N2): a trial
    # where the row's seam_skill never completes in-session never presents
    # the scored moment — invalid, re-run, symmetric across arms. Completion
    # = the take's tool_result came back without error; names match
    # suffix-aware (namespaced keys are a library-general hazard).
    ok_ids = {b.get("tool_use_id") for e in events if e.get("type") == "user"
              for b in e.get("message", {}).get("content", [])
              if isinstance(b, dict) and b.get("type") == "tool_result"
              and not b.get("is_error")}
    completed = {(b.get("input", {}).get("skill") or b.get("input", {}).get("name"))
                 for b in skill_uses if b.get("id") in ok_ids}
    seam = trial.get("seam_skill")
    seam_ok = seam is None or any(
        s and (s == seam or s.endswith(f":{seam}")) for s in completed)
    valid = roster_ok and seam_ok
    why = (None if valid else
           "roster/init mismatch — invalid, re-run" if not roster_ok else
           f"seam skill {seam} never completed in-session — invalid, re-run")
    return {"trial": trial, "valid": valid, "takes": takes, "why": why}

def merge_results(new: list) -> None:
    """Merge into results-index.json by trial_id — never wholesale-overwrite:
    existing entries (and their sealed streams) stand when re-run or extension
    rows execute later."""
    idx_path = RIG / "out" / "results-index.json"
    idx = {r["trial"]["trial_id"]: r for r in
           (json.loads(idx_path.read_text()) if idx_path.exists() else [])}
    for r in new:
        idx[r["trial"]["trial_id"]] = r
    idx_path.write_text(json.dumps(
        sorted(idx.values(), key=lambda r: r["trial"]["trial_id"]), indent=2))

def packets() -> None:
    """Emit the stripped scorer packets: final text + mechanical takes under
    neutral trial ids ONLY — no tree names, no raw streams, no arm map. The
    scorer reads these files and nothing else."""
    results = json.loads((RIG / "out" / "results-index.json").read_text())
    pdir = RIG / "out" / "packets"
    pdir.mkdir(exist_ok=True)
    for r in results:
        if not r.get("valid") or r["trial"]["trial_id"].startswith("pilot-"):
            continue  # pilot outputs never enter sealed scoring
        tid = r["trial"]["trial_id"]
        events = [json.loads(l) for l in
                  (RIG / "out" / f"{tid}.jsonl").read_text().splitlines() if l.strip()]
        final = next((e.get("result", "") for e in reversed(events)
                      if e.get("type") == "result"), "")
        (pdir / f"{tid}.json").write_text(json.dumps(
            {"trial_id": tid, "final_text": final, "takes": r["takes"]}, indent=2))

def tally(grades_path: Path) -> None:
    """Derive pass/overfire from the scorer's RAW events via the sealed keys,
    then apply the sealed escalation rule mechanically — EXTEND flags print
    before any per-arm detail. grades.json (scorer output, events only):
    {trial_id: {"event": "take"|"offer"|"none", "skill": <named-or-null>}}.
    The scorer never emits pass/overfire; it cannot — the keys are sealed.
    armmap/trial-keys.json (sealed at Task 7, never scorer-readable) is keyed
    by TASK id — keys derive from each task prompt's own authorization
    language, so derived re-run/extension rows of the same task inherit them:
    {task_id: {"kind": "positive"|"negative", "pass_event": "take"|"offer",
               "overfire": [[event, skill-or-null], ...]}}"""
    grades = json.loads(grades_path.read_text())
    armmap = json.loads((RIG / "armmap" / "arm-map.json").read_text())
    keys = json.loads((RIG / "armmap" / "trial-keys.json").read_text())
    sched = load_schedule()
    ridx = {r["trial"]["trial_id"]: r for r in
            json.loads((RIG / "out" / "results-index.json").read_text())}
    # Fail-closed input validation: grades and schedule must match the sealed
    # shape exactly before anything is counted — an unknown value must block,
    # never silently become a failure or a non-overfire.
    EVENTS = {"take", "offer", "none"}
    sched_ids = {t["trial_id"] for t in sched}
    if (unknown := sorted(set(grades) - sched_ids)):
        sys.exit(f"tally blocked: grades for unscheduled trials: {unknown}")
    if (bad := sorted(tid for tid, g in grades.items()
                      if not isinstance(g, dict) or g.get("event") not in EVENTS
                      or "skill" not in g
                      or not (g["skill"] is None or isinstance(g["skill"], str)))):
        sys.exit(f"tally blocked: malformed grade rows: {bad}")
    if (nokey := sorted({t["task_id"] for t in sched} - set(keys))):
        sys.exit(f"tally blocked: no sealed key for tasks: {nokey}")
    if (badkind := sorted(k for k, v in keys.items()
                          if v.get("kind") not in ("positive", "negative"))):
        sys.exit(f"tally blocked: keys with unknown kind: {badkind}")
    if (badtree := sorted({t["tree"] for t in sched} - set(armmap))):
        sys.exit(f"tally blocked: scheduled trees missing from arm map: {badtree}")
    by_id = {t["trial_id"]: t for t in sched}
    if (badrep := sorted(
            t["trial_id"] for t in sched if t.get("replaces") and (
                t["replaces"] not in by_id or any(
                    t.get(f) != by_id[t["replaces"]].get(f)
                    for f in ("probe", "task_id", "tree", "seam_skill"))))):
        sys.exit("tally blocked: replacement rows replacing unknown trials or "
                 f"changing probe/task/tree/seam_skill: {badrep}")
    probe_kinds = {}
    for t in sched:
        probe_kinds.setdefault(t["probe"], set()).add(keys[t["task_id"]]["kind"])
    if (mixed := sorted(p for p, ks in probe_kinds.items() if len(ks) > 1)):
        sys.exit(f"tally blocked: probes mixing positive and negative kinds: {mixed}")
    # Hard gate: NOTHING prints until every scheduled trial carries a grade or
    # an explicit invalid marker, and every invalid row has a replacement row.
    # A silent skip lands an arm at n!=3, the escalation check passes over it,
    # and per-arm detail would print with the sealed extend-before-unblinding
    # rule never consulted — premature unblinding on a mundane bookkeeping gap.
    ungraded = [t["trial_id"] for t in sched
                if grades.get(t["trial_id"]) is None
                and ridx.get(t["trial_id"], {}).get("valid", True)]
    if ungraded:
        sys.exit(f"tally blocked: no grade and no invalid marker for {ungraded}")
    replaced = {t.get("replaces") for t in sched if t.get("replaces")}
    dangling = [t["trial_id"] for t in sched
                if not ridx.get(t["trial_id"], {}).get("valid", True)
                and t["trial_id"] not in replaced]
    if dangling:
        sys.exit(f"tally blocked: invalid trials without replacement rows: {dangling}")
    per = {}
    for t in sched:
        g = grades.get(t["trial_id"])
        if g is None:
            continue  # explicitly-invalid row; its replacement carries the grade
        k = keys[t["task_id"]]
        if k["kind"] == "positive":
            rec = {"pass": g.get("event") == k["pass_event"], "over": False}
        else:
            rec = {"pass": False,
                   "over": [g.get("event"), g.get("skill")] in k["overfire"]}
        rec["kind"] = k["kind"]
        per.setdefault((t["probe"], armmap[t["tree"]]), []).append(rec)
    counts = {pa: {"n": len(v), "pass": sum(r["pass"] for r in v),
                   "overfire": sum(r["over"] for r in v), "kind": v[0]["kind"]}
              for pa, v in sorted(per.items())}
    # Escalation (sealed rule): positive probe — either arm split 2-1 at n=3;
    # negative probe — arms' overfire counts differ by exactly one at n=3
    # -> extend BOTH arms to 5 for that probe. Detail prints only when no
    # probe needs extension, so the flag never rides in with per-arm results.
    extend = []
    for probe in sorted({p for p, _ in counts}):
        arms = [c for (p, _), c in sorted(counts.items()) if p == probe]
        if len(arms) != 2 or any(c["n"] != 3 for c in arms):
            continue  # rule is defined at n=3 with both arms present
        if arms[0]["kind"] == "positive" and any(c["pass"] in (1, 2) for c in arms):
            extend.append(probe)
        if arms[0]["kind"] == "negative" and abs(arms[0]["overfire"] - arms[1]["overfire"]) == 1:
            extend.append(probe)
    for probe in extend:
        print(f"EXTEND: {probe} -> run both arms to 5, blind-grade only the added trials")
    if extend:
        return
    print(json.dumps({f"{p}/{a}": {"n": c["n"], "pass": c["pass"],
          "overfire": c["overfire"]} for (p, a), c in sorted(counts.items())},
          indent=2))

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "record":
        record_hashes()
    elif cmd == "verify":
        verify_sealed_inputs()
        print("OK: sealed inputs match the hash record")
    elif cmd == "reset-tree":  # canary helper — extract exactly what trials run
        print(reset_tree(sys.argv[2]))
    elif cmd == "run":
        verify_sealed_inputs()  # fail closed BEFORE any trial spends
        argv = sys.argv[2:]
        sched = load_schedule(pilot="--pilot" in argv)
        wanted = {a for a in argv if a != "--pilot"}
        if wanted:
            sched = [t for t in sched if t["trial_id"] in wanted]
        # Idempotent + selective: an existing output stream is never
        # re-executed or overwritten — sealed streams and standing grades
        # survive re-invocation; re-runs and extensions enter as NEW rows
        # (new trial ids) via schedule-extensions.json (Task 4.7 rule).
        done = {t["trial_id"] for t in sched
                if (RIG / "out" / f"{t['trial_id']}.jsonl").exists()}
        if done:
            print(f"skipping existing streams: {sorted(done)}")
        merge_results([run_trial(t) for t in sched
                       if t["trial_id"] not in done])
    elif cmd == "packets":
        packets()
    elif cmd == "tally":
        tally(RIG / "grades.json")
```

7. **Schedule.** Generate `schedule.json`: for each probe/task cell and each tree, the planned trial rows, deterministically interleaved by arm from `SEED` (e.g. seeded `random.Random(SEED).shuffle` over the cell list) so backend drift cannot correlate with arm. Row shape: `trial_id`, `probe`, `task_id`, `tree`, plus — on every seam-probe and N2 row, the two probes whose scored moment requires an in-session skill completion — `seam_skill`: the exact skill whose completion the trial must reach (`diagnose` for the seam probe; N2's terrain skill per its pilot-confirmed scenario). `runner.py` marks a `seam_skill` row invalid when that skill never completes in-session (suffix-aware take match; completion = the take's `tool_result` returns without error), so unreached-seam rows never enter scorer packets. `pilot-schedule.json` rows carry the same shape. Trial ids carry the per-cell replicate index (`…-r1`, `…-r2`, …) so derived rows extend the counter deterministically. Regenerated only if the prereg changes counts; the seed and generator line are quoted in the prereg. Derived-row rule (sealed in the Task-7 prereg, applied mechanically, never improvised): (a) *invalid re-run* — an invalidated trial is replaced by a new row with the same probe, task, and tree, the next per-cell replicate index in its `trial_id`, and a `replaces: <old_trial_id>` field; the old row keeps its invalid marker and its stream is never overwritten; (b) *escalation extension* — when `tally` prints EXTEND for a probe, both arms gain rows to n=5 for that probe, reusing the cell's task assignments, replicate indices continuing the counter, order continued from the same seeded generator. Derived rows are appended to `schedule-extensions.json` only — the sealed `schedule.json` and its hash stay untouched — and executed selectively (`runner.py run <new trial ids>`). Sealed keys need no per-row additions: `trial-keys.json` is keyed by `task_id`, so derived rows inherit their task's key.
8. **Effective-load canary (per tree, arm-map holder only, never the scorer).** Run the canary against a freshly tar-extracted copy — the artifact trials actually execute — never against `trees/<tree>` directly (which would pass on a stale tar and also lets the CLI write session state into the source tree). For each tree: `CLAUDE_CONFIG_DIR="$(python3 runner.py reset-tree <tree>)" claude -p "Quote, byte-exact, the first markdown heading of your user-global instruction memory. Then answer YES or NO: does a section titled 'Skill Use' appear in it? Then answer YES or NO: does the phrase 'consult ~/.agents/docs/agents/charter.md' appear in it?" --model <pinned>`. Required: heading byte-matches `# Global Instructions — Replica`; host phrase NO in both; `## Skill Use` YES in the ON tree and NO in the OFF tree. A failure blocks all trials in that tree. Run before the pilot and again immediately before sealed runs.
9. **Hash record (mechanical, fail-closed).** Before the pilot and again before sealed runs, run `python3 runner.py record`. It refuses to write unless `fixture/MANIFEST.txt` matches the live fixture contents exactly and each pristine tar expands byte-identically to its source tree, then writes `armmap/hash-record.json` covering every runtime-consumed artifact: both pristine tarballs and every file under `trees/` (replicas, skills, settings), every fixture file, every task file, `runner.py`, `schedule.json`, `expected-roster.json`, `sentinel-absent.json`, `armmap/arm-map.json` (and `armmap/trial-keys.json` once Task 7 seals it); plus `claude --version` output, the model id, the trial permission mode, and the trial environment variable set. `runner.py run` re-runs both integrity checks and re-verifies the whole record before spending any trial, hard-stopping on any mismatch; `python3 runner.py verify` re-checks on demand and is re-run after each batch before grading. A mismatch invalidates the run (not a contract failure): pre-seal, amend deliberately and re-record; post-seal, abort and report.
10. **Environment surfaces record.** In a sibling `armmap/environment-record.json` (executor-maintained — `runner.py record` owns and overwrites `hash-record.json`, so the two never clobber each other) record: auto-memory disabled (env var), connectors suppressed (confirm absent in the pilot's `system/init`), managed/server-managed settings presence on this host (`ls /Library/Application\ Support/ClaudeCode/ 2>/dev/null; ls ~/Library/Application\ Support/ClaudeCode/managed-settings.json 2>/dev/null` — record presence/absence and hashes), the auth method (Keychain), the trial permission mode (`bypassPermissions`), and the invoking-shell surface: run `runner.py` from a plain terminal, never from inside a Claude or Codex session — trials inherit the invoking process environment (arm-symmetric either way, but it belongs in the record; capture the names of any `CLAUDE*`/`CODEX*` variables present at run time).

## Task 5 — Author trial tasks fresh-context (feeds Task 6)

Trial prompts must not be authored by this session or any context that has read this plan or the design (the Era-86 lesson: 4 of 6 first-draft prompts leaked discipline vocabulary; regenerate, never hand-patch).

1. For each of the six probes (3 positive, 3 negative), write a **facts-only kernel**: what the fixture is, what the user in the scenario wants, what state exists — zero skill names, zero expectations, zero arm/discipline vocabulary. The kernel for the seam probe describes only the failing behavior a user would report; the mid-task kernel only the refactor ask; N1–N3 kernels only their neutral scenarios.
2. Spawn a fresh subagent per prompt with ONLY the kernel and the instruction "write the user message this person would send to a coding agent working in this project" — no plan, no design, no probe taxonomy in its context. Fresh means a default named/general-purpose spawn, which starts context-isolated by documented default (a subagent gets a fresh context window and none of the parent conversation); never the `fork` subagent type or `/fork`, which inherits the whole conversation. The same isolation rule binds the step-3 reviewer and the Task-8 scorer; the mechanism and active tool contract are recorded in the prereg (Task 7.1, blinding).
3. Adversarially review each returned prompt (a second fresh subagent may do this): reject and regenerate on any leak of expected skill names, assertions, arm identity, intended answers, or authorization ambiguity (seam prompts must be unambiguous between take-authorized and offer-only readings — that wording is what the sealed per-trial authorization key derives from). Save accepted prompts as `tasks/<task_id>.txt`; write separate pilot-only tasks the same way (pilot tasks and outputs are excluded from sealed scoring).
4. Update the hash record.

## Task 6 — Unsealed paired pilot (step 4)

1. Run the effective-load canary (Task 4.8). Then run the pilot: for every probe, positive and negative, a cheap paired run (1–2 trials per arm per probe) using the pilot-only tasks, via `runner.py run --pilot` against `pilot-schedule.json` (pilot trial ids carry a `pilot-` prefix so they can never collide with sealed rows or enter sealed packets).
2. Confirm per channel: the exact roster check passes with zero sentinel hits (a sentinel hit means delivery is broken — fix delivery before confirming `expected-roster.json`) and no permission denials appear in the stream; the observable event is extractable (takes mechanically from `tool_use`; offers gradeable from final text); the scoring key is unambiguous; the OFF-arm base rate leaves headroom (no ceiling); for the seam probe, both arms reliably reach an in-session skill completion at all (a trial where no skill completes never reaches the seam — invalid, re-run, symmetric across arms), and the runner's mechanical `seam_skill` detection (Task 4.7) fires correctly against the pilot's seam and N2 streams — adapt the completion parsing pre-seal if the `tool_result` shape differs; for each negative probe, the scenario is unambiguously gradeable and the OFF-arm overfire base rate is measured.
3. Resolve every empty, ambiguous, or ceilinged channel by redesign (fixture, kernel regeneration, or observable-rule sharpening) — or drop a **positive** channel to characterization-only with that recorded. The negative calibration gate cannot be waived or dropped: a negative channel still ambiguous after redesign leaves the gate unmet and blocks GO (design, Negative controls).
4. Record pilot outcomes (per channel: fired/empty/ambiguous/ceiling, base rates, redesigns made) in a `pilot-notes.md` inside the rig. Pilot tasks and outputs never enter sealed scoring.

## Task 7 — Preregistration, adversarial review, seal (step 5)

1. Write `docs/plans/2026-07-NN-skill-use-probes-preregistration.md` following the sealed shape of [`2026-07-10-skill-value-test-preregistration.md`](2026-07-10-skill-value-test-preregistration.md) (frontmatter with `type: pre-registration`, status line, append-only-below-seal rule). Contents, all fixed before any sealed data: the question; the two arms (byte-identical replicas ± the Task-2 block, quoted); the fresh sealed task texts; the fixture manifest hash; the pinned roster and skill-copy commit SHA; `claude --version` and the exact model id; the full hash record; the environment-surfaces record; the observable scoring rules (take = a `tool_use` block naming the exact target Skill; offer = the response explicitly names the target invocation token and proposes a clear handoff — generic suggestions do not count); the per-trial authorization keys derived from each seam/N2 prompt's own authorization language; the negative-control overfire keys (which takes/continuations count as overfire per N1/N2/N3), both key sets recorded as `armmap/trial-keys.json`; the seeded schedule (seed, generator, and the emitted order); the derived-row rule (Task 4.7: invalid re-run and escalation-extension rows, id/replicate/key derivation, `schedule-extensions.json`-only appends); the fixed trial permission mode; trial counts (3/arm/probe) and the escalation rule (either arm splits 2–1 on a positive probe, or negative-probe overfire counts differ by exactly one → extend both arms to 5 for that probe before unblinding; first-round grades stand; the scorer blind-grades only added trials; the scorer's escalation inference is an accepted bounded leak); pass criteria (positive: with-arm ≥2/3 and strictly exceeds without-arm; post-escalation ≥4/5 and strictly exceeds); the ceiling rule (a sealed without-arm ceiling is inconclusive-by-ceiling, never a pass); the calibration gate (at final counts, ON overfire ≤ OFF overfire on every negative probe; an ON excess returns the corresponding clause and the combined block for redesign); aggregation (GO requires all three positive probes to pass AND the gate to hold; fail/inconclusive returns the affected clause and the combined block; other probes' results retained as bounded evidence only); blinding (neutral names, arm map outside trial-visible paths, scorer blind to arm, artifact leak inspection before unblinding, and the subagent-isolation mechanism for every blind role — prompt authors, prompt reviewers, scorer: default context-isolated spawns with the active harness and tool contract named, `fork`-type spawns banned); and the honest bound (Claude-side, same-model-scored — quote the design's weighting line).
2. Obtain an adversarial design review of the prereg — run `review-family:scrutinize` against it with the methodology's design-panel questions (any verdict pre-ordained? any gate unreachable? any divergence cell forbidden by construction? is the motivating premise true?). Patch before data if needed.
3. Commit the prereg. That commit SHA is the seal. From here: no edits above the seal line, no post-hoc adjustment, no reuse of pilot outputs.

## Task 8 — Sealed probe runs (step 6)

1. Re-run the effective-load canary per tree (against freshly extracted run trees, per Task 4.8) and `python3 runner.py verify`; `runner.py run` re-verifies the sealed inputs itself and refuses to spend any trial on a mismatch.
2. Execute exactly the sealed schedule: `python3 .agents/scratch/skill-use-probes/runner.py run` (the executor acts as arm-map holder; re-invocation is safe — existing streams are never re-executed or overwritten). Invalid trials (roster/init mismatch; in-session seam never reached, detected mechanically via the row's `seam_skill` — seam probe and N2 alike; CLI version change) are re-run symmetrically as replacement rows per the sealed Task-4.7 derived-row rule (`runner.py run <new trial ids>`) and invalidity rates reported; a mid-run `claude` version change invalidates the affected trials.
3. Blind grading: first re-run `python3 runner.py verify` (a post-batch mismatch invalidates the affected trials before any grading), then emit the stripped per-trial packets with `python3 runner.py packets` (final text plus the mechanical takes list under neutral trial ids — no tree names, no raw streams, no arm map) and hand the scorer (a fresh subagent under the Task-5 isolation rule: default context-isolated spawn, never `fork`-type) only those packets and the sealed observable rules. The scorer returns `grades.json` as raw events (`take`/`offer`/`none` plus the named skill) — never pass/overfire, which derive from the sealed keys at tally. Inspect the packets for arm/intent leaks before unblinding.
4. `python3 runner.py tally` derives pass/overfire via the sealed keys and applies the escalation rule, printing EXTEND flags before any per-arm detail — and printing nothing at all while any scheduled trial lacks a grade or an explicit invalid-with-replacement marker; if escalation fires, append the extension rows per the sealed Task-4.7 derived-row rule, run only those (`runner.py run <added trial ids>`), blind-grade only those, re-tally, then unblind.
5. Record in an appendix below the prereg seal line: raw per-trial grades, validity log, escalations, unblinded per-arm results, the verdict per probe, the calibration-gate result, and the bounded interpretation (Claude-side, same-model-scored). Commit.
6. Outcome routing: all three positive probes pass AND the gate holds → proceed to Task 9 with a probe-backed GO recommendation. Any fail/inconclusive/gate-breach → stop, report to JP with the affected clause named; the design returns that clause and the combined block for redesign (a true silence fail returns bullet 1). Do not proceed to Task 9 with a NO-GO-shaped result unless JP directs otherwise.

## Task 9 — Charter Admission consult + JP ratification (step 7; Gate 2)

1. Run the Admission consult against `docs/agents/charter.md` for the two decisions as distinct adjudications (one consult may cover both): **Decision A** (runtime `## Skill Use` contract in both user-global files) and **Decision B** (repo `AGENTS.md` convention line). The design's Charter Package section already drafts Q1–Q3 for each; the consult re-answers them against the now-existing probe evidence, the subagent-exposure pricing, and the request-time-overlap adjudication (fixed-terrain reinforcement, or the Task-3 fallback state).
2. Present to JP: the consult's per-decision recommendation, the sealed probe results, and the open ratification question. Record JP's separate GO/NO-GO per decision in `## Build Records`.
3. A NO-GO on either decision stops that decision's landing tasks (Task 10 for A; Task 11 for B); the other may proceed if independently GO. Commit the record.

## Task 10 — Land Decision A: global files + drift canary (step 8; only after A-GO)

1. Insert the Task-2 final `## Skill Use` block into `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, in both files immediately after the `## Behavior Contracts` section, byte-identically (verify: extract both sections and `diff` them — zero delta).
2. Create `scripts/check-skill-use-contract.sh` (mode `755`), following the `check-protected-set.sh` pattern but byte-exact and section-scoped:

```bash
#!/usr/bin/env bash
# check-skill-use-contract.sh — drift DETECTION for the canonical always-loaded
# "## Skill Use" contract, which must be byte-identical in both user-global
# instruction files (admitted via docs/agents/contract-decisions.md, Decision A;
# design: docs/plans/2026-07-11-skill-use-contract-design.md). CANON below is
# the single textual source: to change the wording (a gated charter change),
# edit it here AND both targets. Reach is repo-session-triggered: this runs at
# session start in .agents, so drift surfaces at the next such session.
set -euo pipefail

CANON=$(cat <<'EOF'
<the Task-2 final block, byte-exact, heading through final bullet>
EOF
)

TARGETS=("$HOME/.claude/CLAUDE.md" "$HOME/.codex/AGENTS.md")

extract() {  # print the "## Skill Use" section: heading up to the next "## " or EOF
  awk '/^## Skill Use$/{f=1} f&&/^## /&&!/^## Skill Use$/{exit} f{print}' "$1"
}

fail=0
for t in "${TARGETS[@]}"; do
  if [ ! -f "$t" ]; then echo "MISSING FILE: $t" >&2; fail=1; continue; fi
  got="$(extract "$t")"
  if [ -z "$got" ]; then echo "DRIFT: $t has no ## Skill Use section" >&2; fail=1
  elif [ "$got" != "$CANON" ]; then
    echo "DRIFT: $t ## Skill Use section is not byte-identical to CANON" >&2
    diff <(printf '%s\n' "$CANON") <(printf '%s\n' "$got") >&2 || true
    fail=1
  fi
done
[ "$fail" -ne 0 ] && { echo "Fix targets to match CANON exactly, or change CANON AND both targets (charter-gated)." >&2; exit 1; }
echo "OK: skill-use contract byte-identical across ${#TARGETS[@]} user-global files"
```

Replace the `CANON` placeholder line with the Task-2 final text before committing. The quoted heredoc is load-bearing: the contract text contains apostrophes ("don't", "skill's") that break a single-quoted assignment, and command substitution strips trailing newlines symmetrically with the `$(extract …)` side of the comparison. A trailing-newline mismatch is still the classic failure; test both directions (run it green, then temporarily perturb one file, see it fail, restore).
3. Wire the canary into all three named surfaces: append the hook entry (same shape as the five existing ones, command `/Users/jp/.agents/scripts/check-skill-use-contract.sh || true`, timeout 15, statusMessage `Checking skill-use contract drift`) to the `SessionStart` hook arrays in **both** `.codex/hooks.json` (tracked) and `.claude/settings.local.json` (untracked), and add the same entry to the recovery-recipe heredoc in the `claude-skills-sync.sh` header comment (so losing the ignored Claude settings does not silently remove the check).
4. Verify: run the script directly (green), then start-of-session behavior via `bash -n` on the script and a JSON parse of both hook files (`python3 -m json.tool`).
5. Commit the tracked surfaces: `scripts/check-skill-use-contract.sh`, `.codex/hooks.json`, `scripts/claude-skills-sync.sh`.

## Task 11 — Land Decision B: the convention line (step 9; only after B-GO)

Add one bullet to `AGENTS.md`, in the `## Skill Editing` section's `SKILL.md:` list (after the description-budget bullet):

```markdown
- When a skill's work has a natural upstream or downstream lane, name the handoff in the body — an exits line or section, phrased availability-conditionally for single-runtime lanes — and add it to the description only when selection-critical. Whether a handoff relationship belongs in the skill at all stays `agent-facing-design`'s judgment; this line fixes only where an already-decided handoff is written.
```

Commit (`AGENTS.md` only).

## Task 12 — Seed the Class-A data layer (step 10)

Nine body edits + one description edit, recomputed per the committed census. Receiving-side skills need no edits. Every edit is build-and-prune (no charter event). Text below is the plan's draft; hold each to the surrounding skill's voice and the repo's dual-runtime token convention while landing, without weakening the named handoff.

1. `skills/diagnose/SKILL.md` — body exit to `tdd`. Insert at the start of Phase 5, before "Write the regression test **before the fix**…" (line 121):

```markdown
The cause is known now, so locking the fix in test-first belongs to `/tdd` (or `$tdd`) — hand it the minimised repro as the RED reproduction; its known-cause bug path picks up exactly here. The steps below are the inline minimum when that handoff is declined or the fix is trivial.
```

2. `skills/tdd/SKILL.md` — body exit to `keep-green`. Append to the Closure checklist (after the full-suite bullet, line 113):

```markdown
- [ ] If the full-suite run is red from your changes and the fix is not simply the current RED→GREEN cycle, hand off to `/keep-green` (or `$keep-green`) to drive it back to green without thrashing.
```

3. `skills/test-trust-audit/SKILL.md` — body exit to `characterization-tests`. Extend the Output routing sentence (line 50) so it ends:

```markdown
Route the fixes out: authoring-time fixes to `tdd`; per-finding tracker items to `/triage` (or `$triage`) where available; and when the sweep shows the suite cannot be trusted to guard an imminent refactor, upgrade, or migration, hand forward to `/characterization-tests` (or `$characterization-tests`) to author the net that work needs first.
```

4. `skills/red-team/SKILL.md` — parallel fan-out exit. Add a bullet to "The close" (after the `/triage` routing bullet, line 41):

```markdown
- **Compose forward when paths land on a designable surface.** Hand attack paths to `/authorization-design` (or `$authorization-design`) as must-deny rows and to `/injection-safe-inputs` (or `$injection-safe-inputs`) as must-block rows — one or both as the findings warrant, sequentially or concurrently; composition is not a license for subagent fan-out.
```

5. `skills/postmortem/SKILL.md` — body exit to `runbook-authoring`. Add to Beat 3, inserted immediately **before** the `/triage` bullet (line 52), never after it: that bullet ends with an explicit "and stop", the contract's precedence clause makes a governing skill's stop controlling, and Task 13.1 smoke-tests exactly this chain — the route must precede the stop:

```markdown
- When an action item is an operational procedure someone will re-run — a rollback, restart, failover, alert response — hand authoring it to `/runbook-authoring` (or `$runbook-authoring`) rather than leaving the procedure inline in the doc.
```

6. `skills/observability-instrumentation/SKILL.md` — body exit to `deploy-plan`. Add to "Done when" (after the final bullet, line 58):

```markdown
- When the instrumented change ships as a risky rollout, hand forward to `/deploy-plan` (or `$deploy-plan`) — the signals just laid down are the gauge it pre-registers and reads.
```

7. `skills/deploy-plan/SKILL.md` — body exit to `outcome-check`. Append to the "After push" list (after the advisory-not-actor bullet, line 34):

```markdown
- **Healthy is not goal-met** — a `healthy` bake-read closes only the technical question; whether the change achieved the goal it shipped for is a later, different read: hand forward to `/outcome-check` (or `$outcome-check`) at the goal's horizon.
```

8. `plugins/review-family/skills/scrutinize-skill/SKILL.md` — body exit to `behavior-smoke-test` (source-only; Class-B publish deferred until JP's ask — from this edit until that ask, the SessionStart `codex-plugins-sync.sh --check` canary reports `DRIFT: review-family`, an expected state per the standing gate, never to be repaired by publishing). Append to the Output section, after the "Findings are argued hypotheses…" paragraph (line 98):

```markdown
When the review's required changes have been applied and the open claim becomes "the changed contract is now followed," proving that is `behavior-smoke-test`'s job (`/behavior-smoke-test` or `$behavior-smoke-test` where available), not a re-review.
```

9. `skills/behavior-smoke-test/SKILL.md` — availability-conditional exit to `skill-benchmark` (Claude-only). Append to the Results section (after line 125):

```markdown
When a passed smoke test raises the quantitative question — pass rates, token or time deltas across repeated trials — that is `skill-benchmark`'s job where available (Claude Code: `/skill-benchmark`); a smoke test proves followership once, never a rate.
```

10. `skills/making-recommendations/SKILL.md` — description edit (selection-critical per the observed miss). In the frontmatter description, replace the final clause `when no concrete options are named yet, clarifying a muddy goal is `outcome-shaping` and shaping a design is `design-exploration`.` with:

```text
when no concrete options are named yet, clarifying a muddy goal is `outcome-shaping` and shaping a design is `design-exploration`; when the field is too thin to rank — no serious rivals on the table — widening it first is `ideate`.
```

11. Pre-commit checks, inline: run `python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py` on each of the ten skill dirs (the known "unexpected key" false positive on documented-valid fields is accepted; anything else is real), then `git diff --check`. Fix failures, then commit the ten files in one commit (`feat(skills): seed skill-use composition exits per approved design`). Task 15 re-runs the full ladder across all edited surfaces.

## Task 13 — Data-layer behavior proof (step 11)

Run and record the representative matrix as `docs/smoke-tests/2026-07-NN-skill-use-data-layer-matrix.md` — a target-to-scenario coverage table naming every touched skill (`diagnose`, `tdd`, `test-trust-audit`, `red-team`, `postmortem`, `observability-instrumentation`, `deploy-plan`, `behavior-smoke-test`, `scrutinize-skill`, `making-recommendations`) with its scenario or an explicit impracticality justification, plus prompts/commands, outcomes, and proof limits. Use the `behavior-smoke-test` skill's harness discipline (fresh context-isolated subagent proxies; scenario forces the choice; proxy never grades itself). Required coverage, from the design:

1. Sequential exits exercised: `diagnose`→`tdd`→`keep-green`; `test-trust-audit`→`characterization-tests`→`simplify-code`; `postmortem`→`runbook-authoring`; `observability-instrumentation`→`deploy-plan`→`outcome-check`.
2. Permissioned offer shown: a handoff offered rather than taken when the request or governing skill stops continuation.
3. Parallel composition exercised: `red-team`→`authorization-design`+`injection-safe-inputs`, without automatic agent fan-out.
4. Runtime-conditional exits verified: the chain-7 wording names Claude-only skills only when available and creates no false Codex route (inspect the landed text + one Codex-side read where practical).
5. Description trigger tested: `making-recommendations` thin-field→`ideate` against should-trigger and nearby should-not-trigger prompts.
6. Plugin-distributed behavior: test `scrutinize-skill` at source; cache/mirror claims stay separate and unmade (Class-B deferred).

A parse, integrity check, delivery check, or cache check cannot substitute for these observations. Commit the matrix doc.

## Task 14 — Decision ledger entries (step 12)

Append to `docs/agents/contract-decisions.md` (append-only; match the existing entry shape in the Decisions section): one entry for Decision A (admission of the `## Skill Use` runtime contract; cite the design doc path + approval/landing commits, the sealed prereg SHA, the probe results appendix, JP's ratification record, and the canary script) and one for Decision B (admission of the `AGENTS.md` convention line; cite the design doc and landing commit). If either was NO-GO, the entry records the rejection/park with its evidence pointer instead. Commit.

## Task 15 — Validation ladder + triage filing (steps 13–14)

1. File the pre-existing global-file drift via the `triage` skill: one issue in `jpsweeney97/agents` stating specifically that `~/.codex/AGENTS.md`'s `## Behavior Contracts` section is missing the capability carve-out clause present in `~/.claude/CLAUDE.md` ("bar one capability carve-out … authoring a skill that can fire unattended or wields irreversible-effect tools (the carve-out)"), with the fix routed to a normal editing session. This is deliberately not folded into the contract landing.
2. Structural ladder on the exact edited surfaces:

```bash
for s in diagnose tdd test-trust-audit red-team postmortem observability-instrumentation deploy-plan behavior-smoke-test making-recommendations; do python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/$s; done
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/review-family/skills/scrutinize-skill
bash scripts/check-library-integrity.sh
scripts/claude-skills-sync.sh --check
scripts/check-skill-use-contract.sh
git diff --check
```

Also parse both hook JSON files (`python3 -m json.tool < .codex/hooks.json`), confirm every path referenced by edited surfaces exists, and re-run any skill's `agents/openai.yaml` parse where that file exists. Treat `quick_validate.py`'s known false-positive ("unexpected key" on documented-valid fields) as accepted; any other failure is real. Structural green does not replace Task 13.
3. Failures found here are fixed and landed as a focused follow-up commit (e.g. `fix(skills): repair validation-ladder findings`); the Task 12 unit is not done until this ladder is green, including that follow-up. Never waive.

## Task 16 — Watch (step 15; record, don't act)

No action now beyond recording: the watch reads at the 2026-08-01 ledger re-read (suffix-aware matching mandatory). Pre-named trigger: unwanted mid-task fires of expensive-by-design lanes (`skill-squad`, `methodology-critique`, `synapsis`, `deep-research`). Also watch seam-handoff sequences, permissioned offers, automatic fan-out attempts, and JP corrections. Request-time silence recurrences read as terrain behavior, not contract failure. Confirm the ledger-entry text (Task 14) names this checkpoint, then close out: report branch state and remaining JP-gated residue (Class-B publish, push).

## Plan notes (self-review + outside view)

Reference class: a pre-registered, blinded ON/OFF evaluation harness plus an always-loaded contract landing, in this repo — the judgment-trust apparatus arc (tests 1–5) and the Era-86 seal are the base rate. What this class reliably required that a spec-only decomposition omits, now built in: pilot channels come back empty/ambiguous/ceilinged and force redesign loops (Task 6.3); first-draft trial prompts leak vocabulary and must be regenerated fresh, never patched (Task 5); harness mechanics (stream-json shape, auth, version drift) eat a preflight (Task 4.1, the version pin, the amendable runner); and canary scripts fail on trailing-newline byte mismatches (Task 10.2's perturb-test). Known bounds, stated rather than certified away: `runner.py`'s `system/init` roster-field name, the `tool_use`/`tool_result` shapes its takes and seam-completion checks parse, and the Codex probe's CLI flags are written against current versions and may need pre-seal adaptation; the fixture and trial prompts are constitutionally authored at build time (blind-eval discipline), so this plan fixes their required properties, not their text. The base rate is a prior, not a guarantee — this plan is debiased against the apparatus arc's failures, not certified complete.
