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
3. **Standing:** `scrutinize-skill`'s edit lands source-complete but unpublished: Task 12 bumps the `review-family` manifest version and writes the changelog entry in the same local commit as the behavior change (repo `AGENTS.md`: bump the manifest version on behavior changes — the bump is a source edit, not a publish act), while the Class-B publish train (Codex republish → mirror) and any push run only on JP's explicit ask. Expected consequence, not a failure: from the Task-12 commit until that ask, `codex-plugins-sync.sh --check` — wired into SessionStart in both `.codex/hooks.json` and `.claude/settings.local.json` — reports `NOT-INSTALLED: review-family@<new version>` at every `.agents` session start (the Codex cache is version-keyed, so a bumped-but-unpublished source reads as not-installed, not `DRIFT`). Leave it red; never "repair" it by publishing without JP's explicit ask.

## File map

Created by this plan:

- `docs/plans/2026-07-12-skill-use-contract-implementation-plan.md` — this plan.
- `.agents/scratch/skill-use-probes/` — the probe rig (git-ignored via the `.agents/` ignore rule; verified in `.gitignore`). Subdirs: `trees/` (two scratch `CLAUDE_CONFIG_DIR` trees + pristine tarballs), `fixture/` (frozen workspace fixture + manifest), `armmap/` (arm map + sealed keys + hash record + seal marker; never readable by the scorer), `tasks/` (fresh-authored trial prompts), `out/` (captured trial streams + stripped scorer packets); plus `runner.py`, `synthetic-suite.py`, `schedule.json`, `pilot-schedule.json`, `schedule-extensions.json` (runner-derived rows only, written by `runner.py extend` and equivalence-checked on every load — the sealed `schedule.json` is never edited and the extension file is never hand-edited), and the exact-roster check inputs `expected-roster.json` and `sentinel-absent.json` at the rig root.
- `docs/plans/2026-07-NN-skill-use-probes-preregistration.md` — the sealed preregistration (Task 7; `NN` = authoring date).
- `scripts/check-skill-use-contract.sh` — the byte-identity drift canary (Task 10).
- `docs/smoke-tests/2026-07-NN-skill-use-data-layer-matrix.md` — the data-layer behavior-proof coverage table (Task 13).

Modified by this plan:

