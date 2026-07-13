---
name: regex-craft
description: "Use when hardening or vetting one regex pattern against catastrophic backtracking (ReDoS) and anchoring/correctness footguns: identify the engine first (backtracking vs automaton flips the verdict), scan the known hazard structures, harden the pattern, and prove it with an executed must-match/must-not-match table plus a backtracking probe — never eyeballed. Not a regex generator. Not for ReDoS as one lens inside a spec-plus-diff review (`implementation-review`), abuse-surface modeling (`red-team`), or a repo-wide vulnerability sweep (`tech-debt-scan` / parked security-audit)."
---

# Regex Craft

Harden one regex pattern against catastrophic backtracking and correctness footguns — and prove it by running it, never by eyeballing three examples. Invocation: `/regex-craft` or `$regex-craft`.

A forcing pass over one regex — an existing or proposed pattern — that identifies the engine it runs on, scans it for the catastrophic-backtracking and anchoring/correctness footguns, hardens it, and proves the result by executing a must-match / must-not-match table plus a backtracking probe. It rewrites the pattern on a working branch when applied; it never pushes, opens a PR, or publishes unless asked.

## Shape — a forcing pass over one regex

**Identify the engine first** — a required first step, not a courtesy. The exploitability verdict for the *same* pattern flips on it: catastrophic backtracking is the dominant hazard on a backtracking engine and *impossible by construction* on a linear/automaton one. Read [references/engine-behavior.md](references/engine-behavior.md) as soon as the engine is named — and again when picking a fix — to place it: engine class, anchor spellings, character-class defaults, mitigation support. State the engine and version. Where it cannot be confirmed, condition the scan on it ("ReDoS-exploitable on PCRE/V8, safe on RE2 — confirm your engine") and flag it loudly; never emit a flat verdict that silently assumes a backtracking engine. A confidently-wrong ReDoS verdict here is a production hang, not a style nit.

Then scan the pattern for the footguns and flag every one that fires — each a forcing question, not a fill-in:

- **Catastrophic backtracking.** Does the pattern nest an ambiguous quantifier inside another (`(a+)+`, `(\d+)*X`) — *exponential* blowup — or place adjacent overlapping quantifiers (`\s*\s*`, `.*.*`, `a.*b.*c`) — *quadratic*? Both explode on **non-matching** input that forces full backtracking, and a quantified group followed by a required token the input lacks is the classic trigger; overlapping alternation under a quantifier (`(a|a)*`, `(a|ab)*`) is the same hazard. Irrelevant on a linear engine.
- **Anchoring for validation.** If a full-string match is required, is the pattern anchored at *both* ends with absolute anchors? An unanchored or prefix-only validator accepts hostile trailing input (`^https://good\.com` matches `https://good.com.evil.com`), and a bare `$` matches before a trailing newline in most engines, so `^\d+$` accepts `"123\n"`. Prefer the engine's absolute anchors — the spelling differs per engine (see `references/engine-behavior.md`) — and confirm the call, too: an API like `re.match` anchors only the start; only `fullmatch` or explicit anchors bind both ends.
- **Mode flags that change meaning.** Is `MULTILINE` making `^`/`$` per-line (an anchor bypass via an injected newline), `DOTALL` letting `.` cross newlines, or case-insensitivity widening a literal — especially a flag set at the compile/call site far from the pattern text? Make the intent explicit inline (`(?m)`/`(?s)`) or anchor with `\A`/`\z` so a distant flag cannot move the string bounds.
- **Character-class breadth.** Do `\d`/`\w`/`\s` carry unintended Unicode breadth? Engines split on whether `\d` is Unicode-wide or ASCII by default (see `references/engine-behavior.md`) — so know which way *your* engine leans, and use `[0-9]` or an ASCII flag where ASCII is meant. Watch the accidental wide range (`[A-z]` spans `Z`–`a`, admitting six punctuation chars) and greedy-vs-lazy or alternation order changing *which* text is captured, not just how fast.

Then **harden** — pick a fix the confirmed engine actually supports, cheapest and most durable first: anchor and bound quantifiers (`{0,n}`); make ambiguity impossible with an atomic group `(?>...)` or possessive quantifier `a++` where the engine supports them (support varies — check `references/engine-behavior.md`, then confirm on the exact version you pinned, never trust a static list); rewrite to remove the overlap (the durable, universal fix); switch to a linear engine (only if the pattern needs no backrefs/lookaround); cap input length; add a per-match timeout (natively supported on only some engines — same reference — an external watchdog elsewhere). Never recommend a construct the engine rejects, and name which class the fix is in — a rewrite removes the vulnerability, a cap or timeout only bounds its cost.

