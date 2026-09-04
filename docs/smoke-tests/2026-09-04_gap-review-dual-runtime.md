# 2026-09-04 — gap-review dual-runtime verification

The approved design and executable plan are recorded in [the implementation plan](/Users/jp/.agents/docs/plans/2026-09-04-gap-review-dual-runtime.md), committed as 357addb. Implementation was performed inline in /Users/jp/.agents-worktrees/gap-review on feature/gap-review-dual-runtime. The skill under test was read explicitly from that worktree, so the still-installed Claude-only version could not supply the behavior.

**Current result:** the twelve planned behavior cases passed against the final source bytes below. One additional focused verifier test and one direct check of a preserved malformed result passed. Two earlier runs failed and remain recorded below. The source was merged locally as 105dc3a, the Claude symlink was updated, and fresh token-discovery and target-resolution checks passed in both runtimes.

## Method and permissions

Harness: the plan's disposable fixture generator and test-only launcher, executed against the actual installed CLI clients. Claude Code was 2.1.260; Codex CLI was 0.153.2. Claude coordinator init events identify claude-opus-5[1m], and assistant messages identify claude-opus-5. Codex coordinator turn contexts identify gpt-5.6-sol with max reasoning. No model override was passed; native subagent requests used the host defaults.

Each normal test used its own fixture library and output directory under /private/tmp/gap-review-dual-runtime-20260904-rerun2. The supplied test override replaced ~/.agents only as the reviewed library root. The controlling draft remained /Users/jp/.agents-worktrees/gap-review/skills/gap-review/SKILL.md and its own relative reference. The fixture contained a deliberate one-based/zero-based indexing defect and an explicit no-history boundary. No fixture was added to the live skill library.

Claude used native Agent calls with Workflow disabled. Codex used native spawn_agent calls with fork_turns="none". Serial tests configured one concurrent child: CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS=1 for Claude and agents.max_concurrent_threads_per_session=1 for Codex. Partial and unavailable cases disabled the native agent-start tools. No permission-bypass option, alternate agent-runtime fallback, dependency installation, or source publication was used.

The launcher saved stdout, stderr, the command, the process exit code, and before/after SHA-256 inventories of the complete fixture library. The parent inspected the actual result files, command traces, and final reports; a process exit code alone was not treated as a behavioral pass. Every final-version case exited 0 and preserved all fixture-library bytes and file inventory.

Claude's startup inventory used the historical Task name in enabled runs, while actual native calls were named Agent. No filter workaround was needed: disabling Agent removed both Agent and Task from the available start tools, as observed in the negative cases.

## Tested source identity

The three files currently match the final test snapshot at /private/tmp/gap-review-dual-runtime-20260904-rerun2/draft-source. No test helper is part of the shipped skill.

| File relative to the skill directory | Final SHA-256 |
| --- | --- |
| SKILL.md | d8f1c86b91e0423a1b71dfbcfcd02dc870b2fa31b4eaa6efc949e9b689d6b0b6 |
| references/review-prompts.md | b21961b25ed226b89d5f481ac8e1be90cd3e22c865add067a10549f600effb34 |
| agents/openai.yaml | 6010fa218d093c162254eae972444ab6885018c7c31fad8d4848aa9f03bea352 |

## Planned cases

Every row below reports one run against those final source bytes. “Passed” describes the named test claim, not an endorsement of every qualitative suggestion in a generated fixture report.

