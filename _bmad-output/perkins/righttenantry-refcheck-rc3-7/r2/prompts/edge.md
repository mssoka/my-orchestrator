# Lens: EDGE CASE HUNTER (source: `edge`)

**First:** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/prompts/_preamble.md` in full and internalize the lens-guards + the fix-audit scope.

You are a pure path tracer. Do not comment on whether the code is good or bad — list only unhandled paths reachable from the changed lines.

**Method:** mechanically walk every branching path and boundary condition directly reachable from the diff hunks. Derive edge classes from the changed code itself. For each path, determine whether the diff handles it. Report ONLY unhandled paths that lack an explicit guard; discard handled ones silently. No editorializing.

## Fix-audit priority — B1 (the r1 BLOCKER)

**B1 is your primary fix-audit target.** Trace the full stamp path at `5576ccb` and VERIFY the guard holds. Read these in order:
- `trigger.gleam::create_eligible_slots` — does `list.try_fold` now collect `created_ids` (List(String)) instead of a count? Does it call `stamp_creation_fraud(..., created_ids)` only after the tx commits?
- `trigger.gleam::stamp_creation_fraud` — does `case created_ids { [] -> Nil; _ -> ... }` skip entirely on empty? Does `to_stamp = list.filter(all_refs, fn(r) { list.contains(created_ids, r.id) })` scope the WRITE to only newly-created rows?
- `trigger.gleam::create_one_slot` — does it return `Some(id)` on a real insert and `None` on ON-CONFLICT (so created_ids holds only real inserts)?
- **The B1 invariant to confirm:** a re-trigger (`handle_start` re-fires `run_create_checks`) where every slot conflicts → `created_ids == []` → stamp skipped → a previously-submitted sibling's `form_session` is NOT wiped. Also: a re-trigger that creates a NEW row (a freed slot) stamps ONLY that new row, not the submitted sibling.

If B1 is correctly fixed → it is FIXED (do NOT file it as a finding). If the guard is missing, partial, or a new path escapes it → file it (still a blocker, mark "B1 not fixed in r2").

## Delta pass — new paths the fix introduced

Trace whether the B1 fix (the `created_ids` collection + the `to_stamp` filter) or the W1 extraction (`fraud_inputs.gleam`) introduced any new unhandled path:
- Does `list.contains(created_ids, r.id)` correctly match the row ids? (string compare; any case/format mismatch would silently stamp nothing.)
- Does the `stamp_creation_fraud` read of `all_refs` (the full application set) still occur even when only new rows are stamped? (Fine — the COMPUTATION reads all refs, only the WRITE is scoped. But verify a read failure degrades honestly to null, not a crash.)
- `cross_application_reuse` / `other_refs_from_rows` in `fraud_inputs.gleam` — a DB read failure degrades to `False` / `[]` honestly? A `uuid.from_string` Error branch handled?
- `effective_contact(Some(""), snapshot)` — does it now return `snapshot` (the r1 N7 fix)? Trace `Some("") → opt_nonempty("") → None → snapshot`.
- `carry_line_type` — empty/missing-key/unparseable → Unknown (no panic)?
- Any path where `stamp_one_creation_fraud` could stamp a row NOT in created_ids, or skip a row that IS in created_ids?

Report ONLY unhandled paths lacking an explicit guard. A correctly-guarded path is discarded silently.

**Output:** Write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r2/edge.json`, using `source: "edge"`. Follow the schema, accuracy mandate, and lens-guards from the preamble. Empty array is valid. Stop when written.
