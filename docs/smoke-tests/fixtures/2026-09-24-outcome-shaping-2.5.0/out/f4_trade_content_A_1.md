My read so far: you want to never lose more than a day of app-file work, and the job runs nightly. Two limits are fixed and I won't ask you to trade them: the job never touches the production database (not even read-only), and it finishes before 6am. Since the database is out of scope, "a day of work" here means files only.

What can still move is what happens on a night the job can't finish by 6am, for example after a large batch of file changes. On such a night you get either an older backup or an incomplete one.

Need from you: on a night the job can't finish by 6am, which would you accept?
1. It stops at 6am, keeps the last complete backup (up to two days old), and tells you.
2. It keeps a partial backup marked incomplete, so newer files are covered but some are missing.
3. Neither is acceptable. Then we look at how much the job copies or how early it starts.
