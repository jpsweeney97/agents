# Prune: case-07, the clinic's missed appointments

## Survivors (field order, exact wordings)

1. Call patients the day before their appointment (user's)
2. Switch the text-message reminders to a different vendor
3. Add a second text-message reminder
4. Offer an online self-rescheduling link

Count: 4 survivors against "about four". One constraint cut, three same-reason cuts, and four dominated cuts came first; three survivor-count cuts followed. No cut needed a trade between the user's values that they have not priced. Every value-based judgment below rests on the three values as the user stated them: chronic-care patients seen over slot revenue; nothing made harder for elderly patients; front-desk workload kept sustainable.

## Cut records

### Constraint

```text
Option:         Extend clinic hours into the evening
Cut:            constraint, fact-established
Reason:         Fails constraint 3 (no new staff or contractors before flu season; the front desk's existing hours are what there is). The option's own wording says it "needs staff on those evenings". Two evenings a week are open hours the clinic does not have now, so they need clinician and front-desk hours beyond the existing ones. The constraint rules that labour out.
Strongest case: Evening slots would give working-age patients and carers an alternative to the daytime slots they keep missing, and the clinic would not have to change anything about reminders.
Revive if:      The user says the clinic can move existing shifts into two evenings without adding hours or cutting daytime capacity. That is a different option ("shift hours", not "extend hours") and would need re-wording before it re-enters the field.
```

### Same reason

```text
Option:         Add email reminders
Cut:            same reason, judgment call
Reason:         Shares its reason for succeeding or failing with "Add a second text-message reminder": both are one more automated reminder at no labour cost. Both work if a second nudge reaches patients the current text is missing; both fail if patients are not acting on automated messages at all. Kept the second text because it reaches every patient the clinic already texts, while email reaches only patients with an address on file, and the elderly chronic-care patients the user cares most about are the least likely to have or read one.
Strongest case: It is a genuinely different channel. If the specific problem is that texts go unread but email is read, it catches patients a second text would miss, at no labour cost.
Revive if:      A large share of the patients who miss have an email address on file and are known not to receive or read the text. If instead texts are not being delivered at all, "Switch the text-message reminders to a different vendor" is the option that answers that, not email.
```

```text
Option:         Mail appointment cards by post
Cut:            same reason, judgment call
Reason:         Shares its reason with the user's candidate "Call patients the day before their appointment": both are a reminder outside the text channel, handled per appointment by the front desk out of its fixed hours. Both work if what is missing is a reminder that reaches patients the texts do not; both fail if the front desk cannot absorb per-appointment work at about 140 appointments a day. The same-reason rule keeps the user's wording when one of the pair is theirs, so the card is the one cut. The call is also faster (the day before, not a week ahead) and gets an answer back; the card is one-way and carries a per-piece cost.
Strongest case: It is the only option that reaches a patient with no phone at all, and it asks nothing of the patient's technology.
Revive if:      The clinic has a meaningful group of patients with no phone number of any kind. They cannot be reached by call or text, and a card is the only channel for them.
```

```text
Option:         Send a policy letter after two missed appointments
Cut:            same reason, judgment call
Reason:         Shares its reason with "Run a patient education campaign about missed appointments": both work by appealing to patients' consideration and sense of the clinic's expectations, not by helping them remember or by removing a barrier. Both succeed only if a meaningful share of the misses are patients who could attend but do not bother; both fail if the misses come from forgetting, transport, or reminders not arriving. Kept the campaign because it costs the front desk no per-patient work and cannot read as a penalty warning to a chronic-care or elderly patient who missed for reasons outside their control, which a letter can, and which would push against the user's first two values and the spirit of constraint 2. The letter is not itself a constraint failure: constraint 2 rules out financial deterrents, and a letter is not one.
Strongest case: It targets the patients who actually miss repeatedly instead of the whole patient list, so its effort goes where the problem is. If a small set of repeat missers drives the rise, this is the only option that addresses them individually.
Revive if:      The clinic's records show the rise since April is concentrated in a small set of patients who miss repeatedly. Then targeting matters and the campaign's broadcast approach does not.
```

### Dominated

```text
Option:         Send reminders earlier
Cut:            dominated, judgment call
Reason:         "Add a second text-message reminder" contains this option: it sends the three-days-before reminder this option proposes and keeps the day-before reminder as well. It is the same configuration change with the same vendor at the same labour cost (none), and it also covers patients who would forget between three days out and the day itself. The only things this option wins on are one fewer message per patient and a trivially lower message cost.
Strongest case: One well-timed reminder may be all a patient reads; a second message can be ignored as noise, and a three-day-out reminder gives time to rearrange without adding volume.
Revive if:      The vendor charges per message in a way that makes a second reminder material, or the user believes patients treat two messages as spam and read neither.
```

```text
Option:         Shorten the booking horizon to two weeks
Cut:            dominated, judgment call
Reason:         Compared against "Add a second text-message reminder", which acts on the same problem (far-ahead bookings being forgotten) by reminding at three days out instead of forbidding the booking. On the user's three values the second reminder is at least as good on each. This option makes booking harder for patients with recurring follow-ups, who must ring back weeks later instead of booking at the visit (value 2, and elderly patients are the largest such group). It risks chronic-care follow-ups never being booked at all (value 1). It moves booking work onto the front desk as call-backs (value 3). The second reminder costs none of that. This option wins only in the case where reminders are not reaching patients at all, and in that case the vendor option, not the horizon, is the answer.
Strongest case: If the misses really are concentrated in appointments booked months ahead, no reminder fixes a booking the patient has stopped planning around, and a short horizon removes that class of miss outright.
Revive if:      The clinic's data show the no-shows are concentrated in appointments booked more than two weeks ahead, and a reminder fix has been tried and did not move them.
```

```text
Option:         Reduce appointment length to add slots
Cut:            dominated, judgment call
Reason:         Does not act on the no-show rate the decision question asks about; its own wording says it makes misses "cost less". Compared against "Add a waitlist that fills cancelled slots automatically", which also treats the loss rather than the miss: the waitlist recovers lost slots without shortening clinical time for anyone and without staff effort, while this option shortens every visit, including the chronic-care follow-ups the user ranks first (value 1), and adds check-ins per day for the front desk (value 3). Where this option wins, more raw slots, the gain is slot capacity, which the user ranks below patients seen. The waitlist is itself cut below on survivor count; that does not change this comparison.
Strongest case: It needs no vendor, no portal, and no patient action; more slots means a missed one costs the clinic less and a patient who needs a follow-up finds one sooner.
Revive if:      The Develop stage finds that slot capacity, not the miss rate, is what limits patients seen, and the clinicians confirm shorter visits would not degrade chronic-care follow-ups.
```

```text
Option:         Require patients to confirm by reply or lose the slot
Cut:            dominated, judgment call
Reason:         Not a constraint failure: constraint 2 rules out financial deterrents, and losing a slot is not one. Compared against "Offer an online self-rescheduling link", which also converts a would-be no-show into a freed slot. On the user's three values the link is at least as good on each. The link never takes an appointment away from a patient who did not act, while this option releases the slot of any patient who did not reply, including chronic-care patients who never saw the message and would have come (value 1). The link is optional, while the reply is mandatory, which makes attending harder for exactly the elderly patients least likely to reply to a text (value 2; the option's own wording names this cost). The link reduces reschedule calls, while released slots need refilling on the morning and generate calls from patients who lost them (value 3). This option wins only on freeing the slots of silent patients, and a freed slot counts as a patient seen only if it is refilled and only when the silent patient would not have come. The user ranks patients seen above slot revenue.
Strongest case: It is the one option that gets a freed slot out of a patient who does nothing, which is most of the twenty-four percent; with a refill mechanism it could recover a large share of the lost slots.
Revive if:      The clinic can show that patients who do not confirm almost never attend, so releasing costs no patient seen, and a refill mechanism exists to fill the released slots the same morning.
```

### Survivor count

```text
Option:         Run a patient education campaign about missed appointments
Cut:            survivor count, judgment call
Reason:         A low-confidence cut of a candidate whose seriousness I could not resolve at sketch depth. It survived the same-reason pairing with the policy letter as the cheaper, non-punitive form of a consideration appeal. What I cannot resolve is whether any part of a rise from eleven to twenty-four percent in about five months is a change in patients' consideration rather than in memory, barriers, or reminder delivery. A change that sharp usually has a cause other than attitude, but nothing in the case settles it.
Strongest case: It is nearly free, needs no vendor and no front-desk time per patient, cannot make anything harder for elderly patients, and can run alongside anything else.
Revive if:      Evidence gathered in Develop shows a meaningful share of misses are patients who could have attended and chose not to, or the user wants a no-cost add-on alongside the recommendation.
```

```text
Option:         Add a waitlist that fills cancelled slots automatically
Cut:            survivor count, judgment call
Reason:         A low-confidence cut of a candidate whose seriousness I could not resolve at sketch depth. As worded it fills cancelled slots. The problem the user described is appointments "missed without notice", which are not cancelled and so leave nothing for the waitlist to fill. How many slots it would recover depends on the clinic's cancellation volume and on patient-portal uptake, neither of which I can see. It does not reduce the no-show rate the question asks about.
Strongest case: It recovers a lost slot for a waiting patient without any staff effort, which serves "patients seen" directly, and it is the natural partner of "Offer an online self-rescheduling link": the link frees slots, and something has to fill them.
Revive if:      The clinic's cancellation volume turns out to be large, or the Develop stage finds that slots freed by the self-rescheduling link go unfilled because the front desk cannot refill them in its existing hours.
```

```text
Option:         Offer telehealth for follow-up visits
Cut:            survivor count, judgment call
Reason:         A low-confidence cut of a candidate whose seriousness I could not resolve at sketch depth. Its payoff rests on the trip being why patients miss, which nothing in the case establishes; a sharp rise since April points more to something that changed (a system, a reminder) than to distances, which do not change. It also has the heaviest set-up of the remaining options before an eight-week deadline: a video platform, clinician workflow, and patient onboarding. It aims at the follow-up visits the user ranks first, which is why this cut is low confidence.
Strongest case: It removes the trip entirely for the chronic-care follow-ups the user cares most about. It is optional, so it makes nothing harder for patients who prefer to come in. If transport is the cause, it could move more of the rate than any reminder change.
Revive if:      Evidence gathered in Develop shows misses cluster among patients with long journeys or transport difficulty, or the clinic's record system already includes a video-visit feature that can be switched on within the eight weeks.
```
