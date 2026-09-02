---
name: document-to-markdown
description: "Use when a task needs the text of a Word, PowerPoint, Excel, OpenDocument, RTF, EPUB, CSV, or text-based PDF file you cannot read directly, converted locally to Markdown with a pinned anydoc CLI and never uploaded. Do not use for HTML or MHTML, email (.eml, .msg), images, scanned PDFs, or creating or editing documents."
---

# Document To Markdown

Convert one office document, spreadsheet, presentation, ebook, or text-based PDF to GitHub-Flavored Markdown on this machine, using the anydoc command-line tool at a pinned version, so you can read its contents. Nothing leaves the machine. Invoke as `/document-to-markdown <file>` or `$document-to-markdown <file>`.

## Use When

- A task needs the contents of a `.doc`, `.docx`, `.docm`, `.ppt`, `.pps`, `.pot`, `.pptx`, `.pptm`, `.ppsx`, `.ppsm`, `.xls`, `.xlsx`, `.xlsm`, `.xlsb`, `.odt`, `.ods`, `.odp`, `.rtf`, `.epub`, `.csv`, or `.pdf` file.
- The user asks to read, open, extract the text of, or convert to Markdown such a file.

## Do Not Use When

- The file is HTML or MHTML, an email (`.eml`, `.msg`), or an image. anydoc does not read these; say so and take another route.
- The PDF is scanned or image-only. anydoc cannot read it, and this skill never sends it anywhere; see exit code 3 below.
- The task needs page numbers, per-page text, or the images inside a PDF. Use a page-aware PDF tool instead (the runtime's `pdf` skill where available).
- The task is to create or edit a document.

## Pinned Tool

Version `0.2.4` of the npm package `@firecrawl/anydoc`. This line is the only place the version is written; bump it here after re-vetting the release.

Resolve the command in this order:

1. `anydoc` on `PATH` (installed once with `npm install -g @firecrawl/anydoc@0.2.4`), when `anydoc --version` prints `0.2.4`.
2. Otherwise `npx -y @firecrawl/anydoc@0.2.4`. Needs Node 20 or newer. The first run downloads the package and a platform binary of about 7 MB from the npm registry into npm's cache; offline, that fails with a nonzero exit, which you report.

Never run the unpinned form `npx @firecrawl/anydoc`; it executes whatever version is newest on npm at that moment.

## Run

Announce one setup line before converting: `Converting <file> locally with anydoc 0.2.4 (no upload) → <output path>`.

```bash
<anydoc> <file> --ocr reject -o <scratch>/<basename>.md
```

- `<scratch>` is the session scratch directory when the harness names one, else `mktemp -d`. Never write next to the source file.
- Run it through the shell tool with a timeout of about two minutes. The converter is its own process, so a crash or hang ends that process, not the session.
- One document per call. For several files, loop and report each outcome.
- Pass `--format <name>` only when detection cannot work: CSV read from stdin (`<anydoc> - --format csv < file`), or a file whose extension is missing or wrong. Names: `doc`, `docx`, `odt`, `pdf`, `ppt`, `pptx`, `rtf`, `epub`, `xlsx`, `ods`, `odp`, `csv`.
- Then read the parts of the Markdown the task needs, using offsets for a large file, instead of loading the whole file into context.

## Exit Codes And Stops

The CLI never prompts. On failure it prints one `anydoc: <message>` line to stderr.

| Exit | Meaning | What to do |
| --- | --- | --- |
| 0 | Converted | Read the output. Mention any known gap below that applies to this format. |
| 1 | Not readable or not convertible (malformed, encrypted, unsupported, resource limit) | Report the stderr line. Do not retry with other flags. |
| 2 | Usage error | Fix the command. |
| 3 | Pages need OCR | Stop. Report the page list from the stderr line. Do not rerun with `--ocr hosted`. |
| 128 or higher, or killed by the timeout | The converter crashed or hung on this file | Report that anydoc crashed on the file. Do not retry. Treat the file as untrusted. |

Never upload. `--ocr hosted` sends the entire document and its filename to Firecrawl's servers. Do not pass it, do not set or read `FIRECRAWL_API_KEY` or `FIRECRAWL_API_URL`, and do not offer it as a retry. If the user wants OCR, that is their decision to make with a different tool: say so and stop.

## Known Gaps

Tell the user when one of these applies to the file at hand:

- Word: headers and footers are not extracted, so letterheads, running titles, and footer references are absent.
- All formats: embedded images appear only as their alt text; no image files are produced.
- PDF: text only, with no page numbers or page boundaries; tables and list markers may flatten; a PDF with a broken font encoding can be reported as needing OCR.
- Legacy `.ppt`: tables flatten into paragraphs. `.odp`: nested list items carry a stray leading dash.
- Spreadsheets: a sheet with one cell far from the others, or padded with blank cells to the last row, can hit a fixed resource limit and fail with exit 1 even though it opens in Excel.
- Silent skips: an unreadable slide, row, or part is dropped with no error. When output looks incomplete, say it may be, rather than presenting it as the whole document.

## In A Codebase

When the task is code rather than a one-off read, prefer the library over the CLI, with an exact pin and OCR rejected: Python `firecrawl-anydoc==0.2.4` (`import anydoc`; the default is `ocr="reject"`; catch `NeedsOcrError` and `ResourceLimitError` separately), Node `"@firecrawl/anydoc": "0.2.4"` with no caret, Rust `anydoc = "=0.2.4"`. Convert untrusted files in a child process with a timeout.

## Report

Close with the output path and size for each file, the exit outcome, and the known gaps that apply. Do not paste the whole Markdown into the reply.
