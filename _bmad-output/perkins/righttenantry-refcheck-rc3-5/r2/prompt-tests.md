# Lens: TEST COVERAGE (source: `tests`) — Perkins r2 FIX-AUDIT

Test coverage analysis via traceability.

For each behaviour change in the delta, trace to a test (new in the delta, or existing). Classify as FULL / PARTIAL / NONE coverage. Emit one finding per gap with severity:
- blocker: P0 gap (critical path, happy + core error) OR P1 coverage <80%
- warning: P1 gap at 80–89% OR P2 gap
- note: P3 gap

Blind-spot heuristics: new/modified API endpoints without matching coverage; auth/authz paths missing negative tests; happy-path-only coverage where error handling is implied; new DB operations without integration coverage; new state transitions without boundary tests. Finally, emit ONE advisory-gate finding (title "Advisory test gate: PASS|CONCERNS|FAIL", category `coverage-gate`, severity per gate).

**This is a FIX-AUDIT round.** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/lens-common.md` FIRST — fix-audit scope (B1+W1-W5 verify FIXED), lens-guards (do NOT re-litigate, do NOT re-open rc3-4), legitimate round-2 findings.

Test-coverage focus for this delta (the W5 fix is YOUR primary subject):
- **W5 (the new `cadence_offsets_pinned_with_fake_clock_test`):** Does it actually pin the 24/24/48/48h offsets, or can it false-pass? Trace: does the sweep actually ADVANCE each seeded row this tick (so `next_attempt_at` moves)? Does `offset_seconds` measure the right thing? Does `no_key_deps()` let the sends no-op so the advances happen? Does the co-nudge gate (form-never-opened) interfere with the t24 row's advance? Could the warm-handoff dispatch (t96 row) throw and abort before the advance commits (it advances BEFORE dispatch — verify)?
- **B1 (the Error→mark_failed conversion):** Is there ANY test that a guarded-UPDATE Error now terminalises the row (status `failed`)? If not — is that a coverage gap worth flagging? (The fix changed 5 branches; none may be directly tested. Weigh: the r1 finding was a liveness/correctness blocker; is the fix's behavior pinned by any test, or does it rest on inspection only?)
- Regression: do the existing sweep integration tests (no-duplicate-T0, terminal-respect, objected/taken-over, full cadence walk) still hold at `33d237e`? Name them.

**Inputs:** `lens-common.md`, `delta-r1-r2.patch`, `diff.patch`, `r1/consolidated.json`, and the full test file `server/test/integration/reference_checks_sweep_integration_test.gleam`. Verify against worktree `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-5-r2` (read-only). NOTE: no Docker test DB is available in this round worktree — do NOT attempt to RUN tests; reason about them by reading.

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/tests.json` — then stop.
Schema per element:
```
{
  "source": "tests",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<exact lines you READ from the file, verbatim>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>",
  "round2_audit": "<FIXED | STILL OPEN | NEW | CARRIED-N<n> | N/A>"
}
```
ONLY the JSON array in the file. `[]` is valid. Open the test file, read the cited lines. Speculation without quoted evidence is dropped.
