# Repair Handoff

Use this path only after REVIEW or DIAGNOSE has established an exact source and rewriting is authorized.

1. Construct a constrained repair brief with `source_prompt_id`, `operation: EDIT`, `creative_latitude: strict_preservation`, `edit_scope: coherent_revision` (or a justified `surgical` scope), retained findings, required changes, protected elements, unaffected locks, prohibited additions, target, and rewrite authorization.
2. When runtime cross-skill invocation is available, hand it once to `$collaborative-image-prompt-architect` as `EDIT` with `strict_preservation`.
3. Verify the returned rewrite once against retained findings, required changes, protected elements, unaffected locks, and prohibited additions. Do not make a recursive handoff.
4. When invocation is unavailable, emit the repair brief. Only when the authorization mapping in `SKILL.md` permits it, implement the repair under the same brief and state that the reviewer retains an evidence-bounded review boundary.

Current target guidance or the applicable target compiler resolves target-specific wording; this reviewer does not claim that compilation, guidance, or one sample proves image quality.
