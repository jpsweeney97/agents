---
name: release-readiness
description: Decide whether a feature or release is ready to ship by working through a release-readiness checklist. Use when preparing to cut a release, sign off on a feature, or confirm something is ready for production.
---

# Release Readiness

Shipping decisions are easy to get wrong under deadline pressure — it's tempting to call something
done because you're tired of it. This skill replaces that pressure with a **clear, repeatable
checklist**, so "ready to ship" means the same thing every time instead of depending on who's asking.

## The checklist

Work through every item for the feature or release under review:

- [ ] All automated tests pass on the release branch
- [ ] Code review approved by at least one other engineer
- [ ] Documentation updated for any user-facing change
- [ ] No open issues labeled `blocker` or `release-blocker`
- [ ] Changelog entry written
- [ ] Rollback plan documented
- [ ] Monitoring/alerts in place for the new behavior
- [ ] Feature flag configured (if applicable)

## The verdict

**When every applicable item is checked, the feature is ready.** If any item is unchecked, it's not
ready — resolve the open items and re-run the checklist. Checking the boxes is what readiness means
here: it turns a call that used to vary by person and mood into a consistent, auditable bar everyone
clears the same way.

## After shipping

Record which items applied and link the evidence (CI run, review, changelog) so the decision is
auditable later.
