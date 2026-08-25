# Lens: ARCHITECTURE (source: `architecture`) — Perkins r2 FIX-AUDIT

Architectural fit review. Given the fix delta and the surrounding codebase:
- Does it follow existing patterns and conventions?
- Does it introduce unnecessary coupling between modules?
- Is there a simpler alternative with the same outcome?
- Does it respect module boundaries and separation of concerns?
- Will it create technical debt or make future changes harder?
- Does complexity match the problem? Any premature abstraction?

**This is a FIX-AUDIT round.** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/lens-common.md` FIRST — fix-audit scope (B1+W1-W5 verify FIXED), lens-guards (do NOT re-litigate, do NOT re-open rc3-4), legitimate round-2 findings.

Architectural focus for this delta:
- The B1 fix converts all 5 guarded-UPDATE Error branches to `mark_failed` + Sentry. Is the "persistent error = poison data = terminalise" decision architecturally sound vs the r1 "transient = retry" stance? (The commit comment argues a global outage fails the due-SELECT first, so a per-row UPDATE error is row-specific.) Is there a risk this terminalises rows on a transient that should retry?
- `now_iso()` exposed as `pub fn` from `sweep` and called by `sweep_handler` — is `sweep` the right home for a time helper, or does it belong in a shared util? (Boundary concern — likely a Note at most.)
- `dispatch_warm_handoff` now takes `outcomes` + does inline Sentry capture — does the inline `sentry_client.capture(...)` duplicate the `capture()` helper pattern? Is there drift?
- The W5 test seeds rows with raw `pog.query` INSERTs (not Squirrel) — consistent with the rest of the test file? (Likely carried from r1 N9 territory.)

**Inputs:** `lens-common.md`, `delta-r1-r2.patch`, `diff.patch`, `r1/consolidated.json`. Verify against worktree `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-5-r2` (read-only).

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/architecture.json` — then stop.
Schema per element:
```
{
  "source": "architecture",
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
ONLY the JSON array in the file. `[]` is valid. Open the file, read the cited lines. Speculation without quoted evidence is dropped.
