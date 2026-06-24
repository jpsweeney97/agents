---
title: "Full skill-library review against the two-bar judgment/trust apparatus"
date: 2026-06-17
type: review-artifact
status: findings-recorded (review-only; no skill edits made)
scope: all 48 live skills (skills/ 34, skills-claude/ 5, plugins/handoff 4, plugins/review-family 5)
apparatus: agent-facing-design "Two Kinds of Skill" + scrutinize-skill (the validated two-bar lens)
workflow_run: wf_2ef028f0-602 (corrected run; superseded the buggy wf_5ee34a4a-4bc)
branch: chore/skill-library-apparatus-review
---

# Full skill-library review against the two-bar apparatus — 2026-06-17

## TL;DR

The 48-skill library is **healthy**. The **judgment bar is clean** — zero substitutive-structure or provoke-too-weakly defects survived verification, and the apparatus's known **over-cutting failure mode did not fire** (no legitimate forcing function was flagged for removal; the two over-cut candidates it did raise were caught by the defend-lens verifier). The library's real weakness is on the **trust bar** and is one coherent shape: **copied machinery with live drift**. ~7 static rules are hand-restated across 4–7 surfaces each and are beginning to diverge. Nothing is broken — the **severity ceiling is `major`, no `critical` survives** (the `main`-branch hook and always-loaded `AGENTS.md` backstop the worst case). **32 of 48 skills are fully clean.**

The remedy is essentially **one consolidation pass** (single-home static constants, reconcile the one live mechanism divergence, add a missing safety marker) plus a small `$`-token delivery-hygiene sweep.

## Method

Two-track multi-agent workflow, every finding cleared two adversarial verifiers:

- **Track 1 — cross-skill duplication scan.** 8 machinery-class hunters swept all 48 `SKILL.md` (+ referenced files) for the apparatus's flagship trust failure mode — *the same gate/rule/mechanism copied across skills, free to drift*. This mode is invisible to a per-skill reviewer by construction. Each cluster was verified by a *defend-as-acceptable* lens (is it unavoidable independent-load duplication, or already single-homed?) and an *evidence* lens (do the cited spans actually carry the same rule?).
- **Track 2 — per-skill review.** One agent per skill applied the two-bar lens, classifying each part as judgment or trust and holding it to the matching bar; each finding was verified by a *defend-the-structure* lens (over-cut catcher) and an *evidence* lens.
- **Synthesis + completeness critic.** Findings + clusters deduped into ranked patterns; a critic then hunted blind spots and spot-checked the riskiest claims against the files.

Verification was deliberately conservative: it **rejected 10 of 30 clusters and 2 of 20 per-skill findings** as over-cuts or not-real-duplication (see "Deliberately not flagged"). The top-ranked items were additionally verified by hand by the orchestrator.

> **Process honesty.** The first run (`wf_5ee34a4a-4bc`) returned a false "48/48 clean, 0 findings" — caused by a script bug (JSON schemas declared after first use → hoisted as `undefined` → every agent ran *schemaless* and the aggregation read `.findings` off plain strings). The completeness critic caught it; its catches were verified firsthand; the run was redone correctly (`wf_2ef028f0-602`). All numbers here are from the corrected run.

## Library health

