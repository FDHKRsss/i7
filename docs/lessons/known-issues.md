# Known issues

_Recurring walls/gotchas and how to get past them. One bullet each._

- Regional/preferential loans (BGK + partner financiers) are normally a "nabór ciągły" with per-product
  terms and no single URL publishing one hard deadline or amount. Don't hunt for a fixed date/figure:
  record the status as "nabór ciągły", verify figures on the BGK product page / partner site, and mark
  unconfirmed values "do weryfikacji" instead of inventing a term or amount.
- EU/central programs (EIC Accelerator, Digital Europe) don't have one Polish deadline — timing is
  rolling/cut-off (EIC) or call-based (DEP), not a single Polish-portal term. Ground them on the European
  Commission / CPPC-KPK / EIT Digital page and use EUR amounts; mark unconfirmed figures "do weryfikacji"
  instead of hunting a Polish deadline or a PLN figure.
- Implement the milestone AND its tracking in one step: mark `- [x]` in `PLAN.md` AND update
  `ARCHITECTURE.md` § "Stan realizacji" + the test count, enumerating EVERY test file (incl.
  `test_mX_fix.py`) in both the count and the `unittest` command line so they match. (M4 recurred twice:
  stale tracking, then a 91-vs-96 count from omitting `test_m4_fix.py`.)
