---
name: plain-language
description: "Use when the user explicitly requests plain-language mode: rewrite the previous answer in full and in brief, then keep later replies plain. Not for automatic rewriting, editing documents, or shortening answers without changing their language."
disable-model-invocation: true
---

# Plain Language

Invocation: `/plain-language` on Claude Code or `$plain-language` on Codex. Run only at the user's explicit request, not because an answer looks complicated.

## Rewrite The Previous Answer

Use the most recent substantive assistant answer before the request, not tool output or a progress update. Read the answer itself; if it is unavailable, ask the user to paste it rather than reconstructing it from a summary. The ongoing plain-language preference still applies.

Briefly state that you are rewriting the previous answer and will keep replies plain in this conversation. Then return these two sections in order:

1. **Full explanation** — preserve every substantive point, replacing unfamiliar technical terms, abbreviations, abstract shorthand, and figurative wording with ordinary, literal words wherever possible. Use complete, natural sentences. Explain rather than compress; this section may be longer than the original.
2. **Main point** — give the essential takeaway and leave out secondary detail. Keep any condition or uncertainty needed to avoid misleading the reader about that takeaway.

Preserve the original meaning, conclusions, qualifications, uncertainty, examples, and distinctions between what was done, proposed, and not verified. Keep exact names, numbers, code, commands, paths, links, and verbatim quotations intact where they identify something or must remain usable; simplify the surrounding explanation. When a technical term cannot be replaced without losing precision, keep it and explain it in ordinary words. Generic technical concepts are not exact names: for example, "not deployed" becomes "not put into live use." When "provider sandbox" means an environment for testing, rewrite it as "the provider’s test environment." Otherwise, explain what the sandbox does in that context.

Do not add new claims or silently correct the original as part of rewriting. If a material error is apparent, identify the correction separately rather than presenting it as equivalent wording. Compare the full explanation with the original before replying: nothing substantive should be lost, strengthened, or invented. Do not show this comparison as a checklist.

Rewrite in chat. Do not repeat actions mentioned in the answer, run commands to verify its claims, or edit files or settings as part of invoking this skill.

## Later Replies

Keep using ordinary, literal language throughout subsequent replies in the current conversation. Replace technical terms wherever possible and explain necessary exact terms. Use whatever structure fits the answer; do not automatically repeat the two sections or the activation notice.

Stay in this mode until the user asks to stop or chooses a conflicting communication style. Accept ordinary wording such as "stop plain-language mode" or "go back to your usual style"; do not require an exact command. A request to use one technical term or quote exact text is not by itself a request to stop.

This preference applies to the current conversation only. Do not write it into memory, account preferences, or instruction files, and do not promise that new conversations will inherit it. Invoking the skill again rewrites the latest substantive answer and keeps the mode active.
