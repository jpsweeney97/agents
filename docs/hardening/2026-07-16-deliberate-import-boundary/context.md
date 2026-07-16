# Hardening Context: deliberate import-execution boundary

This is a derived hardening analysis for the `deliberate` validator modularization gate. It is not a Codex Security scan and does not claim any proposed hardening has been implemented.

## Source Identity

- Local source root: `/Users/jp/.agents`
- Analysis target revision: `288e4caa9d35a9a172f6e65e2305927e1ae3fcef`
- Local `main`: `c6e5554f02b4308013c0fb4e55cd486e3c47811e`
- `origin/main`: `61583d5b824deb8a977928c4f945a0162e8ecec6`
- Branch at analysis time: `fix/deliberate-gate2-import-authority`
- Source drift: none for the checked working tree at the time of inventory; the branch is local-only and ahead of both `main` and `origin/main`.
- Evidence collection digest: `0f29bee7b7d1270d7cec4d454f536d3ded33c6c8e43fafd66fab10bc79fb1513`

The collection digest is reproducible from these UTF-8 lines, in this exact order, with a trailing newline after every line, hashed with SHA-256:

```text
target=288e4caa9d35a9a172f6e65e2305927e1ae3fcef
main=c6e5554f02b4308013c0fb4e55cd486e3c47811e
origin=61583d5b824deb8a977928c4f945a0162e8ecec6
handoff=f0b4de4702a542dcfff58993e942240496bf021c43a0b47409a81606d6227d8e
adr=f2afc54310846e4c59bf8a41c67eb6a9c9a44ee25ae83b230847611403d13304
gate1=c06001627b506adcdb2331160a7c92d929b414c4bf9cd91b9e86c39b27973445
checker=e682fda0adb7b2f96a75995f93a87fe55a63682e890a3cf7040646f15673870c
tests=26613210396e6f50ad200444d24766f27d2e7d56c42484532866111d1269a50f
contract-data=3a8369dfb7a6eae7e79aa881ce6fd5a74319887c30aa5d7272d130cb6a29d62a
```

The user-supplied conversation summary is included as evidence for intent and reported verification results, but it does not have a stable standalone file hash in this analysis directory.

## Artifact Roles

- Local context: `context.md` is audit context and may contain the local source root path.
- Distributable artifacts: `hardening.md`, `hardening.json`, `proposals/`, and `diagrams/`. These files must avoid local absolute paths.
- Schema authority: `hardening.json` follows the `codex-security:propose-security-hardening` proposal format (`documentType: "codex-security.hardening-analysis"`, `schemaVersion: "1.0"`). There is no repo-local JSON Schema file for this format; validation in this analysis is structural and cross-reference based.

## Evidence Inventory

| Evidence | Title | Kind | Path or source | SHA-256 | What it contributes |
| --- | --- | --- | --- | --- | --- |
| `E001` | User-supplied closure summary | disclosure | Conversation prompt supplied on 2026-07-16 | Not file-backed | Reports the verified zipimport blocker, the disguised-zip follow-up bypass, the repair scope, and the fresh verification table. |
| `E002` | Branch handoff for zipimport closure | document | `.agents/handoffs/2026-07-15_23-06-24_deliberate-v6-gate2-zipimport-closed-clean-review.md` | `f0b4de4702a542dcfff58993e942240496bf021c43a0b47409a81606d6227d8e` | Records the branch state, clean re-review claim, evidence ladder, residual risks, and next decision. |
| `E003` | ADR-0001 module authentication boundary | document | `docs/adr/0001-authenticate-deliberate-modules-as-direct-method-surfaces.md` | `f2afc54310846e4c59bf8a41c67eb6a9c9a44ee25ae83b230847611403d13304` | Defines direct per-file method-surface authentication, Gate 1, Gate 2, cache-prefix requirements, runtime pre-import census, and accepted residuals. |
| `E004` | Gate-2 import-closure checker | source | `skills/deliberate/tests/check_import_closure.py` | `e682fda0adb7b2f96a75995f93a87fe55a63682e890a3cf7040646f15673870c` | Shows the current non-executing authoring checker, complete scripts census, zip-magic sniff, identifier ban, and equality checks. |
| `E005` | Gate-2 regression tests | source | `skills/deliberate/tests/test_import_closure.py` | `26613210396e6f50ad200444d24766f27d2e7d56c42484532866111d1269a50f` | Shows the current regression coverage for sourceless bytecode, symlinks, packages, dynamic import aliases, zip archives, disguised zip archives, and benign false-positive controls. |
| `E006` | Gate-1 dual-path layout smoke | experiment | `docs/smoke-tests/2026-07-15_deliberate-gate1-dual-path-layout-spike.md` | `c06001627b506adcdb2331160a7c92d929b414c4bf9cd91b9e86c39b27973445` | Establishes dual delivery-path import behavior, bytecode-cache hazard, cache-prefix mitigation limits, and interpreter variance. |
| `E007` | Current method-surface inventory | source | `skills/deliberate/references/contract-data.yaml` | `3a8369dfb7a6eae7e79aa881ce6fd5a74319887c30aa5d7272d130cb6a29d62a` | Shows the current authenticated method-surface set and that the production validator remains single-file at `contract-data-version: 5`. |

## Evidence Limits

- The verification table in `E001` and `E002` was not rerun during this hardening analysis. I inspected the live source artifacts and branch identity, but I did not repeat the full 38-test suite, mutation sweep, or dual-path checker runs here.
- The current hardening analysis is anchored to a local branch that has not been pushed or merged. Any implementation work should refresh the target revision first.
- The future runtime pre-import census does not exist yet. Claims about it are proposed design direction or ADR requirements, not observed behavior.
- The analysis is scoped to Python code under `skills/deliberate/scripts/`. External code reached through `sys.path` outside that directory remains an accepted residual in ADR-0001 unless a later design broadens the trust boundary.