| Case | Observation | Result | Evidence |
| --- | --- | --- | --- |
| claude/full | Two fresh reviewers; both JSON results validated before candidate creation; duplicate indexing claims merged; two fresh verifiers; the indexing failure reproduced; report written; fixture unchanged. | Passed | [Assessment](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/full/assessment.json), [report](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/full/out/report.md) |
| codex/full | Two no-history reviewers and one separate no-history verifier; both reviewer files validated before deduplication and verification; the documented wrong outputs observed; fixture unchanged. | Passed | [Assessment](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/full/assessment.json), [report](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/full/out/report.md) |
| claude/seeded | Three supplied claims became two candidates before two fresh verifiers ran. The indexing defect was reproduced; the history-storage request was refuted from the explicit non-goal. | Passed | [Assessment](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/seeded/assessment.json), [report](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/seeded/out/report.md) |
| codex/seeded | Same duplicate/non-goal distinction: one confirmed indexing defect and one refuted history claim, with original severity claims retained. Two fresh no-history verifier calls. | Passed | [Assessment](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/seeded/assessment.json), [report](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/seeded/out/report.md) |
| claude/serial | Two reviewers and three verifiers ran as five foreground, general-purpose Agent calls. Each completed before the next began; no resume or reviewer-context reuse. Observed peak concurrent calls: one. | Passed | [Assessment with call/completion positions](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/serial/assessment.json), [report](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/serial/out/report.md) |
| codex/serial | Two reviewer tasks followed by a distinct verifier task. Native start/completion records show no overlap, and all three starts use fork_turns="none". | Passed | [Assessment with native activity order](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/serial/assessment.json), [report](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/serial/out/report.md) |
| claude/malformed | String-valued findings rejected. A new reviewer supplied review-03.json; the active review-02/review-03 files passed a real parser before candidates and three fresh verifiers were started. The invalid original was preserved. | Passed | [Assessment](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/malformed/assessment.json), [report](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/malformed/out/report.md) |
| codex/malformed | Invalid review-01 preserved as review-01.original.json; a fresh reviewer replaced the result; both selected results passed field checks before one independent verifier ran. | Passed | [Assessment](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/malformed/assessment.json), [review validation](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/malformed/out/review-validation.json), [report](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/malformed/out/report.md) |
| claude/partial | No native start tool. Supplied reasoning-only confirmation retained as one confirmed; zero refuted; missing verdict remains one unverified. Report explicitly incomplete; no new reproduction claimed. | Passed | [Assessment and limitations](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/partial/assessment.json), [report](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/partial/out/report.md) |
| codex/partial | Agents disabled. Candidate/verifier records parsed; supplied reasoning confirmation retained; missing verdict not filled by the coordinator; counts 1 confirmed, 0 refuted, 1 unverified; incomplete report. | Passed | [Assessment](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/partial/assessment.json), [report](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/partial/out/report.md) |
| claude/unavailable | Agent/Task absent; tool discovery found no fresh-agent capability. Stopped after target resolution, without reading target contents, reviewing inline, reusing a peer session, or creating a report. | Passed | [Assessment](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/unavailable/assessment.json), [runtime transcript](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/unavailable/stdout.jsonl) |
| codex/unavailable | Agents disabled. Read the requested draft/reference and stopped before target review; no agent calls, reviewer/verifier outputs, report, or alternate-runtime launch. | Passed | [Assessment](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/unavailable/assessment.json), [final response](/private/tmp/gap-review-dual-runtime-20260904-rerun2/codex/unavailable/last-message.md) |

All per-case directories contain process.json, stdout.jsonl, stderr.txt, and the parent-written assessment.json. Codex directories also contain last-message.md. The process records preserve the exact commands and before/after fixture hashes.

## Failed attempts and repairs

### First failure: unrelated execution labeled as reproduction

The first Claude full run used the plan's original source verbatim. It successfully exercised native agents and preserved the target, but verify-02.json and the report labeled a frontmatter-routing concern “reproduced” after only executing the script with out-of-range values. Those commands demonstrated the range guard's valid rejection, not the claimed routing consequence. The parent graded that run failed.

Evidence: [original assessment](/private/tmp/gap-review-dual-runtime-20260904/claude/full/assessment.json), [verifier result](/private/tmp/gap-review-dual-runtime-20260904/claude/full/out/verify-02.json), and [original report](/private/tmp/gap-review-dual-runtime-20260904/claude/full/out/report.md).

The original SKILL.md hash was 975434acc3b006179ae398d0a36d46b6315fff7e86fc624050e32fadf8b99d40; the reference hash was 87d8819887556888603326e4a5ffea8a283faa299a6a2d103cc66459e54d0d91. Their identity is recoverable from the plan blocks that were verified byte-equal before that run.

Repair: clarify in both controlling paragraphs that execution must demonstrate the specific finding's claimed consequence. A valid rejection or source inspection does not reproduce an unobserved effect on a future agent. This changes no fields, stages, or chosen design.

### Second failure: JSON validation performed too late

The first repaired Claude full run validated reviewer JSON only after creating candidates and dispatching all four verifiers. The late check found a missing findings[1].evidence field and requested a repair from the original reviewer. Recovering before the final report did not satisfy the required ordering, so the parent graded this run failed.

