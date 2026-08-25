# Lens: Codebase Fit (source: `codebase`) — Perkins RC3.5 r1

Read and follow `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/lens-prompts/_shared_context.md` first (inputs, invariants, output contract). Then apply this lens.

## YOUR LENS — reality check against the actual codebase
Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match? (e.g. `send.send_invite` / `send.send_reminder` / `send.send_co_nudge` signatures; `messages.RefereeContext` / `AttemptEntry` / `ReminderStage` / `channel_name` / `outcome_name` / `build_warm_handoff_email_html` / `warm_handoff_email_subject`; `ref_result.partial_result` / `minimal_terminal_result` / `StructureContext`; `questions.decode_draft`; `ref_slot_from_string`; `notification_dispatch.notify_reference_unreachable`; `response_helpers.require_internal_secret`; `sentry_client.BackgroundEvent` / `tags`; `sms_client.init` / `Disabled`.)
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.) Note: `result.gleam` already had a `parse_attempts` + `attempt_decoder`; `sweep.gleam` adds its own `parse_attempts_entries` + `attempt_decoder` — is that a duplication?
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.) The `send_test.gleam` change — verify the `send_warm_handoff` removal didn't orphan a test or leave a dangling reference.
- Does it leave orphan code — functions, exports, types no longer referenced after this change? (`send_warm_handoff` was removed; grep for any remaining caller. `messages.build_warm_handoff_email_html` should now have exactly one caller — the sweep's dispatch.)

## OUTPUT
Write ONLY your JSON array to: `/Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-5/r1/codebase.json`
Use `"source": "codebase"`. Then stop.
