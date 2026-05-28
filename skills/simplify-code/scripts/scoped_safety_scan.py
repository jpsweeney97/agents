#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


Status = Literal["clean", "positive", "uncertain"]
Category = Literal[
    "secret_risk",
    "binary_or_unreadable",
    "large_file",
    "generated_or_vendor_hint",
]

SCHEMA_VERSION = 1
DEFAULT_MAX_BYTES = 1_048_576

GENERATED_OR_VENDOR_PARTS = {
    ".generated",
    "__generated__",
    "autogen",
    "generated",
    "node_modules",
    "third_party",
    "vendor",
}
GENERATED_OR_VENDOR_NAMES = {
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
}
SECRET_SUSPICIOUS_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".netrc",
    "credentials",
    "credentials.json",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
    "secrets.json",
}
SECRET_SUSPICIOUS_SUFFIXES = {
    ".asc",
    ".crt",
    ".der",
    ".gpg",
    ".jks",
    ".key",
    ".kubeconfig",
    ".p12",
    ".pem",
    ".pfx",
}

SECRET_ASSIGNMENT_RE = re.compile(
    r"""(?ix)
    \b(
        api[_-]?key|
        access[_-]?token|
        auth[_-]?token|
        client[_-]?secret|
        credential|
        password|
        private[_-]?key|
        secret|
        token
    )\b
    \s*[:=]\s*
    (?P<quote>['\"])[^'\"\n]{8,}(?P=quote)
    """
)
TOKEN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("OPENAI_API_KEY", re.compile(r"\bsk-[A-Za-z0-9_-]{10,}\b")),
    ("GITHUB_TOKEN", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("AWS_ACCESS_KEY_ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("SLACK_TOKEN", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    (
        "PRIVATE_KEY_BLOCK",
        re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    ),
)


@dataclass(frozen=True)
class Finding:
    category: Category
    status: Status
    rule_id: str
    reason: str
    line: int | None = None
    byte_offset: int | None = None
    target: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "category": self.category,
            "status": self.status,
            "rule_id": self.rule_id,
            "line": self.line,
            "byte_offset": self.byte_offset,
            "reason": self.reason,
        }
        if self.target is not None:
            data["target"] = self.target
        return data


def initial_categories() -> dict[Category, Status]:
    return {
        "secret_risk": "clean",
        "binary_or_unreadable": "clean",
        "large_file": "clean",
        "generated_or_vendor_hint": "clean",
    }


def strongest_status(statuses: list[Status]) -> Status:
    if "positive" in statuses:
        return "positive"
    if "uncertain" in statuses:
        return "uncertain"
    return "clean"


def update_category(
    categories: dict[Category, Status], category: Category, status: Status
) -> None:
    categories[category] = strongest_status([categories[category], status])


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def is_binary(data: bytes) -> bool:
    if b"\x00" in data:
        return True
    if not data:
        return False
    control = sum(byte < 32 and byte not in {9, 10, 12, 13} for byte in data)
    return control / len(data) > 0.30


def is_dense_minified_text(text: str) -> bool:
    lines = text.splitlines() or [text]
    longest_line = max(len(line) for line in lines)
    return longest_line > 500 and len(lines) <= 3


