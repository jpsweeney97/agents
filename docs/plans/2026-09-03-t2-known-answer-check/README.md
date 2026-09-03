# T2 known-answer check (2026-09-03)

The `check first` step from the deliberate 2.0 run on the T2 question (`docs/plans/2026-09-03-deliberate-t2-successor-run/04-close.md`), executed by a session on 2026-09-03 on JP's instruction. The check: author one decision case whose best option is fixed by the case's evidence but not visible at sketch depth, then confirm that property with two fresh reads, one from Prune's view and one from Shape's, in at most three attempts. This directory holds the case, the evidence, the sealed answer, both reads, and one dispatch of deliberate 2.0's Prune on the case.

**Outcome in one line.** The case passed both reads on the first attempt, so "Known-answer cases, Prune only" is buildable; and on the one Prune dispatch run so far, 2.0's Prune cut the known winner at survivor count, with a revive condition that names the fixing fact almost verbatim.

## Design choice, made before authoring

Kind B (the Recommend stage's second kind): the facts that fix the winner sit only in the evidence, which 2.0's Prune never receives. Reasons: it is the T2 question in its conditional form ("given a candidate whose case lives only in evidence, how often is it cut"); it matches how 2.0 dispatches Prune (the stage table in `plugins/decide/skills/deliberate/SKILL.md` gives Prune no evidence); and the two-reader test is coherent for it. Kind A's reader-A test is not coherent: an agent asked directly for the best option will find facts placed in front of it. If the ten-case run happens, every case stays Kind B.

## The case

`case-01/case.md` is Prune's view: the question (a nightly partner-export job missing its 06:00 deadline; fix within six weeks), one user candidate marked as theirs, three confirmed constraints each with what it costs, three values, survivor count about four, and a field of sixteen candidates in `ideate` shape. `case-01/evidence.md` is what Shape would add: nine excerpts (timing profile, API reference, a supplier support ticket, the job's configuration, a log line, worker metrics, the partner contract, an incident note, team notes). The organisation and supplier are fictional so that no reader can answer from outside knowledge.

`sealed/case-01-ANSWER.md` was written at 15:18, before any reader was dispatched, and was never given to any reader or to the Prune agent. It names the winner, the five facts that fix it, where each sits, why every other candidate loses on the evidence, and what is visible in Prune's view (constraints visibly disqualify four candidates; none of that points at the winner).

Winner: **Tune the catalog fetch's request parameters**, position 7 of 16. Fixed by E4 (the job pages at size 50, the library default), E2 (the API allows 1000), E5 (41,869 requests for 2.09 million items, 4h07m), and E1 with E6 (the fetch is the whole problem and the worker is idle). From Prune's view it reads as the modest member of a five-candidate fetch group, beside four candidates that promise to remove most of the fetch.

## Attempt 1: both reads passed

| Reader | View | Files given | Named as best | Winner among runners-up? | Verdict |
| --- | --- | --- | --- | --- | --- |
| A | Prune's | `case.md` | Poll the catalog hourly during the day and only assemble at night | No (runners-up: incremental fetch, concurrent pricing, start earlier) | PASS: winner not visible at sketch depth |
| B | Shape's | `case.md` + `evidence.md` | Tune the catalog fetch's request parameters | n/a | PASS: evidence fixes the winner |

Reader A's stated unknowns are exactly what Prune's view lacks ("the case never states where the hours actually go"; "if the Corvid API does support a changed-since filter"). Reader B cited E1, E2, E4, E5, E6, E8, E9, computed the twentyfold request reduction unprompted, and named the three modest in-budget options as runners-up, each judged insufficient alone. Files: `case-01/read-A.md`, `case-01/read-B.md`.

Dispatch: two fresh in-session agents (general-purpose, session model), each told to read only the named files, with no listing, search, or commands, and told nothing about the purpose. Both reads returned within three minutes of dispatch. The whole check, from reading the recommendation to both reads returned, took about twelve minutes against a 30 to 60 minute budget.

**Result of the check: candidate 5 is buildable.** One case passed on the first attempt.

## One Prune dispatch on case-01: the winner was cut

