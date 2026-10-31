# Patterns

_Reusable techniques that worked, so they are reused not rediscovered._

- Per-milestone verification: a small unittest `tests/test_mX.py` asserting the deliverable
  `docs/granty-2026.md` is on disk and contains that milestone's required content; run via
  `python3 -m unittest tests.test_mX`.
