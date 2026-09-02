---
name: document-to-markdown
description: "Use when a task needs the text, structure, or embedded images of a Word, PowerPoint, Excel, OpenDocument, RTF, or EPUB file, a CSV, or the text of a text-based PDF, converted locally to Markdown with a pinned anydoc build and never uploaded. For read-only tasks this comes before the runtime's document-authoring skills (docx, pptx, xlsx, pdf), which own creating and editing. Do not use for HTML or MHTML, email (.eml, .msg), image files, scanned PDFs, per-page or per-slide questions, or creating or editing documents."
---

# Document To Markdown

Convert one office document, spreadsheet, presentation, ebook, or text-based PDF to GitHub-Flavored Markdown on this machine, using the anydoc command-line tool at a pinned version, so you can read its contents. When the task needs the pictures inside an office file, or structure the Markdown flattened, a second path runs the anydoc Python library at the same pinned version to write the embedded assets and the document model. Nothing leaves the machine on either path. Invoke as `/document-to-markdown <file>` or `$document-to-markdown <file>`.

## Use When

- A task needs the contents of a `.doc`, `.docx`, `.docm`, `.dotx`, `.ppt`, `.pps`, `.pot`, `.pptx`, `.pptm`, `.ppsx`, `.ppsm`, `.potx`, `.xls`, `.xlsx`, `.xlsm`, `.xlsb`, `.xltx`, `.odt`, `.ods`, `.odp`, `.rtf`, `.epub`, `.csv`, or `.pdf` file.
- The user asks to read, open, extract the text of, or convert to Markdown such a file.
- The task only reads the file. The runtime's document-authoring skills claim reading too (on Claude Code `docx`, `pptx`, `xlsx`, and `pdf`; on Codex the bundled `pdf`); for a read-only task this skill comes first, because it runs a pinned local converter with no upload path. They own creating and editing.
- A `.csv` or other delimited text file only when the task wants it rendered as a Markdown table; the runtime reads plain text directly.

## Do Not Use When

- The file is HTML or MHTML, an email (`.eml`, `.msg`), or an image. anydoc does not read these; say so and take another route.
- The PDF is scanned or image-only. anydoc cannot read it, and this skill never sends it anywhere; see exit code 3 and the PDF known gap below.
- The task needs page numbers, per-page text, or the images inside a PDF. Use a page-aware tool instead: on Claude Code the Read tool renders PDF pages locally (pass a `pages` range) and the `pdf` skill covers the rest; on Codex the bundled `pdf` skill, where available.
- The task needs slide numbers or the text of one slide. anydoc does not mark slides (see Known Gaps); use the runtime's presentation skill where available (Claude Code: `pptx`), which keeps slide markers.
- The task is to create or edit a document.

## Pinned Tool

Version `0.2.4` of anydoc, as the npm package `@firecrawl/anydoc` for the Markdown path and the PyPI package `firecrawl-anydoc` for the library path. The version appears in every command and pin in this file (this line, both resolution steps, the setup line, the library sentence, and In A Codebase) and in the `dependencies` line at the top of `scripts/anydoc_extract.py`; a bump changes all of them, so grep for the old version after editing.

The baseline for this pin is the vet report `docs/reviews/2026-09-01-anydoc-vet.md` in the `~/.agents` repo. Before bumping, re-vet the release against it: read the release notes for breaking changes (they have shipped in patch releases), confirm the two known crash cases (a crafted `.ppt` with deeply nested records; a crafted PDF with one highly compressible stream) are no worse, and confirm the OCR default is still `reject`. The mechanics of the bump belong to `dependency-upgrade` where available, plus the repo's validation ladder.

Resolve the command in this order:

1. `anydoc` on `PATH` (installed once with `npm install -g @firecrawl/anydoc@0.2.4`), when `anydoc --version` prints `0.2.4`.
2. Otherwise `npx -y @firecrawl/anydoc@0.2.4`. Needs Node 20 or newer. The first run downloads the package and a platform binary of about 7 MB from the npm registry into npm's cache; offline, that fails with a nonzero exit, which you report.

Never run the unpinned form `npx @firecrawl/anydoc`; it executes whatever version is newest on npm at that moment.

## Run

Announce one setup line before converting: `Converting <file> locally with anydoc 0.2.4 (no upload) → <output path>`.

```bash
<timeout> <anydoc> <file> --ocr reject -o <scratch>/<file name>.md
```

