# Prune: case-09, the pantry's volunteer schedule

Survivor count asked for: about four. Survivors carried: five. Cut records: ten. Field of fifteen fully accounted for.

## Survivors (field order, exact wordings)

1. **Move scheduling to the volunteers' group chat** (user's)
2. **Use a shared calendar with sign-up slots**
3. **Use the scheduling module of the pantry's donor-management system**
4. **Set fixed weekly shifts per volunteer**
5. **Recruit shift leads to manage their own shifts**

Five, not four. Two further cuts were available and each was blocked by a trade between the user's stated values that they have not priced, so I did not invent the weight:

- Cutting "Move scheduling to the volunteers' group chat" against "Use a shared calendar with sign-up slots" would price zero-setup adoption (value 1, and the six-week window) against capacity enforcement (value 2).
- Cutting "Recruit shift leads to manage their own shifts" against the tool options would price the coordinator's protected hours (value 3) against reliability that rests on volunteer leads (value 1).

Checks each survivor carries into the next stage (these are not cuts):

- Group chat: whether the chat is a system the pantry has a data-protection agreement for (constraint 3), and whether visible claims in a thread stop the fifth person claiming a four-person shift.
- Shared calendar: whether the pantry's calendar can hold more than one booking per slot, since shifts need several people, and whether it sits under the same data-protection agreement as the spreadsheet.
- Donor-management module: whether the module is on the pantry's current plan. If it is not, adopting it is new software spending and the option fails constraint 1.
- Fixed weekly shifts: how the holiday surge's extra shifts get staffed when the standing pattern covers only a normal week.
- Shift leads: what the leads look at to see who has signed up. The option's own description says it depends on that.

## Cut records (field order)

```text
Option:         Rebuild the spreadsheet with validation and locking
Cut:            same reason, judgment call
Reason:         This and "Use a shared calendar with sign-up slots" are the same move: make a tool the pantry already has enforce shift capacity, so volunteers sign themselves up and the coordinator stops reconciling email. Both succeed if volunteers will self-serve in the existing suite and fail if they will not. I keep the calendar because its capacity limit is built into the product. The spreadsheet's would be hand-built formulas and protected ranges that the coordinator must maintain and that a volunteer can break or work around, which spends the hours value 3 protects.
Strongest case: It is the tool all 140 volunteers already know, so there is no adoption step inside a six-week window. A grid models multi-person shifts trivially, where calendar slots may not. Adding drop-downs, counts, and locks is a short build with no data-protection question, because the data already lives there.
Revive if:      The pantry's calendar cannot hold several bookings per slot, or is not covered by the existing data-protection agreement, leaving the spreadsheet the only existing-suite tool that can model shifts. Or the next stage finds the coordinator can build and hold the locks without ongoing maintenance.
```

```text
Option:         Use a free scheduling app
Cut:            constraint, fact-established
Reason:         Fails constraint 3. The option is a new service that would hold volunteer names, phone numbers, and availability. The user's own cost line for that constraint says "free apps and new services that hold volunteer data are out." The field's note says the same thing: "a new place volunteer data would live."
Strongest case: It is the only option built for exactly this job: capacity per shift, self-service sign-up, reminders, and a coordinator view, with no build and no training beyond an invite. It could be live well inside six weeks.
Revive if:      The pantry obtains a data-protection agreement with a specific app before the surge, or the board lifts constraint 3 for it.
```

```text
Option:         Have a volunteer build a custom tool
Cut:            constraint, fact-established
Reason:         Fails constraint 3. A scheduling site holds names and availability by definition of the job, and a site a volunteer builds is a new system the pantry has no data-protection agreement for. The cost line says "new services that hold volunteer data are out." Hosting closes the other exit: paid hosting is new software spending (constraint 1), and free hosting is another new service holding the data (constraint 3).
Strongest case: It would fit the pantry's shifts exactly, cost nothing, and a willing developer is already offering. A small sign-up site with capacity per shift is a modest build.
Revive if:      The developer can build it inside a system the pantry already has an agreement for, such as a form or small app hosted within the existing suite, and someone other than that one volunteer can maintain it. At that point it is a variant of the existing-suite options, not a separate one. The six-week deadline and the field's own caveat, "maintained by whoever is around", would still count against it.
```

```text
Option:         Reduce the number of shift types
Cut:            survivor count, judgment call
Reason:         A low-confidence cut to reach the count. I could not resolve at sketch depth whether shift variety causes any of the unstaffed or double-staffed shifts; the background names no such cause. On its own the option changes nothing about who claims what, or whether a full shift stops taking claims. It reads as a simplification that makes any survivor easier rather than a fix. It is not cut for being unserious.
Strongest case: Fewer shift types means fewer things for any tool or lead to track, fewer ways for a claim to land on the wrong shift, and a simpler schedule to learn in six weeks. It costs no money, no data, and no staff.
Revive if:      The next stage finds that mis-claims across shift types are a real share of the double-staffing, or that a survivor's setup (calendar slots, a lead per shift type) gets materially easier with fewer types. It combines with every survivor.
```

```text
Option:         Require sign-up a month ahead
Cut:            survivor count, judgment call
Reason:         A low-confidence cut to reach the count. This changes when claims arrive, not how they are held. The double-staffing half of the problem remains unless the coordinator reconciles by hand, which is the work value 3 protects against. Volunteers are already dropping off, and asking them to commit four weeks out is likely to depress sign-ups further. I could not see at sketch depth whether the gap-filling time it buys outweighs that. On timing, the surge starts in six weeks, so the first closed month would have to close in about two, before any other fix is in.
Strongest case: It gives the coordinator a full month to see and fill gaps instead of discovering them the day before, which directly serves value 1, and it needs no tool change at all.
Revive if:      The next stage finds most unstaffed shifts were never claimed rather than no-shows, and that volunteers will plan a month out. Or it is adopted as the cadence inside a survivor that enforces capacity.
```

