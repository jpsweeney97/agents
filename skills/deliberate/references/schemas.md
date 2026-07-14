# deliberate — schemas, record key set, bounds, content identity

Prose renderings of the canonical schemas. `references/contract-data.yaml` is the single machine-readable source: the validator loads it at run time, and every generated block below is mechanically compared against it by `deliberate-validate.py check-renderings` in the validation ladder.

Reload point: the orchestrator re-reads this file when composing or validating any envelope, run-state item, or capsule after compaction.

## Content identity, one algorithm

A content identifier is the full SHA-256 of the target's raw bytes (displayed 12-hex-truncated in chat, stored full in envelopes and the capsule). Path-kind rules: a named path must resolve, symlinks followed, to a regular file — hashed directly — or a directory, expanded once at setup into its recursive regular files in sorted relative-path order, each pinned individually (the expansion manifest is part of the identity; a symlinked or non-regular descendant is unpinnable). Anything else is unpinnable — preflight `invalid invocation` at setup, `evidence unavailable` at re-run. Identity is byte-exact and runtime-neutral, so a Claude-produced capsule and a Codex re-resolution of the same input agree or the drift is real.

```bash
uv run --script scripts/deliberate-validate.py identity --data references/contract-data.yaml [--as-evidence] <path>...
```

The validator's own identifier is verified with the platform hasher, never with itself: `shasum -a 256 scripts/deliberate-validate.py` (or equivalent) before every invocation.

## Declared bounds

Each invocation-facing bound is a correctable default, echoed when it binds; the two parse caps are the validator's own boundary.

<!-- generated:bounds -->
- `in-packet-evidence-bytes`: 262144
- `directory-expansion-max-descendants`: 512
- `named-evidence-expanded-bytes`: 67108864
- `per-stage-retrievals`: 32
- `verbatim-directive-history`: 8
- `capsule-bytes`: 262144
- `parse-bytes`: 1048576
- `parse-depth`: 32
<!-- /generated:bounds -->

## The labeled record key set

Exclusion records (Prune) and disposition records (Recommend) share one key set. Envelopes and the capsule carry the keyed YAML form; chat renders the labeled text template in `references/methods.md`. Prune's cut bases are `constraint`, `equivalence`, `dominance`, `survivor budget`; Recommend's are `post-prune filter`, `post-prune dominance`, `post-prune collapse`, `only-serious-option rival`.

<!-- generated:record-keys -->
- `option` — required. complete original wording, provenance flag intact — validation rejects paraphrase
- `status` — required; one of: active, revived. revived — historized by a revival directive: capsule history only, outside Contest eligibility and every packet
- `delegation` — required. what the invocation authorized here
- `predicate-source` — required; one of: direct user rule, agent-derived proposition
- `cut-basis` — required; one of: constraint, equivalence, dominance, survivor budget, post-prune filter, post-prune dominance, post-prune collapse, only-serious-option rival
- `epistemic-status` — required; one of: fact-established at comparable resolution, contestable sketch-depth judgment
- `reason` — required
- `evidence-provenance` — optional. list of {source, retrieved-at} for each external fact the reason or epistemic status relies on; each must resolve to a stored or same-envelope retrieval
- `load-bearing-premise` — required
- `strongest-case` — required. written before the kill
- `revive-if` — required
- `evidence-warning` — optional
<!-- /generated:record-keys -->

## deliberate-envelope/v1

One fenced YAML document per stage return: UTF-8, fixed key set (unknown keys rejected), prose values as block scalars — transport, never a semantic form the judgment agent fills to feel done.

<!-- generated:envelope-keys -->
- `schema` — required; constant `deliberate-envelope/v1`
- `stage` — required; one of: generate, prune, shape, recommend, contest
- `status` — required. three-class grammar, mechanically enforced: `completed`, `exit: <the named honest exit>`, or `failed: <reason>`
- `artifacts` — required. map carrying exactly the stage's obliged-artifact keys; each value present, `not produced: <reason>` (never on a completed stage), or (conditional artifacts only) `not applicable`
- `retrievals` — required. `none`, or list of {source, retrieved-at, fact, concerns} — concerns is `candidate-neutral` or the list of every candidate the fact names, evidences, or was retrieved to investigate; capped by bounds.per-stage-retrievals
- `encounters` — required. `none`, or list of {kind: withheld-class | instruction-like, where, note} per the read-isolation rule
- `pins` — required. list of {surface, id} — the constituent and evidence identifiers the stage actually verified; `none` when the stage loaded no pinned surface
- `model` — required. effective model when observable; `unknown` otherwise
<!-- /generated:envelope-keys -->

