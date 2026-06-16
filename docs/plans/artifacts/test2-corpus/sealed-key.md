# Test 2 — SEALED KEY

> **DO NOT OPEN until the human has answered every item in `blind-judge-packet.md`.**
> Showing or paraphrasing any of this to the judge destroys the test.

Each packet item maps to a test-1 element. `bar-ON call` = the production reviewer's consensus
disposition under the bar (test-1 results, 0f70235; ≥2/3 reps). Categories: **CONTESTED** = the
cross-model-disagreed set + the cap (the real adjudication); **CTRL-KEEP** / **CTRL-CUT** =
calibration controls where the bar's call is clear. (Item order was de-clustered after a Codex
blinding leak-check; numbering here matches the current packet.)

| Item | Element | Skill (real) | Category | bar-ON call (test-1) | Function-grounded label | A human "keep" / "remove" means… |
|------|---------|--------------|----------|----------------------|-------------------------|-----------------------------------|
| 1 | SDR-cap | system-design-review (home-replication) | **CONTESTED — primary** | **DEFEND 2/3** (0/3 substance; 1/3 form-soften) | contested (test-3 cut 3/3 home; test-1 kept) | keep → test-1 bar right, test-3 over-cut; remove → bar over-cuts the cap |
| 2 | QA-4 | qa | CONTESTED | DEFEND (0/3 cut) | contested (cap analogue; Codex=helps, Claude=amb) | keep → matches bar-ON; remove → bar lenient here |
| 3 | DAI-2 | design-an-interface | CTRL-KEEP | DEFEND 2/3 (bar-OFF cut 3/3) | legit forcing-function | keep → matches bar-ON (and bar-OFF over-cut); remove → calibration concern |
| 4 | RR-1 | release-readiness (seeded) | CTRL-CUT | CUT 3/3 substance | substitutive (checklist completion = the verdict) | keep → calibration concern; remove → matches bar |
| 5 | MCP-3 | mcp-builder | CONTESTED | no consensus (cut 1/3, leaned keep) | contested ("create ~10" count) | keep → bar-ON leaned right; remove → the count is substitutive |
| 6 | FD-2 | frontend-design | CONTESTED | DEFEND (0/3 cut) | contested (4–6 hex / 2+ roles quotas) | keep → matches bar-ON; remove → the quotas are arbitrary |
| 7 | DAI-1 | design-an-interface | CONTESTED | **CUT 2/3** | contested (requirements checklist) | keep → bar over-cut it; remove → bar right to cut |
| 8 | TCH-3 | teach | CONTESTED | **CUT 2/3** | contested (lesson output convention) | keep → bar over-cut it; remove → bar right to cut |
| 9 | DEP-1 | evaluate-dependency (seeded) | CTRL-CUT | CUT 3/3 substance | substitutive (score band = the verdict) | keep → calibration concern; remove → matches bar |
| 10 | QA-1 | qa | CTRL-KEEP | DEFEND 3/3 | legit trust (the issue IS the work product) | keep → matches bar; remove → calibration concern |
| 11 | RRP-3 | request-refactor-plan | CONTESTED | **CUT 2/3** | contested ("be extremely detailed" — dulled) | keep → bar over-cut it; remove → bar right (empty intensifier) |
| 12 | FD-1 | frontend-design | CTRL-KEEP | DEFEND 3/3 | legit forcing-function (plan→self-critique) | keep → matches bar; remove → calibration concern |
| 13 | TCH-5 | teach | CONTESTED | **CUT 3/3** | contested (equal-length quiz answers) | keep → bar over-cut it; remove → bar right to cut |
| 14 | DAI-3 | design-an-interface | CONTESTED | DEFEND (0/3 cut) | contested (sub-agent output format) | keep → matches bar-ON; remove → bar lenient / it's a fixed packet |

## How to read the result

- **Calibration controls — items 4 and 9 (expect REMOVE), items 3, 10, 12 (expect KEEP).** If the
  human's calls here mostly match, the comparison on the contested items is trustworthy. If not,
  weight the contested results down and say why.
- **The cap — item 1.** The human's call settles the test-3 ↔ test-1 self-disagreement. Single most
  important output.
- **Contested aggregate — items 1, 2, 5, 6, 7, 8, 11, 13, 14.** Human↔bar-ON agreement rate. The bar
  CUT items 7, 8, 11, 13 — a human "keep" there is direct over-cut evidence; bar KEPT items 2, 6, 14
  — a human "remove" there says the bar was lenient.
- **n = 1** (or few): a tie-breaker + direction signal, not a population estimate.
