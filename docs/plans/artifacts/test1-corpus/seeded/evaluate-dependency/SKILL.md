---
name: evaluate-dependency
description: Decide whether to adopt a third-party dependency (library, framework, or service) using a structured weighted-scoring evaluation. Use when choosing whether to add a dependency, comparing candidate libraries, or wanting a consistent, defensible adoption decision.
---

# Evaluate a Dependency

Adopting a dependency is a long-term commitment — it shapes your build, your security surface, and your maintenance burden for years. This skill keeps adoption decisions **consistent across candidates** by scoring each one the same way, so two engineers evaluating the same library land in the same place.

## Workflow

### 1. Gather the candidate facts

Collect the signals you'll score: maintenance (last release, open-issue ratio, maintainer count), adoption (downloads, dependents, notable users), fit (license, runtime match, bundle size, API surface), and risk (CVE history, breaking-change cadence, transitive dependency count).

### 2. Score the eight dimensions

Score each from **1 (poor) to 5 (excellent)**. If a signal is genuinely unknown, score it 2 and note the gap in the evidence record.

| # | Dimension | Weight |
|---|-----------|--------|
| 1 | Maintenance health | 3 |
| 2 | Community adoption | 2 |
| 3 | Documentation quality | 2 |
| 4 | License compatibility | 3 |
| 5 | Security track record | 3 |
| 6 | Performance | 1 |
| 7 | API ergonomics | 2 |
| 8 | Migration cost (reverse-scored: 5 = cheap to leave) | 2 |

### 3. Read off the recommendation

Multiply each score by its weight and sum (max 90). Find the band the total lands in:

- **72–90 → Adopt**
- **54–71 → Adopt with reservations** (open a tracking issue for the two weakest dimensions)
- **Below 54 → Reject**

The band is the recommendation. Scoring the same dimensions the same way is what makes adoption calls consistent and comparable across the team over time.

### 4. Record the evidence

Alongside the score, write down what's behind it: the key facts for each dimension, anything the score doesn't capture, and any context specific to how *this* team would use the dependency. Keep it as long or short as the decision warrants.

### 5. Share it

Post the score, the recommendation band, and the evidence record so the decision is reviewable.
