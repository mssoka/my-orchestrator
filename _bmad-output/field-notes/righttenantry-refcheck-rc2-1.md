# Field notes: righttenantry-refcheck-rc2-1

- Squirrel types ALL cast expressions non-`Option` (even `CASE WHEN x IS NULL THEN NULL ...`) and can't codegen `timestamptz` results at all — nullable non-text columns must be `COALESCE(x::text, '')` with `NULLIF($n,'')` on writes, or you ship decode-failures/''-in-index bugs (house `ai/sql.gleam` has the latent instance).
- `make test-db-up` port 54321 can be occupied by a sibling minion's container — run your own `postgres:16-alpine` on 54322 + `TEST_DB_PORT=54322 scripts/reset-test-db.sh`, and point `DATABASE_URL` there for squirrel (never staging).
- Integration `truncate_all` in `server/test/integration/test_db.gleam` is a fixed table list — any new table without a FK to a truncated parent must be added or tests leak rows across runs.
