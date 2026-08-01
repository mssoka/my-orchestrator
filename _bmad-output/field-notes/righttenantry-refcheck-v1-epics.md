# Field notes: righttenantry-refcheck-v1-epics (2026-07-31)

- The refcheck v1 architecture and UX docs (both "final" 2026-07-29) contradict
  each other in 4+ places (correction mechanics, autosave/partial, link TTL,
  notification types) — when two same-day design docs both claim to be binding,
  diff them BEFORE writing stories; the UX §15 decisions record is the
  tiebreaker only where it explicitly names the decision.
- Working lavish HTML recipe for large markdown: `npx -y marked --gfm -o
  .lavish/_body.html <file>.md` (writes to file, no pipe truncation), then a
  python file-write wrapper for the brand CSS/hero — 88KB artifact, tail
  verified, no truncation (confirms the 2026-07-29 curated trap).
- User redirected the trigger mid-job (shortlist → new `viewed` status): check
  the actual status enum + stepper component in the repo before spec'ing a
  trigger story (`client/src/components/status_stepper.gleam`,
  `shared/src/shared/application.gleam` — enum value needs DB + shared +
  client + PATCH validation updates).
