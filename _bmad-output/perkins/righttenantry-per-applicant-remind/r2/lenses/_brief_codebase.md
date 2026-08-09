Reality check against the actual codebase. Verify by reading files, not by assuming:
- Do files, functions, types, and imports referenced in the diff actually exist and match?
- Are naming conventions and style consistent with the rest of the project?
- Does the diff duplicate logic that already exists elsewhere? (Point to the existing helper in `location`.)
- Are new dependencies (imports, packages) available, or do they need adding?
- Are there existing tests this diff likely breaks? (Name them in `location`.)
- Does it leave orphan code — functions, exports, types no longer referenced after this change?

Round-2 specific: verify the new allowlist arm's Msg variant `ApiReturnedApplicantReminder` exists in msg.gleam with the shape the pattern expects, and that the 3 new integration tests reference real helpers (remind_applicant_request, assert_no_reminder_stamps) and a real endpoint route (POST /api/v1/vacancies/:id/remind-applicant).
