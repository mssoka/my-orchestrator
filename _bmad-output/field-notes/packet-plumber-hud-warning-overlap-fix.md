# Field notes — packet-plumber-hud-warning-overlap-fix (2026-08-14)

- `_pr_body.md` in the worktree root is a STALE leftover from a previous job
  (Job C) — write your own PR body file; never reuse it.
- The drag-rejection/cost cursor anchor (`i32(cur.x)+12, i32(cur.y)-14`) is
  now the single source of truth at the top of the drag block — hoist
  `to_screen` once, don't duplicate the anchor per branch.
- Full local suite = lint.sh + `odin test core` + `odin build app` +
  `harness.sh run|drift-check|preview-check` (CI is billing-blocked); 18/18
  harness demos green = T2 goldens byte-identical = the no-shift proof.
