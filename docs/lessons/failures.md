# Failures

_Regressions: what broke, the PROVEN root cause, and the fix._

- Recorded "brak git" as an environment fact without verifying; a later live check showed the git CLI IS
  available (commit `5b58528` worked), so the stale note and its "no-commit" acceptance rule were wrong.
  Root cause: asserting a tool/environment fact from memory instead of a quick command. Fix: verify with a
  real command (`git status`) before making tool availability a done-criterion or recording it as fact.
- Card 4.4's Fast Track direction was inverted (recorded "EIT Digital → EIC Accelerator"; the source says
  EIC Accelerator companies / Seal-of-Excellence laureates apply to the EIT Digital Accelerator, i.e.
  EIC → EIT Digital). Root cause: asserting a relationship/direction claim from memory instead of
  re-reading the cited source. Fix: re-fetch the source and transcribe the exact sentence before stating
  "which feeds into which".
- test_m5.py initially asserted exact surface strings (`osoba prawna`, `Sekcja 5`) that the report
  legitimately renders as inflected Polish (`osobie prawnej`) or bold Markdown (`**5**`), causing false
  red tests. Root cause: asserting literal wording/formatting instead of semantic content. Fix: assert
  stable tokens/identifiers and semantic presence (`prawn`, the number, `karta X.Y` references), never an
  exact case/declension form or `**`/`*` marker.
- M5 test reconciliation reported "130 tests / 7 files, all green" and called the record "correct", while
  the durable record and reality were 138/8 (the agent omitted `test_m5_fix.py`, 8 tests). Root cause:
  running `grep -c 'def test_'` and `python3 -m unittest` on a partial file list (skipping
  `test_m5_fix.py`) and asserting the count from memory/a prior summary instead of the real run. Fix:
  enumerate EVERY test file (incl. `test_mX_fix.py`) in both commands and trust the actual output —
  `python3 -m unittest tests.test_m1 tests.test_m2 tests.test_m3 tests.test_m3_fix tests.test_m4 tests.test_m4_fix tests.test_m5 tests.test_m5_fix`
  → `Ran 138 tests ... OK` (19+14+19+19+20+11+28+8 = 138).
