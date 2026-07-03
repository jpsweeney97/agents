#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Sequence


Mode = Literal["conversation", "hybrid", "technical"]
Provider = Literal["auto", "codex", "claude"]
ResolvedProvider = Literal["codex", "claude"]

SKIPPED_USER_PREFIXES = (
    "<skill>",
    "<environment_context>",
    "<permissions instructions>",
    "<app-context>",
    "<collaboration_mode>",
    "<apps_instructions>",
    "<skills_instructions>",
    "<plugins_instructions>",
    "## Memory",
    "========= MEMORY_SUMMARY BEGINS",
    "# AGENTS.md instructions for ",
    "Base directory for this skill:",
)


@dataclass(frozen=True)
class Record:
    """A parsed JSONL session row."""

    line_no: int
    timestamp: str
    record_type: str
    payload: dict[str, Any]
    raw: str


@dataclass(frozen=True)
class ExportPlan:
    """Resolved transcript export parameters."""

    source: Path
    provider: ResolvedProvider
    start_line: int
    end_line: int
    mode: Mode
    output: Path
    title: str


def fail(operation: str, reason: str, got: object) -> None:
    """Exit with the repo-standard failure message shape."""

    print(f"{operation} failed: {reason}. Got: {got!r:.100}", file=sys.stderr)
    raise SystemExit(1)


def load_records(path: Path) -> list[Record]:
    """Load a JSONL session file."""

    if not path.exists():
        fail("load session", "file does not exist", str(path))
    records: list[Record] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw_line in enumerate(handle, 1):
            raw = raw_line.rstrip("\n")
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                fail("parse session", f"invalid JSON on line {line_no}: {exc}", raw[:200])
            if not isinstance(obj, dict):
                fail("parse session", f"expected JSON object on line {line_no}", obj)
            records.append(
                Record(
                    line_no=line_no,
                    timestamp=str(obj.get("timestamp", "")),
                    record_type=str(obj.get("type", "")),
                    payload=obj,
                    raw=raw,
                )
            )
    if not records:
        fail("load session", "no records found", str(path))
    return records


def codex_root() -> Path:
    """Return the default Codex session-log root."""

    return Path.home() / ".codex" / "sessions"


def claude_root() -> Path:
    """Return the default Claude project-log root."""

    return Path.home() / ".claude" / "projects"


def candidate_roots(provider: Provider) -> list[Path]:
    """Return provider roots to search."""

    if provider == "codex":
        return [codex_root()]
    if provider == "claude":
        return [claude_root()]
    return [codex_root(), claude_root()]


def iter_session_files(provider: Provider) -> list[Path]:
    """List local session JSONL files newest first."""

    files: list[Path] = []
    for root in candidate_roots(provider):
        if root.exists():
            files.extend(path for path in root.rglob("*.jsonl") if path.is_file())
    if not files:
        fail("resolve session", "no session JSONL files found for provider", provider)
    return sorted(files, key=lambda path: path.stat().st_mtime, reverse=True)


def recursively_collect_text(value: Any) -> list[str]:
    """Collect string leaves from a parsed JSON value."""

    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        texts: list[str] = []
        for item in value:
            texts.extend(recursively_collect_text(item))
        return texts
    if isinstance(value, dict):
        texts = []
        for item in value.values():
            texts.extend(recursively_collect_text(item))
        return texts
    return []


def decoded_text_contains(path: Path, needles: Sequence[str]) -> bool:
    """Return whether all needles appear in the file's raw or decoded text."""

    remaining = set(needles)
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            matched = {needle for needle in remaining if needle in raw_line}
            remaining -= matched
            if not remaining:
                return True
            try:
                obj = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            joined_text = "\n".join(recursively_collect_text(obj))
            matched = {needle for needle in remaining if needle in joined_text}
            remaining -= matched
            if not remaining:
                return True
    return not remaining


