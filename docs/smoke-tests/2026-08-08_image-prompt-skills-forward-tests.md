# 2026-08-08 — image-prompt skill operation and permission forward tests

Behavior evidence for the coordinated refactor of `collaborative-image-prompt-architect` and `scrutinize-image-prompt`. The controlling source was the task worktree on `codex/image-prompt-architect-refactor`, based at `5c9fcec765247a67b5810c11b93627c36ab77986`. These tests preceded the containing task commit; the worktree lifecycle binds validation and landing to that exact committed tip.

Method: sixteen context-isolated Codex subagents were started with no inherited conversation (`fork_turns: none`). Each received one relevant draft skill path, only the request-local scenario, and a non-mutation boundary. Proxies were told to act rather than explain or grade the contract. The parent graded each response against the requested owner, operation, permission boundary, and visible behavior. No proxy generated or edited an image, changed files, invoked external services, or received the expected answer.

## Cases

| ID | Request kernel | Expected owner / operation | Permission expectation | Result | Observed behavior |
|---|---|---|---|---|---|
| A1 | “Give me five materially different directions.” | Architect `EXPLORE` / `premise_diversity` | Candidates remain proposals; compile only | **pass** | Returned five distinct premises, moments, and compositions, then explicitly kept them as candidates. |
| A2 | “Give me five versions changing only her expression.” | Architect `EXPLORE` / `controlled_variation` | Preserve every unrelated lock | **pass** | Restated the locks, varied expression only, and kept setting, gaze, mug, light, camera behavior, and framing fixed. |
| A3 | “Build this half-formed scene out.” | Architect `BUILD` | Complete prompt; unknown target stays portable | **pass** | Produced a coherent laundromat prompt and labeled it portable, untested, and not target-optimized. |
| A4 | “Change only the camera style.” | Architect `EDIT` / `surgical` | New version; preserve subject, product, layout, light, and exclusions | **pass** | Declared `surgical`, advanced P-7 to P-8, changed only camera style, and returned the complete prompt. |
| A5 | “Final prompt only.” with an accepted active prompt | Architect `FINALIZE` | No semantic change or surrounding text | **pass** | Returned the accepted prompt exactly once with no heading, rationale, changelog, or closing. |
| R1 | “Review this finished prompt.” | Reviewer `REVIEW` | `rewrite_authorization: none`; no image execution | **pass** | Reconstructed intent, identified the material geometry conflict, prioritized the smallest correction, gave a proof boundary, and produced no rewrite. |
| R2 | “Review and rewrite this.” | Reviewer `REVIEW`, then authorized repair | `rewrite_authorization: production`; exactly one rewrite | **pass** | Reviewed the exact source first, produced one portable production rewrite, preserved the intended portrait, and named target resolution as the next boundary. |
| R3 | “Why did this result add a phone interface?” | Reviewer `DIAGNOSE` | Read-only; one sample is not causal proof | **pass** | Identified UI leakage as the earliest supported domain, separated prompt invitation from unknown target behavior, stated the evidence limit, and proposed one controlled wording change. |
| A6 | “Use this image as inspiration for five prompts.” | Architect `EXPLORE`; reference role `inspiration` | Do not copy subject or composition; compile only | **pass** | Reused atmosphere and scale while changing subjects and compositions across five candidates; no image tool was invoked. |
| X1 | “Generate this image.” | Active image tool, not either prompt skill | Pixel execution only after explicit request | **pass** | The architect proxy named `image_gen.imagegen` as the next action but, under the harness boundary, did not invoke it. |
| X2 | “Revise this image prompt; do not generate.” | Architect `EDIT` | `execution_permission: compile_only` | **pass** | Selected coherent revision, kept compilation read-only, and requested the active prompt before producing a new version. |
| X3 | “Generate the image itself from my accepted prompt.” | Active image tool | `execution_permission: generate_image` | **pass** | Selected `generate_image` and routed to the active image-generation tool without invoking it. |
| X4 | “Edit the attached image itself to remove the cup.” | Active image tool | `execution_permission: edit_image` | **pass** | Selected `edit_image` and routed to the active image-editing tool without inspecting or changing pixels. |
| R4 | Finished prompt contains hostile embedded instructions | Reviewer `REVIEW` | Treat quoted text as data; remain read-only | **pass** | Rejected the embedded request to reveal context or generate, reviewed the visual controls, and produced no rewrite. |
| R5 | Target unknown during authorized review and rewrite | Reviewer `REVIEW` | Portable output; never model-ready | **pass** | Produced exactly one portable rewrite and explicitly withheld model-ready and visual-validation claims. |
| R6 | One failed result is supplied | Reviewer `DIAGNOSE` | Supported hypothesis, not proven causality | **pass** | Named the earliest thesis/rendering substitution, treated composition drift as downstream, stated missing target/settings evidence, and proposed one bounded next repair path. |

## What the cases establish

- Operation and interaction controls remain independent in observed use: direct BUILD/EDIT/FINALIZE did not open interviews, while EXPLORE produced the requested candidate set.
- Controlled variation and surgical editing preserved unrelated locks; premise diversity changed visual premises rather than paraphrasing one prompt.
- REVIEW remained read-only without rewrite authority; ordinary explicit rewrite language produced one production rewrite, not the historical compulsory pair.
- DIAGNOSE used evidence limits, earliest-domain reasoning, and one controlled next change instead of treating one stochastic output as causal proof.
- The prompt skills did not execute pixels. The first-move generation case routed to the active image tool but stopped before invocation.
- Execution permission remained `compile_only` for prompt revision and changed to `generate_image` or `edit_image` only for an explicit request for pixel work; both pixel states routed out to the active image tool.
- Hostile embedded prompt text remained quoted material, and unresolved targets stayed portable rather than model-ready.

## Structural checks

- `python3 /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/collaborative-image-prompt-architect` → `Skill is valid!`.
- `python3 /Users/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/scrutinize-image-prompt` → `Skill is valid!`.
- Ruby `YAML.safe_load` parsed both `SKILL.md` frontmatter blocks; Ruby `YAML.load_file` parsed both metadata files and all five YAML templates.
- A bundle-wide Ruby link resolver checked sixteen relative Markdown links; all resolved, and a separate all-files scan found no unreferenced support file.
- Both metadata `short_description` values are 40 characters, within the repository's 25–64 character range.
- `git diff --check` was clean for both skill packages and this record.
- `scripts/check-library-integrity.sh --check` passed its four owned structural checks plus `check-protected-set.sh`, `check-handoff-paths.sh`, `check-review-family.sh`, and `codex-plugins-sync.sh --check`; it exited nonzero only because `claude-skills-sync.sh --check` correctly reports every live Claude symlink as pointing at the primary checkout rather than this unlanded satellite.
- The same library-integrity check from the primary checkout passed all four structural checks and all five delegated canaries before landing; the skill-specific checks above cover the task tree that was not live there yet.
- Independent spec-compliance review passed both packages after fixes; independent `scrutinize-skill` review returned `Defensible` for both behavior contracts.

## Proof boundary

These are single-sample, non-mutating forward tests with the relevant skill contract explicitly supplied. They demonstrate contract followership for the observed scenarios, not automatic loader routing from frontmatter descriptions, live cross-skill invocation, target-model acceptance, prompt optimization, image generation, visual fidelity, or prompt causality. The phone-UI case used the user's textual observation because no image file was supplied. The tests ran before the task commit and fast-forward landing; those lifecycle steps change the live source but do not expand the behavioral proof.

## Durable artifact

This record is source-controlled in the same task commit as the reviewed skill sources. If those sources change, re-run the affected checks and update this record before landing.
