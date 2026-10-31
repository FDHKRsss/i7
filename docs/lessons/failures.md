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
