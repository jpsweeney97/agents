I haven't proposed any approaches yet. Your capsule has four parts that are still your wording or unpriced, so I'm asking about those first. Anything you leave unanswered goes into the design marked "unconfirmed", not as your choice.

Before designing I'll read the project's existing notification code, its docs and decision records, the domain glossary, and recent commits. The current folder is an empty scratch folder and not a git repo, so I don't know where the project is.

One conflict I found: your settled sentence says "everything else waits for the daily digest", but (b) says neither-urgent-nor-important items get no notification at all. It's unclear whether the digest counts as a notification.

**Need from you:**

1. Where is the project? Give me the folder path.
2. "Urgent" means it blocks someone's work today. Whose work?
   1. Anyone's work the item affects.
   2. Only yours.
   3. Neither. I'll tell you the right definition.
3. Do neither-urgent-nor-important items appear in the digest?
   1. Yes, in a low-priority section. There is no push and no badge. This fits "everything else waits for the digest".
   2. No. They are left out of the digest and only found by opening the app.
4. The digest goes out at 9am local time. "Local" means:
   1. Your device's current timezone, so it moves when you travel.
   2. One fixed timezone that you set once.
5. Is a delay of up to 24 hours acceptable? An item that arrives at 9:01am and matters that same day would not reach you until 9am the next day.
   1. Yes, accept the delay.
   2. No. I want a way to move an item to immediate delivery when it turns out to matter. I'll design that in.
   3. Not sure. I'll show the design both ways with the cost of each.

Answer with numbers, e.g. "1: /path, 2.1, 3.1, 4.1, 5.3".
