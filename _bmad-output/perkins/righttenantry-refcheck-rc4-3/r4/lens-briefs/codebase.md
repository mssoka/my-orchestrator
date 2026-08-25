# LENS: codebase (source tag: `codebase`) — Perkins r4 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r4/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract), then `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r4/lens-briefs/prior-findings.md` (the r4 FIX AUDIT list — you own the codebase-class items: the r3 TOCTOU BLOCKER (wiring), r3 N8-client ?slot= test, r3 N5 single-slot edit, r3 N16 export toast, r3 N17 dead decoder field, r3 N8/N9-spec drift).

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project (snake_case files, PascalCase types, `SubjectVerbObject` messages, `view_` prefix, Squirrel SQL modules, `data-testid` on interactive elements, copy in `copy.gleam`)?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding? (No JavaScript FFI — approved packages only; Erlang FFI fine.)
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

**Round 4 — VERIFY-DON'T-REOPEN: FIRST classify each prior codebase-class finding against the current worktree (fixed = silent; still present/wrong fix = finding with original severity, title prefixed `STILL PRESENT (r3): `). Then hunt NEW issues.**

**Round-specific checks:**

1. **THE r3 TOCTOU BLOCKER — the wiring question (the round's #1 mandate).** The PR adds `mark_awaiting_correction_wrong_person.sql` and its generated function `mark_awaiting_correction_wrong_person` in sql.gleam. Grep the server for callers OUTSIDE sql.gleam. If the only "use" is the generated module itself and the wrong-person handler still calls `update_reference_call_status`, you have TWO findings: (a) STILL PRESENT (r3): blocker — the executed UPDATE is unguarded on taken_over_at; (b) orphan code — the guarded query + its generated code ship dead. Verify exactly which query `apply_wrong_person` executes in the worktree.
2. **RC2.3 API reuse.** Client "Start this check now" calls the EXISTING endpoint with `?slot=` per-row; server honors the slot (per-slot re-arm, no re-arm on declined).
3. **Server route arms.** New router arms match existing patterns (middleware, JSON decoding, error responses); client API functions hit exactly those paths.
4. **Shared types/decoders.** Additive payload keys with back-compat decoders; client decoders match server encoders field-for-field.
5. **Migration consistency.** `20260812140000_reference_call_corrected_name.sql` — `IF NOT EXISTS`, additive only, 14-digit prefix; adds everything the code writes; schema_migration_test extended.
6. **Squirrel.** Generated `sql.gleam` consistent with the `.sql` sources; timestamp handling per conventions. **Check the r3-rework's rewritten `find_reference_call_by_send_ref.sql`** — typed comparisons, guarded casts (r3 N14sql), and that the generated code matches the SQL text byte-for-byte.
7. **Client wiring.** New messages follow `SubjectVerbObject`; model fields initialized; every new message handled or intentionally ignored; refetch after action actually re-invokes the detail fetch. The r3 N17: the substitution response's `reference_call_id` — decoded but discarded (dead plumbing) — check whether the r3-rework dropped the field or the decode. The r3 N16: `AppCompletedRefcheckExport` toast route guard.
8. **Orphan check.** Any function/const added in this PR that nothing calls — beyond the mark_awaiting_correction_wrong_person wiring question (which is the big one): the r3 N18 `no_em_dash_test` duplicate disjunct; unused imports; helpers made `pub` solely for tests that then aren't referenced.
9. **Button disabled rendering (r1 B2 — verify still holds).** Enabled action buttons OMIT the `disabled` attribute; serialized adjacency test pins it.
10. **The r3 W6 queued take-over.** Queued rows offer "Take over manually" AND the Queued arm of row_detail renders the take-over confirm (a menu entry with no confirm surface = dead control — read reference_panel.gleam's Queued arm).

Verify against the worktree — read the actual files. Quote exact lines in `evidence`.
