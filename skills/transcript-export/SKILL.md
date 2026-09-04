---
name: transcript-export
description: "Use when JP wants to export, save, reconstruct, or share a Codex or Claude session transcript as Markdown, including full-session exports, subsection exports bounded by messages or line numbers, conversation-only transcripts, hybrid transcripts, or technical transcripts with tool calls and outputs. Do not use for ordinary summarization unless JP asks for a saved transcript file."
---

# Transcript Export

Export a Codex or Claude session transcript into a Markdown file with the provider, range, and detail level JP actually wants.

Use `scripts/export_transcript.py` for these steps, which are easy to get wrong by hand: resolving the JSONL session, detecting the provider, selecting the requested range, filtering duplicate/runtime-only records, and formatting the transcript.

## Before You Start

If JP already specifies the provider, range, detail level, and output path, proceed without another question.

If any of those choices are missing, ask only for the missing decision, briefly:

- Provider: `auto`, `codex`, or `claude`. Default to `auto` unless the source is ambiguous.
- Range: full session; subsection from message/phrase/line A to message/phrase/line B; from message/phrase/line A through the current end.
- Detail: conversation-only; hybrid; full technical.
- Output: use JP's supplied path, or propose `/Users/jp/Laboratory/inbox/<short-slug>-transcript.md` when no destination is given.

Do not make JP reconstruct implementation details. If he says "from the Haley text through the commit message," translate that into marker strings or line numbers yourself after inspecting the raw session file.

## Detail Levels

- Conversation-only: visible user messages and visible assistant messages. Omit tool calls, tool outputs, injected skill bodies, AGENTS/environment payloads, duplicate event mirrors, session metadata, hook/status records, and hidden reasoning/thinking blocks.
- Hybrid: conversation-only transcript plus brief tool-call and tool-output summaries so JP can see what work happened without including every byte of command output.
- Full technical: visible conversation plus provider tool calls, tool arguments, and full tool outputs. For Codex, include supported function/custom/tool-search call records and outputs. For Claude, include assistant `tool_use` blocks and user `tool_result` blocks. Still omit hidden reasoning/thinking records, encrypted reasoning content, duplicate event mirrors, repeated session metadata, hook/status records, turn-context instruction blobs, and injected skill/AGENTS/environment payloads unless JP explicitly asks for raw JSONL and the applicable policy permits it.

## Session And Range Discovery

Prefer exact source discovery over guessing.

Use one of these ways:

- If the thread id or JSONL path is known, pass `--thread-id <id>` or `--session-file <path>`.
- If JP names boundary text, search `~/.codex/sessions` and `~/.claude/projects` with `rg` to find the JSONL file, then pass `--contains`, `--provider`, and marker arguments to the script.
- If exporting the current session and no boundary text is available, identify the current thread/session through the app/thread tooling when available. If multiple candidate JSONL files remain, show the candidate filenames and ask JP to choose.

Provider source roots:

- Codex: `~/.codex/sessions/**/*.jsonl`
- Claude: `~/.claude/projects/**/*.jsonl`

Common commands:

```bash
/Users/jp/.agents/skills/transcript-export/scripts/export_transcript.py \
  --session-file /path/to/rollout.jsonl \
  --provider auto \
  --mode conversation \
  --output /Users/jp/Laboratory/inbox/session-transcript.md
```

```bash
/Users/jp/.agents/skills/transcript-export/scripts/export_transcript.py \
  --provider codex \
  --contains "I am interested in exploring how a reframing skill could be designed" \
  --start-marker "I am interested in exploring how a reframing skill could be designed" \
  --end-marker "Implemented `reality-check` under `/Users/jp/.agents/skills/` and committed it locally." \
  --mode technical \
  --output /Users/jp/Laboratory/inbox/reality-check-skill-transcript.md
```

```bash
/Users/jp/.agents/skills/transcript-export/scripts/export_transcript.py \
  --provider codex \
  --thread-id 019f23e7-1b78-76c1-92c2-0c731af2c4ea \
  --start-line 1057 \
  --end-line 1453 \
  --mode hybrid \
  --output /Users/jp/Laboratory/inbox/reality-check-hybrid-transcript.md
```

```bash
/Users/jp/.agents/skills/transcript-export/scripts/export_transcript.py \
  --provider claude \
  --session-file /Users/jp/.claude/projects/-Users-jp--agents/<session-id>.jsonl \
  --start-marker "I actually did a real `outcome-shaping` run" \
  --mode hybrid \
  --output /Users/jp/Laboratory/inbox/claude-session-hybrid-transcript.md
```

## Verification

After writing the transcript:

- Confirm the output file exists and report its line/byte count.
- If boundary markers were used, verify the start and end markers are present.
- Inspect the first and last visible sections to make sure the export starts and stops at the intended place.
- If there is a known later message that must not be included, verify it is absent.

In the final response, state the output path, provider, source JSONL path, line range exported, detail level, and proof checks run. If the output path is inside a git worktree whose rules require committing generated Markdown, follow that repo's commit rules; otherwise do not invent a commit step.
