#!/usr/bin/env python3
"""PostToolUse hook: append Skill-tool fires to the global skill-usage ledger.

Pure telemetry — imposes nothing on agents, never blocks, always exits 0.
Registered user-level (PostToolUse, matcher "Skill") so fires are recorded in every
repo. The dedupe key matches scripts/skill-usage-miner.py's key shape, so mined
backfills and live hook records coexist without double-counting.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LEDGER = Path.home() / ".claude" / "logs" / "skill-usage-ledger.jsonl"


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Skill":
        return 0
    skill = str((data.get("tool_input") or {}).get("skill") or "").lstrip("/").strip()
    if not skill:
        return 0
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    tool_use_id = data.get("tool_use_id") or f"hook-{now}"
    rec = {
        "key": f"{data.get('session_id')}:{tool_use_id}",
        "ts": now,
        "skill": skill,
        "source": "model",
        "cwd": data.get("cwd"),
        "session": data.get("session_id"),
        "sidechain": False,
        "via": "hook",
    }
    try:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with LEDGER.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