```text
Option:         Over-recruit volunteers to absorb no-shows
Cut:            dominated, judgment call
Reason:         "Send confirmation reminders two days before each shift" is at least as good on everything that matters and better on several things. Both attack the same target, no-shows, by their own descriptions. On value 1, reminders reduce no-shows where more volunteers only tolerate them. On value 2, reminders are neutral, where adding people to a scheduler that already double-staffed fourteen shifts last month makes turning up to a full shift more likely. On value 3, a reminder batch is a templated send, where recruiting means screening and onboarding. On the six-week window, reminders start next week. The pool is not thin: about 140 active volunteers for about thirty shifts a week. The dominating option later falls to a survivor-count cut of its own; that does not restore this one, which was worse than it.
Strongest case: The surge will need more hands than a normal week, and numbers are the one cover that works even when the scheduler fails. Recruitment also brings in people who may replace those who stopped signing up.
Revive if:      The next stage finds the unstaffed shifts were shifts nobody claimed rather than no-shows, and the surge needs more volunteers than the pool holds. Then it is a supply problem, and this becomes a complement to a survivor rather than a fix for the scheduling.
```

```text
Option:         Train the coordinator on advanced spreadsheet use
Cut:            same reason, judgment call
Reason:         This and "Rebuild the spreadsheet with validation and locking" succeed or fail for the same reason: whether the current spreadsheet, used to its full ability, can enforce capacity and cut reconciliation. The option's own words tie its value to that: "so the current tool is used to its full ability." The rebuild is the direct form, delivered now. The course delivers the same end state later, and only if the coordinator then does the rebuild. I kept the rebuild as the pair's representative; it then falls to its own record above.
Strongest case: It invests in the one person who will run whatever is chosen, it costs no software and no data, and a coordinator who can build and repair the schedule tool stops depending on whoever set it up.
Revive if:      The spreadsheet rebuild is revived and the coordinator cannot build or hold the locks without training. Also check whether a paid course counts as new spending under the board's freeze; the constraint as stated covers subscriptions and software, not courses, so I did not cut on it.
```

```text
Option:         Send confirmation reminders two days before each shift
Cut:            survivor count, judgment call
Reason:         A low-confidence cut to reach the count. By its own description it "changes nothing about how shifts are claimed," so it cannot touch the double-staffed shifts, which were the larger count last month (fourteen against nine). What it can touch is the no-show share of the nine unstaffed shifts, and I could not see at sketch depth what that share is. It reads as a complement to any survivor rather than a fix for the question asked. It is not cut for being unserious; it dominated "Over-recruit volunteers to absorb no-shows" on its own ground.
Strongest case: No-shows are the one failure no sign-up tool fixes, and a two-day reminder is the cheapest known lever on them. It starts next week, costs nothing, and holds no new data if sent from the pantry's existing email.
Revive if:      The next stage finds no-shows account for most of the unstaffed shifts. It then belongs inside the recommendation alongside whichever survivor fixes the claiming. Note that sends done by hand, weekly, for about thirty shifts spend the hours value 3 protects; the calendar and donor-module survivors may send reminders on their own.
```

```text
Option:         Put a paper sign-up board at the pantry
Cut:            dominated, judgment call
Reason:         "Use a shared calendar with sign-up slots" is at least as good on everything that matters and better on reach. Both cap a shift by giving it a fixed number of lines or slots, so both serve value 2. On value 1 the calendar is better: any of the 140 volunteers can claim from home, where the board is seen only by whoever is on site that week, so gaps fill from a fraction of the pool. On value 3 both spare the coordinator reconciliation. The board's one edge, no technology, is small here because the volunteers already schedule by spreadsheet and email. A board in a room the public uses also puts volunteer names where clients can read them; not a constraint failure, but a cost.
Strongest case: It needs nothing set up, nothing learned, and raises no data-protection question about a system. A physical line per shift is the plainest capacity limit there is, and volunteers who come in weekly would see it every visit.
Revive if:      A material share of volunteers cannot or will not use online sign-up, or the calendar turns out not to hold several bookings per slot or not to be covered by the existing agreement. It could also serve as a same-day backup next to a survivor.
```

```text
Option:         Weekly scheduling call with the coordinator
Cut:            dominated, judgment call
Reason:         "Use a shared calendar with sign-up slots" is at least as good on everything that matters and better on two of the three values. On value 2 both cap shifts, the call by the coordinator's live tally. On value 1 the calendar is better because it reaches all 140 volunteers; the option's own description says the call "misses anyone who cannot attend," and for a pool that size that is most people in any given week. On value 3 the calendar is better: the call spends a fixed hour of the coordinator's twenty every week plus the write-up, which value 3 says scheduling should not do. The call's one edge, talking people into empty shifts live, costs exactly those hours, and I could not see at sketch depth that it outweighs the reach lost.
Strongest case: One synchronous moment settles the whole week with no tool at all. The coordinator can see gaps forming and fill them by asking, which no sign-up tool does, and it builds the kind of contact that keeps volunteers from drifting away.
Revive if:      The next stage finds most volunteers can and will attend a fixed weekly slot, or that the coordinator's gap-filling by persuasion is the only thing that fills the surge. It could also survive as a short gap-filling call layered on a survivor, rather than as the claiming channel.
```
