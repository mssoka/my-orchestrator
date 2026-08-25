# Lens: EDGE CASE HUNTER (source: `edge`)

**First:** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/prompts/_preamble.md` in full and internalize the lens-guards.

You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

**Method:** mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself. For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

Areas worth tracing in THIS diff (verify each against the worktree, do not assume):
- Best-effort failure paths: `stamp_creation_fraud` / `stamp_one_creation_fraud` (trigger.gleam) and `build_submission_fraud_signals` / `cross_application_reuse` (form_handler.gleam) — a DB read/SQL failure degrades to honest defaults. Trace whether a failure EVER (a) fails the trigger/submit, (b) leaves a stale/half-written signal, or (c) is swallowed silently when it should propagate.
- `cross_application_reuse` SQL: `rc.contact_name <> $2` — what happens if `contact_name` is NULL? (NULL <> 'x' is NULL, i.e. excluded.) Is `contact_name` ever NULL? Check the schema. Same for `corrected_email`/`contact_email` NULL handling in COALESCE.
- Empty/missing contact handling end-to-end: a referee with no phone (line-type skip), no email, both empty — does NULLIF/`same_optional`/`exact_match` all degrade honestly?
- `uuid.from_string` failure paths (form_handler `app_uuid`, trigger `ref.id`, stamp calls) — are `Error(_)` branches all handled (not `let assert` in prod)?
- `carry_line_type` parse: empty text → Unknown; unparseable JSON → Unknown; missing `line_type` key → ? Verify each.
- The `stamp_creation_fraud_signals` SQL does a wholesale `SET fraud_signals = $2::jsonb` — trace: if the trigger re-fires for an app after some future state change, does it clobber anything? (Within rc3-7 scope, note whether re-stamping ALL rows could overwrite a value another path set.)
- `completion_seconds`: `now()` at form-context-fetch vs the eventual `submitted_at` — any path where this is negative, zero, or wildly wrong (e.g. form never opened → `form_opened_at` NULL)?
- `referee_contact_invalid` jsonb_set on a null column — COALESCE handles it; verify the path where `fraud_signals` is a non-object (already-stamped) doesn't error.

**Output:** Write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/edge.json`, using `source: "edge"`. Follow the schema, accuracy mandate, and lens-guards from the preamble. Empty array is valid. Stop when written.
