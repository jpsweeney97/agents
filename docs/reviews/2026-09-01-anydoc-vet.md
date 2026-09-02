# Vet report: firecrawl/anydoc

Target: https://github.com/firecrawl/anydoc at commit 261fc25 (v0.2.4 plus three README-only commits). Checked on 2026-09-01.

## Verdict

**Adopt with conditions. It is a legitimate, well-built library from Firecrawl, safe to use offline on documents you trust, and a good fit for your Python stack. Do not install its bundled agent skill as shipped, do not use its hosted OCR mode, and do not run it in-process on documents you did not choose.**

The four conditions, each explained below:

1. Pin exact versions everywhere. The project ships breaking changes in patch releases.
2. Treat exit code 3 (needs OCR) as a stop. Never pass `--ocr hosted`, and keep `FIRECRAWL_API_KEY` out of agent environments.
3. Convert untrusted or downloaded files in a subprocess with a memory cap and a timeout. Two crashes are reproducible today.
4. Write your own skill in your repo instead of running `npx skills add firecrawl/anydoc`. The installer writes into `~/.agents/skills` and `~/.claude/skills`, which your repo and sync script own.

## What it is

A Rust library that converts Word, PowerPoint, Excel, OpenDocument, RTF, EPUB, CSV, and text-based PDF files into GitHub-Flavored Markdown. It ships Node, Python, and WebAssembly bindings and an `npx` command-line tool. Firecrawl (legal name Sideguide Technologies Inc.) built it for their paid Parse product and open-sourced it under MIT on 2026-08-03. It has about 19,900 stars after four weeks.

## Legitimacy and provenance

**The code is what it says it is, and nothing in it phones home.**

- The author of 118 of 130 commits is a Firecrawl employee: commits from a sideguide.dev address, public member of the firecrawl GitHub organization, 56 commits in the main Firecrawl repo since January. The GitHub account is seven months old with one public repo, which is normal for a work login.
- The main Firecrawl product pins this crate as a dependency. That anchors continuity: it will not be abandoned while Firecrawl Parse exists.
- No telemetry, crash reporting, update check, or version ping exists on any of the four delivery surfaces. The Rust crate has no HTTP or TLS dependency at all. The demo web page loads no third-party scripts.
- The npm package has no install scripts. The Node loader only loads locally installed platform packages; it cannot download anything at runtime.
- npm and PyPI packages carry provenance attestations tied to the release workflow at the tagged commit. PyPI uses trusted publishing (no long-lived secret). npm and crates.io publish with long-lived personal tokens. The compiled binaries inside the packages are built on Blacksmith (a third-party CI runner service), so the attestation proves the package came out of the workflow, not that the binary bytes were built on GitHub-hosted machines. If that matters, build from the crates.io source or the PyPI sdist.
- Weak points: no branch protection, no rulesets, no second reviewer, ten workflow actions pinned by floating tag rather than commit hash, and `wasm-pack` fetched by `curl` with no checksum. Anyone with push access can publish to all three registries with one tag push.

## Privacy

**With the defaults, no document bytes leave the machine on any surface. I ran the real Node and Python wrapper code against a local stub with the environment variables set and no `ocr` option; zero requests were made.**

The opt-in `ocr: hosted` mode is the one exception, and it has three problems:

- It sends the entire PDF, including pages that parsed fine locally, plus the real filename, to `api.firecrawl.dev`. Keyless use is allowed, so no account is needed.
- It never sets Firecrawl's `zeroDataRetention` request option. Firecrawl's marketing FAQ says Parse does not cache documents, but the privacy policy and terms of service say nothing specific about uploaded documents, and the terms contain a broad content license clause.
- `FIRECRAWL_API_URL` is trusted without any check. A poisoned environment redirects the upload and the API key to any host, including plain HTTP.

The bundled agent skill makes this worse. Rule 5 tells an agent that when the CLI exits 3, it should rerun with `--ocr hosted`. There is no instruction to ask the user first, and the CLI prints nothing before uploading. An agent following that skill uploads any scanned PDF it meets.

## Safety against hostile files

**The zip and XML layers are genuinely well defended, but two crashes are reproducible on v0.2.4, and neither can be caught from Node or Python.**

Verified strengths:

- Decompression bombs are rejected before decompressing, by reading through a hard-capped reader rather than trusting the declared size. Tested with the repo's own abuse fixtures.
- Path traversal out of an archive is impossible by construction.
- The XML reader does no DTD or entity expansion, so the classic XML attacks do not apply, and it enforces depth and node-count caps.
- Zero `unsafe` blocks in the crate and all three bindings. A parser bug can crash the process but cannot become memory corruption.
- 12 fuzz targets exist, though they never run in CI and three formats (pptx, ods, odp) have no target.

