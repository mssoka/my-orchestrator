- source_spec: `_bmad-output/implementation-artifacts/spec-pr-review-sensor.md`
  summary: Commit a reproducible stubbed-pi test harness for nefario-watch (this change verified via an ephemeral /tmp harness; the repo has no test infra for .pi extensions at all).
  evidence: Step-04 Blind Hunter finding — the extension's I/O matrix (now 4 sensors) can only be re-verified by hand; previous sensors shipped the same way, so the gap pre-dates this story and needs a repo-level decision on where extension tests live.
