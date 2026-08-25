# Field notes — righttenantry-refcheck-rc1-1-grapheme-fix

- Gleam `string.slice` counts GRAPHEMES while Postgres `length()` counts CODEPOINTS — codepoint-bounded slicing (`to_utf_codepoints |> list.take |> from_utf_codepoints`) is the only cut that guarantees a DB CHECK `length() <= N` holds for adversarial multi-codepoint headers (ZWJ emoji: 1 grapheme = 7 codepoints).
- Test-DB port 54321 is contended across sibling worktrees — spin your own `postgres:16-alpine` container on a free port and pass `TEST_DATABASE_URL=postgresql://test:test@localhost:<port>/righttenantry_test` to `gleam test -- --tag integration` (Makefile hardcodes 54321).
- Reverting a fix for a negative control via python replace is easy to get wrong when the call has an inline arg (`slice_codepoint_bounded(value, 512)` vs piped `|> slice_codepoint_bounded(64)`) — grep the file after the revert; the UA path survived my first revert and silently kept the fix.