Reproduced crashes (the workflow agent found them; I reran both myself):

| Input | Size | Result |
| --- | --- | --- |
| Crafted .ppt with 50,000 nested record containers | 413 KB | Process aborts with a stack overflow, exit code 134 |
| Crafted PDF with one highly compressible content stream | 1 MB | About 4 GB resident memory before returning an error |

The .ppt bug is a recursion that resets its own depth counter. The PDF problem is that PDFs bypass all of anydoc's limits and go straight to pdf-inspector and lopdf, which inflate without bound. Open PR #148 fixes the .ppt bug and several related ones; it has been open since 2026-08-28 with no maintainer response. There is also no time limit on any conversion.

The safety caps are hard-coded and cannot be raised. Issue #156 reports that three of about 3,800 real corporate spreadsheets are wrongly rejected by them.

Practical rule: in-process use is fine for documents you produced or chose. For anything downloaded, run the conversion as a child process with an OS memory limit and a wall-clock timeout, so a crash is a nonzero exit rather than a dead host.

## Code quality

**The Rust core is unusually clean for a four-week-old project, and I verified the test suite and lints locally.**

- `cargo test --locked`: 296 tests pass, 0 fail, 1 ignored (needs a private corpus). Cold build 29 seconds on this machine.
- `cargo clippy -D warnings`: clean. Rustdoc: clean. Zero TODO or FIXME markers.
- `cargo audit`: 0 vulnerabilities. Two warnings, both under the PDF dependency chain: `ttf-parser` is unmaintained with no fix available, and `chacha20 0.10.1` is yanked. The project shipped a known lopdf denial-of-service advisory for its first four releases and fixed it two days after someone reported it. All dependency licenses are permissive.
- The advertised architecture (every format goes through one document model and one Markdown serializer) is real in the code, with one exception: PDF bypasses both and returns pdf-inspector's Markdown directly. So PDF output escaping, tables, and lists differ from the office formats, and `to_document` does not work for PDF.
- One design choice conflicts with your no-silent-fallback rule. Unreadable parts, unusable slides, bad CSV rows, and missing images are skipped with a log message and the conversion still returns success. The Python and Node bindings never wire up that log, so from Python a partial result is indistinguishable from a complete one. Only the Rust crate with a logger installed can see the skips. Hard failures (encrypted, malformed, resource limit, needs OCR) do raise properly.
- The document model is mirrored by hand in six places across the bindings, so forking to extend it is a six-file change.

## Maintenance

**One person writes 91 percent of the code, nobody reviews it, and community contributions are effectively closed.**

