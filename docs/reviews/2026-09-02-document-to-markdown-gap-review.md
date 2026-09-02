# Gap review: skills/document-to-markdown

Date: 2026-09-02. Reviewed at `main` commit `1250395` in `~/.agents`. Evaluation only: nothing in the target was edited, committed, landed, or published.

## Summary

Target resolved: `skills/document-to-markdown`, a dual-runtime trust skill (two files: `SKILL.md` and `scripts/anydoc_extract.py`). Every mechanical check passes. The review found 20 confirmed findings and refuted none: 3 high, 10 medium, 7 low. The three high findings are (1) a scanned page inside a text PDF can be dropped silently with exit 0, so the exit-3 promise is not exhaustive; (2) same-stem documents overwrite each other's output silently and a reused model directory keeps stale assets; (3) the exit table treats every nonzero exit as anydoc's verdict on the document, so launcher and toolchain failures (npm registry, Codex sandbox, uv, missing binding) read as "document unreadable". Four items need a decision from JP (all design or boundary choices); the rest is an 18-item fix batch, 14 of which can be applied without a decision.

## Method

- Phase 0 (inline, orchestrator): read both target files, ran the AGENTS.md Validation Ladder and the delivery checks, queried both registries, and ran the pinned CLI and the script against 27 fixtures. Facts are in the appendix; they were handed to every reviewer as established and not re-litigated.
- Phase 1 (Workflow): four dimension reviewers (consistency, lifecycle, edge cases, routing and dual-runtime delivery), one dedup agent. 32 raw findings, 20 after merging by root cause.
- Phase 2: one refute-default verifier per merged finding for the 10 highest-severity findings (fleet cap of 15 agents: 4 + 1 + 10). The 10 lowest-severity merged findings were verified inline by the orchestrator with the same refute-default stance; each states its evidence below. Agent verifiers confirmed 10 of 10, adjusting two severities (one high to medium, one medium to low). Inline verification confirmed 10 of 10.
- Fleet: 15 agents, 1.72 M subagent tokens, 260 tool calls, 33 minutes.

Evidence labels used below: **reproduced** = someone ran the failing thing and watched it fail (reviewer, verifier, or orchestrator, named); **by argument** = confirmed from the quoted text and the established facts without a runnable reproduction.

## Clean

Only these claims are made:

- Phase 0 mechanical checks all pass: `quick_validate.py` valid; frontmatter parses (60-word description); `ruff check` and `ruff format --check` clean; `git diff --check` clean; `check-library-integrity.sh` all pass (name equals directory, cited paths resolve, no orphan support files, frontmatter valid); `claude-skills-sync.sh --check` clean and the `~/.claude/skills/document-to-markdown` symlink resolves; both registries hold 0.2.4 as latest; the pinned npx CLI and the pinned uv script both run on this machine.
- No target surface was read without findings: both `SKILL.md` and `scripts/anydoc_extract.py` carry confirmed findings. The consistency surfaces outside the target (the pinned Python stub and wrapper, the vet report, the ledger line, AGENTS.md) were read by reviewers and produced no finding against those surfaces themselves.
- The never-upload boundary held under every test: `--ocr reject` with `FIRECRAWL_API_URL` and `FIRECRAWL_API_KEY` set made no network attempt; the library path has no OCR argument at all.

## Confirmed findings

### High

**F1. A scanned page inside a mixed text PDF is dropped silently with exit 0.** contract-defect, consistency. **Reproduced** by the reviewer, the verifier (independent fixtures built with fpdf2, including two scanned pages among eight text pages), and the orchestrator (`reviewer-consistency/mixed.pdf`: 3 pages, page 2 has no text and one image; CLI exit 0, 221 bytes, empty stderr, the page simply absent).
`SKILL.md` line 18 says a scanned PDF is caught by exit code 3, the exit-3 row says pages needing OCR are reported, and the Known Gaps PDF bullet lists no case where a page vanishes. On the pinned build, a PDF that mixes text pages and scanned pages is often converted with exit 0 and the scanned pages missing, with no marker in the Markdown. The pinned Python library behaves the same (no `NeedsOcrError`), so the In A Codebase advice to catch that error does not catch it either. The vet report recorded the neighbouring upstream defect (issue 144) and the skill did not carry it into Known Gaps. Realistic loss: a contract with a scanned signature page, or a report with a scanned exhibit, is reported as fully converted.
Verifier correction: the mechanism is upstream pdf-inspector's whole-document classification, not the page count. The reviewer's "1 of 3 drops, 1 of 4 exits 3" pattern was a fixture artifact: identical repeated pages are de-duplicated by anydoc, which left the larger fixtures nearly text-empty and flipped the classifier. With distinct normal-length text pages the scanned page was dropped in every mix tried.
Fix: batch item 1.

