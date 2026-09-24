I haven't started the design. I need five answers first, and the last one is the question your capsule says was never asked.

Once I know where the project lives, I'll read the existing notification code, its docs and decision records (ADRs, written design decisions), the glossary entries for "urgent" and "important", and recent commits that touch notifications. Then I'll propose approaches. Until you confirm items 2–4, I'm treating them as your proposals, not settled.

Need from you (a reply like "1 path, 2 yes, 3 yes, 4 yes, 5 option 2" works):

1. Which project holds the notification system? This session's folder is a scratch directory, not a git repository. Give me a path, or say "no code yet".
2. "Urgent" means it blocks someone's work today. Confirm, or give me your wording.
3. An item that is neither urgent nor important gets no notification of any kind: no push, no digest line, no badge. It stays findable by opening the app. Right?
4. The digest goes out at 9am in the recipient's local time. Right?
5. Suppose a digest item turns out to matter the same day. It then waits until the next 9am. Is that acceptable?
   1. Yes, a day's delay is fine, and there is no way to promote an item.
   2. No. Someone can promote a digest item to immediate once it matters. This adds a promotion path to the design.
   3. Fine for some kinds of items, not others. Tell me which.
