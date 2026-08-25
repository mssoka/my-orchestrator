# Field notes — righttenantry-refcheck-rc4-4 (2026-08-13)

- RC4.4's "four codec variants" briefing count was the RC2.1 set; `reference_awaiting_correction` joined in RC3.6 and IS emitted — completeness demanded all FIVE variants or the dropdown stays decode-broken. Always grep the DB enum migrations, not the briefing, for the emitted set.
- The old client-side timeline sort (raw `at` string compare) silently mis-ordered same-day events: PG `::text` uses a space separator, the sweep stamps RFC3339 `T` — space (0x20) < 'T' (0x54) sorts the evening before the morning. Server-built timeline must normalise space→T before sorting (or the rc4-2 W4 "chronological" fix quietly regresses).
- Post-correction cadence restart: correct_reference_call resets attempt_count to 0, so batch index alone mislabels the re-invite as "Reminder N" — segment send batches by corrected_at boundary.
- Squirrel regen churns `application/sql.gleam` formatting hunks unrelated to new columns (reverted one) + `ai/sql.gleam` whitespace (revert whole file); verify each hunk before keeping.
- Integration suite on own container (:54328) — the sibling worktrees own 54321/54326/54327/54332-34; `TEST_DATABASE_URL=postgresql://test:test@localhost:54328/righttenantry_test gleam test -- --tag integration` after `TEST_DB_PORT=54328 bash scripts/reset-test-db.sh`.
- Gleam guards can't call functions — nested `case string.compare(...) { Gt if ... -> ... }` with `import gleam/order.{Gt}`.