**F2. Same-stem documents silently overwrite each other's output, and a reused model directory keeps stale assets that the report then miscounts.** contract-defect, lifecycle + edge cases (claimed high and medium; verifier kept high). **Reproduced** by the reviewers and the verifier (`report.docx` then `report.xlsx` into the same scratch: the docx Markdown is gone, exit 0 both times; `q1/report.docx` then `q2/report.docx`: the first is lost; a reused model directory keeps `report-0.png` and `report-1.bin` while the new `document.json` lists zero assets), and by the orchestrator in Phase 0 (stale assets case).
Both output paths are built from the basename alone (`<scratch>/<basename>.md`, `<scratch>/<basename>-model`), the CLI truncates on `-o`, and the script does `mkdir(exist_ok=True)` with no existing-output check. "Loop and report each outcome" over a folder makes the collision routine.
Verifier correction: `<basename>` is not wholly undefined. Line 56 (`assets/<basename>-<id>.<ext>`) together with the script's `args.file.stem` pins it to the stem, so the text already commits to the colliding reading. A fix that renames outputs must also change line 56 and the script's asset naming so they stay in step.
Fix: decision 2, then batch item 15.

**F3. The exit table assumes every nonzero exit is anydoc's verdict on the document; launcher and toolchain failures land on the wrong rows.** contract-defect, lifecycle + edge cases + routing (claimed medium, medium, high, low across four raw findings; verifier kept high). **Reproduced** by the reviewers and the verifier: a fresh npm cache with the registry unreachable exits 1 with 21 stderr lines and no `anydoc:` line; a missing native binding makes `--version` print 0.2.4 with exit 0 while the conversion exits 1 with a Node stack trace; a fresh uv cache with the index blocked exits 2 with `error: Request failed after 3 retries`; uv off `PATH` exits 127; the Codex `workspace-write` sandbox refuses the npm cache write.
The exit-1 row then says "not readable or not convertible, do not retry", and uv's exit 2 reads as "usage error, fix the command". Line 63 ("On failure it prints one `anydoc: <message>` line") is the only signal that could separate the cases, and the table does not use it.
Verifier correction: the plain offline case is already half-covered (lines 29 and 55 say "which you report"). The genuinely uncovered cases are the sandbox cache denial, the missing native binding, uv's exit 2, and exit 127. The high grade rests on the Codex sandbox case.
Fix: batch item 2.

### Medium

**F4. The shell-tool timeout does not kill a hung converter under Claude Code, and a coreutils `timeout` kill returns 124, which matches no row.** contract-defect, edge cases (claimed high; verifier adjusted to medium). **Reproduced** by the verifier under Claude Code 2.1.258: a piped hang with a 6 s tool timeout was "moved to the background" with a task id, and the `tail`, `npm exec`, and `node` processes were still alive 46 minutes later; the official tools reference documents the same behaviour. Orchestrator: `timeout 1 sleep 3` exits 124; `/usr/bin/timeout` does not exist on stock macOS (Homebrew coreutils provides it here).
Line 42 says "a crash or hang ends that process, not the session" and the last table row says "killed by the timeout". Under Claude Code neither happens by itself.
Verifier correction: the backgrounded task is killable through the harness (`TaskStop <id>` ended the whole process group in the reproduction), and a foreground subagent's backgrounded command ends when the subagent returns. So the fix is a wording change plus a `timeout` wrapper, not a new mechanism.
Fix: batch item 3.

