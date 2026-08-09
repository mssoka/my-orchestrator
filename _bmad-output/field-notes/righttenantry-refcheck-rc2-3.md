# righttenantry-refcheck-rc2-3 — field notes

- 2026-08-08 (rc2-3): pgo rejects a text param bound to a boolean column via
  `$n::boolean` (`UnexpectedArgumentType("bool", "<<\"false\">>")`) — inline the
  boolean literal into the test-seed SQL string instead (or pass a real bool);
  text→enum casts (`$n::application_status`) work fine, text→bool does not.
- 2026-08-08 (rc2-3): Gleam case-exhaustiveness bites on `pog.Returned` list
  patterns — `Ok(pog.Returned(_, [row]))` + `Ok(pog.Returned(_, []))` is NOT
  exhaustive (compiler wants the theoretical 2+-row case); use an `Ok(_) ->`
  catch-all for the "0 rows / conflict / unexpected multi-row" arm on INSERT...
  RETURNING and single-row guarded UPDATE guards. Same trap in three places.
- 2026-08-08 (rc2-3): the briefing's "Migration: ALTER TYPE reference_call_status
  ADD VALUE 'skipped'" was STALE — rc2-1 already added it; `audit_log.event_type`
  is TEXT so new event wire-strings need no migration either. Net migration count
  for the story: zero. (Another instance of "verify the briefing's stated current
  state on disk before acting" — the epics A-register + rc2-1 spec were the truth.)
