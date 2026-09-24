Both constraints are now fixed, and I won't ask you to trade them.

My read so far: you want to never lose more than a day of work in the app files, using a nightly job. Fixed: it never touches the production database, even read-only, and it finishes before 6am. Since the database is out, this job does not protect database data.

What can still change is how much the job copies, against the time it has before 6am.

Need from you:
1. Is it fine that this job doesn't protect database data?
   1. Yes, the database is backed up another way.
   2. Yes, it stays unprotected and that's acceptable.
   3. Not sure.
2. If a full copy of the app files can't finish before 6am, which would you accept?
   1. Copy only changed files each night. This is more to build.
   2. Leave out some folders. This protects less.
   3. I don't know how big the app files are. Measure them first.
