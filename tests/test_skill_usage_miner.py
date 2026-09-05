"""Collapse-view and footnote tests for skill-usage-miner.py (T1 over-count repair).

Each collapse test pins a defect class proven in the 2026-07-18/19 treatment
census work: the 8fa43ba8/359a3b70 session-fork replay, the 5c843a6a 13-second
double-invoke, and the typed-command + Skill-call double record of one fire.
Hermetic: pure-function tests on the imported module; no ledger or transcript IO.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

MINER_PATH = Path(__file__).resolve().parent.parent / "scripts" / "skill-usage-miner.py"
_spec = importlib.util.spec_from_file_location("skill_usage_miner", MINER_PATH)
assert _spec is not None and _spec.loader is not None
miner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(miner)


def row(
    key: str,
    skill: str,
    ts: str | None,
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
    assert "Codex read rows" in out


# ---- Codex model-invoked loads and the archived store (2026-09-05 repair) ----
#
# Specimens: athena-kb-local session 01a04483 (2026-08-27) loaded regex-craft with
# `sed -n '1,360p' /Users/jp/.agents/skills/regex-craft/SKILL.md` inside a
# custom_tool_call/exec JS snippet; cross-model session 019e9ee6 (2026-06-07) loaded
# zoom-out with a function_call/exec_command JSON `{"cmd": "cat .../SKILL.md"}`.
# Neither wrote a <skill> block, so neither had a ledger row.


def _rollout_line(ts: str, payload: dict) -> str:
    return json.dumps({"timestamp": ts, "type": "response_item", "payload": payload})


def _exec_js(ts: str, cmd: str, call_id: str = "call_1") -> str:
    snippet = (
        "const r = await tools.exec_command({\n  cmd: " + json.dumps(cmd) + ",\n});"
    )
    return _rollout_line(
        ts,
        {
            "type": "custom_tool_call",
            "name": "exec",
            "call_id": call_id,
            "input": snippet,
        },
    )


def _exec_json(ts: str, cmd: str, call_id: str = "call_2") -> str:
    return _rollout_line(
        ts,
        {
            "type": "function_call",
            "name": "exec_command",
            "call_id": call_id,
            "arguments": json.dumps({"cmd": cmd, "workdir": "/Users/jp/x"}),
        },
    )


def _typed_tag(ts: str, skill: str) -> str:
    text = f"<skill>\n<name>{skill}</name>\n<path>/x/{skill}/SKILL.md</path>\n---\nname: {skill}\n"
    return _rollout_line(
        ts,
        {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": text}],
        },
    )


def _write_rollout(tmp_path, lines: list[str], session: str = "sess-1") -> Path:
    meta = json.dumps(
        {
            "timestamp": "2026-08-27T18:37:35.000Z",
            "type": "session_meta",
            "payload": {"id": session, "cwd": "/Users/jp/athena-kb-local"},
        }
    )
    p = tmp_path / "rollout-2026-08-27T14-37-35-sess-1.jsonl"
    p.write_text("\n".join([meta, *lines]) + "\n", encoding="utf-8")
    return p


def test_codex_shell_read_of_skill_md_is_a_model_fire(tmp_path) -> None:
    p = _write_rollout(
        tmp_path,
        [
            _exec_js(
                "2026-08-27T19:57:09.519Z",
                "wc -l /Users/jp/.agents/skills/regex-craft/SKILL.md\n"
                "sed -n '1,360p' /Users/jp/.agents/skills/regex-craft/SKILL.md",
            ),
        ],
    )
    rows = list(miner.iter_codex_fires(p))
    assert len(rows) == 1
    r = rows[0]
    assert r["skill"] == "regex-craft"
    assert r["kind"] == "read"
    assert r["source"] == "model"
    assert r["runtime"] == "codex"
    assert r["key"] == "codex:sess-1:read:regex-craft"
    assert r["ts"] == "2026-08-27T19:57:09.519Z"
    assert r["cwd"] == "/Users/jp/athena-kb-local"
    assert r["session_reads"] == 1
    assert "archived" not in r


def test_codex_read_row_once_per_session_and_skill(tmp_path) -> None:
    # The same file read twice, minutes apart, is one load: the key is store- and
    # time-independent, so a re-mine or an archive move never duplicates it either.
    p = _write_rollout(
        tmp_path,
        [
            _exec_json(
                "2026-06-07T00:00:00Z", "cat /Users/jp/.codex/skills/zoom-out/SKILL.md"
            ),
            _exec_json(
                "2026-06-07T00:20:00Z",
                "sed -n '40,80p' /Users/jp/.codex/skills/zoom-out/SKILL.md",
                call_id="call_3",
            ),
        ],
    )
    rows = list(miner.iter_codex_fires(p))
    assert [r["key"] for r in rows] == ["codex:sess-1:read:zoom-out"]
    assert rows[0]["ts"] == "2026-06-07T00:00:00Z"
    assert rows[0]["read_burst"] == 1
    assert rows[0]["session_reads"] == 1


def test_read_burst_separates_a_roster_scan_from_a_lone_choice(tmp_path) -> None:
    # Three skills read within two minutes (a routing scan), then one skill read an
    # hour later on its own (a choice): the burst is 3 for the scan reads and 1 for
    # the lone read, while session_reads is 4 for all of them.
    p = _write_rollout(
        tmp_path,
        [
            _exec_js(
                "2026-08-13T16:00:00Z", "cat /Users/jp/.agents/skills/tdd/SKILL.md"
            ),
            _exec_js(
                "2026-08-13T16:00:40Z",
                "cat /Users/jp/.agents/skills/diagnose/SKILL.md",
                call_id="call_b",
            ),
            _exec_js(
                "2026-08-13T16:01:50Z",
                "cat /Users/jp/.agents/skills/keep-green/SKILL.md",
                call_id="call_c",
            ),
            _exec_js(
                "2026-08-13T17:05:00Z",
                "cat /Users/jp/.agents/skills/regex-craft/SKILL.md",
                call_id="call_d",
            ),
        ],
    )
    rows = {r["skill"]: r for r in miner.iter_codex_fires(p)}
    assert {s: r["read_burst"] for s, r in rows.items()} == {
        "tdd": 3,
        "diagnose": 3,
        "keep-green": 3,
        "regex-craft": 1,
    }
    assert {r["session_reads"] for r in rows.values()} == {4}
    assert miner.SCAN_READ_BURST <= 4  # the scan above is classed as a scan


def test_codex_read_is_plugin_qualified_under_plugin_trees(tmp_path) -> None:
    p = _write_rollout(
        tmp_path,
        [
            _exec_js(
                "2026-07-11T13:44:30Z",
                "sed -n '1,240p' /Users/jp/.codex/plugins/cache/turbo-mode/handoff/3.2.1/skills/load-handoff/SKILL.md",
            ),
            _exec_json(
                "2026-07-11T13:45:30Z",
                "cat /Users/jp/.agents/plugins/decide/skills/scope-cut/SKILL.md",
                call_id="call_4",
            ),
        ],
    )
    skills = sorted(r["skill"] for r in miner.iter_codex_fires(p))
    assert skills == ["decide:scope-cut", "handoff:load-handoff"]
    assert miner.skill_from_read_path("/Users/jp/.agents/skills/tdd") == "tdd"


def test_codex_read_suppressed_when_same_session_tagged_the_skill(tmp_path) -> None:
    # A typed `$tdd` already marks the load; a later re-read of the file is not a
    # second fire. `session_reads` still counts it, so a scanning session is visible.
    p = _write_rollout(
        tmp_path,
        [
            _typed_tag("2026-08-27T19:00:00Z", "tdd"),
            _exec_js(
                "2026-08-27T19:30:00Z", "cat /Users/jp/.agents/skills/tdd/SKILL.md"
            ),
            _exec_js(
                "2026-08-27T19:31:00Z",
                "cat /Users/jp/.agents/skills/regex-craft/SKILL.md",
                call_id="call_5",
            ),
        ],
    )
    rows = list(miner.iter_codex_fires(p))
    assert [(r["skill"], r.get("kind")) for r in rows] == [
        ("tdd", None),
        ("regex-craft", "read"),
    ]
    assert rows[1]["session_reads"] == 2
    # the suppressed tdd read still counts toward the burst: two reads 60s apart
    assert rows[1]["read_burst"] == 2


def test_codex_read_ignores_globs_edits_and_outputs(tmp_path) -> None:
    p = _write_rollout(
        tmp_path,
        [
            # a roster glob, a bare filename, and a find: no directory, no load
            _exec_js(
                "2026-08-27T19:00:00Z", "grep -l x /Users/jp/.agents/skills/*/SKILL.md"
            ),
            _exec_js("2026-08-27T19:01:00Z", "cat SKILL.md", call_id="call_6"),
            _exec_js("2026-08-27T19:02:00Z", "find . -name SKILL.md", call_id="call_7"),
            # an edit of a skill file is not a load
            _rollout_line(
                "2026-08-27T19:03:00Z",
                {
                    "type": "custom_tool_call",
                    "name": "apply_patch",
                    "call_id": "call_8",
                    "input": "*** Update File: /Users/jp/.agents/skills/tdd/SKILL.md\n",
                },
            ),
            # the skill body arriving in a tool OUTPUT is not a call
            _rollout_line(
                "2026-08-27T19:04:00Z",
                {
                    "type": "custom_tool_call_output",
                    "call_id": "call_9",
                    "output": "cat /Users/jp/.agents/skills/steelman/SKILL.md\n---\nname: steelman\n",
                },
            ),
        ],
    )
    assert list(miner.iter_codex_fires(p)) == []


def test_codex_archived_rows_are_marked_and_share_the_key(tmp_path) -> None:
    p = _write_rollout(
        tmp_path,
        [
            _exec_js(
                "2026-08-27T19:57:09Z",
                "cat /Users/jp/.agents/skills/regex-craft/SKILL.md",
            )
        ],
    )
    live = list(miner.iter_codex_fires(p))
    arch = list(miner.iter_codex_fires(p, archived=True))
    assert live[0]["key"] == arch[0]["key"]
    assert arch[0]["archived"] is True
    assert "archived" not in live[0]


def test_codex_roots_include_the_archived_store() -> None:
    assert miner.CODEX_ARCHIVED_DIR.name == "archived_sessions"
    assert miner.CODEX_ARCHIVED_DIR.parent == miner.CODEX_SESSIONS_DIR.parent
    assert miner.CODEX_ROOTS == (miner.CODEX_SESSIONS_DIR, miner.CODEX_ARCHIVED_DIR)


def test_read_and_tag_rows_burst_collapse_together() -> None:
    # A tag and a read of the same skill seconds apart in one session are one fire.
    tag = row(
        "codex:s:2026-08-27T19:00:00Z:tdd",
        "tdd",
        "2026-08-27T19:00:00Z",
        "s",
        runtime="codex",
    )
    rd = row(
        "codex:s:read:tdd",
        "tdd",
        "2026-08-27T19:00:30Z",
        "s",
        source="model",
        runtime="codex",
        kind="read",
    )
    kept, stats = miner.collapse([tag, rd])
    assert kept == [tag]
    assert stats == {"fork": 0, "burst": 1}


def test_summary_counts_reads_in_their_own_column(capsys) -> None:
    rows = [
        row(
            "codex:s:read:tdd",
            "tdd",
            "2026-08-27T19:00:00Z",
            "s",
            source="model",
            runtime="codex",
            kind="read",
        ),
        row(
            "codex:t:2026-08-28T19:00:00Z:tdd",
            "tdd",
            "2026-08-28T19:00:00Z",
            "t",
            runtime="codex",
        ),
    ]
    miner.summarize(rows)
    out = capsys.readouterr().out
    header = next(line for line in out.splitlines() if line.startswith("skill "))
    assert "reads" in header
    tdd_line = next(line for line in out.splitlines() if line.startswith("tdd "))
    cols = tdd_line.split()
    # skill total model user codex reads subag cwds last
    assert cols[1:6] == ["2", "1", "1", "2", "1"]
