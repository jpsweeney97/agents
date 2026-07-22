---
type: feasibility-report
project: agents
created: 2026-07-21
source: "T2 prereg v2 sequencing step 2 (docs/plans/2026-07-19-deliberate-shallow-prune-control-preregistration.md @ 29aa6f3); panel: docs/plans/2026-07-21-deliberate-t2-design-panel-report.md"
---

# T2 feasibility checks: read-scope confinement, cross-family channel, token exposure

The three checks the prereg's sequencing step 2 owes before the mini-pilot. All three were run live on this machine on 2026-07-21 (Claude Code 2.1.217, codex-cli 0.144.6, macOS 26.5.2). Design input only; nothing here is sealed evidence, and no T2 case data was collected — every probe used one synthetic judgment packet about a fictional community-library decision, content-unrelated to `deliberate`, authored for these probes and spent by them.

## Verdicts

1. **Read-scope confinement for blind Claude-side roles: ENFORCEABLE at dispatch** — via headless `claude -p --settings <deny-profile>`, not via the in-session Agent tool.
2. **Blind cross-family judge channel: DEMONSTRATED end-to-end** — packet delivered to an OpenAI-family model via `codex exec`, strict-JSON judgment captured, apparatus-free context achievable; codex-side read scope is instruction-level only, disclosed below.
3. **Per-dispatch token counts: EXPOSED on all three dispatch routes** — the prereg's byte-proxy fallback is not needed as the primary instrument.

## Check 1 — dispatch-time read-scope confinement (Claude-side blind roles)

Method: two-arm differential probe, identical prompt, `claude -p --model haiku` from a packet directory in session scratch. The probe attempts, in order: Read of `./packet.md`; Read of `/Users/jp/.agents/AGENTS.md`; Read of the committed prereg; a Bash file read (`head -1`) of AGENTS.md; a WebSearch.

- **Control arm (no profile):** packet read succeeded; both out-of-cwd Read-tool attempts were auto-denied by the headless default ("requested permissions... but you haven't granted it yet"); WebSearch auto-denied; **the Bash file read succeeded** — the escape hatch a bare headless dispatch leaves open.
- **Enforcement arm (`--settings blind-settings.json`** — deny list: `Bash`, `WebFetch`, `WebSearch`, `Read(//Users/jp/.agents/**)`, `Read(//Users/jp/.claude/**)`, `Read(//Users/jp/.codex/**)`, `Read(~/personal/**)`): packet read succeeded; both repo reads denied with "File is in a directory that is denied by your permission settings."; Bash and WebSearch were absent from the agent's tool list entirely. Complete confinement, proven by the differential against the control arm.
- **Ambient strip:** `--safe-mode` composes with `--settings` — a probe under both reported no context mention of charter/deliberate/skill-usage (its one "worktree" hit is the built-in Workflow tool description, harness-generic) while the deny rule still fired. `--bare` is unusable on this machine (returns "Not logged in").

Bounds and consequences for the seal:

- Documented limit: Read deny rules cover built-in file tools and recognized Bash file commands, not arbitrary subprocesses. Denying `Bash` outright closes the subprocess channel; blind roles (case-writers, extractors, judges, packet composers, leak probes) need no shell. If a blind role ever needs Bash, OS-level `sandbox.filesystem.denyRead` is the documented second layer (untested here).
- The in-session Agent tool cannot carry per-dispatch path-scoped deny profiles — subagent definitions restrict tools only, and permission rules are session-wide. The sealed protocol should therefore dispatch every blind role headless: `claude -p --safe-mode --settings <role-profile> --model <role-model>` from a packet-directory cwd. The pilot's in-session dispatch route is not confinement-capable.
- The probe profile is a probe artifact; the sealed run must pin its own per-role profiles (including denying `Agent`, `Skill`, `Workflow`, and MCP tools for judge roles) at seal time.

## Check 2 — live end-to-end blind cross-family judge dispatch

