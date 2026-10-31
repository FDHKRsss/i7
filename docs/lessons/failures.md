# Failures

_Regressions: what broke, the PROVEN root cause, and the fix._

- Assumed a `git_commit_push` tool existed and listed it as a done-criterion; this environment has no git
  tool, so the criterion was unmeetable. Root cause: relying on a tool without verifying it is available.
  Fix: redefine acceptance as "file persisted via `write_file`", and check a tool actually exists before
  making it a required step.
