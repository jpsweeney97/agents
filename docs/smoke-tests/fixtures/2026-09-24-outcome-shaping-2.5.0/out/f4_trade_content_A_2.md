My read so far: you want to never lose more than a day of work. The way you get it is a nightly copy of the app files, finished before 6am. Three things are fixed, and I won't ask you to trade them:

- The job runs nightly.
- It never touches the production database, even read-only.
- It finishes before 6am.

That means this job gives the database no protection. I'm treating that as intended.

What can still move is completeness against the deadline. On a night when the copy can't finish by 6am, which do you want?

Need from you: pick one, or correct the read.
1. Stop at 6am and keep the partial backup, with a message telling you it's partial.
2. Discard the unfinished copy, keep last night's complete backup, and tell you the night failed.
3. Something else.
