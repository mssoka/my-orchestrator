# Field notes — righttenantry-agents-wif-durable

- 2026-09-06: `herdr wait agent-status` doesn't exist in this CLI build — use `herdr agent wait <pane> --until idle --timeout N` (and `pane run` for prompts).
- 2026-09-06: invariant tests asserting on `_resource_block` output must strip WHOLE-LINE comments (`^\s*#` + MULTILINE) — comment prose inside a tf resource block can satisfy substring asserts (masked a real condition regression in my first draft); unanchored `#[^\n]*` corrupts HCL strings containing '#'.
- 2026-09-06: PR-branch lint (ruff F541) runs in pre-commit AFTER your message-drafting — run `uv run ruff check` on touched test files before committing; f-strings without placeholders (even with `{{}}` escapes) fail the hook and force an amend dance.
