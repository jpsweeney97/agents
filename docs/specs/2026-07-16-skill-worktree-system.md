# Design Spec: skill-worktree system — permanent per-skill worktrees with fresh task branches

**Status:** approved design, pilot complete (2026-07-16) · **Date:** 2026-07-16 · **Source:** design conversation with JP (settled model supplied; two Patch-Before rounds adjudicated by JP before any mutation). Class: repo operating procedure plus a deferred durable-owner decision — the procedure doc itself is not a charter event; authoring the eventual owning skill (irreversible Git operations) is charter-gated at that time.

## Settled model (not reopenable here)

Every skill gets one permanent satellite worktree under `/Users/jp/.agents-worktrees/<identity>`; every change is a fresh task branch cut from verified current `main`, landed into the primary checkout by fast-forward only, then safely deleted. The directory is the skill; the branch is the task. The primary checkout at `/Users/jp/.agents` is permanently the integration lane and the only live runtime source (Codex scans it in place; Claude serves it through `~/.claude/skills` symlinks). Development parallelizes across satellites; integration serializes through the primary. Satellites are never a delivery source: no `claude-skills-sync.sh --link`, plugin publish, mirror update, push, or PR from a satellite, ever.

## Identity and naming

- Worktree identity = skill directory basename, assigned at creation, immutable thereafter. An existing directory is never renamed; a later colliding skill takes a root-prefixed identity (`claude--<name>`) at its own creation. Preflight asserts census-wide basename uniqueness.
- Task branches are repo-global: activation hard-fails if the name exists. Skill-scoped tasks use `<type>/<skill-id>--<slug>`; cross-cutting tasks use `<type>/<slug>`; `<type>` is an accurate `feature`/`fix`/`chore`.

## Lifecycle

Nominal: `ABSENT → PARKED → ACTIVE → READY → [INTEGRATE] → LANDED → PARKED`, with rebase-and-revalidate looping READY on a stale base.

- **Create:** `git worktree add --detach <path> main`, then `git worktree lock --reason "parked skill workspace (permanent)"`. The lock blocks ordinary and single-`--force` removal; `--force --force` still removes it, so the lifecycle prohibits forced removal outright — the lock is friction, not proof.
- **PARKED is proven, never assumed** — all four before any activation: HEAD detached (`symbolic-ref -q HEAD` fails); clean per the ignored-state policy below; `merge-base --is-ancestor HEAD main`; `rev-list --count main..HEAD` = 0. Ancestry failure means a clean orphan commit → PARKED-ORPHAN recovery: switch nothing, surface `git log main..HEAD`, user adjudicates (adopt / explicit rescue ref / explicit discard).
- **Activate:** under the worktree lease, branch-name-free check, then `git -C <wt> switch -c <branch> main` — from the explicit `main` ref, never parked HEAD — and prove tip == `rev-parse main`.
- **Validate:** the surface-exact validation ladder; completing it records `{branch, validated_tip: <exact SHA>, ladder, ignored_state, timestamp}` under `.git/skill-worktree/validations/`. Records are transient: once a task's landing is proven and its branch deleted, trash its record at the park/delete step. Exception: the pilot's records are retained as fixtures for the durable-owner build, then trashed.
- **Integrate (serialized):** under the integration lease, with mandatory post-acquisition recheck — primary on `main` and clean, no op markers, upstream state read, freshness (`merge-base --is-ancestor main <task>`), `rev-parse <task>` == `validated_tip`, satellite clean. Then `git merge --ff-only <task>` from the primary; never fall back to a merge commit. Landed proof: `merge-base --is-ancestor <task> main`. A stale base fails freshness → rebase in the satellite, full revalidation (new `validated_tip`), re-enter the queue.
- **Park:** `git -C <wt> switch --detach main`, re-prove PARKED.
- **Delete:** `git branch -d <task>` only after the ancestry proof; `-d` refusal despite that proof is an evidence contradiction — stop, never `-D`.

### Recovery states (Git-reconstructable)

