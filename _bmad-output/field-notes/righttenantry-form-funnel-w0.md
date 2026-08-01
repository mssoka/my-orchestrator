# Field notes — righttenantry-form-funnel-w0 (2026-07-31)

- `server/priv/static/*` is gitignored with a per-file exception list — any new
  static asset MUST get a `!path` exception in `.gitignore` or it silently
  never deploys (caught only by the review swarm).
- Squirrel: `run_squirrel.sh` sources `.env` and clobbers your override —
  run `cd server && DATABASE_URL=postgres://test:test@localhost:54321/righttenantry_test gleam run -m squirrel`
  directly after `make test-db-up` (never let it point at staging), and
  revert the formatter churn it leaves in unrelated generated files.
- gleam `decode.subfield` + `decode.optional` does NOT tolerate missing keys
  (the whole decode fails) — for back-compat payloads use
  `decode.optional_field(..., default, ...)` at the parent level.
