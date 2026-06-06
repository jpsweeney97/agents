# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Layout

This repo uses a single-context layout.

Expected locations:

- `CONTEXT.md` at the repo root
- `docs/adr/` for architectural decision records

If these files do not exist, proceed silently. Do not flag their absence or suggest creating them upfront. The producer skill, `/grill-with-docs`, creates them lazily when terms or decisions actually get resolved.

## Before exploring, read these

- `CONTEXT.md` at the repo root, if it exists
- Relevant ADRs in `docs/adr/`, if they exist

## Use the glossary's vocabulary

When output names a domain concept, use the term as defined in `CONTEXT.md`. Do not drift to synonyms the glossary explicitly avoids.

If the concept you need is not in the glossary yet, note that as a possible gap for `/grill-with-docs`.

## Flag ADR conflicts

If output contradicts an existing ADR, surface it explicitly rather than silently overriding it.
