# LENS: codebase (source tag: `codebase`) — Perkins r3 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r3/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract), then `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r3/lens-briefs/prior-findings.md` (the FIX AUDIT list — you own the codebase-class items: r2 W3 (route guard), r2 W5 (identical-trio), r2 W6 (queued take-over), r2 W8 (coverage-gate — the advisory), r2 N2 (spec drift), r2 N3 (ON CONFLICT predicate), r2 N5 (single-slot edit), r2 N8 (client `?slot=`), r2 N12 (name caption), r2 N13 (name-twice caption), r2 N15 (update_trio bogus error)).

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project (snake_case files, PascalCase types, `SubjectVerbObject` messages, `view_` prefix, Squirrel SQL modules, `data-testid` on interactive elements, copy in `copy.gleam`)?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding? (Remember: no JavaScript FFI — approved packages only; Erlang FFI fine.)
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

**This is round 3 of a re-review: FIRST classify each prior codebase-class finding against the current worktree (fixed = silent; still present/wrong fix = finding with original severity, title prefixed `STILL PRESENT (r2): `). Then hunt NEW issues.**

**Round-specific checks:**

1. **RC2.3 API reuse.** "Start this check now" starts via the RC2.3 API — does the client call the EXISTING endpoint with `?slot=` per-row, and does the server honor the slot (r2 N4: per-slot re-arm ONLY the requested slot, no re-arm on declined)? Check `client/src/api/reference_checks_api.gleam` against the server router arms.
2. **Server route arms.** The new router arms (take-over / correct / substitute) — match the router's existing patterns (middleware, JSON decoding, error responses)? Do the client API functions hit exactly those paths with the right methods/bodies?
3. **Shared types/decoders.** The additive payload keys (`taken_over_at`, `corrected_at`, `correction_cycles`, corrected trio) in `shared/src/shared/reference_call.gleam` — back-compat decoders (absent-key/null default)? Do client decoders match server encoders field-for-field?
4. **Migration consistency.** `20260812140000_reference_call_corrected_name.sql` — `IF NOT EXISTS`, additive only, 14-digit prefix? Does it add everything the code writes (`corrected_name`, `corrected_at`, `taken_over_at`, `correction_cycles` — were some already in RC4.1's migration)? The `schema_migration_test` `amended_columns_present_test` extended with the RC4.3 additive columns (r1 N15)?
5. **Squirrel.** New SQL files under `server/src/reference_checks/sql/` — generated `sql.gleam` consistent with the `.sql` sources? Timestamp handling per conventions (`::text` casts, `CASE WHEN $1 = '' THEN NULL`)? **The r2 W1 fix: the stale-bounce gate moved into SQL — is the SQL comparison genuinely typed `timestamptz >= timestamptz` (not `::text`)?**
6. **Client model/msg/client wiring.** New messages follow `SubjectVerbObject`; model fields initialized; `client.gleam` update handles the new messages; refetch after action actually re-invokes the detail fetch. Any message defined but never handled, or handled but never sent? **The r2 W3 fix: the `ApiReturnedRefcheckAction` id-match guard must ALSO check the route (stale responses on unrelated pages must be dropped — toast AND refetch).** The r2 N8: the client's `?slot=` wire format must be tested. The r2 N12: the duplicate name caption must be gone.
7. **Orphan check.** Any function/const added in this PR that nothing calls? The r2 N15: `update_trio`'s unknown-slot arm — does it still fabricate a bogus `UnexpectedArgumentCount` error? Any old code left behind that this PR was supposed to replace? The r2 W5: the substitute prefill must be EMPTY (not the terminal referee's own contact) — verify in the client.
8. **Button disabled rendering (the r1 B2 fix — verify still holds).** Enabled action buttons OMIT the `disabled` attribute entirely; serialized adjacency test pins it.
9. **The r2 W6 fix.** Queued rows must offer "Take over manually" (the server hook `can_take_over` is True for queued rows) — verify the client affordance now covers queued rows.

Verify against the worktree — read the actual files. Quote exact lines in `evidence`.
