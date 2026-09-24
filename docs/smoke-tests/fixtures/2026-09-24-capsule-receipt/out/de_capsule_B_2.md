I'm not designing yet: four parts of your capsule are still open, and I'm treating them as questions you haven't answered. The confirmed part ("urgent things reach me right away, everything else waits for the digest", and "push every important item immediately" ruled out) I take as given.

This working directory is an empty scratch folder and not a git repository, so I have no project context yet. Once you point me at the project, I'd read the existing notification code, any docs or design notes on it, the project's term list, and recent commits. I'd read the key files myself before proposing anything.

Need from you (answer as "1A, 2B, …"):

1. **Delay.** If a digest item turns out to matter the same day, is waiting until the next 9am digest acceptable?
   - A: Yes, always.
   - B: No, an item must be able to jump to immediate once it starts mattering.
   - C: Only for some kinds of items (tell me which).

2. **Urgent.** Is "urgent = blocks someone's work today" your definition?
   - A: Yes, as written.
   - B: Different (tell me how).

3. **Conflict in your wording.** "Everything else waits for the digest" and "neither urgent nor important gets no notification" can't both cover the neither-urgent-nor-important items. Which is true for them?
   - A: Not in the digest, and no badge. Visible only if I open the app.
   - B: In the digest, but no badge.
   - C: Dropped entirely, not shown anywhere.

4. **Important.** What makes an item "important" instead of "neither"? One sentence is enough.

5. **9am local time.** Whose clock?
   - A: One fixed time zone.
   - B: Each recipient's own time zone.
   - C: Configurable per recipient.

6. **Project.** What is the path or repo for the notification system?

After your answers I'll propose two or three approaches, with a recommendation and the strongest rival.