**F5. "The version is written in exactly two places" is false; the documented bump leaves the executed commands on the old version.** contract-defect, consistency + lifecycle. **Reproduced** by the verifier (a simulated bump on a scratch copy, done exactly as line 24 says, left seven `0.2.4` literals) and the orchestrator (`0.2.4` on `SKILL.md` lines 24, 28, 29, 35, 55, 88, nine occurrences, plus the script's line 4).
Verifier correction: a stale line 28 also rejects a correctly upgraded global install, because it checks for the literal `0.2.4`, so both CLI resolution steps stay on the old version whatever is installed. The ledger entry repeats the misstatement as "a single pinned version line".
Fix: batch item 4.

**F6. The description promises the embedded images and structured content of a PDF; the body excludes both.** contract-defect, consistency. **Reproduced** by the verifier (a PDF with 40 lines of text and one embedded PNG: the Markdown path exits 0 with the image absent, the library path exits 1). Lines 19, 49, and 80 each exclude PDF images; the description offers them.
Verifier correction: headings and tables do come through the Markdown path for PDF, so the crisp contradiction is embedded images and page-level content, not all structure. Any parenthetical naming another skill should use the body's availability-conditional wording.
Fix: decision 1, then batch item 16.

**F7. The script passes `--format` through unvalidated: an unknown or alias name exits 1 as a document error where the CLI exits 2 or accepts the alias, and the script's exit-3 branch is unreachable.** contract-defect, consistency + lifecycle + edge cases. **Reproduced** by the reviewers, the verifier, and the orchestrator (`--format xls` and `--format bogus`: script exit 1, CLI exit 0 and exit 2 respectively; both PDFs exit 1 before parsing, so `NeedsOcrError` can never be raised).
Line 58 says the exit codes are "the same table below". The script's docstring lists exit 3 as possible.
Verifier correction: `--format ''` is treated as absent by the script (`if explicit:`), so the empty-string case is not reachable through the script; and the script's own stderr line lists the twelve accepted names, so a session has something to correct against.
Fix: batch item 5.

**F8. The script's mkdir, asset writes, and `document.json` write run outside the `try` block, so reachable filesystem errors after a successful parse exit 1 with a raw traceback and no `anydoc-extract:` line.** contract-defect, consistency + edge cases. **Reproduced** by the reviewer, the verifier (outdir is a file; a 250-character stem gives OSError 63 on the asset name while the CLI converts the same file; a read-only parent; passing the Markdown path as outdir), and the orchestrator (outdir is a file).
Verifier correction to the proposed fix: truncate the stem by UTF-8 byte length, not characters, or simply let an `except OSError` wrap report it; an explicit `is_dir()` check misses a regular file as a parent component, so the wrap is what closes the hole.
Fix: batch item 6.

**F9. Line 44's `--format` rule over-prescribes for mis-named containers, and the exit-1 row's blanket "do not retry" forbids the one corrective rerun.** contract-defect, consistency + edge cases; the `.tsv` sub-defect from the template-extensions finding is folded in here because it has the same root cause. **Reproduced** by the reviewers, the verifier, and the orchestrator: `renamed.pdf` and `noext` (docx bytes) convert with no flag; `renamed.pdf --format pdf` and `text.pdf --format docx` exit 1 because an explicit `--format` overrides content detection; `data.tsv` exits 1 with "unrecognized file content and extension" and converts to a correct table with `--format csv`.
Line 44 says detection "cannot work" when the extension is missing or wrong; the pinned wrapper's docstring says content is detected first and the extension is only a fallback for signature-less formats. The exit-1 row then says "do not retry with other flags", which forbids the `--format csv` rerun that a delimited text file needs.
Verifier correction: the "guessed from the wrong extension" path is contrived. The realistic harm is an extension-less file, where a session reads line 44 as "detection cannot work, so `--format` is mandatory" and stalls or guesses when the bare run works, and the delimited-text case.
Fix: batch item 7.

**F10. No path for keeping the Markdown: scratch-only output plus "never write next to the source" leaves the deliverable case uncovered.** gap, lifecycle. **By argument** (orchestrator inline). Use When line 13 includes "convert to Markdown such a file", a deliverable request. Line 41 allows only the session scratch directory or `mktemp -d` and forbids writing next to the source; line 92 reports the scratch path. Nothing says whether a user-named destination is allowed, whether to copy after converting, or that scratch output does not outlive the session. A session facing "convert report.docx to markdown for me" either breaks the rule or hands back a temporary path. Not a re-proposal of the scratch boundary: the fix keeps it (convert into scratch, then copy to the destination the user named).
Fix: decision 4, then batch item 17.

**F11. The description's "you cannot read directly" clause contradicts the body's unconditional Use When list.** contract-defect, routing (two raw findings merged: PDF on Claude Code, CSV on both runtimes). **Reproduced in part** by the reviewer and the orchestrator: Claude Code's Read tool opened `fixtures/text.pdf` and rendered `fixtures/scan.pdf` locally (page images, no network); it refuses `.docx` as binary. CSV is plain text on both runtimes. So for "read this PDF" on Claude, the description says do not fire and the body (lines 12, 13) says fire; the loader cannot decide. The two realistic PDF intents land on the wrong side: a long text PDF is where the Markdown path beats page images, yet the description excludes it; "what does page 4 say" is best served by the runtime's own page reader, yet line 19 routes it to the `pdf` skill only.
Fix: decision 1, then batch item 16.

**F12. Slide-numbered questions are unanswerable through this skill, and the text neither says so nor routes them away.** gap, routing. **Reproduced** by the reviewer and the orchestrator: `cli-out/pres.md` runs both slides together with zero separators or slide numbers; the document model has no slide or section block kind and no origin field on blocks. Known Gaps covers the analogous PDF page gap (line 81) and line 19 routes page needs away; nothing covers slides. The Claude neighbour (`anthropic-skills:pptx`) extracts "one `## Slide N` section per slide".
Orchestrator correction: on Codex, the only document neighbour confirmed in the rendered CLI skills list is the bundled `pdf` skill; a `presentations` skill named by the reviewer did not appear in that list, so the Codex half of the routing sentence should be phrased "where available".
Fix: batch item 8 (Known Gaps) and decision 3 (routing sentence).

**F13. The description does not resolve the read-only collision with the runtimes' document-authoring skills, which all claim reading.** gap, routing. **By argument** (orchestrator inline, from the four Claude neighbour descriptions read from the desktop app's bundled plugin copy): `docx` ("create, read, edit, or manipulate Word documents"), `pptx` ("any time a .pptx file is involved in any way ... reading, parsing, or extracting text"), `xlsx` ("open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv"), `pdf` ("anything with PDF files ... reading or extracting text/tables"). All four are live in this session. The target's differentiator ("converted locally with a pinned anydoc build and never uploaded") is a how, not a when, so for "read this .docx and summarize it" the loader has no rule for which side wins, and the neighbours' claims are longer and more imperative. The cost is the skill's own value: a neighbour builds its own extraction with its own tooling and no pin.
Orchestrator correction: the Codex side is weaker than the reviewer stated; only `pdf` was confirmed there.
Fix: decision 1, then batch item 16.

