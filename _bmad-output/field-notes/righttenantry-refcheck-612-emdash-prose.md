# Field notes — righttenantry-refcheck-612-emdash-prose

Job: #612 — em-dash exemptions removed; 15 spec-verbatim strings re-composed dash-free; lint boundary hardened.

- Issue title said "16 exemptions" but the lint set and the issue's own table both had 15 — count from the CODE (`SPEC_VERBATIM_OWNERS`), not the title, and say so in the PR.
- The lint only scanned raw U+2014 bytes — a Gleam literal `"\u{2014}"` (escape form) compiled to the same char and PASSED. Escape-form detection must be escape-aware (even backslash run = real escape; `\\u{2014}` literal text is not a dash). Prove with positive AND escaped-backslash negative controls.
- Widening `SERVER_INCLUDE` surfaces latent violations in files that were never scanned (log-only helper strings in `document_upload.gleam`); re-word the log strings dash-free rather than leave a scope claim that's false — and watch the Python docstring: writing `\u{2014}` inside it is a SyntaxError, use a raw string.
