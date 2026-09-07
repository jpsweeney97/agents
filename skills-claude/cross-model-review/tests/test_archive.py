from pathlib import Path

import pytest
from cmr_archive import Archive, ReviewError


def test_source_is_preserved_and_archive_is_external(tmp_path: Path) -> None:
    repo = tmp_path / "target"
    repo.mkdir()
    source = repo / "plan.md"
    source.write_bytes(b"# Original\r\nKeep data local.\r\n")
    archive = Archive.create(tmp_path / "review", repo, source, 3)
    state = archive.load()
    assert state["used"] == 0
    assert archive.text(state["original"]) == "# Original\r\nKeep data local.\r\n"
    assert source.read_bytes() == b"# Original\r\nKeep data local.\r\n"
    with pytest.raises(ReviewError, match="outside the target"):
        Archive.create(repo / "bad-review", repo, source, 3)
