I haven't started building. The approval came from the review session rather than from you, and it didn't address the two decisions I put to you. I applied its one redline: the flag is now `--after` and the helper is `parse_after()`. The rest of the design is unchanged.

**Still open after the redline:**
- **Unconfirmed premise:** I haven't checked that the `notes search` grammar already uses `--after`. The review session's word is the only source.
- **Not addressed by the review:** its note doesn't mention the local-midnight anchor or the error on future dates.
- **New ambiguity:** `--after 2026-09-20` now reads two ways. My design includes notes changed after 00:00 on the 20th. "After" more naturally means starting on the 21st. `--since` didn't have this problem.
- **No pressure round yet:** two premises come from my own reading of the code: `updated_at` compares correctly as an ISO string, and ADR-0003 requires search parity. I can't tell whether the review session tested them.

Need from you:
1. Flag name: (a) `--after` only, (b) `--since` as you first asked.
2. `--after 2026-09-20` starts: (a) at 00:00 on the 20th, (b) at 00:00 on the 21st.
3. Local-midnight anchor and the error on future dates: (a) keep both, (b) change one (tell me which).
4. Before approving: (a) run `grill-me` on the design, (b) approve now and let `implementation-planning` be the first test of those premises.
