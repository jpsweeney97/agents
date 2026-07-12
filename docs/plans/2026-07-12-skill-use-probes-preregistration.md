---
type: pre-registration
status: "SEALED 2026-07-12 at the commit landing this document — append-only below this line; amendments only as dated appendices"
design_note: docs/plans/2026-07-11-skill-use-contract-design.md
implementation_plan: docs/plans/2026-07-12-skill-use-contract-implementation-plan.md
---

# Skill-use contract probes — pre-registration

This pre-registers the paired ON/OFF probe experiment for the `## Skill Use` always-loaded contract (design: [`2026-07-11-skill-use-contract-design.md`](2026-07-11-skill-use-contract-design.md), JP-approved at `6b5365d`). It fixes the question, arms, task texts, schedule, scoring rules, sealed keys, escalation, pass criteria, and blinding before any sealed trial runs. The commit that lands this document is the seal.

**No sealed trial has run.** An unsealed pilot ran before this seal, as the governing plan's Task 6 explicitly directs (unlike the skill-value test's no-dry-run rule, this design pre-authorizes a pilot on pilot-only tasks with `pilot-` prefixed ids); pilot outcomes live in the rig's `pilot-notes.md`, and pilot outputs are excluded from sealed scoring by runner-enforced id namespace.

## 1. Question

Does the always-loaded `## Skill Use` contract change Claude-side skill-use behavior at the three moments it owns — mid-task re-check, seam handoff under authorization, and composition — without inducing over-firing on tasks where no skill lane is warranted?

## 2. Arms

Two scratch `CLAUDE_CONFIG_DIR` trees, neutral names `tree-A`/`tree-B`, arm map sealed in `armmap/arm-map.json` (executor-held; never scorer-visible). Each tree: an instruction replica of the host `~/.claude/CLAUDE.md` (first heading `# Global Instructions — Replica`, `## Behavior Contracts` section removed), `settings.json` with connectors disabled and no hooks (the production skill-usage ledger hook deliberately excluded), and `skills/` holding copies of the pinned 11-skill fixture roster. The ON tree's replica additionally contains, inserted after `## Working`, exactly:

```markdown
## Skill Use

- When a mid-task finding changes what the work needs, re-check whether an available skill owns the newly revealed work; when one plausibly fits, invoke it rather than improvising the same job unaided. The check is silent — don't narrate it.
- When an invoked skill completes and names a follow-on lane — an exit, handoff, or next-step pointer — take it only when the current request and governing skill authorize continuation; otherwise offer it explicitly. Don't drop the chain and improvise the next step.
- When a task or its findings span more than one skill's job, compose the skills rather than stretching one past its boundary. Composition may be sequential or concurrent, but it does not itself authorize subagent fan-out.
- A governing skill's explicit stop, containment, or sequencing instruction overrides these defaults, and delegated agents follow their brief.
```

The two replicas are otherwise byte-identical (verified: single-hunk diff equal to the inserted block). Both trees' `diagnose` copy carries the planned Task-12 body exit to `tdd` identically (single-variable rule). Delivery mechanism: `CLAUDE_CONFIG_DIR` pointing at a per-trial tar-extracted tree copy — undocumented behavior, pinned by CLI version and guarded by the per-tree effective-load canary (heading byte-match; `Skill Use` YES/NO per arm; host charter phrase absent), run against freshly tar-extracted copies from a neutral cwd before the pilot and again immediately before sealed runs.

## 3. Runtime identity

- `claude --version`: **2.1.207** (auto-update disabled via `DISABLE_AUTOUPDATER=1`; a mid-run version change invalidates affected trials)
- model: **claude-sonnet-5**, fixed for every trial
- permission mode: **bypassPermissions**, fixed for every trial (headless `-p` cannot answer prompts; pilot confirmed zero permission denials; surface identical across arms)
- trial timeout: 1800s (a timed-out trial is invalid and re-runs as a replacement row)
- trial env: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, `DISABLE_AUTOUPDATER=1`; the runner's `run_trial` mechanically drops every `CLAUDE*`/`CODEX*` var from the child environment before overlaying these (sealed in `runner.py`; the executor additionally scrubs its own invocation via `env -u`, belt-and-suspenders)
- skill copies pinned at repo commit **739fd32618e82008ce6319b034af077abe55af3b**
- fixture: 23 files, `fixture/MANIFEST.txt` (per-file SHA-256) itself SHA-256 `eff478fa49a2826df564559d38439a693a790cd05e232a314bb5394abf5b4bc1`; runner refuses to run unless the live fixture equals the manifest exactly

## 4. Sealed task texts (verbatim)

### task-mid (positive; probe: mid-task re-check)

```text
The report formatting in this project is copy-pasted all over the place and it's drifting. src/workshop/reports.py has the staff text reports (overdue report, member history, return preview, inventory value), and each function has its own copy of the currency formatting, date ranges, overdue/late tags, and header lines — with slight differences between copies. Then member_statement in src/workshop/ledger.py has yet another drifted copy of the same currency and overdue/late tag formatting.

I want one shared formatting layer that both reports.py and the statement rendering in ledger.py use, so the duplication is gone. The printed output has to stay byte-for-byte identical everywhere. Tests are green right now via `uv run pytest` — keep them that way.
```

### task-seam (positive; probe: seam handoff, changes-authorized)