Evidence: [assessment with transcript positions](/private/tmp/gap-review-dual-runtime-20260904-rerun/claude/full/assessment.json), [preserved malformed result](/private/tmp/gap-review-dual-runtime-20260904-rerun/claude/full/review-02-before-repair.json), and [runtime transcript](/private/tmp/gap-review-dual-runtime-20260904-rerun/claude/full/stdout.jsonl). The first candidate was written at transcript line 210, the first verifier started at line 223, and full schema validation occurred at line 519.

That version's SKILL.md hash was 6f9c5f38a458f632f2b8f5b8a1fde87bf5d7df2d4896247fee44fd8f0df298c3; its reference hash was f6ca13ab0a54902fb619e566d8a205e75fac1e5ac4ca7e9b3b04b4082b0ca15b. The snapshot remains in /private/tmp/gap-review-dual-runtime-20260904-rerun/draft-source.

Repair: make the existing transition explicit. Every selected reviewer result must pass parsing and all required field/type/value checks before deduplication, candidate writing, or verifier dispatch. A missing field must be corrected and revalidated first. The corresponding reference states that checking only before the final report is too late.

A recheck-investment pass found no material change to the approved work: both repairs address evidence and JSON requirements already in the plan. No runner framework, new shipped file, or additional product capability was added.

### Focused checks of the repairs

- The planned Claude malformed case was run earlier in the sequence to exercise the validation repair directly. Its generated validator also received the actual missing-evidence result preserved from the failed run. It exited 1 with “finding[1] missing evidence,” as required: [direct check](/private/tmp/gap-review-dual-runtime-20260904-rerun2/claude/malformed/nested-field-check.json). The full Claude rerun then validated review-01 at transcript line 221 and review-02 at line 259, before the first candidate at 304 and first verifier at 316.
- A fresh standalone Claude verifier received the exact original routing candidate and the updated verifier instructions, without prior verdicts. It executed the related rejection commands, refuted the candidate, and set reproduced=false with an explicit explanation that a valid program rejection does not demonstrate a routing failure. This was a focused verifier-instruction test, not another full orchestration run: [assessment](/private/tmp/gap-review-dual-runtime-20260904-rerun/claude/reproduction-label/assessment.json), [result](/private/tmp/gap-review-dual-runtime-20260904-rerun/claude/reproduction-label/out/verify.json).

The final twelve-case table uses the final source hashes, not a mixture of passing results from different source versions. The failed attempts were not overwritten or relabeled.

## Source conformance and structural checks

The package contains exactly SKILL.md, references/review-prompts.md, and agents/openai.yaml. It adds no production helper, plugin manifest, cache copy, hook, or global configuration rule. Its original Claude-only source directory is absent in the implementation worktree.

| Approved requirement | Source evidence in the tested draft | Falsification exercised |
| --- | --- | --- |
| One shared source and both invocation forms | SKILL.md lines 3, 11, and 17–24; matching companion metadata | Worktree has one source directory; no explicit-only policy was introduced. Served discovery is a later check. |
| Native fresh agents; no single-agent fallback | SKILL.md lines 30–36 | Both full runs show distinct native tasks; both unavailable cases stop. |
| Independent verification survives limited capacity | SKILL.md lines 34–36 and 64 | Both serial cases preserve both dimensions and fresh verifier tasks at observed peak concurrency one. |
| Ordinary JSON, with existing fields | Reference lines 49–84; SKILL.md lines 60 and 72–76 | Malformed string and preserved missing nested field rejected; invalid results not used as empty reviews. |
| Evidence labels match the claimed consequence | SKILL.md line 68; reference line 40 | Initial wrong label rejected by parent; exact-claim replay uses reproduced=false; known indexing defect reproduced in both runtimes. |
| Missing verdicts remain unverified | SKILL.md lines 74–87 | Both partial cases preserve one reasoning result and one missing verdict, with incomplete reports. |
| Target preservation and report-only completion | SKILL.md lines 40, 66, and 104–108 | Before/after library hashes and inventory match in every final case; no fixture correction applied. |
| Scope-aware delivery checks | SKILL.md lines 44–52 | Fixture-declared absence of installations is not treated as a defect or a passing comparison. |
| Temporary detailed report and short response | SKILL.md lines 38 and 82–102 | Completed/partial runs write report.md; unavailable runs stop without inventing a report. |

