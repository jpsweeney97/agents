# Review Records

Durable artifacts from broad, read-only reviews of this repo — capability-growth reviews, whole-library reviews, architecture or system-design reviews, and other standalone review reports worth keeping past the session that produced them.

These records exist because **a good review is expensive to re-derive.** A multi-agent library review or an architecture pass reads dozens of surfaces, verifies citations, and reasons across the whole system; that work should leave a durable, re-checkable trail instead of evaporating into chat. A record captures the findings, the evidence they rest on, and the limits of the pass.

## What lives here

- One Markdown record per review, named `YYYY-MM-DD-<topic>.md` (date-prefixed with a dash, like the repo's `docs/audits/` and `docs/plans/` artifacts; `<topic>` names what was reviewed).
- Not every review earns a record. Persist one when the review is broad enough, costly enough to reproduce, or decision-shaping enough to be worth a durable evidence trail. A quick read-only answer in chat stays in chat.

## Not this directory

- Technical-debt audits go to `docs/audits/` (produced by `tech-debt-scan`, named `YYYY-MM-DD-<target-slug>-debt-scan.md`).
- Implementation plans and evaluation/apparatus artifacts go to `docs/plans/`.
- Behavior smoke-test records go to `docs/smoke-tests/`.
- Use `docs/reviews/` for review reports that have no other home.

## Record shape

Reviews vary by target, so the body shape follows the review itself. Each record should carry:

- **Frontmatter** anchoring the pass: `type: review`, `date`, `scope` (what was inspected), `reviewed_commit` (the HEAD the citations are true at), `method` (how the review was produced), and `posture` (e.g. read-only, capability-growth biased).
- **A structured body** suited to the review — for a capability-growth review, an executive summary, a coverage/limits statement, the findings, and ordered next moves; for other review types, the shape that review naturally takes.
- **Local `path:line` citations** for every substantive claim about the repo, and links for external inspirations.
- **An Evidence Boundary** note: what was and was not inspected, which citations were independently verified, and that later edits can invalidate them.

## Status of these records

Evidence, not authority. A record is true *at the commit it names*. Later edits can invalidate a specific citation or finding — re-verify against live source rather than trusting a stale record. Live files, drift checks, and a fresh review outrank anything written here.

## The methodology-treatment arc (closed 2026-07-21)

JP closed the methodology-treatment arc on 2026-07-21, after nineteen treatments (two inversions, seventeen holds; the `*-methodology-critique.md` briefs in this directory are the record). The call was made against the signal named in §8 of the reflexive brief (`2026-07-19-methodology-critique-methodology-critique.md`): the verdict stratum stopped surprising sixteen runs ago, while the findings stratum had not — so the close is a portfolio-level resource decision about the marginal price of facts. It does not use the genre tally as evidence about any particular target, consistent with the tally-is-history law the same treatment landed.

What the close changes: there is no default next target and no standing treatment cadence. `methodology-check` is the standing methodology pass; the full treatment remains reachable only through its escalation rider or a fresh JP commission.

What the close does not change: `methodology-critique` stays live and unretired (skills are build-and-prune); its per-admission push grant stays dormant and untouched — a treatment can only run on JP's commission anyway; the charter admission entry is unchanged; the 2026-08-01 suffix-aware ledger re-read remains owed and unaffected; and the endorsed repairs (`f92158d`) stand, with their verification arriving downstream or not at all, as the repaired text itself states.