def resolve_session_file(args: argparse.Namespace) -> Path:
    """Resolve the session file requested by CLI arguments."""

    session_file = args.session_file
    if session_file is not None:
        return Path(session_file).expanduser().resolve()

    provider: Provider = args.provider
    if args.thread_id:
        files = iter_session_files(provider)
        matches = [path for path in files if args.thread_id in path.name]
        if not matches:
            matches = [path for path in files if decoded_text_contains(path, [args.thread_id])]
        if len(matches) == 1:
            return matches[0]
        if not matches:
            fail("resolve session", "no session file matched thread id", args.thread_id)
        fail("resolve session", "multiple session files matched thread id", [str(path) for path in matches[:10]])

    contains = list(args.contains or [])
    if args.start_marker:
        contains.append(args.start_marker)
    if args.end_marker:
        contains.append(args.end_marker)
    if contains:
        matches = [path for path in iter_session_files(provider) if decoded_text_contains(path, contains)]
        if len(matches) == 1 or (matches and args.latest_match):
            return matches[0]
        if not matches:
            fail("resolve session", "no session file contained all marker text", contains)
        fail(
            "resolve session",
            "multiple session files contained the marker text; rerun with --session-file or --latest-match",
            [str(path) for path in matches[:10]],
        )

    if args.latest:
        return iter_session_files(provider)[0]

    fail("resolve session", "provide --session-file, --thread-id, --contains, or --latest", vars(args))


def detect_provider(path: Path, records: Sequence[Record], requested: Provider) -> ResolvedProvider:
    """Resolve the provider for a session file."""

    if requested != "auto":
        return requested
    path_text = str(path)
    if "/.codex/sessions/" in path_text:
        return "codex"
    if "/.claude/projects/" in path_text:
        return "claude"
    record_types = {record.record_type for record in records[:30]}
    if record_types & {"response_item", "event_msg", "session_meta", "turn_context"}:
        return "codex"
    if record_types & {"assistant", "user", "attachment", "system", "last-prompt", "mode", "permission-mode"}:
        return "claude"
    fail("detect provider", "could not infer provider; pass --provider codex or --provider claude", path_text)


def codex_payload(record: Record) -> dict[str, Any]:
    """Return a Codex payload, normalizing missing payload to an empty object."""

    payload = record.payload.get("payload", {})
    return payload if isinstance(payload, dict) else {}


def codex_kind(record: Record) -> str:
    """Return the logical payload kind for a Codex record."""

    payload = codex_payload(record)
    value = payload.get("type") if record.record_type == "response_item" else record.record_type
    return str(value or "")


def extract_codex_message_text(record: Record) -> str:
    """Extract concatenated text from a Codex message payload."""

    content = codex_payload(record).get("content", [])
    if not isinstance(content, list):
        return ""
    texts: list[str] = []
    for part in content:
        if isinstance(part, str):
            texts.append(part)
        elif isinstance(part, dict):
            for key in ("text", "input_text", "output_text"):
                value = part.get(key)
                if isinstance(value, str):
                    texts.append(value)
                    break
    return "\n".join(texts).rstrip()


def is_codex_message(record: Record) -> bool:
    """Return whether the Codex record is a chat message item."""

    return record.record_type == "response_item" and codex_kind(record) == "message"


def is_visible_codex_message(record: Record) -> bool:
    """Return whether a Codex message should appear by default."""

    if not is_codex_message(record):
        return False
    payload = codex_payload(record)
    role = payload.get("role")
    if role == "assistant":
        return True
    if role != "user":
        return False
    text = extract_codex_message_text(record).lstrip()
    return not any(text.startswith(prefix) for prefix in SKIPPED_USER_PREFIXES)


def claude_message(record: Record) -> dict[str, Any]:
    """Return a Claude message object from a record."""

    message = record.payload.get("message", {})
    return message if isinstance(message, dict) else {}


def claude_content(record: Record) -> Any:
    """Return Claude message content."""

    return claude_message(record).get("content")