| State | Identifying facts | Route |
|---|---|---|
| ACTIVE-CONFLICT | `rebase-merge`/`rebase-apply` under the satellite's git-dir | `resolve-conflicts`, then full revalidation |
| READY-INVALID | commits present; validation record red/absent | fix / `keep-green`; barred from integration |
| COMMITTED-UNLANDED | on task branch; ahead of `main`; not ancestor; lease stale/absent | reconstruct, re-lease, freshness, integrate |
| LANDED-UNPARKED | branch ancestor of `main`; worktree still on it | resume at park step |
| PARKED-UNDELETED | detached and clean; merged branch still exists | `-d`; refusal = contradiction, stop |
| PARKED-ORPHAN | detached HEAD not ancestor of `main` | preserve and surface; user adjudicates |
| LEASE-ORPHANED | lease exists; owner foreign/unknown | surface; user-authorized break; reconstruct |

The authoritative inspection is the fact-vector (HEAD kind, op markers, tree state with ignored classification, branch↔`main` ancestry both directions, lease state); an unmappable vector is a hard stop.

## Leases (cooperative serialization)

Lease root `/Users/jp/.agents/.git/skill-worktree/leases/` — inside the common Git dir: outside every working tree, shared by all worktrees, survives sessions. Two kinds: `wt-<identity>.lease/` (held activation → proven re-park) and `integration.lease/` (held recheck → merge → ancestry proof). Acquisition is atomic `mkdir` then `owner.json` `{session_id, runtime, acquired_at, purpose, worktree, branch, diag:{pid, pid_start, host}}`. Ownership authority is `session_id` + `runtime` only — `CLAUDE_CODE_SESSION_ID` (claude-code) or `CODEX_THREAD_ID` (codex); PID facts are diagnostics for recovery adjudication, never decision inputs. Foreign, missing, or unreadable ownership → fail closed, explicit user-authorized break (`trash`), then full reconstruction. The leases bind only protocol participants; against non-participants the post-acquisition recheck narrows the race window, and Git's own ref locking plus `--ff-only` protect the ref update itself. Universal enforcement (hooks) is a durable-owner question.

## Ignored-state policy

Classified at every activation and integration from `git ls-files --others --ignored --exclude-standard -z` (leaf files — collapsed directory views hide contents) plus `status --porcelain`. Persist-silently: `.DS_Store` only. Report-and-record (named in activation and validation records; "none" is an explicit entry): `.agents/handoffs/`, `.agents/scratch/`, `.claude/`, `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.ruff_cache/`, leftover `.plugin-eval/`. Unknown ignored path: hard stop. The primary's pre-existing ignored state is recorded as baseline and left to `git-hygiene`.

## Upstream and rollback

Upstream read from `rev-list --left-right --count main...origin/main`, no fetch: ahead-only allowed and reported (the steady state while landings accumulate unpushed); behind or diverged stop; no usable tracking ref is a reported proof limitation, not a stop. `origin/main` carries no task-level rollback authority. Pre-merge, everything is disposable (abandoning an unmerged branch needs explicit user say-so since it needs `-D`). Post-landing rollback is always a new, separately authorized revert task through this same lifecycle — no ref-reset path.

## Scale boundary

Pilot success authorizes nothing beyond the pilot. Full rollout requires a separate inventory-scale gate: canonical inventory definition (93 `SKILL.md` surfaces at design time; whether plugin skills get satellites is a gate question), read-only reconciliation dry-runs, add/rename/retire/missing-directory/unexpected-directory/stale-lock cases, and measured full-inventory health-check behavior. The durable owner of this procedure (provisionally a `git-cycle` skill) stays undecided until the pilot exposes the real command and recovery surface; authoring it routes through `agent-facing-design` and the charter's irreversible-operations gate.

## Pilot design (scope: Git lifecycle only)

