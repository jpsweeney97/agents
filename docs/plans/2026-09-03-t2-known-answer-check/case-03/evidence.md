# Evidence the user supplied for the crash-spike decision

Eleven excerpts.

## E1. Crash reports, last fourteen days (crash-reporting dashboard)

96% of crashes share one stack trace, topped by `AnalyticsSDK.SessionTracker.onForeground`, raising `InvalidArgumentException`, on operating system 19.0 and 19.0.1 only. It fires when the app returns to the foreground, on every screen, whether or not any feature is in use. The remaining 4% are the long tail that existed before. On operating system 18 the crash rate is unchanged at 0.4%.

## E2. Analytics SDK vendor changelog (public)

- 4.2.1, released three days ago: "Fix crash in SessionTracker on OS 19 foreground transitions (InvalidArgumentException)."
- 4.2.0, released five weeks ago: "Minor: new consent API. No breaking changes."
- Migration notes 4.1 → 4.2: no API changes required by integrators.

## E3. App dependency manifest (excerpt)

```
analytics-sdk: 4.1.0
crash-reporter: 2.8.3
image-loader: 6.0.2
networking: 3.11.0
ui-framework: 12.4.1
```

Exact versions are pinned; nothing floats. The previous app release (7.3) and the current release (7.4) both declare `analytics-sdk: 4.1.0`.

## E4. Rollback analysis (from the crash dashboard, filtered by app version)

Users still on release 7.3 with operating system 19: crash rate 3.0%. Users on 7.4 with operating system 19: 3.1%. Users on either release with operating system 18: 0.4%.

## E5. Store featuring requirements (email from the featuring team)

- Crash-free sessions of at least 99% over the seven days before review.
- The engagement events listed in the attached schema must be present and reporting (session start, screen view, retention cohort); these are produced by the app's analytics SDK.
- Build submission at least seven days before the review date. Postponement is not offered; a missed slot is reassigned.

## E6. Engineering notes, last week

- The exception is raised inside the analytics SDK's compiled binary on its own thread. A `try/catch` around the SDK's initialisation and around every call site in app code was tried for two days: no effect, because the crash occurs on the SDK's thread during a foreground callback the app does not invoke.
- A global exception handler cannot intercept an uncaught exception on a thread the app does not own on this platform.
- The crash does not correlate with any app feature; it occurs on foreground regardless of screen.

## E7. Operating system adoption among the app's users

Operating system 19: 61% and rising about 4 points a week. Operating system 18 and older: 39%.

## E8. Assessments on file

- Server-side engagement pipeline: about six weeks; would also require a new event ingestion service.
- Native rewrite of a screen: two weeks per screen; crashes are not screen-specific (E1).
- Removing libraries: the analytics SDK produces the events in E5 and cannot be removed; the other four libraries do not appear in any crash stack.

## E9. Crash reporting settings

Sampling is already at 100% of sessions. The stack trace in E1 is fully symbolicated.

## E10. Memory

The exception type is an argument error, not a memory termination; memory terminations are 0.1% of sessions and unchanged since the update.

## E11. Dependency currency (from the July release checklist)

All third-party libraries were at their latest versions at the July release except the analytics SDK, where 4.2.0 was skipped as "no changes needed." Since then only the analytics SDK has published a new version (E2).
