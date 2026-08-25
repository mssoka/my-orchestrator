# LENS: codebase (source tag: `codebase`) — Perkins r1 refcheck rc4-3

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-3/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, lens-guards, output contract).

Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project (snake_case files, PascalCase types, `SubjectVerbObject` messages, `view_` prefix, Squirrel SQL modules, `data-testid` on interactive elements, copy in `copy.gleam`)?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding? (Remember: no JavaScript FFI — approved packages only; Erlang FFI fine.)
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

**Round-specific checks:**

1. **RC2.3 API reuse.** "Start this check now" starts via the RC2.3 API — does the client call the EXISTING endpoint (from RC2.3's story) or a new one? If new, is the RC2.3 endpoint left orphaned, or correctly extended? Check `client/src/api/reference_checks_api.gleam` against the server router arms for the RC2.3 start/skip routes.
2. **Server route arms.** The 3 new router arms (take-over / correct / substitute — plus whatever the briefing says: "3 router arms; 4 audit events") — do they match the router's existing patterns (middleware, JSON decoding, error responses)? Do the client API functions hit exactly those paths with the right methods/bodies?
3. **Shared types/decoders.** The additive payload keys (`row trio`, `taken_over_at`, `correction_cycles`) in `shared/src/shared/reference_call.gleam` — back-compat decoders (absent-key default None)? Do client decoders match server encoders field-for-field?
4. **Migration consistency.** `20260812140000_reference_call_corrected_name.sql` — `IF NOT EXISTS`, additive only, matches the existing migration conventions (14-digit prefix)? Does it add `corrected_name` AND the columns the code writes (`taken_over_at`, `correction_cycles` — were those already in RC4.1's migration, or are they missing here)?
5. **Squirrel.** New SQL files under `server/src/reference_checks/sql/` — is the generated `sql.gleam` in the diff consistent with the `.sql` sources (functions exist for each query)? Timestamp handling per conventions (`::text` casts, `CASE WHEN $1 = '' THEN NULL`)?
6. **Client model/msg/client wiring.** New messages follow `SubjectVerbObject`; model fields initialized; `client.gleam` update handles the new messages; refetch after action actually re-invokes the detail fetch. Any message defined but never handled, or handled but never sent?
7. **Orphan check.** Any function/const added in this PR that nothing calls (e.g. a copy constant never rendered, an API function never invoked, a SQL function never used)? Any old code left behind that this PR was supposed to replace (e.g. a placeholder menu, a dead branch)?

Verify against the worktree — read the actual files. Quote exact lines in `evidence`.
