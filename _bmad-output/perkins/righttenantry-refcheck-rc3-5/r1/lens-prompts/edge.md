# Lens: Edge Case Hunter (source: `edge`) — Perkins RC3.5 r1

Read and follow `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/lens-prompts/_shared_context.md` first (inputs, invariants, output contract). Then apply this lens.

## YOUR LENS — pure path tracer
You are a pure path tracer. Do not comment on whether the code is good or bad — list only **unhandled paths** reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, Resend, Twilio), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate, a `next_attempt_at`/`attempt_count` combination the cadence doesn't expect, a decode/JSON-parse failure mid-tick.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

Concentrate on the cadence engine (`server/src/reference_checks/sweep.gleam`), the 5 SQL guarded updates (`sql/sweep_*.sql`), the due-SELECT, and the warm-handoff dispatch. The hard questions: what happens on a decode failure mid-row, a duplicate concurrent tick, a row with `attempt_count` that doesn't match any case, a Twilio/Resend no-op that returns an unexpected shape, a `next_attempt_at` already NULL, a form-token mint collision, the warm-handoff dispatch running but the guarded advance having returned 0 rows.

## OUTPUT
Write ONLY your JSON array to: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/edge.json`
Use `"source": "edge"`. Then stop.
