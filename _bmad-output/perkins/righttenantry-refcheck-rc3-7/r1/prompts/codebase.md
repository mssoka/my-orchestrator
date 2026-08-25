# Lens: CODEBASE FIT (source: `codebase`)

**First:** Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/prompts/_preamble.md` in full and internalize the lens-guards.

Reality check against the actual codebase. Verify by reading files in the worktree, NOT by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Specifics worth checking in THIS diff (verify against the worktree):
- **Orphan code.** `result.gleam`'s stub `form_session_fraud_signals` was removed. Verify NOTHING still calls it (grep). The old `referee_number_wrong` slug — verify it's gone (grep the whole worktree, not just the diff). Any now-unused import?
- **Squirrel regen consistency.** `sql.gleam` is Squirrel-generated. The diff adds `CountCrossApplicationContactReuseRow`, `GetApplicationReferenceContactsRow`, `StampCreationFraudSignalsRow`, `StampRefereeContactInvalidRow` types + functions, and amends `GetApplicationReferenceDataRow` / `GetFormContextByFormTokenRow`. Verify each generated function matches its `.sql` file (param count, the SQL text embedded, the `::text` casts). Spot-check that the `get_form_context_by_form_token` column ordering in the decoder (`decode.field(24..31)`) matches the SELECT column order in the `.sql`.
- **`lookup.line_type_from_string` / `line_type_to_string`** — verify `LineType` is the existing type with variants `Mobile`/`Landline`/`VoIP`/`Unknown` (case + capitalisation). The string mapping uses lowercase `"voip"` — consistent?
- **`request_helpers.client_ip` / `client_user_agent`** — verify these helpers exist and are the established capture functions.
- **`stamp_creation_fraud_signals` SQL comment says `fraud_signals: TEXT`** but the Squirrel function signature takes `arg_2: Json` and does `json.to_string`. Is that an inconsistency that matters, or cosmetic? (Read the `.sql` and the generated fn.)
- **`fraud_signals` column pre-existence.** The PR claims no migration (column from rc2-1). Verify the column exists in the migrations (`supabase/migrations/`) and is `jsonb` nullable — grep.
- **Existing tests likely to break:** `result_test.gleam` (updated in diff), any other test that constructs `StructureContext` or reads `get_form_context_by_form_token` rows.

Verify each claim by reading the actual files.

**Output:** Write ONLY a JSON array to `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-7/r1/codebase.json`, using `source: "codebase"`. Follow the schema, accuracy mandate, and lens-guards from the preamble. Empty array is valid. Stop when written.
