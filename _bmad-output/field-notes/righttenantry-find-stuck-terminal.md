# righttenantry-find-stuck-terminal — field notes

- 2026-08-11: the backtick command-substitution trap hits `psql -c "..."` SQL **comments** too, not just `gh --body` heredocs — a `-- \`kind\` is...` comment inside the double-quoted `-c` arg got bash-substituted (`line N: kind: command not found` to stderr, query still ran). No backticks anywhere inside a `-c "..."` string, comments included.
- 2026-08-11: `gh pr create --body-file <path>` errors `open ...: no such file or directory` if you drop the extension by reflex — the file exists, you just named it wrong. Pass the real filename.
- 2026-08-11: macOS `grep` has no `-P` (perl-regex) — to find non-ASCII / specific codepoints use `perl -CSD -ne '... \x{2014} ...'`; the plain-byte form silently misses multibyte chars (first check wrongly said "0 em-dashes", `-CSD` found the U+2014 I'd added).
