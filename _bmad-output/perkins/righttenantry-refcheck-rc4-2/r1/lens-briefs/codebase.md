# LENS: codebase (source tag: `codebase`) — Perkins r1 refcheck rc4-2

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r1/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

Reality check against the actual codebase. Verify by reading files, not by assuming:

- **Files/functions/types referenced in the diff actually exist and match.** New imports in `client/src/client.gleam` (msg, shared/reference_call, set), `client/src/pages/application_detail.gleam` (components/reference_panel), `client/src/components/reference_panel.gleam` (components/contact_chip, helpers/format, shared/application, shared/reference_call constructors, lustre keyed). Do `contact_chip.view`'s labelled args (icon:, value:, kind:, on_copy:, testid:) match the real signature? Does `format.format_timestamp_short` exist with that signature? Does `format.format_currency` exist? Does `msg.UserCopiedContact` exist? Does `application.Application` have all the fields used in the fixture (landlord_ref_name, character_ref_name, employer_ref_name, reference_contact_choice, etc.)? Does `ApplicationDetail` have `attestation_on_file` and `reference_calls`?
- **Shared type shape.** `ReferenceCallDetail` constructor field ORDER in the test fixtures must match the record definition (labelled args are order-free, but record updates `..row(...)` and positional construction must be right). `ReferenceCallHooks` constructor, `ReferenceCallAttempt` fields (at, channel, outcome, detail), `RefSlot` variants.
- **Server row type.** `ListReferenceCallsForDetailRow` gained two fields — is every construction site updated (test fixtures, `sample_reference_call_row`), and the Squirrel-generated decoder field indices (7/8 → 9/10) consistent with the SQL SELECT order?
- **Naming/style consistency** with the rest of the project (snake_case, msg naming, view_ prefixes, labelled args, data-testid conventions).
- **Duplication.** Does the panel duplicate logic that exists elsewhere (e.g. month_abbr vs helpers/format's month_abbr — check `client/src/helpers/format.gleam` line ~155 has a `month_abbr`; the new `copy.gleam` also has one — duplicate?; status-pill class strings elsewhere; word-maps elsewhere)?
- **Existing tests this diff likely breaks.** grep for existing tests touching `ReferenceCallDetail` construction (client tests, shared tests, server tests) — do they all pass the new required fields?
- **Orphan code.** Any new exports unused, or existing code left orphaned by the change?

For each finding, quote the exact lines and name the conflicting/duplicated location. Verify against the worktree.
