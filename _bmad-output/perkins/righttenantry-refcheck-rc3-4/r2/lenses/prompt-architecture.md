You are reviewer **architecture** in a Perkins round-2 fix-audit.

First read /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/lenses/_shared_context.md in full. Then read the delta at /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/r1-to-r2-delta.patch. Your worktree (read code here): /Users/moses/.herdr/worktrees/RightTenantry/perkins-refcheck-rc3-4-r2.

## YOUR LENS
Architectural fit of the delta. Does the rework follow existing patterns (the notify_application_scored precedent for B1, the /apply truncate for W2, the form_question_pages _focus_seconds precedent for W1)? Does the N3 objected-routing branch (case on row.status inside the Declined classify arm) fit the classify design? Any new coupling or tech debt introduced by the fixes? Is complexity proportionate?

## OUTPUT
Write ONLY a JSON array to the file: /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r2/lenses/architecture.json
Follow the OUTPUT CONTRACT in the shared context exactly. Source value MUST be "architecture". Then stop.
