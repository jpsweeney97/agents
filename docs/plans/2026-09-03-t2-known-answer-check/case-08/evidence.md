# Evidence the user supplied for the checkout decision

Eleven excerpts.

## E1. Checkout funnel by step (analytics; spring = April to May, summer = July to August)

| Step | Drop-off, spring | Drop-off, summer |
| --- | --- | --- |
| Cart to checkout start | 30% | 30% |
| Account or guest choice | 6% | 6% |
| Address | 11% | 12% |
| Shipping | 8% | 8% |
| Payment | 22% | 51% |

Payment-step drop-off, summer, by device: mobile 61%, desktop 19% (desktop was 20% in spring).

## E2. Payment provider (Paylane) dashboard and status notice

3-D Secure challenge outcomes since June 12: on mobile browsers, 58% of challenges end "abandoned or timed out"; on desktop, 9%. Provider status notice, June 20: "Merchants using the embedded card form (custom integration) may see elevated challenge failures on mobile browsers after the June browser privacy update, which blocks the challenge frame's third-party storage. Hosted Checkout is unaffected. Migration guide: one to two developer days. Fraud rules and wallet buttons behave identically in both modes."

## E3. Store's payment integration (agency notes)

Embedded card form (custom integration) since 2023. Agency estimate to switch to Hosted Checkout: twelve hours including testing. The fraud rules run on Paylane's side in both modes. Wallet buttons are already live in the current integration.

## E4. Wallet usage

9% of checkouts pay with a wallet. Abandonment among wallet payers: 31% in summer, 30% in spring. Among card payers: 76% in summer, 49% in spring.

## E5. Account and forms

Guest checkout has been available since 2024; 64% of orders are guest orders, and the account prompt appears after purchase. The address step has seven fields; the phone field has been mandatory since 2024; address-step drop-off is 12% against 11% in spring.

## E6. Page performance

Checkout pages load in 1.9 seconds on mobile (2.0 in spring).

## E7. Shipping

Shipping costs have been shown on the cart page since 2023, and a free-shipping threshold bar is on the cart page. Shipping-step drop-off is unchanged at 8%.

## E8. Abandoned-cart email

Live since 2023; recovers about 4% of abandoned carts. Recovered shoppers who return on mobile fail at the payment step at the summer rate (E2).

## E9. Earlier tests

Exit-intent discount (2025): conversion +1.2 points, margin −6%. Trust badges and a progress indicator have been on the checkout since 2023.

## E10. Provider documentation on payment methods

Instalments and bank transfer, in the embedded integration, pass through the same challenge frame as cards. A layout test cannot alter the provider's challenge frame.

## E11. Contract and certification

Paylane contract runs to March; ninety days' notice to terminate; a new provider's compliance certification takes eight to ten weeks.
