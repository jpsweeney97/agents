# SEALED ANSWER — case-03, attempt 2 (never given to a reader or the Prune agent)

Written before any attempt-2 dispatch. Kind B.

## What changed from attempt 1, and why

Attempt 1 failed the Reader A test: A named the winner, reasoning from the four-option analytics-library cluster plus constraint 2's "keep sending the analytics events" that the analytics SDK was the suspected site. Attempt 2 removes that pointer: the field's dependency group is now generic (update all third-party libraries; remove non-essential libraries; server-side reporting) with a "pin and rebuild" decoy, constraint 2 no longer names an SDK, and the winner's "Sets it apart" reads as a maintenance gamble. The evidence still fixes the winner (E1, E2, E3, E11).

## Winner

**Update the app's third-party libraries** (dependencies group).

## Fixing facts (evidence only)

1. E1: 96% of crashes are one stack inside the analytics SDK on OS 19 foreground.
2. E2: the vendor released 4.2.1 three days ago fixing exactly that; E3: the app is on 4.1.0; migration needs no code change.
3. E11: every other library is already current, so "update third-party libraries" means, in effect, one bump; E3: versions are pinned, so "pin and rebuild" changes nothing.
4. E4: rollback keeps the same SDK version and the same crash rate.
5. E6: app-side guards, a handler, and a feature flag cannot reach a crash on the SDK's own thread.
Cost: a version bump plus a test build, about a day; constraint 2 kept (the SDK stays); no new vendor.

## Why every other candidate loses

- Roll back (user's): E4.
- Drop OS 19: E7, 61% of users.
- Pin and rebuild: E3/E11, already pinned; the pinned version is the crashing one.
- Remove non-essential libraries: E8, the crashing library is the one constraint 2 requires; the others are not in any stack.
- Server-side pipeline: E8, six weeks.
- Guards / handler / feature flag: E6.
- Native rewrite: E8, E1.
- Reduce memory: E10.
- Raise sampling: E9.
- Postpone: E5.
- Prompt OS update: E7, the new OS is the trigger.
- Contractor: constraint 3.

## Visible in Prune's view (not fixing facts)

Constraint 2 visibly pressures "remove non-essential libraries"; constraint 3 kills the contractor; constraint 1 pressures the rewrite and the server-side pipeline. None points at the winner.

## Pass criteria

Reader A (case.md only) must not name the winner; Reader B (case.md + evidence.md) must.

Attempt 2 of at most 3.
