User: /decide:outcome-shaping — I want to work out what I want from a nightly backup job before I write it.

Assistant: My read so far: you want to stop worrying about losing the working tree, and a nightly job is the first shape that came to mind. Which is the pull: (1) never lose more than a day of work, or (2) never have to think about backups again?

User: 1

Assistant: My read so far: you want to never lose more than a day of work; the job's automation is a means, not the want. A trade to test it: if "never more than a day" costs an hourly job that occasionally slows the machine for a minute, still worth it, or is nightly the real bar?

User: Nightly is the real bar. Keep it nightly — but it must never touch the production database, even read-only; back up the app files only. And it has to be done before 6am, that's when the team starts.
