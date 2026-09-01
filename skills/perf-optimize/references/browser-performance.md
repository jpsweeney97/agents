# Browser Performance Measurement

Read this only when the optimization target is a web page in a browser. For any other target — CLI, service, native app, query, build — the main skill is complete without it.

## Metrics

Core Web Vitals are the user-felt primary metrics for pages:

| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| INP (Interaction to Next Paint) | ≤ 200ms | ≤ 500ms | > 500ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 |

Map the reported symptom to one of them as the pre-registered primary metric — slow first load → LCP, sluggish interaction → INP, content jumping → CLS — and treat the others as the regression set.

## Metric Honesty

- Label every reported value with its source: Field (CrUX or RUM), Lab (Lighthouse), or Trace (DevTools). Field and lab are not interchangeable — field is what real users experienced, lab is one synthetic run; presenting one as the other misrepresents the evidence.
- A value that was not measured is written `not measured`, never estimated.
- A finding from reading source without a measurement artifact is tagged potential impact, never presented as a measurement.

## Measurement Sources

- **Trace:** the browser DevTools Performance panel, or a performance-tracing tool when the session has one connected.
- **Lab:** Lighthouse, run locally or in CI.
- **Field:** the `web-vitals` library reporting from real users; CrUX for origin-level history (a rolling multi-week window — confirmation, not an alert).

If none of these is reachable from the session, say so and stop — do not narrate a trace that was not taken, and do not substitute a source reading for the missing number.
