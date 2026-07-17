# Local-marketplace cache auto-sync probe — 2026-07-17

This is a factual evidence record for the delivery-contract correction. It is not a Gate B grant: Gate B for git-cycle 1.5.3 remains withheld, so no fresh-Codex proving row, mirror, or push follows from this record.

## Controlled scratch-state probe

The probe used an isolated Codex state with a `probe-mart` local marketplace and a dummy plugin. The plugin was explicitly installed at 1.0.0, then its source was changed to create source/cache drift. Each listed trigger was exercised separately.

| Trigger | Cache outcome |
| --- | --- |
| CLI `codex plugin list` | Unchanged; it reported installed 1.0.0 and did not flag drift. |
| CLI `codex plugin marketplace list` or `upgrade` | Unchanged; the upgrade path covers Git marketplaces only. |
| `codex exec` session start | Unchanged; the run reached model authentication and failed there. |
| Idle `codex app-server` boot or its `initialize` handshake | Unchanged. |
| App-server `skills/list` | Unchanged. |
| App-server `plugin/list` | Synchronized the drifted local source into cache and pruned the old version directory. |

The transition reproduced twice: 1.0.0 → 1.0.1, then—after re-drifting—the same `plugin/list` trigger produced 1.0.2. The retained state holds only `dummy/1.0.2` in the probe cache, while the source and cache manifests both say 1.0.2.

## Retained-log corroboration

The retained app-server method log contains a `skills/list` response resolving `dummy:dummy-skill` at cache path `.../probe-mart/dummy/1.0.0/skills/dummy-skill/SKILL.md`, and a `plugin/list` response for `dummy@probe-mart` reporting `localVersion: 1.0.1`, `installed: true`, and `enabled: true`. Its SHA-256 is `6e0aee632fe180d5b6bd223386ffc391e6fcb6023c9217fc27316f7533e08cd5`; the matching initialize and app-server-output logs hash to `60718c3a775124a405c48df2b24d55c8ef0163f3be82cdbe9844e9aa4ecab3fb` and `0183fc69072938b0bfdf9cedc22c51753ff743944e7fd84eafd92f9f4a8c4b30` respectively. The scratch logs are retained only as corroborating raw material; this tracked record carries the durable finding.

## Production correlation

The reported production process table placed `/Applications/ChatGPT.app/Contents/Resources/codex … app-server` at 12:39 PM, coincident with the observed maintenance burst. The git-cycle cache directory was born at 12:39:54, followed by the bundled-marketplace refresh at 12:40:00 and `config.toml` rewrite at 12:41. The previous 1.4.2 cache directory was pruned while 1.5.3 appeared, matching the controlled probe's replacement fingerprint.

## Scope and unresolved decisions

This finding is specific to the observed local-marketplace path and current app-server behavior on this machine. It establishes that source/cache equality and cache presence are not authorization evidence, and that `NOT-INSTALLED` observes only the momentary mismatch. It does not choose a stable withheld-window mitigation, change the release-cut version-bump lockstep policy, or establish behavior for every Codex build or marketplace type. Those are separate decisions.
