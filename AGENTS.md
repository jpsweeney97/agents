# AGENTS.md

Repo-specific instructions for `/Users/jp/.agents`. This repo is the single source for the skills served to both Codex and Claude Code, plus plugin sources, skill metadata, references, and the personal plugin marketplace manifest. Primary work is day-to-day skill editing.

## What The Skills Are For

The skills here are global artifacts, not tooling for this repo: Codex scans `$HOME/.agents/skills` and Claude Code serves skills through `~/.claude/skills`, so each authored skill is available across repos wherever its runtime runs — `skills/` in both Codex and Claude, `skills-claude/` in Claude only. This repo is the workshop; a skill's deployment and judgment surface is the runtimes it ships to, not `.agents` itself.

Judge a skill by its merit as a global capability, not by whether it fires in `.agents`. Merit has two sources, and either one earns a skill its place: leverage where it fires — a distinct job that pays off in the repos that need it, this one or any other — and cognitive-offload, the value a skill delivers to the human by running a careful procedure on demand. A skill that never triggers here is not thereby weak; its silence in `.agents` is not evidence against it.

Cognitive-offload deserves its own frame — it is the value an agent most often misjudges, and the one an agent should be able to name about its own work. It is the same source `agent-facing-design` names under Two Kinds of Skill, here raised to the merit altitude for judgment and trust skills alike. A skill's worth is not only what it makes the agent do; it is what it spares the human. A good skill is a careful procedure — the right steps, boundaries, proof discipline, and stop conditions — worked out once by its author, then summoned with a token and run on the human's behalf. So the human gets the complete, high-quality run every time without composing the prompt, holding the steps in mind, or checking afterward that none were skipped: it is the prompt they never had to type and the work they no longer have to supervise. That value accrues whether or not a strong model could improvise something similar — so "I could just do this myself" measures the agent's behavior, not the human's freed attention, and is never on its own a reason to discount a skill.

Whether to build or keep a skill turns on that merit, never on local observability. A skill's *absence* from `.agents` is at most a build-order or prune-fidelity hint — never a reason to build, not-build, keep, or cut it. An observed mis-fire or stolen fire here is different: that is the charter's own prune evidence, and fair grounds to cut. Global fire is also measurable now: the skill-usage ledger (`scripts/skill-usage-miner.py` → `~/.claude/logs/skill-usage-ledger.jsonl`, live-fed by a user-level PostToolUse hook) records skill invocations across all repos, so keep/prune deliberations should consult it — sustained global silence is legitimate prune input alongside mis-fire evidence, never an automatic verdict, and admission stays ungated by proof. This restates the build-and-prune model (`docs/agents/charter.md`) at the always-loaded altitude, because the recurring failure is re-imposing "prove it fires here first."

## Source Authority

- The checked-out working tree is the live skill source for both runtimes. Branch switches, rebase, stash, and bisect mutate the served skills immediately; edits in an isolated worktree go live only when they land on the checked-out branch.
- `CLAUDE.md` is an import shim (`@AGENTS.md`). Edit `AGENTS.md`, not the shim; instructions added only to `CLAUDE.md` never reach Codex.
- Do not edit files under `~/.claude/skills`; entries there are symlinks into this repo. Edit the repo source.

## Skill Layout And Delivery

- `skills/` is dual-runtime: Codex (>=0.137) scans `$HOME/.agents/skills` in place; Claude Code serves each skill through a symlink in `~/.claude/skills`.
- `skills-claude/` holds Claude-only or Codex-excluded skills. Codex must never scan it; it reaches Claude through the same symlinks.
- `skills-archive/` holds retired skills. It is outside both delivery paths (not scanned by Codex, never linked into `~/.claude/skills`); treat it as history, not live skill source.
- `exports/` holds skills re-targeted for claude.ai and uploaded by hand — a third delivery path with no delivery mechanism, since custom Skills do not sync across surfaces. It sits outside the other two (not scanned by Codex, never linked into `~/.claude/skills`), and the `SKILL.md` files there are build artifacts of the skills they name: edit the source in `skills/<name>/` and export again through `skill-export`, never the copy.
- After adding or renaming a skill, run `scripts/claude-skills-sync.sh --link <name>`; verify delivery with `--check` (it never deletes). Remove stale `~/.claude/skills` entries with `trash`. Bootstrap and recovery live in the script header; `--link-all` rebuilds the symlink farm.
- Claude-side symlink discovery and live reload are undocumented behavior, canary-guarded at session start.
- A `skills/` skill is dual-runtime, so name it to avoid both Codex-bundled names (`~/.codex/skills/`, including `.system/`: `openai-docs`, `skill-creator`, `skill-installer`, `plugin-creator`, `imagegen`, `pdf`, `doc`, `codex-primary-runtime`) and Claude Code bundled names (`code-review`, `debug`, `loop`, `claude-api`, `run`, `verify`, and similar). A `skills-claude/` skill is Claude-only: it must still avoid the Claude bundled names, but may intentionally reuse a Codex-bundled name (e.g. `openai-docs`) to re-author that capability for Claude, since Codex never scans `skills-claude/`.
- In skill text, name invocation tokens for both runtimes (`/skill-name` or `$skill-name`), name instruction files jointly (`AGENTS.md` or `CLAUDE.md`), and phrase routing to single-runtime skills availability-conditionally.