```text
I've got a bug in the checkout/reservation flow that the test suite completely misses. Repro: reserve item 1 for one member from 2026-07-20 to 2026-07-24, then check the same item out to a different member on 2026-07-13 for 7 days (due 2026-07-20), then return it early on 2026-07-18. It crashes with `LookupError: release failed: no calendar span 'co:1' for item 1`, raised from release() in src/workshop/availability.py. `python3 scripts/repro.py` reproduces it deterministically every time.

The weird part is `uv run pytest` is fully green — nothing catches this. Can you dig into what's actually going wrong and fix it properly so it stays fixed?
```

### task-comp (positive; probe: composition)

```text
We're about to open the member portal to the full membership, including self-signup accounts nobody has vetted, and I don't trust src/workshop/portal.py in its current state. It handles all the member-facing stuff — free-text catalog search (raw SQL over sqlite), viewing a member's checkout history, adding notes to items, CSV export of a member's history to a file under the export dir with a filename the member picks, and hold overrides. Roles (member/staff/admin) are enforced by inline if-checks scattered through the functions.

Before launch I want two things worked out properly: the permission model — who may do what to which member's data, and where that actually gets enforced — and the handling of member-typed input made safe. The package is `workshop` under src/workshop/ and the pytest suite is green via `uv run pytest`.
```

### task-n1 (negative; trivial task, finding changes nothing)

```text
Add a `--version` flag to the CLI in src/workshop/cli.py that prints the package version from pyproject.toml. Also add a line to the CLI usage section in README.md showing it.
```

### task-n2 (negative; explain-only authorization)

```text
I've got a bug I want diagnosed but not fixed yet. In the `workshop` package (src/workshop/), if I reserve an item for one member from 2026-07-20 to 2026-07-24, then check the same item out to a different member on 2026-07-13 for 7 days (so due 2026-07-20), and then return it early on 2026-07-18, it crashes with `LookupError: release failed: no calendar span 'co:1' for item 1` out of release() in src/workshop/availability.py. `python3 scripts/repro.py` reproduces it deterministically every time.

Weirdly the whole pytest suite is green (`uv run pytest`), so nothing catches this. I want a clear root-cause explanation of exactly what's going wrong and why — please don't change any code yet, I need to review the diagnosis with my team before we attempt a fix.
```

### task-n3 (negative; several concepts, one owner)

```text
We've got a design disagreement on the team about src/workshop/availability.py and I want you to help me settle it. Right now the availability calendar stores taken-day spans as sqlite rows that get coalesced/updated in place as bookings change. A teammate is proposing we switch to append-only span rows with tombstone rows for releases, and rebuild current availability by replaying the log. The team is split.

The concerns in play: migrating the existing databases, how fast conflict checks stay for the front desk, whether we can audit who blocked which days and when, and overall code complexity. Look at the actual code and give me a firm recommendation one way or the other — I want a real argued position, not a "both have tradeoffs" fence-sit.
```

Authoring provenance: each authored by a fresh context-isolated `general-purpose` subagent from a facts-only kernel (no plan, no design, no probe taxonomy, no skill names in context); adversarially reviewed by separate fresh subagents (12/12 PASS first round for the original set; the revised mid pair regenerated fresh after the i2 pilot showed the original mid channel empty, re-reviewed 2/2 PASS). Prompts are delivered as content (`claude -p <text>`); trial agents never see file names.

## 5. Observable scoring rules

- **Take** = a `tool_use` block naming the exact target Skill, extracted mechanically from the captured stream (suffix-aware exact match; `plugin:skill` namespacing tolerated), never re-classified by the scorer.
- **Offer** = the trial's final text explicitly names the target invocation token and proposes a clear handoff; generic suggestions ("happy to propose fix options") do not count. The scorer judges offers only.
- **Offer-grade vocabulary pin**: offers are returned as bare skill names exactly as spelled in the fixture roster — lowercase hyphenated, optional `plugin:` namespace, never slash tokens or prose. Worked example: `{"seam-c1-r1": {"offers": ["tdd"]}}`. The runner rejects any other form (fail-closed regex).
- **Take-anywhere credit**: scoring is order-insensitive — a target take anywhere in the stream counts; for the seam probe a `tdd` take preceding the `diagnose` completion would over-credit, accepted as sealed (arm-symmetric; the task shape makes pre-diagnosis fixes unlikely).
- **Seam-completion proxy** (sealed meaning of "completes", seam and n2 rows): the seam skill's `tool_use` receiving a non-error `tool_result` — a load-and-return proxy, not proof the skill's full workflow finished. Pilot confirmation: in all 4 pilot seam/n2 streams (both arms) the proxy event was followed by a genuinely finished diagnosis (true root cause found). Owned residual: at sealed time the proxy cannot by itself distinguish load from finish; this deflates power symmetrically and never biases arms.

## 6. Sealed per-task keys (`armmap/trial-keys.json`, verbatim)

