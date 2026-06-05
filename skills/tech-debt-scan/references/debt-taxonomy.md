# Debt Taxonomy

Debt needs a named cost and payer.

Lenses: CH complexity/duplication/dead-code/naming/size/smells; AD
boundaries/leaks/layering/coupling/cycles/seams; DP
currency/maintenance/license/unused/skew/compatibility/lock-drift; TD
coverage/brittleness/flakes/layers/mock-drift/runtime; OP
telemetry/rollback/bring-up/oncall/performance/scaling; KN
doc-drift/undocumented/bus-factor/ownership/ADRs/onboarding.

`P` primary, `S` secondary. Use highest overlap.

| Archetype | CH | AD | DP | TD | OP | KN |
| --- | --- | --- | --- | --- | --- | --- |
| Long-lived app | P | S | S | S | S | P |
| Greenfield-on-legacy | S | P | S | P | S | S |
| High-velocity startup | P | S | S | P | P | S |
| Mature platform | S | S | P | S | P | S |
| Heavily integrated | S | S | P | S | P | S |
| Single-author project | S | S | S | S | S | P |

Map only concrete anchor conflicts for refactor/ship, coverage/deploy, upgrade/
shim, observability/simplicity, local/strategic repair, docs location, and
bus-factor/speed. Bus-factor-1 missing docs is `P0` only with transition,
successor, near deadline, or active blocker.
