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
- `test_m2_real.py::test_stan_pliku_footer_not_stale` asserted the literal phrase `pozostałe karty (…)`;
  the M3 regional grounding legitimately rewrote that footer clause, so the test went red and the M3-real
  acceptance stuck. Root cause: a guard test written to prevent footer drift itself asserted a literal
  surface phrase instead of semantic content. Fix: assert the semantic anchor (the footer's "remaining"
  clause no longer names the already-grounded cards 2.3–2.6), never a verbatim phrase. Recurrence of the
  "literal vs semantic" trap above, this time in a guard test rather than the report body.
- M5 test reconciliation reported "130 tests / 7 files, all green" and called the record "correct", while
  the durable record and reality were 138/8 (the agent omitted `test_m5_fix.py`, 8 tests). Root cause:
  running `grep -c 'def test_'` and `python3 -m unittest` on a partial file list (skipping
  `test_m5_fix.py`) and asserting the count from memory/a prior summary instead of the real run. Fix:
  enumerate EVERY test file (incl. `test_mX_fix.py`) in both commands and trust the actual output
  (→ 138 tests OK).
- A step was rejected as scope drift after editing only `docs/lessons/*` (test-count bookkeeping) and
  neither advancing `docs/granty-2026.md` nor closing any `PLAN.md` milestone. Root cause: treating
  test-inventory / lessons reconciliation as a step's deliverable instead of the report. Fix: a
  build/verification step must advance the report (PASS 2 grounding) and close a milestone; lessons /
  tracking / test-count edits are side effects, never the whole step.
