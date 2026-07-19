"""Collapse-view and footnote tests for skill-usage-miner.py (T1 over-count repair).

Each collapse test pins a defect class proven in the 2026-07-18/19 treatment
census work: the 8fa43ba8/359a3b70 session-fork replay, the 5c843a6a 13-second
double-invoke, and the typed-command + Skill-call double record of one fire.
Hermetic: pure-function tests on the imported module; no ledger or transcript IO.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

MINER_PATH = Path(__file__).resolve().parent.parent / "scripts" / "skill-usage-miner.py"
_spec = importlib.util.spec_from_file_location("skill_usage_miner", MINER_PATH)
assert _spec is not None and _spec.loader is not None
miner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(miner)


def row(
    key: str,
    skill: str,
    ts: "str | None",
    session: str,
    source: str = "user",
    **extra: object,
) -> dict:
    return {
        "key": key,
        "skill": skill,
        "ts": ts,
        "session": session,
        "source": source,
        "cwd": "/tmp/x",
        "sidechain": False,
        **extra,
    }


def test_fork_replay_collapses_to_one_fire() -> None:
    # The real specimen shape: a forked session file replays the same user record
    # (same uuid, same ts) under a new sessionId.
    uuid = "3417c08d-ea7e-49db-b303-d5b1038d3fe4"
    a = row(
        f"s-orig:{uuid}:methodology-critique",
        "methodology-critique",
        "2026-07-06T15:45:46.710Z",
        "s-orig",
    )
    b = row(
        f"s-fork:{uuid}:methodology-critique",
        "methodology-critique",
        "2026-07-06T15:45:46.710Z",
        "s-fork",
    )
    kept, stats = miner.collapse([a, b])
    assert kept == [a]
    assert stats == {"fork": 1, "burst": 0}


def test_codex_rows_exempt_from_fork_collapse() -> None:
    # Codex key tails (`ts:skill`) are not globally unique across sessions; two
    # sessions firing the same skill at the same second are two fires.
    ts = "2026-07-06T15:45:46.710Z"
    a = row(f"codex:sess-a:{ts}:tdd", "tdd", ts, "sess-a", runtime="codex")
    b = row(f"codex:sess-b:{ts}:tdd", "tdd", ts, "sess-b", runtime="codex")
    kept, stats = miner.collapse([a, b])
    assert kept == [a, b]
    assert stats["fork"] == 0


def test_hook_fallback_keys_exempt_from_fork_collapse() -> None:
    # `hook-{ts}` fallback tails (tool_use_id absent) can collide across sessions.
    a = row("s1:hook-2026-07-06T15:45:46+00:00", "tdd", None, "s1", source="model")
    b = row("s2:hook-2026-07-06T15:45:46+00:00", "tdd", None, "s2", source="model")
    kept, stats = miner.collapse([a, b])
    assert kept == [a, b]
    assert stats["fork"] == 0


def test_burst_collapse_13s_double_invoke() -> None:
    # The real specimen: session 5c843a6a fired methodology-critique at
    # 17:05:30 and again 13 seconds later; one fire.
    a = row(
        "s:u1:methodology-critique",
        "methodology-critique",
        "2026-07-06T17:05:30.385Z",
        "s",
    )
    b = row(
        "s:u2:methodology-critique",
        "methodology-critique",
        "2026-07-06T17:05:43.261Z",
        "s",
    )
    kept, stats = miner.collapse([a, b])
    assert kept == [a]
    assert stats == {"fork": 0, "burst": 1}


def test_burst_collapse_merges_typed_command_and_skill_call() -> None:
    # One fire can leave a typed-command row (alias short form) and a hook row
    # (plugin-qualified form) seconds apart; the bare canonical name merges them.
    typed = row("s:u1:load", "load", "2026-07-19T17:15:11.284Z", "s", source="user")
    hook = row(
        "s:toolu_01AAAA",
        "handoff:load-handoff",
        "2026-07-19T17:15:20+00:00",
        "s",
        source="model",
        via="hook",
    )
    kept, stats = miner.collapse([typed, hook])
    assert len(kept) == 1
    assert stats["burst"] == 1


def test_no_burst_collapse_beyond_window_or_across_sessions() -> None:
    a = row("s:u1:tdd", "tdd", "2026-07-06T15:00:00Z", "s")
    b = row("s:u2:tdd", "tdd", "2026-07-06T15:05:00Z", "s")  # 5 min apart
    c = row("t:u3:tdd", "tdd", "2026-07-06T15:00:05Z", "t")  # other session
    kept, stats = miner.collapse([a, b, c])
    assert kept == [a, b, c]
    assert stats == {"fork": 0, "burst": 0}


def test_burst_anchor_is_last_kept_row_not_chained() -> None:
    # 0s, +30s, +59s, +90s: the +90s row is beyond the window from the anchor
    # (0s) and starts a new fire even though it is within 60s of the +59s row.
    rows = [
        row(
            f"s:u{i}:tdd",
            "tdd",
            f"2026-07-06T15:00:{s:02d}Z" if s < 60 else "2026-07-06T15:01:30Z",
            "s",
        )
        for i, s in enumerate((0, 30, 59, 90))
    ]
    kept, stats = miner.collapse(rows)
    assert [r["key"] for r in kept] == ["s:u0:tdd", "s:u3:tdd"]
    assert stats["burst"] == 2


def test_rows_without_ts_never_burst_collapse() -> None:
    a = row("s:u1:tdd", "tdd", None, "s")
    b = row("s:u2:tdd", "tdd", None, "s")
    kept, stats = miner.collapse([a, b])
    assert kept == [a, b]
    assert stats["burst"] == 0


def test_summary_prints_collapse_view_and_t1_footnote(capsys) -> None:
    miner.summarize([])
    out = capsys.readouterr().out
    assert "T1 blindness footnote" in out
    assert "partially endogenous" in out
    assert "collapsed 0 fork replays" in out