- `<scratch>` is the session scratch directory when the harness names one, else `mktemp -d`. Never write next to the source file unasked.
- `<file name>` is the source file's name with its extension (`report.docx` becomes `report.docx.md`), so two sources that share a stem never share an output. Do not reuse an output path in a session: if it already exists, add a numeric suffix and say so.
- `<timeout>` is `timeout 120` when that command exists (GNU coreutils: standard on Linux, Homebrew on macOS at `/opt/homebrew/bin/timeout`, absent from stock macOS), which kills the converter after two minutes with exit 124. When it is absent, leave `<timeout>` empty and set the shell tool's own timeout to about two minutes, knowing that Claude Code's shell tool may move a timed-out command to the background instead of killing it: then no exit code arrives, so stop the background task by the id the tool reports and treat the file as hung. The converter is its own process, so a crash cannot take the session down, but a hang does not end by itself.
- The timeout is the only guard a shell gives you on macOS; there is no reliable per-process memory cap. A crafted PDF has reached about 4 GB of memory before failing, and an out-of-memory kill arrives as exit 137. For a downloaded or otherwise untrusted file, say so before converting.
- One document per anydoc call. For several files, run one shell call per file so the timeout applies per file, print `<file>: exit <n>` after each conversion, and keep going after a failure; the report lists every file with its outcome.
- Detection reads the file content first; the extension matters only for CSV and other delimited text (`.tsv`, `.txt`), which carry no signature and need `--format csv` (the parser detects the delimiter). Stdin needs it for CSV too (`<anydoc> - --format csv < file`). Do not pass `--format` for a container whose extension is wrong or missing: content detection handles it, and an explicit wrong `--format` breaks a conversion that would have worked. Names: `doc`, `docx`, `odt`, `pdf`, `ppt`, `pptx`, `rtf`, `epub`, `xlsx`, `ods`, `odp`, `csv`; the CLI also accepts extension aliases such as `xls`.
- Then read the parts of the Markdown the task needs, using offsets for a large file, instead of loading the whole file into context.
- When the user asks for the Markdown itself or names a destination, still convert into `<scratch>`, then copy the finished file (and the model directory when it ran) to the path the user named. When the request is a deliverable and no destination was named, ask for one. The scratch rule stops unasked writes into the user's tree; it does not bar a destination the user chose.

## Images And The Document Model

Use this second path when the task needs the pictures embedded in the file, or when the Markdown flattened something the task depends on (a merged-cell table, footnotes, list numbering, which paragraph is a heading). It is not a substitute for the Markdown path, and it does not work for PDF, which has no document model.

```bash
uv run <skill dir>/scripts/anydoc_extract.py <file> <scratch>/<file name>-model [--format <name>]
```

- `<skill dir>` is this skill's directory, given when the skill loads: Claude Code prints it as `Base directory for this skill` (also available as `${CLAUDE_SKILL_DIR}`); Codex lists it as the `(file: .../document-to-markdown/SKILL.md)` entry, expanded through its skill roots table. In this library it resolves to `~/.agents/skills/document-to-markdown`.
- The script runs the pinned `firecrawl-anydoc==0.2.4` library through `uv`. The first run downloads a wheel of about 3 MB from PyPI into uv's cache; offline, that fails with a nonzero exit, which you report.
- It writes `assets/<file name>-<id>.<ext>` for every embedded image or object (`report.docx-0.png`; an SVG gets `.svg`, a non-image object `.bin`), and `document.json`: the whole model as nested objects, each showing only the fields its `kind` uses, with image inlines pointing at assets by `asset_id`.
- It refuses an output directory that already holds files (exit 2), so a re-run never mixes one document's assets with another's; give each run its own directory.
- It prints a summary: top-level block counts, note and asset counts, and one line per asset with its media type, size, and path. Read `document.json` selectively; it is larger than the Markdown.
- Same setup line, scratch rule, timeout, and one-file-per-call rule as the Markdown path. Its failures print one `anydoc-extract: <message>` line and exit 1 (the document could not be read or parsed, PDF included, or an output file could not be written) or 2 (usage: missing arguments, an unknown `--format` name, an output path that is not a directory, or a non-empty output directory). It never exits 3: a PDF is refused before parsing, so the OCR check never runs here.
- The library call this path uses has no OCR option and no network path at all, so no upload is possible here even by mistake.

## Exit Codes And Stops

