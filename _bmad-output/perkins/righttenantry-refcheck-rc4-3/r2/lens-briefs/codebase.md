# LENS: codebase (source tag: `codebase`) — Perkins r2 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r2/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract), then `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r2/lens-briefs/prior-findings.md` (the FIX AUDIT list — you own the codebase-class items: B3, W1, W2, W5, W7, W9, W11, N5, N6, N7, N9, N10).

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project (snake_case files, PascalCase types, `SubjectVerbObject` messages, `view_` prefix, Squirrel SQL modules, `data-testid` on interactive elements, copy in `copy.gleam`)?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding? (Remember: no JavaScript FFI — approved packages only; Erlang FFI fine.)
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

**This is round 2 of a re-review: FIRST classify each prior codebase-class finding against the current worktree (fixed = silent; still present/wrong fix = finding with original severity, title prefixed `STILL PRESENT (r1): `). Then hunt NEW issues.**

**Round-specific checks:**

1. **RC2.3 API reuse.** "Start this check now" starts via the RC2.3 API — does the client call the EXISTING endpoint (from RC2.3's story) or a new one? If new, is the RC2.3 endpoint left orphaned, or correctly extended? Check `client/src/api/reference_checks_api.gleam` against the server router arms for the RC2.3 start/skip routes.
2. **Server route arms.** The new router arms (take-over / correct / substitute) — do they match the router's existing patterns (middleware, JSON decoding, error responses)? Do the client API functions hit exactly those paths with the right methods/bodies?
3. **Shared types/decoders.** The additive payload keys (`row trio`, `taken_over_at`, `corrected_at`, `correction_cycles`) in `shared/src/shared/reference_call.gleam` — back-compat decoders (absent-key default None)? Do client decoders match server encoders field-for-field? The r1 N16: `correction_cycles` null tolerance — every additive key must decode with null/absent tolerance so an old server payload can't fail the whole decode.
4. **Migration consistency.** `20260812140000_reference_call_corrected_name.sql` — `IF NOT EXISTS`, additive only, matches the existing migration conventions (14-digit prefix)? Does it add `corrected_name` AND `corrected_at` (the code writes both?) AND the columns the code writes (`taken_over_at`, `correction_cycles` — were those already in RC4.1's migration, or are they missing here)? The r1 N15: `schema_migration_test` `amended_columns_present_test` extended with the RC4.3 additive columns?
5. **Squirrel.** New SQL files under `server/src/reference_checks/sql/` — is the generated `sql.gleam` in the diff consistent with the `.sql` sources (functions exist for each query, generated code matches the SQL semantics)? Timestamp handling per conventions (`::text` casts, `CASE WHEN $1 = '' THEN NULL`)?
6. **Client model/msg/client wiring.** New messages follow `SubjectVerbObject`; model fields initialized; `client.gleam` update handles the new messages; refetch after action actually re-invokes the detail fetch. Any message defined but never handled, or handled but never sent? The r1 W8: the `ApiReturnedRefcheckAction` id-match guard must ALSO check the route (stale responses on unrelated pages). The r1 W9: panel state reset on route change per the model.gleam doc.
7. **Orphan check.** Any function/const added in this PR that nothing calls (the r1 N5: `refcheck_toast_action_failed` unused; the r1 N6: unreachable `RefcheckCorrect` overflow arm; the r1 N7: hardcoded error string in client.gleam)? Any old code left behind that this PR was supposed to replace (e.g. a placeholder menu, a dead branch)? The r1 W5: the saving-flag wedge — failed correct/substitute must reset `saving` so the §8.3 save button re-enables.
8. **Button disabled rendering (the r1 B2 fix).** Verify in `reference_panel.gleam` that enabled action buttons OMIT the `disabled` attribute entirely (not `attribute('disabled', '')`), across Start check / Take over / Save & resend / Save & send invite — and that a serialized adjacency test pins it.

Verify against the worktree — read the actual files. Quote exact lines in `evidence`.