Two satellites — A `decision-record`, B `work-router` — and three tasks: T1 `fix/decision-record--stale-registration` (real skill fix, full skill ladder); T2 `chore/skill-worktree-spec` (this document, docs ladder), activated from the same `main` as T1 to force stale-base reconciliation when T1 lands first; T3 `chore/skill-worktree-pilot-evidence` (evidence append, proving directory reuse). Plus a foreign-session lease probe. The pilot proves reuse, fresh-branch-from-verified-main, lease-serialized integration, stale-base reconciliation, parking proofs, deletion-after-ancestry, and delivery-integrity preservation. It does not prove Claude-only delivery-root behavior, branch-local runtime behavior (a satellite's edit is invisible to both runtimes until landed), or inventory scale.

The evidence record lands as a follow-up append (T3); T3's own landing proof lives in Git history and the pilot's closing report.

## Pilot evidence record (2026-07-16)

Observed in the executing session (`CLAUDE_CODE_SESSION_ID` fdba0921…, claude-code runtime); every transition below was proven by command output at execution time, and every guard listed fired or passed exactly as designed.

- **Preflight (P0):** primary clean on `main` at `b3faad1`, `main...origin/main` = `0 0`, no op markers, single worktree; census 93 `SKILL.md` surfaces, zero basename collisions; all `~/.claude/skills` symlinks resolved into the primary; both delivery `--check` scripts exit 0; planned branch names free; sibling root verified empty and unregistered; primary leaf-ignored baseline 938 files recorded. `CODEX_THREAD_ID` absent in this runtime — session identity carried by `CLAUDE_CODE_SESSION_ID`, per the runtime-identity rule.
- **Create:** satellites `decision-record` and `work-router` added detached at `b3faad1` and locked; all four PARKED proofs passed on both; leaf-ignored state "none present" on both.
- **Foreign-lease probe:** planted `wt-pilot-simulation.lease` owned by a fabricated session id; re-acquisition refused by atomic `mkdir`; ownership check rendered FOREIGN and failed closed; broken by `trash` under the pre-approved probe authority; lease root verified empty after.
- **T1** `fix/decision-record--stale-registration` (satellite A): activated from explicit `main` at `b3faad1` with base proof; one-line skill fix; full skill ladder green (frontmatter parse, `quick_validate.py`, referenced paths, `diff --check`, behavior fact-check against `grill-with-docs/SKILL.md:102`); committed `5ecf7e0` = `validated_tip`; landed under the integration lease after full post-acquisition recheck; ff-only `b3faad1 → 5ecf7e0`; ancestry proven; primary's served copy verified pre-edit before landing and post-edit after (the isolation and hand-off properties observed directly); A re-parked with proofs; branch safe-deleted; lease released.
- **T2** `chore/skill-worktree-spec` (satellite B): activated from the same `b3faad1` base concurrently with T1; committed `d31813b`; after T1 landed, freshness check failed as designed (stale base detected); rebased in the satellite to tip `e1d7832`; `validated_tip` mismatch (`d31813b` ≠ `e1d7832`) forced full revalidation before landing — the binding worked; landed ff-only `5ecf7e0 → e1d7832` with upstream reading "ahead 1, behind 0" allowed and reported per the ahead-only rule; B re-parked with proofs; branch safe-deleted; leases released.
- **Reuse (T3, this append):** satellite B re-leased for a second task; all PARKED proofs re-passed; prior task branch verified absent (no task-history leak); `chore/skill-worktree-pilot-evidence` activated from explicit current `main` (`e1d7832`) with base proof; interim delivery checks exit 0; landed ff-only `e1d7832 → 4ccfa07` under the integration lease after full recheck (upstream "ahead 2, behind 0" allowed per the ahead-only rule); B re-parked with all proofs; branch safe-deleted; leases released. Closing sweep green: both delivery `--check` scripts exit 0, every `~/.claude/skills` symlink targeting the primary, census 93 unchanged, no task branches remaining, lease root empty, final upstream "ahead 3, behind 0".
- **Hook interaction (observed, not designed):** the user-level protected-branch hook permitted satellite edits on task branches while the primary sat on `main` — branch identity resolves per-worktree. Noted as an observation for the durable owner, not a guarantee.

- **Closeout** (`chore/skill-worktree-pilot-closeout`, satellite A's second task — giving both satellites a proven reuse cycle): activated from a deliberately stale parked HEAD (`5ecf7e0` behind `main` `4ccfa07`), proving stale-parked activation branches from explicit current `main`; flipped status to pilot complete, recorded T3's proofs, corrected the non-participant enforcement wording, and stated the validation-record lifecycle. Its own landing is the final pilot commit in Git history — one deliberate hop of delegation, terminal by convention.

Boundary honored throughout: no push, no publish, no sync `--link`, no mirror/cache/marketplace mutation, no forced removal, no `-D`. Scope claims unchanged from "Pilot design" above.
