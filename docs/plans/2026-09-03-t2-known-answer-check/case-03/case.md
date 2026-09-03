# Decision case: the crash spike before the featuring slot

## Decision question

How should the app team bring the mobile app's crash rate back under one percent of sessions, from about three percent since the phone operating system's latest update, before the app store featuring slot in three weeks?

## Background, as the user stated it

A consumer app with about 200,000 monthly users and four engineers. The crash rate was 0.4% of sessions for a year. On the day the phone operating system's version 19 update began rolling out, it rose to 3.1% and has stayed there. Store reviews have started mentioning crashes. The app has been offered a featuring slot in three weeks; the store's featuring team reviews stability before confirming.

## User's candidates (marked as theirs, quoted exactly)

- **Roll back to the previous app release** — "Re-publish the last version that shipped before the crash spike." (user's)

## Hard constraints the user confirmed, with what each costs

1. The featuring review is in three weeks and a build must be submitted at least seven days before it, so there are about two weeks of engineering time. What it costs: anything that needs more than two weeks is out.
2. The submitted build must keep the engagement reporting the store's featuring team audits: session starts, screen views, and retention cohorts must keep arriving. What it costs: stripping out reporting to reduce risk is out.
3. No new paid services or vendor contracts. What it costs: paid crash-analysis upgrades, new vendors, and contractors are out.

## Values the user stated

- Users' stability matters more than any new feature this cycle.
- Keep the codebase small; the team is four people.
- Do not lose the featuring slot.

## Survivor count

About four.

---

# Field

Grouped by what each option changes: which build users run, the app's dependencies, the app's own code, and the release or the users. Order within a group is not a quality order.

## Change which build users run

**Roll back to the previous app release** (user's) — "Re-publish the last version that shipped before the crash spike."
Sets it apart: no engineering; bets the spike came from the app's most recent release.

**Drop support for the new operating system version** — Mark the app as incompatible with version 19 so users on it cannot install or update.
Sets it apart: removes the affected users rather than the crash; a store-listing change, not a code change.

**Pin all third-party libraries and rebuild** — Rebuild the app with every dependency held at the exact versions of the last release that was stable, in case something moved underneath it.
Sets it apart: bets the spike came from a library that changed without the team noticing; no code change.

## Change the app's dependencies

**Update the app's third-party libraries** — Bump every third-party dependency to the latest version its vendor has published, and ship.
Sets it apart: routine maintenance; helps only where a vendor has fixed something since the app last updated.

**Remove non-essential third-party libraries** — Strip out the dependencies the app can do without, to shrink what can fail.
Sets it apart: less code from other people in the app; whatever those libraries did stops.

**Move engagement reporting to a server-side pipeline** — Send raw events to the team's own backend and compute engagement there, removing that client-side logic from the app.
Sets it apart: puts the team in control of the whole reporting path; the largest engineering move in the field.

## Change the app's own code

**Add crash-handling guards around the failing code paths** — Wrap the code that appears in crash reports in defensive checks so it fails quietly instead of crashing.
Sets it apart: contains the damage without understanding the cause; standard first aid.

**Ship a hotfix that catches the exception** — Install a global exception handler that swallows the specific error and keeps the app running.
Sets it apart: one handler rather than many guards; the crash becomes a logged event.

**Add a remote feature flag to disable the crashing feature** — Put the feature the crashes cluster in behind a flag that can be turned off from the server without a release.
Sets it apart: gives the team a switch for future spikes too; the feature goes dark for everyone while the flag is off.

**Rewrite the affected screen natively** — Reimplement the screen where crashes cluster using the platform's native toolkit rather than the shared framework.
Sets it apart: removes a layer that may be at fault; a rewrite of one screen, not the app.

**Reduce the app's memory use** — Cut image caches and in-memory state so the app is less likely to be terminated under pressure on the new operating system.
Sets it apart: bets the new version tightened memory limits; helps every device a little.

**Raise crash-report sampling to find the cause** — Turn crash reporting up to capture every session in full detail and spend the two weeks on diagnosis.
Sets it apart: chooses understanding over acting; nothing ships until the cause is known.

## Change the release or the users

**Ask the store to postpone the featuring slot** — Request a later slot so the fix can be made without a deadline.
Sets it apart: removes the time pressure rather than the crash.

**Prompt users to update their operating system** — Show an in-app message asking users on affected versions to update.
Sets it apart: costs a dialog; bets the crash is on the old version, not the new one.

**Hire a contractor who specialises in the new operating system** — Bring in an outside engineer for two weeks to find and fix the cause.
Sets it apart: adds capacity and expertise the team lacks; money rather than time.