### Low

**F14. No upgrade or re-vet procedure: "after re-vetting the release" names no checks, and the vet report the skill rests on is never referenced.** gap, lifecycle (claimed medium; verifier adjusted to low). **By argument**: `grep docs/reviews` in the skill returns nothing; the fixtures behind commit `1250395`'s live runs were scratch artifacts, so a bump session must rebuild them. Verifier correction: the proposed six-step subsection would copy machinery `dependency-upgrade` and the Validation Ladder already own; what is missing is about three sentences.
Fix: batch item 9.

**F15. Hostile-file guidance carries the vet report's timeout but drops its memory cap, and "treat the file as untrusted" carries no obligation.** contract-defect, consistency + lifecycle. **By argument** (orchestrator inline; quotes confirmed at vet report lines 13, 60, 66, 119 and `SKILL.md` lines 42, 71, 88). The vet's adoption condition 3 names two guards for downloaded files, an OS memory limit and a timeout, because the crafted PDF reaches about 4 GB resident before erroring. The skill carries the timeout only. macOS gives no reliable per-process resident-memory cap from a shell, so the honest fix is a warning in Run and a real requirement in In A Codebase.
Fix: batch item 10.

**F16. The folder loop is under-specified: timeout scope, per-file outcome line, and whether one crash stops the loop.** gap, lifecycle. **By argument** (orchestrator inline). Line 42's two-minute timeout is per shell call; line 43's "loop and report each outcome" does not say one call per file, so a single-call loop over 40 files is killed at two minutes with the earlier outcomes lost unless printed. `timeout` is not on stock macOS (confirmed: no `/usr/bin/timeout`; Homebrew coreutils provides it here).
Fix: batch item 11.

