from pathlib import Path

import pytest
from cmr_archive import Archive
from cmr_protocol import invoke, response_schema
from cross_model_runtime.codex_transport import CodexResult, CodexTransportError


def test_malformed_response_is_saved_before_validation(tmp_path: Path) -> None:
    archive = Archive(tmp_path)
    request = {
        "prompt": "Review candidate",
        "schema": response_schema("abc"),
        "repo": str(tmp_path),
        "session": None,
        "timeout": 180.0,
    }

    def malformed(*args: object, **kwargs: object) -> CodexResult:
        return CodexResult("not JSON", 0, "thread evidence", "diagnostic", ("codex",))

    with pytest.raises(CodexTransportError, match="not valid JSON"):
        invoke(archive, "01-opening", request, malformed)
    raw = archive.read("01-opening.raw.json")
    assert raw["final_message"] == "not JSON"
    assert raw["stdout"] == "thread evidence"
    assert raw["stderr"] == "diagnostic"
