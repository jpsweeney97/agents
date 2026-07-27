#!/usr/bin/env python3
"""Night porter: digest the failure ledger and surface it where JP looks.

Reads ~/.claude/logs/failure-ledger.jsonl (appended live by the
PostToolUseFailure hook ~/.claude/hooks/failure-ledger.py), computes a digest
of the failures that arrived since the previous run — counts by tool and by
directory, recurring error signatures tracked across runs, deltas against the
previous window — writes it to ~/.claude/logs/failure-digest.md, persists its
cursor and signature memory in ~/.claude/logs/failure-digest-state.json, and
posts a macOS notification when there is something worth reading.

Scheduled nightly by com.jp.night-porter (source of truth:
scripts/com.jp.night-porter.plist in this repo). The optional phone-push
upgrade (a Claude Code Desktop scheduled task that runs this script with
--no-notify and pushes the HEADLINE line) is pinned in
scripts/night-porter-task-prompt.md and replaces the macOS notification leg.

Delivery contract:
- The digest file is the durable record; the notification is the attention
  tap. Notifications fire when the window has new failures, and always on
  Sundays as a liveness heartbeat (a quiet porter and a dead porter must not
  look alike). Anomalies (missing ledger, corrupt state, shrunken ledger)
  always notify: the porter never fails silently by design.
- The last stdout line is always "HEADLINE: <one-line summary>" — a labeled
  output contract for downstream consumers.

Cursor discipline: the state keeps a byte offset into the append-only ledger.
Complete (newline-terminated) lines are consumed whether or not they parse —
unparseable complete lines are counted and reported in the digest, never
silently skipped and never re-read. An unterminated trailing fragment (a
mid-append partial write) is left for the next run. A ledger smaller than the
cursor means rotation or hand-editing: the cursor resets to zero with a loud
note and a notification.

Stdlib-only on purpose: the LaunchAgent runs /usr/bin/python3, and pinned
mise interpreter paths die silently on runtime upgrades (see the
com.jp.skill-usage-miner precedent).

Usage: failure-digest.py [--ledger PATH] [--digest PATH] [--state PATH]
                         [--no-notify]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_LEDGER = Path.home() / ".claude" / "logs" / "failure-ledger.jsonl"
DEFAULT_DIGEST = Path.home() / ".claude" / "logs" / "failure-digest.md"
DEFAULT_STATE = Path.home() / ".claude" / "logs" / "failure-digest-state.json"

STATE_VERSION = 1
MAX_SIGNATURES = 200
MAX_RECURRING_SHOWN = 10
HEADLINE_MAX = 180

_EXIT_CODE_ONLY = re.compile(r"(?i)^exit code \d+$")


def now_local() -> datetime:
    """Return the current time as an aware datetime in the local timezone."""
    return datetime.now(timezone.utc).astimezone()


def fmt_local(dt: datetime) -> str:
    """Format an aware datetime for display in the local timezone."""
    return dt.astimezone().strftime("%Y-%m-%d %H:%M %Z")


def parse_ts(raw: str) -> datetime:
    """Parse a ledger ISO timestamp into an aware datetime.

    Raises:
        ValueError: if the timestamp is not ISO-8601 or is naive.
    """
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        raise ValueError(f"parse ts failed: naive timestamp. Got: {raw!r:.100}")
    return dt


def tilde(path: str) -> str:
    """Abbreviate the home-directory prefix of a path to ~ for display."""
    home = str(Path.home())
    return "~" + path[len(home) :] if path.startswith(home) else path


def signature(tool: str, error: str) -> str:
    """Normalize an error into a stable grouping signature.

    Takes the first informative line (skipping a bare "Exit code N" line in
    favor of the line after it), then masks hex constants, hashes, decimal
    runs, and absolute paths so cosmetic differences collapse into one key.
    """
    lines = [ln.strip() for ln in error.splitlines() if ln.strip()]
    if not lines:
        return f"{tool}|<empty error>"
    first = lines[0]
    if _EXIT_CODE_ONLY.match(first) and len(lines) > 1:
        first = f"{first}: {lines[1]}"
    sig = re.sub(r"0x[0-9a-fA-F]+", "#", first)
    sig = re.sub(r"\b[0-9a-f]{7,40}\b", "#", sig)
    sig = re.sub(r"\d+", "#", sig)
    sig = re.sub(r"(?:/[^\s:'\"]+)+", "<path>", sig)
    sig = re.sub(r"\s+", " ", sig).strip().lower()[:120]
    return f"{tool}|{sig}"


def example_line(entry: dict[str, Any]) -> str:
    """Build a one-line human-readable example for a ledger entry."""
    error = str(entry.get("error", ""))
    lines = [ln.strip() for ln in error.splitlines() if ln.strip()]
    text = ""
    if lines:
        text = lines[0]
        if _EXIT_CODE_ONLY.match(text) and len(lines) > 1:
            text = f"{text}: {lines[1]}"
    if entry.get("command"):
        cmd = str(entry["command"]).replace("\n", " ")[:60]
        text = f"$ {cmd} → {text}"
    return text[:160]


def load_state(path: Path) -> tuple[dict[str, Any], str | None]:
    """Load porter state, quarantining a corrupt file instead of dying.

    A corrupt state file is renamed aside (preserved as evidence) and the
    porter restarts from an empty state — surfaced to the caller as a reset
    note, never silently. A missing file is a normal first run.

    Returns:
        (state, reset_note) — reset_note is None unless recovery happened.
    """
    if not path.exists():
        return {}, None

    def _quarantine(reason: str) -> tuple[dict[str, Any], str]:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        aside = path.with_name(f"{path.name}.corrupt-{stamp}")
        path.rename(aside)
        return {}, (
            f"state file was corrupt ({reason}); preserved at {tilde(str(aside))} "
            "and restarted from scratch — digest windows reset"
        )

    text = path.read_text(encoding="utf-8")
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError as exc:
        return _quarantine(str(exc))
    if not isinstance(loaded, dict):
        return _quarantine(f"state root is {type(loaded).__name__}, not object")
    return loaded, None


def atomic_write(path: Path, content: str) -> None:
    """Write a file atomically via a same-directory temp file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def read_new_entries(
    ledger: Path, offset: int
) -> tuple[list[dict[str, Any]], int, list[str], str | None]:
    """Read complete ledger lines from the byte cursor onward.

    Consumes every newline-terminated line (parsed or not); leaves an
    unterminated trailing fragment for the next run. If the file is smaller
    than the cursor, resets to zero and reports it.

    Returns:
        (entries, new_offset, malformed_snippets, cursor_note)
    """
    size = ledger.stat().st_size
    cursor_note: str | None = None
    if offset > size:
        cursor_note = (
            f"ledger is smaller than the saved cursor ({size} < {offset} bytes) — "
            "rotated or hand-edited; cursor reset to 0, so counts may re-include "
            "older entries once"
        )
        offset = 0

    entries: list[dict[str, Any]] = []
    malformed: list[str] = []
    with ledger.open("rb") as fh:
        fh.seek(offset)
        pos = offset
        for raw in fh:
            if not raw.endswith(b"\n"):
                break  # mid-append partial write; next run picks it up
            pos += len(raw)
            line = raw.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError as exc:
                malformed.append(f"{line[:80]!r} ({exc})")
                continue
            if not isinstance(parsed, dict):
                malformed.append(f"{line[:80]!r} (entry is not an object)")
                continue
            try:
                parse_ts(str(parsed["ts"]))
            except (ValueError, KeyError) as exc:
                malformed.append(f"{line[:80]!r} (bad ts: {exc})")
                continue
            entries.append(parsed)
    return entries, pos, malformed, cursor_note


