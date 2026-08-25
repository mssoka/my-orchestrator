# Lens: EDGE CASE (source: `edge`) — Perkins r2 FIX-AUDIT

You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the r1→r2 fix delta. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs), off-by-one errors, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

**This is a FIX-AUDIT round.** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/lens-common.md` FIRST — it defines the fix-audit scope (B1+W1-W5 to verify FIXED), the lens-guards (do NOT re-litigate r1 findings or re-open rc3-4), and what a legitimate round-2 finding is. Your job: verify the fixes don't leave a NEW unhandled path, and re-trace the paths the fix delta touched. Pay special attention to:
- The `mark_failed` Error-branch conversion (B1): can `mark_failed` itself fail silently? Does the row actually leave the due-queue? Does a transient DB blip now wrongly terminalise a row?
- `dispatch_warm_handoff` threading `outcomes` (W2): empty outcomes list, outcomes with non-email channels, the append ordering.
- `now_iso()` (W1): format edge cases, the SQL cast path.
- The W5 test's seed/select: does it actually exercise the cadence advance, or could it false-pass?

**Inputs to read:** `lens-common.md`, then `delta-r1-r2.patch` (the fix), `diff.patch` (full feature), `r1/consolidated.json` (prior findings). Verify claims against the worktree at `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-5-r2` (read-only).

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/edge.json` — then stop.
Schema per element:
```
{
  "source": "edge",
  "severity": "blocker" | "warning" | "note",
  "category": "<short tag>",
  "title": "<one-line summary>",
  "location": "<file:line | file:hunk | N/A>",
  "evidence": "<exact lines you READ from the file, verbatim. 'N/A' ONLY for a no-code-anchor claim.>",
  "detail": "<≤40 words>",
  "recommended_fix": "<≤40 words>",
  "round2_audit": "<FIXED | STILL OPEN | NEW | CARRIED-N<n> | N/A>"
}
```
ONLY the JSON array in the file (no prose/fencing). `[]` is valid. Open the file, read the cited lines — do not guess. A finding without locatable evidence is a hallucination; drop it.