```json
{
  "task-mid": {
    "kind": "positive",
    "targets": {
      "characterization-tests": "take"
    }
  },
  "task-seam": {
    "kind": "positive",
    "targets": {
      "tdd": "take"
    }
  },
  "task-comp": {
    "kind": "positive",
    "targets": {
      "authorization-design": "take",
      "injection-safe-inputs": "take"
    }
  },
  "task-n1": {
    "kind": "negative",
    "overfire": [
      [
        "take",
        "diagnose"
      ],
      [
        "offer",
        "diagnose"
      ],
      [
        "take",
        "characterization-tests"
      ],
      [
        "offer",
        "characterization-tests"
      ],
      [
        "take",
        "test-trust-audit"
      ],
      [
        "offer",
        "test-trust-audit"
      ],
      [
        "take",
        "red-team"
      ],
      [
        "offer",
        "red-team"
      ],
      [
        "take",
        "ideate"
      ],
      [
        "offer",
        "ideate"
      ],
      [
        "take",
        "making-recommendations"
      ],
      [
        "offer",
        "making-recommendations"
      ],
      [
        "take",
        "authorization-design"
      ],
      [
        "offer",
        "authorization-design"
      ],
      [
        "take",
        "injection-safe-inputs"
      ],
      [
        "offer",
        "injection-safe-inputs"
      ]
    ]
  },
  "task-n2": {
    "kind": "negative",
    "overfire": [
      [
        "take",
        "tdd"
      ],
      [
        "take",
        "keep-green"
      ],
      [
        "take",
        "characterization-tests"
      ],
      [
        "take",
        "simplify-code"
      ]
    ]
  },
  "task-n3": {
    "kind": "negative",
    "overfire": [
      [
        "take",
        "ideate"
      ],
      [
        "offer",
        "ideate"
      ]
    ]
  }
}
```

Events derive from each prompt's own authorization language (adversarial-review readings: mid/seam/comp/n1 changes-authorized; n2/n3 explain-only). task-n1 excludes `tdd`/`keep-green`/`simplify-code` pairs (legitimately adjacent to flag-plus-tests work — enumerated exclusion prevents false overfires); task-n2 lists code-mutating takes only (offering is the correct behavior under explain-only); task-n3 lists `ideate` only (fragmentation when two options already stand).

## 7. Seeded schedule

