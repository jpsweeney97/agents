# Prune: the press that keeps stopping

Field of fifteen. Survivor count asked for: about four. Five survive; ten cut records follow.

## Survivors (field order, exact wordings)

1. **Take the manufacturer's annual service contract** — carried forward because a cut would need an unpriced value trade; see the note below.
2. **Introduce a preventive-maintenance schedule**
3. **Train the operators in fault repair**
4. **Stock spare parts for the common failures**
5. **Install condition sensors on the press**

## Notes carried forward

Trade that blocked a cut: "Take the manufacturer's annual service contract" runs directly against the stated value "Avoid depending on a single vendor's service contract". It is also the only option that puts scheduled expert hands on the press, which constraint 3 forbids to anyone but the two operators and the manufacturer's technician. Cutting it would mean deciding that vendor independence outweighs that reliability gain, a trade the user has not priced. It is carried, not endorsed, for Develop to price.

Six of the cuts below are each a bet on a specific cause of the stops: stress, paper stock, air supply, electrical supply, room environment, controller. The file gives no cause, and the rise from three lost days to fourteen in one quarter is unexplained. Every one of those revive conditions keys on the stop log or the operators' account of what the fourteen days were. Develop should ask for that before developing the survivors; it may revive one of these cuts.

Two survivor cautions for Develop. "Train the operators in fault repair": if both operators attend a course together for more than two working days the press stands idle and constraint 2 is touched, so stagger them or confirm course length. "Install condition sensors on the press": fitting is manufacturer work under constraint 3 and the sensors need running time to learn what normal looks like, so check that ten weeks covers procurement, fitting, and a baseline.

## Cut records

```text
Option:         Buy a second press as a backup
Cut:            constraint, fact-established
Reason:         Fails constraint 1. The confirmed constraint's own text says "a press, even used, or a major refurbishment is out" of the $20,000 capital cap, and the option is to "Purchase a used press of the same class". This is the user's candidate; it dies only by this record. The case it makes, keeping work moving during a stop rather than reducing stops, is carried by "Outsource overflow to a partner shop" (itself cut on survivor count below, with its own revive condition), so the case is not lost with the option.
Strongest case: It is the only option in the field that keeps printing while the main press is down, and it works whatever the cause of the stops turns out to be. Fourteen lost days in one quarter against a peak that is half the year's revenue is the kind of loss a backup machine is bought for.
Revive if:      The capital cap is lifted or raised to a level a used press of this class fits under, or the user reframes the acquisition as a lease or hire and confirms that falls outside constraint 1. Either is a change to the constraint, not a re-reading of it.
```

```text
Option:         Outsource overflow to a partner shop
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. Two things I cannot see from here: whether a partner shop has room in October to December, when every print shop is in the same peak, and whether the user counts moving jobs elsewhere as reducing downtime at all, since the decision question is downtime on the main press and this option leaves the stops exactly as they are. Passes all three constraints. It carries the bypass case from the cut second press.
Strongest case: Capacity without capital, arranged in days rather than weeks, and it protects the customer relationship on the days the press is down whatever the survivors achieve. A shop that turns work away in peak loses more than the job.
Revive if:      A partner confirms in writing that it can take Halden's overflow through peak, or Develop finds the survivors cannot bring expected lost days low enough to protect peak on their own.
```

```text
Option:         Hire a maintenance technician
Cut:            constraint, fact-established
Reason:         Fails constraint 3. Under the shop's insurance only the two trained operators or the manufacturer's certified technician may work on the press. The option is to "Employ a technician to look after the press", which puts a third person's hands on it; an employee is neither of the two operators nor the manufacturer's technician. The constraint's stated cost is that any option needing other hands on the press has to go through the manufacturer. A hire scoped to the two smaller machines only would be a different, narrower option than the one in the field, and would not touch the main press's downtime.
Strongest case: Daily dedicated attention is the closest thing to a standing fix for a machine whose stops have quadrupled in a quarter, and a salary sits outside the capital cap.
Revive if:      The insurer confirms it will extend cover to a named third person after training, in time for peak, or the constraint is otherwise reworded to admit an employed technician.
```