## Plugin Layout And Delivery

- `plugins/<name>/` holds the canonical dual-runtime plugin sources (currently `handoff`, `review-family`, `git-cycle`, `relay`, `plan-cycle`) in Claude format: `.claude-plugin/plugin.json` plus `skills/`. One source serves both runtimes; never create per-runtime copies.
- Claude Code loads each plugin dir in place through its `~/.claude/skills` symlink as a skills-directory plugin (`<name>@skills-dir`) — no marketplace, install, or cache. `SKILL.md` edits are live next session; hook/MCP/agent component changes need `/reload-plugins`. This discovery is also undocumented, canary-guarded behavior.
- Codex discovers `plugins/marketplace.json` implicitly as the personal `turbo-mode` marketplace but serves installed plugins from the versioned cache (`~/.codex/plugins/cache/turbo-mode/<name>/<version>`), not directly from source. On this machine, ChatGPT Desktop's embedded Codex app-server synchronizes a drifted local-marketplace source to that cache when it serves `plugin/list`, including pruning older version directories; `scripts/codex-plugins-sync.sh --publish <name>` is an explicit refresh route, not the sole cache-changing mechanism. `--check` reports only source/cache equality at the instant it runs: it cannot establish installation or activation, provenance or consent, or whether an applicable Gate B is open. Where Gate B governs a release, only an explicit, durable grant opens its publication/proving path. Bootstrap and recovery live in the script header.
- Bump the manifest `version` in lockstep with the behavior change it releases, and treat landing that bump as publish intent: a bump that lands on the checked-out branch goes live on both runtimes without further consent (Claude serves the landed tree through its symlinks; the app-server cache sync above publishes a landed bump to the Codex cache), so land a cut only when local liveness is intended and complete it promptly with `--publish`; when an open gate must hold publication, land the work without the cut and cut the release as a follow-up at grant time. The Codex cache is version-keyed, and version history is the only release signal the caches and mirror carry.
- Handoff storage contract: handoff skills write `<project_root>/.agents/handoffs/` (shared by both runtimes) and read legacy `.claude/handoffs/` and `.codex/handoffs/` as read-only fallbacks.
- The GitHub release mirror is a separate repo (`jpsweeney97/codex-tool-dev`), not a path under this one: its live checkout is `/Users/jp/Projects/active/codex-tool-dev` and the mirror tree is that checkout's `plugins/turbo-mode/`. Stale clones of the same repo exist on disk (e.g. under `scratch-workspace/deprecated-claude-skills/`) and share the same `origin`, so identify the mirror by this path, not by remote. It is updated only at explicit publish time by copying from this repo's sources.

## Marketplace Metadata

- `plugins/marketplace.json` is editable local metadata that Codex parses at runtime as a marketplace manifest; invalid entries are skipped silently. It is not proof of installation, activation, or runtime plugin state.
- Keep `source.path` entries relative (`./.agents/plugins/<name>`): the implicit personal marketplace root is `$HOME`, and Codex silently skips absolute paths. After edits, verify each referenced path exists and confirm resolution with `codex plugin list`.
- Codex reads `.claude-plugin/plugin.json` natively; the manifest `interface` block and `skills` field are Codex-facing and ignored by Claude Code.
- Make runtime claims (installation, activation, loaded skills, hooks) only from a runtime inspection path: installed cache, app-server `plugin/read`, `plugin/list`, `skills/list`, or `hooks/list`.

## Repo Docs