def claude_content_blocks(record: Record) -> list[dict[str, Any]]:
    """Return Claude content blocks when content is a list."""

    content = claude_content(record)
    if not isinstance(content, list):
        return []
    return [part for part in content if isinstance(part, dict)]


def extract_claude_text(record: Record) -> str:
    """Extract visible text blocks from a Claude message record."""

    content = claude_content(record)
    if isinstance(content, str):
        return content.rstrip()
    texts = [str(part.get("text", "")) for part in claude_content_blocks(record) if part.get("type") == "text" and part.get("text")]
    return "\n".join(texts).rstrip()


def claude_tool_uses(record: Record) -> list[dict[str, Any]]:
    """Return Claude assistant tool_use blocks."""

    if record.record_type != "assistant":
        return []
    return [part for part in claude_content_blocks(record) if part.get("type") == "tool_use"]


def claude_tool_results(record: Record) -> list[dict[str, Any]]:
    """Return Claude user tool_result blocks."""

    if record.record_type != "user":
        return []
    return [part for part in claude_content_blocks(record) if part.get("type") == "tool_result"]


def is_visible_claude_message(record: Record) -> bool:
    """Return whether a Claude message should appear by default."""

    if record.record_type not in {"user", "assistant"}:
        return False
    if record.payload.get("isMeta"):
        return False
    if claude_message(record).get("role") not in {"user", "assistant"}:
        return False
    text = extract_claude_text(record).lstrip()
    if not text:
        return False
    return not any(text.startswith(prefix) for prefix in SKIPPED_USER_PREFIXES)


def is_visible_message(record: Record, provider: ResolvedProvider) -> bool:
    """Return whether a provider record is visible conversation."""

    if provider == "codex":
        return is_visible_codex_message(record)
    return is_visible_claude_message(record)


def marker_score(record: Record, provider: ResolvedProvider) -> int:
    """Prefer visible messages over technical payloads and duplicate mirrors."""

    if is_visible_message(record, provider):
        return 0
    if provider == "codex" and is_codex_message(record):
        return 1
    if provider == "claude" and record.record_type in {"user", "assistant"}:
        return 1
    if record.record_type in {"event_msg", "attachment", "system"}:
        return 4
    return 2


def structured_text(record: Record, provider: ResolvedProvider) -> str:
    """Return parsed text useful for marker matching."""

    if provider == "codex" and is_codex_message(record):
        return extract_codex_message_text(record)
    if provider == "claude":
        return "\n".join(recursively_collect_text(record.payload))
    return ""


def record_contains(record: Record, provider: ResolvedProvider, marker: str) -> bool:
    """Return whether a marker appears in raw or structured record text."""

    return marker in record.raw or marker in structured_text(record, provider)


def find_marker_line(records: Sequence[Record], provider: ResolvedProvider, marker: str, after_line: int) -> int:
    """Find the best matching line for a marker after a line number."""

    candidates = [record for record in records if record.line_no > after_line and record_contains(record, provider, marker)]
    if not candidates:
        fail("resolve range", "marker not found after requested line", {"marker": marker, "after_line": after_line})
    return min(candidates, key=lambda record: (marker_score(record, provider), record.line_no)).line_no


def resolve_range(records: Sequence[Record], provider: ResolvedProvider, args: argparse.Namespace) -> tuple[int, int]:
    """Resolve inclusive start and end line numbers."""

    if args.start_line is not None and args.start_marker is not None:
        fail("resolve range", "provide only one start boundary", {"start_line": args.start_line, "start_marker": args.start_marker})
    if args.end_line is not None and args.end_marker is not None:
        fail("resolve range", "provide only one end boundary", {"end_line": args.end_line, "end_marker": args.end_marker})

    first_line = records[0].line_no
    last_line = records[-1].line_no
    start_line = args.start_line if args.start_line is not None else first_line
    if args.start_marker:
        start_line = find_marker_line(records, provider, args.start_marker, first_line - 1)

    end_line = args.end_line if args.end_line is not None else last_line
    if args.end_marker:
        end_line = find_marker_line(records, provider, args.end_marker, start_line - 1)

    if start_line < first_line or start_line > last_line:
        fail("resolve range", "start line outside session", {"start_line": start_line, "first": first_line, "last": last_line})
    if end_line < first_line or end_line > last_line:
        fail("resolve range", "end line outside session", {"end_line": end_line, "first": first_line, "last": last_line})
    if end_line < start_line:
        fail("resolve range", "end line is before start line", {"start_line": start_line, "end_line": end_line})
    return start_line, end_line


