---
name: authorization-design
description: "Use when designing or vetting the access-control model for one resource, endpoint, or feature — who may do what to which objects: enumerate subject-action-resource decisions, choose RBAC/ABAC/ownership, place enforcement, close object-level (IDOR/BOLA) and tenant-isolation gaps, map privilege escalation, and prove it with a must-allow/must-deny access matrix. Not for login/session/token mechanics (authentication), attacker modeling (red-team), or a repo-wide vulnerability sweep."
---

# Authorization Design

Design the access-control model for one resource, endpoint, or feature — who may do what to which objects — and prove it with a must-allow/must-deny access matrix, never with reassurance. Invocation: `/authorization-design` or `$authorization-design`.

A forcing pass over one authorization surface — an endpoint being designed, a feature under review, a resource already coded — that enumerates the subject-action-resource decisions, chooses the access model, places enforcement fail-closed, closes the object-level and tenant-isolation gaps, maps privilege escalation, and proves the result with a concrete access matrix: executed where a running surface exists, honestly labeled authored-not-executed where none does. It edits on a working branch when applied; it never pushes, opens a PR, or publishes unless asked.

## Shape — a forcing pass over one surface

**Pin the surface and the subjects first.** The one resource, endpoint, or feature under design, and every subject class that can reach it: end users in each role, service accounts, background jobs, admin tooling, cross-service callers — the callers a happy-path list forgets. The unlisted subject is the one nobody checks.

Then work the surface in order, each step a forcing question about this surface, not a fill-in:

