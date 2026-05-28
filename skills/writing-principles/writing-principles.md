# Writing Principles Reference

Codex instruction docs only: `AGENTS.md`, `SKILL.md`, skill support Markdown, and `agents/*.md`.

Use this file only for Medium/High rigor, explicit audits, unclear violations, or full self-checks.

## Modes

- Review-only: report violations and wait.
- Edit/refactor/create: fix scoped violations and report.
- Missing target, scope, or authority: stop and ask.
- Conflicting intent: follow higher-priority instructions; report unresolved conflicts.

## Risk

| Risk | When | Rigor |
| ---- | ---- | ----- |
| Low | personal, reversible, under 50 lines | passes 1-3 |
| Medium | project defaults, coordination, 50-150 lines | passes 1-6 |
| High | multi-agent, destructive/downstream, over 150 lines | passes 1-10, items 1-53 |

Default to Medium.

## Principles

Lower number wins in conflicts.

1. Be Specific: concrete paths, commands, values, referents.
2. Define Terms: expand jargon and acronyms first use.
3. Show Examples: demonstrate abstract or fragile rules.
4. Verify Interpretation: checkpoint ambiguous or high-risk actions.
5. State Boundaries: in scope, out of scope, mutable, read-only.
6. Specify Failure Modes: state failure behavior.
7. Specify Defaults: state fallback behavior.
8. Declare Preconditions: required paths, tools, versions, state, checks.
9. Close Loopholes: block rationalizations and minimal compliance.
10. Front-Load: put critical commands, decisions, limits first.
11. Group Related: keep conditions next to consequences.
12. Keep Parallel: match voice, format, hierarchy.
13. Specify Outcomes: define observable success.
14. Economy: remove non-executable words.

Conflict rule: keep lower-numbered principles intact first. If tied, keep more executable and verifiable intent. If still tied, use the shorter version.

## Self-Check

High-risk work uses all 53 checks.

Pass 1, Specificity:
1. Pronouns have clear referents.
2. Vague nouns are concrete.
3. Vague verbs are concrete.
4. Commands include needed paths, args, and cwd assumptions.

Pass 2, Terms and Examples:
5. Jargon is defined.
6. Acronyms are expanded.
7. Abstract rules include examples or formats.

Pass 3, Verification and Authority:
8. High-risk instructions are identified.
9. High-risk instructions have checkpoints or confirmation.
10. Checkpoints verify observable state.
11. Cross-document rules state authority.
12. Overlaps state override, defer, or scope relationships.
13. Skill files state relationship to `AGENTS.md`.
14. `AGENTS.md` states skill/subagent relationships when relevant.
15. Scope limits are explicit.

Pass 4, Boundaries:
16. In-scope surfaces are named.
17. Out-of-scope surfaces are named.
18. Mutable/read-only surfaces are named when relevant.

Pass 5, Preconditions, Failure, Defaults:
19. Preconditions have failure handling.
20. Critical operations state `if X fails, do Y`.
21. Error handling is concrete.
22. File/command/state references include environment context.
23. Dependent steps cite prior success criteria.
24. Each `Requires:` has a `Check:`.
25. Checks are executable or observable.
26. Compound preconditions have separate checks.
27. Unhandled cases have defaults.
28. Defaults are observable.
29. Tool/API dependencies include compatibility constraints when needed.
30. Dynamic resources include freshness checks when needed.
31. Version/freshness failures have handling.

Pass 6, Loopholes:
32. Rules include enough rationale to prevent letter-only compliance.
33. Prohibitions close common rationalizations.
34. Scope words like "reasonable" and "as needed" are concrete.

Pass 7, Structure:
35. Critical info precedes background.
36. Conditions precede consequences.
37. Related instructions are grouped.
38. Lists are parallel.
39. Peer headings are consistent.
40. Terms are consistent.

Pass 8, Outcomes:
41. Instructions have observable success criteria.
42. Outcomes verify through command output, file state, or visible state.
43. "Ensure", "verify", and "confirm" define accepted evidence.

Pass 9, Economy:
44. Filler is removed.
45. Redundant modifiers are removed.
46. Non-executable sentences are removed.
47. Repetition is consolidated.
48. Passive voice becomes active where clearer.
49. Negatives become affirmatives unless prohibition is clearer.

Pass 10, Coherence:
50. Sections do not contradict.
51. A fresh Codex session can follow the doc.
52. Minimal compliance still satisfies intent.
53. Edits converge; recurring/reversing edits are diagnosed.

## Output

Review-only output: `"[Principle #X]: [description] at [location]"`.

Edit output: what changed, why it changed, verification, remaining risks.