- Every merged PR was reviewed only by bots. The 4,400-line Excel parser rewrite merged on bot review alone.
- 45 community PRs are open. Exactly one community PR has ever been merged. The observed pattern is that the maintainer re-implements a contributor's fix in their own commit hours to days later, closes the PR with thanks, and gives no credit in the commit or release notes. Plan to keep any patch of yours in a fork.
- Issue response is fast when it matches what the maintainer is already building and silent otherwise. The last maintainer comment anywhere in issues or PRs is 2026-08-20. Issue #144, a v0.2.4 regression where one image-only page makes a whole PDF convert to nothing, has three confirmations, a community fix, and no maintainer response in five days.
- Breaking changes ship as patch releases: v0.2.1 and v0.2.3 added enum variants and removed a public struct field. Only the error enum is marked non-exhaustive. A community PR proposing the standard fix (#154) is unanswered.
- No CONTRIBUTING, SECURITY, CHANGELOG, roadmap, or deprecation policy exists. Release notes exist only from v0.2.0 on.
- Fourteen releases in 24 days, then a six-day gap. Commit activity comes in bursts with four-to-six-day gaps; the author was active in the main Firecrawl repo on 2026-08-29, so the current quiet reads as split attention, not abandonment.

## Claims versus reality

- The supported-format table is accurate: all 21 extensions route to a real parser. I converted one fixture of every format from a source build; all succeeded.
- "Median conversion under 5 ms" holds by a wide margin for office formats: 0.1 to 2 ms in-process on this M1. The benchmark that produced the number excludes PDFs. The PDF fixture took 6 to 25 ms.
- The benchmark is self-run on a private corpus, judged by one LLM, and dates from v0.1.7. Its harness has a bug that under-reports the `unstructured` competitor on ppt and pptx, which is why those cells show a dash. Treat the table as a hypothesis to test on your own files, not as evidence.
- The README has a syntax error in the Node example, a dead anchor, and a stale number, all from README-only commits made after the last release.
- NeedsOcr fires not only on scanned pages but also on text PDFs with broken font encodings. With hosted OCR on, such a PDF would be uploaded.

## Fit for you

**The Python package is a good technical fit. The bundled skill and its installer are not.**

Python package:

- Fully typed (`py.typed`, hand-written stubs checked by a test), one exception subclass per error variant under `anydoc.ConvertError`, releases the GIL around every conversion. A cp310-abi3 macOS arm64 wheel exists and your mise Python 3.14 accepts it.
- The distribution name is `firecrawl-anydoc` but the import is `anydoc`. The bare PyPI name `anydoc` is an unrelated 2023 package; write the dependency as `firecrawl-anydoc`.
- The `Block` and `Inline` classes use a `kind` field with every payload field optional, so a type checker will not narrow by kind. Expect explicit None checks.

Command-line tool: one file per call, stdin support, four documented exit codes, one-line stderr, never prompts. Good shape for agent tool use. No batch mode. Needs Node 20 or newer; you have 24.

Coverage gaps that matter for document-to-Markdown-for-agents work: no HTML or MHTML, no .eml or .msg, no images or local OCR, no per-page PDF output or page numbers, embedded images become bare alt text, and Word headers and footers are dropped entirely. Issue #132 about headers and footers shows as closed and completed, but the reporter closed it themselves and no code landed. A PDF-heavy workflow still needs a page-aware PDF tool such as pymupdf or pdfplumber alongside this.

The agent skill (`skills/convert-documents-to-markdown/SKILL.md`): rules 1 through 4 and 6 are accurate and worth keeping. Two rules conflict with your charter and repo layout. It runs `npx -y @firecrawl/anydoc` unpinned, so every agent session executes whatever version is latest on npm. Rule 5 routes exit code 3 to the hosted upload with no human decision. Under your charter this is an install of third-party contract text that wields an irreversible tool, so it is gated. Separately, the recommended installer (`npx skills add ... -g`) writes its canonical copy to `~/.agents/skills/<name>` and a symlink into `~/.claude/skills/`, which would drop an untracked directory into your repo working tree and a foreign symlink your sync script would flag.

## Recommended adoption shape

1. Python: `uv add firecrawl-anydoc==0.2.4` with an exact pin. Keep the default `ocr="reject"`. Catch `NeedsOcrError` and `ResourceLimitError` separately and route those files elsewhere. Never set `FIRECRAWL_API_KEY` in an agent environment.
2. Agents: install the CLI once at a pinned version (`npm install -g @firecrawl/anydoc@0.2.4` under mise Node, or `npx -y @firecrawl/anydoc@0.2.4`), one file per call, output to a scratch path.
3. Skill: hand-author one on a branch in `~/.agents/skills/`, keeping rules 1 through 4 and 6, replacing rule 5 with "exit 3 means stop and report the pages that need OCR; never rerun with `--ocr hosted`", adding a non-use boundary for HTML, email, images, and scanned PDFs, and noting that headers and footers are not extracted. Deliver it with `scripts/claude-skills-sync.sh --link`.
4. Untrusted files: subprocess with a memory cap and a timeout. Wait for PR #148 or its equivalent before trusting .ppt in-process.
5. Upgrades: wait a day or two after each tag (v0.2.2 was a same-day hotfix of v0.2.1), read `.github/releases/<tag>.md`, and expect compile breaks if you match on the model enums.

## What was checked and what was not

Checked: a full clone at 261fc25; eight parallel review agents (claims, privacy and egress, supply chain, parser robustness, maintenance, code quality, fit, and a build-and-run proof) whose findings were adversarially verified where the run got that far (nine verdicts, none refuted, before I stopped the run at your request); my own reruns of `cargo test`, `cargo audit`, `cargo deny`, and both crash reproductions; live GitHub, npm, PyPI, and crates.io state as of 2026-09-01.

Not checked: the prebuilt npm and PyPI binaries were not installed or executed (everything ran from a source build); Firecrawl's actual retention behavior for keyless Parse uploads could not be verified beyond their public pages; the launch channel behind the star count could not be verified (Hacker News rate-limited the check); Windows behavior; the pdf-inspector crate's own code beyond its dependency tree.

The raw agent outputs, the privacy wire capture, and the crash-reproduction crate were session scratchpad artifacts and are not kept; the reproduction recipe is in the "Safety against hostile files" section (nested 0x03F0 records in a PowerPoint Document OLE stream; one FlateDecode stream inflating to 1 GiB). Outcome: the local skill `skills/document-to-markdown` (commit 4124286) and the ledger entry of the same date in `docs/agents/contract-decisions.md`.
