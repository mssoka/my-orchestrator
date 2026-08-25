# Field notes — refcheck-followup-607

- macOS grep has no -P/\x{2014}; for em-dash archaeology use `rg -l '"[^"]*—'` (ripgrep handles UTF-8) then a python comment-stripping pass to separate real string-literal em-dashes from comments — the raw grep flags ~70 files that are comment-only.
- The em-dash ban lint must skip dev-facing `wisp.log_*` arguments (they legitimately carry em-dashes) and `client/src/copy.gleam` (spec-verbatim home); scope = user-facing view/composition modules. A YAML step NAME with an unquoted colon (`AR-RC13: ...`) breaks the workflow parser — quote it.
- Item 3 (timeline format-mix sort) was already fixed+pinned server-side by RC4.4 (`attempt_log_appends_lifecycle_events_test` + `normalize_at` before sort); verify-and-strengthen is the honest delivery — add the inverted-mix fixture (space-form attempt `at`) rather than duplicating the canonical one.
- `git checkout -- <file>` to restore a lint negative-control is fine, but it wipes your OTHER edits in that file — re-apply them in one python replace pass, then `grep -c '" — "'` to prove the composition sites are gone.
