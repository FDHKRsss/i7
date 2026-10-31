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
- Update milestone tracking in the SAME step as the work: mark `- [x]` in `PLAN.md` AND update
  `ARCHITECTURE.md` § "Stan realizacji" + the test count. Derive test counts with `grep -c 'def test_'`
  over EVERY test file (incl. `test_mX_fix.py`) and enumerate them all in the `unittest` command — never
  from memory or a partial list. This recurred across M4 (3×) and M5 (2×); the authoritative count and
  command line live in `ARCHITECTURE.md` § "Stan realizacji".