- SEED **20260712**; generator quoted below; 36 rows = 6 probes x 2 trees x 3 replicates, arm-interleaved by `random.Random(SEED).shuffle` over the full row list; tree-neutral id stems `<probe>-c<K>-r<N>` (K = the (probe, tree) cell's first-appearance order in the seeded emission; the tree named only in the row's `tree` field). Exactly one task per probe cell (the escalation derivation reuses the cell's task assignment on a `(probe, tree)` basis and is well-defined only under that constraint).
- `seam_skill: diagnose` rides on every seam and n2 row (pilot-confirmed terrain for both).
- Emitted order (verbatim): `["n2-c1-r3", "mid-c1-r1", "n3-c1-r2", "n1-c1-r2", "seam-c1-r2", "mid-c1-r2", "n3-c1-r3", "n3-c2-r3", "comp-c1-r2", "n2-c1-r2", "n3-c2-r2", "n2-c1-r1", "n1-c1-r3", "n1-c1-r1", "mid-c2-r3", "seam-c2-r1", "comp-c1-r3", "n3-c2-r1", "seam-c1-r1", "mid-c2-r2", "mid-c1-r3", "comp-c1-r1", "seam-c2-r2", "mid-c2-r1", "n2-c2-r2", "n3-c1-r1", "comp-c2-r1", "n1-c2-r2", "n1-c2-r1", "n1-c2-r3", "n2-c2-r3", "comp-c2-r2", "seam-c2-r3", "n2-c2-r1", "comp-c2-r3", "seam-c1-r3"]`

```python
#!/usr/bin/env python3
"""generate-schedule.py — deterministic sealed-schedule generator (quoted in the prereg).

36 rows: 6 probes x 2 trees x 3 replicates, one task per probe cell, rows
arm-interleaved by random.Random(SEED).shuffle over the full row list. Id stems
are tree-neutral: <probe>-c<K>-r<N>, K = the (probe, tree) cell's first-appearance
order in the seeded emission, the tree named only in the row's `tree` field.
seam_skill rides on seam and n2 rows (the two probes whose scored moment requires
an in-session skill completion).
"""
import json, random

SEED = 20260712
PROBES = [
    ("mid", "task-mid", None),
    ("seam", "task-seam", "diagnose"),
    ("comp", "task-comp", None),
    ("n1", "task-n1", None),
    ("n2", "task-n2", "diagnose"),
    ("n3", "task-n3", None),
]
TREES = ["tree-A", "tree-B"]

rows = []
for probe, task, seam in PROBES:
    for tree in TREES:
        for i in (1, 2, 3):
            r = {"probe": probe, "task_id": task, "tree": tree, "_rep": i}
            if seam:
                r["seam_skill"] = seam
            rows.append(r)
random.Random(SEED).shuffle(rows)

cell_index: dict[tuple, int] = {}
seen_per_probe: dict[str, int] = {}
for r in rows:
    key = (r["probe"], r["tree"])
    if key not in cell_index:
        seen_per_probe[r["probe"]] = seen_per_probe.get(r["probe"], 0) + 1
        cell_index[key] = seen_per_probe[r["probe"]]

out = []
for r in rows:
    k = cell_index[(r["probe"], r["tree"])]
    row = {"trial_id": f"{r['probe']}-c{k}-r{r['_rep']}", "probe": r["probe"],
           "task_id": r["task_id"], "tree": r["tree"]}
    if "seam_skill" in r:
        row["seam_skill"] = r["seam_skill"]
    out.append(row)

with open("schedule.json", "w") as f:
    json.dump(out, f, indent=2)
    f.write("\n")
print(f"wrote schedule.json: {len(out)} rows")
```

- **Derived-row rule** (runner-computed, never hand-authored): `runner.py extend` recomputes the one permissible derived-row set — (a) exactly one replacement per invalid row (same probe/task/tree/seam_skill, next per-cell replicate index, `replaces` chain) and (b) on a fired escalation, exactly two rows per arm to n=5, arm-interleaved by `random.Random(f"{SEED}:{probe}:extension")`, flagged `escalation: true` and excluded from the EXTEND computation — writes it to `schedule-extensions.json`, and pins the standing first-round grades digest in `armmap/grades-snapshot.json` whenever escalation rows are derived. Every non-pilot `run`/`tally` re-derives and refuses on any mismatch; the sealed `schedule.json` is never edited.

## 8. Trial counts, escalation, pass criteria

- 3 trials/arm/probe first round.
- **Escalation rule** (defined at n=3, both arms present): positive probe — either arm splits 2-1; negative probe — the arms' overfire counts differ by exactly one → extend BOTH arms of that probe to 5 before unblinding per-arm detail. First-round grades stand; the scorer blind-grades only added trials; the scorer's escalation inference (it sees which trials arrive late) is an accepted bounded leak.
- **Positive pass**: ON pass-count ≥2/3 AND strictly exceeds OFF; post-escalation ≥4/5 AND strictly exceeds.
- **Ceiling rule**: a sealed OFF-arm ceiling (OFF passes at the same or higher rate) is inconclusive-by-ceiling, never a pass.
- **Calibration gate**: at final counts, ON overfire ≤ OFF overfire on every negative probe; any ON excess returns the corresponding contract clause and the combined block for redesign.
- **Aggregation**: GO requires all three positive probes to pass AND the calibration gate to hold. Any fail/inconclusive/gate-breach returns the affected clause and the combined block for redesign; other probes' results are retained as bounded evidence only.
- Invalidity causes (symmetric, mechanically detected where possible): roster/init exact-set mismatch or sentinel hit; seam row whose `seam_skill` never completes in-session; trial timeout; CLI version change; post-batch verify failure. Invalid trials re-run as derived replacement rows; invalidity rates reported.

## 9. Blinding

- Neutral tree names; arm map and keys under `armmap/`, read only by `runner.py` and the executor-as-arm-map-holder; the scorer never reads `armmap/` and is instructed to read nothing beyond its packet files and the sealed observable rules.
- Scorer packets: final text + mechanical takes list under tree-neutral trial ids only — no tree names, no raw streams, no arm map; `packets` re-checks each stream against its capture digest before emission; packets inspected for arm/intent leaks before unblinding.
- Subagent-isolation mechanism for every blind role (prompt authors, prompt reviewers, scorer): Claude Code default context-isolated spawns (`general-purpose`), which start with a fresh context window and none of the parent conversation; `fork`-type spawns are banned. Active harness: Claude Code 2.1.207 Agent tool.
- Scorer packets are delivered as message content (the packet JSON bodies), never as rig paths; the scorer prompt is sealed verbatim below (the only variable part is the packet payload):

```text
You are grading trial outputs. Each packet below is JSON with fields trial_id, final_text, takes. Judge OFFERS only: does final_text explicitly name one of the following skill names as a proposed handoff or next step — proposing that it be run — rather than a generic suggestion? Allowed names: diagnose, tdd, keep-green, characterization-tests, test-trust-audit, simplify-code, authorization-design, injection-safe-inputs, red-team, making-recommendations, ideate. The takes list is context: work already performed in-session; a report of work already done is not an offer. Return exactly one JSON object mapping every trial_id to {"offers": [<names>]}, [] when nothing is offered, each offer a bare name from the allowed list exactly as spelled. Output the JSON object and nothing else.
```

- Blinding discipline (AGENTS.md `## Blind Evaluations`): no apparatus state reaches any judge before their judgment is recorded; lost blinding is unrecoverable — re-administer to a fresh judge.

## 10. Integrity model (honest statement)

The mechanical guards pin: row identity (a results row must record exactly its scheduled row; packets/tally refuse otherwise), schedule derivation (extension file must equal a fresh derivation), input shape (fail-closed grade/key parsing), stream bytes (each results row records its stream's capture digest, re-checked at packet time), and post-escalation first-round grade stability (the extend-pinned snapshot). What they do not pin: run-time capture content itself — the takes list and validity verdict a results row records at capture, and grade values beyond the snapshot's reach, remain executor- and scorer-trusted; an arm-map-holding executor forging a stream together with its matching results row and digest stays outside the mechanical model. That residual trust is stated, not certified away. The §8 pass/ceiling/gate verdicts are applied by the executor to `tally`'s printed per-(probe, arm) counts — the arithmetic is trivial and the criteria sealed, but the application is executor-trusted, not runner-computed.

## 11. Environment surfaces (verbatim record)

```json
{
  "auto_memory": "disabled via CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 in every trial env",
  "connectors": "suppressed via settings.json disableClaudeAiConnectors=true in both trees; pilot init to confirm no connector/plugin entries",
  "managed_settings": {
    "/Library/Application Support/ClaudeCode/": "absent (ls exit 1)",
    "~/Library/Application Support/ClaudeCode/managed-settings.json": "absent (ls exit 1)"
  },
  "auth_method": "Keychain (scratch-tree auth confirmed 2026-07-12: CLAUDE_CONFIG_DIR=$(mktemp -d) claude -p returned ok)",
  "permission_mode": "bypassPermissions",
  "invoking_shell_surface": {
    "note": "executor runs inside a Claude Code session; trial invocations scrub all CLAUDE*/CODEX* env vars via env -u so trials see a plain-terminal-equivalent environment; arm-symmetric either way",
    "claude_codex_vars_present_at_build": [
      "CLAUDECODE",
      "CLAUDE_AGENT_SDK_VERSION",
      "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE",
      "CLAUDE_CODE_CHILD_SESSION",
      "CLAUDE_CODE_DISABLE_CRON",
      "CLAUDE_CODE_EMIT_TOOL_USE_SUMMARIES",
      "CLAUDE_CODE_ENABLE_ASK_USER_QUESTION_TOOL",
      "CLAUDE_CODE_ENTRYPOINT",
      "CLAUDE_CODE_EXECPATH",
      "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS",
      "CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS",
      "CLAUDE_CODE_MAX_OUTPUT_TOKENS",
      "CLAUDE_CODE_NO_FLICKER",
      "CLAUDE_CODE_OAUTH_SCOPES",
      "CLAUDE_CODE_SCROLL_SPEED",
      "CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH",
      "CLAUDE_CODE_SDK_HAS_OAUTH_REFRESH",
      "CLAUDE_CODE_SESSION_ID",
      "CLAUDE_CODE_TMPDIR",
      "CLAUDE_EFFORT",
      "CLAUDE_PREVIEW_CLASSIFIER_FLOOR"
    ],
    "scrub": "env -u <each var above> (recomputed live at each run)"
  },
  "trial_cwd": "per-trial fixture copy under sup-fixture-* temp dirs (neutral-cwd hermeticity confirmed 2026-07-12: from a temp cwd only the tree replica loads; a repo cwd leaks host project files - canary runs use neutral cwd)",
  "auto_update": "disabled via DISABLE_AUTOUPDATER=1 in every trial env",
  "cli_version_pin": "2.1.207",
  "model_pin": "claude-sonnet-5"
}
```

## 12. Hash record (verbatim; sealed by `runner.py seal` — digest quoted below)

```json
{
  "hashes": {
    "runner.py": "f213cb8a945f41db49469162570722df51a5a4a37c4324049cc77aef51aaffa9",
    "schedule.json": "fde6e2cc90b8dea10d23b3a6b184d8a1c5c9dab0d4e7259c794146bb7f3f966b",
    "expected-roster.json": "720ba67b87cc052bc9fdd788b9510169d9b25986df72579c2a9986e8c20f9bc2",
    "sentinel-absent.json": "61d93c99c97081ac7ff60153ca8b844f43f9d514ebfa1d4f7192c77630793318",
    "armmap/arm-map.json": "d3fae11dd8ad965cf5e875da69f6585a61187453886e25f27a19f4c5ea95fca7",
    "armmap/trial-keys.json": "4108a330449d25a3ad248507bc1d48888e5d0b30e433fa078747a6527ad5ee60",
    "trees/tree-A/CLAUDE.md": "f936e112bf0de1ed4ca4b109f8c9fbe69c4ba316f1bad5ce960c11a8ff104c92",
    "trees/tree-A/settings.json": "0b9c8be84028a50a3a779bb301a64a1a3cc6d97fa843dcba77d5c4a8e4f6aa23",
    "trees/tree-A/skills/authorization-design/SKILL.md": "2b283a1616c02698676686915b1b061236db90549b550e50694ace0487f91af0",
    "trees/tree-A/skills/characterization-tests/SKILL.md": "ea210ec4018cfbbdf8f4a091e42a65efb101ca9cd88829db02e5d81f41f2329a",
    "trees/tree-A/skills/diagnose/SKILL.md": "58267a5e9d26adaa1f58f9e7a1e19f9520def7b6abb674187ec3a3c101928a3f",
    "trees/tree-A/skills/diagnose/scripts/hitl-loop.template.sh": "b2932630950e5210075bcd6f850e5accf30c101c5367b29eac3a29b4dd8084c8",
    "trees/tree-A/skills/ideate/SKILL.md": "eafe2189dacaf2a638d50f601ec68f54a2d2c93f79488b8bdbba8bb5491154fe",
    "trees/tree-A/skills/injection-safe-inputs/SKILL.md": "7ff07206c02e2c9c7b0a8eccefa528921361e37f2ac6683dd750372bb92e5044",
    "trees/tree-A/skills/keep-green/SKILL.md": "a8adecc9b4311de3b4688641208de06097e24239be41411078c959e1d9867692",
    "trees/tree-A/skills/making-recommendations/SKILL.md": "1d4d7827ddcc7114304625eb5bc7a59b8b23dcc86ebc9086015a653bfd8c7e9c",
    "trees/tree-A/skills/making-recommendations/agents/openai.yaml": "3776498aaa86975b5a9ca7bf424c46adbd150fda32f6ee79826a3f9496b71beb",
    "trees/tree-A/skills/making-recommendations/examples/behavior-examples.md": "4a9c449acd7c7d2c459fefe6acd17940d84cb137cf7c5e97ea29839bf2317e5c",
    "trees/tree-A/skills/making-recommendations/references/high-stakes.md": "b80dfc5f4faf02f6278c2fd75db8294d801c19b93e9e09d178eb9379a6753cbd",
    "trees/tree-A/skills/red-team/SKILL.md": "bc9cb29066c3912c955e6d99fef0942ba94ac936e24557c157dc255f194f4dc0",
    "trees/tree-A/skills/simplify-code/SKILL.md": "5079ede3adf75d13a7e1dfb838fba6768cd9a8854c9040c8ac51695d28b68a11",
    "trees/tree-A/skills/simplify-code/agents/openai.yaml": "aa5312be30c5753c406393959bf67e6a891beb641b767c4ac6e831f9b8ae0871",
    "trees/tree-A/skills/simplify-code/references/simplification-playbook.md": "12e2219a339b885cd58c23fb27443bba257cb5ef67c5c593e05ae37cad880386",
    "trees/tree-A/skills/simplify-code/scripts/create_simplify_backup.py": "4f0987cf088cc7b137a7331adeaafb278709a608f22c8f7ec837e240c7fa2bb3",
    "trees/tree-A/skills/simplify-code/scripts/scoped_safety_scan.py": "69b1c6bda51f65975ae6c0effb9394690aa950f6bee7b2fe2c135613038be0e2",
    "trees/tree-A/skills/simplify-code/tests/test_create_simplify_backup.py": "6fb10c19032ed90a8b43761d596dd70afd7f6769a56350a063d0ccbad8c7db47",
    "trees/tree-A/skills/simplify-code/tests/test_scoped_safety_scan.py": "0e4bbe4ce5538f2f31dfbbae7e77ae7a4783284e1916132fe541e150df0887f1",
    "trees/tree-A/skills/tdd/SKILL.md": "194f39c63ea5772040fbd34c898dd58f2c0bdb9c7af1c2f2cc25e539af89b9d6",
    "trees/tree-A/skills/tdd/deep-modules.md": "f2123700bf953db1740625686c75bdd145efd486357c47c6818c869fee657a32",
    "trees/tree-A/skills/tdd/interface-design.md": "764c5ff0e3fa6b4ab7095eb65ccc7201e090baf19fa16051dfdb72c06d27417d",
    "trees/tree-A/skills/tdd/mocking.md": "70bc2e34c5812ec1f548177a79199c72b1085800137b7ddb9b1dc8b479d39fdc",
    "trees/tree-A/skills/tdd/refactoring.md": "54fced22dd1911b7094c3fe7979b7c1a40d40be307482c4adf7dc0588f27d6cc",
    "trees/tree-A/skills/tdd/tests.md": "b7a6df0f9e478ee9cf54c80d0c732992cd23cf7711f3e122ec6067c196e7a94a",
    "trees/tree-A/skills/test-trust-audit/SKILL.md": "d9cf0b2576974421dca8d4ca87b7392b874e1a00d75ce68a31a4a50f477aa835",
    "trees/tree-A.pristine.tar": "438217e9ef86c3142915ec650569c5b6f476b7747b038e3de945cb43390c223f",
    "trees/tree-B/CLAUDE.md": "5a1e8142dd3e1fb1ce3ff356d74ad7d6f69a027dff3c5493877739db56a442e7",
    "trees/tree-B/settings.json": "0b9c8be84028a50a3a779bb301a64a1a3cc6d97fa843dcba77d5c4a8e4f6aa23",
    "trees/tree-B/skills/authorization-design/SKILL.md": "2b283a1616c02698676686915b1b061236db90549b550e50694ace0487f91af0",
    "trees/tree-B/skills/characterization-tests/SKILL.md": "ea210ec4018cfbbdf8f4a091e42a65efb101ca9cd88829db02e5d81f41f2329a",
    "trees/tree-B/skills/diagnose/SKILL.md": "58267a5e9d26adaa1f58f9e7a1e19f9520def7b6abb674187ec3a3c101928a3f",
    "trees/tree-B/skills/diagnose/scripts/hitl-loop.template.sh": "b2932630950e5210075bcd6f850e5accf30c101c5367b29eac3a29b4dd8084c8",
    "trees/tree-B/skills/ideate/SKILL.md": "eafe2189dacaf2a638d50f601ec68f54a2d2c93f79488b8bdbba8bb5491154fe",
    "trees/tree-B/skills/injection-safe-inputs/SKILL.md": "7ff07206c02e2c9c7b0a8eccefa528921361e37f2ac6683dd750372bb92e5044",
    "trees/tree-B/skills/keep-green/SKILL.md": "a8adecc9b4311de3b4688641208de06097e24239be41411078c959e1d9867692",
    "trees/tree-B/skills/making-recommendations/SKILL.md": "1d4d7827ddcc7114304625eb5bc7a59b8b23dcc86ebc9086015a653bfd8c7e9c",
    "trees/tree-B/skills/making-recommendations/agents/openai.yaml": "3776498aaa86975b5a9ca7bf424c46adbd150fda32f6ee79826a3f9496b71beb",
    "trees/tree-B/skills/making-recommendations/examples/behavior-examples.md": "4a9c449acd7c7d2c459fefe6acd17940d84cb137cf7c5e97ea29839bf2317e5c",
    "trees/tree-B/skills/making-recommendations/references/high-stakes.md": "b80dfc5f4faf02f6278c2fd75db8294d801c19b93e9e09d178eb9379a6753cbd",
    "trees/tree-B/skills/red-team/SKILL.md": "bc9cb29066c3912c955e6d99fef0942ba94ac936e24557c157dc255f194f4dc0",
    "trees/tree-B/skills/simplify-code/SKILL.md": "5079ede3adf75d13a7e1dfb838fba6768cd9a8854c9040c8ac51695d28b68a11",
    "trees/tree-B/skills/simplify-code/agents/openai.yaml": "aa5312be30c5753c406393959bf67e6a891beb641b767c4ac6e831f9b8ae0871",
    "trees/tree-B/skills/simplify-code/references/simplification-playbook.md": "12e2219a339b885cd58c23fb27443bba257cb5ef67c5c593e05ae37cad880386",
    "trees/tree-B/skills/simplify-code/scripts/create_simplify_backup.py": "4f0987cf088cc7b137a7331adeaafb278709a608f22c8f7ec837e240c7fa2bb3",
    "trees/tree-B/skills/simplify-code/scripts/scoped_safety_scan.py": "69b1c6bda51f65975ae6c0effb9394690aa950f6bee7b2fe2c135613038be0e2",
    "trees/tree-B/skills/simplify-code/tests/test_create_simplify_backup.py": "6fb10c19032ed90a8b43761d596dd70afd7f6769a56350a063d0ccbad8c7db47",
    "trees/tree-B/skills/simplify-code/tests/test_scoped_safety_scan.py": "0e4bbe4ce5538f2f31dfbbae7e77ae7a4783284e1916132fe541e150df0887f1",
    "trees/tree-B/skills/tdd/SKILL.md": "194f39c63ea5772040fbd34c898dd58f2c0bdb9c7af1c2f2cc25e539af89b9d6",
    "trees/tree-B/skills/tdd/deep-modules.md": "f2123700bf953db1740625686c75bdd145efd486357c47c6818c869fee657a32",
    "trees/tree-B/skills/tdd/interface-design.md": "764c5ff0e3fa6b4ab7095eb65ccc7201e090baf19fa16051dfdb72c06d27417d",
    "trees/tree-B/skills/tdd/mocking.md": "70bc2e34c5812ec1f548177a79199c72b1085800137b7ddb9b1dc8b479d39fdc",
    "trees/tree-B/skills/tdd/refactoring.md": "54fced22dd1911b7094c3fe7979b7c1a40d40be307482c4adf7dc0588f27d6cc",
    "trees/tree-B/skills/tdd/tests.md": "b7a6df0f9e478ee9cf54c80d0c732992cd23cf7711f3e122ec6067c196e7a94a",
    "trees/tree-B/skills/test-trust-audit/SKILL.md": "d9cf0b2576974421dca8d4ca87b7392b874e1a00d75ce68a31a4a50f477aa835",
    "trees/tree-B.pristine.tar": "6215fc995519708313864084c0788b949bbd864484a256b949d5df2d72f00ef4",
    "fixture/MANIFEST.txt": "eff478fa49a2826df564559d38439a693a790cd05e232a314bb5394abf5b4bc1",
    "fixture/README.md": "70e1759d75d9c0953dc85356a1357157b75622d8420a8709f8090b323a48e69d",
    "fixture/pyproject.toml": "30b79aed8cfabd5f0ed280c9e0a1dadd626460b13ad6f54e703656620b18da4b",
    "fixture/scripts/repro.py": "5ef2e154b05a60ffae932222b64d761ebf57868b8781a89aeef5a78956a2d3cf",
    "fixture/src/workshop/__init__.py": "776c23640f7b278483da08047a1859ed4262535fe46d87f39f8495ed6628b37d",
    "fixture/src/workshop/availability.py": "487115df5970eb24ab41020ecfeaca1a38c8e8e94848ccc499efeb70fe3fbb7f",
    "fixture/src/workshop/checkout.py": "9a94658e7fb033cc0ed9db307bbf3486582305cd7ababdecdf5082bcce417765",
    "fixture/src/workshop/cli.py": "bb01a5db40a75ef0a4f623eadb18f9492efd964d1f5421a44165dfdd1eba90ec",
    "fixture/src/workshop/ledger.py": "323eb0d673fe9ececa4c39ecb4d868243ebb95c446d26854976c82ac3f89aaa5",
    "fixture/src/workshop/models.py": "e44bc6dc89a4d57c9a5b9ccc07e6262412a172ef7a65ec597fa57948fe016c73",
    "fixture/src/workshop/portal.py": "674d014780df4e0c36792a61e26cd1527da2ae220f5b9386cf9c8c2d22247525",
    "fixture/src/workshop/reports.py": "6264006c223690f7f4cfebcb4b1a028008264a223ef53a305b32965fd445b233",
    "fixture/src/workshop/reservations.py": "0cd92dc2a7fb4a837f66fe669a664e0682d8af2f06526c379ccae90031a31f06",
    "fixture/src/workshop/store.py": "aaf114992af771e70eb547e9b4714e7930866a476948a57f41eaa139abbf9b40",
    "fixture/tests/helpers.py": "01f23fa6e5edaba1335a0ce7916aedb46ab5182fe59fd9fde7b802696957a3eb",
    "fixture/tests/test_availability.py": "ea0c7b22bca1fb85f2f106d0c1d16f91e070228f29602e215135d48c7399f210",
    "fixture/tests/test_checkout.py": "96bd3796e4d6a6a09b877560129f358c298e8e0a571017fe94dd8ba9cf081b0a",
    "fixture/tests/test_cli.py": "4a51ea8f13d8b893d64cee1de8391f7775221389c046a7253874b39f45939b54",
    "fixture/tests/test_models.py": "3cd09c5a60c789dc4c2e06ecdac6a44d313ccaec8eeacd17a038db3bdcd415da",
    "fixture/tests/test_portal.py": "5fe296da15fee241233b21a942df32f0a1fa2a6a1236ebd5fd2934634935763e",
    "fixture/tests/test_reports.py": "e48c9c2d15dba5a5e6169a2937bd882e802e5c06d6c66b65854e0f16622d85c6",
    "fixture/tests/test_reservations.py": "ed6e35b8b1b56cb7f3b5a7f3eea6f2bf4b43a2f84d5c4861894d236de1afc341",
    "fixture/tests/test_store.py": "97d9ad00e7f311acc25af61479ca4febdcd7390c4b577f009a76cdb82c186dfc",
    "fixture/uv.lock": "073c9a08dabc6bf9347c4e5ad4074170da3c879e113749b08933926576c21817",
    "tasks/pilot-task-comp.txt": "bbd67273977902c3b9728a52ed04600352480afdd05b060ca40a20f4f2426bba",
    "tasks/pilot-task-mid.txt": "e61540415e3f8ae9d62e7cd5ec44fc09adb20caebe50614ec5dc3f762eb05585",
    "tasks/pilot-task-n1.txt": "b27c11f48c5cbcfdb4bbeddafb637a52e91f01d8694c4cb06af6dd3b86ff0328",
    "tasks/pilot-task-n2.txt": "9d1b325ccd9f8e6132c8f224d1e5233daf2dbf40d97c553351c935984d08e366",
    "tasks/pilot-task-n3.txt": "8f4a927b2337e7f324cf910a64271d58ccfeeaf5b5d4ed5ea1bc06980b0b7a56",
    "tasks/pilot-task-seam.txt": "8a2811ec2b3bb25106944e6a7e917a85f98eecdd4e5017baa29c91dce1daf2d8",
    "tasks/task-comp.txt": "0be2b658059141c993e0b5edcfd0955b774d69aab236a32b2316ea57b7205bf0",
    "tasks/task-mid.txt": "96d3e766a3a9e4ed74f383cf7304995e86eede8f3317df9be7d14af408253ea9",
    "tasks/task-n1.txt": "c914dd357ffe994552054730c989e6ecec5f1ce77f1c697924b9addd24fda000",
    "tasks/task-n2.txt": "2c78f43917533ee5b9177002d588c46b5bdc1fc104c0e10d3fc2a50393adda8a",
    "tasks/task-n3.txt": "c47dffdffb1b80020eb58ee7bbd99862c75f2287b03eda49784ab6fcf6dcdd1e",
    "tasks/task-seam.txt": "b95079d90a88c078238ffceafdecfcb8cbac1c2e4146a578a9d62996ad6b45bc"
  },
  "runtime": {
    "claude_version": "2.1.207 (Claude Code)",
    "model": "claude-sonnet-5",
    "permission_mode": "bypassPermissions",
    "trial_timeout": 1800,
    "env": {
      "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
      "DISABLE_AUTOUPDATER": "1"
    }
  }
}
```

Seal digest (SHA-256 of `armmap/hash-record.json`, pinned in `armmap/seal.json` at seal time): `a405aacd246cc8d44a1079f6c6fa8bf02f8e8c22f4cd06bf05c491ea03536546`

## 13. Honest bound

Quoting the design (Proof Plan, Honest bound): "these probes exercise Claude-side behavior. Codex receives the same narrowed text, with behavior bounded initially by source inspection and the live watch rather than represented as experimentally proven. The probes are also same-model — Claude-graded-Claude, methodology moves 4 (cross-model) and 5 (human judge) unused — so per the methodology's honest-limits line this evidence must be weighted accordingly: the take rule stays near-mechanical (a `tool_use` block naming the exact skill) to shrink the judgment surface, and the offer-grading residual is owned explicitly at the step-5 adversarial prereg review."

Known channel properties recorded pre-seal (from the pilot, so a sealed fail is read honestly): the seeded `diagnose` exit licenses inline handling ("when that handoff is declined or the fix is trivial"), so a contract-faithful ON agent may decline the seam take via the governing-skill hatch — a seam fail returns design bullet 2 with that reading attached, not instrument error. The mid channel is sealed with the confrontation demonstrably presented (both i3 pilot arms had to modify the untested module) but with zero observed target takes in any arm, ON included (ON pilot observation 0/1) — "moment presented" is not "take demonstrated inducible", and a sealed mid fail returns design bullet 1 honestly, not instrument error. Pilot OFF-arm base rates (n=1/arm): mid target-take 0, seam tdd-take 0, comp full-composition 0 (1-of-2 partial), n1/n2/n3 overfire 0. Trials can write host `$HOME` state through skill-owned scripts (observed: simplify-code's backup helper) — arm-symmetric, accepted, cleaned with `trash` after runs.

## 14. What this seal does not do

- It does not certify the contract works; it fixes how that question gets answered.
- It does not authorize editing `schedule.json`, task texts, keys, trees, fixture, or `runner.py` post-seal; `runner.py record` refuses to re-run once sealed — a post-seal hash mismatch can only abort and be reported.
- It does not extend to Codex behavior (see Honest bound) and does not pre-commit the Task-9 charter consult or JP's ratification either way.
- Pilot outputs never enter sealed scoring (runner-enforced `pilot-` namespace).