Method: `codex exec --sandbox read-only --skip-git-repo-check --ephemeral --json -o <file>` from the packet directory, judging the synthetic packet (two candidate proposals, verdict as strict JSON).

- **Channel fires:** exit 0; the judgment arrived as strict JSON in the output file (`{"winner":"B","confidence":"medium",...}`); config model `gpt-5.6-sol` (self-report "GPT-5 (Codex)"); token usage in the `turn.completed` event. Judgment capture, model selection (`-m`), no session persistence (`--ephemeral`), and a JSON-schema enforcement flag (`--output-schema`, untested) all exist.
- **Default dispatch leaks apparatus:** the first run's event stream contained "Skill descriptions were shortened to fit the 2% skills context budget. Codex can still see every skill" — codex scans `$HOME/.agents/skills` globally, so a default judge dispatch carries every skill description, `deliberate`'s included, plus `~/.codex/AGENTS.md` (which names the charter). There is no skills feature flag to disable this (`--disable skills` errors; `codex features list` has no such flag).
- **Mitigation proven:** dispatching with `HOME=<bare dir> CODEX_HOME=<dir containing only auth.json>` strips the apparatus: the probe reported charter NO, deliberate NO, skill-usage NO, and the skills-budget event disappeared. (Its one "trash" hit traced to codex's own built-in destructive-actions guidance — vendor baseline, not this repo's files.)
- **Codex-side read scope is instruction-level only:** under `--sandbox read-only` the probe's shell read of `/Users/jp/.agents/AGENTS.md` succeeded — codex's read-only sandbox blocks writes, not reads, and no codex flag confines reads to a directory. Enforced confinement would need an external OS wrapper (macOS `sandbox-exec` profile or a separate user account) — possible, untested.

Fold for the seal: the cross-family channel precondition (prereg §Leakage) is dischargeable — the demonstrated dispatch shape is bare-HOME + auth-only CODEX_HOME + packet-dir cwd + read-only sandbox + `--ephemeral`, with confinement instruction-level and the packet itself leak-free (the executed leak probe already required by the prereg is the operative defense on this side). The seal should state this asymmetry explicitly: Claude-side blind roles enforced, codex-side judges instruction-level. The repo is GitHub-private, bounding the network-side leak surface; whether codex's read-only sandbox also blocks network for shell commands was not tested.

## Check 3 — per-dispatch token exposure

All three dispatch routes expose runtime token counts; the pilot's bytes/wall-clock-only record was an instrumentation gap, not a harness limit.

- **In-session Agent tool (the pilot's route):** each subagent writes its own transcript at `<session-dir>/subagents/agent-<name>-<id>.jsonl` with per-message `usage` (input, output, cache-read, cache-creation). Demonstrated on the five real T2 panel agents: summed output tokens — control 51,790; gates 40,348; leakage 25,124; measurement 36,233; method 34,364. Post-hoc and mechanical.
- **Headless `claude -p --output-format json`:** per-dispatch `usage`, per-model `modelUsage`, and `total_cost_usd` in the result JSON (observed directly on the check-1 probes).
- **`codex exec --json`:** `turn.completed` carries `usage` including input, cached-input, output, and reasoning tokens (observed: 43,474 in / 343 out / 145 reasoning on the judge run).

Fold for the seal: the prereg's instrumentation clause ("runtime token counts only if the harness exposes them, else the byte-proxy flagged as estimate") resolves to tokens-as-primary. The instrumentation spec must fix the summation grain — per-message input counts embed cache splits, so the sealed formula should name what is summed (e.g., output tokens summed per dispatch; input reported as final-call context plus cache splits) rather than a bare "total tokens." The budget ceiling stays in dispatch-count and operator-hours as pre-registered; token figures become recorded measures, not the ceiling.

## Probe hygiene

The synthetic packet and probe outputs live only in session scratch; probe sessions were unpersisted (`--no-session-persistence` / `--ephemeral`); the temporary auth-only `CODEX_HOME` copy was trashed immediately after the codex probes. Total probe cost: five small dispatches (two haiku probes, one safe-mode haiku probe, two codex probes).