Then **prove it by execution, not inspection** — green on three happy examples is not the proof:

- **Correctness.** Run a **must-match / must-not-match table** against the real engine: the intended-valid inputs and, critically, the bypass cases the footgun scan surfaced (the trailing newline, the `good.com.evil.com`, the embedded newline, the non-ASCII digit). Executed, not eyeballed.
- **ReDoS.** Either confirm the engine is linear (catastrophic backtracking is N/A — then re-check the rewrite still compiles and matches), or **pump it**: build the adversarial input (pumpable prefix + N repetitions of the ambiguous atom + a failing suffix) and time the match as N grows — small N for suspected exponential, N≈1k/5k/10k for quadratic — wrapping the probe in its own timeout. Super-linear growth is a positive vulnerability result.
- Render exactly one verdict: **safe-as-proven** (the bounded hazard ∩ the untrusted inputs this pattern actually receives was probed and the residual named — never "no residual exists") / **unsafe-here-because** / **unverified** (with the exact check a human must still run; never round up to safe). A fix proven on one engine does not transfer — re-prove per engine when the pattern runs in more than one runtime.

Close by **checking the footguns off** explicitly: engine confirmed (or each verdict conditioned on it); backtracking, anchoring, mode-flag, and character-class footguns scanned; the fix uses a construct the engine supports; the must-match / must-not-match table and the ReDoS probe were *executed*; verdict and residual stated. An unchecked or merely-eyeballed footgun is the finding.

## Modes and scope

- **Applied vs advisory follows the invocation.** On a live pattern in code or a PR, author the hardened pattern and run the proof as concrete edits and an executed table. On a proposed pattern or in review, deliver the hardened pattern, the findings, and the proof for a human. Default to the mode the context implies; ask once when genuinely ambiguous. Applied mode does not dissolve the judgment — surface each engine assumption and each rewrite as a flagged decision in the diff, not a default silently baked in.
- **One pattern.** Default scope is one regex. Pointed at a file or repo full of patterns, narrow to the one named or the riskiest and *say so* — this is a forcing pass, not an audit. The *same* vulnerable pattern copy-pasted across many sites is a uniform rewrite for `migration-campaign`; a scored backlog of regex debt is `tech-debt-scan`'s job.

## Proof boundary

Never assert a match outcome or a timing result you did not run; report only what the executed probe produced. The proof is bounded — the table covers the cases reasoned out, the pump covers the tested atom up to the tested N on the tested engine — so state what was verified and bound the residual: *"rewrote `(a+)+` to a non-backtracking form; must / must-not table passes on Python 3.12 `re`, pumped to N=10k with flat timing; residual: match-set equivalence assumed from the table, unverified on other engines."* Advisory-until-asked: rewrite on a working branch, publish nothing unless asked.

## Fences

- ReDoS as one lens inside a spec-plus-diff review of a change → `implementation-review`; one supplied regex, no spec, no diff → here. A review that flags a risky regex hands the pattern here.
- Whole-surface abuse modeling → `red-team`; own only the one regex here.
- A repo-wide sweep for vulnerable patterns → the parked security-audit; a scored regex-debt backlog → `tech-debt-scan`. A scan finding is a valid trigger; the scan is not this skill.
- A hang whose cause is unclear and needs a repro → `diagnose`; a named backtracking hazard has no cause to discover, only a pattern to harden and prove.

## Done when

- The engine and version are confirmed, or every exploitability verdict is conditioned on them and flagged.
- The pattern is scanned for all four footgun classes — catastrophic backtracking, anchoring, mode flags, character-class breadth — and every fire is flagged.
- The hardening uses a mitigation the confirmed engine actually supports, surfaced as a flagged rewrite, with the intended match set preserved.
- The result is proven by *execution*: a must-match / must-not-match table run against the real engine (including the bypass cases the scan surfaced) and a ReDoS probe (engine-is-linear confirmation or an adversarial pump), not eyeballed examples.
- Exactly one verdict is rendered — *safe-as-proven* / *unsafe-here-because* / *unverified* — with the residual bound stated and a note that a fix proven on one engine is unproven on another. Delivered in the mode the invocation implies, advisory-until-asked, nothing published unless asked.