def fence(text: str, lang: str = "") -> str:
    """Create a Markdown fence that cannot be closed by the text."""

    max_run = max((len(match.group(0)) for match in re.finditer(r"`+", text)), default=0)
    ticks = "`" * max(3, max_run + 1)
    return f"{ticks}{lang}\n{text.rstrip()}\n{ticks}\n"


def pretty_json(value: Any) -> str:
    """Format JSON-like data deterministically."""

    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)


def parse_call_arguments(arguments: Any) -> Any:
    """Parse a Codex function-call arguments field when it is JSON."""

    if isinstance(arguments, str):
        try:
            return json.loads(arguments)
        except json.JSONDecodeError:
            return arguments
    return arguments


def summarize_output(output: str) -> str:
    """Summarize a tool output for hybrid transcripts."""

    lines = output.rstrip().splitlines()
    exit_line = next((line for line in lines if "Process exited with code" in line or line.startswith("Exit code ")), None)
    output_marker_index = next((index for index, line in enumerate(lines) if line == "Output:"), None)
    body_lines = lines[output_marker_index + 1 :] if output_marker_index is not None else lines
    preview = "\n".join(body_lines[:18]).strip()
    if len(preview) > 1600:
        preview = preview[:1600].rstrip() + "\n...[truncated]"
    omitted = max(len(body_lines) - 18, 0)
    parts = []
    if exit_line:
        parts.append(exit_line)
    if preview:
        parts.append("Output preview:\n" + preview)
    if omitted:
        parts.append(f"Omitted {omitted} additional output lines in hybrid mode.")
    return "\n\n".join(parts) if parts else "(no output)"


def compact_tool_input(tool_input: Any) -> str:
    """Render compact tool input for hybrid transcripts."""

    if not isinstance(tool_input, dict):
        return fence(pretty_json(tool_input) if not isinstance(tool_input, str) else tool_input)
    summary_lines = []
    for key in ("command", "cmd", "description", "file_path", "path", "cwd", "workdir"):
        if key in tool_input:
            summary_lines.append(f"- `{key}`: `{tool_input[key]}`")
    if summary_lines:
        return "\n".join(summary_lines) + "\n"
    return fence(pretty_json(tool_input), "json")


def render_codex_message(record: Record) -> str:
    """Render a visible Codex chat message."""

    payload = codex_payload(record)
    role = str(payload.get("role", "message")).title()
    phase = payload.get("phase")
    phase_text = f" [{phase}]" if isinstance(phase, str) and phase else ""
    text = extract_codex_message_text(record)
    heading = f"## {role} Message{phase_text} (line {record.line_no}, {record.timestamp})\n"
    return heading + "\n" + text.rstrip() + "\n"


def render_codex_function_call(record: Record, mode: Mode) -> str:
    """Render a Codex function call item."""

    payload = codex_payload(record)
    name = str(payload.get("name", "function_call"))
    call_id = payload.get("call_id", "")
    args = parse_call_arguments(payload.get("arguments", ""))
    heading = f"## Tool Call: {name} (line {record.line_no}, call_id {call_id})\n"
    if mode == "hybrid":
        return heading + "\n" + compact_tool_input(args)
    body = pretty_json(args) if not isinstance(args, str) else args
    language = "json" if not isinstance(args, str) else ""
    return heading + "\n" + fence(body, language)


