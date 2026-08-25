# LENS: edge (source tag: `edge`) — Perkins r1 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract).

You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

Method: mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself — no fixed checklist. Examples: boundary conditions (empty lists, nulls, zero counts, max sizes), concurrent operations and race conditions, unhandled error paths in new code, external service unavailability (DB, APIs, auth), off-by-one errors, implicit type coercion, state the new code doesn't account for, input the new code doesn't validate.

For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard in the diff; discard handled ones silently. No editorializing.

**Round-specific paths to walk (this PR wires row actions):**

1. **Take-over races:** take-over while the sweep is mid-flight on the same row (guarded `UPDATE ... WHERE status = <expected>` 0-row result — does the handler stand down gracefully?); take-over from a terminal state (form_completed/objected/unreachable — wait, unreachable is a legal pre-state, form_completed/objected are not); double-take-over (idempotent? second confirm?). Late form completion AFTER take-over — does the form handler still transition `taken_over` → `form_completed` and notify, or does the take-over block it?
2. **Correction edge cases:** correct a row whose referee fields are empty; correct with the SAME values as the snapshot (no-op correction — cycles increment?); correction when `correction_cycles` is already 1 (should be blocked — the one-cycle rule); correction on a row not in `awaiting_correction`; concurrent correction + sweep; correction after take-over.
3. **Substitute edge cases:** double-submit (the idempotent CTE — does the second request return the existing successor WITHOUT a new row/audit?); substitute on a non-terminal row (objected/unreachable only?); substitute when the slot already has a live row; substitute with empty trio; concurrent substitute + exhaust; the audit row for substitute (old + new ids — does the idempotent path skip the duplicate audit?).
4. **Exhaustion (live):** second failure at the delivery webhooks (email bounce / SMS failure) AND the wrong-person route — both must convert to `unreachable` + `referee_contact_invalid` stamp; first failure must NOT exhaust; what happens to a row already taken over when a failure arrives (should still exhaust? or is take-over a superseding state?); exhaustion races with a correction just applied.
5. **Client-side:** menu dispatch on a row whose state changed server-side since render (stale refetch?); confirm → cancel → confirm loops; toasts on error responses; the detail refetch after action (fails? shows stale state?); `?slot=` per-row start param on the RC2.3 endpoint (unknown slot? already-started slot?).

Verify each path against the actual worktree code (read the handler + SQL), not just the diff. Report only unhandled paths. Accuracy > volume.