Dispatched as 2.0 dispatches it: a fresh in-session agent told it is the Prune stage of a `deliberate` run, carrying the Prune method text verbatim from `SKILL.md`, reading only `case.md`, writing `case-01/02-prune.md`. It returned five survivors and eleven cut records in about six minutes.

| Item | Result |
| --- | --- |
| Winner kept or cut | **Cut** |
| Cut type | survivor count, judgment call |
| Reason given | "its seriousness could not be resolved at sketch depth ... the case gives no view of the current settings" |
| `Strongest case` | "if the job currently fetches in small pages with aggressive retries it could recover hours at no cost" |
| `Revive if` names the fixing fact? | **Yes.** "Develop finds the current request settings far below the API's documented limits" is E4 against E2 exactly. |
| Survivors | Start the job earlier; Parallelize the fetch across more workers; Upgrade the worker to a larger instance (user's); Keep a local catalog cache and refresh it by diff; Poll the catalog hourly during the day and only assemble at night |
| Survivors that the evidence supports | None of the five (see the sealed answer's per-candidate list) |

Other observations from the ledger, recorded because they bear on the run's design and on 2.0's behaviour, not as findings:

- Prune stopped at five survivors against "about four" and wrote that a sixth survivor-count record "would be false" because all five were serious at sketch depth. That is the contract's own rule working (keep extra survivors rather than invent a weight), and it means the survivor count was not the only pressure on the winner: it was cut in preference to five others at the same depth.
- Prune read two candidates as constraint-1 contract changes by judgment (the bulk file from the supplier; reducing the feed's sections). On the evidence both are correctly out, but the recorded reasons are not the evidence's reasons.
- Prune's same-reason cut kept "cache by diff" over "incremental fetch" precisely because the case did not establish a changed-since filter; the evidence kills both, for the same reason (identifiers regenerate nightly).

What this one dispatch means, and no more: on one authored Kind-B field, Prune's sketch-depth judgment did not keep a winner it had no way to recognise, and the cut record carried the exact revive condition. That reproduces T2's single descriptive finding (the record anticipated the challenge) on 2.0, at n = 1. It says nothing about a rate.

## What the ten-case run would add

Per the recommendation: about ten Kind-B cases, one or two Prune dispatches each, counting cut or kept by cut type and, for each cut winner, whether its `Revive if` names the fixing fact. On this session's timings each case costs about ten minutes to author, two reader dispatches to validate, and one or two Prune dispatches: roughly fifteen to twenty minutes wall clock per case, so ten cases fit in two to three hours of one session. A second question the first result raises, outside the recommendation's scope: whether the stages after Prune (Shape, Recommend, Contest) catch a cut winner whose revive condition names the fact. That would be a different count, priced separately.

Blinding note for any continuation: new cases' sealed answers must stay outside the repository tree until that case's Prune dispatch has run, because in-session Prune agents are unconfined. `sealed/case-01-ANSWER.md` is in the tree only because case-01's dispatch is complete.

## Honest limits

- One case, one author (the session), one model family for author, readers, and Prune. Validity rests on one read each way, not repeated reads.
- The readers and the Prune agent were in-session and unconfined; each was told to read only the named files, and none of their outputs cites anything outside them.
- Reader A's pass is the weaker of the two for Kind B, as the sealed note predicted: with the fixing facts absent from its view it could only have named the winner by chance or by leakage in the wording. Its value is as a leakage check, and it found none.
- The Prune agent knew it was inside a `deliberate` run, as a real dispatch would; it was not told the case was authored or that a winner existed.

## Files

| Path | What it is |
| --- | --- |
| `case-01/case.md` | Prune's view: question, user's candidate, constraints at price, values, survivor count, field of 16 |
| `case-01/evidence.md` | the nine evidence excerpts Shape would see |
| `sealed/case-01-ANSWER.md` | winner, fixing facts, per-candidate kills, pass criteria; written before any dispatch |
| `case-01/read-A.md` | Reader A (Prune's view) |
| `case-01/read-B.md` | Reader B (Shape's view) |
| `case-01/02-prune.md` | deliberate 2.0's Prune output on the case |