def update_signatures(
    signatures: dict[str, dict[str, Any]], entries: list[dict[str, Any]]
) -> None:
    """Fold this window's entries into the cross-run signature memory."""
    window_sigs: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        key = signature(str(entry.get("tool_name", "?")), str(entry.get("error", "")))
        window_sigs.setdefault(key, []).append(entry)
    for key, hits in window_sigs.items():
        latest = max(hits, key=lambda e: str(e["ts"]))
        record = signatures.get(key)
        if record is None:
            record = {
                "count": 0,
                "windows": 0,
                "first_seen": str(hits[0]["ts"]),
                "last_seen": str(latest["ts"]),
                "example": example_line(latest),
            }
            signatures[key] = record
        record["count"] += len(hits)
        record["windows"] += 1
        record["last_seen"] = str(latest["ts"])
        record["example"] = example_line(latest)
    if len(signatures) > MAX_SIGNATURES:
        keep = sorted(
            signatures.items(), key=lambda kv: str(kv[1]["last_seen"]), reverse=True
        )[:MAX_SIGNATURES]
        signatures.clear()
        signatures.update(dict(keep))


def recurring(
    signatures: dict[str, dict[str, Any]],
) -> list[tuple[str, dict[str, Any]]]:
    """Return signatures that qualify as recurring, strongest first."""
    hits = [
        (key, rec)
        for key, rec in signatures.items()
        if int(rec["windows"]) >= 2 or int(rec["count"]) >= 3
    ]
    hits.sort(key=lambda kv: (int(kv[1]["windows"]), int(kv[1]["count"])), reverse=True)
    return hits[:MAX_RECURRING_SHOWN]