```text
Option:         Replace the press's controller
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. Three unknowns: whether a current-generation control unit fits under the $20,000 cap (constraint 1), whether the swap and commissioning stop the press for more than two working days (constraint 2), and whether the stops have anything to do with the controller, since the file gives no cause. Passes constraint 3 because it is a manufacturer job. Neither constraint failure is established from the file, so this is not a constraint cut.
Strongest case: A 2015 controller is the part most likely to be out of support; if the stops are control faults, nothing else in the field fixes them, and a controller swap is a bounded job next to a refurbishment.
Revive if:      The stop log shows control-system faults or resets, and the manufacturer quotes the unit and fitting under $20,000 with a stop of two working days or less.
```

```text
Option:         Run the press at reduced speed
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. It costs nothing, passes every constraint, and its only cost is throughput, which the user has priced below reliability. Its seriousness turns entirely on whether the stops are stress-related, which the file does not say; if they are not, it gives away throughput across the half-year of revenue and changes nothing. The trade it needs is already priced, so this cut is blocked only by the unknown cause, not by a value.
Strongest case: Free, reversible the same day, and on the one value trade the user has priced it sits on the right side. If the stops are heat, wear-rate, or vibration faults, this alone could bring them down before peak.
Revive if:      The stop log or the operators' account points to stress-related faults, such as stops clustering after long high-speed runs or in warm conditions.
```

```text
Option:         Full refurbishment by the manufacturer
Cut:            constraint, fact-established
Reason:         Fails constraints 1 and 2. Constraint 1's own text says "a major refurbishment is out" of the capital cap. Constraint 2's says "teardown-scale work is out", and the option's own description calls it "the longest stop" in the field. Passes constraint 3.
Strongest case: The only option that resets the machine rather than managing it, and the most thorough answer to stops that have quadrupled in a quarter.
Revive if:      The decision is re-asked for after peak, when neither the capital cap nor the two-day stoppage limit applies as worded.
```

```text
Option:         Service the shop's compressed-air system
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. Routine contractor work that touches nothing on the press, so it passes all three constraints cleanly and is likely cheap. Whether it is serious depends on whether the stops are air-related, typically feeder and sheet-transport faults, which the file does not say. It shares a feed diagnostic with "Change paper stock supplier" but bets on a different feed cause, so neither is cut for the same reason as the other.
Strongest case: A sheet-fed press depends on clean, dry air for feeding, air systems degrade quietly, and an overhaul also protects the two smaller machines. Of the cause bets it is the cheapest to be wrong about.
Revive if:      The stop log shows feeder, suction, or sheet-transport faults, or the air-supply contractor's inspection finds moisture or pressure problems.
```

```text
Option:         Upgrade the shop's electrical supply
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. Whether it is serious depends on whether the stops are electrical, which the file does not say. The cost of a distribution board and surge protection is probably inside the cap but not established; the changeover may need a short shop power-down, likely under two days but not established. Passes constraint 3 because nothing on the press is touched.
Strongest case: Protects every machine at once, and a surge or supply fault is the kind of cause that produces sudden, unexplained stops with no wear to find afterwards.
Revive if:      The stop log shows resets, control faults, or stops shared with the smaller machines, or the shop has other signs of supply trouble.
```

```text
Option:         Add climate control to the pressroom
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. Its own description makes it "the largest building change in the field", so it probably fails the $20,000 cap and may not be installed inside ten weeks, but neither is established from the file. Whether it is serious depends on whether the stops are environmental, which the file does not say. Passes constraint 3.
Strongest case: The rise from three lost days to fourteen between consecutive quarters is the pattern a seasonal change in heat or humidity would produce, and stable conditions help paper, ink, and machine alike year after year.
Revive if:      The stop log correlates with weather or humidity, and a quote comes in under the cap with an installation that does not stop the press.
```

```text
Option:         Change paper stock supplier
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. No press work and little cost, so it passes all three constraints. Whether it is serious depends on whether the stops are feed problems caused by the stock, which the file does not say; it also cannot be ruled out from the file that the stock or supplier changed around the time the stops rose. It shares a feed diagnostic with "Service the shop's compressed-air system" but on a different cause.
Strongest case: If the stock changed when the stops rose, this is the whole answer at almost no cost, and it needs no one's hands on the press.
Revive if:      The stop log shows misfeeds or double sheets, or the paper stock or supplier changed in or just before the bad quarter.
```