## deliberate-runstate/v1

Every orchestrator-written run-state store item; helper-validated at write exactly as envelopes are at acceptance. Item files are named `<seq>-<kind>[-<stage>].yaml` under the store root.

<!-- generated:runstate-keys -->
- `schema` — required; constant `deliberate-runstate/v1`
- `kind` — required; one of: echo, decomposition, pins, envelope, brief-render, terminal-claim, capsule-progress, capsule-import
- `run` — required. run identifier; every item carries it and must match the echo item's
- `seq` — required. monotonic write sequence integer; the echo item is seq 0 and the store's first write
- `stage` — optional. required for envelope and brief-render items
- `body` — required. keyed payload per kind; fixed top-level key set per body-keys below

Body key sets per kind:

- `echo`: `invocation-wording-initial`, `directives`, `fields`
- `decomposition`: `frame`, `candidates`, `stakes`, `soft-prefs`, `values`, `composition-provenance`
- `pins`: `constituents`, `method`, `evidence`, `in-packet`
- `envelope`: `document`, `amendments`
- `brief-render`: `brief-id`
- `terminal-claim`: `terminal`, `claim`, `survivor`
- `capsule-progress`: `capsule`
- `capsule-import`: `capsule`
<!-- /generated:runstate-keys -->

## deliberate-capsule/v1

The recovery capsule (and, with `not produced` markers and a recorded failure terminal, the failure capsule). Every key is present on every capsule; `capsule-complete` is the final key, carrying a content identifier over every byte of the document strictly before the line on which it appears — a terminator-less or identifier-mismatched paste fails validation as incomplete. The whole rendered capsule and any pasted capsule are bounded by `capsule-bytes`.

<!-- generated:capsule-keys -->
- `schema` — required; constant `deliberate-capsule/v1`
- `run` — required
- `terminal` — required. the recorded terminal name, or `close rendered` when Recommend's close stands
- `effective-contract` — required. map: frame, field-mode, constraints, values, soft-prefs, stakes, evidence-inputs, evidence-authorization, evidence-identity, method-identity, survivor-budget, degradation-permission, bounds, invocation-wording: {initial, directives (verbatim within bounds.verbatim-directive-history, older collapsed to content identifiers), source-capsule-id}; each contract field carries {value, provenance} so an import restores the exact echo
- `setup-decomposition` — required. map: frame, candidates (each {wording, provenance-flag, authority-note}), stakes, composition-provenance ({invocation-span, delegation-span})
- `recommend-authority-packet` — required. survivor wordings, ordering with provenance, per-survivor authority notes, any overflow disclosure, stakes/reversibility
- `original-field` — required. complete generated or user-supplied field — present whenever any field was validated; `not produced: <reason>` only on a failure before Generate returned a validated field
- `generation-boundary` — required. untouched-fixed-points line | `Generate not run: closed-to-widening` | not produced
- `survivors` — required
- `overflow` — required. any disclosed budget overflow with its blocked-cut disclosures
- `records` — required. every exclusion and disposition record with its `status`
- `retrievals` — required. the run's accepted retrievals in full — each with producing stage, source, retrieval time, and effective `concerns`
- `surface` — required. Shape's comparison surface, verbatim when produced
- `consequences` — required. Shape-recorded constraint consequences
- `close` — required. Recommend's close, verbatim when produced
- `registered-leans` — required. Recommend's registered leans ({agent-first-lean, user-visible-lean}), verbatim when produced
- `terminal-claim` — required. the close-less terminal's claim item ({terminal, claim, survivor}) when one was recorded
- `exclusion-check` — required. the rendered exclusion check line
- `provisional-seed` — required. marked unaccepted when present
- `revival-instructions` — required
- `proof-boundary` — required. map: packet-isolation, read-isolation, constituent-pins, method-identity, effective-models, evidence-scope-used, containment, store-path, collapses, not-proven
- `capsule-complete` — required. final key; content identifier over the document body above it
<!-- /generated:capsule-keys -->

## Validator exit codes

`0` pass · `1` validation failure · `2` refusal (unauthorized read, off-column request, unsupported schema, bound breach, usage) · `4` required run-state item absent — the orchestrator maps exit 4 to `store failed: read`, and exit 2 on a pasted capsule's schema version to the preflight refusal (a capsule under an unsupported schema resumes only through a shipped migration, never reinterpreted).