Apply the table only when stderr carries an `anydoc:` line (CLI) or an `anydoc-extract:` line (script). Any other nonzero exit is the launcher or toolchain, not a verdict on the document: npx could not reach the registry or write its cache (a sandbox that blocks writes outside the workspace does this on Codex), Node found no native binding for the platform, uv could not fetch the wheel (uv exits 2), or the command is not on `PATH` (exit 127). Report it as a toolchain failure with the stderr, and do not treat the file as unreadable.

The CLI never prompts. On failure it prints one `anydoc: <message>` line to stderr and writes no output file.

| Exit | Meaning | What to do |
| --- | --- | --- |
| 0 | Converted | Read the output. Mention any known gap below that applies to this format. |
| 1 | Not readable or not convertible (malformed, encrypted, unsupported, resource limit) | Report the stderr line. Do not retry with other flags. Exception: `unrecognized file content and extension` on a delimited text file (`.tsv`, `.txt`): rerun once with `--format csv`. |
| 2 | Usage error | Fix the command. |
| 3 | Pages need OCR (reported for some documents only; see the PDF known gap) | Stop. Report the page list from the stderr line. Do not rerun with `--ocr hosted`. |
| 124 | Killed by `timeout` | Report that anydoc hung on the file. Do not retry on either path. Treat the file as untrusted: name it as such in the report and do not open it with another in-process parser. |
| 128 or higher (134 crash, 137 out of memory), or a hang the shell tool backgrounded | The converter crashed or hung on this file | Report that anydoc crashed or hung on the file. Do not retry on either path. Treat the file as untrusted: name it as such in the report and do not open it with another in-process parser. |

Never upload. `--ocr hosted` sends the entire document and its filename to Firecrawl's servers. Do not pass it, do not set or read `FIRECRAWL_API_KEY` or `FIRECRAWL_API_URL`, and do not offer it as a retry. If the user wants OCR, that is their decision to make with a different tool: say so and stop. Where the runtime can show or read the pages locally, say that too: on Claude Code the Read tool renders PDF pages as images (pass a `pages` range) and the `pdf` skill offers local OCR with pytesseract on rendered pages; on Codex the bundled `pdf` skill renders pages with `pdftoppm` for viewing, where available. None of these sends the file anywhere.

## Known Gaps

Tell the user when one of these applies to the file at hand:

- Word: headers and footers are not extracted, so letterheads, running titles, and footer references are absent.
- All formats: in the Markdown, embedded images appear only as their alt text. The library path above writes the image files; for PDF there is no way to get them.
- PDF: text only, with no page numbers or page boundaries; tables and list markers may flatten; a PDF with a broken font encoding can be reported as needing OCR. Exit 3 is not exhaustive: a PDF that mixes text pages with scanned pages is often converted with exit 0 and the scanned pages dropped with no diagnostic. When a PDF may hold scanned pages (signature pages, exhibits, appendices), say the output may be missing pages, or compare the page count with a page-aware tool.
- Presentations (`.ppt`, `.pptx`, `.odp`): slides are not marked. The Markdown and the model run all slides together with no slide numbers or boundaries; slide titles are plain paragraphs, and speaker notes are block quotes after each slide's text.
- Legacy `.ppt`: tables flatten into paragraphs. `.odp`: nested list items carry a stray leading dash.
- Spreadsheets: a sheet with one cell far from the others, or padded with blank cells to the last row, can hit a fixed resource limit and fail with exit 1 even though it opens in Excel.
- Silent skips: an unreadable slide, row, or part is dropped with no error. When output looks incomplete, say it may be, rather than presenting it as the whole document.

## In A Codebase

When the task is code rather than a one-off read, prefer the library over the CLI, with an exact pin and OCR rejected: Python `firecrawl-anydoc==0.2.4` (`import anydoc`; the default is `ocr="reject"`; catch `NeedsOcrError` and `ResourceLimitError` separately, and do not treat the absence of `NeedsOcrError` as proof that every page was read), Node `"@firecrawl/anydoc": "0.2.4"` with no caret, Rust `anydoc = "=0.2.4"`. Convert untrusted files in a child process with a memory limit and a timeout; a crafted PDF has reached about 4 GB, and no conversion has a built-in time limit.

## Report

Close with the output path and size for each file, the exit outcome, and the known gaps that apply. When the library path ran, add the assets directory with its file count and the `document.json` path. Say that scratch output may not outlive the session, and give the copied path when one was made. Do not paste the whole Markdown or the JSON into the reply.
