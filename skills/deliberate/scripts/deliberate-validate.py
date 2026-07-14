#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""deliberate — bundled validator, brief renderer, and content-identity helper.

One implementation, invoked identically from Claude Code and Codex via Bash,
for: stage-brief rendering (pre-dispatch packet construction from the run-state
store and the canonical matrix), envelope validation, capsule validation,
run-state item validation and writes, content-identity computation, authored-
rendering comparison for the validation ladder, and the must-block/must-pass
fixture set.

Canonical data: references/contract-data.yaml — loaded at run time, never
copied here. Every check is deterministic shape and consistency only; nothing
here is semantic judgment, and orchestrator judgment never stands in for a
failed check.

Validator boundary (part of the skill contract):
- YAML parsed with a safe event-checked loader: custom tags rejected, anchors
  and aliases rejected before expansion, input past the byte or depth cap
  rejected before parse, exactly one document.
- Schemas bind fixed key sets; unknown keys are rejected, never ignored.
- argv-only invocation; every path argument is a literal path.
- Every read is canonicalized (symlinks resolved) and checked against the
  explicit read set for the command before any byte is read.
- The self-hash bootstrap is non-circular: the orchestrator verifies this
  script's content identifier with the platform hasher (`shasum -a 256` or
  equivalent), never with this script.

