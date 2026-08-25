# Lens: CODEBASE FIT (source: `codebase`) — Perkins r2 FIX-AUDIT

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the delta actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the delta duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this delta likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types, consts no longer referenced after this change?

**This is a FIX-AUDIT round.** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/lens-common.md` FIRST — fix-audit scope (B1+W1-W5 verify FIXED), lens-guards (do NOT re-litigate, do NOT re-open rc3-4), legitimate round-2 findings.

Codebase-fit focus for this delta:
- The removed `const reason_processing_error` (N2): is it referenced ANYWHERE else after removal? (grep the repo.) Orphan check.
- The new `pub fn now_iso()` + imports `gleam/time/calendar`, `gleam/time/timestamp`: do these resolve? Is `now_iso` now the single source of the `at` stamp, or is there drift (other callers still passing `""`)?
- `outcomes_to_entries` (new helper): does it duplicate `outcome_entry` / `messages.first_name` logic? Does `messages.channel_name` / `messages.outcome_name` exist and match the `ChannelOutcome` fields? (r1 N6/N8 territory — confirm not worsened.)
- `mark_failed` now passes the per-call `reason` to `sweep_mark_failed` — does the SQL signature accept an arbitrary string? (Confirmed TEXT, but verify the Squirrel-generated function signature matches.)
- `sentry_client.BackgroundEvent` / `event_type: "ReferenceWarmHandoffLost"` / `tags`: does this match the `sentry_client` API used elsewhere?

**Inputs:** `lens-common.md`, `delta-r1-r2.patch`, `diff.patch`, `r1/consolidated.json`. Verify against worktree `/Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-5-r2` (read-only).

--- OUTPUT ---
Write ONE valid JSON array to EXACTLY: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r2/codebase.json` — then stop.
Schema per element:
```
{
  "source": "codebase",
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
ONLY the JSON array in the file. `[]` is valid. Open the file, read the cited lines, grep for orphans. Speculation without quoted evidence is dropped.
