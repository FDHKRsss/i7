# Patterns

_Reusable techniques that worked, so they are reused not rediscovered._

- Per-milestone verification: a small unittest `tests/test_mX.py` asserting the deliverable
  `docs/granty-2026.md` is on disk and contains that milestone's required content; run via
  `python3 -m unittest tests.test_mX`. Encode the actual acceptance checks as assertions: every card has
  all 10 schema fields, a source URL with an access date NOT post-dated (≤ today), beneficiary split into
  physical/legal, digital/IT scope, and no `TODO` placeholders.
- When a milestone ends with a specific correction or grounding (e.g. a card re-attributed to a dated
  source, or a figure flagged `do weryfikacji`), extend that milestone's unittest to assert the exact fix.
  Generic format checks (10 fields, URL, access date, no TODO) still pass even if the specific correction
  regresses — so the specific fix needs its own assertion.
- When two official sources describe the same instrument under different names or list different products,
  don't silently pick one: keep the official/current name and add an explicit note recording the
  discrepancy, and attribute each table row to its exact source (a `†` marker on the row + a footnote
  under the table) instead of one blanket citation.
