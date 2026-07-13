---
name: injection-safe-inputs
description: "Use when designing or vetting how one trust boundary handles untrusted input — a request body, upload, webhook, query param, or file path: identify every sink the input reaches (SQL, shell, path, HTML/JS, template, LDAP), apply the sink-correct defense, cover mass assignment, deserialization, and size/type limits, and prove it with a must-block/must-pass payload table. Not for hardening one regex (regex-craft), LLM prompt injection, or a repo-wide vulnerability sweep."
---

# Injection-Safe Inputs

Design how one trust boundary handles untrusted input — sink-first, one named defense per sink — and prove it with a must-block/must-pass payload table, never with reassurance. Invocation: `/injection-safe-inputs` or `$injection-safe-inputs`.

A forcing pass over one trust boundary — a request body, an upload, a webhook, a query parameter, a file path — that traces the input to every sink it reaches, applies the sink-correct defense at each, dispositions mass assignment, unsafe deserialization, and size/type limits, and proves the result with a concrete payload table in two halves: executed where a running surface exists, honestly labeled authored-not-executed where none does. It edits on a working branch when applied; it never pushes, opens a PR, or publishes unless asked.

## Shape — a forcing pass over one boundary

**Pin the boundary and follow the data first.** The one entry point under design — request body, upload, webhook, query parameter, file path — and each field's full downstream path: where it is stored, logged, rendered, executed, or passed on to another service. Second-order injection is found here, not at the entry: input stored quietly today still reaches the sink when it is rendered or queried tomorrow. Trace the data, not the request handler.

Then work the boundary in order, each step a forcing question about this boundary, not a fill-in:

- **Census the sinks.** For each downstream use, name the sink class: SQL/NoSQL query, shell or process invocation, filesystem path, HTML/JS render context, template engine, LDAP/directory query. The census is the gate the rest hangs on — each defense is chosen per sink, so an unidentified sink is an unguarded one. An input that reaches no sink needs limits only.
- **Name the sink-correct defense, per sink — never generic "sanitization".** SQL/NoSQL: parameterized queries / prepared statements — never string-building, never escaping-as-primary; escaping is a legacy fallback at best, parameterization removes the class. Shell/process: argument arrays with `shell=false` — never string interpolation into a command line. Filesystem path: canonicalize FIRST, then enforce an allowlisted base-directory prefix — the order is the content: decode and normalize before the check, or `%2e%2e%2f` and symlinks walk past it. HTML/JS: context-aware output encoding at render time — the sink side, never the entry; encoding at input time corrupts the data for every non-HTML sink and still misses render contexts — with framework auto-escaping left ON. Template engine: user input as data only, never concatenated into template source (server-side template injection). LDAP/directory: the engine's escaping API. The rule to state plainly: **validation supplements, defenses replace** — an allowlist check is a good filter, but parameterization is what removes the vulnerability class.
- **Disposition the boundary trio.** Mass assignment: bind allowlisted fields only, never object-splat a request body into a model — a smuggled `role=admin` field rides the splat in. Unsafe deserialization: never `pickle`, `ObjectInputStream`, or `yaml.load` on untrusted bytes — safe loaders or plain data formats. Size/type/encoding limits, declared at the boundary: length caps, content-type checks, reject-don't-truncate.

## Prove it — the payload table

The proof is a table of concrete cases in two mandatory halves:

- **Must-block.** Per identified sink, the classic payload plus one bypass-class variant: `' OR 1=1--`, a `; rm x`-shaped argument, `../../etc/passwd` and its URL-encoded form, `<img onerror=...>`, `{{7*7}}`, a splatted `role=admin` field, an oversized body.
- **Must-pass.** Realistic benign inputs that overzealous filtering breaks: `O'Brien`, a path containing spaces, prose containing `<` or `{{`. Over-blocking is a correctness regression, not safety — a table of only attack payloads rewards it.

Two honest states, stated per row set:

- **Executed.** A running surface exists: run the rows against it and report the observed result per row. Never assert an outcome that was not run.
- **Authored, not executed.** Design time, nothing to run yet: deliver the table with exact execution instructions — the requests to make, the payload per row, the expected behavior — and say plainly that it has not run.

Keep the table sampled-and-said: it proves the rows that ran, never "injection-proof".

Render exactly one verdict:

- **defended-as-proven** — the table executed and every row observed as specified; scoped to the rows that ran, never beyond them.
- **designed-not-yet-proven** — the table is authored and execution is pending; the design is complete, the proof is not.
- **gap-found-because** — a must-block payload passed, a must-pass input blocked, or a sink has no named defense; name the gap and its row.

Never "sanitized", never "injection-proof": no table proves more than the cases it contains, and the verdict never outruns the table.

## Modes and scope

- **Applied vs advisory follows the invocation.** On live code, author the defense edits and run the table on a working branch — executed rows, observed results, each defense placement surfaced as a flagged decision in the diff. On a design doc, a spec, or a review, deliver the advisory pack: the sink census, the defense per sink, the trio dispositions, the table with execution instructions. Default to the mode the context implies; ask once when genuinely ambiguous.
- **One boundary.** Default scope is one trust boundary. Pointed at a whole app, narrow to the named boundary — or the riskiest, and say so: this is a forcing pass, not an audit. A repo-wide injection sweep is a different job (see Fences).

## Proof boundary

Never assert a block or pass outcome you did not observe; report only what the executed rows produced, and label everything else authored. The proof is bounded — the table covers the payloads reasoned out, on the surface it ran against — so state what was verified and bound the residual: *"12 rows executed against the dev server, all as specified; residual: the CSV write path asserted from a code read, not observed; the webhook consumer untested."* Advisory-until-asked: edit on a working branch, publish nothing unless asked.

## Fences

- **vs `regex-craft`.** It hardens one pattern, engine-first, ending in an executed regex proof; this designs one boundary's handling across every sink. Compose: a validation pattern this skill specifies is handed there for hardening, not re-derived here.
- **vs `red-team`.** It models a motivated adversary across a whole system and renders no verdict; this runs a known-class design procedure on one boundary and ends in one. Compose them: red-team's attack paths make excellent must-block rows.
- **vs `implementation-review`** (when `review-family:implementation-review` is available). It reviews a completed change against a spec plus a diff; this designs or vets one boundary's input handling, before or without a diff.
- **vs repo-wide sweeps.** A vulnerability sweep across a codebase is the parked security-audit — or the bundled `security-review` where the runtime ships one — and a scored debt backlog is `tech-debt-scan`'s job. A sweep finding is a valid trigger; the sweep is not this skill.
- **LLM prompt injection is deliberately unowned.** Untrusted text reaching a model's context is a real boundary this skill does not cover, and no named neighbor covers it either — say so and stop; do not stretch the sink table over it or invent a routing target.

## Done when

- The boundary is pinned and each field's full downstream path traced — stored, logged, rendered, executed, passed on — including the second-order uses.
- Every sink is censused and given its named sink-correct defense, with output encoding placed at render time and canonicalize-then-check ordering stated for paths.
- The boundary trio — mass assignment, unsafe deserialization, size/type/encoding limits — is dispositioned.
- The payload table is delivered with both halves — must-block and must-pass — each row set honestly labeled executed or authored-not-executed.
- Exactly one verdict is rendered — defended-as-proven / designed-not-yet-proven / gap-found-because — scoped to the table, with the residual named. Delivered in the mode the invocation implies, advisory-until-asked, nothing published unless asked.
