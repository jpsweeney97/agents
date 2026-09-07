import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


@pytest.fixture(autouse=True)
def prevent_real_codex(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    directory = tmp_path / "forbidden-codex-bin"
    directory.mkdir()
    executable = directory / "codex"
    executable.write_text(
        "#!/bin/sh\nprintf '%s\\n' 'Real Codex calls are forbidden in tests' >&2\nexit 97\n"
    )
    executable.chmod(0o755)
    monkeypatch.setenv("PATH", str(directory) + os.pathsep + os.environ["PATH"])
