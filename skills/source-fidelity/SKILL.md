---
name: source-fidelity
description: "Use when the user asks whether a derived text or structured document faithfully carries its source under the requested transformation, including omissions, unsupported additions, changed meaning, exact literals, or structure. Read-only. Do not use to create or repair the derivative, assess writing quality, review code against a spec, or judge visual or audio fidelity."
---

# Source Fidelity

Check an existing derivative against its source material and the transformation the user requested. Report discrepancies; do not repair either artifact.

## Boundary

- Work with readable text and structured documents, including transcripts, Markdown, records, and skill exports. Format-specific extraction may help read a document, but an incomplete extraction cannot prove the whole document faithful. Do not claim visual layout, image, audio, or code-behavior fidelity.
- This is an independent post-transformation check. Authoring skills own creation and revision; `implementation-review` owns completed code against a plan or spec. General quality critique without a source-to-derivative question belongs elsewhere.
- Do not edit files, stage, commit, or publish during this audit. Report in chat by default; save the audit only if the user requests a file. If the request also asks for repairs, finish the audit and stop; repair is a separate follow-up task.

## Establish the comparison

1. Identify the exact source set, derivative, versions or current file state, and requested scope. Read the artifacts themselves, not only an author's summary or an older handoff. A diff containing before and after text supports a conclusion about that diff, not automatically the whole artifact.
2. State the setup briefly: `Comparing <source> → <derivative>; allowed changes: <rule>; scope: <scope>; read-only.` Make a consequential inferred rule visible so the user can correct it.
3. Determine what must remain exact, what meaning must carry through, what may be omitted, reordered, or rewritten, and what the task intentionally excludes. Use the user's transformation request rather than treating all differences as defects. If a missing or ambiguous rule would change the conclusion, ask one focused question. If a required artifact is inaccessible, stop and name it rather than substituting another.

## Check fidelity

- Cover the complete named scope when possible. Divide a large comparison into sections or records; never silently sample and then give a whole-artifact conclusion. If full coverage is not possible, name the inspected and uninspected portions.
- Compare both directions. For each source element the transformation must retain, find its counterpart in the derivative. For each substantive derivative claim or record, find support in the source or an explicitly allowed addition. Look for missing content, unsupported additions, altered meaning or certainty, misplaced attribution, and broken relationships; inspect wording, order, names, numbers, markers, metadata, links, and structure when the transformation makes them relevant.
- Use diffs, hashes, counts, parsers, or normalized-text comparisons for requirements they can actually prove. Read source and derivative context to judge meaning. A structural or exact-text check does not establish semantic fidelity; a text extraction does not establish fidelity of material it may have skipped.
- Distinguish permitted compression or adaptation from a material discrepancy. Do not flag a change merely because its words differ when the requested transformation allowed rewriting.

## Report

Lead with the strongest conclusion the checked scope supports: material discrepancies found, no material discrepancy found in the checked scope, or unable to determine. Never call an uninspected artifact faithful.

For each material discrepancy, give the source location, derivative location or expected location if missing, the governing transformation rule, the observed difference, and why it matters. Keep a clean result short. Name any consequential inferred rule, coverage limit, inaccessible material, or extraction limit. Suggestions may identify a next repair, but do not perform it in this skill.
