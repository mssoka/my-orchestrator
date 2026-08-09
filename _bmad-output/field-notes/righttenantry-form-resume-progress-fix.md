# Field notes — righttenantry-form-resume-progress-fix

- agent-browser `click` silently no-ops on the stepper's Back/Continue
  buttons under an emulated mobile viewport (sticky progress bar overlap) —
  drive stepper nav via `eval` clicks on `[data-testid=step-continue-<id>]`;
  `fill` can't set input[type=date] either (set value + dispatch input/change).
- Reseeding a resume leg without the UI: INSERT into application_draft with a
  url-safe-base64 `continue_token` and the draft `fields` JSON — the token
  seam works for any hand-minted row, no Resend round-trip needed.
- Review-swarm note: `make build` in a fresh worktree fails at tailwind
  until `npm ci` (worktrees ship no node_modules; `make test` never notices
  because js-tests use bare node).
