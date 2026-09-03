# SEALED ANSWER — case-03 (never given to a reader or the Prune agent)

Written before any dispatch. Kind B. Disguise: the winner is a dependency bump that depends on someone else (the vendor) having already fixed something; at sketch depth it sits in a group of three analytics-library options that all "bet on the SDK", so a same-reason cut keeping a different one, or a survivor-count cut, is the trap.

## Winner

**Update the analytics SDK to its latest release** (analytics-library group).

## Fixing facts (evidence only)

1. E1: 96% of crashes are one stack inside the analytics SDK's SessionTracker on OS 19 foreground.
2. E2: the vendor released 4.2.1 three days ago fixing exactly that crash; the app is on 4.1.0 (E3); migration 4.1 → 4.2 needs no API changes.
3. E4: the previous release has the same SDK version and the same crash rate, so rollback does nothing.
4. E6: app-side guards, a global handler, and a feature flag cannot reach a crash on the SDK's own thread.
Cost: a version bump plus a test build, about a day; ships well inside the two weeks; keeps the analytics events (constraint 2); no new vendor (constraint 3).

## Why every other candidate loses

- Roll back (user's): E4.
- Drop OS 19 support: E7, 61% of users; also does not reduce the crash rate on the store's metric for the users who remain on 19 with the old build already installed.
- Remove the SDK: constraint 2 (E5 requires the events).
- Replace the SDK: E8, three to four weeks and a contract; constraints 1 and 3.
- Server-side pipeline: E8, six weeks; constraint 1.
- Guards / hotfix handler / feature flag: E6, the crash is on the SDK's thread and not feature-linked.
- Native rewrite: E8 and E1, crashes are not screen-specific.
- Reduce memory: E10.
- Raise sampling: E9, already 100% and the cause is already known.
- Postpone: E5, not offered.
- Prompt users to update OS: E7, the new OS is the trigger.
- Contractor: constraint 3.

## Visible in Prune's view (not fixing facts)

Constraint 2 visibly kills removing the SDK; constraint 3 visibly kills the contractor and probably the vendor swap; constraint 1 pressures the rewrite and server-side options. None points at the winner over its siblings.

## Pass criteria

Reader A (case.md only) must not name the winner; Reader B (case.md + evidence.md) must.

Attempt 1 of at most 3.
