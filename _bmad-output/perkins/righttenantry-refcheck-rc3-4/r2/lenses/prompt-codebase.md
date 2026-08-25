You are reviewer **codebase** in a Perkins round-2 fix-audit.

First read /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/lenses/_shared_context.md in full. Then read the delta at /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/r1-to-r2-delta.patch. Your worktree (read code here): /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r2.

## YOUR LENS
Reality-check the delta against the actual codebase. Do the new tests reference real columns/query shapes (result->'fraud_signals'->'form_session'->>'focus_seconds_reported' path, the notification/audit tables, the channel CHECK)? Does the B1 fix match the real notify_application_scored precedent at ai_client.gleam:1925? Does the W2 slice match the real application_handler.truncate? Are there orphan symbols or broken references? Verify by reading files.

## OUTPUT
Write ONLY a JSON array to the file: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/lenses/codebase.json
Follow the OUTPUT CONTRACT in the shared context exactly. Source value MUST be "codebase". Then stop.