| Bar | Verdict |
| --- | --- |
| **Judgment** | **Clean.** 0 confirmed substitutive/toothless findings across all judgment skills (review family, grilling, recommendations, design, interviewer, diagnose, scrutinize family). The over-cutting failure mode did not fire. Three zero-finding judgment skills were spot-checked (outcome-interviewer, scrutinize, grill-me, making-recommendations) — genuinely clean with real forcing functions; the zero-provoke-too-weakly result is true health, not under-scrutiny. |
| **Trust** | **Leaky on machinery single-sourcing.** ~7 static rules hand-copied across 4–7 surfaces with live drift. Most consequential: a real mechanism divergence (git-hygiene config-glob vs three skills' hardcoded list) and one real safety-set gap (git-hygiene omits `revert`/`REVERT_HEAD`). |
| **Delivery hygiene** | **Recurring but low.** A minority drift — 4 of 9 self-naming skills miss the Codex `$name` token; a couple of "repo instructions" references don't name `AGENTS.md`/`CLAUDE.md` jointly. |

- **48 reviewed · 32 clean · 16 with ≥1 confirmed finding · 18 per-skill findings confirmed · 20 clusters confirmed (dedup → 7 patterns) · severity ceiling `major`, no `critical`.**
- Defects concentrate in three families — the **git-lifecycle quartet** (merge-branch / closeout-check / acceptance-map / git-hygiene), the **handoff quartet**, the **review-family quintet** — plus a **repo-invariant restatement** class and a scatter of per-skill template/token nits.

## Findings — 7 ranked cross-cutting patterns

### P0 · `major` · Protected-branch / commit gate copied across the git-lifecycle quartet, one mechanism already drifted
**Skills:** merge-branch, closeout-check, acceptance-map, git-hygiene (+ execute-plan as consumer). The literal fallback list `main`,`master`,`develop`,`release/*` + "repo-defined-first, else fallback" rule is **byte-identical** in merge-branch:61-62, closeout-check:171-173, acceptance-map:225-227. **git-hygiene:16-19 enforces the same gate via a `branchProtection` config glob with NO literal list** — so a repo protecting only `develop` is guarded by three skills but **not** git-hygiene. merge-branch:80 carries a narrower second in-skill copy (drops `release/*`). `AGENTS.md`:260-262 owns the branch convention + names the enforcing hook but states only the positive rule, not the protected set. **Fix:** single-home the protected-set definition + `chore/fix/feature` prefix list in always-loaded `AGENTS.md` "Git And Cleanup"; replace the three verbatim blocks + the merge-branch:80 variant with one-line cites; reconcile git-hygiene's glob as the documented per-repo *override* on top of that default. **Keep each skill's protected-branch *response* (stop-and-ask vs self-branch vs refuse) inline — that is per-skill behavior, not drift.**

### P1 · `major` · Git preflight operation-in-progress set drifted (real safety gap)
**Skills:** merge-branch, git-hygiene. merge-branch:33,57-59 aborts on rebase/merge/cherry-pick/**revert**/bisect and names the markers (`MERGE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `BISECT_LOG`, …). git-hygiene:40 + reference:20 are prose-only ("rebase, merge, cherry-pick, or bisect") and **omit `revert`/`REVERT_HEAD`** — so an agent cleaning up during a paused `git revert` is aborted by one skill but not the other. *(Verified firsthand.)* **Fix:** add `revert`/`REVERT_HEAD` to git-hygiene now; extract the canonical operation set + marker names into one shared preflight surface both cite. Each skill keeps its own action-on-abort.

### P2 · `major` · Review-family conventions copied across the five review skills, drifting on safety surfaces
**Skills:** scrutinize, scrutinize-skill, implementation-review, system-design-review, review-reviewer. (a) **Read-only / protected-action boundary** written as five different verb lists (scrutinize:127, scrutinize-skill:197-199, implementation-review:52, system-design-review:45-47, review-reviewer:33-38) — closing one gap leaves the others exposed. (b) **Routing block:** the dedicated `scrutinize-skill` lane is **omitted from implementation-review, system-design-review, and review-reviewer**, so a skill-contract target landing in those lanes gets no redirect; opener verbatim in 4 / rewritten in 1; closer absent from review-reviewer. (c) **Evidence-floor** re-authored five ways with split `unverified` vs `needs-verification` vocabulary, forcing review-reviewer to publish its own cross-walk. (d) **Bounded-review** mechanism re-authored four ways. **Fix:** routing text must stay in each body (references load on demand and can't route), but normalize the opener/closer to one wording, single-home the precedence rule + the read-only core list + the evidence-floor sentence in a **plugin reference** each cites, pick ONE unverified-marker token, and immediately add the missing `scrutinize-skill` redirect to the three lanes. **Plugin-distributed → Plugin Layout publish path.**

### P3 · `major` · Handoff path-set + project-root resolution re-rendered across all four handoff skills
**Skills:** load-handoff, save-handoff, search-handoffs, throughline. The three-path storage contract (`.agents/handoffs/` primary + `.claude`/`.codex` legacy read-only) is restated in 6–7 places (load:23-26, search:15-18, throughline:48-51, save:8/27-29/68-69, references/handoff-format.md:5-11, references/throughline-format.md:5-9) — already disagreeing on whether the block carries the `*.md` glob — **despite being already single-homed in always-loaded `AGENTS.md`:72-74.** The project-root two-step (`git rev-parse --show-toplevel` else cwd) is byte-identical in all four (latent-drift trap, zero drift today). **Fix:** cite `AGENTS.md`:72-74 (or promote references/handoff-format.md as the portable single block for the mirror) and keep only the per-skill verb inline; fold project-root into the same surface. **Plugin Layout publish path.**

### P4 · `major` · "Don't invent an installed-runtime proof layer" repo invariant restated five times
**Skills:** closeout-check, agent-facing-design, skill-ux-design, writing-principles (+ behavior-smoke-test on the validation ladder). The repo-source-equals-live invariant is restated at closeout-check:128-132, agent-facing-design:177-180 (drops hook/service exceptions), writing-principles:195-197, and **twice inside skill-ux-design** (217-219 AND 326-329) — with drifting exclusion lists, though `AGENTS.md`:248-253 already states it authoritatively. Separately the **validation ladder** is re-listed in writing-principles:199-218, skill-ux-design, behavior-smoke-test:178-184, and **all three omit the load-bearing `quick_validate` `argument-hint`/`disable-model-invocation` accepted-failure caveat** (`AGENTS.md`:227-231) — the one item whose omission could make an agent "fix" a false failure by deleting a valid field. **Fix:** trim the skill copies to a one-line pointer to the `AGENTS.md` proof-boundaries bullet + Validation Ladder; de-dup skill-ux-design's two internal restatements to one. Pure repo invariant — strong single-home candidate.

### P5 · `minor` · Delivery hygiene: dual-runtime trigger named only as `/name`, never `$name`
**Skills:** caveman:3 (`/caveman`), load-handoff:3/14 (`/load`), search-handoffs:3 (`/search`), save-handoff:3 (`/save`), setup-matt-pocock-skills seed domain.md:11,45 (`/grill-with-docs`); + tech-debt-scan says "repo instructions" without naming `AGENTS.md`/`CLAUDE.md` jointly. `AGENTS.md` mandates naming both runtimes' tokens; sibling throughline already dual-names. **Compliance is actually high — 5 of 9 self-naming skills already dual-name; these are the minority drift.** Codex routing via `openai.yaml` is not dead, so this is declaration-text polish. **Fix:** one sweep adding `$name` beside `/name` in each routing-critical declaration; name the instruction files jointly where tech-debt-scan points the agent at them.

### P6 · `minor` · Template/example text that contradicts its own skill's live contract
**Skills:** skill-ux-design, next-steps, improve-codebase-architecture, to-issues. skill-ux-design closeout templates (274, 293) hardcode `Proof boundary: ... no realistic behavior smoke test was run` as fixed prose, not a fill-in slot (fragile if the agent ever *did* run one). next-steps example.md:47 models a one-shot "tell me the path" that collapses the offer/accept/ask-path handshake SKILL.md:48 prescribes. improve-codebase-architecture:55 has a dangling "as before" + field-label drift (`Benefits` vs `Wins`) vs the authoritative HTML-REPORT.md. to-issues:83-88 seeds "Criterion 1/2/3" placeholders with no quality guidance (substitutive-fill risk on a trust artifact). **Fix:** make the proof line a conditional fill-in slot; align next-steps' example to the body contract; drop "as before" + unify labels; replace to-issues' numbered placeholders with one line on observable-check intent. All are wording/template fixes.

## Full ranked findings (25)

The patterns above roll up most of these; the table is the complete leverage-ordered backlog.

| # | sev | skill(s) | finding |
| --- | --- | --- | --- |
| 1 | major | merge-branch/acceptance-map/closeout-check/git-hygiene | Protected-branch list copied verbatim ×3; git-hygiene resolves "protected" via a divergent config-glob with no literal fallback |
| 2 | major | merge-branch/git-hygiene | Operation-in-progress detection drifted: git-hygiene omits revert/REVERT_HEAD |
| 3 | major | review-family ×5 | Read-only/protected-action boundary copied as five divergent verb lists |
| 4 | major | impl-review/system-design-review/review-reviewer | `scrutinize-skill` lane omitted from three routing blocks |
| 5 | major | handoff ×4 | Three-path storage contract re-rendered in 6–7 surfaces despite single-home in AGENTS.md |
| 6 | major | closeout-check/agent-facing-design/skill-ux-design/writing-principles | "Don't invent installed-runtime layer" invariant restated ×5 with drift |
| 7 | major | grill-with-docs/improve-codebase-architecture/tech-debt-scan/design-exploration | "Leave writes uncommitted" default copied ×4, masking the two-lane commit-policy split |
| 8 | major | review-family ×5 | Bounded-review mechanism re-authored four ways |
| 9 | minor | handoff ×4 | Project-root resolution byte-identical ×4 (latent-drift trap) |
| 10 | minor | review-family ×5 | Evidence-floor re-authored five ways, split `unverified` vocabulary |
| 11 | minor | writing-principles/skill-ux-design/behavior-smoke-test | Validation ladder re-listed ×3, all omitting the quick_validate caveat |
| 12 | minor | skill-ux-design | Closeout template hardcodes a "no behavior smoke test" denial (should be a fill-in slot) |
| 13 | minor | caveman | Exit locked to two literal phrases while entry is intent-based (crude-rule-overreach) |
| 14 | minor | git-hygiene | `branchProtection` used for commit-gating but documented only as deletion-protection |
| 15 | minor | to-issues | No explicit next-lane handoff/stop after publishing (asymmetry vs to-prd) |
| 16 | minor | to-issues | Acceptance-criteria template fixed-shape but unguided (substitutive-fill risk) |
| 17 | minor | caveman | Trigger declared `/caveman` only, never `$caveman` |
| 18 | minor | load-handoff | Own trigger `/load` without `$load` |
| 19 | minor | search-handoffs | Own trigger `/search` without `$search` |
| 20 | minor | next-steps | example.md closing line collapses the offer/accept/ask-path handshake |
| 21 | minor | friction-to-guards | Instruction-prose handoff lane left unnamed (it is writing-principles) |
| 22 | minor | improve-codebase-architecture | Report-card "as before" dangling ref + field-label drift vs HTML-REPORT.md |
| 23 | minor | setup-matt-pocock-skills | Codex explicit-invocation lock incomplete (no agents/openai.yaml); seed names `/grill-with-docs` single-runtime |
| 24 | minor | writing-principles | Edit Gate restates the stay-in/route-out boundary 3× plus a Scope pre-statement |
| 25 | minor | tech-debt-scan | "Repo instructions" never names AGENTS.md/CLAUDE.md jointly |

## Deliberately NOT flagged (rejected as over-cut / not-real-duplication)

Recorded so they are not re-litigated. Verification judged these per-skill phrasing or unavoidable independent-load duplication, not drift-prone copied machinery:

- **Over-cut (per-skill):** claude-code-docs `openai.yaml` token form; writing-principles machinery enumeration vs agent-facing-design.
- **Not-real-duplication (clusters):** default-branch resolution order (merge-branch/git-hygiene/orient-status); the structural/behavioral/runtime **proof-class taxonomy** (8 surfaces — judged shared vocabulary, not a gate to single-home; *note: borderline, given AGENTS.md:246-253 is a plausible home*); "shared primary location" prose; the read-only **verb-list guardrail** (overlaps the confirmed P2 boundary finding but rejected as a standalone cluster); never-rm/use-trash rule; verification boundary (no-install/fetch/start-services); publish-authority stop; per-finding evidence-pointer requirement; "None found" discipline; `unverified` marker vocabulary.

## Settled-revisits (3) — confirmed, not reopened

- **The one `critical`-tagged protected-branch cluster → correctly downgraded to `major`.** The `main`-branch hook + always-loaded `AGENTS.md` bound the highest-damage case; all three literal-list skills defer to repo-defined branches first. Residual risk is drift among lower-stakes patterns + the git-hygiene mechanism divergence — real, but `major`. No `critical` stands.
- **execute-plan Defensible despite appearing in the gate cluster.** Its gate-at-start-of-work posture is correct per-skill behavior (it's an executor, not a commit-lifecycle gate); only the static prefix list it omits is the shared concern, fixed by single-homing — not by changing execute-plan.
- **Two opposed commit lifecycles are a correct two-lane policy, not a contradiction.** Lifecycle/trust skills auto-commit a verified scoped result; analysis/exploration skills leave writes uncommitted. The only defect is that the boundary lives in scattered prose rather than one documented decision (P-rank 7).

## Per-skill verdicts (48)

- **Defensible, no confirmed finding (32):** agent-facing-design, baseline, behavior-smoke-test, claude-code-docs, design-exploration, diagnose, execute-plan, gh-address-comments, gh-pr-review-loop, grill-me, grill-with-docs, implementation-planning, making-recommendations, markdown-reformat, markdown-synthesis, merge-branch, orient-status, outcome-interviewer, prototype, simplify-code, tdd, to-prd, zoom-out, exiting-worktrees, openai-docs, skill-benchmark, throughline, implementation-review, review-reviewer, scrutinize, scrutinize-skill, system-design-review. *(merge-branch, agent-facing-design, etc. appear in cross-cutting clusters as **consumers** of shared rules — the fix lands in the shared home, not the skill.)*
- **Defensible with a confirmed downgrade/nit (Defensible verdict, ≥1 finding):** acceptance-map, improve-codebase-architecture, next-steps, tech-debt-scan, to-issues, triage, friction-to-guards, save-handoff.
- **Minor revision (8):** caveman, closeout-check, git-hygiene, skill-ux-design, writing-principles, setup-matt-pocock-skills, load-handoff, search-handoffs.

## Recommended consolidation pass (sequenced)

One coherent remediation clears most majors. **Local `skills/` edits land immediately on merge; the handoff and review-family fixes are plugin-distributed and follow the Plugin Layout publish path (version bump + Codex republish + mirror).**

1. **`AGENTS.md` single-homes (local, highest leverage):** add the canonical protected-branch set + `chore/fix/feature` prefix list (P0); document the two-lane commit policy beside existing guidance (P-rank 7). Then trim the verbatim copies in merge-branch/closeout-check/acceptance-map and the repo-invariant restatements (P4) to cites.
2. **git-hygiene reconciliation (local):** add `revert`/`REVERT_HEAD` (P1); position `branchProtection` as the documented per-repo override on the canonical default (P0) and fix its reference doc (rank 14).
3. **Handoff plugin (publish path):** four skills cite the path-set + project-root home (P3, rank 9).
4. **Review-family plugin (publish path):** add the missing `scrutinize-skill` redirects; normalize opener/closer; single-home the read-only core list + evidence-floor + bounded-review contract in a plugin reference (P2, ranks 8/10).
5. **`$`-token + template sweep (local):** P5 tokens; P6 template fixes.

Each behavior-touching edit should carry a forward/smoke check; land on a working branch, fast-forward to `main`.

## Caveats & limits

- **Verification was conservative** — it favored precision (10 clusters + 2 findings rejected). The proof-class taxonomy rejection is the most debatable; revisit if a consolidation pass touches that area.
- **Over-consolidation guard.** Only *static constants* go to `AGENTS.md`. Per-skill *behavior* (protected-branch responses, execute-plan's gate posture, each review skill's verdict vocabulary) stays inline — you cannot single-home core behavior across independently-loaded skills.
- **skill-ux-design rank 12 severity.** The completeness critic argued `major`; this artifact keeps it `minor` — a verification-mode dry-run *validation* check is not a *behavior smoke test*, so the hardcoded line isn't necessarily false. The defect is fragility (fixed prose where a fill-in slot belongs), not a live false claim.
- **Completeness bound.** Cross-skill coverage is complete for the machinery classes found in `SKILL.md` bodies; a class confined to `references/`-only files could be unscanned. Three candidate unflagged classes were spot-checked and correctly excluded.
- **Plugin caches/mirror** were not inspected; this review is of source `SKILL.md` + referenced files.

## References

- Corrected workflow: `wf_2ef028f0-602` (output: task `w02u9w68u`). Superseded buggy run: `wf_5ee34a4a-4bc`.
- Apparatus sources: `skills/agent-facing-design/SKILL.md` (Two Kinds of Skill); `plugins/review-family/skills/scrutinize-skill/SKILL.md`.
- Prior backlog snapshot: `docs/plans/artifacts/skill-library-backlog-retriaged-2026-06-15.md`.