**F17. The exit-3 stop names no local, no-upload route where one exists on the runtime.** gap, lifecycle + routing. **Reproduced** by the orchestrator: the Read tool rendered `fixtures/scan.pdf` page 1 locally with no network; the Claude `pdf` skill documents local OCR (pytesseract over rendered pages, lines 233 to 236 of its `SKILL.md`); the Codex bundled `pdf` skill renders pages with `pdftoppm`. Line 73 says OCR is the user's decision "with a different tool" and stops, naming none. Not a challenge to the never-upload boundary: every route named is local.
Fix: decision 3, then batch item 18.

**F18. Template extensions `.dotx`, `.potx`, `.xltx` convert but are unlisted.** gap, lifecycle. **Reproduced** by the reviewer and the orchestrator (LibreOffice-made `plain.dotx`, `pres.potx`, `sheet.xltx` all exit 0 on the CLI; content detection reads the OOXML package). Line 12 lists 21 extensions without them, so a session following the list declines them. (`.xlsb` stays listed but untested: LibreOffice has no export filter for it.)
Fix: batch item 12.

**F19. SVG assets are written with the extension `.svgxml`.** contract-defect, edge cases. **Reproduced** by the reviewer (a hand-built docx with an SVG picture: `assets/crafted-0.svgxml`) and at function level by the orchestrator (`image/svg+xml` maps to `svgxml`; the pinned binary carries `image/svg+xml` among its emitted media types, alongside png, jpeg, bmp, emf, wmf, octet-stream, and ms-ole-object, all of which map to usable names). No viewer or image library associates `.svgxml` with SVG, so the one purpose of the library path is defeated for SVG until the file is renamed.
Fix: batch item 13.

**F20. The `<skill dir>` placeholder in the uv command is never defined.** gap, routing. **Reproduced** by the reviewer and the orchestrator: `<skill dir>` appears once (line 52) with no definition, while `<anydoc>` and `<scratch>` are defined. Both runtimes supply the path: Claude Code prints "Base directory for this skill" on invocation and documents a `${CLAUDE_SKILL_DIR}` substitution; Codex's rendered skills list gives `(file: r1/document-to-markdown/SKILL.md)` with a roots table `r1 = /Users/jp/.agents/skills` (confirmed with `codex debug prompt-input`). The in-library precedent (`claude-home-audit`) defines its `$SKILL_DIR` token in prose.
Fix: batch item 14.

## Refuted findings

None. Ten findings went to refute-default agent verifiers and all ten were confirmed; two had their severity lowered (F4 high to medium, F14 medium to low). Ten went to the orchestrator's inline refute-default check and all ten were confirmed; the evidence for each is stated in its entry, and two received scope corrections (F12 and F13, the Codex neighbour claims). The raw-to-merged step merged 32 findings into 20 without dropping any (every raw index appears in exactly one merged group).

## Decisions needed from JP

Recorded 2026-09-02: JP chose the lean on all four (1a, 2a, 3a, 4a). The fix batch below is therefore fully specified; items 15 to 18 follow those choices.

**1. Rewrite the frontmatter description (F6, F11, F13).** All three confirmed defects live in the description, which is routing text JP owns under AGENTS.md Skill Editing.
   1. One rewrite: drop "you cannot read directly", limit "embedded images and structured content" to the non-PDF formats, and add one sentence giving this skill precedence over the runtime's document-authoring skills when the task only reads a file. About 80 to 85 words. AGENTS.md allows going past 60 (and up to about 90) only to prevent a specific likely misroute, and F13 is that misroute. **Lean.**
   2. Fix F6 and F11 only and stay at or under 60 words; leave the neighbour collision to the neighbours' own descriptions.
   3. Leave the description alone and fix the body only.

**2. Output naming scheme (F2).**
   1. Name outputs by the full file name: `<scratch>/<file name>.md` and `<scratch>/<file name>-model/` (so `report.docx.md` and `report.docx-model/`), and change line 56 and the script's asset naming to match; the script additionally refuses a non-empty output directory. **Lean.**
   2. Keep the stem but add a collision rule: refuse to overwrite, append a numeric suffix, and have the script refuse a non-empty output directory.
   3. A per-run subdirectory (`<scratch>/<run id>/`), leaving names as they are.