def has_generated_or_vendor_hint(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    if parts & GENERATED_OR_VENDOR_PARTS:
        return True
    return path.name.lower() in GENERATED_OR_VENDOR_NAMES


def has_suspicious_secret_path(path: Path) -> bool:
    lower_name = path.name.lower()
    if lower_name in SECRET_SUSPICIOUS_NAMES:
        return True
    return any(lower_name.endswith(suffix) for suffix in SECRET_SUSPICIOUS_SUFFIXES)


def scan_text_for_secrets(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for match in SECRET_ASSIGNMENT_RE.finditer(text):
        findings.append(
            Finding(
                category="secret_risk",
                status="positive",
                rule_id="SECRET_ASSIGNMENT",
                line=line_for_offset(text, match.start()),
                byte_offset=len(text[: match.start()].encode("utf-8")),
                reason="Secret-like assignment detected; value redacted.",
            )
        )
    for rule_id, pattern in TOKEN_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(
                Finding(
                    category="secret_risk",
                    status="positive",
                    rule_id=rule_id,
                    line=line_for_offset(text, match.start()),
                    byte_offset=len(text[: match.start()].encode("utf-8")),
                    reason="Credential-looking value detected; value redacted.",
                )
            )
    return findings


def add_finding(
    categories: dict[Category, Status], findings: list[Finding], finding: Finding
) -> None:
    update_category(categories, finding.category, finding.status)
    findings.append(finding)


def missing_or_symlink_result(
    path: Path, categories: dict[Category, Status], findings: list[Finding]
) -> dict[str, object] | None:
    if not path.exists() and not path.is_symlink():
        add_finding(
            categories,
            findings,
            Finding(
                category="binary_or_unreadable",
                status="uncertain",
                rule_id="MISSING_PATH",
                reason="Path does not exist; risk cannot be ruled out.",
            ),
        )
        return file_result(path, categories, findings)

    if path.is_symlink():
        add_finding(
            categories,
            findings,
            Finding(
                category="binary_or_unreadable",
                status="uncertain",
                rule_id="SYMLINK",
                reason="Symlink not followed; target path reported without scanning target bytes.",
                target=os.readlink(path),
            ),
        )
        return file_result(path, categories, findings)

    return None


def add_path_hints(
    path: Path, categories: dict[Category, Status], findings: list[Finding]
) -> None:
    if has_generated_or_vendor_hint(path):
        add_finding(
            categories,
            findings,
            Finding(
                category="generated_or_vendor_hint",
                status="positive",
                rule_id="GENERATED_OR_VENDOR_PATH",
                reason="Path has an explicit generated or vendor hint.",
            ),
        )

    if has_suspicious_secret_path(path):
        add_finding(
            categories,
            findings,
            Finding(
                category="secret_risk",
                status="uncertain",
                rule_id="SUSPICIOUS_SECRET_PATH",
                reason="Path or extension is commonly used for secrets; content marker not required.",
            ),
        )


def read_text_or_result(
    path: Path,
    max_bytes: int,
    categories: dict[Category, Status],
    findings: list[Finding],
) -> str | dict[str, object]:
    size = path.stat().st_size
    if size > max_bytes:
        add_finding(
            categories,
            findings,
            Finding(
                category="large_file",
                status="positive",
                rule_id="LARGE_FILE",
                reason="File exceeds max_bytes threshold.",
            ),
        )
        return file_result(path, categories, findings)

    data = path.read_bytes()
    if is_binary(data):
        add_finding(
            categories,
            findings,
            Finding(
                category="binary_or_unreadable",
                status="positive",
                rule_id="BINARY_FILE",
                reason="Binary-looking bytes detected; content not copied or interpreted.",
            ),
        )
        return file_result(path, categories, findings)

    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        add_finding(
            categories,
            findings,
            Finding(
                category="binary_or_unreadable",
                status="uncertain",
                rule_id="DECODE_FAILURE",
                reason="File could not be decoded as UTF-8.",
            ),
        )
        return file_result(path, categories, findings)


def add_text_findings(
    text: str, categories: dict[Category, Status], findings: list[Finding]
) -> None:
    for finding in scan_text_for_secrets(text):
        add_finding(categories, findings, finding)

    if is_dense_minified_text(text):
        add_finding(
            categories,
            findings,
            Finding(
                category="generated_or_vendor_hint",
                status="uncertain",
                rule_id="DENSE_MINIFIED_TEXT",
                reason="Dense minified-looking text detected.",
            ),
        )


def add_error_finding(
    categories: dict[Category, Status],
    findings: list[Finding],
    rule_id: str,
    reason: str,
) -> None:
    add_finding(
        categories,
        findings,
        Finding(
            category="binary_or_unreadable",
            status="uncertain",
            rule_id=rule_id,
            reason=reason,
        ),
    )


def scan_path(path: Path, max_bytes: int) -> dict[str, object]:
    categories = initial_categories()
    findings: list[Finding] = []

    try:
        early_result = missing_or_symlink_result(path, categories, findings)
        if early_result is not None:
            return early_result

        add_path_hints(path, categories, findings)
        text_or_result = read_text_or_result(path, max_bytes, categories, findings)
        if isinstance(text_or_result, dict):
            return text_or_result

        add_text_findings(text_or_result, categories, findings)
    except OSError:
        add_error_finding(
            categories, findings, "READ_ERROR", "Path could not be read; risk cannot be ruled out."
        )
    except Exception:
        add_error_finding(
            categories,
            findings,
            "SCANNER_ERROR",
            "Scanner internal error while processing path.",
        )

    return file_result(path, categories, findings)


def file_result(
    path: Path, categories: dict[Category, Status], findings: list[Finding]
) -> dict[str, object]:
    status = strongest_status(list(categories.values()))
    return {
        "path": str(path),
        "status": status,
        "categories": categories,
        "findings": [finding.to_json() for finding in findings],
    }


def build_payload(paths: list[Path], max_bytes: int) -> dict[str, object]:
    files = [scan_path(path, max_bytes=max_bytes) for path in paths]
    overall_status = strongest_status([file_data["status"] for file_data in files])  # type: ignore[list-item]
    return {
        "schema_version": SCHEMA_VERSION,
        "overall_status": overall_status,
        "max_bytes": max_bytes,
        "files": files,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan scoped files for simplify-code lane and backup safety risks."
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=DEFAULT_MAX_BYTES,
        help=(
            "Per-file size threshold. Use the default for real simplify-code "
            "eligibility unless the user approves a different threshold."
        ),
    )
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args(argv)
    if args.max_bytes < 1:
        parser.error("--max-bytes must be a positive integer")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        payload = build_payload(args.paths, max_bytes=args.max_bytes)
    except Exception as exc:
        sys.stderr.write(
            f"scoped safety scan failed: internal error. Got: {exc!r:.100}\n"
        )
        return 2
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if payload["overall_status"] == "clean" else 1


if __name__ == "__main__":
    raise SystemExit(main())