def build_headline(
    total: int,
    by_tool: Counter[str],
    top_example: str | None,
    since_label: str,
    alerts: list[str],
    malformed_count: int,
) -> str:
    """Compose the one-line summary used for stdout and notifications.

    Porter-health alerts (corrupt state, missing ledger, cursor reset) own
    the headline outright; unparseable ledger lines only append a suffix so
    they never mask the failure count.
    """
    if alerts:
        return f"night porter: {alerts[0]}"[:HEADLINE_MAX]
    if total == 0:
        head = f"0 new tool failures since {since_label}."
    else:
        tools = ", ".join(f"{tool} {count}" for tool, count in by_tool.most_common(3))
        rest = sum(by_tool.values()) - sum(c for _, c in by_tool.most_common(3))
        if rest > 0:
            tools += f", +{rest} more"
        head = f"{total} new tool failure{'s' if total != 1 else ''}: {tools}"
        if top_example:
            head += f" · top: {top_example}"
    if malformed_count:
        head += f" · {malformed_count} unparseable line{'s' if malformed_count != 1 else ''}"
    return head[:HEADLINE_MAX]


def build_digest(
    generated: datetime,
    since_label: str,
    entries: list[dict[str, Any]],
    prev_window: dict[str, Any],
    signatures: dict[str, dict[str, Any]],
    total_seen: int,
    since_ever: str,
    ledger: Path,
    malformed: list[str],
    notes: list[str],
) -> str:
    """Render the digest Markdown."""
    by_tool: Counter[str] = Counter(str(e.get("tool_name", "?")) for e in entries)
    by_cwd: Counter[str] = Counter(tilde(str(e.get("cwd", "?"))) for e in entries)
    prev_by_tool: dict[str, int] = dict(prev_window.get("by_tool", {}))
    prev_total = prev_window.get("total")

    lines = [
        "# Failure Ledger Digest",
        "",
        f"- Generated: {fmt_local(generated)} (night porter)",
        f"- Window: since {since_label}",
        f"- New failures: {len(entries)}"
        + (
            f" (previous window: {prev_total})"
            if prev_total is not None
            else " (first digest)"
        ),
        f"- All time: {total_seen} failures since {since_ever}",
        f"- Ledger: {tilde(str(ledger))}",
    ]
    for note in notes:
        lines.append(f"- **Attention: {note}**")
    lines.append("")

    lines.append("## By tool")
    lines.append("")
    if by_tool:
        lines.append("| Tool | Count | Δ vs previous window |")
        lines.append("|------|-------|----------------------|")
        for tool, count in by_tool.most_common():
            if prev_total is None:
                delta = "—"
            else:
                diff = count - prev_by_tool.get(tool, 0)
                delta = f"{diff:+d}" if diff else "±0"
            lines.append(f"| {tool} | {count} | {delta} |")
        dropped = [t for t in prev_by_tool if t not in by_tool]
        if dropped:
            lines.append("")
            lines.append(
                "Cleared since last window: "
                + ", ".join(f"{t} (was {prev_by_tool[t]})" for t in sorted(dropped))
            )
    else:
        lines.append("No new failures this window.")
    lines.append("")

    lines.append("## By directory")
    lines.append("")
    if by_cwd:
        lines.append("| Directory | Count |")
        lines.append("|-----------|-------|")
        for cwd, count in by_cwd.most_common():
            lines.append(f"| {cwd} | {count} |")
    else:
        lines.append("No new failures this window.")
    lines.append("")

    lines.append("## Recurring patterns")
    lines.append("")
    recur = recurring(signatures)
    if recur:
        for key, rec in recur:
            tool, _, sig = key.partition("|")
            lines.append(
                f"- **{tool}** · `{sig}` — {rec['count']} total across "
                f"{rec['windows']} digest window(s); last {fmt_local(parse_ts(str(rec['last_seen'])))}"
            )
            lines.append(f"  - example: `{rec['example']}`")
    else:
        lines.append(
            "(none yet — a pattern is recurring after appearing in 2+ digests "
            "or 3+ times in one window)"
        )
    lines.append("")

    lines.append("## Notes")
    lines.append("")
    if malformed:
        lines.append(
            f"- {len(malformed)} unparseable ledger line(s), consumed and skipped:"
        )
        for snippet in malformed[:5]:
            lines.append(f"  - {snippet}")
    else:
        lines.append("- 0 unparseable ledger lines.")
    lines.append(
        "- Recurring-failure insight feeds `friction-to-guards`; the raw ledger "
        "holds full error text."
    )
    lines.append("")
    return "\n".join(lines)


