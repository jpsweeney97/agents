# Dialogue Workflow

Use this adaptive workflow for prompt work. It is not an opening questionnaire, a generated-result diagnostic method, or a pixel-execution procedure.

## Router

Route skeptical prompt evaluation to `$scrutinize-image-prompt` `REVIEW`; generated-output analysis or repair to reviewer `DIAGNOSE`; and explicit pixel work to an active image tool only when explicitly requested. Otherwise choose `EXPLORE` for multiple directions or variants, `EDIT` for requested modification or target adaptation, `FINALIZE` for an accepted unchanged prompt, and `BUILD` for a coherent new prompt. A supplied existing prompt does not by itself select `EDIT`.

## Interaction depth and latitude

Always reconstruct the scene internally. In `direct`, make low-risk choices and continue; no opening interview. In `guided`, identify the single uncertainty that most changes the intended image, recommend the strongest choice with benefit and tradeoff, and ask one focused question. Surface the reconstruction only when it helps.

Set latitude independently: `strict_preservation` adds no material content; `tasteful_completion` fills low-risk gaps coherently; `exploratory_authorship` makes bolder proposals that remain unaccepted. Locks and reference controls outrank latitude.

## EXPLORE

Choose `premise_diversity` when alternatives should differ in premise, frozen moment, composition, relationship, spatial reading, or emotional reading. Choose `controlled_variation` only with all locks fixed and an explicit list of dimensions allowed to vary. Label candidates as proposals; selection or continued development alone makes one active.

## BUILD

Establish accepted facts, visual thesis, subject or event, viewpoint, frozen moment, three or four salience priorities, reference roles, and low-risk completion choices. Resolve only material uncertainty. Once coherent, produce the complete prompt; keep decision provenance, schema, rationale, and most measurements internal.

## EDIT

Pin the active prompt, requested delta, dependencies the delta forces, and unrelated locks that remain. Treat `only` or `identical` as `surgical`, an ordinary revision as `coherent_revision`, and an explicitly requested overhaul as `broad_rewrite`. Preserve the prior version and create a new one. Surgical work may adjust dependent camera, light, focus, or rendering for continuity, but cannot redesign the subject, event, setting, or mood. Target adaptation reformulates language without changing identity.

An authorized reviewer repair brief is an `EDIT` request with `strict_preservation`: retain its source prompt, apply only the authorized repair and essential dependencies, and protect named elements. Do not inspect, diagnose, or claim causal conclusions about the generated result here.

## FINALIZE

Require an accepted active prompt. Strip drafting residue and discussion, make no visual or semantic change, and emit the prompt exactly once. For “prompt only,” emit nothing else. If the prompt is still a loose proposal, return to `BUILD`.

## References and handoff

Inspect every available visual reference before naming observed controlled traits. For every material reference, name its role, controlled traits, permitted variation, and non-inferable traits. Use `identity_reference`, `environment_reference`, `wardrobe_reference`, `pose_reference`, `composition_reference`, `rendering_reference`, `inspiration`, `generated_evidence`, `edit_target`, or `unknown`. If it is inaccessible, retain only the user-declared role, mark visual traits unverified, and ask for reattachment only when they materially affect prompt work.

Default the workspace to `compile_only`. Resolve target authority from the user-named target-model skill or current guidance, then the active tool's current skill or guidance, then current official guidance only when needed. Compile target-specific wording only from that resolved authority. The compiler may reorder, compress, and phrase for the target but cannot change locks, import rejected ideas, or execute. Without resolved current authority, provide portable wording and say it has not been verified, tested, optimized, or called model-ready.
