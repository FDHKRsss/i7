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
- The TASK header's pass label can be stale: a coder was handed "STUB pass" while `PLAN.md` /
  `ARCHITECTURE.md` showed PASS 1 fully done and PASS 2 mid-flight. Don't trust the header's phase — read
  `PLAN.md` + `ARCHITECTURE.md` § "Stan realizacji" and follow the ACTUAL repo state (the docs are
  authoritative over the TASK header).
- Update milestone tracking in the SAME step as the work: mark `- [x]` in `PLAN.md` AND update
  `ARCHITECTURE.md` § "Stan realizacji" + the test count. Derive test counts with `grep -c 'def test_'`
  over EVERY test file and enumerate them all in the `unittest` command — never from memory or a partial
  list. Non-standard filenames get silently omitted: include BOTH `test_mX_fix.py` AND `test_mX_real.py`
  (recurred M4 3×, M5 2×, M2-real 1×). The authoritative count + command line live in `ARCHITECTURE.md`
  § "Stan realizacji".
- In-file status footers / progress lists (e.g. the `_Stan pliku_` note, or §7.2 open-items) are a second
  copy of the ground-state that silently falls stale after grounding — the footer still listed cards
  2.3–2.6 as "remaining to verify" after they were grounded. Update it in the SAME step as the grounding
  and add a test asserting the footer matches the grounded-card bodies (e.g.
  `test_m2_real.py::test_stan_pliku_`), so it can't drift again.
- Self-audit / verification sections tend to over-claim: a "see §7.2" cross-reference (e.g. "all ungrounded
  fragments are openly marked") must correspond 1:1 to the actual open-items list, or the audit itself is
  inconsistent and gets flagged. Before asserting such a sentence, verify it against the real report
  content, not against an aspiration.
- The deliverable `docs/granty-2026.md` grows past read_file's "is this text?" heuristic (very long table
  rows) and read_file returns "(binary or non-UTF8 file)" even though the file is valid UTF-8 (confirm
  with `file` / a `python3` `.decode('utf-8')`). Don't treat that error as corruption or give up: read the
  section you need via `run_command` (`grep -n`, `sed -n`, `cat`, or a small `python3` one-liner).