**3. Naming other tools in the body (F12, F17).** Both fixes name a neighbouring skill or a runtime tool.
   1. Name them availability-conditionally, per AGENTS.md ("on Claude Code, ...; on Codex, ... where available"). **Lean.**
   2. Keep the generic "page-aware tool" phrasing and add only the Known Gaps facts, leaving the session to find the neighbour.

**4. Deliverable destination (F10).**
   1. Convert into scratch, then copy the finished file (and the model directory when it ran) to a destination the user named; when the request is a deliverable and no destination was named, ask for one; state in the report that scratch output may not outlive the session. **Lean.**
   2. Keep scratch-only output and always ask before any copy.

## Fix batch

Items 1 to 14 need no decision. Items 15 to 18 wait on the decision named.

1. (F1) Known Gaps, PDF bullet: add that a PDF mixing text and scanned pages can be converted with exit 0 and the scanned pages dropped with no diagnostic; when a PDF may hold scanned pages, say the output may be missing pages or compare page counts with a page-aware tool. Exit-3 row: "Pages need OCR (reported for some documents only; see the PDF gap)". Line 18: point to both the exit-3 row and the PDF gap. In A Codebase: absence of `NeedsOcrError` is not proof every page was read.
2. (F3) Above the exit table: apply the table only when stderr carries an `anydoc:` (CLI) or `anydoc-extract:` (script) line; any other nonzero exit is the launcher or toolchain (npx, node, uv, a sandbox denying a cache write, `PATH`), to be reported as such and never read as a verdict on the document. Add rows for 127 (command not found) and 124 (coreutils `timeout` kill).
3. (F4) Line 42: say that under Claude Code the shell tool may move a timed-out command to the background instead of killing it; wrap the command in `timeout 120` when that binary exists (Homebrew coreutils here; not stock macOS) and otherwise stop the backgrounded task by its id; fold 124 into the crash row.
4. (F5) Line 24: replace "exactly two places" with the enumerated list (lines 24, 28, 29, 35, 55, 88 and the script's `dependencies` line), or restructure so the version is written once and every command refers to that line.
5. (F7) Script: give `--format` `choices=` over the twelve names so a bad name exits 2 with argparse's message; resolve aliases through `anydoc.format_from_extension` before rejecting; delete the unreachable `NeedsOcrError` branch and correct the docstring; line 58: the script exits 0, 1, or 2 only.
6. (F8) Script: wrap `mkdir`, the asset writes, and the `document.json` write in `try/except OSError` routed through `fail(1, ...)`; guard the stem by UTF-8 byte length.
7. (F9) Line 44: "Detection reads the file content first; the extension matters only for CSV and other delimited text (`.tsv`, `.txt`), which need `--format csv`. Do not pass `--format` for a container whose extension is wrong or missing." Exit-1 row: one exception, a delimited text file that failed with "unrecognized file content and extension" is rerun once with `--format csv`.
8. (F12) Known Gaps: presentations bullet (slides are not marked; slide titles are plain paragraphs; speaker notes are block quotes after each slide's text; no slide numbers on either path).
9. (F14) Pinned Tool: three sentences naming `docs/reviews/2026-09-01-anydoc-vet.md` as the baseline, what a re-vet checks (release notes, the two known crash cases, the OCR default still `reject`), and that `dependency-upgrade` plus the Validation Ladder own the mechanics.
10. (F15) Line 88: "a child process with a memory limit and a timeout; a crafted PDF has reached about 4 GB, and no conversion has a built-in time limit." Line 42: the timeout is the only guard a shell gives on macOS; an out-of-memory kill arrives as exit 137.
11. (F16) Line 43: one shell call per file so the timeout applies per file; print `<file>: exit <n>` after each conversion; a failure on one file does not stop the loop; the report lists every file with its outcome.
12. (F18) Line 12: add `.dotx`, `.potx`, `.xltx`.
13. (F19) Script `asset_extension`: drop the `+suffix` before cleaning so `image/svg+xml` gives `svg`; update the docstring example.
14. (F20) Under the uv command: define `<skill dir>` (Claude Code: the "Base directory for this skill" line, also available as `${CLAUDE_SKILL_DIR}`; Codex: the `(file: ...)` entry expanded through the skill roots table; on this machine `/Users/jp/.agents/skills/document-to-markdown`).
15. (F2, after decision 2) Rename the output paths per the chosen scheme; change line 56 and the script's asset naming in step; script refuses a non-empty output directory.
16. (F6, F11, F13, after decision 1) The description text.
17. (F10, after decision 4) Run bullet on destinations and the Report line on scratch lifetime.
18. (F17, after decision 3) After "say so and stop" on line 73: name the local routes (Claude Code: the Read tool renders PDF pages; the `pdf` skill offers local OCR; Codex: the bundled `pdf` skill renders pages with `pdftoppm`), phrased availability-conditionally.

## Observations outside the target

Not findings against the skill; listed so they are not lost.

- The ledger entry at `docs/agents/contract-decisions.md:152` says commit `4124286` carries a "live forward test of exit 0/1/3"; that commit's message says "No live invocation yet", and the live runs in the history (commit `1250395`) exercised the script only. The CLI ran on this machine for the first time during this review. The same entry repeats the "single pinned version line" claim from F5. The ledger is append-only, so the route is an appended correction line, if JP wants one.
- A `.doc` written by macOS `textutil` is rejected by anydoc ("not an OLE2 compound file: Malformed MiniFAT") while a LibreOffice-written `.doc` converts. Reproduced by the orchestrator on both paths; not assessed for how common textutil-made files are, so not graded.

## Coverage record

Files each reviewer reports reading in full (the coverage behind the Clean section):

- consistency: `SKILL.md`, `scripts/anydoc_extract.py`, the pinned `_anydoc.pyi` and `__init__.py`, the vet report, `AGENTS.md`.
- lifecycle: the same six, plus `~/.codex/skills/pdf/SKILL.md` and the pinned npm package's `cli.js`, `anydoc.js`, and `package.json`.
- edge cases: the same six, plus `contract-decisions.md` lines 150 to 154 only.
- routing: `SKILL.md`, the script, `_anydoc.pyi`, the vet report, `AGENTS.md`, the Codex `skill-creator` and `pdf` skills.

## Artifacts (session scratchpad, temporary; not preserved with this file)

- `phase0-facts.md`: the established-facts list given to the reviewers.
- `workflow-result.json`: raw, merged, verified, and dropped findings with verifier verdicts.
- `fixtures/`: the 27 Phase 0 fixtures; `cli-out/` and `lib-out/`: their outputs; `reviewer-*/` and `verifier-*/`: the agents' reproductions; `inline-verify/`: the orchestrator's inline reproductions.
- Workflow transcript: `~/.claude/projects/-Users-jp--agents/0dd652d8-74d8-4aa7-9d73-806e98ade5c6/subagents/workflows/wf_e52faecc-4a5/`.

## Appendix: Phase 0 established facts

Target: `skills/document-to-markdown` — dual-runtime skill (Codex scans `~/.agents/skills` in place; Claude serves it through the `~/.claude/skills/document-to-markdown` symlink). Two files: `SKILL.md` (92 lines) and `scripts/anydoc_extract.py` (190 lines). No `references/`, `examples/`, or `agents/openai.yaml`.

Mechanical checks (all pass):

| Check | Result |
| --- | --- |
| `quick_validate.py skills/document-to-markdown` | Skill is valid |
| Frontmatter parse; description length | parses; 60 words |
| `ruff check` / `ruff format --check` on the script | clean / already formatted |
| `git diff --check`; working tree | clean; clean at `main` |
| `scripts/check-library-integrity.sh` | all 5 structural checks + 5 delegated canaries pass |
| `scripts/claude-skills-sync.sh --check` | clean; symlink resolves to the repo dir |
| Registry pins | npm `@firecrawl/anydoc` latest = 0.2.4, engines node >= 20; PyPI `firecrawl-anydoc` latest = 0.2.4, requires_python >= 3.10, arm64 wheel 3.26 MB |
| Local toolchain | node v24.11.1, npx 11.6.2, uv 0.11.32 (script runs on uv-managed CPython 3.13); `anydoc` not on PATH; pinned npx run prints 0.2.4; npx cache holds the 6.8 MB package after first run |
| Extension map | all 21 listed extensions map to a format via `format_from_extension`; dot/dotx/potx/xltx/txt/md/html/tsv/odf map to None |

Live runs (fixtures in the session scratchpad; the CLI had never been run on this machine before this review — no npx cache existed):

- CLI exit 0 on every supported fixture (docx with a PNG and an OLE object, pptx, xlsx, soffice-made doc/xls/ppt, rtf, odt, epub, csv, text PDF, wrong-extension docx, extension-less docx, name with spaces, dotted stem, stdin csv with `--format csv`, stdin docx with no flag, `--format xls` alias). Corrupted-part docx/pptx/xlsx exit 0 with the part silently dropped.
- CLI exit 1: textutil-made `.doc` ("not an OLE2 compound file"), 0-byte file, `.html`, `.txt` holding CSV bytes without `--format`, nonexistent file, directory, and `-o` into a directory that does not exist (conversion succeeded, write failed: "anydoc: ENOENT").
- CLI exit 2: invalid `--format`, unknown option, no arguments. Exit 3: image-only PDF ("anydoc: page 1 of 1 needs OCR"), unchanged and with no network attempt when `FIRECRAWL_API_URL`/`FIRECRAWL_API_KEY` are set.
- Every CLI failure prints one `anydoc: <message>` stderr line and writes no output file; `-o` overwrites an existing file silently; the PNG appears in the Markdown as the bare alt text with no image syntax.
- Script: exit 0 with `assets/` and `document.json` on every non-PDF fixture (asset names `<stem>-<id>.<ext>`, image inlines carry `asset_id`, `kind` first, None fields dropped). Exit 1 with one `anydoc-extract:` line on PDFs (text and scanned alike — the PDF check runs before parsing, so exit 3 is unreachable), malformed/empty files, undetectable formats, nonexistent input, invalid `--format` (also `xls`, an alias the CLI accepts; CLI gives 2 here). Exit 1 with a raw Python traceback when the outdir path is an existing file. Exit 2 with argparse text when arguments are missing. Re-running into an outdir that holds another document's assets leaves the stale asset files while `document.json` lists 0 assets.
- Helper probes: coreutils `timeout` exits 124 on kill; `asset_extension` gives `svgxml`, `xemf`, `pngcharsetbinary` for `image/svg+xml`, `image/x-emf`, `image/png; charset=binary`, and `bin` for `IMAGE/PNG`.
- Not re-run (taken from the vet report): crafted `.ppt` → stack overflow exit 134; crafted 1 MB PDF → ~4 GB resident before erroring; no time limit inside the library.

Observation outside the target (not a finding): the ledger entry at `docs/agents/contract-decisions.md:152` says commit `4124286` carries a "live forward test of exit 0/1/3"; that commit's message says "No live invocation yet". The live runs recorded in the history are commit `1250395`'s script runs. The CLI facts above are the first live CLI evidence on this machine.

Routing neighbours (read from the Claude desktop app's bundled anthropic-skills plugin copy; Codex bundled `pdf` read from `~/.codex/skills/pdf/SKILL.md`):

- `anthropic-skills:docx` — "create, read, edit, or manipulate Word documents (.docx files) … extracting or reorganizing content from .docx files".
- `anthropic-skills:xlsx` — "any time a spreadsheet file is the primary input or output … open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file".
- `anthropic-skills:pdf` — "do anything with PDF files. This includes reading or extracting text/tables from PDFs … extracting images, and OCR on scanned PDFs".
- `anthropic-skills:pptx` — "any time a .pptx file is involved in any way … reading, parsing, or extracting text from any .pptx file".
- Codex bundled `pdf` — "reading, creating, or reviewing PDF files where rendering and layout matter".
- In-library precedent for locating a skill's own script from both runtimes: one skill defines `$SKILL_DIR` explicitly before `uv run "$SKILL_DIR/scripts/…"`; `document-to-markdown` uses the bare placeholder `<skill dir>`.
- Claude Code documents a `${CLAUDE_SKILL_DIR}` substitution ("The directory containing the skill's SKILL.md file … Use this in bash injection commands to reference scripts or files bundled with the skill, regardless of the current working directory"), substituted in skill Markdown and `allowed-tools`. Codex has no equivalent documented locally; the in-library dual-runtime precedent (`claude-home-audit`) defines `$SKILL_DIR` in prose as "this skill's base directory (announced when the skill loads)".
