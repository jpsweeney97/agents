from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "scripts" / "scoped_safety_scan.py"


def run_scan(*paths: Path | str, max_bytes: int | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(SCANNER)]
    if max_bytes is not None:
        cmd.extend(["--max-bytes", str(max_bytes)])
    cmd.extend(str(path) for path in paths)
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def scan_json(*paths: Path | str, max_bytes: int | None = None) -> tuple[int, dict[str, object]]:
    result = run_scan(*paths, max_bytes=max_bytes)
    assert result.stdout, result.stderr
    return result.returncode, json.loads(result.stdout)


def first_file(payload: dict[str, object]) -> dict[str, object]:
    files = payload["files"]
    assert isinstance(files, list)
    assert files
    return files[0]


def findings(payload: dict[str, object]) -> list[dict[str, object]]:
    file_payload = first_file(payload)
    found = file_payload["findings"]
    assert isinstance(found, list)
    return found


def write(path: Path, data: bytes | str) -> Path:
    if isinstance(data, bytes):
        path.write_bytes(data)
    else:
        path.write_text(data, encoding="utf-8")
    return path


def test_clean_source_is_clean(tmp_path: Path) -> None:
    source = write(tmp_path / "example.py", "def add(a: int, b: int) -> int:\n    return a + b\n")

    code, payload = scan_json(source)

    assert code == 0
    assert payload["schema_version"] == 1
    assert payload["overall_status"] == "clean"
    file_payload = first_file(payload)
    assert file_payload["status"] == "clean"
    assert file_payload["categories"] == {
        "secret_risk": "clean",
        "binary_or_unreadable": "clean",
        "large_file": "clean",
        "generated_or_vendor_hint": "clean",
    }
    assert file_payload["findings"] == []


def test_secret_marker_is_positive_without_snippet(tmp_path: Path) -> None:
    secret_value = "sk-test-secret-value"
    source = write(tmp_path / "settings.py", f"api_key = '{secret_value}'\n")

    code, payload = scan_json(source)

    assert code == 1
    assert payload["overall_status"] == "positive"
    file_payload = first_file(payload)
    assert file_payload["status"] == "positive"
    assert file_payload["categories"]["secret_risk"] == "positive"
    serialized = json.dumps(payload)
    assert secret_value not in serialized
    assert source.read_text(encoding="utf-8").strip() not in serialized
    assert findings(payload)[0]["rule_id"] == "SECRET_ASSIGNMENT"
    assert findings(payload)[0]["line"] == 1


def test_suspicious_extension_without_marker_is_uncertain(tmp_path: Path) -> None:
    source = write(tmp_path / ".env", "DEBUG=true\n")

    code, payload = scan_json(source)

    assert code == 1
    assert payload["overall_status"] == "uncertain"
    file_payload = first_file(payload)
    assert file_payload["status"] == "uncertain"
    assert file_payload["categories"]["secret_risk"] == "uncertain"
    assert findings(payload)[0]["rule_id"] == "SUSPICIOUS_SECRET_PATH"


def test_binary_file_is_positive(tmp_path: Path) -> None:
    source = write(tmp_path / "blob.bin", b"\x00\x01\x02\x03")

    code, payload = scan_json(source)

    assert code == 1
    file_payload = first_file(payload)
    assert file_payload["status"] == "positive"
    assert file_payload["categories"]["binary_or_unreadable"] == "positive"
    assert findings(payload)[0]["rule_id"] == "BINARY_FILE"


def test_large_file_is_positive_and_test_override_can_make_it_clean(tmp_path: Path) -> None:
    source = write(tmp_path / "large.txt", "x" * 12)

    positive_code, positive_payload = scan_json(source, max_bytes=8)
    clean_code, clean_payload = scan_json(source, max_bytes=64)

    assert positive_code == 1
    assert first_file(positive_payload)["categories"]["large_file"] == "positive"
    assert findings(positive_payload)[0]["rule_id"] == "LARGE_FILE"
    assert clean_code == 0
    assert clean_payload["overall_status"] == "clean"


def test_missing_path_is_uncertain(tmp_path: Path) -> None:
    missing = tmp_path / "missing.py"

    code, payload = scan_json(missing)

    assert code == 1
    file_payload = first_file(payload)
    assert file_payload["status"] == "uncertain"
    assert file_payload["categories"]["binary_or_unreadable"] == "uncertain"
    assert findings(payload)[0]["rule_id"] == "MISSING_PATH"


def test_symlink_is_uncertain_and_not_followed(tmp_path: Path) -> None:
    target = write(tmp_path / "target.py", "token = 'sk-target-secret'\n")
    link = tmp_path / "link.py"
    link.symlink_to(target)

    code, payload = scan_json(link)

    assert code == 1
    file_payload = first_file(payload)
    assert file_payload["status"] == "uncertain"
    assert file_payload["categories"]["binary_or_unreadable"] == "uncertain"
    finding = findings(payload)[0]
    assert finding["rule_id"] == "SYMLINK"
    assert finding["target"] == str(target)
    assert "sk-target-secret" not in json.dumps(payload)


def test_generated_vendor_path_is_positive(tmp_path: Path) -> None:
    source_dir = tmp_path / "vendor"
    source_dir.mkdir()
    source = write(source_dir / "library.py", "def library() -> None:\n    pass\n")

    code, payload = scan_json(source)

    assert code == 1
    file_payload = first_file(payload)
    assert file_payload["status"] == "positive"
    assert file_payload["categories"]["generated_or_vendor_hint"] == "positive"
    assert findings(payload)[0]["rule_id"] == "GENERATED_OR_VENDOR_PATH"


def test_minified_dense_text_is_uncertain(tmp_path: Path) -> None:
    source = write(tmp_path / "bundle.js", "var a=" + "1;" * 400)

    code, payload = scan_json(source)

    assert code == 1
    file_payload = first_file(payload)
    assert file_payload["status"] == "uncertain"
    assert file_payload["categories"]["generated_or_vendor_hint"] == "uncertain"
    assert findings(payload)[0]["rule_id"] == "DENSE_MINIFIED_TEXT"


def test_usage_errors_return_exit_two_without_json_result() -> None:
    result = run_scan("--max-bytes")

    assert result.returncode == 2
    assert not result.stdout.strip()