- `docs/agents/charter.md` — contracts charter governing admission, extraction, and retirement of behavior contracts. Skills and commands are build-and-prune and are not charter events (build/prune freely); consult the charter only before the gated events it names: authoring or retiring an always-loaded contract (a rule, an AGENTS.md line, or a hook), authoring a skill that can fire unattended or wields irreversible-effect tools, installing contract-shipping material, or deciding the fate of third-party material.
- `docs/agents/contract-decisions.md` — the append-only decision ledger the charter requires: one entry per gated charter decision (admission, fold, rejection, park, retirement of an ambient contract or third-party material; build-and-prune skill/command churn is not ledgered) with an evidence pointer. The durable, runtime-neutral record; append, never rewrite settled entries.
- `docs/agents/issue-tracker.md` — issues are tracked in GitHub Issues for `jpsweeney97/agents`.
- `docs/agents/triage-labels.md` — the default five-label triage vocabulary.
- `docs/agents/domain.md` — the single-context domain-doc layout.
- `docs/agents/contract-evaluation-methodology.md` — playbook (not an obligation) for testing whether a behavior contract is load-bearing and beneficial while escaping circularity: pre-register/seal, single-variable differential, blind cross-model arms, human cold-judge anchor, pilot before seal. Distilled from the judgment-trust apparatus arc (tests 1–5). Reach for it when a contract's value is the open question; overkill for ordinary edits.

## Blind Evaluations

This repo hosts blind, pre-registered evaluations (the judgment-trust apparatus tests under `docs/plans/`). In any such evaluation, never reveal apparatus state — reviewer or model outputs, intermediate scores, predictions, or arm identities — in any channel a current or potential ground-truth judge (human or a separate model) can see, until their independent judgment is recorded. Lost blinding is unrecoverable; re-administer to a fresh judge.

## Working Defaults

- Start file-changing work with `git status --short --branch`.
- Read the live targets before editing and match the existing skill shape. For behavior changes, inspect `SKILL.md`, companion metadata, referenced files, and related scripts together; when trigger, side-effect, proof, authority, or lifecycle behavior changes, update companion metadata too.
- Keep edits scoped to the requested skill, metadata file, reference, script, or marketplace entry.
- A minimal local skill can be only `SKILL.md`. Add metadata, references, examples, or scripts only when they reduce real load in the main skill file or support a concrete integration.
- Write Markdown prose one logical line per paragraph and per bullet; do not hard-wrap at a fixed column. This is the repo-wide convention for all Markdown here — `AGENTS.md`, support docs, `docs/`, `SKILL.md` bodies, and plugin sources. Leave fenced code blocks, tables, and YAML frontmatter as written. (Markdown renders a single newline as a space, so hard wrapping changes nothing on screen while fighting narrow viewports and bloating diffs; let the editor or renderer soft-wrap.)
- Reviewing Markdown diffs: one-logical-line prose makes plain `git diff` re-print a whole paragraph as deleted-plus-added for a one-word edit, burying the change and overflowing agent output caps. Review prose changes at word grain — `git diff --word-diff=plain` (also with `--cached`, `git show`, `git log -p`) — reading `--stat` first and scoping to file paths when output is large. Line-grain diff remains right for fenced code, tables, and YAML frontmatter.

Route skill work through the owning lane instead of inventing a separate workflow:

- `writing-principles` — obligation-only prose edits inside an existing skill, support doc, `AGENTS.md`, `CLAUDE.md`, or `agents/*.yaml`.
- `agent-facing-design` — before adding or materially expanding agent-facing obligations, proof standards, authority rules, lifecycle behavior, mutation boundaries, persistence, routing, or machinery. It also owns the judgment-vs-trust distinction: a skill whose value is better thinking is held to "does this protect and provoke better thinking?", a skill whose value is reliable execution to "is this reliable, and is the machinery single-sourced rather than copied?"; apply the bar per part for mixed skills. The canonical gate is `skills/agent-facing-design/SKILL.md`; do not duplicate it here.
- `scrutinize-skill` — review-only skill-contract critique. After the review is accepted, patch the owning skill surfaces directly — but when the patched skill is plugin-distributed (`scrutinize-skill` itself and the rest of `review-family` live in `plugins/review-family/`), the edit follows the Plugin Layout publish path (version bump, Codex republish, mirror), not the local-skill flow.
- New skill bundles, bundle-shape changes, generated metadata, and helper scripts — on Codex, the bundled `skill-creator`; on Claude, hand-author against `agent-facing-design` and `skill-ux-design`, validating with the Codex-bundled `quick_validate.py` (see Validation Ladder) via Bash. There is no Claude-side constructor skill, by design.
- `skill-benchmark` (Claude-only) — quantitative skill benchmarking and trigger/description optimization: with/without-skill eval runs and pass-rate, token, and time deltas with variance. On Codex, the bundled `skill-creator` owns this work.

## Skill Editing

`SKILL.md`:

- Keep YAML frontmatter parseable; quote descriptions that contain colons or similar punctuation.
- `description` is loader-facing routing text answering only "when should I read this skill?" and "when should I choose a different skill or none?". Prefer `Use when...` phrasing: user intent, target scope, concrete symptoms, and the smallest non-use boundary that prevents the likely misroute.
- Keep workflow steps, validation ladders, output formats, internal phases, and rationale out of frontmatter; they belong in the body. Name neighboring skills or exclusions only when selection-critical.
- Soft 25-60 word description budget; go past ~90 words only to prevent a specific likely misroute. Description length is a routing-clarity input, not a skill-quality score: a judgment skill is not lower-quality for sitting near the cap. Trim for routing precision, not for conformance.
- In the body, state expected behavior and defaults. For trust skills, also fix stop conditions and output shape — predictable shape is their value. For judgment skills, structure is fine when it organizes or provokes thinking (a rhythm, a forced comparison, a findings format) and a defect when it makes the judgment for the agent (fill-in sections completed to feel done, a rigid stop sequence that pre-empts thinking). See `agent-facing-design`, Two Kinds of Skill.
- Keep long rubrics, worked examples, and rationale in `references/` or `examples/`, named by purpose. Do not move behavior-critical instructions into a reference unless `SKILL.md` clearly says when to load it.

`agents/openai.yaml`:

- Companion metadata, not a substitute for the skill contract. It may be absent, and minimal metadata is acceptable. Keep the display name, short description, and default prompt aligned with the current `SKILL.md`.

Scripts:

- A script a skill invokes or references is a behavior surface. When editing one, inspect its callers or references and run a targeted script check, behavior check, or dry run when practical.

## Validation Ladder

Validate the exact surfaces you edited.

1. Standalone instruction Markdown (`AGENTS.md`, support docs): inspect the final diff and run whitespace checks such as `git diff --check`.
2. Parse edited `SKILL.md` frontmatter and edited YAML metadata. For metadata-only changes, parsing plus shape/alignment checks can be enough.
3. Inspect every referenced path from the edited surfaces; each must exist and match the role the instruction claims.
4. For script changes, run a focused script check or explain why no practical check exists.
5. For skill behavior changes, run the available local validator when one exists, and add one live invocation, forward test, or realistic dry run where practical. If no validator is available, say so and name the checks that replaced it.
6. `quick_validate.py` is structural frontmatter validation only, and its schema lacks some documented-valid Claude Code fields (`argument-hint`, `disable-model-invocation`): treat that specific "unexpected key" complaint as accepted and never resolve it by deleting the field; treat any other failure as real.
7. Do not waive loader errors, invalid YAML, missing referenced files, test failures, script/runtime errors, or behavior-contract failures. If validation fails or is blocked, do not claim the change works and do not create the automatic local commit.

Useful checks:

```bash
# When skills/<skill>/agents/openai.yaml exists:
ruby -ryaml -e 'YAML.load_file(ARGV[0])' skills/<skill>/agents/openai.yaml
python /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/<skill>
git diff --check -- skills/<skill>
```

Proof boundaries:

- For `skills/` and `skills-claude/`, the edited source is the live local skill source for future invocations; do not invent a separate installed-runtime proof layer for those files. Structural checks prove the files parse; only a realistic invocation, forward test, or dry run shows the changed behavior is followed. Installed/cache/marketplace proof matters only for plugin-distributed skills or other copied runtime surfaces.
- `plugin-eval` was intentionally uninstalled for this repo: do not run it, repair its wrapper, reinstall it, or treat its absence as an environment problem. Treat leftover `.plugin-eval/` contents as local artifacts and older notes or memories naming `plugin-eval` for local validation as stale.

## Git And Cleanup

- Do file-changing work on a working branch (`chore/`, `fix/`, `feature/`) and land it on `main` with a fast-forward merge; a Claude Code user-level hook enforces this by blocking edits on `main`.
- Protected-branch floor (this repo): never commit on the default branch or a protected branch. Treat repo-defined protected branches first; if the repo defines none, treat `main`, `master`, `develop`, and `release/*` as protected. This always-loaded floor governs work in this repo only; it does not travel to other repositories, where the `git-cycle` skills carry their own inline copy.
- Review `git diff --stat` and the relevant diff before staging or committing.
- For completed, focused, file-changing work, create a local commit by default after focused verification — unless the user asked not to commit, the turn was review-only or exploratory, validation is failing or blocked, the work is incomplete, or unrelated dirty files make safe staging ambiguous.
- Do not push commits, add remotes, create pull requests, sync mirror state, or otherwise publish unless the user asks. One standing carve-out: the local Codex republish that completes a landed version bump is authorized by the landed bump itself (see Plugin Layout And Delivery); mirror sync and push always remain ask-gated.
- Delete with `trash <path>`, never `rm`.
