LENS: edge (source tag: "edge") — Edge Case Hunter. EXACT OUTPUT PATH: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/lenses/edge.json`

**FIRST: read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/lenses/_shared_header.md` for the output contract, schema, and accuracy mandate.** Then apply your lens below.

## YOUR LENS — Pure path tracer

Do not comment on whether the code is good or bad — list ONLY unhandled paths reachable from the changed lines. Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself.

Pay special attention to (derive from the code, don't assume):
- **Objection stickiness (AD-6/AD-14):** does a late event (second stop POST, a late submit POST, a future bounce/sweep) move an already-`objected` row? Trace every guarded `UPDATE ... WHERE status=...` and confirm the guard. Verify `apply_objection`'s single-writer + write-only-on-row-returned.
- **One submission (AD-3):** a second POST on a terminal token — does it leak a duplicate result/audit/notification, or render the branded page?
- **Abuse-posture fake success:** does the fake-success path on decline/stop/wrong-person ACCIDENTALLY persist the state change? (stop is critical — a fake object on a leaked token would silently opt out a real referee.)
- **GET mutates nothing (prefetch safety):** `handle_stop_get` / `handle_decline_get` / `handle_wrong_person_get` — confirm they mutate nothing.
- **Wrong-person no-resend (AD-7):** `awaiting_correction` NULLs `next_attempt_at` — confirm the SQL CASE includes it.
- **Boundary inputs:** empty draft, malformed `_focus_seconds`, missing `_form_loaded_at`, corrupt UUID in row.id/application_id, null retention_due_at, token not found, DB query failure.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard. Discard handled ones silently. No editorializing. `[]` is a fine answer.