- `docs/plans/2026-07-11-skill-use-contract-design.md` — gains a `## Build Records` appendix (Tasks 2, 3, 8).
- `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md` — the `## Skill Use` block (Task 10, post-GO only).
- `.codex/hooks.json` (tracked), `.claude/settings.local.json` (untracked), `scripts/claude-skills-sync.sh` header recipe — canary wiring (Task 10).
- `AGENTS.md` — one convention line in Skill Editing (Task 11, post-GO only).
- Nine `SKILL.md` bodies + one description (Task 12): `skills/diagnose`, `skills/tdd`, `skills/test-trust-audit`, `skills/red-team`, `skills/postmortem`, `skills/observability-instrumentation`, `skills/deploy-plan`, `skills/behavior-smoke-test`, `plugins/review-family/skills/scrutinize-skill`, `skills/making-recommendations` (description only).
- `plugins/review-family/.claude-plugin/plugin.json` + `plugins/review-family/CHANGELOG.md` — version bump and changelog entry for the `scrutinize-skill` behavior change (Task 12; publication stays JP-gated).
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
2. **Instruction replica.** Author one replica file used by both trees: take the current `~/.claude/CLAUDE.md` content, change the first heading to `# Global Instructions — Replica`, and remove the entire `## Behavior Contracts` section (it points at this repo's charter and would confound trials; its removal also supplies the distinctive-absent host phrase). The distinctive host phrase for canary checks is: `consult ~/.agents/docs/agents/charter.md` — present in the host file (where the path is backtick-wrapped, so any literal-match check against the host must use the backtick form; the model-answered canary question below is unaffected), absent from the replica. The ON tree's replica additionally contains the Task-2 final `## Skill Use` block inserted after the `## Working` section; the OFF tree's replica lacks it; the two replicas are otherwise byte-identical (verify: construct the OFF replica first, produce the ON replica from it by that one insertion, then `diff` the two files and confirm the only hunk is exactly the inserted block).
3. **Scratch trees.** Build `trees/tree-A/` and `trees/tree-B/` (neutral names). Each contains: `CLAUDE.md` (the arm's replica), `settings.json` with `{"disableClaudeAiConnectors": true}` and no hooks (the production skill-usage ledger hook is deliberately excluded — it writes to the `$HOME`-keyed live ledger the 2026-08-01 watch reads; takes come from each trial's own `tool_use` stream), and `skills/` containing **copies** (not symlinks) of the pinned fixture roster, all copied from this repo at one recorded commit SHA. Fixture roster (identical in both trees, all probes): `diagnose`, `tdd`, `keep-green`, `characterization-tests`, `test-trust-audit`, `simplify-code`, `authorization-design`, `injection-safe-inputs`, `red-team`, `making-recommendations`, `ideate`. Exception, per the design's single-variable rule: both trees' `diagnose` copy carries the planned body exit to `tdd` (draft the Task-12 diagnose edit early, apply it identically to both trees' copies only — the repo source stays unedited until Task 12). Tar each finished tree with the tree directory as the top-level entry (`tar -cf trees/tree-A.pristine.tar -C trees tree-A` — `runner.py` extracts each trial's copy into a fresh disposable dir and expects `tree-A/…` as the tar's top level) for per-trial resets; the tar, not the tree, is the artifact trials actually execute, so both tarballs are hashed and tar↔tree identity is verified mechanically (4.9). The trees contain **no plugins** (no plugin dirs, no plugin state in the tree's `.claude.json`): the design's "identical seeded settings, skills, and skills-directory plugins" is satisfied by identical absence, the pilot's `system/init` must show no plugin-sourced entries, and the exact-roster check below is what catches host plugin or skill leakage at trial time. Fixed trial permission surface (design: "fixed permissions/tools"): every trial runs with `--permission-mode bypassPermissions`, set in `runner.py` — headless `-p` runs cannot answer permission prompts, so default-mode denials would gut the positive probes' real work (edits, test runs) and keep the seam probe from ever reaching an in-session skill completion; bypass is acceptable because each trial is confined to a disposable fixture copy and a scratch tree, and the surface is identical across arms. The pilot confirms no permission denials appear in any stream; if the pinned CLI rejects the mode in headless runs, the pre-seal fallback is an explicit allowlist in the tree `settings.json`, recorded identically. The mode is recorded in the hash and environment records (4.9/4.10) and the prereg. Then write the two roster-check inputs at the rig root. `expected-roster.json`: the JSON array of the **full** expected init roster — the eleven fixture skills plus whatever built-in entries headless mode reports — as the runtime's `system/init` event spells them, pilot-confirmed against the first pilot trial's actual init event (adjust pre-seal if the field or spellings differ). `sentinel-absent.json`: a JSON array of host-only skill names outside the fixture roster (at minimum `skill-benchmark`, `synapsis`, `work-router`) that must appear in **no** trial's init roster; `runner.py run` refuses to spend trials while this file is empty — an accidentally emptied list would silently disarm the guard. `runner.py` requires exact set equality with `expected-roster.json` and zero sentinel hits (design: "the exact expected target-skill roster") — a subset check would pass silently if the host's ~90-skill library loaded instead of the tree's, since every fixture name also exists on the host, and the sentinel list guards the pilot-confirmation itself: any sentinel name in the pilot init means delivery was broken while `expected-roster.json` was being confirmed, so fix delivery rather than accepting that roster.
4. **Arm map.** Write `armmap/arm-map.json` mapping `tree-A`/`tree-B` → `ON`/`OFF` (decide by one coin flip, record it). Only `runner.py` and the executor-as-arm-map-holder read this directory; the blind scorer never does. Sealed per-trial authorization keys and negative-control overfire keys also land here as `trial-keys.json` (Task 7) — the tally derivation input.
5. **Workspace fixture.** Author `fixture/` as one small frozen project that can host every probe: a small Python service (uv layout, runnable tests) containing (a) an untested legacy module that any refactor of it would first need characterization (mid-task probe: the trial task is a refactor elsewhere whose finding reveals this module); (b) one reproducible failing behavior whose cause is not stated anywhere in the fixture (seam probe: request-time terrain routes into `diagnose`; the scored moment is `diagnose` completing and naming `tdd`); (c) a feature surface whose findings span access-control design and untrusted-input handling (composition probe: both `authorization-design` and `injection-safe-inputs`); plus material for N1 (a mid-task finding that changes nothing about what the work needs), N2 (a completed skill naming a follow-on the prompt does not authorize), and N3 (a several-concept task still owned by one skill). Write `fixture/MANIFEST.txt` listing every file with its SHA-256 (`shasum -a 256`). The fixture contains no skill names, no arm vocabulary, and no discipline vocabulary — mechanized, not just asserted: a word-bounded case-insensitive grep over `fixture/` for every fixture-roster skill name and the discipline terms (`arm`, `probe`, `trial`, `overfire`, `contract`, `skill use`) must return zero hits; record the command and output in `pilot-notes.md` and re-run it at each 4.9 hash-record pass.
6. **Runner.** Write `runner.py` — the arm-map-holding script. Complete initial implementation below; pre-seal amendments from the pilot are expected and legitimate (only post-seal surfaces freeze; amend the suite alongside the runner). Before the first Task-4.9 hash record, run the synthetic suite embedded after the runner (`python3 synthetic-suite.py` from the rig root; both files ran green as embedded in the 2026-07-12 patch session — re-run against the extracted copies, since transcription drift is exactly what it catches). The suite is the only pre-seal proof the mechanical rules work (the pilot never exercises escalation or the guards) and covers: exact-target scoring (a wrong-skill take never passes; namespaced and duplicate names match suffix-aware), multi-target composition cardinality (one-of-two missing or merely-mentioned fails; unexpected extra activity does not block a pass), offer-vs-take separation (a take never satisfies an offer-only target), negative overfire keys firing on takes and on offers with unlisted skills ignored, the escalation flow (2–1 split and overfire-differ-by-one EXTEND; flags and pending ids print with per-arm detail suppressed until the graded extension unblocks full n=5), derivation equivalence (invalid rows force derived replacements; chains replace replacements; hand edits — double replacements, wrong replicate indices, changed cells, unauthorized or over-extension escalation rows — block), duplicate trial ids, grades attached to invalid trials, the malformed-input blocks (bad offer shapes, the retired `{event, skill}` grade shape, unscheduled or never-run grades, missing or malformed sealed keys, mixed-kind probes, arm-map gaps, ungraded first-round trials), the sealed-id namespace and row-identity guards (pilot rows must carry the `pilot-` prefix and sealed rows must not; a results row must record exactly its scheduled row or tally and packets refuse; a stream with no matching results row hard-stops `run`, while a matching one still skips idempotently), the scorer offer-vocabulary guard (token forms like `/ideate` and case drift block), an empty sentinel file blocking `run`, and the seal and run guards (record→verify→seal→record-refused, post-seal record tamper, unknown trial ids):

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
# runner.py — arm-map-holding trial runner for the skill-use contract probes.
# Executes the seeded, arm-interleaved schedule; resets fixture + config tree
# per trial; captures stream-json; extracts init roster and Skill takes; emits
# stripped scorer packets; scores mechanically from each trial's takes list
# plus the scorer's offer grades via the sealed keys; applies the sealed
# escalation rule; and derives every post-seal schedule row itself —
# replacement and escalation rows are pure functions of sealed inputs, and
# run/tally refuse to proceed unless schedule-extensions.json equals that
# derivation exactly. The scorer NEVER runs this and never reads armmap/.
# This script never deletes anything: each trial extracts/copies into fresh
# unique sup-* temp dirs; leftovers are reclaimed manually with `trash` when
# wanted — the trash-only rule holds with no carve-out.
# Fail-closed seal: `record` writes the hash record over every runtime-
# consumed artifact (pristine tars included) after proving manifest↔fixture
# and tar↔tree identity; `seal` pins the record's own digest, after which
# `record` refuses to overwrite it; `run` refuses to spend trials while any
# check mismatches; `verify` re-checks on demand (again after batches).
import json, random, re, shutil, subprocess, sys, tarfile, tempfile, hashlib
from pathlib import Path

RIG = Path(__file__).parent
SEED = 20260712  # recorded in the prereg; schedule is a pure function of it
MODEL = "RECORDED-IN-PREREG"  # exact --model id, fixed for every trial
PERMISSION_MODE = "bypassPermissions"  # fixed trial permission surface (4.3); in the prereg record
ENV = {"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "DISABLE_AUTOUPDATER": "1"}
EVENTS = ("take", "offer")
# Offer grades must be bare skill names as spelled in the fixture roster
# (lowercase hyphenated, optional plugin: namespace) — a token form like
# "/ideate" or case drift would silently score as no-offer and hollow the
# calibration gate, so any other form blocks instead.
OFFER_RE = re.compile(r"^[a-z0-9][a-z0-9-]*(:[a-z0-9][a-z0-9-]*)?$")

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load_json(p: Path, default=None):
    if not p.exists():
        if default is not None:
            return default
        sys.exit(f"load failed: required file missing. Got: {p}")
    return json.loads(p.read_text())

def hash_inventory() -> dict:
    """Every runtime-consumed artifact, rig-relative: the pristine tarballs
    and all tree files, every fixture and task file, this script, the sealed
    schedule and roster inputs, the arm map, and (once sealed) the keys.
    schedule-extensions.json is deliberately absent: it legitimately grows
    post-seal, and its integrity check is derivation-equivalence on every
    load (load_schedule), not freezing."""
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
    if (RIG / "armmap" / "seal.json").exists():
        sys.exit("record refused: armmap/seal.json exists — re-recording after "
                 "the seal would re-bless drifted inputs. A post-seal mismatch "
                 "aborts the run; it is never re-recorded.")
    verify_fixture_manifest()
    verify_tars()
    (RIG / "armmap" / "hash-record.json").write_text(json.dumps(
        {"hashes": hash_inventory(), "runtime": runtime_identity()}, indent=2))
    print("recorded: armmap/hash-record.json")

def seal_record() -> None:
    """One-way: pin the hash record's own digest. Run once at Task-7 seal
    time; the printed digest is quoted in the committed preregistration.
    From then on `record` refuses to run."""
    verify_sealed_inputs()
    digest = sha256(RIG / "armmap" / "hash-record.json")
    (RIG / "armmap" / "seal.json").write_text(
        json.dumps({"hash_record_sha256": digest}, indent=2))
    print(f"sealed: hash-record digest {digest}")

def verify_sealed_inputs() -> None:
    """Hard gate before any trial spends; re-run after each batch. A mismatch
    invalidates the run (not a contract failure): pre-seal, amend deliberately
    and re-record; post-seal, abort and report — `record` refuses post-seal."""
    seal = RIG / "armmap" / "seal.json"
    if seal.exists():
        want = json.loads(seal.read_text()).get("hash_record_sha256")
        if sha256(RIG / "armmap" / "hash-record.json") != want:
            sys.exit("verify failed: hash-record.json does not match the "
                     "sealed digest — the record was rewritten after the "
                     "seal. Abort and report; never re-record.")
    rec = json.loads((RIG / "armmap" / "hash-record.json").read_text())
    verify_fixture_manifest()
    verify_tars()
    live = hash_inventory()
    if rec["hashes"] != live:
        drift = sorted({k for k, _ in set(rec["hashes"].items()) ^ set(live.items())})
        sys.exit(f"verify failed: hash record mismatch. Got: {drift}")
    if rec["runtime"] != runtime_identity():
        sys.exit(f"verify failed: runtime identity changed. Got: {runtime_identity()}")

def replicate_index(tid: str) -> int:
    stem, sep, idx = tid.rpartition("-r")
    if not (stem and sep and idx.isdigit()):
        sys.exit(f"schedule failed: trial id lacks -r<N> replicate suffix. Got: {tid!r}")
    return int(idx)

def validity() -> dict:
    """trial_id -> valid, from results-index.json; never-run rows are absent
    (treated valid-so-far by callers via .get(tid, True))."""
    return {r["trial"]["trial_id"]: bool(r.get("valid"))
            for r in load_json(RIG / "out" / "results-index.json", [])}

def load_grades(path: Path, required: bool = False) -> dict:
    """Offers-only scorer rows, fail-closed on shape:
    {trial_id: {"offers": [<skill-name>, ...]}} — [] when no offer. Any other
    shape (including the retired {"event","skill"} form) blocks."""
    if required and not path.exists():
        sys.exit(f"grades failed: no grades file. Got: {path}")
    grades = load_json(path, {})
    if (bad := sorted(t for t, g in grades.items()
                      if not isinstance(g, dict)
                      or not isinstance(g.get("offers"), list)
                      or not all(isinstance(s, str) for s in g["offers"]))):
        sys.exit(f"grades failed: malformed rows (need offers: [str]): {bad}")
    if (badv := sorted(t for t, g in grades.items()
                       if any(not OFFER_RE.fullmatch(s) for s in g["offers"]))):
        sys.exit("grades failed: offer strings must be bare skill names as "
                 f"spelled in the fixture roster (no /tokens, no prose): {badv}")
    return grades

def load_keys() -> dict:
    """Sealed per-task keys, fail-closed on shape:
    {task_id: {"kind": "positive", "targets": {<skill>: "take"|"offer", ...}}
             | {"kind": "negative", "overfire": [["take"|"offer", <skill>], ...]}}
    No wildcards exist: negative keys enumerate their overfire pairs
    explicitly (an any-skill null would fire on the trial's legitimate
    main-task take)."""
    keys = load_json(RIG / "armmap" / "trial-keys.json")
    for k, v in sorted(keys.items()):
        ok = isinstance(v, dict) and (
            (v.get("kind") == "positive"
             and isinstance(v.get("targets"), dict) and v["targets"]
             and all(isinstance(s, str) and e in EVENTS
                     for s, e in v["targets"].items()))
            or (v.get("kind") == "negative"
                and isinstance(v.get("overfire"), list) and v["overfire"]
                and all(isinstance(p, list) and len(p) == 2
                        and p[0] in EVENTS and isinstance(p[1], str)
                        for p in v["overfire"])))
        if not ok:
            sys.exit(f"keys failed: malformed sealed key (kind/targets/overfire): {k}")
    return keys

def matches(name, target: str) -> bool:
    """Suffix-aware exact-target match — namespaced keys (`plugin:skill`)
    are a library-general hazard; wrong skills never match."""
    return isinstance(name, str) and (name == target or name.endswith(f":{target}"))

def score_trial(takes: list, offers: list, key: dict) -> dict:
    """Positive: pass only when EVERY sealed target skill shows its required
    event — take-targets matched against the mechanical takes list,
    offer-targets against the scorer's offer grades. A wrong-skill event
    never counts; a take never satisfies an offer-target (or vice versa);
    extra non-target activity never blocks a positive pass (over-firing is
    the negative probes' question). Negative: overfire when ANY sealed
    [event, skill] pair shows."""
    def shows(event: str, skill: str) -> bool:
        pool = takes if event == "take" else offers
        return any(matches(n, skill) for n in pool)
    if key["kind"] == "positive":
        return {"pass": all(shows(ev, sk) for sk, ev in sorted(key["targets"].items())),
                "over": False, "kind": "positive"}
    return {"pass": False, "kind": "negative",
            "over": any(shows(ev, sk) for ev, sk in key["overfire"])}

def arm_counts(rows: list, grades: dict, keys: dict, armmap: dict,
               valid: dict, ridx: dict) -> dict:
    """Per (probe, arm) counts over the valid+graded subset of rows; callers
    gate completeness before trusting these."""
    per = {}
    for t in rows:
        tid = t["trial_id"]
        if not valid.get(tid, True):
            continue
        g = grades.get(tid)
        if g is None:
            continue
        rec = score_trial(ridx.get(tid, {}).get("takes", []), g["offers"],
                          keys[t["task_id"]])
        per.setdefault((t["probe"], armmap[t["tree"]]), []).append(rec)
    return {pa: {"n": len(v), "pass": sum(r["pass"] for r in v),
                 "overfire": sum(r["over"] for r in v), "kind": v[0]["kind"]}
            for pa, v in sorted(per.items())}

def extend_probes(counts: dict) -> list:
    """Sealed escalation rule, defined at n=3 with both arms present:
    positive — either arm splits 2-1; negative — the arms' overfire counts
    differ by exactly one -> extend BOTH arms to 5 for that probe."""
    out = []
    for probe in sorted({p for p, _ in counts}):
        arms = [c for (p, _), c in sorted(counts.items()) if p == probe]
        if len(arms) != 2 or any(c["n"] != 3 for c in arms):
            continue
        if arms[0]["kind"] == "positive" and any(c["pass"] in (1, 2) for c in arms):
            out.append(probe)
        if arms[0]["kind"] == "negative" and abs(arms[0]["overfire"] - arms[1]["overfire"]) == 1:
            out.append(probe)
    return out

def derive_extensions() -> list:
    """The ONE permissible derived-row set, recomputed from the sealed
    schedule, the validity log, and the standing first-round grades — never
    hand-authored. (a) Every invalid row gains exactly one replacement: same
    probe/task/tree/seam_skill, next per-cell replicate index, `replaces`
    naming the invalid id; chains continue the same rule. (b) When the sealed
    escalation rule fires on the first-round counts, each arm of that probe
    gains exactly two rows (to n=5), reusing the cell's task assignment,
    replicate indices continuing the counter, arm-interleaved by
    random.Random(f"{SEED}:{probe}:extension"). Escalation rows carry
    `escalation: true` (their replacements inherit it) and are excluded from
    the EXTEND computation, so the derivation is stable across re-tallies —
    and any hand edit to grades or the extension file surfaces as an
    equivalence mismatch instead of a changed result."""
    rows = [dict(r) for r in load_json(RIG / "schedule.json")]
    valid = validity()
    derived = []

    def cell_key(r):
        return (r["probe"], r["task_id"], r["tree"])

    def add_replacements():
        while True:
            replaced = {r.get("replaces") for r in rows}
            due = sorted(r["trial_id"] for r in rows
                         if not valid.get(r["trial_id"], True)
                         and r["trial_id"] not in replaced)
            if not due:
                return
            r = next(x for x in rows if x["trial_id"] == due[0])
            cell = [x for x in rows if cell_key(x) == cell_key(r)]
            nxt = 1 + max(replicate_index(x["trial_id"]) for x in cell)
            new = {k: v for k, v in r.items() if k != "replaces"}
            new["trial_id"] = f"{r['trial_id'].rpartition('-r')[0]}-r{nxt}"
            new["replaces"] = r["trial_id"]
            rows.append(new)
            derived.append(new)

    add_replacements()
    grades = load_grades(RIG / "grades.json")
    keys = load_keys() if (RIG / "armmap" / "trial-keys.json").exists() else {}
    r1 = [r for r in rows if not r.get("escalation")]
    if keys and all(grades.get(r["trial_id"]) is not None
                    for r in r1 if valid.get(r["trial_id"], True)):
        armmap = load_json(RIG / "armmap" / "arm-map.json")
        if (badtree := sorted({t["tree"] for t in r1} - set(armmap))):
            sys.exit(f"schedule failed: scheduled trees missing from arm map: {badtree}")
        if (nokey := sorted({t["task_id"] for t in r1} - set(keys))):
            sys.exit(f"schedule failed: no sealed key for tasks: {nokey}")
        ridx = {r["trial"]["trial_id"]: r
                for r in load_json(RIG / "out" / "results-index.json", [])}
        counts = arm_counts(r1, grades, keys, armmap, valid, ridx)
        for probe in extend_probes(counts):
            added = []
            for tree in sorted({r["tree"] for r in r1 if r["probe"] == probe}):
                cell = [x for x in rows if x["probe"] == probe and x["tree"] == tree]
                for _ in range(2):  # replacements hold each cell at 3 valid -> exactly two more per arm
                    nxt = 1 + max(replicate_index(x["trial_id"]) for x in cell)
                    new = {k: v for k, v in cell[0].items()
                           if k in ("probe", "task_id", "tree", "seam_skill")}
                    new["trial_id"] = f"{cell[0]['trial_id'].rpartition('-r')[0]}-r{nxt}"
                    new["escalation"] = True
                    cell.append(new)
                    added.append(new)
            random.Random(f"{SEED}:{probe}:extension").shuffle(added)
            rows += added
            derived += added
        add_replacements()  # escalation rows can themselves come back invalid
    return derived

def load_schedule(pilot: bool = False) -> list:
    """The pilot- prefix is a runner-enforced namespace, not a convention: a
    pilot row without it would write its stream under a sealed id, and run's
    skip-if-done logic would then silently replace the sealed execution."""
    if pilot:
        sched = load_json(RIG / "pilot-schedule.json")
        if (bad := sorted(t["trial_id"] for t in sched
                          if not t["trial_id"].startswith("pilot-"))):
            sys.exit(f"schedule failed: pilot rows without the pilot- prefix: {bad}")
    else:
        base = load_json(RIG / "schedule.json")
        required = derive_extensions()
        on_disk = load_json(RIG / "schedule-extensions.json", [])
        if on_disk != required:
            delta = sorted({str(r.get("trial_id")) if isinstance(r, dict) else repr(r)
                            for r in on_disk + required
                            if r not in on_disk or r not in required})
            sys.exit("schedule failed: schedule-extensions.json does not equal "
                     "the derived row set — regenerate with `runner.py extend`, "
                     f"never hand-edit. Got: {delta or 'row-order drift'}")
        sched = base + required
        if (bad := sorted(t["trial_id"] for t in sched
                          if t["trial_id"].startswith("pilot-"))):
            sys.exit(f"schedule failed: sealed rows carrying the pilot- prefix: {bad}")
    ids = [t["trial_id"] for t in sched]
    if (dupes := sorted({i for i in ids if ids.count(i) > 1})):
        sys.exit(f"schedule failed: duplicate trial ids: {dupes}")
    return sched

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
    seam_ok = seam is None or any(matches(s, seam) for s in completed)
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
    scorer reads these files and nothing else, and judges OFFERS only (the
    takes ride along as context so a report of work already done is not
    mistaken for a proposed handoff)."""
    results = json.loads((RIG / "out" / "results-index.json").read_text())
    by_id = {t["trial_id"]: t for t in load_schedule()}
    pdir = RIG / "out" / "packets"
    pdir.mkdir(exist_ok=True)
    for r in results:
        if not r.get("valid") or r["trial"]["trial_id"].startswith("pilot-"):
            continue  # pilot outputs never enter sealed scoring
        tid = r["trial"]["trial_id"]
        if by_id.get(tid) != r["trial"]:  # same row-identity guard as tally
            sys.exit("packets blocked: results-index row does not match its "
                     f"scheduled row: {tid}")
        events = [json.loads(l) for l in
                  (RIG / "out" / f"{tid}.jsonl").read_text().splitlines() if l.strip()]
        final = next((e.get("result", "") for e in reversed(events)
                      if e.get("type") == "result"), "")
        (pdir / f"{tid}.json").write_text(json.dumps(
            {"trial_id": tid, "final_text": final, "takes": r["takes"]}, indent=2))

def tally(grades_path: Path) -> None:
    """Score mechanically — takes from the captured stream (results-index),
    offers from the scorer's grades — via the sealed keys, then apply the
    sealed escalation rule: EXTEND flags print before any per-arm detail, and
    nothing prints while any valid first-round trial lacks a grade or any
    grade sits on an invalid trial. grades.json and trial-keys.json shapes
    (and their fail-closed guards) live in load_grades/load_keys; scoring
    semantics live in score_trial. The scorer never emits pass/overfire — it
    cannot: the keys are sealed."""
    grades = load_grades(grades_path, required=True)
    keys = load_keys()
    armmap = load_json(RIG / "armmap" / "arm-map.json")
    sched = load_schedule()  # enforces derivation equivalence + unique ids
    valid = validity()
    ridx = {r["trial"]["trial_id"]: r
            for r in load_json(RIG / "out" / "results-index.json")}
    sched_ids = {t["trial_id"] for t in sched}
    if (unknown := sorted(set(grades) - sched_ids)):
        sys.exit(f"tally blocked: grades for unscheduled trials: {unknown}")
    if (norun := sorted(t for t in grades if t not in ridx)):
        sys.exit(f"tally blocked: grades for trials with no captured result: {norun}")
    # Row-identity guard: every captured result occupying a scheduled id must
    # record exactly the sealed/derived row it claims to be — a stream produced
    # under another row (wrong tree, wrong task, pilot slip) blocks here.
    by_id = {t["trial_id"]: t for t in sched}
    if (forged := sorted(tid for tid, r in ridx.items()
                         if tid in by_id and r.get("trial") != by_id[tid])):
        sys.exit("tally blocked: results-index rows that do not match their "
                 f"scheduled rows: {forged}")
    # Invalid rows must carry NO grade: a grade recorded before a late
    # invalidation (post-batch verify failure) or by mistake is removed
    # explicitly and re-tallied — counted silently, it would double a cell
    # alongside its replacement.
    if (badg := sorted(t for t in grades if not valid.get(t, True))):
        sys.exit(f"tally blocked: grades attached to invalid trials: {badg}")
    if (nokey := sorted({t["task_id"] for t in sched} - set(keys))):
        sys.exit(f"tally blocked: no sealed key for tasks: {nokey}")
    if (badtree := sorted({t["tree"] for t in sched} - set(armmap))):
        sys.exit(f"tally blocked: scheduled trees missing from arm map: {badtree}")
    probe_kinds = {}
    for t in sched:
        probe_kinds.setdefault(t["probe"], set()).add(keys[t["task_id"]]["kind"])
    if (mixed := sorted(p for p, ks in probe_kinds.items() if len(ks) > 1)):
        sys.exit(f"tally blocked: probes mixing positive and negative kinds: {mixed}")
    # Hard gate: every valid FIRST-ROUND trial needs a grade before anything
    # prints (replacement completeness is already forced by the derivation
    # equivalence in load_schedule). A silent skip would land an arm at n!=3,
    # and per-arm detail would print with the sealed extend-before-unblinding
    # rule never consulted — premature unblinding on a bookkeeping gap.
    r1 = [t for t in sched if not t.get("escalation")]
    if (ungraded := sorted(t["trial_id"] for t in r1
                           if valid.get(t["trial_id"], True)
                           and grades.get(t["trial_id"]) is None)):
        sys.exit(f"tally blocked: no grade for first-round trials: {ungraded}")
    pending = extend_probes(arm_counts(r1, grades, keys, armmap, valid, ridx))
    if pending:
        todo = sorted(t["trial_id"] for t in sched if t.get("escalation")
                      and valid.get(t["trial_id"], True)
                      and grades.get(t["trial_id"]) is None)
        if todo:  # detail stays suppressed until the extension is graded
            for probe in pending:
                print(f"EXTEND: {probe} -> run both arms to 5, "
                      "blind-grade only the added trials")
            print(f"pending extension trials: {todo}")
            return
    counts = arm_counts(sched, grades, keys, armmap, valid, ridx)
    print(json.dumps({f"{p}/{a}": {"n": c["n"], "pass": c["pass"],
          "overfire": c["overfire"]} for (p, a), c in sorted(counts.items())},
          indent=2))

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "record":
        record_hashes()
    elif cmd == "seal":
        seal_record()
    elif cmd == "verify":
        verify_sealed_inputs()
        print("OK: sealed inputs match the hash record")
    elif cmd == "reset-tree":  # canary helper — extract exactly what trials run
        print(reset_tree(sys.argv[2]))
    elif cmd == "extend":
        # Derives, never invents: writing the file spends nothing; run/tally
        # still refuse unless the on-disk content equals a fresh derivation.
        required = derive_extensions()
        (RIG / "schedule-extensions.json").write_text(json.dumps(required, indent=2))
        print(f"wrote schedule-extensions.json: {len(required)} derived rows")
    elif cmd == "run":
        verify_sealed_inputs()  # fail closed BEFORE any trial spends
        argv = sys.argv[2:]
        sched = load_schedule(pilot="--pilot" in argv)
        wanted = {a for a in argv if a != "--pilot"}
        if (missing := sorted(wanted - {t["trial_id"] for t in sched})):
            sys.exit(f"run blocked: unknown trial ids: {missing}")
        if wanted:
            sched = [t for t in sched if t["trial_id"] in wanted]
        if not json.loads((RIG / "sentinel-absent.json").read_text()):
            sys.exit("run blocked: sentinel-absent.json is empty — the "
                     "host-leak sentinel guard is disarmed (Task 4.3 "
                     "requires at least three host-only names)")
        # Idempotent + selective: an existing output stream is never
        # re-executed or overwritten — sealed streams and standing grades
        # survive re-invocation; re-runs and extensions enter as NEW rows
        # (new trial ids) via the derived schedule-extensions.json. A stream
        # is "done" ONLY with a matching results-index row recording exactly
        # its scheduled row; a stream without one (interrupted batch, foreign
        # or pilot-slipped output) hard-stops instead of silently standing in
        # for the scheduled execution.
        idx = {r["trial"]["trial_id"]: r
               for r in load_json(RIG / "out" / "results-index.json", [])}
        if (orphaned := sorted(
                t["trial_id"] for t in sched
                if (RIG / "out" / f"{t['trial_id']}.jsonl").exists()
                and idx.get(t["trial_id"], {}).get("trial") != t)):
            sys.exit("run blocked: existing streams without matching "
                     f"results-index rows: {orphaned} — a foreign or stale "
                     "output occupies a scheduled id; never overwrite or "
                     "delete, resolve per Task 8.2")
        done = {t["trial_id"] for t in sched
                if (RIG / "out" / f"{t['trial_id']}.jsonl").exists()}
        if done:
            print(f"skipping existing streams: {sorted(done)}")
        for t in sched:  # merge per trial so an interruption orphans at most one stream
            if t["trial_id"] not in done:
                merge_results([run_trial(t)])
    elif cmd == "packets":
        packets()
    elif cmd == "tally":
        tally(RIG / "grades.json")
    else:
        sys.exit("usage: runner.py record|seal|verify|reset-tree <tree>|"
                 "extend|run [--pilot] [trial ids]|packets|tally")
```

And `synthetic-suite.py`, kept beside the runner at the rig root (its disposable case rigs land in `sup-suite-*` temp dirs, never deleted — reclaim with `trash`):

```python
#!/usr/bin/env python3
"""synthetic-suite.py — pre-seal proof of runner.py's mechanical rules.

Builds a disposable rig per case under sup-suite-* temp dirs (never deleted;
reclaim with `trash`) and asserts scoring, derivation, escalation, and guard
behavior. Run from the rig root, next to runner.py: `python3 synthetic-suite.py`.
Every case must print `ok`; any FAIL exits 1. The pilot never exercises
escalation or the guards, so this suite is the only pre-seal proof the
mechanical rules work.
"""
import json, shutil, subprocess, sys, tarfile, tempfile, hashlib
from pathlib import Path

HERE = Path(__file__).parent
FAILS = []

def check(name, cond, out=""):
    print(("ok   " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)
        if out:
            print("     " + out.replace("\n", "\n     "))

def rig(sched, keys=None, grades=None, results=None, ext=None, armmap=None):
    d = Path(tempfile.mkdtemp(prefix="sup-suite-"))
    shutil.copy(HERE / "runner.py", d / "runner.py")
    (d / "armmap").mkdir()
    (d / "out").mkdir()
    (d / "schedule.json").write_text(json.dumps(sched))
    (d / "armmap" / "arm-map.json").write_text(json.dumps(
        {"tree-A": "ON", "tree-B": "OFF"} if armmap is None else armmap))
    if keys is not None:
        (d / "armmap" / "trial-keys.json").write_text(json.dumps(keys))
    if grades is not None:
        (d / "grades.json").write_text(json.dumps(grades))
    if results is not None:
        (d / "out" / "results-index.json").write_text(json.dumps(results))
    if ext is not None:
        (d / "schedule-extensions.json").write_text(json.dumps(ext))
    return d

def run(d, *args):
    return subprocess.run([sys.executable, "runner.py", *args],
                          cwd=d, capture_output=True, text=True)

def row(tid, probe, task, tree, **kw):
    return {"trial_id": tid, "probe": probe, "task_id": task, "tree": tree, **kw}

def res(r, valid=True, takes=()):
    return {"trial": r, "valid": valid, "takes": list(takes)}

def counts(out):
    return json.loads(out[out.index("{"):])

# ---- Group A: scoring semantics (exact-target, multi-target, offer-vs-take)
POS_TAKE = {"task-p": {"kind": "positive", "targets": {"characterization-tests": "take"}}}
POS_OFFER = {"task-p": {"kind": "positive", "targets": {"tdd": "offer"}}}
POS_BOTH = {"task-p": {"kind": "positive",
                       "targets": {"authorization-design": "take",
                                   "injection-safe-inputs": "take"}}}
NEG = {"task-n": {"kind": "negative", "overfire": [["take", "red-team"], ["offer", "ideate"]]}}

def one(keys, takes, offers, probe="p", task="task-p"):
    r = row(f"{probe}-A-r1", probe, task, "tree-A")
    d = rig([r], keys=keys, grades={r["trial_id"]: {"offers": offers}},
            results=[res(r, takes=takes)], ext=[])
    return run(d, "tally")

p = one(POS_TAKE, ["totally-unrelated-skill"], [])
check("A1 wrong-skill take on a positive probe is NOT a pass",
      p.returncode == 0 and counts(p.stdout)["p/ON"]["pass"] == 0, p.stdout + p.stderr)
p = one(POS_TAKE, ["characterization-tests"], [])
check("A2 exact-target take passes",
      p.returncode == 0 and counts(p.stdout)["p/ON"]["pass"] == 1, p.stdout + p.stderr)
p = one(POS_TAKE, ["review-family:characterization-tests", "review-family:characterization-tests"], [])
check("A3 namespaced + duplicate take still matches its target",
      p.returncode == 0 and counts(p.stdout)["p/ON"]["pass"] == 1, p.stdout + p.stderr)
p = one(POS_BOTH, ["authorization-design", "injection-safe-inputs"], [])
check("A4 composition: both targets taken passes",
      p.returncode == 0 and counts(p.stdout)["p/ON"]["pass"] == 1, p.stdout + p.stderr)
p = one(POS_BOTH, ["authorization-design"], [])
check("A5 composition: one of two targets missing fails",
      p.returncode == 0 and counts(p.stdout)["p/ON"]["pass"] == 0, p.stdout + p.stderr)
p = one(POS_BOTH, ["authorization-design"], [])  # second target merely mentioned in text -> no offer grade
check("A6 composition: one taken, other merely mentioned (no offer grade) fails",
      p.returncode == 0 and counts(p.stdout)["p/ON"]["pass"] == 0, p.stdout + p.stderr)
p = one(POS_BOTH, ["authorization-design", "injection-safe-inputs", "ideate"], [])
check("A7 unexpected extra skill does not block a positive pass",
      p.returncode == 0 and counts(p.stdout)["p/ON"]["pass"] == 1, p.stdout + p.stderr)
p = one(POS_OFFER, [], ["tdd"])
check("A8 offer-target satisfied by a graded offer passes",
      p.returncode == 0 and counts(p.stdout)["p/ON"]["pass"] == 1, p.stdout + p.stderr)
p = one(POS_OFFER, ["tdd"], [])
check("A9 take does NOT satisfy an offer-only target",
      p.returncode == 0 and counts(p.stdout)["p/ON"]["pass"] == 0, p.stdout + p.stderr)
p = one(NEG, ["red-team"], [], task="task-n")
check("A10 sealed overfire pair fires on a matching take",
      p.returncode == 0 and counts(p.stdout)["p/ON"]["overfire"] == 1, p.stdout + p.stderr)
p = one(NEG, ["diagnose"], [], task="task-n")
check("A11 unlisted skill take is not an overfire",
      p.returncode == 0 and counts(p.stdout)["p/ON"]["overfire"] == 0, p.stdout + p.stderr)
p = one(NEG, [], ["ideate"], task="task-n")
check("A12 sealed offer-overfire pair fires on a graded offer",
      p.returncode == 0 and counts(p.stdout)["p/ON"]["overfire"] == 1, p.stdout + p.stderr)

# ---- Group B: escalation flow (derived rows, EXTEND before detail, full loop)
def sched33(probe="mid", task="task-mid"):
    return [row(f"{probe}-{t}-r{i}", probe, task, f"tree-{t}")
            for t in ("A", "B") for i in (1, 2, 3)]

def grades_for(sched, passing):  # passing: set of trial ids whose takes hit the target
    return ({r["trial_id"]: {"offers": []} for r in sched},
            [res(r, takes=["characterization-tests"] if r["trial_id"] in passing
                 else ["simplify-code"]) for r in sched])

KEY33 = {"task-mid": {"kind": "positive", "targets": {"characterization-tests": "take"}}}
s = sched33()
g, rx = grades_for(s, {"mid-A-r1", "mid-A-r2"})  # ON arm 2-1 -> EXTEND
d = rig(s, keys=KEY33, grades=g, results=rx)
p = run(d, "tally")
check("B5 tally refuses while the derived extension file is missing/stale",
      p.returncode != 0 and "runner.py extend" in p.stderr, p.stdout + p.stderr)
p = run(d, "extend")
ext = json.loads((d / "schedule-extensions.json").read_text())
check("B4a extend derives exactly two escalation rows per arm, r4/r5, flagged",
      len(ext) == 4
      and sorted(e["trial_id"] for e in ext)
          == ["mid-A-r4", "mid-A-r5", "mid-B-r4", "mid-B-r5"]
      and all(e.get("escalation") is True and e["task_id"] == "task-mid" for e in ext),
      json.dumps(ext))
p = run(d, "extend")
check("B4b derivation is deterministic (second extend writes identical content)",
      json.loads((d / "schedule-extensions.json").read_text()) == ext)
p = run(d, "tally")
check("B1 EXTEND flag + pending ids print, per-arm detail suppressed",
      p.returncode == 0 and "EXTEND: mid" in p.stdout
      and "pending extension trials" in p.stdout and "pass" not in p.stdout,
      p.stdout + p.stderr)
g2 = {**g, **{e["trial_id"]: {"offers": []} for e in ext}}
rx2 = rx + [res(e, takes=["characterization-tests"]) for e in ext]
(d / "grades.json").write_text(json.dumps(g2))
(d / "out" / "results-index.json").write_text(json.dumps(rx2))
p = run(d, "tally")
check("B4c graded extension unblocks full n=5 detail, EXTEND stable",
      p.returncode == 0 and counts(p.stdout)["mid/ON"]["n"] == 5
      and counts(p.stdout)["mid/OFF"]["n"] == 5
      and counts(p.stdout)["mid/ON"]["pass"] == 4, p.stdout + p.stderr)

g, rx = grades_for(s, {"mid-A-r1", "mid-A-r2", "mid-A-r3"})  # clean 3-0
d = rig(s, keys=KEY33, grades=g, results=rx, ext=[])
p = run(d, "tally")
check("B2 clean 3-0 prints detail with no EXTEND",
      p.returncode == 0 and "EXTEND" not in p.stdout
      and counts(p.stdout)["mid/ON"]["pass"] == 3, p.stdout + p.stderr)

sn = sched33(probe="n1", task="task-n1")
kn = {"task-n1": {"kind": "negative", "overfire": [["take", "red-team"]]}}
gn = {r["trial_id"]: {"offers": []} for r in sn}
rn = [res(r, takes=["red-team"] if r["trial_id"] == "n1-A-r1" else []) for r in sn]
d = rig(sn, keys=kn, grades=gn, results=rn)
run(d, "extend")
p = run(d, "tally")
check("B3 negative overfire-differ-by-one triggers EXTEND",
      p.returncode == 0 and "EXTEND: n1" in p.stdout, p.stdout + p.stderr)

# ---- Group C: replacement derivation + tamper cases
def valid_grades(sched, invalid=("mid-A-r1",)):
    return {r["trial_id"]: {"offers": []} for r in sched
            if r["trial_id"] not in invalid}

s = sched33()
rxi = [res(r, valid=(r["trial_id"] != "mid-A-r1"),
           takes=["characterization-tests"]) for r in s]
d = rig(s, keys=KEY33, grades=valid_grades(s), results=rxi)
p = run(d, "tally")
check("C1 invalid row without its derived replacement blocks at load",
      p.returncode != 0 and "runner.py extend" in p.stderr, p.stdout + p.stderr)
run(d, "extend")
ext = json.loads((d / "schedule-extensions.json").read_text())
check("C2a replacement row preserves probe/task/tree, next index, replaces",
      ext == [row("mid-A-r4", "mid", "task-mid", "tree-A", replaces="mid-A-r1")],
      json.dumps(ext))
gfull = {r["trial_id"]: {"offers": []} for r in s if r["trial_id"] != "mid-A-r1"}
gfull["mid-A-r4"] = {"offers": []}
rx_full = [r for r in rxi] + [res(ext[0], takes=["characterization-tests"])]
(d / "grades.json").write_text(json.dumps(gfull))
(d / "out" / "results-index.json").write_text(json.dumps(rx_full))
p = run(d, "tally")
check("C2b graded replacement restores full-n aggregation (n=3 per arm)",
      p.returncode == 0 and counts(p.stdout)["mid/ON"]["n"] == 3
      and counts(p.stdout)["mid/ON"]["pass"] == 3, p.stdout + p.stderr)
# chain: the replacement itself comes back invalid
rx_chain = rxi + [res(ext[0], valid=False)]
(d / "out" / "results-index.json").write_text(json.dumps(rx_chain))
(d / "grades.json").unlink()
run(d, "extend")
ext2 = json.loads((d / "schedule-extensions.json").read_text())
check("C9 replacement chain: invalid replacement gains its own r5 replacement",
      [e["trial_id"] for e in ext2] == ["mid-A-r4", "mid-A-r5"]
      and ext2[1]["replaces"] == "mid-A-r4", json.dumps(ext2))

def tamper(mutate, name, expect="never hand-edit"):
    s = sched33()
    rxi = [res(r, valid=(r["trial_id"] != "mid-A-r1"),
               takes=["characterization-tests"]) for r in s]
    d = rig(s, keys=KEY33, grades=valid_grades(s), results=rxi)
    run(d, "extend")
    ext = json.loads((d / "schedule-extensions.json").read_text())
    mutate(ext)
    (d / "schedule-extensions.json").write_text(json.dumps(ext))
    p = run(d, "tally")
    check(name, p.returncode != 0 and expect in p.stderr, p.stdout + p.stderr)

tamper(lambda e: e.append(row("mid-A-r5", "mid", "task-mid", "tree-A", replaces="mid-A-r1")),
       "C3 second replacement for one invalid trial blocks")
tamper(lambda e: e[0].update(trial_id="mid-A-r7"),
       "C4 wrong replicate index blocks")
tamper(lambda e: e.append(row("mid-B-r4", "mid", "task-mid", "tree-B", escalation=True)),
       "C5 escalation row without a fired EXTEND blocks")
tamper(lambda e: e[0].update(tree="tree-B"),
       "C4b replacement changing its cell blocks")
s = sched33()
g, rx = grades_for(s, {"mid-A-r1", "mid-A-r2"})
d = rig(s, keys=KEY33, grades=g, results=rx)
run(d, "extend")
ext = json.loads((d / "schedule-extensions.json").read_text())
ext.append(row("mid-A-r6", "mid", "task-mid", "tree-A", escalation=True))
(d / "schedule-extensions.json").write_text(json.dumps(ext))
p = run(d, "tally")
check("C6 over-extension past n=5 blocks",
      p.returncode != 0 and "never hand-edit" in p.stderr, p.stdout + p.stderr)

dup = [row("p-A-r1", "p", "task-p", "tree-A"), row("p-A-r1", "p", "task-p", "tree-A")]
d = rig(dup, keys=POS_TAKE, grades={"p-A-r1": {"offers": []}},
        results=[res(dup[0], takes=[])], ext=[])
p = run(d, "tally")
check("C7 duplicate trial ids block",
      p.returncode != 0 and "duplicate trial ids" in p.stderr, p.stdout + p.stderr)

r1_ = row("p-A-r1", "p", "task-p", "tree-A")
r2_ = row("p-A-r2", "p", "task-p", "tree-A", replaces="p-A-r1")
d = rig([r1_], keys=POS_TAKE,
        grades={"p-A-r1": {"offers": []}, "p-A-r2": {"offers": []}},
        results=[res(r1_, valid=False), res(r2_, takes=["characterization-tests"])],
        ext=[r2_])
p = run(d, "tally")
check("C8 grade attached to an invalid trial blocks",
      p.returncode != 0 and "grades attached to invalid trials" in p.stderr,
      p.stdout + p.stderr)

# ---- Group D: malformed-input blocks
def expect_block(name, needle, **kw):
    d = rig(**kw)
    p = run(d, "tally")
    check(name, p.returncode != 0 and needle in p.stderr, p.stdout + p.stderr)

r1_ = row("p-A-r1", "p", "task-p", "tree-A")
base = dict(sched=[r1_], keys=POS_TAKE, results=[res(r1_, takes=[])], ext=[])
expect_block("D1 offers not a list blocks", "malformed rows",
             **{**base, "grades": {"p-A-r1": {"offers": "tdd"}}})
expect_block("D2 retired {event,skill} grade shape blocks", "malformed rows",
             **{**base, "grades": {"p-A-r1": {"event": "take", "skill": "tdd"}}})
expect_block("D3 grade for an unscheduled trial blocks", "unscheduled trials",
             **{**base, "grades": {"p-A-r1": {"offers": []}, "ghost-r1": {"offers": []}}})
expect_block("D4 grade for a trial with no captured result blocks",
             "no captured result",
             sched=[r1_, row("p-A-r2", "p", "task-p", "tree-A")], keys=POS_TAKE,
             grades={"p-A-r1": {"offers": []}, "p-A-r2": {"offers": []}},
             results=[res(r1_, takes=[])], ext=[])
expect_block("D5 scheduled task with no sealed key blocks", "no sealed key",
             **{**base, "keys": {}, "grades": {"p-A-r1": {"offers": []}}})
expect_block("D6a unknown key kind blocks", "malformed sealed key",
             **{**base, "keys": {"task-p": {"kind": "positve", "targets": {"tdd": "take"}}},
                "grades": {"p-A-r1": {"offers": []}}})
expect_block("D6b positive key without targets blocks", "malformed sealed key",
             **{**base, "keys": {"task-p": {"kind": "positive", "targets": {}}},
                "grades": {"p-A-r1": {"offers": []}}})
expect_block("D6c negative wildcard (null skill) blocks", "malformed sealed key",
             **{**base, "keys": {"task-p": {"kind": "negative", "overfire": [["take", None]]}},
                "grades": {"p-A-r1": {"offers": []}}})
rB = row("p-B-r1", "p", "task-n", "tree-B")
expect_block("D7 probe mixing positive and negative kinds blocks", "mixing",
             sched=[r1_, rB], keys={**POS_TAKE, **NEG},
             grades={"p-A-r1": {"offers": []}, "p-B-r1": {"offers": []}},
             results=[res(r1_, takes=[]), res(rB, takes=[])], ext=[])
expect_block("D8 scheduled tree missing from arm map blocks", "arm map",
             **{**base, "grades": {"p-A-r1": {"offers": []}}, "armmap": {"tree-B": "OFF"}})
expect_block("D9 ungraded valid first-round trial blocks", "no grade",
             **{**base, "grades": {}})

# ---- Group F: scorer offer-vocabulary guard
expect_block("F1 token-form offer string (/ideate) blocks", "bare skill names",
             **{**base, "grades": {"p-A-r1": {"offers": ["/ideate"]}}})
expect_block("F2 case-drifted offer string (Ideate) blocks", "bare skill names",
             **{**base, "grades": {"p-A-r1": {"offers": ["Ideate"]}}})

# ---- Group G: sealed-id namespace + row-identity guards
expect_block("G1 pilot-prefixed row in the sealed schedule blocks",
             "pilot- prefix",
             sched=[row("pilot-p-A-r1", "p", "task-p", "tree-A")],
             keys=POS_TAKE, grades={}, ext=[])
r1_ = row("p-A-r1", "p", "task-p", "tree-A")
expect_block("G2 results row not matching its scheduled row blocks tally",
             "do not match their scheduled rows",
             sched=[r1_], keys=POS_TAKE,
             grades={"p-A-r1": {"offers": []}},
             results=[res(row("p-A-r1", "p", "task-p", "tree-B"), takes=[])],
             ext=[])
d = rig([r1_], keys=POS_TAKE,
        results=[res(row("p-A-r1", "p", "task-p", "tree-B"), takes=[])], ext=[])
(d / "out" / "p-A-r1.jsonl").write_text('{"type":"result","result":"done"}\n')
p = run(d, "packets")
check("G3 packets refuses a results row not matching its scheduled row",
      p.returncode != 0 and "does not match its scheduled row" in p.stderr,
      p.stdout + p.stderr)

# ---- Group E: seal + run guards (mini real rig; needs `claude --version`)
def mini_rig(sentinels):
    d = rig([row("p-A-r1", "p", "task-p", "tree-A")], keys=POS_TAKE, ext=[])
    for t in ("tree-A", "tree-B"):
        (d / "trees" / t).mkdir(parents=True)
        (d / "trees" / t / "CLAUDE.md").write_text(f"# {t}\n")
        with tarfile.open(d / "trees" / f"{t}.pristine.tar", "w") as tar:
            tar.add(d / "trees" / t, arcname=t)
    (d / "fixture").mkdir()
    (d / "fixture" / "f.txt").write_text("fixture\n")
    digest = hashlib.sha256((d / "fixture" / "f.txt").read_bytes()).hexdigest()
    (d / "fixture" / "MANIFEST.txt").write_text(f"{digest}  f.txt\n")
    (d / "tasks").mkdir()
    (d / "expected-roster.json").write_text("[]")
    (d / "sentinel-absent.json").write_text(json.dumps(sentinels))
    return d

d = mini_rig(["skill-benchmark"])
p = run(d, "record")
check("E0 record writes the hash record on a coherent rig",
      p.returncode == 0 and (d / "armmap" / "hash-record.json").exists(), p.stderr)
p = run(d, "verify")
check("E0b verify passes on the recorded rig", p.returncode == 0, p.stderr)
p = run(d, "run", "no-such-trial-r9")
check("E3 run blocks on unknown trial ids",
      p.returncode != 0 and "unknown trial ids" in p.stderr, p.stdout + p.stderr)
(d / "pilot-schedule.json").write_text(json.dumps(
    [row("mid-A-r1", "mid", "task-mid", "tree-A")]))  # pilot row WITHOUT prefix
p = run(d, "run", "--pilot")
check("E4 run --pilot refuses pilot rows without the pilot- prefix",
      p.returncode != 0 and "pilot- prefix" in p.stderr, p.stdout + p.stderr)
(d / "out" / "p-A-r1.jsonl").write_text('{"type":"result","result":"x"}\n')
p = run(d, "run", "p-A-r1")
check("E5 run hard-stops on a stream with no matching results row",
      p.returncode != 0 and "occupies a scheduled id" in p.stderr,
      p.stdout + p.stderr)
(d / "out" / "results-index.json").write_text(json.dumps(
    [res(row("p-A-r1", "p", "task-p", "tree-A"), takes=[])]))
p = run(d, "run", "p-A-r1")
check("E6 run still skips a stream whose results row matches its schedule row",
      p.returncode == 0 and "skipping existing streams" in p.stdout,
      p.stdout + p.stderr)
p = run(d, "seal")
check("E1a seal pins the hash-record digest",
      p.returncode == 0 and (d / "armmap" / "seal.json").exists(), p.stderr)
p = run(d, "record")
check("E1b record refuses after the seal",
      p.returncode != 0 and "record refused" in p.stderr, p.stdout + p.stderr)
rec = json.loads((d / "armmap" / "hash-record.json").read_text())
rec["runtime"]["model"] = "tampered"
(d / "armmap" / "hash-record.json").write_text(json.dumps(rec, indent=2))
p = run(d, "verify")
check("E2 post-seal rewrite of the hash record blocks verify",
      p.returncode != 0 and "sealed digest" in p.stderr, p.stdout + p.stderr)
d = mini_rig([])
run(d, "record")
p = run(d, "run", "p-A-r1")
check("E7 run blocks while sentinel-absent.json is empty",
      p.returncode != 0 and "sentinel guard is disarmed" in p.stderr,
      p.stdout + p.stderr)

print()
if FAILS:
    sys.exit(f"synthetic suite failed: {len(FAILS)} case(s): {FAILS}")
print(f"synthetic suite: all cases passed")
```

7. **Schedule.** Generate `schedule.json`: for each probe/task cell and each tree, the planned trial rows, deterministically interleaved by arm from `SEED` (e.g. seeded `random.Random(SEED).shuffle` over the cell list) so backend drift cannot correlate with arm. Row shape: `trial_id`, `probe`, `task_id`, `tree`, plus — on every seam-probe and N2 row, the two probes whose scored moment requires an in-session skill completion — `seam_skill`: the exact skill whose completion the trial must reach (`diagnose` for the seam probe; N2's terrain skill per its pilot-confirmed scenario). `runner.py` marks a `seam_skill` row invalid when that skill never completes in-session (suffix-aware take match; completion = the take's `tool_result` returns without error), so unreached-seam rows never enter scorer packets. `pilot-schedule.json` rows carry the same shape. Trial ids carry the per-cell replicate index (`…-r1`, `…-r2`, …) so derived rows extend the counter deterministically, and id stems are tree-neutral — `<probe>-c<K>-r<N>` with `K` the cell's index in the seeded emission order, the tree named only in the row's `tree` field — so packet ids and derived ids never hand the scorer arm-grouping information (Task 8.3's "no tree names" is then mechanical, not aspirational; the synthetic suite's letter-stem ids are mechanics fixtures, not this convention). Regenerated only if the prereg changes counts; the seed and generator line are quoted in the prereg. Derived-row rule (sealed in the Task-7 prereg, computed by the runner, never hand-authored): `runner.py extend` recomputes the ONE permissible derived-row set from the sealed schedule, the validity log, and the standing first-round grades, and writes it to `schedule-extensions.json`; every non-pilot `run` and `tally` re-derives that set and refuses to proceed unless the on-disk file equals it exactly, so a hand edit — an extra replacement, a wrong replicate index, an unauthorized escalation row — cannot survive to execution or counting. (a) *invalid re-run* — every invalidated trial gains exactly one replacement row: same probe, task, tree, and `seam_skill`, the next per-cell replicate index, and `replaces: <old_trial_id>`; chains continue the same rule when a replacement itself invalidates; the old row keeps its invalid marker and its stream is never overwritten; (b) *escalation extension* — when the sealed escalation rule fires on the first-round counts, both arms of that probe gain exactly two rows (to n=5), reusing the cell's task assignment, replicate indices continuing the counter, arm-interleaved by `random.Random(f"{SEED}:{probe}:extension")`; escalation rows carry `escalation: true` (their replacements inherit it) and are excluded from the EXTEND computation, so the derivation is stable across re-tallies and any post-hoc edit to first-round grades surfaces as an equivalence mismatch rather than a changed result. The sealed `schedule.json` and its hash stay untouched; derived rows are executed selectively (`runner.py run <new trial ids>`). Sealed keys need no per-row additions: `trial-keys.json` is keyed by `task_id`, so derived rows inherit their task's key.
8. **Effective-load canary (per tree, arm-map holder only, never the scorer).** Run the canary against a freshly tar-extracted copy — the artifact trials actually execute — never against `trees/<tree>` directly (which would pass on a stale tar and also lets the CLI write session state into the source tree). For each tree: `CLAUDE_CONFIG_DIR="$(python3 runner.py reset-tree <tree>)" claude -p "Quote, byte-exact, the first markdown heading of your user-global instruction memory. Then answer YES or NO: does a section titled 'Skill Use' appear in it? Then answer YES or NO: does the phrase 'consult ~/.agents/docs/agents/charter.md' appear in it?" --model <pinned>`. Required: heading byte-matches `# Global Instructions — Replica`; host phrase NO in both; `## Skill Use` YES in the ON tree and NO in the OFF tree. A failure blocks all trials in that tree. Run before the pilot and again immediately before sealed runs.
9. **Hash record (mechanical, fail-closed).** Run `python3 runner.py record` before the pilot and again after any pre-seal amendment (Task 7.3 re-records once the sealed keys land, then seals); after the seal the only check is `python3 runner.py verify` — `record` refuses to run once `armmap/seal.json` exists. It refuses to write unless `fixture/MANIFEST.txt` matches the live fixture contents exactly and each pristine tar expands byte-identically to its source tree, then writes `armmap/hash-record.json` covering every runtime-consumed artifact: both pristine tarballs and every file under `trees/` (replicas, skills, settings), every fixture file, every task file, `runner.py`, `schedule.json`, `expected-roster.json`, `sentinel-absent.json`, `armmap/arm-map.json` (and `armmap/trial-keys.json` once Task 7 seals it); plus `claude --version` output, the model id, the trial permission mode, and the trial environment variable set. `runner.py run` re-runs both integrity checks and re-verifies the whole record before spending any trial, hard-stopping on any mismatch; `python3 runner.py verify` re-checks on demand and is re-run after each batch before grading. A mismatch invalidates the run (not a contract failure): pre-seal, amend deliberately and re-record; post-seal, abort and report. `schedule-extensions.json` is deliberately outside the hash record: it legitimately grows post-seal, and its integrity check is the Task-4.7 derivation equivalence on every load, not freezing. The seal itself is mechanical: at Task-7 seal time `python3 runner.py seal` pins the hash record's own digest into `armmap/seal.json` (the digest is quoted in the prereg), after which `record` refuses to run — a post-seal mismatch can only be reported, never re-blessed by re-recording.
10. **Environment surfaces record.** In a sibling `armmap/environment-record.json` (executor-maintained — `runner.py record` owns and overwrites `hash-record.json`, so the two never clobber each other) record: auto-memory disabled (env var), connectors suppressed (confirm absent in the pilot's `system/init`), managed/server-managed settings presence on this host (`ls /Library/Application\ Support/ClaudeCode/ 2>/dev/null; ls ~/Library/Application\ Support/ClaudeCode/managed-settings.json 2>/dev/null` — record presence/absence and hashes), the auth method (Keychain), the trial permission mode (`bypassPermissions`), and the invoking-shell surface: run `runner.py` from a plain terminal, never from inside a Claude or Codex session — trials inherit the invoking process environment (arm-symmetric either way, but it belongs in the record; capture the names of any `CLAUDE*`/`CODEX*` variables present at run time).

## Task 5 — Author trial tasks fresh-context (feeds Task 6)

Trial prompts must not be authored by this session or any context that has read this plan or the design (the Era-86 lesson: 4 of 6 first-draft prompts leaked discipline vocabulary; regenerate, never hand-patch).

1. For each of the six probes (3 positive, 3 negative), write a **facts-only kernel**: what the fixture is, what the user in the scenario wants, what state exists — zero skill names, zero expectations, zero arm/discipline vocabulary. The kernel for the seam probe describes only the failing behavior a user would report; the mid-task kernel only the refactor ask; N1–N3 kernels only their neutral scenarios.
2. Spawn a fresh subagent per prompt with ONLY the kernel and the instruction "write the user message this person would send to a coding agent working in this project" — no plan, no design, no probe taxonomy in its context. Fresh means a default named/general-purpose spawn, which starts context-isolated by documented default (a subagent gets a fresh context window and none of the parent conversation); never the `fork` subagent type or `/fork`, which inherits the whole conversation. The same isolation rule binds the step-3 reviewer and the Task-8 scorer; the mechanism and active tool contract are recorded in the prereg (Task 7.1, blinding).
3. Adversarially review each returned prompt (a second fresh subagent may do this): reject and regenerate on any leak of expected skill names, assertions, arm identity, intended answers, or authorization ambiguity (seam prompts must be unambiguous between take-authorized and offer-only readings — that wording is what the sealed per-trial authorization key derives from). Save accepted prompts as `tasks/<task_id>.txt`; write separate pilot-only tasks the same way (pilot tasks and outputs are excluded from sealed scoring).
4. Update the hash record.

## Task 6 — Unsealed paired pilot (step 4)

1. Run the effective-load canary (Task 4.8). Then run the pilot: for every probe, positive and negative, a cheap paired run (1–2 trials per arm per probe) using the pilot-only tasks, via `runner.py run --pilot` against `pilot-schedule.json` (pilot trial ids carry a `pilot-` prefix, enforced by the runner — `run --pilot` refuses rows without it and the sealed schedule path refuses rows with it — so a pilot output can never occupy a sealed id or enter sealed packets).
2. Confirm per channel: the exact roster check passes with zero sentinel hits (a sentinel hit means delivery is broken — fix delivery before confirming `expected-roster.json`) and no permission denials appear in the stream; the observable event is extractable (takes mechanically from `tool_use`; offers gradeable from final text); the scoring key is unambiguous; the OFF-arm base rate leaves headroom (no ceiling); for the seam probe, both arms reliably reach an in-session skill completion at all (a trial where no skill completes never reaches the seam — invalid, re-run, symmetric across arms), and the runner's mechanical `seam_skill` detection (Task 4.7) fires correctly against the pilot's seam and N2 streams — adapt the completion parsing pre-seal if the `tool_result` shape differs, and read the proxy-marked pilot seam streams to confirm the proxy (a non-error `tool_result` for the take) tracks a genuinely finished diagnosis rather than a mere skill load; if it does not, sharpen the proxy pre-seal or record the residual in the prereg's honest-bound section (it deflates power symmetrically, never biases arms); for each negative probe, the scenario is unambiguously gradeable and the OFF-arm overfire base rate is measured.
3. Resolve every empty, ambiguous, or ceilinged channel by redesign (fixture, kernel regeneration, or observable-rule sharpening) — or drop a **positive** channel to characterization-only with that recorded. The negative calibration gate cannot be waived or dropped: a negative channel still ambiguous after redesign leaves the gate unmet and blocks GO (design, Negative controls). Every redesign iteration gets fresh pilot trial ids: bump an iteration counter in `pilot-schedule.json`'s ids (`pilot-i2-…`, `pilot-i3-…`) whenever a pilot fixture, task, parser, or observable rule changes — the runner never re-executes an existing stream, so a reused id would silently re-read the pre-redesign output as if it were the new design's. The no-overwrite rule stays.
4. Record pilot outcomes (per channel: fired/empty/ambiguous/ceiling, base rates, redesigns made) in a `pilot-notes.md` inside the rig. Pilot tasks and outputs never enter sealed scoring.

## Task 7 — Preregistration, adversarial review, seal (step 5)

1. Write `docs/plans/2026-07-NN-skill-use-probes-preregistration.md` following the sealed shape of [`2026-07-10-skill-value-test-preregistration.md`](2026-07-10-skill-value-test-preregistration.md) (frontmatter with `type: pre-registration`, status line, append-only-below-seal rule). Contents, all fixed before any sealed data: the question; the two arms (byte-identical replicas ± the Task-2 block, quoted); the fresh sealed task texts; the fixture manifest hash; the pinned roster and skill-copy commit SHA; `claude --version` and the exact model id; the full hash record; the environment-surfaces record; the observable scoring rules (take = a `tool_use` block naming the exact target Skill, extracted mechanically from the captured stream and never re-classified by the scorer; offer = the response explicitly names the target invocation token and proposes a clear handoff — generic suggestions do not count; the scorer judges offers only, returned per trial as `{"offers": [...]}`); the offer-grade vocabulary pin (offers are bare skill names exactly as spelled in the fixture roster — lowercase hyphenated, optional `plugin:` namespace, never slash tokens or prose; worked example: `{"seam-c1-r1": {"offers": ["tdd"]}}` — the runner rejects any other form); the seam-completion proxy definition (in-session completion = the seam skill's `tool_use` receiving a non-error `tool_result` — a load-and-return proxy, not proof the skill's full workflow finished; this proxy is the sealed meaning of "completes", with the Task-6.2 stream-reading confirmation or the owned residual recorded here); the per-task sealed keys recorded as `armmap/trial-keys.json` — each positive task a `targets` map naming every required skill with its required event (`take` or `offer`: the composition probe lists both target skills; seam/N2 events derive from each prompt's own authorization language), each negative task an explicit `overfire` pair list (`[event, skill]`, no wildcards: every take or offer that counts as overfire per N1/N2/N3 is enumerated); the seeded schedule (seed, generator, and the emitted order); the derived-row rule (Task 4.7: runner-derived replacement and escalation rows, equivalence-checked on every load, never hand-authored); the fixed trial permission mode; trial counts (3/arm/probe) and the escalation rule (either arm splits 2–1 on a positive probe, or negative-probe overfire counts differ by exactly one → extend both arms to 5 for that probe before unblinding; first-round grades stand; the scorer blind-grades only added trials; the scorer's escalation inference is an accepted bounded leak); pass criteria (positive: with-arm ≥2/3 and strictly exceeds without-arm; post-escalation ≥4/5 and strictly exceeds); the ceiling rule (a sealed without-arm ceiling is inconclusive-by-ceiling, never a pass); the calibration gate (at final counts, ON overfire ≤ OFF overfire on every negative probe; an ON excess returns the corresponding clause and the combined block for redesign); aggregation (GO requires all three positive probes to pass AND the gate to hold; fail/inconclusive returns the affected clause and the combined block; other probes' results retained as bounded evidence only); blinding (neutral names, arm map outside trial-visible paths, scorer blind to arm, artifact leak inspection before unblinding, and the subagent-isolation mechanism for every blind role — prompt authors, prompt reviewers, scorer: default context-isolated spawns with the active harness and tool contract named, `fork`-type spawns banned); the integrity model's named residual (the guards close honest slips and hand edits — pilot ids are namespace-enforced, and a stream or results row that does not record exactly its scheduled row blocks — but an arm-map-holding executor forging both a stream and its matching results row for a scheduled id remains outside the mechanical model: that residual trust is stated, not certified away); and the honest bound (Claude-side, same-model-scored — quote the design's weighting line).
2. Obtain an adversarial design review of the prereg — run `review-family:scrutinize` against it with the methodology's design-panel questions (any verdict pre-ordained? any gate unreachable? any divergence cell forbidden by construction? is the motivating premise true?). Patch before data if needed.
3. Re-run `python3 runner.py record` (the sealed keys and any final pre-seal amendments changed the hash inventory — sealing against a stale record fails closed), then run `python3 runner.py seal` and quote the printed hash-record digest in the prereg, then commit the prereg. That commit SHA is the seal. From here: no edits above the seal line, no post-hoc adjustment, no reuse of pilot outputs — and `runner.py record` refuses to run, so a post-seal hash mismatch can only be reported, never re-recorded.

## Task 8 — Sealed probe runs (step 6)

1. Re-run the effective-load canary per tree (against freshly extracted run trees, per Task 4.8) and `python3 runner.py verify`; `runner.py run` re-verifies the sealed inputs itself and refuses to spend any trial on a mismatch.
2. Execute exactly the sealed schedule: `python3 .agents/scratch/skill-use-probes/runner.py run` (the executor acts as arm-map holder; re-invocation is safe — existing streams are never re-executed or overwritten, and a stream counts as done only when its results-index row records exactly its scheduled row: `run` hard-stops on a stream with no matching row. An interrupted batch can leave at most one such orphan — results merge per trial — resolved by appending an explicit invalid row for that trial to `results-index.json` (`valid: false`, `why: orphaned stream — interrupted batch`), never by overwriting or deleting the stream; `runner.py extend` then derives its replacement). Invalid trials (roster/init mismatch; in-session seam never reached, detected mechanically via the row's `seam_skill` — seam probe and N2 alike; CLI version change) are re-run symmetrically as replacement rows per the sealed Task-4.7 derived-row rule (`runner.py extend` derives them; then `runner.py run <new trial ids>`) and invalidity rates reported; a mid-run `claude` version change invalidates the affected trials.
3. Blind grading: first re-run `python3 runner.py verify` (a post-batch mismatch invalidates the affected trials before any grading), then emit the stripped per-trial packets with `python3 runner.py packets` (final text plus the mechanical takes list under neutral trial ids — no tree names, no raw streams, no arm map) and hand the scorer (a fresh subagent under the Task-5 isolation rule: default context-isolated spawn, never `fork`-type) only those packets and the sealed observable rules. The scorer returns `grades.json` as offer judgments only — `{trial_id: {"offers": [<skill>, ...]}}`, an empty list when nothing is offered, each offer a bare skill name exactly as spelled in the fixture roster (the sealed vocabulary pin; the runner rejects slash tokens, case drift, and prose); the packet's mechanical takes list rides along as context so a report of work already done is not misread as a proposed handoff — never takes as grades, and never pass/overfire, which derive from the sealed keys at tally. Inspect the packets for arm/intent leaks before unblinding.
4. `python3 runner.py tally` scores via the sealed keys and applies the escalation rule, printing EXTEND flags and the pending derived trial ids before any per-arm detail — and printing nothing at all while any valid first-round trial lacks a grade, any grade sits on an invalid trial, or `schedule-extensions.json` differs from the runner's own derivation; if escalation fires, run `python3 runner.py extend` (the runner derives the rows itself — never hand-append), run only the added ids (`runner.py run <added trial ids>`), blind-grade only those, re-tally, then unblind.
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
  count="$(grep -c '^## Skill Use$' "$t" || true)"
  if [ "$count" -ne 1 ]; then
    echo "DRIFT: $t has $count '## Skill Use' headings (need exactly 1)" >&2; fail=1; continue
  fi
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

Replace the `CANON` placeholder line with the Task-2 final text before committing. The quoted heredoc is load-bearing: the contract text contains apostrophes ("don't", "skill's") that break a single-quoted assignment, and command substitution strips trailing newlines symmetrically with the `$(extract …)` side of the comparison. A trailing-newline mismatch is still the classic failure; test both directions (run it green, then temporarily perturb one file, see it fail, restore), and include the duplicate-section perturbation: append a second `## Skill Use` section near the end of one target and confirm the heading-count check flags it — the extractor alone reads only the first section, so without the count guard a stale later duplicate would pass.
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

1. `skills/diagnose/SKILL.md` — body exit to `tdd`. Insert at the start of Phase 5, before "Write the regression test **before the fix**…" (line 122):

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

8. `plugins/review-family/skills/scrutinize-skill/SKILL.md` — body exit to `behavior-smoke-test` (source-complete, publish-gated: bump `plugins/review-family/.claude-plugin/plugin.json` from `0.8.0` to `0.9.0` and add a dated `0.9.0` section to `plugins/review-family/CHANGELOG.md` describing this exit, in this task's commit; Class-B publish — Codex republish, mirror — stays deferred until JP's ask, and from this commit until that ask the SessionStart `codex-plugins-sync.sh --check` canary reports `NOT-INSTALLED: review-family@0.9.0`, an expected state per the standing gate, never to be repaired by publishing). Append to the Output section, after the "Findings are argued hypotheses…" paragraph (line 98):

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

11. Pre-commit checks, inline: run `python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py` on each of the ten skill dirs (the known "unexpected key" false positive on documented-valid fields is accepted; anything else is real), parse the bumped manifest (`python3 -m json.tool < plugins/review-family/.claude-plugin/plugin.json`), then `git diff --check`. Fix failures, then commit the ten skill files plus the review-family manifest and changelog in one commit (`feat(skills): seed skill-use composition exits; bump review-family to 0.9.0`). Task 15 re-runs the full ladder across all edited surfaces.

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
[ ! -x scripts/check-skill-use-contract.sh ] || scripts/check-skill-use-contract.sh  # absent (and skipped) only on a Decision-A NO-GO
git diff --check
```

Also parse both hook JSON files (`python3 -m json.tool < .codex/hooks.json`), confirm every path referenced by edited surfaces exists, and re-run any skill's `agents/openai.yaml` parse where that file exists. Treat `quick_validate.py`'s known false-positive ("unexpected key" on documented-valid fields) as accepted; any other failure is real. Structural green does not replace Task 13.
3. Failures found here are fixed and landed as a focused follow-up commit (e.g. `fix(skills): repair validation-ladder findings`); the Task 12 unit is not done until this ladder is green, including that follow-up. Never waive.

## Task 16 — Watch (step 15; record, don't act)

No action now beyond recording: the watch reads at the 2026-08-01 ledger re-read (suffix-aware matching mandatory). Pre-named trigger: unwanted mid-task fires of expensive-by-design lanes (`skill-squad`, `methodology-critique`, `synapsis`, `deep-research`). Also watch seam-handoff sequences, permissioned offers, automatic fan-out attempts, and JP corrections. Request-time silence recurrences read as terrain behavior, not contract failure. Confirm the ledger-entry text (Task 14) names this checkpoint, then close out: report branch state and remaining JP-gated residue (Class-B publish, push).

## Plan notes (self-review + outside view)

Reference class: a pre-registered, blinded ON/OFF evaluation harness plus an always-loaded contract landing, in this repo — the judgment-trust apparatus arc (tests 1–5) and the Era-86 seal are the base rate. What this class reliably required that a spec-only decomposition omits, now built in: pilot channels come back empty/ambiguous/ceilinged and force redesign loops (Task 6.3); first-draft trial prompts leak vocabulary and must be regenerated fresh, never patched (Task 5); harness mechanics (stream-json shape, auth, version drift) eat a preflight (Task 4.1, the version pin, the amendable runner); and canary scripts fail on trailing-newline byte mismatches (Task 10.2's perturb-test). Known bounds, stated rather than certified away: `runner.py`'s `system/init` roster-field name, the `tool_use`/`tool_result` shapes its takes and seam-completion checks parse, and the Codex probe's CLI flags are written against current versions and may need pre-seal adaptation; the fixture and trial prompts are constitutionally authored at build time (blind-eval discipline), so this plan fixes their required properties, not their text. The base rate is a prior, not a guarantee — this plan is debiased against the apparatus arc's failures, not certified complete.
