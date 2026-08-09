You are reviewing a code diff. You have read-only access to the repository and may verify the diff's claims against the actual codebase using your available tools.

--- PROJECT CONVENTIONS ---
RightTenantry is a Gleam/Lustre monorepo (client SPA + Wisp API + shared types) for an AI-powered tenant-vetting product, in production. Key conventions:
- No JavaScript FFI in the client (approved packages only: gleam_time, plinth, rsvp, modem).
- No `let assert` in production code — use `case` with explicit error handling.
- Every outbound HTTP call in server/src must set an explicit timeout via httpc.configure() |> httpc.timeout(<ms>).
- No em-dashes in any user-facing copy (global ban, CI-guarded).
- Squirrel for type-safe SQL: queries live in server/src/<module>/sql/*.sql.
- All fallible operations return Result; messages are SubjectVerbObject; landlord-facing strings live in client/src/copy.gleam.
- The email reminder system lives in server/src/inbound_email/: a two-stage gate (stage 1 = initial doc-gathering nudge, never-reminded; stage 2 = follow-up, stage-1 series completed >= 2 days ago), per-email scoping in the inbound_email_sender_state view. Bulk remind handler: handle_remind_applicants (mark_reminders_for_vacancy + mark_followup_reminders_for_vacancy → stamp + return recipients → send via send_reminders_background → clear rejected stamps).

--- DIFF ---
