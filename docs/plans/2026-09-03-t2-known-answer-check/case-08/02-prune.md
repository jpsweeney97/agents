# Prune: checkout abandonment before the holidays

## Survivors (field order)

1. **Add guest checkout** (user's) — "Let shoppers buy without creating an account."
2. **Reduce the address form to the minimum** — Drop every address field the carrier does not require and use address autocomplete.
3. **Show shipping costs earlier** — Display shipping on the product and cart pages rather than at the shipping step.
4. **Add express wallet payments** — Offer wallet buttons so shoppers can pay with a saved wallet instead of typing a card.
5. **Switch the payment step to the provider's hosted checkout page** — Send shoppers to Paylane's own hosted payment page for the card step instead of the card form embedded in the store's checkout.

Survivor count asked for was about four; five survive. A sixth cut would have to decide whether the drop comes from cost surprise, form length, or the payment step. That is a fact about the checkout I cannot see at sketch depth, not a trade between the user's values, so the five are carried forward. Each survivor attacks a different point in the path (account wall, address typing, cost surprise, card typing, the embedded card form itself), and none fails a confirmed constraint.

## Cut records

```text
Option:         Replace the payment provider
Cut:            constraint, fact-established
Reason:         Fails constraint 1. The Paylane contract runs to March, switching needs ninety days' notice and a compliance re-certification, and the holidays start in seven weeks. The user confirmed that replacing the provider is out.
Strongest case: If Paylane's mobile card form is what changed over the summer, this is the direct fix and the only option that removes the provider's form for every shopper without a redirect.
Revive if:      The decision is revisited after the holidays, when notice can be given inside the contract window, and the surviving payment-step changes show the drop is concentrated at the card form.
```

```text
Option:         Simplify the account creation form
Cut:            same reason, judgment call
Reason:         Succeeds or fails for the same reason as "Add guest checkout": both pay off only if the account wall is where shoppers leave, and both do nothing if it is not. One kept; the user's wording kept per rule. Guest checkout is also the fuller version of the same bet on mobile, since it removes the wall rather than lowering it.
Strongest case: It keeps every order attached to an account, which may matter to the fraud rules or to returns and loyalty, and it is a form edit that costs a few hours.
Revive if:      Guest checkout is blocked by the store platform or by fraud rules that need account history, or the user says accounts must stay mandatory for returns or loyalty.
```

```text
Option:         Remove the mandatory phone-number field
Cut:            same reason, judgment call
Reason:         Succeeds or fails for the same reason as "Reduce the address form to the minimum": both pay off only if the address form's length and typing burden is the driver. The address reduction drops every field the carrier does not require, phone included, and adds autocomplete, which is the larger mobile win. The phone-only change is the first day of that work and ships inside it.
Strongest case: It costs almost nothing, needs no new service, and could go live this week as a probe of whether form friction matters at all.
Revive if:      The autocomplete integration does not fit the seventy-hour budget, or the carrier turns out to require most address fields, leaving phone as the one removable field. It is then the cheap fallback.
```

```text
Option:         Raise the free-shipping threshold visibility
Cut:            same reason, judgment call
Reason:         Succeeds or fails for the same reason as "Show shipping costs earlier": both pay off only if shipping-cost surprise is the driver. The direct version was kept. The threshold bar's distinct contribution is an order-size nudge, which the user ranked below conversion this season, and a "spend more to unlock" bar can send a shopper back to browsing instead of forward to payment.
Strongest case: It reassures on cost and raises order size in one cart-page change, and it is cheap.
Revive if:      Most carts sit just under the free-shipping threshold, so the bar would mostly reassure rather than nudge, or the user re-ranks order size above conversion.
```

```text
Option:         A/B test the checkout layout
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. It is a way of choosing among layout changes rather than a change itself. The variants it compares must be built out of the same seventy hours, and the field text says it takes weeks to read, inside a seven-week window that also has to hold the build and the shipping of the winner.
Strongest case: About nine thousand orders a month at roughly three in ten completion means around thirty thousand started checkouts a month, enough to read a large effect in a couple of weeks. It is the only option that protects against shipping a change that makes things worse.
Revive if:      The team can build two variants inside the first two weeks and is willing to ship the winner with little time left, or the survivors disagree so sharply that a test is the only way to choose.
```

```text
Option:         Add a progress indicator
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. It is a display change that removes nothing from the path. A rise of nineteen points in three months after two years near half points to something in the checkout that changed, and a step counter does not touch whatever changed.
Strongest case: It is cheap, adds no steps, and if the checkout has many steps on a small screen, not knowing how many remain is a real reason to leave.
Revive if:      The checkout has four or more steps and the drop is spread evenly across them rather than concentrated at one.
```

```text
Option:         Add trust badges at the payment step
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. It is a display change beside the card form. Two survivors, express wallets and the hosted checkout page, change the payment step itself; badges decorate it. If hesitation at the card form is the driver, the survivors address it more directly.
Strongest case: It is the cheapest change in the field aimed at the moment of payment, and if a security scare or a redesign over the summer made the card form look less trustworthy, badges are the direct answer.
Revive if:      The drop concentrates at the card form and neither payment-step survivor is possible, or the summer coincided with a visible trust problem such as a breach notice or a site redesign.
```

```text
Option:         Add an exit-intent discount
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. Exit-intent detection watches the cursor move toward the browser edge, which does not exist on touch screens, so on two-thirds mobile traffic it fires late or not at all. It also pays margin on every triggered order and treats leaving rather than the reason for leaving. The user's ranking of conversion above order value permits a margin trade, so the value alone does not kill it; mobile first weighs against it.
Strongest case: It is fast to add through most storefront tools and recovers some shoppers at the exact moment of loss, with no change to the checkout path.
Revive if:      The store's platform has a mobile exit signal that works, and the drop is concentrated at the final place-order moment rather than earlier.
```

```text
Option:         Add more payment methods
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. Each method is an integration, and two integrations against a seventy-hour budget crowd out everything else. Instalments usually come from a separate provider, which constraint 1 bars; I could not confirm whether Paylane offers them natively. Bank transfer is a slow, desktop-leaning method that does not fit mobile first. "Add express wallet payments" changes the payment step for mobile at a fraction of the cost.
Strongest case: If the average order is high enough that affordability, not friction, is the driver, instalments are the fix and nothing else in the field is.
Revive if:      Paylane offers instalments as a native feature, and cart data shows abandonment concentrated in high-value orders.
```

```text
Option:         Retarget abandoned carts by email
Cut:            survivor count, judgment call
Reason:         Low-confidence cut; seriousness could not be resolved at sketch depth. It recovers orders after the shopper has already left and does not lower the rate the question names. I could not tell at sketch depth whether the user would count recovered orders as reduced abandonment. It also needs an email captured before the shopper leaves, which the account wall may be preventing.
Strongest case: It is a marketing change that costs little development time, works whatever the cause turns out to be, and can run alongside any survivor.
Revive if:      The user says recovered revenue counts toward the goal, or the survivors are shipped and there is still budget for a follow-up layer.
```
