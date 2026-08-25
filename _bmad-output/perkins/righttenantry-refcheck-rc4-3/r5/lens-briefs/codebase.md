# LENS: codebase (source tag: `codebase`) — Perkins r5 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/_shared.md`
FIRST (shared context, inputs, lens-guards, output contract), then
`/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r5/lens-briefs/prior-findings.md`
(the r5 FIX AUDIT list — you own the codebase-class items: B1 TOCTOU wiring, N1 per-row
edit dict, N2 Escape fix, N4 substitution-response-id carry, N12 Cancel const, N14
refcheck_action_strings, N19 test hygiene).

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project (snake_case
  files, PascalCase types, `SubjectVerbObject` messages, `view_` prefix, Squirrel SQL
  modules, `data-testid` on interactive elements, copy in `copy.gleam`)?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing
  helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding? (No
  JavaScript FFI — approved packages only; Erlang FFI fine.)
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this
  change?

**Round 5 — VERIFY-DON'T-REOPEN: FIRST classify each prior codebase-class finding against
the current worktree (fixed = silent; still present/wrong fix = finding with original
severity, title prefixed `STILL PRESENT (r4): `). Then hunt NEW issues.**

**Round-specific checks:**

1. **B1 TOCTOU — the wiring question (the round's #1 mandate).** Grep the server for
   callers of `mark_awaiting_correction_wrong_person` OUTSIDE sql.gleam — exactly one:
   `apply_wrong_person` in form_handler.gleam. And `update_reference_call_status` must have
   NO caller on the wrong-person path. If the handler still executed the unguarded UPDATE,
   that's a blocker (see prior-findings (a)).
2. **Per-row edit dict (N1).** `refcheck_edit: Dict(String, RefcheckEdit)` — model, initial,
   reset, every read/write site in client.gleam + reference_panel.gleam uses dict ops (no
   leftover `option.Some(RefcheckEdit)` patterns); `gleam/dict` import in model.gleam.
3. **Escape fix (N2).** `tabindex="-1"` + `attribute.autofocus(True)` on the menu div —
   matches the confirm_modal precedent (attribute.autofocus used there); the keydown
   handler unchanged.
4. **N4 carry.** The substitution response id — decoder still returns it; the
   justification (informational; refetch authoritative) must exist as a code comment. Is
   the decoded value genuinely dead, or consumed somewhere? If consumed, the carry
   justification would be wrong — check.
5. **N12/N14.** `copy.refcheck_edit_cancel` const used by view_edit_trio (no inline
   literal); `refcheck_action_strings` includes it + `refcheck_action_correct_details`
   (copy_test.gleam ~310-345).
6. **N19 hygiene.** `model.Model(..model.initial())` fieldless update in
   refcheck_late_response_is_dropped_test (client_test.gleam ~6413) — still there?;
   objected_row_substitute_surface_test re-declaring the hooks record the `base_hooks()`
   helper exists for (reference_panel_test.gleam ~1533) — still there?; unused `eff`
   bindings in the validation tests; the unreachable `WHEN rc.correction_cycles >= 1` arm
   in find_reference_call_by_send_ref.sql — removed?
7. **Squirrel.** Generated sql.gleam matches the .sql sources byte-for-byte
   (find_reference_call_by_send_ref, mark_awaiting_correction_wrong_person,
   list_reference_calls_for_application — the decoder field shifts 6→7, 12→13 ... are
   correct and every consumer compiles against them). Timestamp handling per conventions.
8. **Migration consistency.** `20260812140000_reference_call_corrected_name.sql` — TWO
   additive columns (corrected_name + corrected_at), `IF NOT EXISTS`, 14-digit prefix;
   schema_migration_test extended; the spec doc now claims two columns.
9. **Client wiring.** New messages follow `SubjectVerbObject`; model fields initialized;
   every new message handled; refetch after action re-invokes the detail fetch.
10. **Orphan check.** Any function/const added in the r5 delta that nothing calls;
    unused imports; helpers made `pub` solely for tests that then aren't referenced.
11. **Objected menu arm (N13).** `overflow_actions`'s Objected arm uses
    `call.hooks.can_substitute_referee` (server hook, not a status re-derivation — AR-RC13).

Verify against the worktree — read the actual files. Quote exact lines in `evidence`.
