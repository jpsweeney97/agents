# Prompt Workspace

The Prompt workspace is optional, sparse continuity state for replaceable wording. It is not Intent and not Evidence. Use it when candidates, revisions, target adaptation, or a user-visible output contract would otherwise lose important context; do not persist it merely because a template exists.

When target handling matters, record the target generator, version, and generation mode separately from the wording. Keep `active_prompt_id` and `active_prompt` separate from candidates and retained `previous_versions`. A candidate is proposed and cannot replace the active prompt until the user selects it or clearly continues work from it. Every `EDIT` creates a new version that retains its prior source, requested delta, unavoidable dependencies, and preserved locks.

Record the operation (`EXPLORE`, `BUILD`, `EDIT`, or `FINALIZE`), interaction depth, latitude, `latest_revision_delta`, target assumptions, output contract, and execution permission only when they affect future work. `execution_permission` is one of `compile_only`, `generate_image`, or `edit_image`; default it to `compile_only`, and select either pixel state only after an explicit request for the image itself. A repair brief from the reviewer is an `EDIT` source only when its rewrite authority and protected elements are explicit; it remains strict preservation.

The workspace may hold target-facing wording, but it must not redefine canonical visual meaning. Intent controls identity and locks; the compiler may reformulate, order, and compress without changing them. Evidence remains reviewer-owned.

Use [prompt-workspace-template.yaml](prompt-workspace-template.yaml) only when structured continuity is worth its cost; otherwise keep the same distinctions in prose.
