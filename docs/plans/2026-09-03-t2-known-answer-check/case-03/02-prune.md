# Prune: case-03, the crash spike before the featuring slot

## Survivors (field order, exact wordings)

1. Roll back to the previous app release (user's)
2. Update the app's third-party libraries
3. Add crash-handling guards around the failing code paths
4. Add a remote feature flag to disable the crashing feature

Survivor count: 4, against a target of about four. No survivor-count cut required deciding a trade between the user's stated values that they have not priced.

## Cut records (field order)

```text
Option:         Drop support for the new operating system version
Cut:            dominated, judgment call
Reason:
  "Roll back to the previous app release" is at least as good on everything that matters here and better on two things.
  Stability: marking the app incompatible with version 19 leaves every existing install on version 19 running the current build and crashing at the same rate, so it cannot bring the session crash rate down for the users already affected. Rolling back is neutral in that same case and fixes the spike if the app's last release caused it.
  Featuring slot: an app that declares itself incompatible with the current operating system version is, at sketch depth, unlikely to pass a featuring team's review; rolling back keeps the app eligible.
  Codebase size and engineering time: equal, since neither changes code.
  Judgment call because the featuring team's reaction to an incompatibility flag is not a stated fact.
Strongest case: It needs no engineering and no release, and it guarantees no new user on version 19 ever has a crashing session.
Revive if:
  The store's stability metric is confirmed to count only installs on supported operating system versions, and the featuring team confirms an app incompatible with the current version can still be featured.

Option:         Pin all third-party libraries and rebuild
Cut:            same reason, judgment call
Reason:
  This option and "Roll back to the previous app release" (user's) succeed or fail for the same reason: both succeed only if the spike came from something the app itself shipped rather than from operating system version 19, and both fail if version 19 is the cause, which the stated timing points to.
  Inside the success case, pinning covers only the "a library moved underneath us" sub-case, while re-publishing the last stable version reverts libraries and code together, so pinning's success set sits inside rollback's.
  Pinning's one distinct advantage, keeping the code shipped since the last stable release, is a feature-preservation the user has already ranked below stability this cycle.
  One of the pair is the user's candidate, so the user's wording stays and the generated one is cut.
  Judgment call because whether pinning's success set sits entirely inside rollback's depends on the last stable build being reproducible, which the field does not show.
Strongest case: If a dependency resolved to a newer version at build time without anyone changing code, pinning fixes exactly that, keeps every feature shipped since, and needs no code change.
Revive if:
  The rollback survivor dies at development depth because the store cannot accept a re-published older build, or because something shipped since the last stable release cannot be reverted; pinning is then the nearest replacement.

Option:         Remove non-essential third-party libraries
Cut:            survivor count, judgment call
Reason:
  A low-confidence cut of a candidate whose seriousness I could not resolve at sketch depth.
  It pays off only if the crash lives inside a library the app can shed, and the field does not say which library, if any, is involved.
  It also carries a constraint-2 risk if a reporting dependency is judged non-essential.
  The surviving "Update the app's third-party libraries" covers the "the crash is in a library" bet from the other side and keeps what the libraries do.
Strongest case: It is the option most aligned with "keep the codebase small", and if the crash is in a library the app does not need, removal fixes it permanently with no vendor dependency.
Revive if:
  Crash reports place the crash inside a library the app can drop without touching session starts, screen views, or retention cohorts, or the update survivor fails because no vendor has shipped a fix.

Option:         Move engagement reporting to a server-side pipeline
Cut:            constraint, judgment call
Reason:
  Constraint 1: building a backend that receives raw events and computes session starts, screen views, and retention cohorts, migrating the client to it, and verifying the store's audit still sees what it audits is, by the field's own description, the largest engineering move here. With four engineers and about two weeks that also have to absorb the crash work, at sketch depth it does not fit.
  Constraint 2: a reporting migration mid-flight is exactly when the audited reporting can stop arriving, and the constraint says it must keep arriving.
  It addresses the crash only in the case where the crash lives in the client-side reporting logic.
  Judgment call because the time estimate cannot be established as fact from the field.
Strongest case: If the crash is inside the client-side reporting code, removing that code from the app fixes the crash and puts the team in control of the whole reporting path for good.
Revive if:
  Crash reports place the crash inside the client reporting logic, and a backend that can already receive raw events and compute cohorts exists, so the migration is a week of work rather than a build-out.

Option:         Ship a hotfix that catches the exception
Cut:            same reason, judgment call
Reason:
  This option and "Add crash-handling guards around the failing code paths" succeed or fail for the same reason: both keep the app running by catching a failure instead of fixing its cause, so both work only if the crash is a catchable exception, and both fail if it is a native crash or a termination by the operating system.
  Of the pair, the guards are kept: they act at the failing paths and leave the app in a state those paths chose, while a global handler that swallows a specific error can leave the app running in a state it did not choose and can mask unrelated errors.
  Neither is the user's candidate.
  Judgment call because which of the pair is safer depends on the crash's shape, which the field does not show.
Strongest case: One handler is less code than many guards, matches "keep the codebase small", and can ship in a day.
Revive if:
  Crash reports show one exception type thrown from many unrelated paths, so guarding each path is more code and more risk than one handler.

Option:         Rewrite the affected screen natively
Cut:            survivor count, judgment call
Reason:
  A low-confidence cut of a candidate whose seriousness I could not resolve at sketch depth.
  It pays off only if the crashes cluster in one screen and the shared framework, not the app's own code or the operating system, is at fault; neither is visible from the field.
  Where the framework is at fault and its vendor has shipped a fix, the surviving "Update the app's third-party libraries" reaches the same result without a rewrite.
  It is also the one candidate that adds a second toolkit to a four-person codebase, and a rewrite plus testing plus submission inside two weeks is tight.
Strongest case: If the framework is at fault and no vendor fix exists within the window, this is the only option that removes the faulty layer rather than working around it.
Revive if:
  Crash reports place the crashes in one screen, the framework is confirmed as the cause, and the update survivor fails because the vendor has no fix.

Option:         Reduce the app's memory use
Cut:            survivor count, judgment call
Reason:
  A low-confidence cut of a candidate whose seriousness I could not resolve at sketch depth.
  It pays off only if the crashes are memory terminations under tighter limits in version 19, and the field does not say what kind of crash this is.
  If they are, it is a serious answer; if they are not, it is maintenance with no effect on the spike.
Strongest case: Memory behaviour is one of the things an operating system update most often changes, the fix helps every device, and it shrinks rather than grows the codebase.
Revive if:
  Crash reports show out-of-memory or system-initiated terminations rather than exceptions, or the crashes concentrate on low-memory devices.

Option:         Raise crash-report sampling to find the cause
Cut:            constraint, judgment call
Reason:
  Constraint 1: as worded, this spends the two weeks on diagnosis with nothing shipping until the cause is known, and a build has to be submitted at the end of those two weeks, so the submitted build would be the one crashing now.
  On its own it does not answer the decision question; it is a first step any survivor would take.
  Judgment call because diagnosis could finish early and hand off to a fix, and the wording does not forbid that.
  Whether full-detail capture of every session needs a paid tier is not established from the field, so it is not part of this reason.
Strongest case: Every survivor guesses at the cause; two weeks of full crash data would let the team fix the actual cause instead of containing a guessed one.
Revive if:
  The run treats diagnosis as the first days of a survivor's plan rather than as a standalone answer, or the cause is found early enough to build and submit a real fix.

Option:         Ask the store to postpone the featuring slot
Cut:            constraint, judgment call
Reason:
  The user confirmed the review date as a hard constraint, with a build due at least seven days before it. This option's only action is to ask for that date to move; it works on the constraint rather than within it, and it does nothing to the crash rate the question asks about.
  Against the stated value "Do not lose the featuring slot", a postponement request risks the slot for no stability gain.
  Judgment call because a store might grant a later slot.
Strongest case: It removes the deadline that forces every other option into a two-week guess, and a fix made without time pressure is more likely to be the right one.
Revive if:
  The user says the date is negotiable or the store has signalled flexibility; constraint 1 then changes and the field should be pruned again.

Option:         Prompt users to update their operating system
Cut:            dominated, judgment call
Reason:
  This option bets the crash is on the old operating system version. The stated background has the spike beginning the day version 19 started rolling out, so its premise runs against the given facts, and pushing more users onto version 19 could raise the crash rate.
  "Roll back to the previous app release" is at least as good on everything that matters: on stability it is neutral in the same case and better where the app's last release is the cause; on codebase size it adds nothing where this adds a dialog; on the featuring slot it keeps the app as it is; and it needs no engineering where this needs a dialog and a release.
  Judgment call because the timing is an association, not a proven cause.
Strongest case: If the crashes are on devices still on the old version, or on devices mid-update, a dialog is the cheapest possible fix.
Revive if:
  Crash reports show the crashes concentrated on devices that have not updated to version 19.

Option:         Hire a contractor who specialises in the new operating system
Cut:            constraint, fact-established
Reason:
  Constraint 3 says no new paid services or vendor contracts, and names contractors as out. This option is a contractor.
Strongest case: It is the only option that adds expertise in the version that coincides with the spike, and it spends money rather than the team's two weeks.
Revive if:
  The user lifts constraint 3, or the specialist can be engaged without a paid contract.
```
