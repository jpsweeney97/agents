---
name: characterization-tests
description: "Use when working code has no tests and a refactor, upgrade, or migration is about to touch it: author a characterization net (golden-master/approval tests) that pins what the code actually does now — bugs included, flagged — taming nondeterminism first, then prove the net works by making a deliberate mutation fail it. Pins current behavior, not correctness. Not for test-first new behavior (tdd), auditing an existing suite (test-trust-audit when available), or doing the refactor itself."
---

# Characterization Tests

The safety net you weave BEFORE changing untested code: pin what it actually does now, prove the net catches change, hand over green. The change itself is someone else's move. Invocation: `/characterization-tests` or `$characterization-tests`.

A pass over one seam of working, untested code that authors a behavior-snapshot net (characterization / golden-master / approval tests): tame nondeterminism first, capture the code's observed behavior as the expected values — bugs included, flagged — run the net green, then prove it detects change by making a deliberate, reverted mutation fail it. The deliverable is the green net plus its proven trigger; the refactor, upgrade, or migration it protects happens after, in its own lane.

## The owned job

This owns **authoring the change-detection net over existing untested code**. No neighbor owns it. `tdd` owns test-first NEW behavior, red before green; `simplify-code` and `dependency-upgrade` both promise behavior preservation, but neither authors the net that would detect a break — this skill is their unstated precondition. Auditing an existing suite's honesty is the neighboring job (route to `test-trust-audit` when available); this skill fires where no suite exists.

Its value: without a net, "the refactor preserved behavior" is an assertion; with one, it is an observation. The human is spared hand-picking the inputs that reach the branches, taming the flakiness that would poison the captures, and remembering the step everyone skips — that a net never seen to fail proves nothing.

## Mixed skill — apply the bar per part

- **Firm (trust).** Expected values captured by RUNNING the current code, never reasoned from intent or docs; the nondeterminism pass ordered before first capture; the pin-bugs-flag-bugs rule; the mandatory mutation proof with restoration proven; the handover naming what the net does and does not cover. A skipped step is a defect — the value is the proven net, not a plausible one.
- **Provoked (judgment).** Where the seam is — which boundary the imminent change will preserve and is therefore worth pinning; which inputs earn a place in the net (branch-reaching, edge-hitting, not bulk); whether an output difference between runs is nondeterminism to tame or behavior to pin. Posed as forcing questions keyed to this code; never a template filled to feel done.

## Shape — the pass

- **Pin the seam.** The outermost stable boundary the upcoming change will preserve: a public function, a CLI invocation, an HTTP handler, a file-in/file-out transform. Pin at the seam, not private helpers — a net over internals freezes the implementation and blocks exactly the refactor it exists to enable.
- **Tame nondeterminism FIRST.** Before any capture, find and control what varies between identical runs: timestamps, UUIDs and random IDs, hash/dict ordering, float formatting, locale, concurrency interleaving. Inject clocks and seeds where the seam allows; otherwise normalize outputs in the capture harness (strip or replace the volatile fields). A net captured before taming flakes forever after.
- **Choose inputs by branch, not bulk.** A handful of inputs that reach different branches and edges — empty, boundary, malformed, the weird-but-real production case — beats hundreds of near-duplicates. Name why each input is in the net.
- **Capture actual behavior as expected.** Run the current code; its observed output becomes the assertion — inline expected values or approval/golden files, preferring small, reviewable goldens (a giant unreviewable snapshot is a rubber stamp, not a contract). Where current output looks WRONG, pin it anyway and flag it as a finding — fixing it now changes behavior mid-netting and defeats the net; the fix is follow-up work after the net and the change land. Label the tests as characterization in their names or comments ("pins current behavior, not correctness") so a future reader doesn't mistake a pinned bug for a spec.
- **Run green.** The whole net passes against the unmodified current code.
- **Prove the net — the mutation check, mandatory.** With a clean tree, introduce ONE deliberate behavior change at the seam's implementation — flip a comparison, move a boundary — run the net, and require at least one failure. Revert and PROVE restoration (`git diff --exit-code` on product code; the net files legitimately differ), then require the net green again. Repeat for 2–3 distinct mutations when the seam has distinct behavior regions. A net never seen to fail is decoration. Never commit a mutation; restore on every exit path, including a runner failure mid-proof.

## Output and handover

The committed net — tests, any golden files, the capture harness — plus a short handover: the seam pinned; the inputs and why each is there; the nondeterminism controls applied; pinned-bug findings flagged for follow-up; the mutations that proved the net and what each caught; and the honest boundary — the net detects changes in the behaviors it pins, nothing more. No "behavior fully covered" claim, ever.

## Modes and scope

- One seam per run. Pointed at a whole legacy module, pin the seam the imminent change will cross and say what was left unpinned.
- Tests only. This skill never performs the refactor, upgrade, or migration it enables — hand that to `simplify-code`, `dependency-upgrade`, or the change's own lane, with the net standing as its tripwire.

## Fences

- **vs `tdd`** (the inversion, named). `tdd`'s test discipline forbids expected values derived from the code under test — for NEW behavior, where the claim is correctness and the expectation must come from an independent source of truth. Characterization deliberately inverts this for EXISTING behavior: the running code IS the only authority on what the system currently does, and a characterization test asserts "unchanged", never "correct" — so deriving expectations from execution is not the tautology `tdd` forbids; it is the point. Both rules are right in their lanes; the label rule above keeps a pinned bug from ever reading as a spec.
- **vs `test-trust-audit`** (when available). It audits an existing suite's honesty; this authors a net where no suite exists. Compose: after this net lands, that audit is how a later reader checks the net hasn't rotted.
- **vs `verify` / `behavior-smoke-test`** (where available). Those prove one change once; this leaves a durable net that keeps detecting.
- **vs `acceptance-map`.** It maps INTENDED behavior from a settled spec; this pins ACTUAL behavior from execution — bugs included.

## Done when

- The seam is named and pinned at the boundary the change preserves, not at internals.
- Every nondeterminism source is dispositioned — injected or normalized — before the first capture.
- Every input in the net has a stated reason.
- The net is green against unmodified current code.
- At least one deliberate mutation was observed to fail the net, restoration was proven, and the net is green again.
- Pinned bugs are flagged as findings for follow-up, never fixed mid-netting.
- The handover states the honest boundary; no product-code change survives; nothing pushed.

## Build-and-prune note

Thin in this authoring repo — little legacy product code lives here — and that silence is not evidence against it. The value is portable to every repo with working, untested code in front of a change, judged by that leverage and its cognitive-offload: the full weave-tame-capture-prove procedure summoned with one token. First-to-prune on observed mis-fire. Watch three failure shapes: **pinning internals**, where the net becomes the obstacle to the refactor it was built to enable; **golden bloat**, where snapshots grow past what anyone reviews and the net decays into a rubber stamp; and the **skipped mutation proof**, where the net is handed over green-only — indistinguishable from the assertion-free tests it would otherwise resemble. Each is drift from net to decoration: prune evidence to collect, not a reason to withhold the build.