- **Enumerate the subject-action-resource decisions.** The concrete triples — who, does what, to which objects — including partial access: read-own vs read-any, write vs approve, field-level visibility (the support agent sees the order, not the card number).
- **Choose the model and say why.** RBAC (role-based: the role set is small and stable), ABAC (attribute- or relationship-based: access follows ownership graphs, org membership, document shares), plain ownership (you touch only your own rows), or a named hybrid. The wrong-fit smell is roles multiplying to encode relationships — `editor_of_project_42` is a relationship wearing a role costume; move it to ABAC or ownership.
- **Place enforcement.** Name the layer where each check runs — route guard, service layer, query predicate, database row-level security — and default fail-closed: a missing rule or an unknown subject denies, never allows. Object-level and tenant checks live in the data-access path, not only the route: a route guard cannot see which row the query returns.
- **Close the object-level gap.** Role checks alone still let any authenticated user read another user's record by ID — IDOR/BOLA (insecure direct object reference / broken object-level authorization), the most common access-control failure in the wild. Every by-ID access needs an ownership or membership predicate on the object it fetches, not just a role test on the endpoint.
- **Guarantee tenant isolation.** In a shared deployment, tenant scoping belongs in every query predicate — not only the URL path, the token claim, or a middleware some code path skips. Treat any query lacking a tenant predicate as a finding, whatever the route guard says.
- **Map privilege escalation.** Who assigns roles, who can grant grants, and both directions: vertical (user-to-admin — the self-service role edit, the invite flow that mints admins) and horizontal (peer-to-peer — reading a sibling user's data). Role-management endpoints are themselves resources on this surface; give them their own rows in the matrix.

## Prove it — the access matrix

The proof is a table of concrete cases: each row a subject × action × object instance resolving to MUST-ALLOW or MUST-DENY. The deny rows carry the proof — the cross-user object ID, the cross-tenant ID, the role without ownership, the unauthenticated caller, the deactivated user, the escalation attempt. A matrix with no deny rows is a reassurance ritual, not a proof.

Two honest states, stated per row set:

- **Executed.** A running surface exists: run the rows as tests or real requests against it and report the observed result per row. Never assert an outcome that was not run.
- **Authored, not executed.** Design time, nothing to run yet: deliver the matrix with exact execution instructions for the implementer — the requests to make, the subjects to authenticate as, the expected status per row — and say plainly that it has not run. Never claim or imply execution that did not happen.

Render exactly one verdict:

- **enforced-as-proven** — the matrix executed and every row observed as specified; scoped to the rows that ran, never beyond them.
- **designed-not-yet-proven** — the matrix is authored and execution is pending; the design is complete, the proof is not.
- **gap-found-because** — a must-deny case allows, or a subject class or action has no decision; name the gap and its row.

Never "secure": no matrix proves more than the cases it contains, and the verdict never outruns the table.

## Modes and scope

- **Applied vs advisory follows the invocation.** On live code, author the enforcement edits and run the matrix on a working branch — executed rows, observed results, each model and placement choice surfaced as a flagged decision in the diff. On a design doc, a spec, or a review, deliver the advisory pack: the decision table, the model choice with rationale, the placement, the matrix with execution instructions. Default to the mode the context implies; ask once when genuinely ambiguous.
- **One surface.** Default scope is one resource, endpoint, or feature. Pointed at a whole app, narrow to the named surface — or the riskiest, and say so: this is a forcing pass, not an audit. A repo-wide sweep for missing checks is a different job (see Fences).

## Proof boundary (the inherited floor)

This is the library-wide evidence-before-claims floor specialized to access behavior. Never assert an allow or deny outcome you did not observe; report only what the executed rows produced, and label everything else authored. The proof is bounded — the matrix covers the rows reasoned out, on the deployment it ran against — so state what was verified and bound the residual: *"14 rows executed against staging, all as specified; residual: field-level visibility asserted from a code read, not observed; admin tooling untested."* Advisory-until-asked: edit on a working branch, publish nothing unless asked. The skill obeys this floor; it does not own it.

## Fences

- **vs authentication.** Login flows, sessions, tokens, MFA, and password policy are out of scope — this skill starts after identity is established and asks only what that identity may do. Authentication design is a neighboring job this skill does not own; say so and hand it back rather than absorbing it.
- **vs `red-team`.** It models a motivated adversary across a whole system and renders no verdict; this runs a known-class design procedure on one surface and ends in one. Compose them: red-team's attack paths make excellent must-deny rows.
- **vs `system-design-review`** (when `review-family:system-design-review` is available). It reviews trust boundaries, data authority, and operational ownership at architecture altitude; this designs one surface's decision table below that altitude. An architecture review that flags a fuzzy trust boundary hands the named surface here.
- **vs `implementation-review`** (when `review-family:implementation-review` is available). It reviews a completed change against a spec plus a diff; this designs or vets one surface's access model, before or without a diff.
- **vs repo-wide sweeps.** A vulnerability sweep across a codebase is the parked security-audit — or the bundled `security-review` where the runtime ships one — and a scored debt backlog is `tech-debt-scan`'s job. A sweep finding is a valid trigger; the sweep is not this skill.
- **vs `contract-change-propagation`.** Changing an authorization contract that existing consumers already depend on is a blast-radius job: design the new model here, map the consumers and the rollout there.

## Done when

- The surface is pinned and every subject class enumerated, including the non-human callers: service accounts, background jobs, admin tooling.
- The subject-action-resource decisions are enumerated, including partial-access distinctions (read-own vs read-any, field-level visibility).
- The model is chosen with a rationale keyed to this domain's sharing semantics, and the role-explosion smell was checked.
- Enforcement is placed at a named layer, fail-closed, with object-level and tenant predicates in the data-access path.
- Every by-ID access carries an ownership or membership predicate; every query in a shared deployment carries a tenant predicate.
- Escalation is mapped in both directions, and role-management endpoints have their own matrix rows.
- The matrix is delivered with must-deny rows, each row set honestly labeled executed or authored-not-executed.
- Exactly one verdict is rendered — enforced-as-proven / designed-not-yet-proven / gap-found-because — scoped to the table, with the residual named. Delivered in the mode the invocation implies, advisory-until-asked, nothing published unless asked.
