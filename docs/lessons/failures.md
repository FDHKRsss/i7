# Failures

_Regressions: what broke, the PROVEN root cause, and the fix._

- Recorded "brak git" as an environment fact without verifying; a later live check showed the git CLI IS
  available (commit `5b58528` worked), so the stale note and its "no-commit" acceptance rule were wrong.
  Root cause: asserting a tool/environment fact from memory instead of a quick command. Fix: verify with a
  real command (`git status`) before making tool availability a done-criterion or recording it as fact.
