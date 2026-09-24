I can't start proposing approaches yet. Three of your compressions are unconfirmed and one is unpriced, and each one changes the design. I've read nothing so far.

**Project context.** The working directory is a scratch path and not a git repo, so I don't know which project this is for. Once you name it, I'll read its existing notification code, docs, ADRs (architecture decision records), glossary and recent commits. I'll read the key files myself before designing.

**Scope.** I'm treating this as one design. Immediate alerts and the daily digest both depend on one decision: is an item urgent, important, or neither? If that decision turns out to need its own design, I'll say so.

**Binding for now:** pushing every important item immediately is ruled out.

Questions (answer as "Q2: 1"):

**Q1. Which project or directory is this for?**

**Q2. Unpriced, and "no" is a valid answer: is a day's delay acceptable when a digest item turns out to matter the same day?** This is a risk you own, so I won't pick for you.
1. Yes, accept the delay.
2. No. A digest item can be promoted to an immediate alert later, for example when someone becomes blocked by it.
3. No. Add a second digest, for example midday.

**Q3. Urgent means "blocks someone's work today." Who decides that?** I'm reading "someone" as you, the recipient. Correct me if it can be anyone.
1. The sender marks it.
2. The system decides from rules.
3. Both. The sender can mark it, and rules can also mark it.

**Q4. Confirm the three classes.** Urgent gets an immediate alert. Important goes in the digest. Neither gets no notification and no badge. Should "neither" items still be visible if someone opens the app and looks?
1. Yes, visible only when looked for.
2. No, not shown anywhere.

**Q5. The digest goes out at 9am local time. Local to whom?**
1. The recipient's own time zone.
2. One fixed time zone for everyone.

Need from you: answers to Q1–Q5. After that I'll propose the approaches that actually differ, with a labeled lean.
