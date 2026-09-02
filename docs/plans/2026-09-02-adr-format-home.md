# ADR-FORMAT.md home: how `decision-record` can join `decide`

Date: 2026-09-02. Status: proposed, awaiting JP's decision. Nothing here is built.

Question (left open by the 2026-09-02 plugin-bundle certificate, `docs/plans/2026-09-02-plugin-bundle-candidates.md` §Open): `decision-record` binds `../grill-with-docs/ADR-FORMAT.md` as the single source of the ADR format and forbids forking it, so it could not sit in the `decide` plugin. Where should that file live so `decision-record` can join?

## Recommendation

Move the single source into the plugin at `plugins/decide/references/ADR-FORMAT.md`. Leave a git-tracked relative symlink at the old path, `skills/grill-with-docs/ADR-FORMAT.md`, pointing at it. Move `decision-record` into `decide` as version 1.1.0 by the copy-first procedure. The two standalone consumers (`grill-with-docs`, `improve-codebase-architecture`) keep their existing references unchanged, because the alias makes the old path still true. If `grill-with-docs` is ever packaged, the alias becomes a byte-identical copy with a drift check; that fallback is decided now so nobody re-derives it.

## Facts the design rests on

1. **Three consumers read the file.** `grill-with-docs/SKILL.md:96` links `./ADR-FORMAT.md`; `improve-codebase-architecture/SKILL.md:91` links `../grill-with-docs/ADR-FORMAT.md`; `decision-record/SKILL.md:24` links `../grill-with-docs/ADR-FORMAT.md` and at `:26` says "do not relocate it (moving it touches every consumer for no gain). If decision-record proves the natural home for the ADR lifecycle, flag relocation as a future cleanup." The maintenance note at `grill-with-docs/SKILL.md:102` names both outside consumers.
2. **What the file is.** 531 words: convention detection, the template, the status vocabulary, numbering, the three-part gate, and what qualifies. `decision-record` consumes all of it and alone owns the lifecycle (status changes, supersession chains). `grill-with-docs` and `improve-codebase-architecture` consume the gate, template, and numbering to offer an ADR mid-session.
3. **Churn.** Three commits since the import (`5e52b7c` import, `b68b952` the `Revisit when` field, `3da8e35` the convention-detection fold on 2026-09-01). As a plugin file every future edit is a `decide` release: manifest bump, CHANGELOG, Codex republish, mirror on ask.
4. **Fire evidence** (`~/.claude/logs/skill-usage-ledger.jsonl` through 2026-09-02, Claude fires only, session co-occurrence not causation). `decision-record`: 19 sessions in 3 repos; 6 of them also fired a `decide` member (`making-recommendations` 3, `design-exploration` 3); 0 fired `grill-with-docs`; 0 fired `improve-codebase-architecture`. `grill-with-docs`: 31 sessions; 0 with `decision-record`; 2 with a `decide` member. In observed use, `decision-record`'s neighbor is `decide`, not the skill that currently holds its format file.
5. **The delivery boundary.** A plugin skill on Codex runs from `~/.codex/plugins/cache/turbo-mode/decide/<version>/`, a copy of the plugin directory and nothing else, so anything a plugin skill cites must be inside the plugin. Standalone skills run in place on Codex (`~/.agents/skills/<name>/`) and through a per-skill symlink on Claude (`~/.claude/skills/<name>` → `~/.agents/skills/<name>`; `~/.claude/skills/decide` → `~/.agents/plugins/decide`).
6. **Which path forms work from a standalone skill** (scratchpad test, 2026-09-02, both resolution modes). A file inside the skill's own directory always resolves. A sibling reference `../<skill>/<file>` resolves under kernel resolution (the physical parent is `skills/`) and under lexical resolution (the farm sibling exists). A direct `../../plugins/decide/references/ADR-FORMAT.md` resolves under kernel resolution but fails under lexical normalization on Claude (it becomes `~/plugins/...`). So no single path text for a plugin file works from a standalone skill on both runtimes without runtime-conditional wording.
7. **A relative symlink at the old path resolves in every case tested.** `skills/grill-with-docs/ADR-FORMAT.md → ../../plugins/decide/references/ADR-FORMAT.md` read in place, read through the Claude farm, read as a sibling from another farm entry, under both physical and lexical resolution. An edit made through the alias lands in the canonical. Git tracks it as mode `120000`; `git diff --check` is clean. The kernel resolves a symlink's own `..` against the link's physical directory, which is why the alias is immune to the problem in fact 6.
8. **Checker behavior.** `scripts/check-library-integrity.sh` check 2 validates only cited tokens that start with `references/`, `scripts/`, or `examples/` (with `../` prefixes). `ADR-FORMAT.md` at a skill root is unvalidated today. A `../../references/ADR-FORMAT.md` citation from inside the plugin is validated (the `handoff` precedent). A standalone citation containing `plugins/decide/references/...` would produce a false dangle, because the `references/...` substring is resolved against the skill directory and the repo root. Check 3 (orphans) covers only per-skill `references/`, `scripts/`, `examples/` directories, so a plugin-level `references/` is outside it, as `handoff`'s already is.
9. **Precedents.** Plugin-level `references/` shared by several skills and carried into the Codex cache: `plugins/handoff/references/` (verified in `cache/turbo-mode/handoff/3.3.0/references/`). Controlled copies with a drift check: `scripts/check-protected-set.sh` (one sentence across seven surfaces), `scripts/check-review-family.sh`. Derived copies with drift reporting: `exports/` and `scripts/exports-drift.sh`. Tracked symlinks in this repo: none today; this would be the first. Adding a skill to a plugin is a minor bump (`git-cycle` 1.7.0 for `land`).
10. **Settled and not reopened here.** `decide` holds seven skills and `pressure-test` (where `grill-with-docs` belongs) is separate because its skills challenge a position rather than form one. The certificate explicitly left the long-term home of `ADR-FORMAT.md` open; this document answers only that.