def notify(message: str) -> None:
    """Post a macOS notification, passing text as argv (never interpolated).

    Raises:
        RuntimeError: if osascript fails, with its stderr.
    """
    script = (
        "on run argv\n"
        "display notification (item 1 of argv) with title (item 2 of argv)\n"
        "end run"
    )
    result = subprocess.run(
        ["osascript", "-e", script, message, "Night porter"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"notify failed: osascript exit {result.returncode}. "
            f"Got: {result.stderr!r:.100}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Night porter: digest the failure ledger and surface it."
    )
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--digest", type=Path, default=DEFAULT_DIGEST)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument(
        "--no-notify",
        action="store_true",
        help="skip the macOS notification (tests; Desktop-task delivery)",
    )
    args = parser.parse_args()

    generated = now_local()
    state, reset_note = load_state(args.state)
    notes: list[str] = [reset_note] if reset_note else []

    if not args.ledger.exists():
        note = (
            f"failure ledger missing at {tilde(str(args.ledger))} — the "
            "PostToolUseFailure hook may be broken (it existed when the porter "
            "was built)"
        )
        notes.insert(0, note)
        headline = build_headline(0, Counter(), None, "—", notes, 0)
        atomic_write(
            args.digest,
            "# Failure Ledger Digest\n\n"
            f"- Generated: {fmt_local(generated)} (night porter)\n"
            f"- **Attention: {note}**\n",
        )
        print(f"digest: {args.digest}")
        print(f"HEADLINE: {headline}")
        if not args.no_notify:
            notify(headline)
        return 0

    since_ts = state.get("last_run")
    since_label = (
        fmt_local(parse_ts(since_ts)) if since_ts else "the beginning of the ledger"
    )

    entries, new_offset, malformed, cursor_note = read_new_entries(
        args.ledger, int(state.get("offset", 0))
    )
    if cursor_note:
        notes.append(cursor_note)

    signatures: dict[str, dict[str, Any]] = dict(state.get("signatures", {}))
    update_signatures(signatures, entries)

    by_tool: Counter[str] = Counter(str(e.get("tool_name", "?")) for e in entries)
    total_seen = int(state.get("total_seen", 0)) + len(entries)
    since_ever = state.get("since") or generated.strftime("%Y-%m-%d")

    top_example: str | None = None
    if entries:
        window_keys = Counter(
            signature(str(e.get("tool_name", "?")), str(e.get("error", "")))
            for e in entries
        )
        top_key = window_keys.most_common(1)[0][0]
        top_example = str(signatures[top_key]["example"])[:80]

    digest_text = build_digest(
        generated,
        since_label,
        entries,
        dict(state.get("prev_window", {})),
        signatures,
        total_seen,
        since_ever,
        args.ledger,
        malformed,
        notes,
    )
    atomic_write(args.digest, digest_text)

    new_state = {
        "version": STATE_VERSION,
        "offset": new_offset,
        "last_run": generated.isoformat(timespec="seconds"),
        "since": since_ever,
        "total_seen": total_seen,
        "prev_window": {"total": len(entries), "by_tool": dict(by_tool)},
        "signatures": signatures,
    }
    atomic_write(args.state, json.dumps(new_state, indent=1) + "\n")

    headline = build_headline(
        len(entries), by_tool, top_example, since_label, notes, len(malformed)
    )
    print(f"digest: {args.digest}")
    print(f"HEADLINE: {headline}")

    is_sunday = generated.weekday() == 6
    if not args.no_notify and (entries or notes or malformed or is_sunday):
        message = headline if entries or notes else f"Quiet: {headline} Porter alive."
        notify(message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
