# LENS: codebase (source tag: `codebase`) — Perkins r2 refcheck rc4-2

Read `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc4-2/r2/lens-briefs/_shared.md` FIRST (shared context, inputs, load-bearing lens-guards, output contract).

Reality check against the actual codebase. Verify by reading files, not by assuming:

- **Files/functions/types referenced in the diff actually exist and match.** New imports in `client/src/client.gleam` (msg, shared/reference_call, set), `client/src/pages/application_detail.gleam` (components/reference_panel), `client/src/components/reference_panel.gleam` (components/contact_chip, helpers/format, shared/application, shared/reference_call constructors, lustre keyed). Do `contact_chip.view`'s labelled args match the real signature? Does `format.format_timestamp_short` exist with that signature? Does `format.format_currency` exist? Does `msg.UserCopiedContact` exist? Does `application.Application` have all the fields used in the fixture? Does `ApplicationDetail` have `attestation_on_file` and `reference_calls`?
- **Shared type shape.** `ReferenceCallDetail` constructor field ORDER in the test fixtures must match the record definition (labelled args are order-free, but record updates `..row(...)` and positional construction must be right). `ReferenceCallHooks` constructor, `ReferenceCallAttempt` fields (at, channel, outcome, detail), `RefSlot` variants.
- **Server row type.** `ListReferenceCallsForDetailRow` gained two fields — is every construction site updated (test fixtures, `sample_reference_call_row`), and the Squirrel-generated decoder field indices consistent with the SQL SELECT order?
- **r1 fix audit — codebase half (verify, don't re-open):**
  - W2: `refcheck_choice_word` maps wire value `"landlord"` (not the phantom `"their_landlord"`), and the total-match word-map test exists.
  - W3: `relationship_other` renders with the parent "Other" row.
  - W4: the form-opened timeline line inserts chronologically.
  - W5: objected-state copy uses gender-neutral phrasing (no hardcoded 'him').
  - W7: character slot's `field_keys` (or the count logic) excludes `free_text_signals` — 6-of-6 for a complete character reference.
  - Notes: dead const `refcheck_off_contacts_label` removed or now used; `month_abbr` dedup (one copy, not two); keyed mini-timeline.
- **Naming/style consistency** with the rest of the project (snake_case, msg naming, view_ prefixes, labelled args, data-testid conventions).
- **Duplication.** Does the panel duplicate logic that exists elsewhere (status-pill class strings elsewhere; word-maps elsewhere; formatters)?
- **Existing tests this diff likely breaks.** grep for existing tests touching `ReferenceCallDetail` construction (client tests, shared tests, server tests) — do they all pass the new required fields?
- **Orphan code.** Any new exports unused, or existing code left orphaned by the change (e.g. a removed `is_terminal` with a lingering caller)?

For each finding, quote the exact lines and name the conflicting/duplicated location. Verify against the worktree.