## Options

| Option | Single source? | Works on both runtimes? | Release tax | Machinery added | Verdict |
|---|---|---|---|---|---|
| A. Canonical into `decide`; symlink alias at the old path | Yes | Yes (fact 7) | `ADR-FORMAT.md` edits become `decide` releases | One tracked symlink, no script | **Recommended** |
| B. Canonical into `decide`; standalone consumers cite the plugin path | Yes | No (fact 6); check 2 false-dangles (fact 8) | Same as A | Runtime-conditional path text | Rejected |
| C. Canonical into `decide`; byte-identical copy at the old path plus a drift script | Controlled copy | Yes | Same as A, plus two files per edit | New script and canary line | Fallback for when `grill-with-docs` is packaged |
| D. Neutral repo home (`docs/agents/` or a root `references/`) | Yes | Standalone skills only; unreachable from the Codex cache (fact 5) | None | None | Rejected: `decision-record` still could not join |
| E. Status quo: `decision-record` stays standalone | Yes | Yes | None | None | Keep only if JP declines the join; fact 4 argues against |
| F. `grill-with-docs` joins `decide` too | Yes | Yes | Larger | None | Rejected: reopens a settled certificate with no new evidence (2 of 31 co-fires) |
| G. Inline the format into `decision-record`'s body | Yes | Yes | Same as A | None | Rejected: makes a fire-time surface the reference target of two outside skills |

Why A over C now: the format file is a trust surface, and `agent-facing-design` holds trust machinery to "reliable and single-sourced rather than copied." A symlink is single-sourced with no script; a controlled copy is the tool for a boundary a symlink cannot cross, and today no such boundary exists (both outside consumers are standalone skills in this repo). C is pre-decided as the replacement the moment one does.

## The recommended design in detail

Files:

- `plugins/decide/references/ADR-FORMAT.md`: the canonical, moved with `git mv` so history follows. Plugin-level rather than under `skills/decision-record/references/` because two skills outside the plugin read it; the `handoff` layout is the precedent.
- `skills/grill-with-docs/ADR-FORMAT.md`: relative symlink `../../plugins/decide/references/ADR-FORMAT.md`. `CONTEXT-FORMAT.md` stays a real file where it is.
- `plugins/decide/skills/decision-record/SKILL.md`: the body, byte-identical except the one paragraph that must change (below).
- `skills/decision-record/`: retired after the live-load gate, as in the three prior packagings.

Text edits, all of them:

- `decision-record`, §Reuse the ADR format: the link becomes `../../references/ADR-FORMAT.md`. The paragraph beginning "decision-record is registered as a consumer" is replaced by: the format ships in this plugin; `grill-with-docs` and `improve-codebase-architecture` read it through the alias at `skills/grill-with-docs/ADR-FORMAT.md` in the source repo; a change to the format is a `decide` release. "Restate none of it" and "no parallel dialect" stay. §Output path's "per the detection rule in `ADR-FORMAT.md`" is a name, not a path, and stays.
- `grill-with-docs/SKILL.md:96`: unchanged. `:102` maintenance note: rewritten to say `ADR-FORMAT.md` here is an alias of `plugins/decide/references/ADR-FORMAT.md`, owned by `decide`, edits to it are `decide` releases; `CONTEXT-FORMAT.md` is real and consumed by `improve-codebase-architecture`; if this skill is renamed, moved, or packaged, the alias must become a byte-identical copy with a drift check.
- `improve-codebase-architecture/SKILL.md:91`: unchanged; the sibling reference resolves through the alias (fact 7).
- `plugins/decide/.claude-plugin/plugin.json`: version 1.1.0; a bare starter prompt for `decision-record` (it is not explicit-only).
- `plugins/decide/README.md`: skill list plus a Writes-table row: writes `docs/adr/NNNN-slug.md`, edits an older ADR's `Status` line on supersession, makes a local commit `docs(adr): ...`, never pushes.
- `plugins/decide/CHANGELOG.md`: a 1.1.0 `Added` entry naming the skill and the format file's move.
- `plugins/decide/PRIVACY.md`: `decision-record` reads whatever source is supplied (conversation, transcript, PR thread) and writes only local files; no new off-machine path.
- Unchanged: `scripts/codex-plugins-sync.sh` (plugin already in the bootstrap list), `scripts/check-protected-set.sh` (no protected sentence in either skill), `AGENTS.md` (the plugin enumeration is the same six), bodies that name `decision-record` bare (`recheck-investment:46`, `grill-with-docs:11`) per the bare-token precedent. No ledger entry: packaging is build-and-prune.

Version: 1.1.0. Adding a skill lets the unit do something new.

Procedure (the Era 144 to 146 copy-first shape, both landings through `worktree-task-cycle` in the `decision-record` satellite, which the route guard requires for these surfaces):

1. Landing 1, `feature/decide-decision-record`: the `git mv`, the symlink, the skill copy with its paragraph edit, the manifest bump, CHANGELOG, README, PRIVACY, the `grill-with-docs` maintenance note. Because the move and the alias land in the same commit, the original `decision-record` keeps resolving (`../grill-with-docs/ADR-FORMAT.md` → alias → canonical); there is no window with two real copies.
2. Validation for landing 1: `quick_validate.py` on the copy; JSON parse of both manifests; `check-library-integrity.sh` (check 2 now validates the in-plugin citation); `git diff --cached --check`; `ls -l` on the alias; `cat ~/.claude/skills/grill-with-docs/ADR-FORMAT.md` and `cat ~/.claude/skills/improve-codebase-architecture/../grill-with-docs/ADR-FORMAT.md`; `codex-plugins-sync.sh --publish decide` and cache byte-identity; a fresh `claude -p` listing `decide:decision-record`; a fresh `codex exec ... < /dev/null` listing `decide:decision-record`; one bounded load probe of `grill-with-docs` per runtime that reads `ADR-FORMAT.md` and reports its first heading, which is the alias proven in real fire rather than in a scratchpad.
3. Landing 2, `chore/decide-retire-decision-record`: trash `skills/decision-record/`, trash the bare `~/.claude/skills/decision-record` link, run the fleet check (the `decision-record` identity is MISSING during the window and settles after retirement, as the twenty prior moves did).
4. Mirror sync on JP's ask; push under `/land`.

The build passes the `agent-facing-design` gate before landing 1: it changes persistence (where the format lives), routing (a skill moves plugins), and adds one mechanism (the alias). This document is the consult's input.

## Risks and limits

- **First tracked symlink in the repo.** Any future script that walks with `find -type f` skips it; acceptable, because the alias is never the canonical. `git ls-files -s` shows mode `120000`. `skill-export` would need to dereference if `grill-with-docs` is ever exported (it is not today).
- **Claude's Read tool was not itself tested**, only kernel and lexical resolution of the paths it would receive. The landing-1 live probe closes that.
- **Never put a symlink inside a plugin.** The Codex cache copy and the mirror sync would carry a link, not the file. Untested and avoided by construction: the real file is inside the plugin, the alias outside.
- **Release tax lands on two more surfaces.** `ADR-FORMAT.md` (3 edits in 3.5 months) and `decision-record` (4 commits since 2026-07-07) become `decide` releases.
- **Source and cache can differ** between a landed format edit and its republish: `grill-with-docs` reads the source through the alias, `decision-record` on Codex reads the cache. `AGENTS.md` already requires completing a landed bump promptly with `--publish`.
- **The join itself rests on co-occurrence.** Fact 4 is session co-firing on Claude only. It says where `decision-record` is used, not that the bundle causes anything.

## Not decided here

- Whether to do the join at all (JP's call; this document only shows it is buildable and how).
- Placement of `next-steps`, `to-questionnaire`, and `decision-owner-map`.
- Any change to the format's content.