Exit codes: 0 pass; 1 validation failure; 2 refusal (unauthorized read,
off-column request, unsupported schema, bound breach, usage); 4 required
run-state item absent (the orchestrator maps this to `store failed: read`).
"""

from __future__ import annotations

import argparse
import hashlib
import io
import os
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_REFUSE = 2
EXIT_STORE_READ = 4

ENVELOPE_SCHEMA = "deliberate-envelope/v1"
RUNSTATE_SCHEMA = "deliberate-runstate/v1"
CAPSULE_SCHEMA = "deliberate-capsule/v1"

SAFE_TAGS = {
    "tag:yaml.org,2002:map",
    "tag:yaml.org,2002:seq",
    "tag:yaml.org,2002:str",
    "tag:yaml.org,2002:int",
    "tag:yaml.org,2002:float",
    "tag:yaml.org,2002:bool",
    "tag:yaml.org,2002:null",
}

PROVENANCE_FLAGS = {"user-seed", "generated", "revived", "accepted", "adopted"}
ENCOUNTER_KINDS = {"withheld-class", "instruction-like"}


class Refusal(Exception):
    """Refused before any content judgment (exit 2)."""


class ValidationFailure(Exception):
    """Deterministic shape/consistency check failed (exit 1)."""


class StoreReadLoss(Exception):
    """A required run-state item is absent or unreadable (exit 4)."""


def fail(op: str, reason: str, got: object = None) -> ValidationFailure:
    suffix = f" Got: {got!r:.300}" if got is not None else ""
    return ValidationFailure(f"{op} failed: {reason}.{suffix}")


def refuse(op: str, reason: str, got: object = None) -> Refusal:
    suffix = f" Got: {got!r:.300}" if got is not None else ""
    return Refusal(f"{op} refused: {reason}.{suffix}")


# ---------------------------------------------------------------------------
# Read-set enforcement
# ---------------------------------------------------------------------------


class ReadSet:
    """Explicit read authorization: canonicalized roots; reads outside refuse."""

    def __init__(self) -> None:
        self.roots: list[Path] = []

    def allow(self, path: Path) -> Path:
        canonical = Path(os.path.realpath(path))
        self.roots.append(canonical)
        return canonical

    def check(self, path: Path) -> Path:
        canonical = Path(os.path.realpath(path))
        for root in self.roots:
            if canonical == root or root in canonical.parents:
                return canonical
        raise refuse("read", f"path outside the explicit read set: {canonical}")

    def read_bytes(self, path: Path) -> bytes:
        canonical = self.check(path)
        if not canonical.exists():
            raise fail("read", f"path does not exist: {canonical}")
        return canonical.read_bytes()


# ---------------------------------------------------------------------------
# Safe YAML
# ---------------------------------------------------------------------------


def safe_parse(raw: bytes, *, byte_cap: int, depth_cap: int, op: str) -> Any:
    """Event-checked safe parse: caps first, then anchors/aliases/tags, one doc."""
    if len(raw) > byte_cap:
        raise refuse(op, f"input of {len(raw)} bytes exceeds the {byte_cap}-byte cap")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise fail(op, f"input is not UTF-8: {exc}")
    depth = 0
    documents = 0
    try:
        for event in yaml.parse(io.StringIO(text)):
            if isinstance(event, yaml.DocumentStartEvent):
                documents += 1
                if documents > 1:
                    raise refuse(op, "multiple YAML documents in one input")
            if isinstance(event, yaml.AliasEvent):
                raise refuse(op, "YAML aliases are rejected before expansion")
            anchor = getattr(event, "anchor", None)
            if anchor is not None and not isinstance(event, yaml.AliasEvent):
                raise refuse(op, f"YAML anchors are rejected: &{anchor}")
            tag = getattr(event, "tag", None)
            if tag is not None and tag not in SAFE_TAGS:
                raise refuse(op, f"YAML tag rejected: {tag}")
            if isinstance(event, (yaml.MappingStartEvent, yaml.SequenceStartEvent)):
                depth += 1
                if depth > depth_cap:
                    raise refuse(op, f"nesting exceeds the depth cap of {depth_cap}")
            if isinstance(event, (yaml.MappingEndEvent, yaml.SequenceEndEvent)):
                depth -= 1
    except yaml.YAMLError as exc:
        raise fail(op, f"YAML does not parse: {exc}")
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise fail(op, f"YAML does not parse: {exc}")


def dump_yaml(value: object) -> str:
    return yaml.safe_dump(
        value, default_flow_style=False, sort_keys=False, allow_unicode=True, width=88
    )


# ---------------------------------------------------------------------------
# Canonical data
# ---------------------------------------------------------------------------


class Contract:
    def __init__(self, data: dict, data_path: Path) -> None:
        self.data = data
        self.data_path = data_path
        self.stages: list[str] = data["stages"]
        self.items: list[dict] = data["packet-items"]
        self.bounds: dict = data["bounds"]
        self.obliged: dict = data["obliged-artifacts"]
        self.record_keys: list[dict] = data["record-keys"]
        self.schemas: dict = data["schemas"]

    def item(self, key: str) -> dict:
        for entry in self.items:
            if entry["key"] == key:
                return entry
        raise refuse("matrix lookup", f"unknown packet item: {key}")

    def cell(self, item_key: str, stage: str) -> dict:
        return self.item(item_key)["matrix"][stage]

    def include_column(self, stage: str) -> list[dict]:
        return [e for e in self.items if e["matrix"][stage]["status"] == "include"]


def load_contract(data_path: Path, readset: ReadSet) -> Contract:
    readset.allow(data_path)
    raw = readset.read_bytes(data_path)
    parsed = safe_parse(raw, byte_cap=4 * 1024 * 1024, depth_cap=48, op="contract data")
    if not isinstance(parsed, dict) or parsed.get("contract-data-version") != 1:
        raise refuse(
            "contract data",
            "unsupported contract-data-version",
            parsed.get("contract-data-version") if isinstance(parsed, dict) else parsed,
        )
    return Contract(parsed, Path(os.path.realpath(data_path)))


# ---------------------------------------------------------------------------
# Content identity
# ---------------------------------------------------------------------------


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def identity_of_path(path: Path, contract: Contract, readset: ReadSet) -> dict:
    """Path-kind rules: regular file → hashed; directory → expanded once into
    recursive regular files in sorted relative-path order, each pinned
    individually; anything else unpinnable."""
    canonical = Path(os.path.realpath(path))
    readset.check(canonical)
    if not canonical.exists():
        raise fail("identity", f"path does not resolve: {path}")
    mode = canonical.stat().st_mode
    if stat.S_ISREG(mode):
        return {"path": str(path), "id": sha256_bytes(readset.read_bytes(canonical))}
    if stat.S_ISDIR(mode):
        cap = contract.bounds["directory-expansion-max-descendants"]
        entries: list[tuple[str, Path]] = []
        for root, dirs, files in os.walk(canonical, followlinks=False):
            dirs.sort()
            for name in sorted(files):
                child = Path(root) / name
                rel = child.relative_to(canonical).as_posix()
                if child.is_symlink():
                    raise fail("identity", f"symlinked descendant is unpinnable: {rel}")
                if not stat.S_ISREG(child.stat().st_mode):
                    raise fail(
                        "identity", f"non-regular descendant is unpinnable: {rel}"
                    )
                entries.append((rel, child))
        entries.sort(key=lambda pair: pair[0])
        if len(entries) > cap:
            raise refuse(
                "identity",
                f"directory expands to {len(entries)} descendants, past the cap of {cap}: {path}",
            )
        manifest = [
            {"relpath": rel, "id": sha256_bytes(readset.read_bytes(child))}
            for rel, child in entries
        ]
        return {"path": str(path), "manifest": manifest}
    raise fail(
        "identity",
        f"path is neither a regular file nor a directory — unpinnable: {path}",
    )


def cmd_identity(args: argparse.Namespace) -> int:
    readset = ReadSet()
    contract = load_contract(Path(args.data), readset)
    results = []
    total_bytes = 0
    for raw_path in args.paths:
        path = Path(raw_path)
        readset.allow(path)
        entry = identity_of_path(path, contract, readset)
        if "manifest" in entry:
            for item in entry["manifest"]:
                total_bytes += (
                    (Path(os.path.realpath(path)) / item["relpath"]).stat().st_size
                )
        else:
            total_bytes += Path(os.path.realpath(path)).stat().st_size
        results.append(entry)
    if args.as_evidence:
        cap = contract.bounds["named-evidence-expanded-bytes"]
        if total_bytes > cap:
            raise refuse(
                "identity",
                f"named evidence set expands to {total_bytes} bytes, past the {cap}-byte bound",
            )
    sys.stdout.write(dump_yaml({"identities": results, "total-bytes": total_bytes}))
    return EXIT_PASS


# ---------------------------------------------------------------------------
# Run-state store
# ---------------------------------------------------------------------------


class Store:
    def __init__(self, root: Path, contract: Contract, readset: ReadSet) -> None:
        self.root = Path(os.path.realpath(root))
        self.contract = contract
        self.readset = readset
        readset.allow(self.root)

    def _files(self) -> list[Path]:
        if not self.root.is_dir():
            raise StoreReadLoss(
                f"store read failed: store root is not a directory: {self.root}"
            )
        return sorted(p for p in self.root.iterdir() if p.suffix == ".yaml")

    def items(self) -> list[dict]:
        out = []
        for path in self._files():
            raw = self.readset.read_bytes(path)
            parsed = safe_parse(
                raw,
                byte_cap=self.contract.bounds["parse-bytes"],
                depth_cap=self.contract.bounds["parse-depth"],
                op=f"run-state item {path.name}",
            )
            validate_runstate_item(parsed, self.contract)
            out.append(parsed)
        out.sort(key=lambda item: item["seq"])
        return out

    def find(self, kind: str, stage: str | None = None) -> list[dict]:
        return [
            i
            for i in self.items()
            if i["kind"] == kind and (stage is None or i.get("stage") == stage)
        ]

    def require(self, kind: str, stage: str | None = None) -> dict:
        found = self.find(kind, stage)
        if not found:
            where = f"{kind}" + (f" for stage {stage}" if stage else "")
            raise StoreReadLoss(
                f"store read failed: required run-state item absent: {where}"
            )
        return found[-1]

    def next_seq(self) -> int:
        existing = self.items()
        return (max(i["seq"] for i in existing) + 1) if existing else 0

    def write(self, item: dict) -> Path:
        validate_runstate_item(item, self.contract)
        echoes = [i for i in self.items() if i["kind"] == "echo"]
        if item["kind"] == "echo":
            if echoes:
                raise refuse(
                    "store write", "echo item already present; one echo per store"
                )
            if item["seq"] != 0:
                raise refuse(
                    "store write",
                    "the echo item must be seq 0, the store's first write",
                )
        else:
            if not echoes:
                raise StoreReadLoss(
                    "store read failed: no echo item; store was never initialized"
                )
            if item["run"] != echoes[0]["run"]:
                raise fail(
                    "store write",
                    f"run identifier mismatch: item {item['run']!r} vs echo {echoes[0]['run']!r}",
                )
        name = f"{item['seq']:03d}-{item['kind']}"
        if item.get("stage"):
            name += f"-{item['stage']}"
        path = self.root / f"{name}.yaml"
        if path.exists():
            raise fail("store write", f"item file already exists: {path.name}")
        tmp = path.with_suffix(".tmp")
        tmp.write_bytes(dump_yaml(item).encode("utf-8"))
        os.replace(tmp, path)
        return path


def validate_runstate_item(item: object, contract: Contract) -> None:
    op = "run-state item validation"
    schema = contract.schemas[RUNSTATE_SCHEMA]
    if not isinstance(item, dict):
        raise fail(op, "item is not a mapping", item)
    keys = {entry["key"] for entry in schema["keys"]}
    unknown = set(item) - keys
    if unknown:
        raise fail(op, f"unknown keys rejected: {sorted(unknown)}")
    for entry in schema["keys"]:
        key = entry["key"]
        if entry.get("required") and key not in item:
            raise fail(op, f"missing required key: {key}")
    if item["schema"] != RUNSTATE_SCHEMA:
        raise refuse(op, f"unsupported schema version: {item['schema']!r}")
    kinds = next(e["enum"] for e in schema["keys"] if e["key"] == "kind")
    if item["kind"] not in kinds:
        raise fail(op, f"unknown kind: {item['kind']!r}")
    if not isinstance(item["seq"], int) or item["seq"] < 0:
        raise fail(op, "seq must be a non-negative integer", item["seq"])
    if item["kind"] in {
        "envelope",
        "concerns-amendment",
        "brief-render",
    } and not item.get("stage"):
        raise fail(op, f"kind {item['kind']} requires a stage")
    if item.get("stage") is not None and item["stage"] not in contract.stages:
        raise fail(op, f"unknown stage: {item['stage']!r}")
    body = item["body"]
    if not isinstance(body, dict):
        raise fail(op, "body is not a mapping", body)
    expected = set(schema["body-keys"][item["kind"]])
    actual = set(body)
    if actual != expected:
        raise fail(
            op,
            f"body keys for kind {item['kind']} must be exactly {sorted(expected)}",
            sorted(actual),
        )
    if item["kind"] == "envelope":
        # written envelopes revalidate against the envelope schema shape
        validate_envelope_shape(body["document"], contract)


# ---------------------------------------------------------------------------
# Envelope validation
# ---------------------------------------------------------------------------


def _is_not_produced(value: object) -> bool:
    return isinstance(value, str) and value.startswith("not produced:")


def _check_record(
    record: object, contract: Contract, allowed_wordings: list[str], stage: str
) -> None:
    op = f"record validation ({stage})"
    if not isinstance(record, dict):
        raise fail(op, "record is not a mapping", record)
    spec = {entry["key"]: entry for entry in contract.record_keys}
    unknown = set(record) - set(spec)
    if unknown:
        raise fail(op, f"unknown record keys rejected: {sorted(unknown)}")
    for key, entry in spec.items():
        if entry["required"] and key not in record:
            raise fail(op, f"record missing required key: {key}", record.get("option"))
        if key in record and "enum" in entry and record[key] not in entry["enum"]:
            raise fail(
                op, f"record key {key} must be one of {entry['enum']}", record[key]
            )
    if record["status"] != "active":
        raise fail(
            op,
            "a stage-produced record must have status `active`; `revived` is orchestrator historization only",
            record["status"],
        )
    prune_bases = {"constraint", "equivalence", "dominance", "survivor budget"}
    recommend_bases = {
        "post-prune filter",
        "post-prune dominance",
        "post-prune collapse",
        "only-serious-option rival",
    }
    basis = record["cut-basis"]
    if stage == "prune" and basis not in prune_bases:
        raise fail(op, f"cut basis {basis!r} is not a Prune basis")
    if stage == "recommend" and basis not in recommend_bases:
        raise fail(op, f"cut basis {basis!r} is not a Recommend disposition basis")
    if record["option"] not in allowed_wordings:
        raise fail(
            op,
            "record `option` is not byte-identical to any stored original wording — paraphrase rejected",
            record["option"],
        )
    prov = record.get("evidence-provenance")
    if prov is not None:
        if not isinstance(prov, list) or not prov:
            raise fail(
                op,
                "evidence-provenance must be a non-empty list of {source, retrieved-at}",
                prov,
            )
        for ref in prov:
            if not isinstance(ref, dict) or set(ref) != {"source", "retrieved-at"}:
                raise fail(
                    op,
                    "evidence-provenance entries must be exactly {source, retrieved-at}",
                    ref,
                )


def _check_option_list(value: object, op: str) -> list[dict]:
    if not isinstance(value, list):
        raise fail(op, "option list must be a list", value)
    for opt in value:
        if not isinstance(opt, dict):
            raise fail(op, "option entries must be mappings", opt)
        unknown = set(opt) - {"wording", "provenance", "insertion"}
        if unknown:
            raise fail(op, f"unknown option keys rejected: {sorted(unknown)}")
        if not isinstance(opt.get("wording"), str) or not opt["wording"].strip():
            raise fail(op, "option wording must be a non-empty string", opt)
        if opt.get("provenance") not in PROVENANCE_FLAGS:
            raise fail(
                op,
                f"option provenance must be one of {sorted(PROVENANCE_FLAGS)}",
                opt.get("provenance"),
            )
    return value


def _check_retrievals(value: object, contract: Contract, op: str) -> list[dict]:
    if value == "none":
        return []
    if not isinstance(value, list):
        raise fail(op, "retrievals must be `none` or a list", value)
    cap = contract.bounds["per-stage-retrievals"]
    if len(value) > cap:
        raise fail(
            op, f"retrievals list of {len(value)} exceeds the per-stage cap of {cap}"
        )
    for entry in value:
        if not isinstance(entry, dict) or set(entry) != {
            "source",
            "retrieved-at",
            "fact",
            "concerns",
        }:
            raise fail(
                op,
                "retrieval entries must be exactly {source, retrieved-at, fact, concerns}",
                entry,
            )
        concerns = entry["concerns"]
        if concerns != "candidate-neutral" and (
            not isinstance(concerns, list)
            or not concerns
            or not all(isinstance(c, str) for c in concerns)
        ):
            raise fail(
                op,
                "concerns must be `candidate-neutral` or a non-empty list of candidate wordings",
                concerns,
            )
    return value


def validate_envelope_shape(document: object, contract: Contract) -> dict:
    """Schema-shape checks that need no store context."""
    op = "envelope validation"
    schema = contract.schemas[ENVELOPE_SCHEMA]
    if not isinstance(document, dict):
        raise fail(op, "envelope is not a mapping", document)
    keys = {entry["key"] for entry in schema["keys"]}
    unknown = set(document) - keys
    if unknown:
        raise fail(op, f"unknown keys rejected: {sorted(unknown)}")
    missing = keys - set(document)
    if missing:
        raise fail(op, f"missing required keys: {sorted(missing)}")
    if document["schema"] != ENVELOPE_SCHEMA:
        raise refuse(op, f"unsupported schema version: {document['schema']!r}")
    stage = document["stage"]
    if stage not in contract.stages:
        raise fail(op, f"unknown stage: {stage!r}")
    status = document["status"]
    if not isinstance(status, str) or not status.strip():
        raise fail(op, "status must be a non-empty string", status)
    artifacts = document["artifacts"]
    if not isinstance(artifacts, dict):
        raise fail(op, "artifacts must be a mapping", artifacts)
    obliged = contract.obliged[stage]
    expected = {entry["key"] for entry in obliged}
    if set(artifacts) != expected:
        raise fail(
            op,
            f"artifacts must carry exactly the stage's obliged keys {sorted(expected)}",
            sorted(artifacts),
        )
    for entry in obliged:
        value = artifacts[entry["key"]]
        if _is_not_produced(value):
            if status == "completed" and entry["required"] == "always":
                raise fail(
                    op,
                    f"a completed stage cannot mark an always-obliged artifact not produced: {entry['key']}",
                )
            continue
        if value == "not applicable":
            if entry["required"] != "conditional":
                raise fail(
                    op,
                    f"only conditional artifacts may be `not applicable`: {entry['key']}",
                )
            continue
        _check_artifact_shape(entry, value, stage)
    _check_retrievals(document["retrievals"], contract, op)
    encounters = document["encounters"]
    if encounters != "none":
        if not isinstance(encounters, list):
            raise fail(op, "encounters must be `none` or a list", encounters)
        for entry in encounters:
            if not isinstance(entry, dict) or set(entry) != {"kind", "where", "note"}:
                raise fail(
                    op, "encounter entries must be exactly {kind, where, note}", entry
                )
            if entry["kind"] not in ENCOUNTER_KINDS:
                raise fail(
                    op,
                    f"encounter kind must be one of {sorted(ENCOUNTER_KINDS)}",
                    entry["kind"],
                )
    pins = document["pins"]
    if pins != "none":
        if not isinstance(pins, list):
            raise fail(op, "pins must be `none` or a list", pins)
        for entry in pins:
            if not isinstance(entry, dict) or set(entry) != {"surface", "id"}:
                raise fail(op, "pin entries must be exactly {surface, id}", entry)
    if not isinstance(document["model"], str) or not document["model"].strip():
        raise fail(
            op,
            "model must be a non-empty string (`unknown` allowed)",
            document["model"],
        )
    return document


def _check_artifact_shape(entry: dict, value: object, stage: str) -> None:
    op = f"artifact validation ({stage}.{entry['key']})"
    shape = entry["shape"]
    if shape == "text":
        if not isinstance(value, str) or not value.strip():
            raise fail(op, "text artifact must be a non-empty string", value)
    elif shape == "option-list":
        _check_option_list(value, op)
    elif shape == "record-list":
        if not isinstance(value, list):
            raise fail(op, "record list must be a list", value)
        # byte-identity checked with store context in validate_envelope_against_store
    elif shape == "overflow":
        if not isinstance(value, dict) or set(value) != {"disclosure", "blocked-cuts"}:
            raise fail(op, "overflow must be exactly {disclosure, blocked-cuts}", value)
        if not isinstance(value["blocked-cuts"], list):
            raise fail(op, "blocked-cuts must be a list", value["blocked-cuts"])
        for cut in value["blocked-cuts"]:
            if not isinstance(cut, dict) or set(cut) != {
                "option",
                "unpriced-trade",
                "why-blocked",
            }:
                raise fail(
                    op,
                    "blocked-cut entries must be exactly {option, unpriced-trade, why-blocked}",
                    cut,
                )
    elif shape == "consequence-list":
        if not isinstance(value, list):
            raise fail(op, "consequence list must be a list", value)
        for row in value:
            if not isinstance(row, dict) or set(row) != {
                "option",
                "constraint",
                "consequence",
            }:
                raise fail(
                    op,
                    "consequence entries must be exactly {option, constraint, consequence}",
                    row,
                )
    elif shape == "leans":
        if not isinstance(value, dict) or set(value) != {
            "agent-first-lean",
            "user-visible-lean",
        }:
            raise fail(
                op,
                "registered-leans must be exactly {agent-first-lean, user-visible-lean}",
                value,
            )
    elif shape == "seed":
        if not isinstance(value, dict) or set(value) != {
            "handle",
            "core-idea",
            "distinct-bet",
        }:
            raise fail(
                op,
                "provisional seed must be exactly {handle, core-idea, distinct-bet}",
                value,
            )
    else:
        raise refuse(op, f"unknown artifact shape in contract data: {shape}")


def _stored_field_wordings(store: Store) -> list[str]:
    """The input field Prune cut from: Generate's validated field, else the
    supplied candidate set (closed-to-widening)."""
    envelopes = store.find("envelope", "generate")
    if envelopes:
        field = envelopes[-1]["body"]["document"]["artifacts"]["field"]
        if isinstance(field, list):
            return [opt["wording"] for opt in field]
    decomposition = store.require("decomposition")
    return [c["wording"] for c in decomposition["body"]["candidates"]]


def _stored_survivor_wordings(store: Store) -> list[str]:
    envelope = store.require("envelope", "prune")
    survivors = envelope["body"]["document"]["artifacts"]["survivors"]
    if not isinstance(survivors, list):
        raise StoreReadLoss("store read failed: prune envelope holds no survivors list")
    return [opt["wording"] for opt in survivors]


def _accepted_retrievals(store: Store) -> list[dict]:
    """Every accepted retrieval with its effective concerns (amendments applied)."""
    facts: list[dict] = []
    for item in store.find("envelope"):
        document = item["body"]["document"]
        retrievals = document["retrievals"]
        if retrievals == "none":
            continue
        for entry in retrievals:
            facts.append(
                {
                    "producing-stage": document["stage"],
                    "source": entry["source"],
                    "retrieved-at": entry["retrieved-at"],
                    "fact": entry["fact"],
                    "concerns": entry["concerns"],
                }
            )
    for item in store.find("concerns-amendment"):
        for amendment in item["body"]["amendments"]:
            ref = amendment["retrieval"]
            for factentry in facts:
                if (
                    factentry["producing-stage"] == ref["producing-stage"]
                    and factentry["source"] == ref["source"]
                    and factentry["retrieved-at"] == ref["retrieved-at"]
                ):
                    base = factentry["concerns"]
                    names = [] if base == "candidate-neutral" else list(base)
                    if amendment["option"] not in names:
                        names.append(amendment["option"])
                    factentry["concerns"] = names
    return facts


def _resolve_citations(document: dict, store: Store) -> list[dict]:
    """Every record citation must resolve to a stored or same-envelope
    retrieval. Returns the concerns amendments acceptance owes."""
    op = "record citation resolution"
    stage = document["stage"]
    stored = _accepted_retrievals(store)
    same_envelope = document["retrievals"]
    local = (
        []
        if same_envelope == "none"
        else [
            {
                "producing-stage": stage,
                "source": e["source"],
                "retrieved-at": e["retrieved-at"],
            }
            for e in same_envelope
        ]
    )
    known = {(f["producing-stage"], f["source"], f["retrieved-at"]) for f in stored}
    known |= {(e["producing-stage"], e["source"], e["retrieved-at"]) for e in local}
    amendments: list[dict] = []
    for key in ("exclusion-records", "disposition-records"):
        records = document["artifacts"].get(key)
        if not isinstance(records, list):
            continue
        for record in records:
            for ref in record.get("evidence-provenance") or []:
                matches = [
                    k
                    for k in known
                    if k[1] == ref["source"] and k[2] == ref["retrieved-at"]
                ]
                if not matches:
                    raise fail(
                        op,
                        "evidence-provenance cites no stored or same-envelope retrieval",
                        ref,
                    )
                producing = matches[0][0]
                amendments.append(
                    {
                        "retrieval": {
                            "producing-stage": producing,
                            "source": ref["source"],
                            "retrieved-at": ref["retrieved-at"],
                        },
                        "option": record["option"],
                    }
                )
    return amendments


def _is_order_preserving_subsequence(survivors: list[str], field: list[str]) -> bool:
    it = iter(field)
    return all(any(word == candidate for candidate in it) for word in survivors)


def validate_envelope_against_store(
    document: dict, store: Store, contract: Contract
) -> list[dict]:
    """Full acceptance validation; returns the concerns amendments owed."""
    stage = document["stage"]
    artifacts = document["artifacts"]
    if stage == "prune":
        field = _stored_field_wordings(store)
        survivors = artifacts.get("survivors")
        if isinstance(survivors, list):
            wordings = [opt["wording"] for opt in survivors]
            if not _is_order_preserving_subsequence(wordings, list(field)):
                raise fail(
                    "envelope validation (prune)",
                    "survivors are not an order-preserving subsequence of the input field — Prune cuts, never reorders",
                    wordings,
                )
        records = artifacts.get("exclusion-records")
        if isinstance(records, list):
            for record in records:
                _check_record(record, contract, field, "prune")
    if stage == "recommend":
        records = artifacts.get("disposition-records")
        if isinstance(records, list):
            allowed = _stored_survivor_wordings(store)
            for record in records:
                _check_record(record, contract, allowed, "recommend")
    return _resolve_citations(document, store)


def cmd_validate_envelope(args: argparse.Namespace) -> int:
    readset = ReadSet()
    contract = load_contract(Path(args.data), readset)
    envelope_path = readset.allow(Path(args.envelope))
    raw = readset.read_bytes(envelope_path)
    document = safe_parse(
        raw,
        byte_cap=contract.bounds["parse-bytes"],
        depth_cap=contract.bounds["parse-depth"],
        op="envelope",
    )
    validate_envelope_shape(document, contract)
    if args.stage and document["stage"] != args.stage:
        raise fail(
            "envelope validation",
            f"envelope stage {document['stage']!r} does not match the dispatched stage {args.stage!r}",
        )
    store = Store(Path(args.store), contract, readset)
    amendments = validate_envelope_against_store(document, store, contract)
    if args.accept:
        seq = store.next_seq()
        run = store.require("echo")["run"]
        store.write(
            {
                "schema": RUNSTATE_SCHEMA,
                "kind": "envelope",
                "run": run,
                "seq": seq,
                "stage": document["stage"],
                "body": {"document": document},
            }
        )
        if amendments:
            store.write(
                {
                    "schema": RUNSTATE_SCHEMA,
                    "kind": "concerns-amendment",
                    "run": run,
                    "seq": seq + 1,
                    "stage": document["stage"],
                    "body": {"amendments": amendments},
                }
            )
    print(
        f"envelope valid: stage={document['stage']} status={document['status']!r}"
        + (
            f" accepted with {len(amendments)} concerns amendment(s)"
            if args.accept
            else ""
        )
    )
    return EXIT_PASS


# ---------------------------------------------------------------------------
# Stage-brief rendering
# ---------------------------------------------------------------------------


def _effective_survivor_share(facts: list[dict], survivors: list[str]) -> list[dict]:
    out = []
    for fact in facts:
        concerns = fact["concerns"]
        if concerns == "candidate-neutral":
            out.append(fact)
        elif isinstance(concerns, list) and all(name in survivors for name in concerns):
            out.append(fact)
    return out


def _method_text(stage: str, contract: Contract, readset: ReadSet) -> str:
    methods_path = contract.data_path.parent / "methods.md"
    readset.allow(methods_path)
    text = readset.read_bytes(methods_path).decode("utf-8")
    start = f"<!-- method:{stage} -->"
    end = f"<!-- /method:{stage} -->"
    if start not in text or end not in text:
        raise fail("method extraction", f"markers for {stage} not found in methods.md")
    return text.split(start, 1)[1].split(end, 1)[0].strip()


def _render_packet_item(
    key: str, stage: str, store: Store, contract: Contract, readset: ReadSet
) -> str | None:
    """Render one packet item's content from byte-exact store items.
    Returns None when a conditional item has nothing to carry."""
    echo_fields = store.require("echo")["body"]["fields"]
    decomposition = store.require("decomposition")["body"]

    def echo_field(name: str) -> object:
        if name not in echo_fields:
            raise StoreReadLoss(f"store read failed: echo field absent: {name}")
        return echo_fields[name]

    if key == "frame":
        return dump_yaml({"frame": decomposition["frame"]})
    if key == "field-mode":
        return dump_yaml({"field-mode": echo_field("field-mode")})
    if key == "constraints":
        return dump_yaml({"constraints": echo_field("constraints")})
    if key == "values":
        return dump_yaml({"values": decomposition["values"]})
    if key == "soft-prefs":
        return dump_yaml({"soft-prefs": decomposition["soft-prefs"]})
    if key == "evidence":
        pins = store.require("pins")["body"]
        return dump_yaml(
            {
                "evidence-inputs": echo_field("evidence-inputs"),
                "evidence-authorization": echo_field("evidence-authorization"),
                "pinned-evidence-identifiers": pins["evidence"],
            }
        )
    if key == "budget":
        return dump_yaml({"survivor-budget": echo_field("survivor-budget")})
    if key == "seeds":
        seeds = [
            c
            for c in decomposition["candidates"]
            if c["provenance-flag"] == "user-seed"
        ]
        return dump_yaml(
            {
                "seeds": [
                    {"wording": c["wording"], "provenance": c["provenance-flag"]}
                    for c in seeds
                ]
            }
        )
    if key == "field":
        envelopes = store.find("envelope", "generate")
        if envelopes:
            artifacts = envelopes[-1]["body"]["document"]["artifacts"]
            return dump_yaml(
                {
                    "field": artifacts["field"],
                    "fixed-points-line": artifacts["fixed-points-line"],
                }
            )
        return dump_yaml(
            {
                "field": [
                    {"wording": c["wording"], "provenance": c["provenance-flag"]}
                    for c in decomposition["candidates"]
                ],
                "fixed-points-line": "Generate not run: closed-to-widening",
            }
        )
    if key == "survivors":
        artifacts = store.require("envelope", "prune")["body"]["document"]["artifacts"]
        mode = echo_field("field-mode")
        mode_value = mode.get("value") if isinstance(mode, dict) else mode
        provenance = (
            "user-supplied order — may evidence lean"
            if mode_value == "closed-to-widening"
            else "Generate-produced order — non-evaluative; never evidence of user lean"
        )
        return dump_yaml(
            {"survivors": artifacts["survivors"], "order-provenance": provenance}
        )
    if key == "authority-notes-survivor":
        survivors = _stored_survivor_wordings(store)
        notes = [
            {"option": c["wording"], "authority-note": c["authority-note"]}
            for c in decomposition["candidates"]
            if c["wording"] in survivors
            and c.get("authority-note") not in (None, "absent")
        ]
        return dump_yaml({"authority-notes": notes})
    if key == "authority-notes-excluded":
        survivors = set(_stored_survivor_wordings(store))
        excluded_by_recommend = set()
        for item in store.find("envelope", "recommend"):
            records = item["body"]["document"]["artifacts"].get("disposition-records")
            if isinstance(records, list):
                excluded_by_recommend |= {r["option"] for r in records}
        notes = [
            {"option": c["wording"], "authority-note": c["authority-note"]}
            for c in decomposition["candidates"]
            if (c["wording"] not in survivors or c["wording"] in excluded_by_recommend)
            and c.get("authority-note") not in (None, "absent")
        ]
        return dump_yaml({"authority-notes": notes})
    if key == "records":
        records: list[dict] = []
        for stage_name in ("prune", "recommend"):
            for item in store.find("envelope", stage_name):
                for artifact_key in ("exclusion-records", "disposition-records"):
                    value = item["body"]["document"]["artifacts"].get(artifact_key)
                    if isinstance(value, list):
                        records.extend(r for r in value if r["status"] == "active")
        return dump_yaml({"records": records})
    if key == "retrievals":
        facts = _accepted_retrievals(store)
        cell = contract.cell("retrievals", stage)
        if cell.get("qualifier") == "survivor share":
            facts = _effective_survivor_share(facts, _stored_survivor_wordings(store))
        return dump_yaml({"retrievals": facts})
    if key == "overflow":
        envelopes = store.find("envelope", "prune")
        if not envelopes:
            return None
        value = envelopes[-1]["body"]["document"]["artifacts"].get(
            "overflow-disclosure"
        )
        if not isinstance(value, dict):
            return None
        # existence and identity only — Prune's per-cut reasoning never crosses
        return dump_yaml(
            {
                "overflow": {
                    "disclosure": value["disclosure"],
                    "blocked-trades": [
                        {
                            "option": cut["option"],
                            "unpriced-trade": cut["unpriced-trade"],
                        }
                        for cut in value["blocked-cuts"]
                    ],
                }
            }
        )
    if key == "consequences":
        artifacts = store.require("envelope", "shape")["body"]["document"]["artifacts"]
        return dump_yaml(
            {"constraint-consequences": artifacts["constraint-consequences"]}
        )
    if key == "surface":
        envelopes = store.find("envelope", "shape")
        if stage == "recommend":
            artifacts = store.require("envelope", "shape")["body"]["document"][
                "artifacts"
            ]
            return dump_yaml({"comparison-surface": artifacts["comparison-surface"]})
        if not envelopes:
            return None
        value = envelopes[-1]["body"]["document"]["artifacts"].get("comparison-surface")
        if not isinstance(value, str) or _is_not_produced(value):
            return None
        return dump_yaml({"comparison-surface": value})
    if key == "close":
        envelopes = store.find("envelope", "recommend")
        if not envelopes:
            return None
        value = envelopes[-1]["body"]["document"]["artifacts"].get("close")
        if not isinstance(value, str) or _is_not_produced(value):
            return None
        return dump_yaml({"close": value})
    if key == "terminal-claim":
        items = store.find("terminal-claim")
        if not items:
            return None
        return dump_yaml({"terminal-claim": items[-1]["body"]})
    if key == "stakes":
        return dump_yaml({"stakes": decomposition["stakes"]})
    if key == "method":
        return _method_text(stage, contract, readset)
    if key == "pin":
        pins = store.require("pins")["body"]
        constituent = {
            "generate": "ideate",
            "shape": "option-shaping",
            "recommend": "making-recommendations",
        }[stage]
        return dump_yaml(
            {"constituent": constituent, "pins": pins["constituents"][constituent]}
        )
    raise refuse("brief render", f"no renderer for packet item {key!r}")


def render_brief(
    stage: str,
    store: Store,
    contract: Contract,
    readset: ReadSet,
    requested: list[str] | None,
) -> str:
    column = [entry["key"] for entry in contract.include_column(stage)]
    if requested is not None:
        off_column = [key for key in requested if key not in column]
        if off_column:
            raise refuse(
                "brief render",
                f"off-column packet item(s) requested into the {stage} brief: {off_column} — "
                f"the {stage} column includes only {column}",
            )
        keys = [key for key in column if key in requested]
    else:
        keys = column
    sections = []
    for key in keys:
        content = _render_packet_item(key, stage, store, contract, readset)
        if content is None:
            continue
        sections.append(f"## packet: {key}\n\n{content.rstrip()}\n")
    obliged_lines = []
    for entry in contract.obliged[stage]:
        shape = contract.data["artifact-shapes"][entry["shape"]]
        obliged_lines.append(f"  - `{entry['key']}` ({entry['required']}) — {shape}")
    template = contract.data["stage-brief-template"]
    extras = contract.data["brief-extras"][stage]
    brief = template.format(
        stage=stage,
        packet="\n".join(sections).rstrip(),
        obliged="\n".join(obliged_lines),
        **{
            "retrieval-cap": contract.bounds["per-stage-retrievals"],
            "extras": extras.rstrip(),
        },
    )
    return brief


def cmd_render_brief(args: argparse.Namespace) -> int:
    readset = ReadSet()
    contract = load_contract(Path(args.data), readset)
    if args.stage not in contract.stages:
        raise refuse("brief render", f"unknown stage: {args.stage!r}")
    store = Store(Path(args.store), contract, readset)
    requested = args.items.split(",") if args.items else None
    brief = render_brief(args.stage, store, contract, readset, requested)
    brief_id = sha256_bytes(brief.encode("utf-8"))
    run = store.require("echo")["run"]
    store.write(
        {
            "schema": RUNSTATE_SCHEMA,
            "kind": "brief-render",
            "run": run,
            "seq": store.next_seq(),
            "stage": args.stage,
            "body": {"brief-id": brief_id},
        }
    )
    sys.stderr.write(f"brief-id: {brief_id} (recorded in run state before dispatch)\n")
    sys.stdout.write(brief)
    return EXIT_PASS


# ---------------------------------------------------------------------------
# Store commands
# ---------------------------------------------------------------------------


def cmd_init_store(args: argparse.Namespace) -> int:
    readset = ReadSet()
    contract = load_contract(Path(args.data), readset)
    root = Path(args.store)
    if root.exists():
        raise refuse(
            "store init",
            f"store path already exists — retire the orphan via `trash` first: {root}",
        )
    parent = Path(os.path.realpath(root.parent))
    readset.allow(parent)
    root.mkdir(mode=0o700)
    store = Store(root, contract, readset)
    body_raw = readset.allow(Path(args.echo_body))
    body = safe_parse(
        readset.read_bytes(body_raw),
        byte_cap=contract.bounds["parse-bytes"],
        depth_cap=contract.bounds["parse-depth"],
        op="echo body",
    )
    item = {
        "schema": RUNSTATE_SCHEMA,
        "kind": "echo",
        "run": args.run,
        "seq": 0,
        "body": body,
    }
    store.write(item)
    print(f"store initialized: {root} (echo seq 0, run {args.run})")
    return EXIT_PASS


def cmd_write_item(args: argparse.Namespace) -> int:
    readset = ReadSet()
    contract = load_contract(Path(args.data), readset)
    store = Store(Path(args.store), contract, readset)
    body_path = readset.allow(Path(args.body))
    body = safe_parse(
        readset.read_bytes(body_path),
        byte_cap=contract.bounds["parse-bytes"],
        depth_cap=contract.bounds["parse-depth"],
        op="item body",
    )
    run = store.require("echo")["run"]
    item = {
        "schema": RUNSTATE_SCHEMA,
        "kind": args.kind,
        "run": run,
        "seq": store.next_seq(),
        "body": body,
    }
    if args.stage:
        item["stage"] = args.stage
    path = store.write(item)
    print(f"item written: {path.name}")
    return EXIT_PASS


def cmd_validate_runstate(args: argparse.Namespace) -> int:
    readset = ReadSet()
    contract = load_contract(Path(args.data), readset)
    item_path = readset.allow(Path(args.item))
    parsed = safe_parse(
        readset.read_bytes(item_path),
        byte_cap=contract.bounds["parse-bytes"],
        depth_cap=contract.bounds["parse-depth"],
        op="run-state item",
    )
    validate_runstate_item(parsed, contract)
    print(f"run-state item valid: kind={parsed['kind']} seq={parsed['seq']}")
    return EXIT_PASS


# ---------------------------------------------------------------------------
# Capsule validation
# ---------------------------------------------------------------------------


def _strip_fences(text: str) -> str:
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "\n".join(lines[1:-1]) + "\n"
    return text if text.endswith("\n") else text + "\n"


def validate_capsule_text(text: str, contract: Contract) -> dict:
    op = "capsule validation"
    body = _strip_fences(text)
    raw = body.encode("utf-8")
    cap = contract.bounds["capsule-bytes"]
    if len(raw) > cap:
        raise refuse(
            op,
            f"pasted capsule of {len(raw)} bytes exceeds the {cap}-byte whole-capsule bound",
        )
    lines = body.splitlines(keepends=True)
    terminator_index = None
    for index in range(len(lines) - 1, -1, -1):
        if lines[index].startswith("capsule-complete:"):
            terminator_index = index
            break
    if terminator_index is None:
        raise fail(
            op,
            "no completeness terminator — a terminator-less paste is incomplete, never resumed from",
        )
    trailing = "".join(lines[terminator_index + 1 :]).strip()
    if trailing:
        raise fail(op, "capsule-complete must be the final key", trailing)
    declared = lines[terminator_index].split(":", 1)[1].strip()
    prefix = "".join(lines[:terminator_index]).encode("utf-8")
    actual = sha256_bytes(prefix)
    if declared != actual:
        raise fail(
            op,
            f"completeness terminator mismatch — the document is truncated or altered: declared {declared[:12]}…, actual {actual[:12]}…",
        )
    parsed = safe_parse(
        raw, byte_cap=cap, depth_cap=contract.bounds["parse-depth"], op=op
    )
    if not isinstance(parsed, dict):
        raise fail(op, "capsule is not a mapping", parsed)
    schema = contract.schemas[CAPSULE_SCHEMA]
    keys = {entry["key"] for entry in schema["keys"]}
    unknown = set(parsed) - keys
    if unknown:
        raise fail(op, f"unknown keys rejected: {sorted(unknown)}")
    missing = keys - set(parsed)
    if missing:
        raise fail(op, f"missing required keys: {sorted(missing)}")
    if parsed["schema"] != CAPSULE_SCHEMA:
        raise refuse(
            op,
            f"unsupported capsule schema version — resumes only through a shipped migration: {parsed['schema']!r}",
        )
    return parsed


def cmd_validate_capsule(args: argparse.Namespace) -> int:
    readset = ReadSet()
    contract = load_contract(Path(args.data), readset)
    capsule_path = readset.allow(Path(args.capsule))
    raw = capsule_path.read_bytes()
    if len(raw) > contract.bounds["capsule-bytes"] + 16:  # fences allowance
        raise refuse(
            "capsule validation",
            f"pasted capsule of {len(raw)} bytes exceeds the {contract.bounds['capsule-bytes']}-byte ingest bound",
        )
    parsed = validate_capsule_text(raw.decode("utf-8"), contract)
    print(f"capsule valid: run={parsed['run']} terminal={parsed['terminal']!r}")
    return EXIT_PASS


# ---------------------------------------------------------------------------
# Authored-rendering generation and comparison
# ---------------------------------------------------------------------------


def gen_matrix(contract: Contract) -> str:
    header = "| Packet item | Generate | Prune | Shape | Recommend | Contest |"
    divider = "| --- | --- | --- | --- | --- | --- |"
    rows = [header, divider]
    for entry in contract.items:
        cells = []
        for stage in contract.stages:
            cell = entry["matrix"][stage]
            mark = "✓" if cell["status"] == "include" else "—"
            if cell.get("qualifier"):
                mark += f" ({cell['qualifier']})"
            cells.append(mark)
        rows.append(
            f"| `{entry['key']}` — {entry['label']} | " + " | ".join(cells) + " |"
        )
    return "\n".join(rows)


def gen_checklist(contract: Contract, stage: str) -> str:
    include, withhold = [], []
    for entry in contract.items:
        cell = entry["matrix"][stage]
        qualifier = f" ({cell['qualifier']})" if cell.get("qualifier") else ""
        if cell["status"] == "include":
            include.append(f"- `{entry['key']}`{qualifier} — {entry['label']}")
        else:
            withhold.append(f"- `{entry['key']}`{qualifier}")
    title = stage.capitalize()
    return (
        f"**{title} — include:**\n\n"
        + "\n".join(include)
        + f"\n\n**{title} — withhold (exhaustive):**\n\n"
        + "\n".join(withhold)
        + "\n\nAn item on neither list is withheld by default; admitting one is a skill edit, never run-time judgment."
    )


def _gen_keys(entries: list[dict]) -> str:
    lines = []
    for entry in entries:
        parts = ["required" if entry.get("required") else "optional"]
        if "const" in entry:
            parts.append(f"constant `{entry['const']}`")
        if "enum" in entry:
            parts.append("one of: " + ", ".join(entry["enum"]))
        line = f"- `{entry['key']}` — " + "; ".join(parts)
        if entry.get("note"):
            line += f". {entry['note']}"
        lines.append(line)
    return "\n".join(lines)


def gen_record_keys(contract: Contract) -> str:
    return _gen_keys(contract.record_keys)


def gen_schema_keys(contract: Contract, schema_name: str) -> str:
    schema = contract.schemas[schema_name]
    out = _gen_keys(schema["keys"])
    if "body-keys" in schema:
        out += "\n\nBody key sets per kind:\n\n"
        out += "\n".join(
            f"- `{kind}`: {', '.join(f'`{key}`' for key in keys)}"
            for kind, keys in schema["body-keys"].items()
        )
    return out


def gen_bounds(contract: Contract) -> str:
    return "\n".join(f"- `{key}`: {value}" for key, value in contract.bounds.items())


GENERATED_BLOCKS = {
    "stage-packets.md": [
        "matrix",
        "checklist-generate",
        "checklist-prune",
        "checklist-shape",
        "checklist-recommend",
        "checklist-contest",
    ],
    "schemas.md": [
        "record-keys",
        "envelope-keys",
        "runstate-keys",
        "capsule-keys",
        "bounds",
    ],
}


def generate_block(name: str, contract: Contract) -> str:
    if name == "matrix":
        return gen_matrix(contract)
    if name.startswith("checklist-"):
        return gen_checklist(contract, name.removeprefix("checklist-"))
    if name == "record-keys":
        return gen_record_keys(contract)
    if name == "envelope-keys":
        return gen_schema_keys(contract, ENVELOPE_SCHEMA)
    if name == "runstate-keys":
        return gen_schema_keys(contract, RUNSTATE_SCHEMA)
    if name == "capsule-keys":
        return gen_schema_keys(contract, CAPSULE_SCHEMA)
    if name == "bounds":
        return gen_bounds(contract)
    raise refuse("rendering generation", f"unknown generated block: {name}")


def cmd_check_renderings(args: argparse.Namespace) -> int:
    readset = ReadSet()
    contract = load_contract(Path(args.data), readset)
    references = contract.data_path.parent
    readset.allow(references)
    drifted = []
    for filename, blocks in GENERATED_BLOCKS.items():
        path = references / filename
        if not path.exists():
            drifted.append(f"{filename}: file missing")
            continue
        text = readset.read_bytes(path).decode("utf-8")
        for block in blocks:
            start = f"<!-- generated:{block} -->"
            end = f"<!-- /generated:{block} -->"
            if start not in text or end not in text:
                drifted.append(f"{filename}: markers for {block} missing")
                continue
            authored = text.split(start, 1)[1].split(end, 1)[0].strip("\n")
            expected = generate_block(block, contract)
            if authored != expected:
                drifted.append(
                    f"{filename}: block {block} drifted from contract-data.yaml"
                )
                if args.write:
                    text = (
                        text.split(start, 1)[0]
                        + start
                        + "\n"
                        + expected
                        + "\n"
                        + end
                        + text.split(end, 1)[1]
                    )
        if args.write:
            path.write_text(text)
    if drifted and not args.write:
        for line in drifted:
            print(f"DRIFT: {line}", file=sys.stderr)
        raise fail(
            "check-renderings",
            f"{len(drifted)} authored rendering(s) drifted from the canonical data file",
        )
    print(
        "renderings rewritten from contract data"
        if args.write
        else "all authored renderings match the canonical data file"
    )
    return EXIT_PASS


# ---------------------------------------------------------------------------
# Fixtures — the must-block/must-pass set
# ---------------------------------------------------------------------------


def _fixture_store(contract: Contract, readset: ReadSet, root: Path) -> Store:
    root.mkdir(mode=0o700)
    store = Store(root, contract, readset)
    store.write(
        {
            "schema": RUNSTATE_SCHEMA,
            "kind": "echo",
            "run": "fixture-run",
            "seq": 0,
            "body": {
                "invocation-wording-initial": "fixture invocation",
                "directives": [],
                "fields": {
                    "field-mode": {"value": "seed-and-widen", "provenance": "default"},
                    "constraints": {
                        "value": [
                            {"constraint": "must run offline", "price": "no cloud sync"}
                        ],
                        "provenance": "user-supplied",
                    },
                    "evidence-inputs": {
                        "value": "none supplied",
                        "provenance": "absent",
                    },
                    "evidence-authorization": {
                        "value": "supplied evidence inputs and named paths may be inspected by default; no additional sources, web research, or probes are authorized",
                        "provenance": "default",
                    },
                    "survivor-budget": {"value": 4, "provenance": "default"},
                },
            },
        }
    )
    store.write(
        {
            "schema": RUNSTATE_SCHEMA,
            "kind": "decomposition",
            "run": "fixture-run",
            "seq": 1,
            "body": {
                "frame": "choose a note-sync approach for a two-person team",
                "candidates": [
                    {
                        "wording": "Option A — file sync over Syncthing",
                        "provenance-flag": "user-seed",
                        "authority-note": {
                            "text": "user lean: mentioned twice, called it 'the obvious one'",
                            "provenance": "inferred",
                            "span": "fixture span",
                        },
                    },
                ],
                "stakes": "absent",
                "soft-prefs": ["ongoing operating burden matters"],
                "values": [],
            },
        }
    )
    store.write(
        {
            "schema": RUNSTATE_SCHEMA,
            "kind": "pins",
            "run": "fixture-run",
            "seq": 2,
            "body": {
                "constituents": {
                    "ideate": [{"path": "skills/ideate/SKILL.md", "id": "0" * 64}],
                    "option-shaping": [
                        {"path": "skills/option-shaping/SKILL.md", "id": "0" * 64}
                    ],
                    "making-recommendations": [
                        {
                            "path": "skills/making-recommendations/SKILL.md",
                            "id": "0" * 64,
                        }
                    ],
                },
                "method": [{"path": "references/methods.md", "id": "0" * 64}],
                "evidence": [],
                "in-packet": [],
            },
        }
    )
    return store


def _expect(name: str, expected: str, function, results: list) -> None:
    """expected: 'block' (Refusal/ValidationFailure) or 'pass'."""
    try:
        function()
        outcome = "pass"
        detail = ""
    except (Refusal, ValidationFailure, StoreReadLoss) as exc:
        outcome = "block"
        detail = str(exc)
    ok = outcome == expected
    results.append((name, expected, outcome, detail, ok))


def cmd_fixtures(args: argparse.Namespace) -> int:
    readset = ReadSet()
    contract = load_contract(Path(args.data), readset)
    fixtures_dir = Path(os.path.realpath(Path(__file__).parent / "fixtures"))
    readset.allow(fixtures_dir)
    results: list = []
    caps = dict(
        byte_cap=contract.bounds["parse-bytes"],
        depth_cap=contract.bounds["parse-depth"],
    )

    def parse_fixture(name: str):
        raw = readset.read_bytes(fixtures_dir / name)
        return safe_parse(raw, **caps, op=name)

    # must block
    _expect(
        "hostile custom tag rejected",
        "block",
        lambda: parse_fixture("must-block/hostile-tag.yaml"),
        results,
    )
    _expect(
        "anchor/alias expansion rejected",
        "block",
        lambda: parse_fixture("must-block/alias-expansion.yaml"),
        results,
    )
    _expect(
        "over-cap input rejected before parse",
        "block",
        lambda: safe_parse(
            b"key: " + b"a" * contract.bounds["parse-bytes"],
            **caps,
            op="synthesized over-cap",
        ),
        results,
    )
    _expect(
        "over-depth input rejected before parse",
        "block",
        lambda: safe_parse(
            (
                "a: " * 0
                + "[" * (contract.bounds["parse-depth"] + 2)
                + "]" * (contract.bounds["parse-depth"] + 2)
            ).encode(),
            **caps,
            op="synthesized over-depth",
        ),
        results,
    )
    _expect(
        "unknown envelope key rejected",
        "block",
        lambda: validate_envelope_shape(
            parse_fixture("must-block/unknown-key-envelope.yaml"), contract
        ),
        results,
    )
    _expect(
        "read outside the explicit read set refused",
        "block",
        lambda: ReadSet().read_bytes(Path("/etc/passwd")),
        results,
    )

    with tempfile.TemporaryDirectory() as tmp:
        sandbox = Path(tmp)
        readset.allow(sandbox)
        store = _fixture_store(contract, readset, sandbox / "deliberate-run-live")
        _expect(
            "off-column packet item refused (authority notes into prune)",
            "block",
            lambda: render_brief(
                "prune", store, contract, readset, ["field", "authority-notes-survivor"]
            ),
            results,
        )
        _expect(
            "off-column packet item refused (excluded identities into recommend)",
            "block",
            lambda: render_brief(
                "recommend", store, contract, readset, ["authority-notes-excluded"]
            ),
            results,
        )
        _expect(
            "in-column generate brief renders",
            "pass",
            lambda: render_brief("generate", store, contract, readset, None),
            results,
        )
        _expect(
            "inert template-looking prose passes",
            "pass",
            lambda: validate_envelope_shape(
                parse_fixture("must-pass/inert-prose-envelope.yaml"), contract
            ),
            results,
        )

        def path_with_spaces():
            spaced = sandbox / "evidence file with spaces.txt"
            spaced.write_text("inert evidence\n")
            local = ReadSet()
            local.allow(spaced)
            return identity_of_path(spaced, contract, local)

        _expect("authorized path with spaces hashes", "pass", path_with_spaces, results)

        def reordering_prune():
            envelope = parse_fixture("must-pass/inert-prose-envelope.yaml")
            store.write(
                {
                    "schema": RUNSTATE_SCHEMA,
                    "kind": "envelope",
                    "run": "fixture-run",
                    "seq": store.next_seq(),
                    "stage": "generate",
                    "body": {"document": envelope},
                }
            )
            reordered = {
                "schema": ENVELOPE_SCHEMA,
                "stage": "prune",
                "status": "completed",
                "artifacts": {
                    "survivors": [
                        {
                            "wording": "Option B — hosted wiki",
                            "provenance": "generated",
                        },
                        {
                            "wording": "Option A — file sync over Syncthing",
                            "provenance": "user-seed",
                        },
                    ],
                    "exclusion-records": [],
                    "overflow-disclosure": "not applicable",
                },
                "retrievals": "none",
                "encounters": "none",
                "pins": "none",
                "model": "unknown",
            }
            validate_envelope_shape(reordered, contract)
            validate_envelope_against_store(reordered, store, contract)

        _expect(
            "reordering prune envelope rejected (order invariant)",
            "block",
            reordering_prune,
            results,
        )

        def paraphrased_record():
            record = {
                "option": "Option A — Syncthing file sync",  # paraphrase of the stored wording
                "status": "active",
                "delegation": "field narrowing under the echoed budget",
                "predicate-source": "agent-derived proposition",
                "cut-basis": "equivalence",
                "epistemic-status": "fact-established at comparable resolution",
                "reason": "shares its mechanism with the seed",
                "load-bearing-premise": "same sync engine",
                "strongest-case": "written before the kill",
                "revive-if": "the mechanisms turn out to differ",
            }
            _check_record(
                record,
                contract,
                ["Option A — file sync over Syncthing", "Option B — hosted wiki"],
                "prune",
            )

        _expect(
            "paraphrased record option rejected", "block", paraphrased_record, results
        )

        def capsule_roundtrip():
            capsule_keys = [
                entry["key"]
                for entry in contract.schemas[CAPSULE_SCHEMA]["keys"]
                if entry["key"] not in ("schema", "capsule-complete")
            ]
            document = {"schema": CAPSULE_SCHEMA}
            for key in capsule_keys:
                document[key] = (
                    "not produced: fixture"
                    if key not in ("run", "terminal")
                    else "fixture"
                )
            body = dump_yaml(document)
            terminator = sha256_bytes(body.encode("utf-8"))
            validate_capsule_text(body + f"capsule-complete: {terminator}\n", contract)

        _expect(
            "well-formed capsule with terminator validates",
            "pass",
            capsule_roundtrip,
            results,
        )

        def truncated_capsule():
            document = {"schema": CAPSULE_SCHEMA}
            for entry in contract.schemas[CAPSULE_SCHEMA]["keys"]:
                if entry["key"] not in ("schema", "capsule-complete"):
                    document[entry["key"]] = "fixture"
            body = dump_yaml(document)
            terminator = sha256_bytes(body.encode("utf-8"))
            truncated = body[len(body) // 2 :]
            validate_capsule_text(
                truncated + f"capsule-complete: {terminator}\n", contract
            )

        _expect(
            "truncated capsule fails the completeness terminator",
            "block",
            truncated_capsule,
            results,
        )

    width = max(len(name) for name, *_ in results)
    failures = 0
    for name, expected, outcome, detail, ok in results:
        marker = "PASS" if ok else "FAIL"
        if not ok:
            failures += 1
        print(f"{marker}  {name:<{width}}  expected={expected} got={outcome}")
        if not ok and detail:
            print(f"      {detail}")
    print(f"\n{len(results) - failures}/{len(results)} fixtures behaved as required")
    if failures:
        raise fail("fixtures", f"{failures} fixture(s) misbehaved")
    return EXIT_PASS


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deliberate-validate.py",
        description="deliberate bundled validator (see module docstring; exit codes: 0 pass, 1 fail, 2 refusal, 4 store read loss)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser(
        "identity", help="content identifiers for paths (SHA-256, path-kind rules)"
    )
    p.add_argument("--data", required=True)
    p.add_argument(
        "--as-evidence",
        action="store_true",
        help="enforce the named-evidence total expanded-byte bound",
    )
    p.add_argument("paths", nargs="+")
    p.set_defaults(func=cmd_identity)

    p = sub.add_parser(
        "init-store", help="create the run-state store and write the echo item (seq 0)"
    )
    p.add_argument("--data", required=True)
    p.add_argument("--store", required=True)
    p.add_argument("--run", required=True)
    p.add_argument(
        "--echo-body", required=True, help="path to a YAML file with the echo body"
    )
    p.set_defaults(func=cmd_init_store)

    p = sub.add_parser("write-item", help="validate and append one run-state item")
    p.add_argument("--data", required=True)
    p.add_argument("--store", required=True)
    p.add_argument("--kind", required=True)
    p.add_argument("--stage")
    p.add_argument("body", help="path to a YAML file with the item body")
    p.set_defaults(func=cmd_write_item)

    p = sub.add_parser(
        "validate-runstate-item", help="validate one run-state item file"
    )
    p.add_argument("--data", required=True)
    p.add_argument("item")
    p.set_defaults(func=cmd_validate_runstate)

    p = sub.add_parser(
        "render-brief", help="render a stage brief from the store per the matrix column"
    )
    p.add_argument("--data", required=True)
    p.add_argument("--store", required=True)
    p.add_argument("--stage", required=True)
    p.add_argument(
        "--items",
        help="comma-separated packet items (default: the full include column); off-column requests refuse",
    )
    p.set_defaults(func=cmd_render_brief)

    p = sub.add_parser(
        "validate-envelope", help="validate a returned stage envelope against the store"
    )
    p.add_argument("--data", required=True)
    p.add_argument("--store", required=True)
    p.add_argument("--stage", help="the dispatched stage; mismatch fails")
    p.add_argument(
        "--accept",
        action="store_true",
        help="on pass, write the envelope and any concerns amendment to the store",
    )
    p.add_argument("envelope")
    p.set_defaults(func=cmd_validate_envelope)

    p = sub.add_parser(
        "validate-capsule", help="validate a capsule document (fences tolerated)"
    )
    p.add_argument("--data", required=True)
    p.add_argument("capsule")
    p.set_defaults(func=cmd_validate_capsule)

    p = sub.add_parser(
        "check-renderings",
        help="compare authored renderings in references/ against the canonical data file",
    )
    p.add_argument("--data", required=True)
    p.add_argument(
        "--write",
        action="store_true",
        help="rewrite generated blocks from the data file",
    )
    p.set_defaults(func=cmd_check_renderings)

    p = sub.add_parser("fixtures", help="run the must-block/must-pass fixture set")
    p.add_argument("--data", required=True)
    p.set_defaults(func=cmd_fixtures)

    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Refusal as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_REFUSE
    except ValidationFailure as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_FAIL
    except StoreReadLoss as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_STORE_READ


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