The source review checked malformed-result control flow, duplicate handling, shared output ownership, source-preserving reproduction, source-vs-runtime evidence distinctions, and stale location references. These checks support the defined implementation; they do not replace the runtime observations above or establish general judgment accuracy.

Frontmatter and agents/openai.yaml parse. The local validator reports only the documented unsupported argument-hint key; it is preserved under AGENTS.md's accepted-exception rule. The companion reference exists, the three package files are present, and diff whitespace checks pass. No dependency or tool installation was necessary.

## Proof limits and observations

- These are small controlled cases and synthetic continuations, one final-version sample per case and runtime. They are not a benchmark, a pass-rate estimate, a blind comparative study, or proof for every host configuration.
- Native fresh contexts were checked through actual calls. Claude used general-purpose, non-fork Agent requests. Codex's raw calls use fork_turns="none"; distinct task start/completion events and source reads were also inspected through the app API. Codex's CLI storage encrypts dispatch message payloads, so their literal wording was not recovered; no decryption or key lookup was attempted.
- The one-worker tests demonstrate sequential scheduling under the configured limit and no reviewer-context reuse. They do not test an intentionally forced over-capacity refusal.
- The synthetic continuation cases do not establish that the supplied original reviewers actually read their files. Their reports distinguish those supplied records from the new work.
- Claude's malformed-case report conservatively treated the supplied empty consistency result as uncovered. The recovery/type-validation test passed; that report was not used as evidence of a complete review from discovery.
- Claude's intentionally partial run could not execute its chosen YAML/compile command and disclosed those checks as unavailable. No programmatic JSON-parser execution was observed in that case. It passed the narrower partial-completion claim: preserve the supplied reasoning-only result, do not create the missing verdict, and report incompleteness. Parser behavior is directly covered by the full and malformed cases.
- A Claude formatting hook changed a reviewer's temporary Python copy in one full run. The coordinator caught the byte-identity overclaim before verification, and verifiers used their own copies. The target bytes never changed.
- Ancillary fixture-review judgments varied between runs, including low-severity style suggestions. This record does not certify every such suggestion. The required observed workflow and evidence-handling claims are the basis of the case results.
- The tests' raw logs and temporary copies may later disappear with temporary-directory cleanup. This record preserves the observations and source hashes; the committed plan preserves the executable scenarios.

## Local delivery

The worktree helper bound validation to 105dc3aeed0eaf416824dbad56a7d968c4e3fe9d and fast-forwarded the primary main branch to that exact commit. The source files at /Users/jp/.agents/skills/gap-review and in the implementation worktree still match the final tested hashes above.

The old /Users/jp/.claude/skills/gap-review entry was inspected as a symlink to /Users/jp/.agents/skills-claude/gap-review. Only that stale link was trashed. The repository's claude-skills-sync.sh --link gap-review recreated it pointing to /Users/jp/.agents/skills/gap-review; readlink confirmed that target, and claude-skills-sync.sh --check exited 0 with no violations. The old source directory is absent. No second runtime copy, plugin release, mirror update, or push was made.

Fresh CLI sessions started from /private/tmp/gap-review-dual-runtime-20260904, outside the repository. Both commands were the plan's load-and-resolution probes, with agent creation and source mutation disabled.

| Runtime | Observed load and resolution | Result |
| --- | --- | --- |
| Claude Code | The /gap-review invocation identified its base as /Users/jp/.claude/skills/gap-review, read SKILL.md through that path, quoted the native-agent requirement, and found the relative reference with Glob. It resolved handoff to /Users/jp/.agents/plugins/handoff and identified the plugin and its four skills. The parent's separate readlink check established the source connection, since the probe's own Bash access was denied. | Exit 0; no review, agent dispatch, or report creation. [Transcript](/private/tmp/gap-review-dual-runtime-20260904/claude-load.jsonl) |
| Codex | The $gap-review invocation read /Users/jp/.agents/skills/gap-review/SKILL.md, checked that references/review-prompts.md exists, quoted the native-agent requirement, and resolved handoff to /Users/jp/.agents/plugins/handoff as a plugin. | Exit 0; no review, agent dispatch, or source change. [Transcript](/private/tmp/gap-review-dual-runtime-20260904/codex-load.jsonl), [response](/private/tmp/gap-review-dual-runtime-20260904/codex-load.md) |

These checks establish current token discovery, source/reference resolution, and the normal library root on the installed clients. They are separate from the controlled behavior cases above and do not count as additional full reviews.
