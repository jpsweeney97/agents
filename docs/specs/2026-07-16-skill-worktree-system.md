# Design Spec: skill-worktree system — permanent per-skill worktrees with fresh task branches

**Status:** approved design, pilot in progress · **Date:** 2026-07-16 · **Source:** design conversation with JP (settled model supplied; two Patch-Before rounds adjudicated by JP before any mutation). Class: repo operating procedure plus a deferred durable-owner decision — the procedure doc itself is not a charter event; authoring the eventual owning skill (irreversible Git operations) is charter-gated at that time.

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
- **Validate:** the surface-exact validation ladder; completing it records `{branch, validated_tip: <exact SHA>, ladder, ignored_state, timestamp}` under `.git/skill-worktree/validations/`.
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

Lease root `/Users/jp/.agents/.git/skill-worktree/leases/` — inside the common Git dir: outside every working tree, shared by all worktrees, survives sessions. Two kinds: `wt-<identity>.lease/` (held activation → proven re-park) and `integration.lease/` (held recheck → merge → ancestry proof). Acquisition is atomic `mkdir` then `owner.json` `{session_id, runtime, acquired_at, purpose, worktree, branch, diag:{pid, pid_start, host}}`. Ownership authority is `session_id` + `runtime` only — `CLAUDE_CODE_SESSION_ID` (claude-code) or `CODEX_THREAD_ID` (codex); PID facts are diagnostics for recovery adjudication, never decision inputs. Foreign, missing, or unreadable ownership → fail closed, explicit user-authorized break (`trash`), then full reconstruction. The leases bind only protocol participants; the post-acquisition recheck is the defense against non-participants. Universal enforcement (hooks) is a durable-owner question.

## Ignored-state policy

Classified at every activation and integration from `git ls-files --others --ignored --exclude-standard -z` (leaf files — collapsed directory views hide contents) plus `status --porcelain`. Persist-silently: `.DS_Store` only. Report-and-record (named in activation and validation records; "none" is an explicit entry): `.agents/handoffs/`, `.agents/scratch/`, `.claude/`, `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.ruff_cache/`, leftover `.plugin-eval/`. Unknown ignored path: hard stop. The primary's pre-existing ignored state is recorded as baseline and left to `git-hygiene`.

## Upstream and rollback

Upstream read from `rev-list --left-right --count main...origin/main`, no fetch: ahead-only allowed and reported (the steady state while landings accumulate unpushed); behind or diverged stop; no usable tracking ref is a reported proof limitation, not a stop. `origin/main` carries no task-level rollback authority. Pre-merge, everything is disposable (abandoning an unmerged branch needs explicit user say-so since it needs `-D`). Post-landing rollback is always a new, separately authorized revert task through this same lifecycle — no ref-reset path.

## Scale boundary

Pilot success authorizes nothing beyond the pilot. Full rollout requires a separate inventory-scale gate: canonical inventory definition (93 `SKILL.md` surfaces at design time; whether plugin skills get satellites is a gate question), read-only reconciliation dry-runs, add/rename/retire/missing-directory/unexpected-directory/stale-lock cases, and measured full-inventory health-check behavior. The durable owner of this procedure (provisionally a `git-cycle` skill) stays undecided until the pilot exposes the real command and recovery surface; authoring it routes through `agent-facing-design` and the charter's irreversible-operations gate.

## Pilot design (scope: Git lifecycle only)

Two satellites — A `decision-record`, B `work-router` — and three tasks: T1 `fix/decision-record--stale-registration` (real skill fix, full skill ladder); T2 `chore/skill-worktree-spec` (this document, docs ladder), activated from the same `main` as T1 to force stale-base reconciliation when T1 lands first; T3 `chore/skill-worktree-pilot-evidence` (evidence append, proving directory reuse). Plus a foreign-session lease probe. The pilot proves reuse, fresh-branch-from-verified-main, lease-serialized integration, stale-base reconciliation, parking proofs, deletion-after-ancestry, and delivery-integrity preservation. It does not prove Claude-only delivery-root behavior, branch-local runtime behavior (a satellite's edit is invisible to both runtimes until landed), or inventory scale.

The evidence record lands as a follow-up append (T3); T3's own landing proof lives in Git history and the pilot's closing report.
