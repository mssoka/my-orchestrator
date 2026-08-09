# righttenantry-form-copy-revision — field notes

- User-ruled verbatim copy + GLOBAL em-dash ban: the acceptance grep must be run over non-comment code lines (indented comments defeat a naive `rg -v '^\s*//'`) — and "user-facing" excludes logs/SQL comments, which is what the 85 surviving server literal `—` hits all are.
- The client copy_test sentence-count pins (≤2 by terminal punctuation) silently constrain dash replacements — sentence breaks can trip them; colon/comma substitutions keep the budget. Case-sensitive `string.contains` also breaks on sentence-initial capitals.
- `edit` tool batches are atomic per call AND per file — a cross-file batch fails wholesale on the first mismatch, and dropping a trailing `,` from oldText leaves `",,"` doubles; perl `s/",,",/"` rescued all five.
