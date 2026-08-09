
--- SPEC / CONTEXT ---
This PR adds a per-applicant "Remind"/"Follow up" button to the landlord Awaiting list, coexisting with the existing bulk "Send reminder to N" button.

CRITICAL LENS-GUARD (deliberate design choices — do NOT flag as defects):
- Do NOT flag "no force-remind / can't bypass the stage gate" as a defect. Gate-respecting-only is the user-confirmed design; force-remind is a deferred follow-up, not a gap. The two-stage gate MUST be respected.
- Do NOT flag "reuses the bulk plumbing instead of standalone" as a defect. Reusing the email template/sending/validation (valid_recipients, send_reminders_background) is the explicit requirement — no duplicate plumbing. Verify the reuse is correct, not that it exists.
- Do NOT flag the bulk button still existing, or the buttons coexisting, as redundancy. The per-applicant button is deliberately ADDITIVE.

Legitimate findings in this area WOULD be: the single-applicant path not faithfully mirroring the bulk's atomicity (stamp-then-send, un-stamp on send-time validation failure); a gate breach (per-applicant endpoint sending a reminder the two-stage gate should suppress — double-send, or stage-2 when only stage-1 is due; the re-enquiry edge of old stage-1 + fresh row is the key case); owner-check/closed-vacancy gaps; stamp races (concurrent per-applicant + bulk, or two per-applicant clicks — is the server-side guard real, not just client-side?); PII leakage (applicant emails logged/echoed beyond the legitimate recipient); em-dashes in user-facing copy; broken Gleam/JS parse; missing tests for pinned behavior.

WORKTREE (the reviewed checkout — verify all claims against these files): /Users/moses/.herdr/worktrees/RightTenantry/perkins-per-applicant-remind-r1

Full specs (read both with your read tool):
- Round briefing: /Users/moses/code/_bmad-output/briefings/perkins-righttenantry-per-applicant-remind-r1.md
- Original job briefing (the spec with acceptance criteria): /Users/moses/code/_bmad-output/briefings/righttenantry-per-applicant-remind.md

--- YOUR LENS ---
