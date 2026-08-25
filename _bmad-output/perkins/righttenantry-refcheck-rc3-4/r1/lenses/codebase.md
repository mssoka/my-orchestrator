LENS: codebase (source tag: "codebase") — Codebase fit / reality check. EXACT OUTPUT PATH: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/lenses/codebase.json`

**FIRST: read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r1/lenses/_shared_header.md` for the output contract, schema, and accuracy mandate.** Then apply your lens below.

## YOUR LENS — Reality check against the actual codebase

Verify by reading files, not assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (e.g. `reference_call.Completed`, `sql.Refused`/`sql.Objected`/`sql.AwaitingCorrection`/`sql.ContactInitiated`, `result.StructureContext`, `result.minimal_terminal_result`, `messages.ChannelOutcome`, `event_type.ReferenceCallCompleted/Declined/Objected/WrongPerson`, `request_helpers.client_ip`/`client_user_agent`)
- Are naming conventions + style consistent with the rest of the project?
- Does the diff duplicate logic that already exists? Point to the existing helper in `location`.
- Are new dependencies (imports, packages) available?
- Are there existing tests this diff likely breaks? Name them.
- Does it leave orphan code — functions/exports/types no longer referenced?

**Carry-forward verification (HIGH PRIORITY — the briefing asks to confirm these are folded):**
- **N3:** the rc3-3 r2 note said delete `form_handler.get_value` and route its call sites through `application_handler.get_form_value` (the local copy omitted the trim — a drift hazard). Grep `form_handler.gleam` for any remaining `get_value` (local def) vs `application_handler.get_form_value` calls. Is it actually folded?
- **N6:** the rc3-3 r2 note said extract a shared `view_post_form` (the briefing calls it `view_resend_form` in one place, `view_post_form` in the minion's completion notes) in `form_pages.gleam`, used by resend + the new exit forms. Confirm the extract exists and is used by both.

**JSONB field-note check (from the briefing):** the integration tests should extract via `result->>'field'` (NOT substring on `result::text`), and status args to Squirrel queries should be `sql.Refused`/`sql.Objected` (the Squirrel-generated enum, NOT `shared.reference_call.Refused`). Confirm.

For each finding, cite file:line + the existing helper/pattern. `[]` is a fine answer.
