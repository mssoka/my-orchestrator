# righttenantry-draft-grace-period — field notes

- `git checkout -- <file>` after a sed-tamper test-run wiped ALL uncommitted
  work in that file (lost the whole new test file's edits; had to re-apply).
  Revert tamper lines with sed on the exact line, never checkout.
- RightTenantry vacancy has NO closed_at: manual-close moment =
  `closed_notified_at` (stamped in the same UPDATE by close_vacancy.sql);
  `vacancy.updated_at` never bumps on close (editable-fields-only trigger) —
  do not anchor time-based logic to it.
- Worktree bootstrap gap: `make build` fails on `tailwindcss: command not
  found` — `ln -s /Users/moses/code/RightTenantry/node_modules node_modules`
  fixes it (gitignored, never committed).