def render_codex_function_output(record: Record, mode: Mode) -> str:
    """Render a Codex function-call output item."""

    payload = codex_payload(record)
    call_id = payload.get("call_id", "")
    output = str(payload.get("output", ""))
    heading = f"## Tool Output (line {record.line_no}, call_id {call_id})\n"
    body = summarize_output(output) if mode == "hybrid" else output
    return heading + "\n" + fence(body)


def payload_without_internal_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    """Remove internal passthrough metadata from rendered payloads."""

    return {key: value for key, value in payload.items() if key != "internal_chat_message_metadata_passthrough"}


def render_codex_generic_technical(record: Record, mode: Mode) -> str:
    """Render supported non-message Codex technical payloads."""

    kind = codex_kind(record)
    heading = f"## Technical Record: {kind or record.record_type} (line {record.line_no}, {record.timestamp})\n"
    payload = payload_without_internal_metadata(codex_payload(record))
    if mode == "hybrid":
        payload = {key: value for key, value in payload.items() if key in {"type", "name", "call_id", "status"}}
    return heading + "\n" + fence(pretty_json(payload), "json")


def should_render_codex(record: Record, mode: Mode) -> bool:
    """Return whether a Codex record belongs in the requested transcript mode."""

    if is_visible_codex_message(record):
        return True
    if mode == "conversation":
        return False
    kind = codex_kind(record)
    return kind in {
        "function_call",
        "function_call_output",
        "custom_tool_call",
        "custom_tool_call_output",
        "tool_search_call",
        "tool_search_output",
    }


def render_codex_record(record: Record, mode: Mode) -> str:
    """Render one selected Codex record."""

    kind = codex_kind(record)
    if is_visible_codex_message(record):
        return render_codex_message(record)
    if kind == "function_call":
        return render_codex_function_call(record, mode)
    if kind == "function_call_output":
        return render_codex_function_output(record, mode)
    return render_codex_generic_technical(record, mode)


def render_claude_message(record: Record) -> str:
    """Render a visible Claude chat message."""

    role = str(claude_message(record).get("role", record.record_type)).title()
    text = extract_claude_text(record)
    heading = f"## {role} Message (line {record.line_no}, {record.timestamp})\n"
    return heading + "\n" + text.rstrip() + "\n"


def render_claude_tool_use(record: Record, block: dict[str, Any], mode: Mode) -> str:
    """Render a Claude tool_use block."""

    name = str(block.get("name", "tool_use"))
    tool_id = str(block.get("id", ""))
    heading = f"## Tool Call: {name} (line {record.line_no}, id {tool_id})\n"
    tool_input = block.get("input", {})
    if mode == "hybrid":
        return heading + "\n" + compact_tool_input(tool_input)
    return heading + "\n" + fence(pretty_json(tool_input), "json")


def render_claude_tool_result(record: Record, block: dict[str, Any], mode: Mode) -> str:
    """Render a Claude tool_result block."""

    tool_id = str(block.get("tool_use_id", ""))
    content = block.get("content", "")
    if not isinstance(content, str):
        content = pretty_json(content)
    heading = f"## Tool Output (line {record.line_no}, tool_use_id {tool_id})\n"
    body = summarize_output(content) if mode == "hybrid" else content
    return heading + "\n" + fence(body)


def should_render_claude(record: Record, mode: Mode) -> bool:
    """Return whether a Claude record belongs in the requested transcript mode."""

    if is_visible_claude_message(record):
        return True
    if mode == "conversation":
        return False
    return bool(claude_tool_uses(record) or claude_tool_results(record))


def render_claude_record(record: Record, mode: Mode) -> str:
    """Render one selected Claude record."""

    sections: list[str] = []
    if is_visible_claude_message(record):
        sections.append(render_claude_message(record))
    if mode != "conversation":
        sections.extend(render_claude_tool_use(record, block, mode) for block in claude_tool_uses(record))
        sections.extend(render_claude_tool_result(record, block, mode) for block in claude_tool_results(record))
    return "\n".join(section.rstrip() for section in sections if section.strip()) + "\n"


