# righttenantry-refcheck-rc4-2 — field notes

- gleam 1.15.1 parser REJECTS `++ [list-literal]` ("operator has no value on its right side") — use `list.append`/spread; the repo never uses `++ [`.
- `decode.dict` fails on JSON arrays (they're `List(Dynamic)`); `list.last` returns Result; `list.filter_map` wants Result; the `type X` import prefix is per-item (bare name = constructor value only).
- `list.all([])` is vacuously True — emptiness must be checked BEFORE the all-terminal branch (the pre-trigger sub-line bug).
- The RC4.1 §8.1 payload had no form-open marker or completion timestamp — RC4.2's "Form opened"/"Reference received" states needed additive `form_opened_at`/`submitted_at` keys (expand-only, optional_field back-compat).