def should_render(record: Record, provider: ResolvedProvider, mode: Mode) -> bool:
    """Return whether a record belongs in the requested transcript mode."""

    if provider == "codex":
        return should_render_codex(record, mode)
    return should_render_claude(record, mode)


def render_record(record: Record, provider: ResolvedProvider, mode: Mode) -> str:
    """Render one selected record."""

    if provider == "codex":
        return render_codex_record(record, mode)
    return render_claude_record(record, mode)


def render_transcript(plan: ExportPlan, records: Sequence[Record]) -> str:
    """Render the complete Markdown transcript."""

    selected = [record for record in records if plan.start_line <= record.line_no <= plan.end_line]
    rendered = [render_record(record, plan.provider, plan.mode) for record in selected if should_render(record, plan.provider, plan.mode)]
    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    omitted_note = (
        "Conversation-only includes visible user and assistant messages. "
        "Hybrid adds compact tool summaries. Full technical adds full tool calls and outputs. "
        "All modes omit hidden reasoning/thinking, encrypted reasoning content, duplicate event mirrors, session metadata, hook/status records, turn-context instruction blobs, and injected skill/AGENTS/environment payloads by default."
    )
    header = [
        f"# {plan.title}",
        "",
        f"- Provider: `{plan.provider}`",
        f"- Source JSONL: `{plan.source}`",
        f"- Line range: `{plan.start_line}-{plan.end_line}`",
        f"- Detail level: `{plan.mode}`",
        f"- Generated: `{generated}`",
        f"- Export note: {omitted_note}",
        "",
    ]
    if not rendered:
        rendered = ["_No records matched the requested transcript mode in this range._\n"]
    return "\n".join(header + rendered)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(description="Export a Codex or Claude JSONL session transcript to Markdown.")
    source = parser.add_argument_group("source")
    source.add_argument("--provider", choices=["auto", "codex", "claude"], default="auto", help="Transcript provider. Defaults to auto-detect.")
    source.add_argument("--session-file", type=Path, help="Exact JSONL session file to export.")
    source.add_argument("--thread-id", help="Codex thread id, Claude session id, or id contained in the rollout filename.")
    source.add_argument("--contains", action="append", help="Text that must appear in the session file; repeatable.")
    source.add_argument("--latest", action="store_true", help="Use the newest local session JSONL file for the selected provider.")
    source.add_argument("--latest-match", action="store_true", help="When marker text matches multiple files, use the newest match.")

    boundaries = parser.add_argument_group("range")
    boundaries.add_argument("--start-line", type=int, help="Inclusive starting JSONL line.")
    boundaries.add_argument("--end-line", type=int, help="Inclusive ending JSONL line.")
    boundaries.add_argument("--start-marker", help="Inclusive starting marker text.")
    boundaries.add_argument("--end-marker", help="Inclusive ending marker text.")

    parser.add_argument("--mode", choices=["conversation", "hybrid", "technical"], required=True)
    parser.add_argument("--output", type=Path, required=True, help="Markdown output path.")
    parser.add_argument("--title", default="Transcript Export", help="Markdown title.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the transcript exporter."""

    parser = build_parser()
    args = parser.parse_args(argv)
    source = resolve_session_file(args)
    records = load_records(source)
    provider = detect_provider(source, records, args.provider)
    start_line, end_line = resolve_range(records, provider, args)
    plan = ExportPlan(
        source=source,
        provider=provider,
        start_line=start_line,
        end_line=end_line,
        mode=args.mode,
        output=Path(args.output).expanduser().resolve(),
        title=args.title,
    )
    markdown = render_transcript(plan, records)
    plan.output.parent.mkdir(parents=True, exist_ok=True)
    plan.output.write_text(markdown, encoding="utf-8")
    print(f"Wrote {plan.output}")
    print(f"Provider: {plan.provider}")
    print(f"Source: {plan.source}")
    print(f"Range: {plan.start_line}-{plan.end_line}")
    print(f"Mode: {plan.mode}")
    print(f"Bytes: {plan.output.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
